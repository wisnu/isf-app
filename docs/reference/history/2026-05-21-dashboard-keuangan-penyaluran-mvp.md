# Dashboard Keuangan & Penyaluran MVP — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ganti dummy dashboard data dengan query nyata dari DB dan tambah dua halaman operasional: Dashboard Keuangan (KPI + trend + anggaran + rekening) dan Dashboard Penyaluran (KPI + anggaran + memo terbaru).

**Architecture:** Backend api-python mendapat dua endpoint baru (`/dashboard/keuangan`, `/dashboard/penyaluran`) yang query langsung ke views `dashboard.v_*` dan table `transaction.*`/`program.*`. BFF proxy pass-through. Frontend dua halaman baru dengan shared components `BudgetProgress.vue`, `RekeningList.vue`, `MemoList.vue`, dan `PeriodFilter.vue`.

**Tech Stack:** FastAPI + asyncpg (api-python), httpx (bff-api), Vue 3 + Tailwind v4 + shadcn-ui (web-vue), PostgreSQL views (`dashboard.v_ashnaf_bymonthyear`, `v_budget_bymonthyear`, `v_dist_monthyear_byproduct`, `v_fund_monthyear_bycash`).

---

## File Map

### apps_zakat/api-python
| File | Aksi |
|---|---|
| `app/modules/dashboard/schema.py` | Tambah schema baru (tidak hapus yang lama) |
| `app/modules/dashboard/service.py` | Tambah fungsi query real DB |
| `app/modules/dashboard/router.py` | Tambah 2 endpoint baru |

### apps_zakat/bff-api
| File | Aksi |
|---|---|
| `app/routers/dashboard.py` | Tambah 2 proxy route baru |

### apps_zakat/web-vue/src
| File | Aksi |
|---|---|
| `components/ui/PeriodFilter.vue` | Baru — bulan/tahun dropdowns |
| `components/widgets/BudgetProgress.vue` | Baru — progress bar anggaran per program |
| `components/widgets/RekeningList.vue` | Baru — tabel saldo rekening |
| `components/widgets/MemoList.vue` | Baru — tabel 5 memo terbaru |
| `pages/DashboardKeuanganPage.vue` | Baru — halaman dashboard keuangan |
| `pages/DashboardPenyaluranPage.vue` | Baru — halaman dashboard penyaluran |
| `router/index.ts` | Tambah 2 route baru |
| `components/AppSidebar.vue` | Tambah 2 nav entry |

---

## Task 1 — Backend: Tambah schema baru di schema.py

**Files:**
- Modify: `apps_zakat/api-python/app/modules/dashboard/schema.py`

- [ ] **Step 1: Append schema baru ke akhir file**

Buka `apps_zakat/api-python/app/modules/dashboard/schema.py` dan append setelah class `DashboardSummary`:

```python
# ── Schema v2 — real-data endpoints ──────────────────────────────────────────

class KpiCardData(BaseModel):
    total: float
    delta_pct: float | None = None   # None = tidak ada data bulan lalu
    format: str = "currency"         # "currency" | "count"


class AsnafItem2(BaseModel):
    label: str
    count: int


class TrendPoint(BaseModel):
    label: str        # "2026-01"
    penerimaan: float
    penyaluran: float


class AnggaranItem(BaseModel):
    owner_id: int
    owner_name: str
    anggaran: float
    realisasi: float
    pct: float        # realisasi / anggaran * 100, capped at 999


class RekeningItem(BaseModel):
    account_no: str
    account_name: str
    account_type: str        # "Bank" | "Kas Besar" | "Kas Kecil" | "Lainnya"
    bank_name: str | None
    balance: float


class MemoItem(BaseModel):
    memo_id: int
    memo_number: str | None
    subject: str | None
    amount: float | None
    memo_type: str          # "R" = Rutin, "N" = Non Rutin
    memo_date: str | None   # "YYYY-MM-DD"


class DashboardKeuangan(BaseModel):
    period: str             # "2026-05"
    kpis: dict[str, KpiCardData]
    trend: list[TrendPoint]
    asnaf: list[AsnafItem2]
    anggaran: list[AnggaranItem]
    rekening: list[RekeningItem]


class DashboardPenyaluran(BaseModel):
    period: str
    kpis: dict[str, KpiCardData]
    anggaran: list[AnggaranItem]
    memo_terbaru: list[MemoItem]
```

- [ ] **Step 2: Verifikasi import tidak rusak**

```bash
cd /media/win_d/workshop/isf-app/apps_zakat/api-python
python -c "from app.modules.dashboard.schema import DashboardKeuangan, DashboardPenyaluran; print('OK')"
```

Expected: `OK`

---

## Task 2 — Backend: Tambah fungsi DB di service.py

**Files:**
- Modify: `apps_zakat/api-python/app/modules/dashboard/service.py`

DB views yang tersedia:
- `dashboard.v_fund_monthyear_bycash` — kolom: `fund_month`, `fund_year`, `accountno`, `accountname`, `fund_amount`
- `dashboard.v_dist_monthyear_byproduct` — kolom: `dist_month`, `dist_year`, `accountno`, `accountname`, `productname`, `dist_amount`
- `dashboard.v_ashnaf_bymonthyear` — kolom: `realization_month`, `realization_year`, `ashnaf_name`, `count_ashnaf`
- `dashboard.v_budget_bymonthyear` — kolom: `budget_month`, `budget_year`, `ownerid`, `ownername`, `budget_amount`, `budget_realization`
- `transaction.cashaccountall` (view) — kolom: `accountno`, `accountname`, `balance`, `status`, `bankname`, `cashaccounttype`
- `transaction.transaction` — `authstatus = 'O'` untuk pending otorisasi
- `program.realizationmemo` — `realmemoid`, `realmemonumber`, `realmemosubject`, `realmemoamount`, `realizationmemotype`, `realmemodate`

- [ ] **Step 1: Ganti isi service.py sepenuhnya**

```python
"""Dashboard service — gabungan dummy (summary lama) dan real-DB (v2)."""

from __future__ import annotations

from datetime import date

from app.modules.dashboard.schema import (
    # Legacy
    AsnafItem, Channel, DashboardSummary, Kpis, KpiPair, Trend, Transaction,
    # v2
    AnggaranItem, AsnafItem2, DashboardKeuangan, DashboardPenyaluran,
    KpiCardData, MemoItem, RekeningItem, TrendPoint,
)
from app.shared.db import fetch_all, fetch_one, ping


# ── Helpers ──────────────────────────────────────────────────────────────────

def _prev_month(bulan: int, tahun: int) -> tuple[int, int]:
    if bulan == 1:
        return 12, tahun - 1
    return bulan - 1, tahun


def _last_6_months(bulan: int, tahun: int) -> list[tuple[int, int]]:
    """Returns [(month, year), ...] oldest→newest, length 6."""
    result = []
    for i in range(5, -1, -1):
        m = bulan - i
        y = tahun
        while m <= 0:
            m += 12
            y -= 1
        result.append((m, y))
    return result


def _pct(realisasi: float, anggaran: float) -> float:
    if anggaran <= 0:
        return 0.0
    return min(999.0, round(realisasi / anggaran * 100, 1))


_CASHTYPE_LABEL: dict[str, str] = {
    "B": "Bank",
    "G": "Kas Besar",
    "K": "Kas Kecil",
}


# ── Real-DB query functions ───────────────────────────────────────────────────

async def _sum_fund(bulan: int, tahun: int) -> float:
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(fund_amount), 0) AS total
        FROM dashboard.v_fund_monthyear_bycash
        WHERE fund_month = $1 AND fund_year = $2
        """,
        bulan, tahun,
    )
    return float(row["total"]) if row else 0.0


async def _sum_dist(bulan: int, tahun: int) -> float:
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(dist_amount), 0) AS total
        FROM dashboard.v_dist_monthyear_byproduct
        WHERE dist_month = $1 AND dist_year = $2
        """,
        bulan, tahun,
    )
    return float(row["total"]) if row else 0.0


async def _saldo_total() -> float:
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(balance), 0) AS total
        FROM transaction.cashaccountall
        WHERE status = 'A'
        """
    )
    return float(row["total"]) if row else 0.0


async def _otorisasi_pending() -> int:
    row = await fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM transaction.transaction
        WHERE authstatus = 'O'
        """
    )
    return int(row["total"]) if row else 0


async def _kpi_card(current: float, prev: float, fmt: str = "currency") -> KpiCardData:
    if prev > 0:
        delta = round((current - prev) / prev * 100, 1)
    else:
        delta = None
    return KpiCardData(total=current, delta_pct=delta, format=fmt)


async def _trend_6bulan(bulan: int, tahun: int) -> list[TrendPoint]:
    months = _last_6_months(bulan, tahun)
    points: list[TrendPoint] = []
    for m, y in months:
        fund = await _sum_fund(m, y)
        dist = await _sum_dist(m, y)
        points.append(TrendPoint(label=f"{y}-{m:02d}", penerimaan=fund, penyaluran=dist))
    return points


async def _asnaf_dist(bulan: int, tahun: int) -> list[AsnafItem2]:
    rows = await fetch_all(
        """
        SELECT ashnaf_name AS label, COALESCE(SUM(count_ashnaf), 0)::int AS cnt
        FROM dashboard.v_ashnaf_bymonthyear
        WHERE realization_month = $1 AND realization_year = $2
        GROUP BY ashnaf_name
        ORDER BY cnt DESC
        """,
        bulan, tahun,
    )
    return [AsnafItem2(label=r["label"], count=r["cnt"]) for r in rows]


async def _anggaran_list(tahun: int) -> list[AnggaranItem]:
    rows = await fetch_all(
        """
        SELECT
            ownerid,
            ownername,
            SUM(budget_amount)                          AS anggaran,
            SUM(COALESCE(budget_realization, 0))        AS realisasi
        FROM dashboard.v_budget_bymonthyear
        WHERE budget_year = $1
        GROUP BY ownerid, ownername
        ORDER BY anggaran DESC
        LIMIT 8
        """,
        tahun,
    )
    result: list[AnggaranItem] = []
    for r in rows:
        ang = float(r["anggaran"] or 0)
        real = float(r["realisasi"] or 0)
        result.append(AnggaranItem(
            owner_id=r["ownerid"],
            owner_name=r["ownername"] or "–",
            anggaran=ang,
            realisasi=real,
            pct=_pct(real, ang),
        ))
    return result


async def _rekening_list() -> list[RekeningItem]:
    rows = await fetch_all(
        """
        SELECT
            accountno, accountname,
            cashaccounttype,
            bankname,
            balance
        FROM transaction.cashaccountall
        WHERE status = 'A'
        ORDER BY
            CASE cashaccounttype WHEN 'B' THEN 1 WHEN 'G' THEN 2 ELSE 3 END,
            accountname
        """
    )
    return [
        RekeningItem(
            account_no=r["accountno"],
            account_name=r["accountname"] or "–",
            account_type=_CASHTYPE_LABEL.get(r["cashaccounttype"] or "", "Lainnya"),
            bank_name=r["bankname"],
            balance=float(r["balance"] or 0),
        )
        for r in rows
    ]


async def _memo_terbaru() -> list[MemoItem]:
    rows = await fetch_all(
        """
        SELECT
            realmemoid, realmemonumber, realmemosubject,
            realmemoamount, realizationmemotype,
            TO_CHAR(realmemodate, 'YYYY-MM-DD') AS memo_date
        FROM program.realizationmemo
        ORDER BY realmemodate DESC NULLS LAST
        LIMIT 5
        """
    )
    return [
        MemoItem(
            memo_id=r["realmemoid"],
            memo_number=r["realmemonumber"],
            subject=r["realmemosubject"],
            amount=float(r["realmemoamount"]) if r["realmemoamount"] is not None else None,
            memo_type=r["realizationmemotype"] or "N",
            memo_date=r["memo_date"],
        )
        for r in rows
    ]


async def _mustahiq_count(bulan: int, tahun: int) -> int:
    """Approx: sum count_ashnaf from distribution view for the period."""
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(count_ashnaf), 0)::int AS total
        FROM dashboard.v_ashnaf_bymonthyear
        WHERE realization_month = $1 AND realization_year = $2
        """,
        bulan, tahun,
    )
    return int(row["total"]) if row else 0


# ── Public API ────────────────────────────────────────────────────────────────

async def get_keuangan(bulan: int, tahun: int) -> DashboardKeuangan | None:
    if not await ping():
        return None

    prev_m, prev_y = _prev_month(bulan, tahun)

    cur_fund   = await _sum_fund(bulan, tahun)
    prev_fund  = await _sum_fund(prev_m, prev_y)
    cur_dist   = await _sum_dist(bulan, tahun)
    prev_dist  = await _sum_dist(prev_m, prev_y)
    saldo      = await _saldo_total()
    otorisasi  = await _otorisasi_pending()

    return DashboardKeuangan(
        period=f"{tahun}-{bulan:02d}",
        kpis={
            "penerimaan": await _kpi_card(cur_fund, prev_fund),
            "penyaluran": await _kpi_card(cur_dist, prev_dist),
            "saldo": KpiCardData(total=saldo, format="currency"),
            "otorisasi_pending": KpiCardData(total=otorisasi, format="count"),
        },
        trend=await _trend_6bulan(bulan, tahun),
        asnaf=await _asnaf_dist(bulan, tahun),
        anggaran=await _anggaran_list(tahun),
        rekening=await _rekening_list(),
    )


async def get_penyaluran(bulan: int, tahun: int) -> DashboardPenyaluran | None:
    if not await ping():
        return None

    prev_m, prev_y = _prev_month(bulan, tahun)

    cur_dist  = await _sum_dist(bulan, tahun)
    prev_dist = await _sum_dist(prev_m, prev_y)
    mustahiq  = await _mustahiq_count(bulan, tahun)
    otorisasi = await _otorisasi_pending()

    return DashboardPenyaluran(
        period=f"{tahun}-{bulan:02d}",
        kpis={
            "penyaluran": await _kpi_card(cur_dist, prev_dist),
            "mustahiq": KpiCardData(total=mustahiq, format="count"),
            "otorisasi_pending": KpiCardData(total=otorisasi, format="count"),
        },
        anggaran=await _anggaran_list(tahun),
        memo_terbaru=await _memo_terbaru(),
    )


# ── Legacy dummy (kept for existing /summary endpoint) ───────────────────────

_DUMMY: dict[str, DashboardSummary] = {
    "perusahaan_a": DashboardSummary(
        tenant_id="perusahaan_a",
        tenant_name="Lembaga ZISWAF A",
        period="2026-05",
        kpis=Kpis(
            penerimaan=KpiPair(total=1_250_000_000, delta_pct=12.4),
            penyaluran=KpiPair(total=875_000_000, delta_pct=-3.2),
            saldo=KpiPair(total=4_800_000_000, delta_pct=8.1),
            donatur_baru=KpiPair(total=142, delta_pct=21.5),
        ),
        trend=Trend(
            labels=["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
            penerimaan=[820_000_000, 905_000_000, 980_000_000, 1_100_000_000, 1_112_000_000, 1_250_000_000],
            penyaluran=[610_000_000, 680_000_000, 740_000_000, 810_000_000, 905_000_000, 875_000_000],
        ),
        asnaf_distribution=[
            AsnafItem(label="Fakir", amount=245_000_000),
            AsnafItem(label="Miskin", amount=198_000_000),
            AsnafItem(label="Amil", amount=87_500_000),
            AsnafItem(label="Mualaf", amount=52_000_000),
            AsnafItem(label="Riqab", amount=0),
            AsnafItem(label="Gharimin", amount=78_000_000),
            AsnafItem(label="Fi Sabilillah", amount=132_000_000),
            AsnafItem(label="Ibnu Sabil", amount=82_500_000),
        ],
        fundraising_channels=[
            Channel(label="Transfer Bank", actual=720_000_000, target=800_000_000),
            Channel(label="Gerai & Booth", actual=240_000_000, target=200_000_000),
            Channel(label="Payroll", actual=180_000_000, target=250_000_000),
            Channel(label="E-Wallet", actual=110_000_000, target=150_000_000),
        ],
        recent_transactions=[
            Transaction(id="tx_a01", date="2026-05-19", type="Zakat Mal", channel="Transfer Bank", amount=15_000_000, donor="Budi Santoso"),
            Transaction(id="tx_a02", date="2026-05-19", type="Infaq", channel="E-Wallet", amount=250_000, donor="Siti Aminah"),
        ],
    ),
    "perusahaan_b": DashboardSummary(
        tenant_id="perusahaan_b",
        tenant_name="Lembaga ZISWAF B",
        period="2026-05",
        kpis=Kpis(
            penerimaan=KpiPair(total=920_000_000, delta_pct=6.8),
            penyaluran=KpiPair(total=640_000_000, delta_pct=14.2),
            saldo=KpiPair(total=2_950_000_000, delta_pct=4.5),
            donatur_baru=KpiPair(total=89, delta_pct=-5.3),
        ),
        trend=Trend(
            labels=["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
            penerimaan=[640_000_000, 715_000_000, 760_000_000, 820_000_000, 861_000_000, 920_000_000],
            penyaluran=[420_000_000, 480_000_000, 525_000_000, 580_000_000, 560_000_000, 640_000_000],
        ),
        asnaf_distribution=[
            AsnafItem(label="Fakir", amount=178_000_000),
            AsnafItem(label="Miskin", amount=152_000_000),
        ],
        fundraising_channels=[
            Channel(label="Transfer Bank", actual=520_000_000, target=600_000_000),
        ],
        recent_transactions=[
            Transaction(id="tx_b01", date="2026-05-19", type="Infaq", channel="E-Wallet", amount=500_000, donor="Dewi Lestari"),
        ],
    ),
}


def get_summary(tenant_id: str) -> DashboardSummary | None:
    return _DUMMY.get(tenant_id)
```

- [ ] **Step 2: Verifikasi import tidak rusak**

```bash
cd /media/win_d/workshop/isf-app/apps_zakat/api-python
python -c "from app.modules.dashboard.service import get_keuangan, get_penyaluran; print('OK')"
```

Expected: `OK`

---

## Task 3 — Backend: Tambah 2 endpoint di router.py

**Files:**
- Modify: `apps_zakat/api-python/app/modules/dashboard/router.py`

- [ ] **Step 1: Ganti isi router.py**

```python
from datetime import date

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.dashboard.service import get_keuangan, get_penyaluran, get_summary
from app.shared.response import err, ok

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

_THIS_MONTH = date.today().month
_THIS_YEAR  = date.today().year


@router.get("/summary")
def summary(tenant_id: str):
    data = get_summary(tenant_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=err("TENANT_NOT_FOUND", f"Tenant '{tenant_id}' not found"),
        )
    return ok(data.model_dump())


@router.get("/keuangan")
async def keuangan(
    bulan: int = Query(default=_THIS_MONTH, ge=1, le=12),
    tahun: int = Query(default=_THIS_YEAR, ge=2000, le=2100),
):
    data = await get_keuangan(bulan, tahun)
    if data is None:
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database not reachable"),
        )
    return ok(data.model_dump())


@router.get("/penyaluran")
async def penyaluran(
    bulan: int = Query(default=_THIS_MONTH, ge=1, le=12),
    tahun: int = Query(default=_THIS_YEAR, ge=2000, le=2100),
):
    data = await get_penyaluran(bulan, tahun)
    if data is None:
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database not reachable"),
        )
    return ok(data.model_dump())
```

- [ ] **Step 2: Test endpoint via curl (api-python direct)**

```bash
curl -s "http://localhost:8000/api/v1/dashboard/keuangan?bulan=5&tahun=2026" | python3 -m json.tool | head -30
```

Expected: JSON dengan `"status": "ok"` dan field `period`, `kpis`, `trend`, `asnaf`, `anggaran`, `rekening`.

Jika DB tidak tersedia: `{"status":"error","code":"DB_UNAVAILABLE",...}` — normal, lanjut.

- [ ] **Step 3: Commit backend**

```bash
cd /media/win_d/workshop/isf-app
git add apps_zakat/api-python/app/modules/dashboard/
git commit -m "feat(dashboard): add real-data keuangan & penyaluran endpoints"
```

---

## Task 4 — BFF: Tambah proxy route keuangan & penyaluran

**Files:**
- Modify: `apps_zakat/bff-api/app/routers/dashboard.py`

- [ ] **Step 1: Ganti isi file**

```python
from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401
from app.services.proxy import get_api_python
from app.shared.response import err

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

_THIS_MONTH = date.today().month
_THIS_YEAR  = date.today().year


async def _require_auth(request: Request):
    """Returns (None, error_response) or (user_id, None)."""
    uid, error = await current_user_id_or_401(request)
    return uid, error


@router.get("/summary")
async def summary(request: Request):
    _, error = await _require_auth(request)
    if error:
        return error

    active_tenant = request.session.get("active_tenant_id")
    if not active_tenant:
        return JSONResponse(status_code=403, content=err("NO_TENANT", "No active tenant"))

    downstream = await get_api_python(
        "/api/v1/dashboard/summary", params={"tenant_id": active_tenant}
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/keuangan")
async def keuangan(
    request: Request,
    bulan: int = Query(default=_THIS_MONTH, ge=1, le=12),
    tahun: int = Query(default=_THIS_YEAR, ge=2000, le=2100),
):
    _, error = await _require_auth(request)
    if error:
        return error

    downstream = await get_api_python(
        "/api/v1/dashboard/keuangan",
        params={"bulan": bulan, "tahun": tahun},
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/penyaluran")
async def penyaluran(
    request: Request,
    bulan: int = Query(default=_THIS_MONTH, ge=1, le=12),
    tahun: int = Query(default=_THIS_YEAR, ge=2000, le=2100),
):
    _, error = await _require_auth(request)
    if error:
        return error

    downstream = await get_api_python(
        "/api/v1/dashboard/penyaluran",
        params={"bulan": bulan, "tahun": tahun},
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
```

- [ ] **Step 2: Verifikasi syntax**

```bash
cd /media/win_d/workshop/isf-app/apps_zakat/bff-api
python -c "from app.routers.dashboard import router; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd /media/win_d/workshop/isf-app
git add apps_zakat/bff-api/app/routers/dashboard.py
git commit -m "feat(bff): proxy keuangan & penyaluran dashboard routes"
```

---

## Task 5 — Frontend: PeriodFilter.vue

**Files:**
- Create: `apps_zakat/web-vue/src/components/ui/PeriodFilter.vue`

- [ ] **Step 1: Buat file**

```vue
<script setup lang="ts">
const props = defineProps<{
  modelBulan: number
  modelTahun: number
}>()

const emit = defineEmits<{
  'update:modelBulan': [number]
  'update:modelTahun': [number]
}>()

const BULAN = [
  { v: 1, l: 'Januari' }, { v: 2, l: 'Februari' }, { v: 3, l: 'Maret' },
  { v: 4, l: 'April' },   { v: 5, l: 'Mei' },       { v: 6, l: 'Juni' },
  { v: 7, l: 'Juli' },    { v: 8, l: 'Agustus' },   { v: 9, l: 'September' },
  { v: 10, l: 'Oktober' },{ v: 11, l: 'November' }, { v: 12, l: 'Desember' },
]

const now = new Date()
const TAHUN = Array.from({ length: 5 }, (_, i) => now.getFullYear() - 2 + i)
</script>

<template>
  <div class="flex items-center gap-2 flex-wrap">
    <select
      class="h-8 rounded-md border border-border bg-surface px-2 text-xs focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
      :value="modelBulan"
      @change="emit('update:modelBulan', Number(($event.target as HTMLSelectElement).value))"
    >
      <option v-for="b in BULAN" :key="b.v" :value="b.v">{{ b.l }}</option>
    </select>
    <select
      class="h-8 rounded-md border border-border bg-surface px-2 text-xs focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary"
      :value="modelTahun"
      @change="emit('update:modelTahun', Number(($event.target as HTMLSelectElement).value))"
    >
      <option v-for="y in TAHUN" :key="y" :value="y">{{ y }}</option>
    </select>
  </div>
</template>
```

---

## Task 6 — Frontend: BudgetProgress.vue

**Files:**
- Create: `apps_zakat/web-vue/src/components/widgets/BudgetProgress.vue`

Warna threshold sesuai PRD: 0–50% abu, 51–80% biru, 81–95% amber, >95% merah.

- [ ] **Step 1: Buat file**

```vue
<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'

interface AnggaranItem {
  owner_id: number
  owner_name: string
  anggaran: number
  realisasi: number
  pct: number
}

defineProps<{ items: AnggaranItem[]; title?: string }>()

function barClass(pct: number): string {
  if (pct > 95) return 'bg-destructive'
  if (pct > 80) return 'bg-warning'
  if (pct > 50) return 'bg-primary'
  return 'bg-muted'
}

function barWidth(pct: number): string {
  return Math.min(100, pct) + '%'
}

function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency', currency: 'IDR', maximumFractionDigits: 0,
  }).format(n)
}
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>{{ title ?? 'Realisasi Anggaran' }}</CardTitle>
      <CardDescription>Serapan anggaran per program · tahun berjalan</CardDescription>
    </CardHeader>
    <CardContent class="space-y-4">
      <div v-if="!items.length" class="text-xs text-muted text-center py-4">
        Tidak ada data anggaran
      </div>
      <div v-for="item in items" :key="item.owner_id" class="space-y-1.5">
        <div class="flex items-baseline justify-between gap-2">
          <span class="text-xs font-medium truncate max-w-[60%]">{{ item.owner_name }}</span>
          <span
            class="text-xs tabular-nums font-semibold shrink-0"
            :class="{
              'text-destructive': item.pct > 95,
              'text-warning': item.pct > 80 && item.pct <= 95,
              'text-primary': item.pct > 50 && item.pct <= 80,
              'text-muted': item.pct <= 50,
            }"
          >{{ item.pct.toFixed(1) }}%</span>
        </div>
        <div class="h-1.5 bg-background rounded-full overflow-hidden">
          <div
            class="h-full rounded-full transition-[width] duration-500"
            :class="barClass(item.pct)"
            :style="{ width: barWidth(item.pct) }"
          />
        </div>
        <div class="flex justify-between text-[10px] text-muted tabular-nums">
          <span>{{ formatIdr(item.realisasi) }}</span>
          <span>anggaran {{ formatIdr(item.anggaran) }}</span>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
```

---

## Task 7 — Frontend: RekeningList.vue

**Files:**
- Create: `apps_zakat/web-vue/src/components/widgets/RekeningList.vue`

- [ ] **Step 1: Buat file**

```vue
<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'

interface RekeningItem {
  account_no: string
  account_name: string
  account_type: string
  bank_name: string | null
  balance: number
}

const props = defineProps<{ items: RekeningItem[] }>()

const total = () => props.items.reduce((s, r) => s + r.balance, 0)

function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency', currency: 'IDR', maximumFractionDigits: 0,
  }).format(n)
}

function badgeClass(type: string): string {
  const m: Record<string, string> = {
    'Bank': 'bg-primary/10 text-primary',
    'Kas Besar': 'bg-positive/10 text-positive',
    'Kas Kecil': 'bg-warning/10 text-warning',
  }
  return m[type] ?? 'bg-muted/10 text-muted'
}
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>Saldo Rekening</CardTitle>
      <CardDescription>Semua rekening aktif</CardDescription>
    </CardHeader>
    <CardContent class="p-0">
      <div class="overflow-x-auto">
        <table class="w-full text-xs">
          <thead class="text-[10px] text-muted uppercase tracking-wide">
            <tr class="border-b border-border">
              <th class="text-left px-4 py-2 font-medium">Nama Rekening</th>
              <th class="text-left px-4 py-2 font-medium">Jenis</th>
              <th class="text-right px-4 py-2 font-medium">Saldo</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="r in items"
              :key="r.account_no"
              class="border-b border-border last:border-0 hover:bg-background/50"
            >
              <td class="px-4 py-1.5">
                <div class="font-medium truncate max-w-[180px]">{{ r.account_name }}</div>
                <div v-if="r.bank_name" class="text-[10px] text-muted">{{ r.bank_name }}</div>
              </td>
              <td class="px-4 py-1.5">
                <span :class="['rounded px-1.5 py-0.5 text-[10px] font-medium', badgeClass(r.account_type)]">
                  {{ r.account_type }}
                </span>
              </td>
              <td class="px-4 py-1.5 text-right tabular-nums font-medium">
                {{ formatIdr(r.balance) }}
              </td>
            </tr>
          </tbody>
          <tfoot class="border-t-2 border-border bg-background/50">
            <tr>
              <td colspan="2" class="px-4 py-2 text-xs font-semibold">Total</td>
              <td class="px-4 py-2 text-right text-xs font-bold tabular-nums">
                {{ formatIdr(total()) }}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
    </CardContent>
  </Card>
</template>
```

---

## Task 8 — Frontend: MemoList.vue

**Files:**
- Create: `apps_zakat/web-vue/src/components/widgets/MemoList.vue`

- [ ] **Step 1: Buat file**

```vue
<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'

interface MemoItem {
  memo_id: number
  memo_number: string | null
  subject: string | null
  amount: number | null
  memo_type: string    // "R" | "N"
  memo_date: string | null
}

defineProps<{ items: MemoItem[] }>()

function formatIdr(n: number | null): string {
  if (n === null) return '—'
  return new Intl.NumberFormat('id-ID', {
    style: 'currency', currency: 'IDR', maximumFractionDigits: 0,
  }).format(n)
}

function formatDate(s: string | null): string {
  if (!s) return '—'
  const d = new Date(s)
  return new Intl.DateTimeFormat('id-ID', { day: '2-digit', month: 'short', year: '2-digit' }).format(d)
}

function typeBadge(t: string) {
  return t === 'R'
    ? { label: 'Rutin', cls: 'bg-primary/10 text-primary' }
    : { label: 'Non Rutin', cls: 'bg-accent/10 text-accent' }
}
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>Memo Penyaluran Terbaru</CardTitle>
      <CardDescription>5 memo terakhir</CardDescription>
    </CardHeader>
    <CardContent class="p-0">
      <div v-if="!items.length" class="text-xs text-muted text-center py-6">
        Tidak ada memo
      </div>
      <div
        v-for="m in items"
        :key="m.memo_id"
        class="flex items-start justify-between gap-3 px-4 py-2.5 border-b border-border last:border-0 hover:bg-background/50"
      >
        <div class="min-w-0 flex-1">
          <div class="flex items-center gap-1.5 mb-0.5">
            <span :class="['rounded px-1.5 py-0.5 text-[10px] font-medium shrink-0', typeBadge(m.memo_type).cls]">
              {{ typeBadge(m.memo_type).label }}
            </span>
            <span class="text-[10px] text-muted tabular-nums">{{ m.memo_number ?? '–' }}</span>
          </div>
          <div class="text-xs font-medium truncate">{{ m.subject ?? '–' }}</div>
          <div class="text-[10px] text-muted">{{ formatDate(m.memo_date) }}</div>
        </div>
        <div class="text-xs font-semibold tabular-nums shrink-0 text-right">
          {{ formatIdr(m.amount) }}
        </div>
      </div>
    </CardContent>
  </Card>
</template>
```

---

## Task 9 — Frontend: DashboardKeuanganPage.vue

**Files:**
- Create: `apps_zakat/web-vue/src/pages/DashboardKeuanganPage.vue`

- [ ] **Step 1: Buat file**

```vue
<script setup lang="ts">
import { Loader2, RefreshCw } from 'lucide-vue-next'
import { ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import AsnafDonut from '@/components/widgets/AsnafDonut.vue'
import BudgetProgress from '@/components/widgets/BudgetProgress.vue'
import KpiCard from '@/components/widgets/KpiCard.vue'
import RekeningList from '@/components/widgets/RekeningList.vue'
import TrendChart from '@/components/widgets/TrendChart.vue'
import { api, ApiError } from '@/lib/api/client'

interface KpiCardData { total: number; delta_pct: number | null; format: string }
interface TrendPoint { label: string; penerimaan: number; penyaluran: number }
interface AsnafItem2 { label: string; count: number }
interface AnggaranItem { owner_id: number; owner_name: string; anggaran: number; realisasi: number; pct: number }
interface RekeningItem { account_no: string; account_name: string; account_type: string; bank_name: string | null; balance: number }

interface Payload {
  period: string
  kpis: Record<string, KpiCardData>
  trend: TrendPoint[]
  asnaf: AsnafItem2[]
  anggaran: AnggaranItem[]
  rekening: RekeningItem[]
}

const now = new Date()
const bulan = ref(now.getMonth() + 1)
const tahun = ref(now.getFullYear())

const data = ref<Payload | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const lastUpdated = ref<string | null>(null)

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<Payload>(
      `/api/dashboard/keuangan?bulan=${bulan.value}&tahun=${tahun.value}`
    )
    lastUpdated.value = new Date().toLocaleTimeString('id-ID')
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat dashboard keuangan'
    data.value = null
  } finally {
    loading.value = false
  }
}

watch([bulan, tahun], load, { immediate: true })

// Helpers untuk bridge AsnafDonut (expects {label, amount})
function asnafToDonut(items: AsnafItem2[]) {
  return items.map(a => ({ label: a.label, amount: a.count }))
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold tracking-tight">Dashboard Keuangan</h1>
        <p v-if="lastUpdated" class="text-[11px] text-muted">Terakhir diperbarui: {{ lastUpdated }}</p>
      </div>
      <div class="flex items-center gap-2">
        <PeriodFilter v-model:model-bulan="bulan" v-model:model-tahun="tahun" />
        <button
          class="h-8 w-8 rounded-md border border-border bg-surface grid place-items-center hover:bg-background disabled:opacity-50"
          :disabled="loading"
          @click="load"
        >
          <RefreshCw class="w-3.5 h-3.5" :class="loading ? 'animate-spin' : ''" />
        </button>
      </div>
    </div>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <div v-if="loading && !data" class="flex justify-center py-16">
      <Loader2 class="w-8 h-8 animate-spin text-primary" />
    </div>

    <template v-else-if="data">
      <!-- Row 1: KPI cards -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
        <KpiCard
          label="Penerimaan"
          :amount="data.kpis.penerimaan.total"
          :delta-pct="data.kpis.penerimaan.delta_pct ?? 0"
        />
        <KpiCard
          label="Penyaluran"
          :amount="data.kpis.penyaluran.total"
          :delta-pct="data.kpis.penyaluran.delta_pct ?? 0"
        />
        <KpiCard
          label="Saldo Kas/Bank"
          :amount="data.kpis.saldo.total"
          :delta-pct="0"
        />
        <KpiCard
          label="Belum Otorisasi"
          :amount="data.kpis.otorisasi_pending.total"
          :delta-pct="0"
          format="count"
        />
      </div>

      <!-- Row 2: Trend + Asnaf -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-3">
        <div class="lg:col-span-2">
          <TrendChart
            :labels="data.trend.map(t => t.label)"
            :penerimaan="data.trend.map(t => t.penerimaan)"
            :penyaluran="data.trend.map(t => t.penyaluran)"
          />
        </div>
        <AsnafDonut :items="asnafToDonut(data.asnaf)" />
      </div>

      <!-- Row 3: Anggaran + Rekening -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
        <BudgetProgress :items="data.anggaran" />
        <RekeningList :items="data.rekening" />
      </div>
    </template>
  </div>
</template>
```

---

## Task 10 — Frontend: DashboardPenyaluranPage.vue

**Files:**
- Create: `apps_zakat/web-vue/src/pages/DashboardPenyaluranPage.vue`

- [ ] **Step 1: Buat file**

```vue
<script setup lang="ts">
import { Loader2, RefreshCw } from 'lucide-vue-next'
import { ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import BudgetProgress from '@/components/widgets/BudgetProgress.vue'
import KpiCard from '@/components/widgets/KpiCard.vue'
import MemoList from '@/components/widgets/MemoList.vue'
import { api, ApiError } from '@/lib/api/client'

interface KpiCardData { total: number; delta_pct: number | null; format: string }
interface AnggaranItem { owner_id: number; owner_name: string; anggaran: number; realisasi: number; pct: number }
interface MemoItem { memo_id: number; memo_number: string | null; subject: string | null; amount: number | null; memo_type: string; memo_date: string | null }

interface Payload {
  period: string
  kpis: Record<string, KpiCardData>
  anggaran: AnggaranItem[]
  memo_terbaru: MemoItem[]
}

const now = new Date()
const bulan = ref(now.getMonth() + 1)
const tahun = ref(now.getFullYear())

const data = ref<Payload | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const lastUpdated = ref<string | null>(null)

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<Payload>(
      `/api/dashboard/penyaluran?bulan=${bulan.value}&tahun=${tahun.value}`
    )
    lastUpdated.value = new Date().toLocaleTimeString('id-ID')
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat dashboard penyaluran'
    data.value = null
  } finally {
    loading.value = false
  }
}

watch([bulan, tahun], load, { immediate: true })
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-xl font-bold tracking-tight">Dashboard Penyaluran</h1>
        <p v-if="lastUpdated" class="text-[11px] text-muted">Terakhir diperbarui: {{ lastUpdated }}</p>
      </div>
      <div class="flex items-center gap-2">
        <PeriodFilter v-model:model-bulan="bulan" v-model:model-tahun="tahun" />
        <button
          class="h-8 w-8 rounded-md border border-border bg-surface grid place-items-center hover:bg-background disabled:opacity-50"
          :disabled="loading"
          @click="load"
        >
          <RefreshCw class="w-3.5 h-3.5" :class="loading ? 'animate-spin' : ''" />
        </button>
      </div>
    </div>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <div v-if="loading && !data" class="flex justify-center py-16">
      <Loader2 class="w-8 h-8 animate-spin text-primary" />
    </div>

    <template v-else-if="data">
      <!-- Row 1: KPI cards -->
      <div class="grid grid-cols-2 lg:grid-cols-3 gap-3">
        <KpiCard
          label="Total Penyaluran"
          :amount="data.kpis.penyaluran.total"
          :delta-pct="data.kpis.penyaluran.delta_pct ?? 0"
        />
        <KpiCard
          label="Mustahiq Terlayani"
          :amount="data.kpis.mustahiq.total"
          :delta-pct="0"
          format="count"
        />
        <KpiCard
          label="Belum Otorisasi"
          :amount="data.kpis.otorisasi_pending.total"
          :delta-pct="0"
          format="count"
        />
      </div>

      <!-- Row 2: Anggaran + Memo -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
        <BudgetProgress :items="data.anggaran" title="Realisasi vs Anggaran Penyaluran" />
        <MemoList :items="data.memo_terbaru" />
      </div>
    </template>
  </div>
</template>
```

---

## Task 11 — Frontend: Router + Sidebar

**Files:**
- Modify: `apps_zakat/web-vue/src/router/index.ts`
- Modify: `apps_zakat/web-vue/src/components/AppSidebar.vue`

- [ ] **Step 1: Tambah 2 route di router/index.ts**

Cari blok routes array, tambah setelah entry `keuangan-coa`:

```typescript
    {
      path: '/dashboard/keuangan',
      name: 'dashboard-keuangan',
      component: () => import('@/pages/DashboardKeuanganPage.vue'),
      meta: { title: 'Dashboard Keuangan' },
    },
    {
      path: '/dashboard/penyaluran',
      name: 'dashboard-penyaluran',
      component: () => import('@/pages/DashboardPenyaluranPage.vue'),
      meta: { title: 'Dashboard Penyaluran' },
    },
```

- [ ] **Step 2: Tambah nav entry di AppSidebar.vue**

Cari objek group dengan label `'Dashboard'` (array items yang berisi `{ label: 'Dashboard', to: '/', ... }`). Tambah 2 item setelahnya dalam array `items` yang sama:

```typescript
{ label: 'Keuangan', icon: Coins, to: '/dashboard/keuangan' },
{ label: 'Penyaluran', icon: HandHeart, to: '/dashboard/penyaluran' },
```

Import `Coins` dan `HandHeart` jika belum ada di baris import AppSidebar (cek baris `import { ... } from 'lucide-vue-next'`).

- [ ] **Step 3: Verifikasi sidebar compile**

Browser buka `http://localhost:5173` — sidebar harus tampil "Keuangan" dan "Penyaluran" di bawah "Dashboard".

- [ ] **Step 4: Commit frontend**

```bash
cd /media/win_d/workshop/isf-app
git add apps_zakat/web-vue/src/
git commit -m "feat(web): dashboard keuangan & penyaluran pages + shared widgets"
```

---

## Task 12 — Sync ke apps_wakaf

**Files:**
- Clone semua file yang baru/berubah ke apps_wakaf

- [ ] **Step 1: Sync api-python**

```bash
cp apps_zakat/api-python/app/modules/dashboard/schema.py  apps_wakaf/api-python/app/modules/dashboard/schema.py
cp apps_zakat/api-python/app/modules/dashboard/service.py apps_wakaf/api-python/app/modules/dashboard/service.py
cp apps_zakat/api-python/app/modules/dashboard/router.py  apps_wakaf/api-python/app/modules/dashboard/router.py
```

- [ ] **Step 2: Sync bff-api**

```bash
cp apps_zakat/bff-api/app/routers/dashboard.py apps_wakaf/bff-api/app/routers/dashboard.py
```

- [ ] **Step 3: Sync web-vue**

```bash
cp apps_zakat/web-vue/src/components/ui/PeriodFilter.vue      apps_wakaf/web-vue/src/components/ui/PeriodFilter.vue
cp apps_zakat/web-vue/src/components/widgets/BudgetProgress.vue apps_wakaf/web-vue/src/components/widgets/BudgetProgress.vue
cp apps_zakat/web-vue/src/components/widgets/RekeningList.vue  apps_wakaf/web-vue/src/components/widgets/RekeningList.vue
cp apps_zakat/web-vue/src/components/widgets/MemoList.vue      apps_wakaf/web-vue/src/components/widgets/MemoList.vue
cp apps_zakat/web-vue/src/pages/DashboardKeuanganPage.vue      apps_wakaf/web-vue/src/pages/DashboardKeuanganPage.vue
cp apps_zakat/web-vue/src/pages/DashboardPenyaluranPage.vue    apps_wakaf/web-vue/src/pages/DashboardPenyaluranPage.vue
cp apps_zakat/web-vue/src/router/index.ts                      apps_wakaf/web-vue/src/router/index.ts
cp apps_zakat/web-vue/src/components/AppSidebar.vue            apps_wakaf/web-vue/src/components/AppSidebar.vue
```

- [ ] **Step 4: Commit sync**

```bash
cd /media/win_d/workshop/isf-app
git add apps_wakaf/
git commit -m "sync: dashboard keuangan & penyaluran ke apps_wakaf"
```

---

## Task 13 — Rebuild containers & verifikasi

- [ ] **Step 1: Rebuild zakat stack**

```bash
cd /media/win_d/workshop/isf-app/infra
podman-compose -f docker-compose.zakat.yml down -v
podman-compose -f docker-compose.zakat.yml up -d --build
```

- [ ] **Step 2: Rebuild wakaf stack**

```bash
podman-compose -f docker-compose.wakaf.yml down -v
podman-compose -f docker-compose.wakaf.yml up -d --build
```

- [ ] **Step 3: Cek containers running**

```bash
podman ps --filter name=isf- --format "table {{.Names}}\t{{.Status}}" | head -20
```

Expected: 6 container running (3 zakat + 3 wakaf).

- [ ] **Step 4: Test endpoint keuangan via BFF (butuh cookie auth)**

```bash
# Login dulu
curl -c /tmp/isf-cookies.txt -s -X POST http://localhost:7000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | python3 -m json.tool | head -5

# Test keuangan
curl -b /tmp/isf-cookies.txt -s \
  "http://localhost:7000/api/dashboard/keuangan?bulan=5&tahun=2026" \
  | python3 -m json.tool | head -40
```

Expected: JSON dengan `"status":"ok"`, field `period`, `kpis`, `trend`, `anggaran`, `rekening`.

Jika DB tidak ada data: field berisi array kosong / nilai 0 — normal.

- [ ] **Step 5: Verifikasi UI browser**

Buka `http://localhost:5173/dashboard/keuangan`:
- Header "Dashboard Keuangan" + PeriodFilter dropdown + tombol refresh
- 4 KPI card baris pertama
- TrendChart + AsnafDonut baris kedua
- BudgetProgress + RekeningList baris ketiga

Buka `http://localhost:5173/dashboard/penyaluran`:
- Header "Dashboard Penyaluran" + PeriodFilter
- 3 KPI card
- BudgetProgress + MemoList

- [ ] **Step 6: Cek sidebar**

Sidebar kiri harus menampilkan:
```
Dashboard
  ├── Dashboard (/)
  ├── Keuangan (/dashboard/keuangan)
  └── Penyaluran (/dashboard/penyaluran)
```

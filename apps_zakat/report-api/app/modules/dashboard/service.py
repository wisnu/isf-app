"""Dashboard service — gabungan dummy (summary lama) dan real-DB (v2)."""

from __future__ import annotations

import asyncio

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


async def _trend_point(m: int, y: int) -> TrendPoint:
    fund, dist = await asyncio.gather(_sum_fund(m, y), _sum_dist(m, y))
    return TrendPoint(label=f"{y}-{m:02d}", penerimaan=fund, penyaluran=dist)


async def _trend_6bulan(bulan: int, tahun: int) -> list[TrendPoint]:
    # Run all months concurrently — sequential awaits exceeded the BFF's 10s
    # read timeout (12 queries × ~1.6s). Pool max_size=10 absorbs the fan-out.
    months = _last_6_months(bulan, tahun)
    return list(await asyncio.gather(*(_trend_point(m, y) for m, y in months)))


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


# ── Per-chart functions (FE fetches each widget independently) ───────────────
# Reuse the same helpers as the bundle composers above. Each returns the
# wrapped shape the frontend `useFetch` queries expect (period+kpis, trend,
# asnaf, anggaran, ...), or None when the DB is down (→ 503 in the router).

async def get_keuangan_kpis(bulan: int, tahun: int) -> dict | None:
    if not await ping():
        return None
    prev_m, prev_y = _prev_month(bulan, tahun)
    # Run the independent aggregates concurrently — sequential awaits pushed this
    # past the BFF's 10s read timeout under parallel widget load (pool contention).
    cur_fund, prev_fund, cur_dist, prev_dist, saldo, otorisasi = await asyncio.gather(
        _sum_fund(bulan, tahun),
        _sum_fund(prev_m, prev_y),
        _sum_dist(bulan, tahun),
        _sum_dist(prev_m, prev_y),
        _saldo_total(),
        _otorisasi_pending(),
    )
    return {
        "period": f"{tahun}-{bulan:02d}",
        "kpis": {
            "penerimaan": (await _kpi_card(cur_fund, prev_fund)).model_dump(),
            "penyaluran": (await _kpi_card(cur_dist, prev_dist)).model_dump(),
            "saldo": KpiCardData(total=saldo, format="currency").model_dump(),
            "otorisasi_pending": KpiCardData(total=otorisasi, format="count").model_dump(),
        },
    }


async def get_keuangan_trend(bulan: int, tahun: int) -> dict | None:
    if not await ping():
        return None
    return {"trend": [p.model_dump() for p in await _trend_6bulan(bulan, tahun)]}


async def get_keuangan_asnaf(bulan: int, tahun: int) -> dict | None:
    if not await ping():
        return None
    return {"asnaf": [a.model_dump() for a in await _asnaf_dist(bulan, tahun)]}


async def get_keuangan_anggaran(tahun: int) -> dict | None:
    if not await ping():
        return None
    return {"anggaran": [a.model_dump() for a in await _anggaran_list(tahun)]}


async def get_keuangan_rekening() -> dict | None:
    if not await ping():
        return None
    return {"rekening": [r.model_dump() for r in await _rekening_list()]}


async def get_penyaluran_kpis(bulan: int, tahun: int) -> dict | None:
    if not await ping():
        return None
    prev_m, prev_y = _prev_month(bulan, tahun)
    cur_dist, prev_dist, mustahiq, otorisasi = await asyncio.gather(
        _sum_dist(bulan, tahun),
        _sum_dist(prev_m, prev_y),
        _mustahiq_count(bulan, tahun),
        _otorisasi_pending(),
    )
    return {
        "period": f"{tahun}-{bulan:02d}",
        "kpis": {
            "penyaluran": (await _kpi_card(cur_dist, prev_dist)).model_dump(),
            "mustahiq": KpiCardData(total=mustahiq, format="count").model_dump(),
            "otorisasi_pending": KpiCardData(total=otorisasi, format="count").model_dump(),
        },
    }


async def get_penyaluran_anggaran(tahun: int) -> dict | None:
    if not await ping():
        return None
    return {"anggaran": [a.model_dump() for a in await _anggaran_list(tahun)]}


async def get_penyaluran_memo() -> dict | None:
    if not await ping():
        return None
    return {"memo_terbaru": [m.model_dump() for m in await _memo_terbaru()]}


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

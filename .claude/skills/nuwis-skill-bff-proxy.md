# Skill: nuwis-skill-bff-proxy
## Pola BFF-API Routes untuk isf-app

---

## Naming Convention — Bahasa Inggris (WAJIB)

BFF adalah permukaan kontrak ke frontend → semua **English**.

- **Prefix & route path**: domain-grouped English kebab-case → `prefix='/api/finance/transaction/fund-collection'`, `@fund_collection_router.get('/lookup/account')`. JANGAN `/penghimpunan`, `/lookup/rekening`, `/transaksi-umum`.
- **Downstream path** ke api-python harus cocok persis dengan prefix English api-python → `get_api_python('/api/finance/transaction/fund-collection/...')`. JANGAN `/api/transaksi/...` atau `/api/fund-collection/...` (tanpa domain prefix).
- **URL scheme**: `/api/{domain}/{group}/{resource}` — contoh: `/api/finance/master/coa`, `/api/finance/transaction/fund-collection`, `/api/finance/monitoring/authorization`.
- **Query param & JSON field**: English snake_case (`date`, `month`, `year`, `account_no`) — JANGAN `tanggal`, `bulan`, `tahun`.
- **File module**: `modules/finance/master.py` (grup entity), `modules/finance/transaction.py` — BUKAN satu file per entity.
- **BEKU**: nilai `entity_type` di payload otorisasi (`'penghimpunan'`, `'budget_owner'`, …) dan `menu_key` (`finance.transactions.fund_collection`) — sudah disepakati English/kode, jangan ubah.
- Bahasa Indonesia hanya di pesan error & komentar.

> Glossary: `docs/todos/2026-06-20-002-refactor-naming-english/glossary.md`

---

## Peran BFF dalam isf-app

```
Vue (browser) → BFF-API (:7000/:7001) → api-python (:8000/:8001)
                                       → report-api (:8010/:8011)
```

BFF bertanggung jawab:
1. **Auth**: validasi JWT token, cek menu permission
2. **Session injection**: masukkan `inputer_id`, `branch_id`, `tenant_id` ke request
3. **Branch resolution**: cek tipe akses cabang, restrict jika Tunggal
4. **Proxy**: forward request ke api-python atau report-api

Vue **tidak pernah** memanggil api-python atau report-api langsung.

---

## Struktur File

```
apps_{portal}/bff-api/app/
├── modules/
│   ├── core/
│   │   ├── auth.py          ← auth routes + auth_google
│   │   └── tenants.py
│   ├── finance/
│   │   ├── master.py        ← coa_router, bank_router, petty_cash_router, parameter_router
│   │   ├── budget.py        ← budget_router
│   │   ├── transaction.py   ← semua 9 transaction routers (fund_collection, fund_distribution, ...)
│   │   ├── upload.py        ← upload_collection_router, hc_zis_router
│   │   ├── inquiry.py       ← transaction_history_router
│   │   ├── monitoring.py    ← authorization_router
│   │   ├── reports.py       ← report_router
│   │   └── dashboard.py     ← dashboard_router
│   └── administration/
│       └── admin.py         ← admin_router
├── services/
│   ├── auth.py              ← require_menu(), current_user_id_or_401()
│   ├── proxy.py             ← get_api_python(), stream_report_api()
│   └── identity_client.py
└── main.py                  ← create_app() factory, include_router() semua modul
```

**Penting — setiap group file bisa punya beberapa named router:**
```python
# modules/finance/master.py
coa_router       = APIRouter(prefix="/api/finance/master/coa", tags=["coa"])
bank_router      = APIRouter(prefix="/api/finance/master/bank", tags=["bank"])
petty_cash_router = APIRouter(prefix="/api/finance/master/petty-cash", ...)
parameter_router = APIRouter(prefix="/api/finance/master/parameter", ...)
```

**main.py** import dan include tanpa tambahan prefix (router sudah carry full path):
```python
from app.modules.finance.master import coa_router, bank_router, petty_cash_router, parameter_router
app.include_router(coa_router)   # path: /api/finance/master/coa/...
app.include_router(bank_router)  # path: /api/finance/master/bank/...
```

---

## Template Router Lengkap

```python
# apps_{portal}/bff-api/app/modules/finance/master.py  (contoh group file)
from __future__ import annotations
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from app.services.auth import require_menu, current_user_id_or_401
from app.services.proxy import get_api_python

# Satu file, beberapa named router — tiap router prefix full path
coa_router = APIRouter(prefix="/api/finance/master/coa", tags=["coa"])
bank_router = APIRouter(prefix="/api/finance/master/bank", tags=["bank"])


# ── COA ──────────────────────────────────────────────────────────────────────

@coa_router.get("/accounts")
async def list_coa(
    request: Request,
    page: int = Query(1),
    limit: int = Query(25),
    search: str = Query(""),
    _: str = Depends(require_menu("finance.coa")),
):
    downstream = await get_api_python(
        "/api/finance/master/coa/accounts",
        params={"page": page, "limit": limit, "search": search},
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Bank ─────────────────────────────────────────────────────────────────────

@bank_router.get("/accounts")
async def list_bank(
    request: Request,
    _: str = Depends(require_menu("finance.bank")),
):
    downstream = await get_api_python("/api/finance/master/bank/accounts")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Delete ───────────────────────────────────────────────────────────────────

@router.delete("/{resource}/{id}")
async def delete_{resource}(
    id: int,
    session=Depends(require_menu("{menu_key}.hapus"))
):
    return await proxy_post(
        f"/api/{domain}/{resource}/{id}", body={}, session=session, method="DELETE"
    )
```

---

## Stream Laporan XLSX

```python
from app.core.proxy import stream_report_api

# Preview data (JSON):  — path slug & params English (begin/end, bukan tgl_awal/tgl_akhir)
@router.get("/report/{name}")
async def report_{name}(
    begin: str,
    end: str,
    session=Depends(require_menu("{menu_key_report}"))
):
    return await proxy_get(
        f"/report/{name}",
        params={"begin": begin, "end": end},
        session=session,
        service="report"  # ← arahkan ke report-api
    )

# Download XLSX:
@router.get("/report/{name}/export.xlsx")
async def export_{name}(
    begin: str,
    end: str,
    session=Depends(require_menu("{menu_key_report}"))
):
    return await stream_report_api(
        f"/report/{name}/export.xlsx",
        params={"begin": begin, "end": end},
        session=session
    )
    # stream_report_api sets Content-Disposition header otomatis
```

---

## _resolve_branch Pattern

```python
from app.core.branch import _resolve_branch

# Di setiap endpoint write yang butuh branch context:
branch_id = _resolve_branch(session)
# Rules:
# - tipe_akses_cabang = 'T' (Tunggal) → returns session["primary_branch"]
# - tipe_akses_cabang = 'S' (Seluruh) → returns None (api-python bisa akses semua)
# - Jika user punya 'T' tapi coba akses branch lain → 403 BRANCH_DENIED
```

---

## Otorisasi Pattern (maker-checker)

```python
# JANGAN proxy ke submission/ (status = DRAFT, tidak muncul di monitoring):
# SALAH: await proxy_post("/api/otorisasi/submission", body=body)

# BENAR: pakai save-and-submit (langsung PENDING, cek limit otomatis):
@router.post("/{resource}/submit")
async def submit_{resource}(
    request: Request,
    session=Depends(require_menu("{menu_key}"))
):
    body = await request.json()
    body["inputer_id"] = session["user_id"]
    body["branch_id"]  = _resolve_branch(session)

    return await proxy_post("/api/otorisasi/save-and-submit", body={
        "entity_type": "{entity_type}",  # contoh: "penghimpunan"
        "payload": body
    }, session=session)
```

---

## Daftar Router di main.py

```python
# apps_{portal}/bff-api/app/main.py
from app.routers import (
    auth,
    keuangan,
    {domain},  # ← tambah baris ini
)

app.include_router(auth.router)
app.include_router(keuangan.router)
app.include_router({domain}.router)  # ← dan baris ini
```

---

## Error Responses

BFF mengembalikan error standard dari api-python:

| Code | HTTP | Keterangan |
|---|---|---|
| `UNAUTHORIZED` | 401 | Token tidak valid / expired |
| `MENU_DENIED` | 403 | User tidak punya menu permission |
| `BRANCH_DENIED` | 403 | User Tunggal mencoba akses branch lain |
| `VALIDATION_ERROR` | 422 | Payload tidak valid |
| `NOT_FOUND` | 404 | Data tidak ditemukan |

Vue menangani ini di `lib/api/client.ts` — BFF cukup forward error dari api-python.

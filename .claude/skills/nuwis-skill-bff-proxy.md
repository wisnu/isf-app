# Skill: nuwis-skill-bff-proxy
## Pola BFF-API Routes untuk isf-app

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
├── routers/
│   └── {domain}.py      ← tambah file baru per domain
├── core/
│   ├── auth.py          ← require_menu(), get_session()
│   ├── proxy.py         ← proxy_get(), proxy_post(), stream_report_api()
│   └── branch.py        ← _resolve_branch()
└── main.py              ← include_router() semua domain
```

---

## Template Router Lengkap

```python
# apps_{portal}/bff-api/app/routers/{domain}.py
from fastapi import APIRouter, Depends, Request, Query
from typing import Optional
from app.core.auth import require_menu, get_session
from app.core.proxy import proxy_get, proxy_post, stream_report_api
from app.core.branch import _resolve_branch

router = APIRouter(prefix="/api/{domain}", tags=["{domain}"])


# ── List (read) ──────────────────────────────────────────────────────────────

@router.get("/{resource}")
async def list_{resource}(
    page: int = Query(1),
    limit: int = Query(25),
    search: str = Query(""),
    session=Depends(require_menu("{menu_key}"))
):
    return await proxy_get(
        f"/api/{domain}/{resource}",
        params={"page": page, "limit": limit, "search": search},
        session=session
    )


# ── Detail ───────────────────────────────────────────────────────────────────

@router.get("/{resource}/{id}")
async def get_{resource}(
    id: int,
    session=Depends(require_menu("{menu_key}"))
):
    return await proxy_get(f"/api/{domain}/{resource}/{id}", session=session)


# ── Create ───────────────────────────────────────────────────────────────────

@router.post("/{resource}")
async def create_{resource}(
    request: Request,
    session=Depends(require_menu("{menu_key}.tambah"))
):
    body = await request.json()
    # BFF inject session data — api-python tidak bisa baca JWT langsung
    body["inputer_id"] = session["user_id"]
    body["branch_id"]  = _resolve_branch(session)
    body["tenant_id"]  = session.get("active_tenant_id")
    return await proxy_post(f"/api/{domain}/{resource}", body=body, session=session)


# ── Update ───────────────────────────────────────────────────────────────────

@router.put("/{resource}/{id}")
async def update_{resource}(
    id: int,
    request: Request,
    session=Depends(require_menu("{menu_key}.edit"))
):
    body = await request.json()
    body["updated_by"] = session["user_id"]
    return await proxy_post(
        f"/api/{domain}/{resource}/{id}", body=body, session=session, method="PUT"
    )


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

# Preview data (JSON):
@router.get("/laporan/{nama}")
async def laporan_{nama}(
    tgl_awal: str,
    tgl_akhir: str,
    session=Depends(require_menu("{menu_key_laporan}"))
):
    return await proxy_get(
        f"/laporan/{nama}",
        params={"tgl_awal": tgl_awal, "tgl_akhir": tgl_akhir},
        session=session,
        service="report"  # ← arahkan ke report-api
    )

# Download XLSX:
@router.get("/laporan/{nama}/export")
async def export_{nama}(
    tgl_awal: str,
    tgl_akhir: str,
    session=Depends(require_menu("{menu_key_laporan}"))
):
    return await stream_report_api(
        f"/laporan/{nama}/export",
        params={"tgl_awal": tgl_awal, "tgl_akhir": tgl_akhir},
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

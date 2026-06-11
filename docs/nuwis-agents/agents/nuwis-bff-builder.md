---
name: nuwis-bff-builder
description: >
  Generate routes BFF-API isf-app: proxy ke api-python, auth decorator,
  _resolve_branch, stream xlsx dari report-api. Bekerja dari specs.md yang
  sudah disediakan. Path: apps_{portal}/bff-api/app/routers/{domain}.py
model: haiku
color: green
---

Kamu adalah BFF-API developer isf-app. Tugasmu menulis routes di
`apps_{portal}/bff-api/app/routers/{domain}.py` yang mem-proxy request
dari frontend Vue ke api-python (atau report-api untuk laporan).

Baca skill `.claude/skills/nuwis-skill-bff-proxy.md` untuk pola lengkap.

## Lokasi File

```
apps_{portal}/bff-api/app/
├── routers/{domain}.py     ← file yang kamu buat/ubah
└── main.py                 ← tambah include_router di sini
```

## Template Route Proxy Standar

```python
# apps_{portal}/bff-api/app/routers/{domain}.py
from fastapi import APIRouter, Depends, Request
from app.core.auth import require_menu, get_session
from app.core.proxy import proxy_get, proxy_post
from app.core.branch import _resolve_branch

router = APIRouter(prefix="/api/{domain}", tags=["{domain}"])

# LIST — proxy GET ke api-python
@router.get("/{resource}")
async def list_{resource}(
    request: Request,
    page: int = 1,
    limit: int = 25,
    session=Depends(require_menu("{menu_key}"))
):
    return await proxy_get(
        f"/api/{domain}/{resource}",
        params={"page": page, "limit": limit},
        session=session
    )

# CREATE — proxy POST ke api-python
@router.post("/{resource}")
async def create_{resource}(
    request: Request,
    session=Depends(require_menu("{menu_key}"))
):
    body = await request.json()
    # inject session data ke payload
    body["inputer_id"] = session["user_id"]
    body["branch_id"] = _resolve_branch(session)
    return await proxy_post("/api/{domain}/{resource}", body=body, session=session)

# UPDATE
@router.put("/{resource}/{id}")
async def update_{resource}(
    id: int,
    request: Request,
    session=Depends(require_menu("{menu_key}.edit"))
):
    body = await request.json()
    return await proxy_post(f"/api/{domain}/{resource}/{id}", body=body, session=session, method="PUT")

# DELETE
@router.delete("/{resource}/{id}")
async def delete_{resource}(
    id: int,
    request: Request,
    session=Depends(require_menu("{menu_key}.hapus"))
):
    return await proxy_post(f"/api/{domain}/{resource}/{id}", body={}, session=session, method="DELETE")
```

## Template Route Stream Laporan (XLSX)

```python
from app.core.proxy import stream_report_api
from fastapi.responses import StreamingResponse

@router.get("/laporan/{nama}")
async def laporan_{nama}(
    request: Request,
    tgl_awal: str,
    tgl_akhir: str,
    session=Depends(require_menu("{menu_key_laporan}"))
):
    # Data JSON untuk preview
    return await proxy_get(
        f"/laporan/{nama}",
        params={"tgl_awal": tgl_awal, "tgl_akhir": tgl_akhir},
        session=session,
        service="report"  # ← arahkan ke report-api
    )

@router.get("/laporan/{nama}/export")
async def export_{nama}(
    request: Request,
    tgl_awal: str,
    tgl_akhir: str,
    session=Depends(require_menu("{menu_key_laporan}"))
):
    # Stream XLSX dari report-api
    return await stream_report_api(
        f"/laporan/{nama}/export",
        params={"tgl_awal": tgl_awal, "tgl_akhir": tgl_akhir},
        session=session
    )
```

## Daftarkan Router di main.py

```python
# apps_{portal}/bff-api/app/main.py
from app.routers import {domain}

app.include_router({domain}.router)
```

## _resolve_branch Pattern

```python
from app.core.branch import _resolve_branch

# Di setiap endpoint yang butuh branch_id:
branch_id = _resolve_branch(session)
# → returns session["primary_branch"] jika tipe_akses_cabang = 'T' (Tunggal)
# → returns None jika tipe_akses_cabang = 'S' (Seluruh) — api-python decide
```

Jangan hardcode `branch_id`. Selalu gunakan `_resolve_branch()`.

## Menu Key per Endpoint

Setiap endpoint HARUS punya `require_menu()` — tidak ada endpoint tanpa auth:

```python
# Read-only endpoints:
session=Depends(require_menu("{domain}.{sub}.lihat"))

# Write endpoints:
session=Depends(require_menu("{domain}.{sub}.tambah"))
session=Depends(require_menu("{domain}.{sub}.edit"))
session=Depends(require_menu("{domain}.{sub}.hapus"))

# Laporan:
session=Depends(require_menu("{domain}.laporan.{nama}"))
```

## Otorisasi Endpoint (jika fitur pakai maker-checker)

```python
# Jangan proxy ke submission/ — pakai save-and-submit:
@router.post("/{resource}/submit")
async def submit_{resource}(
    request: Request,
    session=Depends(require_menu("{menu_key}"))
):
    body = await request.json()
    body["inputer_id"] = session["user_id"]
    body["branch_id"] = _resolve_branch(session)
    return await proxy_post("/api/otorisasi/save-and-submit", body={
        "entity_type": "{entity_type}",
        "payload": body
    }, session=session)
```

## Daftar Checks Sebelum Selesai

- [ ] Setiap endpoint punya `require_menu()` decorator
- [ ] `inputer_id` diambil dari session (bukan dari body request langsung)
- [ ] `branch_id` pakai `_resolve_branch(session)` (bukan hardcoded)
- [ ] Router terdaftar di `main.py`
- [ ] Stream laporan pakai `stream_report_api()` (bukan proxy biasa)
- [ ] Tidak ada URL langsung ke api-python (:8000) dari router

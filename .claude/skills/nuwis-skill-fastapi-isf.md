# Skill: nuwis-skill-fastapi-isf
## Pola FastAPI untuk api-python isf-app

Skill ini mencakup pola spesifik proyek untuk modul di `apps_{portal}/api-python/app/modules/`.

---

## Struktur Modul Standar

```
apps_{portal}/api-python/app/modules/{domain}/
├── __init__.py        ← import router
├── router.py          ← FastAPI endpoints + dependency injection
├── service.py         ← business logic + asyncpg queries
├── schema.py          ← Pydantic v2 request/response models
└── repo.py            ← (opsional) raw queries jika service.py terlalu kompleks
```

---

## router.py — Pola Standar

> ⚠️ **CRITICAL**: api-python TIDAK memiliki `app.core`. Jangan import dari `app.core.auth`,
> `app.core.db`, atau `app.core.response`. Auth/menu guard hanya ada di BFF-API layer.
> api-python adalah internal service — koneksi DB via `get_pool().acquire()` dari `app.shared.db`.

```python
from fastapi import APIRouter, HTTPException, Request
from app.shared.db import get_pool
from app.shared.response import ok
from app.modules.{domain} import service, schema

router = APIRouter(prefix="/{domain}", tags=["{domain}"])

@router.get("")
async def list_{resource}(
    page: int = 1,
    limit: int = 25,
    search: str = "",
    branch_code: str = "",
):
    async with get_pool().acquire() as db:
        rows, total = await service.list_{resource}(db, page=page, limit=limit, search=search, branch_code=branch_code)
    return ok({
        "rows": rows,
        "pagination": {"page": page, "limit": limit, "total": total, "total_pages": -(-total // limit) if total else 0}
    })

@router.get("/{id}")
async def get_{resource}(id: int):
    async with get_pool().acquire() as db:
        row = await service.get_{resource}_by_id(db, id)
    if not row:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return ok(row)

@router.post("")
async def create_{resource}(
    payload: schema.Create{Resource},
    request: Request,
):
    # session diinject BFF via request.state.session
    session = request.state.session
    user_id = session["user_id"]
    branch_code = session.get("primary_branch", "")

    from app.modules.otorisasi import service as otorisasi_svc
    result = await otorisasi_svc.save_and_submit(
        entity_type='{resource}',
        module='{menu_key}',
        payload=payload.model_dump(),
        user_id=user_id,
        branch_code=branch_code,
    )
    return ok(result)

@router.put("/{id}")
async def update_{resource}(
    id: int,
    payload: schema.Update{Resource},
    request: Request,
):
    async with get_pool().acquire() as db:
        result = await service.update_{resource}(db, id, payload)
    return ok(result)

@router.delete("/{id}")
async def delete_{resource}(id: int):
    async with get_pool().acquire() as db:
        await service.delete_{resource}(db, id)
    return ok({"deleted": True})
```

---

## service.py — Pola Query asyncpg

```python
from asyncpg import Connection
from app.modules.{domain}.schema import Create{Resource}, Update{Resource}

async def list_{resource}(
    db: Connection,
    page: int = 1,
    limit: int = 25,
    search: str = ""
) -> tuple[list[dict], int]:
    offset = (page - 1) * limit

    # Gunakan CAST, bukan ::
    rows = await db.fetch(
        """
        SELECT
          id,
          nama,
          CAST(tanggal AS VARCHAR) AS tanggal,
          CAST(jumlah AS NUMERIC(20, 4)) AS jumlah,
          keterangan
        FROM {schema}.{tabel}
        WHERE ($1 = '' OR nama ILIKE '%' || $1 || '%')
        ORDER BY id DESC
        LIMIT $2 OFFSET $3
        """,
        search, limit, offset
    )

    total = await db.fetchval(
        "SELECT COUNT(*) FROM {schema}.{tabel} WHERE ($1 = '' OR nama ILIKE '%' || $1 || '%')",
        search
    )

    return [dict(r) for r in rows], total

async def create_{resource}(
    db: Connection,
    payload: Create{Resource},
    inputer_id: str,
    branch_id: int | None = None
) -> dict:
    async with db.transaction():
        row = await db.fetchrow(
            """
            INSERT INTO {schema}.{tabel} (nama, tanggal, jumlah, inputer_id, branch_id)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, nama, CAST(tanggal AS VARCHAR) AS tanggal, jumlah, inputer_id
            """,
            payload.nama,
            payload.tanggal,
            payload.jumlah,
            inputer_id,
            branch_id
        )
    return dict(row)
```

---

## schema.py — Pydantic v2

```python
from pydantic import BaseModel, Field, field_validator
from datetime import date
from decimal import Decimal
from typing import Optional

class Create{Resource}(BaseModel):
    nama: str = Field(min_length=1, max_length=255)
    tanggal: date
    jumlah: Decimal = Field(gt=0, decimal_places=4)
    keterangan: Optional[str] = None
    # Diinject oleh BFF — required di schema tapi diisi oleh server
    inputer_id: str
    branch_id: Optional[int] = None

class Update{Resource}(BaseModel):
    nama: Optional[str] = None
    keterangan: Optional[str] = None

class {Resource}Row(BaseModel):
    id: int
    nama: str
    tanggal: str   # ISO YYYY-MM-DD (sudah VARCHAR dari CAST)
    jumlah: Decimal
    keterangan: Optional[str]
```

---

## Response Wrapper `ok()`

```python
from app.shared.response import ok  # BUKAN app.core.response

# Single object:
return ok({"id": 1, "nama": "test"})
# → {"data": {"id": 1, "nama": "test"}, "meta": {"request_id": "..."}}

# List + pagination:
return ok({"rows": rows, "pagination": pagination})
# → {"data": {"rows": [...], "pagination": {...}}, "meta": {...}}

# JANGAN pakai JSONResponse langsung:
return JSONResponse({"data": rows})  # SALAH — tidak ada meta.request_id
```

---

## Aturan SQL Kritis

### CAST — Tidak Boleh Pakai `::`

```python
# SALAH — Firebird/MSSQL syntax, tidak konsisten:
"WHERE CAST(tanggal::date AS VARCHAR) = $1"
"SELECT amount::numeric"

# BENAR — SQL standar:
"WHERE CAST(tanggal AS DATE) = $1"
"SELECT CAST(amount AS NUMERIC(20,4))"
```

### Date Column

```python
# Simpan dan query sebagai DATE, bukan VARCHAR:
INSERT INTO ... (tanggal) VALUES ($1)
# → payload.tanggal sudah date object dari Pydantic

# Di SELECT, return sebagai VARCHAR agar JSON-serializable:
SELECT CAST(tanggal AS VARCHAR) AS tanggal
# → "2026-01-15" (ISO, bukan "15-01-2026")
# Frontend yang format ke DD-MM-YYYY via dmy()
```

### Discriminator Hardcoded

```python
# Discriminator adalah domain constraint, BUKAN filter parameter:
rows = await db.fetch(
    """
    SELECT * FROM transaction.accounttransactionitem
    WHERE accounttitype = 'D'  -- ← hardcoded, bukan $1
      AND tanggal BETWEEN $1 AND $2
    """,
    tgl_awal, tgl_akhir
)
```

---

## asyncpg Pool Init — Wajib di shared/db.py

> Dipakai saat membuat `db.py` baru atau menambah pool. Jangan pakai pattern lama.

```python
import asyncio
import asyncpg

async def init_pool() -> asyncpg.Pool | None:
    global _pool
    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        return None
    # Wajib: SSL default asyncpg gagal di podman rootless (host.containers.internal)
    if "sslmode" not in dsn:
        sep = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{sep}sslmode=disable"
    last_exc: Exception | None = None
    for attempt in range(10):
        try:
            _pool = await asyncpg.create_pool(dsn, min_size=0, max_size=10, command_timeout=15)
            return _pool
        except (OSError, asyncpg.PostgresConnectionFailureError) as e:
            last_exc = e
            await asyncio.sleep(2)
    raise RuntimeError(f"Cannot connect to DB after 10 attempts: {last_exc}") from last_exc
```

**Tiga aturan wajib:**
1. `sslmode=disable` — Postgres host ini tidak pakai SSL; asyncpg default `ssl=prefer` menyebabkan `ConnectionRefusedError`
2. `min_size=0` — pool "berhasil init" tanpa actual connect; koneksi dibuat lazy saat `acquire()` pertama
3. Retry 10x dengan 2s delay — atasi race condition container startup vs network route

**bff-api extra:** tambah `await asyncio.sleep(3)` sebelum retry loop.

---

## Pendaftaran Router

```python
# apps_{portal}/api-python/app/main.py
from app.modules.{domain}.router import router as {domain}_router

app.include_router({domain}_router)
```

---

## Report API (report-api, bukan api-python)

Untuk laporan, modul ada di `apps_{portal}/report-api/app/modules/`:

```python
# service.py — query DWH view, read-only
async def get_laporan_{nama}(db, tgl_awal: date, tgl_akhir: date) -> list[dict]:
    rows = await db.fetch(
        """
        SELECT * FROM dwh.v_{nama_view}
        WHERE tanggal BETWEEN $1 AND $2
        ORDER BY tanggal, id
        """,
        tgl_awal, tgl_akhir
    )
    return [dict(r) for r in rows]

# export.py — openpyxl xlsx export
import openpyxl, io

def export_xlsx(rows: list[dict], filename: str) -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = filename
    if rows:
        ws.append(list(rows[0].keys()))  # header dari keys
        for row in rows:
            ws.append(list(row.values()))
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()
```

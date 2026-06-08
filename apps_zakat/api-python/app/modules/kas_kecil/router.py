from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.kas_kecil.schema import KasKecilCreate, KasKecilUpdate
from app.modules.kas_kecil.service import (
    create_kas_kecil,
    delete_kas_kecil,
    get_kas_kecil_detail,
    get_lookup_branches,
    get_lookup_currencies,
    get_lookup_gl_accounts,
    list_kas_kecil,
    update_kas_kecil,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix="/kas-kecil", tags=["kas-kecil"])


@router.get("/accounts")
async def accounts(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await list_kas_kecil(search=search, page=page, page_size=page_size)
    return ok(data.model_dump())


@router.get("/accounts/{account_no}")
async def get_account(account_no: str):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    detail = await get_kas_kecil_detail(account_no)
    if detail is None:
        raise HTTPException(status_code=404, detail="Rekening kas kecil tidak ditemukan")
    return ok(detail.model_dump())


@router.post("/accounts", status_code=201)
async def create_account(payload: KasKecilCreate):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    account_no = await create_kas_kecil(payload)
    return ok({"account_no": account_no})


@router.put("/accounts/{account_no}")
async def update_account(account_no: str, payload: KasKecilUpdate):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    existing = await get_kas_kecil_detail(account_no)
    if existing is None:
        raise HTTPException(status_code=404, detail="Rekening kas kecil tidak ditemukan")
    await update_kas_kecil(account_no, payload)
    return ok({})


@router.delete("/accounts/{account_no}")
async def delete_account(account_no: str):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    existing = await get_kas_kecil_detail(account_no)
    if existing is None:
        raise HTTPException(status_code=404, detail="Rekening kas kecil tidak ditemukan")
    await delete_kas_kecil(account_no)
    return ok({})


@router.get("/lookup/branches")
async def lookup_branches():
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await get_lookup_branches()
    return ok({"data": [item.model_dump() for item in data]})


@router.get("/lookup/currencies")
async def lookup_currencies():
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await get_lookup_currencies()
    return ok({"data": [item.model_dump() for item in data]})


@router.get("/lookup/gl_accounts")
async def lookup_gl_accounts(
    search: str | None = Query(default=None, max_length=100),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await get_lookup_gl_accounts(search=search)
    return ok({"data": [item.model_dump() for item in data]})

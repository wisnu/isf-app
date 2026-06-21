from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.finance.master.bank.service import (
    get_bank_account_detail,
    get_lookup_banks,
    get_lookup_branches,
    get_lookup_currencies,
    get_lookup_gl_accounts,
    get_lookup_products,
    list_bank_accounts,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix="/finance/master/bank", tags=["bank"])


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
    data = await list_bank_accounts(search=search, page=page, page_size=page_size)
    return ok(data.model_dump())


@router.get("/accounts/{account_no}")
async def get_account(account_no: str):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    detail = await get_bank_account_detail(account_no)
    if detail is None:
        raise HTTPException(status_code=404, detail="Rekening tidak ditemukan")
    return ok(detail.model_dump())


@router.get("/lookup/banks")
async def lookup_banks():
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await get_lookup_banks()
    return ok({"data": [item.model_dump() for item in data]})


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


@router.get("/lookup/products")
async def lookup_products(
    search: str | None = Query(default=None, max_length=100),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await get_lookup_products(search=search)
    return ok({"data": [item.model_dump() for item in data]})

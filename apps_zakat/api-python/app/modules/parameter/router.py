from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.shared.db import ping
from app.shared.response import err, ok
from . import service

router = APIRouter(prefix="/parameter", tags=["parameter"])


@router.get("/pemilik-anggaran")
async def list_owners(
    page:  int          = Query(default=1,    ge=1),
    limit: int          = Query(default=25,   ge=1, le=100),
    q:     str | None   = Query(default=None, max_length=100),
):
    if not await ping():
        return JSONResponse(503, content=err("DB_UNAVAILABLE", "Database tidak tersedia"))
    data = await service.list_budget_owners(page=page, limit=limit, q=q)
    return ok(data)


@router.get("/pemilik-anggaran/lookup")
async def lookup_owners(q: str | None = Query(default=None, max_length=100)):
    if not await ping():
        return JSONResponse(503, content=err("DB_UNAVAILABLE", "Database tidak tersedia"))
    data = await service.lookup_groups(q=q)
    return ok({"data": data})


@router.get("/pemilik-anggaran/{ownerid}")
async def get_owner(ownerid: int):
    if not await ping():
        return JSONResponse(503, content=err("DB_UNAVAILABLE", "Database tidak tersedia"))
    data = await service.get_budget_owner(ownerid)
    return ok(data)

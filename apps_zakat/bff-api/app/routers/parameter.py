from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python

router = APIRouter(prefix="/parameter", tags=["parameter"])


@router.get("/pemilik-anggaran")
async def list_owners(
    request:  Request,
    _:        str       = Depends(require_menu("finance.parameter.budget_owner")),
    page:     int       = Query(default=1,    ge=1),
    limit:    int       = Query(default=25,   ge=1, le=100),
    q:        str | None = Query(default=None),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    params: dict = {"page": page, "limit": limit}
    if q:
        params["q"] = q
    downstream = await get_api_python("/api/parameter/pemilik-anggaran", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/pemilik-anggaran/lookup")
async def lookup_owners(
    request: Request,
    _:       str       = Depends(require_menu("finance.parameter.budget_owner")),
    q:       str | None = Query(default=None),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    params: dict = {}
    if q:
        params["q"] = q
    downstream = await get_api_python("/api/parameter/pemilik-anggaran/lookup", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/pemilik-anggaran/{ownerid}")
async def get_owner(
    request:  Request,
    ownerid:  int,
    _:        str = Depends(require_menu("finance.parameter.budget_owner")),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    downstream = await get_api_python(f"/api/parameter/pemilik-anggaran/{ownerid}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

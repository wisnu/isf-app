from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401
from app.services.proxy import get_api_python
from app.shared.response import err

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def summary(request: Request):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    active_tenant = request.session.get("active_tenant_id")
    if not active_tenant:
        return JSONResponse(
            status_code=403, content=err("NO_TENANT", "No active tenant for this session")
        )

    downstream = await get_api_python(
        "/api/dashboard/summary", params={"tenant_id": active_tenant}
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/keuangan")
async def keuangan(request: Request, bulan: int = None, tahun: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params = {}
    if bulan is not None:
        params["bulan"] = bulan
    if tahun is not None:
        params["tahun"] = tahun

    downstream = await get_api_python("/api/dashboard/keuangan", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/penyaluran")
async def penyaluran(request: Request, bulan: int = None, tahun: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params = {}
    if bulan is not None:
        params["bulan"] = bulan
    if tahun is not None:
        params["tahun"] = tahun

    downstream = await get_api_python("/api/dashboard/penyaluran", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

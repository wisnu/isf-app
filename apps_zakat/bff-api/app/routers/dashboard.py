from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401
from app.services.proxy import get_report_api
from app.shared.response import err

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _period_params(month: int | None, year: int | None) -> dict:
    params: dict = {}
    if month is not None:
        params["month"] = month
    if year is not None:
        params["year"] = year
    return params


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

    downstream = await get_report_api(
        "/api/dashboard/summary", params={"tenant_id": active_tenant}
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/finance")
async def finance(request: Request, month: int = None, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params = {}
    if month is not None:
        params["month"] = month
    if year is not None:
        params["year"] = year

    downstream = await get_report_api("/api/dashboard/finance", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/fund-distribution")
async def fund_distribution(request: Request, month: int = None, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params = {}
    if month is not None:
        params["month"] = month
    if year is not None:
        params["year"] = year

    downstream = await get_report_api("/api/dashboard/fund-distribution", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Per-chart endpoints (FE fetches each widget independently) ───────────────

@router.get("/finance/kpis")
async def finance_kpis(request: Request, month: int = None, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api(
        "/api/dashboard/finance/kpis", params=_period_params(month, year)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/finance/trend")
async def finance_trend(request: Request, month: int = None, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api(
        "/api/dashboard/finance/trend", params=_period_params(month, year)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/finance/asnaf")
async def finance_asnaf(request: Request, month: int = None, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api(
        "/api/dashboard/finance/asnaf", params=_period_params(month, year)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/finance/anggaran")
async def finance_anggaran(request: Request, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    params: dict = {}
    if year is not None:
        params["year"] = year
    downstream = await get_report_api("/api/dashboard/finance/anggaran", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/finance/rekening")
async def finance_rekening(request: Request):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api("/api/dashboard/finance/rekening")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/fund-distribution/kpis")
async def fund_distribution_kpis(request: Request, month: int = None, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api(
        "/api/dashboard/fund-distribution/kpis", params=_period_params(month, year)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/fund-distribution/anggaran")
async def fund_distribution_anggaran(request: Request, year: int = None):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    params: dict = {}
    if year is not None:
        params["year"] = year
    downstream = await get_report_api("/api/dashboard/fund-distribution/anggaran", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/fund-distribution/memo")
async def fund_distribution_memo(request: Request):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api("/api/dashboard/fund-distribution/memo")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

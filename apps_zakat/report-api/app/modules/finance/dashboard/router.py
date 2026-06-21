from datetime import date as _date

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.modules.finance.dashboard.service import (
    get_finance,
    get_finance_budget,
    get_finance_asnaf,
    get_finance_kpis,
    get_finance_account,
    get_finance_trend,
    get_fund_distribution,
    get_fund_distribution_budget,
    get_fund_distribution_kpis,
    get_fund_distribution_memo,
    get_summary,
)
from app.shared.response import err, ok

_DB_UNAVAILABLE = err("DB_UNAVAILABLE", "Database tidak tersedia")

router = APIRouter(prefix="/finance/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(tenant_id: str):
    data = get_summary(tenant_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=err("TENANT_NOT_FOUND", f"Tenant '{tenant_id}' not found"),
        )
    return ok(data.model_dump())


@router.get("/finance")
async def finance(
    month: int = _date.today().month,
    year: int = _date.today().year,
):
    data = await get_finance(month, year)
    if data is None:
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database tidak tersedia"),
        )
    return ok(data.model_dump())


@router.get("/fund-distribution")
async def fund_distribution(
    month: int = _date.today().month,
    year: int = _date.today().year,
):
    data = await get_fund_distribution(month, year)
    if data is None:
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database tidak tersedia"),
        )
    return ok(data.model_dump())


# ── Per-chart endpoints (FE fetches each widget independently) ───────────────

@router.get("/finance/kpis")
async def finance_kpis(
    month: int = _date.today().month,
    year: int = _date.today().year,
):
    data = await get_finance_kpis(month, year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/finance/trend")
async def finance_trend(
    month: int = _date.today().month,
    year: int = _date.today().year,
):
    data = await get_finance_trend(month, year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/finance/asnaf")
async def finance_asnaf(
    month: int = _date.today().month,
    year: int = _date.today().year,
):
    data = await get_finance_asnaf(month, year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/finance/budget")
async def finance_budget(
    year: int = _date.today().year,
):
    data = await get_finance_budget(year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/finance/account")
async def finance_account():
    data = await get_finance_account()
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/fund-distribution/kpis")
async def fund_distribution_kpis(
    month: int = _date.today().month,
    year: int = _date.today().year,
):
    data = await get_fund_distribution_kpis(month, year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/fund-distribution/budget")
async def fund_distribution_budget(
    year: int = _date.today().year,
):
    data = await get_fund_distribution_budget(year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/fund-distribution/memo")
async def fund_distribution_memo():
    data = await get_fund_distribution_memo()
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)

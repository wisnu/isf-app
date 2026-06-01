from datetime import date as _date

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.modules.dashboard.service import (
    get_keuangan,
    get_keuangan_anggaran,
    get_keuangan_asnaf,
    get_keuangan_kpis,
    get_keuangan_rekening,
    get_keuangan_trend,
    get_penyaluran,
    get_penyaluran_anggaran,
    get_penyaluran_kpis,
    get_penyaluran_memo,
    get_summary,
)
from app.shared.response import err, ok

_DB_UNAVAILABLE = err("DB_UNAVAILABLE", "Database tidak tersedia")

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(tenant_id: str):
    data = get_summary(tenant_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=err("TENANT_NOT_FOUND", f"Tenant '{tenant_id}' not found"),
        )
    return ok(data.model_dump())


@router.get("/keuangan")
async def keuangan(
    bulan: int = _date.today().month,
    tahun: int = _date.today().year,
):
    data = await get_keuangan(bulan, tahun)
    if data is None:
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database tidak tersedia"),
        )
    return ok(data.model_dump())


@router.get("/penyaluran")
async def penyaluran(
    bulan: int = _date.today().month,
    tahun: int = _date.today().year,
):
    data = await get_penyaluran(bulan, tahun)
    if data is None:
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database tidak tersedia"),
        )
    return ok(data.model_dump())


# ── Per-chart endpoints (FE fetches each widget independently) ───────────────

@router.get("/keuangan/kpis")
async def keuangan_kpis(
    bulan: int = _date.today().month,
    tahun: int = _date.today().year,
):
    data = await get_keuangan_kpis(bulan, tahun)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/keuangan/trend")
async def keuangan_trend(
    bulan: int = _date.today().month,
    tahun: int = _date.today().year,
):
    data = await get_keuangan_trend(bulan, tahun)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/keuangan/asnaf")
async def keuangan_asnaf(
    bulan: int = _date.today().month,
    tahun: int = _date.today().year,
):
    data = await get_keuangan_asnaf(bulan, tahun)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/keuangan/anggaran")
async def keuangan_anggaran(
    tahun: int = _date.today().year,
):
    data = await get_keuangan_anggaran(tahun)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/keuangan/rekening")
async def keuangan_rekening():
    data = await get_keuangan_rekening()
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/penyaluran/kpis")
async def penyaluran_kpis(
    bulan: int = _date.today().month,
    tahun: int = _date.today().year,
):
    data = await get_penyaluran_kpis(bulan, tahun)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/penyaluran/anggaran")
async def penyaluran_anggaran(
    tahun: int = _date.today().year,
):
    data = await get_penyaluran_anggaran(tahun)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/penyaluran/memo")
async def penyaluran_memo():
    data = await get_penyaluran_memo()
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)

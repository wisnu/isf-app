from datetime import date as _date

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.modules.dashboard.service import get_summary, get_keuangan, get_penyaluran
from app.shared.response import err, ok

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

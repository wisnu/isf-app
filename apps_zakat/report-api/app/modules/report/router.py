from fastapi import APIRouter

from app.modules.report.service import dwh_health
from app.shared.response import ok

router = APIRouter(prefix="/report", tags=["report"])


@router.get("/ping")
async def ping():
    """Scaffold health — konfirmasi modul report aktif + konektivitas DWH."""
    return ok({"status": "ok", "dwh": await dwh_health()})

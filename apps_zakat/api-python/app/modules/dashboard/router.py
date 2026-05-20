from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.modules.dashboard.service import get_summary
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

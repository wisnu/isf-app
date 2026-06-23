import io

from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse

from app.modules.appadmin.schema import RoleMenuPermissionUpdateRequest
from app.modules.appadmin.service import (
    ValidationError,
    list_role_menu_permission,
    replace_role_menu_permission,
    export_role_menu_permission_excel,
)
from app.shared.response import err, ok

router = APIRouter(prefix="/appadmin", tags=["appadmin"])


# ── Action-level permission endpoints ────────────────────────────────────────

@router.get("/role-menu-permission")
async def get_role_menu_permission(role_id: str):
    try:
        snapshot = await list_role_menu_permission(role_id)
    except ValidationError as exc:
        return JSONResponse(
            status_code=400,
            content=err(exc.code, exc.message, details=exc.details),
        )
    return ok(snapshot.model_dump())


@router.put("/role-menu-permission")
async def put_role_menu_permission(payload: RoleMenuPermissionUpdateRequest):
    try:
        result = await replace_role_menu_permission(
            payload.role_id, payload.permissions, payload.updated_by
        )
    except ValidationError as exc:
        return JSONResponse(
            status_code=400,
            content=err(exc.code, exc.message, details=exc.details),
        )
    return ok(result.model_dump())


@router.get("/role-menu-permission/export")
async def export_role_menu_permission():
    xlsx_bytes = await export_role_menu_permission_excel()
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=role-menu-permission.xlsx"},
    )

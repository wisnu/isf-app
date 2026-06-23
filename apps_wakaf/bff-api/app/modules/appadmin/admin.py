from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python, stream_api_python

router = APIRouter(prefix="/api/appadmin", tags=["appadmin"])


class MappingPairIn(BaseModel):
    role_id: str
    menu_key: str


class RoleMenuUpdateIn(BaseModel):
    mapping: list[MappingPairIn]


@router.get("/role-menu")
async def get_role_menu(
    request: Request,
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    downstream = await get_api_python("/api/appadmin/role-menu")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/role-menu")
async def put_role_menu(
    payload: RoleMenuUpdateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    body = {
        "mapping": [p.model_dump() for p in payload.mapping],
        "updated_by": user_id,
    }
    downstream = await post_api_python(
        "/api/appadmin/role-menu", json_body=body, method="PUT"
    )

    audit = getattr(request.app.state, "audit", None)
    if audit is not None and downstream.status_code == 200:
        try:
            result = downstream.json()
            diff = result.get("data", {}).get("diff", {})
            await audit.log(
                "role_menu_updated",
                user_id=user_id,
                payload={
                    "total_rows": result.get("data", {}).get("total_rows"),
                    "added_count": len(diff.get("added", [])),
                    "removed_count": len(diff.get("removed", [])),
                },
            )
        except Exception:
            pass

    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ============================================================================
# ROLE-MENU-PERMISSION ENDPOINTS
# ============================================================================


class RoleMenuPermissionIn(BaseModel):
    menu_key: str
    actions: list[str]


class RoleMenuPermissionUpdateIn(BaseModel):
    role_id: str
    permissions: list[RoleMenuPermissionIn]


@router.get("/role-menu-permission")
async def get_role_menu_permission(
    role_id: str,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    downstream = await get_api_python(
        "/api/appadmin/role-menu-permission", params={"role_id": role_id}
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/role-menu-permission")
async def put_role_menu_permission(
    payload: RoleMenuPermissionUpdateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    body = {
        "role_id": payload.role_id,
        "permissions": [p.model_dump() for p in payload.permissions],
        "updated_by": user_id,
    }
    downstream = await post_api_python(
        "/api/appadmin/role-menu-permission", json_body=body, method="PUT"
    )

    audit = getattr(request.app.state, "audit", None)
    if audit is not None and downstream.status_code == 200:
        try:
            result = downstream.json().get("data", {})
            await audit.log(
                "role_menu_permission_updated",
                user_id=user_id,
                payload={
                    "role_id": payload.role_id,
                    "added_count": result.get("added_count"),
                    "removed_count": result.get("removed_count"),
                },
            )
        except Exception:
            pass

    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/role-menu-permission/export")
async def export_role_menu_permission(
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    downstream = await stream_api_python("/api/appadmin/role-menu-permission/export")
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=role-menu-permission.xlsx"},
    )

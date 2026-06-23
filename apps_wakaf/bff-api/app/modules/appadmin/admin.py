from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python, stream_api_python

router = APIRouter(prefix="/api/appadmin", tags=["appadmin"])


# ============================================================================
# ROLE MANAGEMENT ENDPOINTS
# ============================================================================


class RoleCreateIn(BaseModel):
    role_id: str
    role_name: str
    description: str | None = None


class RoleUpdateIn(BaseModel):
    role_name: str
    description: str | None = None


class RoleStatusIn(BaseModel):
    status: str


@router.get("/roles")
async def list_roles(
    request: Request,
    page: int = 1,
    limit: int = 25,
    keyword: str | None = None,
    status: str | None = None,
    user_id: str = Depends(require_menu("appadmin.roles")),
):
    params: dict = {"page": page, "limit": limit}
    if keyword:
        params["keyword"] = keyword
    if status:
        params["status"] = status
    downstream = await get_api_python("/api/appadmin/roles", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/roles")
async def create_role(
    payload: RoleCreateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.roles.create")),
):
    body = {**payload.model_dump(), "created_by": user_id}
    downstream = await post_api_python("/api/appadmin/roles", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/roles/{role_id}")
async def get_role(
    role_id: str,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.roles")),
):
    downstream = await get_api_python(f"/api/appadmin/roles/{role_id.upper()}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/roles/{role_id}")
async def update_role(
    role_id: str,
    payload: RoleUpdateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.roles.edit")),
):
    body = {**payload.model_dump(), "updated_by": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/roles/{role_id.upper()}", json_body=body, method="PUT"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.patch("/roles/{role_id}/status")
async def update_role_status(
    role_id: str,
    payload: RoleStatusIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.roles.edit")),
):
    body = {**payload.model_dump(), "updated_by": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/roles/{role_id.upper()}/status", json_body=body, method="PATCH"
    )
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

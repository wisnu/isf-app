from __future__ import annotations

import bcrypt

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix="/api/appadmin", tags=["appadmin"])

MIN_PASSWORD_LENGTH = 8


class MappingPairIn(BaseModel):
    role_id: str
    menu_key: str


class RoleMenuUpdateIn(BaseModel):
    mapping: list[MappingPairIn]


class BranchCreateIn(BaseModel):
    branch_code: str
    branch_name: str
    branch_type: str
    parent_branch_code: str | None = None
    office_name: str | None = None
    office_npwp: str | None = None
    office_address: str | None = None
    office_postal_code: str | None = None
    office_phone1: str | None = None
    office_phone2: str | None = None
    office_phone3: str | None = None


class BranchUpdateIn(BaseModel):
    branch_name: str
    branch_type: str
    parent_branch_code: str | None = None
    office_name: str | None = None
    office_npwp: str | None = None
    office_address: str | None = None
    office_postal_code: str | None = None
    office_phone1: str | None = None
    office_phone2: str | None = None
    office_phone3: str | None = None


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
# BRANCH MANAGEMENT ENDPOINTS
# ============================================================================


@router.get("/branches")
async def list_branches(
    request: Request,
    status_active: str | None = None,
    keyword: str | None = None,
    page: int = 1,
    limit: int = 25,
    user_id: str = Depends(require_menu("appadmin.branch.list")),
):
    params: dict = {
        "page": page,
        "limit": limit,
    }
    if status_active is not None:
        params["status_aktif"] = status_active
    if keyword is not None:
        params["keyword"] = keyword

    downstream = await get_api_python("/api/appadmin/branches", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/branches/parents")
async def list_parent_branches(
    request: Request,
    user_id: str = Depends(require_menu("appadmin.branch.list")),
):
    downstream = await get_api_python("/api/appadmin/branches/parents")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/branches")
async def create_branch(
    payload: BranchCreateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.branch.create")),
):
    body = {
        **payload.model_dump(),
        "user_input": user_id,
    }
    downstream = await post_api_python("/api/appadmin/branches", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/branches/{branch_code}")
async def get_branch_detail(
    branch_code: str,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.branch.list")),
):
    downstream = await get_api_python(f"/api/appadmin/branches/{branch_code}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/branches/{branch_code}")
async def update_branch(
    branch_code: str,
    payload: BranchUpdateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.branch.edit")),
):
    body = {
        **payload.model_dump(),
        "user_updated": user_id,
    }
    downstream = await post_api_python(
        f"/api/appadmin/branches/{branch_code}",
        json_body=body,
        method="PUT"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.patch("/branches/{branch_code}/deactivate")
async def deactivate_branch(
    branch_code: str,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.branch.edit")),
):
    body = {"user_updated": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/branches/{branch_code}/deactivate",
        json_body=body,
        method="PATCH"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.patch("/branches/{branch_code}/activate")
async def activate_branch(
    branch_code: str,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.branch.edit")),
):
    body = {"user_updated": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/branches/{branch_code}/activate",
        json_body=body,
        method="PATCH"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================


class UserCreateIn(BaseModel):
    user_id: str
    display_name: str
    password: str
    primary_branch: str
    branch_access: str = "single"
    roles: list[str] = []
    branches: list[str] = []


class UserUpdateIn(BaseModel):
    display_name: str
    primary_branch: str
    branch_access: str = "single"


class UserPasswordIn(BaseModel):
    new_password: str


class UserStatusIn(BaseModel):
    status: str


class UserRolesIn(BaseModel):
    roles: list[str]


class UserBranchesIn(BaseModel):
    branches: list[str]


@router.get("/users")
async def list_users(
    request: Request,
    page: int = 1,
    limit: int = 25,
    keyword: str | None = None,
    status: str | None = None,
    is_locked: bool | None = None,
    user_id: str = Depends(require_menu("appadmin.users")),
):
    params: dict = {"page": page, "limit": limit}
    if keyword:
        params["keyword"] = keyword
    if status:
        params["status"] = status
    if is_locked is not None:
        params["is_locked"] = str(is_locked).lower()
    downstream = await get_api_python("/api/appadmin/users", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/users")
async def create_user(
    payload: UserCreateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.users.create")),
):
    if len(payload.password) < MIN_PASSWORD_LENGTH:
        return JSONResponse(
            status_code=400,
            content={"error": {"code": "WEAK_PASSWORD", "message": f"Password minimal {MIN_PASSWORD_LENGTH} karakter"}, "meta": {}},
        )
    password_hash = bcrypt.hashpw(payload.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    body = {
        "user_id": payload.user_id.strip().upper(),
        "display_name": payload.display_name,
        "password_hash": password_hash,
        "primary_branch": payload.primary_branch,
        "branch_access": payload.branch_access,
        "roles": payload.roles,
        "branches": payload.branches,
        "created_by": user_id,
    }
    downstream = await post_api_python("/api/appadmin/users", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/users/{target_user_id}")
async def get_user(
    target_user_id: str,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.users")),
):
    downstream = await get_api_python(f"/api/appadmin/users/{target_user_id.upper()}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/users/{target_user_id}")
async def update_user(
    target_user_id: str,
    payload: UserUpdateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.users.edit")),
):
    body = {**payload.model_dump(), "updated_by": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/users/{target_user_id.upper()}", json_body=body, method="PUT"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.patch("/users/{target_user_id}/status")
async def update_user_status(
    target_user_id: str,
    payload: UserStatusIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.users.edit")),
):
    body = {**payload.model_dump(), "updated_by": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/users/{target_user_id.upper()}/status", json_body=body, method="PATCH"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/users/{target_user_id}/password")
async def reset_user_password(
    target_user_id: str,
    payload: UserPasswordIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.users.edit")),
):
    if len(payload.new_password) < MIN_PASSWORD_LENGTH:
        return JSONResponse(
            status_code=400,
            content={"error": {"code": "WEAK_PASSWORD", "message": f"Password minimal {MIN_PASSWORD_LENGTH} karakter"}, "meta": {}},
        )
    password_hash = bcrypt.hashpw(payload.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    body = {"password_hash": password_hash}
    downstream = await post_api_python(
        f"/api/appadmin/users/{target_user_id.upper()}/password", json_body=body, method="PUT"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/users/{target_user_id}/roles")
async def update_user_roles(
    target_user_id: str,
    payload: UserRolesIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.users.edit")),
):
    body = {**payload.model_dump(), "updated_by": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/users/{target_user_id.upper()}/roles", json_body=body, method="PUT"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/users/{target_user_id}/branches")
async def update_user_branches(
    target_user_id: str,
    payload: UserBranchesIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.users.edit")),
):
    body = {**payload.model_dump(), "updated_by": user_id}
    downstream = await post_api_python(
        f"/api/appadmin/users/{target_user_id.upper()}/branches", json_body=body, method="PUT"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


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

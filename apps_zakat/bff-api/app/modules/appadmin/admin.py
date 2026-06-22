from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix="/api/appadmin", tags=["appadmin"])


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

from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.appadmin.user import service
from app.modules.appadmin.user.schema import (
    UserBranchesRequest,
    UserCreateRequest,
    UserPasswordRequest,
    UserRolesRequest,
    UserStatusRequest,
    UserUpdateRequest,
)
from app.shared.response import err, ok

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    keyword: str | None = Query(None),
    status: str | None = Query(None),
    is_locked: bool | None = Query(None),
):
    rows, total = await service.list_users(
        page=page, limit=limit, keyword=keyword, status=status, is_locked=is_locked
    )
    return ok({
        "rows": [r.model_dump() for r in rows],
        "pagination": {"page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit},
    })


@router.post("")
async def create_user(payload: UserCreateRequest):
    try:
        result = await service.create_user(payload)
        return ok(result.model_dump())
    except ValueError as e:
        return JSONResponse(status_code=409, content=err("DUPLICATE_USER", str(e)))


@router.get("/{user_id}")
async def get_user(user_id: str):
    result = await service.get_user(user_id.upper())
    if result is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"User '{user_id}' tidak ditemukan"))
    return ok(result.model_dump())


@router.put("/{user_id}")
async def update_user(user_id: str, payload: UserUpdateRequest):
    existing = await service.get_user(user_id.upper())
    if existing is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"User '{user_id}' tidak ditemukan"))
    result = await service.update_user(user_id.upper(), payload)
    return ok(result.model_dump())


@router.patch("/{user_id}/status")
async def update_status(user_id: str, payload: UserStatusRequest):
    existing = await service.get_user(user_id.upper())
    if existing is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"User '{user_id}' tidak ditemukan"))
    result = await service.update_user_status(user_id.upper(), payload)
    return ok(result.model_dump())


@router.put("/{user_id}/password")
async def reset_password(user_id: str, payload: UserPasswordRequest):
    existing = await service.get_user(user_id.upper())
    if existing is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"User '{user_id}' tidak ditemukan"))
    await service.reset_user_password(user_id.upper(), payload)
    return ok({"reset": True})


@router.put("/{user_id}/roles")
async def update_roles(user_id: str, payload: UserRolesRequest):
    existing = await service.get_user(user_id.upper())
    if existing is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"User '{user_id}' tidak ditemukan"))
    result = await service.update_user_roles(user_id.upper(), payload)
    return ok(result.model_dump())


@router.put("/{user_id}/branches")
async def update_branches(user_id: str, payload: UserBranchesRequest):
    existing = await service.get_user(user_id.upper())
    if existing is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"User '{user_id}' tidak ditemukan"))
    result = await service.update_user_branches(user_id.upper(), payload)
    return ok(result.model_dump())

from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.appadmin.role import service
from app.modules.appadmin.role.schema import (
    RoleCreateRequest,
    RoleStatusRequest,
    RoleUpdateRequest,
)
from app.shared.response import err, ok

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("")
async def list_roles(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    keyword: str | None = Query(None),
    status: str | None = Query(None),
):
    rows, total = await service.list_roles(page=page, limit=limit, keyword=keyword, status=status)
    return ok({
        "rows": [r.model_dump() for r in rows],
        "pagination": {"page": page, "limit": limit, "total": total, "total_pages": (total + limit - 1) // limit},
    })


@router.post("")
async def create_role(payload: RoleCreateRequest):
    try:
        result = await service.create_role(payload)
        return ok(result.model_dump())
    except ValueError as e:
        return JSONResponse(status_code=409, content=err("DUPLICATE_ROLE", str(e)))


@router.get("/{role_id}")
async def get_role(role_id: str):
    result = await service.get_role(role_id.upper())
    if result is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"Role '{role_id}' tidak ditemukan"))
    return ok(result.model_dump())


@router.put("/{role_id}")
async def update_role(role_id: str, payload: RoleUpdateRequest):
    existing = await service.get_role(role_id.upper())
    if existing is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"Role '{role_id}' tidak ditemukan"))
    result = await service.update_role(role_id.upper(), payload)
    return ok(result.model_dump())


@router.patch("/{role_id}/status")
async def update_status(role_id: str, payload: RoleStatusRequest):
    existing = await service.get_role(role_id.upper())
    if existing is None:
        return JSONResponse(status_code=404, content=err("NOT_FOUND", f"Role '{role_id}' tidak ditemukan"))
    result = await service.update_role_status(role_id.upper(), payload)
    return ok(result.model_dump())

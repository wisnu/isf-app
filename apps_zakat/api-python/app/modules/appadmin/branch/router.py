"""Branch router — Cabang management endpoints."""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.appadmin.branch import service
from app.modules.appadmin.branch.schema import BranchCreateRequest, BranchUpdateRequest
from app.shared.response import err, ok

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("")
async def list_branches(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    status_aktif: str | None = Query("T"),
    keyword: str | None = Query(None),
):
    """List branches with pagination and filters."""
    rows, total = await service.list_branches(
        page=page,
        limit=limit,
        status_aktif=status_aktif,
        keyword=keyword,
    )
    return ok(
        {
            "rows": [r.model_dump() for r in rows],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit,
            },
        }
    )


@router.get("/parents")
async def list_parent_branches():
    """List parent branches (status_cabang='B' and status_aktif='T')."""
    rows = await service.list_parent_branches()
    return ok({"rows": [r.model_dump() for r in rows]})


@router.post("")
async def create_branch(payload: BranchCreateRequest):
    """Create new branch."""
    try:
        result = await service.create_branch(payload, inputer_id=payload.user_input or "SYSTEM")
        return ok(result.model_dump())
    except ValueError as e:
        return JSONResponse(
            status_code=409,
            content=err("DUPLICATE_CODE", str(e)),
        )


@router.get("/{branch_code}")
async def get_branch(branch_code: str):
    """Get branch detail."""
    result = await service.get_branch(branch_code)
    if result is None:
        return JSONResponse(
            status_code=404,
            content=err("NOT_FOUND", f"Cabang '{branch_code}' tidak ditemukan"),
        )
    return ok(result.model_dump())


@router.put("/{branch_code}")
async def update_branch(branch_code: str, payload: BranchUpdateRequest):
    """Update branch (kode_cabang readonly)."""
    # Check if branch exists
    existing = await service.get_branch(branch_code)
    if existing is None:
        return JSONResponse(
            status_code=404,
            content=err("NOT_FOUND", f"Cabang '{branch_code}' tidak ditemukan"),
        )

    result = await service.update_branch(branch_code, payload)
    return ok(result.model_dump())


@router.patch("/{branch_code}/deactivate")
async def deactivate_branch(branch_code: str):
    """Deactivate branch (set status_aktif='F')."""
    existing = await service.get_branch(branch_code)
    if existing is None:
        return JSONResponse(
            status_code=404,
            content=err("NOT_FOUND", f"Cabang '{branch_code}' tidak ditemukan"),
        )

    result = await service.deactivate_branch(branch_code)
    return ok(result.model_dump())


@router.patch("/{branch_code}/activate")
async def activate_branch(branch_code: str):
    """Activate branch (set status_aktif='T')."""
    existing = await service.get_branch(branch_code)
    if existing is None:
        return JSONResponse(
            status_code=404,
            content=err("NOT_FOUND", f"Cabang '{branch_code}' tidak ditemukan"),
        )

    result = await service.activate_branch(branch_code)
    return ok(result.model_dump())

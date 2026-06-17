"""FastAPI router for Uang Muka Penyerahan (Cash Advance) endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.shared.db import get_pool
from app.shared.response import ok
from . import uang_muka_service
from .uang_muka_schema import (
    UangMukaCreate,
    UangMukaUpdate,
)


router = APIRouter(prefix="/transaksi/uang-muka", tags=["transaksi-uang-muka"])


# ============================================================================
# LIST & DETAIL
# ============================================================================


@router.get("")
async def list_uang_muka(
    page: int = 1,
    limit: int = 25,
    date_from: str = "",
    date_to: str = "",
    employee_id: int = 0,
    authstatus: str = "",
    branch_code: str = "",
):
    """List Uang Muka transactions."""
    async with get_pool().acquire() as db:
        rows, total = await uang_muka_service.list_uang_muka(
            db,
            branch_code=branch_code,
            page=page,
            limit=limit,
            date_from=date_from,
            date_to=date_to,
            employee_id=employee_id,
            authstatus=authstatus,
        )

    return ok({
        "rows": rows,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": -(-total // limit) if total else 0,
        },
    })


@router.get("/lookup/employee")
async def lookup_employee(
    search: str = "",
    branch_code: str = "",
):
    """Lookup employee by name/number."""
    rows = await uang_muka_service.lookup_employee(search=search, branch_code=branch_code)
    return ok({"rows": rows})


@router.get("/lookup/cash-account")
async def lookup_cash_account(
    branch_code: str = "",
):
    """Lookup cash account."""
    rows = await uang_muka_service.lookup_cash_account(branch_code=branch_code)
    return ok({"rows": rows})


@router.get("/lookup/budget")
async def lookup_budget(
    search: str = "",
):
    """Lookup budget."""
    rows = await uang_muka_service.lookup_budget(search=search)
    return ok({"rows": rows})


@router.get("/{transaction_id}")
async def get_uang_muka(
    transaction_id: int,
):
    """Get Uang Muka detail by ID."""
    async with get_pool().acquire() as db:
        row = await uang_muka_service.get_uang_muka_detail(db, transaction_id)
    if not row:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return ok(row)


# ============================================================================
# CREATE / UPDATE / DELETE via Otorisasi
# ============================================================================


@router.post("")
async def create_uang_muka(
    payload: UangMukaCreate,
    request: Request,
):
    """Create new Uang Muka via otorisasi save-and-submit."""
    from app.modules.otorisasi import service as otorisasi_svc

    session = request.state.session
    user_id = session["user_id"]
    branch_code = session.get("primary_branch", "")

    result = await otorisasi_svc.save_and_submit(
        entity_type='uang_muka',
        module='keuangan.transaksi.uang-muka-penyerahan',
        payload=payload.model_dump(),
        user_id=user_id,
        branch_code=branch_code,
    )

    return ok(result)


@router.put("/{transaction_id}")
async def update_uang_muka(
    transaction_id: int,
    payload: UangMukaUpdate,
    request: Request,
):
    raise HTTPException(status_code=501, detail="Not yet implemented")


@router.delete("/{transaction_id}")
async def delete_uang_muka(
    transaction_id: int,
    request: Request,
):
    raise HTTPException(status_code=501, detail="Not yet implemented")

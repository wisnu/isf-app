"""FastAPI router for Uang Muka Pengembalian (Cash Advance Return, CAR)."""
from __future__ import annotations

from fastapi import APIRouter, Request

from app.shared.db import get_pool
from app.shared.response import ok
from . import cash_advance_settlement_service
from .cash_advance_settlement_schema import CashAdvanceSettlementCreate

router = APIRouter(prefix="/transaction/cash-advance-settlement", tags=["cash-advance-settlement"])


@router.get("")
async def list_pengembalian(
    page: int = 1,
    limit: int = 25,
    date_from: str = "",
    date_to: str = "",
    employee_id: int = 0,
    branch_code: str = "",
):
    async with get_pool().acquire() as db:
        rows, total = await cash_advance_settlement_service.list_pengembalian(
            db,
            branch_code=branch_code,
            page=page,
            limit=limit,
            date_from=date_from,
            date_to=date_to,
            employee_id=employee_id,
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


@router.post("")
async def create_pengembalian(
    payload: CashAdvanceSettlementCreate,
    request: Request,
):
    from app.modules.authorization import service as otorisasi_svc

    session = request.state.session
    user_id = session["user_id"]
    branch_code = session.get("primary_branch", "")

    result = await otorisasi_svc.save_and_submit(
        entity_type='uang_muka_pengembalian',
        module='keuangan.transaksi.uang-muka-pengembalian',
        payload=payload.model_dump(),
        user_id=user_id,
        branch_code=branch_code,
    )
    return ok(result)


@router.get("/lookup/open-cash-advance")
async def lookup_open_cash_advance(
    employee_id: int,
    branch_code: str = "",
):
    """List open (belum di-LPJ) CA transactions for a given employee."""
    rows = await cash_advance_settlement_service.lookup_open_cash_advance(
        employee_id=employee_id,
        branch_code=branch_code,
    )
    return ok({"rows": rows})

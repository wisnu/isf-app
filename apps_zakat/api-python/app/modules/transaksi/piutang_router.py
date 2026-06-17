"""FastAPI router for Piutang (Pinjam/Bayar) endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.shared.db import get_pool
from app.shared.response import ok
from . import piutang_service
from .piutang_schema import PiutangCreate


router = APIRouter(prefix="/transaksi/piutang", tags=["transaksi-piutang"])


# ============================================================================
# LIST & DETAIL
# ============================================================================


@router.get("")
async def list_piutang(
    page: int = 1,
    limit: int = 25,
    transaction_type: str = "",
    debtor_type: str = "",
    date_from: str = "",
    date_to: str = "",
    branch_code: str = "",
):
    """List Piutang transactions (Pinjam/Bayar) with optional filters."""
    async with get_pool().acquire() as db:
        rows, total = await piutang_service.list_piutang(
            db,
            branch_code=branch_code,
            page=page,
            limit=limit,
            transaction_type=transaction_type,
            debtor_type=debtor_type,
            date_from=date_from,
            date_to=date_to,
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


@router.get("/debitur/lookup")
async def lookup_debtors(
    q: str = "",
    limit: int = 50,
    branch_code: str = "",
):
    """Lookup debtors by name/code (from DEBTOR_ALL view)."""
    async with get_pool().acquire() as db:
        rows = await piutang_service.lookup_debtors(
            db,
            branch_code=branch_code,
            search=q,
            limit=limit,
        )
    return ok({"rows": rows})


@router.get("/debitur-external/list")
async def list_external_debtors(
    limit: int = 100,
    branch_code: str = "",
):
    """List all external debtors."""
    async with get_pool().acquire() as db:
        rows = await piutang_service.list_external_debtors(
            db,
            branch_code=branch_code,
            limit=limit,
        )
    return ok({"rows": rows})


@router.get("/{transaction_id}")
async def get_piutang(
    transaction_id: int,
):
    """Get Piutang detail by transaction ID."""
    async with get_pool().acquire() as db:
        row = await piutang_service.get_piutang_detail(db, transaction_id)
    if not row:
        raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return ok(row)


# ============================================================================
# CREATE via Otorisasi
# ============================================================================


@router.post("")
async def create_piutang(
    payload: PiutangCreate,
    request: Request,
):
    """Create new Piutang (Pinjam/Bayar) via otorisasi save-and-submit."""
    from app.modules.otorisasi import service as otorisasi_svc

    session = request.state.session
    user_id = session["user_id"]
    branch_code = session.get("primary_branch", "")

    if payload.channel_type == 'C' and not payload.cash_account_no:
        raise HTTPException(status_code=400, detail="Cash account required for channel type C")
    if payload.channel_type == 'G' and not payload.gl_account_code:
        raise HTTPException(status_code=400, detail="GL account required for channel type G")

    result = await otorisasi_svc.save_and_submit(
        entity_type='piutang',
        module='keuangan.piutang.pinjam-bayar',
        payload=payload.model_dump(),
        user_id=user_id,
        branch_code=branch_code,
    )

    return ok(result)

"""FastAPI router for Transfer Antar Rekening (transactioncode='TI') endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, Request

from app.shared.db import get_pool
from app.shared.response import ok
from . import inter_account_transfer_service as svc
from .inter_account_transfer_schema import TransferAntarRekeningCreate

_MENU = 'keuangan.transaksi.transfer-antar-rekening'

router = APIRouter(prefix='/transaksi/transfer-antar-rekening', tags=['transfer-antar-rekening'])


# ── List & Detail ──────────────────────────────────────────────────────────────

@router.get('')
async def list_transfers(
    request: Request,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=200),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    branch_code: str | None = Query(default=None),
):
    async with get_pool().acquire() as db:
        rows, total = await svc.list_transfers(
            db,
            branch_code=branch_code or '',
            page=page,
            limit=limit,
            date_from=date_from or '',
            date_to=date_to or '',
        )
    return ok({
        'rows': rows,
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'total_pages': -(-total // limit) if total else 0,
        },
    })


@router.get('/lookup/cash-accounts')
async def lookup_cash_accounts(
    search: str | None = Query(default=None),
    branch_code: str | None = Query(default=None),
):
    rows = await svc.lookup_cash_accounts(
        search=search or '',
        branch_code=branch_code or '',
    )
    return ok({'rows': rows})


@router.get('/{transaction_id}')
async def get_transfer(
    transaction_id: int,
):
    async with get_pool().acquire() as db:
        row = await svc.get_transfer_detail(db, transaction_id)
    if not row:
        raise HTTPException(status_code=404, detail='Data tidak ditemukan')
    return ok(row)


# ── Create via Otorisasi ───────────────────────────────────────────────────────

@router.post('')
async def create_transfer(
    payload: TransferAntarRekeningCreate,
    request: Request,
):
    """Create Transfer Antar Rekening via otorisasi save-and-submit."""
    from app.modules.authorization import service as otorisasi_svc

    session = request.state.session
    user_id = session['user_id']
    branch_code = session.get('primary_branch', '') or ''

    data = payload.model_dump()
    data['items'] = [{'amount': payload.amount}]

    result = await otorisasi_svc.save_and_submit(
        entity_type='transfer_antar_rekening',
        module=_MENU,
        payload=data,
        user_id=user_id,
        branch_code=branch_code,
    )
    return ok(result)

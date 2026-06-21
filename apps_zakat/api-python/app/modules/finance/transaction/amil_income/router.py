"""FastAPI router for Penerimaan Amil (CI - Cash In Amil)."""
from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.finance.monitoring.authorization import service as otorisasi_service
from app.shared.response import err, ok
from . import service as amil_income_service
from .schema import AmilIncomeCreate

router = APIRouter(prefix='/finance/transaction/amil-income', tags=['amil-income'])


# Lookup endpoints
@router.get('/lookup/kas-account')
async def lookup_kas_account(
    branch_code: str = Query(default=''),
    payment_type: str = Query(default=''),
):
    """Search amil cash/bank accounts (is_amil_account='T', status='A')."""
    rows = await amil_income_service.get_kas_accounts_lookup(
        branch_code=branch_code,
        payment_type=payment_type,
    )
    return ok({'rows': rows})


@router.get('/lookup/gl-account')
async def lookup_gl_account(
    branch_code: str = Query(default=''),
    search: str = Query(default=''),
):
    """Search GL accounts for amil revenue (account_type='I', leaf, 430xxx family)."""
    rows = await amil_income_service.get_gl_accounts_lookup(
        branch_code=branch_code,
        search=search,
    )
    return ok({'rows': rows})


@router.get('/next-number')
async def get_next_number(
    payment_type: str = Query(default='B'),
    branch_code: str = Query(default=''),
    bank_account_no: str = Query(default=''),
):
    """Get next transaction number for CI."""
    result = await amil_income_service.get_next_transaction_number(
        payment_type=payment_type,
        branch_code=branch_code,
        bank_account_no=bank_account_no,
    )
    return ok(result)


@router.get('')
async def list_amil_income(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    branch_code: str = Query(default=''),
    date_from: str = Query(default=''),
    date_to: str = Query(default=''),
):
    """List CI transactions (penerimaan amil) with optional filters."""
    rows, total = await amil_income_service.list_amil_income(
        branch_code=branch_code,
        page=page,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
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


@router.get('/{transaction_id}')
async def get_amil_income(transaction_id: int):
    """Get CI transaction detail with items."""
    row = await amil_income_service.get_amil_income(transaction_id)
    if not row:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Transaksi penerimaan amil {transaction_id} tidak ditemukan'),
        )
    return ok(row)


@router.post('/save-and-submit')
async def create_amil_income(body: AmilIncomeCreate):
    """Create CI transaction via otorisasi save-and-submit.

    Sistem otomatis cek limit:
    - Jika amount <= limit → langsung AUTHORIZED
    - Jika amount > limit → status PENDING (menunggu approval)
    """
    payload = body.model_dump()
    user_id = payload.pop('inputer_id', '') or 'SYSTEM'
    branch_code = payload.pop('branch_code', '') or '001'

    result = await otorisasi_service.save_and_submit(
        entity_type='amil_income',
        module='keuangan',
        payload=payload,
        user_id=user_id,
        branch_code=branch_code,
    )
    return ok({
        'submission_id': result.get('submission_id'),
        'status': result.get('status'),
        'transaction_id': result.get('transaction_id'),
        'message': 'Transaksi disimpan dan menunggu persetujuan' if result.get('status') == 'PENDING'
            else 'Transaksi disimpan dan otomatis disetujui (amount <= limit)',
        'entity_type': 'amil_income',
    })

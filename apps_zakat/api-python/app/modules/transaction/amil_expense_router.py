"""FastAPI router for Pengeluaran Amil (CO - Cash Out Amil)."""
from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.authorization import service as otorisasi_service
from app.shared.response import err, ok
from . import amil_expense_service
from .amil_expense_schema import AmilExpenseCreate

router = APIRouter(prefix='/transaction/amil-expense', tags=['amil-expense'])


# Lookup endpoints
@router.get('/lookup/bank-account')
async def lookup_bank_account(
    branch_code: str = Query(default=''),
):
    """Search all active bank/kas accounts (TANPA isamilaccount filter — DELTA vs amil-income)."""
    rows = await amil_expense_service.get_bank_accounts_lookup(
        branch_code=branch_code,
    )
    return ok({'rows': rows})


@router.get('/lookup/petty-cash-account')
async def lookup_petty_cash_account(
    branch_code: str = Query(default=''),
):
    """Search petty cash accounts for Kas payment type."""
    rows = await amil_expense_service.get_petty_cash_accounts_lookup(
        branch_code=branch_code,
    )
    return ok({'rows': rows})


@router.get('/lookup/gl-account')
async def lookup_gl_account(
    branch_code: str = Query(default=''),
    search: str = Query(default=''),
):
    """Search GL accounts for amil expense (account_type='X', parent='310301')."""
    rows = await amil_expense_service.get_gl_accounts_lookup(
        branch_code=branch_code,
        search=search,
    )
    return ok({'rows': rows})


@router.get('/lookup/budget')
async def lookup_budget(
    search: str = Query(default=''),
):
    """Search budget (kode budget + pemilik) for amil expense grid items."""
    rows = await amil_expense_service.lookup_budget(search=search)
    return ok({'rows': rows})


@router.get('/next-number')
async def get_next_number(
    payment_type: str = Query(default='K'),
    branch_code: str = Query(default=''),
    bank_account_no: str = Query(default=''),
):
    """Get next transaction number for CO."""
    result = await amil_expense_service.get_next_transaction_number(
        payment_type=payment_type,
        branch_code=branch_code,
        bank_account_no=bank_account_no,
    )
    return ok(result)


@router.get('')
async def list_amil_expense(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    branch_code: str = Query(default=''),
    date_from: str = Query(default=''),
    date_to: str = Query(default=''),
):
    """List CO transactions (pengeluaran amil) with optional filters."""
    rows, total = await amil_expense_service.list_amil_expense(
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
async def get_amil_expense(transaction_id: int):
    """Get CO transaction detail with items."""
    row = await amil_expense_service.get_amil_expense(transaction_id)
    if not row:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Transaksi pengeluaran amil {transaction_id} tidak ditemukan'),
        )
    return ok(row)


@router.post('/save-and-submit')
async def create_amil_expense(body: AmilExpenseCreate):
    """Create CO transaction via otorisasi save-and-submit.

    Sistem otomatis cek limit:
    - Jika amount <= limit → langsung AUTHORIZED
    - Jika amount > limit → status PENDING (menunggu approval)
    """
    payload = body.model_dump()
    user_id = payload.pop('inputer_id', '') or 'SYSTEM'
    branch_code = payload.pop('branch_code', '') or '001'

    try:
        result = await otorisasi_service.save_and_submit(
            entity_type='amil_expense',
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
            'entity_type': 'amil_expense',
        })
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=400,
            content=err('CREATE_ERROR', str(exc)),
        )

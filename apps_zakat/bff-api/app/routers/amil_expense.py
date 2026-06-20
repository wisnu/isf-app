"""BFF router for Pengeluaran Amil (CO - Cash Out Amil)."""
from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

router = APIRouter(prefix='/amil-expense', tags=['amil-expense'])

_MENU = 'finance.transactions.amil_expense'
_BASE = '/api/transaction/amil-expense'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@router.get('/')
async def list_amil_expense(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
):
    s = _session(request)
    params: dict = {'page': page, 'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to

    downstream = await get_api_python(_BASE, params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/bank-account')
async def lookup_bank_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    """Proxy lookup rekening bank untuk pengeluaran amil ke api-python.

    DELTA: TIDAK ada filter isamilaccount='T' — semua rekening aktif boleh digunakan.
    """
    s = _session(request)
    params: dict = {}
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python(f'{_BASE}/lookup/bank-account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/petty-cash-account')
async def lookup_petty_cash_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    """Proxy lookup rekening kas kecil untuk pengeluaran amil ke api-python."""
    s = _session(request)
    params: dict = {}
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python(f'{_BASE}/lookup/petty-cash-account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/gl-account')
async def lookup_gl_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup GL account beban amil (310301xxx, account_type='X') ke api-python.

    DELTA: account_type='X' (Expense/Beban), bukan 'I' (Income) seperti amil-income.
    """
    s = _session(request)
    params: dict = {}
    if search:
        params['search'] = search
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python(f'{_BASE}/lookup/gl-account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/budget')
async def lookup_budget(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup budget (kode budget + pemilik) ke api-python."""
    params: dict = {}
    if search:
        params['search'] = search
    downstream = await get_api_python(f'{_BASE}/lookup/budget', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/next-number')
async def next_number(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    payment_type: str = Query(default='K'),
    bank_account_no: str = Query(default=''),
):
    """Get next transaction number (KK-YYYY-branch-cashCode-seq).

    Default payment_type='K' (Kas Kecil) — DELTA vs amil-income default 'B' (Bank).
    """
    s = _session(request)
    params: dict = {'payment_type': payment_type}
    if bank_account_no:
        params['bank_account_no'] = bank_account_no
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python(f'{_BASE}/next-number', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{transaction_id}')
async def get_amil_expense(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'{_BASE}/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/save-and-submit')
async def create_amil_expense(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    """Create & submit pengeluaran amil via otorisasi save-and-submit."""
    s = _session(request)
    body = await request.json()
    body['inputer_id'] = s['user_id']
    body['branch_code'] = s['branch'] or '001'

    url = f"{settings.api_python_base_url}{_BASE}/save-and-submit"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

# NOTE: no PUT/DELETE — amil expense follows the otorisasi maker-checker lifecycle
# (edits/cancels happen via the Otorisasi page on the submission), mirroring amil-income.
# api-python exposes no update/delete endpoints for this entity.

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings
import httpx

fund_collection_router = APIRouter(prefix='/api/finance/transaction/fund-collection', tags=['fund-collection'])

_MENU = 'finance.transactions.fund_collection'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@fund_collection_router.get('/lookup/account')
async def lookup_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    type: str = Query(default='bank'),
):
    s = _session(request)
    params: dict = {'type': type}
    if s['branch']:
        params['branch'] = s['branch']
    downstream = await get_api_python('/api/finance/transaction/fund-collection/lookup/account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_collection_router.get('/lookup/product')
async def lookup_product(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    currency: str = Query(default='IDR'),
):
    s = _session(request)
    params = {'branch_code': s['branch'] or '001', 'currency': currency}
    downstream = await get_api_python('/api/finance/transaction/fund-collection/lookup/product', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_collection_router.get('/lookup/donor')
async def lookup_donor(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    q: str = Query(...),
):
    s = _session(request)
    params: dict = {'q': q}
    if s['branch']:
        params['branch'] = s['branch']
    downstream = await get_api_python('/api/finance/transaction/fund-collection/lookup/donor', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_collection_router.get('/')
async def list_fund_collection(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    s = _session(request)
    params: dict = {'begin': begin, 'end': end, 'page': page, 'page_size': page_size}
    if s['branch']:
        params['branch'] = s['branch']
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/finance/transaction/fund-collection/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_collection_router.get('/{transaction_id}')
async def detail_fund_collection(
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/finance/transaction/fund-collection/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_collection_router.post('/')
async def create_fund_collection(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/finance/transaction/fund-collection/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

fund_distribution_router = APIRouter(prefix='/api/finance/transaction/fund-distribution', tags=['fund-distribution'])

_MENU = 'finance.transactions.fund_distribution'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@fund_distribution_router.get('/lookup/ashnaf')
async def lookup_ashnaf(_: str = Depends(require_menu(_MENU))):
    downstream = await get_api_python('/api/finance/transaction/fund-distribution/lookup/ashnaf')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_distribution_router.get('/lookup/account')
async def lookup_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    type: str = Query(default='bank'),
):
    s = _session(request)
    params: dict = {'type': type}
    if s['branch']:
        params['branch'] = s['branch']
    downstream = await get_api_python('/api/finance/transaction/fund-distribution/lookup/account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_distribution_router.get('/lookup/product')
async def lookup_product(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    currency: str = Query(default='IDR'),
):
    s = _session(request)
    params = {'branch_code': s['branch'] or '001', 'currency': currency}
    downstream = await get_api_python('/api/finance/transaction/fund-distribution/lookup/product', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_distribution_router.get('/lookup/fund-product-account')
async def lookup_fund_product_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    bank_account_no: str = Query(...),
):
    s = _session(request)
    params = {'bank_account_no': bank_account_no, 'branch_code': s['branch'] or '001'}
    downstream = await get_api_python(
        '/api/finance/transaction/fund-distribution/lookup/fund-product-account', params=params
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_distribution_router.get('/')
async def list_fund_distribution(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    s = _session(request)
    params: dict = {'begin': begin, 'end': end, 'page': page, 'page_size': page_size}
    if s['branch']:
        params['branch'] = s['branch']
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/finance/transaction/fund-distribution/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_distribution_router.get('/{transaction_id}')
async def detail_fund_distribution(
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/finance/transaction/fund-distribution/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@fund_distribution_router.post('/')
async def create_fund_distribution(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/finance/transaction/fund-distribution/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

"""BFF router for Penerimaan Amil (CI - Cash In Amil)."""

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

amil_income_router = APIRouter(prefix='/api/finance/transaction/amil-income', tags=['amil-income'])

_MENU = 'finance.transactions.amil_income'
_BASE = '/api/transaction/amil-income'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@amil_income_router.get('/')
async def list_amil_income(
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


@amil_income_router.get('/lookup/kas-account')
async def lookup_kas_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    payment_type: str = Query(default=''),
):
    """Proxy lookup rekening kas/bank amil ke api-python."""
    s = _session(request)
    params: dict = {}
    if payment_type:
        params['payment_type'] = payment_type
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python(f'{_BASE}/lookup/kas-account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@amil_income_router.get('/lookup/gl-account')
async def lookup_gl_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup GL account pendapatan amil (430xxx) ke api-python."""
    s = _session(request)
    params: dict = {}
    if search:
        params['search'] = search
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python(f'{_BASE}/lookup/gl-account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@amil_income_router.get('/next-number')
async def next_number(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    payment_type: str = Query(default='B'),
    bank_account_no: str = Query(default=''),
):
    s = _session(request)
    params: dict = {'payment_type': payment_type}
    if bank_account_no:
        params['bank_account_no'] = bank_account_no
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python(f'{_BASE}/next-number', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@amil_income_router.get('/{transaction_id}')
async def get_amil_income(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'{_BASE}/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@amil_income_router.post('/save-and-submit')
async def create_amil_income(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    body['inputer_id'] = s['user_id']
    body['branch_code'] = s['branch'] or '001'

    url = f"{settings.api_python_base_url}{_BASE}/save-and-submit"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

"""BFF router for Pengeluaran Amil (CO - Cash Out Amil)."""

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

amil_expense_router = APIRouter(prefix='/api/finance/transaction/amil-expense', tags=['amil-expense'])

_MENU = 'finance.transactions.amil_expense'
_BASE = '/api/transaction/amil-expense'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@amil_expense_router.get('/')
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


@amil_expense_router.get('/lookup/bank-account')
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


@amil_expense_router.get('/lookup/petty-cash-account')
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


@amil_expense_router.get('/lookup/gl-account')
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


@amil_expense_router.get('/lookup/budget')
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


@amil_expense_router.get('/next-number')
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


@amil_expense_router.get('/{transaction_id}')
async def get_amil_expense(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'{_BASE}/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@amil_expense_router.post('/save-and-submit')
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

cash_advance_router = APIRouter(prefix='/api/finance/transaction/cash-advance', tags=['cash-advance'])

_MENU = 'finance.transactions.cash_advance'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@cash_advance_router.get('/lookup/employee')
async def lookup_employee(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    s = _session(request)
    params: dict = {'search': search}
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python('/api/finance/transaction/cash-advance/lookup/employee', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@cash_advance_router.get('/lookup/cash-account')
async def lookup_cash_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    params: dict = {}
    if s['branch']:
        params['branch_code'] = s['branch']
    else:
        params['branch_code'] = '001'
    downstream = await get_api_python('/api/finance/transaction/cash-advance/lookup/cash-account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@cash_advance_router.get('/lookup/budget')
async def lookup_budget(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
    actual_date: str = Query(...),
):
    s = _session(request)
    params = {'search': search, 'actual_date': actual_date}
    downstream = await get_api_python('/api/finance/transaction/cash-advance/lookup/budget', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@cash_advance_router.get('/')
async def list_cash_advance(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=200),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    employee_id: int | None = Query(default=None),
    authstatus: str | None = Query(default=None),
):
    s = _session(request)
    params: dict = {'page': page, 'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to
    if employee_id:
        params['employee_id'] = employee_id
    if authstatus:
        params['authstatus'] = authstatus
    downstream = await get_api_python('/api/finance/transaction/cash-advance', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@cash_advance_router.get('/{id}')
async def detail_cash_advance(
    id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/finance/transaction/cash-advance/{id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@cash_advance_router.post('/')
async def create_cash_advance(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/transaction/cash-advance"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

cash_advance_settlement_router = APIRouter(prefix='/api/finance/transaction/cash-advance-settlement', tags=['cash-advance-settlement'])

_MENU = 'finance.transactions.cash_advance_lpj'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@cash_advance_settlement_router.get('/lookup/open-cash-advance')
async def lookup_open_cash_advance(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    employee_id: int = Query(...),
):
    s = _session(request)
    params: dict = {'employee_id': employee_id}
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python('/api/finance/transaction/cash-advance-settlement/lookup/open-cash-advance', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@cash_advance_settlement_router.get('/')
async def list_pengembalian(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=200),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    employee_id: int | None = Query(default=None),
):
    s = _session(request)
    params: dict = {'page': page, 'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to
    if employee_id:
        params['employee_id'] = employee_id
    downstream = await get_api_python('/api/finance/transaction/cash-advance-settlement', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@cash_advance_settlement_router.post('/')
async def create_pengembalian(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/transaction/cash-advance-settlement"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

inter_account_transfer_router = APIRouter(prefix='/api/finance/transaction/inter-account-transfer', tags=['inter-account-transfer'])

_MENU = 'finance.transactions.fund_transfer'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@inter_account_transfer_router.get('/lookup/cash-accounts')
async def lookup_cash_accounts(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str | None = Query(default=None),
):
    s = _session(request)
    params: dict = {}
    if search:
        params['search'] = search
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python('/api/finance/transaction/inter-account-transfer/lookup/cash-accounts', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@inter_account_transfer_router.get('/')
async def list_transfers(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=200),
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
    downstream = await get_api_python('/api/finance/transaction/inter-account-transfer', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@inter_account_transfer_router.get('/{transaction_id}')
async def get_transfer(
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/transaction/inter-account-transfer/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@inter_account_transfer_router.post('/')
async def create_transfer(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/transaction/inter-account-transfer"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params={
            'user_id': s['user_id'],
            'branch_code': s['branch'] or '001',
        })
    return JSONResponse(status_code=resp.status_code, content=resp.json())

"""BFF router for Transaksi Umum (GT - General Transaction)."""

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

general_transaction_router = APIRouter(prefix='/api/finance/transaction/general', tags=['general-transaction'])

_MENU = 'finance.transactions.general'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@general_transaction_router.get('/')
async def list_general_transaction(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    search: str | None = Query(default=None),
):
    s = _session(request)
    params: dict = {'page': page, 'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to
    if search:
        params['search'] = search

    downstream = await get_api_python('/api/transaction/general', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@general_transaction_router.get('/lookup/cash-bank')
async def lookup_cash_bank(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup rekening kas/bank ke api-python."""
    s = _session(request)
    params: dict = {}
    if search:
        params['search'] = search
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python('/api/transaction/general/lookup/cash-bank', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@general_transaction_router.get('/lookup/product')
async def lookup_product(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
    fund_entity: int = Query(default=0),
):
    """Proxy lookup product penghimpunan ke api-python."""
    s = _session(request)
    params: dict = {}
    if search:
        params['search'] = search
    if fund_entity:
        params['fund_entity'] = fund_entity
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python('/api/transaction/general/lookup/product', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@general_transaction_router.get('/lookup/distribution')
async def lookup_distribution(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup program distribution ke api-python."""
    params: dict = {}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/transaction/general/lookup/distribution', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@general_transaction_router.get('/lookup/donor')
async def lookup_donor(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup donor ke api-python."""
    params: dict = {}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/transaction/general/lookup/donor', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@general_transaction_router.get('/{transaction_id}')
async def get_general_transaction(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/transaction/general/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@general_transaction_router.post('/')
async def create_general_transaction(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    body['inputer_id'] = s['user_id']
    body['branch_code'] = s['branch'] or '001'

    url = f"{settings.api_python_base_url}/api/transaction/general"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

receivable_router = APIRouter(prefix='/api/finance/transaction/receivable', tags=['receivable'])

_MENU = 'finance.transactions.receivable'


def _session(request: Request) -> dict:
    """Resolve user_id, branch dari session berdasarkan access type."""
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@receivable_router.get('/')
async def list_receivable(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    transaction_type: str | None = Query(default=None),
    debtor_type: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
):
    """List piutang dengan filter dan pagination."""
    s = _session(request)
    params: dict = {'page': page, 'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if transaction_type:
        params['transaction_type'] = transaction_type
    if debtor_type:
        params['debtor_type'] = debtor_type
    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to

    downstream = await get_api_python('/api/transaction/receivable/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@receivable_router.post('/')
async def create_receivable(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    """Create piutang (pinjam/bayar) via otorisasi save-and-submit."""
    s = _session(request)
    body = await request.json()
    # Inject session data
    body['inputer_id'] = s['user_id']
    body['branch_code'] = s['branch'] or '001'

    url = f"{settings.api_python_base_url}/api/transaction/receivable/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@receivable_router.put('/{transaction_no}')
async def update_receivable(
    request: Request,
    transaction_no: str,
    _: str = Depends(require_menu(_MENU)),
):
    """Update piutang (cancel old + create new via otorisasi)."""
    s = _session(request)
    body = await request.json()
    # Inject session data
    body['inputer_id'] = s['user_id']
    body['branch_code'] = s['branch'] or '001'

    url = f"{settings.api_python_base_url}/api/transaction/receivable/{transaction_no}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.put(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@receivable_router.get('/debtor/')
async def lookup_debtor(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    q: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    """Lookup debtor (karyawan + eksternal) untuk form selection."""
    s = _session(request)
    params: dict = {'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if q:
        params['q'] = q

    downstream = await get_api_python('/api/transaction/receivable/debtor/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@receivable_router.get('/debtor-external/')
async def list_debtor_external(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    q: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    """List debtor eksternal."""
    s = _session(request)
    params: dict = {'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if q:
        params['q'] = q

    downstream = await get_api_python('/api/transaction/receivable/debtor-external/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
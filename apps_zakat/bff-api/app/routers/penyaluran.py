from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

router = APIRouter(prefix='/penyaluran', tags=['penyaluran'])

_MENU = 'finance.transactions.fund_distribution'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@router.get('/lookup/ashnaf')
async def lookup_ashnaf(_: str = Depends(require_menu(_MENU))):
    downstream = await get_api_python('/api/transaction/penyaluran/lookup/ashnaf')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/rekening')
async def lookup_rekening(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    type: str = Query(default='bank'),
):
    s = _session(request)
    params: dict = {'type': type}
    if s['branch']:
        params['branch'] = s['branch']
    downstream = await get_api_python('/api/transaction/penyaluran/lookup/rekening', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/produk')
async def lookup_produk(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    currency: str = Query(default='IDR'),
):
    s = _session(request)
    params = {'branch_code': s['branch'] or '001', 'currency': currency}
    downstream = await get_api_python('/api/transaction/penyaluran/lookup/produk', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/fund-product-account')
async def lookup_fund_product_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    bank_account_no: str = Query(...),
):
    s = _session(request)
    params = {'bank_account_no': bank_account_no, 'branch_code': s['branch'] or '001'}
    downstream = await get_api_python(
        '/api/transaction/penyaluran/lookup/fund-product-account', params=params
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/')
async def list_penyaluran(
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
    downstream = await get_api_python('/api/transaction/penyaluran/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{transaction_id}')
async def detail_penyaluran(
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/transaction/penyaluran/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/')
async def create_penyaluran(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/transaction/penyaluran/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

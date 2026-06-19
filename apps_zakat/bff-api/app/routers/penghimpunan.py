from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

router = APIRouter(prefix='/penghimpunan', tags=['penghimpunan'])

_MENU = 'finance.transactions.fund_collection'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


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
    downstream = await get_api_python('/api/transaction/penghimpunan/lookup/rekening', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/produk')
async def lookup_produk(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    currency: str = Query(default='IDR'),
):
    s = _session(request)
    params = {'branch_code': s['branch'] or '001', 'currency': currency}
    downstream = await get_api_python('/api/transaction/penghimpunan/lookup/produk', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/donor')
async def lookup_donor(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    q: str = Query(...),
):
    s = _session(request)
    params: dict = {'q': q}
    if s['branch']:
        params['branch'] = s['branch']
    downstream = await get_api_python('/api/transaction/penghimpunan/lookup/donor', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/')
async def list_penghimpunan(
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
    downstream = await get_api_python('/api/transaction/penghimpunan/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{transaction_id}')
async def detail_penghimpunan(
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/transaction/penghimpunan/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/')
async def create_penghimpunan(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/transaction/penghimpunan/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

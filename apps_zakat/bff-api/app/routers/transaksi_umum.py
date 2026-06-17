"""BFF router for Transaksi Umum (GT - General Transaction)."""
from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

router = APIRouter(prefix='/transaksi-umum', tags=['transaksi-umum'])

_MENU = 'keuangan.transaksi.umum'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@router.get('/')
async def list_transaksi_umum(
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

    downstream = await get_api_python('/api/transaksi/umum', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/kasbank')
async def lookup_kasbank(
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
    downstream = await get_api_python('/api/transaksi/umum/lookup/kasbank', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/produk')
async def lookup_produk(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
    fund_entity: int = Query(default=0),
):
    """Proxy lookup produk penghimpunan ke api-python."""
    s = _session(request)
    params: dict = {}
    if search:
        params['search'] = search
    if fund_entity:
        params['fund_entity'] = fund_entity
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python('/api/transaksi/umum/lookup/produk', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/penyaluran')
async def lookup_penyaluran(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup program penyaluran ke api-python."""
    params: dict = {}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/transaksi/umum/lookup/penyaluran', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/donor')
async def lookup_donor(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    """Proxy lookup donor ke api-python."""
    params: dict = {}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/transaksi/umum/lookup/donor', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{transaction_id}')
async def get_transaksi_umum(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/transaksi/umum/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/')
async def create_transaksi_umum(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    body['inputer_id'] = s['user_id']
    body['branch_code'] = s['branch'] or '001'

    url = f"{settings.api_python_base_url}/api/transaksi/umum"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

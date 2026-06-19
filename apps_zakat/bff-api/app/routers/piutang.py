from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

router = APIRouter(prefix='/piutang', tags=['piutang'])

_MENU = 'finance.transactions.receivable'


def _session(request: Request) -> dict:
    """Resolve user_id, branch dari session berdasarkan access type."""
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@router.get('/')
async def list_piutang(
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

    downstream = await get_api_python('/api/transaksi/piutang/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/')
async def create_piutang(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    """Create piutang (pinjam/bayar) via otorisasi save-and-submit."""
    s = _session(request)
    body = await request.json()
    # Inject session data
    body['inputer_id'] = s['user_id']
    body['branch_code'] = s['branch'] or '001'

    url = f"{settings.api_python_base_url}/api/transaksi/piutang/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.put('/{transaction_no}')
async def update_piutang(
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

    url = f"{settings.api_python_base_url}/api/transaksi/piutang/{transaction_no}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.put(url, json=body)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/debitur/')
async def lookup_debitur(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    q: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    """Lookup debitur (karyawan + eksternal) untuk form selection."""
    s = _session(request)
    params: dict = {'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if q:
        params['q'] = q

    downstream = await get_api_python('/api/transaksi/piutang/debitur/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/debitur-external/')
async def list_debitur_external(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    q: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
):
    """List debitur eksternal."""
    s = _session(request)
    params: dict = {'limit': limit}
    if s['branch']:
        params['branch_code'] = s['branch']
    if q:
        params['q'] = q

    downstream = await get_api_python('/api/transaksi/piutang/debitur-external/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

router = APIRouter(prefix='/transaksi/uang-muka', tags=['uang-muka'])

_MENU = 'finance.transactions.cash_advance'


def _session(request: Request) -> dict:
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@router.get('/lookup/employee')
async def lookup_employee(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
):
    s = _session(request)
    params: dict = {'search': search}
    if s['branch']:
        params['branch_code'] = s['branch']
    downstream = await get_api_python('/api/transaksi/uang-muka/lookup/employee', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/cash-account')
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
    downstream = await get_api_python('/api/transaksi/uang-muka/lookup/cash-account', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/budget')
async def lookup_budget(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str = Query(default=''),
    actual_date: str = Query(...),
):
    s = _session(request)
    params = {'search': search, 'actual_date': actual_date}
    downstream = await get_api_python('/api/transaksi/uang-muka/lookup/budget', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/')
async def list_uang_muka(
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
    downstream = await get_api_python('/api/transaksi/uang-muka', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{id}')
async def detail_uang_muka(
    id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/transaksi/uang-muka/{id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/')
async def create_uang_muka(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/transaksi/uang-muka"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())

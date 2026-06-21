from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, Response

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python, stream_api_python

router = APIRouter(prefix='/api/finance/inquiry/transaction-history', tags=['transaction-history'])

_MENU = 'finance.transactions.history'
_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def _inject(request: Request) -> dict:
    """Derive is_spv, user_id, branch from session."""
    roles = request.session.get('roles') or []
    is_spv = 'SPVKEU' in roles
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'is_spv': is_spv, 'user_id': user_id, 'branch': branch}


@router.get('/search')
async def search(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    inj = _inject(request)
    params: dict = {
        'begin': begin, 'end': end, 'date_type': date_type,
        'sort_by': sort_by, 'search_category': search_category,
        'page': page, 'page_size': page_size,
        'is_spv': str(inj['is_spv']).lower(),
        'user_id': inj['user_id'],
    }
    if inj['branch']:
        params['branch'] = inj['branch']
    if search_text:
        params['search_text'] = search_text
    if cash_account_no:
        params['cash_account_no'] = cash_account_no
    downstream = await get_api_python('/api/finance/inquiry/transaction-history/search', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/search/export.xlsx')
async def search_export(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
):
    inj = _inject(request)
    params: dict = {
        'begin': begin, 'end': end, 'date_type': date_type,
        'sort_by': sort_by, 'search_category': search_category,
        'is_spv': str(inj['is_spv']).lower(), 'user_id': inj['user_id'],
    }
    if inj['branch']:
        params['branch'] = inj['branch']
    if search_text:
        params['search_text'] = search_text
    if cash_account_no:
        params['cash_account_no'] = cash_account_no
    downstream = await stream_api_python(
        '/api/transaction-history/search/export.xlsx', params=params
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    fname = f'histori-transaksi-{begin}-{end}.xlsx'
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': f'attachment; filename="{fname}"'},
    )


@router.get('/transactions/{transaction_id}')
async def get_detail(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(
        f'/api/transaction-history/transactions/{transaction_id}'
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/transactions/{transaction_id}/delete')
async def do_delete(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    inj = _inject(request)
    downstream = await post_api_python(
        f'/api/transaction-history/transactions/{transaction_id}/delete',
        json_body={
            'user_id': inj['user_id'],
            'branch_code': inj['branch'],
            'is_spv': inj['is_spv'],
        },
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/transactions/{transaction_id}/repost')
async def do_repost(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    inj = _inject(request)
    downstream = await post_api_python(
        f'/api/transaction-history/transactions/{transaction_id}/repost',
        json_body={
            'user_id': inj['user_id'],
            'branch_code': inj['branch'],
            'is_spv': inj['is_spv'],
        },
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

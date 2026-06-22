from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(
    prefix='/api/distribution/realization-return',
    tags=['realization-return'],
)

_MENU_KEY = 'distribution.realization-return.list'


def _resolve_branch(request: Request) -> str | None:
    access = request.session.get('branch_access', 'single')
    if access == 'all':
        return None
    return request.session.get('primary_branch') or ''


@router.get('/lookup/cost-items')
async def lookup_cost_items(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/distribution/realization-return/lookup/cost-items')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/realizations')
async def lookup_realizations(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
    search: str | None = Query(default=None),
    realization_type: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    if realization_type:
        params['realization_type'] = realization_type
    downstream = await get_api_python('/api/distribution/realization-return/lookup/realizations', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/realization/{realization_id}/details')
async def get_realization_details(
    request: Request,
    realization_id: int,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/realization-return/realization/{realization_id}/details')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('')
async def list_realization_returns(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
    begin_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    branch_code: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch = _resolve_branch(request)
    params: dict = {'page': page, 'page_size': page_size}
    if begin_date:
        params['begin_date'] = begin_date
    if end_date:
        params['end_date'] = end_date
    if branch is not None:
        params['branch_code'] = branch
    elif branch_code:
        params['branch_code'] = branch_code
    downstream = await get_api_python('/api/distribution/realization-return', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{return_id}')
async def get_realization_return(
    request: Request,
    return_id: int,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/realization-return/{return_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('', status_code=201)
async def create_realization_return(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    branch = _resolve_branch(request)
    if branch is not None:
        body['branch_code'] = branch
    body['user_input'] = request.session.get('username', '')
    downstream = await post_api_python('/api/distribution/realization-return', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put('/{return_id}')
async def update_realization_return(
    request: Request,
    return_id: int,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/realization-return/{return_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete('/{return_id}')
async def delete_realization_return(
    request: Request,
    return_id: int,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/realization-return/{return_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

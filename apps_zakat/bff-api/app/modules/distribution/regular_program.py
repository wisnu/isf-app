from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix='/api/distribution/regular-program', tags=['regular-program'])

_MENU = 'distribution.program.regular'


def _resolve_branch(request: Request) -> str | None:
    access = request.session.get('branch_access', 'single')
    if access == 'all':
        return None
    return request.session.get('primary_branch') or ''


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get('/lookup/products')
async def lookup_products(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/distribution/regular-program/lookup/products')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/mustahiq')
async def lookup_mustahiq(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str | None = Query(default=None),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/regular-program/lookup/mustahiq', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── List + Detail ─────────────────────────────────────────────────────────────

@router.get('')
async def list_regular_programs(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    product_id: int | None = Query(default=None),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch = _resolve_branch(request)
    params: dict = {'page': page, 'page_size': page_size}
    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to
    if branch is not None:
        params['branch_code'] = branch
    if product_id is not None:
        params['product_id'] = product_id
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/regular-program', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{program_id}')
async def get_regular_program(
    request: Request,
    program_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/regular-program/{program_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Create / Update / Delete ──────────────────────────────────────────────────

@router.post('', status_code=201)
async def create_regular_program(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    branch = _resolve_branch(request)
    if branch is not None:
        body['branch_code'] = branch
    downstream = await post_api_python('/api/distribution/regular-program', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put('/{program_id}')
async def update_regular_program(
    request: Request,
    program_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/regular-program/{program_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete('/{program_id}')
async def delete_regular_program(
    request: Request,
    program_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/regular-program/{program_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

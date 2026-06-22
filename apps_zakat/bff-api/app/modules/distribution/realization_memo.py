from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

regular_router = APIRouter(
    prefix='/api/distribution/realization-memo/regular',
    tags=['realization-memo-regular'],
)
non_regular_router = APIRouter(
    prefix='/api/distribution/realization-memo/non-regular',
    tags=['realization-memo-non-regular'],
)

_MENU_REGULAR = 'distribution.program.memo-regular'
_MENU_NON_REGULAR = 'distribution.program.memo-non-regular'


def _resolve_branch(request: Request) -> str | None:
    access = request.session.get('branch_access', 'single')
    if access == 'all':
        return None
    return request.session.get('primary_branch') or ''


def _make_routes(router: APIRouter, api_prefix: str, menu_key: str) -> None:

    @router.get('/lookup/programs')
    async def _lookup_programs(
        request: Request,
        _: str = Depends(require_menu(menu_key)),
        search: str | None = Query(default=None),
    ):
        _, err_resp = await current_user_id_or_401(request)
        if err_resp:
            return err_resp
        params: dict = {}
        if search:
            params['search'] = search
        downstream = await get_api_python(f'/api/{api_prefix}/lookup/programs', params=params)
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    @router.get('')
    async def _list(
        request: Request,
        _: str = Depends(require_menu(menu_key)),
        date_from: str | None = Query(default=None),
        date_to: str | None = Query(default=None),
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
        if search:
            params['search'] = search
        downstream = await get_api_python(f'/api/{api_prefix}', params=params)
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    @router.get('/{memo_id}')
    async def _get(
        request: Request,
        memo_id: int,
        _: str = Depends(require_menu(menu_key)),
    ):
        _, err_resp = await current_user_id_or_401(request)
        if err_resp:
            return err_resp
        downstream = await get_api_python(f'/api/{api_prefix}/{memo_id}')
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    @router.post('', status_code=201)
    async def _create(
        request: Request,
        _: str = Depends(require_menu(menu_key)),
    ):
        user_id, err_resp = await current_user_id_or_401(request)
        if err_resp:
            return err_resp
        body = await request.json()
        branch = _resolve_branch(request)
        if branch is not None:
            body['branch_code'] = branch
        downstream = await post_api_python(f'/api/{api_prefix}', json_body=body)
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    @router.put('/{memo_id}')
    async def _update(
        request: Request,
        memo_id: int,
        _: str = Depends(require_menu(menu_key)),
    ):
        _, err_resp = await current_user_id_or_401(request)
        if err_resp:
            return err_resp
        body = await request.json()
        downstream = await post_api_python(
            f'/api/{api_prefix}/{memo_id}',
            json_body=body,
            method='PUT',
        )
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    @router.delete('/{memo_id}')
    async def _delete(
        request: Request,
        memo_id: int,
        _: str = Depends(require_menu(menu_key)),
    ):
        _, err_resp = await current_user_id_or_401(request)
        if err_resp:
            return err_resp
        downstream = await post_api_python(
            f'/api/{api_prefix}/{memo_id}',
            json_body={},
            method='DELETE',
        )
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())


_make_routes(regular_router,     'distribution/realization-memo/regular',     _MENU_REGULAR)
_make_routes(non_regular_router, 'distribution/realization-memo/non-regular', _MENU_NON_REGULAR)

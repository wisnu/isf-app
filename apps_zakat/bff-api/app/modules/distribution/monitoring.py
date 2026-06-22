from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(
    prefix='/api/distribution/monitoring-visits',
    tags=['monitoring-visits'],
)

_MENU_KEY = 'distribution.monitoring.list'


@router.get('/lookup/mustahiq')
async def lookup_mustahiq(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
    search: str | None = Query(default=None),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/monitoring-visits/lookup/mustahiq', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/programs')
async def lookup_programs(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
    mustahiq_id: int | None = Query(default=None),
    search: str | None = Query(default=None),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {}
    if mustahiq_id:
        params['mustahiq_id'] = mustahiq_id
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/monitoring-visits/lookup/programs', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('')
async def list_monitoring_visits(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
    begin_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if begin_date:
        params['begin_date'] = begin_date
    if end_date:
        params['end_date'] = end_date
    downstream = await get_api_python('/api/distribution/monitoring-visits', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{visit_id}')
async def get_monitoring_visit(
    request: Request,
    visit_id: int,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/monitoring-visits/{visit_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('', status_code=201)
async def create_monitoring_visit(
    request: Request,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python('/api/distribution/monitoring-visits', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put('/{visit_id}')
async def update_monitoring_visit(
    request: Request,
    visit_id: int,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/monitoring-visits/{visit_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete('/{visit_id}')
async def delete_monitoring_visit(
    request: Request,
    visit_id: int,
    _: str = Depends(require_menu(_MENU_KEY)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/monitoring-visits/{visit_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix='/api/distribution/partner', tags=['partner'])
_MENU = 'distribution.partner.list'


@router.get('')
async def list_partners(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/partner', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{partner_id}')
async def get_partner(
    request: Request,
    partner_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/partner/{partner_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('', status_code=201)
async def create_partner(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python('/api/distribution/partner', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put('/{partner_id}')
async def update_partner(
    request: Request,
    partner_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/partner/{partner_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete('/{partner_id}')
async def delete_partner(
    request: Request,
    partner_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/partner/{partner_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

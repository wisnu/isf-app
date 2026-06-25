from __future__ import annotations

import urllib.parse

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

_MENU = 'fundraising.donation.bsz'

router = APIRouter(
    prefix='/api/fundraising/bsz',
    tags=['fundraising-bsz'],
)


# ── GET /api/fundraising/bsz/zakat-objects ────────────────────────────────────
@router.get('/zakat-objects')
async def get_zakat_objects(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/fundraising/bsz/zakat-objects')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── GET /api/fundraising/bsz/available-transactions ───────────────────────────
@router.get('/available-transactions')
async def get_available_transactions(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    donor_id: int = Query(...),
    begin_date: str = Query(...),
    end_date: str = Query(...),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(
        '/api/fundraising/bsz/available-transactions',
        params={'donor_id': donor_id, 'begin_date': begin_date, 'end_date': end_date},
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── GET /api/fundraising/bsz ──────────────────────────────────────────────────
@router.get('')
async def list_bsz(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    donor_id: int | None = Query(default=None),
    begin_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=200),
    page: int = Query(default=1, ge=1),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    raw_params: dict = {'page': page, 'limit': limit}
    if donor_id is not None:
        raw_params['donor_id'] = donor_id
    if begin_date:
        raw_params['begin_date'] = begin_date
    if end_date:
        raw_params['end_date'] = end_date
    downstream = await get_api_python('/api/fundraising/bsz', params=raw_params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── GET /api/fundraising/bsz/{bsz_id} ────────────────────────────────────────
@router.get('/{bsz_id}')
async def get_bsz(
    request: Request,
    bsz_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/fundraising/bsz/{bsz_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── POST /api/fundraising/bsz ─────────────────────────────────────────────────
@router.post('')
async def create_bsz(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python('/api/fundraising/bsz', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── DELETE /api/fundraising/bsz/{bsz_id} ─────────────────────────────────────
@router.delete('/{bsz_id}')
async def delete_bsz(
    request: Request,
    bsz_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/fundraising/bsz/{bsz_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

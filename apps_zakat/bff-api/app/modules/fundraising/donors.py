from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

_CORP_MENU = 'fundraising.donor.corporate'
_IND_MENU = 'fundraising.donor.individual'

corporate_router = APIRouter(
    prefix='/api/fundraising/donors/corporate',
    tags=['fundraising-donor-corporate'],
)

individual_router = APIRouter(
    prefix='/api/fundraising/donors/individual',
    tags=['fundraising-donor-individual'],
)

lookup_router = APIRouter(
    prefix='/api/fundraising/donors',
    tags=['fundraising-donor-lookup'],
)


def _resolve_branch(request: Request) -> str | None:
    access = request.session.get('branch_access', 'single')
    if access == 'all':
        return None
    return request.session.get('primary_branch') or ''


# ── Lookups ───────────────────────────────────────────────────────────────────

@lookup_router.get('/lookup/provinces')
async def lookup_provinces(request: Request):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/fundraising/donors/lookup/provinces')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@lookup_router.get('/lookup/countries')
async def lookup_countries(request: Request):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/fundraising/donors/lookup/countries')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@lookup_router.get('/lookup/marketers')
async def lookup_marketers(request: Request):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/fundraising/donors/lookup/marketers')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@lookup_router.get('/lookup/field-of-work')
async def lookup_field_of_work(request: Request):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/fundraising/donors/lookup/field-of-work')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@lookup_router.get('/lookup/work-areas')
async def lookup_work_areas(request: Request):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/fundraising/donors/lookup/work-areas')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Corporate ─────────────────────────────────────────────────────────────────

@corporate_router.get('')
async def list_corporate(
    request: Request,
    _: str = Depends(require_menu(_CORP_MENU)),
    search: str | None = Query(default=None),
    search_by: str | None = Query(default=None),
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    if search_by:
        params['search_by'] = search_by
    if status:
        params['status'] = status
    downstream = await get_api_python('/api/fundraising/donors/corporate', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.get('/{donor_id}')
async def get_corporate(
    request: Request,
    donor_id: int,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/fundraising/donors/corporate/{donor_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.post('', status_code=201)
async def create_corporate(
    request: Request,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch = _resolve_branch(request)
    body = await request.json()
    if branch is not None:
        body['branch_code'] = branch
    downstream = await post_api_python('/api/fundraising/donors/corporate', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.put('/{donor_id}')
async def update_corporate(
    request: Request,
    donor_id: int,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/fundraising/donors/corporate/{donor_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.patch('/{donor_id}/status')
async def toggle_corporate_status(
    request: Request,
    donor_id: int,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/fundraising/donors/corporate/{donor_id}/status',
        json_body=body,
        method='PATCH',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Individual ────────────────────────────────────────────────────────────────

@individual_router.get('')
async def list_individual(
    request: Request,
    _: str = Depends(require_menu(_IND_MENU)),
    search: str | None = Query(default=None),
    search_by: str | None = Query(default=None),
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    if search_by:
        params['search_by'] = search_by
    if status:
        params['status'] = status
    downstream = await get_api_python('/api/fundraising/donors/individual', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@individual_router.get('/{donor_id}')
async def get_individual(
    request: Request,
    donor_id: int,
    _: str = Depends(require_menu(_IND_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/fundraising/donors/individual/{donor_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@individual_router.post('', status_code=201)
async def create_individual(
    request: Request,
    _: str = Depends(require_menu(_IND_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch = _resolve_branch(request)
    body = await request.json()
    if branch is not None:
        body['branch_code'] = branch
    downstream = await post_api_python('/api/fundraising/donors/individual', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@individual_router.put('/{donor_id}')
async def update_individual(
    request: Request,
    donor_id: int,
    _: str = Depends(require_menu(_IND_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/fundraising/donors/individual/{donor_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@individual_router.patch('/{donor_id}/status')
async def toggle_individual_status(
    request: Request,
    donor_id: int,
    _: str = Depends(require_menu(_IND_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/fundraising/donors/individual/{donor_id}/status',
        json_body=body,
        method='PATCH',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix='/api/distribution/proposal', tags=['proposal'])

_MENU = 'distribution.proposal.list'


def _resolve_branch(request: Request) -> str | None:
    """Return primary_branch if single-access, empty string if all-access."""
    access = request.session.get('branch_access', 'single')
    if access == 'all':
        return None
    return request.session.get('primary_branch') or ''


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get('/lookup/product-groups')
async def lookup_product_groups(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/distribution/proposal/lookup/product-groups')
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
    downstream = await get_api_python('/api/distribution/proposal/lookup/mustahiq', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/total-by-mustahiq')
async def total_by_mustahiq(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    mustahiq_id: int = Query(...),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(
        '/api/distribution/proposal/total-by-mustahiq',
        params={'mustahiq_id': mustahiq_id},
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── List + Detail ─────────────────────────────────────────────────────────────

@router.get('')
async def list_proposals(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    status: str | None = Query(default=None),
    mustahiq_id: int | None = Query(default=None),
    product_group_id: int | None = Query(default=None),
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
    if status:
        params['status'] = status
    if mustahiq_id is not None:
        params['mustahiq_id'] = mustahiq_id
    if product_group_id is not None:
        params['product_group_id'] = product_group_id
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/proposal', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{proposal_id}')
async def get_proposal(
    request: Request,
    proposal_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/proposal/{proposal_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Create / Update / Delete ──────────────────────────────────────────────────

@router.post('', status_code=201)
async def create_proposal(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    # Inject branch_code from session
    branch = _resolve_branch(request)
    if branch is not None:
        body['branch_code'] = branch
    downstream = await post_api_python('/api/distribution/proposal', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put('/{proposal_id}')
async def update_proposal(
    request: Request,
    proposal_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/proposal/{proposal_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete('/{proposal_id}')
async def delete_proposal(
    request: Request,
    proposal_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/proposal/{proposal_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

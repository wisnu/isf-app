from __future__ import annotations

import urllib.parse

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import (
    get_api_python, post_api_python, stream_api_python,
)

_MENU = 'fundraising.donation.confirm'

router = APIRouter(
    prefix='/api/fundraising/donation-confirm',
    tags=['fundraising-donation-confirm'],
)


def _resolve_branch(request: Request) -> str | None:
    """Resolve branch_code dari session.
    - Jika branch_access='all', return None (api-python decide)
    - Jika branch_access='single', return primary_branch
    """
    access = request.session.get('branch_access', 'single')
    if access == 'all':
        return None
    return request.session.get('primary_branch') or ''


# ── GET /api/fundraising/donation-confirm ────────────────────────────────────
# List unconfirmed donations dengan filter
@router.get('')
async def list_donation_confirm(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    branch_code: str | None = Query(default=None),
    is_all_branch: bool | None = Query(default=None),
    search_category: str | None = Query(default=None),
    search_text: str | None = Query(default=None),
    amount_from: float | None = Query(default=None),
    amount_to: float | None = Query(default=None),
    description: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=500),
    page: int = Query(default=1, ge=1),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    # Build params dict
    params: dict = {'page': page, 'limit': limit}

    # Inject branch_code dari session jika single-branch access
    resolved_branch = _resolve_branch(request)
    if resolved_branch is not None:
        params['branch_code'] = resolved_branch
    elif branch_code:
        params['branch_code'] = branch_code

    # Add filter params if provided
    if begin_date:
        params['begin_date'] = begin_date
    if end_date:
        params['end_date'] = end_date
    if is_all_branch is not None:
        params['is_all_branch'] = is_all_branch
    if search_category:
        params['search_category'] = search_category
    if search_text:
        params['search_text'] = search_text
    if amount_from is not None:
        params['amount_from'] = amount_from
    if amount_to is not None:
        params['amount_to'] = amount_to
    if description:
        params['description'] = description

    downstream = await get_api_python('/api/fundraising/donation-confirm', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── DELETE /api/fundraising/donation-confirm/{transaction_id} ─────────────────
# Delete unconfirmed donation transaction
@router.delete('/{transaction_id}')
async def delete_donation_confirm(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    # Inject user branch info as query params for validation
    branch_code = _resolve_branch(request)
    branch_access = request.session.get('branch_access', 'single')
    roles = request.session.get('roles', [])

    qs_params: dict = {'user_branch_access': branch_access}
    if branch_code is not None:
        qs_params['user_branch_code'] = branch_code
    if roles:
        qs_params['user_roles'] = ','.join(roles)

    qs = urllib.parse.urlencode(qs_params)
    downstream = await post_api_python(
        f'/api/fundraising/donation-confirm/{transaction_id}?{qs}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── POST /api/fundraising/donation-confirm/{transaction_id}/post-journal ──────
# Post journal entries for confirmed donation
@router.post('/{transaction_id}/post-journal')
async def post_journal_donation_confirm(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    # Body can be empty or contain journal config
    try:
        body = await request.json()
    except Exception:
        body = {}

    downstream = await post_api_python(
        f'/api/fundraising/donation-confirm/{transaction_id}/post-journal',
        json_body=body,
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── GET /api/fundraising/donation-confirm/{transaction_id}/receipt ────────────
# Stream receipt file (PDF/binary)
@router.get('/{transaction_id}/receipt')
async def receipt_donation_confirm(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    # Stream binary response from api-python
    downstream = await stream_api_python(
        f'/api/fundraising/donation-confirm/{transaction_id}/receipt',
    )

    if downstream.status_code >= 400:
        return JSONResponse(
            status_code=downstream.status_code,
            content=downstream.json(),
        )

    # Return streamed binary response (PDF/file)
    return StreamingResponse(
        iter([downstream.content]),
        status_code=downstream.status_code,
        media_type=downstream.headers.get('content-type', 'application/octet-stream'),
        headers={
            'Content-Disposition': downstream.headers.get('Content-Disposition', ''),
        } if downstream.headers.get('Content-Disposition') else {},
    )


# ── PUT /api/fundraising/donation-confirm/{transaction_item_id}/donor ────────
# Update donor info for a donation item
@router.put('/{transaction_item_id}/donor')
async def update_donor_donation_confirm(
    request: Request,
    transaction_item_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    body = await request.json()

    downstream = await post_api_python(
        f'/api/fundraising/donation-confirm/{transaction_item_id}/donor',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

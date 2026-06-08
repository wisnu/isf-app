from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import AppHTTPError, require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings
from app.shared.response import err, ok

router = APIRouter(prefix='/otorisasi', tags=['otorisasi'])

_ENTITY_MENU: dict[str, str] = {
    'penghimpunan':        'keuangan.transaksi.penghimpunan',
    'penyaluran':          'keuangan.transaksi.penyaluran',
    'upload_penghimpunan': 'keuangan.upload.penghimpunan',
    'coa':                 'keuangan.coa',
    'kas':                 'keuangan.kas',
    'bank':                'keuangan.bank',
}
_MENU_MONITORING = 'keuangan.monitoring.otorisasi'


def _session(request: Request) -> dict:
    return {
        'user_id': request.session.get('user_id', ''),
        'branch': '' if request.session.get('branch_access') == 'all'
                  else (request.session.get('primary_branch') or ''),
        'branch_access': request.session.get('branch_access', 'single'),
    }


async def _check_dynamic_menu(request: Request, entity_type: str) -> None:
    """Resolve entity_type → menu_key, then run require_menu check inline."""
    menu_key = _ENTITY_MENU.get(entity_type)
    if not menu_key:
        raise AppHTTPError(
            status_code=422,
            content=err('VALIDATION_ERROR', f"entity_type tidak dikenal: '{entity_type}'"),
        )
    # require_menu returns an async callable — call it directly
    checker = require_menu(menu_key)
    await checker(request)


# ---------------------------------------------------------------------------
# Fixed-menu endpoints (monitoring)
# ---------------------------------------------------------------------------

@router.get('/pending/')
async def list_pending(
    request: Request,
    _: str = Depends(require_menu(_MENU_MONITORING)),
    module: str | None = Query(default=None),
    entity_type: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    s = _session(request)
    params: dict = {'status': 'PENDING', 'page': page, 'page_size': page_size}
    if module:
        params['module'] = module
    if entity_type:
        params['entity_type'] = entity_type
    if s['branch']:
        params['branch'] = s['branch']
    if s['branch_access']:
        params['branch_access'] = s['branch_access']
    downstream = await get_api_python('/api/otorisasi/submissions/', params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    raw = downstream.json()
    # api-python returns flat {data: [...], pagination: {...}, meta: {...}}
    # Repack to standard ok({rows, pagination}) so api.get() unwraps correctly
    return JSONResponse(ok({
        'rows': raw.get('data', []),
        'pagination': raw.get('pagination', {}),
    }))


@router.post('/submission/{submission_id}/approve')
async def approve_submission(
    submission_id: int,
    request: Request,
    _: str = Depends(require_menu(_MENU_MONITORING)),
):
    s = _session(request)
    body = await request.json() if await _has_body(request) else {}
    params = {'authorizer_id': s['user_id'], 'branch_access': s['branch_access']}
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}/approve"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/submission/{submission_id}/reject')
async def reject_submission(
    submission_id: int,
    request: Request,
    _: str = Depends(require_menu(_MENU_MONITORING)),
):
    s = _session(request)
    body = await request.json() if await _has_body(request) else {}
    params = {'authorizer_id': s['user_id']}
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}/reject"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/bulk/approve')
async def bulk_approve(
    request: Request,
    _: str = Depends(require_menu(_MENU_MONITORING)),
):
    s = _session(request)
    body = await request.json()
    params = {'authorizer_id': s['user_id'], 'branch_access': s['branch_access']}
    url = f"{settings.api_python_base_url}/api/otorisasi/bulk/approve"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/bulk/reject')
async def bulk_reject(
    request: Request,
    _: str = Depends(require_menu(_MENU_MONITORING)),
):
    s = _session(request)
    body = await request.json()
    params = {'authorizer_id': s['user_id']}
    url = f"{settings.api_python_base_url}/api/otorisasi/bulk/reject"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/entity-config/')
async def list_entity_config(
    request: Request,
    _: str = Depends(require_menu(_MENU_MONITORING)),
    module: str | None = Query(default=None),
):
    params: dict = {}
    if module:
        params['module'] = module
    downstream = await get_api_python('/api/otorisasi/entity-config/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# Dynamic-menu endpoints (entity_type resolved from request)
# ---------------------------------------------------------------------------

@router.post('/submission/')
async def create_submission(request: Request):
    """Create submission. Menu check is dynamic based on entity_type in body."""
    body = await request.json()
    entity_type = body.get('entity_type', '')
    await _check_dynamic_menu(request, entity_type)
    s = _session(request)
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/my-submissions/')
async def my_submissions(
    request: Request,
    entity_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    """List own submissions. Menu check is dynamic based on entity_type query param."""
    if entity_type:
        await _check_dynamic_menu(request, entity_type)
    else:
        # No entity_type filter — require at least one menu from ENTITY_MENU
        checker = require_menu(_MENU_MONITORING)
        await checker(request)
    s = _session(request)
    params: dict = {
        'submitted_by': s['user_id'],
        'page': page,
        'page_size': page_size,
    }
    if entity_type:
        params['entity_type'] = entity_type
    if status:
        params['status'] = status
    downstream = await get_api_python('/api/otorisasi/submissions/', params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    raw = downstream.json()
    # Repack to standard ok({rows, pagination}) so api.get() unwraps correctly
    return JSONResponse(ok({
        'rows': raw.get('data', []),
        'pagination': raw.get('pagination', {}),
    }))


@router.get('/submission/{submission_id}')
async def get_submission(submission_id: int, request: Request):
    """Get submission detail.
    Accessible by otorisator (monitoring menu) OR inputer (entity's own menu).
    Fetch first, then check — entity_type is needed to resolve inputer's menu key.
    """
    downstream = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    entity_type = (downstream.json().get('data') or {}).get('entity_type', '')

    # Allow if user has monitoring menu (otorisator)
    try:
        await require_menu(_MENU_MONITORING)(request)
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    except AppHTTPError:
        pass

    # Fallback: allow if user has entity's own menu (inputer editing their draft)
    try:
        await _check_dynamic_menu(request, entity_type)
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    except AppHTTPError:
        return JSONResponse(
            status_code=403,
            content=err('MENU_DENIED', f"Menu '{entity_type}' tidak diizinkan"),
        )


@router.put('/submission/{submission_id}')
async def update_submission(
    submission_id: int,
    request: Request,
):
    """Update submission. Fetch detail first to resolve entity_type, then check menu."""
    detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if detail.status_code != 200:
        return JSONResponse(status_code=detail.status_code, content=detail.json())
    detail_data = detail.json()
    entity_type = (detail_data.get('data') or {}).get('entity_type', '')
    await _check_dynamic_menu(request, entity_type)
    s = _session(request)
    body = await request.json()
    params = {'user_id': s['user_id']}
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.put(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.delete('/submission/{submission_id}')
async def delete_submission(
    submission_id: int,
    request: Request,
):
    """Delete submission. Fetch detail first to resolve entity_type, then check menu."""
    detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if detail.status_code != 200:
        return JSONResponse(status_code=detail.status_code, content=detail.json())
    detail_data = detail.json()
    entity_type = (detail_data.get('data') or {}).get('entity_type', '')
    await _check_dynamic_menu(request, entity_type)
    s = _session(request)
    params = {'user_id': s['user_id']}
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.request('DELETE', url, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/submission/{submission_id}/submit')
async def submit_submission(
    submission_id: int,
    request: Request,
):
    """Mark draft as PENDING. Fetch detail first to resolve entity_type, then check menu."""
    detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if detail.status_code != 200:
        return JSONResponse(status_code=detail.status_code, content=detail.json())
    detail_data = detail.json()
    entity_type = (detail_data.get('data') or {}).get('entity_type', '')
    await _check_dynamic_menu(request, entity_type)
    s = _session(request)
    body = await request.json() if await _has_body(request) else {}
    params = {'user_id': s['user_id']}
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}/submit"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


# ---------------------------------------------------------------------------
# Limit Transaksi endpoints
# ---------------------------------------------------------------------------

@router.post('/save-and-submit/')
async def save_and_submit(request: Request):
    """Simpan submission baru + cek limit + dispatch atau PENDING."""
    body = await request.json()
    entity_type = body.get('entity_type', '')
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    await require_menu(menu_key)(request)
    s = _session(request)
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/otorisasi/save-and-submit/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.put('/save-and-submit/{submission_id}')
async def update_and_submit(submission_id: int, request: Request):
    """Update submission REJECTED + cek limit + dispatch atau PENDING."""
    detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if detail.status_code != 200:
        return JSONResponse(status_code=detail.status_code, content=detail.json())
    entity_type = (detail.json().get('data') or {}).get('entity_type', '')
    await _check_dynamic_menu(request, entity_type)
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/otorisasi/save-and-submit/{submission_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.put(url, json=body, params={'user_id': s['user_id']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/user-limit/')
async def get_user_limit(
    request: Request,
    entity_type: str = Query(...),
):
    """Return limit user untuk entity_type."""
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    await require_menu(menu_key)(request)
    s = _session(request)
    downstream = await get_api_python(
        '/api/otorisasi/user-limit/',
        params={'user_id': s['user_id'], 'entity_type': entity_type},
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

async def _has_body(request: Request) -> bool:
    """Returns True if the request has a non-empty body."""
    body = await request.body()
    return bool(body)

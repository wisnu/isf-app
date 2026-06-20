from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_multipart_api_python
from app.shared.config import settings

router = APIRouter(prefix='/transaction', tags=['transaction-hc-zis'])

_MENU_UPLOAD = 'finance.upload.zis_routine'
_MENU_LIST = 'finance.upload.zis_routine_list'


def _branch_for_session(request: Request) -> str:
    """Resolve branch_code dari session berdasarkan access type."""
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    return '' if access == 'all' else primary


@router.post('/upload/hc-zis/parse')
async def parse_hc_zis(
    request: Request,
    _: str = Depends(require_menu(_MENU_UPLOAD)),
    file: UploadFile = File(...),
    tanggal_transaksi: str = Query(...),
):
    """Parse file HC ZIS ke preview rows (validasi, ekstrak data tanpa simpan)."""
    branch_code = _branch_for_session(request)
    data = await file.read()
    downstream = await post_multipart_api_python(
        f'/api/transaction/upload/hc-zis/parse?tanggal_transaksi={tanggal_transaksi}&branch_code={branch_code}',
        data={},
        file_content=data,
        filename=file.filename or 'upload.xlsx',
        content_type=file.content_type or 'application/octet-stream',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/upload/hc-zis/submit')
async def submit_hc_zis(
    request: Request,
    _: str = Depends(require_menu(_MENU_UPLOAD)),
):
    """Submit parsed HC ZIS data: simpan batch + rows ke database."""
    user_id = request.session.get('user_id', '')
    branch_code = _branch_for_session(request)
    body = await request.json()

    url = f"{settings.api_python_base_url}/api/transaction/upload/hc-zis/submit"
    async with httpx.AsyncClient(timeout=30.0) as client:
        downstream = await client.post(
            url,
            json=body,
            params={'user_id': user_id, 'branch_code': branch_code}
        )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/upload/hc-zis/batches')
async def list_hc_zis_batches(
    request: Request,
    _: str = Depends(require_menu(_MENU_LIST)),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    batch_period_desc: str | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
):
    """List upload batches HC ZIS dengan filter dan pagination."""
    branch_code = _branch_for_session(request)
    params = {
        'page': page,
        'limit': limit,
        'branch_code': branch_code,
    }
    if batch_period_desc:
        params['batch_period_desc'] = batch_period_desc
    if date_from:
        params['date_from'] = date_from
    if date_to:
        params['date_to'] = date_to

    downstream = await get_api_python('/api/transaction/upload/hc-zis/batches', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/upload/hc-zis/batches/{batch_id}')
async def get_hc_zis_batch(
    request: Request,
    batch_id: int,
    _: str = Depends(require_menu(_MENU_LIST)),
):
    """Ambil detail batch HC ZIS + rows."""
    downstream = await get_api_python(
        f'/api/transaction/upload/hc-zis/batches/{batch_id}'
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put('/upload/hc-zis/batches/{batch_id}/date')
async def update_hc_zis_batch_date(
    request: Request,
    batch_id: int,
    _: str = Depends(require_menu(_MENU_LIST)),
):
    """Update tanggal_transaksi untuk batch HC ZIS (hanya status DRAFT/REJECTED)."""
    user_id = request.session.get('user_id', '')
    branch_code = _branch_for_session(request)
    body = await request.json()

    url = f"{settings.api_python_base_url}/api/transaction/upload/hc-zis/batches/{batch_id}/date"
    async with httpx.AsyncClient(timeout=30.0) as client:
        downstream = await client.put(
            url,
            json=body,
            params={'user_id': user_id, 'branch_code': branch_code}
        )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete('/upload/hc-zis/batches/{batch_id}')
async def delete_hc_zis_batch(
    request: Request,
    batch_id: int,
    _: str = Depends(require_menu(_MENU_LIST)),
):
    """Hapus batch HC ZIS (hanya status DRAFT)."""
    user_id = request.session.get('user_id', '')
    branch_code = _branch_for_session(request)

    url = f"{settings.api_python_base_url}/api/transaction/upload/hc-zis/batches/{batch_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        downstream = await client.delete(
            url,
            params={'user_id': user_id, 'branch_code': branch_code}
        )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse, Response

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_multipart_api_python
from app.shared.config import settings
from app.shared.response import err

router = APIRouter(prefix='/transaction', tags=['transaction'])

_UPLOAD_MENU = 'keuangan.upload.penghimpunan'
_APPROVE_MENU = 'keuangan.upload.penghimpunan.approve'
_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def _branch_for_session(request: Request) -> str:
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    return '' if access == 'all' else primary


@router.post('/upload/penghimpunan/parse')
async def parse(
    request: Request,
    _: str = Depends(require_menu(_UPLOAD_MENU)),
    file: UploadFile = File(...),
):
    branch_code = _branch_for_session(request)
    data = await file.read()
    downstream = await post_multipart_api_python(
        '/api/transaction/upload/penghimpunan/parse',
        data={'branch_code': branch_code},
        file_content=data,
        filename=file.filename or 'upload',
        content_type=file.content_type or 'application/octet-stream',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/upload/penghimpunan/draft')
async def draft(
    request: Request,
    _: str = Depends(require_menu(_UPLOAD_MENU)),
    file: UploadFile = File(...),
):
    user_id = request.session.get('user_id', '')
    branch_code = _branch_for_session(request)
    data = await file.read()
    downstream = await post_multipart_api_python(
        '/api/transaction/upload/penghimpunan/draft',
        data={'branch_code': branch_code, 'upload_user': user_id},
        file_content=data,
        filename=file.filename or 'upload',
        content_type=file.content_type or 'application/octet-stream',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/upload/penghimpunan/template')
async def template(
    request: Request,
    _: str = Depends(require_menu(_UPLOAD_MENU)),
):
    downstream = await get_api_python('/api/transaction/upload/penghimpunan/template')
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': 'attachment; filename="template-upload-penghimpunan.xlsx"'},
    )


@router.get('/upload/penghimpunan/batches')
async def batches(
    request: Request,
    _: str = Depends(require_menu(_APPROVE_MENU)),
    begin: str | None = Query(default=None),
    end: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    params: dict = {}
    if begin:
        params['begin'] = begin
    if end:
        params['end'] = end
    if status:
        params['status'] = status
    downstream = await get_api_python('/api/transaction/upload/penghimpunan/batches', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/upload/penghimpunan/batches/{batch_id}')
async def batch_detail(
    request: Request,
    batch_id: int,
    _: str = Depends(require_menu(_APPROVE_MENU)),
):
    downstream = await get_api_python(
        f'/api/transaction/upload/penghimpunan/batches/{batch_id}'
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/upload/penghimpunan/batches/{batch_id}/approve')
async def approve(
    request: Request,
    batch_id: int,
    _: str = Depends(require_menu(_APPROVE_MENU)),
):
    user_id = request.session.get('user_id', '')
    branch_code = _branch_for_session(request)
    url = f"{settings.api_python_base_url}/api/transaction/upload/penghimpunan/batches/{batch_id}/approve"
    async with httpx.AsyncClient(timeout=60.0) as client:
        downstream = await client.post(url, json={
            'authorized_user': user_id,
            'branch_code': branch_code,
            'inputer': user_id,
        })
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

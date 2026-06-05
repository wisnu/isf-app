from __future__ import annotations

from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.modules.transaction import service
from app.modules.transaction.commit import approve_batch
from app.modules.transaction.template import build_template
from app.shared.response import err, ok

router = APIRouter(prefix='/transaction', tags=['transaction'])

_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class ApproveRequest(BaseModel):
    authorized_user: str
    branch_code: str
    inputer: str


@router.post('/upload/penghimpunan/parse')
async def parse_endpoint(
    file: UploadFile = File(...),
    branch_code: str = '',
):
    filename = file.filename or 'upload'
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ('xls', 'xlsx'):
        return JSONResponse(
            status_code=422,
            content=err('INVALID_FORMAT', 'Hanya file .xls dan .xlsx yang diterima'),
        )
    data = await file.read()
    try:
        rows = await service.parse_upload(filename, data)
    except Exception as exc:
        return JSONResponse(status_code=400, content=err('PARSE_ERROR', str(exc)))
    return ok({'rows': [r.model_dump() for r in rows], 'filename': filename})


@router.post('/upload/penghimpunan/draft')
async def draft_endpoint(
    file: UploadFile = File(...),
    branch_code: str = '',
    upload_user: str = '',
):
    filename = file.filename or 'upload'
    data = await file.read()
    try:
        rows = await service.parse_upload(filename, data)
        result = await service.save_draft(filename, branch_code, upload_user, rows)
    except ValueError as exc:
        return JSONResponse(status_code=400, content=err('DRAFT_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())


@router.get('/upload/penghimpunan/template')
async def template_endpoint():
    xlsx = build_template()
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': 'attachment; filename="template-upload-penghimpunan.xlsx"'},
    )


@router.get('/upload/penghimpunan/batches')
async def batches_endpoint(
    begin: str | None = Query(default=None),
    end: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    batches = await service.list_batches(begin, end, status)
    return ok([b.model_dump() for b in batches])


@router.get('/upload/penghimpunan/batches/{batch_id}')
async def batch_detail_endpoint(batch_id: int):
    detail = await service.get_batch_detail(batch_id)
    if not detail:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Batch {batch_id} tidak ditemukan'),
        )
    return ok(detail.model_dump())


@router.post('/upload/penghimpunan/batches/{batch_id}/approve')
async def approve_endpoint(batch_id: int, req: ApproveRequest):
    try:
        committed = await approve_batch(
            batch_id, req.authorized_user, req.branch_code, req.inputer
        )
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except ValueError as exc:
        if 'sudah pernah' in str(exc):
            return JSONResponse(status_code=409, content=err('ALREADY_APPROVED', str(exc)))
        return JSONResponse(status_code=400, content=err('APPROVE_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok({'batch_id': batch_id, 'total_committed': committed})

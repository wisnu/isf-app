from __future__ import annotations
from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.shared.response import ok, err
from .schema import SubmissionIn, UpdatePayloadIn, ApproveIn, RejectIn, BulkApproveIn, BulkRejectIn
from . import repo, service


def _serialize(obj: dict) -> dict:
    """Convert datetime/date objects in a dict to ISO strings for JSON serialization."""
    result = {}
    for k, v in obj.items():
        if isinstance(v, datetime):
            result[k] = v.isoformat()
        elif isinstance(v, date):
            result[k] = v.isoformat()
        else:
            result[k] = v
    return result

router = APIRouter(prefix='/otorisasi', tags=['otorisasi'])


@router.post('/submission/')
async def create_submission(
    body: SubmissionIn,
    user_id: str = Query(...),
    branch_code: str = Query(...),
):
    try:
        result = await service.save_draft(body.entity_type, body.module, body.payload, user_id, branch_code)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.get('/submission/{submission_id}')
async def get_submission(submission_id: int):
    sub = await repo.get_submission(submission_id)
    if not sub:
        return JSONResponse(err('NOT_FOUND', 'Submission tidak ditemukan'), status_code=404)
    log = await repo.get_approval_log(submission_id)
    data = _serialize(dict(sub))
    data['approval_log'] = [_serialize(dict(l)) for l in log]
    return JSONResponse(ok(data))


@router.put('/submission/{submission_id}')
async def update_submission(submission_id: int, body: UpdatePayloadIn, user_id: str = Query(...)):
    sub = await repo.get_submission(submission_id)
    if not sub:
        return JSONResponse(err('NOT_FOUND', 'Submission tidak ditemukan'), status_code=404)
    if sub['submitted_by'] != user_id:
        return JSONResponse(err('FORBIDDEN', 'Bukan submission Anda'), status_code=403)
    if sub['status'] not in ('DRAFT', 'REJECTED'):
        return JSONResponse(err('INVALID_STATUS', 'Tidak bisa diedit'), status_code=400)
    await repo.update_payload(submission_id, body.payload)
    return JSONResponse(ok({'id': submission_id, 'status': 'DRAFT'}))


@router.delete('/submission/{submission_id}')
async def delete_submission(submission_id: int, user_id: str = Query(...)):
    sub = await repo.get_submission(submission_id)
    if not sub:
        return JSONResponse(err('NOT_FOUND', 'Submission tidak ditemukan'), status_code=404)
    if sub['submitted_by'] != user_id:
        return JSONResponse(err('FORBIDDEN', 'Bukan submission Anda'), status_code=403)
    if sub['status'] not in ('DRAFT', 'REJECTED'):
        return JSONResponse(err('INVALID_STATUS', 'Tidak bisa dihapus'), status_code=400)
    await repo.delete_submission(submission_id)
    return JSONResponse(ok({'deleted': True}))


@router.post('/submission/{submission_id}/submit')
async def submit_submission(submission_id: int, user_id: str = Query(...)):
    try:
        result = await service.submit_for_auth(submission_id, user_id)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.get('/submissions/')
async def list_submissions(
    module: str | None = Query(None),
    entity_type: str | None = Query(None),
    status: str | None = Query(None),
    submitted_by: str | None = Query(None),
    branch: str | None = Query(None),
    branch_access: str = Query('single'),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
):
    rows, total = await repo.list_submissions(
        module=module, entity_type=entity_type, status=status,
        submitted_by=submitted_by, branch=branch, branch_access=branch_access,
        page=page, page_size=page_size,
    )
    return JSONResponse({
        'data': [_serialize(dict(r)) for r in rows],
        'pagination': {'page': page, 'limit': page_size, 'total': total, 'total_pages': -(-total // page_size)},
        'meta': {'request_id': ''},
    })


@router.post('/submission/{submission_id}/approve')
async def approve_submission(
    submission_id: int, body: ApproveIn,
    authorizer_id: str = Query(...),
    branch_access: str = Query('single'),
):
    try:
        result = await service.approve(submission_id, authorizer_id, branch_access, body.notes)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.post('/submission/{submission_id}/reject')
async def reject_submission(submission_id: int, body: RejectIn, authorizer_id: str = Query(...)):
    try:
        result = await service.reject(submission_id, authorizer_id, body.notes)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.post('/bulk/approve')
async def bulk_approve(body: BulkApproveIn, authorizer_id: str = Query(...), branch_access: str = Query('single')):
    results = await service.bulk_approve(body.ids, authorizer_id, branch_access)
    return JSONResponse(ok(results))


@router.post('/bulk/reject')
async def bulk_reject(body: BulkRejectIn, authorizer_id: str = Query(...)):
    results = await service.bulk_reject(body.ids, authorizer_id, body.notes)
    return JSONResponse(ok(results))


@router.get('/entity-config/')
async def get_entity_configs(module: str | None = Query(None)):
    configs = await repo.list_entity_configs(module)
    return JSONResponse(ok([dict(c) for c in configs]))

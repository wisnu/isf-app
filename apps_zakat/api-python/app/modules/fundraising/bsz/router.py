from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.fundraising.bsz.schema import CreateBszBody
from app.modules.fundraising.bsz.service import (
    create_bsz,
    delete_bsz,
    get_available_transactions,
    get_bsz_detail,
    list_bsz,
    list_zakat_objects,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/fundraising/bsz', tags=['fundraising-bsz'])


@router.get('/zakat-objects')
async def get_zakat_objects():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    items = await list_zakat_objects()
    return ok([i.model_dump() for i in items])


@router.get('/available-transactions')
async def fetch_available_transactions(
    donor_id: int = Query(...),
    begin_date: str = Query(..., description='ISO YYYY-MM-DD'),
    end_date: str = Query(..., description='ISO YYYY-MM-DD'),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        rows = await get_available_transactions(donor_id, begin_date, end_date)
        return ok([r.model_dump() for r in rows])
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.get('')
async def list_bsz_endpoint(
    donor_id: int | None = Query(default=None),
    begin_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=200),
    page: int = Query(default=1, ge=1),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await list_bsz(
            donor_id=donor_id,
            begin_date=begin_date,
            end_date=end_date,
            limit=limit,
            page=page,
        )
        return ok({'rows': [r.model_dump() for r in result.rows], 'pagination': result.pagination.model_dump()})
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.get('/{bsz_id}')
async def get_bsz(bsz_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        detail = await get_bsz_detail(bsz_id)
        if detail is None:
            return JSONResponse(status_code=404, content=err('NOT_FOUND', f'BSZ {bsz_id} tidak ditemukan'))
        return ok(detail.model_dump())
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.post('')
async def create_bsz_endpoint(body: CreateBszBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await create_bsz(body)
        return ok(result.model_dump())
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{bsz_id}')
async def delete_bsz_endpoint(bsz_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_bsz(bsz_id)
        return ok({'status': 'deleted', 'bsz_id': bsz_id})
    except ValueError as e:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

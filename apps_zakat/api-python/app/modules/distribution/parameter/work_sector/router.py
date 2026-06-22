from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.parameter.work_sector.schema import CreateUpdateWorkSectorBody
from app.modules.distribution.parameter.work_sector.service import (
    create_work_sector,
    delete_work_sector,
    get_work_sector,
    list_work_sectors,
    update_work_sector,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/parameter/work-sector', tags=['distribution-parameter'])


@router.get('')
async def list_work_sectors_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_work_sectors(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.get('/{work_sector_id}')
async def get_work_sector_endpoint(work_sector_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_work_sector(work_sector_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Bidang pekerjaan tidak ditemukan')
    return ok(detail.model_dump())


@router.post('', status_code=201)
async def create_work_sector_endpoint(body: CreateUpdateWorkSectorBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        work_sector_id = await create_work_sector(body)
        return ok({'work_sector_id': work_sector_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/{work_sector_id}')
async def update_work_sector_endpoint(work_sector_id: int, body: CreateUpdateWorkSectorBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_work_sector(work_sector_id, body)
        return ok({'work_sector_id': work_sector_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{work_sector_id}')
async def delete_work_sector_endpoint(work_sector_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_work_sector(work_sector_id)
        return ok({'work_sector_id': work_sector_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

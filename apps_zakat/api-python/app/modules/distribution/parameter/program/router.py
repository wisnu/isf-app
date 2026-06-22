from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.parameter.program.schema import CreateUpdateDistributionProgramBody
from app.modules.distribution.parameter.program.service import (
    create_distribution_program,
    delete_distribution_program,
    get_distribution_program,
    list_distribution_programs,
    update_distribution_program,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/parameter/program', tags=['distribution-parameter'])


@router.get('')
async def list_programs_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_distribution_programs(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.get('/{program_id}')
async def get_program_endpoint(program_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_distribution_program(program_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Program penyaluran tidak ditemukan')
    return ok(detail.model_dump())


@router.post('', status_code=201)
async def create_program_endpoint(body: CreateUpdateDistributionProgramBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        program_id = await create_distribution_program(body)
        return ok({'program_id': program_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/{program_id}')
async def update_program_endpoint(program_id: int, body: CreateUpdateDistributionProgramBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_distribution_program(program_id, body)
        return ok({'program_id': program_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{program_id}')
async def delete_program_endpoint(program_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_distribution_program(program_id)
        return ok({'program_id': program_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.parameter.program_type.schema import CreateUpdateProgramTypeBody
from app.modules.distribution.parameter.program_type.service import (
    create_program_type,
    delete_program_type,
    get_program_type,
    list_program_types,
    lookup_program_types,
    update_program_type,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/parameter/program-type', tags=['distribution-parameter'])


@router.get('/lookup')
async def get_program_type_lookup():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    items = await lookup_program_types()
    return ok([i.model_dump() for i in items])


@router.get('')
async def list_program_types_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_program_types(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.get('/{program_type_id}')
async def get_program_type_endpoint(program_type_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_program_type(program_type_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Jenis program tidak ditemukan')
    return ok(detail.model_dump())


@router.post('', status_code=201)
async def create_program_type_endpoint(body: CreateUpdateProgramTypeBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        program_type_id = await create_program_type(body)
        return ok({'program_type_id': program_type_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/{program_type_id}')
async def update_program_type_endpoint(program_type_id: int, body: CreateUpdateProgramTypeBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_program_type(program_type_id, body)
        return ok({'program_type_id': program_type_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{program_type_id}')
async def delete_program_type_endpoint(program_type_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_program_type(program_type_id)
        return ok({'program_type_id': program_type_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

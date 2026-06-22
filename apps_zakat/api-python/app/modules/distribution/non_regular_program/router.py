from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.non_regular_program.schema import (
    CreateNonRegularProgramBody,
    UpdateNonRegularProgramBody,
)
from app.modules.distribution.non_regular_program.service import (
    create_non_regular_program,
    delete_non_regular_program,
    get_non_regular_program,
    list_non_regular_programs,
    lookup_mustahiq,
    lookup_products,
    update_non_regular_program,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/non-regular-program', tags=['non-regular-program'])


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get('/lookup/products')
async def get_lookup_products():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_products()
    return ok({'data': [item.model_dump() for item in data]})


@router.get('/lookup/mustahiq')
async def get_lookup_mustahiq(search: str | None = Query(default=None, max_length=100)):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_mustahiq(search=search)
    return ok({'data': [item.model_dump() for item in data]})


# ── List ──────────────────────────────────────────────────────────────────────

@router.get('')
async def list_non_regular_programs_endpoint(
    date_from: str | None = Query(default=None, max_length=10),
    date_to: str | None = Query(default=None, max_length=10),
    product_id: int | None = Query(default=None, gt=0),
    branch_code: str | None = Query(default=None, max_length=10),
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_non_regular_programs(
        date_from=date_from,
        date_to=date_to,
        product_id=product_id,
        branch_code=branch_code,
        search=search,
        page=page,
        page_size=page_size,
    )
    return ok(result.model_dump())


# ── Detail ────────────────────────────────────────────────────────────────────

@router.get('/{program_id}')
async def get_non_regular_program_endpoint(program_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_non_regular_program(program_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Program non rutin tidak ditemukan')
    return ok(detail.model_dump())


# ── Create ────────────────────────────────────────────────────────────────────

@router.post('', status_code=201)
async def create_non_regular_program_endpoint(body: CreateNonRegularProgramBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        program_id = await create_non_regular_program(body)
        return ok({'program_id': program_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── Update ────────────────────────────────────────────────────────────────────

@router.put('/{program_id}')
async def update_non_regular_program_endpoint(program_id: int, body: UpdateNonRegularProgramBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_non_regular_program(program_id, body)
        return ok({'program_id': program_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── Delete ────────────────────────────────────────────────────────────────────

@router.delete('/{program_id}')
async def delete_non_regular_program_endpoint(program_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_non_regular_program(program_id)
        return ok({'program_id': program_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

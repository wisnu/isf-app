from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.mustahiq.schema import (
    CreateUpdateCorporateBody,
    CreateUpdatePersonalBody,
    ToggleStatusBody,
)
from app.modules.distribution.mustahiq.service import (
    create_corporate,
    create_personal,
    delete_mustahiq,
    get_corporate,
    get_personal,
    list_corporate,
    list_personal,
    lookup_banks,
    lookup_provinces,
    toggle_status,
    update_corporate,
    update_personal,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/mustahiq', tags=['mustahiq'])


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get('/lookup/provinces')
async def get_lookup_provinces():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_provinces()
    return ok({'data': [item.model_dump() for item in data]})


@router.get('/lookup/banks')
async def get_lookup_banks():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_banks()
    return ok({'data': [item.model_dump() for item in data]})


# ── Corporate ─────────────────────────────────────────────────────────────────

@router.get('/corporate')
async def list_corporate_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_corporate(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.get('/corporate/{mustahiq_id}')
async def get_corporate_endpoint(mustahiq_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_corporate(mustahiq_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Mustahiq Lembaga tidak ditemukan')
    return ok(detail.model_dump())


@router.post('/corporate', status_code=201)
async def create_corporate_endpoint(body: CreateUpdateCorporateBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        mustahiq_id = await create_corporate(body)
        return ok({'mustahiq_id': mustahiq_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/corporate/{mustahiq_id}')
async def update_corporate_endpoint(mustahiq_id: int, body: CreateUpdateCorporateBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_corporate(mustahiq_id, body)
        return ok({'mustahiq_id': mustahiq_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/corporate/{mustahiq_id}')
async def delete_corporate_endpoint(mustahiq_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_mustahiq(mustahiq_id, 'MC')
        return ok({'mustahiq_id': mustahiq_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/corporate/{mustahiq_id}/status')
async def toggle_corporate_status(mustahiq_id: int, body: ToggleStatusBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await toggle_status(mustahiq_id, 'MC', body.status)
        return ok({'mustahiq_id': mustahiq_id, 'status': body.status})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── Personal ──────────────────────────────────────────────────────────────────

@router.get('/personal')
async def list_personal_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_personal(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.get('/personal/{mustahiq_id}')
async def get_personal_endpoint(mustahiq_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_personal(mustahiq_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Mustahiq Individu tidak ditemukan')
    return ok(detail.model_dump())


@router.post('/personal', status_code=201)
async def create_personal_endpoint(body: CreateUpdatePersonalBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        mustahiq_id = await create_personal(body)
        return ok({'mustahiq_id': mustahiq_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/personal/{mustahiq_id}')
async def update_personal_endpoint(mustahiq_id: int, body: CreateUpdatePersonalBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_personal(mustahiq_id, body)
        return ok({'mustahiq_id': mustahiq_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/personal/{mustahiq_id}')
async def delete_personal_endpoint(mustahiq_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_mustahiq(mustahiq_id, 'MP')
        return ok({'mustahiq_id': mustahiq_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/personal/{mustahiq_id}/status')
async def toggle_personal_status(mustahiq_id: int, body: ToggleStatusBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await toggle_status(mustahiq_id, 'MP', body.status)
        return ok({'mustahiq_id': mustahiq_id, 'status': body.status})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

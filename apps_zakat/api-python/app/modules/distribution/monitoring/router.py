from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.monitoring.schema import (
    CreateVisitBody,
    UpdateVisitBody,
)
from app.modules.distribution.monitoring.service import (
    create_visit,
    delete_visit,
    get_visit,
    list_visits,
    lookup_mustahiq,
    lookup_programs,
    update_visit,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(
    prefix='/distribution/monitoring-visits',
    tags=['monitoring-visits'],
)


@router.get('/lookup/mustahiq')
async def _lookup_mustahiq(search: str | None = Query(default=None, max_length=100)):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_mustahiq(search=search)
    return ok({'items': [item.model_dump() for item in data]})


@router.get('/lookup/programs')
async def _lookup_programs(
    mustahiq_id: int | None = Query(default=None),
    search: str | None = Query(default=None, max_length=100),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_programs(mustahiq_id=mustahiq_id, search=search)
    return ok({'items': [item.model_dump() for item in data]})


@router.get('')
async def _list(
    begin_date: str = Query(..., max_length=10),
    end_date: str = Query(..., max_length=10),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await list_visits(
            begin_date=begin_date,
            end_date=end_date,
            page=page,
            page_size=page_size,
        )
        return ok(result.model_dump())
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.get('/{visit_id}')
async def _get(visit_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_visit(visit_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Kunjungan tidak ditemukan')
    return ok(detail.model_dump())


@router.post('', status_code=201)
async def _create(body: CreateVisitBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        visit_id = await create_visit(body=body)
        return ok({'visit_id': visit_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/{visit_id}')
async def _update(visit_id: int, body: UpdateVisitBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_visit(visit_id=visit_id, body=body)
        return ok({'visit_id': visit_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{visit_id}')
async def _delete(visit_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_visit(visit_id=visit_id)
        return ok({'visit_id': visit_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

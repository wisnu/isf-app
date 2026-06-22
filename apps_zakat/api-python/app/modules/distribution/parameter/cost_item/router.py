from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.parameter.cost_item.schema import CreateUpdateCostItemBody
from app.modules.distribution.parameter.cost_item.service import (
    create_cost_item,
    delete_cost_item,
    get_cost_item,
    list_cost_items,
    update_cost_item,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/parameter/cost-item', tags=['distribution-parameter'])


@router.get('')
async def list_cost_items_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_cost_items(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.get('/{cost_item_id}')
async def get_cost_item_endpoint(cost_item_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_cost_item(cost_item_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Rincian biaya tidak ditemukan')
    return ok(detail.model_dump())


@router.post('', status_code=201)
async def create_cost_item_endpoint(body: CreateUpdateCostItemBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        cost_item_id = await create_cost_item(body)
        return ok({'cost_item_id': cost_item_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/{cost_item_id}')
async def update_cost_item_endpoint(cost_item_id: int, body: CreateUpdateCostItemBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_cost_item(cost_item_id, body)
        return ok({'cost_item_id': cost_item_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{cost_item_id}')
async def delete_cost_item_endpoint(cost_item_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_cost_item(cost_item_id)
        return ok({'cost_item_id': cost_item_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

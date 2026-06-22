from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.realization_return.schema import (
    CreateRealizationReturnBody,
    UpdateRealizationReturnBody,
)
from app.modules.distribution.realization_return.service import (
    create_return,
    delete_return,
    get_return,
    list_returns,
    lookup_cost_items,
    lookup_realization_details,
    lookup_realizations,
    update_return,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(
    prefix='/distribution/realization-return',
    tags=['realization-return'],
)


@router.get('/lookup/cost-items')
async def _lookup_cost_items():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_cost_items()
    return ok({'items': [item.model_dump() for item in data]})


@router.get('/lookup/realizations')
async def _lookup_realizations(
    search: str | None = Query(default=None, max_length=100),
    realization_type: str | None = Query(default=None, max_length=1),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        data, total = await lookup_realizations(
            search=search,
            realization_type=realization_type,
            page=page,
            page_size=page_size,
        )
        return ok({
            'rows': [item.model_dump() for item in data],
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total': total,
                'total_pages': (total + page_size - 1) // page_size if total > 0 else 1,
            },
        })
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.get('/realization/{realization_id}/details')
async def _lookup_realization_details(realization_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        data = await lookup_realization_details(realization_id)
        return ok({'rows': [item.model_dump() for item in data]})
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.get('')
async def _list(
    begin_date: str = Query(..., max_length=10),
    end_date: str = Query(..., max_length=10),
    branch_code: str | None = Query(default=None, max_length=5),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await list_returns(
            begin_date=begin_date,
            end_date=end_date,
            branch_code=branch_code,
            page=page,
            page_size=page_size,
        )
        return ok(result.model_dump())
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.get('/{return_id}')
async def _get(return_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_return(return_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Pengembalian realisasi tidak ditemukan')
    return ok(detail.model_dump())


@router.post('', status_code=201)
async def _create(body: CreateRealizationReturnBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        return_id = await create_return(body=body)
        return ok({'return_id': return_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/{return_id}')
async def _update(return_id: int, body: UpdateRealizationReturnBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_return(return_id=return_id, body=body)
        return ok({'return_id': return_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{return_id}')
async def _delete(return_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_return(return_id=return_id)
        return ok({'message': 'Pengembalian realisasi berhasil dihapus'})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

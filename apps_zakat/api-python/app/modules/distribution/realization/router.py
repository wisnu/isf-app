from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.realization.schema import (
    CreateRealizationBody,
    UpdateRealizationBody,
)
from app.modules.distribution.realization.service import (
    create_realization,
    delete_realization,
    get_realization,
    list_realizations,
    lookup_memo_detail,
    lookup_memos,
    update_realization,
)
from app.shared.db import ping
from app.shared.response import err, ok

regular_router = APIRouter(
    prefix='/distribution/realization/regular',
    tags=['realization-regular'],
)

non_regular_router = APIRouter(
    prefix='/distribution/realization/non-regular',
    tags=['realization-non-regular'],
)

_REGULAR_TYPE = 'R'
_NON_REGULAR_TYPE = 'N'


def _make_routes(router: APIRouter, realization_type: str) -> None:

    @router.get('/lookup/memos')
    async def _lookup_memos(search: str | None = Query(default=None, max_length=100)):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        data = await lookup_memos(realization_type=realization_type, search=search)
        return ok({'data': [item.model_dump() for item in data]})

    @router.get('/lookup/memo-detail/{memo_id}')
    async def _lookup_memo_detail(memo_id: int):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        data = await lookup_memo_detail(memo_id)
        return ok({'data': [item.model_dump() for item in data]})

    @router.get('')
    async def _list(
        date_from: str | None = Query(default=None, max_length=10),
        date_to: str | None = Query(default=None, max_length=10),
        branch_code: str | None = Query(default=None, max_length=10),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=25, ge=1, le=500),
    ):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        result = await list_realizations(
            realization_type=realization_type,
            date_from=date_from,
            date_to=date_to,
            branch_code=branch_code,
            page=page,
            page_size=page_size,
        )
        return ok(result.model_dump())

    @router.get('/{realization_id}')
    async def _get(realization_id: int):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        detail = await get_realization(realization_id, realization_type)
        if detail is None:
            raise HTTPException(status_code=404, detail='Realisasi tidak ditemukan')
        return ok(detail.model_dump())

    @router.post('', status_code=201)
    async def _create(body: CreateRealizationBody):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        try:
            realization_id = await create_realization(realization_type=realization_type, body=body)
            return ok({'realization_id': realization_id})
        except ValueError as e:
            return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
        except Exception as e:
            return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

    @router.put('/{realization_id}')
    async def _update(realization_id: int, body: UpdateRealizationBody):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        try:
            await update_realization(realization_id=realization_id, realization_type=realization_type, body=body)
            return ok({'realization_id': realization_id})
        except ValueError as e:
            return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
        except Exception as e:
            return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

    @router.delete('/{realization_id}')
    async def _delete(realization_id: int):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        try:
            await delete_realization(realization_id=realization_id, realization_type=realization_type)
            return ok({'realization_id': realization_id})
        except ValueError as e:
            return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
        except Exception as e:
            return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


_make_routes(regular_router, _REGULAR_TYPE)
_make_routes(non_regular_router, _NON_REGULAR_TYPE)

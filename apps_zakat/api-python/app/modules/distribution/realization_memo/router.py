from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.realization_memo.schema import (
    CreateMemoBody,
    UpdateMemoBody,
)
from app.modules.distribution.realization_memo.service import (
    create_memo,
    delete_memo,
    get_memo,
    list_memos,
    lookup_programs,
    update_memo,
)
from app.shared.db import ping
from app.shared.response import err, ok

regular_router = APIRouter(
    prefix='/distribution/realization-memo/regular',
    tags=['realization-memo-regular'],
)

non_regular_router = APIRouter(
    prefix='/distribution/realization-memo/non-regular',
    tags=['realization-memo-non-regular'],
)

_REGULAR_TYPE = 'R'
_NON_REGULAR_TYPE = 'N'


def _make_routes(router: APIRouter, memo_type: str) -> None:

    @router.get('/lookup/programs')
    async def _lookup_programs(search: str | None = Query(default=None, max_length=100)):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        data = await lookup_programs(memo_type=memo_type, search=search)
        return ok({'data': [item.model_dump() for item in data]})

    @router.get('')
    async def _list(
        date_from: str | None = Query(default=None, max_length=10),
        date_to: str | None = Query(default=None, max_length=10),
        search: str | None = Query(default=None, max_length=100),
        branch_code: str | None = Query(default=None, max_length=10),
        page: int = Query(default=1, ge=1),
        page_size: int = Query(default=25, ge=1, le=500),
    ):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        result = await list_memos(
            memo_type=memo_type,
            date_from=date_from,
            date_to=date_to,
            search=search,
            branch_code=branch_code,
            page=page,
            page_size=page_size,
        )
        return ok(result.model_dump())

    @router.get('/{memo_id}')
    async def _get(memo_id: int):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        detail = await get_memo(memo_id, memo_type)
        if detail is None:
            raise HTTPException(status_code=404, detail='Memo tidak ditemukan')
        return ok(detail.model_dump())

    @router.post('', status_code=201)
    async def _create(body: CreateMemoBody):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        try:
            memo_id = await create_memo(memo_type=memo_type, body=body)
            return ok({'memo_id': memo_id})
        except ValueError as e:
            return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
        except Exception as e:
            return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

    @router.put('/{memo_id}')
    async def _update(memo_id: int, body: UpdateMemoBody):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        try:
            await update_memo(memo_id=memo_id, memo_type=memo_type, body=body)
            return ok({'memo_id': memo_id})
        except ValueError as e:
            return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
        except Exception as e:
            return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

    @router.delete('/{memo_id}')
    async def _delete(memo_id: int):
        if not await ping():
            return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
        try:
            await delete_memo(memo_id=memo_id, memo_type=memo_type)
            return ok({'memo_id': memo_id})
        except ValueError as e:
            return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
        except Exception as e:
            return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


_make_routes(regular_router, _REGULAR_TYPE)
_make_routes(non_regular_router, _NON_REGULAR_TYPE)

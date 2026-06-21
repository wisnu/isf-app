"""FastAPI router for Penghimpunan Dana (Fund Collection)."""
from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.shared.response import err, ok
from . import service

router = APIRouter(prefix='/finance/transaction/fund-collection', tags=['fund-collection'])


@router.get('/lookup/account')
async def lookup_account(branch_code: str = Query(default=''), search: str = Query(default='')):
    rows = await service.lookup_account(branch_code=branch_code, search=search)
    return ok({'rows': rows})


@router.get('/lookup/product')
async def lookup_product(branch_code: str = Query(default=''), search: str = Query(default='')):
    rows = await service.lookup_product(branch_code=branch_code, search=search)
    return ok({'rows': rows})


@router.get('/lookup/donor')
async def lookup_donor(branch_code: str = Query(default=''), search: str = Query(default='')):
    rows = await service.lookup_donor(branch_code=branch_code, search=search)
    return ok({'rows': rows})


@router.get('')
async def list_fund_collection(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    branch_code: str = Query(default=''),
    date_from: str = Query(default=''),
    date_to: str = Query(default=''),
):
    rows, total = await service.list_fund_collection(
        branch_code=branch_code, page=page, limit=limit,
        date_from=date_from, date_to=date_to,
    )
    return ok({
        'rows': rows,
        'pagination': {'page': page, 'limit': limit, 'total': total,
                       'total_pages': -(-total // limit) if total else 0},
    })


@router.get('/{transaction_id}')
async def get_fund_collection(transaction_id: int):
    row = await service.get_fund_collection(transaction_id)
    if not row:
        return JSONResponse(status_code=404,
                            content=err('NOT_FOUND', f'Transaksi penghimpunan {transaction_id} tidak ditemukan'))
    return ok(row)


@router.post('/save-and-submit')
async def create_fund_collection(body: dict):
    try:
        result = await service.create_fund_collection(body)
        return ok(result)
    except Exception as exc:
        return JSONResponse(status_code=400, content=err('CREATE_ERROR', str(exc)))

"""FastAPI router for Transaksi Umum (GT - General Transaction)."""
from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.finance.monitoring.authorization import service as otorisasi_service
from app.shared.response import err, ok
from . import service as general_service
from .schema import GeneralCreate

router = APIRouter(prefix='/transaction/general', tags=['general-transaction'])


# Lookup endpoints
@router.get('/lookup/cash-bank')
async def lookup_kasbank(
    search: str = Query(default=''),
    branch_code: str = Query(default=''),
):
    """Search cash/bank accounts (rekening kas/bank)."""
    rows = await general_service.lookup_kasbank(search=search, branch_code=branch_code)
    return ok({'rows': rows})


@router.get('/lookup/product')
async def lookup_produk(
    search: str = Query(default=''),
    branch_code: str = Query(default=''),
    fund_entity: int = Query(default=0),
):
    """Search product accounts for penghimpunan (collection)."""
    rows = await general_service.lookup_produk(
        search=search, branch_code=branch_code, fund_entity=fund_entity
    )
    return ok({'rows': rows})


@router.get('/lookup/distribution')
async def lookup_penyaluran(search: str = Query(default='')):
    """Search distribution/penyaluran programs."""
    rows = await general_service.lookup_penyaluran(search=search)
    return ok({'rows': rows})


@router.get('/lookup/donor')
async def lookup_donor(search: str = Query(default='')):
    """Search donors."""
    rows = await general_service.lookup_donor(search=search)
    return ok({'rows': rows})


@router.get('')
async def list_transaksi_umum(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    branch_code: str = Query(default=''),
    date_from: str = Query(default=''),
    date_to: str = Query(default=''),
    search: str = Query(default=''),
):
    rows, total = await general_service.list_transaksi_umum(
        branch_code=branch_code,
        page=page,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
        search=search,
    )
    return ok({
        'rows': rows,
        'pagination': {
            'page': page,
            'limit': limit,
            'total': total,
            'total_pages': -(-total // limit) if total else 0,
        },
    })


@router.get('/{transaction_id}')
async def get_transaksi_umum(transaction_id: int):
    row = await general_service.get_transaksi_umum(transaction_id)
    if not row:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Transaksi {transaction_id} tidak ditemukan'),
        )
    return ok(row)


@router.post('')
async def create_general(body: GeneralCreate):
    """Create GT transaction via otorisasi save-and-submit.

    Supports 4 item types:
    - Type 'G': GL/Ledger (existing)
    - Type 'B': Kas/Bank
    - Type 'C': Penghimpunan (Donor/Collection)
    - Type 'D': Penyaluran (Distribution)
    """
    payload = body.model_dump()
    user_id = payload.pop('inputer_id', '') or 'SYSTEM'
    branch_code = payload.pop('branch_code', '') or '001'

    try:
        result = await otorisasi_service.save_and_submit(
            entity_type='transaksi_umum',
            module='keuangan',
            payload=payload,
            user_id=user_id,
            branch_code=branch_code,
        )
        return ok({
            'submission_id': result.get('submission_id'),
            'status': result.get('status'),
            'transaction_id': result.get('transaction_id'),
            'bypassed_auth': result.get('bypassed_auth', False),
            'entity_type': 'transaksi_umum',
        })
    except Exception as exc:
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=400,
            content=err('CREATE_ERROR', str(exc)),
        )

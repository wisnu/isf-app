"""FastAPI router for Transaksi Umum (GT - General Transaction)."""
from __future__ import annotations

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.otorisasi import service as otorisasi_service
from app.shared.response import err, ok
from . import transaksi_umum_service
from .transaksi_umum_schema import TransaksiUmumCreate

router = APIRouter(prefix='/transaksi/umum', tags=['transaksi-umum'])


@router.get('')
async def list_transaksi_umum(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    branch_code: str = Query(default=''),
    date_from: str = Query(default=''),
    date_to: str = Query(default=''),
    search: str = Query(default=''),
):
    rows, total = await transaksi_umum_service.list_transaksi_umum(
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
    row = await transaksi_umum_service.get_transaksi_umum(transaction_id)
    if not row:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Transaksi {transaction_id} tidak ditemukan'),
        )
    return ok(row)


@router.post('')
async def create_transaksi_umum(body: TransaksiUmumCreate):
    """Create GT transaction via otorisasi save-and-submit."""
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
            'submission_id': result['id'],
            'status': result['status'],
            'kode_entri': 'TRANS050',
            'entity_type': 'transaksi_umum',
        })
    except Exception as exc:
        return JSONResponse(
            status_code=400,
            content=err('CREATE_ERROR', str(exc)),
        )

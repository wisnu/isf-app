from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, Response

from app.shared.db import ping
from app.shared.response import err, ok
from . import service
from .export import build_xlsx

router = APIRouter(prefix='/finance/inquiry/receivable', tags=['receivable-inquiry'])

_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


@router.get('/accounts')
async def list_accounts(branch: str = Query(default='')):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    rows = await service.list_accounts(branch_code=branch)
    return ok({'rows': [r.model_dump() for r in rows]})


@router.get('/history')
async def get_history(
    account_no: str = Query(...),
    begin: str = Query(...),
    end: str = Query(...),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await service.get_history(account_no=account_no, begin=begin, end=end)
    if not result:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', 'Rekening tidak ditemukan'))
    return ok(result.model_dump())


@router.get('/history/export.xlsx')
async def export_history(
    account_no: str = Query(...),
    begin: str = Query(...),
    end: str = Query(...),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await service.get_history(account_no=account_no, begin=begin, end=end)
    if not result:
        raise HTTPException(status_code=404, detail='Rekening tidak ditemukan')
    xlsx = build_xlsx(result, begin, end)
    safe = account_no.replace('/', '-')
    fname = f'riwayat-piutang-{safe}-{begin}-{end}.xlsx'
    return Response(content=xlsx, media_type=_XLSX_MIME,
                    headers={'Content-Disposition': f'attachment; filename="{fname}"'})

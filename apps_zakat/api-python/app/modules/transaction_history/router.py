from __future__ import annotations
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.modules.transaction_history import service
from app.modules.transaction_history.delete import delete_transaction
from app.modules.transaction_history.export import build_histori_xlsx
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/transaction-history', tags=['transaction-history'])
_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class DeleteRequest(BaseModel):
    user_id: str
    branch_code: str
    is_spv: bool = False


class RepostRequest(BaseModel):
    user_id: str
    branch_code: str
    is_spv: bool = False


@router.get('/search')
async def search(
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
    branch: str | None = Query(default=None),
    is_spv: bool = Query(default=False),
    user_id: str = Query(default=''),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await service.search(
        begin=begin, end=end, date_type=date_type, sort_by=sort_by,
        search_category=search_category, search_text=search_text,
        cash_account_no=cash_account_no, page=page, page_size=page_size,
        branch=branch, is_spv=is_spv, user_id=user_id,
    )
    return ok(result.model_dump())


@router.get('/search/export.xlsx')
async def search_export(
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    is_spv: bool = Query(default=False),
    user_id: str = Query(default=''),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    rows = await service.search(
        begin=begin, end=end, date_type=date_type, sort_by=sort_by,
        search_category=search_category, search_text=search_text,
        cash_account_no=cash_account_no, limit=500,
        branch=branch, is_spv=is_spv, user_id=user_id,
    )
    xlsx = build_histori_xlsx(rows, begin, end)
    fname = f'histori-transaksi-{begin}-{end}.xlsx'
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': f'attachment; filename="{fname}"'},
    )


@router.get('/transactions/{transaction_id}')
async def get_detail(transaction_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await service.detail(transaction_id)
    if not result:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Transaksi {transaction_id} tidak ditemukan'),
        )
    return ok(result.model_dump())


@router.post('/transactions/{transaction_id}/delete')
async def do_delete(transaction_id: int, req: DeleteRequest):
    try:
        result = await delete_transaction(
            transaction_id, req.user_id, req.branch_code, req.is_spv
        )
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except PermissionError:
        return JSONResponse(
            status_code=403,
            content=err('BRANCH_FORBIDDEN', 'Anda tidak dapat menghapus transaksi milik cabang lain'),
        )
    except ValueError as exc:
        code = str(exc)
        if code == 'EXTERNAL_TX':
            return JSONResponse(
                status_code=400,
                content=err('EXTERNAL_TX', 'Transaksi dari sistem eksternal tidak dapat dihapus'),
            )
        if code == 'ALREADY_PENDING_DELETE':
            return JSONResponse(
                status_code=409,
                content=err('ALREADY_PENDING_DELETE', 'Transaksi sudah dalam antrean hapus'),
            )
        return JSONResponse(status_code=400, content=err('DELETE_ERROR', code))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())


@router.post('/transactions/{transaction_id}/repost')
async def do_repost(transaction_id: int, req: RepostRequest):
    try:
        result = await service.repost_journal(
            transaction_id, req.user_id, req.branch_code, req.is_spv
        )
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except PermissionError:
        return JSONResponse(
            status_code=403,
            content=err('BRANCH_FORBIDDEN', 'Anda tidak dapat memproses transaksi milik cabang lain'),
        )
    except ValueError as exc:
        if 'ALREADY_POSTED' in str(exc):
            return JSONResponse(
                status_code=409,
                content=err('ALREADY_POSTED', 'Transaksi sudah di-posting'),
            )
        return JSONResponse(status_code=400, content=err('REPOST_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())

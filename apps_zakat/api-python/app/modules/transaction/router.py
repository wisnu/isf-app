from __future__ import annotations

import asyncio

from fastapi import APIRouter, File, Query, UploadFile
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.modules.transaction import service
from app.modules.transaction.commit import approve_batch
from app.modules.transaction.template import build_template
from app.modules.transaction import penyaluran_repo as prp
from app.modules.transaction import penyaluran_service as psvc
from app.modules.transaction.penyaluran_schema import ASHNAF_LIST, PenyaluranCreate
from app.modules.transaction import penghimpunan_repo as phrp
from app.modules.transaction import penghimpunan_service as phsvc
from app.modules.transaction.penghimpunan_schema import PenghimpunanCreate
from app.shared.db import fetch_all, fetch_one
from app.shared.response import err, ok

router = APIRouter(prefix='/transaction', tags=['transaction'])

_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class ApproveRequest(BaseModel):
    authorized_user: str
    branch_code: str
    inputer: str


@router.post('/upload/penghimpunan/parse')
async def parse_endpoint(
    file: UploadFile = File(...),
    branch_code: str = '',
):
    filename = file.filename or 'upload'
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ('xls', 'xlsx'):
        return JSONResponse(
            status_code=422,
            content=err('INVALID_FORMAT', 'Hanya file .xls dan .xlsx yang diterima'),
        )
    data = await file.read()
    try:
        rows = await service.parse_upload(filename, data)
    except Exception as exc:
        return JSONResponse(status_code=400, content=err('PARSE_ERROR', str(exc)))
    return ok({'rows': [r.model_dump() for r in rows], 'filename': filename})


@router.post('/upload/penghimpunan/draft')
async def draft_endpoint(
    file: UploadFile = File(...),
    branch_code: str = '',
    upload_user: str = '',
):
    filename = file.filename or 'upload'
    data = await file.read()
    try:
        rows = await service.parse_upload(filename, data)
        result = await service.save_draft(filename, branch_code, upload_user, rows)
    except ValueError as exc:
        return JSONResponse(status_code=400, content=err('DRAFT_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())


@router.get('/upload/penghimpunan/template')
async def template_endpoint():
    xlsx = build_template()
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': 'attachment; filename="template-upload-penghimpunan.xlsx"'},
    )


@router.get('/upload/penghimpunan/batches')
async def batches_endpoint(
    begin: str | None = Query(default=None),
    end: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    batches = await service.list_batches(begin, end, status)
    return ok([b.model_dump() for b in batches])


@router.get('/upload/penghimpunan/batches/{batch_id}')
async def batch_detail_endpoint(batch_id: int):
    detail = await service.get_batch_detail(batch_id)
    if not detail:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Batch {batch_id} tidak ditemukan'),
        )
    return ok(detail.model_dump())


@router.post('/upload/penghimpunan/batches/{batch_id}/approve')
async def approve_endpoint(batch_id: int, req: ApproveRequest):
    try:
        committed = await approve_batch(
            batch_id, req.authorized_user, req.branch_code, req.inputer
        )
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except ValueError as exc:
        if 'sudah pernah' in str(exc):
            return JSONResponse(status_code=409, content=err('ALREADY_APPROVED', str(exc)))
        return JSONResponse(status_code=400, content=err('APPROVE_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok({'batch_id': batch_id, 'total_committed': committed})


# ── Penyaluran Dana (DD001) ───────────────────────────────────────────────────

@router.get('/penyaluran/lookup/ashnaf')
async def penyaluran_lookup_ashnaf():
    return ok(ASHNAF_LIST)


@router.get('/penyaluran/lookup/rekening')
async def penyaluran_lookup_rekening(
    type: str = Query(default='bank'),
    branch: str | None = Query(default=None),
):
    type_map = {'bank': 'A', 'petty': 'P', 'cabang': 'R'}
    rows = await prp.fetch_rekening(type_map.get(type, 'A'), branch)
    return ok([r.model_dump() for r in rows])


@router.get('/penyaluran/lookup/produk')
async def penyaluran_lookup_produk(
    branch_code: str = Query(...),
    currency: str = Query(default='IDR'),
):
    rows = await prp.fetch_products(branch_code, currency)
    return ok([r.model_dump() for r in rows])


@router.get('/penyaluran/lookup/fund-product-account')
async def penyaluran_lookup_fund_product_account(
    bank_account_no: str = Query(...),
    branch_code: str = Query(...),
):
    rows = await prp.fetch_fund_product_accounts(bank_account_no, branch_code)
    return ok([r.model_dump() for r in rows])


@router.get('/penyaluran/')
async def penyaluran_list(
    begin: str = Query(...),
    end: str = Query(...),
    search: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    page_size = min(page_size, 200)
    total, rows = await asyncio.gather(
        prp.count_list(begin, end, search, branch),
        prp.fetch_list(begin, end, search, branch, page, page_size),
    )
    total_pages = max(1, (total + page_size - 1) // page_size)
    return ok({
        'rows': [r.model_dump() for r in rows],
        'pagination': {'page': page, 'limit': page_size, 'total': total, 'total_pages': total_pages},
    })


@router.get('/penyaluran/{transaction_id}')
async def penyaluran_detail(transaction_id: int):
    row = await fetch_one(
        """SELECT t.transactionid, t.transactionno,
              to_char(t.actualdate,'YYYY-MM-DD') AS actual_date,
              t.description, t.amount::float, t.channelcode,
              t.channelaccountno, fa.accountname AS channel_name,
              t.inputer, t.authstatus, t.branchcode, t.journalno,
              to_char(t.transactiondate,'YYYY-MM-DD') AS transaction_date,
              t.referenceno, t.paidto, t.receivedfrom, t.rate, t.currencycode
           FROM transaction.transaction t
           LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
           WHERE t.transactionid = $1 AND t.transactioncode = 'DD001'""",
        transaction_id,
    )
    if not row:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', 'Transaksi tidak ditemukan'))
    items = await fetch_all(
        """SELECT ati.accounttitype, ati.accountno, ati.ashnaf, ati.fundentity,
                  ati.distributionitemaccount, ati.distributioncategory, ati.fundaccountno,
                  ti.amount::float, ti.description, ti.mutationtype,
                  fa.accountname
           FROM transaction.transactionitem ti
           JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
           LEFT JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
           WHERE ti.transactionid = $1
           ORDER BY ti.transactionitemid""",
        transaction_id,
    )
    return ok({**dict(row), 'items': [dict(i) for i in items]})


@router.post('/penyaluran/')
async def penyaluran_create(
    req: PenyaluranCreate,
    branch_code: str = Query(default=''),
    user_id: str = Query(default=''),
):
    try:
        result = await psvc.create_penyaluran(req, user_id, branch_code)
    except ValueError as exc:
        return JSONResponse(status_code=422, content=err('VALIDATION_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())


# ── Penghimpunan Dana (SD001) ─────────────────────────────────────────────────

@router.get('/penghimpunan/lookup/rekening')
async def penghimpunan_lookup_rekening(
    type: str = Query(default='bank'),
    branch: str | None = Query(default=None),
):
    type_map = {'bank': 'A', 'petty': 'P', 'cabang': 'R'}
    rows = await prp.fetch_rekening(type_map.get(type, 'A'), branch)
    return ok([r.model_dump() for r in rows])


@router.get('/penghimpunan/lookup/produk')
async def penghimpunan_lookup_produk(
    branch_code: str = Query(...),
    currency: str = Query(default='IDR'),
):
    rows = await prp.fetch_products(branch_code, currency)
    return ok([r.model_dump() for r in rows])


@router.get('/penghimpunan/lookup/donor')
async def penghimpunan_lookup_donor(
    q: str = Query(...),
    branch: str | None = Query(default=None),
):
    rows = await phrp.search_donors(q, branch)
    return ok(rows)


@router.get('/penghimpunan/')
async def penghimpunan_list(
    begin: str = Query(...),
    end: str = Query(...),
    search: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    page_size = min(page_size, 200)
    total, rows = await asyncio.gather(
        phrp.count_list(begin, end, search, branch),
        phrp.fetch_list(begin, end, search, branch, page, page_size),
    )
    total_pages = max(1, (total + page_size - 1) // page_size)
    return ok({
        'rows': [r.model_dump() for r in rows],
        'pagination': {'page': page, 'limit': page_size, 'total': total, 'total_pages': total_pages},
    })


@router.get('/penghimpunan/{transaction_id}')
async def penghimpunan_detail(transaction_id: int):
    row = await fetch_one(
        """SELECT t.transactionid, t.transactionno,
              to_char(t.actualdate,'YYYY-MM-DD') AS actual_date,
              t.description, CAST(t.amount AS float) AS amount, t.channelcode,
              t.channelaccountno, fa.accountname AS channel_name,
              t.inputer, t.authstatus, t.branchcode, t.journalno,
              to_char(t.transactiondate,'YYYY-MM-DD') AS transaction_date,
              t.referenceno, t.paidto, t.donorno, t.donorname,
              t.rate, t.currencycode
           FROM transaction.transaction t
           LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
           WHERE t.transactionid = $1 AND t.transactioncode = 'SD001'""",
        transaction_id,
    )
    if not row:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', 'Transaksi tidak ditemukan'))
    items = await fetch_all(
        """SELECT ati.accounttitype, ati.accountno, ati.fundentity,
                  CAST(ti.amount AS float) AS amount, ti.description,
                  fa.accountname
           FROM transaction.transactionitem ti
           JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
           LEFT JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
           WHERE ti.transactionid = $1
           ORDER BY ti.transactionitemid""",
        transaction_id,
    )
    return ok({**dict(row), 'items': [dict(i) for i in items]})


@router.post('/penghimpunan/')
async def penghimpunan_create(
    req: PenghimpunanCreate,
    branch_code: str = Query(default=''),
    user_id: str = Query(default=''),
):
    try:
        result = await phsvc.create_penghimpunan(req, user_id, branch_code)
    except ValueError as exc:
        return JSONResponse(status_code=422, content=err('VALIDATION_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())

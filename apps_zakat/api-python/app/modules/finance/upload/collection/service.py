from __future__ import annotations
from app.modules.transaction import repository as repo
from app.modules.transaction.parse import parse_file
from app.modules.transaction.schema import (
    BatchDetail, BatchItem, BatchSummary, DraftResponse, ParsedRow,
)


async def parse_upload(filename: str, data: bytes) -> list[ParsedRow]:
    known_accounts = await repo.get_bank_accounts()
    seen_refs = await repo.get_existing_refs()
    return parse_file(filename, data, known_accounts, seen_refs)


async def save_draft(
    filename: str,
    branch_code: str,
    upload_user: str,
    rows: list[ParsedRow],
) -> DraftResponse:
    saveable = [r for r in rows if r.status != 'invalid']
    if not saveable:
        raise ValueError('Tidak ada baris yang bisa disimpan (semua invalid)')

    total_amount = sum(r.total_kredit for r in saveable)
    batch_id = await repo.insert_batch(
        filename=filename,
        branch_code=branch_code,
        upload_user=upload_user,
        total_record=len(saveable),
        total_amount=total_amount,
    )
    await repo.insert_batch_items(batch_id, [r.model_dump() for r in saveable])
    valid_count = sum(1 for r in saveable if r.status == 'valid')
    warning_count = sum(1 for r in saveable if r.status == 'warning')
    return DraftResponse(
        batch_id=batch_id,
        total_valid=valid_count,
        total_warning=warning_count,
    )


async def list_batches(
    begin: str | None = None,
    end: str | None = None,
    status: str | None = None,
) -> list[BatchSummary]:
    rows = await repo.list_batches(begin, end, status)
    return [
        BatchSummary(
            batch_id=r['batchid'],
            filename=r['filename'] or '',
            upload_date=str(r['uploaddate'])[:10] if r['uploaddate'] else '',
            upload_user=r['uploaduser'] or '',
            branch_code=r['branchcode'] or '',
            total_record=int(r['totalrecord'] or 0),
            total_amount=float(r['totalamount'] or 0),
            authstatus=r['authstatus'] or 'P',
        )
        for r in rows
    ]


async def get_batch_detail(batch_id: int) -> BatchDetail | None:
    batch = await repo.get_batch(batch_id)
    if not batch:
        return None
    items_raw = await repo.get_batch_items(batch_id)
    items = [
        BatchItem(
            batch_item_id=it['batchitemid'],
            row_no=i + 1,
            no_rekening=it['bankaccountno'] or '',
            tanggal=str(it['transactiondate'])[:10] if it['transactiondate'] else '',
            keterangan=it['description'] or '',
            no_ref=it['referenceno'] or '',
            total_kredit=float(it['amount'] or 0),
            zakat_profesi=float(it['amountzakatprofesi'] or 0),
            zakat_maal=float(it['amountzakatmaal'] or 0),
            zakat_fitrah=float(it['amountzakatfitrah'] or 0),
            zakat_perusahaan=float(it['amountzakatperusahaan'] or 0),
            infaq=float(it['amountinfaq'] or 0),
            infaq_terikat=float(it['amountinfaqterikat'] or 0),
            dpu=float(it['amountdpu'] or 0),
            anak_yatim=float(it['amountanakyatim'] or 0),
            anak_asuh=float(it['amountanakasuh'] or 0),
            titipan_wakaf=float(it['amounttitipanwakaf'] or 0),
            titipan_qurban=float(it['amounttitipanqurban'] or 0),
            qurban=float(it['amountqurban'] or 0),
            non_halal=float(it['amountnonhalal'] or 0),
            fidyah=float(it['amountfidyah'] or 0),
            status='valid' if it['validationstatus'] == 'T' else 'warning',
            pesan='',
            transaction_no=it['transactionno'],
        )
        for i, it in enumerate(items_raw)
    ]
    return BatchDetail(
        batch_id=batch['batchid'],
        filename=batch['filename'] or '',
        upload_date=str(batch['uploaddate'])[:10] if batch['uploaddate'] else '',
        upload_user=batch['uploaduser'] or '',
        branch_code=batch['branchcode'] or '',
        total_record=int(batch['totalrecord'] or 0),
        total_amount=float(batch['totalamount'] or 0),
        authstatus=batch['authstatus'] or 'P',
        authorized_user=batch['authorizeduser'],
        items=items,
    )

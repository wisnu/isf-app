"""Business logic for HC ZIS upload."""
from __future__ import annotations

from app.shared.db import get_pool
from .parse import parse_hc_zis_file
from .schema import (
    HCZisParseResult,
    HCZisSubmitRequest,
    HCZisBatchSummary,
    HCZisBatchDetail,
    HCZisTotals,
    HCZisItem,
    HCZisUpdateDateRequest,
)


async def parse_and_validate(
    filename: str,
    data: bytes,
    tanggal_transaksi: str = "",
) -> HCZisParseResult:
    """Parse file and check for duplicate batchperioddesc."""
    result = parse_hc_zis_file(filename, data)
    result.tanggal_transaksi = tanggal_transaksi
    result.namafile = filename

    pool = get_pool()
    exists = await pool.fetchval(
        "SELECT 1 FROM transaction.humancapitalbatch WHERE batchperioddesc = $1",
        result.batch_period_desc,
    )
    if exists:
        result.is_duplicate = True

    return result


async def submit_upload(
    req: HCZisSubmitRequest,
    user_id: str,
    branch_code: str,
) -> dict:
    """Submit HC ZIS upload to otorisasi — goes to PENDING."""
    from app.modules.finance.monitoring.authorization import service as otorisasi_svc

    return await otorisasi_svc.save_and_submit(
        entity_type='hc_zis_upload',
        module='transaksi',
        payload=req.model_dump(),
        user_id=user_id,
        branch_code=branch_code,
    )


async def submit_delete(
    batch_id: int,
    user_id: str,
    branch_code: str,
) -> dict:
    """Submit batch delete to otorisasi."""
    from app.modules.finance.monitoring.authorization import service as otorisasi_svc

    pool = get_pool()
    batch = await pool.fetchrow(
        """SELECT batchid, batchperioddesc,
                  CAST(transactiondate AS VARCHAR) AS transactiondate
           FROM transaction.humancapitalbatch WHERE batchid = $1""",
        batch_id,
    )
    if not batch:
        raise ValueError(f'Batch {batch_id} tidak ditemukan')

    return await otorisasi_svc.save_and_submit(
        entity_type='hc_zis_delete',
        module='transaksi',
        payload={
            'batch_id': batch_id,
            'batch_period_desc': batch['batchperioddesc'],
            'transaction_date': batch['transactiondate'],
        },
        user_id=user_id,
        branch_code=branch_code,
    )


async def submit_update_date(
    batch_id: int,
    req: HCZisUpdateDateRequest,
    user_id: str,
    branch_code: str,
) -> dict:
    """Submit date update to otorisasi."""
    from app.modules.finance.monitoring.authorization import service as otorisasi_svc

    pool = get_pool()
    batch = await pool.fetchrow(
        """SELECT batchid, batchperioddesc,
                  CAST(transactiondate AS VARCHAR) AS transactiondate
           FROM transaction.humancapitalbatch WHERE batchid = $1""",
        batch_id,
    )
    if not batch:
        raise ValueError(f'Batch {batch_id} tidak ditemukan')

    return await otorisasi_svc.save_and_submit(
        entity_type='hc_zis_update_date',
        module='transaksi',
        payload={
            'batch_id': batch_id,
            'batch_period_desc': batch['batchperioddesc'],
            'tanggal_lama': batch['transactiondate'],
            'tanggal_baru': req.tanggal_transaksi,
        },
        user_id=user_id,
        branch_code=branch_code,
    )


async def list_batches(
    branch_code: str,
    page: int = 1,
    limit: int = 25,
    batch_period_desc: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> tuple[list[HCZisBatchSummary], int]:
    """List HC ZIS batches with otorisasi status. Paginated."""
    pool = get_pool()
    offset = (page - 1) * limit

    where_parts: list[str] = []
    params: list = []

    if branch_code:
        params.append(branch_code)
        where_parts.append(f'h.branchcode = ${len(params)}')
    if batch_period_desc:
        params.append(f'%{batch_period_desc}%')
        where_parts.append(f'h.batchperioddesc ILIKE ${len(params)}')
    if date_from:
        params.append(date_from)
        where_parts.append(f'CAST(h.transactiondate AS DATE) >= CAST(${len(params)} AS DATE)')
    if date_to:
        params.append(date_to)
        where_parts.append(f'CAST(h.transactiondate AS DATE) <= CAST(${len(params)} AS DATE)')

    where_clause = ' AND '.join(where_parts) if where_parts else '1=1'

    count_params = params[:]
    params.extend([limit, offset])

    rows = await pool.fetch(
        f"""SELECT h.batchid,
                   h.batchperioddesc,
                   CAST(h.transactiondate AS VARCHAR) AS tanggaltransaksi,
                   h.namafile,
                   h.uploaduserid,
                   CAST(h.uploaddate AS VARCHAR) AS uploaddate,
                   COALESCE(h.grandtotal, 0) AS grandtotal,
                   COALESCE(h.totalrecord, 0) AS totalrecord,
                   h.submissionid,
                   o.status AS submission_status
            FROM transaction.humancapitalbatch h
            LEFT JOIN otorisasi.submission o ON o.id = h.submissionid
            WHERE {where_clause}
            ORDER BY h.uploaddate DESC, h.batchid DESC
            LIMIT ${len(params) - 1} OFFSET ${len(params)}""",
        *params,
    )

    total = await pool.fetchval(
        f'SELECT COUNT(*) FROM transaction.humancapitalbatch h WHERE {where_clause}',
        *count_params,
    )

    return [
        HCZisBatchSummary(
            batch_id=r['batchid'],
            batch_period_desc=r['batchperioddesc'],
            tanggal_transaksi=r['tanggaltransaksi'] or '',
            namafile=r['namafile'] or '',
            upload_user_id=r['uploaduserid'] or '',
            upload_date=r['uploaddate'] or '',
            grand_total=float(r['grandtotal']),
            grand_count=int(r['totalrecord']),
            submission_id=r['submissionid'],
            submission_status=r['submission_status'],
        )
        for r in rows
    ], int(total or 0)


async def get_batch_detail(batch_id: int) -> HCZisBatchDetail | None:
    """Fetch batch header + all items + otorisasi status."""
    pool = get_pool()

    batch = await pool.fetchrow(
        """SELECT h.batchid,
                  h.batchperioddesc,
                  CAST(h.transactiondate AS VARCHAR) AS tanggaltransaksi,
                  h.namafile,
                  h.uploaduserid,
                  CAST(h.uploaddate AS VARCHAR) AS uploaddate,
                  COALESCE(h.grandtotal, 0) AS grandtotal,
                  COALESCE(h.totalrecord, 0) AS totalrecord,
                  h.submissionid,
                  o.status AS submission_status
           FROM transaction.humancapitalbatch h
           LEFT JOIN otorisasi.submission o ON o.id = h.submissionid
           WHERE h.batchid = $1""",
        batch_id,
    )
    if not batch:
        return None

    items_rows = await pool.fetch(
        """SELECT batchitemid, employeenumber, name,
                  businessareacode, businessareadescription,
                  birthplace, workareaname, mobilephone,
                  CAST(birthdate AS VARCHAR) AS birthdate,
                  gender, maritalstatus, position, organizationalunit,
                  COALESCE(amountzakat, 0) AS amountzakat,
                  COALESCE(amountinfaq, 0) AS amountinfaq,
                  COALESCE(amountanakasuh, 0) AS amountanakasuh,
                  COALESCE(amountanakyatim, 0) AS amountanakyatim,
                  COALESCE(amountwakaf, 0) AS amountwakaf,
                  COALESCE(amountqurban, 0) AS amountqurban,
                  COALESCE(totalamount, 0) AS totalamount,
                  iscreateemployeedata, donorid
           FROM transaction.humancapitalbatchitem
           WHERE batchid = $1
           ORDER BY batchitemid ASC""",
        batch_id,
    )

    totals = HCZisTotals()
    parsed_items: list[HCZisItem] = []

    for i, r in enumerate(items_rows, 1):
        zakat = float(r['amountzakat'])
        infaq = float(r['amountinfaq'])
        asuh = float(r['amountanakasuh'])
        yatim = float(r['amountanakyatim'])
        wakaf = float(r['amountwakaf'])
        taqurma = float(r['amountqurban'])
        total = zakat + infaq + asuh + yatim + wakaf + taqurma

        parsed_items.append(HCZisItem(
            data_no=i,
            business_area_code=r['businessareacode'] or '',
            business_area_desc=r['businessareadescription'] or '',
            employee_number=r['employeenumber'] or '',
            employee_name=r['name'] or '',
            birth_place=r['birthplace'] or '',
            work_area_name=r['workareaname'] or '',
            mobile_phone=r['mobilephone'] or '',
            birth_date=r['birthdate'] or '',
            gender=r['gender'] or '',
            marital_status=r['maritalstatus'] or '',
            position=r['position'] or '',
            organization_unit=r['organizationalunit'] or '',
            zakat_amount=zakat,
            infaq_amount=infaq,
            anak_asuh_amount=asuh,
            anak_yatim_amount=yatim,
            wakaf_amount=wakaf,
            taqurma_amount=taqurma,
            total_amount=total,
        ))

        if zakat > 0:
            totals.zakat_amount += zakat; totals.zakat_count += 1
        if infaq > 0:
            totals.infaq_amount += infaq; totals.infaq_count += 1
        if asuh > 0:
            totals.anak_asuh_amount += asuh; totals.anak_asuh_count += 1
        if yatim > 0:
            totals.anak_yatim_amount += yatim; totals.anak_yatim_count += 1
        if wakaf > 0:
            totals.wakaf_amount += wakaf; totals.wakaf_count += 1
        if taqurma > 0:
            totals.taqurma_amount += taqurma; totals.taqurma_count += 1

    totals.grand_total = (
        totals.zakat_amount + totals.infaq_amount + totals.anak_asuh_amount
        + totals.anak_yatim_amount + totals.wakaf_amount + totals.taqurma_amount
    )
    totals.grand_count = len(parsed_items)

    return HCZisBatchDetail(
        batch_id=batch['batchid'],
        batch_period_desc=batch['batchperioddesc'],
        tanggal_transaksi=batch['tanggaltransaksi'] or '',
        namafile=batch['namafile'] or '',
        upload_user_id=batch['uploaduserid'] or '',
        upload_date=batch['uploaddate'] or '',
        submission_id=batch['submissionid'],
        submission_status=batch['submission_status'],
        totals=totals,
        items=parsed_items,
    )

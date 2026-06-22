from __future__ import annotations

import math
from datetime import date as _Date

from app.modules.distribution.realization.schema import (
    CreateRealizationBody,
    MemoDetailItem,
    MemoLookupItem,
    Pagination,
    RealizationDetail,
    RealizationDetailInput,
    RealizationDetailRow,
    RealizationList,
    RealizationRow,
    UpdateRealizationBody,
)
from app.shared.db import fetch_all, fetch_one, get_pool


def _parse_date(val) -> str | None:
    if val is None:
        return None
    try:
        return val.strftime('%Y-%m-%d')
    except AttributeError:
        s = str(val)
        return s[:10] if len(s) >= 10 else s


def _row_to_realization(r: dict) -> RealizationRow:
    return RealizationRow(
        realization_id=r['realizationid'],
        realization_date=_parse_date(r['realizationdate']),
        realization_description=r['realizationdescription'],
        realization_location=r['realizationlocation'],
        memo_number=r['realmemonumber'],
        memo_id=r.get('realmemoid'),  # NEW: track memo ID
        status_receivables=r['statusreceivables'],
        status_reclpj=r['statusreclpj'],
        branch_code=r['branchcode'],
        realization_amount=r['realizationamount'],
    )


# ── Lookup: memos selectable for a realization ───────────────────────────────

async def lookup_memos(realization_type: str, search: str | None = None) -> list[MemoLookupItem]:
    conds = ['rm.realizationmemotype = $1']
    params: list = [realization_type]

    if search and search.strip():
        params.append(f'%{search.strip().lower()}%')
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(rm.realmemonumber, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(rm.realmemosubject, \'\')) LIKE ${idx})'
        )

    where = 'WHERE ' + ' AND '.join(conds)

    rows = await fetch_all(
        f"""
        SELECT
            rm.realmemoid,
            rm.realmemonumber,
            rm.realmemodate,
            rm.realmemoamount,
            rm.realmemosubject
        FROM program.realizationmemo rm
        {where}
        ORDER BY rm.realmemodate DESC, rm.realmemoid DESC
        LIMIT 200
        """,
        *params,
    )
    return [
        MemoLookupItem(
            realization_memo_id=r['realmemoid'],
            realization_memo_number=r['realmemonumber'],
            realization_memo_date=_parse_date(r['realmemodate']),
            realization_memo_amount=r['realmemoamount'],
            realization_memo_subject=r['realmemosubject'],
        )
        for r in rows
    ]


# ── Lookup: memo detail for auto-populate grid ───────────────────────────────

async def lookup_memo_detail(memo_id: int) -> list[MemoDetailItem]:
    rows = await fetch_all(
        """
        SELECT
            d.mustahiqproductid,
            d.realmemodetailamount AS memo_amount,
            mp.mustahiqproductname,
            p.productname,
            c.customername,
            mp.ashnaf,
            mp.productid AS fund_product_id,
            COALESCE(ca.accountno, '') AS account_no,
            COALESCE(ca.accountname, '') AS account_name,
            CAST(pr.proposaldate AS DATE) AS proposal_date,
            pr.proposalnominal AS proposal_nominal,
            pr.proposalreferenceby AS proposal_reference_by
        FROM program.realizationmemodetail d
        JOIN program.mustahiqproduct mp ON mp.mustahiqproductid = d.mustahiqproductid
        JOIN program.product p ON p.productid = mp.productid
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        LEFT JOIN transaction.cashaccount ca ON ca.accountno = mp.accountno
        LEFT JOIN program.proposal pr ON pr.mustahiqproductid = mp.mustahiqproductid
        WHERE d.realmemoid = $1
        ORDER BY d.realmemodetailid
        """,
        memo_id,
    )
    return [
        MemoDetailItem(
            mustahiq_product_id=r['mustahiqproductid'],
            product_name=r['productname'],
            mustahiq_name=r['customername'],
            program_detail_name=r['mustahiqproductname'],
            account_no=r['account_no'],
            account_name=r['account_name'],
            memo_amount=r['memo_amount'] or 0.0,
            ashnaf=r['ashnaf'],
            fund_product_id=r['fund_product_id'],
            proposal_date=_parse_date(r['proposal_date']),
            proposal_nominal=r['proposal_nominal'],
            proposal_reference_by=r['proposal_reference_by'],
        )
        for r in rows
    ]


# ── List ──────────────────────────────────────────────────────────────────────

async def list_realizations(
    realization_type: str,
    date_from: str | None = None,
    date_to: str | None = None,
    branch_code: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> RealizationList:
    conds = ['r.realizationtype = $1']
    params: list = [realization_type]

    if date_from:
        params.append(_Date.fromisoformat(date_from))
        conds.append(f'CAST(r.realizationdate AS DATE) >= ${len(params)}')

    if date_to:
        params.append(_Date.fromisoformat(date_to))
        conds.append(f'CAST(r.realizationdate AS DATE) <= ${len(params)}')

    if branch_code:
        params.append(branch_code)
        conds.append(f'r.branchcode = ${len(params)}')

    where = 'WHERE ' + ' AND '.join(conds)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS total
        FROM program.realization r
        {where}
        """,
        *params,
    )
    total = count_row['total'] if count_row else 0
    total_pages = max(1, math.ceil(total / page_size))

    offset = (page - 1) * page_size
    params.append(page_size)
    limit_idx = len(params)
    params.append(offset)
    offset_idx = len(params)

    rows = await fetch_all(
        f"""
        SELECT
            r.realizationid,
            r.realizationdate,
            r.realizationdescription,
            r.realizationlocation,
            rm.realmemonumber,
            rm.realmemoid,
            r.statusreceivables,
            r.statusreclpj,
            r.branchcode,
            r.realizationamount
        FROM program.realization r
        LEFT JOIN program.realizationmemo rm ON rm.realmemoid = r.realmemoid
        {where}
        ORDER BY r.realizationdate DESC, r.realizationid DESC
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        """,
        *params,
    )

    return RealizationList(
        rows=[_row_to_realization(r) for r in rows],
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_realization(realization_id: int, realization_type: str) -> RealizationDetail | None:
    row = await fetch_one(
        """
        SELECT
            r.realizationid,
            r.realizationdate,
            r.realizationdescription,
            r.realizationlocation,
            rm.realmemonumber,
            rm.realmemoid,
            r.statusreceivables,
            r.statusreclpj,
            r.branchcode,
            r.realizationamount
        FROM program.realization r
        LEFT JOIN program.realizationmemo rm ON rm.realmemoid = r.realmemoid
        WHERE r.realizationid = $1
          AND r.realizationtype = $2
        """,
        realization_id,
        realization_type,
    )
    if row is None:
        return None

    detail_rows = await fetch_all(
        """
        SELECT
            d.realizationdetailid,
            d.mustahiqproductid,
            d.memoamount,
            d.realizationamount,
            d.detaildescription,
            p.productname,
            c.customername,
            mp.mustahiqproductname,
            COALESCE(d.accountno, '') AS account_no,
            COALESCE(ca.accountname, '') AS account_name,
            d.ashnaf,
            d.fundproductid
        FROM program.realizationdetail d
        JOIN program.mustahiqproduct mp ON mp.mustahiqproductid = d.mustahiqproductid
        JOIN program.product p ON p.productid = mp.productid
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        LEFT JOIN transaction.cashaccount ca ON ca.accountno = d.accountno
        WHERE d.realizationid = $1
        ORDER BY d.realizationdetailid
        """,
        realization_id,
    )

    budget_rows = await fetch_all(
        """
        SELECT budgetid FROM program.realizationbudget
        WHERE realizationid = $1
        """,
        realization_id,
    )

    partner_rows = await fetch_all(
        """
        SELECT partnerid FROM program.realizationpartner
        WHERE realizationid = $1
        """,
        realization_id,
    )

    return RealizationDetail(
        **_row_to_realization(row).model_dump(),
        details=[
            RealizationDetailRow(
                realization_detail_id=d['realizationdetailid'],
                mustahiq_product_id=d['mustahiqproductid'],
                product_name=d['productname'],
                mustahiq_name=d['customername'],
                program_detail_name=d['mustahiqproductname'],
                account_no=d['account_no'],
                account_name=d['account_name'],
                memo_amount=d['memoamount'] or 0.0,
                realization_amount=d['realizationamount'] or 0.0,
                ashnaf=d['ashnaf'],
                fund_product_id=d['fundproductid'],
            )
            for d in detail_rows
        ],
        budgets=[b['budgetid'] for b in budget_rows],
        partners=[p['partnerid'] for p in partner_rows],
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_realization(
    realization_type: str,
    body: CreateRealizationBody,
    user_input: str | None = None,
) -> int:
    if not body.details:
        raise ValueError('Realisasi harus memiliki minimal satu detail program')

    if not body.memo_id or body.memo_id == 0:
        raise ValueError('Memo ID tidak boleh kosong atau 0')

    if not body.description or not body.description.strip():
        raise ValueError('Deskripsi realisasi tidak boleh kosong')

    if not body.location or not body.location.strip():
        raise ValueError('Lokasi realisasi tidak boleh kosong')

    total_amount = sum(d.realization_amount for d in body.details)
    pool = get_pool()

    async with pool.acquire() as conn:
        # Verify memo exists and matches type
        memo_check = await conn.fetchrow(
            """
            SELECT realmemoid FROM program.realizationmemo
            WHERE realmemoid = $1 AND realizationmemotype = $2
            """,
            body.memo_id,
            realization_type,
        )
        if not memo_check:
            raise ValueError(f'Memo tidak ditemukan atau tipe tidak sesuai')

        realization_id = await conn.fetchval("SELECT nextval('program.seq_realization')")

        await conn.execute(
            """
            INSERT INTO program.realization (
                realizationid, realizationdate, realmemoid, realizationtype,
                realizationdescription, realizationinputdate, realizationinputuser,
                realizationlocation, statusreceivables, branchcode, realizationamount
            ) VALUES ($1, $2, $3, $4, $5, NOW(), $6, $7, $8, $9, $10)
            """,
            realization_id,
            _Date.fromisoformat(body.realization_date),
            body.memo_id,
            realization_type,
            body.description,
            user_input,
            body.location,
            body.status_receivables or 'T',
            body.branch_code,
            total_amount,
        )

        # Insert employee if status_receivables='Y'
        if body.status_receivables == 'Y' and body.employee_id:
            await conn.execute(
                """
                UPDATE program.realization
                SET employeeid = $1
                WHERE realizationid = $2
                """,
                body.employee_id,
                realization_id,
            )

        # Insert details
        for detail in body.details:
            detail_id = await conn.fetchval("SELECT nextval('program.seq_realizationdetail')")

            # Get memo amount from memo detail
            memo_detail = await conn.fetchrow(
                """
                SELECT realmemodetailamount FROM program.realizationmemodetail
                WHERE mustahiqproductid = $1 AND realmemoid = $2
                """,
                detail.mustahiq_product_id,
                body.memo_id,
            )
            memo_amount = memo_detail['realmemodetailamount'] if memo_detail else 0.0

            # Get account number from mustahiqproduct
            mp_row = await conn.fetchrow(
                """
                SELECT accountno, ashnaf, productid FROM program.mustahiqproduct
                WHERE mustahiqproductid = $1
                """,
                detail.mustahiq_product_id,
            )
            account_no = mp_row['accountno'] if mp_row else None
            ashnaf = mp_row['ashnaf'] if mp_row else None
            fund_product_id = mp_row['productid'] if mp_row else None

            await conn.execute(
                """
                INSERT INTO program.realizationdetail (
                    realizationdetailid, realizationid, mustahiqproductid,
                    memoamount, realizationamount, detaildescription,
                    accountno, branchcode, ashnaf, fundproductid
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """,
                detail_id,
                realization_id,
                detail.mustahiq_product_id,
                memo_amount,
                detail.realization_amount,
                detail.detail_description,
                account_no,
                body.branch_code,
                ashnaf,
                fund_product_id,
            )

        # Insert budgets
        if body.budgets:
            for budget_id in body.budgets:
                if budget_id and budget_id > 0:
                    realbudget_id = await conn.fetchval(
                        "SELECT nextval('program.seq_realizationbudget')"
                    )
                    await conn.execute(
                        """
                        INSERT INTO program.realizationbudget (
                            realbudgetid, realizationid, budgetid
                        ) VALUES ($1, $2, $3)
                        """,
                        realbudget_id,
                        realization_id,
                        budget_id,
                    )

        # Insert partners
        if body.partners:
            for partner_id in body.partners:
                if partner_id and partner_id > 0:
                    realpartner_id = await conn.fetchval(
                        "SELECT nextval('program.seq_realizationpartner')"
                    )
                    await conn.execute(
                        """
                        INSERT INTO program.realizationpartner (
                            realizationpartnerid, realizationid, partnerid
                        ) VALUES ($1, $2, $3)
                        """,
                        realpartner_id,
                        realization_id,
                        partner_id,
                    )

    # TODO: integrasi CreateRealizationTransaction belum diimplementasi
    return realization_id


# ── Update ────────────────────────────────────────────────────────────────────

async def update_realization(
    realization_id: int,
    realization_type: str,
    body: UpdateRealizationBody,
) -> None:
    if not body.details:
        raise ValueError('Realisasi harus memiliki minimal satu detail program')

    if not body.memo_id or body.memo_id == 0:
        raise ValueError('Memo ID tidak boleh kosong atau 0')

    if not body.description or not body.description.strip():
        raise ValueError('Deskripsi realisasi tidak boleh kosong')

    if not body.location or not body.location.strip():
        raise ValueError('Lokasi realisasi tidak boleh kosong')

    total_amount = sum(d.realization_amount for d in body.details)
    pool = get_pool()

    async with pool.acquire() as conn:
        # Check realization exists and get current status
        existing = await conn.fetchrow(
            """
            SELECT realizationid, statusreceivables, statusreclpj
            FROM program.realization
            WHERE realizationid = $1 AND realizationtype = $2
            """,
            realization_id,
            realization_type,
        )
        if not existing:
            raise ValueError('Realisasi tidak ditemukan')

        # Validation: cannot update if statusreceivables='Y' AND statusreclpj='Y'
        if existing['statusreceivables'] == 'Y' and existing['statusreclpj'] == 'Y':
            raise ValueError('Tidak dapat mengubah realisasi yang sudah memiliki LPJ')

        # Check realizationreturn
        rreturn = await conn.fetchrow(
            "SELECT COUNT(*) AS cnt FROM program.realizationreturn WHERE realizationid = $1",
            realization_id,
        )
        if rreturn and rreturn['cnt'] > 0:
            raise ValueError('Tidak dapat mengubah realisasi yang memiliki data pengembalian')

        # Verify memo exists and matches type
        memo_check = await conn.fetchrow(
            """
            SELECT realmemoid FROM program.realizationmemo
            WHERE realmemoid = $1 AND realizationmemotype = $2
            """,
            body.memo_id,
            realization_type,
        )
        if not memo_check:
            raise ValueError(f'Memo tidak ditemukan atau tipe tidak sesuai')

        result = await conn.execute(
            """
            UPDATE program.realization SET
                realizationdate = $2,
                realmemoid = $3,
                realizationdescription = $4,
                realizationlocation = $5,
                statusreceivables = $6,
                employeeid = $7,
                branchcode = $8,
                realizationamount = $9
            WHERE realizationid = $1
              AND realizationtype = $10
            """,
            realization_id,
            _Date.fromisoformat(body.realization_date),
            body.memo_id,
            body.description,
            body.location,
            body.status_receivables or 'T',
            body.employee_id if body.status_receivables == 'Y' else None,
            body.branch_code,
            total_amount,
            realization_type,
        )
        if result == 'UPDATE 0':
            raise ValueError('Realisasi tidak ditemukan')

        # Delete and re-insert details
        await conn.execute(
            "DELETE FROM program.realizationdetail WHERE realizationid = $1",
            realization_id,
        )

        for detail in body.details:
            detail_id = await conn.fetchval("SELECT nextval('program.seq_realizationdetail')")

            # Get memo amount from memo detail
            memo_detail = await conn.fetchrow(
                """
                SELECT realmemodetailamount FROM program.realizationmemodetail
                WHERE mustahiqproductid = $1 AND realmemoid = $2
                """,
                detail.mustahiq_product_id,
                body.memo_id,
            )
            memo_amount = memo_detail['realmemodetailamount'] if memo_detail else 0.0

            # Get account number, ashnaf, productid from mustahiqproduct
            mp_row = await conn.fetchrow(
                """
                SELECT accountno, ashnaf, productid FROM program.mustahiqproduct
                WHERE mustahiqproductid = $1
                """,
                detail.mustahiq_product_id,
            )
            account_no = mp_row['accountno'] if mp_row else None
            ashnaf = mp_row['ashnaf'] if mp_row else None
            fund_product_id = mp_row['productid'] if mp_row else None

            await conn.execute(
                """
                INSERT INTO program.realizationdetail (
                    realizationdetailid, realizationid, mustahiqproductid,
                    memoamount, realizationamount, detaildescription,
                    accountno, branchcode, ashnaf, fundproductid
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                """,
                detail_id,
                realization_id,
                detail.mustahiq_product_id,
                memo_amount,
                detail.realization_amount,
                detail.detail_description,
                account_no,
                body.branch_code,
                ashnaf,
                fund_product_id,
            )

        # Delete and re-insert budgets
        await conn.execute(
            "DELETE FROM program.realizationbudget WHERE realizationid = $1",
            realization_id,
        )

        if body.budgets:
            for budget_id in body.budgets:
                if budget_id and budget_id > 0:
                    realbudget_id = await conn.fetchval(
                        "SELECT nextval('program.seq_realizationbudget')"
                    )
                    await conn.execute(
                        """
                        INSERT INTO program.realizationbudget (
                            realbudgetid, realizationid, budgetid
                        ) VALUES ($1, $2, $3)
                        """,
                        realbudget_id,
                        realization_id,
                        budget_id,
                    )

        # Delete and re-insert partners
        await conn.execute(
            "DELETE FROM program.realizationpartner WHERE realizationid = $1",
            realization_id,
        )

        if body.partners:
            for partner_id in body.partners:
                if partner_id and partner_id > 0:
                    realpartner_id = await conn.fetchval(
                        "SELECT nextval('program.seq_realizationpartner')"
                    )
                    await conn.execute(
                        """
                        INSERT INTO program.realizationpartner (
                            realizationpartnerid, realizationid, partnerid
                        ) VALUES ($1, $2, $3)
                        """,
                        realpartner_id,
                        realization_id,
                        partner_id,
                    )


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_realization(realization_id: int, realization_type: str) -> None:
    pool = get_pool()

    async with pool.acquire() as conn:
        check = await conn.fetchrow(
            """
            SELECT realizationid, statusreceivables, statusreclpj
            FROM program.realization
            WHERE realizationid = $1 AND realizationtype = $2
            """,
            realization_id,
            realization_type,
        )
        if not check:
            raise ValueError('Realisasi tidak ditemukan')

        # Validation: cannot delete if statusreceivables='Y' AND statusreclpj='Y'
        if check['statusreceivables'] == 'Y' and check['statusreclpj'] == 'Y':
            raise ValueError('Tidak dapat menghapus realisasi yang sudah memiliki LPJ')

        # Check realizationreturn
        rreturn = await conn.fetchrow(
            "SELECT COUNT(*) AS cnt FROM program.realizationreturn WHERE realizationid = $1",
            realization_id,
        )
        if rreturn and rreturn['cnt'] > 0:
            raise ValueError('Tidak dapat menghapus realisasi yang memiliki data pengembalian')

        # Delete in order of dependencies
        await conn.execute(
            "DELETE FROM program.realizationdetail WHERE realizationid = $1",
            realization_id,
        )
        await conn.execute(
            "DELETE FROM program.realizationbudget WHERE realizationid = $1",
            realization_id,
        )
        await conn.execute(
            "DELETE FROM program.realizationpartner WHERE realizationid = $1",
            realization_id,
        )
        await conn.execute(
            "DELETE FROM program.realization WHERE realizationid = $1 AND realizationtype = $2",
            realization_id,
            realization_type,
        )

from __future__ import annotations

import math
from datetime import date as _Date

from app.modules.distribution.realization_memo.schema import (
    CreateMemoBody,
    MemoDetail,
    MemoDetailRow,
    MemoList,
    MemoRow,
    Pagination,
    ProgramLookupItem,
    UpdateMemoBody,
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


def _row_to_memo(r: dict) -> MemoRow:
    return MemoRow(
        memo_id=r['realmemoid'],
        memo_number=r['realmemonumber'],
        memo_subject=r['realmemosubject'],
        memo_from=r['realmemofrom'],
        memo_to=r['realmemoto'],
        memo_amount=r['realmemoamount'],
        memo_date=_parse_date(r['realmemodate']),
        branch_code=r['branchcode'],
        user_input=r['userinput'],
    )


# ── Lookup: programs selectable for a memo ────────────────────────────────────

async def lookup_programs(memo_type: str, search: str | None = None) -> list[ProgramLookupItem]:
    conds = ['mp.mustahiqproducttype = $1']
    params: list = [memo_type]

    if search and search.strip():
        params.append(f'%{search.strip().lower()}%')
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(c.customername, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(p.productname, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(mp.mustahiqproductname, \'\')) LIKE ${idx})'
        )

    where = 'WHERE ' + ' AND '.join(conds)

    rows = await fetch_all(
        f"""
        SELECT
            mp.mustahiqproductid,
            mp.mustahiqproductname,
            p.productname,
            c.customername,
            CAST(mp.distributionamount AS DOUBLE PRECISION) AS distributionamount
        FROM program.mustahiqproduct mp
        JOIN program.product p ON p.productid = mp.productid
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        ORDER BY c.customername, p.productname
        LIMIT 200
        """,
        *params,
    )
    return [
        ProgramLookupItem(
            mustahiq_product_id=r['mustahiqproductid'],
            mustahiq_product_name=r['mustahiqproductname'],
            product_name=r['productname'],
            mustahiq_name=r['customername'],
            distribution_amount=r['distributionamount'],
        )
        for r in rows
    ]


# ── List ──────────────────────────────────────────────────────────────────────

async def list_memos(
    memo_type: str,
    date_from: str | None = None,
    date_to: str | None = None,
    search: str | None = None,
    branch_code: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> MemoList:
    conds = ['rm.realizationmemotype = $1']
    params: list = [memo_type]

    if date_from:
        params.append(_Date.fromisoformat(date_from))
        conds.append(f'CAST(rm.realmemodate AS DATE) >= ${len(params)}')

    if date_to:
        params.append(_Date.fromisoformat(date_to))
        conds.append(f'CAST(rm.realmemodate AS DATE) <= ${len(params)}')

    if branch_code:
        params.append(branch_code)
        conds.append(f'rm.branchcode = ${len(params)}')

    if search and search.strip():
        params.append(f'%{search.strip().lower()}%')
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(rm.realmemonumber, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(rm.realmemosubject, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(rm.realmemofrom, \'\')) LIKE ${idx})'
        )

    where = 'WHERE ' + ' AND '.join(conds)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS total
        FROM program.realizationmemo rm
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
            rm.realmemoid,
            rm.realmemonumber,
            rm.realmemosubject,
            rm.realmemofrom,
            rm.realmemoto,
            rm.realmemoamount,
            rm.realmemodate,
            rm.branchcode,
            rm.userinput
        FROM program.realizationmemo rm
        {where}
        ORDER BY rm.realmemodate DESC, rm.realmemoid DESC
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        """,
        *params,
    )

    return MemoList(
        rows=[_row_to_memo(r) for r in rows],
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_memo(memo_id: int, memo_type: str) -> MemoDetail | None:
    row = await fetch_one(
        """
        SELECT
            rm.realmemoid,
            rm.realmemonumber,
            rm.realmemosubject,
            rm.realmemofrom,
            rm.realmemoto,
            rm.realmemoamount,
            rm.realmemodate,
            rm.branchcode,
            rm.userinput
        FROM program.realizationmemo rm
        WHERE rm.realmemoid = $1
          AND rm.realizationmemotype = $2
        """,
        memo_id,
        memo_type,
    )
    if row is None:
        return None

    detail_rows = await fetch_all(
        """
        SELECT
            d.realmemodetailid,
            d.mustahiqproductid,
            d.realmemodetailamount,
            p.productname,
            c.customername,
            mp.mustahiqproductname
        FROM program.realizationmemodetail d
        JOIN program.mustahiqproduct mp ON mp.mustahiqproductid = d.mustahiqproductid
        JOIN program.product p ON p.productid = mp.productid
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        WHERE d.realmemoid = $1
        ORDER BY d.realmemodetailid
        """,
        memo_id,
    )

    return MemoDetail(
        **_row_to_memo(row).model_dump(),
        details=[
            MemoDetailRow(
                memo_detail_id=d['realmemodetailid'],
                mustahiq_product_id=d['mustahiqproductid'],
                product_name=d['productname'],
                mustahiq_name=d['customername'],
                program_detail_name=d['mustahiqproductname'],
                amount=d['realmemodetailamount'] or 0.0,
            )
            for d in detail_rows
        ],
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_memo(memo_type: str, body: CreateMemoBody, user_input: str | None = None) -> int:
    if not body.details:
        raise ValueError('Memo harus memiliki minimal satu program penyaluran')

    total_amount = sum(d.amount for d in body.details)
    pool = get_pool()

    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT realmemoid FROM program.realizationmemo WHERE realmemonumber = $1",
            body.memo_number,
        )
        if existing:
            raise ValueError(f'Nomor memo {body.memo_number} sudah ada di database')

        memo_id = await conn.fetchval("SELECT nextval('program.seq_realizationmemo')")

        await conn.execute(
            """
            INSERT INTO program.realizationmemo (
                realmemoid, realmemonumber, realmemosubject, realmemoamount,
                realmemofrom, realmemoto, realizationmemotype,
                realmemodate, inputdate, userinput, branchcode
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW(), $9, $10)
            """,
            memo_id,
            body.memo_number,
            body.memo_subject,
            total_amount,
            body.memo_from,
            body.memo_to,
            memo_type,
            _Date.fromisoformat(body.memo_date),
            user_input,
            body.branch_code,
        )

        for detail in body.details:
            mp_row = await conn.fetchrow(
                "SELECT productid FROM program.mustahiqproduct WHERE mustahiqproductid = $1",
                detail.mustahiq_product_id,
            )
            product_id = mp_row['productid'] if mp_row else None

            detail_id = await conn.fetchval("SELECT nextval('program.seq_realizationmemodetail')")
            await conn.execute(
                """
                INSERT INTO program.realizationmemodetail (
                    realmemodetailid, realmemoid, mustahiqproductid, productid, realmemodetailamount
                ) VALUES ($1, $2, $3, $4, $5)
                """,
                detail_id,
                memo_id,
                detail.mustahiq_product_id,
                product_id,
                detail.amount,
            )

    return memo_id


# ── Update ────────────────────────────────────────────────────────────────────

async def update_memo(memo_id: int, memo_type: str, body: UpdateMemoBody) -> None:
    if not body.details:
        raise ValueError('Memo harus memiliki minimal satu program penyaluran')

    total_amount = sum(d.amount for d in body.details)
    pool = get_pool()

    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            """
            SELECT realmemoid FROM program.realizationmemo
            WHERE realmemonumber = $1 AND realmemoid <> $2
            """,
            body.memo_number,
            memo_id,
        )
        if existing:
            raise ValueError(f'Nomor memo {body.memo_number} sudah digunakan')

        result = await conn.execute(
            """
            UPDATE program.realizationmemo SET
                realmemonumber = $2,
                realmemosubject = $3,
                realmemoamount = $4,
                realmemofrom = $5,
                realmemoto = $6,
                realmemodate = $7
            WHERE realmemoid = $1
              AND realizationmemotype = $8
            """,
            memo_id,
            body.memo_number,
            body.memo_subject,
            total_amount,
            body.memo_from,
            body.memo_to,
            _Date.fromisoformat(body.memo_date),
            memo_type,
        )
        if result == 'UPDATE 0':
            raise ValueError('Memo tidak ditemukan')

        await conn.execute(
            "DELETE FROM program.realizationmemodetail WHERE realmemoid = $1",
            memo_id,
        )

        for detail in body.details:
            mp_row = await conn.fetchrow(
                "SELECT productid FROM program.mustahiqproduct WHERE mustahiqproductid = $1",
                detail.mustahiq_product_id,
            )
            product_id = mp_row['productid'] if mp_row else None

            detail_id = await conn.fetchval("SELECT nextval('program.seq_realizationmemodetail')")
            await conn.execute(
                """
                INSERT INTO program.realizationmemodetail (
                    realmemodetailid, realmemoid, mustahiqproductid, productid, realmemodetailamount
                ) VALUES ($1, $2, $3, $4, $5)
                """,
                detail_id,
                memo_id,
                detail.mustahiq_product_id,
                product_id,
                detail.amount,
            )


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_memo(memo_id: int, memo_type: str) -> None:
    pool = get_pool()
    async with pool.acquire() as conn:
        check = await conn.fetchrow(
            "SELECT realmemoid FROM program.realizationmemo WHERE realmemoid = $1 AND realizationmemotype = $2",
            memo_id,
            memo_type,
        )
        if not check:
            raise ValueError('Memo tidak ditemukan')

        await conn.execute(
            "DELETE FROM program.realizationmemodetail WHERE realmemoid = $1",
            memo_id,
        )
        await conn.execute(
            "DELETE FROM program.realizationmemo WHERE realmemoid = $1 AND realizationmemotype = $2",
            memo_id,
            memo_type,
        )

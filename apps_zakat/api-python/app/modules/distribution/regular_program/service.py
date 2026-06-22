from __future__ import annotations

import math

from app.modules.distribution.regular_program.schema import (
    CreateRegularProgramBody,
    MustahiqLookupItem,
    Pagination,
    ProductLookupItem,
    RegularProgramDetail,
    RegularProgramList,
    RegularProgramRow,
    UpdateRegularProgramBody,
)
from app.shared.db import fetch_all, fetch_one, get_pool


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_date(val) -> str | None:
    if val is None:
        return None
    try:
        return val.strftime('%Y-%m-%d')
    except AttributeError:
        s = str(val)
        return s[:10] if len(s) >= 10 else s


# ── Lookups ───────────────────────────────────────────────────────────────────

async def lookup_products() -> list[ProductLookupItem]:
    rows = await fetch_all(
        """
        SELECT p.productid, p.productname
        FROM program.product p
        WHERE p.status = 'A' OR p.status IS NULL
        ORDER BY p.productname
        """,
    )
    return [
        ProductLookupItem(product_id=r['productid'], product_name=r['productname'])
        for r in rows
    ]


async def lookup_mustahiq(search: str | None = None) -> list[MustahiqLookupItem]:
    conds = ['1=1']
    params: list = []

    if search and search.strip():
        params.append(f'%{search.strip().lower()}%')
        idx = len(params)
        conds.append(f'LOWER(COALESCE(c.customername, \'\')) LIKE ${idx}')

    where = 'WHERE ' + ' AND '.join(conds)

    rows = await fetch_all(
        f"""
        SELECT m.mustahiqid, c.customername
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        ORDER BY c.customername
        LIMIT 100
        """,
        *params,
    )
    return [
        MustahiqLookupItem(mustahiq_id=r['mustahiqid'], mustahiq_name=r['customername'])
        for r in rows
    ]


# ── List ──────────────────────────────────────────────────────────────────────

async def list_regular_programs(
    date_from: str | None = None,
    date_to: str | None = None,
    product_id: int | None = None,
    branch_code: str | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> RegularProgramList:
    conds = ["mp.mustahiqproducttype = 'R'"]
    params: list = []

    if date_from:
        params.append(date_from)
        conds.append(f'mp.datestart >= ${len(params)}')

    if date_to:
        params.append(date_to)
        conds.append(f'mp.datestart <= ${len(params)}')

    if product_id is not None:
        params.append(product_id)
        conds.append(f'mp.productid = ${len(params)}')

    if branch_code:
        params.append(branch_code)
        conds.append(f'mp.branchcode = ${len(params)}')

    if search and search.strip():
        p = f'%{search.strip().lower()}%'
        params.append(p)
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(c.customername, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(mp.mustahiqproductname, \'\')) LIKE ${idx})'
        )

    where = 'WHERE ' + ' AND '.join(conds)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS total
        FROM program.mustahiqproduct mp
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        JOIN program.product p ON p.productid = mp.productid
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
            mp.mustahiqproductid,
            mp.mustahiqid,
            c.customername,
            mp.productid,
            p.productname,
            mp.mustahiqproductname,
            CAST(mp.distributionamount AS DOUBLE PRECISION) AS distributionamount,
            mp.datestart,
            mp.dateend,
            mp.proposalid,
            mp.branchcode,
            mp.ashnaf
        FROM program.mustahiqproduct mp
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        JOIN program.product p ON p.productid = mp.productid
        {where}
        ORDER BY mp.datestart DESC, mp.mustahiqproductid DESC
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        """,
        *params,
    )

    return RegularProgramList(
        rows=[
            RegularProgramRow(
                program_id=r['mustahiqproductid'],
                mustahiq_id=r['mustahiqid'],
                mustahiq_name=r['customername'],
                product_id=r['productid'],
                product_name=r['productname'],
                program_detail_name=r['mustahiqproductname'],
                distribution_amount=r['distributionamount'],
                date_start=_parse_date(r['datestart']),
                date_end=_parse_date(r['dateend']),
                proposal_id=r['proposalid'],
                branch_code=r['branchcode'],
                ashnaf=r['ashnaf'],
            )
            for r in rows
        ],
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_regular_program(program_id: int) -> RegularProgramDetail | None:
    row = await fetch_one(
        """
        SELECT
            mp.mustahiqproductid,
            mp.mustahiqid,
            c.customername,
            mp.productid,
            p.productname,
            mp.mustahiqproductname,
            CAST(mp.distributionamount AS DOUBLE PRECISION) AS distributionamount,
            mp.datestart,
            mp.dateend,
            mp.proposalid,
            pr.proposalno,
            mp.branchcode,
            mp.ashnaf
        FROM program.mustahiqproduct mp
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        JOIN program.product p ON p.productid = mp.productid
        LEFT JOIN program.proposal pr ON pr.proposalid = mp.proposalid
        WHERE mp.mustahiqproductid = $1
          AND mp.mustahiqproducttype = 'R'
        """,
        program_id,
    )
    if row is None:
        return None
    return RegularProgramDetail(
        program_id=row['mustahiqproductid'],
        mustahiq_id=row['mustahiqid'],
        mustahiq_name=row['customername'],
        product_id=row['productid'],
        product_name=row['productname'],
        program_detail_name=row['mustahiqproductname'],
        distribution_amount=row['distributionamount'],
        date_start=_parse_date(row['datestart']),
        date_end=_parse_date(row['dateend']),
        proposal_id=row['proposalid'],
        proposal_no=row['proposalno'],
        branch_code=row['branchcode'],
        ashnaf=row['ashnaf'],
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_regular_program(body: CreateRegularProgramBody) -> int:
    pool = get_pool()
    async with pool.acquire() as conn:
        program_id = await conn.fetchval("SELECT nextval('program.seq_mustahiqproduct')")
        await conn.execute(
            """
            INSERT INTO program.mustahiqproduct (
                mustahiqproductid,
                mustahiqid,
                productid,
                mustahiqproductname,
                distributionamount,
                datestart,
                dateend,
                proposalid,
                branchcode,
                ashnaf,
                mustahiqproducttype
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 'R')
            """,
            program_id,
            body.mustahiq_id,
            body.product_id,
            body.program_detail_name,
            body.distribution_amount,
            body.date_start,
            body.date_end,
            body.proposal_id,
            body.branch_code,
            body.ashnaf,
        )
    return program_id


# ── Update ────────────────────────────────────────────────────────────────────

async def update_regular_program(program_id: int, body: UpdateRegularProgramBody) -> None:
    pool = get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            UPDATE program.mustahiqproduct SET
                mustahiqid = $2,
                productid = $3,
                mustahiqproductname = $4,
                distributionamount = $5,
                datestart = $6,
                dateend = $7,
                proposalid = $8,
                ashnaf = $9
            WHERE mustahiqproductid = $1
              AND mustahiqproducttype = 'R'
            """,
            program_id,
            body.mustahiq_id,
            body.product_id,
            body.program_detail_name,
            body.distribution_amount,
            body.date_start,
            body.date_end,
            body.proposal_id,
            body.ashnaf,
        )
    if result == 'UPDATE 0':
        raise ValueError('Program rutin tidak ditemukan')


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_regular_program(program_id: int) -> None:
    pool = get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            DELETE FROM program.mustahiqproduct
            WHERE mustahiqproductid = $1
              AND mustahiqproducttype = 'R'
            """,
            program_id,
        )
    if result == 'DELETE 0':
        raise ValueError('Program rutin tidak ditemukan')

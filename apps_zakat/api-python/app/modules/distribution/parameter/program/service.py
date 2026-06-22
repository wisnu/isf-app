from __future__ import annotations

from app.modules.distribution.parameter.program.schema import (
    CreateUpdateDistributionProgramBody,
    DistributionProgramDetail,
    DistributionProgramList,
    DistributionProgramRow,
    FUND_CATEGORY_CHOICES,
    Pagination,
    PROGRAM_TYPE_CHOICES,
)
from app.shared.db import fetch_all, fetch_one, get_pool


def _build_where(search: str | None) -> tuple[str, list]:
    conds: list[str] = []
    params: list = []
    if search and search.strip():
        p = f'%{search.strip().lower()}%'
        params.append(p)
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(p.productcode, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(p.productname, \'\')) LIKE ${idx})'
        )
    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''
    return where, params


async def list_distribution_programs(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> DistributionProgramList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_where(search)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM program.product p
        LEFT JOIN program.productgroup pg ON pg.productgroupid = p.productgroupid
        {where}
        """,
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    lp = len(params) + 1
    op = len(params) + 2
    rows = await fetch_all(
        f"""
        SELECT
            p.productid      AS program_id,
            p.productcode    AS code,
            p.productname    AS name,
            p.producttype    AS program_type,
            p.productgroupid AS program_group_id,
            pg.productgroupname AS program_group_name,
            p.fundcategory   AS fund_category,
            p.status
        FROM program.product p
        LEFT JOIN program.productgroup pg ON pg.productgroupid = p.productgroupid
        {where}
        ORDER BY pg.productgroupname NULLS LAST, p.productname
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return DistributionProgramList(
        rows=[
            DistributionProgramRow(
                program_id=r['program_id'],
                code=r['code'],
                name=r['name'],
                program_type=r['program_type'],
                program_type_name=PROGRAM_TYPE_CHOICES.get(r['program_type'] or '', r['program_type']),
                program_group_id=r['program_group_id'],
                program_group_name=r['program_group_name'],
                fund_category=r['fund_category'],
                fund_category_name=FUND_CATEGORY_CHOICES.get(r['fund_category'] or '', r['fund_category']),
                status=r['status'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


async def get_distribution_program(program_id: int) -> DistributionProgramDetail | None:
    row = await fetch_one(
        """
        SELECT
            p.productid      AS program_id,
            p.productcode    AS code,
            p.productname    AS name,
            p.description,
            p.producttype    AS program_type,
            p.productgroupid AS program_group_id,
            pg.productgroupname AS program_group_name,
            p.fundcategory   AS fund_category,
            p.status
        FROM program.product p
        LEFT JOIN program.productgroup pg ON pg.productgroupid = p.productgroupid
        WHERE p.productid = $1
        LIMIT 1
        """,
        program_id,
    )
    if not row:
        return None
    return DistributionProgramDetail(
        program_id=row['program_id'],
        code=row['code'],
        name=row['name'],
        description=row['description'],
        program_type=row['program_type'],
        program_type_name=PROGRAM_TYPE_CHOICES.get(row['program_type'] or '', row['program_type']),
        program_group_id=row['program_group_id'],
        program_group_name=row['program_group_name'],
        fund_category=row['fund_category'],
        fund_category_name=FUND_CATEGORY_CHOICES.get(row['fund_category'] or '', row['fund_category']),
        status=row['status'],
    )


async def create_distribution_program(body: CreateUpdateDistributionProgramBody) -> int:
    if body.program_type not in ('R', 'N'):
        raise ValueError('Bentuk program harus R (Rutin) atau N (Non Rutin)')
    if body.fund_category not in ('Z', 'I', 'W', 'A', 'N'):
        raise ValueError('Jenis dana tidak valid')

    existing = await fetch_one(
        "SELECT productid FROM program.product WHERE LOWER(productcode) = LOWER($1)",
        body.code,
    )
    if existing:
        raise ValueError(f'Kode program "{body.code}" sudah digunakan')

    group_row = await fetch_one(
        'SELECT productgroupname FROM program.productgroup WHERE productgroupid = $1',
        body.program_group_id,
    )
    if not group_row:
        raise ValueError('Jenis program (group) tidak ditemukan')

    async with get_pool().acquire() as conn:
        program_id = await conn.fetchval("SELECT nextval('program.seq_product')")
        await conn.execute(
            """
            INSERT INTO program.product
                (productid, productcode, productname, description, producttype,
                 productgroupid, productgroupname, fundcategory, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            """,
            program_id,
            body.code.upper(),
            body.name,
            body.description or '',
            body.program_type,
            body.program_group_id,
            group_row['productgroupname'],
            body.fund_category,
            body.status or 'A',
        )
    return program_id


async def update_distribution_program(
    program_id: int, body: CreateUpdateDistributionProgramBody
) -> None:
    row = await fetch_one(
        'SELECT productid FROM program.product WHERE productid = $1',
        program_id,
    )
    if not row:
        raise ValueError('Program penyaluran tidak ditemukan')

    if body.program_type not in ('R', 'N'):
        raise ValueError('Bentuk program harus R (Rutin) atau N (Non Rutin)')
    if body.fund_category not in ('Z', 'I', 'W', 'A', 'N'):
        raise ValueError('Jenis dana tidak valid')

    conflict = await fetch_one(
        "SELECT productid FROM program.product WHERE LOWER(productcode) = LOWER($1) AND productid != $2",
        body.code,
        program_id,
    )
    if conflict:
        raise ValueError(f'Kode program "{body.code}" sudah digunakan')

    group_row = await fetch_one(
        'SELECT productgroupname FROM program.productgroup WHERE productgroupid = $1',
        body.program_group_id,
    )
    if not group_row:
        raise ValueError('Jenis program (group) tidak ditemukan')

    async with get_pool().acquire() as conn:
        await conn.execute(
            """
            UPDATE program.product SET
                productcode      = $1,
                productname      = $2,
                description      = $3,
                producttype      = $4,
                productgroupid   = $5,
                productgroupname = $6,
                fundcategory     = $7,
                status           = $8
            WHERE productid = $9
            """,
            body.code.upper(),
            body.name,
            body.description or '',
            body.program_type,
            body.program_group_id,
            group_row['productgroupname'],
            body.fund_category,
            body.status or 'A',
            program_id,
        )


async def delete_distribution_program(program_id: int) -> None:
    row = await fetch_one(
        'SELECT productid FROM program.product WHERE productid = $1',
        program_id,
    )
    if not row:
        raise ValueError('Program penyaluran tidak ditemukan')

    used = await fetch_one(
        """
        SELECT realizationid FROM program.realization WHERE productid = $1
        UNION ALL
        SELECT realizationmemoid FROM program.realizationmemo WHERE productid = $1
        LIMIT 1
        """,
        program_id,
    )
    if used:
        raise ValueError('Program tidak dapat dihapus karena sudah digunakan dalam transaksi realisasi')

    async with get_pool().acquire() as conn:
        await conn.execute(
            'DELETE FROM program.product WHERE productid = $1',
            program_id,
        )

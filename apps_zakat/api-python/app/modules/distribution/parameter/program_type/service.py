from __future__ import annotations

from app.modules.distribution.parameter.program_type.schema import (
    CreateUpdateProgramTypeBody,
    Pagination,
    ProgramTypeDetail,
    ProgramTypeList,
    ProgramTypeLookupItem,
    ProgramTypeRow,
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
            f'(LOWER(COALESCE(pg.productgroupcode, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(pg.productgroupname, \'\')) LIKE ${idx})'
        )
    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''
    return where, params


async def list_program_types(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> ProgramTypeList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_where(search)

    count_row = await fetch_one(
        f'SELECT CAST(COUNT(*) AS INTEGER) AS c FROM program.productgroup pg {where}',
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    lp = len(params) + 1
    op = len(params) + 2
    rows = await fetch_all(
        f"""
        SELECT
            pg.productgroupid   AS program_type_id,
            pg.productgroupcode AS code,
            pg.productgroupname AS name,
            pg.description,
            pg.statusaktif      AS status
        FROM program.productgroup pg
        {where}
        ORDER BY pg.productgroupname
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return ProgramTypeList(
        rows=[
            ProgramTypeRow(
                program_type_id=r['program_type_id'],
                code=r['code'],
                name=r['name'],
                description=r['description'],
                status=r['status'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


async def get_program_type(program_type_id: int) -> ProgramTypeDetail | None:
    row = await fetch_one(
        """
        SELECT
            productgroupid   AS program_type_id,
            productgroupcode AS code,
            productgroupname AS name,
            description,
            statusaktif      AS status
        FROM program.productgroup
        WHERE productgroupid = $1
        LIMIT 1
        """,
        program_type_id,
    )
    if not row:
        return None
    return ProgramTypeDetail(
        program_type_id=row['program_type_id'],
        code=row['code'],
        name=row['name'],
        description=row['description'],
        status=row['status'],
    )


async def create_program_type(body: CreateUpdateProgramTypeBody) -> int:
    existing = await fetch_one(
        "SELECT productgroupid FROM program.productgroup WHERE LOWER(productgroupcode) = LOWER($1)",
        body.code,
    )
    if existing:
        raise ValueError(f'Kode jenis program "{body.code}" sudah digunakan')

    async with get_pool().acquire() as conn:
        program_type_id = await conn.fetchval("SELECT nextval('program.seq_productgroup')")
        await conn.execute(
            """
            INSERT INTO program.productgroup
                (productgroupid, productgroupcode, productgroupname, description, statusaktif)
            VALUES ($1, $2, $3, $4, $5)
            """,
            program_type_id,
            body.code.upper(),
            body.name,
            body.description or '',
            body.status or 'A',
        )
    return program_type_id


async def update_program_type(program_type_id: int, body: CreateUpdateProgramTypeBody) -> None:
    row = await fetch_one(
        'SELECT productgroupid FROM program.productgroup WHERE productgroupid = $1',
        program_type_id,
    )
    if not row:
        raise ValueError('Jenis program tidak ditemukan')

    conflict = await fetch_one(
        """
        SELECT productgroupid FROM program.productgroup
        WHERE LOWER(productgroupcode) = LOWER($1) AND productgroupid != $2
        """,
        body.code,
        program_type_id,
    )
    if conflict:
        raise ValueError(f'Kode jenis program "{body.code}" sudah digunakan')

    async with get_pool().acquire() as conn:
        await conn.execute(
            """
            UPDATE program.productgroup SET
                productgroupcode = $1,
                productgroupname = $2,
                description      = $3,
                statusaktif      = $4
            WHERE productgroupid = $5
            """,
            body.code.upper(),
            body.name,
            body.description or '',
            body.status or 'A',
            program_type_id,
        )


async def delete_program_type(program_type_id: int) -> None:
    row = await fetch_one(
        'SELECT productgroupid FROM program.productgroup WHERE productgroupid = $1',
        program_type_id,
    )
    if not row:
        raise ValueError('Jenis program tidak ditemukan')

    used = await fetch_one(
        'SELECT productid FROM program.product WHERE productgroupid = $1 LIMIT 1',
        program_type_id,
    )
    if used:
        raise ValueError('Jenis program tidak dapat dihapus karena masih digunakan oleh program penyaluran')

    async with get_pool().acquire() as conn:
        await conn.execute(
            'DELETE FROM program.productgroup WHERE productgroupid = $1',
            program_type_id,
        )


async def lookup_program_types() -> list[ProgramTypeLookupItem]:
    rows = await fetch_all(
        """
        SELECT productgroupid AS program_type_id, productgroupname AS name
        FROM program.productgroup
        WHERE statusaktif = 'A' OR statusaktif IS NULL
        ORDER BY productgroupname
        """,
    )
    return [
        ProgramTypeLookupItem(program_type_id=r['program_type_id'], name=r['name'])
        for r in rows
    ]

from __future__ import annotations

from app.modules.distribution.parameter.work_sector.schema import (
    CreateUpdateWorkSectorBody,
    Pagination,
    WorkSectorDetail,
    WorkSectorList,
    WorkSectorRow,
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
            f'(LOWER(COALESCE(ws.workcode, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(ws.workname, \'\')) LIKE ${idx})'
        )
    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''
    return where, params


async def list_work_sectors(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> WorkSectorList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_where(search)

    count_row = await fetch_one(
        f'SELECT CAST(COUNT(*) AS INTEGER) AS c FROM program.worksector ws {where}',
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    lp = len(params) + 1
    op = len(params) + 2
    rows = await fetch_all(
        f"""
        SELECT
            ws.workid      AS work_sector_id,
            ws.workcode    AS code,
            ws.workname    AS name,
            ws.statusaktif AS status
        FROM program.worksector ws
        {where}
        ORDER BY ws.workcode
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return WorkSectorList(
        rows=[
            WorkSectorRow(
                work_sector_id=r['work_sector_id'],
                code=r['code'],
                name=r['name'],
                status=r['status'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


async def get_work_sector(work_sector_id: int) -> WorkSectorDetail | None:
    row = await fetch_one(
        """
        SELECT workid AS work_sector_id, workcode AS code, workname AS name, statusaktif AS status
        FROM program.worksector
        WHERE workid = $1
        LIMIT 1
        """,
        work_sector_id,
    )
    if not row:
        return None
    return WorkSectorDetail(
        work_sector_id=row['work_sector_id'],
        code=row['code'],
        name=row['name'],
        status=row['status'],
    )


async def create_work_sector(body: CreateUpdateWorkSectorBody) -> int:
    existing = await fetch_one(
        "SELECT workid FROM program.worksector WHERE LOWER(workcode) = LOWER($1)",
        body.code,
    )
    if existing:
        raise ValueError(f'Kode bidang pekerjaan "{body.code}" sudah digunakan')

    async with get_pool().acquire() as conn:
        work_sector_id = await conn.fetchval("SELECT nextval('program.seq_worksector')")
        await conn.execute(
            """
            INSERT INTO program.worksector (workid, workcode, workname, statusaktif)
            VALUES ($1, $2, $3, $4)
            """,
            work_sector_id,
            body.code.upper(),
            body.name.upper(),
            body.status or 'A',
        )
    return work_sector_id


async def update_work_sector(work_sector_id: int, body: CreateUpdateWorkSectorBody) -> None:
    row = await fetch_one(
        'SELECT workid FROM program.worksector WHERE workid = $1',
        work_sector_id,
    )
    if not row:
        raise ValueError('Bidang pekerjaan tidak ditemukan')

    conflict = await fetch_one(
        "SELECT workid FROM program.worksector WHERE LOWER(workcode) = LOWER($1) AND workid != $2",
        body.code,
        work_sector_id,
    )
    if conflict:
        raise ValueError(f'Kode bidang pekerjaan "{body.code}" sudah digunakan')

    async with get_pool().acquire() as conn:
        await conn.execute(
            """
            UPDATE program.worksector SET
                workcode    = $1,
                workname    = $2,
                statusaktif = $3
            WHERE workid = $4
            """,
            body.code.upper(),
            body.name.upper(),
            body.status or 'A',
            work_sector_id,
        )


async def delete_work_sector(work_sector_id: int) -> None:
    row = await fetch_one(
        'SELECT workid FROM program.worksector WHERE workid = $1',
        work_sector_id,
    )
    if not row:
        raise ValueError('Bidang pekerjaan tidak ditemukan')

    async with get_pool().acquire() as conn:
        await conn.execute(
            'DELETE FROM program.worksector WHERE workid = $1',
            work_sector_id,
        )

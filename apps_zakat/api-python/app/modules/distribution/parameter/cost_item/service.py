from __future__ import annotations

from app.modules.distribution.parameter.cost_item.schema import (
    CostItemDetail,
    CostItemList,
    CostItemRow,
    CreateUpdateCostItemBody,
    Pagination,
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
            f'(LOWER(COALESCE(ci.costitemcode, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(ci.costitemdescription, \'\')) LIKE ${idx})'
        )
    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''
    return where, params


async def list_cost_items(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> CostItemList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_where(search)

    count_row = await fetch_one(
        f'SELECT CAST(COUNT(*) AS INTEGER) AS c FROM program.costitem ci {where}',
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    lp = len(params) + 1
    op = len(params) + 2
    rows = await fetch_all(
        f"""
        SELECT
            ci.costitemid          AS cost_item_id,
            ci.costitemcode        AS code,
            ci.costitemdescription AS description
        FROM program.costitem ci
        {where}
        ORDER BY ci.costitemid
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return CostItemList(
        rows=[
            CostItemRow(
                cost_item_id=r['cost_item_id'],
                code=r['code'],
                description=r['description'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


async def get_cost_item(cost_item_id: int) -> CostItemDetail | None:
    row = await fetch_one(
        """
        SELECT costitemid AS cost_item_id, costitemcode AS code, costitemdescription AS description
        FROM program.costitem
        WHERE costitemid = $1
        LIMIT 1
        """,
        cost_item_id,
    )
    if not row:
        return None
    return CostItemDetail(
        cost_item_id=row['cost_item_id'],
        code=row['code'],
        description=row['description'],
    )


async def create_cost_item(body: CreateUpdateCostItemBody) -> int:
    existing = await fetch_one(
        "SELECT costitemid FROM program.costitem WHERE LOWER(costitemcode) = LOWER($1)",
        body.code,
    )
    if existing:
        raise ValueError(f'Kode rincian biaya "{body.code}" sudah digunakan')

    async with get_pool().acquire() as conn:
        cost_item_id = await conn.fetchval("SELECT nextval('program.seq_costitem')")
        await conn.execute(
            """
            INSERT INTO program.costitem (costitemid, costitemcode, costitemdescription)
            VALUES ($1, $2, $3)
            """,
            cost_item_id,
            body.code.upper(),
            body.description.upper(),
        )
    return cost_item_id


async def update_cost_item(cost_item_id: int, body: CreateUpdateCostItemBody) -> None:
    row = await fetch_one(
        'SELECT costitemid FROM program.costitem WHERE costitemid = $1',
        cost_item_id,
    )
    if not row:
        raise ValueError('Rincian biaya tidak ditemukan')

    conflict = await fetch_one(
        "SELECT costitemid FROM program.costitem WHERE LOWER(costitemcode) = LOWER($1) AND costitemid != $2",
        body.code,
        cost_item_id,
    )
    if conflict:
        raise ValueError(f'Kode rincian biaya "{body.code}" sudah digunakan')

    async with get_pool().acquire() as conn:
        await conn.execute(
            """
            UPDATE program.costitem SET
                costitemcode        = $1,
                costitemdescription = $2
            WHERE costitemid = $3
            """,
            body.code.upper(),
            body.description.upper(),
            cost_item_id,
        )


async def delete_cost_item(cost_item_id: int) -> None:
    row = await fetch_one(
        'SELECT costitemid FROM program.costitem WHERE costitemid = $1',
        cost_item_id,
    )
    if not row:
        raise ValueError('Rincian biaya tidak ditemukan')

    used = await fetch_one(
        'SELECT realizationcostid FROM program.realizationcost WHERE costitemid = $1 LIMIT 1',
        cost_item_id,
    )
    if used:
        raise ValueError('Rincian biaya tidak dapat dihapus karena masih digunakan dalam transaksi realisasi')

    async with get_pool().acquire() as conn:
        await conn.execute(
            'DELETE FROM program.costitem WHERE costitemid = $1',
            cost_item_id,
        )

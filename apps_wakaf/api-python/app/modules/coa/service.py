from __future__ import annotations

from app.modules.coa.schema import (
    TYPE_LABELS,
    CoaList,
    CoaRow,
    CoaStats,
    Pagination,
)
from app.shared.db import fetch_all, fetch_one


def _build_where(search: str | None) -> tuple[str, list]:
    if search and search.strip():
        return (
            "WHERE LOWER(account_code) LIKE $1 OR LOWER(COALESCE(account_name, '')) LIKE $1",
            [f"%{search.strip().lower()}%"],
        )
    return "", []


def _to_row(r: dict) -> CoaRow:
    return CoaRow(
        code=r["account_code"],
        name=r["account_name"],
        type_code=(r["account_type"] or "").strip() or None,
        type_label=TYPE_LABELS.get((r["account_type"] or "").strip(), "Lainnya"),
        level=r["account_level"],
        is_detail=(r["is_detail"] or "").upper() == "T",
        is_system=(r["is_system"] or "").upper() == "T",
        parent=r["fl_parent_account"] or None,
        balance=float(r["balance"] or 0),
    )


_SELECT_COLS = """
    account_code,
    account_name,
    account_level,
    is_detail,
    account_type,
    is_system,
    fl_parent_account,
    COALESCE(balance, 0)::float8 AS balance
"""


async def list_accounts(
    search: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> CoaList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, where_params = _build_where(search)

    total_row = await fetch_one(
        f"SELECT COUNT(*)::int AS c FROM transaction.account {where}",
        *where_params,
    )
    total_count = int((total_row or {}).get("c", 0))

    stat_rows = await fetch_all(
        f"""
        SELECT account_type, COUNT(*)::int AS c
        FROM transaction.account
        {where}
        GROUP BY account_type
        """,
        *where_params,
    )
    by_type: dict[str, int] = {}
    for r in stat_rows:
        label = TYPE_LABELS.get((r["account_type"] or "").strip(), "Lainnya")
        by_type[label] = by_type.get(label, 0) + int(r["c"])

    offset = (page - 1) * page_size
    limit_pos = len(where_params) + 1
    offset_pos = len(where_params) + 2
    page_rows = await fetch_all(
        f"""
        SELECT {_SELECT_COLS}
        FROM transaction.account
        {where}
        ORDER BY account_code
        LIMIT ${limit_pos} OFFSET ${offset_pos}
        """,
        *(where_params + [page_size, offset]),
    )

    coa_rows = [_to_row(r) for r in page_rows]
    total_pages = (total_count + page_size - 1) // page_size if total_count else 0

    return CoaList(
        rows=coa_rows,
        stats=CoaStats(total=total_count, by_type=by_type),
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total_count,
            total_pages=total_pages,
        ),
    )


async def list_all_rows(
    search: str | None = None,
    max_rows: int = 10000,
) -> list[CoaRow]:
    """Return all rows matching filter (no pagination). Capped for safety."""
    where, where_params = _build_where(search)
    rows = await fetch_all(
        f"""
        SELECT {_SELECT_COLS}
        FROM transaction.account
        {where}
        ORDER BY account_code
        LIMIT {int(max_rows)}
        """,
        *where_params,
    )
    return [_to_row(r) for r in rows]

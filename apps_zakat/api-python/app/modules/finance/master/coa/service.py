from __future__ import annotations

from app.modules.coa.schema import (
    TYPE_LABELS,
    CoaList,
    CoaRow,
    CoaStats,
    Pagination,
)
from app.shared.db import fetch_all, fetch_one


_VALID_TYPE_CODES = set(TYPE_LABELS.keys())  # {"A","L","E","I","X"}


def _parse_types(types: str | None) -> list[str]:
    if not types:
        return []
    return [t.strip().upper() for t in types.split(",") if t.strip().upper() in _VALID_TYPE_CODES]


def _build_where(
    search: str | None,
    types: str | None = None,
    is_detail: str | None = None,
    max_level: int | None = None,
) -> tuple[str, list]:
    conds: list[str] = []
    params: list = []

    if search and search.strip():
        params.append(f"%{search.strip().lower()}%")
        conds.append(
            f"(LOWER(account_code) LIKE ${len(params)} "
            f"OR LOWER(COALESCE(account_name, '')) LIKE ${len(params)})"
        )

    type_codes = _parse_types(types)
    if type_codes:
        params.append(type_codes)
        conds.append(f"account_type = ANY(${len(params)}::text[])")

    if is_detail and is_detail.upper() in ("T", "F"):
        params.append(is_detail.upper())
        conds.append(f"UPPER(COALESCE(is_detail, '')) = ${len(params)}")

    if max_level is not None and max_level >= 0:
        params.append(max_level)
        conds.append(f"account_level <= ${len(params)}")

    where = "WHERE " + " AND ".join(conds) if conds else ""
    return where, params


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
    types: str | None = None,
    is_detail: str | None = None,
    max_level: int | None = None,
    page: int = 1,
    page_size: int = 50,
) -> CoaList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, where_params = _build_where(search, types, is_detail, max_level)

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
    types: str | None = None,
    is_detail: str | None = None,
    max_level: int | None = None,
    max_rows: int = 10000,
) -> list[CoaRow]:
    where, where_params = _build_where(search, types, is_detail, max_level)
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

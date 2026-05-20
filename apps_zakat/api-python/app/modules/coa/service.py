from __future__ import annotations

from app.modules.coa.schema import TYPE_LABELS, CoaList, CoaRow, CoaStats
from app.shared.db import fetch_all


async def list_accounts(search: str | None = None, limit: int = 1000) -> CoaList:
    where = ""
    params: list = []
    if search and search.strip():
        params.append(f"%{search.strip().lower()}%")
        where = "WHERE LOWER(account_code) LIKE $1 OR LOWER(COALESCE(account_name, '')) LIKE $1"

    rows = await fetch_all(
        f"""
        SELECT
            account_code,
            account_name,
            account_level,
            is_detail,
            account_type,
            is_system,
            fl_parent_account,
            COALESCE(balance, 0)::float8 AS balance
        FROM transaction.account
        {where}
        ORDER BY account_code
        LIMIT {int(limit)}
        """,
        *params,
    )

    coa_rows = [
        CoaRow(
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
        for r in rows
    ]

    stats = CoaStats(
        total=len(coa_rows),
        by_type={
            label: sum(1 for x in coa_rows if x.type_label == label)
            for label in (set(TYPE_LABELS.values()) | {"Lainnya"})
        },
    )

    return CoaList(rows=coa_rows, stats=stats)

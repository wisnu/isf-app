"""Report service — laporan jurnal harian (fase view-based).

Baca via pool **dwh** (read-only). Sumber: dwh.v_journal_daily (membungkus
transaction.* legacy) + enterprise.cabang untuk daftar cabang. Fase berikut
bisa diganti tabel ETL independen tanpa ubah kontrak.
"""

from __future__ import annotations

from datetime import date

from app.shared.db import fetch_all_dwh, fetch_one_dwh, ping_dwh

# Batas baris aman untuk export sync (lihat spec; async = fase 2).
CAP = 50_000


async def dwh_health() -> bool:
    return await ping_dwh()


def _journal_where(branch: str | None, begin: str, end: str) -> tuple[str, list]:
    """Bangun WHERE + args positional. branch None → semua cabang.
    begin/end ISO string → date object (asyncpg meng-encode param ::date)."""
    args: list = [date.fromisoformat(begin), date.fromisoformat(end)]
    clause = "journal_date >= $1::date AND journal_date < ($2::date + INTERVAL '1 day')"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    return clause, args


async def journal_daily_count(branch: str | None, begin: str, end: str) -> int:
    clause, args = _journal_where(branch, begin, end)
    row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_journal_daily WHERE {clause}", *args
    )
    return int(row["n"]) if row else 0


_SELECT_COLS = """
    to_char(journal_date, 'YYYY-MM-DD') AS journal_date,
    journal_no, transactionno, account_branch_code,
    account_code, account_name, subaccountcode, subaccountname, description,
    COALESCE(debit_ekuiv, 0)::float8  AS debit_ekuiv,
    COALESCE(credit_ekuiv, 0)::float8 AS credit_ekuiv,
    inputer
"""

_ORDER = "ORDER BY journal_date, journal_no, transactionno, debit_ekuiv DESC"


async def journal_daily_page(
    branch: str | None, begin: str, end: str, page: int, page_size: int
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await journal_daily_count(branch, begin, end)
    clause, args = _journal_where(branch, begin, end)
    offset = (page - 1) * page_size
    args_page = [*args, page_size, offset]
    sql = (
        f"SELECT {_SELECT_COLS} FROM dwh.v_journal_daily WHERE {clause} "
        f"{_ORDER} LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}"
    )
    rows = await fetch_all_dwh(sql, *args_page)
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


async def journal_daily_rows(branch: str | None, begin: str, end: str) -> list[dict] | None:
    """Semua baris (sampai CAP) untuk export. None bila DB down."""
    if not await ping_dwh():
        return None
    clause, args = _journal_where(branch, begin, end)
    sql = (
        f"SELECT {_SELECT_COLS} FROM dwh.v_journal_daily WHERE {clause} "
        f"{_ORDER} LIMIT {CAP}"
    )
    return await fetch_all_dwh(sql, *args)


async def list_branches(scope: str) -> list[dict] | None:
    """scope='all' → semua cabang aktif; selain itu → satu cabang (kode)."""
    if not await ping_dwh():
        return None
    if scope == "all":
        return await fetch_all_dwh(
            "SELECT kode_cabang AS code, nama_cabang AS name FROM enterprise.cabang "
            "WHERE status_aktif = 'T' ORDER BY kode_cabang"
        )
    return await fetch_all_dwh(
        "SELECT kode_cabang AS code, nama_cabang AS name FROM enterprise.cabang "
        "WHERE kode_cabang = $1",
        scope,
    )


# ── List Transaksi Umum (GT) — grouped master-detail ─────────────────────────

def _gt_where(branch: str | None, begin: str, end: str) -> tuple[str, list]:
    args: list = [date.fromisoformat(begin), date.fromisoformat(end)]
    clause = "actualdate >= $1::date AND actualdate < ($2::date + INTERVAL '1 day')"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    return clause, args


async def general_transaction_page(
    branch: str | None, begin: str, end: str, page: int, page_size: int
) -> dict | None:
    if not await ping_dwh():
        return None
    clause, args = _gt_where(branch, begin, end)

    tx_total_row = await fetch_one_dwh(
        f"SELECT count(DISTINCT transactionid) AS n FROM dwh.v_general_transaction WHERE {clause}",
        *args,
    )
    item_total_row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_general_transaction WHERE {clause}", *args
    )
    tx_total = int(tx_total_row["n"]) if tx_total_row else 0
    item_total = int(item_total_row["n"]) if item_total_row else 0

    offset = (page - 1) * page_size
    headers = await fetch_all_dwh(
        f"""
        SELECT transactionid, transactionno,
               to_char(min(transactiondate), 'YYYY-MM-DD') AS transactiondate,
               to_char(min(actualdate), 'YYYY-MM-DD')      AS actualdate,
               min(header_description)                     AS description,
               min(inputer)                                AS inputer
        FROM dwh.v_general_transaction WHERE {clause}
        GROUP BY transactionid, transactionno
        ORDER BY min(actualdate), transactionid
        LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}
        """,
        *args, page_size, offset,
    )
    ids = [h["transactionid"] for h in headers]
    items_by_tx: dict[int, list] = {i: [] for i in ids}
    if ids:
        item_rows = await fetch_all_dwh(
            """
            SELECT transactionid, refaccountno, refaccountname, mutationtype,
                   COALESCE(amount, 0)::float8 AS amount, item_description,
                   budget_code, budget_item_description
            FROM dwh.v_general_transaction
            WHERE transactionid = ANY($1::int[])
            ORDER BY transactionid
            """,
            ids,
        )
        for r in item_rows:
            items_by_tx.setdefault(r["transactionid"], []).append(
                {k: v for k, v in r.items() if k != "transactionid"}
            )

    transactions = [
        {
            "transactionno": h["transactionno"],
            "transactiondate": h["transactiondate"],
            "actualdate": h["actualdate"],
            "description": h["description"],
            "inputer": h["inputer"],
            "items": items_by_tx.get(h["transactionid"], []),
        }
        for h in headers
    ]
    return {
        "transactions": transactions,
        "total": tx_total,
        "item_total": item_total,
        "capped": item_total > CAP,
        "page": page,
        "page_size": page_size,
    }


async def general_transaction_rows(branch: str | None, begin: str, end: str) -> list[dict] | None:
    """Semua item rows (sampai CAP) untuk export, ordered per transaksi."""
    if not await ping_dwh():
        return None
    clause, args = _gt_where(branch, begin, end)
    return await fetch_all_dwh(
        f"""
        SELECT transactionid, transactionno,
               to_char(transactiondate, 'YYYY-MM-DD') AS transactiondate,
               to_char(actualdate, 'YYYY-MM-DD')      AS actualdate,
               header_description, inputer,
               refaccountno, refaccountname, mutationtype,
               COALESCE(amount, 0)::float8 AS amount, item_description,
               budget_code, budget_item_description
        FROM dwh.v_general_transaction WHERE {clause}
        ORDER BY actualdate, transactionid
        LIMIT {CAP}
        """,
        *args,
    )


async def general_transaction_item_count(branch: str | None, begin: str, end: str) -> int:
    clause, args = _gt_where(branch, begin, end)
    row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_general_transaction WHERE {clause}", *args
    )
    return int(row["n"]) if row else 0

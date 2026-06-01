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


# ── Transaksi Kas/Bank Harian (fDailyCash) — per rekening + running balance ──

async def list_cash_accounts(branch: str) -> list[dict] | None:
    if not await ping_dwh():
        return None
    return await fetch_all_dwh(
        "SELECT accountno AS account_no, accountname AS account_name, "
        "cashaccounttype AS account_type FROM transaction.cashaccountall "
        "WHERE branchcode = $1 AND status = 'A' ORDER BY accountname",
        branch,
    )


def _cash_where(account: str, begin: str, end: str) -> tuple[str, list]:
    args: list = [account, date.fromisoformat(begin), date.fromisoformat(end)]
    clause = (
        "account_no = $1 AND actualdate >= $2::date "
        "AND actualdate < ($3::date + INTERVAL '1 day')"
    )
    return clause, args

_NET = "CASE WHEN mutationtype = 'D' THEN amount ELSE -amount END"


async def _cash_begin_balance(account: str, begin: str) -> float:
    row = await fetch_one_dwh(
        f"SELECT COALESCE(SUM({_NET}), 0)::float8 AS bal FROM dwh.v_cash_mutation "
        "WHERE account_no = $1 AND actualdate < $2::date",
        account, date.fromisoformat(begin),
    )
    return float(row["bal"]) if row else 0.0


_CASH_ITEM_COLS = """
    to_char(actualdate, 'YYYY-MM-DD') AS actualdate, transactionno, mutationtype,
    COALESCE(amount, 0)::float8 AS amount, reference_no, description, auth_status, inputer
"""
_CASH_ORDER = "ORDER BY actualdate, transactionitemid"


async def _cash_sums(clause: str, args: list) -> tuple[float, float, int]:
    row = await fetch_one_dwh(
        f"""SELECT
              COALESCE(SUM(CASE WHEN mutationtype='D' THEN amount ELSE 0 END), 0)::float8 AS d,
              COALESCE(SUM(CASE WHEN mutationtype='C' THEN amount ELSE 0 END), 0)::float8 AS c,
              count(*) AS n
            FROM dwh.v_cash_mutation WHERE {clause}""",
        *args,
    )
    return (float(row["d"]), float(row["c"]), int(row["n"])) if row else (0.0, 0.0, 0)


def _attach_running_balance(rows: list[dict], start_balance: float) -> None:
    bal = start_balance
    for r in rows:
        bal += r["amount"] if r["mutationtype"] == "D" else -r["amount"]
        r["balance"] = bal


async def cash_mutation_page(
    account: str, begin: str, end: str, page: int, page_size: int
) -> dict | None:
    if not await ping_dwh():
        return None
    clause, args = _cash_where(account, begin, end)
    begin_balance = await _cash_begin_balance(account, begin)
    total_debit, total_credit, total = await _cash_sums(clause, args)

    offset = (page - 1) * page_size
    # Saldo pada awal page = saldo awal + net dari baris-baris sebelum offset.
    prefix_row = await fetch_one_dwh(
        f"""SELECT COALESCE(SUM(net), 0)::float8 AS s FROM (
              SELECT {_NET} AS net FROM dwh.v_cash_mutation WHERE {clause}
              {_CASH_ORDER} LIMIT ${len(args) + 1}
            ) q""",
        *args, offset,
    )
    start_balance = begin_balance + (float(prefix_row["s"]) if prefix_row else 0.0)

    rows = await fetch_all_dwh(
        f"SELECT {_CASH_ITEM_COLS} FROM dwh.v_cash_mutation WHERE {clause} "
        f"{_CASH_ORDER} LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}",
        *args, page_size, offset,
    )
    _attach_running_balance(rows, start_balance)

    return {
        "account_no": account,
        "begin_balance": begin_balance,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "end_balance": begin_balance + total_debit - total_credit,
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


async def cash_mutation_export(account: str, begin: str, end: str) -> dict | None:
    """Semua rows (sampai CAP) + running balance penuh + ringkasan, utk export."""
    if not await ping_dwh():
        return None
    clause, args = _cash_where(account, begin, end)
    begin_balance = await _cash_begin_balance(account, begin)
    total_debit, total_credit, _total = await _cash_sums(clause, args)
    rows = await fetch_all_dwh(
        f"SELECT {_CASH_ITEM_COLS} FROM dwh.v_cash_mutation WHERE {clause} "
        f"{_CASH_ORDER} LIMIT {CAP}",
        *args,
    )
    _attach_running_balance(rows, begin_balance)
    return {
        "account_no": account,
        "begin_balance": begin_balance,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "end_balance": begin_balance + total_debit - total_credit,
        "rows": rows,
    }


async def cash_mutation_item_count(account: str, begin: str, end: str) -> int:
    clause, args = _cash_where(account, begin, end)
    row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_cash_mutation WHERE {clause}", *args
    )
    return int(row["n"]) if row else 0


async def cash_account_label(account: str) -> str:
    row = await fetch_one_dwh(
        "SELECT accountname FROM transaction.cashaccountall WHERE accountno = $1", account
    )
    name = row["accountname"] if row else None
    return f"{account} - {name}" if name else account


# ── Rekapitulasi Transaksi Kas/Bank (fSummaryCash) — per akun, group valuta ──

async def cash_summary(branch: str, begin: str, end: str) -> dict | None:
    if not await ping_dwh():
        return None
    rows = await fetch_all_dwh(
        """
        SELECT account_no, account_name, currency_code,
          SUM(CASE WHEN mutationtype='D' AND actualdate >= $2::date THEN amount ELSE 0 END)::float8 AS debit,
          SUM(CASE WHEN mutationtype='C' AND actualdate >= $2::date THEN amount ELSE 0 END)::float8 AS credit,
          SUM(CASE WHEN actualdate < $2::date
                   THEN (CASE WHEN mutationtype='D' THEN amount ELSE -amount END)
                   ELSE 0 END)::float8 AS begin_balance
        FROM dwh.v_cash_summary_src
        WHERE branch_code = $1 AND actualdate < ($3::date + INTERVAL '1 day')
        GROUP BY account_no, account_name, currency_code
        ORDER BY currency_code, account_no
        """,
        branch, date.fromisoformat(begin), date.fromisoformat(end),
    )

    groups: list[dict] = []
    by_ccy: dict[str, dict] = {}
    grand = {"begin_balance": 0.0, "total_debit": 0.0, "total_credit": 0.0, "total_end": 0.0}
    for r in rows:
        total = r["debit"] - r["credit"]
        end_balance = r["begin_balance"] + total
        item = {
            "account_no": r["account_no"],
            "account_name": r["account_name"],
            "begin_balance": r["begin_balance"],
            "debit": r["debit"],
            "credit": r["credit"],
            "total": total,
            "end_balance": end_balance,
        }
        ccy = r["currency_code"] or "-"
        g = by_ccy.get(ccy)
        if g is None:
            g = {
                "currency": ccy,
                "rows": [],
                "subtotal": {"begin_balance": 0.0, "debit": 0.0, "credit": 0.0, "total": 0.0, "end_balance": 0.0},
            }
            by_ccy[ccy] = g
            groups.append(g)
        g["rows"].append(item)
        st = g["subtotal"]
        st["begin_balance"] += item["begin_balance"]
        st["debit"] += item["debit"]
        st["credit"] += item["credit"]
        st["total"] += total
        st["end_balance"] += end_balance
        # Grand total — semua IDR (rate=1); konversi multi-valuta menyusul.
        grand["begin_balance"] += item["begin_balance"]
        grand["total_debit"] += item["debit"]
        grand["total_credit"] += item["credit"]
        grand["total_end"] += end_balance

    return {"groups": groups, "grand": grand, "period": _period(begin, end)}


def _period(begin: str, end: str) -> str:
    return begin if begin == end else f"{begin} s/d {end}"

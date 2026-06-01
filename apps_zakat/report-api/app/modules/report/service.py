"""Report service — laporan jurnal harian (fase view-based).

Baca via pool **dwh** (read-only). Sumber: dwh.v_journal_daily (membungkus
transaction.* legacy) + enterprise.cabang untuk daftar cabang. Fase berikut
bisa diganti tabel ETL independen tanpa ubah kontrak.
"""

from __future__ import annotations

import calendar
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


# ── Monitoring Saldo Kas/Bank Bulanan (fSummaryCashMonthly) ──────────────────

_CASHTYPE_LABEL = {"A": "BANK", "R": "KAS CABANG", "P": "PETTY CASH"}
MONTHS_ID = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


async def cash_monthly(branch: str, year: int) -> dict | None:
    if not await ping_dwh():
        return None
    # 12 tanggal akhir bulan kalender utk year → param $2..$13.
    month_ends = [date(year, m, calendar.monthrange(year, m)[1]) for m in range(1, 13)]
    net = "CASE WHEN mutationtype='D' THEN amount ELSE -amount END"
    cols = ",\n".join(
        f"SUM(CASE WHEN actualdate <= ${i + 2}::date THEN {net} ELSE 0 END)::float8 AS balance_{i + 1}"
        for i in range(12)
    )
    sql = f"""
        SELECT account_no, account_name, account_type,
               {cols}
        FROM dwh.v_cash_summary_src
        WHERE branch_code = $1 AND actualdate <= $13::date
        GROUP BY account_no, account_name, account_type
        ORDER BY account_type, account_no
    """
    rows = await fetch_all_dwh(sql, branch, *month_ends)

    groups: list[dict] = []
    by_type: dict[str, dict] = {}
    for r in rows:
        balances = [r[f"balance_{m}"] for m in range(1, 13)]
        atype = r["account_type"] or "-"
        g = by_type.get(atype)
        if g is None:
            g = {
                "type": atype,
                "type_label": _CASHTYPE_LABEL.get(atype, "LAINNYA"),
                "rows": [],
                "totals": [0.0] * 12,
            }
            by_type[atype] = g
            groups.append(g)
        g["rows"].append(
            {"account_no": r["account_no"], "account_name": r["account_name"], "balances": balances}
        )
        for m in range(12):
            g["totals"][m] += balances[m]

    return {"groups": groups, "year": year, "months": MONTHS_ID}


# ── Trial Balance (fTrialBalance) — neraca saldo per detail account ───────────
#
# Legacy-faithful (GetTrialBalancePerCabang.py, cabang `onlydetail`):
#   saldo_awal  = balancecumulative max(datevalue <= begin-1)  per accountinstance
#   saldo_akhir = balancecumulative max(datevalue <= end)
#   debit/kredit= SUM dailybalance.debit/credit dalam [begin, end]
# Bila end >= today, tambah mutasi journalitem [begin, end] (langsung + lawan
# fl_cpa_accountinstance) karena dailybalance belum dihitung utk tanggal itu.

_ACCTYPE_LABEL = {
    "A": "AKTIVA",
    "L": "KEWAJIBAN",
    "E": "DANA / EKUITAS",
    "I": "PENDAPATAN",
    "X": "BEBAN",
}
_ACCTYPE_ORDER = {"A": 0, "L": 1, "E": 2, "I": 3, "X": 4}


class ReportValidationError(ValueError):
    """Param tidak valid (mis. begin > end) → 422 di router."""


def _tb_per_instance_sql(branch: str | None, with_journal: bool) -> str:
    """Query agregat per (account_code, branch_code).
    Positional args: $1=begin-1, $2=end, $3=begin(mutation), [$4=branch]."""
    branch_clause = "AND ai.branch_code = $4" if branch else ""

    if with_journal:
        journ_cte = """,
        journ AS (
            SELECT accountinstance_id,
                   SUM(amount_debit)  AS debit,
                   SUM(amount_credit) AS credit,
                   SUM(bal)           AS balance
            FROM (
                SELECT ji.accountinstance_id AS accountinstance_id,
                       ji.amount_debit, ji.amount_credit,
                       (ji.amount_credit - ji.amount_debit) * COALESCE(ai.balance_sign, 1) AS bal
                FROM transaction.journal j
                JOIN transaction.journalitem ji ON j.journal_no = ji.fl_journal
                JOIN transaction.accountinstance ai ON ai.accountinstance_id = ji.accountinstance_id
                WHERE j.journal_date >= $3::date AND j.journal_date <= $2::date
                UNION ALL
                SELECT ai2.accountinstance_id,
                       ji.amount_debit, ji.amount_credit,
                       (ji.amount_credit - ji.amount_debit) AS bal
                FROM transaction.journal j
                JOIN transaction.journalitem ji ON j.journal_no = ji.fl_journal
                JOIN transaction.accountinstance ai1 ON ai1.accountinstance_id = ji.accountinstance_id
                JOIN transaction.accountinstance ai2 ON ai2.accountinstance_id = ai1.fl_cpa_accountinstance
                WHERE j.journal_date >= $3::date AND j.journal_date <= $2::date
            ) u
            GROUP BY accountinstance_id
        )"""
        journ_join = "LEFT JOIN journ jn ON jn.accountinstance_id = i.accountinstance_id"
        j_debit = "SUM(COALESCE(jn.debit, 0))::float8   AS j_debit"
        j_credit = "SUM(COALESCE(jn.credit, 0))::float8  AS j_credit"
        j_balance = "SUM(COALESCE(jn.balance, 0))::float8 AS j_balance"
    else:
        journ_cte = ""
        journ_join = ""
        j_debit = "0::float8 AS j_debit"
        j_credit = "0::float8 AS j_credit"
        j_balance = "0::float8 AS j_balance"

    return f"""
        WITH inst AS (
            SELECT ai.accountinstance_id, ai.account_code, ai.branch_code
            FROM transaction.accountinstance ai
            WHERE 1=1 {branch_clause}
        ),
        bal_begin AS (
            SELECT DISTINCT ON (d.accountinstance_id) d.accountinstance_id, d.balancecumulative
            FROM transaction.dailybalance d
            WHERE d.datevalue <= $1::date
            ORDER BY d.accountinstance_id, d.datevalue DESC
        ),
        bal_end AS (
            SELECT DISTINCT ON (d.accountinstance_id) d.accountinstance_id, d.balancecumulative
            FROM transaction.dailybalance d
            WHERE d.datevalue <= $2::date
            ORDER BY d.accountinstance_id, d.datevalue DESC
        ),
        mut AS (
            SELECT accountinstance_id, SUM(debit) AS debit, SUM(credit) AS credit
            FROM transaction.dailybalance
            WHERE datevalue >= $3::date AND datevalue <= $2::date
            GROUP BY accountinstance_id
        ){journ_cte}
        SELECT a.account_code, a.account_name, a.account_type, i.branch_code,
               SUM(COALESCE(bb.balancecumulative, 0))::float8 AS saldo_awal,
               SUM(COALESCE(be.balancecumulative, 0))::float8 AS saldo_akhir,
               SUM(COALESCE(m.debit, 0))::float8  AS debit,
               SUM(COALESCE(m.credit, 0))::float8 AS credit,
               {j_debit}, {j_credit}, {j_balance}
        FROM inst i
        JOIN transaction.account a ON a.account_code = i.account_code
        LEFT JOIN bal_begin bb ON bb.accountinstance_id = i.accountinstance_id
        LEFT JOIN bal_end be   ON be.accountinstance_id = i.accountinstance_id
        LEFT JOIN mut m        ON m.accountinstance_id = i.accountinstance_id
        {journ_join}
        WHERE a.is_detail = 'T' AND a.account_type IN ('A','L','E','I','X')
        GROUP BY a.account_code, a.account_name, a.account_type, i.branch_code
        ORDER BY i.branch_code, a.account_code
    """


async def trial_balance(
    branch: str | None, begin: str, end: str, today: date
) -> dict | None:
    b = date.fromisoformat(begin)
    e = date.fromisoformat(end)
    if b > e:
        raise ReportValidationError("Rentang tanggal filter salah (awal > akhir).")
    if not await ping_dwh():
        return None

    begin_minus_1 = date.fromordinal(b.toordinal() - 1)
    with_journal = e >= today
    sql = _tb_per_instance_sql(branch, with_journal)
    args: list = [begin_minus_1, e, b]
    if branch:
        args.append(branch)
    rows = await fetch_all_dwh(sql, *args)

    konsolidasi = branch is None
    by_acct: dict = {}
    order: list = []
    for r in rows:
        key = r["account_code"] if konsolidasi else (r["account_code"], r["branch_code"])
        agg = by_acct.get(key)
        debit = r["debit"] + (r["j_debit"] if with_journal else 0.0)
        credit = r["credit"] + (r["j_credit"] if with_journal else 0.0)
        saldo_akhir = r["saldo_akhir"] + (r["j_balance"] if with_journal else 0.0)
        if agg is None:
            agg = {
                "account_code": r["account_code"],
                "account_name": r["account_name"],
                "account_type": r["account_type"],
                "branch_code": None if konsolidasi else r["branch_code"],
                "saldo_awal": 0.0,
                "debit": 0.0,
                "credit": 0.0,
                "saldo_akhir": 0.0,
            }
            by_acct[key] = agg
            order.append(key)
        agg["saldo_awal"] += r["saldo_awal"]
        agg["debit"] += debit
        agg["credit"] += credit
        agg["saldo_akhir"] += saldo_akhir

    # group per account_type
    groups: list[dict] = []
    by_type: dict[str, dict] = {}
    grand = {"saldo_awal": 0.0, "debit": 0.0, "credit": 0.0, "saldo_akhir": 0.0}
    for key in order:
        a = by_acct[key]
        atype = a["account_type"]
        g = by_type.get(atype)
        if g is None:
            g = {
                "type": atype,
                "type_label": _ACCTYPE_LABEL.get(atype, atype),
                "rows": [],
                "subtotal": {"saldo_awal": 0.0, "debit": 0.0, "credit": 0.0, "saldo_akhir": 0.0},
            }
            by_type[atype] = g
            groups.append(g)
        g["rows"].append(a)
        for k in ("saldo_awal", "debit", "credit", "saldo_akhir"):
            g["subtotal"][k] += a[k]
            grand[k] += a[k]

    groups.sort(key=lambda g: _ACCTYPE_ORDER.get(g["type"], 99))
    return {
        "groups": groups,
        "grand_total": grand,
        "begin": begin,
        "end": end,
        "konsolidasi": konsolidasi,
        "with_journal": with_journal,
    }


# ── Neraca (fNeraca / neraca5.py) — hierarkis via accounthierarchy ────────────
#
# Saldo per account = rollup balancecumulative semua child (accounthierarchy)
# pada max(datevalue <= tanggal). Tipe A/L/E, level < maxlevel, indent per level.
# Dua kolom: posisi tanggal + pembanding akhir periode sebelumnya.

_NERACA_MAXLEVEL = 99  # level "semua"


def _prev_period_end(t: date, jenisperiode: str) -> date:
    """Akhir periode sebelumnya. Tahunan → 31 Des thn lalu; Bulanan → akhir bln lalu."""
    if jenisperiode == "T":
        first = date(t.year, 1, 1)
    else:
        first = date(t.year, t.month, 1)
    return date.fromordinal(first.toordinal() - 1)


def _neraca_balance_cte(label: str, date_param: int, branch_param: int | None) -> str:
    """CTE rollup saldo per parent account pada tanggal $date_param.
    branch_param None → semua cabang (konsolidasi)."""
    branch_clause = f"AND ai.branch_code = ${branch_param}" if branch_param else ""
    return f"""
        maxd_{label} AS (
            SELECT accountinstance_id, MAX(datevalue) AS maxdate
            FROM transaction.dailybalance
            WHERE datevalue <= ${date_param}::date
            GROUP BY accountinstance_id
        ),
        bal_{label} AS (
            SELECT h.fl_parentaccountcode AS account_code,
                   SUM(d1.balancecumulative) AS balance
            FROM transaction.accounthierarchy h
            JOIN transaction.accountinstance ai ON h.fl_childaccountcode = ai.account_code
            JOIN transaction.dailybalance d1 ON d1.accountinstance_id = ai.accountinstance_id
            JOIN maxd_{label} d2 ON d2.accountinstance_id = d1.accountinstance_id
                                AND d1.datevalue = d2.maxdate
            WHERE 1=1 {branch_clause}
            GROUP BY h.fl_parentaccountcode
        )"""


async def neraca(
    branch: str | None, tanggal: str, jenisperiode: str, level: int, today: date
) -> dict | None:
    t = date.fromisoformat(tanggal)
    if t > today:
        raise ReportValidationError("Tanggal tidak boleh lebih besar dari hari ini.")
    jp = "T" if (jenisperiode or "T").upper().startswith("T") else "B"
    prev = _prev_period_end(t, jp)
    maxlevel = level if level and level > 0 else _NERACA_MAXLEVEL
    if not await ping_dwh():
        return None

    # args: $1=tanggal, $2=prev, $3=maxlevel, [$4=branch]
    branch_param = 4 if branch else None
    sql = f"""
        WITH {_neraca_balance_cte('now', 1, branch_param)},
        {_neraca_balance_cte('prev', 2, branch_param)}
        SELECT ac.account_code, ac.account_name, ac.account_level, ac.account_type,
               COALESCE(b.balance, 0)::float8  AS balance,
               COALESCE(bp.balance, 0)::float8 AS balance_prev
        FROM transaction.account ac
        LEFT JOIN bal_now b   ON b.account_code = ac.account_code
        LEFT JOIN bal_prev bp ON bp.account_code = ac.account_code
        WHERE ac.account_type IN ('A','L','E') AND ac.account_level < $3
        ORDER BY ac.account_code
    """
    args: list = [t, prev, maxlevel]
    if branch:
        args.append(branch)
    rows = await fetch_all_dwh(sql, *args)

    aktiva: list[dict] = []
    pasiva: list[dict] = []
    tot_a = tot_a_prev = tot_p = tot_p_prev = 0.0
    for r in rows:
        item = {
            "account_code": r["account_code"],
            "account_name": r["account_name"],
            "account_level": r["account_level"],
            "account_type": r["account_type"],
            "balance": r["balance"],
            "balance_prev": r["balance_prev"],
        }
        if r["account_type"] == "A":
            aktiva.append(item)
            if r["account_level"] == 0:
                tot_a += r["balance"]
                tot_a_prev += r["balance_prev"]
        else:  # L, E
            pasiva.append(item)
            if r["account_level"] == 0:
                tot_p += r["balance"]
                tot_p_prev += r["balance_prev"]

    selisih = tot_a - tot_p
    return {
        "aktiva": aktiva,
        "pasiva": pasiva,
        "total_aktiva": tot_a,
        "total_aktiva_prev": tot_a_prev,
        "total_pasiva": tot_p,
        "total_pasiva_prev": tot_p_prev,
        "selisih": selisih,
        "status_balance": "BALANCE" if abs(selisih) < 0.01 else "TIDAK BALANCE",
        "tanggal": tanggal,
        "tanggal_prev": prev.isoformat(),
        "jenisperiode": "Tahunan" if jp == "T" else "Bulanan",
        "konsolidasi": branch is None,
    }


# ── Arus Kas (fArusKas / S_ArusKas.py) — config-driven via BalanceSumItem ─────
#
# Mutasi per item (group AK_MUT) = net signed (A/X → debit-credit, else
# credit-debit) × nilai_kurs atas journalitem dalam [begin, end]. Saldo kas awal
# (group AK_BAL 'kasbalance') = rolled-up balancecumulative_ekuiv pada begin-1.
# Layout 3 seksi (Operasi/Investasi/Pendanaan) di-port faithful dari S_ArusKas.


async def _balancesum_mutations(
    branch: str | None, begin: date, end: date, group_code: str
) -> dict:
    """item_code(lower) → {net, debit, credit} mutasi journalitem dalam [begin,end]
    untuk BalanceSumGroup `group_code` (mis. AK_MUT / PD_MUT)."""
    args: list = [begin, end, group_code]
    branch_clause = ""
    if branch:
        args.append(branch)
        branch_clause = f"AND ai.branch_code = ${len(args)}"
    sql = f"""
        SELECT v.item_code,
            SUM(CASE WHEN v.account_type IN ('A','X')
                     THEN (ji.amount_debit - ji.amount_credit) * ji.nilai_kurs
                     ELSE (ji.amount_credit - ji.amount_debit) * ji.nilai_kurs END)::float8 AS net,
            SUM(ji.amount_debit  * ji.nilai_kurs)::float8 AS debit,
            SUM(ji.amount_credit * ji.nilai_kurs)::float8 AS credit
        FROM dwh.v_aruskas_item_account v
        JOIN transaction.accountinstance ai ON ai.account_code = v.account_code
        JOIN transaction.journalitem ji     ON ji.accountinstance_id = ai.accountinstance_id
        JOIN transaction.journal j           ON j.journal_no = ji.fl_journal
        WHERE v.group_code = $3
          AND j.journal_date >= $1::date
          AND j.journal_date < ($2::date + INTERVAL '1 day')
          {branch_clause}
        GROUP BY v.item_code
    """
    rows = await fetch_all_dwh(sql, *args)
    return {r["item_code"]: {"net": r["net"], "debit": r["debit"], "credit": r["credit"]} for r in rows}


async def _balancesum_balance(
    branch: str | None, at: date, group_code: str
) -> dict:
    """item_code(lower) → balancecumulative_ekuiv pada max(datevalue<=at), per item
    BalanceSumGroup `group_code` (mis. AK_BAL / PD_BAL)."""
    args: list = [at, group_code]
    branch_clause = ""
    if branch:
        args.append(branch)
        branch_clause = f"AND ai.branch_code = ${len(args)}"
    sql = f"""
        SELECT v.item_code, COALESCE(SUM(d1.balancecumulative_ekuiv), 0)::float8 AS bal
        FROM dwh.v_aruskas_item_account v
        JOIN transaction.accountinstance ai ON ai.account_code = v.account_code
        JOIN transaction.dailybalance d1    ON d1.accountinstance_id = ai.accountinstance_id
        JOIN (
            SELECT accountinstance_id, MAX(datevalue) AS t
            FROM transaction.dailybalance WHERE datevalue <= $1::date
            GROUP BY accountinstance_id
        ) d2 ON d1.accountinstance_id = d2.accountinstance_id AND d1.datevalue = d2.t
        WHERE v.group_code = $2 {branch_clause}
        GROUP BY v.item_code
    """
    rows = await fetch_all_dwh(sql, *args)
    return {r["item_code"]: r["bal"] for r in rows}


async def aruskas(branch: str | None, begin: str, end: str, today: date) -> dict | None:
    b = date.fromisoformat(begin)
    e = date.fromisoformat(end)
    if b > e:
        raise ReportValidationError("Rentang tanggal filter salah (awal > akhir).")
    if not await ping_dwh():
        return None

    mut = await _balancesum_mutations(branch, b, e, "AK_MUT")
    opening_d = await _balancesum_balance(branch, date.fromordinal(b.toordinal() - 1), "AK_BAL")
    opening = sum(opening_d.values())

    def mb(item: str) -> float:
        return (mut.get(item) or {}).get("net", 0.0) or 0.0

    def td(item: str) -> float:
        return (mut.get(item) or {}).get("debit", 0.0) or 0.0

    def tc(item: str) -> float:
        return (mut.get(item) or {}).get("credit", 0.0) or 0.0

    operasi = [
        {"label": "Penerimaan Zakat", "value": mb("opspenerimaanzakat")},
        {"label": "Penerimaan Infaq/Shadaqah", "value": mb("opspenerimaaninfaq")},
        {"label": "Penerimaan Bagian Amil", "value": mb("opspenerimaanamil")},
        {"label": "Penyaluran Zakat", "value": -mb("opspenyaluranzakat")},
        {"label": "Penyaluran Infaq/Shadaqah",
         "value": -(mb("opspenyaluraninfaq") - mb("opsdepresiasikelolaaninfaq"))},
        {"label": "Penggunaan Dana Amil",
         "value": -(mb("opspenyaluranamil") - mb("opsdepresiasiassetamil"))},
    ]
    investasi = [
        {"label": "Pembelian Aset Tetap", "value": -td("invassettetap")},
        {"label": "Pembelian Aset Kelolaan", "value": -td("invassetkelolaan")},
        {"label": "Pelepasan Aset Tetap", "value": tc("invassettetap")},
        {"label": "Pelepasan Aset Kelolaan", "value": tc("invassetkelolaan")},
    ]
    pendanaan = [
        {"label": "Piutang Bergulir (Qardh)", "value": -mb("piutangbergulir")},
        {"label": "Piutang Penyaluran", "value": -mb("piutangpenyaluran")},
        {"label": "Persediaan", "value": -mb("persediaan")},
        {"label": "Barang Berharga", "value": -mb("barangberharga")},
        {"label": "Uang Muka", "value": -mb("uangmuka")},
        {"label": "Biaya Dibayar Dimuka", "value": -mb("biayadibayardimuka")},
        {"label": "Piutang Talangan Dana Zakat", "value": -mb("piutangtalangandanazakat")},
        {"label": "Piutang Talangan Dana Infaq", "value": -mb("piutangtalangandanainfaq")},
        {"label": "Piutang Talangan Dana Amil", "value": -mb("piutangtalangandanaamil")},
        {"label": "Hutang Pihak Ketiga", "value": mb("hutangpihakketiga")},
        {"label": "Biaya Yang Masih Harus Dibayar", "value": mb("biayayangmasihharusdibayar")},
        {"label": "Titipan Dana", "value": mb("titipandana")},
        {"label": "Dana Non Halal", "value": mb("dananonhalal")},
        {"label": "Hutang Pajak", "value": mb("hutangpajak")},
        {"label": "Hutang Talangan Dana Zakat", "value": mb("hutangtalangandanazakat")},
        {"label": "Hutang Talangan Dana Infaq", "value": mb("hutangtalangandanainfaq")},
        {"label": "Hutang Talangan Dana Amil", "value": mb("hutangtalangandanaamil")},
        {"label": "Kewajiban Imbalan Pasca Kerja", "value": mb("kewajibanimbalanpascakerja")},
        {"label": "Liabilitas Lainnya",
         "value": mb("liabilitasjangkapendeklainnya") + mb("liabilitasjangkapanjanglainnya")},
    ]

    def _sec(title: str, lines: list[dict]) -> dict:
        return {"title": title, "lines": lines, "subtotal": sum(x["value"] for x in lines)}

    sections = [
        _sec("Arus Kas dari Aktivitas Operasi", operasi),
        _sec("Arus Kas dari Aktivitas Investasi", investasi),
        _sec("Arus Kas dari Aktivitas Pendanaan", pendanaan),
    ]
    kenaikan = sum(s["subtotal"] for s in sections)
    return {
        "sections": sections,
        "kenaikan_bersih": kenaikan,
        "saldo_awal": opening,
        "saldo_akhir": opening + kenaikan,
        "begin": begin,
        "end": end,
        "konsolidasi": branch is None,
    }


# ── Buku Besar (fGeneralLedger) — per akun detail + saldo awal/akhir ──────────
#
# Posting langsung (journalitem.fl_account) per akun detail; saldo awal =
# rolled balancecumulative_ekuiv pada max(datevalue < begin); net per akun
# (A/X → debit-credit, else credit-debit); saldo akhir = awal + net.


async def list_detail_accounts(branch: str | None) -> list[dict] | None:
    if not await ping_dwh():
        return None
    args: list = []
    where = "a.is_detail = 'T'"
    if branch:
        args.append(branch)
        where += (
            " AND EXISTS (SELECT 1 FROM transaction.accountinstance ai "
            f"WHERE ai.account_code = a.account_code AND ai.branch_code = ${len(args)})"
        )
    return await fetch_all_dwh(
        f"SELECT a.account_code AS code, a.account_name AS name "
        f"FROM transaction.account a WHERE {where} ORDER BY a.account_code",
        *args,
    )


async def _gl_opening(branch: str | None, begin: date, account: str | None) -> dict:
    args: list = [begin]
    clause = ""
    if branch:
        args.append(branch)
        clause += f" AND ai.branch_code = ${len(args)}"
    if account:
        args.append(account)
        clause += f" AND ai.account_code = ${len(args)}"
    sql = f"""
        SELECT ai.account_code, COALESCE(SUM(d1.balancecumulative_ekuiv), 0)::float8 AS bal
        FROM transaction.accountinstance ai
        JOIN transaction.dailybalance d1 ON d1.accountinstance_id = ai.accountinstance_id
        JOIN (
            SELECT accountinstance_id, MAX(datevalue) AS t
            FROM transaction.dailybalance WHERE datevalue < $1::date
            GROUP BY accountinstance_id
        ) d2 ON d1.accountinstance_id = d2.accountinstance_id AND d1.datevalue = d2.t
        WHERE 1=1 {clause}
        GROUP BY ai.account_code
    """
    rows = await fetch_all_dwh(sql, *args)
    return {r["account_code"]: r["bal"] for r in rows}


async def general_ledger(
    branch: str | None, begin: str, end: str, account: str | None
) -> dict | None:
    b = date.fromisoformat(begin)
    e = date.fromisoformat(end)
    if b > e:
        raise ReportValidationError("Rentang tanggal filter salah (awal > akhir).")
    if not await ping_dwh():
        return None

    opening = await _gl_opening(branch, b, account)

    args: list = [b, e]
    clause = ""
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    if account:
        args.append(account)
        clause += f" AND account_code = ${len(args)}"
    sql = f"""
        SELECT account_code, account_type, account_name,
               to_char(journal_date, 'YYYY-MM-DD') AS journal_date,
               transactionno, additionaldescription, description,
               subaccountcode, subaccountname,
               COALESCE(debit_ekuiv, 0)::float8  AS debit_ekuiv,
               COALESCE(credit_ekuiv, 0)::float8 AS credit_ekuiv,
               lawan_code, lawan_name
        FROM dwh.v_general_ledger
        WHERE journal_date >= $1::date AND journal_date < ($2::date + INTERVAL '1 day')
          {clause}
        ORDER BY account_code, journal_date, transactionno, journal_no
        LIMIT {CAP + 1}
    """
    rows = await fetch_all_dwh(sql, *args)
    capped = len(rows) > CAP
    rows = rows[:CAP]

    accounts: list[dict] = []
    cur: dict | None = None
    for r in rows:
        if cur is None or cur["account_code"] != r["account_code"]:
            awal = opening.get(r["account_code"], 0.0)
            cur = {
                "account_code": r["account_code"],
                "account_name": r["account_name"],
                "account_type": r["account_type"],
                "saldo_awal": awal,
                "total_debit": 0.0,
                "total_credit": 0.0,
                "rows": [],
            }
            accounts.append(cur)
        desc = r["description"] or ""
        if r["additionaldescription"]:
            desc = f"{desc} ({r['additionaldescription']})"
        sub = " - ".join(p for p in [r["subaccountcode"], r["subaccountname"]] if p)
        cur["rows"].append(
            {
                "journal_date": r["journal_date"],
                "transactionno": r["transactionno"],
                "description": desc,
                "subaccount": sub,
                "debit": r["debit_ekuiv"],
                "credit": r["credit_ekuiv"],
                "lawan": " - ".join(p for p in [r["lawan_code"], r["lawan_name"]] if p),
            }
        )
        cur["total_debit"] += r["debit_ekuiv"]
        cur["total_credit"] += r["credit_ekuiv"]

    for a in accounts:
        net = (
            a["total_debit"] - a["total_credit"]
            if a["account_type"] in ("A", "X")
            else a["total_credit"] - a["total_debit"]
        )
        a["net"] = net
        a["saldo_akhir"] = a["saldo_awal"] + net

    return {
        "accounts": accounts,
        "begin": begin,
        "end": end,
        "konsolidasi": branch is None,
        "capped": capped,
    }


# ── Perubahan Dana (S_PerubahanDana) — laporan per dana (config PD_MUT/PD_BAL) ─
#
# Mutasi item PD_MUT + saldo awal PD_BAL (begin-1). Penerimaan zakat dipecah
# Badan/Perorangan via rc_code (DON02 / DON01+null) atas akun item 'zakatcoll'.


async def _zakat_collection_split(
    branch: str | None, begin: date, end: date
) -> tuple[float, float]:
    """(corporate=DON02, personal=DON01+null) atas akun item PD_MUT 'zakatcoll'."""
    args: list = [begin, end]
    branch_clause = ""
    if branch:
        args.append(branch)
        branch_clause = f"AND ac.branch_code = ${len(args)}"
    sql = f"""
        SELECT ji.rc_code AS rc, SUM((ji.amount_credit - ji.amount_debit) * ji.nilai_kurs)::float8 AS amount
        FROM transaction.journal j
        JOIN transaction.journalitem ji     ON j.journal_no = ji.fl_journal
        JOIN transaction.accountinstance ac ON ji.accountinstance_id = ac.accountinstance_id
        WHERE j.journal_date >= $1::date AND j.journal_date < ($2::date + INTERVAL '1 day')
          AND EXISTS (
            SELECT 1 FROM dwh.v_aruskas_item_account v
            WHERE v.group_code = 'PD_MUT' AND v.item_code = 'zakatcoll'
              AND v.account_code = ac.account_code
          )
          {branch_clause}
        GROUP BY ji.rc_code
    """
    rows = await fetch_all_dwh(sql, *args)
    by_rc = {(r["rc"] or ""): r["amount"] for r in rows}
    corporate = by_rc.get("DON02", 0.0) or 0.0
    personal = (by_rc.get("DON01", 0.0) or 0.0) + (by_rc.get("", 0.0) or 0.0)
    return corporate, personal


async def perubahan_dana(branch: str | None, begin: str, end: str) -> dict | None:
    b = date.fromisoformat(begin)
    e = date.fromisoformat(end)
    if b > e:
        raise ReportValidationError("Rentang tanggal filter salah (awal > akhir).")
    if not await ping_dwh():
        return None

    mut = await _balancesum_mutations(branch, b, e, "PD_MUT")
    bal = await _balancesum_balance(branch, date.fromordinal(b.toordinal() - 1), "PD_BAL")
    corporate, personal = await _zakat_collection_split(branch, b, e)

    def mb(item: str) -> float:
        return (mut.get(item) or {}).get("net", 0.0) or 0.0

    def bb(item: str) -> float:
        return bal.get(item, 0.0) or 0.0

    def _fund(name: str, penerimaan: list[dict], penyaluran: list[dict], saldo_awal: float) -> dict:
        tp = sum(x["value"] for x in penerimaan)
        td = sum(x["value"] for x in penyaluran)
        surplus = tp - td
        return {
            "fund": name,
            "penerimaan": penerimaan,
            "penyaluran": penyaluran,
            "total_penerimaan": tp,
            "total_penyaluran": td,
            "surplus": surplus,
            "saldo_awal": saldo_awal,
            "saldo_akhir": saldo_awal + surplus,
        }

    zakat = _fund(
        "Dana Zakat",
        [
            {"label": "Penerimaan dari Muzakki Badan/Perusahaan", "value": corporate},
            {"label": "Penerimaan dari Muzakki Perorangan", "value": personal},
            {"label": "Bagi Hasil/Penempatan Dana Zakat", "value": mb("bagihasilzakat")},
        ],
        [
            {"label": "Hak Amil dari Zakat", "value": mb("zakatdistamil")},
            {"label": "Fakir", "value": mb("zakatdistfakir")},
            {"label": "Riqab", "value": mb("zakatdistriqob")},
            {"label": "Gharimin", "value": mb("zakatdistghorimin")},
            {"label": "Mualaf", "value": mb("zakatdistmualaf")},
            {"label": "Fisabilillah", "value": mb("zakatdistfisabilillah")},
            {"label": "Ibnu Sabil", "value": mb("zakatdistibnusabil")},
        ],
        bb("zakatbeginbalance"),
    )
    infaq = _fund(
        "Dana Infaq/Shadaqah",
        [
            {"label": "Penerimaan Infaq Terikat", "value": mb("infaqterikatcoll")},
            {"label": "Hasil Kelolaan Infaq Terikat", "value": mb("infaqterikatkelolaan")},
            {"label": "Penerimaan Infaq Tidak Terikat", "value": mb("infaqtakterikatcoll")},
            {"label": "Bagi Hasil Infaq Tidak Terikat", "value": mb("bagihasiltterikat")},
            {"label": "Hasil Kelolaan Infaq Tidak Terikat", "value": mb("infaqtterikatkelolaan")},
        ],
        [
            {"label": "Penyaluran Infaq Terikat", "value": mb("infaqterikatdist")},
            {"label": "Hak Amil atas Infaq Terikat", "value": mb("amilbalanceterikat")},
            {"label": "Penyaluran Infaq Tidak Terikat", "value": mb("infaqtakterikatdist")},
            {"label": "Hak Amil atas Infaq Tidak Terikat", "value": mb("amilbalancetterikat")},
        ],
        bb("infaqterikatbeginbalance") + bb("infaqumumbeginbalance"),
    )
    nonhalal = _fund(
        "Dana Non Halal",
        [{"label": "Penerimaan Dana Non Halal", "value": mb("fasumcoll")}],
        [{"label": "Penyaluran Dana Non Halal", "value": mb("fasumdist")}],
        bb("fasumbeginbalance"),
    )
    amil = _fund(
        "Dana Amil",
        [
            {"label": "Bagian Amil dari Dana Zakat", "value": mb("amilporsizakat")},
            {"label": "Bagian Amil dari Infaq Terikat", "value": mb("amilporsiinfaqterikat")},
            {"label": "Bagian Amil dari Infaq Tidak Terikat", "value": mb("amilporsiinfaqtakterikat")},
            {"label": "Penerimaan Langsung Amil", "value": mb("amilpenerimaanlangsung")},
            {"label": "Bagi Hasil Bank Syariah", "value": mb("bhsyariahcoll")},
            {"label": "Bagi Hasil Deposito/Investasi/Kelolaan",
             "value": mb("bhdepositocoll") + mb("bhinvestcoll") + mb("danakelolaancoll")},
            {"label": "Pendapatan Lain-lain", "value": mb("pendlain2coll")},
        ],
        [
            {"label": "Beban Amil", "value": mb("amilcost")},
            {"label": "Beban Amil Lainnya", "value": mb("amilothercost")},
        ],
        bb("amilbeginbalance"),
    )

    funds = [zakat, infaq, nonhalal, amil]
    return {
        "funds": funds,
        "total_saldo_akhir": sum(f["saldo_akhir"] for f in funds),
        "begin": begin,
        "end": end,
        "konsolidasi": branch is None,
    }


# ── Perubahan Dana Detail (S_PerubahanDanaDetil) — rincian per akun ───────────


async def _balancesum_member_mutations(
    branch: str | None, begin: date, end: date, group_code: str
) -> dict:
    """item_code(lower) → {account_code: {name, net}} — mutasi per akun member."""
    args: list = [begin, end, group_code]
    branch_clause = ""
    if branch:
        args.append(branch)
        branch_clause = f"AND ai.branch_code = ${len(args)}"
    sql = f"""
        SELECT v.item_code, v.account_code, a.account_name AS account_name,
            SUM(CASE WHEN v.account_type IN ('A','X')
                     THEN (ji.amount_debit - ji.amount_credit) * ji.nilai_kurs
                     ELSE (ji.amount_credit - ji.amount_debit) * ji.nilai_kurs END)::float8 AS net
        FROM dwh.v_aruskas_item_account v
        JOIN transaction.account a          ON a.account_code = v.account_code
        JOIN transaction.accountinstance ai ON ai.account_code = v.account_code
        JOIN transaction.journalitem ji     ON ji.accountinstance_id = ai.accountinstance_id
        JOIN transaction.journal j           ON j.journal_no = ji.fl_journal
        WHERE v.group_code = $3
          AND j.journal_date >= $1::date
          AND j.journal_date < ($2::date + INTERVAL '1 day')
          {branch_clause}
        GROUP BY v.item_code, v.account_code, a.account_name
    """
    rows = await fetch_all_dwh(sql, *args)
    out: dict = {}
    for r in rows:
        out.setdefault(r["item_code"], {})[r["account_code"]] = {
            "account_name": r["account_name"],
            "net": r["net"],
        }
    return out


async def _zakat_collection_split_members(
    branch: str | None, begin: date, end: date
) -> tuple[dict, dict]:
    """(corporate, personal) per akun: {account_code: {name, net}}; DON02 vs DON01+null."""
    args: list = [begin, end]
    branch_clause = ""
    if branch:
        args.append(branch)
        branch_clause = f"AND ac.branch_code = ${len(args)}"
    sql = f"""
        SELECT a.account_code, a.account_name, ji.rc_code AS rc,
               SUM((ji.amount_credit - ji.amount_debit) * ji.nilai_kurs)::float8 AS net
        FROM transaction.journal j
        JOIN transaction.journalitem ji     ON j.journal_no = ji.fl_journal
        JOIN transaction.accountinstance ac ON ji.accountinstance_id = ac.accountinstance_id
        JOIN transaction.account a          ON a.account_code = ac.account_code
        WHERE j.journal_date >= $1::date AND j.journal_date < ($2::date + INTERVAL '1 day')
          AND EXISTS (
            SELECT 1 FROM dwh.v_aruskas_item_account v
            WHERE v.group_code = 'PD_MUT' AND v.item_code = 'zakatcoll'
              AND v.account_code = a.account_code
          )
          {branch_clause}
        GROUP BY a.account_code, a.account_name, ji.rc_code
    """
    rows = await fetch_all_dwh(sql, *args)
    corp: dict = {}
    pers: dict = {}
    for r in rows:
        target = corp if (r["rc"] or "") == "DON02" else pers
        ex = target.get(r["account_code"])
        if ex:
            ex["net"] += r["net"]
        else:
            target[r["account_code"]] = {"account_name": r["account_name"], "net": r["net"]}
    return corp, pers


def _detail_section(title: str, members: dict) -> dict:
    """{account_code:{name,net}} → {title, rows:[...], total}."""
    rows = [
        {"account_code": code, "account_name": m["account_name"], "value": m["net"]}
        for code, m in sorted(members.items())
    ]
    return {"title": title, "rows": rows, "total": sum(r["value"] for r in rows)}


async def perubahan_dana_detail(branch: str | None, begin: str, end: str) -> dict | None:
    b = date.fromisoformat(begin)
    e = date.fromisoformat(end)
    if b > e:
        raise ReportValidationError("Rentang tanggal filter salah (awal > akhir).")
    if not await ping_dwh():
        return None

    mm = await _balancesum_member_mutations(branch, b, e, "PD_MUT")
    corp, pers = await _zakat_collection_split_members(branch, b, e)

    def mem(item: str) -> dict:
        return mm.get(item, {})

    funds = [
        {
            "fund": "Dana Zakat",
            "sections": [
                _detail_section("Penerimaan Zakat dari Muzakki Badan/Perusahaan", corp),
                _detail_section("Penerimaan Zakat dari Muzakki Perorangan", pers),
                _detail_section("Bagi Hasil Penempatan Zakat", mem("bagihasilzakat")),
                _detail_section("Penyaluran Zakat - Amil", mem("zakatdistamil")),
                _detail_section("Penyaluran Zakat - Fakir", mem("zakatdistfakir")),
                _detail_section("Penyaluran Zakat - Riqab", mem("zakatdistriqob")),
                _detail_section("Penyaluran Zakat - Gharimin", mem("zakatdistghorimin")),
                _detail_section("Penyaluran Zakat - Mualaf", mem("zakatdistmualaf")),
                _detail_section("Penyaluran Zakat - Fisabilillah", mem("zakatdistfisabilillah")),
                _detail_section("Penyaluran Zakat - Ibnu Sabil", mem("zakatdistibnusabil")),
            ],
        },
        {
            "fund": "Dana Infaq/Shadaqah",
            "sections": [
                _detail_section("Penerimaan Infaq Terikat", mem("infaqterikatcoll")),
                _detail_section("Hasil Pengelolaan Infaq Terikat", mem("infaqterikatkelolaan")),
                _detail_section("Penerimaan Infaq Tidak Terikat", mem("infaqtakterikatcoll")),
                _detail_section("Bagi Hasil Penempatan Infaq", mem("bagihasiltterikat")),
                _detail_section("Hasil Pengelolaan Infaq Tidak Terikat", mem("infaqtterikatkelolaan")),
                _detail_section("Penyaluran Infaq Terikat", mem("infaqterikatdist")),
                _detail_section("Hak Amil atas Infaq Terikat", mem("amilbalanceterikat")),
                _detail_section("Penyaluran Infaq Tidak Terikat", mem("infaqtakterikatdist")),
                _detail_section("Hak Amil atas Infaq Tidak Terikat", mem("amilbalancetterikat")),
            ],
        },
        {
            "fund": "Dana Non Halal",
            "sections": [
                _detail_section("Penerimaan Non Halal", mem("fasumcoll")),
                _detail_section("Penyaluran Non Halal", mem("fasumdist")),
            ],
        },
        {
            "fund": "Dana Amil",
            "sections": [
                _detail_section("Bagian Amil atas Penerimaan Zakat", mem("zakatamil")),
                _detail_section("Bagian Amil atas Infaq Terikat", mem("amilporsiinfaqterikat")),
                _detail_section("Bagian Amil atas Infaq Tidak Terikat", mem("amilporsiinfaqtakterikat")),
                _detail_section("Penerimaan Amil Langsung", mem("amilpenerimaanlangsung")),
                _detail_section("Penerimaan Bagi Hasil Syariah", mem("bhsyariahcoll")),
                _detail_section(
                    "Penerimaan Hasil Kelolaan",
                    {**mem("bhdepositocoll"), **mem("bhinvestcoll"), **mem("danakelolaancoll")},
                ),
                _detail_section("Pendapatan Lain-lain", mem("pendlain2coll")),
                _detail_section("Beban Amil", mem("amilcost")),
                _detail_section("Beban Amil Lainnya", mem("amilothercost")),
            ],
        },
    ]
    return {
        "funds": funds,
        "begin": begin,
        "end": end,
        "konsolidasi": branch is None,
    }


# ── Penerimaan / Pengeluaran Amil (fCashInReport / fCashOutReport) ────────────

_AMIL_VIEW = {"in": "dwh.v_amil_cashin", "out": "dwh.v_amil_cashout"}


def _amil_where(branch: str | None, begin: str, end: str) -> tuple[str, list]:
    args: list = [date.fromisoformat(begin), date.fromisoformat(end)]
    clause = "actualdate >= $1::date AND actualdate <= $2::date"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    return clause, args


async def amil_cash(
    kind: str, branch: str | None, begin: str, end: str, page: int, page_size: int
) -> dict | None:
    if not await ping_dwh():
        return None
    view = _AMIL_VIEW[kind]
    clause, args = _amil_where(branch, begin, end)
    tot = await fetch_one_dwh(
        f"SELECT count(*) n, COALESCE(SUM(amount),0)::float8 s FROM {view} WHERE {clause}", *args
    )
    total = int(tot["n"]) if tot else 0
    extra = ", budgetcode, budgetitemdescription" if kind == "out" else ""
    args_page = args + [page_size, (page - 1) * page_size]
    rows = await fetch_all_dwh(
        f"SELECT to_char(actualdate,'YYYY-MM-DD') AS actualdate, account_code, account_name, "
        f"description, amount, referenceno, transactionno, inputer, channel{extra} "
        f"FROM {view} WHERE {clause} ORDER BY actualdate, transactionno "
        f"LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}",
        *args_page,
    )
    return {
        "rows": rows,
        "total": total,
        "total_amount": float(tot["s"]) if tot else 0.0,
        "page": page,
        "page_size": page_size,
    }


async def amil_cash_rows(kind: str, branch: str | None, begin: str, end: str) -> list[dict] | None:
    if not await ping_dwh():
        return None
    view = _AMIL_VIEW[kind]
    clause, args = _amil_where(branch, begin, end)
    extra = ", budgetcode, budgetitemdescription" if kind == "out" else ""
    return await fetch_all_dwh(
        f"SELECT to_char(actualdate,'YYYY-MM-DD') AS actualdate, account_code, account_name, "
        f"description, amount, referenceno, transactionno, inputer, channel{extra} "
        f"FROM {view} WHERE {clause} ORDER BY actualdate, transactionno LIMIT {CAP}",
        *args,
    )


async def amil_cash_count(kind: str, branch: str | None, begin: str, end: str) -> int:
    if not await ping_dwh():
        return 0
    clause, args = _amil_where(branch, begin, end)
    row = await fetch_one_dwh(f"SELECT count(*) n FROM {_AMIL_VIEW[kind]} WHERE {clause}", *args)
    return int(row["n"]) if row else 0

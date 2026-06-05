from __future__ import annotations
from app.shared.db import fetch_all, fetch_one

_SORT_MAP = {
    'actual_date':      't.actualdate',
    'transaction_date': 't.transactiondate',
    'transaction_no':   't.transactionno',
    'donor_no':         't.donorno',
    'donor_name':       't.donorname',
    'channel_name':     'f.accountname',
}

_SEARCH_COL = {
    'transno':     't.transactionno',
    'donorno':     't.donorno',
    'donorname':   't.donorname',
    'description': 't.description',
    'refno':       't.referenceno',
}

_TX_SELECT = """
    SELECT
      t.transactionid, t.transactionno,
      to_char(t.transactiondate, 'YYYY-MM-DD') AS transactiondate,
      to_char(t.actualdate,      'YYYY-MM-DD') AS actualdate,
      t.amount::float, t.donorno, t.donorname, t.referenceno,
      t.description, t.inputer, t.authstatus, t.isposted,
      t.branchcode, t.authoperationmode, t.channelaccountno,
      f.accountname AS channelname,
      e.exttransactionid, s.titlesubsystem
    FROM transaction.transaction t
    LEFT JOIN transaction.financialaccount    f ON f.accountno = t.channelaccountno
    LEFT JOIN transaction.externaltransaction e ON e.transactionid = t.transactionid
    LEFT JOIN transaction.accsubsystem        s ON s.subsystemcode = e.subsystemcode
"""


def build_search_where(
    begin: str,
    end: str,
    date_type: str,
    search_category: str,
    search_text: str | None,
    cash_account_no: str | None,
    branch: str | None,
    is_spv: bool,
    user_id: str,
) -> tuple[str, list]:
    """Return (WHERE clause string without 'WHERE', args list).
    Pure function — no DB access — fully unit-testable."""
    date_col = 't.actualdate' if date_type == 'actual' else 't.transactiondate'
    conds: list[str] = [
        f"{date_col}::date >= $1",
        f"{date_col}::date <= $2",
    ]
    args: list = [begin, end]

    if branch:
        args.append(branch)
        conds.append(f"t.branchcode = ${len(args)}")

    if not is_spv and user_id:
        args.append(user_id.upper())
        conds.append(f"UPPER(COALESCE(t.inputer,'')) = ${len(args)}")

    if search_category != 'none' and search_text and search_category in _SEARCH_COL:
        args.append(f'%{search_text.upper()}%')
        conds.append(f"UPPER(COALESCE({_SEARCH_COL[search_category]}, '')) LIKE ${len(args)}")

    if cash_account_no:
        args.append(cash_account_no)
        conds.append(f"t.channelaccountno = ${len(args)}")

    return ' AND '.join(conds), args


async def search_transactions(
    begin: str, end: str,
    date_type: str = 'actual',
    sort_by: str = 'actual_date',
    search_category: str = 'none',
    search_text: str | None = None,
    cash_account_no: str | None = None,
    limit: int = 50,
    branch: str | None = None,
    is_spv: bool = False,
    user_id: str = '',
) -> list[dict]:
    where, args = build_search_where(
        begin, end, date_type, search_category, search_text,
        cash_account_no, branch, is_spv, user_id,
    )
    order_col = _SORT_MAP.get(sort_by, 't.actualdate')
    limit = min(max(1, limit), 500)
    return await fetch_all(
        f"{_TX_SELECT} WHERE {where} ORDER BY {order_col} ASC LIMIT {limit}",
        *args,
    )


async def get_transaction(transaction_id: int) -> dict | None:
    return await fetch_one(
        """SELECT t.transactionid, t.transactionno, t.journalno,
              to_char(t.transactiondate,'YYYY-MM-DD') AS transactiondate,
              to_char(t.actualdate,'YYYY-MM-DD') AS actualdate,
              t.amount::float, t.donorno, t.donorname, t.referenceno,
              t.description, t.inputer, t.authstatus, t.isposted,
              t.branchcode, t.authoperationmode, t.channelaccountno,
              f.accountname AS channelname,
              e.exttransactionid, s.titlesubsystem
            FROM transaction.transaction t
            LEFT JOIN transaction.financialaccount    f ON f.accountno = t.channelaccountno
            LEFT JOIN transaction.externaltransaction e ON e.transactionid = t.transactionid
            LEFT JOIN transaction.accsubsystem        s ON s.subsystemcode = e.subsystemcode
            WHERE t.transactionid = $1""",
        transaction_id,
    )


async def get_journal_items(journal_no: str) -> list[dict]:
    return await fetch_all(
        """SELECT ji.journalitem_no, ji.fl_account,
                  a.account_name,
                  ji.branch_code, ji.valuta_code,
                  COALESCE(ji.amount_debit, 0)::float  AS amount_debit,
                  COALESCE(ji.amount_credit, 0)::float AS amount_credit,
                  ji.description, ji.subaccountcode, ji.subaccountname
           FROM transaction.journalitem ji
           LEFT JOIN transaction.account a ON a.account_code = ji.fl_account
           WHERE ji.fl_journal = $1
           ORDER BY ji.journalitem_no""",
        journal_no,
    )


async def get_transaction_items_for_ops(transaction_id: int) -> list[dict]:
    """Fetch transactionitem + accounttransactionitem — used by delete and repost."""
    return await fetch_all(
        """SELECT ti.transactionitemid, ti.mutationtype, ti.amount::float,
                  ati.accounttitype, ati.accountno, ati.fundentity, ati.donorid
           FROM transaction.transactionitem ti
           JOIN transaction.accounttransactionitem ati
             ON ati.transactionitemid = ti.transactionitemid
           WHERE ti.transactionid = $1""",
        transaction_id,
    )

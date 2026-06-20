from __future__ import annotations
from datetime import date as _date
from app.shared.db import fetch_all, fetch_one
from app.modules.transaction.fund_collection_schema import PenghimpunanListRow


def build_list_where(
    begin: str,
    end: str,
    search: str | None,
    branch: str | None,
) -> tuple[str, list]:
    args: list = ['SD001', _date.fromisoformat(begin), _date.fromisoformat(end)]
    conds = [
        "t.transactioncode = $1",
        "t.actualdate >= $2",
        "t.actualdate <= $3",
    ]
    if branch:
        args.append(branch)
        conds.append(f"t.branchcode = ${len(args)}")
    if search:
        args.append(f'%{search.upper()}%')
        conds.append(f"UPPER(COALESCE(t.transactionno,'')) LIKE ${len(args)}")
    return ' AND '.join(conds), args


_LIST_SELECT = """
    SELECT
      t.transactionid, t.transactionno,
      to_char(t.actualdate, 'YYYY-MM-DD') AS actual_date,
      t.description, CAST(t.amount AS float) AS amount,
      t.channelcode, t.channelaccountno,
      fa.accountname AS channel_name,
      t.inputer, t.authstatus, t.authaction, t.branchcode,
      t.donorname
    FROM transaction.transaction t
    LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
"""


async def count_list(begin: str, end: str, search: str | None, branch: str | None) -> int:
    where, args = build_list_where(begin, end, search, branch)
    row = await fetch_one(
        f"SELECT CAST(COUNT(*) AS integer) AS n FROM transaction.transaction t WHERE {where}",
        *args,
    )
    return int((row or {}).get('n', 0))


async def fetch_list(
    begin: str,
    end: str,
    search: str | None,
    branch: str | None,
    page: int,
    page_size: int,
) -> list[PenghimpunanListRow]:
    where, args = build_list_where(begin, end, search, branch)
    offset = (page - 1) * page_size
    args += [page_size, offset]
    rows = await fetch_all(
        f"{_LIST_SELECT} WHERE {where}"
        f" ORDER BY t.actualdate DESC, t.transactionid DESC"
        f" LIMIT ${len(args) - 1} OFFSET ${len(args)}",
        *args,
    )
    return [
        PenghimpunanListRow(
            transaction_id=int(r['transactionid']),
            transaction_no=r.get('transactionno'),
            actual_date=str(r.get('actual_date') or '')[:10],
            description=r.get('description'),
            amount=float(r.get('amount') or 0),
            channel_code=r.get('channelcode'),
            channel_account_no=r.get('channelaccountno'),
            channel_name=r.get('channel_name'),
            inputer=r.get('inputer'),
            auth_status=r.get('authstatus'),
            auth_action=r.get('authaction'),
            branch_code=r.get('branchcode'),
            donor_name=r.get('donorname'),
        )
        for r in rows
    ]


async def search_donors(q: str, branch: str | None = None, limit: int = 20) -> list[dict]:
    args: list = [f'%{q.upper()}%']
    where = "(UPPER(COALESCE(d.donorname,'')) LIKE $1 OR UPPER(COALESCE(d.donorno,'')) LIKE $1)"
    if branch:
        args.append(branch)
        where += f" AND d.branchcode = ${len(args)}"
    rows = await fetch_all(
        f"""SELECT d.donorid, d.donorno, d.donorname, d.phonenumber, d.donortype
            FROM transaction.donor d
            WHERE {where}
            ORDER BY d.donorname
            LIMIT {limit}""",
        *args,
    )
    return [
        {
            'donor_id': int(r['donorid']),
            'donor_no': r.get('donorno'),
            'donor_name': r.get('donorname'),
            'phone_number': r.get('phonenumber'),
            'donor_type': r.get('donortype'),
        }
        for r in rows
    ]

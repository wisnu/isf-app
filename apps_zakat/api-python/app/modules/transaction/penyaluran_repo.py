from __future__ import annotations
from datetime import date as _date
from app.shared.db import fetch_all, fetch_one, get_pool
from app.modules.transaction.penyaluran_schema import (
    FundProductAccountRow, ProductRow, RekeningRow,
    PenyaluranListRow, FUND_ENTITY_MAP,
)


def build_list_where(
    begin: str,
    end: str,
    search: str | None,
    branch: str | None,
) -> tuple[str, list]:
    """Pure function — unit-testable, no DB access."""
    args: list = ['DD001', _date.fromisoformat(begin), _date.fromisoformat(end)]
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
      t.description, t.amount::float,
      t.channelcode, t.channelaccountno,
      fa.accountname AS channel_name,
      t.inputer, t.authstatus, t.branchcode
    FROM transaction.transaction t
    LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
"""


async def count_list(begin: str, end: str, search: str | None, branch: str | None) -> int:
    where, args = build_list_where(begin, end, search, branch)
    row = await fetch_one(
        f"SELECT COUNT(*)::int AS n FROM transaction.transaction t WHERE {where}",
        *args,
    )
    return int((row or {}).get('n', 0))


async def fetch_list(
    begin: str, end: str,
    search: str | None,
    branch: str | None,
    page: int,
    page_size: int,
) -> list[PenyaluranListRow]:
    where, args = build_list_where(begin, end, search, branch)
    offset = (page - 1) * page_size
    args += [page_size, offset]
    rows = await fetch_all(
        f"{_LIST_SELECT} WHERE {where}"
        f" ORDER BY t.actualdate DESC, t.transactionid DESC"
        f" LIMIT ${len(args)-1} OFFSET ${len(args)}",
        *args,
    )
    return [
        PenyaluranListRow(
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
            branch_code=r.get('branchcode'),
        )
        for r in rows
    ]


async def fetch_rekening(account_type: str, branch: str | None) -> list[RekeningRow]:
    args: list = [account_type]
    where = "ca.cashaccounttype = $1"
    if branch:
        args.append(branch)
        where += f" AND fa.branchcode = ${len(args)}"
    rows = await fetch_all(
        f"""SELECT ca.accountno, fa.accountname, ca.accountinterface,
               fa.currencycode, fa.branchcode,
               ca.bankname, ca.bankaccountno, ca.cashcode,
               ca.productid, ca.fundcategory
            FROM transaction.cashaccount ca
            JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
            WHERE {where}
            ORDER BY fa.accountname""",
        *args,
    )
    return [
        RekeningRow(
            account_no=r['accountno'],
            account_name=r.get('accountname') or r['accountno'],
            account_interface=r.get('accountinterface'),
            currency_code=r.get('currencycode'),
            branch_code=r.get('branchcode'),
            bank_name=r.get('bankname'),
            bank_account_no=r.get('bankaccountno'),
            cash_code=r.get('cashcode'),
            product_id=r.get('productid'),
            fund_category=r.get('fundcategory'),
        )
        for r in rows
    ]


async def fetch_products(branch: str, currency: str = 'IDR') -> list[ProductRow]:
    rows = await fetch_all(
        """SELECT p.productid, p.productname, p.fundcategory, p.productcode,
                  pa.accountno
           FROM transaction.product p
           JOIN transaction.productaccount pa ON pa.productid = p.productid
           JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
           WHERE fa.branchcode = $1
             AND fa.currencycode = $2
             AND p.isdetail = 'T'
             AND p.status = 'A'
           ORDER BY p.fundcategory, p.productname""",
        branch, currency,
    )
    return [
        ProductRow(
            product_id=int(r['productid']),
            product_name=r['productname'],
            fund_category=r.get('fundcategory') or 'I',
            product_code=r.get('productcode'),
            account_no=r['accountno'],
            fund_entity=FUND_ENTITY_MAP.get(r.get('fundcategory') or 'I', 2),
        )
        for r in rows
    ]


async def fetch_fund_product_accounts(bank_account_no: str, branch: str) -> list[FundProductAccountRow]:
    rows = await fetch_all(
        """SELECT pa.accountno, fa.accountname, ca.productid, ca.fundcategory
           FROM transaction.cashaccount ca
           JOIN transaction.productaccount pa ON pa.productid = ca.productid
           JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
           WHERE ca.accountno = $1 AND fa.branchcode = $2""",
        bank_account_no, branch,
    )
    if not rows:
        rows = await fetch_all(
            """SELECT pa.accountno, fa.accountname, pa.productid, NULL AS fundcategory
               FROM transaction.productaccount pa
               JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
               WHERE fa.branchcode = $1 AND fa.currencycode = 'IDR'
               ORDER BY fa.accountname LIMIT 20""",
            branch,
        )
    return [
        FundProductAccountRow(
            account_no=r['accountno'],
            account_name=r.get('accountname') or r['accountno'],
            product_id=r.get('productid'),
            fund_category=r.get('fundcategory'),
        )
        for r in rows
    ]


async def get_cashaccount(account_no: str) -> dict | None:
    return await fetch_one(
        """SELECT ca.accountno, ca.accountinterface, ca.cashaccounttype,
                  ca.cashcode, fa.currencycode, fa.branchcode
           FROM transaction.cashaccount ca
           JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
           WHERE ca.accountno = $1""",
        account_no,
    )


async def get_branch_cash(branch: str, currency: str = 'IDR') -> dict | None:
    return await fetch_one(
        """SELECT ca.accountno, ca.accountinterface
           FROM transaction.cashaccount ca
           JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
           WHERE ca.cashaccounttype = 'R' AND fa.branchcode = $1
             AND fa.currencycode = $2
           LIMIT 1""",
        branch, currency,
    )

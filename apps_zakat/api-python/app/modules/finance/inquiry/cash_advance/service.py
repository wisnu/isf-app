from __future__ import annotations
from datetime import date
from app.shared.db import get_pool
from .schema import AccountOption, HistoryResult, HistoryRow


def _parse_date(s: str) -> date:
    return date.fromisoformat(s)


async def list_accounts(branch_code: str) -> list[AccountOption]:
    sql = """
        SELECT
            CAST(fa.accountno AS VARCHAR) AS account_no,
            fa.accountname                AS account_name,
            fa.branchcode                 AS branch_code
        FROM transaction.financialaccount fa
        JOIN transaction.accountreceivable ar ON ar.accountno = fa.accountno
        WHERE ar.accountreceivabletype = 'C'
          AND fa.status = 'A'
          AND (CAST($1 AS TEXT) = '' OR fa.branchcode = $1)
        ORDER BY fa.accountname, fa.accountno
    """
    async with get_pool().acquire() as db:
        rows = await db.fetch(sql, branch_code)
    return [AccountOption(
        account_no=str(r['account_no']),
        account_name=r['account_name'] or '',
        branch_code=r['branch_code'] or '',
    ) for r in rows]


async def get_history(account_no: str, begin: str, end: str) -> HistoryResult | None:
    begin_d = _parse_date(begin)
    end_d = _parse_date(end)

    sql_meta = """
        SELECT
            fa.accountname AS account_name,
            fa.branchcode  AS branch_code,
            COALESCE(
                (SELECT SUM(CASE ti2.mutationtype WHEN 'D' THEN ti2.ekuivalenamount ELSE -ti2.ekuivalenamount END)
                 FROM transaction.accounttransactionitem ati2
                 JOIN transaction.transactionitem ti2 ON ti2.transactionitemid = ati2.transactionitemid
                 JOIN transaction.transaction t2 ON t2.transactionid = ti2.transactionid
                 WHERE ati2.accountno = $1
                   AND t2.actualdate < $2)
            , 0.0) AS beginning_balance
        FROM transaction.financialaccount fa
        WHERE fa.accountno = $1
    """
    sql_rows = """
        SELECT
            ati.transactionitemid                                                          AS transaction_item_id,
            CAST(t.actualdate AS VARCHAR)                                                  AS actual_date,
            t.transactioncode                                                              AS transaction_code,
            ti.mutationtype                                                                AS mutation_type,
            ti.ekuivalenamount                                                             AS ekuiv_amount,
            t.referenceno                                                                  AS reference_no,
            t.description                                                                  AS description,
            t.inputer                                                                      AS inputer,
            t.transactionno                                                                AS transaction_no,
            CASE t.authstatus WHEN 'T' THEN 'Sudah Otorisasi' ELSE 'Belum Otorisasi' END AS auth_status
        FROM transaction.accounttransactionitem ati
        JOIN transaction.transactionitem ti ON ti.transactionitemid = ati.transactionitemid
        JOIN transaction.transaction t ON t.transactionid = ti.transactionid
        WHERE ati.accountno = $1
          AND t.actualdate >= $2
          AND t.actualdate <= $3
        ORDER BY t.actualdate ASC, ati.transactionitemid ASC
    """
    async with get_pool().acquire() as db:
        meta = await db.fetchrow(sql_meta, account_no, begin_d)
        if not meta:
            return None
        raw_rows = await db.fetch(sql_rows, account_no, begin_d, end_d)

    beginning_balance = float(meta['beginning_balance'] or 0.0)
    running = beginning_balance
    total_debet = 0.0
    total_kredit = 0.0
    result_rows: list[HistoryRow] = []

    for r in raw_rows:
        amount = float(r['ekuiv_amount'] or 0.0)
        mutation = r['mutation_type']
        if mutation == 'D':
            debet = amount
            kredit = 0.0
            running += amount
            total_debet += amount
        else:
            debet = 0.0
            kredit = amount
            running -= amount
            total_kredit += amount

        result_rows.append(HistoryRow(
            transaction_item_id=int(r['transaction_item_id']),
            actual_date=str(r['actual_date'] or '')[:10],
            transaction_code=r['transaction_code'],
            mutation_type=mutation,
            amount=amount,
            debet=debet,
            kredit=kredit,
            running_balance=running,
            reference_no=r['reference_no'],
            description=r['description'],
            transaction_no=r['transaction_no'],
            inputer=r['inputer'],
            auth_status=r['auth_status'],
        ))

    return HistoryResult(
        account_no=account_no,
        account_name=meta['account_name'] or '',
        branch_code=meta['branch_code'] or '',
        beginning_balance=beginning_balance,
        total_debet=total_debet,
        total_kredit=total_kredit,
        ending_balance=beginning_balance + total_debet - total_kredit,
        rows=result_rows,
    )

"""Business logic for Uang Muka Pengembalian / LPJ (Cash Advance Return, transactioncode='CAR')."""
from __future__ import annotations

from datetime import date, datetime, timezone

from asyncpg import Connection

from app.shared.db import get_pool


async def list_pengembalian(
    db: Connection,
    branch_code: str,
    page: int = 1,
    limit: int = 25,
    date_from: str = "",
    date_to: str = "",
    employee_id: int = 0,
) -> tuple[list[dict], int]:
    offset = (page - 1) * limit

    where_parts = [
        "t.transactioncode = 'CAR'",
        "ati.accounttitype = 'C'",
        "ati.cattype = 'C'",
        "ar.accountreceivabletype = 'C'",
    ]
    params: list = []
    idx = 1

    if branch_code:
        where_parts.append(f"t.branchcode = ${idx}")
        params.append(branch_code)
        idx += 1
    if date_from:
        where_parts.append(f"CAST(t.actualdate AS DATE) >= ${idx}")
        params.append(date.fromisoformat(date_from))
        idx += 1
    if date_to:
        where_parts.append(f"CAST(t.actualdate AS DATE) <= ${idx}")
        params.append(date.fromisoformat(date_to))
        idx += 1
    if employee_id > 0:
        where_parts.append(f"ar.employeeid = ${idx}")
        params.append(employee_id)
        idx += 1

    where = " AND ".join(where_parts)

    total = await db.fetchval(
        f"""SELECT COUNT(DISTINCT t.transactionid)
            FROM transaction.transaction t
            JOIN transaction.transactionitem ti ON ti.transactionid = t.transactionid
            JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
            JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
            JOIN transaction.accountreceivable ar ON ar.accountno = ati.accountno
            WHERE {where}""",
        *params,
    )

    params_page = params + [limit, offset]
    rows = await db.fetch(
        f"""SELECT DISTINCT
                t.transactionid,
                t.transactionno AS transaction_no,
                CAST(t.actualdate AS VARCHAR) AS actual_date,
                t.amount,
                t.authstatus AS auth_status,
                t.branchcode AS branch_code,
                t.inputer,
                t.description,
                t.referenceno AS reference_no,
                fa.accountname AS employee_name,
                ar.employeeid
            FROM transaction.transaction t
            JOIN transaction.transactionitem ti ON ti.transactionid = t.transactionid
            JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
            JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
            JOIN transaction.accountreceivable ar ON ar.accountno = ati.accountno
            WHERE {where}
            ORDER BY t.actualdate DESC, t.transactionid DESC
            LIMIT ${idx} OFFSET ${idx + 1}""",
        *params_page,
    )
    return [dict(r) for r in rows], int(total or 0)


async def lookup_open_cash_advance(
    employee_id: int,
    branch_code: str = "",
) -> list[dict]:
    """Return open (belum di-LPJ) CA transactions for this employee."""
    pool = get_pool()
    params: list = [employee_id]
    branch_filter = ""
    if branch_code:
        branch_filter = " AND t.branchcode = $2"
        params.append(branch_code)

    rows = await pool.fetch(
        f"""SELECT
                t.transactionid,
                t.transactionno AS transaction_no,
                CAST(t.actualdate AS VARCHAR) AS actual_date,
                t.description,
                ti.amount,
                ti.transactionitemid
            FROM transaction.transaction t
            JOIN transaction.transactionitem ti ON ti.transactionid = t.transactionid
            JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
            JOIN transaction.accountreceivable ar ON ar.accountno = ati.accountno
            WHERE t.transactioncode = 'CA'
              AND t.authstatus = 'T'
              AND ati.accounttitype = 'C'
              AND ati.cattype = 'D'
              AND ar.accountreceivabletype = 'C'
              AND ar.employeeid = $1
              AND ati.returntransactionitemid IS NULL
              {branch_filter}
            ORDER BY t.actualdate DESC
            LIMIT 50""",
        *params,
    )
    return [dict(r) for r in rows]


async def create_from_payload(
    payload: dict,
    user_id: str,
    branch_code: str,
) -> int:
    """Otorisasi dispatcher — creates CAR transaction after supervisor approves.

    Returns transactionid as result_entity_id.
    """
    pool = get_pool()

    actual_date = date.fromisoformat(payload['actual_date'])
    ref_item_id = int(payload['ref_transaction_item_id'])
    ref_amount = float(payload['ref_amount'])
    amount = float(payload['amount'])
    cash_account_no = payload['cash_account_no']  # = cashaccount.cashaccountno
    reference_no = payload.get('reference_no', '')
    description = payload.get('description', '')
    fund_entity = int(payload.get('fund_entity', 4))

    year = actual_date.year
    now = datetime.now(timezone.utc)
    now_naive = now.replace(tzinfo=None)

    async with pool.acquire() as conn:
        async with conn.transaction():
            # 1. Fetch original CA employee item — validates it exists and is still open
            ca_item = await conn.fetchrow(
                """SELECT ati.transactionitemid,
                          ati.accountno AS employee_accountno,
                          ati.returntransactionitemid,
                          ti.transactionid AS ca_transactionid,
                          t.transactionno AS ca_transactionno
                   FROM transaction.accounttransactionitem ati
                   JOIN transaction.transactionitem ti
                     ON ti.transactionitemid = ati.transactionitemid
                   JOIN transaction.transaction t
                     ON t.transactionid = ti.transactionid
                   WHERE ati.transactionitemid = $1
                     AND ati.accounttitype = 'C'
                     AND ati.cattype = 'D'""",
                ref_item_id,
            )
            if not ca_item:
                raise ValueError(f'CA item {ref_item_id} tidak ditemukan')
            if ca_item['returntransactionitemid'] is not None:
                raise ValueError('Uang muka ini sudah memiliki pengembalian (LPJ)')

            employee_accountno = ca_item['employee_accountno']
            ca_transaction_id = int(ca_item['ca_transactionid'])
            ca_transactionno = ca_item['ca_transactionno'] or ''

            # 2. Look up cash account (cashaccountno → financial accountno)
            cash_acct = await conn.fetchrow(
                """SELECT ca.accountno, ca.cashcode,
                          COALESCE(ca.accountinterface, ca.accountno) AS interface_accountno
                   FROM transaction.cashaccount ca
                   WHERE ca.cashaccountno = $1""",
                cash_account_no,
            )
            if not cash_acct:
                raise ValueError(f'Rekening kas {cash_account_no} tidak ditemukan')

            cash_financial_accountno = cash_acct['accountno']
            cash_code = cash_acct['cashcode'] or 'LAZ'
            cash_interface_accountno = cash_acct['interface_accountno']

            # 3. Generate transaction number (same KK- prefix as CA)
            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            transaction_no = f"KK-{year}-{branch_code}-{cash_code}-{int(seq):07d}"

            # 4. Generate journal number
            jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            journal_no = f"CAR.{year}.{actual_date.month:02d}.{int(jseq):07d}"

            desc = description or f"Pengembalian {ca_transactionno}"
            journal_code = '10'

            # 5. INSERT transaction
            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """INSERT INTO transaction.transaction
                   (transactionid, transactiondate, transactiontime, actualdate,
                    referenceno, description, inputer, transactioncode, channelcode,
                    branchcode, authstatus, isposted, journalno, amount, currencycode,
                    transactionno)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,'CAR','10',$8,'T',false,$9,$10,'IDR',$11)""",
                transaction_id, actual_date, now_naive.time(), actual_date,
                reference_no, desc, user_id.upper(),
                branch_code, journal_no, amount, transaction_no,
            )

            # 6. Journal infrastructure
            block_id = int(await conn.fetchval("SELECT nextval('transaction.seq_journalblock')"))
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, class_id, key_id, journal_no, subsystemcode, transaction_tag)
                   VALUES ($1,'Transaction',$2,$3,'CORE','CAR')""",
                block_id, transaction_id, journal_no,
            )
            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_type, journal_date, journal_date_posting,
                    transaction_date, description, userid_create, userid_posting,
                    is_posted, status, journal_state, branch_code,
                    source_app, source_app_class, source_app_ref, lastitemno)
                   VALUES ($1,'CAR',$2,$2,$2,$3,$4,$4,'T','C','C',$5,'CORE','Transaction',$6,2)""",
                journal_no, actual_date, desc,
                user_id.upper(), branch_code, str(transaction_id),
            )

            journalitem_no = 0

            # 7. CAR CREDIT item — employee AR account (receivable reduces)
            car_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """INSERT INTO transaction.transactionitem
                   (transactionitemid, transactionid, branchcode, currencycode,
                    mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                    description, refaccountno, accountcode, parameterjournalid)
                   VALUES ($1,$2,$3,'IDR','C',$4,1.0,$4,'A',$5,$6,$6,$7)""",
                car_item_id, transaction_id, branch_code,
                ref_amount, desc, employee_accountno, journal_code,
            )
            await conn.execute(
                """INSERT INTO transaction.accounttransactionitem
                   (transactionitemid, accounttitype, accountno, cattype, fundentity, isupdatebalance)
                   VALUES ($1,'C',$2,'C',$3,'T')""",
                car_item_id, employee_accountno, fund_entity,
            )
            await conn.execute(
                "UPDATE transaction.financialaccount SET balance = COALESCE(balance, 0) - $2 WHERE accountno = $1",
                employee_accountno, ref_amount,
            )
            journalitem_no += 1
            await conn.execute(
                """INSERT INTO transaction.journalitem
                   (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                    description, branch_code, valuta_code, journalitemtype,
                    userid_create, id_journalblock, source_class_id, source_key_id)
                   VALUES ($1,$2,$3,0,$4,$5,$6,'IDR','V',$7,$8,'AccountTransactionItem',$9)""",
                journal_no, journalitem_no, employee_accountno, ref_amount,
                desc, branch_code, user_id.upper(), block_id, car_item_id,
            )

            # 8. Cash DEBIT item — cash account (money coming back)
            cash_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """INSERT INTO transaction.transactionitem
                   (transactionitemid, transactionid, branchcode, currencycode,
                    mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                    description, refaccountno, accountcode, parameterjournalid)
                   VALUES ($1,$2,$3,'IDR','D',$4,1.0,$4,'A',$5,$6,$6,$7)""",
                cash_item_id, transaction_id, branch_code,
                amount, desc, cash_financial_accountno, journal_code,
            )
            await conn.execute(
                """INSERT INTO transaction.accounttransactionitem
                   (transactionitemid, accountno, isupdatebalance)
                   VALUES ($1,$2,'T')""",
                cash_item_id, cash_financial_accountno,
            )
            await conn.execute(
                "UPDATE transaction.financialaccount SET balance = COALESCE(balance, 0) + $2 WHERE accountno = $1",
                cash_financial_accountno, amount,
            )
            journalitem_no += 1
            await conn.execute(
                """INSERT INTO transaction.journalitem
                   (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                    description, branch_code, valuta_code, journalitemtype,
                    userid_create, id_journalblock, source_class_id, source_key_id)
                   VALUES ($1,$2,$3,$4,0,$5,$6,'IDR','V',$7,$8,'AccountTransactionItem',$9)""",
                journal_no, journalitem_no, cash_interface_accountno, amount,
                desc, branch_code, user_id.upper(), block_id, cash_item_id,
            )

            # 9. Mark original CA item as returned
            await conn.execute(
                "UPDATE transaction.accounttransactionitem SET returntransactionitemid = $2 WHERE transactionitemid = $1",
                ref_item_id, car_item_id,
            )

            # 10. Record return relationship
            await conn.execute(
                """INSERT INTO transaction.cashadvancereturninfo
                   (sourcetransactionid, returntransactionid, branchcode, returnamount, reimburseamount)
                   VALUES ($1,$2,$3,$4,0)""",
                ca_transaction_id, transaction_id, branch_code, amount,
            )

            # 11. History
            hist_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transhistoryofchanges')"))
            await conn.execute(
                """INSERT INTO transaction.transhistoryofchanges
                   (historyid, transactionid, transactionno, userid, processtime, changetype)
                   VALUES ($1,$2,$3,$4,$5,'I')""",
                hist_id, transaction_id, transaction_no, user_id.upper(), now_naive,
            )

    return transaction_id

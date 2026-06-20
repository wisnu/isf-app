"""Business logic for Uang Muka Penyerahan (Cash Advance)."""
from __future__ import annotations

from datetime import date, datetime, timezone
from asyncpg import Connection

from app.shared.db import get_pool
from .cash_advance_schema import UangMukaCreate, UangMukaUpdate


async def list_uang_muka(
    db: Connection,
    branch_code: str,
    page: int = 1,
    limit: int = 25,
    date_from: str = "",
    date_to: str = "",
    employee_id: int = 0,
    authstatus: str = "",
) -> tuple[list[dict], int]:
    """List Uang Muka transactions with optional filters."""
    offset = (page - 1) * limit

    # Build WHERE conditions
    where_parts = [
        "t.transactioncode = 'CA'",
        "ati.accounttitype = 'C'",
        "ati.cattype = 'D'",
        "ar.accountreceivabletype = 'C'",
    ]
    params = []
    param_idx = 1

    if branch_code:
        where_parts.append(f"t.branchcode = ${param_idx}")
        params.append(branch_code)
        param_idx += 1

    if date_from:
        where_parts.append(f"CAST(t.actualdate AS DATE) >= ${param_idx}")
        params.append(date.fromisoformat(date_from))
        param_idx += 1

    if date_to:
        where_parts.append(f"CAST(t.actualdate AS DATE) <= ${param_idx}")
        params.append(date.fromisoformat(date_to))
        param_idx += 1

    if employee_id > 0:
        where_parts.append(f"ar.employeeid = ${param_idx}")
        params.append(employee_id)
        param_idx += 1

    if authstatus:
        where_parts.append(f"t.authstatus = ${param_idx}")
        params.append(authstatus)
        param_idx += 1

    where_clause = " AND ".join(where_parts)

    # Count total
    total = await db.fetchval(
        f"""
        SELECT COUNT(DISTINCT t.transactionid)
        FROM transaction.transaction t
        JOIN transaction.transactionitem ti ON ti.transactionid = t.transactionid
        JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
        JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
        JOIN transaction.accountreceivable ar ON ar.accountno = ati.accountno
        WHERE {where_clause}
        """,
        *params
    )

    # Fetch rows
    limit_param_idx = param_idx
    offset_param_idx = param_idx + 1
    params.append(limit)
    params.append(offset)

    rows = await db.fetch(
        f"""
        SELECT DISTINCT
            t.transactionid,
            t.transactionno,
            CAST(t.actualdate AS VARCHAR) as actualdate,
            t.amount,
            t.authstatus,
            t.branchcode,
            t.inputer,
            t.description,
            fa.accountname as employee_name,
            ar.employeeid
        FROM transaction.transaction t
        JOIN transaction.transactionitem ti ON ti.transactionid = t.transactionid
        JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
        JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
        JOIN transaction.accountreceivable ar ON ar.accountno = ati.accountno
        WHERE {where_clause}
        ORDER BY t.actualdate DESC, t.transactionid DESC
        LIMIT ${limit_param_idx} OFFSET ${offset_param_idx}
        """,
        *params
    )

    return [dict(r) for r in rows], total


async def get_uang_muka_detail(
    db: Connection,
    transaction_id: int,
) -> dict | None:
    """Get full detail of Uang Muka transaction including has_return_trans flag."""
    row = await db.fetchrow(
        """
        SELECT
            t.transactionid,
            t.transactionno,
            CAST(t.actualdate AS VARCHAR) as actualdate,
            t.amount,
            t.authstatus,
            t.branchcode,
            t.inputer,
            t.description,
            ar.employeeid,
            fa.accountname as employee_name,
            ca.cashaccountno as cash_account_no,
            t.referenceno as reference_no,
            EXISTS(
                SELECT 1 FROM transaction.transactionitem ti2
                JOIN transaction.accounttransactionitem ati2 ON ati2.transactionitemid = ti2.transactionitemid
                WHERE ti2.transactionid = t.transactionid
                  AND ati2.accounttitype = 'C'
                  AND ati2.cattype = 'C'
            ) as has_return_trans
        FROM transaction.transaction t
        JOIN transaction.transactionitem ti ON ti.transactionid = t.transactionid
        JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
        JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
        JOIN transaction.accountreceivable ar ON ar.accountno = ati.accountno
        JOIN transaction.cashaccount ca ON ca.accountno = ti.accountno
        WHERE t.transactionid = $1
          AND t.transactioncode = 'CA'
          AND ati.accounttitype = 'C'
          AND ati.cattype = 'D'
          AND ar.accountreceivabletype = 'C'
        LIMIT 1
        """,
        transaction_id
    )

    return dict(row) if row else None


async def create_from_payload(
    payload: dict,
    user_id: str,
    branch_code: str,
) -> int:
    """Create Uang Muka transaction from otorisasi payload.

    This is called by otorisasi dispatcher when submission is AUTHORIZED.
    Returns transactionid for result_entity_id.
    """
    pool = get_pool()

    # Extract payload
    actual_date = date.fromisoformat(payload['actual_date'])
    employee_id = payload['employee_id']
    employee_name = payload['employee_name']
    cash_account_no = payload['cash_account_no']
    amount = float(payload['amount'])
    reference_no = payload.get('reference_no', '')
    description = payload.get('description', '')
    budget_id = payload.get('budget_id', 0)
    real_memo_id = payload.get('real_memo_id', 0)

    now = datetime.now(timezone.utc)
    now_naive = now.replace(tzinfo=None)
    year = actual_date.year

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Step 1: Check/create EmployeeCashAdvance account (accountreceivabletype='C')
            employee_ca_account = await conn.fetchval(
                """
                SELECT accountno FROM transaction.accountreceivable
                WHERE employeeid = $1
                  AND accountreceivabletype = 'C'
                LIMIT 1
                """,
                employee_id
            )

            if not employee_ca_account:
                # Generate new account number for EmployeeCashAdvance
                # Pattern: assume CA prefix like others
                next_seq = await conn.fetchval(
                    "SELECT nextval('transaction.seq_accountno')"
                )
                employee_ca_account = f"CA-{employee_id}-{int(next_seq):05d}"

                # Create account in financialaccount
                await conn.execute(
                    """
                    INSERT INTO transaction.financialaccount
                    (accountno, accountname, description, accounttype, isactive, createddate, createdby)
                    VALUES ($1, $2, $3, 'CA', true, $4, $5)
                    """,
                    employee_ca_account,
                    f"Cash Advance - {employee_name}",
                    f"Employee cash advance for {employee_name}",
                    now_naive,
                    user_id.upper(),
                )

                # Create account in accountreceivable
                await conn.execute(
                    """
                    INSERT INTO transaction.accountreceivable
                    (accountno, employeeid, accountreceivabletype, isactive, createddate, createdby)
                    VALUES ($1, $2, 'C', true, $3, $4)
                    """,
                    employee_ca_account,
                    employee_id,
                    now_naive,
                    user_id.upper(),
                )

            # Step 2: Generate transaction number
            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            # Get cash code from cash account
            cash_code = await conn.fetchval(
                "SELECT cashcode FROM transaction.cashaccount WHERE cashaccountno = $1",
                cash_account_no
            )
            if not cash_code:
                cash_code = 'KAS'

            transaction_no = f"KK-{year}-{branch_code}-{cash_code}-{int(seq):07d}"

            # Step 3: Generate journal number
            jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            journal_no = f"KK001.{year}.{actual_date.month:02d}.{int(jseq):07d}"

            # Step 4: Insert transaction
            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """
                INSERT INTO transaction.transaction
                (transactionid, transactiondate, transactiontime, actualdate,
                 referenceno, description, inputer, transactioncode, channelcode,
                 branchcode, authstatus, isposted, journalno, amount, currencycode)
                VALUES ($1, $2, $3, $4, $5, $6, $7, 'CA', '10', $8, 'T', false, $9, $10, 'IDR')
                """,
                transaction_id,
                now_naive.date(),
                now_naive.time(),
                actual_date,
                reference_no,
                description,
                user_id.upper(),
                branch_code,
                journal_no,
                amount,
            )

            # Step 5: Create transactionitem & accounttransactionitem
            # Row 1: Employee CA account (DEBIT, accounttitype='C', cattype='D')
            item_id_1 = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """
                INSERT INTO transaction.transactionitem
                (transactionitemid, transactionid, sequenceno, accountno, debitamount, creditamount)
                VALUES ($1, $2, 1, $3, $4, 0)
                """,
                item_id_1,
                transaction_id,
                employee_ca_account,
                amount,
            )

            await conn.execute(
                """
                INSERT INTO transaction.accounttransactionitem
                (transactionitemid, accountno, accounttitype, cattype, amount, basecurrencyamount, exchangerate)
                VALUES ($1, $2, 'C', 'D', $3, $3, 1.0)
                """,
                item_id_1,
                employee_ca_account,
                amount,
            )

            # Row 2: Cash account (CREDIT, accounttitype='A', cattype default)
            item_id_2 = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            ca_account = await conn.fetchval(
                "SELECT accountno FROM transaction.cashaccount WHERE cashaccountno = $1",
                cash_account_no
            )
            await conn.execute(
                """
                INSERT INTO transaction.transactionitem
                (transactionitemid, transactionid, sequenceno, accountno, debitamount, creditamount)
                VALUES ($1, $2, 2, $3, 0, $4)
                """,
                item_id_2,
                transaction_id,
                ca_account,
                amount,
            )

            await conn.execute(
                """
                INSERT INTO transaction.accounttransactionitem
                (transactionitemid, accountno, accounttitype, cattype, amount, basecurrencyamount, exchangerate)
                VALUES ($1, $2, 'A', '', $3, $3, 1.0)
                """,
                item_id_2,
                ca_account,
                amount,
            )

            # Step 6: Link to budget if provided
            if budget_id > 0:
                await conn.execute(
                    """
                    INSERT INTO transaction.transactionbudget
                    (transactionid, budgetid)
                    VALUES ($1, $2)
                    ON CONFLICT DO NOTHING
                    """,
                    transaction_id,
                    budget_id,
                )

            # Step 7: Link to cash advance memo if provided
            if real_memo_id > 0:
                await conn.execute(
                    """
                    INSERT INTO transaction.cashadvancememoinfo
                    (transactionid, memoid)
                    VALUES ($1, $2)
                    ON CONFLICT DO NOTHING
                    """,
                    transaction_id,
                    real_memo_id,
                )

    return transaction_id


# Lookup functions
async def lookup_employee(
    search: str = "",
    branch_code: str = "",
) -> list[dict]:
    """Lookup employee by name/number."""
    pool = get_pool()

    where_parts = ["e.isactive = true"]
    params = []
    param_idx = 1

    if search:
        where_parts.append(f"LOWER(e.employeename) LIKE LOWER('%' || ${param_idx} || '%')")
        params.append(search)
        param_idx += 1

    if branch_code:
        where_parts.append(f"e.branchcode = ${param_idx}")
        params.append(branch_code)
        param_idx += 1

    where_clause = " AND ".join(where_parts)

    rows = await pool.fetch(
        f"""
        SELECT e.employeeid, e.employeename, e.employeenumber
        FROM enterprise.employee e
        WHERE {where_clause}
        ORDER BY e.employeename
        LIMIT 50
        """,
        *params
    )

    return [dict(r) for r in rows]


async def lookup_cash_account(
    branch_code: str = "",
) -> list[dict]:
    """Lookup cash account."""
    pool = get_pool()

    where_parts = ["ca.isactive = true"]
    params = []
    param_idx = 1

    if branch_code:
        where_parts.append(f"ca.branchcode = ${param_idx}")
        params.append(branch_code)
        param_idx += 1

    where_clause = " AND ".join(where_parts)

    rows = await pool.fetch(
        f"""
        SELECT ca.cashaccountno, ca.cashaccountname, ca.accountno
        FROM transaction.cashaccount ca
        WHERE {where_clause}
        ORDER BY ca.cashaccountname
        LIMIT 100
        """,
        *params
    )

    return [dict(r) for r in rows]


async def lookup_budget(
    search: str = "",
) -> list[dict]:
    """Lookup budget."""
    pool = get_pool()

    where_parts = ["b.isactive = true"]
    params = []
    param_idx = 1

    if search:
        where_parts.append(f"LOWER(b.budgetcode) LIKE LOWER('%' || ${param_idx} || '%')")
        params.append(search)
        param_idx += 1

    where_clause = " AND ".join(where_parts)

    rows = await pool.fetch(
        f"""
        SELECT b.budgetid, b.budgetcode, b.description, bo.ownername
        FROM transaction.budget b
        LEFT JOIN transaction.budgetowner bo ON bo.budgetownerid = b.budgetownerid
        WHERE {where_clause}
        ORDER BY b.budgetcode
        LIMIT 50
        """,
        *params
    )

    return [dict(r) for r in rows]

"""Business logic for Piutang (Pinjam/Bayar)."""
from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal
from asyncpg import Connection

from app.shared.db import get_pool


async def list_receivable(
    db: Connection,
    branch_code: str,
    page: int = 1,
    limit: int = 25,
    transaction_type: str = "",
    debtor_type: str = "",
    date_from: str = "",
    date_to: str = "",
) -> tuple[list[dict], int]:
    """List Piutang transactions (EAR=Pinjam, PEAR=Bayar) with optional filters."""
    offset = (page - 1) * limit

    # Build WHERE conditions — hardcoded discriminators
    where_parts = [
        "t.transactioncode IN ('EAR', 'PEAR')",
    ]
    params = []
    param_idx = 1

    if branch_code:
        where_parts.append(f"t.branchcode = ${param_idx}")
        params.append(branch_code)
        param_idx += 1

    if transaction_type in ('P', 'B'):
        # P=EAR, B=PEAR
        tx_code = 'EAR' if transaction_type == 'P' else 'PEAR'
        where_parts.append(f"t.transactioncode = ${param_idx}")
        params.append(tx_code)
        param_idx += 1

    if date_from:
        where_parts.append(f"CAST(t.actualdate AS DATE) >= ${param_idx}")
        params.append(date.fromisoformat(date_from))
        param_idx += 1

    if date_to:
        where_parts.append(f"CAST(t.actualdate AS DATE) <= ${param_idx}")
        params.append(date.fromisoformat(date_to))
        param_idx += 1

    where_clause = " AND ".join(where_parts)

    # Count total
    total = await db.fetchval(
        f"""
        SELECT COUNT(DISTINCT t.transactionid)
        FROM transaction.transaction t
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
            t.transactionid as id,
            t.transactionno as transaction_no,
            t.transactioncode as transaction_code,
            CASE WHEN t.transactioncode = 'EAR' THEN 'P' ELSE 'B' END as transaction_type,
            CAST(t.actualdate AS VARCHAR) as actual_date,
            t.branchcode as branch_code,
            t.inputer,
            COALESCE(t.donorname, 'Unknown') as debtor_name,
            '' as debtor_type,
            t.paidto as account_name,
            t.amount,
            t.currencycode as currency_code,
            'AUTHORIZED' as status,
            t.referenceno as reference_no,
            t.description
        FROM transaction.transaction t
        WHERE {where_clause}
        ORDER BY actual_date DESC, id DESC
        LIMIT ${limit_param_idx} OFFSET ${offset_param_idx}
        """,
        *params
    )

    return [dict(r) for r in rows], total


async def get_receivable_detail(
    db: Connection,
    transaction_id: int,
) -> dict | None:
    """Get full detail of Receivable transaction."""
    row = await db.fetchrow(
        """
        SELECT
            t.transactionid as id,
            t.transactionno as transaction_no,
            t.transactioncode as transaction_code,
            CASE WHEN t.transactioncode = 'EAR' THEN 'P' ELSE 'B' END as transaction_type,
            CAST(t.actualdate AS VARCHAR) as actual_date,
            t.amount,
            t.authstatus as auth_status,
            t.branchcode as branch_code,
            t.inputer,
            t.description,
            t.paidto as account_name,
            t.referenceno as reference_no,
            t.currencycode as currency_code,
            t.donorname as debtor_name
        FROM transaction.transaction t
        WHERE t.transactionid = $1
          AND t.transactioncode IN ('EAR', 'PEAR')
        LIMIT 1
        """,
        transaction_id
    )

    return dict(row) if row else None


async def lookup_debtors(
    db: Connection,
    branch_code: str = "",
    search: str = "",
    limit: int = 50,
) -> list[dict]:
    """Lookup debtors from DEBTOR_ALL view (union of Employee + ExternalDebtor)."""
    where_parts = []
    params = []
    param_idx = 1

    if branch_code:
        where_parts.append(f"d.branchcode = ${param_idx}")
        params.append(branch_code)
        param_idx += 1

    if search:
        where_parts.append(f"(LOWER(d.debtorname) LIKE LOWER('%' || ${param_idx} || '%') OR LOWER(d.debtorcode) LIKE LOWER('%' || ${param_idx} || '%'))")
        params.append(search)
        param_idx += 1

    where_clause = " WHERE " + " AND ".join(where_parts) if where_parts else ""

    rows = await db.fetch(
        f"""
        SELECT
            debtorid as debtor_id,
            debtorcode as debtor_code,
            debtorname as debtor_name,
            debtortype as debtor_type,
            branchcode as branch_code
        FROM transaction.debtor_all
        {where_clause}
        ORDER BY debtorname
        LIMIT {limit}
        """,
        *params
    )

    return [dict(r) for r in rows]


async def list_external_debtors(
    db: Connection,
    branch_code: str = "",
    limit: int = 100,
) -> list[dict]:
    """List all external debtors."""
    where_parts = ["ed.isactive = true"]
    params = []
    param_idx = 1

    if branch_code:
        where_parts.append(f"ed.branchcode = ${param_idx}")
        params.append(branch_code)
        param_idx += 1

    where_clause = " AND ".join(where_parts)

    rows = await db.fetch(
        f"""
        SELECT
            ed.debtorid as debtor_id,
            ed.debtorcode as debtor_code,
            ed.debtorname as debtor_name,
            ed.debtorphone as debtor_phone,
            ed.debtoraddress as debtor_address,
            ed.description
        FROM transaction.externaldebtor ed
        WHERE {where_clause}
        ORDER BY ed.debtorname
        LIMIT {limit}
        """,
        *params
    )

    return [dict(r) for r in rows]


async def create_from_payload(
    payload: dict,
    user_id: str,
    branch_code: str,
) -> int:
    """Create Piutang transaction from otorisasi payload.

    This is called by otorisasi dispatcher when submission is AUTHORIZED.
    Returns transaction_id for result_entity_id.

    Logic:
    1. EAR (Pinjam): auto-create AccountReceivable if not exists
    2. PEAR (Bayar): lookup only (error if not found)
    3. Generate transactionno
    4. Insert transaction with proper fields
    """
    pool = get_pool()

    actual_date = date.fromisoformat(payload['actual_date'])
    transaction_type = payload['transaction_type']  # 'P' or 'B'
    channel_type = payload['channel_type']  # 'C' or 'G'
    cash_account_no = payload.get('cash_account_no', '')
    gl_account_code = payload.get('gl_account_code', '')
    debtor_id = payload['debtor_id']
    debtor_type = payload['debtor_type']  # 'E' or 'X'
    amount = Decimal(str(payload['amount']))
    reference_no = payload.get('reference_no', '')
    description = payload.get('description', '')
    casher = payload.get('casher', user_id)

    # Determine transaction code & AR type
    tx_code = 'EAR' if transaction_type == 'P' else 'PEAR'
    ar_type = 'E' if debtor_type == 'E' else 'D'

    now = datetime.now(timezone.utc)
    now_naive = now.replace(tzinfo=None)
    year = actual_date.year

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Step 1: Lookup/verify debtor and get debtor name
            debtor_row = await conn.fetchrow(
                """
                SELECT debtorname FROM transaction.debtor_all
                WHERE debtorid = $1 AND debtortype = $2
                LIMIT 1
                """,
                debtor_id, debtor_type
            )
            if not debtor_row:
                raise ValueError(f"Debtor '{debtor_id}' (type {debtor_type}) tidak ditemukan")
            debtor_name = debtor_row['debtorname']

            # Step 2: Lookup/create AccountReceivable for piutang
            # Search for existing AR account
            ar_account = await conn.fetchval(
                """
                SELECT accountno FROM transaction.accountreceivable
                WHERE accountreceivabletype = $1
                  AND (
                    (accountreceivabletype = 'E' AND employeeid = $2)
                    OR (accountreceivabletype = 'D' AND debtorid = $3)
                  )
                LIMIT 1
                """,
                ar_type,
                debtor_id if ar_type == 'E' else None,
                debtor_id if ar_type == 'D' else None,
            )

            # Auto-create if EAR (Pinjam) and not exists
            if not ar_account and tx_code == 'EAR':
                next_seq = await conn.fetchval(
                    "SELECT nextval('transaction.seq_accountno')"
                )
                ar_account = f"AR-{ar_type}-{debtor_id}-{int(next_seq):05d}"

                # Insert into accountreceivable directly
                await conn.execute(
                    """
                    INSERT INTO transaction.accountreceivable
                    (accountno, accountreceivabletype, employeeid, debtorid, isactive, createddate, createdby)
                    VALUES ($1, $2, $3, $4, true, $5, $6)
                    """,
                    ar_account,
                    ar_type,
                    debtor_id if ar_type == 'E' else None,
                    debtor_id if ar_type == 'D' else None,
                    now_naive,
                    user_id.upper(),
                )
            elif not ar_account and tx_code == 'PEAR':
                raise ValueError(f"Rekening piutang belum dibuat. Buat transaksi Pinjam (EAR) terlebih dahulu.")

            # Step 3: Generate transaction number
            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            transaction_no = f"{tx_code}-{branch_code}-{year}-{actual_date.month:02d}-{actual_date.day:02d}"

            # Step 4: Insert transaction
            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """
                INSERT INTO transaction.transaction
                (transactionid, transactionno, transactioncode, transactiondate, transactiontime,
                 actualdate, branchcode, inputer, receivedfrom, amount, currencycode,
                 referenceno, description, paidto, authstatus, isposted, donorname)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, 'IDR',
                        $11, $12, $13, 'T', false, $14)
                """,
                transaction_id,
                transaction_no,
                tx_code,
                now_naive.date(),
                now_naive.time(),
                actual_date,
                branch_code,
                user_id.upper(),
                casher,
                float(amount),
                reference_no,
                description,
                ar_account,
                debtor_name,
            )

    return transaction_id

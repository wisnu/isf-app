"""Business logic for Penerimaan Amil (transactioncode='CI').

Model verified against 308 real CI rows in mziss_laz + legacy scripts/Transaction/CashIn.py.
Mirrors the proven journal/balance pattern of general_service.py.

A Penerimaan Amil transaction posts up to 3 kinds of legs:
  1. GL income credit   — amil revenue account (430xxx), mutationtype 'C', parameterjournalid '10'
  2. source credit       — optional per-item source cash account (Bank mode), 'C', pjid 'C20', + fundaccountno
  3. destination debit    — the chosen amil cash/bank account, 'D', total, pjid '10'
Each account leg also writes accounttransactionitem + updates financialaccount.balance,
and every leg writes a journalitem under one journalblock/journal (mirrors transaksi_umum).
"""
from __future__ import annotations

from datetime import date, datetime, timezone

from app.shared.db import get_pool

# amil revenue accounts live under 430000 PENERIMAAN DANA AMIL (account_type='I')
_GL_AMIL_PREFIX = '43'


async def list_amil_income(
    branch_code: str = '',
    page: int = 1,
    limit: int = 25,
    date_from: str = '',
    date_to: str = '',
) -> tuple[list[dict], int]:
    """List CI transactions with optional filters."""
    pool = get_pool()
    offset = (page - 1) * limit

    where_parts = ["t.transactioncode = 'CI'"]
    params: list = []
    idx = 1

    if branch_code:
        where_parts.append(f't.branchcode = ${idx}')
        params.append(branch_code)
        idx += 1
    if date_from:
        where_parts.append(f'CAST(t.actualdate AS DATE) >= ${idx}')
        params.append(date.fromisoformat(date_from))
        idx += 1
    if date_to:
        where_parts.append(f'CAST(t.actualdate AS DATE) <= ${idx}')
        params.append(date.fromisoformat(date_to))
        idx += 1

    where = ' AND '.join(where_parts)

    async with pool.acquire() as conn:
        total = await conn.fetchval(
            f'SELECT COUNT(DISTINCT t.transactionid) FROM transaction.transaction t WHERE {where}',
            *params,
        )
        rows = await conn.fetch(
            f"""
            SELECT
                t.transactionid                 AS id,
                t.transactionno,
                CAST(t.actualdate AS VARCHAR) AS actual_date,
                COALESCE(t.channelaccountno, '') AS bank_account_no,
                COALESCE(fa.accountname, '')    AS bank_account_name,
                CAST(t.amount AS NUMERIC(18,2)) AS total_amount,
                COALESCE(t.referenceno, '')     AS reference_no,
                COALESCE(t.description, '')      AS description,
                COALESCE(t.inputer, '')          AS inputer,
                t.branchcode                     AS branch_code,
                t.authstatus                     AS auth_status,
                COALESCE(t.authuser, '')         AS auth_user,
                CASE WHEN t.authdate IS NULL THEN '' ELSE CAST(t.authdate AS VARCHAR) END AS auth_date,
                COALESCE(t.channelcode, '')      AS channel_code,
                CASE WHEN t.authstatus = 'T' THEN 'AUTHORIZED' ELSE 'PENDING' END AS status
            FROM transaction.transaction t
            LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
            WHERE {where}
            ORDER BY t.actualdate DESC, t.transactionid DESC
            LIMIT ${idx} OFFSET ${idx + 1}
            """,
            *params, limit, offset,
        )

    return [dict(r) for r in rows], int(total or 0)


async def get_amil_income(transaction_id: int) -> dict | None:
    """Get CI transaction detail with GL line items."""
    pool = get_pool()
    async with pool.acquire() as conn:
        header = await conn.fetchrow(
            """
            SELECT
                t.transactionid,
                t.transactionno,
                CAST(t.actualdate AS VARCHAR) AS actual_date,
                COALESCE(t.channelaccountno, '') AS bank_account_no,
                COALESCE(fa.accountname, '')    AS bank_account_name,
                COALESCE(t.referenceno, '')     AS reference_no,
                COALESCE(t.description, '')      AS description,
                CAST(COALESCE(t.rate, 1.0) AS NUMERIC(15,4)) AS rate,
                CAST(t.amount AS NUMERIC(18,2)) AS total_amount,
                COALESCE(t.inputer, '')          AS inputer,
                t.branchcode                     AS branch_code,
                COALESCE(t.paidto, '')           AS paid_to,
                COALESCE(t.receivedfrom, '')     AS received_from,
                t.authstatus                     AS auth_status,
                COALESCE(t.authuser, '')         AS auth_user,
                CASE WHEN t.authdate IS NULL THEN '' ELSE CAST(t.authdate AS VARCHAR) END AS auth_date,
                COALESCE(t.channelcode, '')      AS channel_code,
                CASE WHEN t.authstatus = 'T' THEN 'AUTHORIZED' ELSE 'PENDING' END AS status
            FROM transaction.transaction t
            LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
            WHERE t.transactionid = $1 AND t.transactioncode = 'CI'
            """,
            transaction_id,
        )
        if not header:
            return None

        # GL income items only (type 'G'); the kas/bank legs are internal postings
        items = await conn.fetch(
            """
            SELECT
                ti.transactionitemid                 AS transaction_item_id,
                ti.refaccountno                       AS account_code,
                COALESCE(ti.refaccountname, '')       AS account_name,
                CAST(ti.amount AS NUMERIC(18,2))      AS amount,
                COALESCE(ti.currencycode, 'IDR')      AS currency_code,
                CAST(COALESCE(ti.rate, 1.0) AS NUMERIC(15,4)) AS rate,
                CAST(COALESCE(ti.ekuivalenamount, ti.amount) AS NUMERIC(18,2)) AS ekuivalen_amount,
                ti.mutationtype                       AS mutation_type,
                COALESCE(ti.description, '')          AS description
            FROM transaction.transactionitem ti
            WHERE ti.transactionid = $1 AND ti.transactionitemtype = 'G'
            ORDER BY ti.transactionitemid
            """,
            transaction_id,
        )

    return {**dict(header), 'items': [dict(i) for i in items]}


async def _resolve_account(conn, accountno: str) -> dict:
    """Resolve a cash/bank account's GL code, name, currency and cashcode."""
    # GL code of a cash/bank account is held in cashaccount.accountinterface
    row = await conn.fetchrow(
        """
        SELECT
            COALESCE(NULLIF(ca.accountinterface, ''), fa.accountcode, '') AS gl_code,
            COALESCE(fa.accountname, '')   AS account_name,
            COALESCE(fa.currencycode, ca.accountcurrency, 'IDR') AS currency_code,
            COALESCE(NULLIF(ca.cashcode, ''), '') AS cash_code
        FROM transaction.cashaccount ca
        LEFT JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
        WHERE ca.accountno = $1
        """,
        accountno,
    )
    return dict(row) if row else {
        'gl_code': '', 'account_name': '', 'currency_code': 'IDR', 'cash_code': '',
    }


async def create_from_payload(
    payload: dict,
    user_id: str,
    branch_code: str,
) -> int:
    """Otorisasi dispatcher — creates the CI transaction after approval.

    Returns transactionid (result_entity_id).
    """
    pool = get_pool()

    actual_date = date.fromisoformat(payload['actual_date'])
    payment_type = (payload.get('payment_type') or 'B').upper()  # 'K' | 'C' | 'B'
    description = payload.get('description', '') or ''
    reference_no = payload.get('reference_no', '') or ''
    paid_to = payload.get('paid_to', '') or user_id.upper()
    received_from = payload.get('received_from', '') or ''
    dest_account_no = payload.get('bank_account_no', '') or ''
    rate = float(payload.get('rate', 1.0) or 1.0)
    items = payload.get('items', [])

    if not items:
        raise ValueError('Minimal 1 item GL account wajib')
    if not dest_account_no:
        raise ValueError('Rekening kas/bank tujuan (bank_account_no) wajib diisi')

    year = actual_date.year
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    channel_code = 'P' if payment_type == 'K' else 'R'
    total_amount = sum(float(i.get('amount', 0)) for i in items)

    async with pool.acquire() as conn:
        async with conn.transaction():
            dest = await _resolve_account(conn, dest_account_no)
            dest_gl = dest['gl_code']
            currency = dest['currency_code'] or 'IDR'
            cash_code = dest['cash_code'] or dest_account_no

            # 1. Numbers: KM-YYYY-BRANCH-CASHCODE-SEQ7 ; journal CI001.YYYY.MM.SEQ7
            voucher_code = await conn.fetchval(
                "SELECT vouchercode FROM transaction.transactiontype WHERE transactioncode = 'CI'"
            ) or 'KM'
            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            transaction_no = f"{voucher_code}-{year}-{branch_code}-{cash_code}-{int(seq):07d}"
            jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            journal_no = f"CI001.{year}.{actual_date.month:02d}.{int(jseq):07d}"

            # 2. Header
            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """INSERT INTO transaction.transaction
                   (transactionid, transactiondate, transactiontime, actualdate,
                    referenceno, description, inputer, transactioncode, channelcode,
                    branchcode, authstatus, isposted, journalno, amount, currencycode,
                    transactionno, channelaccountno, paidto, receivedfrom, rate)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,'CI',$8,$9,'T','F',$10,$11,$12,$13,$14,$15,$16,$17)""",
                transaction_id, now_naive, now_naive, actual_date,
                reference_no, description, user_id.upper(), channel_code, branch_code,
                journal_no, total_amount, currency, transaction_no,
                dest_account_no, paid_to, received_from, rate,
            )

            # 3. Journal block + journal header
            block_id = int(await conn.fetchval("SELECT nextval('transaction.seq_journalblock')"))
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, class_id, key_id, journal_no, subsystemcode, transaction_tag)
                   VALUES ($1,'Transaction',$2,$3,'CORE','CI')""",
                block_id, transaction_id, journal_no,
            )
            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_type, journal_date, journal_date_posting,
                    transaction_date, description, userid_create, userid_posting,
                    is_posted, status, journal_state, branch_code,
                    source_app, source_app_class, source_app_ref, lastitemno)
                   VALUES ($1,'CI',$2,$2,$2,$3,$4,$4,'T','C','C',$5,'CORE','Transaction',$6,$7)""",
                journal_no, actual_date, description,
                user_id.upper(), branch_code, str(transaction_id), len(items) + 1,
            )

            jline = 0

            async def _journal_item(fl_account: str, debit: float, credit: float, desc: str, item_id: int):
                nonlocal jline
                jline += 1
                await conn.execute(
                    """INSERT INTO transaction.journalitem
                       (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                        description, branch_code, valuta_code, journalitemtype,
                        userid_create, id_journalblock, source_class_id, source_key_id)
                       VALUES ($1,$2,$3,$4,$5,$6,$7,'IDR','V',$8,$9,'TransactionItem',$10)""",
                    journal_no, jline, fl_account, debit, credit,
                    desc, branch_code, user_id.upper(), block_id, item_id,
                )

            # 4. GL income items (credit) + optional per-item source-account credit (Bank mode, C20)
            for item in items:
                amount = float(item.get('amount', 0))
                item_rate = float(item.get('rate', 1.0) or 1.0)
                account_code = item.get('account_code', '')
                account_name = item.get('account_name', '') or ''
                item_desc = item.get('description', '') or description
                item_currency = item.get('currency_code', 'IDR') or 'IDR'

                gl_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
                await conn.execute(
                    """INSERT INTO transaction.transactionitem
                       (transactionitemid, transactionid, branchcode, currencycode,
                        mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                        description, refaccountno, refaccountname, accountcode,
                        parameterjournalid, glnumber, glname)
                       VALUES ($1,$2,$3,$4,'C',$5,$6,$7,'G',$8,$9,$10,$9,'10',$9,$10)""",
                    gl_item_id, transaction_id, branch_code, item_currency,
                    amount, item_rate, amount * item_rate, item_desc,
                    account_code, account_name,
                )
                await _journal_item(account_code, 0.0, amount, item_desc, gl_item_id)

                # Optional source cash account leg (Bank-in transfer between accounts)
                source_no = item.get('cash_account_no') or ''
                if source_no:
                    src = await _resolve_account(conn, source_no)
                    fund_account_no = item.get('fund_account_no') or ''
                    src_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
                    await conn.execute(
                        """INSERT INTO transaction.transactionitem
                           (transactionitemid, transactionid, branchcode, currencycode,
                            mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                            description, refaccountno, refaccountname, accountcode, parameterjournalid)
                           VALUES ($1,$2,$3,$4,'C',$5,$6,$7,'A',$8,$9,$10,$11,'C20')""",
                        src_item_id, transaction_id, branch_code, item_currency,
                        amount, item_rate, amount * item_rate, item_desc,
                        source_no, src['account_name'], src['gl_code'],
                    )
                    await conn.execute(
                        """INSERT INTO transaction.accounttransactionitem
                           (transactionitemid, accountno, accounttitype, fundentity,
                            isupdatebalance, fundaccountno)
                           VALUES ($1, $2, 'A', 0, 'T', $3)""",
                        src_item_id, source_no, fund_account_no,
                    )
                    # source cash account is credited → asset balance decreases
                    await conn.execute(
                        "UPDATE transaction.financialaccount SET balance = balance - $1 WHERE accountno = $2",
                        amount, source_no,
                    )
                    await _journal_item(src['gl_code'], 0.0, amount, item_desc, src_item_id)

            # 5. Destination amil cash/bank debit (total)
            dest_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """INSERT INTO transaction.transactionitem
                   (transactionitemid, transactionid, branchcode, currencycode,
                    mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                    description, refaccountno, refaccountname, accountcode, parameterjournalid)
                   VALUES ($1,$2,$3,$4,'D',$5,$6,$7,'A',$8,$9,$10,$11,'10')""",
                dest_item_id, transaction_id, branch_code, currency,
                total_amount, rate, total_amount * rate, description,
                dest_account_no, dest['account_name'], dest_gl,
            )
            await conn.execute(
                """INSERT INTO transaction.accounttransactionitem
                   (transactionitemid, accountno, accounttitype, fundentity, isupdatebalance)
                   VALUES ($1, $2, 'A', 0, 'T')""",
                dest_item_id, dest_account_no,
            )
            # destination amil cash/bank is debited (receipt) → asset balance increases
            await conn.execute(
                "UPDATE transaction.financialaccount SET balance = balance + $1 WHERE accountno = $2",
                total_amount, dest_account_no,
            )
            await _journal_item(dest_gl, total_amount, 0.0, description, dest_item_id)

            # 6. History
            hist_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transhistoryofchanges')"))
            await conn.execute(
                """INSERT INTO transaction.transhistoryofchanges
                   (historyid, transactionid, transactionno, userid, processtime, changetype)
                   VALUES ($1,$2,$3,$4,$5,'I')""",
                hist_id, transaction_id, transaction_no, user_id.upper(), now_naive,
            )

    return transaction_id


async def get_kas_accounts_lookup(
    branch_code: str = '',
    payment_type: str = '',
) -> list[dict]:
    """Lookup amil cash/bank accounts (isamilaccount='T', active)."""
    pool = get_pool()
    where_parts = ["ca.isamilaccount = 'T'", "COALESCE(fa.status, 'A') = 'A'"]
    params: list = []
    idx = 1
    if branch_code:
        where_parts.append(f'fa.branchcode = ${idx}')
        params.append(branch_code)
        idx += 1
    where = ' AND '.join(where_parts)

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            f"""
            SELECT
                ca.accountno                       AS account_no,
                COALESCE(fa.accountname, ca.accountno) AS account_name,
                COALESCE(ca.bankname, '')          AS bank_name,
                COALESCE(NULLIF(ca.cashcode, ''), ca.accountno) AS cash_code,
                COALESCE(fa.currencycode, ca.accountcurrency, 'IDR') AS currency_code,
                COALESCE(fa.status, 'A')           AS status,
                true                               AS is_amil_account,
                COALESCE(fa.branchcode, '')        AS branch_code
            FROM transaction.cashaccount ca
            LEFT JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
            WHERE {where}
            ORDER BY account_name
            """,
            *params,
        )
    return [dict(r) for r in rows]


async def get_gl_accounts_lookup(
    branch_code: str = '',
    search: str = '',
) -> list[dict]:
    """Lookup amil revenue GL accounts (account_type='I', leaf, 430xxx family)."""
    pool = get_pool()
    where_parts = [
        "c.account_type = 'I'",
        "c.is_detail = 'T'",
        f"c.account_code LIKE '{_GL_AMIL_PREFIX}%'",
    ]
    params: list = []
    idx = 1
    if search:
        where_parts.append(f"(LOWER(c.account_code) LIKE ${idx} OR LOWER(c.account_name) LIKE ${idx})")
        params.append(f'%{search.lower()}%')
        idx += 1
    where = ' AND '.join(where_parts)

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            f"""
            SELECT
                c.account_code                   AS account_code,
                c.account_name                   AS account_name,
                c.account_type                   AS account_type,
                COALESCE(c.fl_parent_account, '') AS parent_account_code,
                COALESCE(p.account_name, '')     AS parent_account_name,
                'A'                              AS status
            FROM transaction.account c
            LEFT JOIN transaction.account p ON p.account_code = c.fl_parent_account
            WHERE {where}
            ORDER BY c.account_code
            """,
            *params,
        )
    return [dict(r) for r in rows]


async def get_next_transaction_number(
    payment_type: str = 'B',
    branch_code: str = '',
    bank_account_no: str = '',
) -> dict:
    """Preview the next CI transaction number (sequence not consumed)."""
    pool = get_pool()
    year = datetime.now(timezone.utc).year

    async with pool.acquire() as conn:
        voucher_code = await conn.fetchval(
            "SELECT vouchercode FROM transaction.transactiontype WHERE transactioncode = 'CI'"
        ) or 'KM'
        cash_code = bank_account_no or 'BMI'
        if bank_account_no:
            acc = await _resolve_account(conn, bank_account_no)
            cash_code = acc['cash_code'] or bank_account_no
        seq = await conn.fetchval("SELECT last_value FROM transaction.seq_transactionnumber")

    next_seq = int(seq or 0) + 1
    prefix = f"{voucher_code}-{year}-{branch_code}-{cash_code}"
    return {
        'next_number': f"{prefix}-{next_seq:07d}",
        'prefix': prefix,
        'sequence': next_seq,
    }

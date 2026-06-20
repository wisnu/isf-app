"""Business logic for Transfer Antar Rekening (transactioncode='TI')."""
from __future__ import annotations

from datetime import date, datetime, timezone

from asyncpg import Connection

from app.shared.db import get_pool


# ── List ──────────────────────────────────────────────────────────────────────

_LIST_SELECT = """
    SELECT
        t.transactionid,
        t.transactionno AS transaction_no,
        CAST(t.actualdate AS VARCHAR) AS actual_date,
        CAST(t.amount AS FLOAT) AS amount,
        t.authstatus AS auth_status,
        t.branchcode AS branch_code,
        t.inputer,
        COALESCE(t.description, '') AS description,
        COALESCE(t.referenceno, '') AS reference_no,
        fa_src.accountname AS source_account_name,
        ca_src.accountno AS source_cash_account_no,
        fa_dst.accountname AS dest_account_name,
        ca_dst.accountno AS dest_cash_account_no
    FROM transaction.transaction t
    LEFT JOIN transaction.transactionitem ti_src
        ON ti_src.transactionid = t.transactionid AND ti_src.mutationtype = 'C'
    LEFT JOIN transaction.financialaccount fa_src ON fa_src.accountno = ti_src.refaccountno
    LEFT JOIN transaction.cashaccount ca_src ON ca_src.accountno = fa_src.accountno
    LEFT JOIN transaction.transactionitem ti_dst
        ON ti_dst.transactionid = t.transactionid AND ti_dst.mutationtype = 'D'
    LEFT JOIN transaction.financialaccount fa_dst ON fa_dst.accountno = ti_dst.refaccountno
    LEFT JOIN transaction.cashaccount ca_dst ON ca_dst.accountno = fa_dst.accountno
"""


async def list_transfers(
    db: Connection,
    branch_code: str = "",
    page: int = 1,
    limit: int = 25,
    date_from: str = "",
    date_to: str = "",
) -> tuple[list[dict], int]:
    offset = (page - 1) * limit

    where_parts = ["t.transactioncode = 'TI'"]
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

    where = " AND ".join(where_parts)

    total = await db.fetchval(
        f"SELECT COUNT(DISTINCT t.transactionid) FROM transaction.transaction t WHERE {where}",
        *params,
    )

    rows = await db.fetch(
        f"{_LIST_SELECT} WHERE {where} ORDER BY t.actualdate DESC, t.transactionid DESC LIMIT ${idx} OFFSET ${idx+1}",
        *params, limit, offset,
    )
    return [dict(r) for r in rows], int(total or 0)


async def get_transfer_detail(db: Connection, transaction_id: int) -> dict | None:
    # Inject the two extra columns into the SELECT list (before FROM), then append WHERE.
    # _LIST_SELECT already carries the full FROM + JOINs (incl. ti_src/ti_dst).
    detail_select = _LIST_SELECT.replace(
        "        ca_dst.accountno AS dest_cash_account_no\n",
        "        ca_dst.accountno AS dest_cash_account_no,\n"
        "        ti_src.refaccountno AS source_account_no,\n"
        "        ti_dst.refaccountno AS dest_account_no\n",
    )
    row = await db.fetchrow(
        f"{detail_select} WHERE t.transactioncode = 'TI' AND t.transactionid = $1",
        transaction_id,
    )
    return dict(row) if row else None


# ── Lookup ─────────────────────────────────────────────────────────────────────

async def lookup_cash_accounts(search: str = "", branch_code: str = "") -> list[dict]:
    """Return semua cash accounts untuk dropdown (bank, kas, kas kecil)."""
    pool = get_pool()
    params: list = []
    conds: list = []
    idx = 1

    if search and search.strip():
        params.append(f"%{search.strip().lower()}%")
        conds.append(
            f"(LOWER(COALESCE(fa.accountname,'')) LIKE ${idx}"
            f" OR LOWER(COALESCE(ca.accountno,'')) LIKE ${idx})"
        )
        idx += 1

    if branch_code:
        params.append(branch_code)
        conds.append(f"fa.branchcode = ${idx}")
        idx += 1

    where = ("WHERE " + " AND ".join(conds)) if conds else ""

    rows = await pool.fetch(
        f"""SELECT
                ca.accountno AS cash_account_no,
                ca.accountno AS account_no,
                fa.accountname AS account_name,
                COALESCE(fa.branchcode, '') AS branch_code,
                CAST(fa.balance AS FLOAT) AS balance,
                COALESCE(ca.cashaccounttype, '') AS cash_account_type
            FROM transaction.cashaccount ca
            JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
            {where}
            ORDER BY fa.accountname
            LIMIT 100""",
        *params,
    )
    return [dict(r) for r in rows]


# ── Otorisasi Dispatcher ───────────────────────────────────────────────────────

async def create_from_payload(
    payload: dict,
    user_id: str,
    branch_code: str,
) -> int:
    """Otorisasi dispatcher — creates TI transaction after approval (or within-limit auto).

    Returns transactionid as result_entity_id.
    """
    pool = get_pool()

    actual_date = date.fromisoformat(payload['actual_date'])
    source_account_no = payload['source_account_no']  # cashaccount.accountno
    dest_account_no = payload['dest_account_no']       # cashaccount.accountno
    amount = float(payload['amount'])
    description = payload.get('description', '') or ''
    reference_no = payload.get('reference_no', '') or ''

    year = actual_date.year
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)

    async with pool.acquire() as conn:
        async with conn.transaction():

            # 1. Resolve source cash account → financial accountno
            src_acct = await conn.fetchrow(
                """SELECT ca.accountno,
                          COALESCE(ca.cashcode, '000') AS cashcode,
                          COALESCE(ca.accountinterface, ca.accountno) AS interface_accountno
                   FROM transaction.cashaccount ca
                   WHERE ca.accountno = $1""",
                source_account_no,
            )
            if not src_acct:
                raise ValueError(f'Rekening sumber {source_account_no} tidak ditemukan')
            src_financial_accountno = src_acct['accountno']
            src_cash_code = src_acct['cashcode']
            src_interface_accountno = src_acct['interface_accountno']

            # 2. Resolve dest cash account → financial accountno
            dst_acct = await conn.fetchrow(
                """SELECT ca.accountno,
                          COALESCE(ca.accountinterface, ca.accountno) AS interface_accountno
                   FROM transaction.cashaccount ca
                   WHERE ca.accountno = $1""",
                dest_account_no,
            )
            if not dst_acct:
                raise ValueError(f'Rekening tujuan {dest_account_no} tidak ditemukan')
            dst_financial_accountno = dst_acct['accountno']
            dst_interface_accountno = dst_acct['interface_accountno']

            if src_financial_accountno == dst_financial_accountno:
                raise ValueError('Rekening sumber dan tujuan tidak boleh sama')

            # 3. Generate transaction number  TI-YYYY-BRANCH-CASHCODE-NNNNNNN
            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            transaction_no = f"TI-{year}-{branch_code}-{src_cash_code}-{int(seq):07d}"

            # 4. Generate journal number
            jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            journal_no = f"TI001.{year}.{actual_date.month:02d}.{int(jseq):07d}"

            journal_code = 'TI'

            # 5. INSERT transaction
            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """INSERT INTO transaction.transaction
                   (transactionid, transactiondate, transactiontime, actualdate,
                    referenceno, description, inputer, transactioncode, channelcode,
                    branchcode, authstatus, isposted, journalno, amount, currencycode,
                    transactionno)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,'TI','10',$8,'T',false,$9,$10,'IDR',$11)""",
                transaction_id, actual_date, now_naive.time(), actual_date,
                reference_no, description, user_id.upper(),
                branch_code, journal_no, amount, transaction_no,
            )

            # 6. Journal block + header
            block_id = int(await conn.fetchval("SELECT nextval('transaction.seq_journalblock')"))
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, class_id, key_id, journal_no, subsystemcode, transaction_tag)
                   VALUES ($1,'Transaction',$2,$3,'CORE','TI')""",
                block_id, transaction_id, journal_no,
            )
            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_type, journal_date, journal_date_posting,
                    transaction_date, description, userid_create, userid_posting,
                    is_posted, status, journal_state, branch_code,
                    source_app, source_app_class, source_app_ref, lastitemno)
                   VALUES ($1,'TI',$2,$2,$2,$3,$4,$4,'T','C','C',$5,'CORE','Transaction',$6,2)""",
                journal_no, actual_date, description,
                user_id.upper(), branch_code, str(transaction_id),
            )

            journalitem_no = 0

            # 7. SOURCE CREDIT — money leaves source, balance decreases
            src_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """INSERT INTO transaction.transactionitem
                   (transactionitemid, transactionid, branchcode, currencycode,
                    mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                    description, refaccountno, accountcode, parameterjournalid)
                   VALUES ($1,$2,$3,'IDR','C',$4,1.0,$4,'A',$5,$6,$6,$7)""",
                src_item_id, transaction_id, branch_code,
                amount, description, src_financial_accountno, journal_code,
            )
            await conn.execute(
                """INSERT INTO transaction.accounttransactionitem
                   (transactionitemid, accountno, isupdatebalance)
                   VALUES ($1,$2,'T')""",
                src_item_id, src_financial_accountno,
            )
            await conn.execute(
                "UPDATE transaction.financialaccount SET balance = COALESCE(balance, 0) - $2 WHERE accountno = $1",
                src_financial_accountno, amount,
            )
            journalitem_no += 1
            await conn.execute(
                """INSERT INTO transaction.journalitem
                   (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                    description, branch_code, valuta_code, journalitemtype,
                    userid_create, id_journalblock, source_class_id, source_key_id)
                   VALUES ($1,$2,$3,0,$4,$5,$6,'IDR','V',$7,$8,'AccountTransactionItem',$9)""",
                journal_no, journalitem_no, src_interface_accountno, amount,
                description, branch_code, user_id.upper(), block_id, src_item_id,
            )

            # 8. DEST DEBIT — money arrives at destination, balance increases
            dst_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """INSERT INTO transaction.transactionitem
                   (transactionitemid, transactionid, branchcode, currencycode,
                    mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                    description, refaccountno, accountcode, parameterjournalid)
                   VALUES ($1,$2,$3,'IDR','D',$4,1.0,$4,'A',$5,$6,$6,$7)""",
                dst_item_id, transaction_id, branch_code,
                amount, description, dst_financial_accountno, journal_code,
            )
            await conn.execute(
                """INSERT INTO transaction.accounttransactionitem
                   (transactionitemid, accountno, isupdatebalance)
                   VALUES ($1,$2,'T')""",
                dst_item_id, dst_financial_accountno,
            )
            await conn.execute(
                "UPDATE transaction.financialaccount SET balance = COALESCE(balance, 0) + $2 WHERE accountno = $1",
                dst_financial_accountno, amount,
            )
            journalitem_no += 1
            await conn.execute(
                """INSERT INTO transaction.journalitem
                   (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                    description, branch_code, valuta_code, journalitemtype,
                    userid_create, id_journalblock, source_class_id, source_key_id)
                   VALUES ($1,$2,$3,$4,0,$5,$6,'IDR','V',$7,$8,'AccountTransactionItem',$9)""",
                journal_no, journalitem_no, dst_interface_accountno, amount,
                description, branch_code, user_id.upper(), block_id, dst_item_id,
            )

            # 9. History
            hist_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transhistoryofchanges')"))
            await conn.execute(
                """INSERT INTO transaction.transhistoryofchanges
                   (historyid, transactionid, transactionno, userid, processtime, changetype)
                   VALUES ($1,$2,$3,$4,$5,'I')""",
                hist_id, transaction_id, transaction_no, user_id.upper(), now_naive,
            )

    return transaction_id

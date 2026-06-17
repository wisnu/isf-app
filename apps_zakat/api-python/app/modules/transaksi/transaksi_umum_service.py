"""Business logic for Transaksi Umum (transactioncode='GT')."""
from __future__ import annotations

from datetime import date, datetime, timezone

from app.shared.db import get_pool


async def list_transaksi_umum(
    branch_code: str = '',
    page: int = 1,
    limit: int = 25,
    date_from: str = '',
    date_to: str = '',
    search: str = '',
) -> tuple[list[dict], int]:
    """List GT transactions with optional filters."""
    pool = get_pool()
    offset = (page - 1) * limit

    where_parts = ["t.transactioncode = 'GT'"]
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

    if search:
        where_parts.append(
            f"(LOWER(t.transactionno) LIKE ${idx} OR LOWER(t.description) LIKE ${idx})"
        )
        params.append(f'%{search.lower()}%')
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
                t.transactionid,
                t.transactionno,
                CAST(t.actualdate AS VARCHAR) AS actual_date,
                t.description,
                t.referenceno                AS reference_no,
                t.branchcode                 AS branch_code,
                t.inputer,
                t.authstatus,
                t.amount
            FROM transaction.transaction t
            WHERE {where}
            ORDER BY t.actualdate DESC, t.transactionid DESC
            LIMIT ${idx} OFFSET ${idx + 1}
            """,
            *params, limit, offset,
        )

    return [dict(r) for r in rows], int(total or 0)


async def get_transaksi_umum(transaction_id: int) -> dict | None:
    """Get GT transaction detail with line items."""
    pool = get_pool()
    async with pool.acquire() as conn:
        header = await conn.fetchrow(
            """
            SELECT
                t.transactionid,
                t.transactionno,
                CAST(t.actualdate AS VARCHAR) AS actual_date,
                t.description,
                t.referenceno                AS reference_no,
                t.branchcode                 AS branch_code,
                t.inputer,
                t.authstatus,
                t.amount
            FROM transaction.transaction t
            WHERE t.transactionid = $1 AND t.transactioncode = 'GT'
            """,
            transaction_id,
        )
        if not header:
            return None

        items = await conn.fetch(
            """
            SELECT
                ti.transactionitemid,
                ti.refaccountno              AS account_code,
                ti.refaccountname            AS account_name,
                ti.mutationtype              AS mutation_type,
                ti.amount,
                ti.description
            FROM transaction.transactionitem ti
            WHERE ti.transactionid = $1
            ORDER BY ti.transactionitemid
            """,
            transaction_id,
        )

    return {**dict(header), 'items': [dict(i) for i in items]}


async def create_from_payload(
    payload: dict,
    user_id: str,
    branch_code: str,
) -> int:
    """Otorisasi dispatcher — creates GT transaction after approval.

    Returns transactionid as result_entity_id.
    """
    pool = get_pool()

    actual_date = date.fromisoformat(payload['actual_date'])
    description = payload.get('description', '') or ''
    reference_no = payload.get('reference_no', '') or ''
    items = payload['items']  # list of {account_code, account_name, mutation_type, amount, description}

    year = actual_date.year
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    total_amount = sum(
        float(i['amount']) for i in items if i['mutation_type'] == 'D'
    )

    async with pool.acquire() as conn:
        async with conn.transaction():

            # 1. Generate transaction number: GT-YYYY-BRANCH-NNNNNNN
            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            transaction_no = f"GT-{year}-{branch_code}-{int(seq):07d}"

            # 2. Generate journal number
            jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            journal_no = f"GT001.{year}.{actual_date.month:02d}.{int(jseq):07d}"

            journal_code = 'GT'

            # 3. INSERT transaction header
            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """INSERT INTO transaction.transaction
                   (transactionid, transactiondate, transactiontime, actualdate,
                    referenceno, description, inputer, transactioncode, channelcode,
                    branchcode, authstatus, isposted, journalno, amount, currencycode,
                    transactionno)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,'GT','10',$8,'T',false,$9,$10,'IDR',$11)""",
                transaction_id, actual_date, now_naive.time(), actual_date,
                reference_no, description, user_id.upper(),
                branch_code, journal_no, total_amount, transaction_no,
            )

            # 4. Journal block
            block_id = int(await conn.fetchval("SELECT nextval('transaction.seq_journalblock')"))
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, class_id, key_id, journal_no, subsystemcode, transaction_tag)
                   VALUES ($1,'Transaction',$2,$3,'CORE','GT')""",
                block_id, transaction_id, journal_no,
            )
            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_type, journal_date, journal_date_posting,
                    transaction_date, description, userid_create, userid_posting,
                    is_posted, status, journal_state, branch_code,
                    source_app, source_app_class, source_app_ref, lastitemno)
                   VALUES ($1,'GT',$2,$2,$2,$3,$4,$4,'T','C','C',$5,'CORE','Transaction',$6,$7)""",
                journal_no, actual_date, description,
                user_id.upper(), branch_code, str(transaction_id), len(items),
            )

            # 5. INSERT transaction items + journal items
            for seq_no, item in enumerate(items, start=1):
                account_code = item['account_code']
                account_name = item['account_name']
                mutation_type = item['mutation_type']  # 'D' or 'C'
                amount = float(item['amount'])
                item_desc = item.get('description', '') or description

                item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
                await conn.execute(
                    """INSERT INTO transaction.transactionitem
                       (transactionitemid, transactionid, branchcode, currencycode,
                        mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                        description, refaccountno, refaccountname, accountcode, parameterjournalid)
                       VALUES ($1,$2,$3,'IDR',$4,$5,1.0,$5,'G',$6,$7,$8,$7,$9)""",
                    item_id, transaction_id, branch_code,
                    mutation_type, amount, item_desc,
                    account_code, account_name, journal_code,
                )

                debit_amt = amount if mutation_type == 'D' else 0
                credit_amt = amount if mutation_type == 'C' else 0
                await conn.execute(
                    """INSERT INTO transaction.journalitem
                       (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                        description, branch_code, valuta_code, journalitemtype,
                        userid_create, id_journalblock, source_class_id, source_key_id)
                       VALUES ($1,$2,$3,$4,$5,$6,$7,'IDR','V',$8,$9,'TransactionItem',$10)""",
                    journal_no, seq_no, account_code, debit_amt, credit_amt,
                    item_desc, branch_code, user_id.upper(), block_id, item_id,
                )

            # 6. History
            hist_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transhistoryofchanges')"))
            await conn.execute(
                """INSERT INTO transaction.transhistoryofchanges
                   (historyid, transactionid, transactionno, userid, processtime, changetype)
                   VALUES ($1,$2,$3,$4,$5,'I')""",
                hist_id, transaction_id, transaction_no, user_id.upper(), now_naive,
            )

    return transaction_id

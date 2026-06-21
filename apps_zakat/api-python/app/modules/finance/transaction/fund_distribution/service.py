from __future__ import annotations
from datetime import date, datetime, timezone

from app.modules.transaction.fund_distribution_repo import get_cashaccount, get_branch_cash
from app.modules.transaction.fund_distribution_schema import (
    CHANNEL_CODE_MAP, PenyaluranCreate, CreateResult,
)
from app.shared.db import get_pool


async def _get_or_create_batch(
    conn, actual_date: date, user_id: str, branch_code: str, now: datetime,
) -> int:
    row = await conn.fetchrow(
        """SELECT batchid FROM transaction.transactionbatch
           WHERE DATE(batchdate) = $1 AND UPPER(inputer) = $2 AND branchcode = $3
           ORDER BY batchid DESC LIMIT 1""",
        actual_date, user_id.upper(), branch_code,
    )
    if row:
        return int(row['batchid'])
    batch_id = await conn.fetchval("SELECT nextval('transaction.seq_transactionbatch')")
    await conn.execute(
        """INSERT INTO transaction.transactionbatch
           (batchid, batchdate, description, inputer, branchcode, isclosed, isposted)
           VALUES ($1, $2, 'Penyaluran Dana', $3, $4, 'F', 'F')""",
        int(batch_id), actual_date, user_id.upper(), branch_code,
    )
    return int(batch_id)


async def _resolve_payment(
    conn, req: PenyaluranCreate, branch_code: str,
) -> tuple[str, str, str]:
    """Return (payment_accountno, payment_interface_coa, cash_code)."""
    if req.payment_type == 'B':
        ca = await get_cashaccount(req.payment_account_no or '')
        if not ca:
            raise ValueError(f'Rekening bank {req.payment_account_no} tidak ditemukan')
        return (
            ca['accountno'],
            ca.get('accountinterface') or ca['accountno'],
            ca.get('cashcode') or 'BANK',
        )
    elif req.payment_type == 'K':
        ca = await get_cashaccount(req.payment_account_no or '')
        if not ca:
            raise ValueError(f'Rekening kas kecil {req.payment_account_no} tidak ditemukan')
        return (
            ca['accountno'],
            ca.get('accountinterface') or ca['accountno'],
            ca.get('cashcode') or 'KAS',
        )
    elif req.payment_type == 'C':
        ca = await get_branch_cash(branch_code, req.currency_code)
        if not ca:
            raise ValueError(f'Rekening kas cabang {branch_code} tidak ditemukan')
        return (
            ca['accountno'],
            ca.get('accountinterface') or ca['accountno'],
            'KAS',
        )
    elif req.payment_type == 'A':
        code = req.asset_code or ''
        return (code, code, 'ASET')
    raise ValueError(f'payment_type tidak dikenal: {req.payment_type}')


async def create_fund_distribution(
    req: PenyaluranCreate,
    user_id: str,
    branch_code: str,
) -> CreateResult:
    for item in req.items:
        if item.fund_entity == 1 and item.ashnaf in ('L', '', None):
            raise ValueError('Ashnaf wajib diisi untuk produk Zakat (fund_entity=1)')

    pool = get_pool()
    now = datetime.now(timezone.utc)
    now_naive = now.replace(tzinfo=None)
    actual_date = date.fromisoformat(req.actual_date)
    year = actual_date.year

    journal_code = '10' if req.product_branch_code == branch_code else '15'
    total_amount = sum(item.amount for item in req.items)
    channel_code = CHANNEL_CODE_MAP[req.payment_type]

    async with pool.acquire() as conn:
        async with conn.transaction():
            batch_id = await _get_or_create_batch(conn, actual_date, user_id, branch_code, now)
            payment_acctno, payment_coa, cash_code = await _resolve_payment(conn, req, branch_code)

            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            transaction_no = f"KK-{year}-{branch_code}-{cash_code}-{int(seq):07d}"

            jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            journal_no = f"DD001.{year}.{actual_date.month:02d}.{int(jseq):07d}"

            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """INSERT INTO transaction.transaction
                   (transactionid, transactiondate, transactiontime, actualdate,
                    referenceno, description, inputer, transactioncode, channelcode,
                    branchcode, authstatus, isposted, batchid, donorid,
                    paidto, receivedfrom, amount, currencycode, rate,
                    transactionno, channelaccountno, sponsorid, volunteerid)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,'DD001',$8,$9,'P','F',$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20)""",
                transaction_id, actual_date, now_naive, actual_date,
                req.reference_no, req.description, user_id.upper(),
                channel_code, branch_code, batch_id,
                req.donor_id, req.paid_to, req.received_from,
                total_amount, req.currency_code, req.rate,
                transaction_no,
                payment_acctno if req.payment_type != 'A' else req.asset_code,
                req.sponsor_id, req.volunteer_id,
            )

            block_id = int(await conn.fetchval("SELECT nextval('transaction.seq_journalblock')"))
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, class_id, key_id, journal_no, subsystemcode, transaction_tag)
                   VALUES ($1,'Transaction',$2,$3,'CORE','DD001')""",
                block_id, transaction_id, journal_no,
            )

            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_type, journal_date, journal_date_posting,
                    transaction_date, description, userid_create, userid_posting,
                    is_posted, status, journal_state, branch_code,
                    source_app, source_app_class, source_app_ref, lastitemno)
                   VALUES ($1,'DD001',$2,$2,$2,$3,$4,$4,'T','C','C',$5,'CORE','Transaction',$6,$7)""",
                journal_no, actual_date, req.description, user_id.upper(),
                branch_code, str(transaction_id), len(req.items) + 1,
            )

            journalitem_no = 0

            for item in req.items:
                item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
                await conn.execute(
                    """INSERT INTO transaction.transactionitem
                       (transactionitemid, transactionid, branchcode, currencycode,
                        mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                        description, refaccountno, accountcode, parameterjournalid)
                       VALUES ($1,$2,$3,$4,'D',$5,$6,$7,'A',$8,$9,$9,$10)""",
                    item_id, transaction_id, branch_code, req.currency_code,
                    item.amount, req.rate, item.amount * req.rate,
                    item.description or req.description,
                    item.account_no, journal_code,
                )
                await conn.execute(
                    """INSERT INTO transaction.accounttransactionitem
                       (transactionitemid, accounttitype, accountno, ashnaf,
                        fundentity, distributionitemaccount, distributioncategory,
                        fundaccountno, isupdatebalance)
                       VALUES ($1,'Z',$2,$3,$4,$5,$6,$7,'T')""",
                    item_id, item.account_no,
                    item.ashnaf if item.fund_entity == 1 else 'L',
                    item.fund_entity,
                    item.dist_item_account, item.distribution_category,
                    req.fund_account_no,
                )
                await conn.execute(
                    "UPDATE transaction.financialaccount SET balance = COALESCE(balance,0) - $2 WHERE accountno = $1",
                    item.account_no, item.amount,
                )
                journalitem_no += 1
                await conn.execute(
                    """INSERT INTO transaction.journalitem
                       (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                        description, branch_code, valuta_code, journalitemtype,
                        userid_create, id_journalblock, source_class_id, source_key_id)
                       VALUES ($1,$2,$3,$4,0,$5,$6,$7,'V',$8,$9,'ProductTransactionItem',$10)""",
                    journal_no, journalitem_no, item.account_no, item.amount,
                    item.description or req.description,
                    branch_code, req.currency_code, user_id.upper(), block_id, item_id,
                )

            pay_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """INSERT INTO transaction.transactionitem
                   (transactionitemid, transactionid, branchcode, currencycode,
                    mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                    description, refaccountno, accountcode, parameterjournalid)
                   VALUES ($1,$2,$3,$4,'C',$5,$6,$7,'A',$8,$9,$9,$10)""",
                pay_item_id, transaction_id, branch_code, req.currency_code,
                total_amount, req.rate, total_amount * req.rate,
                req.description, payment_acctno, journal_code,
            )
            await conn.execute(
                """INSERT INTO transaction.accounttransactionitem
                   (transactionitemid, accountno, isupdatebalance)
                   VALUES ($1,$2,'T')""",
                pay_item_id, payment_acctno,
            )
            if req.payment_type != 'A':
                await conn.execute(
                    "UPDATE transaction.financialaccount SET balance = COALESCE(balance,0) - $2 WHERE accountno = $1",
                    payment_acctno, total_amount,
                )
            journalitem_no += 1
            await conn.execute(
                """INSERT INTO transaction.journalitem
                   (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                    description, branch_code, valuta_code, journalitemtype,
                    userid_create, id_journalblock, source_class_id, source_key_id)
                   VALUES ($1,$2,$3,0,$4,$5,$6,$7,'V',$8,$9,'AccountTransactionItem',$10)""",
                journal_no, journalitem_no, payment_coa, total_amount,
                req.description, branch_code, req.currency_code,
                user_id.upper(), block_id, pay_item_id,
            )

            await conn.execute(
                "UPDATE transaction.transaction SET journalno = $2 WHERE transactionid = $1",
                transaction_id, journal_no,
            )

            hist_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transhistoryofchanges')"))
            await conn.execute(
                """INSERT INTO transaction.transhistoryofchanges
                   (historyid, transactionid, transactionno, userid, processtime, changetype)
                   VALUES ($1,$2,$3,$4,$5,'I')""",
                hist_id, transaction_id, transaction_no, user_id.upper(), now_naive,
            )

    return CreateResult(transaction_id=transaction_id, transaction_no=transaction_no)


async def create_from_payload(payload: dict, user_id: str, branch_code: str) -> int:
    """Adapter untuk otorisasi dispatcher. Menerima dict payload, return transaction_id."""
    req = PenyaluranCreate(**payload)
    result = await create_penyaluran(req, user_id, branch_code)
    return result.transaction_id

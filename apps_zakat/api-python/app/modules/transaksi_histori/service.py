from __future__ import annotations
from datetime import datetime, timezone
from app.modules.transaksi_histori import repository as repo
from app.modules.transaksi_histori.schema import (
    JournalItem, RepostResult, TransaksiDetail, TransaksiRow,
)
from app.shared.db import get_pool


def _to_row(r: dict) -> TransaksiRow:
    return TransaksiRow(
        transactionid=int(r['transactionid']),
        transactionno=r.get('transactionno'),
        transactiondate=str(r.get('transactiondate') or '')[:10],
        actualdate=str(r.get('actualdate') or '')[:10],
        amount=float(r.get('amount') or 0),
        donorno=r.get('donorno'),
        donorname=r.get('donorname'),
        referenceno=r.get('referenceno'),
        description=r.get('description'),
        inputer=r.get('inputer'),
        authstatus=r.get('authstatus'),
        isposted=r.get('isposted'),
        authoperationmode=r.get('authoperationmode'),
        branchcode=r.get('branchcode'),
        channelaccountno=r.get('channelaccountno'),
        channelname=r.get('channelname'),
        exttransactionid=r.get('exttransactionid'),
        titlesubsystem=r.get('titlesubsystem'),
    )


async def search(
    begin: str, end: str,
    date_type: str = 'actual',
    sort_by: str = 'actual_date',
    search_category: str = 'none',
    search_text: str | None = None,
    cash_account_no: str | None = None,
    limit: int = 50,
    branch: str | None = None,
    is_spv: bool = False,
    user_id: str = '',
) -> list[TransaksiRow]:
    rows = await repo.search_transactions(
        begin=begin, end=end, date_type=date_type, sort_by=sort_by,
        search_category=search_category, search_text=search_text,
        cash_account_no=cash_account_no, limit=limit,
        branch=branch, is_spv=is_spv, user_id=user_id,
    )
    return [_to_row(r) for r in rows]


async def detail(transaction_id: int) -> TransaksiDetail | None:
    row = await repo.get_transaction(transaction_id)
    if not row:
        return None
    journal_no = row.get('journalno')
    ji_raw = await repo.get_journal_items(journal_no) if journal_no else []
    journal_items = [
        JournalItem(
            journalitem_no=int(ji['journalitem_no']),
            fl_account=ji.get('fl_account'),
            account_name=ji.get('account_name'),
            branch_code=ji.get('branch_code'),
            valuta_code=ji.get('valuta_code'),
            amount_debit=float(ji.get('amount_debit') or 0),
            amount_credit=float(ji.get('amount_credit') or 0),
            description=ji.get('description'),
            subaccountcode=ji.get('subaccountcode'),
            subaccountname=ji.get('subaccountname'),
        )
        for ji in ji_raw
    ]
    return TransaksiDetail(**_to_row(row).model_dump(), journal_items=journal_items)


async def repost_journal(
    transaction_id: int,
    user_id: str,
    branch_code: str,
    is_spv: bool,
) -> RepostResult:
    pool = get_pool()
    async with pool.acquire() as conn:
        tx = await conn.fetchrow(
            """SELECT transactionid, transactionno, transactiondate,
                      branchcode, isposted
               FROM transaction.transaction WHERE transactionid = $1""",
            transaction_id,
        )
        if not tx:
            raise LookupError(f'Transaksi {transaction_id} tidak ditemukan')
        if not is_spv and (tx['branchcode'] or '').strip() != (branch_code or '').strip():
            raise PermissionError('BRANCH_FORBIDDEN')
        if (tx['isposted'] or 'F') == 'T':
            raise ValueError('ALREADY_POSTED')

        items = await conn.fetch(
            """SELECT ti.transactionitemid, ti.amount::float,
                      ati.accounttitype, ati.accountno
               FROM transaction.transactionitem ti
               JOIN transaction.accounttransactionitem ati
                 ON ati.transactionitemid = ti.transactionitemid
               WHERE ti.transactionid = $1""",
            transaction_id,
        )

        trans_date = tx['transactiondate']
        branch = (tx['branchcode'] or branch_code or '001').strip()
        year = trans_date.year if hasattr(trans_date, 'year') else int(str(trans_date)[:4])

        async with conn.transaction():
            seq = await conn.fetchval(
                "SELECT nextval('transaction.seq_transactionnumber')"
            )
            journal_no = f'J{branch}-{year}-{seq:07d}'

            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_date, journal_date_posting, description,
                    userid_create, branch_code, is_posted, status, source_app)
                   VALUES ($1,$2,$2,$3,$4,$5,'T','A','isf-app')""",
                journal_no, trans_date, tx['transactionno'], user_id, branch,
            )

            item_no = 1
            for item in items:
                if item['accounttitype'] == 'D':
                    await conn.execute(
                        """INSERT INTO transaction.journalitem
                           (fl_journal, journalitem_no, fl_account,
                            amount_credit, amount_debit, branch_code, valuta_code, userid_create)
                           VALUES ($1,$2,$3,$4,0,$5,'IDR',$6)""",
                        journal_no, item_no, item['accountno'],
                        item['amount'], branch, user_id,
                    )
                elif item['accounttitype'] == 'A':
                    await conn.execute(
                        """INSERT INTO transaction.journalitem
                           (fl_journal, journalitem_no, fl_account,
                            amount_debit, amount_credit, branch_code, valuta_code, userid_create)
                           VALUES ($1,$2,$3,$4,0,$5,'IDR',$6)""",
                        journal_no, item_no, item['accountno'],
                        item['amount'], branch, user_id,
                    )
                item_no += 1

            jblock_id = await conn.fetchval(
                "SELECT nextval('transaction.seq_journalblock')"
            )
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, journal_no, system_id, class_id, key_id)
                   VALUES ($1,$2,'TRANS','Transaction',$3)""",
                jblock_id, journal_no, transaction_id,
            )
            await conn.execute(
                "UPDATE transaction.transaction SET journalno=$1, isposted='T' WHERE transactionid=$2",
                journal_no, transaction_id,
            )

    return RepostResult(journal_no=journal_no, success=True)

# apps_zakat/api-python/app/modules/transaksi_histori/delete.py
"""Delete transaksi dua jalur:
  - authstatus='F': hapus langsung (reverse journal + balance jika sudah posted)
  - authstatus='T': tandai untuk dihapus (perlu approval supervisor)
"""
from __future__ import annotations
from datetime import datetime, timezone
from app.modules.transaksi_histori.schema import DeleteResult
from app.shared.db import get_pool


async def delete_transaction(
    transaction_id: int,
    user_id: str,
    branch_code: str,
    is_spv: bool,
) -> DeleteResult:
    pool = get_pool()
    async with pool.acquire() as conn:
        tx = await conn.fetchrow(
            """SELECT transactionid, transactionno, branchcode,
                      authstatus, authoperationmode, isposted, journalno
               FROM transaction.transaction WHERE transactionid = $1""",
            transaction_id,
        )
        if not tx:
            raise LookupError(f'Transaksi {transaction_id} tidak ditemukan')

        if not is_spv and (tx['branchcode'] or '').strip() != (branch_code or '').strip():
            raise PermissionError('BRANCH_FORBIDDEN')

        ext = await conn.fetchrow(
            "SELECT exttransactionid FROM transaction.externaltransaction "
            "WHERE transactionid = $1",
            transaction_id,
        )
        if ext:
            raise ValueError('EXTERNAL_TX')

        if (tx['authstatus'] or 'F') == 'F' and (tx['authoperationmode'] or '') == 'D':
            raise ValueError('ALREADY_PENDING_DELETE')

        if (tx['authstatus'] or 'F') == 'F':
            # Case A: unauth — delete immediately
            async with conn.transaction():
                if (tx['isposted'] or 'F') == 'T' and tx['journalno']:
                    jno = tx['journalno']
                    # Fetch items to reverse balances
                    items = await conn.fetch(
                        """SELECT ti.amount::float,
                                  ati.accounttitype, ati.accountno,
                                  ati.fundentity, ati.donorid
                           FROM transaction.transactionitem ti
                           JOIN transaction.accounttransactionitem ati
                             ON ati.transactionitemid = ti.transactionitemid
                           WHERE ti.transactionid = $1""",
                        transaction_id,
                    )
                    for item in items:
                        # Reverse balance on every account (both product and bank were +amount)
                        await conn.execute(
                            "UPDATE transaction.financialaccount "
                            "SET balance = COALESCE(balance,0) - $1 WHERE accountno = $2",
                            item['amount'], item['accountno'],
                        )
                        # Reverse donortotalfund only for product (type 'D') items
                        if item['accounttitype'] == 'D' and item['donorid'] and item['fundentity']:
                            existing = await conn.fetchrow(
                                """SELECT totalfundid FROM fund.donortotalfund
                                   WHERE donorid = $1 AND fundentity = $2
                                   ORDER BY totalfundid LIMIT 1""",
                                item['donorid'], item['fundentity'],
                            )
                            if existing:
                                await conn.execute(
                                    "UPDATE fund.donortotalfund "
                                    "SET totalamount = COALESCE(totalamount,0) - $1 "
                                    "WHERE totalfundid = $2",
                                    item['amount'], int(existing['totalfundid']),
                                )
                    # Delete journal
                    await conn.execute(
                        "DELETE FROM transaction.journalblock WHERE journal_no = $1", jno
                    )
                    await conn.execute(
                        "DELETE FROM transaction.journalitem WHERE fl_journal = $1", jno
                    )
                    await conn.execute(
                        "DELETE FROM transaction.journal WHERE journal_no = $1", jno
                    )

                # Delete transaction records
                await conn.execute(
                    """DELETE FROM transaction.accounttransactionitem
                       WHERE transactionitemid IN (
                           SELECT transactionitemid FROM transaction.transactionitem
                           WHERE transactionid = $1
                       )""",
                    transaction_id,
                )
                await conn.execute(
                    "DELETE FROM transaction.transactionitem WHERE transactionid = $1",
                    transaction_id,
                )
                await conn.execute(
                    "DELETE FROM transaction.transaction WHERE transactionid = $1",
                    transaction_id,
                )
                hist_id = await conn.fetchval(
                    "SELECT nextval('transaction.seq_transhistoryofchanges')"
                )
                await conn.execute(
                    """INSERT INTO transaction.transhistoryofchanges
                       (historyid, transactionid, transactionno, userid, processtime, changetype)
                       VALUES ($1,$2,$3,$4,$5,'D')""",
                    hist_id, transaction_id, tx['transactionno'],
                    user_id, datetime.now(timezone.utc),
                )
            return DeleteResult(
                deleted=True, pending_approval=False,
                message='Transaksi berhasil dihapus',
            )

        else:
            # Case B: auth — mark for supervisor approval
            await conn.execute(
                "UPDATE transaction.transaction "
                "SET authstatus='F', authoperationmode='D' WHERE transactionid=$1",
                transaction_id,
            )
            return DeleteResult(
                deleted=False, pending_approval=True,
                message='Transaksi ditandai untuk dihapus, menunggu otorisasi supervisor',
            )

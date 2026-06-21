"""Dispatcher services for HC ZIS batch operations (otorisasi dispatchers).

These are called automatically by otorisasi when submission status → AUTHORIZED.
All three are registered in otorisasi/service.py:_register_defaults().
"""
from __future__ import annotations

from datetime import datetime, timezone

from app.shared.db import get_pool

# Fund entity mapping for HC ZIS (Wakaf=3 is SKIPPED)
_HC_ZIS_FUNDS: list[dict] = [
    {'field': 'amountzakat',    'product_key': 'ZakatProfesi',  'fund_entity': 1, 'bank_param': 'BANKZAKAT'},
    {'field': 'amountinfaq',    'product_key': 'Infaq',          'fund_entity': 2, 'bank_param': 'BANKINFAQ'},
    {'field': 'amountanakasuh', 'product_key': 'AnakAsuh',       'fund_entity': 2, 'bank_param': 'BANKASUH'},
    {'field': 'amountanakyatim','product_key': 'AnakYatim',      'fund_entity': 2, 'bank_param': 'BANKYATIM'},
    {'field': 'amountqurban',   'product_key': 'TitipanQurban',  'fund_entity': 2, 'bank_param': 'BANKQURBAN'},
    # amountwakaf SKIP — fund_entity 3 disabled
]

from app.modules.finance.upload.collection.schema import PRODUCT_ID_MAP


async def _load_bank_params(conn) -> dict[str, str]:
    """Load bank accountno per jenis dana dari parameterglobal."""
    keys = ['BANKZAKAT', 'BANKINFAQ', 'BANKASUH', 'BANKYATIM', 'BANKQURBAN']
    rows = await conn.fetch(
        """SELECT kode_parameter, nilai_parameter_string
           FROM transaction.parameterglobal
           WHERE kode_parameter = ANY($1::varchar[])""",
        keys,
    )
    params = {r['kode_parameter']: r['nilai_parameter_string'] for r in rows}
    missing = [k for k in keys if not params.get(k)]
    if missing:
        raise ValueError(f"Parameter bank belum dikonfigurasi: {missing}")
    return params


async def _get_or_create_donor(conn, item: dict, branch_code: str) -> int:
    """Cari donor berdasarkan employeenumber; buat baru jika belum ada.

    Returns donorid.
    """
    emp_no = item.get('employeenumber') or ''

    # Cari existing donor by personalnumber
    row = await conn.fetchrow(
        """SELECT d.donorid FROM fund.donor d
           JOIN fund.individualdonor id ON id.donorid = d.donorid
           WHERE id.personalnumber = $1
             AND COALESCE(d.status, 'A') <> 'N'
           ORDER BY d.donorid LIMIT 1""",
        emp_no,
    )
    if row:
        return int(row['donorid'])

    # Buat donor baru
    donor_id = await conn.fetchval("SELECT nextval('fund.seq_donor')")
    donor_no = await conn.fetchval(
        "SELECT LPAD(CAST(nextval('fund.seq_donoridgen') AS VARCHAR), 7, '0')"
    )
    donor_no_str = f'P{donor_no}'
    name = item.get('name') or emp_no or 'KARYAWAN'

    await conn.execute(
        """INSERT INTO fund.donor
           (donorid, donorno, donorname, donorgroup, donortype, status, branchcode, created_at)
           VALUES ($1, $2, $3, 'R', 'I', 'A', $4, NOW())""",
        donor_id, donor_no_str, name, branch_code,
    )
    await conn.execute(
        """INSERT INTO fund.individualdonor
           (donorid, personalnumber, isinternalemployee,
            gender, maritalstatus, birthplace, birthdate,
            mobilephone, position, organizationalunit)
           VALUES ($1, $2, 'T', $3, $4, $5,
                   CAST($6 AS DATE), $7, $8, $9)""",
        donor_id, emp_no,
        item.get('gender') or '',
        item.get('maritalstatus') or '',
        item.get('birthplace') or '',
        item.get('birthdate') or None,
        item.get('mobilephone') or '',
        item.get('position') or '',
        item.get('organizationalunit') or '',
    )
    return int(donor_id)


async def _collection_account(conn, product_id: int, branch_code: str) -> str | None:
    row = await conn.fetchrow(
        """SELECT pa.accountno
           FROM transaction.productaccount pa
           JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
           WHERE pa.productid = $1
             AND fa.branchcode = $2
             AND fa.financialaccounttype = 'P'
             AND COALESCE(fa.status, 'A') = 'A'
           ORDER BY pa.accountno LIMIT 1""",
        product_id, branch_code,
    )
    return row['accountno'] if row else None


async def _upsert_donor_total_fund(conn, donor_id: int, fund_entity: int, amount: float) -> None:
    existing = await conn.fetchrow(
        """SELECT totalfundid FROM fund.donortotalfund
           WHERE donorid = $1 AND fundentity = $2
           ORDER BY totalfundid LIMIT 1""",
        donor_id, fund_entity,
    )
    if existing:
        await conn.execute(
            """UPDATE fund.donortotalfund
               SET totalamount = COALESCE(totalamount, 0) + $2
               WHERE totalfundid = $1""",
            int(existing['totalfundid']), amount,
        )
    else:
        new_id = await conn.fetchval("SELECT nextval('fund.seq_donortotalfund')")
        await conn.execute(
            """INSERT INTO fund.donortotalfund (totalfundid, donorid, fundentity, totalamount)
               VALUES ($1, $2, $3, $4)""",
            int(new_id), donor_id, fund_entity, amount,
        )


async def _commit_hc_item(
    conn,
    item: dict,
    *,
    donor_id: int,
    branch_code: str,
    inputer: str,
    bank_params: dict[str, str],
    year: int,
    batch_id: int,
) -> None:
    """Create accounting records for one HC ZIS batch item (per jenis dana aktif)."""
    now = datetime.now(timezone.utc)

    for fund_def in _HC_ZIS_FUNDS:
        amount_raw = item.get(fund_def['field'])
        amount = float(amount_raw) if amount_raw else 0.0
        if amount <= 0:
            continue

        product_id = PRODUCT_ID_MAP.get(fund_def['product_key'])
        if not product_id:
            continue

        fund_entity = fund_def['fund_entity']
        bank_accountno = bank_params.get(fund_def['bank_param'])
        if not bank_accountno:
            continue

        coll_acct = await _collection_account(conn, product_id, branch_code)
        if not coll_acct:
            continue

        # Resolve cash account
        cash_row = await conn.fetchrow(
            "SELECT accountno, cashcode FROM transaction.cashaccount WHERE bankaccountno = $1 OR accountno = $1 LIMIT 1",
            bank_accountno,
        )
        if not cash_row:
            continue
        cash_accountno = cash_row['accountno']
        cash_code = cash_row.get('cashcode') or 'KM'

        # Transaction number + journal
        seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
        transactionno = f'BPZIS-{year}-{int(seq):07d}'
        jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
        journal_no = f'J{branch_code}-{year}-{int(jseq):07d}'
        description = f"HC ZIS {item.get('name', '')} {fund_def['product_key']}"

        trx_id = await conn.fetchval("SELECT nextval('transaction.seq_transaction')")
        await conn.execute(
            """INSERT INTO transaction.transaction
               (transactionid, transactiondate, transactiontime, actualdate,
                description, inputer, transactioncode, channelcode,
                branchcode, authstatus, isposted, batchid,
                donorid, donorname, amount, currencycode, transactionno)
               VALUES ($1, $2, $3, $2, $4, $5, 'SD002', 'A', $6,
                       'A', 'T', $7, $8, $9, $10, 'IDR', $11)""",
            trx_id, now, now,
            description, inputer, branch_code,
            batch_id, donor_id, item.get('name', ''), amount, transactionno,
        )

        # Journal block
        block_id = await conn.fetchval("SELECT nextval('transaction.seq_journalblock')")
        await conn.execute(
            """INSERT INTO transaction.journalblock
               (id_journalblock, class_id, key_id, journal_no, subsystemcode, transaction_tag)
               VALUES ($1, 'Transaction', $2, $3, 'CORE', 'SD002')""",
            int(block_id), trx_id, journal_no,
        )

        # Journal header
        await conn.execute(
            """INSERT INTO transaction.journal
               (journal_no, journal_type, journal_date, journal_date_posting,
                transaction_date, description, userid_create, userid_posting,
                is_posted, status, journal_state, branch_code,
                source_app, source_app_class, source_app_ref, lastitemno)
               VALUES ($1, 'SD002', $2, $2, $2, $3, $4, $4,
                       'T', 'C', 'C', $5, 'CORE', 'Transaction', $6, 2)""",
            journal_no, now, description, inputer, branch_code, str(trx_id),
        )

        # Credit item (fund collection)
        item_id = await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')")
        await conn.execute(
            """INSERT INTO transaction.transactionitem
               (transactionitemid, transactionid, branchcode, currencycode,
                mutationtype, amount, transactionitemtype, description, refaccountno, accountcode)
               VALUES ($1, $2, $3, 'IDR', 'C', $4, 'A', $5, $6, $6)""",
            item_id, trx_id, branch_code, amount, description, coll_acct,
        )
        await conn.execute(
            """INSERT INTO transaction.accounttransactionitem
               (transactionitemid, accounttitype, accountno, fundentity, donorid, isupdatebalance)
               VALUES ($1, 'D', $2, $3, $4, 'T')""",
            item_id, coll_acct, fund_entity, donor_id,
        )
        await conn.execute(
            "UPDATE transaction.financialaccount SET balance = COALESCE(balance, 0) + $2 WHERE accountno = $1",
            coll_acct, amount,
        )
        await _upsert_donor_total_fund(conn, donor_id, fund_entity, amount)

        # Journal credit line
        await conn.execute(
            """INSERT INTO transaction.journalitem
               (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                description, branch_code, valuta_code, journalitemtype, userid_create,
                id_journalblock, source_class_id, source_key_id)
               VALUES ($1, 1, $2, 0, $3, $4, $5, 'IDR', 'V', $6, $7, 'DonorTransactionItem', $8)""",
            journal_no, coll_acct, amount, description, branch_code, inputer, int(block_id), item_id,
        )

        # Debit item (cash)
        bank_item_id = await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')")
        await conn.execute(
            """INSERT INTO transaction.transactionitem
               (transactionitemid, transactionid, branchcode, currencycode,
                mutationtype, amount, transactionitemtype, description, refaccountno, accountcode)
               VALUES ($1, $2, $3, 'IDR', 'D', $4, 'A', $5, $6, $6)""",
            bank_item_id, trx_id, branch_code, amount, description, cash_accountno,
        )
        await conn.execute(
            """INSERT INTO transaction.accounttransactionitem
               (transactionitemid, accounttitype, accountno, isupdatebalance)
               VALUES ($1, 'C', $2, 'T')""",
            bank_item_id, cash_accountno,
        )
        await conn.execute(
            "UPDATE transaction.financialaccount SET balance = COALESCE(balance, 0) + $2 WHERE accountno = $1",
            cash_accountno, amount,
        )

        await conn.execute(
            """INSERT INTO transaction.journalitem
               (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                description, branch_code, valuta_code, journalitemtype, userid_create,
                id_journalblock, source_class_id, source_key_id)
               VALUES ($1, 2, $2, $3, 0, $4, $5, 'IDR', 'V', $6, $7, 'AccountTransactionItem', $8)""",
            journal_no, cash_accountno, amount, description, branch_code, inputer, int(block_id), bank_item_id,
        )

        await conn.execute(
            "UPDATE transaction.transaction SET journalno = $2 WHERE transactionid = $1",
            trx_id, journal_no,
        )

        # Mark item as processed + set transactionid
        await conn.execute(
            """UPDATE transaction.humancapitalbatchitem
               SET isprocessed = 'Y', transactionid = $2, donorid = $3
               WHERE batchitemid = $1""",
            item['batchitemid'], trx_id, donor_id,
        )


async def create_from_payload(payload: dict, user_id: str, branch_code: str) -> int:
    """Dispatcher: hc_zis_upload — INSERT batch + items + create transactions."""
    pool = get_pool()
    year = datetime.now(timezone.utc).year

    batch_period_desc = payload.get('batch_period_desc', '')
    tanggal_transaksi = payload.get('tanggal_transaksi', '')
    namafile = payload.get('namafile', '')
    items_data = payload.get('items', [])
    totals = payload.get('totals', {})

    async with pool.acquire() as conn:
        bank_params = await _load_bank_params(conn)

        # Insert batch header
        async with conn.transaction():
            batch_id = await conn.fetchval(
                """INSERT INTO transaction.humancapitalbatch
                   (batchperioddesc, transactiondate, uploaduserid, uploaddate,
                    namafile, branchcode, grandtotal, totalrecord)
                   VALUES ($1, CAST($2 AS DATE), $3, NOW(), $4, $5, $6, $7)
                   RETURNING batchid""",
                batch_period_desc, tanggal_transaksi, user_id,
                namafile, branch_code,
                float(totals.get('grand_total', 0)),
                len(items_data),
            )

        # Process each item
        for item_data in items_data:
            total_amount = (
                float(item_data.get('zakat_amount', 0))
                + float(item_data.get('infaq_amount', 0))
                + float(item_data.get('anak_asuh_amount', 0))
                + float(item_data.get('anak_yatim_amount', 0))
                + float(item_data.get('taqurma_amount', 0))
            )
            if total_amount <= 0:
                continue

            async with conn.transaction():
                # Insert item row
                batchitemid = await conn.fetchval(
                    """INSERT INTO transaction.humancapitalbatchitem
                       (batchid, datano, businessareacode, businessareadescription,
                        employeenumber, name, birthplace, workareaname, mobilephone,
                        birthdate, gender, maritalstatus, position, organizationalunit,
                        amountzakat, amountinfaq, amountanakasuh, amountanakyatim,
                        amountwakaf, amountqurban, totalamount)
                       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9,
                               CASE WHEN $10 = '' THEN NULL ELSE CAST($10 AS DATE) END,
                               $11, $12, $13, $14,
                               $15, $16, $17, $18, $19, $20, $21)
                       RETURNING batchitemid""",
                    batch_id,
                    int(item_data.get('data_no', 0)),
                    item_data.get('business_area_code', ''),
                    item_data.get('business_area_desc', ''),
                    item_data.get('employee_number', ''),
                    item_data.get('employee_name', ''),
                    item_data.get('birth_place', ''),
                    item_data.get('work_area_name', ''),
                    item_data.get('mobile_phone', ''),
                    item_data.get('birth_date', ''),
                    item_data.get('gender', ''),
                    item_data.get('marital_status', ''),
                    item_data.get('position', ''),
                    item_data.get('organization_unit', ''),
                    float(item_data.get('zakat_amount', 0)),
                    float(item_data.get('infaq_amount', 0)),
                    float(item_data.get('anak_asuh_amount', 0)),
                    float(item_data.get('anak_yatim_amount', 0)),
                    float(item_data.get('wakaf_amount', 0)),
                    float(item_data.get('taqurma_amount', 0)),
                    total_amount,
                )

                # Map field names to DB column names for _commit_hc_item
                item_db = {
                    'batchitemid': batchitemid,
                    'employeenumber': item_data.get('employee_number', ''),
                    'name': item_data.get('employee_name', ''),
                    'gender': item_data.get('gender', ''),
                    'maritalstatus': item_data.get('marital_status', ''),
                    'birthplace': item_data.get('birth_place', ''),
                    'birthdate': item_data.get('birth_date', '') or None,
                    'mobilephone': item_data.get('mobile_phone', ''),
                    'position': item_data.get('position', ''),
                    'organizationalunit': item_data.get('organization_unit', ''),
                    'amountzakat': float(item_data.get('zakat_amount', 0)),
                    'amountinfaq': float(item_data.get('infaq_amount', 0)),
                    'amountanakasuh': float(item_data.get('anak_asuh_amount', 0)),
                    'amountanakyatim': float(item_data.get('anak_yatim_amount', 0)),
                    'amountwakaf': float(item_data.get('wakaf_amount', 0)),
                    'amountqurban': float(item_data.get('taqurma_amount', 0)),
                }

                donor_id = await _get_or_create_donor(conn, item_db, branch_code)
                await _commit_hc_item(
                    conn, item_db,
                    donor_id=donor_id,
                    branch_code=branch_code,
                    inputer=user_id,
                    bank_params=bank_params,
                    year=year,
                    batch_id=batch_id,
                )

    return batch_id


async def delete_from_payload(payload: dict, user_id: str, branch_code: str) -> None:
    """Dispatcher: hc_zis_delete — reverse transactions + delete batch."""
    pool = get_pool()
    batch_id = int(payload.get('batch_id', 0))
    if not batch_id:
        raise ValueError('batch_id missing in payload')

    async with pool.acquire() as conn:
        # Fetch all transaction IDs from batch items
        items = await conn.fetch(
            "SELECT batchitemid, transactionid FROM transaction.humancapitalbatchitem WHERE batchid = $1",
            batch_id,
        )
        trx_ids = [int(r['transactionid']) for r in items if r['transactionid']]

        async with conn.transaction():
            for trx_id in trx_ids:
                # Reverse balance for each transaction item
                await conn.execute(
                    """UPDATE transaction.financialaccount fa
                       SET balance = COALESCE(fa.balance, 0) - CAST(ti.amount AS numeric)
                       FROM transaction.transactionitem ti
                       JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
                       WHERE ti.transactionid = $1
                         AND ati.accountno = fa.accountno
                         AND ati.isupdatebalance = 'T'""",
                    trx_id,
                )
                # Reverse donortotalfund
                await conn.execute(
                    """UPDATE fund.donortotalfund dtf
                       SET totalamount = COALESCE(dtf.totalamount, 0) - CAST(ti.amount AS numeric)
                       FROM transaction.transactionitem ti
                       JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
                       WHERE ti.transactionid = $1
                         AND ati.accounttitype = 'D'
                         AND dtf.donorid = ati.donorid
                         AND dtf.fundentity = ati.fundentity""",
                    trx_id,
                )
                # Delete journal items + journal + block
                journal_no = await conn.fetchval(
                    "SELECT journalno FROM transaction.transaction WHERE transactionid = $1", trx_id
                )
                if journal_no:
                    await conn.execute("DELETE FROM transaction.journalitem WHERE fl_journal = $1", journal_no)
                    await conn.execute("DELETE FROM transaction.journalblock WHERE journal_no = $1", journal_no)
                    await conn.execute("DELETE FROM transaction.journal WHERE journal_no = $1", journal_no)

                await conn.execute("DELETE FROM transaction.accounttransactionitem WHERE transactionitemid IN (SELECT transactionitemid FROM transaction.transactionitem WHERE transactionid = $1)", trx_id)
                await conn.execute("DELETE FROM transaction.transactionitem WHERE transactionid = $1", trx_id)
                await conn.execute("DELETE FROM transaction.transaction WHERE transactionid = $1", trx_id)

            await conn.execute("DELETE FROM transaction.humancapitalpassedreport WHERE batchid = $1", batch_id)
            await conn.execute("DELETE FROM transaction.humancapitalbatchitem WHERE batchid = $1", batch_id)
            await conn.execute("DELETE FROM transaction.humancapitalbatch WHERE batchid = $1", batch_id)


async def update_date_from_payload(payload: dict, user_id: str, branch_code: str) -> None:
    """Dispatcher: hc_zis_update_date — update transaction date + journal period."""
    pool = get_pool()
    batch_id = int(payload.get('batch_id', 0))
    tanggal_baru = payload.get('tanggal_baru', '')
    if not batch_id or not tanggal_baru:
        raise ValueError('batch_id or tanggal_baru missing in payload')

    new_date_parts = tanggal_baru.split('-')
    new_year = int(new_date_parts[0]) if len(new_date_parts) >= 1 else 0
    new_month = int(new_date_parts[1]) if len(new_date_parts) >= 2 else 0

    async with pool.acquire() as conn:
        # Get all transaction IDs from this batch
        trx_ids = await conn.fetch(
            "SELECT transactionid FROM transaction.humancapitalbatchitem WHERE batchid = $1 AND transactionid IS NOT NULL",
            batch_id,
        )

        async with conn.transaction():
            for row in trx_ids:
                trx_id = int(row['transactionid'])
                await conn.execute(
                    "UPDATE transaction.transaction SET actualdate = CAST($2 AS DATE), transactiondate = CAST($2 AS DATE) WHERE transactionid = $1",
                    trx_id, tanggal_baru,
                )
                journal_no = await conn.fetchval(
                    "SELECT journalno FROM transaction.transaction WHERE transactionid = $1", trx_id
                )
                if journal_no:
                    await conn.execute(
                        """UPDATE transaction.journal
                           SET journal_date = CAST($2 AS DATE),
                               journal_date_posting = CAST($2 AS DATE),
                               fl_accountingperiode = $3,
                               fl_accountingyear = $4
                           WHERE journal_no = $1""",
                        journal_no, tanggal_baru, new_month, new_year,
                    )

            await conn.execute(
                "UPDATE transaction.humancapitalbatch SET transactiondate = CAST($2 AS DATE) WHERE batchid = $1",
                batch_id, tanggal_baru,
            )

"""Commit (approve) a manual upload batch into real accounting transactions.

When a supervisor approves a batch (``transaction.batchupload``), every row in
``transaction.batchuploaditem`` is turned into a full set of accounting records:

  * ``transaction.transaction``                (header, ``transactioncode='SDMULTI'``)
  * ``transaction.transactionitem``            (one credit per product + one bank debit)
  * ``transaction.accounttransactionitem``     (account-level detail per item)
  * ``transaction.financialaccount``           (running balance update per account)
  * ``fund.donortotalfund``                    (per-donor cumulative fund, upsert)
  * ``transaction.journal`` + ``journalitem``  (double-entry: credit products, debit bank)
  * ``transaction.journalblock``               (journal/source linkage)
  * ``transaction.transhistoryofchanges``      (audit, ``changetype='I'``)

All work for a single item runs inside one ``async with conn.transaction()`` block
so a failure rolls the whole item back. The batch header is flipped to authorized
(``authstatus='A'``) only after every item has committed.

Schema facts verified against ``mziss_laz`` (2026-06):
  * ``fund.donortotalfund`` PK is ``totalfundid`` and has **no** unique key on
    (donorid, fundentity) -> we SELECT-then-INSERT/UPDATE. Id from
    ``fund.seq_donortotalfund``.
  * The collection account for a product at a branch is the ``productaccount`` row
    whose ``financialaccount.branchcode = branch_code`` and ``financialaccounttype='P'``.
  * Real existing SDMULTI rows: credit item -> accounttitype 'D', isupdatebalance 'T';
    bank debit item -> accountno = cashaccount.accountno, isupdatebalance 'T'.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone

from app.modules.transaction.schema import FUND_ENTITY_MAP, PRODUCT_ID_MAP
from app.shared.db import get_pool


# product key -> batchuploaditem amount column
FIELD_MAP: dict[str, str] = {
    'ZakatProfesi':    'amountzakatprofesi',
    'ZakatMaal':       'amountzakatmaal',
    'ZakatFitrah':     'amountzakatfitrah',
    'ZakatPerusahaan': 'amountzakatperusahaan',
    'Infaq':           'amountinfaq',
    'InfaqTerikat':    'amountinfaqterikat',
    'DPU':             'amountdpu',
    'AnakYatim':       'amountanakyatim',
    'AnakAsuh':        'amountanakasuh',
    'TitipanWakaf':    'amounttitipanwakaf',
    'TitipanQurban':   'amounttitipanqurban',
    'Qurban':          'amountqurban',
    'NonHalal':        'amountnonhalal',
    'Fidyah':          'amountfidyah',
}

# Regex to pull a donor name out of a bank-statement description.
# Matches "... DARI BUDI ...", "TRANSFER DARI BUDI", "TRF DARI BUDI".
_DONOR_NAME_RE = re.compile(
    r'(?:TRANSFER\s+DARI|TRF\s+DARI|DARI)\s+([A-Z][A-Z .,\'-]{2,60})',
    re.IGNORECASE,
)


def _extract_donor_name(description: str | None) -> str | None:
    """Best-effort donor name extraction from a transaction description."""
    if not description:
        return None
    m = _DONOR_NAME_RE.search(description)
    if not m:
        return None
    name = m.group(1).strip(' .,\'-')
    return name or None


async def _get_default_donor(conn) -> tuple[int, str]:
    """Return (donorid, donorname) of the configured default ('Hamba Allah')."""
    row = await conn.fetchrow(
        """SELECT nilai_parameter, nilai_parameter_string
           FROM transaction.parameterglobal
           WHERE kode_parameter = 'DEF_DONOR'"""
    )
    donor_id = 1
    if row and row['nilai_parameter'] is not None:
        donor_id = int(row['nilai_parameter'])
    drow = await conn.fetchrow(
        "SELECT donorid, donorname FROM fund.donor WHERE donorid = $1",
        donor_id,
    )
    if drow:
        return int(drow['donorid']), (drow['donorname'] or 'HAMBA ALLAH')
    return donor_id, 'HAMBA ALLAH'


async def _match_donor_by_name(conn, name: str) -> tuple[int, str] | None:
    """Find an active donor whose name matches ``name`` (case-insensitive)."""
    row = await conn.fetchrow(
        """SELECT donorid, donorname
           FROM fund.donor
           WHERE UPPER(donorname) = UPPER($1)
             AND COALESCE(status, 'A') <> 'N'
           ORDER BY donorid
           LIMIT 1""",
        name,
    )
    if row:
        return int(row['donorid']), (row['donorname'] or name)
    return None


async def _resolve_donor(conn, description: str | None,
                         default_donor: tuple[int, str]) -> tuple[int, str]:
    """Pick a donor from the description if we can, else the default donor."""
    name = _extract_donor_name(description)
    if name:
        matched = await _match_donor_by_name(conn, name)
        if matched:
            return matched
    return default_donor


async def _collection_account(conn, product_id: int, branch_code: str) -> str | None:
    """Resolve the collection (fund) account for a product at a branch.

    The right account is the ``productaccount`` row joined to ``financialaccount``
    where the financial account lives in this branch and is a product/fund account
    (``financialaccounttype = 'P'``).
    """
    row = await conn.fetchrow(
        """SELECT pa.accountno
           FROM transaction.productaccount pa
           JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
           WHERE pa.productid = $1
             AND fa.branchcode = $2
             AND fa.financialaccounttype = 'P'
             AND COALESCE(fa.status, 'A') = 'A'
           ORDER BY pa.accountno
           LIMIT 1""",
        product_id, branch_code,
    )
    return row['accountno'] if row else None


async def _bank_account(conn, bankaccountno: str | None) -> dict | None:
    """Resolve the cash/bank account row by its bankaccountno (or accountno)."""
    if not bankaccountno:
        return None
    row = await conn.fetchrow(
        """SELECT accountno, bankaccountno, cashcode, productid, fundcategory
           FROM transaction.cashaccount
           WHERE bankaccountno = $1 OR accountno = $1
           LIMIT 1""",
        bankaccountno,
    )
    return dict(row) if row else None


async def _upsert_donor_total_fund(conn, donor_id: int, fund_entity: int,
                                   amount: float) -> None:
    """Add ``amount`` to the donor's cumulative fund for a fund-entity.

    ``fund.donortotalfund`` has no unique key on (donorid, fundentity), so we
    SELECT-then-UPDATE/INSERT inside the surrounding transaction.
    """
    existing = await conn.fetchrow(
        """SELECT totalfundid
           FROM fund.donortotalfund
           WHERE donorid = $1 AND fundentity = $2
           ORDER BY totalfundid
           LIMIT 1""",
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
            """INSERT INTO fund.donortotalfund
               (totalfundid, donorid, fundentity, totalamount)
               VALUES ($1, $2, $3, $4)""",
            int(new_id), donor_id, fund_entity, amount,
        )


def _product_fund_entity(product_id: int, product_key: str) -> int:
    """Map a product to its fund entity via the product's fund category.

    PRODUCT keys roughly map: Zakat* -> 'Z', Infaq -> 'I', InfaqTerikat/DPU/
    AnakYatim/AnakAsuh/Qurban/TitipanQurban -> 'T', TitipanWakaf -> 'W',
    NonHalal -> 'N'. We derive the category from the product key prefix so the
    FUND_ENTITY_MAP lookup stays a single source of truth.
    """
    if product_key.startswith('Zakat') or product_key == 'Fidyah':
        cat = 'Z'
    elif product_key == 'Infaq':
        cat = 'I'
    elif product_key == 'TitipanWakaf':
        cat = 'W'
    elif product_key == 'NonHalal':
        cat = 'N'
    else:
        cat = 'T'
    return FUND_ENTITY_MAP.get(cat, 2)


async def _commit_item(conn, item: dict, *, branch_code: str, inputer: str,
                       default_donor: tuple[int, str], year: int) -> tuple[int, str]:
    """Create all accounting records for a single batch item.

    Returns (transactionid, transactionno).
    """
    now = datetime.now(timezone.utc)
    trx_date = item.get('transactiondate') or now
    description = item.get('description') or ''

    # ── donor resolution ────────────────────────────────────────────────────
    donor_id, donor_name = await _resolve_donor(conn, description, default_donor)

    # ── per-product amounts (only > 0) ───────────────────────────────────────
    products: list[tuple[str, int, float, str]] = []  # (key, product_id, amount, coll_acct)
    total_amount = 0.0
    for key, col in FIELD_MAP.items():
        raw = item.get(col)
        amount = float(raw) if raw is not None else 0.0
        if amount <= 0:
            continue
        product_id = PRODUCT_ID_MAP[key]
        coll_acct = await _collection_account(conn, product_id, branch_code)
        if not coll_acct:
            raise ValueError(
                f"No collection account for product {key} ({product_id}) "
                f"at branch {branch_code}"
            )
        products.append((key, product_id, amount, coll_acct))
        total_amount += amount

    if not products:
        raise ValueError(
            f"Batch item {item.get('batchitemid')} has no product amount > 0"
        )

    # ── bank account ─────────────────────────────────────────────────────────
    bank = await _bank_account(conn, item.get('bankaccountno'))
    if not bank:
        raise ValueError(
            f"Unknown bank account {item.get('bankaccountno')!r} "
            f"for batch item {item.get('batchitemid')}"
        )
    bank_accountno = bank['accountno']
    cash_code = bank.get('cashcode') or 'KM'

    # ── transactionno + journal_no ───────────────────────────────────────────
    seq_no = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
    transactionno = f"SDMULTI-{year}-{branch_code}-{cash_code}-{int(seq_no):07d}"
    jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
    journal_no = f"J{branch_code}-{year}-{int(jseq):07d}"

    # ── transaction header ───────────────────────────────────────────────────
    transaction_id = await conn.fetchval("SELECT nextval('transaction.seq_transaction')")
    await conn.execute(
        """INSERT INTO transaction.transaction
           (transactionid, transactiondate, transactiontime, actualdate,
            referenceno, description, inputer, transactioncode, channelcode,
            branchcode, authstatus, isposted, batchid,
            donorid, donorname, amount, currencycode, transactionno)
           VALUES ($1, $2, $3, $2, $4, $5, $6, 'SDMULTI', 'A',
                   $7, 'A', 'T', $8, $9, $10, $11, 'IDR', $12)""",
        transaction_id, trx_date, now,
        item.get('referenceno'), description, inputer,
        branch_code, item.get('batchid'),
        donor_id, donor_name, total_amount, transactionno,
    )

    # journal block (links journal <-> transaction source)
    block_id = await conn.fetchval("SELECT nextval('transaction.seq_journalblock')")
    await conn.execute(
        """INSERT INTO transaction.journalblock
           (id_journalblock, class_id, key_id, journal_no, subsystemcode,
            transaction_tag)
           VALUES ($1, 'Transaction', $2, $3, 'CORE', 'SDMULTI')""",
        int(block_id), transaction_id, journal_no,
    )

    # journal header
    await conn.execute(
        """INSERT INTO transaction.journal
           (journal_no, journal_type, journal_date, journal_date_posting,
            transaction_date, description, userid_create, userid_posting,
            is_posted, status, journal_state, branch_code,
            source_app, source_app_class, source_app_ref, lastitemno)
           VALUES ($1, 'SDMULTI', $2, $2, $2, $3, $4, $4,
                   'T', 'C', 'C', $5, 'CORE', 'Transaction', $6, $7)""",
        journal_no, trx_date, description, inputer, branch_code,
        str(transaction_id), len(products) + 1,
    )

    journalitem_no = 0

    # ── credit side: one transactionitem + accounttransactionitem per product ─
    for key, product_id, amount, coll_acct in products:
        fund_entity = _product_fund_entity(product_id, key)

        item_id = await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')")
        await conn.execute(
            """INSERT INTO transaction.transactionitem
               (transactionitemid, transactionid, branchcode, currencycode,
                mutationtype, amount, transactionitemtype, description,
                refaccountno, accountcode)
               VALUES ($1, $2, $3, 'IDR', 'C', $4, 'A', $5, $6, $6)""",
            item_id, transaction_id, branch_code, amount, description, coll_acct,
        )
        await conn.execute(
            """INSERT INTO transaction.accounttransactionitem
               (transactionitemid, accounttitype, accountno, fundentity,
                donorid, isupdatebalance)
               VALUES ($1, 'D', $2, $3, $4, 'T')""",
            item_id, coll_acct, fund_entity, donor_id,
        )
        # update the collection account balance (credit increases fund)
        await conn.execute(
            """UPDATE transaction.financialaccount
               SET balance = COALESCE(balance, 0) + $2
               WHERE accountno = $1""",
            coll_acct, amount,
        )
        # cumulative donor fund
        await _upsert_donor_total_fund(conn, donor_id, fund_entity, amount)

        # journal credit line
        journalitem_no += 1
        await conn.execute(
            """INSERT INTO transaction.journalitem
               (fl_journal, journalitem_no, fl_account, amount_debit,
                amount_credit, description, branch_code, valuta_code,
                journalitemtype, userid_create, id_journalblock,
                source_class_id, source_key_id)
               VALUES ($1, $2, $3, 0, $4, $5, $6, 'IDR', 'V', $7, $8,
                       'DonorTransactionItem', $9)""",
            journal_no, journalitem_no, coll_acct, amount, description,
            branch_code, inputer, int(block_id), item_id,
        )

    # ── debit side: bank ──────────────────────────────────────────────────────
    bank_item_id = await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')")
    await conn.execute(
        """INSERT INTO transaction.transactionitem
           (transactionitemid, transactionid, branchcode, currencycode,
            mutationtype, amount, transactionitemtype, description,
            refaccountno, accountcode)
           VALUES ($1, $2, $3, 'IDR', 'D', $4, 'A', $5, $6, $6)""",
        bank_item_id, transaction_id, branch_code, total_amount, description,
        bank_accountno,
    )
    await conn.execute(
        """INSERT INTO transaction.accounttransactionitem
           (transactionitemid, accounttitype, accountno, isupdatebalance)
           VALUES ($1, 'A', $2, 'T')""",
        bank_item_id, bank_accountno,
    )
    await conn.execute(
        """UPDATE transaction.financialaccount
           SET balance = COALESCE(balance, 0) + $2
           WHERE accountno = $1""",
        bank_accountno, total_amount,
    )
    journalitem_no += 1
    await conn.execute(
        """INSERT INTO transaction.journalitem
           (fl_journal, journalitem_no, fl_account, amount_debit,
            amount_credit, description, branch_code, valuta_code,
            journalitemtype, userid_create, id_journalblock,
            source_class_id, source_key_id)
           VALUES ($1, $2, $3, $4, 0, $5, $6, 'IDR', 'V', $7, $8,
                   'AccountTransactionItem', $9)""",
        journal_no, journalitem_no, bank_accountno, total_amount, description,
        branch_code, inputer, int(block_id), bank_item_id,
    )

    # ── link journal back onto the transaction header ─────────────────────────
    await conn.execute(
        "UPDATE transaction.transaction SET journalno = $2 WHERE transactionid = $1",
        transaction_id, journal_no,
    )

    # ── audit ─────────────────────────────────────────────────────────────────
    history_id = await conn.fetchval(
        "SELECT nextval('transaction.seq_transhistoryofchanges')"
    )
    await conn.execute(
        """INSERT INTO transaction.transhistoryofchanges
           (historyid, transactionid, transactionno, userid, processtime, changetype)
           VALUES ($1, $2, $3, $4, $5, 'I')""",
        int(history_id), transaction_id, transactionno, inputer,
        now.replace(tzinfo=None),
    )

    # ── stamp the batch item ───────────────────────────────────────────────────
    await conn.execute(
        """UPDATE transaction.batchuploaditem
           SET transactionid = $2, transactionno = $3, donorid = $4,
               authstatus = 'A'
           WHERE batchitemid = $1""",
        item['batchitemid'], transaction_id, transactionno, donor_id,
    )

    return transaction_id, transactionno


async def approve_batch(batch_id: int, authorized_user: str, branch_code: str,
                        inputer: str) -> int:
    """Approve a batch: turn every batch item into real accounting transactions.

    Each item is committed in its own DB transaction; the batch header is flipped
    to authorized only after all items succeed. Returns the count of committed
    transactions as an ``int``.
    """
    pool = get_pool()
    year = datetime.now(timezone.utc).year

    async with pool.acquire() as conn:
        # Check batch exists and is not already approved
        batch_row = await conn.fetchrow(
            "SELECT authstatus FROM transaction.batchupload WHERE batchid = $1",
            batch_id,
        )
        if not batch_row:
            raise LookupError(f'Batch {batch_id} tidak ditemukan')
        if batch_row['authstatus'] == 'A':
            raise ValueError('Batch sudah pernah diotorisasi')
        if batch_row['authstatus'] == 'Q':
            raise ValueError('Batch sedang dalam proses otorisasi')

        items = await conn.fetch(
            """SELECT * FROM transaction.batchuploaditem
               WHERE batchid = $1
                 AND COALESCE(authstatus, 'P') <> 'A'
               ORDER BY batchitemid""",
            batch_id,
        )
        default_donor = await _get_default_donor(conn)

        committed = 0
        grand_total = 0.0
        for raw in items:
            item = dict(raw)
            # skip rows that failed validation
            if (item.get('validationstatus') or 'T') == 'F':
                continue
            async with conn.transaction():
                _, _ = await _commit_item(
                    conn, item,
                    branch_code=branch_code,
                    inputer=inputer,
                    default_donor=default_donor,
                    year=year,
                )
            committed += 1
            # accumulate the item's total for the batch header
            for col in FIELD_MAP.values():
                v = item.get(col)
                if v is not None and float(v) > 0:
                    grand_total += float(v)

        # ── finalize batch header ──────────────────────────────────────────────
        async with conn.transaction():
            await conn.execute(
                """UPDATE transaction.batchupload
                   SET authstatus = 'A',
                       authorizeduser = $2,
                       totalrecord = $3,
                       totalamount = $4
                   WHERE batchid = $1""",
                batch_id, authorized_user, committed, grand_total,
            )

    return committed


async def approve_batch_background(
    batch_id: int,
    authorized_user: str,
    branch_code: str,
    inputer: str,
) -> None:
    """Background task wrapper untuk approve_batch.
    Memanggil approve_batch() dan menangani error dengan set authstatus='F'."""
    from app.modules.transaction.repository import set_batch_failed
    try:
        await approve_batch(batch_id, authorized_user, branch_code, inputer)
    except Exception:
        await set_batch_failed(batch_id)

from __future__ import annotations
from app.shared.db import fetch_all, fetch_one, get_pool


async def get_bank_accounts() -> set[str]:
    """Return set of known bankaccountno from transaction.cashaccount."""
    rows = await fetch_all(
        "SELECT bankaccountno FROM transaction.cashaccount WHERE bankaccountno IS NOT NULL"
    )
    return {r['bankaccountno'] for r in rows if r['bankaccountno']}


async def get_existing_refs() -> set[tuple]:
    """Return set of (referenceno, transactiondate::date::text, amount) already in batchuploaditem."""
    rows = await fetch_all(
        """SELECT referenceno, to_char(transactiondate, 'YYYY-MM-DD') AS tdate, amount
           FROM transaction.batchuploaditem
           WHERE referenceno IS NOT NULL"""
    )
    return {(r['referenceno'], r['tdate'] or '', float(r['amount'] or 0)) for r in rows}


async def insert_batch(
    *,
    filename: str,
    branch_code: str,
    upload_user: str,
    total_record: int,
    total_amount: float,
) -> int:
    """Insert into transaction.batchupload, return batchid."""
    from datetime import datetime, timezone
    pool = get_pool()
    async with pool.acquire() as conn:
        batch_id = await conn.fetchval(
            "SELECT nextval('transaction.seq_batchupload')"
        )
        await conn.execute(
            """INSERT INTO transaction.batchupload
               (batchid, filename, branchcode, uploaduser, uploaddate,
                totalrecord, totalamount, batchuploadtype, authstatus)
               VALUES ($1,$2,$3,$4,$5,$6,$7,'M','P')""",
            batch_id, filename, branch_code, upload_user,
            datetime.now(timezone.utc), total_record, total_amount,
        )
    return batch_id


async def insert_batch_items(batch_id: int, rows: list[dict]) -> None:
    """Bulk insert batchuploaditem rows."""
    pool = get_pool()
    async with pool.acquire() as conn:
        for row in rows:
            item_id = await conn.fetchval(
                "SELECT nextval('transaction.seq_batchuploaditem')"
            )
            await conn.execute(
                """INSERT INTO transaction.batchuploaditem
                   (batchitemid, batchid, transactiondate, amount, description,
                    referenceno, bankaccountno, validationstatus,
                    amountzakatprofesi, amountzakatmaal, amountzakatfitrah,
                    amountzakatperusahaan, amountinfaq, amountinfaqterikat,
                    amountdpu, amountanakyatim, amountanakasuh,
                    amounttitipanwakaf, amounttitipanqurban,
                    amountqurban, amountnonhalal, amountfidyah)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,$8,
                           $9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22)""",
                item_id, batch_id,
                row['tanggal'], row['total_kredit'], row['keterangan'],
                row['no_ref'], row['no_rekening'],
                'T' if row['status'] == 'valid' else 'F',
                row['zakat_profesi'], row['zakat_maal'], row['zakat_fitrah'],
                row['zakat_perusahaan'], row['infaq'], row['infaq_terikat'],
                row['dpu'], row['anak_yatim'], row['anak_asuh'],
                row['titipan_wakaf'], row['titipan_qurban'],
                row['qurban'], row['non_halal'], row['fidyah'],
            )


async def list_batches(
    begin: str | None,
    end: str | None,
    status: str | None,
) -> list[dict]:
    conds = ["batchuploadtype = 'M'"]
    params: list = []
    if begin:
        params.append(begin)
        conds.append(f"uploaddate::date >= ${len(params)}")
    if end:
        params.append(end)
        conds.append(f"uploaddate::date <= ${len(params)}")
    if status and status.upper() in ('P', 'A'):
        params.append(status.upper())
        conds.append(f"COALESCE(authstatus,'P') = ${len(params)}")
    where = 'WHERE ' + ' AND '.join(conds)
    rows = await fetch_all(
        f"""SELECT batchid, filename, uploaddate, uploaduser, branchcode,
                   COALESCE(totalrecord,0) AS totalrecord,
                   COALESCE(totalamount,0) AS totalamount,
                   COALESCE(authstatus,'P') AS authstatus
            FROM transaction.batchupload
            {where}
            ORDER BY uploaddate DESC
            LIMIT 500""",
        *params,
    )
    return rows


async def get_batch(batch_id: int) -> dict | None:
    return await fetch_one(
        """SELECT batchid, filename, uploaddate, uploaduser, branchcode,
                  COALESCE(totalrecord,0) AS totalrecord,
                  COALESCE(totalamount,0) AS totalamount,
                  COALESCE(authstatus,'P') AS authstatus,
                  authorizeduser
           FROM transaction.batchupload
           WHERE batchid = $1""",
        batch_id,
    )


async def get_batch_items(batch_id: int) -> list[dict]:
    return await fetch_all(
        """SELECT batchitemid, transactiondate, amount, description, referenceno,
                  bankaccountno, validationstatus,
                  amountzakatprofesi, amountzakatmaal, amountzakatfitrah,
                  amountzakatperusahaan, amountinfaq, amountinfaqterikat,
                  amountdpu, amountanakyatim, amountanakasuh,
                  amounttitipanwakaf, amounttitipanqurban,
                  amountqurban, amountnonhalal, amountfidyah,
                  transactionno
           FROM transaction.batchuploaditem
           WHERE batchid = $1
           ORDER BY batchitemid""",
        batch_id,
    )

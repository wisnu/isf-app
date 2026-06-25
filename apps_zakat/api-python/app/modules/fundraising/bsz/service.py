from __future__ import annotations

import datetime

from app.modules.fundraising.bsz.schema import (
    AvailableTransaction,
    BszDetail,
    BszDetailItem,
    BszList,
    BszRow,
    BszTransactionItem,
    CreateBszBody,
    Pagination,
    ZakatObjectItem,
)
from app.shared.db import get_pool

_ROMAN = {
    1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
    7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII',
}


def _fmt_date(val) -> str:
    if val is None:
        return ''
    if hasattr(val, 'strftime'):
        return val.strftime('%Y-%m-%d')
    return str(val)[:10]


async def _next_id_gen(conn, id_code: str, table: str, pk_col: str) -> int:
    row = await conn.fetchrow(
        'SELECT last_id FROM fund.id_gen WHERE id_code=$1 FOR UPDATE', id_code
    )
    if row:
        new_id = row['last_id'] + 1
        await conn.execute('UPDATE fund.id_gen SET last_id=$1 WHERE id_code=$2', new_id, id_code)
    else:
        current_max = await conn.fetchval(f'SELECT COALESCE(MAX({pk_col}), 0) FROM {table}')
        new_id = current_max + 1
        await conn.execute(
            'INSERT INTO fund.id_gen(id_code, last_id, locked) VALUES($1,$2,$3)',
            id_code, new_id, 'F'
        )
    return new_id


async def _next_bsz_number(conn, year: int, month: int) -> str:
    year_str = str(year)
    row = await conn.fetchrow(
        "SELECT last_id FROM fund.custom_idgen WHERE idname='BSZ' AND idcode=$1 FOR UPDATE",
        year_str,
    )
    if row:
        new_id = row['last_id'] + 1
        await conn.execute(
            "UPDATE fund.custom_idgen SET last_id=$1 WHERE idname='BSZ' AND idcode=$2",
            new_id, year_str,
        )
    else:
        new_id = 1
        await conn.execute(
            "INSERT INTO fund.custom_idgen(idname, idcode, last_id, locked) VALUES('BSZ',$1,$2,'F')",
            year_str, new_id,
        )
    return f"{new_id:03d}/{_ROMAN[month]}/BPZIS/{year}"


async def list_zakat_objects() -> list[ZakatObjectItem]:
    async with get_pool().acquire() as conn:
        rows = await conn.fetch(
            "SELECT zakahobjectid, zakahobjectcode, zakahobjectname FROM fund.zakahobject ORDER BY zakahobjectid"
        )
    return [ZakatObjectItem(id=r['zakahobjectid'], code=r['zakahobjectcode'], name=r['zakahobjectname']) for r in rows]


async def list_bsz(
    donor_id: int | None,
    begin_date: str | None,
    end_date: str | None,
    limit: int,
    page: int,
) -> BszList:
    offset = (page - 1) * limit

    conditions = ['1=1']
    params: list = []
    p = 1

    if donor_id is not None:
        conditions.append(f'b.donorid = ${p}')
        params.append(donor_id)
        p += 1
    if begin_date:
        conditions.append(f"b.bszdate::date >= ${p}::date")
        params.append(begin_date)
        p += 1
    if end_date:
        conditions.append(f"b.bszdate::date <= ${p}::date")
        params.append(end_date)
        p += 1

    where = ' AND '.join(conditions)

    count_sql = f"""
        SELECT COUNT(DISTINCT b.bszid)
        FROM fund.bsz b
        JOIN fund.donor d ON b.donorid = d.donorid
        WHERE {where}
    """

    data_sql = f"""
        SELECT
            b.bszid,
            b.bsznumber,
            b.donorid,
            d.donorname,
            COALESCE(d.donorno, '') AS donorno,
            CAST(b.bszdate AS date) AS bszdate,
            CAST(b.bszperiodbegin AS date) AS periodbegin,
            CAST(b.bszperiodend AS date) AS periodend,
            COALESCE(SUM(bd.zakahvalue), 0) AS total
        FROM fund.bsz b
        JOIN fund.donor d ON b.donorid = d.donorid
        LEFT JOIN fund.bszdetail bd ON b.bszid = bd.bszid
        WHERE {where}
        GROUP BY b.bszid, b.bsznumber, b.donorid, d.donorname, d.donorno, b.bszdate, b.bszperiodbegin, b.bszperiodend
        ORDER BY b.bszdate DESC
        LIMIT ${p} OFFSET ${p+1}
    """
    params_data = params + [limit, offset]

    async with get_pool().acquire() as conn:
        total = await conn.fetchval(count_sql, *params)
        rows = await conn.fetch(data_sql, *params_data)

    items = [
        BszRow(
            bsz_id=r['bszid'],
            bsz_number=r['bsznumber'] or '',
            donor_id=r['donorid'],
            donor_name=r['donorname'] or '',
            donor_no=r['donorno'],
            bsz_date=_fmt_date(r['bszdate']),
            period_begin=_fmt_date(r['periodbegin']),
            period_end=_fmt_date(r['periodend']),
            total=float(r['total']),
        )
        for r in rows
    ]
    total_pages = max(1, (total + limit - 1) // limit)
    return BszList(rows=items, pagination=Pagination(page=page, limit=limit, total=total, total_pages=total_pages))


async def get_bsz_detail(bsz_id: int) -> BszDetail | None:
    async with get_pool().acquire() as conn:
        header = await conn.fetchrow("""
            SELECT
                b.bszid, b.bsznumber, b.donorid,
                d.donorname, COALESCE(d.donorno,'') AS donorno,
                d.npwz, d.npwp, d.addressstreet AS address,
                CAST(b.bszdate AS date) AS bszdate,
                CAST(b.bszperiodbegin AS date) AS periodbegin,
                CAST(b.bszperiodend AS date) AS periodend
            FROM fund.bsz b
            JOIN fund.donor d ON b.donorid = d.donorid
            WHERE b.bszid = $1
        """, bsz_id)

        if not header:
            return None

        detail_rows = await conn.fetch("""
            SELECT
                bd.item, zo.zakahobjectname AS zakahobject,
                COALESCE(bd.year, 0) AS year,
                COALESCE(bd.percentage, 2.5) AS percentage,
                COALESCE(bd.basicvalue, 0) AS basicvalue,
                COALESCE(bd.zakahvalue, 0) AS zakahvalue
            FROM fund.bszdetail bd
            LEFT JOIN fund.zakahobject zo ON bd.item = zo.zakahobjectid
            WHERE bd.bszid = $1
            ORDER BY bd.item
        """, bsz_id)

        tran_rows = await conn.fetch("""
            SELECT
                bt.transactionitemid,
                t.transactionno,
                CAST(t.actualdate AS date) AS actualdate,
                ti.amount,
                fa.accountname,
                t.description,
                COALESCE(p.zakahobject, '1') AS zakahobject
            FROM fund.bsztransaction bt
            JOIN transaction.transactionitem ti ON bt.transactionitemid = ti.transactionitemid
            JOIN transaction.transaction t ON ti.transactionid = t.transactionid
            JOIN transaction.accounttransactionitem ati
                ON ti.transactionitemid = ati.transactionitemid
               AND ati.fundentity = 1
               AND ati.accounttitype = 'D'
            JOIN transaction.financialaccount fa ON ati.accountno = fa.accountno
            LEFT JOIN transaction.productaccount pa ON fa.accountno = pa.accountno
            LEFT JOIN transaction.product p ON pa.productid = p.productid
            WHERE bt.bszid = $1
            ORDER BY t.actualdate, t.transactionno
        """, bsz_id)

    items = [
        BszDetailItem(
            item=r['item'],
            zakat_object=r['zakahobject'] or '',
            year=r['year'],
            percentage=float(r['percentage']),
            basic_value=float(r['basicvalue']),
            zakah_value=float(r['zakahvalue']),
        )
        for r in detail_rows
    ]
    transactions = [
        BszTransactionItem(
            transaction_item_id=r['transactionitemid'],
            transaction_no=r['transactionno'] or '',
            transaction_date=_fmt_date(r['actualdate']),
            amount=float(r['amount']),
            account_name=r['accountname'] or '',
            description=r['description'],
            zakah_object=r['zakahobject'],
        )
        for r in tran_rows
    ]

    return BszDetail(
        bsz_id=header['bszid'],
        bsz_number=header['bsznumber'] or '',
        donor_id=header['donorid'],
        donor_name=header['donorname'] or '',
        donor_no=header['donorno'],
        npwz=header['npwz'],
        npwp=header['npwp'],
        address=header['address'],
        bsz_date=_fmt_date(header['bszdate']),
        period_begin=_fmt_date(header['periodbegin']),
        period_end=_fmt_date(header['periodend']),
        items=items,
        transactions=transactions,
    )


async def get_available_transactions(
    donor_id: int,
    begin_date: str,
    end_date: str,
) -> list[AvailableTransaction]:
    # end_date exclusive (next day) to match legacy behavior
    end_dt = datetime.date.fromisoformat(end_date) + datetime.timedelta(days=1)

    async with get_pool().acquire() as conn:
        rows = await conn.fetch("""
            SELECT DISTINCT ON (ti.transactionitemid)
                ti.transactionitemid,
                t.transactionno,
                CAST(t.actualdate AS date) AS actualdate,
                ti.amount,
                fa.accountname,
                t.description,
                COALESCE(p.zakahobject, '1') AS zakahobject
            FROM transaction.transaction t
            JOIN transaction.transactionitem ti ON t.transactionid = ti.transactionid
            JOIN transaction.accounttransactionitem ati
                ON ti.transactionitemid = ati.transactionitemid
               AND ati.fundentity = 1
               AND ati.accounttitype = 'D'
               AND ati.donorid = $1
            JOIN transaction.financialaccount fa ON ati.accountno = fa.accountno
            LEFT JOIN transaction.productaccount pa ON fa.accountno = pa.accountno
            LEFT JOIN transaction.product p ON pa.productid = p.productid
            WHERE t.actualdate >= $2::date
              AND t.actualdate < $3::date
              AND NOT EXISTS (
                  SELECT 1 FROM fund.bsztransaction bt WHERE bt.transactionitemid = ti.transactionitemid
              )
            ORDER BY ti.transactionitemid, t.actualdate, t.transactionno
        """, donor_id, begin_date, str(end_dt))

    return [
        AvailableTransaction(
            transaction_item_id=r['transactionitemid'],
            transaction_no=r['transactionno'] or '',
            transaction_date=_fmt_date(r['actualdate']),
            amount=float(r['amount']),
            account_name=r['accountname'] or '',
            description=r['description'],
            zakah_object=r['zakahobject'],
        )
        for r in rows
    ]


async def create_bsz(body: CreateBszBody) -> BszDetail:
    if not body.items:
        raise ValueError('BSZ harus memiliki minimal satu item detail')
    if not body.transactions:
        raise ValueError('BSZ harus memiliki minimal satu transaksi')

    total_from_items = sum(item.zakah_value for item in body.items)
    total_from_trans = sum(0 for _ in body.transactions)  # amount from DB

    now = datetime.datetime.now()

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            bsz_id = await _next_id_gen(conn, 'BSZ', 'fund.bsz', 'bszid')
            bsz_number = await _next_bsz_number(conn, now.year, now.month)

            await conn.execute("""
                INSERT INTO fund.bsz (bszid, bsznumber, donorid, bszdate, bszperiodbegin, bszperiodend)
                VALUES ($1, $2, $3, $4, $5::date, $6::date)
            """, bsz_id, bsz_number, body.donor_id, now, body.period_begin, body.period_end)

            for detail in body.items:
                if detail.zakah_value == 0:
                    continue
                detail_id = await _next_id_gen(conn, 'BSZDETAIL', 'fund.bszdetail', 'bszdetailid')
                await conn.execute("""
                    INSERT INTO fund.bszdetail (bszdetailid, bszid, item, percentage, year, basicvalue, zakahvalue)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                """, detail_id, bsz_id, detail.item, detail.percentage, detail.year, detail.basic_value, detail.zakah_value)

            for tran in body.transactions:
                tran_id = await _next_id_gen(conn, 'BSZTRANSACTION', 'fund.bsztransaction', 'bsztransactionid')
                await conn.execute("""
                    INSERT INTO fund.bsztransaction (bsztransactionid, bszid, transactionitemid)
                    VALUES ($1, $2, $3)
                """, tran_id, bsz_id, tran.transaction_item_id)

    result = await get_bsz_detail(bsz_id)
    if result is None:
        raise RuntimeError('BSZ created but not found after insert')
    return result


async def delete_bsz(bsz_id: int) -> None:
    async with get_pool().acquire() as conn:
        exists = await conn.fetchval('SELECT bszid FROM fund.bsz WHERE bszid=$1', bsz_id)
        if not exists:
            raise ValueError(f'BSZ {bsz_id} tidak ditemukan')
        async with conn.transaction():
            await conn.execute('DELETE FROM fund.bsztransaction WHERE bszid=$1', bsz_id)
            await conn.execute('DELETE FROM fund.bszdetail WHERE bszid=$1', bsz_id)
            await conn.execute('DELETE FROM fund.bsz WHERE bszid=$1', bsz_id)

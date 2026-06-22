from __future__ import annotations

import math
from datetime import date as _Date
from decimal import Decimal

from app.modules.distribution.realization_return.schema import (
    CostItem,
    CreateRealizationReturnBody,
    Pagination,
    RealizationDetailLookupRow,
    RealizationLookupItem,
    RealizationReturnCostInput,
    RealizationReturnCostRow,
    RealizationReturnDetail,
    RealizationReturnDetailInput,
    RealizationReturnDetailRow,
    RealizationReturnList,
    RealizationReturnRow,
    UpdateRealizationReturnBody,
)
from app.shared.db import fetch_all, fetch_one, get_pool


def _parse_date(val) -> str | None:
    """Convert date/datetime to ISO YYYY-MM-DD string."""
    if val is None:
        return None
    try:
        return val.strftime('%Y-%m-%d')
    except AttributeError:
        s = str(val)
        return s[:10] if len(s) >= 10 else s


def _parse_decimal(val) -> float | None:
    """Convert decimal to float or None."""
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _row_to_return(r: dict) -> RealizationReturnRow:
    return RealizationReturnRow(
        return_id=r['returnid'],
        return_date=_parse_date(r['returndate']),
        return_description=r['returndescription'] or '',
        return_amount=_parse_decimal(r['returnamount']),
        realization_amount=_parse_decimal(r['realizationamount']),
        memo_number=r['realmemonumber'],
        branch_code=r['branchcode'],
    )


# ── Lookup: Cost Items ───────────────────────────────────────────────────────

async def lookup_cost_items() -> list[CostItem]:
    """Fetch all cost items."""
    rows = await fetch_all(
        """
        SELECT
            costitemid,
            costitemcode,
            costitemdescription
        FROM program.costitem
        ORDER BY costitemcode
        """
    )
    return [
        CostItem(
            cost_item_id=r['costitemid'],
            cost_item_code=r['costitemcode'],
            cost_item_description=r['costitemdescription'],
        )
        for r in rows
    ]


# ── Lookup: Realizations ─────────────────────────────────────────────────────

async def lookup_realizations(
    search: str | None = None,
    realization_type: str | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[RealizationLookupItem], int]:
    """
    Lookup realizations that do NOT already have a return.
    Exclude realizations that already have a return (no duplicate returns).
    """
    conds = [
        "NOT EXISTS (SELECT 1 FROM program.realizationreturn rr WHERE rr.realizationid = r.realizationid)"
    ]
    params: list = []

    if realization_type and realization_type.strip():
        params.append(realization_type.strip())
        conds.append(f'r.realizationtype = ${len(params)}')

    if search and search.strip():
        params.append(f'%{search.strip().lower()}%')
        idx = len(params)
        conds.append(f'LOWER(rm.realmemonumber) LIKE ${idx}')

    where = ' AND '.join(conds)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS total
        FROM program.realization r
        JOIN program.realizationmemo rm ON rm.realmemoid = r.realmemoid
        WHERE {where}
        """,
        *params,
    )
    total = count_row['total'] if count_row else 0
    total_pages = max(1, math.ceil(total / page_size))

    offset = (page - 1) * page_size
    params.append(page_size)
    limit_idx = len(params)
    params.append(offset)
    offset_idx = len(params)

    rows = await fetch_all(
        f"""
        SELECT
            r.realizationid,
            CAST(r.realizationdate AS DATE) AS realizationdate,
            r.realizationdescription,
            CAST(r.realizationamount AS numeric(30,8)) AS realizationamount,
            r.realizationtype,
            rm.realmemonumber
        FROM program.realization r
        JOIN program.realizationmemo rm ON rm.realmemoid = r.realmemoid
        WHERE {where}
        ORDER BY r.realizationdate DESC, r.realizationid DESC
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        """,
        *params,
    )

    return (
        [
            RealizationLookupItem(
                realization_id=r['realizationid'],
                realization_date=_parse_date(r['realizationdate']),
                realization_description=r['realizationdescription'],
                realization_amount=_parse_decimal(r['realizationamount']),
                realization_type=r['realizationtype'],
                memo_number=r['realmemonumber'],
            )
            for r in rows
        ],
        total,
    )


# ── Lookup: Realization Details ──────────────────────────────────────────────

async def lookup_realization_details(realization_id: int) -> list[RealizationDetailLookupRow]:
    """
    Load detail grid for a realization when selecting it.
    Join with mustahiqproduct and cashaccount.
    """
    rows = await fetch_all(
        """
        SELECT
            rd.realizationdetailid,
            CAST(rd.realizationamount AS numeric(30,8)) AS realization_amount,
            rd.accountno,
            mp.mustahiqproductid,
            mp.mustahiqproductname,
            ca.bankname AS account_name
        FROM program.realizationdetail rd
        JOIN program.mustahiqproduct mp ON mp.mustahiqproductid = rd.mustahiqproductid
        LEFT JOIN transaction.cashaccount ca ON ca.accountno = rd.accountno
        WHERE rd.realizationid = $1
        ORDER BY rd.realizationdetailid
        """,
        realization_id,
    )
    return [
        RealizationDetailLookupRow(
            realization_detail_id=r['realizationdetailid'],
            realization_amount=_parse_decimal(r['realization_amount']),
            account_no=r['accountno'],
            mustahiq_product_id=r['mustahiqproductid'],
            mustahiq_product_name=r['mustahiqproductname'],
            account_name=r['account_name'],
        )
        for r in rows
    ]


# ── List ──────────────────────────────────────────────────────────────────────

async def list_returns(
    begin_date: str,
    end_date: str,
    branch_code: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> RealizationReturnList:
    """List realization returns within date range, optionally filtered by branch."""
    conds = [
        "CAST(rr.returndate AS DATE) >= $1",
        "CAST(rr.returndate AS DATE) <= $2",
    ]
    params = [_Date.fromisoformat(begin_date), _Date.fromisoformat(end_date)]

    if branch_code:
        params.append(branch_code)
        conds.append(f'rr.branchcode = ${len(params)}')

    where = ' AND '.join(conds)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS total
        FROM program.realizationreturn rr
        WHERE {where}
        """,
        *params,
    )
    total = count_row['total'] if count_row else 0
    total_pages = max(1, math.ceil(total / page_size))

    offset = (page - 1) * page_size
    params.append(page_size)
    limit_idx = len(params)
    params.append(offset)
    offset_idx = len(params)

    rows = await fetch_all(
        f"""
        SELECT
            rr.returnid,
            CAST(rr.returndate AS DATE) AS returndate,
            rr.returndescription,
            CAST(rr.returnamount AS numeric(30,8)) AS returnamount,
            CAST(r.realizationamount AS numeric(30,8)) AS realizationamount,
            rm.realmemonumber,
            rr.branchcode
        FROM program.realizationreturn rr
        JOIN program.realization r ON r.realizationid = rr.realizationid
        JOIN program.realizationmemo rm ON rm.realmemoid = r.realmemoid
        WHERE {where}
        ORDER BY rr.returndate DESC, rr.returnid DESC
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        """,
        *params,
    )

    return RealizationReturnList(
        rows=[_row_to_return(r) for r in rows],
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_return(return_id: int) -> RealizationReturnDetail | None:
    """Fetch realization return with all details and costs."""
    row = await fetch_one(
        """
        SELECT
            rr.returnid,
            CAST(rr.returndate AS DATE) AS returndate,
            rr.returndescription,
            CAST(rr.returnamount AS numeric(30,8)) AS returnamount,
            CAST(rr.costamount AS numeric(30,4)) AS costamount,
            rr.realizationid,
            CAST(r.realizationdate AS DATE) AS realizationdate,
            r.realizationdescription,
            CAST(r.realizationamount AS numeric(30,8)) AS realizationamount,
            rm.realmemonumber,
            rr.branchcode
        FROM program.realizationreturn rr
        JOIN program.realization r ON r.realizationid = rr.realizationid
        JOIN program.realizationmemo rm ON rm.realmemoid = r.realmemoid
        WHERE rr.returnid = $1
        """,
        return_id,
    )
    if row is None:
        return None

    # Fetch details
    details = await fetch_all(
        """
        SELECT
            rrd.returndetailid,
            rrd.realizationdetailid,
            rrd.mustahiqproductid,
            mp.mustahiqproductname,
            rrd.accountno,
            ca.bankname AS account_name,
            CAST(rd.realizationamount AS numeric(30,8)) AS realization_amount,
            CAST(rrd.returnamount AS numeric(30,8)) AS return_amount,
            rrd.detaildescription
        FROM program.realizationreturndetail rrd
        JOIN program.mustahiqproduct mp ON mp.mustahiqproductid = rrd.mustahiqproductid
        LEFT JOIN transaction.cashaccount ca ON ca.accountno = rrd.accountno
        LEFT JOIN program.realizationdetail rd ON rd.realizationdetailid = rrd.realizationdetailid
        WHERE rrd.returnid = $1
        ORDER BY rrd.returndetailid
        """,
        return_id,
    )

    # Fetch costs
    costs = await fetch_all(
        """
        SELECT
            rc.realizationcostid,
            rc.costitemid,
            ci.costitemcode,
            ci.costitemdescription,
            CAST(rc.costamount AS numeric(30,4)) AS cost_amount
        FROM program.realizationcost rc
        LEFT JOIN program.costitem ci ON ci.costitemid = rc.costitemid
        WHERE rc.returnid = $1
        ORDER BY rc.realizationcostid
        """,
        return_id,
    )

    return RealizationReturnDetail(
        return_id=row['returnid'],
        return_date=_parse_date(row['returndate']),
        return_description=row['returndescription'],
        return_amount=_parse_decimal(row['returnamount']),
        cost_amount=_parse_decimal(row['costamount']),
        realization_id=row['realizationid'],
        realization_date=_parse_date(row['realizationdate']),
        realization_description=row['realizationdescription'],
        realization_amount=_parse_decimal(row['realizationamount']),
        memo_number=row['realmemonumber'],
        branch_code=row['branchcode'],
        details=[
            RealizationReturnDetailRow(
                return_detail_id=d['returndetailid'],
                realization_detail_id=d['realizationdetailid'],
                mustahiq_product_id=d['mustahiqproductid'],
                mustahiq_product_name=d['mustahiqproductname'],
                account_no=d['accountno'],
                account_name=d['account_name'],
                realization_amount=_parse_decimal(d['realization_amount']),
                return_amount=_parse_decimal(d['return_amount']),
                detail_description=d['detaildescription'],
            )
            for d in details
        ],
        costs=[
            RealizationReturnCostRow(
                cost_id=c['realizationcostid'],
                cost_item_id=c['costitemid'],
                cost_item_code=c['costitemcode'],
                cost_item_description=c['costitemdescription'],
                cost_amount=_parse_decimal(c['cost_amount']),
            )
            for c in costs
        ],
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_return(body: CreateRealizationReturnBody) -> int:
    """
    Create a new realization return with details and costs.

    Validations:
    - return_date >= realization_date
    - realization_id must exist
    - total return + total cost == total realization (from details sum)
    - each return_amount >= 0 and <= realization_amount for that detail
    """
    if not body.details:
        raise ValueError('Return harus memiliki minimal satu detail')

    return_date = _Date.fromisoformat(body.return_date)
    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Fetch realization to validate
            realization = await conn.fetchrow(
                """
                SELECT
                    realizationid,
                    CAST(realizationdate AS DATE) AS realizationdate,
                    CAST(realizationamount AS numeric(30,8)) AS realizationamount
                FROM program.realization
                WHERE realizationid = $1
                """,
                body.realization_id,
            )
            if not realization:
                raise ValueError('Realisasi tidak ditemukan')

            real_date = realization['realizationdate']
            if return_date < real_date:
                raise ValueError(f'Tanggal pengembalian tidak boleh sebelum tanggal realisasi ({real_date})')

            # Fetch realization details to validate amounts
            real_details = await conn.fetch(
                """
                SELECT
                    realizationdetailid,
                    CAST(realizationamount AS numeric(30,8)) AS realizationamount
                FROM program.realizationdetail
                WHERE realizationid = $1
                """,
                body.realization_id,
            )
            detail_map = {d['realizationdetailid']: d['realizationamount'] for d in real_details}

            # Validate each input detail
            total_return = Decimal('0')
            for detail_input in body.details:
                real_amount = detail_map.get(detail_input.realization_detail_id)
                if real_amount is None:
                    raise ValueError(
                        f'Detail realisasi {detail_input.realization_detail_id} tidak ditemukan'
                    )
                if detail_input.return_amount > real_amount:
                    raise ValueError(
                        f'Jumlah pengembalian {detail_input.return_amount} melebihi '
                        f'jumlah realisasi {real_amount}'
                    )
                total_return += detail_input.return_amount

            total_cost = sum(c.cost_amount for c in body.costs)
            total_expected = realization['realizationamount']

            if total_return + total_cost != total_expected:
                raise ValueError(
                    f'Total pengembalian + biaya ({total_return + total_cost}) '
                    f'harus sama dengan total realisasi ({total_expected})'
                )

            # Insert realizationreturn
            return_id = await conn.fetchval("SELECT nextval('program.seq_realizationreturn')")
            await conn.execute(
                """
                INSERT INTO program.realizationreturn (
                    returnid, returndate, returndescription, returnamount, costamount,
                    realizationid, branchcode, inputuser, inputdate
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW())
                """,
                return_id,
                return_date,
                body.return_description,
                total_return,
                total_cost,
                body.realization_id,
                body.branch_code or '',
                body.user_input or 'system',
            )

            # Insert details
            for detail_input in body.details:
                detail_id = await conn.fetchval("SELECT nextval('program.seq_realizationreturndetail')")
                await conn.execute(
                    """
                    INSERT INTO program.realizationreturndetail (
                        returndetailid, returnid, realizationdetailid, mustahiqproductid,
                        accountno, returnamount, realizationamount, detaildescription
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    detail_id,
                    return_id,
                    detail_input.realization_detail_id,
                    detail_input.mustahiq_product_id,
                    detail_input.account_no,
                    detail_input.return_amount,
                    detail_map[detail_input.realization_detail_id],
                    detail_input.detail_description,
                )

            # Insert costs
            for cost_input in body.costs:
                cost_id = await conn.fetchval("SELECT nextval('program.seq_realizationcost')")
                await conn.execute(
                    """
                    INSERT INTO program.realizationcost (
                        realizationcostid, costitemid, costamount, additionaldescription,
                        realizationid, realizationcosttype, returnid
                    ) VALUES ($1, $2, $3, $4, $5, 'R', $6)
                    """,
                    cost_id,
                    cost_input.cost_item_id,
                    cost_input.cost_amount,
                    cost_input.additional_description,
                    body.realization_id,
                    return_id,
                )

    return return_id


# ── Update ────────────────────────────────────────────────────────────────────

async def update_return(return_id: int, body: UpdateRealizationReturnBody) -> None:
    """
    Update realization return and replace all details and costs.
    Same validations as create.
    """
    if not body.details:
        raise ValueError('Return harus memiliki minimal satu detail')

    return_date = _Date.fromisoformat(body.return_date)
    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Check return exists
            existing = await conn.fetchrow(
                "SELECT returnid, realizationid FROM program.realizationreturn WHERE returnid = $1",
                return_id,
            )
            if not existing:
                raise ValueError('Pengembalian tidak ditemukan')

            # Fetch realization to validate
            realization = await conn.fetchrow(
                """
                SELECT
                    realizationid,
                    CAST(realizationdate AS DATE) AS realizationdate,
                    CAST(realizationamount AS numeric(30,8)) AS realizationamount
                FROM program.realization
                WHERE realizationid = $1
                """,
                body.realization_id,
            )
            if not realization:
                raise ValueError('Realisasi tidak ditemukan')

            real_date = realization['realizationdate']
            if return_date < real_date:
                raise ValueError(f'Tanggal pengembalian tidak boleh sebelum tanggal realisasi ({real_date})')

            # Fetch realization details to validate amounts
            real_details = await conn.fetch(
                """
                SELECT
                    realizationdetailid,
                    CAST(realizationamount AS numeric(30,8)) AS realizationamount
                FROM program.realizationdetail
                WHERE realizationid = $1
                """,
                body.realization_id,
            )
            detail_map = {d['realizationdetailid']: d['realizationamount'] for d in real_details}

            # Validate each input detail
            total_return = Decimal('0')
            for detail_input in body.details:
                real_amount = detail_map.get(detail_input.realization_detail_id)
                if real_amount is None:
                    raise ValueError(
                        f'Detail realisasi {detail_input.realization_detail_id} tidak ditemukan'
                    )
                if detail_input.return_amount > real_amount:
                    raise ValueError(
                        f'Jumlah pengembalian {detail_input.return_amount} melebihi '
                        f'jumlah realisasi {real_amount}'
                    )
                total_return += detail_input.return_amount

            total_cost = sum(c.cost_amount for c in body.costs)
            total_expected = realization['realizationamount']

            if total_return + total_cost != total_expected:
                raise ValueError(
                    f'Total pengembalian + biaya ({total_return + total_cost}) '
                    f'harus sama dengan total realisasi ({total_expected})'
                )

            # Update return header
            await conn.execute(
                """
                UPDATE program.realizationreturn SET
                    returndate = $2,
                    returndescription = $3,
                    returnamount = $4,
                    costamount = $5,
                    realizationid = $6
                WHERE returnid = $1
                """,
                return_id,
                return_date,
                body.return_description,
                total_return,
                total_cost,
                body.realization_id,
            )

            # Delete old details and costs (use discriminator WHERE returnid = ?)
            await conn.execute("DELETE FROM program.realizationreturndetail WHERE returnid = $1", return_id)
            await conn.execute("DELETE FROM program.realizationcost WHERE returnid = $1", return_id)

            # Insert new details
            for detail_input in body.details:
                detail_id = await conn.fetchval("SELECT nextval('program.seq_realizationreturndetail')")
                await conn.execute(
                    """
                    INSERT INTO program.realizationreturndetail (
                        returndetailid, returnid, realizationdetailid, mustahiqproductid,
                        accountno, returnamount, realizationamount, detaildescription
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    """,
                    detail_id,
                    return_id,
                    detail_input.realization_detail_id,
                    detail_input.mustahiq_product_id,
                    detail_input.account_no,
                    detail_input.return_amount,
                    detail_map[detail_input.realization_detail_id],
                    detail_input.detail_description,
                )

            # Insert new costs
            for cost_input in body.costs:
                cost_id = await conn.fetchval("SELECT nextval('program.seq_realizationcost')")
                await conn.execute(
                    """
                    INSERT INTO program.realizationcost (
                        realizationcostid, costitemid, costamount, additionaldescription,
                        realizationid, realizationcosttype, returnid
                    ) VALUES ($1, $2, $3, $4, $5, 'R', $6)
                    """,
                    cost_id,
                    cost_input.cost_item_id,
                    cost_input.cost_amount,
                    cost_input.additional_description,
                    body.realization_id,
                    return_id,
                )


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_return(return_id: int) -> None:
    """Delete realization return and cascade delete details and costs."""
    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Check return exists
            existing = await conn.fetchrow(
                "SELECT returnid FROM program.realizationreturn WHERE returnid = $1",
                return_id,
            )
            if not existing:
                raise ValueError('Pengembalian tidak ditemukan')

            # Delete details and costs (use discriminator WHERE returnid = ?)
            await conn.execute("DELETE FROM program.realizationreturndetail WHERE returnid = $1", return_id)
            await conn.execute("DELETE FROM program.realizationcost WHERE returnid = $1", return_id)

            # Delete return
            await conn.execute("DELETE FROM program.realizationreturn WHERE returnid = $1", return_id)

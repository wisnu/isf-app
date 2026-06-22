from __future__ import annotations

import math
from datetime import date as _Date

from app.modules.distribution.monitoring.schema import (
    CreateVisitBody,
    MustahiqLookupItem,
    Pagination,
    ProgramLookupItem,
    UpdateVisitBody,
    VisitDetail,
    VisitItemRow,
    VisitList,
    VisitPersonRow,
    VisitRow,
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


def _parse_datetime(val) -> str | None:
    """Convert datetime to ISO string or None."""
    if val is None:
        return None
    try:
        return val.isoformat()
    except AttributeError:
        return str(val) if val else None


def _row_to_visit(r: dict) -> VisitRow:
    return VisitRow(
        visit_id=r['visitid'],
        visit_date=_parse_date(r['visitdate']),
        visit_location=r['visitlocation'] or '',
        visit_address=r['visitaddress'] or '',
        mustahiq_name=r['customername'],
        program_name=r['productname'],
        mustahiq_product_name=r['mustahiqproductname'],
    )


# ── Lookup: mustahiq ─────────────────────────────────────────────────────────

async def lookup_mustahiq(search: str | None = None) -> list[MustahiqLookupItem]:
    """Lookup mustahiq by name or address."""
    conds = []
    params: list = []

    if search and search.strip():
        params.append(f'%{search.strip().lower()}%')
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(c.customername, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(c.addressstreet, \'\')) LIKE ${idx})'
        )

    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''

    rows = await fetch_all(
        f"""
        SELECT
            m.mustahiqid,
            c.customername,
            COALESCE(
                COALESCE(c.addressstreet, '')
                || COALESCE(' ' || c.addresskelurahan, '')
                || COALESCE(' ' || c.addresskecamatan, ''),
                ''
            ) AS address
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        ORDER BY c.customername
        LIMIT 200
        """,
        *params,
    )
    return [
        MustahiqLookupItem(
            mustahiq_id=r['mustahiqid'],
            mustahiq_name=r['customername'],
            address=r['address'],
        )
        for r in rows
    ]


# ── Lookup: programs ─────────────────────────────────────────────────────────

async def lookup_programs(
    mustahiq_id: int | None = None, search: str | None = None
) -> list[ProgramLookupItem]:
    """Lookup mustahiq products (programs) optionally filtered by mustahiq_id."""
    conds = []
    params: list = []

    if mustahiq_id:
        params.append(mustahiq_id)
        conds.append(f'mp.mustahiqid = ${len(params)}')

    if search and search.strip():
        params.append(f'%{search.strip().lower()}%')
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(c.customername, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(p.productname, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(mp.mustahiqproductname, \'\')) LIKE ${idx})'
        )

    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''

    rows = await fetch_all(
        f"""
        SELECT
            mp.mustahiqproductid,
            mp.mustahiqproductname,
            p.productname,
            c.customername
        FROM program.mustahiqproduct mp
        JOIN program.product p ON p.productid = mp.productid
        JOIN program.mustahiq m ON m.mustahiqid = mp.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        ORDER BY c.customername, p.productname
        LIMIT 200
        """,
        *params,
    )
    return [
        ProgramLookupItem(
            mustahiq_product_id=r['mustahiqproductid'],
            program_name=r['productname'],
            mustahiq_product_name=r['mustahiqproductname'],
            mustahiq_name=r['customername'],
        )
        for r in rows
    ]


# ── List ──────────────────────────────────────────────────────────────────────

async def list_visits(
    begin_date: str,
    end_date: str,
    page: int = 1,
    page_size: int = 25,
) -> VisitList:
    """List visits within date range."""
    params = [_Date.fromisoformat(begin_date), _Date.fromisoformat(end_date)]

    count_row = await fetch_one(
        """
        SELECT CAST(COUNT(*) AS INTEGER) AS total
        FROM program.visit a
        WHERE a.visittype = 'P'
          AND CAST(a.visitdate AS DATE) >= $1
          AND CAST(a.visitdate AS DATE) <= $2
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
        """
        SELECT
            a.visitid,
            CAST(a.visitdate AS DATE) AS visitdate,
            a.visitlocation,
            a.visitaddress,
            c.customername,
            COALESCE(p.productname, '') AS productname,
            COALESCE(mp.mustahiqproductname, '') AS mustahiqproductname
        FROM program.visit a
        JOIN program.mustahiq m ON m.mustahiqid = a.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        LEFT JOIN program.mustahiqproduct mp ON mp.mustahiqproductid = a.mustahiqproductid
        LEFT JOIN program.product p ON p.productid = mp.productid
        WHERE a.visittype = 'P'
          AND CAST(a.visitdate AS DATE) >= $1
          AND CAST(a.visitdate AS DATE) <= $2
        ORDER BY a.visitdate DESC, a.visitid DESC
        LIMIT $3 OFFSET $4
        """,
        *params,
    )

    return VisitList(
        rows=[_row_to_visit(r) for r in rows],
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        ),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_visit(visit_id: int) -> VisitDetail | None:
    """Fetch visit with all related persons and items."""
    row = await fetch_one(
        """
        SELECT
            a.visitid,
            CAST(a.visitdate AS DATE) AS visitdate,
            a.visitlocation,
            a.visitaddress,
            a.visitbegintime,
            a.visitendtime,
            c.customername,
            COALESCE(p.productname, '') AS productname,
            COALESCE(mp.mustahiqproductname, '') AS mustahiqproductname
        FROM program.visit a
        JOIN program.mustahiq m ON m.mustahiqid = a.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        LEFT JOIN program.mustahiqproduct mp ON mp.mustahiqproductid = a.mustahiqproductid
        LEFT JOIN program.product p ON p.productid = mp.productid
        WHERE a.visitid = $1
          AND a.visittype = 'P'
        """,
        visit_id,
    )
    if row is None:
        return None

    # Fetch persons by type
    persons_amil = await fetch_all(
        """
        SELECT visitpersonid, visitpersonname, visitpersonposition
        FROM program.visitperson
        WHERE visitid = $1 AND visitpersontype = 'A'
        ORDER BY visitpersonid
        """,
        visit_id,
    )

    persons_mustahiq = await fetch_all(
        """
        SELECT visitpersonid, visitpersonname, visitpersonposition
        FROM program.visitperson
        WHERE visitid = $1 AND visitpersontype = 'S'
        ORDER BY visitpersonid
        """,
        visit_id,
    )

    # Fetch items by type
    purposes = await fetch_all(
        """
        SELECT visititemid, visititemannotation
        FROM program.visititem
        WHERE visitid = $1 AND visititemtype = 'P'
        ORDER BY visititemid
        """,
        visit_id,
    )

    results = await fetch_all(
        """
        SELECT visititemid, visititemannotation
        FROM program.visititem
        WHERE visitid = $1 AND visititemtype = 'R'
        ORDER BY visititemid
        """,
        visit_id,
    )

    followups = await fetch_all(
        """
        SELECT visititemid, visititemannotation
        FROM program.visititem
        WHERE visitid = $1 AND visititemtype = 'F'
        ORDER BY visititemid
        """,
        visit_id,
    )

    visit_detail = _row_to_visit(row)
    return VisitDetail(
        visit_id=visit_detail.visit_id,
        visit_date=visit_detail.visit_date,
        visit_location=visit_detail.visit_location,
        visit_address=visit_detail.visit_address,
        visit_begin_time=_parse_datetime(row['visitbegintime']),
        visit_end_time=_parse_datetime(row['visitendtime']),
        mustahiq_name=visit_detail.mustahiq_name,
        program_name=visit_detail.program_name,
        mustahiq_product_name=visit_detail.mustahiq_product_name,
        persons_amil=[
            VisitPersonRow(
                visit_person_id=p['visitpersonid'],
                visit_person_name=p['visitpersonname'],
                visit_person_position=p['visitpersonposition'],
            )
            for p in persons_amil
        ],
        persons_mustahiq=[
            VisitPersonRow(
                visit_person_id=p['visitpersonid'],
                visit_person_name=p['visitpersonname'],
                visit_person_position=p['visitpersonposition'],
            )
            for p in persons_mustahiq
        ],
        purposes=[
            VisitItemRow(
                visit_item_id=i['visititemid'],
                visit_item_annotation=i['visititemannotation'] or '',
            )
            for i in purposes
        ],
        results=[
            VisitItemRow(
                visit_item_id=i['visititemid'],
                visit_item_annotation=i['visititemannotation'] or '',
            )
            for i in results
        ],
        followups=[
            VisitItemRow(
                visit_item_id=i['visititemid'],
                visit_item_annotation=i['visititemannotation'] or '',
            )
            for i in followups
        ],
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_visit(body: CreateVisitBody) -> int:
    """Create a new visit with persons and items."""
    if not body.persons_amil:
        raise ValueError('Visit harus memiliki minimal satu orang dari BPZIS')
    if not body.persons_mustahiq:
        raise ValueError('Visit harus memiliki minimal satu orang dari mustahiq')
    if not body.purposes:
        raise ValueError('Visit harus memiliki minimal satu tujuan')
    if not body.results:
        raise ValueError('Visit harus memiliki minimal satu hasil')
    if not body.followups:
        raise ValueError('Visit harus memiliki minimal satu tindak lanjut')

    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Insert visit
            visit_id = await conn.fetchval("SELECT nextval('program.seq_visit')")
            await conn.execute(
                """
                INSERT INTO program.visit (
                    visitid, visittype, visitdate, visitlocation, visitaddress,
                    visitbegintime, visitendtime, mustahiqid, mustahiqproductid
                ) VALUES ($1, 'P', $2, $3, $4, $5, $6, $7, $8)
                """,
                visit_id,
                _Date.fromisoformat(body.visit_date),
                body.visit_location,
                body.visit_address,
                body.visit_begin_time,
                body.visit_end_time,
                body.mustahiq_id,
                body.mustahiq_product_id,
            )

            # Insert persons (amil)
            for person in body.persons_amil:
                person_id = await conn.fetchval("SELECT nextval('program.seq_visitperson')")
                await conn.execute(
                    """
                    INSERT INTO program.visitperson (
                        visitpersonid, visitid, visitpersonname, visitpersonposition, visitpersontype
                    ) VALUES ($1, $2, $3, $4, 'A')
                    """,
                    person_id,
                    visit_id,
                    person.visit_person_name,
                    person.visit_person_position,
                )

            # Insert persons (mustahiq)
            for person in body.persons_mustahiq:
                person_id = await conn.fetchval("SELECT nextval('program.seq_visitperson')")
                await conn.execute(
                    """
                    INSERT INTO program.visitperson (
                        visitpersonid, visitid, visitpersonname, visitpersonposition, visitpersontype
                    ) VALUES ($1, $2, $3, $4, 'S')
                    """,
                    person_id,
                    visit_id,
                    person.visit_person_name,
                    person.visit_person_position,
                )

            # Insert items (purposes)
            for item in body.purposes:
                item_id = await conn.fetchval("SELECT nextval('program.seq_visititem')")
                await conn.execute(
                    """
                    INSERT INTO program.visititem (
                        visititemid, visitid, visititemtype, visititemannotation
                    ) VALUES ($1, $2, 'P', $3)
                    """,
                    item_id,
                    visit_id,
                    item.visit_item_annotation,
                )

            # Insert items (results)
            for item in body.results:
                item_id = await conn.fetchval("SELECT nextval('program.seq_visititem')")
                await conn.execute(
                    """
                    INSERT INTO program.visititem (
                        visititemid, visitid, visititemtype, visititemannotation
                    ) VALUES ($1, $2, 'R', $3)
                    """,
                    item_id,
                    visit_id,
                    item.visit_item_annotation,
                )

            # Insert items (followups)
            for item in body.followups:
                item_id = await conn.fetchval("SELECT nextval('program.seq_visititem')")
                await conn.execute(
                    """
                    INSERT INTO program.visititem (
                        visititemid, visitid, visititemtype, visititemannotation
                    ) VALUES ($1, $2, 'F', $3)
                    """,
                    item_id,
                    visit_id,
                    item.visit_item_annotation,
                )

    return visit_id


# ── Update ────────────────────────────────────────────────────────────────────

async def update_visit(visit_id: int, body: UpdateVisitBody) -> None:
    """Update visit and replace all persons and items."""
    if not body.persons_amil:
        raise ValueError('Visit harus memiliki minimal satu orang dari BPZIS')
    if not body.persons_mustahiq:
        raise ValueError('Visit harus memiliki minimal satu orang dari mustahiq')
    if not body.purposes:
        raise ValueError('Visit harus memiliki minimal satu tujuan')
    if not body.results:
        raise ValueError('Visit harus memiliki minimal satu hasil')
    if not body.followups:
        raise ValueError('Visit harus memiliki minimal satu tindak lanjut')

    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Check visit exists
            existing = await conn.fetchrow(
                "SELECT visitid FROM program.visit WHERE visitid = $1 AND visittype = 'P'",
                visit_id,
            )
            if not existing:
                raise ValueError('Visit tidak ditemukan')

            # Update visit
            await conn.execute(
                """
                UPDATE program.visit SET
                    visitdate = $2,
                    visitlocation = $3,
                    visitaddress = $4,
                    visitbegintime = $5,
                    visitendtime = $6,
                    mustahiqid = $7,
                    mustahiqproductid = $8
                WHERE visitid = $1
                """,
                visit_id,
                _Date.fromisoformat(body.visit_date),
                body.visit_location,
                body.visit_address,
                body.visit_begin_time,
                body.visit_end_time,
                body.mustahiq_id,
                body.mustahiq_product_id,
            )

            # Delete old persons and items
            await conn.execute("DELETE FROM program.visitperson WHERE visitid = $1", visit_id)
            await conn.execute("DELETE FROM program.visititem WHERE visitid = $1", visit_id)

            # Insert new persons (amil)
            for person in body.persons_amil:
                person_id = await conn.fetchval("SELECT nextval('program.seq_visitperson')")
                await conn.execute(
                    """
                    INSERT INTO program.visitperson (
                        visitpersonid, visitid, visitpersonname, visitpersonposition, visitpersontype
                    ) VALUES ($1, $2, $3, $4, 'A')
                    """,
                    person_id,
                    visit_id,
                    person.visit_person_name,
                    person.visit_person_position,
                )

            # Insert new persons (mustahiq)
            for person in body.persons_mustahiq:
                person_id = await conn.fetchval("SELECT nextval('program.seq_visitperson')")
                await conn.execute(
                    """
                    INSERT INTO program.visitperson (
                        visitpersonid, visitid, visitpersonname, visitpersonposition, visitpersontype
                    ) VALUES ($1, $2, $3, $4, 'S')
                    """,
                    person_id,
                    visit_id,
                    person.visit_person_name,
                    person.visit_person_position,
                )

            # Insert new items (purposes)
            for item in body.purposes:
                item_id = await conn.fetchval("SELECT nextval('program.seq_visititem')")
                await conn.execute(
                    """
                    INSERT INTO program.visititem (
                        visititemid, visitid, visititemtype, visititemannotation
                    ) VALUES ($1, $2, 'P', $3)
                    """,
                    item_id,
                    visit_id,
                    item.visit_item_annotation,
                )

            # Insert new items (results)
            for item in body.results:
                item_id = await conn.fetchval("SELECT nextval('program.seq_visititem')")
                await conn.execute(
                    """
                    INSERT INTO program.visititem (
                        visititemid, visitid, visititemtype, visititemannotation
                    ) VALUES ($1, $2, 'R', $3)
                    """,
                    item_id,
                    visit_id,
                    item.visit_item_annotation,
                )

            # Insert new items (followups)
            for item in body.followups:
                item_id = await conn.fetchval("SELECT nextval('program.seq_visititem')")
                await conn.execute(
                    """
                    INSERT INTO program.visititem (
                        visititemid, visitid, visititemtype, visititemannotation
                    ) VALUES ($1, $2, 'F', $3)
                    """,
                    item_id,
                    visit_id,
                    item.visit_item_annotation,
                )


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_visit(visit_id: int) -> None:
    """Delete visit and cascade delete persons and items."""
    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            # Check visit exists
            existing = await conn.fetchrow(
                "SELECT visitid FROM program.visit WHERE visitid = $1 AND visittype = 'P'",
                visit_id,
            )
            if not existing:
                raise ValueError('Visit tidak ditemukan')

            # Delete cascade
            await conn.execute("DELETE FROM program.visititem WHERE visitid = $1", visit_id)
            await conn.execute("DELETE FROM program.visitperson WHERE visitid = $1", visit_id)
            await conn.execute("DELETE FROM program.visit WHERE visitid = $1", visit_id)

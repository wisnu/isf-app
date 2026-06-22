from __future__ import annotations

from app.modules.distribution.partner.schema import (
    CreateUpdatePartnerBody,
    PartnerDetail,
    PartnerList,
    PartnerRow,
    Pagination,
)
from app.shared.db import fetch_all, fetch_one, get_pool


def _build_search_where(search: str | None) -> tuple[str, list]:
    conds: list[str] = []
    params: list = []

    if search and search.strip():
        p = f'%{search.strip().lower()}%'
        params.append(p)
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(c.customername, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(c.addressstreet, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(c.phonenumber, \'\')) LIKE ${idx})'
        )

    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''
    return where, params


async def list_partners(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> PartnerList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_search_where(search)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM program.partner p
        JOIN program.customer c ON c.customerid = p.customerid
        {where}
        """,
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    lp = len(params) + 1
    op = len(params) + 2
    rows = await fetch_all(
        f"""
        SELECT
            p.partnerid,
            c.customername  AS name,
            c.addressstreet AS address,
            c.phonenumber   AS phone_number,
            c.customerstatus AS status
        FROM program.partner p
        JOIN program.customer c ON c.customerid = p.customerid
        {where}
        ORDER BY c.customername
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return PartnerList(
        rows=[
            PartnerRow(
                partner_id=r['partnerid'],
                name=r['name'],
                address=r['address'],
                phone_number=r['phone_number'],
                status=r['status'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


async def get_partner(partner_id: int) -> PartnerDetail | None:
    row = await fetch_one(
        """
        SELECT
            p.partnerid,
            c.customername        AS name,
            c.addressstreet       AS address,
            c.addresskelurahan    AS address_kelurahan,
            c.addresskecamatan    AS address_kecamatan,
            c.addresscity         AS address_city,
            c.phonenumber         AS phone_number,
            c.email               AS email,
            p.partnercpname       AS cp_name,
            p.partnercpaddress    AS cp_address,
            p.partnercpmobilephone AS cp_mobile_phone,
            p.partnercpemail      AS cp_email,
            c.customerstatus      AS status
        FROM program.partner p
        JOIN program.customer c ON c.customerid = p.customerid
        WHERE p.partnerid = $1
        LIMIT 1
        """,
        partner_id,
    )
    if not row:
        return None
    return PartnerDetail(
        partner_id=row['partnerid'],
        name=row['name'],
        address=row['address'],
        address_kelurahan=row['address_kelurahan'],
        address_kecamatan=row['address_kecamatan'],
        address_city=row['address_city'],
        phone_number=row['phone_number'],
        email=row['email'],
        cp_name=row['cp_name'],
        cp_address=row['cp_address'],
        cp_mobile_phone=row['cp_mobile_phone'],
        cp_email=row['cp_email'],
        status=row['status'],
    )


async def create_partner(body: CreateUpdatePartnerBody) -> int:
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            customer_id = await conn.fetchval("SELECT nextval('program.seq_customer')")
            await conn.execute(
                """
                INSERT INTO program.customer
                    (customerid, customername, addressstreet, addresskelurahan, addresskecamatan,
                     addresscity, phonenumber, email, customertype, customerstatus)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'PT', 'A')
                """,
                customer_id,
                body.name,
                body.address or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.address_city or '',
                body.phone_number or '',
                body.email or '',
            )
            partner_id = await conn.fetchval("SELECT nextval('program.seq_partner')")
            await conn.execute(
                """
                INSERT INTO program.partner
                    (partnerid, customerid, partnername, partnercpname, partnercpaddress,
                     partnercpmobilephone, partnercpemail)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                partner_id,
                customer_id,
                body.name,
                body.cp_name or '',
                body.cp_address or '',
                body.cp_mobile_phone or '',
                body.cp_email or '',
            )
            return partner_id


async def update_partner(partner_id: int, body: CreateUpdatePartnerBody) -> None:
    row = await fetch_one(
        'SELECT customerid FROM program.partner WHERE partnerid = $1',
        partner_id,
    )
    if not row:
        raise ValueError('Mitra tidak ditemukan')

    customer_id = row['customerid']
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE program.customer SET
                    customername     = $1,
                    addressstreet    = $2,
                    addresskelurahan = $3,
                    addresskecamatan = $4,
                    addresscity      = $5,
                    phonenumber      = $6,
                    email            = $7
                WHERE customerid = $8
                """,
                body.name,
                body.address or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.address_city or '',
                body.phone_number or '',
                body.email or '',
                customer_id,
            )
            await conn.execute(
                """
                UPDATE program.partner SET
                    partnername           = $1,
                    partnercpname         = $2,
                    partnercpaddress      = $3,
                    partnercpmobilephone  = $4,
                    partnercpemail        = $5
                WHERE partnerid = $6
                """,
                body.name,
                body.cp_name or '',
                body.cp_address or '',
                body.cp_mobile_phone or '',
                body.cp_email or '',
                partner_id,
            )


async def delete_partner(partner_id: int) -> None:
    row = await fetch_one(
        'SELECT customerid FROM program.partner WHERE partnerid = $1',
        partner_id,
    )
    if not row:
        raise ValueError('Mitra tidak ditemukan')

    customer_id = row['customerid']
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute('DELETE FROM program.partner WHERE partnerid = $1', partner_id)
            await conn.execute('DELETE FROM program.customer WHERE customerid = $1', customer_id)

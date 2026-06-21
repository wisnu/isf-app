from __future__ import annotations

from app.modules.distribution.mustahiq.schema import (
    BankAccountDetail,
    BankLookupItem,
    MustahiqCorporateDetail,
    MustahiqList,
    MustahiqPersonalDetail,
    MustahiqRow,
    Pagination,
    ProvinceLookupItem,
    CreateUpdateCorporateBody,
    CreateUpdatePersonalBody,
)
from app.shared.db import fetch_all, fetch_one, get_pool


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_date(val) -> str | None:
    if val is None:
        return None
    try:
        return val.strftime('%Y-%m-%d')
    except AttributeError:
        s = str(val)
        return s[:10] if len(s) >= 10 else s


def _build_search_where(mustahiq_type: str, search: str | None) -> tuple[str, list]:
    conds = ['m.mustahiqtype = $1']
    params: list = [mustahiq_type]

    if search and search.strip():
        p = f'%{search.strip().lower()}%'
        params.append(p)
        idx = len(params)
        conds.append(
            f'(LOWER(COALESCE(c.customername, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(c.customerno, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(c.addressstreet, \'\')) LIKE ${idx}'
            f' OR LOWER(COALESCE(c.phonenumber, \'\')) LIKE ${idx})'
        )

    return 'WHERE ' + ' AND '.join(conds), params


# ── Bank accounts ─────────────────────────────────────────────────────────────

async def _get_bank_accounts(mustahiq_id: int) -> list[BankAccountDetail]:
    rows = await fetch_all(
        """
        SELECT
            ba.bankaccountid,
            ba.bankaccountno,
            ba.bankaccountname,
            ba.bankcode,
            ba.isdefault
        FROM program.mustahiqbankaccount mba
        JOIN program.bankaccountlist ba ON ba.bankaccountid = mba.bankaccountid
        WHERE mba.mustahiqid = $1
        ORDER BY ba.bankaccountid
        """,
        mustahiq_id,
    )
    return [
        BankAccountDetail(
            bank_account_id=r['bankaccountid'],
            account_no=r['bankaccountno'],
            account_name=r['bankaccountname'],
            bank_code=r['bankcode'],
            is_default=r['isdefault'],
        )
        for r in rows
    ]


async def _replace_bank_accounts(conn, mustahiq_id: int, bank_accounts: list) -> None:
    existing = await conn.fetch(
        'SELECT bankaccountid FROM program.mustahiqbankaccount WHERE mustahiqid = $1',
        mustahiq_id,
    )
    old_ids = [r['bankaccountid'] for r in existing]

    if old_ids:
        await conn.execute(
            'DELETE FROM program.mustahiqbankaccount WHERE mustahiqid = $1',
            mustahiq_id,
        )
        await conn.execute(
            'DELETE FROM program.bankaccountlist WHERE bankaccountid = ANY($1)',
            old_ids,
        )

    for acc in bank_accounts:
        ba_id = await conn.fetchval("SELECT nextval('program.seq_bankaccountlist')")
        await conn.execute(
            """
            INSERT INTO program.bankaccountlist
                (bankaccountid, bankaccountno, bankaccountname, bankcode, isdefault, bankaccountlisttype)
            VALUES ($1, $2, $3, $4, $5, 'M')
            """,
            ba_id,
            acc.account_no or '',
            acc.account_name or '',
            acc.bank_code or '',
            acc.is_default or 'F',
        )
        await conn.execute(
            'INSERT INTO program.mustahiqbankaccount (bankaccountid, mustahiqid) VALUES ($1, $2)',
            ba_id,
            mustahiq_id,
        )


# ── List ──────────────────────────────────────────────────────────────────────

async def list_corporate(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> MustahiqList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_search_where('MC', search)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(DISTINCT m.mustahiqid) AS INTEGER) AS c
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        """,
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    lp = len(params) + 1
    op = len(params) + 2
    page_rows = await fetch_all(
        f"""
        SELECT DISTINCT ON (m.mustahiqid)
            m.mustahiqid,
            c.customerno   AS no_mustahiq,
            c.customername AS name,
            c.addressstreet AS address,
            c.phonenumber  AS phone_number,
            c.customerstatus AS status
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        ORDER BY m.mustahiqid
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return MustahiqList(
        rows=[
            MustahiqRow(
                mustahiq_id=r['mustahiqid'],
                no_mustahiq=r['no_mustahiq'],
                name=r['name'],
                address=r['address'],
                phone_number=r['phone_number'],
                status=r['status'],
            )
            for r in page_rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


async def list_personal(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> MustahiqList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_search_where('MP', search)

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(DISTINCT m.mustahiqid) AS INTEGER) AS c
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        """,
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    lp = len(params) + 1
    op = len(params) + 2
    page_rows = await fetch_all(
        f"""
        SELECT DISTINCT ON (m.mustahiqid)
            m.mustahiqid,
            c.customerno   AS no_mustahiq,
            c.customername AS name,
            c.addressstreet AS address,
            c.phonenumber  AS phone_number,
            c.customerstatus AS status
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        {where}
        ORDER BY m.mustahiqid
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return MustahiqList(
        rows=[
            MustahiqRow(
                mustahiq_id=r['mustahiqid'],
                no_mustahiq=r['no_mustahiq'],
                name=r['name'],
                address=r['address'],
                phone_number=r['phone_number'],
                status=r['status'],
            )
            for r in page_rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_corporate(mustahiq_id: int) -> MustahiqCorporateDetail | None:
    row = await fetch_one(
        """
        SELECT
            m.mustahiqid,
            c.customerno          AS no_mustahiq,
            c.customername        AS name,
            c.addressstreet       AS address,
            c.addresskelurahan    AS address_kelurahan,
            c.addresskecamatan    AS address_kecamatan,
            c.idpropinsi          AS province_id,
            c.addresspostalcode   AS postal_code,
            m.mustahiqreferenceby AS reference_by,
            c.phonenumber         AS phone_number,
            c.customerstatus      AS status,
            COALESCE(cc.cpname,          mc.cpname)          AS cp_name,
            COALESCE(cc.cpphonenumber,   mc.cpphonenumber)   AS cp_phone_number,
            COALESCE(cc.cpmobilenumber,  mc.cpmobilenumber)  AS cp_mobile_number
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        LEFT JOIN program.customercorporate cc ON cc.customerid = m.customerid
        LEFT JOIN program.mustahiqcorporate mc ON mc.mustahiqid = m.mustahiqid
        WHERE m.mustahiqid = $1 AND m.mustahiqtype = 'MC'
        LIMIT 1
        """,
        mustahiq_id,
    )
    if not row:
        return None

    bank_accounts = await _get_bank_accounts(mustahiq_id)
    return MustahiqCorporateDetail(
        mustahiq_id=row['mustahiqid'],
        no_mustahiq=row['no_mustahiq'],
        name=row['name'],
        address=row['address'],
        address_kelurahan=row['address_kelurahan'],
        address_kecamatan=row['address_kecamatan'],
        province_id=row['province_id'],
        postal_code=row['postal_code'],
        reference_by=row['reference_by'],
        phone_number=row['phone_number'],
        cp_name=row['cp_name'],
        cp_phone_number=row['cp_phone_number'],
        cp_mobile_number=row['cp_mobile_number'],
        status=row['status'],
        bank_accounts=bank_accounts,
    )


async def get_personal(mustahiq_id: int) -> MustahiqPersonalDetail | None:
    row = await fetch_one(
        """
        SELECT
            m.mustahiqid,
            c.customerno          AS no_mustahiq,
            c.customername        AS name,
            c.addressstreet       AS address,
            c.addresskelurahan    AS address_kelurahan,
            c.addresskecamatan    AS address_kecamatan,
            c.idpropinsi          AS province_id,
            c.addresspostalcode   AS postal_code,
            m.mustahiqreferenceby AS reference_by,
            c.phonenumber         AS phone_number,
            c.customerstatus      AS status,
            m.ashnaf              AS ashnaf,
            cp.gender             AS gender,
            cp.birthplace         AS birth_place,
            cp.birthdate          AS birth_date,
            cp.identitynumber     AS identity_number,
            cp.identitytype       AS identity_type,
            cp.religion           AS religion,
            cp.totalfamily        AS total_family,
            cp.formaleducation    AS formal_education,
            cp.marital            AS marital,
            cp.worksector         AS work_sector,
            mp.mustahiqincome     AS income
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        LEFT JOIN program.customerpersonal cp ON cp.customerid = m.customerid
        LEFT JOIN program.mustahiqpersonal mp ON mp.mustahiqid = m.mustahiqid
        WHERE m.mustahiqid = $1 AND m.mustahiqtype = 'MP'
        LIMIT 1
        """,
        mustahiq_id,
    )
    if not row:
        return None

    bank_accounts = await _get_bank_accounts(mustahiq_id)
    return MustahiqPersonalDetail(
        mustahiq_id=row['mustahiqid'],
        no_mustahiq=row['no_mustahiq'],
        name=row['name'],
        address=row['address'],
        address_kelurahan=row['address_kelurahan'],
        address_kecamatan=row['address_kecamatan'],
        province_id=row['province_id'],
        postal_code=row['postal_code'],
        reference_by=row['reference_by'],
        phone_number=row['phone_number'],
        status=row['status'],
        ashnaf=row['ashnaf'],
        gender=row['gender'],
        birth_place=row['birth_place'],
        birth_date=_parse_date(row['birth_date']),
        identity_number=row['identity_number'],
        identity_type=row['identity_type'],
        religion=row['religion'],
        total_family=row['total_family'],
        formal_education=row['formal_education'],
        income=row['income'],
        marital=row['marital'],
        work_sector=row['work_sector'],
        bank_accounts=bank_accounts,
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_corporate(body: CreateUpdateCorporateBody) -> int:
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            customer_id = await conn.fetchval("SELECT nextval('program.seq_customer')")
            await conn.execute(
                """
                INSERT INTO program.customer
                    (customerid, customername, addressstreet, addresskelurahan, addresskecamatan,
                     idpropinsi, addresspostalcode, phonenumber, customertype, customerstatus)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'CC', 'A')
                """,
                customer_id,
                body.name,
                body.address or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.province_id,
                body.postal_code or '',
                body.phone_number or '',
            )
            await conn.execute(
                """
                INSERT INTO program.customercorporate (customerid, cpname, cpphonenumber, cpmobilenumber)
                VALUES ($1, $2, $3, $4)
                """,
                customer_id,
                body.cp_name or '',
                body.cp_phone_number or '',
                body.cp_mobile_number or '',
            )

            mustahiq_id = await conn.fetchval("SELECT nextval('program.seq_mustahiq')")
            await conn.execute(
                """
                INSERT INTO program.mustahiq (mustahiqid, mustahiqtype, customerid, mustahiqreferenceby)
                VALUES ($1, 'MC', $2, $3)
                """,
                mustahiq_id,
                customer_id,
                body.reference_by or '',
            )
            await conn.execute(
                """
                INSERT INTO program.mustahiqcorporate (mustahiqid, cpname, cpphonenumber, cpmobilenumber)
                VALUES ($1, $2, $3, $4)
                """,
                mustahiq_id,
                body.cp_name or '',
                body.cp_phone_number or '',
                body.cp_mobile_number or '',
            )

            await _replace_bank_accounts(conn, mustahiq_id, body.bank_accounts)
            return mustahiq_id


async def create_personal(body: CreateUpdatePersonalBody) -> int:
    from datetime import date as date_type
    birth_date = None
    if body.birth_date:
        try:
            birth_date = date_type.fromisoformat(body.birth_date[:10])
        except (ValueError, TypeError):
            birth_date = None

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            customer_id = await conn.fetchval("SELECT nextval('program.seq_customer')")
            await conn.execute(
                """
                INSERT INTO program.customer
                    (customerid, customername, addressstreet, addresskelurahan, addresskecamatan,
                     idpropinsi, addresspostalcode, phonenumber, customertype, customerstatus)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'CP', 'A')
                """,
                customer_id,
                body.name,
                body.address or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.province_id,
                body.postal_code or '',
                body.phone_number or '',
            )
            await conn.execute(
                """
                INSERT INTO program.customerpersonal
                    (customerid, gender, birthplace, birthdate, identitynumber, identitytype,
                     religion, totalfamily, formaleducation, marital, worksector)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                """,
                customer_id,
                body.gender or '',
                body.birth_place or '',
                birth_date,
                body.identity_number or '',
                body.identity_type or '',
                body.religion,
                body.total_family,
                body.formal_education or '',
                body.marital or '',
                body.work_sector or '',
            )

            mustahiq_id = await conn.fetchval("SELECT nextval('program.seq_mustahiq')")
            await conn.execute(
                """
                INSERT INTO program.mustahiq
                    (mustahiqid, mustahiqtype, customerid, ashnaf, mustahiqreferenceby)
                VALUES ($1, 'MP', $2, $3, $4)
                """,
                mustahiq_id,
                customer_id,
                body.ashnaf or '',
                body.reference_by or '',
            )
            await conn.execute(
                """
                INSERT INTO program.mustahiqpersonal
                    (mustahiqid, mustahiqgender, mustahiqbirthplace, mustahiqbirthdate,
                     mustahiqidentitynumber, mustahiqidentitytype, mustahiqreligion,
                     mustahiqtotalfamily, mustahiqformaleducation, mustahiqmarital,
                     mustahiqworksector, mustahiqashnaf, mustahiqincome)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """,
                mustahiq_id,
                body.gender or '',
                body.birth_place or '',
                birth_date,
                body.identity_number or '',
                body.identity_type or '',
                body.religion,
                body.total_family,
                body.formal_education or '',
                body.marital or '',
                body.work_sector or '',
                body.ashnaf or '',
                body.income,
            )

            await _replace_bank_accounts(conn, mustahiq_id, body.bank_accounts)
            return mustahiq_id


# ── Update ────────────────────────────────────────────────────────────────────

async def update_corporate(mustahiq_id: int, body: CreateUpdateCorporateBody) -> None:
    row = await fetch_one(
        "SELECT customerid FROM program.mustahiq WHERE mustahiqid = $1 AND mustahiqtype = 'MC'",
        mustahiq_id,
    )
    if not row:
        raise ValueError('Mustahiq Lembaga tidak ditemukan')

    customer_id = row['customerid']
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE program.customer SET
                    customername       = $1,
                    addressstreet      = $2,
                    addresskelurahan   = $3,
                    addresskecamatan   = $4,
                    idpropinsi         = $5,
                    addresspostalcode  = $6,
                    phonenumber        = $7
                WHERE customerid = $8
                """,
                body.name,
                body.address or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.province_id,
                body.postal_code or '',
                body.phone_number or '',
                customer_id,
            )
            await conn.execute(
                """
                INSERT INTO program.customercorporate (customerid, cpname, cpphonenumber, cpmobilenumber)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (customerid) DO UPDATE SET
                    cpname          = EXCLUDED.cpname,
                    cpphonenumber   = EXCLUDED.cpphonenumber,
                    cpmobilenumber  = EXCLUDED.cpmobilenumber
                """,
                customer_id,
                body.cp_name or '',
                body.cp_phone_number or '',
                body.cp_mobile_number or '',
            )
            await conn.execute(
                """
                UPDATE program.mustahiq SET mustahiqreferenceby = $1 WHERE mustahiqid = $2
                """,
                body.reference_by or '',
                mustahiq_id,
            )
            await conn.execute(
                """
                INSERT INTO program.mustahiqcorporate (mustahiqid, cpname, cpphonenumber, cpmobilenumber)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (mustahiqid) DO UPDATE SET
                    cpname         = EXCLUDED.cpname,
                    cpphonenumber  = EXCLUDED.cpphonenumber,
                    cpmobilenumber = EXCLUDED.cpmobilenumber
                """,
                mustahiq_id,
                body.cp_name or '',
                body.cp_phone_number or '',
                body.cp_mobile_number or '',
            )
            await _replace_bank_accounts(conn, mustahiq_id, body.bank_accounts)


async def update_personal(mustahiq_id: int, body: CreateUpdatePersonalBody) -> None:
    from datetime import date as date_type
    row = await fetch_one(
        "SELECT customerid FROM program.mustahiq WHERE mustahiqid = $1 AND mustahiqtype = 'MP'",
        mustahiq_id,
    )
    if not row:
        raise ValueError('Mustahiq Individu tidak ditemukan')

    customer_id = row['customerid']
    birth_date = None
    if body.birth_date:
        try:
            birth_date = date_type.fromisoformat(body.birth_date[:10])
        except (ValueError, TypeError):
            birth_date = None

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE program.customer SET
                    customername       = $1,
                    addressstreet      = $2,
                    addresskelurahan   = $3,
                    addresskecamatan   = $4,
                    idpropinsi         = $5,
                    addresspostalcode  = $6,
                    phonenumber        = $7
                WHERE customerid = $8
                """,
                body.name,
                body.address or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.province_id,
                body.postal_code or '',
                body.phone_number or '',
                customer_id,
            )
            await conn.execute(
                """
                INSERT INTO program.customerpersonal
                    (customerid, gender, birthplace, birthdate, identitynumber, identitytype,
                     religion, totalfamily, formaleducation, marital, worksector)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT (customerid) DO UPDATE SET
                    gender          = EXCLUDED.gender,
                    birthplace      = EXCLUDED.birthplace,
                    birthdate       = EXCLUDED.birthdate,
                    identitynumber  = EXCLUDED.identitynumber,
                    identitytype    = EXCLUDED.identitytype,
                    religion        = EXCLUDED.religion,
                    totalfamily     = EXCLUDED.totalfamily,
                    formaleducation = EXCLUDED.formaleducation,
                    marital         = EXCLUDED.marital,
                    worksector      = EXCLUDED.worksector
                """,
                customer_id,
                body.gender or '',
                body.birth_place or '',
                birth_date,
                body.identity_number or '',
                body.identity_type or '',
                body.religion,
                body.total_family,
                body.formal_education or '',
                body.marital or '',
                body.work_sector or '',
            )
            await conn.execute(
                "UPDATE program.mustahiq SET ashnaf = $1, mustahiqreferenceby = $2 WHERE mustahiqid = $3",
                body.ashnaf or '',
                body.reference_by or '',
                mustahiq_id,
            )
            await conn.execute(
                """
                INSERT INTO program.mustahiqpersonal
                    (mustahiqid, mustahiqgender, mustahiqbirthplace, mustahiqbirthdate,
                     mustahiqidentitynumber, mustahiqidentitytype, mustahiqreligion,
                     mustahiqtotalfamily, mustahiqformaleducation, mustahiqmarital,
                     mustahiqworksector, mustahiqashnaf, mustahiqincome)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                ON CONFLICT (mustahiqid) DO UPDATE SET
                    mustahiqgender          = EXCLUDED.mustahiqgender,
                    mustahiqbirthplace      = EXCLUDED.mustahiqbirthplace,
                    mustahiqbirthdate       = EXCLUDED.mustahiqbirthdate,
                    mustahiqidentitynumber  = EXCLUDED.mustahiqidentitynumber,
                    mustahiqidentitytype    = EXCLUDED.mustahiqidentitytype,
                    mustahiqreligion        = EXCLUDED.mustahiqreligion,
                    mustahiqtotalfamily     = EXCLUDED.mustahiqtotalfamily,
                    mustahiqformaleducation = EXCLUDED.mustahiqformaleducation,
                    mustahiqmarital         = EXCLUDED.mustahiqmarital,
                    mustahiqworksector      = EXCLUDED.mustahiqworksector,
                    mustahiqashnaf          = EXCLUDED.mustahiqashnaf,
                    mustahiqincome          = EXCLUDED.mustahiqincome
                """,
                mustahiq_id,
                body.gender or '',
                body.birth_place or '',
                birth_date,
                body.identity_number or '',
                body.identity_type or '',
                body.religion,
                body.total_family,
                body.formal_education or '',
                body.marital or '',
                body.work_sector or '',
                body.ashnaf or '',
                body.income,
            )
            await _replace_bank_accounts(conn, mustahiq_id, body.bank_accounts)


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_mustahiq(mustahiq_id: int, mustahiq_type: str) -> None:
    row = await fetch_one(
        'SELECT customerid FROM program.mustahiq WHERE mustahiqid = $1 AND mustahiqtype = $2',
        mustahiq_id,
        mustahiq_type,
    )
    if not row:
        raise ValueError('Mustahiq tidak ditemukan')

    customer_id = row['customerid']
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            existing_ba = await conn.fetch(
                'SELECT bankaccountid FROM program.mustahiqbankaccount WHERE mustahiqid = $1',
                mustahiq_id,
            )
            old_ba_ids = [r['bankaccountid'] for r in existing_ba]

            if old_ba_ids:
                await conn.execute(
                    'DELETE FROM program.mustahiqbankaccount WHERE mustahiqid = $1',
                    mustahiq_id,
                )
                await conn.execute(
                    'DELETE FROM program.bankaccountlist WHERE bankaccountid = ANY($1)',
                    old_ba_ids,
                )

            if mustahiq_type == 'MC':
                await conn.execute(
                    'DELETE FROM program.mustahiqcorporate WHERE mustahiqid = $1',
                    mustahiq_id,
                )
            else:
                await conn.execute(
                    'DELETE FROM program.mustahiqpersonal WHERE mustahiqid = $1',
                    mustahiq_id,
                )

            await conn.execute(
                'DELETE FROM program.mustahiq WHERE mustahiqid = $1',
                mustahiq_id,
            )

            if mustahiq_type == 'MC':
                await conn.execute(
                    'DELETE FROM program.customercorporate WHERE customerid = $1',
                    customer_id,
                )
            else:
                await conn.execute(
                    'DELETE FROM program.customerpersonal WHERE customerid = $1',
                    customer_id,
                )

            await conn.execute(
                'DELETE FROM program.customer WHERE customerid = $1',
                customer_id,
            )


# ── Toggle status ─────────────────────────────────────────────────────────────

async def toggle_status(mustahiq_id: int, mustahiq_type: str, new_status: str) -> None:
    if new_status not in ('A', 'N'):
        raise ValueError("Status harus 'A' (Aktif) atau 'N' (NonAktif)")

    row = await fetch_one(
        """
        SELECT c.customerstatus, c.customerid
        FROM program.mustahiq m
        JOIN program.customer c ON c.customerid = m.customerid
        WHERE m.mustahiqid = $1 AND m.mustahiqtype = $2
        LIMIT 1
        """,
        mustahiq_id,
        mustahiq_type,
    )
    if not row:
        raise ValueError('Mustahiq tidak ditemukan')

    current = (row['customerstatus'] or '').strip()
    if current == new_status:
        label = 'aktif' if new_status == 'A' else 'non-aktif'
        raise ValueError(f'Mustahiq sudah berstatus {label}')

    customer_id = row['customerid']
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                'UPDATE program.customer SET customerstatus = $1 WHERE customerid = $2',
                new_status,
                customer_id,
            )


# ── Lookups ───────────────────────────────────────────────────────────────────

async def lookup_provinces() -> list[ProvinceLookupItem]:
    rows = await fetch_all(
        'SELECT idpropinsi, propinsi FROM transaction.propinsi ORDER BY propinsi'
    )
    return [
        ProvinceLookupItem(province_id=r['idpropinsi'], province_name=r['propinsi'])
        for r in rows
    ]


async def lookup_banks() -> list[BankLookupItem]:
    rows = await fetch_all(
        'SELECT bankcode, bankshortname, bankname FROM transaction.bank ORDER BY bankshortname'
    )
    return [
        BankLookupItem(
            bank_code=r['bankcode'],
            bank_short_name=r['bankshortname'],
            bank_name=r['bankname'],
        )
        for r in rows
    ]

from __future__ import annotations

from app.modules.fundraising.donors.schema import (
    BankAccountItem,
    CommitmentItem,
    CorporateDonorDetail,
    CreateUpdateCorporateBody,
    CreateUpdateIndividualBody,
    DonorList,
    DonorRow,
    FieldOfWorkLookupItem,
    CountryLookupItem,
    IndividualDonorDetail,
    MarketerLookupItem,
    Pagination,
    ProvinceLookupItem,
    WorkAreaLookupItem,
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


_SEQ_MAP = {
    'DONOR':           "SELECT nextval('fund.seq_donor')",
    'BANKACCOUNTLIST': "SELECT nextval('fund.seq_bankaccountlist')",
    'DONORCOMMITMENT': "SELECT nextval('fund.seq_donorcommitment')",
}


async def _next_id_gen(conn, id_code: str, table: str = '', pk_col: str = '') -> int:
    if id_code in _SEQ_MAP:
        return await conn.fetchval(_SEQ_MAP[id_code])
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


async def _next_donor_no(conn, prefix: str) -> str:
    row = await conn.fetchrow(
        "SELECT last_id FROM fund.custom_idgen WHERE idname='DONOR' AND idcode=$1 FOR UPDATE",
        prefix,
    )
    if row:
        new_id = row['last_id'] + 1
        await conn.execute(
            "UPDATE fund.custom_idgen SET last_id=$1 WHERE idname='DONOR' AND idcode=$2",
            new_id, prefix,
        )
    else:
        current_max = await conn.fetchval(
            "SELECT COALESCE(MAX(CAST(SUBSTRING(donorno, 2) AS INTEGER)), 0) "
            "FROM fund.donor WHERE donorno LIKE $1",
            prefix + '%',
        )
        new_id = current_max + 1
        await conn.execute(
            "INSERT INTO fund.custom_idgen(idname, idcode, last_id, locked) VALUES('DONOR',$1,$2,'F')",
            prefix, new_id,
        )
    return prefix + str(new_id).zfill(7)


async def _get_bank_accounts(donor_id: int) -> list[BankAccountItem]:
    rows = await fetch_all(
        """
        SELECT
            bal.bankaccountid,
            bal.bankaccountno,
            bal.bankaccountname,
            bal.bankcode
        FROM fund.donorbankaccount dba
        JOIN fund.bankaccountlist bal ON bal.bankaccountid = dba.bankaccountid
        WHERE dba.donorid = $1
        ORDER BY bal.bankaccountid
        """,
        donor_id,
    )
    return [
        BankAccountItem(
            bank_account_id=r['bankaccountid'],
            bank_account_no=r['bankaccountno'],
            bank_account_name=r['bankaccountname'],
            bank_code=r['bankcode'],
        )
        for r in rows
    ]


async def _get_commitments(donor_id: int) -> list[CommitmentItem]:
    rows = await fetch_all(
        """
        SELECT commitmentid, accountno, commitmentamount
        FROM fund.donorcommitment
        WHERE donorid = $1
        ORDER BY commitmentid
        """,
        donor_id,
    )
    return [
        CommitmentItem(
            commitment_id=r['commitmentid'],
            account_no=r['accountno'],
            commitment_amount=float(r['commitmentamount']) if r['commitmentamount'] else None,
        )
        for r in rows
    ]


async def _replace_bank_accounts(conn, donor_id: int, bank_accounts: list[BankAccountItem]) -> None:
    existing = await conn.fetch(
        'SELECT bankaccountid FROM fund.donorbankaccount WHERE donorid = $1', donor_id
    )
    old_ids = [r['bankaccountid'] for r in existing]
    if old_ids:
        await conn.execute(
            'DELETE FROM fund.donorbankaccount WHERE donorid = $1', donor_id
        )
        await conn.execute(
            'DELETE FROM fund.bankaccountlist WHERE bankaccountid = ANY($1)', old_ids
        )
    for acc in bank_accounts:
        ba_id = await _next_id_gen(conn, 'BANKACCOUNTLIST', 'fund.bankaccountlist', 'bankaccountid')
        await conn.execute(
            """
            INSERT INTO fund.bankaccountlist
                (bankaccountid, bankaccountno, bankaccountname, bankcode, isdefault, bankaccountlisttype)
            VALUES ($1, $2, $3, $4, 'F', 'D')
            """,
            ba_id,
            acc.bank_account_no or '',
            acc.bank_account_name or '',
            acc.bank_code or '',
        )
        await conn.execute(
            'INSERT INTO fund.donorbankaccount (bankaccountid, donorid) VALUES ($1, $2)',
            ba_id, donor_id,
        )


async def _replace_commitments(conn, donor_id: int, commitments: list[CommitmentItem]) -> None:
    await conn.execute('DELETE FROM fund.donorcommitment WHERE donorid = $1', donor_id)
    for c in commitments:
        c_id = await _next_id_gen(conn, 'DONORCOMMITMENT', 'fund.donorcommitment', 'commitmentid')
        await conn.execute(
            """
            INSERT INTO fund.donorcommitment (commitmentid, donorid, accountno, commitmentamount)
            VALUES ($1, $2, $3, $4)
            """,
            c_id, donor_id,
            c.account_no or '',
            c.commitment_amount or 0,
        )


# ── Lookup ────────────────────────────────────────────────────────────────────

async def lookup_provinces() -> list[ProvinceLookupItem]:
    rows = await fetch_all(
        'SELECT idpropinsi, propinsi FROM fund.propinsi ORDER BY propinsi'
    )
    return [ProvinceLookupItem(id_propinsi=r['idpropinsi'], province_name=r['propinsi']) for r in rows]


async def lookup_countries() -> list[CountryLookupItem]:
    rows = await fetch_all(
        'SELECT idnegara, nama_negara FROM fund.negara ORDER BY nama_negara'
    )
    return [CountryLookupItem(id_negara=r['idnegara'], country_name=r['nama_negara']) for r in rows]


async def lookup_marketers() -> list[MarketerLookupItem]:
    rows = await fetch_all(
        "SELECT marketerid, marketercode, marketername FROM fund.marketer ORDER BY marketername"
    )
    return [
        MarketerLookupItem(
            marketer_id=r['marketerid'],
            marketer_code=r['marketercode'],
            marketer_name=r['marketername'],
        )
        for r in rows
    ]


async def lookup_field_of_work() -> list[FieldOfWorkLookupItem]:
    rows = await fetch_all(
        'SELECT fworkid, fworkcode, fworkname, fnpwzcode FROM fund.fieldofwork ORDER BY fworkname'
    )
    return [
        FieldOfWorkLookupItem(
            fwork_id=r['fworkid'],
            fwork_code=r['fworkcode'],
            fwork_name=r['fworkname'],
            fnpwz_code=r['fnpwzcode'],
        )
        for r in rows
    ]


async def lookup_work_areas() -> list[WorkAreaLookupItem]:
    rows = await fetch_all(
        'SELECT workareaid, workareacode, workareaname FROM fund.workarea ORDER BY workareaname'
    )
    return [
        WorkAreaLookupItem(
            work_area_id=r['workareaid'],
            work_area_code=r['workareacode'],
            work_area_name=r['workareaname'],
        )
        for r in rows
    ]


# ── Corporate — List ──────────────────────────────────────────────────────────

async def list_corporate(
    search: str | None = None,
    search_by: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> DonorList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))

    conds: list[str] = []
    params: list = []

    if status and status in ('A', 'N'):
        params.append(status)
        conds.append(f'd.status = ${len(params)}')

    if search and search.strip():
        p = f'%{search.strip().lower()}%'
        params.append(p)
        idx = len(params)
        col_map = {
            'donor_no': 'd.donorno',
            'address': 'd.addressstreet',
            'phone': 'd.phonenumber',
            'npwp': 'd.npwp',
            'corporation': 'cd.corporation',
            'siupp': 'cd.siupp',
            'cp_name': 'cd.cpname',
            'cp_email': 'cd.cpemail',
        }
        if search_by in col_map:
            conds.append(f'LOWER(COALESCE({col_map[search_by]}, \'\')) LIKE ${idx}')
        else:
            conds.append(
                f'(LOWER(COALESCE(d.donorname, \'\')) LIKE ${idx}'
                f' OR LOWER(COALESCE(d.donorno, \'\')) LIKE ${idx}'
                f' OR LOWER(COALESCE(d.phonenumber, \'\')) LIKE ${idx})'
            )

    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM fund.donor d
        JOIN fund.corporatedonor cd ON cd.donorid = d.donorid
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
            d.donorid,
            d.donorno,
            d.donorname,
            CAST(d.joindate AS DATE) AS joindate,
            d.phonenumber,
            d.status
        FROM fund.donor d
        JOIN fund.corporatedonor cd ON cd.donorid = d.donorid
        {where}
        ORDER BY d.donorid DESC
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return DonorList(
        rows=[
            DonorRow(
                donor_id=r['donorid'],
                donor_no=r['donorno'],
                donor_name=r['donorname'],
                join_date=_parse_date(r['joindate']),
                phone_number=r['phonenumber'],
                status=r['status'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


# ── Corporate — Detail ────────────────────────────────────────────────────────

async def get_corporate(donor_id: int) -> CorporateDonorDetail | None:
    row = await fetch_one(
        """
        SELECT
            d.donorid,
            d.donorno,
            d.donorname,
            d.status,
            d.branchcode,
            CAST(d.joindate AS DATE)       AS joindate,
            d.npwp,
            d.npwz,
            d.economicsector,
            d.phonenumber,
            d.fax,
            d.addressstreet,
            d.addresskelurahan,
            d.addresskecamatan,
            d.addresscity,
            d.addresspostalcode,
            d.idpropinsi,
            p.propinsi                     AS province_name,
            d.idnegara,
            n.nama_negara                  AS country_name,
            d.marketerid,
            m.marketercode,
            m.marketername,
            cd.corporation,
            cd.siupp,
            cd.cpname,
            cd.cpemail,
            cd.cpphonenumber,
            cd.cpmobilenumber
        FROM fund.donor d
        JOIN fund.corporatedonor cd ON cd.donorid = d.donorid
        LEFT JOIN fund.propinsi p   ON p.idpropinsi = d.idpropinsi
        LEFT JOIN fund.negara n     ON n.idnegara   = d.idnegara
        LEFT JOIN fund.marketer m   ON m.marketerid = d.marketerid
        WHERE d.donorid = $1
        """,
        donor_id,
    )
    if not row:
        return None

    bank_accounts = await _get_bank_accounts(donor_id)
    commitments = await _get_commitments(donor_id)

    return CorporateDonorDetail(
        donor_id=row['donorid'],
        donor_no=row['donorno'],
        donor_name=row['donorname'],
        corporation=row['corporation'],
        economic_sector=row['economicsector'],
        siupp=row['siupp'],
        join_date=_parse_date(row['joindate']),
        npwp=row['npwp'],
        npwz=row['npwz'],
        status=row['status'],
        branch_code=row['branchcode'],
        marketer_id=row['marketerid'],
        marketer_code=row['marketercode'],
        marketer_name=row['marketername'],
        id_negara=row['idnegara'],
        country_name=row['country_name'],
        id_propinsi=row['idpropinsi'],
        province_name=row['province_name'],
        address_city=row['addresscity'],
        address_postal_code=row['addresspostalcode'],
        address_kecamatan=row['addresskecamatan'],
        address_kelurahan=row['addresskelurahan'],
        address_street=row['addressstreet'],
        phone_number=row['phonenumber'],
        fax=row['fax'],
        cp_name=row['cpname'],
        cp_phone=row['cpphonenumber'],
        cp_mobile=row['cpmobilenumber'],
        cp_email=row['cpemail'],
        bank_accounts=bank_accounts,
        commitments=commitments,
    )


# ── Corporate — Create ────────────────────────────────────────────────────────

async def create_corporate(body: CreateUpdateCorporateBody) -> int:
    from datetime import date as date_type

    join_date = None
    if body.join_date:
        try:
            join_date = date_type.fromisoformat(body.join_date[:10])
        except (ValueError, TypeError):
            join_date = None

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            donor_id = await _next_id_gen(conn, 'DONOR', 'fund.donor', 'donorid')
            donor_no = await _next_donor_no(conn, 'C')

            await conn.execute(
                """
                INSERT INTO fund.donor
                    (donorid, donorno, donorname, status, branchcode, joindate, npwp, npwz,
                     economicsector, phonenumber, fax, addressstreet, addresskelurahan,
                     addresskecamatan, addresscity, addresspostalcode, addressstate,
                     idpropinsi, idnegara, marketerid, donortype)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,'C')
                """,
                donor_id, donor_no,
                body.donor_name.upper(),
                body.status or 'A',
                body.branch_code or '',
                join_date,
                body.npwp or '',
                body.npwz or '',
                body.economic_sector or '',
                body.phone_number or '',
                body.fax or '',
                body.address_street or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.address_city or '',
                body.address_postal_code or '',
                '',
                body.id_propinsi,
                body.id_negara,
                body.marketer_id,
            )
            await conn.execute(
                """
                INSERT INTO fund.corporatedonor
                    (donorid, corporation, siupp, cpname, cpemail, cpphonenumber, cpmobilenumber)
                VALUES ($1,$2,$3,$4,$5,$6,$7)
                """,
                donor_id,
                body.corporation or '',
                body.siupp or '',
                body.cp_name or '',
                body.cp_email or '',
                body.cp_phone or '',
                body.cp_mobile or '',
            )
            await _replace_bank_accounts(conn, donor_id, body.bank_accounts)
            await _replace_commitments(conn, donor_id, body.commitments)
            return donor_id


# ── Corporate — Update ────────────────────────────────────────────────────────

async def update_corporate(donor_id: int, body: CreateUpdateCorporateBody) -> None:
    from datetime import date as date_type

    row = await fetch_one('SELECT donorid FROM fund.donor WHERE donorid=$1', donor_id)
    if not row:
        raise ValueError('Donatur Korporat tidak ditemukan')

    join_date = None
    if body.join_date:
        try:
            join_date = date_type.fromisoformat(body.join_date[:10])
        except (ValueError, TypeError):
            join_date = None

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE fund.donor SET
                    donorname       = $1,
                    status          = $2,
                    joindate        = $3,
                    npwp            = $4,
                    npwz            = $5,
                    economicsector  = $6,
                    phonenumber     = $7,
                    fax             = $8,
                    addressstreet   = $9,
                    addresskelurahan= $10,
                    addresskecamatan= $11,
                    addresscity     = $12,
                    addresspostalcode=$13,
                    idpropinsi      = $14,
                    idnegara        = $15,
                    marketerid      = $16
                WHERE donorid = $17
                """,
                body.donor_name.upper(),
                body.status or 'A',
                join_date,
                body.npwp or '',
                body.npwz or '',
                body.economic_sector or '',
                body.phone_number or '',
                body.fax or '',
                body.address_street or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.address_city or '',
                body.address_postal_code or '',
                body.id_propinsi,
                body.id_negara,
                body.marketer_id,
                donor_id,
            )
            await conn.execute(
                """
                INSERT INTO fund.corporatedonor
                    (donorid, corporation, siupp, cpname, cpemail, cpphonenumber, cpmobilenumber)
                VALUES ($1,$2,$3,$4,$5,$6,$7)
                ON CONFLICT (donorid) DO UPDATE SET
                    corporation    = EXCLUDED.corporation,
                    siupp          = EXCLUDED.siupp,
                    cpname         = EXCLUDED.cpname,
                    cpemail        = EXCLUDED.cpemail,
                    cpphonenumber  = EXCLUDED.cpphonenumber,
                    cpmobilenumber = EXCLUDED.cpmobilenumber
                """,
                donor_id,
                body.corporation or '',
                body.siupp or '',
                body.cp_name or '',
                body.cp_email or '',
                body.cp_phone or '',
                body.cp_mobile or '',
            )
            await _replace_bank_accounts(conn, donor_id, body.bank_accounts)
            await _replace_commitments(conn, donor_id, body.commitments)


# ── Individual — List ─────────────────────────────────────────────────────────

async def list_individual(
    search: str | None = None,
    search_by: str | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> DonorList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))

    conds: list[str] = []
    params: list = []

    if status and status in ('A', 'N'):
        params.append(status)
        conds.append(f'd.status = ${len(params)}')

    if search and search.strip():
        p = f'%{search.strip().lower()}%'
        params.append(p)
        idx = len(params)
        col_map = {
            'donor_no': 'd.donorno',
            'address': 'd.addressstreet',
            'phone': 'd.phonenumber',
            'email': 'id.email',
            'mobile': 'id.mobilephone',
            'identity': 'id.identitynumber',
        }
        if search_by in col_map:
            conds.append(f'LOWER(COALESCE({col_map[search_by]}, \'\')) LIKE ${idx}')
        else:
            conds.append(
                f'(LOWER(COALESCE(d.donorname, \'\')) LIKE ${idx}'
                f' OR LOWER(COALESCE(d.donorno, \'\')) LIKE ${idx}'
                f' OR LOWER(COALESCE(id.mobilephone, \'\')) LIKE ${idx})'
            )

    where = ('WHERE ' + ' AND '.join(conds)) if conds else ''

    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM fund.donor d
        JOIN fund.individualdonor id ON id.donorid = d.donorid
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
            d.donorid,
            d.donorno,
            d.donorname,
            CAST(d.joindate AS DATE) AS joindate,
            d.phonenumber,
            d.status
        FROM fund.donor d
        JOIN fund.individualdonor id ON id.donorid = d.donorid
        {where}
        ORDER BY d.donorid ASC
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0
    return DonorList(
        rows=[
            DonorRow(
                donor_id=r['donorid'],
                donor_no=r['donorno'],
                donor_name=r['donorname'],
                join_date=_parse_date(r['joindate']),
                phone_number=r['phonenumber'],
                status=r['status'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


# ── Individual — Detail ───────────────────────────────────────────────────────

async def get_individual(donor_id: int) -> IndividualDonorDetail | None:
    row = await fetch_one(
        """
        SELECT
            d.donorid,
            d.donorno,
            d.donorname,
            d.status,
            d.branchcode,
            CAST(d.joindate AS DATE)       AS joindate,
            d.npwp,
            d.npwz,
            d.economicsector,
            d.phonenumber,
            d.fax,
            d.addressstreet,
            d.addresskelurahan,
            d.addresskecamatan,
            d.addresscity,
            d.addresspostalcode,
            d.idpropinsi,
            p.propinsi                     AS province_name,
            d.idnegara,
            n.nama_negara                  AS country_name,
            d.marketerid,
            m.marketercode,
            m.marketername,
            id.gender,
            CAST(id.birthdate AS DATE)     AS birthdate,
            id.birthplace,
            id.identitytype,
            id.identitynumber,
            id.religion,
            id.maritalstate,
            id.email,
            id.mobilephone,
            id.statusrumah,
            id.isinternalemployee,
            id.workidentitynumber,
            id.workareaid,
            wa.workareacode,
            wa.workareaname,
            id.workareaidinitial,
            wai.workareacode                AS work_area_initial_code,
            wai.workareaname                AS work_area_initial_name,
            id.workunit,
            id.workposition,
            id.workbusinessarea,
            id.fworkid,
            fw.fworkcode,
            fw.fworkname,
            id.donorgroup,
            id.idpropinsioffice,
            po.propinsi                    AS office_province_name,
            id.officeaddress,
            id.officekelurahan,
            id.officekecamatan,
            id.officecity,
            id.officephonenumber,
            id.officepostalcode,
            id.corporatename,
            id.jobposition,
            id.couplename,
            id.child
        FROM fund.donor d
        JOIN fund.individualdonor id ON id.donorid = d.donorid
        LEFT JOIN fund.propinsi p    ON p.idpropinsi  = d.idpropinsi
        LEFT JOIN fund.negara n      ON n.idnegara    = d.idnegara
        LEFT JOIN fund.marketer m    ON m.marketerid  = d.marketerid
        LEFT JOIN fund.workarea wa   ON wa.workareaid = id.workareaid
        LEFT JOIN fund.workarea wai  ON wai.workareaid = id.workareaidinitial
        LEFT JOIN fund.fieldofwork fw ON fw.fworkid   = id.fworkid
        LEFT JOIN fund.propinsi po   ON po.idpropinsi = id.idpropinsioffice
        WHERE d.donorid = $1
        """,
        donor_id,
    )
    if not row:
        return None

    bank_accounts = await _get_bank_accounts(donor_id)
    commitments = await _get_commitments(donor_id)

    return IndividualDonorDetail(
        donor_id=row['donorid'],
        donor_no=row['donorno'],
        donor_name=row['donorname'],
        status=row['status'],
        branch_code=row['branchcode'],
        join_date=_parse_date(row['joindate']),
        npwp=row['npwp'],
        npwz=row['npwz'],
        economic_sector=row['economicsector'],
        phone_number=row['phonenumber'],
        fax=row['fax'],
        address_street=row['addressstreet'],
        address_kelurahan=row['addresskelurahan'],
        address_kecamatan=row['addresskecamatan'],
        address_city=row['addresscity'],
        address_postal_code=row['addresspostalcode'],
        id_propinsi=row['idpropinsi'],
        province_name=row['province_name'],
        id_negara=row['idnegara'],
        country_name=row['country_name'],
        marketer_id=row['marketerid'],
        marketer_code=row['marketercode'],
        marketer_name=row['marketername'],
        gender=row['gender'],
        birth_date=_parse_date(row['birthdate']),
        birth_place=row['birthplace'],
        identity_type=row['identitytype'],
        identity_number=row['identitynumber'],
        religion=row['religion'],
        marital_state=row['maritalstate'],
        email=row['email'],
        mobile_phone=row['mobilephone'],
        status_rumah=row['statusrumah'],
        is_internal_employee=row['isinternalemployee'],
        work_identity_number=row['workidentitynumber'],
        work_area_id=row['workareaid'],
        work_area_code=row['workareacode'],
        work_area_name=row['workareaname'],
        work_area_id_initial=row['workareaidinitial'],
        work_area_initial_code=row['work_area_initial_code'],
        work_area_initial_name=row['work_area_initial_name'],
        work_unit=row['workunit'],
        work_position=row['workposition'],
        work_business_area=row['workbusinessarea'],
        fwork_id=row['fworkid'],
        fwork_code=row['fworkcode'],
        fwork_name=row['fworkname'],
        donor_group=row['donorgroup'],
        id_propinsi_office=row['idpropinsioffice'],
        office_province_name=row['office_province_name'],
        office_address=row['officeaddress'],
        office_kelurahan=row['officekelurahan'],
        office_kecamatan=row['officekecamatan'],
        office_city=row['officecity'],
        office_phone_number=row['officephonenumber'],
        office_postal_code=row['officepostalcode'],
        corporate_name=row['corporatename'],
        job_position=row['jobposition'],
        couple_name=row['couplename'],
        child=row['child'],
        bank_accounts=bank_accounts,
        commitments=commitments,
    )


# ── Individual — Create ───────────────────────────────────────────────────────

async def create_individual(body: CreateUpdateIndividualBody) -> int:
    from datetime import date as date_type

    if body.is_internal_employee == 'T' and not body.work_identity_number:
        raise ValueError('NIP wajib diisi untuk karyawan internal')

    if body.work_identity_number and body.is_internal_employee == 'T':
        existing = await fetch_one(
            "SELECT donorid FROM fund.individualdonor WHERE isinternalemployee='T' AND workidentitynumber=$1",
            body.work_identity_number,
        )
        if existing:
            raise ValueError(f'NIP {body.work_identity_number} sudah terdaftar sebagai donatur')

    join_date = None
    if body.join_date:
        try:
            join_date = date_type.fromisoformat(body.join_date[:10])
        except (ValueError, TypeError):
            join_date = None

    birth_date = None
    if body.birth_date:
        try:
            birth_date = date_type.fromisoformat(body.birth_date[:10])
        except (ValueError, TypeError):
            birth_date = None

    donor_group = body.donor_group or ('R' if body.is_internal_employee == 'T' else 'N')

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            donor_id = await _next_id_gen(conn, 'DONOR', 'fund.donor', 'donorid')
            donor_no = await _next_donor_no(conn, 'P')

            await conn.execute(
                """
                INSERT INTO fund.donor
                    (donorid, donorno, donorname, status, branchcode, joindate, npwp, npwz,
                     economicsector, phonenumber, fax, addressstreet, addresskelurahan,
                     addresskecamatan, addresscity, addresspostalcode, addressstate,
                     idpropinsi, idnegara, marketerid, donortype)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,'P')
                """,
                donor_id, donor_no,
                body.donor_name.upper(),
                body.status or 'A',
                body.branch_code or '',
                join_date,
                body.npwp or '',
                body.npwz or '',
                body.economic_sector or '',
                body.phone_number or '',
                body.fax or '',
                body.address_street or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.address_city or '',
                body.address_postal_code or '',
                '',
                body.id_propinsi,
                body.id_negara,
                body.marketer_id,
            )
            await conn.execute(
                """
                INSERT INTO fund.individualdonor
                    (donorid, gender, birthplace, birthdate, identitytype, identitynumber,
                     religion, maritalstate, email, mobilephone, statusrumah,
                     isinternalemployee, workidentitynumber, workareaid, workareaidinitial,
                     workunit, workposition, workbusinessarea, fworkid,
                     donorgroup, idpropinsioffice, officeaddress, officekelurahan, officekecamatan,
                     officecity, officephonenumber, officepostalcode,
                     corporatename, jobposition, couplename, child)
                VALUES ($1,$2,$3,$4,'K',$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23,$24,$25,$26,$27,$28,$29,$30)
                """,
                donor_id,
                body.gender or '',
                body.birth_place or '',
                birth_date,
                body.identity_number or '',
                body.religion,
                body.marital_state or '',
                body.email or '',
                body.mobile_phone or '',
                body.status_rumah or '',
                body.is_internal_employee or 'F',
                body.work_identity_number or '',
                body.work_area_id,
                body.work_area_id_initial,
                body.work_unit or '',
                body.work_position or '',
                body.work_business_area or '',
                body.fwork_id,
                donor_group,
                body.id_propinsi_office,
                body.office_address or '',
                body.office_kelurahan or '',
                body.office_kecamatan or '',
                body.office_city or '',
                body.office_phone_number or '',
                body.office_postal_code or '',
                body.corporate_name or '',
                body.job_position or '',
                body.couple_name or '',
                body.child,
            )
            await _replace_bank_accounts(conn, donor_id, body.bank_accounts)
            await _replace_commitments(conn, donor_id, body.commitments)
            return donor_id


# ── Individual — Update ───────────────────────────────────────────────────────

async def update_individual(donor_id: int, body: CreateUpdateIndividualBody) -> None:
    from datetime import date as date_type

    row = await fetch_one('SELECT donorid FROM fund.donor WHERE donorid=$1', donor_id)
    if not row:
        raise ValueError('Donatur Individu tidak ditemukan')

    if body.is_internal_employee == 'T' and not body.work_identity_number:
        raise ValueError('NIP wajib diisi untuk karyawan internal')

    if body.work_identity_number and body.is_internal_employee == 'T':
        existing = await fetch_one(
            "SELECT donorid FROM fund.individualdonor WHERE isinternalemployee='T' AND workidentitynumber=$1 AND donorid<>$2",
            body.work_identity_number, donor_id,
        )
        if existing:
            raise ValueError(f'NIP {body.work_identity_number} sudah terdaftar sebagai donatur lain')

    join_date = None
    if body.join_date:
        try:
            join_date = date_type.fromisoformat(body.join_date[:10])
        except (ValueError, TypeError):
            join_date = None

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
                UPDATE fund.donor SET
                    donorname        = $1,
                    status           = $2,
                    joindate         = $3,
                    npwp             = $4,
                    npwz             = $5,
                    economicsector   = $6,
                    phonenumber      = $7,
                    fax              = $8,
                    addressstreet    = $9,
                    addresskelurahan = $10,
                    addresskecamatan = $11,
                    addresscity      = $12,
                    addresspostalcode= $13,
                    idpropinsi       = $14,
                    idnegara         = $15,
                    marketerid       = $16
                WHERE donorid = $17
                """,
                body.donor_name.upper(),
                body.status or 'A',
                join_date,
                body.npwp or '',
                body.npwz or '',
                body.economic_sector or '',
                body.phone_number or '',
                body.fax or '',
                body.address_street or '',
                body.address_kelurahan or '',
                body.address_kecamatan or '',
                body.address_city or '',
                body.address_postal_code or '',
                body.id_propinsi,
                body.id_negara,
                body.marketer_id,
                donor_id,
            )
            await conn.execute(
                """
                UPDATE fund.individualdonor SET
                    gender           = $1,
                    birthplace       = $2,
                    birthdate        = $3,
                    identitynumber   = $4,
                    religion         = $5,
                    maritalstate     = $6,
                    email            = $7,
                    mobilephone      = $8,
                    statusrumah      = $9,
                    isinternalemployee = $10,
                    workidentitynumber = $11,
                    workareaid       = $12,
                    workareaidinitial= $13,
                    workunit         = $14,
                    workposition     = $15,
                    workbusinessarea = $16,
                    fworkid          = $17,
                    idpropinsioffice = $18,
                    officeaddress    = $19,
                    officekelurahan  = $20,
                    officekecamatan  = $21,
                    officecity       = $22,
                    officephonenumber= $23,
                    officepostalcode = $24,
                    corporatename    = $25,
                    jobposition      = $26,
                    couplename       = $27,
                    child            = $28
                WHERE donorid = $29
                """,
                body.gender or '',
                body.birth_place or '',
                birth_date,
                body.identity_number or '',
                body.religion,
                body.marital_state or '',
                body.email or '',
                body.mobile_phone or '',
                body.status_rumah or '',
                body.is_internal_employee or 'F',
                body.work_identity_number or '',
                body.work_area_id,
                body.work_area_id_initial,
                body.work_unit or '',
                body.work_position or '',
                body.work_business_area or '',
                body.fwork_id,
                body.id_propinsi_office,
                body.office_address or '',
                body.office_kelurahan or '',
                body.office_kecamatan or '',
                body.office_city or '',
                body.office_phone_number or '',
                body.office_postal_code or '',
                body.corporate_name or '',
                body.job_position or '',
                body.couple_name or '',
                body.child,
                donor_id,
            )
            await _replace_bank_accounts(conn, donor_id, body.bank_accounts)
            await _replace_commitments(conn, donor_id, body.commitments)


# ── Toggle Status ─────────────────────────────────────────────────────────────

async def toggle_status(donor_id: int, status: str) -> None:
    if status not in ('A', 'N'):
        raise ValueError('Status harus A atau N')
    result = await fetch_one(
        'UPDATE fund.donor SET status=$1 WHERE donorid=$2 RETURNING donorid',
        status, donor_id,
    )
    if not result:
        raise ValueError('Donatur tidak ditemukan')

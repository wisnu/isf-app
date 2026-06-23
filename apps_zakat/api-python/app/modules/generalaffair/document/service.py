from __future__ import annotations

import os
from datetime import date as _date, datetime

from app.modules.generalaffair.document.schema import (
    CreateDocumentTypeBody,
    CreateIncomingBody,
    CreateOutgoingBody,
    DisposisiItem,
    DocumentTypeDetail,
    DocumentTypeListResponse,
    DocumentTypeRow,
    IncomingDocumentDetail,
    IncomingDocumentListResponse,
    IncomingDocumentRow,
    OutgoingDocumentDetail,
    OutgoingDocumentListResponse,
    OutgoingDocumentRow,
    Pagination,
    UpdateIncomingBody,
    UpdateOutgoingBody,
    WorkUnitLookupItem,
)
from app.shared.db import fetch_all, fetch_one, get_pool


def _parse_date(val) -> str | None:
    if val is None:
        return None
    try:
        return val.strftime('%Y-%m-%d')
    except AttributeError:
        s = str(val)
        return s[:10] if len(s) >= 10 else s


def _to_date(s: str | None) -> _date | None:
    if not s:
        return None
    return _date.fromisoformat(str(s)[:10])


def _roman_month(month: int) -> str:
    months = {
        1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI',
        7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X', 11: 'XI', 12: 'XII'
    }
    return months.get(month, '')


async def _next_seq(conn, idname: str, idcode: str) -> int:
    row = await conn.fetchrow(
        'SELECT last_id FROM personalia.custom_idgen WHERE idname=$1 AND idcode=$2 FOR UPDATE',
        idname, idcode
    )
    if row:
        new_id = row['last_id'] + 1
        await conn.execute(
            'UPDATE personalia.custom_idgen SET last_id=$1 WHERE idname=$2 AND idcode=$3',
            new_id, idname, idcode
        )
    else:
        new_id = 1
        await conn.execute(
            'INSERT INTO personalia.custom_idgen(idname, idcode, last_id, locked) VALUES($1,$2,$3,$4)',
            idname, idcode, 1, 'F'
        )
    return new_id


async def _next_id(conn, id_code: str, table: str, pk_col: str) -> int:
    row = await conn.fetchrow(
        'SELECT last_id FROM personalia.id_gen WHERE id_code=$1 FOR UPDATE', id_code
    )
    if row:
        new_id = row['last_id'] + 1
        await conn.execute('UPDATE personalia.id_gen SET last_id=$1 WHERE id_code=$2', new_id, id_code)
    else:
        current_max = await conn.fetchval(f'SELECT COALESCE(MAX({pk_col}), 0) FROM {table}')
        new_id = current_max + 1
        await conn.execute(
            'INSERT INTO personalia.id_gen(id_code, last_id, locked) VALUES($1,$2,$3)',
            id_code, new_id, 'F'
        )
    return new_id


async def _next_dokumen_id(conn) -> int:
    return await _next_id(conn, 'DOKUMEN', 'personalia.dokumen', 'dokumenid')


async def _next_disposisi_id(conn) -> int:
    return await _next_id(conn, 'DISPOSISI', 'personalia.disposisi', 'disposisiid')


def _generate_incoming_nomor(seq: int, jenis_kode: str, branch_code: str, tanggal: str) -> str:
    doc_prefix = os.getenv('PERSONALIA_DOC_PREFIX', 'MAI')
    try:
        dt = datetime.fromisoformat(tanggal)
        month = _roman_month(dt.month)
        year = dt.year
        return f'{seq:05d}/{doc_prefix}/{month}/{year}'
    except Exception:
        return f'{seq:05d}/{doc_prefix}/I/2026'


def _generate_outgoing_nomor(seq: int, jenis_kode: str, work_unit_id: str, year: int) -> str:
    doc_prefix = os.getenv('PERSONALIA_DOC_PREFIX', 'MAI')
    if work_unit_id == 'MNG':
        return f'{doc_prefix}/{seq:05d}/{year}'
    else:
        return f'{doc_prefix}.{work_unit_id}/{seq:05d}/{year}'


# ── Document Types CRUD ───────────────────────────────────────────────────────

async def list_document_types(search: str | None = None, page: int = 1, page_size: int = 25) -> DocumentTypeListResponse:
    offset = (page - 1) * page_size
    where_clause = ''
    params = []

    if search and search.strip():
        p = f'%{search.strip().lower()}%'
        params = [p, p]
        where_clause = 'WHERE LOWER(kodejenisdokumen) LIKE $1 OR LOWER(namajenisdokumen) LIKE $2'

    limit_idx = len(params) + 1
    offset_idx = len(params) + 2

    rows = await fetch_all(
        f'''
        SELECT
            idjenisdokumen AS id_jenis_dokumen,
            kodejenisdokumen AS kode_jenis_dokumen,
            namajenisdokumen AS nama_jenis_dokumen
        FROM personalia.jenisdokumen
        {where_clause}
        ORDER BY idjenisdokumen
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        ''',
        *params, page_size, offset
    )

    total = await fetch_one(
        f'SELECT COUNT(*) as cnt FROM personalia.jenisdokumen {where_clause}',
        *params
    )
    total_count = total['cnt'] if total else 0

    row_list = [
        DocumentTypeRow(
            id_jenis_dokumen=r['id_jenis_dokumen'],
            kode_jenis_dokumen=r['kode_jenis_dokumen'],
            nama_jenis_dokumen=r['nama_jenis_dokumen'],
        )
        for r in rows
    ]

    return DocumentTypeListResponse(
        rows=row_list,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total_count,
            total_pages=(total_count + page_size - 1) // page_size
        )
    )


async def create_document_type(kode: str, nama: str) -> dict:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                'SELECT last_id FROM personalia.id_gen WHERE id_code=$1 FOR UPDATE', 'JENISDOKUMEN'
            )
            if row:
                new_id = row['last_id'] + 1
                await conn.execute('UPDATE personalia.id_gen SET last_id=$1 WHERE id_code=$2', new_id, 'JENISDOKUMEN')
            else:
                current_max = await conn.fetchval(
                    'SELECT COALESCE(MAX(idjenisdokumen), 0) FROM personalia.jenisdokumen'
                )
                new_id = current_max + 1
                await conn.execute(
                    'INSERT INTO personalia.id_gen(id_code, last_id, locked) VALUES($1,$2,$3)',
                    'JENISDOKUMEN', new_id, 'F'
                )
            await conn.execute(
                'INSERT INTO personalia.jenisdokumen(idjenisdokumen, kodejenisdokumen, namajenisdokumen) VALUES($1,$2,$3)',
                new_id, kode, nama
            )
    return {'id_jenis_dokumen': new_id}


async def update_document_type(id: int, kode: str, nama: str) -> dict:
    pool = get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            'UPDATE personalia.jenisdokumen SET kodejenisdokumen=$1, namajenisdokumen=$2 WHERE idjenisdokumen=$3',
            kode, nama, id
        )
    return {'id_jenis_dokumen': id}


async def delete_document_type(id: int) -> None:
    pool = get_pool()
    async with pool.acquire() as conn:
        ref_count = await conn.fetchval(
            'SELECT COUNT(*) FROM personalia.dokumen WHERE idjenisdokumen=$1',
            id
        )
        if ref_count > 0:
            raise ValueError(f'Jenis dokumen digunakan oleh {ref_count} dokumen')
        await conn.execute('DELETE FROM personalia.jenisdokumen WHERE idjenisdokumen=$1', id)


# ── Lookups ───────────────────────────────────────────────────────────────────

async def lookup_work_units() -> list[WorkUnitLookupItem]:
    rows = await fetch_all(
        '''
        SELECT
            workunitid AS work_unit_id,
            description
        FROM personalia.workunit
        WHERE status='A'
        ORDER BY workunitid
        '''
    )
    return [
        WorkUnitLookupItem(work_unit_id=r['work_unit_id'], description=r['description'])
        for r in rows
    ]


# ── Incoming Documents CRUD ───────────────────────────────────────────────────

async def list_incoming(
    search: str | None = None,
    id_jenis_dokumen: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    page: int = 1,
    page_size: int = 25,
    branch: str | None = None,
) -> IncomingDocumentListResponse:
    offset = (page - 1) * page_size
    conds = []
    params = []

    conds.append('(d.tipedokumen IS NULL OR d.tipedokumen != \'K\')')

    if search and search.strip():
        s = f'%{search.strip().lower()}%'
        conds.append(
            '(LOWER(COALESCE(d.nomor,\'\')) LIKE $' + str(len(params) + 1) +
            ' OR LOWER(COALESCE(dm.pengirim,\'\')) LIKE $' + str(len(params) + 2) +
            ' OR LOWER(COALESCE(d.perihal,\'\')) LIKE $' + str(len(params) + 3) + ')'
        )
        params.extend([s, s, s])

    if id_jenis_dokumen is not None:
        conds.append('d.idjenisdokumen = $' + str(len(params) + 1))
        params.append(id_jenis_dokumen)

    if date_from:
        conds.append('CAST(d.tanggaldokumen AS DATE) >= $' + str(len(params) + 1))
        params.append(_to_date(date_from))

    if date_to:
        conds.append('CAST(d.tanggaldokumen AS DATE) <= $' + str(len(params) + 1))
        params.append(_to_date(date_to))

    if branch:
        conds.append('d.branchcode = $' + str(len(params) + 1))
        params.append(branch)

    where_clause = 'WHERE ' + ' AND '.join(conds) if conds else ''

    limit_idx = len(params) + 1
    offset_idx = len(params) + 2

    rows = await fetch_all(
        f'''
        SELECT
            d.dokumenid,
            d.nomor,
            dm.pengirim,
            d.perihal,
            CAST(d.tanggaldokumen AS VARCHAR) AS tanggal_dokumen,
            CAST(dm.tanggalterima AS VARCHAR) AS tanggal_terima,
            jd.namajenisdokumen,
            d.branchcode
        FROM personalia.dokumen d
        LEFT JOIN personalia.dokumenmasuk dm ON d.dokumenid = dm.dokumenid
        LEFT JOIN personalia.jenisdokumen jd ON d.idjenisdokumen = jd.idjenisdokumen
        {where_clause}
        ORDER BY d.tanggaldokumen DESC, d.dokumenid DESC
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        ''',
        *params, page_size, offset
    )

    total = await fetch_one(
        f'''
        SELECT COUNT(*) as cnt
        FROM personalia.dokumen d
        LEFT JOIN personalia.dokumenmasuk dm ON d.dokumenid = dm.dokumenid
        {where_clause}
        ''',
        *params
    )
    total_count = total['cnt'] if total else 0

    row_list = [
        IncomingDocumentRow(
            dokumen_id=r['dokumenid'],
            nomor=r['nomor'],
            pengirim=r['pengirim'],
            perihal=r['perihal'],
            tanggal_dokumen=_parse_date(r['tanggal_dokumen']),
            tanggal_terima=_parse_date(r['tanggal_terima']),
            nama_jenis_dokumen=r['namajenisdokumen'],
            branch_code=r['branchcode'],
        )
        for r in rows
    ]

    return IncomingDocumentListResponse(
        rows=row_list,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total_count,
            total_pages=(total_count + page_size - 1) // page_size
        )
    )


async def get_incoming_detail(dokumen_id: int) -> IncomingDocumentDetail | None:
    row = await fetch_one(
        '''
        SELECT
            d.dokumenid,
            d.nomor,
            dm.pengirim,
            d.perihal,
            CAST(d.tanggaldokumen AS VARCHAR) AS tanggal_dokumen,
            CAST(dm.tanggalterima AS VARCHAR) AS tanggal_terima,
            jd.namajenisdokumen,
            dm.ditujukanke,
            dm.nomoreksternaldokumen,
            d.keterangan,
            d.branchcode
        FROM personalia.dokumen d
        LEFT JOIN personalia.dokumenmasuk dm ON d.dokumenid = dm.dokumenid
        LEFT JOIN personalia.jenisdokumen jd ON d.idjenisdokumen = jd.idjenisdokumen
        WHERE d.dokumenid = $1
        ''',
        dokumen_id
    )

    if not row:
        return None

    disposisi_rows = await fetch_all(
        '''
        SELECT
            CAST(tanggal AS VARCHAR) AS tanggal,
            disposisioleh,
            keterangandisposisi
        FROM personalia.disposisi
        WHERE dokumenid = $1
        ORDER BY disposisiid
        ''',
        dokumen_id
    )

    disposisi = [
        DisposisiItem(
            tanggal=_parse_date(d['tanggal']),
            disposisi_oleh=d['disposisioleh'],
            keterangan_disposisi=d['keterangandisposisi'],
        )
        for d in disposisi_rows
    ]

    return IncomingDocumentDetail(
        dokumen_id=row['dokumenid'],
        nomor=row['nomor'],
        pengirim=row['pengirim'],
        perihal=row['perihal'],
        tanggal_dokumen=_parse_date(row['tanggal_dokumen']),
        tanggal_terima=_parse_date(row['tanggal_terima']),
        nama_jenis_dokumen=row['namajenisdokumen'],
        ditujukan_ke=row['ditujukanke'],
        nomor_eksternal=row['nomoreksternaldokumen'],
        keterangan=row['keterangan'],
        branch_code=row['branchcode'],
        disposisi=disposisi,
    )


async def create_incoming(data: CreateIncomingBody, user_input: str, branch_code: str) -> dict:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            dokumen_id = await _next_dokumen_id(conn)
            idcode = f'{data.id_jenis_dokumen}-{branch_code}'
            seq = await _next_seq(conn, 'DOKUMENMASUK', idcode)
            nomor = _generate_incoming_nomor(seq, '', branch_code, data.tanggal_dokumen)

            await conn.execute(
                '''
                INSERT INTO personalia.dokumen
                    (dokumenid, idjenisdokumen, nomor, perihal, tanggaldokumen, tipedokumen, branchcode, keterangan, userinput, tanggalinput)
                VALUES ($1, $2, $3, $4, $5, NULL, $6, $7, $8, NOW())
                ''',
                dokumen_id, data.id_jenis_dokumen, nomor, data.perihal, _to_date(data.tanggal_dokumen), branch_code, data.keterangan, user_input
            )

            await conn.execute(
                '''
                INSERT INTO personalia.dokumenmasuk
                    (dokumenid, pengirim, tanggalterima, ditujukanke, nomoreksternaldokumen)
                VALUES ($1, $2, $3, $4, $5)
                ''',
                dokumen_id, data.pengirim, _to_date(data.tanggal_terima), data.ditujukan_ke, data.nomor_eksternal_dokumen
            )

            for disp in data.disposisi:
                disp_id = await _next_disposisi_id(conn)
                await conn.execute(
                    '''
                    INSERT INTO personalia.disposisi
                        (disposisiid, dokumenid, tanggal, disposisioleh, keterangandisposisi)
                    VALUES ($1, $2, $3, $4, $5)
                    ''',
                    disp_id, dokumen_id, _to_date(disp.tanggal), disp.disposisi_oleh, disp.keterangan_disposisi
                )

    return {'nomor': nomor, 'dokumen_id': dokumen_id}


async def update_incoming(dokumen_id: int, data: UpdateIncomingBody, user_ubah: str) -> dict:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                '''
                UPDATE personalia.dokumen
                SET idjenisdokumen=$1, perihal=$2, tanggaldokumen=$3, keterangan=$4, userubah=$5, tanggalubah=NOW()
                WHERE dokumenid=$6
                ''',
                data.id_jenis_dokumen, data.perihal, _to_date(data.tanggal_dokumen), data.keterangan, user_ubah, dokumen_id
            )

            await conn.execute(
                '''
                UPDATE personalia.dokumenmasuk
                SET pengirim=$1, tanggalterima=$2, ditujukanke=$3, nomoreksternaldokumen=$4
                WHERE dokumenid=$5
                ''',
                data.pengirim, _to_date(data.tanggal_terima), data.ditujukan_ke, data.nomor_eksternal_dokumen, dokumen_id
            )

            await conn.execute('DELETE FROM personalia.disposisi WHERE dokumenid=$1', dokumen_id)

            for disp in data.disposisi:
                disp_id = await _next_disposisi_id(conn)
                await conn.execute(
                    '''
                    INSERT INTO personalia.disposisi
                        (disposisiid, dokumenid, tanggal, disposisioleh, keterangandisposisi)
                    VALUES ($1, $2, $3, $4, $5)
                    ''',
                    disp_id, dokumen_id, _to_date(disp.tanggal), disp.disposisi_oleh, disp.keterangan_disposisi
                )

    return {'dokumen_id': dokumen_id}


# ── Outgoing Documents CRUD ───────────────────────────────────────────────────

async def list_outgoing(
    search: str | None = None,
    id_jenis_dokumen: int | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    page: int = 1,
    page_size: int = 25,
    branch: str | None = None,
) -> OutgoingDocumentListResponse:
    offset = (page - 1) * page_size
    conds = ['d.tipedokumen = \'K\'']
    params = []

    if search and search.strip():
        s = f'%{search.strip().lower()}%'
        conds.append(
            '(LOWER(COALESCE(d.nomor,\'\')) LIKE $' + str(len(params) + 1) +
            ' OR LOWER(COALESCE(dk.tujuan,\'\')) LIKE $' + str(len(params) + 2) +
            ' OR LOWER(COALESCE(d.perihal,\'\')) LIKE $' + str(len(params) + 3) + ')'
        )
        params.extend([s, s, s])

    if id_jenis_dokumen is not None:
        conds.append('d.idjenisdokumen = $' + str(len(params) + 1))
        params.append(id_jenis_dokumen)

    if date_from:
        conds.append('CAST(d.tanggaldokumen AS DATE) >= $' + str(len(params) + 1))
        params.append(_to_date(date_from))

    if date_to:
        conds.append('CAST(d.tanggaldokumen AS DATE) <= $' + str(len(params) + 1))
        params.append(_to_date(date_to))

    if branch:
        conds.append('d.branchcode = $' + str(len(params) + 1))
        params.append(branch)

    where_clause = 'WHERE ' + ' AND '.join(conds)

    limit_idx = len(params) + 1
    offset_idx = len(params) + 2

    rows = await fetch_all(
        f'''
        SELECT
            d.dokumenid,
            d.nomor,
            dk.pic,
            dk.tujuan,
            d.perihal,
            CAST(d.tanggaldokumen AS VARCHAR) AS tanggal_dokumen,
            CAST(dk.tanggalkirim AS VARCHAR) AS tanggal_kirim,
            dk.workunitid,
            wu.description,
            jd.namajenisdokumen,
            dk.statuskirim,
            d.branchcode
        FROM personalia.dokumen d
        LEFT JOIN personalia.dokumenkeluar dk ON d.dokumenid = dk.dokumenid
        LEFT JOIN personalia.jenisdokumen jd ON d.idjenisdokumen = jd.idjenisdokumen
        LEFT JOIN personalia.workunit wu ON dk.workunitid = wu.workunitid
        {where_clause}
        ORDER BY d.tanggaldokumen DESC, d.dokumenid DESC
        LIMIT ${limit_idx} OFFSET ${offset_idx}
        ''',
        *params, page_size, offset
    )

    total = await fetch_one(
        f'''
        SELECT COUNT(*) as cnt
        FROM personalia.dokumen d
        LEFT JOIN personalia.dokumenkeluar dk ON d.dokumenid = dk.dokumenid
        {where_clause}
        ''',
        *params
    )
    total_count = total['cnt'] if total else 0

    row_list = [
        OutgoingDocumentRow(
            dokumen_id=r['dokumenid'],
            nomor=r['nomor'],
            pic=r['pic'],
            tujuan=r['tujuan'],
            perihal=r['perihal'],
            tanggal_dokumen=_parse_date(r['tanggal_dokumen']),
            tanggal_kirim=_parse_date(r['tanggal_kirim']),
            work_unit_id=r['workunitid'],
            work_unit_desc=r['description'],
            nama_jenis_dokumen=r['namajenisdokumen'],
            status_kirim=r['statuskirim'],
            branch_code=r['branchcode'],
        )
        for r in rows
    ]

    return OutgoingDocumentListResponse(
        rows=row_list,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total_count,
            total_pages=(total_count + page_size - 1) // page_size
        )
    )


async def get_outgoing_detail(dokumen_id: int) -> OutgoingDocumentDetail | None:
    row = await fetch_one(
        '''
        SELECT
            d.dokumenid,
            d.nomor,
            dk.pic,
            dk.tujuan,
            d.perihal,
            CAST(d.tanggaldokumen AS VARCHAR) AS tanggal_dokumen,
            CAST(dk.tanggalkirim AS VARCHAR) AS tanggal_kirim,
            dk.workunitid,
            wu.description,
            jd.namajenisdokumen,
            dk.statuskirim,
            dk.konseptor,
            d.keterangan,
            d.branchcode
        FROM personalia.dokumen d
        LEFT JOIN personalia.dokumenkeluar dk ON d.dokumenid = dk.dokumenid
        LEFT JOIN personalia.jenisdokumen jd ON d.idjenisdokumen = jd.idjenisdokumen
        LEFT JOIN personalia.workunit wu ON dk.workunitid = wu.workunitid
        WHERE d.dokumenid = $1
        ''',
        dokumen_id
    )

    if not row:
        return None

    return OutgoingDocumentDetail(
        dokumen_id=row['dokumenid'],
        nomor=row['nomor'],
        pic=row['pic'],
        tujuan=row['tujuan'],
        perihal=row['perihal'],
        tanggal_dokumen=_parse_date(row['tanggal_dokumen']),
        tanggal_kirim=_parse_date(row['tanggal_kirim']),
        work_unit_id=row['workunitid'],
        work_unit_desc=row['description'],
        nama_jenis_dokumen=row['namajenisdokumen'],
        status_kirim=row['statuskirim'],
        konseptor=row['konseptor'],
        keterangan=row['keterangan'],
        branch_code=row['branchcode'],
    )


async def create_outgoing(data: CreateOutgoingBody, user_input: str, branch_code: str) -> dict:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            dokumen_id = await _next_dokumen_id(conn)
            year = datetime.now().year
            idcode = f'{data.id_jenis_dokumen}-{branch_code}-{year}'
            seq = await _next_seq(conn, 'DOKUMENKELUAR', idcode)
            nomor = _generate_outgoing_nomor(seq, '', data.work_unit_id, year)

            await conn.execute(
                '''
                INSERT INTO personalia.dokumen
                    (dokumenid, idjenisdokumen, nomor, perihal, tanggaldokumen, tipedokumen, branchcode, keterangan, userinput, tanggalinput)
                VALUES ($1, $2, $3, $4, $5, 'K', $6, $7, $8, NOW())
                ''',
                dokumen_id, data.id_jenis_dokumen, nomor, data.perihal, _to_date(data.tanggal_dokumen), branch_code, data.keterangan, user_input
            )

            await conn.execute(
                '''
                INSERT INTO personalia.dokumenkeluar
                    (dokumenid, pic, konseptor, tujuan, tanggalkirim, workunitid)
                VALUES ($1, $2, $3, $4, $5, $6)
                ''',
                dokumen_id, data.pic, data.konseptor, data.tujuan, _to_date(data.tanggal_kirim), data.work_unit_id
            )

    return {'nomor': nomor, 'dokumen_id': dokumen_id}


async def update_outgoing(dokumen_id: int, data: UpdateOutgoingBody, user_ubah: str) -> dict:
    pool = get_pool()
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                '''
                UPDATE personalia.dokumen
                SET idjenisdokumen=$1, perihal=$2, tanggaldokumen=$3, keterangan=$4, userubah=$5, tanggalubah=NOW()
                WHERE dokumenid=$6
                ''',
                data.id_jenis_dokumen, data.perihal, _to_date(data.tanggal_dokumen), data.keterangan, user_ubah, dokumen_id
            )

            await conn.execute(
                '''
                UPDATE personalia.dokumenkeluar
                SET pic=$1, konseptor=$2, tujuan=$3, tanggalkirim=$4, statuskirim=$5, workunitid=$6
                WHERE dokumenid=$7
                ''',
                data.pic, data.konseptor, data.tujuan, _to_date(data.tanggal_kirim), data.status_kirim, data.work_unit_id, dokumen_id
            )

    return {'dokumen_id': dokumen_id}

from __future__ import annotations

from datetime import datetime

from app.modules.distribution.proposal.schema import (
    CreateProposalBody,
    MustahiqLookupItem,
    Pagination,
    ProductGroupLookupItem,
    ProposalDetail,
    ProposalList,
    ProposalRow,
    TotalByMustahiqResponse,
    TotalByMustahiqRow,
    UpdateProposalBody,
)
from app.shared.db import fetch_all, fetch_one, get_pool


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_date(val) -> str | None:
    """Convert timestamp/date to ISO YYYY-MM-DD."""
    if val is None:
        return None
    try:
        return val.strftime('%Y-%m-%d')
    except AttributeError:
        s = str(val)
        return s[:10] if len(s) >= 10 else s


async def _generate_proposal_no(conn, product_group_id: int, received_date: str) -> str:
    """Generate proposal number: {productgroupcode}/{seq:05d}/{MM}/{YY}"""
    # 1. Get product group code
    pg_row = await conn.fetchrow(
        'SELECT productgroupcode FROM program.productgroup WHERE productgroupid = $1',
        product_group_id,
    )
    if not pg_row:
        raise ValueError('Jenis program tidak ditemukan')

    pg_code = pg_row['productgroupcode']

    # 2. Parse MM, YY from received_date (ISO YYYY-MM-DD)
    try:
        dt = datetime.strptime(received_date[:10], '%Y-%m-%d')
        mm = dt.strftime('%m')
        yy = dt.strftime('%y')
    except (ValueError, TypeError):
        raise ValueError('Format tanggal penerimaan harus ISO YYYY-MM-DD')

    # 3. Count existing proposals in this month/group (FOR UPDATE to ensure concurrency safety)
    count_row = await conn.fetchrow(
        """
        SELECT CAST(COUNT(*) AS INTEGER) AS cnt
        FROM program.proposal
        WHERE productgroupid = $1
          AND CAST(EXTRACT(MONTH FROM proposalreceiveddate) AS VARCHAR) = $2
          AND CAST(EXTRACT(YEAR FROM proposalreceiveddate) AS VARCHAR) = $3
        FOR UPDATE
        """,
        product_group_id,
        mm,
        '20' + yy,
    )

    seq = (count_row['cnt'] if count_row else 0) + 1
    seq_str = f'{seq:05d}'

    return f'{pg_code}/{seq_str}/{mm}/{yy}'


# ── List ──────────────────────────────────────────────────────────────────────

async def list_proposals(
    date_from: str | None = None,
    date_to: str | None = None,
    branch_code: str | None = None,
    status: str | None = None,
    mustahiq_id: int | None = None,
    product_group_id: int | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> ProposalList:
    """List proposals with filters and pagination."""
    page = max(1, page)
    page_size = max(1, min(500, page_size))

    # Build WHERE conditions
    conds = ['1=1']
    params: list = []

    if date_from:
        params.append(date_from)
        conds.append(f'CAST(p.proposalreceiveddate AS DATE) >= ${len(params)}')

    if date_to:
        params.append(date_to)
        conds.append(f'CAST(p.proposalreceiveddate AS DATE) <= ${len(params)}')

    if branch_code:
        params.append(branch_code)
        conds.append(f'p.branchcode = ${len(params)}')

    if status:
        params.append(status)
        conds.append(f'p.proposalstatus = ${len(params)}')

    if mustahiq_id:
        params.append(mustahiq_id)
        conds.append(f'p.mustahiqid = ${len(params)}')

    if product_group_id:
        params.append(product_group_id)
        conds.append(f'p.productgroupid = ${len(params)}')

    if search and search.strip():
        search_pat = f'%{search.strip().lower()}%'
        params.append(search_pat)
        conds.append(
            f'(LOWER(COALESCE(p.proposalno, \'\')) LIKE ${len(params)}'
            f' OR LOWER(COALESCE(p.proposaldescription, \'\')) LIKE ${len(params)-len(params)+len(params)})'
        )
        params.append(search_pat)

    where_clause = ' AND '.join(conds)

    # Count total
    count_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM program.proposal p
        WHERE {where_clause}
        """,
        *params,
    )
    total = int((count_row or {}).get('c', 0))

    # Fetch paginated rows
    lp = len(params) + 1
    op = len(params) + 2
    rows = await fetch_all(
        f"""
        SELECT
            p.proposalid,
            p.proposalno,
            CAST(p.proposaldate AS VARCHAR) AS proposal_date,
            CAST(p.proposalreceiveddate AS VARCHAR) AS received_date,
            p.proposaldescription,
            p.proposalnominal,
            p.proposalreceivedby,
            p.proposalreferenceby,
            p.proposalreferenceposition,
            p.proposalstatus,
            p.mustahiqid,
            c.customername,
            p.productgroupid,
            pg.productgroupname,
            p.branchcode
        FROM program.proposal p
        JOIN program.mustahiq m ON m.mustahiqid = p.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        JOIN program.productgroup pg ON pg.productgroupid = p.productgroupid
        WHERE {where_clause}
        ORDER BY p.proposalreceiveddate DESC, p.proposalid DESC
        LIMIT ${lp} OFFSET ${op}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total + page_size - 1) // page_size if total else 0

    return ProposalList(
        rows=[
            ProposalRow(
                proposal_id=r['proposalid'],
                proposal_no=r['proposalno'],
                proposal_date=r['proposal_date'][:10] if r['proposal_date'] else None,
                received_date=r['received_date'][:10] if r['received_date'] else None,
                description=r['proposaldescription'],
                nominal=r['proposalnominal'],
                received_by=r['proposalreceivedby'],
                reference_by=r['proposalreferenceby'],
                reference_position=r['proposalreferenceposition'],
                status=r['proposalstatus'],
                mustahiq_id=r['mustahiqid'],
                mustahiq_name=r['customername'],
                product_group_id=r['productgroupid'],
                product_group_name=r['productgroupname'],
                branch_code=r['branchcode'],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, page_size=page_size, total=total, total_pages=total_pages),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_proposal(proposal_id: int) -> ProposalDetail | None:
    """Get proposal detail including customer address."""
    row = await fetch_one(
        """
        SELECT
            p.proposalid,
            p.proposalno,
            CAST(p.proposaldate AS VARCHAR) AS proposal_date,
            CAST(p.proposalreceiveddate AS VARCHAR) AS received_date,
            p.proposaldescription,
            p.proposalnominal,
            p.proposalreceivedby,
            p.proposalreferenceby,
            p.proposalreferenceposition,
            p.proposalstatus,
            p.mustahiqid,
            c.customername,
            c.addressstreet,
            c.addresskelurahan,
            c.addresskecamatan,
            p.productgroupid,
            pg.productgroupname,
            p.branchcode
        FROM program.proposal p
        JOIN program.mustahiq m ON m.mustahiqid = p.mustahiqid
        JOIN program.customer c ON c.customerid = m.customerid
        JOIN program.productgroup pg ON pg.productgroupid = p.productgroupid
        WHERE p.proposalid = $1
        """,
        proposal_id,
    )

    if not row:
        return None

    return ProposalDetail(
        proposal_id=row['proposalid'],
        proposal_no=row['proposalno'],
        proposal_date=row['proposal_date'][:10] if row['proposal_date'] else None,
        received_date=row['received_date'][:10] if row['received_date'] else None,
        description=row['proposaldescription'],
        nominal=row['proposalnominal'],
        received_by=row['proposalreceivedby'],
        reference_by=row['proposalreferenceby'],
        reference_position=row['proposalreferenceposition'],
        status=row['proposalstatus'],
        mustahiq_id=row['mustahiqid'],
        mustahiq_name=row['customername'],
        product_group_id=row['productgroupid'],
        product_group_name=row['productgroupname'],
        branch_code=row['branchcode'],
        address_street=row['addressstreet'],
        address_kelurahan=row['addresskelurahan'],
        address_kecamatan=row['addresskecamatan'],
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_proposal(body: CreateProposalBody) -> int:
    """Create new proposal. Status always 'B' (Baru)."""
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            # Check mustahiq exists
            mustahiq_row = await conn.fetchrow(
                'SELECT mustahiqid FROM program.mustahiq WHERE mustahiqid = $1',
                body.mustahiq_id,
            )
            if not mustahiq_row:
                raise ValueError('Mustahiq tidak ditemukan')

            # Check product group exists
            pg_row = await conn.fetchrow(
                'SELECT productgroupid FROM program.productgroup WHERE productgroupid = $1',
                body.product_group_id,
            )
            if not pg_row:
                raise ValueError('Jenis program tidak ditemukan')

            # Generate proposal number (inside transaction for concurrency safety)
            proposal_no = await _generate_proposal_no(
                conn, body.product_group_id, body.received_date
            )

            # Insert proposal
            proposal_id = await conn.fetchval("SELECT nextval('program.seq_proposal')")
            await conn.execute(
                """
                INSERT INTO program.proposal
                    (proposalid, proposalno, proposaldescription, proposalnominal,
                     proposalreferenceby, proposalstatus, mustahiqid, proposaldate,
                     proposalreceiveddate, proposalreceivedby, proposalreferenceposition,
                     productgroupid, branchcode)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                """,
                proposal_id,
                proposal_no,
                body.description or '',
                body.nominal,
                body.reference_by or '',
                'B',  # Status always 'B'
                body.mustahiq_id,
                body.proposal_date,
                body.received_date,
                body.received_by or '',
                body.reference_position,
                body.product_group_id,
                body.branch_code,
            )

            return proposal_id


# ── Update ────────────────────────────────────────────────────────────────────

async def update_proposal(proposal_id: int, body: UpdateProposalBody) -> None:
    """Update proposal. Cannot change branch_code."""
    proposal_row = await fetch_one(
        'SELECT mustahiqid, productgroupid FROM program.proposal WHERE proposalid = $1',
        proposal_id,
    )

    if not proposal_row:
        raise ValueError('Proposal tidak ditemukan')

    # Verify mustahiq exists
    mustahiq_row = await fetch_one(
        'SELECT mustahiqid FROM program.mustahiq WHERE mustahiqid = $1',
        body.mustahiq_id,
    )
    if not mustahiq_row:
        raise ValueError('Mustahiq tidak ditemukan')

    # Verify product group exists
    pg_row = await fetch_one(
        'SELECT productgroupid FROM program.productgroup WHERE productgroupid = $1',
        body.product_group_id,
    )
    if not pg_row:
        raise ValueError('Jenis program tidak ditemukan')

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE program.proposal SET
                    proposaldescription = $1,
                    proposalnominal = $2,
                    proposalreferenceby = $3,
                    proposaldate = $4,
                    proposalreceiveddate = $5,
                    proposalreceivedby = $6,
                    proposalreferenceposition = $7,
                    mustahiqid = $8,
                    productgroupid = $9
                WHERE proposalid = $10
                """,
                body.description or '',
                body.nominal,
                body.reference_by or '',
                body.proposal_date,
                body.received_date,
                body.received_by or '',
                body.reference_position,
                body.mustahiq_id,
                body.product_group_id,
                proposal_id,
            )


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_proposal(proposal_id: int) -> None:
    """Delete proposal. Guard: cannot delete if status='S' (Disetujui)."""
    row = await fetch_one(
        'SELECT proposalstatus FROM program.proposal WHERE proposalid = $1',
        proposal_id,
    )

    if not row:
        raise ValueError('Proposal tidak ditemukan')

    if row['proposalstatus'] == 'S':
        raise ValueError('Proposal sudah disetujui, tidak dapat dihapus')

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                'DELETE FROM program.proposal WHERE proposalid = $1',
                proposal_id,
            )


# ── Total by Mustahiq ─────────────────────────────────────────────────────────

async def get_total_by_mustahiq(mustahiq_id: int) -> int:
    """Get total number of proposals ever submitted by a mustahiq."""
    row = await fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM program.proposal
        WHERE mustahiqid = $1
        """,
        mustahiq_id,
    )

    return int(row['total']) if row else 0


# ── Lookups ───────────────────────────────────────────────────────────────────

async def lookup_product_groups() -> list[ProductGroupLookupItem]:
    """Get all active product groups."""
    rows = await fetch_all(
        """
        SELECT productgroupid, productgroupcode, productgroupname
        FROM program.productgroup
        WHERE COALESCE(statusaktif, '') = 'A'
        ORDER BY productgroupname
        """
    )

    return [
        ProductGroupLookupItem(
            product_group_id=r['productgroupid'],
            product_group_code=r['productgroupcode'],
            product_group_name=r['productgroupname'],
        )
        for r in rows
    ]


async def lookup_mustahiq(search: str | None = None) -> list[MustahiqLookupItem]:
    """Search mustahiq by name."""
    if search and search.strip():
        search_pat = f'%{search.strip().lower()}%'
        rows = await fetch_all(
            """
            SELECT m.mustahiqid, c.customername
            FROM program.mustahiq m
            JOIN program.customer c ON c.customerid = m.customerid
            WHERE LOWER(COALESCE(c.customername, '')) LIKE $1
            ORDER BY c.customername
            LIMIT 50
            """,
            search_pat,
        )
    else:
        rows = await fetch_all(
            """
            SELECT m.mustahiqid, c.customername
            FROM program.mustahiq m
            JOIN program.customer c ON c.customerid = m.customerid
            ORDER BY c.customername
            LIMIT 50
            """
        )

    return [
        MustahiqLookupItem(mustahiq_id=r['mustahiqid'], mustahiq_name=r['customername'])
        for r in rows
    ]

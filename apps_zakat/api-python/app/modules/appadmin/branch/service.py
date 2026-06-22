"""Branch service — Cabang CRUD operations."""

from __future__ import annotations

from datetime import datetime

from app.modules.appadmin.branch.schema import (
    BranchCreateRequest,
    BranchDetail,
    BranchListItem,
    BranchUpdateRequest,
    ParentBranchItem,
)
from app.shared.db import execute, fetch_all, fetch_one


async def list_branches(
    page: int = 1,
    limit: int = 25,
    status_aktif: str | None = "T",
    keyword: str | None = None,
) -> tuple[list[BranchListItem], int]:
    """List branches with pagination and filters.

    Args:
        page: Page number (1-indexed)
        limit: Rows per page
        status_aktif: Filter by status — 'T' (Aktif), 'F' (Tidak Aktif), or None (semua)
        keyword: Filter by branch_code or branch_name (ILIKE)
    """
    offset = (page - 1) * limit

    # Build WHERE clause
    where_parts = []
    params: list = []

    if status_aktif is not None and status_aktif != "":
        param_idx = len(params) + 1
        where_parts.append(f"c.status_aktif = ${param_idx}")
        params.append(status_aktif)

    if keyword:
        param_idx = len(params) + 1
        where_parts.append(
            f"(c.kode_cabang ILIKE ${param_idx} OR c.nama_cabang ILIKE ${param_idx})"
        )
        params.append(f"%{keyword}%")

    where_clause = " WHERE " + " AND ".join(where_parts) if where_parts else ""

    # Fetch rows
    limit_idx = len(params) + 1
    offset_idx = len(params) + 2
    query = (
        "SELECT "
        "c.kode_cabang, "
        "c.nama_cabang, "
        "c.tipe_cabang, "
        "c.status_cabang, "
        "c.kode_cabang_induk, "
        "ci.nama_cabang AS parent_branch_name, "
        "c.status_aktif "
        "FROM enterprise.cabang c "
        "LEFT JOIN enterprise.cabang ci ON ci.kode_cabang = c.kode_cabang_induk "
        f"{where_clause} "
        "ORDER BY c.kode_cabang ASC "
        f"LIMIT ${limit_idx} OFFSET ${offset_idx}"
    )
    params.append(limit)
    params.append(offset)

    rows = await fetch_all(query, *params)

    rows_converted = [
        BranchListItem(
            branch_code=r["kode_cabang"],
            branch_name=r["nama_cabang"],
            branch_type=r["tipe_cabang"],
            branch_status=r["status_cabang"],
            parent_branch_code=r["kode_cabang_induk"],
            parent_branch_name=r["parent_branch_name"],
            is_active=r["status_aktif"] == "T",
        )
        for r in rows
    ]

    # Count total
    count_query = "SELECT COUNT(*) as cnt FROM enterprise.cabang c" + where_clause
    count_result = await fetch_one(count_query, *params[:-2])
    total = count_result["cnt"] if count_result else 0

    return rows_converted, total


async def list_parent_branches() -> list[ParentBranchItem]:
    """List parent branches for dropdown — cabang Utama (status_cabang='B' or tipe_cabang IN ('CU','PO'))."""
    rows = await fetch_all(
        "SELECT kode_cabang, nama_cabang "
        "FROM enterprise.cabang "
        "WHERE status_aktif = 'T' "
        "  AND (status_cabang = 'B' OR tipe_cabang IN ('CU', 'PO', 'NO')) "
        "ORDER BY kode_cabang ASC"
    )
    return [ParentBranchItem(branch_code=r["kode_cabang"], branch_name=r["nama_cabang"]) for r in rows]


async def get_branch(branch_code: str) -> BranchDetail | None:
    """Get branch detail."""
    row = await fetch_one(
        "SELECT "
        "c.kode_cabang, "
        "c.nama_cabang, "
        "c.tipe_cabang, "
        "c.status_cabang, "
        "c.kode_cabang_induk, "
        "ci.nama_cabang AS parent_branch_name, "
        "c.status_aktif, "
        "c.status_akses, "
        "c.kantor_nama, "
        "c.kantor_npwp, "
        "c.kantor_alamat, "
        "c.kantor_kode_pos, "
        "c.kantor_telepon1, "
        "c.kantor_telepon2, "
        "c.kantor_telepon3, "
        "c.user_input, "
        "CAST(c.tanggal_input AS VARCHAR) AS tanggal_input "
        "FROM enterprise.cabang c "
        "LEFT JOIN enterprise.cabang ci ON ci.kode_cabang = c.kode_cabang_induk "
        "WHERE c.kode_cabang = $1",
        branch_code,
    )
    if not row:
        return None

    return BranchDetail(
        branch_code=row["kode_cabang"],
        branch_name=row["nama_cabang"],
        branch_type=row["tipe_cabang"],
        branch_status=row["status_cabang"],
        parent_branch_code=row["kode_cabang_induk"],
        parent_branch_name=row["parent_branch_name"],
        is_active=row["status_aktif"] == "T",
        office_name=row["kantor_nama"],
        office_npwp=row["kantor_npwp"],
        office_address=row["kantor_alamat"],
        office_postal_code=row["kantor_kode_pos"],
        office_phone1=row["kantor_telepon1"],
        office_phone2=row["kantor_telepon2"],
        office_phone3=row["kantor_telepon3"],
        access_status=row["status_akses"],
        created_by=row["user_input"],
        created_at=row["tanggal_input"],
    )


async def create_branch(payload: BranchCreateRequest, inputer_id: str) -> BranchDetail:
    """Create new branch.

    Auto-set:
    - status_cabang: 'B' if tipe_cabang IN ('CU','PO') else 'S'
    - status_aktif: 'T'
    - status_otorisasi: '1'
    - status_akses: 'O'
    - tanggal_input: now()
    - user_input: inputer_id
    - terminal_input: 'isf-app'
    - If tipe_cabang IN ('CU','PO'): kode_cabang_induk = NULL
    """
    # Determine status_cabang
    status_cabang = "B" if payload.branch_type in ("CU", "PO") else "S"

    # If status_cabang='B', force kode_cabang_induk to NULL
    kode_cabang_induk = None if status_cabang == "B" else payload.parent_branch_code

    # Check for duplicate code
    existing = await fetch_one(
        "SELECT kode_cabang FROM enterprise.cabang WHERE kode_cabang = $1",
        payload.branch_code,
    )
    if existing:
        raise ValueError(f"Kode cabang {payload.branch_code} sudah ada")

    # Insert
    await execute(
        "INSERT INTO enterprise.cabang "
        "("
        "kode_cabang, "
        "nama_cabang, "
        "tipe_cabang, "
        "status_cabang, "
        "kode_cabang_induk, "
        "status_aktif, "
        "status_otorisasi, "
        "status_akses, "
        "kantor_nama, "
        "kantor_npwp, "
        "kantor_alamat, "
        "kantor_kode_pos, "
        "kantor_telepon1, "
        "kantor_telepon2, "
        "kantor_telepon3, "
        "tanggal_input, "
        "user_input, "
        "terminal_input"
        ") VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18)",
        payload.branch_code,
        payload.branch_name,
        payload.branch_type,
        status_cabang,
        kode_cabang_induk,
        "T",  # status_aktif
        "1",  # status_otorisasi
        "O",  # status_akses
        payload.office_name,
        payload.office_npwp,
        payload.office_address,
        payload.office_postal_code,
        payload.office_phone1,
        payload.office_phone2,
        payload.office_phone3,
        datetime.now(),
        inputer_id,
        "isf-app",
    )

    # Fetch and return created branch
    return await get_branch(payload.branch_code)  # type: ignore


async def update_branch(branch_code: str, payload: BranchUpdateRequest) -> BranchDetail:
    """Update branch. Cannot change kode_cabang."""
    # Determine status_cabang based on branch_type
    status_cabang = "B" if payload.branch_type in ("CU", "PO") else "S"

    # If status_cabang='B', force kode_cabang_induk to NULL
    kode_cabang_induk = None if status_cabang == "B" else payload.parent_branch_code

    # Update
    await execute(
        "UPDATE enterprise.cabang SET "
        "nama_cabang = $1, "
        "tipe_cabang = $2, "
        "status_cabang = $3, "
        "kode_cabang_induk = $4, "
        "kantor_nama = $5, "
        "kantor_npwp = $6, "
        "kantor_alamat = $7, "
        "kantor_kode_pos = $8, "
        "kantor_telepon1 = $9, "
        "kantor_telepon2 = $10, "
        "kantor_telepon3 = $11 "
        "WHERE kode_cabang = $12",
        payload.branch_name,
        payload.branch_type,
        status_cabang,
        kode_cabang_induk,
        payload.office_name,
        payload.office_npwp,
        payload.office_address,
        payload.office_postal_code,
        payload.office_phone1,
        payload.office_phone2,
        payload.office_phone3,
        branch_code,
    )

    # Fetch and return updated branch
    return await get_branch(branch_code)  # type: ignore


async def deactivate_branch(branch_code: str) -> BranchDetail:
    """Deactivate branch (set status_aktif='F')."""
    await execute(
        "UPDATE enterprise.cabang SET status_aktif = 'F' WHERE kode_cabang = $1",
        branch_code,
    )
    return await get_branch(branch_code)  # type: ignore


async def activate_branch(branch_code: str) -> BranchDetail:
    """Activate branch (set status_aktif='T')."""
    await execute(
        "UPDATE enterprise.cabang SET status_aktif = 'T' WHERE kode_cabang = $1",
        branch_code,
    )
    return await get_branch(branch_code)  # type: ignore

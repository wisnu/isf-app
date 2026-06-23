"""Role (Peran) management service.

enterprise.peran       — business pool (mziss_laz)
isf_auth.role_menu     — auth pool (isf_auth_zakat)
"""

from __future__ import annotations

from datetime import datetime

from app.modules.appadmin.role.schema import (
    RoleCreateRequest,
    RoleDetail,
    RoleListItem,
    RoleStatusRequest,
    RoleUpdateRequest,
)
from app.shared.db import execute, fetch_all, fetch_all_isf_auth, fetch_one, get_pool


async def list_roles(
    page: int = 1,
    limit: int = 25,
    keyword: str | None = None,
    status: str | None = None,
) -> tuple[list[RoleListItem], int]:
    offset = (page - 1) * limit
    where_parts: list[str] = []
    params: list = []

    if keyword:
        idx = len(params) + 1
        where_parts.append(f"(p.id_peran ILIKE ${idx} OR p.nama_peran ILIKE ${idx})")
        params.append(f"%{keyword}%")

    if status == "active":
        where_parts.append("p.status_peran = 'A'")
    elif status == "inactive":
        where_parts.append("p.status_peran = 'T'")

    where = " WHERE " + " AND ".join(where_parts) if where_parts else ""

    limit_idx = len(params) + 1
    offset_idx = len(params) + 2
    rows = await fetch_all(
        "SELECT p.id_peran, p.nama_peran, p.deskripsi, p.status_peran, "
        "COUNT(lpu.id_user) AS user_count "
        "FROM enterprise.peran p "
        "LEFT JOIN enterprise.listperanuser lpu USING (id_peran)"
        f"{where} "
        "GROUP BY p.id_peran, p.nama_peran, p.deskripsi, p.status_peran "
        "ORDER BY p.id_peran ASC "
        f"LIMIT ${limit_idx} OFFSET ${offset_idx}",
        *params, limit, offset,
    )
    count_row = await fetch_one(
        "SELECT COUNT(*) AS cnt FROM enterprise.peran p" + where, *params
    )
    total = count_row["cnt"] if count_row else 0

    items = [
        RoleListItem(
            role_id=r["id_peran"],
            role_name=r["nama_peran"] or r["id_peran"],
            description=r["deskripsi"],
            status="active" if r["status_peran"] == "A" else "inactive",
            user_count=int(r["user_count"]),
        )
        for r in rows
    ]
    return items, total


async def get_role(role_id: str) -> RoleDetail | None:
    row = await fetch_one(
        "SELECT p.id_peran, p.nama_peran, p.deskripsi, p.status_peran, "
        "COUNT(lpu.id_user) AS user_count "
        "FROM enterprise.peran p "
        "LEFT JOIN enterprise.listperanuser lpu USING (id_peran) "
        "WHERE p.id_peran = $1 "
        "GROUP BY p.id_peran, p.nama_peran, p.deskripsi, p.status_peran",
        role_id,
    )
    if not row:
        return None

    menu_rows = await fetch_all_isf_auth(
        "SELECT DISTINCT menu_key FROM isf_auth.role_menu_permission WHERE role_id=$1 ORDER BY menu_key",
        role_id,
    )
    return RoleDetail(
        role_id=row["id_peran"],
        role_name=row["nama_peran"] or row["id_peran"],
        description=row["deskripsi"],
        status="active" if row["status_peran"] == "A" else "inactive",
        user_count=int(row["user_count"]),
        menu_keys=[m["menu_key"] for m in menu_rows],
    )


async def create_role(payload: RoleCreateRequest) -> RoleDetail:
    role_id = payload.role_id.strip().upper()

    existing = await fetch_one("SELECT id_peran FROM enterprise.peran WHERE id_peran=$1", role_id)
    if existing:
        raise ValueError(f"ID Role '{role_id}' sudah terdaftar")

    now = datetime.now()
    await execute(
        "INSERT INTO enterprise.peran (id_peran, nama_peran, deskripsi, status_peran, "
        "user_input, tanggal_input, terminal_input) "
        "VALUES ($1, $2, $3, 'A', $4, $5, $6)",
        role_id, payload.role_name, payload.description, payload.created_by, now, "isf-app",
    )
    result = await get_role(role_id)
    assert result is not None
    return result


async def update_role(role_id: str, payload: RoleUpdateRequest) -> RoleDetail:
    await execute(
        "UPDATE enterprise.peran SET nama_peran=$1, deskripsi=$2, "
        "user_perbarui=$3, tanggal_perbarui=$4 WHERE id_peran=$5",
        payload.role_name, payload.description, payload.updated_by, datetime.now(), role_id,
    )
    result = await get_role(role_id)
    assert result is not None
    return result


async def update_role_status(role_id: str, payload: RoleStatusRequest) -> RoleDetail:
    status_code = "A" if payload.status == "active" else "T"
    await execute(
        "UPDATE enterprise.peran SET status_peran=$1, user_perbarui=$2, tanggal_perbarui=$3 "
        "WHERE id_peran=$4",
        status_code, payload.updated_by, datetime.now(), role_id,
    )
    result = await get_role(role_id)
    assert result is not None
    return result

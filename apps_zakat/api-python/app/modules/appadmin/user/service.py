"""User management service.

enterprise.userapp   — business pool (mziss_laz)
isf_auth.users       — auth pool (isf_auth_zakat)
isf_auth.user_credentials — password hashes
isf_auth.tenant_memberships — tenant assignments

On create: insert into both pools atomically (best-effort; enterprise first, then auth).
id_user in enterprise == id in isf_auth.users == username (uppercase).
BFF is responsible for password hashing (bcrypt); api-python only stores the hash.
"""

from __future__ import annotations

from datetime import datetime

from app.modules.appadmin.user.schema import (
    UserBranchesRequest,
    UserCreateRequest,
    UserDetail,
    UserListItem,
    UserPasswordRequest,
    UserRolesRequest,
    UserStatusRequest,
    UserUpdateRequest,
)
from app.shared.db import execute, fetch_all, fetch_all_isf_auth, fetch_one, get_isf_auth_pool, get_pool

DEFAULT_TENANT = "perusahaan_a"


async def list_users(
    page: int = 1,
    limit: int = 25,
    keyword: str | None = None,
    status: str | None = None,
    is_locked: bool | None = None,
) -> tuple[list[UserListItem], int]:
    offset = (page - 1) * limit
    where_parts: list[str] = []
    params: list = []

    if keyword:
        idx = len(params) + 1
        where_parts.append(f"(u.id_user ILIKE ${idx} OR u.nama_user ILIKE ${idx})")
        params.append(f"%{keyword}%")

    if status == "active":
        where_parts.append("u.status_profil = 'A'")
    elif status == "inactive":
        where_parts.append("u.status_profil = 'T'")

    if is_locked is True:
        where_parts.append("u.kunci_akses = 'T'")
    elif is_locked is False:
        where_parts.append("u.kunci_akses = 'F'")

    where = " WHERE " + " AND ".join(where_parts) if where_parts else ""

    limit_idx = len(params) + 1
    offset_idx = len(params) + 2
    rows = await fetch_all(
        "SELECT u.id_user, u.nama_user, u.status_profil, u.kunci_akses, "
        "u.kode_cabang, u.tipe_akses_cabang "
        "FROM enterprise.userapp u"
        f"{where} ORDER BY u.id_user ASC LIMIT ${limit_idx} OFFSET ${offset_idx}",
        *params, limit, offset,
    )
    count_row = await fetch_one(
        "SELECT COUNT(*) AS cnt FROM enterprise.userapp u" + where, *params
    )
    total = count_row["cnt"] if count_row else 0

    user_ids = [r["id_user"] for r in rows]
    role_map: dict[str, list[str]] = {uid: [] for uid in user_ids}
    if user_ids:
        role_rows = await fetch_all(
            "SELECT id_user, id_peran FROM enterprise.listperanuser "
            "WHERE id_user = ANY($1::text[]) ORDER BY id_user, id_peran",
            user_ids,
        )
        for rr in role_rows:
            role_map[rr["id_user"]].append(rr["id_peran"])

    items = [
        UserListItem(
            user_id=r["id_user"],
            display_name=r["nama_user"] or "",
            status="active" if r["status_profil"] == "A" else "inactive",
            is_locked=r["kunci_akses"] == "T",
            primary_branch=r["kode_cabang"],
            branch_access="all" if r["tipe_akses_cabang"] == "S" else "single",
            role_ids=role_map.get(r["id_user"], []),
        )
        for r in rows
    ]
    return items, total


async def get_user(user_id: str) -> UserDetail | None:
    row = await fetch_one(
        "SELECT u.id_user, u.nama_user, u.status_profil, u.kunci_akses, "
        "u.kode_cabang, u.tipe_akses_cabang "
        "FROM enterprise.userapp u WHERE u.id_user = $1",
        user_id,
    )
    if not row:
        return None

    role_rows = await fetch_all(
        "SELECT lpu.id_peran, p.nama_peran "
        "FROM enterprise.listperanuser lpu "
        "LEFT JOIN enterprise.peran p USING (id_peran) "
        "WHERE lpu.id_user = $1 ORDER BY lpu.id_peran",
        user_id,
    )
    branch_rows = await fetch_all(
        "SELECT kode_cabang FROM enterprise.listcabangdiizinkan WHERE id_user = $1 ORDER BY kode_cabang",
        user_id,
    )
    return UserDetail(
        user_id=row["id_user"],
        display_name=row["nama_user"] or "",
        status="active" if row["status_profil"] == "A" else "inactive",
        is_locked=row["kunci_akses"] == "T",
        primary_branch=row["kode_cabang"],
        branch_access="all" if row["tipe_akses_cabang"] == "S" else "single",
        roles=[{"role_id": r["id_peran"], "role_name": r["nama_peran"] or r["id_peran"]} for r in role_rows],
        allowed_branches=[b["kode_cabang"] for b in branch_rows],
    )


async def create_user(payload: UserCreateRequest) -> UserDetail:
    user_id = payload.user_id.strip().upper()

    existing = await fetch_one("SELECT id_user FROM enterprise.userapp WHERE id_user = $1", user_id)
    if existing:
        raise ValueError(f"ID User '{user_id}' sudah terdaftar")

    branch_access_code = "S" if payload.branch_access == "all" else "T"
    now = datetime.now()

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO enterprise.userapp "
                "(id_user, nama_user, status_profil, kunci_akses, kode_cabang, "
                "tipe_akses_cabang, level_user, maksimum_jumlah_login, "
                "tanggal_didaftarkan, user_input, terminal_input) "
                "VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)",
                user_id, payload.display_name, "A", "F", payload.primary_branch,
                branch_access_code, 1, 1, now, payload.created_by, "isf-app",
            )
            if payload.roles:
                await conn.executemany(
                    "INSERT INTO enterprise.listperanuser (id_peran, id_user, level_peranuser) "
                    "VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
                    [(role_id, user_id, 1) for role_id in payload.roles],
                )
            branches = list({payload.primary_branch, *payload.branches})
            if branches:
                await conn.executemany(
                    "INSERT INTO enterprise.listcabangdiizinkan (id_user, kode_cabang) "
                    "VALUES ($1, $2) ON CONFLICT DO NOTHING",
                    [(user_id, b) for b in branches],
                )

    isf_pool = get_isf_auth_pool()
    async with isf_pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO isf_auth.users (id, username, display_name, status) "
                "VALUES ($1, $2, $3, $4) ON CONFLICT (username) DO NOTHING",
                user_id, user_id, payload.display_name, "active",
            )
            await conn.execute(
                "INSERT INTO isf_auth.user_credentials (user_id, password_hash) "
                "VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET password_hash = EXCLUDED.password_hash",
                user_id, payload.password_hash,
            )
            await conn.execute(
                "INSERT INTO isf_auth.tenant_memberships (user_id, tenant_id, is_default) "
                "VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
                user_id, DEFAULT_TENANT, True,
            )

    result = await get_user(user_id)
    assert result is not None
    return result


async def update_user(user_id: str, payload: UserUpdateRequest) -> UserDetail:
    branch_access_code = "S" if payload.branch_access == "all" else "T"
    await execute(
        "UPDATE enterprise.userapp SET nama_user=$1, kode_cabang=$2, tipe_akses_cabang=$3, "
        "user_perbarui=$4, tanggal_perbarui=$5 WHERE id_user=$6",
        payload.display_name, payload.primary_branch, branch_access_code,
        payload.updated_by, datetime.now(), user_id,
    )
    async with get_isf_auth_pool().acquire() as conn:
        await conn.execute(
            "UPDATE isf_auth.users SET display_name=$1 WHERE id=$2",
            payload.display_name, user_id,
        )
    result = await get_user(user_id)
    assert result is not None
    return result


async def update_user_status(user_id: str, payload: UserStatusRequest) -> UserDetail:
    status_code = "A" if payload.status == "active" else "T"
    await execute(
        "UPDATE enterprise.userapp SET status_profil=$1, user_perbarui=$2, tanggal_perbarui=$3 "
        "WHERE id_user=$4",
        status_code, payload.updated_by, datetime.now(), user_id,
    )
    isf_status = "active" if payload.status == "active" else "inactive"
    async with get_isf_auth_pool().acquire() as conn:
        await conn.execute("UPDATE isf_auth.users SET status=$1 WHERE id=$2", isf_status, user_id)
    result = await get_user(user_id)
    assert result is not None
    return result


async def reset_user_password(user_id: str, payload: UserPasswordRequest) -> None:
    async with get_isf_auth_pool().acquire() as conn:
        await conn.execute(
            "INSERT INTO isf_auth.user_credentials (user_id, password_hash) "
            "VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET "
            "password_hash=EXCLUDED.password_hash, updated_at=NOW()",
            user_id, payload.password_hash,
        )


async def update_user_roles(user_id: str, payload: UserRolesRequest) -> UserDetail:
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute("DELETE FROM enterprise.listperanuser WHERE id_user=$1", user_id)
            if payload.roles:
                await conn.executemany(
                    "INSERT INTO enterprise.listperanuser (id_peran, id_user, level_peranuser) "
                    "VALUES ($1, $2, 1) ON CONFLICT DO NOTHING",
                    [(role_id, user_id) for role_id in payload.roles],
                )
    result = await get_user(user_id)
    assert result is not None
    return result


async def update_user_branches(user_id: str, payload: UserBranchesRequest) -> UserDetail:
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute("DELETE FROM enterprise.listcabangdiizinkan WHERE id_user=$1", user_id)
            if payload.branches:
                await conn.executemany(
                    "INSERT INTO enterprise.listcabangdiizinkan (id_user, kode_cabang) "
                    "VALUES ($1, $2) ON CONFLICT DO NOTHING",
                    [(user_id, b) for b in payload.branches],
                )
    result = await get_user(user_id)
    assert result is not None
    return result

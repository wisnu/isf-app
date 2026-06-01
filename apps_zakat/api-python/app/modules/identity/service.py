"""Identity service — live lookup roles/branches/menus dari enterprise.* + isf_auth.role_menu."""

from __future__ import annotations

from app.modules.identity.schema import BranchInfo, ProfileResponse, RoleInfo
from app.shared.db import fetch_all, fetch_all_isf_auth, fetch_one


async def get_profile(user_id: str) -> ProfileResponse | None:
    user = await fetch_one(
        "SELECT id_user, status_profil, kode_cabang, tipe_akses_cabang "
        "FROM enterprise.userapp WHERE id_user = $1",
        user_id,
    )
    if not user:
        return None

    role_rows = await fetch_all(
        """
        SELECT lpu.id_peran, p.nama_peran, lpu.level_peranuser
        FROM enterprise.listperanuser lpu
        JOIN enterprise.peran p USING (id_peran)
        WHERE lpu.id_user = $1 AND p.status_peran = 'A'
        ORDER BY lpu.level_peranuser DESC NULLS LAST, lpu.id_peran
        """,
        user_id,
    )

    branch_rows = await fetch_all(
        "SELECT kode_cabang FROM enterprise.listcabangdiizinkan WHERE id_user = $1 ORDER BY kode_cabang",
        user_id,
    )

    role_ids = [r["id_peran"] for r in role_rows]
    if role_ids:
        # isf_auth sekarang di DB terpisah — pakai pool isf_auth, bukan enterprise pool.
        menu_rows = await fetch_all_isf_auth(
            "SELECT DISTINCT menu_key FROM isf_auth.role_menu WHERE id_peran = ANY($1::text[])",
            role_ids,
        )
    else:
        menu_rows = []

    primary_branch = user.get("kode_cabang")
    branches = [
        BranchInfo(kode_cabang=b["kode_cabang"], is_primary=(b["kode_cabang"] == primary_branch))
        for b in branch_rows
    ]

    return ProfileResponse(
        user_id=user["id_user"],
        status="active" if user.get("status_profil") == "A" else "inactive",
        roles=[
            RoleInfo(id_peran=r["id_peran"], nama_peran=r["nama_peran"], level=r["level_peranuser"])
            for r in role_rows
        ],
        branches=branches,
        menus=sorted({m["menu_key"] for m in menu_rows}),
        primary_branch=primary_branch,
        branch_access="all" if user.get("tipe_akses_cabang") == "S" else "single",
    )

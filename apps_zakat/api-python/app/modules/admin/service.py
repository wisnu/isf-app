"""Admin service — list & replace role-menu mapping.

`enterprise.*` di-query lewat enterprise pool (mziss_laz). `isf_auth.*` di-query
dan ditulis lewat isf_auth pool (isf_auth_zakat). Validasi enterprise.peran
dilakukan read-only; atomic transaction hanya membungkus DELETE+INSERT pada
isf_auth.role_menu (sumber kebenaran mapping role→menu).
"""

from __future__ import annotations

from app.modules.admin.schema import (
    MappingPair, MenuInfo, RoleInfo, RoleMenuDiff, RoleMenuSnapshot, RoleMenuUpdateResponse,
)
from app.shared.db import fetch_all, fetch_all_isf_auth, get_isf_auth_pool


class ValidationError(Exception):
    """Raised dari replace_role_menu kalau input tidak valid."""

    def __init__(self, code: str, message: str, details: list | None = None):
        self.code = code
        self.message = message
        self.details = details or []


async def list_role_menu() -> RoleMenuSnapshot:
    role_rows = await fetch_all(
        """
        SELECT p.id_peran AS role_id, p.nama_peran AS role_name,
               (SELECT count(DISTINCT id_user) FROM enterprise.listperanuser WHERE id_peran = p.id_peran) AS user_count
        FROM enterprise.peran p
        WHERE p.status_peran = 'A'
          AND EXISTS (SELECT 1 FROM enterprise.listperanuser WHERE id_peran = p.id_peran)
        ORDER BY user_count DESC, p.id_peran
        """
    )
    menu_rows = await fetch_all_isf_auth(
        "SELECT menu_key, label, group_label, sort_order FROM isf_auth.menu WHERE status = 'A' ORDER BY sort_order, menu_key"
    )
    mapping_rows = await fetch_all_isf_auth(
        "SELECT id_peran AS role_id, menu_key FROM isf_auth.role_menu ORDER BY id_peran, menu_key"
    )

    return RoleMenuSnapshot(
        roles=[RoleInfo(**r) for r in role_rows],
        menus=[MenuInfo(**m) for m in menu_rows],
        mapping=[MappingPair(**p) for p in mapping_rows],
    )


async def replace_role_menu(
    mapping: list[MappingPair], updated_by: str
) -> RoleMenuUpdateResponse:
    """Atomic replace seluruh isi isf_auth.role_menu dengan snapshot baru.

    Validasi enterprise.peran read-only dari pool enterprise; validasi
    isf_auth.menu + atomic DELETE+INSERT dilakukan dalam satu transaction
    pada pool isf_auth. Cross-pool tidak butuh distributed tx — kedua sisi
    hanya dibaca-tulis pada satu DB masing-masing.
    """
    # 3. Cek duplikat (in-memory, sebelum DB)
    pairs = [(m.role_id, m.menu_key) for m in mapping]
    if len(set(pairs)) != len(pairs):
        seen: set[tuple[str, str]] = set()
        dupes: list[tuple[str, str]] = []
        for p in pairs:
            if p in seen:
                dupes.append(p)
            else:
                seen.add(p)
        raise ValidationError(
            "DUPLICATE_PAIR",
            "Mapping berisi pasangan duplikat",
            details=[f"{a}|{b}" for a, b in dupes],
        )

    # 1. Validate id_peran semua valid — read-only dari enterprise pool.
    input_perans = list({m.role_id for m in mapping})
    if input_perans:
        valid_rows = await fetch_all(
            "SELECT id_peran FROM enterprise.peran WHERE id_peran = ANY($1::text[]) AND status_peran = 'A'",
            input_perans,
        )
        valid_perans = {r["id_peran"] for r in valid_rows}
        invalid = sorted(set(input_perans) - valid_perans)
        if invalid:
            raise ValidationError(
                "INVALID_ROLE",
                "id_peran tidak ada di enterprise.peran aktif",
                details=invalid,
            )

    isf_pool = get_isf_auth_pool()
    async with isf_pool.acquire() as conn:
        async with conn.transaction():
            # 2. Validate menu_key semua valid (di pool yang sama dengan tulisnya)
            input_menus = list({m.menu_key for m in mapping})
            if input_menus:
                valid_rows = await conn.fetch(
                    "SELECT menu_key FROM isf_auth.menu WHERE menu_key = ANY($1::text[]) AND status = 'A'",
                    input_menus,
                )
                valid_menus = {r["menu_key"] for r in valid_rows}
                invalid = sorted(set(input_menus) - valid_menus)
                if invalid:
                    raise ValidationError(
                        "INVALID_MENU",
                        "menu_key tidak ada di isf_auth.menu aktif",
                        details=invalid,
                    )

            # 4. Compute diff vs current state
            current_rows = await conn.fetch("SELECT id_peran, menu_key FROM isf_auth.role_menu")
            current_pairs = {(r["id_peran"], r["menu_key"]) for r in current_rows}
            new_pairs = set(pairs)
            added_pairs = new_pairs - current_pairs
            removed_pairs = current_pairs - new_pairs

            # 5. Atomic replace
            await conn.execute("DELETE FROM isf_auth.role_menu")
            if mapping:
                await conn.executemany(
                    "INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by) VALUES ($1, $2, $3)",
                    [(m.role_id, m.menu_key, updated_by) for m in mapping],
                )

    return RoleMenuUpdateResponse(
        updated=True,
        total_rows=len(mapping),
        diff=RoleMenuDiff(
            added=[MappingPair(role_id=a, menu_key=b) for a, b in sorted(added_pairs)],
            removed=[MappingPair(role_id=a, menu_key=b) for a, b in sorted(removed_pairs)],
        ),
    )

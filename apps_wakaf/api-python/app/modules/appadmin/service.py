"""Admin service — list & replace role-menu mapping.

`enterprise.*` di-query lewat enterprise pool (mziss_wakaf). `isf_auth.*` di-query
dan ditulis lewat isf_auth pool (isf_auth_wakaf). Validasi enterprise.peran
dilakukan read-only; atomic transaction hanya membungkus DELETE+INSERT pada
isf_auth.role_menu (sumber kebenaran mapping role→menu).
"""

from __future__ import annotations

import io

from app.modules.appadmin.schema import (
    VALID_ACTIONS,
    MappingPair,
    MenuInfo,
    MenuPermission,
    RoleInfo,
    RoleMenuDiff,
    RoleMenuPermissionSnapshot,
    RoleMenuPermissionUpdateResponse,
    RoleMenuSnapshot,
    RoleMenuUpdateResponse,
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
            "SELECT id_peran FROM enterprise.peran WHERE id_peran = ANY(CAST($1 AS text[])) AND status_peran = 'A'",
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
                    "SELECT menu_key FROM isf_auth.menu WHERE menu_key = ANY($1) AND status = 'A'",
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


# ── New: action-level permission functions ───────────────────────────────────


def _build_permission_map(rows: list[dict]) -> dict[tuple[str, str], list[str]]:
    """Group action rows into {(role_id, menu_key): [actions]} dict."""
    result: dict[tuple[str, str], list[str]] = {}
    for r in rows:
        key = (r["role_id"], r["menu_key"])
        if key not in result:
            result[key] = []
        result[key].append(r["action"])
    return result


async def list_role_menu_permission(role_id: str) -> RoleMenuPermissionSnapshot:
    """Return roles, menus, and permissions for one role_id."""
    # Validate role exists
    valid = await fetch_all(
        "SELECT id_peran FROM enterprise.peran WHERE id_peran = $1 AND status_peran = 'A'",
        role_id,
    )
    if not valid:
        raise ValidationError("INVALID_ROLE", f"role_id '{role_id}' tidak ditemukan", [role_id])

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
    perm_rows = await fetch_all_isf_auth(
        "SELECT role_id, menu_key, action FROM isf_auth.role_menu_permission WHERE role_id = $1 ORDER BY menu_key, action",
        role_id,
    )

    perm_map = _build_permission_map([dict(r) for r in perm_rows])
    all_menu_keys = [r["menu_key"] for r in menu_rows]
    permissions = [
        MenuPermission(menu_key=mk, actions=perm_map.get((role_id, mk), []))
        for mk in all_menu_keys
    ]

    return RoleMenuPermissionSnapshot(
        roles=[RoleInfo(**r) for r in role_rows],
        menus=[MenuInfo(**m) for m in menu_rows],
        permissions=permissions,
    )


async def replace_role_menu_permission(
    role_id: str,
    permissions: list[MenuPermission],
    updated_by: str,
) -> RoleMenuPermissionUpdateResponse:
    """Atomic replace all permissions for one role_id."""
    # Validate role exists
    valid = await fetch_all(
        "SELECT id_peran FROM enterprise.peran WHERE id_peran = $1 AND status_peran = 'A'",
        role_id,
    )
    if not valid:
        raise ValidationError("INVALID_ROLE", f"role_id '{role_id}' tidak ditemukan", [role_id])

    # Validate all action values
    invalid_actions = [
        f"{p.menu_key}:{a}"
        for p in permissions
        for a in p.actions
        if a not in VALID_ACTIONS
    ]
    if invalid_actions:
        raise ValidationError("INVALID_ACTION", "Action tidak valid", invalid_actions)

    # Collect menu_keys that have at least one action
    input_menu_keys = list({p.menu_key for p in permissions if p.actions})

    isf_pool = get_isf_auth_pool()
    async with isf_pool.acquire() as conn:
        async with conn.transaction():
            if input_menu_keys:
                valid_menu_rows = await conn.fetch(
                    "SELECT menu_key FROM isf_auth.menu WHERE menu_key = ANY($1) AND status = 'A'",
                    input_menu_keys,
                )
                valid_menus = {r["menu_key"] for r in valid_menu_rows}
                invalid_menus = sorted(set(input_menu_keys) - valid_menus)
                if invalid_menus:
                    raise ValidationError("INVALID_MENU", "menu_key tidak valid", invalid_menus)

            # Compute diff
            old_rows = await conn.fetch(
                "SELECT menu_key, action FROM isf_auth.role_menu_permission WHERE role_id = $1",
                role_id,
            )
            old_pairs = {(r["menu_key"], r["action"]) for r in old_rows}
            new_pairs = {
                (p.menu_key, a)
                for p in permissions
                for a in p.actions
            }
            added = len(new_pairs - old_pairs)
            removed = len(old_pairs - new_pairs)

            # Atomic replace for this role
            await conn.execute(
                "DELETE FROM isf_auth.role_menu_permission WHERE role_id = $1", role_id
            )
            if new_pairs:
                await conn.executemany(
                    "INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action, updated_by) VALUES ($1, $2, $3, $4)",
                    [(role_id, mk, action, updated_by) for mk, action in sorted(new_pairs)],
                )

    return RoleMenuPermissionUpdateResponse(
        updated=True,
        role_id=role_id,
        total_pairs=len(new_pairs),
        added_count=added,
        removed_count=removed,
    )


async def export_role_menu_permission_excel() -> bytes:
    """Generate Excel matrix: rows=role x menu, columns=actions."""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        raise RuntimeError("openpyxl not installed")

    role_rows = await fetch_all(
        """
        SELECT p.id_peran AS role_id, p.nama_peran AS role_name
        FROM enterprise.peran p
        WHERE p.status_peran = 'A'
          AND EXISTS (SELECT 1 FROM enterprise.listperanuser WHERE id_peran = p.id_peran)
        ORDER BY p.id_peran
        """
    )
    menu_rows = await fetch_all_isf_auth(
        "SELECT menu_key, label, group_label, sort_order FROM isf_auth.menu WHERE status = 'A' ORDER BY group_label, sort_order, menu_key"
    )
    all_perm_rows = await fetch_all_isf_auth(
        "SELECT role_id, menu_key, action FROM isf_auth.role_menu_permission ORDER BY role_id, menu_key, action"
    )

    perm_set = {(r["role_id"], r["menu_key"], r["action"]) for r in all_perm_rows}
    actions = ["view", "tambah", "edit", "hapus", "detail"]

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Permission Matrix"

    header_fill = PatternFill("solid", fgColor="4472C4")
    header_font = Font(bold=True, color="FFFFFF")
    center = Alignment(horizontal="center")

    # Header row
    ws.cell(row=1, column=1, value="Role ID").font = header_font
    ws.cell(row=1, column=1).fill = header_fill
    ws.cell(row=1, column=2, value="Role Name").font = header_font
    ws.cell(row=1, column=2).fill = header_fill
    ws.cell(row=1, column=3, value="Domain").font = header_font
    ws.cell(row=1, column=3).fill = header_fill
    ws.cell(row=1, column=4, value="Menu").font = header_font
    ws.cell(row=1, column=4).fill = header_fill

    for i, action in enumerate(actions, start=5):
        cell = ws.cell(row=1, column=i, value=action.upper()[:1])
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center

    row_num = 2
    for role in role_rows:
        for menu in menu_rows:
            ws.cell(row=row_num, column=1, value=role["role_id"])
            ws.cell(row=row_num, column=2, value=role["role_name"])
            ws.cell(row=row_num, column=3, value=menu["group_label"])
            ws.cell(row=row_num, column=4, value=menu["label"])
            for i, action in enumerate(actions, start=5):
                has = "v" if (role["role_id"], menu["menu_key"], action) in perm_set else ""
                ws.cell(row=row_num, column=i, value=has).alignment = center
            row_num += 1

    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 18
    ws.column_dimensions["D"].width = 35

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()

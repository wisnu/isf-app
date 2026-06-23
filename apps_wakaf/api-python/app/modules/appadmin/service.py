"""Admin service — list & replace role-menu mapping.

`enterprise.*` di-query lewat enterprise pool (mziss_laz). `isf_auth.*` di-query
dan ditulis lewat isf_auth pool (isf_auth_zakat). Validasi enterprise.peran
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
                    "SELECT menu_key FROM isf_auth.menu WHERE menu_key = ANY(CAST($1 AS text[])) AND status = 'A'",
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


_DOMAIN_ORDER = ["finance", "distribution", "fundraising", "generalaffair", "appadmin", "dashboard"]
_DOMAIN_SORT  = {d: i for i, d in enumerate(_DOMAIN_ORDER)}
_DOMAIN_LABEL = {
    "finance":       "KEUANGAN",
    "distribution":  "PROGRAM / PENYALURAN",
    "fundraising":   "PENGHIMPUNAN",
    "generalaffair": "ADMINISTRASI & UMUM",
    "appadmin":      "PENGATURAN AKSES",
    "dashboard":     "DASHBOARD",
}
_ACTION_LABELS = [
    ("view",   "List (Lihat Daftar)"),
    ("tambah", "Create (Tambah Data)"),
    ("detail", "Read (Detail Data)"),
    ("edit",   "Edit (Ubah Data)"),
    ("hapus",  "Delete (Hapus Data)"),
]


async def export_role_menu_permission_excel(
    role_id: str | None = None,
    domain: str | None = None,
) -> bytes:
    """Generate Excel — rows = menu × action, columns = roles (matches UI layout).

    role_id: filter to one role (None = all roles)
    domain:  filter to one domain prefix e.g. 'finance' (None = all domains)
    """
    try:
        import openpyxl
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    except ImportError:
        raise RuntimeError("openpyxl not installed")

    # ── Roles ──
    if role_id:
        role_rows = await fetch_all(
            "SELECT p.id_peran AS role_id, p.nama_peran AS role_name FROM enterprise.peran p WHERE p.status_peran = 'A' AND p.id_peran = $1",
            role_id,
        )
    else:
        role_rows = await fetch_all(
            """
            SELECT p.id_peran AS role_id, p.nama_peran AS role_name
            FROM enterprise.peran p
            WHERE p.status_peran = 'A'
              AND EXISTS (SELECT 1 FROM enterprise.listperanuser WHERE id_peran = p.id_peran)
            ORDER BY p.id_peran
            """
        )

    # ── Menus ──
    if domain:
        menu_rows = await fetch_all_isf_auth(
            "SELECT menu_key, label, group_label, sort_order FROM isf_auth.menu WHERE status = 'A' AND menu_key LIKE $1 ORDER BY sort_order, menu_key",
            f"{domain}.%",
        )
    else:
        menu_rows = await fetch_all_isf_auth(
            "SELECT menu_key, label, group_label, sort_order FROM isf_auth.menu WHERE status = 'A' ORDER BY sort_order, menu_key"
        )

    def _domain_prefix(key: str) -> str:
        return key.split(".")[0]

    menu_rows = sorted(
        menu_rows,
        key=lambda m: (_DOMAIN_SORT.get(_domain_prefix(m["menu_key"]), 99), m["sort_order"], m["menu_key"]),
    )

    # Group menus by domain
    from collections import OrderedDict
    domain_groups: dict[str, list] = OrderedDict()
    for m in menu_rows:
        d = _domain_prefix(m["menu_key"])
        if d not in domain_groups:
            domain_groups[d] = []
        domain_groups[d].append(m)

    # ── Permissions ──
    role_ids = [r["role_id"] for r in role_rows]
    perm_set: set = set()
    if role_ids:
        perm_rows = await fetch_all_isf_auth(
            "SELECT role_id, menu_key, action FROM isf_auth.role_menu_permission WHERE role_id = ANY(CAST($1 AS text[]))",
            role_ids,
        )
        perm_set = {(r["role_id"], r["menu_key"], r["action"]) for r in perm_rows}

    # ── Build workbook ──
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Permission Matrix"

    # Styles
    hdr_fill   = PatternFill("solid", fgColor="1F2937")   # dark header (matches UI)
    hdr_font   = Font(bold=True, color="FFFFFF", size=9)
    dom_fill   = PatternFill("solid", fgColor="374151")   # domain row
    dom_font   = Font(bold=True, color="FFFFFF", size=9)
    menu_fill  = PatternFill("solid", fgColor="F3F4F6")   # menu header row
    menu_font  = Font(bold=True, color="374151", size=9)
    act_font   = Font(size=9, color="4B5563")
    chk_font   = Font(size=9, color="1D4ED8", bold=True)
    center_al  = Alignment(horizontal="center", vertical="center")
    left_al    = Alignment(horizontal="left",   vertical="center")
    thin_side  = Side(style="thin", color="D1D5DB")
    thin_bdr   = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    n_roles = len(role_rows)
    last_col = n_roles + 1  # col 1 = menu label, col 2..n_roles+1 = roles

    # ── Row 1: header ──
    cell = ws.cell(row=1, column=1, value="Menu & Hak Akses")
    cell.font = hdr_font; cell.fill = hdr_fill; cell.alignment = left_al; cell.border = thin_bdr
    for ci, role in enumerate(role_rows, start=2):
        cell = ws.cell(row=1, column=ci, value=role["role_name"].upper())
        cell.font = hdr_font; cell.fill = hdr_fill; cell.alignment = center_al; cell.border = thin_bdr

    ws.freeze_panes = "B2"
    ws.row_dimensions[1].height = 28

    row_num = 2
    for d_key, menus in domain_groups.items():
        # ── Domain section header ──
        ws.merge_cells(start_row=row_num, start_column=1, end_row=row_num, end_column=last_col)
        cell = ws.cell(row=row_num, column=1, value=_DOMAIN_LABEL.get(d_key, d_key.upper()))
        cell.font = dom_font; cell.fill = dom_fill; cell.alignment = left_al; cell.border = thin_bdr
        ws.row_dimensions[row_num].height = 18
        row_num += 1

        for menu in menus:
            # ── Menu sub-header ──
            ws.merge_cells(start_row=row_num, start_column=1, end_row=row_num, end_column=last_col)
            cell = ws.cell(row=row_num, column=1, value=f"📁  {menu['label']}")
            cell.font = menu_font; cell.fill = menu_fill; cell.alignment = left_al; cell.border = thin_bdr
            ws.row_dimensions[row_num].height = 16
            row_num += 1

            # ── Action rows ──
            for action_key, action_label in _ACTION_LABELS:
                cell = ws.cell(row=row_num, column=1, value=f"    ↳  {action_label}")
                cell.font = act_font; cell.alignment = left_al; cell.border = thin_bdr
                for ci, role in enumerate(role_rows, start=2):
                    has = (role["role_id"], menu["menu_key"], action_key) in perm_set
                    cell = ws.cell(row=row_num, column=ci, value="✓" if has else "")
                    cell.font = chk_font if has else act_font
                    cell.alignment = center_al
                    cell.border = thin_bdr
                ws.row_dimensions[row_num].height = 15
                row_num += 1

    # ── Column widths ──
    ws.column_dimensions["A"].width = 38
    # Role columns: narrow
    for ci in range(2, n_roles + 2):
        col_letter = ws.cell(row=1, column=ci).column_letter
        ws.column_dimensions[col_letter].width = max(14, len(role_rows[ci - 2]["role_name"]) + 2)

    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.read()

# Role-Menu Action-Level Permission — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the boolean `role_menu` table with `role_menu_permission` (role × menu × action), add a role-first UI with accordion domains and 5 action checkboxes per menu, and an Excel export of the full matrix.

**Architecture:** New table `isf_auth.role_menu_permission(role_id, menu_key, action)` replaces `isf_auth.role_menu`. The BFF fetches action-aware menus at login (stored in Pinia, not cookie). The frontend exposes a `usePermission(menuKey)` composable for `canView/canAdd/canEdit/canDelete/canDetail` checks. The role-menu admin page is redesigned to role-first: pick a role, see accordion groups with 5-column action checkboxes.

**Tech Stack:** PostgreSQL 15 · FastAPI + asyncpg · openpyxl · Vue 3.5 + Pinia · Tailwind 4 · PrimeVue unstyled

## Global Constraints

- All SQL: use `CAST(x AS type)` — never `x::type`
- All Python identifiers: English snake_case
- All Vue files: `<script setup lang="ts">` — no Options API
- HTTP from FE: only via `shared/api/client.ts` (`GET`, `POST`, `blob`)
- DB credentials on host: `transaction:solusi`
- Auth DB names: `isf_auth_zakat`, `isf_auth_wakaf`
- Business DB names: `mziss_laz`, `mziss_wakaf`
- Apply all isf_auth migrations to **both** auth DBs
- Valid action values: `'view'`, `'tambah'`, `'edit'`, `'hapus'`, `'detail'`
- Checking a non-view action must auto-check `view`; unchecking `view` must clear all actions

---

## File Map

| File | Action |
|---|---|
| `infra/db/migrations/isf_auth/add-role-menu-permission.sql` | Create |
| `apps_zakat/api-python/app/modules/appadmin/schema.py` | Modify — add permission models |
| `apps_zakat/api-python/app/modules/appadmin/service.py` | Modify — add 3 new functions |
| `apps_zakat/api-python/app/modules/appadmin/router.py` | Modify — add 3 new endpoints |
| `apps_zakat/bff-api/app/services/auth_db.py` | Modify — update `get_menus_by_roles()` |
| `apps_zakat/bff-api/app/services/auth.py` | Modify — update cache type + `require_menu()` |
| `apps_zakat/bff-api/app/modules/appadmin/admin.py` | Modify — add 3 new BFF endpoints |
| `apps_zakat/web-vue/src/app/stores/auth.store.ts` | Modify — new `User` type + `menuActions` |
| `apps_zakat/web-vue/src/shared/composables/usePermission.ts` | Create |
| `apps_zakat/web-vue/src/modules/appadmin/views/role-menu/RoleMenuView.vue` | Modify — redesign |
| `testing/e2e-role-menu-permission.sh` | Create |

Mirror steps to `apps_wakaf/` after zakat is validated (Task 6).

---

## Task 1: DB Migration

**Files:**
- Create: `infra/db/migrations/isf_auth/add-role-menu-permission.sql`

**Interfaces:**
- Produces: table `isf_auth.role_menu_permission(id, role_id, menu_key, action, updated_by, updated_at)` + unique constraint `(role_id, menu_key, action)`; all existing `role_menu` data migrated as `action='view'`; `role_menu` table dropped

- [ ] **Step 1: Write the migration SQL**

Create `infra/db/migrations/isf_auth/add-role-menu-permission.sql`:

```sql
-- Migration: replace role_menu with role_menu_permission
-- Apply to both isf_auth_zakat and isf_auth_wakaf

BEGIN;

-- 1. Create new table
CREATE TABLE IF NOT EXISTS isf_auth.role_menu_permission (
    id          SERIAL PRIMARY KEY,
    role_id     VARCHAR(50)  NOT NULL,
    menu_key    VARCHAR(100) NOT NULL,
    action      VARCHAR(20)  NOT NULL
                CHECK (action IN ('view','tambah','edit','hapus','detail')),
    updated_by  VARCHAR(100),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_role_menu_action UNIQUE (role_id, menu_key, action)
);

-- 2. Migrate all existing role_menu rows → action='view'
INSERT INTO isf_auth.role_menu_permission (role_id, menu_key, action)
SELECT id_peran, menu_key, 'view'
FROM isf_auth.role_menu
ON CONFLICT (role_id, menu_key, action) DO NOTHING;

-- 3. Drop old table (BFF must be updated before this runs in prod)
DROP TABLE IF EXISTS isf_auth.role_menu;

COMMIT;
```

- [ ] **Step 2: Apply to zakat auth DB**

```bash
psql -U transaction -d isf_auth_zakat -h localhost \
  -f infra/db/migrations/isf_auth/add-role-menu-permission.sql
```

Expected output: `CREATE TABLE` → `INSERT 0 N` → `DROP TABLE` → `COMMIT`

- [ ] **Step 3: Apply to wakaf auth DB**

```bash
psql -U transaction -d isf_auth_wakaf -h localhost \
  -f infra/db/migrations/isf_auth/add-role-menu-permission.sql
```

Expected output: same as above

- [ ] **Step 4: Verify**

```bash
psql -U transaction -d isf_auth_zakat -h localhost -c \
  "SELECT role_id, menu_key, action FROM isf_auth.role_menu_permission LIMIT 5;"
```

Expected: rows with `action='view'` for existing mappings. No `role_menu` table.

- [ ] **Step 5: Commit**

```bash
git add infra/db/migrations/isf_auth/add-role-menu-permission.sql
git commit -m "[ROLE-MENU] feat(db): replace role_menu with role_menu_permission

Adds role_menu_permission(role_id, menu_key, action) with CHECK constraint.
Migrates all existing rows to action='view'. Drops role_menu.

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: api-python — Schema + Service + Router

**Files:**
- Modify: `apps_zakat/api-python/app/modules/appadmin/schema.py`
- Modify: `apps_zakat/api-python/app/modules/appadmin/service.py`
- Modify: `apps_zakat/api-python/app/modules/appadmin/router.py`

**Interfaces:**
- Consumes: `isf_auth.role_menu_permission` table (from Task 1); `isf_auth.menu` table; `enterprise.peran` table
- Produces:
  - `GET /api/appadmin/role-menu-permission` → `RoleMenuPermissionSnapshot`
  - `PUT /api/appadmin/role-menu-permission` → `RoleMenuPermissionUpdateResponse`
  - `GET /api/appadmin/role-menu-permission/export` → Excel bytes (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`)

- [ ] **Step 1: Write pytest for service functions**

Create `apps_zakat/api-python/tests/appadmin/test_permission_service.py`:

```python
"""Unit tests for role_menu_permission service logic."""
import pytest
from unittest.mock import AsyncMock, patch

from app.modules.appadmin.service import (
    _build_permission_map,
    ValidationError,
)


def test_build_permission_map_groups_actions():
    rows = [
        {"role_id": "KEU", "menu_key": "finance.dashboard", "action": "view"},
        {"role_id": "KEU", "menu_key": "finance.dashboard", "action": "tambah"},
        {"role_id": "ADM", "menu_key": "finance.dashboard", "action": "view"},
    ]
    result = _build_permission_map(rows)
    assert set(result[("KEU", "finance.dashboard")]) == {"view", "tambah"}
    assert set(result[("ADM", "finance.dashboard")]) == {"view"}


def test_build_permission_map_empty():
    result = _build_permission_map([])
    assert result == {}
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
cd apps_zakat/api-python && python -m pytest tests/appadmin/test_permission_service.py -v
```

Expected: `ImportError` or `AttributeError` — `_build_permission_map` does not exist yet

- [ ] **Step 3: Update schema.py**

Replace full content of `apps_zakat/api-python/app/modules/appadmin/schema.py`:

```python
from pydantic import BaseModel


class RoleInfo(BaseModel):
    role_id: str
    role_name: str
    user_count: int


class MenuInfo(BaseModel):
    menu_key: str
    label: str
    group_label: str
    sort_order: int


class MappingPair(BaseModel):
    role_id: str
    menu_key: str


class RoleMenuSnapshot(BaseModel):
    roles: list[RoleInfo]
    menus: list[MenuInfo]
    mapping: list[MappingPair]


class RoleMenuUpdateRequest(BaseModel):
    mapping: list[MappingPair]
    updated_by: str


class RoleMenuDiff(BaseModel):
    added: list[MappingPair]
    removed: list[MappingPair]


class RoleMenuUpdateResponse(BaseModel):
    updated: bool
    total_rows: int
    diff: RoleMenuDiff


# ── New: action-level permission models ──────────────────────────────────────

VALID_ACTIONS = frozenset({"view", "tambah", "edit", "hapus", "detail"})


class MenuPermission(BaseModel):
    menu_key: str
    actions: list[str]


class RoleMenuPermissionSnapshot(BaseModel):
    roles: list[RoleInfo]
    menus: list[MenuInfo]
    permissions: list[MenuPermission]  # scoped to one role_id


class RoleMenuPermissionUpdateRequest(BaseModel):
    role_id: str
    permissions: list[MenuPermission]
    updated_by: str


class RoleMenuPermissionUpdateResponse(BaseModel):
    updated: bool
    role_id: str
    total_pairs: int
    added_count: int
    removed_count: int


class AllRolesPermissionSnapshot(BaseModel):
    roles: list[RoleInfo]
    menus: list[MenuInfo]
    all_permissions: list[dict]  # [{role_id, menu_key, action}]
```

- [ ] **Step 4: Add helper + new service functions to service.py**

Add to end of `apps_zakat/api-python/app/modules/appadmin/service.py`:

```python
# ── New: action-level permission functions ───────────────────────────────────

from app.modules.appadmin.schema import (
    VALID_ACTIONS, AllRolesPermissionSnapshot, MenuPermission,
    RoleMenuPermissionSnapshot, RoleMenuPermissionUpdateRequest,
    RoleMenuPermissionUpdateResponse,
)
import io


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

    # Validate all menu_keys and action values
    input_menu_keys = list({p.menu_key for p in permissions if p.actions})
    invalid_actions = [
        f"{p.menu_key}:{a}"
        for p in permissions
        for a in p.actions
        if a not in VALID_ACTIONS
    ]
    if invalid_actions:
        raise ValidationError("INVALID_ACTION", "Action tidak valid", invalid_actions)

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
    """Generate Excel matrix: rows=roles × menus, columns=actions."""
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

    role_map = {r["role_id"]: r["role_name"] for r in role_rows}
    row_num = 2
    for role in role_rows:
        for menu in menu_rows:
            ws.cell(row=row_num, column=1, value=role["role_id"])
            ws.cell(row=row_num, column=2, value=role["role_name"])
            ws.cell(row=row_num, column=3, value=menu["group_label"])
            ws.cell(row=row_num, column=4, value=menu["label"])
            for i, action in enumerate(actions, start=5):
                has = "✓" if (role["role_id"], menu["menu_key"], action) in perm_set else ""
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
```

- [ ] **Step 5: Run tests — should pass now**

```bash
cd apps_zakat/api-python && python -m pytest tests/appadmin/test_permission_service.py -v
```

Expected: 2 PASSED

- [ ] **Step 6: Add 3 new endpoints to router.py**

Add to end of `apps_zakat/api-python/app/modules/appadmin/router.py`:

```python
from fastapi.responses import StreamingResponse
import io
from app.modules.appadmin.schema import RoleMenuPermissionUpdateRequest
from app.modules.appadmin.service import (
    list_role_menu_permission,
    replace_role_menu_permission,
    export_role_menu_permission_excel,
)


@router.get("/role-menu-permission")
async def get_role_menu_permission(role_id: str):
    snapshot = await list_role_menu_permission(role_id)
    return ok(snapshot.model_dump())


@router.put("/role-menu-permission")
async def put_role_menu_permission(payload: RoleMenuPermissionUpdateRequest):
    try:
        result = await replace_role_menu_permission(
            payload.role_id, payload.permissions, payload.updated_by
        )
    except ValidationError as exc:
        return JSONResponse(
            status_code=400,
            content=err(exc.code, exc.message, details=exc.details),
        )
    return ok(result.model_dump())


@router.get("/role-menu-permission/export")
async def export_role_menu_permission():
    xlsx_bytes = await export_role_menu_permission_excel()
    return StreamingResponse(
        io.BytesIO(xlsx_bytes),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=role-menu-permission.xlsx"},
    )
```

- [ ] **Step 7: Smoke-test api-python endpoints**

```bash
# Confirm api-python starts
cd apps_zakat/api-python && python -m pytest tests/ -v -k "permission"

# Or via running service:
curl -s "http://localhost:8000/api/appadmin/role-menu-permission?role_id=KEU" | python -m json.tool | head -20
```

Expected: JSON with `roles`, `menus`, `permissions` keys

- [ ] **Step 8: Commit**

```bash
git add apps_zakat/api-python/app/modules/appadmin/schema.py \
        apps_zakat/api-python/app/modules/appadmin/service.py \
        apps_zakat/api-python/app/modules/appadmin/router.py \
        apps_zakat/api-python/tests/appadmin/test_permission_service.py
git commit -m "[ROLE-MENU] feat(api-python): add role-menu-permission endpoints and export

GET/PUT /appadmin/role-menu-permission + GET /role-menu-permission/export.
Service replaces per-role atomic replace with action-level granularity.
Excel export: flat table rows=role×menu, columns=V/T/E/H/D.

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: BFF — auth_db + auth.py + admin.py

**Files:**
- Modify: `apps_zakat/bff-api/app/services/auth_db.py` (line 162–170)
- Modify: `apps_zakat/bff-api/app/services/auth.py`
- Modify: `apps_zakat/bff-api/app/modules/appadmin/admin.py`

**Interfaces:**
- Consumes: `isf_auth.role_menu_permission` (Task 1); api-python endpoints (Task 2)
- Produces:
  - `get_menus_by_roles()` returns `list[dict]` with `{menu_key, actions}`
  - Login/me response `menus` field: `[{menu_key, actions[]}]`
  - `require_menu(key)` still gates on `action='view'`
  - BFF exposes `GET/PUT /api/appadmin/role-menu-permission` + `GET /api/appadmin/role-menu-permission/export`

- [ ] **Step 1: Update get_menus_by_roles() in auth_db.py**

In `apps_zakat/bff-api/app/services/auth_db.py`, replace lines 162–170:

```python
# OLD:
async def get_menus_by_roles(self, roles: list[str]) -> list[str]:
    """Return distinct menu_keys assigned to the given role ids."""
    if not roles:
        return []
    rows = await fetch_all(
        "SELECT DISTINCT menu_key FROM isf_auth.role_menu WHERE id_peran = ANY($1)",
        roles,
    )
    return [r["menu_key"] for r in rows]

# NEW:
async def get_menus_by_roles(self, roles: list[str]) -> list[dict]:
    """Return menu permissions for roles as [{menu_key, actions[]}].

    Aggregates across all roles — union of actions per menu_key.
    """
    if not roles:
        return []
    rows = await fetch_all(
        """
        SELECT menu_key,
               array_agg(DISTINCT action ORDER BY action) AS actions
        FROM isf_auth.role_menu_permission
        WHERE role_id = ANY($1)
        GROUP BY menu_key
        ORDER BY menu_key
        """,
        roles,
    )
    return [{"menu_key": r["menu_key"], "actions": list(r["actions"])} for r in rows]
```

- [ ] **Step 2: Update _menu_cache type and require_menu() in auth.py**

In `apps_zakat/bff-api/app/services/auth.py`, make these changes:

```python
# Line 18 — update cache type annotation:
# OLD:
_menu_cache: dict[frozenset, tuple[list[str], float]] = {}
# NEW:
_menu_cache: dict[frozenset, tuple[list[dict], float]] = {}

# Lines 22-30 — update return type annotation:
# OLD:
async def get_menus_for_roles(roles: list[str], db: AuthDB) -> list[str]:
# NEW:
async def get_menus_for_roles(roles: list[str], db: AuthDB) -> list[dict]:

# Lines 127-128 — update require_menu() check:
# OLD:
menus = await get_menus_for_roles(roles, db)
if menu_key not in menus:
# NEW:
menus = await get_menus_for_roles(roles, db)
if not any(m["menu_key"] == menu_key for m in menus):
```

- [ ] **Step 3: Verify BFF auth still works (login + me)**

```bash
# Login and check menus shape
curl -s -c /tmp/cookies.txt -X POST http://localhost:7000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}' | python -m json.tool | grep -A5 '"menus"'
```

Expected: `menus` field is now array of `{"menu_key": "...", "actions": ["view", ...]}` objects

- [ ] **Step 4: Add BFF endpoints for role-menu-permission in admin.py**

Add to `apps_zakat/bff-api/app/modules/appadmin/admin.py` after the existing `/role-menu` endpoints (after line 93):

```python
from fastapi.responses import StreamingResponse as BFFStreamingResponse
from app.services.proxy import get_api_python_raw


class RoleMenuPermissionIn(BaseModel):
    menu_key: str
    actions: list[str]


class RoleMenuPermissionUpdateIn(BaseModel):
    role_id: str
    permissions: list[RoleMenuPermissionIn]


@router.get("/role-menu-permission")
async def get_role_menu_permission(
    role_id: str,
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    downstream = await get_api_python(
        "/api/appadmin/role-menu-permission", params={"role_id": role_id}
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/role-menu-permission")
async def put_role_menu_permission(
    payload: RoleMenuPermissionUpdateIn,
    request: Request,
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    body = {
        "role_id": payload.role_id,
        "permissions": [p.model_dump() for p in payload.permissions],
        "updated_by": user_id,
    }
    downstream = await post_api_python(
        "/api/appadmin/role-menu-permission", json_body=body, method="PUT"
    )

    audit = getattr(request.app.state, "audit", None)
    if audit is not None and downstream.status_code == 200:
        try:
            result = downstream.json().get("data", {})
            await audit.log(
                "role_menu_permission_updated",
                user_id=user_id,
                payload={
                    "role_id": payload.role_id,
                    "added_count": result.get("added_count"),
                    "removed_count": result.get("removed_count"),
                },
            )
        except Exception:
            pass

    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/role-menu-permission/export")
async def export_role_menu_permission(
    user_id: str = Depends(require_menu("appadmin.role_menu")),
):
    downstream = await get_api_python_raw("/api/appadmin/role-menu-permission/export")
    return BFFStreamingResponse(
        content=downstream.aiter_bytes(),
        status_code=downstream.status_code,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=role-menu-permission.xlsx"},
    )
```

> Note: If `get_api_python_raw` does not exist in `app/services/proxy.py`, add a variant that returns the raw httpx response without calling `.json()`. Check `proxy.py` first — if there is already a streaming proxy pattern (e.g., `stream_report_api`), use that instead.

- [ ] **Step 5: Smoke-test BFF endpoints**

```bash
# Login first
curl -s -c /tmp/c.txt -X POST http://localhost:7000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}' > /dev/null

# GET permissions for role KEU
curl -s -b /tmp/c.txt \
  "http://localhost:7000/api/appadmin/role-menu-permission?role_id=KEU" \
  | python -m json.tool | head -20
```

Expected: `{"data": {"roles": [...], "menus": [...], "permissions": [...]}, "meta": {...}}`

- [ ] **Step 6: Commit**

```bash
git add apps_zakat/bff-api/app/services/auth_db.py \
        apps_zakat/bff-api/app/services/auth.py \
        apps_zakat/bff-api/app/modules/appadmin/admin.py
git commit -m "[ROLE-MENU] feat(bff): update menu cache + add role-menu-permission proxy endpoints

get_menus_by_roles now returns [{menu_key, actions[]}] from role_menu_permission.
require_menu checks action='view' presence. Adds GET/PUT/export BFF proxy.

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: web-vue — Auth Store + usePermission Composable

**Files:**
- Modify: `apps_zakat/web-vue/src/app/stores/auth.store.ts`
- Create: `apps_zakat/web-vue/src/shared/composables/usePermission.ts`

**Interfaces:**
- Consumes: BFF `menus` field from `/api/auth/login` and `/api/auth/me` (now `{menu_key, actions[]}[]`)
- Produces:
  - `auth.menus` computed — `string[]` (backward compat: list of menu_keys)
  - `auth.menuActions` computed — `Record<string, string[]>` (new: action lookup)
  - `auth.hasMenu(key)` — still works, now uses `.some()` internally
  - `usePermission(menuKey)` — returns `{canView, canAdd, canEdit, canDelete, canDetail}` as `ComputedRef<boolean>`

- [ ] **Step 1: Update auth.store.ts**

Replace `apps_zakat/web-vue/src/app/stores/auth.store.ts` with:

```typescript
import { computed, shallowRef } from 'vue'
import { acceptHMRUpdate, defineStore } from 'pinia'

import { api, ApiError } from '@/shared/api/client'
import type { MenuKey } from '@/shared/constants/menu-keys'

export interface Tenant { id: string; name: string }

export interface MenuPermission {
  menu_key: string
  actions: string[]
}

export interface User {
  username: string
  name: string
  tenants: Tenant[]
  default_tenant: string | null
  roles: string[]
  branches: string[]
  primary_branch: string | null
  menus: MenuPermission[]
  branch_access?: 'all' | 'single'
}

export interface AuthProviders {
  password: boolean
  google: boolean
}

export const useAuthStore = defineStore('auth', () => {
  const initialized = shallowRef(false)
  const user = shallowRef<User | null>(null)
  const activeTenantId = shallowRef<string | null>(null)
  const providers = shallowRef<AuthProviders>({ password: true, google: false })
  const providersLoaded = shallowRef(false)

  const activeTenant = computed<Tenant | null>(() => {
    if (!user.value || !activeTenantId.value) return null
    return user.value.tenants.find((t) => t.id === activeTenantId.value) ?? null
  })
  const hasTenant = computed(() => Boolean(activeTenantId.value))

  // Backward-compat: list of menu_keys the user has 'view' access to
  const menus = computed<string[]>(() =>
    user.value?.menus.map(m => m.menu_key) ?? []
  )

  // New: action lookup by menu_key
  const menuActions = computed<Record<string, string[]>>(() => {
    if (!user.value) return {}
    return Object.fromEntries(user.value.menus.map(m => [m.menu_key, m.actions]))
  })

  function hasMenu(key: MenuKey | string): boolean {
    return Boolean(user.value?.menus.some(m => m.menu_key === key))
  }

  async function loadProviders() {
    if (providersLoaded.value) return
    try {
      const result = await api.get<AuthProviders>('/api/auth/providers')
      providers.value = result
    } catch {
      // fallback to defaults
    } finally {
      providersLoaded.value = true
    }
  }

  async function bootstrap() {
    try {
      const me = await api.get<{ user: User; active_tenant_id: string | null }>('/api/auth/me')
      user.value = me.user
      activeTenantId.value = me.active_tenant_id
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        user.value = null
        activeTenantId.value = null
      } else {
        throw e
      }
    } finally {
      initialized.value = true
    }
  }

  async function login(username: string, password: string) {
    const result = await api.post<{ user: User; active_tenant_id: string }>(
      '/api/auth/login', { username, password },
    )
    user.value = result.user
    activeTenantId.value = result.active_tenant_id
  }

  async function logout() {
    try {
      await api.post('/api/auth/logout')
    } finally {
      user.value = null
      activeTenantId.value = null
    }
  }

  async function switchTenant(tenantId: string) {
    const result = await api.post<{ active_tenant_id: string }>(
      '/api/tenants/switch', { tenant_id: tenantId },
    )
    activeTenantId.value = result.active_tenant_id
  }

  async function refreshProfile() {
    await api.post('/api/auth/refresh-profile')
    const me = await api.get<{ user: User; active_tenant_id: string | null }>('/api/auth/me')
    user.value = me.user
    activeTenantId.value = me.active_tenant_id
  }

  return {
    initialized,
    user,
    activeTenantId,
    providers,
    providersLoaded,
    activeTenant,
    hasTenant,
    menus,
    menuActions,
    hasMenu,
    loadProviders,
    bootstrap,
    login,
    logout,
    switchTenant,
    refreshProfile,
  }
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
}
```

- [ ] **Step 2: Create usePermission.ts**

Create `apps_zakat/web-vue/src/shared/composables/usePermission.ts`:

```typescript
import { computed } from 'vue'
import { useAuthStore } from '@/app/stores/auth.store'

export function usePermission(menuKey: string) {
  const auth = useAuthStore()
  const actions = computed(() => auth.menuActions[menuKey] ?? [])
  return {
    canView:   computed(() => actions.value.includes('view')),
    canAdd:    computed(() => actions.value.includes('tambah')),
    canEdit:   computed(() => actions.value.includes('edit')),
    canDelete: computed(() => actions.value.includes('hapus')),
    canDetail: computed(() => actions.value.includes('detail')),
  }
}
```

- [ ] **Step 3: TypeScript check**

```bash
cd apps_zakat/web-vue && npx tsc --noEmit 2>&1 | head -30
```

Expected: 0 errors. If there are errors about `menus.includes(key)` in other components — those still work because `auth.menus` computed returns `string[]`.

- [ ] **Step 4: Commit**

```bash
git add apps_zakat/web-vue/src/app/stores/auth.store.ts \
        apps_zakat/web-vue/src/shared/composables/usePermission.ts
git commit -m "[ROLE-MENU] feat(web-vue): update auth store for action-level menus + usePermission

User.menus is now MenuPermission[]. menus computed stays string[] for compat.
menuActions computed adds Record<menu_key, actions[]>. New usePermission(key)
composable exposes canView/canAdd/canEdit/canDelete/canDetail.

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: web-vue — RoleMenuView Redesign

**Files:**
- Modify: `apps_zakat/web-vue/src/modules/appadmin/views/role-menu/RoleMenuView.vue`

**Interfaces:**
- Consumes:
  - `GET /api/appadmin/role-menu-permission?role_id=X` → `{ data: { roles, menus, permissions } }`
  - `PUT /api/appadmin/role-menu-permission` body: `{ role_id, permissions: [{menu_key, actions[]}] }`
  - `GET /api/appadmin/role-menu-permission/export` → Excel blob download
- Produces: redesigned page with role picker + accordion domain groups + 5-action checkbox matrix

- [ ] **Step 1: Check existing shared components available**

```bash
ls apps_zakat/web-vue/src/shared/components/
```

Confirm these exist: `SearchSelect.vue`, `Button.vue` (or `Button` export), `Alert.vue`, layout components used in current `RoleMenuView.vue`.

- [ ] **Step 2: Write the new RoleMenuView.vue**

Replace full content of `apps_zakat/web-vue/src/modules/appadmin/views/role-menu/RoleMenuView.vue`:

```vue
<script setup lang="ts">
import { ref, computed, watch, onBeforeUnmount } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { ChevronDown, ChevronRight, RefreshCw, Save, X, Download } from 'lucide-vue-next'

import { api } from '@/shared/api/client'
import { downloadBlob } from '@/shared/utils/download'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import Button from '@/shared/components/Button.vue'
import Alert from '@/shared/components/Alert.vue'

// ── Types ────────────────────────────────────────────────────────────────────

interface RoleInfo   { role_id: string; role_name: string; user_count: number }
interface MenuInfo   { menu_key: string; label: string; group_label: string; sort_order: number }
interface MenuPermission { menu_key: string; actions: string[] }

interface Snapshot {
  roles: RoleInfo[]
  menus: MenuInfo[]
  permissions: MenuPermission[]
}

const ACTIONS = [
  { key: 'view',   label: 'V', title: 'View' },
  { key: 'tambah', label: 'T', title: 'Tambah' },
  { key: 'edit',   label: 'E', title: 'Edit' },
  { key: 'hapus',  label: 'H', title: 'Hapus' },
  { key: 'detail', label: 'D', title: 'View Detail' },
] as const

type ActionKey = typeof ACTIONS[number]['key']

// ── State ────────────────────────────────────────────────────────────────────

const loading    = ref(false)
const saving     = ref(false)
const exporting  = ref(false)
const error      = ref('')
const success    = ref('')

const allRoles   = ref<RoleInfo[]>([])
const allMenus   = ref<MenuInfo[]>([])
const selectedRoleId = ref<string | null>(null)

// current: menu_key → Set of actions (editable copy)
// original: menu_key → Set of actions (snapshot for dirty tracking)
const current  = ref(new Map<string, Set<string>>())
const original = ref(new Map<string, Set<string>>())

const expandedGroups = ref(new Set<string>())

// ── Derived ──────────────────────────────────────────────────────────────────

const roleOptions = computed(() =>
  allRoles.value.map(r => ({
    value: r.role_id,
    label: `${r.role_id} — ${r.role_name}`,
  }))
)

const groupedMenus = computed(() => {
  const groups = new Map<string, MenuInfo[]>()
  for (const menu of allMenus.value) {
    if (!groups.has(menu.group_label)) groups.set(menu.group_label, [])
    groups.get(menu.group_label)!.push(menu)
  }
  return Array.from(groups.entries()).map(([label, menus]) => ({ label, menus }))
})

const isDirty = computed(() => {
  if (current.value.size !== original.value.size) return true
  for (const [mk, acts] of current.value) {
    const orig = original.value.get(mk) ?? new Set<string>()
    if (acts.size !== orig.size) return true
    for (const a of acts) if (!orig.has(a)) return true
  }
  return false
})

const dirtyCount = computed(() => {
  let count = 0
  const allKeys = new Set([...current.value.keys(), ...original.value.keys()])
  for (const mk of allKeys) {
    const curr = current.value.get(mk) ?? new Set<string>()
    const orig = original.value.get(mk) ?? new Set<string>()
    for (const a of ACTIONS.map(a => a.key)) {
      if (curr.has(a) !== orig.has(a)) count++
    }
  }
  return count
})

// ── Helpers ──────────────────────────────────────────────────────────────────

function hasAction(menuKey: string, action: string): boolean {
  return current.value.get(menuKey)?.has(action) ?? false
}

function isDirtyCell(menuKey: string, action: string): boolean {
  const curr = current.value.get(menuKey)?.has(action) ?? false
  const orig = original.value.get(menuKey)?.has(action) ?? false
  return curr !== orig
}

function activeMenuCount(group: { menus: MenuInfo[] }): number {
  return group.menus.filter(m => (current.value.get(m.menu_key)?.size ?? 0) > 0).length
}

function cloneMap(src: Map<string, Set<string>>): Map<string, Set<string>> {
  return new Map(Array.from(src.entries()).map(([k, v]) => [k, new Set(v)]))
}

function applySnapshot(permissions: MenuPermission[]) {
  const map = new Map<string, Set<string>>()
  for (const p of permissions) {
    map.set(p.menu_key, new Set(p.actions))
  }
  // ensure all menus have an entry (even empty)
  for (const m of allMenus.value) {
    if (!map.has(m.menu_key)) map.set(m.menu_key, new Set())
  }
  current.value  = map
  original.value = cloneMap(map)
}

// ── Data loading ─────────────────────────────────────────────────────────────

async function loadRoles() {
  loading.value = true
  error.value   = ''
  try {
    // Use roles list from first load (any role_id works to get roles list)
    if (allRoles.value.length === 0) {
      const snap = await api.get<Snapshot>(
        '/api/appadmin/role-menu-permission',
        { role_id: '__none__' }
      )
      allRoles.value = snap.roles
      allMenus.value = snap.menus
    }
  } catch (e: any) {
    error.value = e?.message ?? 'Gagal memuat daftar role'
  } finally {
    loading.value = false
  }
}

async function loadPermissions(roleId: string) {
  loading.value = true
  error.value   = ''
  success.value = ''
  try {
    const snap = await api.get<Snapshot>(
      '/api/appadmin/role-menu-permission',
      { role_id: roleId }
    )
    if (allRoles.value.length === 0) {
      allRoles.value = snap.roles
      allMenus.value = snap.menus
    }
    applySnapshot(snap.permissions)
  } catch (e: any) {
    error.value = e?.message ?? 'Gagal memuat permission'
  } finally {
    loading.value = false
  }
}

// ── Actions ───────────────────────────────────────────────────────────────────

function toggleAction(menuKey: string, action: ActionKey, event: Event) {
  const checked = (event.target as HTMLInputElement).checked
  const set = new Map(current.value)
  const actions = new Set(set.get(menuKey) ?? [])

  if (action === 'view' && !checked) {
    // Uncheck view → clear all actions
    actions.clear()
  } else if (action !== 'view' && checked) {
    // Check non-view → also check view
    actions.add('view')
    actions.add(action)
  } else {
    if (checked) actions.add(action)
    else actions.delete(action)
  }

  set.set(menuKey, actions)
  current.value = set
}

function toggleGroup(groupLabel: string) {
  if (expandedGroups.value.has(groupLabel)) {
    expandedGroups.value.delete(groupLabel)
  } else {
    expandedGroups.value.add(groupLabel)
  }
  expandedGroups.value = new Set(expandedGroups.value)
}

function activateAll(groupLabel: string) {
  const group = groupedMenus.value.find(g => g.label === groupLabel)
  if (!group) return
  const map = cloneMap(current.value)
  for (const m of group.menus) {
    map.set(m.menu_key, new Set(ACTIONS.map(a => a.key)))
  }
  current.value = map
}

function onDiscard() {
  current.value = cloneMap(original.value)
  success.value = ''
  error.value   = ''
}

async function onSave() {
  if (!selectedRoleId.value || !isDirty.value) return
  saving.value  = true
  error.value   = ''
  success.value = ''
  try {
    const permissions = Array.from(current.value.entries()).map(([menu_key, actSet]) => ({
      menu_key,
      actions: Array.from(actSet),
    }))
    const result = await api.post<{ updated: boolean; role_id: string; added_count: number; removed_count: number }>(
      '/api/appadmin/role-menu-permission',
      { role_id: selectedRoleId.value, permissions },
      { method: 'PUT' }
    )
    original.value = cloneMap(current.value)
    success.value  = `Tersimpan: +${result.added_count} ditambah, −${result.removed_count} dihapus`
  } catch (e: any) {
    error.value = e?.message ?? 'Gagal menyimpan permission'
  } finally {
    saving.value = false
  }
}

async function exportExcel() {
  exporting.value = true
  error.value     = ''
  try {
    const blob = await api.blob('/api/appadmin/role-menu-permission/export')
    downloadBlob(blob, 'role-menu-permission.xlsx')
  } catch (e: any) {
    error.value = e?.message ?? 'Gagal export Excel'
  } finally {
    exporting.value = false
  }
}

// ── Watchers ──────────────────────────────────────────────────────────────────

watch(selectedRoleId, async (newId, oldId) => {
  if (!newId) return
  if (oldId && isDirty.value) {
    const ok = window.confirm('Ada perubahan yang belum disimpan. Lanjutkan pindah role?')
    if (!ok) {
      selectedRoleId.value = oldId
      return
    }
  }
  await loadPermissions(newId)
})

const beforeUnload = (e: BeforeUnloadEvent) => {
  if (isDirty.value) { e.preventDefault(); e.returnValue = '' }
}
window.addEventListener('beforeunload', beforeUnload)
onBeforeUnmount(() => window.removeEventListener('beforeunload', beforeUnload))

onBeforeRouteLeave((_to, _from, next) => {
  if (!isDirty.value) return next()
  const ok = window.confirm('Ada perubahan yang belum disimpan. Keluar halaman?')
  next(ok)
})

// ── Init ──────────────────────────────────────────────────────────────────────
loadRoles()
</script>

<template>
  <div class="flex flex-col gap-4 p-4">

    <!-- Header -->
    <div class="flex items-center justify-between">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Pengaturan Menu</h1>
      <div class="flex items-center gap-2">
        <Button variant="outline" size="sm" :disabled="exporting" @click="exportExcel">
          <Download class="w-3.5 h-3.5 mr-1" />
          Export Excel
        </Button>
        <Button variant="outline" size="sm" :disabled="!selectedRoleId || loading" @click="selectedRoleId && loadPermissions(selectedRoleId)">
          <RefreshCw class="w-3.5 h-3.5 mr-1" :class="loading ? 'animate-spin' : ''" />
          Refresh
        </Button>
        <Button variant="outline" size="sm" :disabled="!isDirty" @click="onDiscard">
          <X class="w-3.5 h-3.5 mr-1" />
          Discard
        </Button>
        <Button size="sm" :disabled="!isDirty || saving" @click="onSave">
          <Save class="w-3.5 h-3.5 mr-1" />
          {{ saving ? 'Menyimpan...' : 'Simpan' }}
        </Button>
      </div>
    </div>

    <!-- Alerts -->
    <Alert v-if="error"   type="error">{{ error }}</Alert>
    <Alert v-if="success" type="success">{{ success }}</Alert>
    <Alert v-if="isDirty && !error && !success" type="warning">
      {{ dirtyCount }} perubahan belum disimpan
    </Alert>

    <!-- Role picker -->
    <div class="max-w-xs">
      <SearchSelect
        v-model="selectedRoleId"
        :options="roleOptions"
        placeholder="Pilih role..."
      />
    </div>

    <!-- Prompt state -->
    <div v-if="!selectedRoleId" class="text-sm text-gray-400 italic">
      Pilih role untuk melihat dan mengatur permission menu.
    </div>

    <!-- Loading -->
    <div v-else-if="loading" class="text-sm text-gray-500">Memuat...</div>

    <!-- Accordion per group -->
    <div v-else class="space-y-2">
      <div
        v-for="group in groupedMenus"
        :key="group.label"
        class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
      >
        <!-- Group header -->
        <button
          type="button"
          class="w-full flex items-center justify-between px-4 py-2.5 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-left"
          @click="toggleGroup(group.label)"
        >
          <span class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-200">
            <component :is="expandedGroups.has(group.label) ? ChevronDown : ChevronRight" class="w-4 h-4" />
            {{ group.label }}
            <span class="text-xs text-gray-400 font-normal">({{ activeMenuCount(group) }} dari {{ group.menus.length }} menu aktif)</span>
          </span>
          <button
            type="button"
            class="text-xs text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 px-2 py-0.5 border border-emerald-300 rounded hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors"
            @click.stop="activateAll(group.label)"
          >
            Aktifkan Semua
          </button>
        </button>

        <!-- Menu table -->
        <div v-show="expandedGroups.has(group.label)" class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-t border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-900">
                <th class="text-left px-4 py-2 text-xs font-medium text-gray-500 w-full">Menu</th>
                <th
                  v-for="action in ACTIONS"
                  :key="action.key"
                  class="px-3 py-2 text-xs font-medium text-gray-500 text-center w-10"
                  :title="action.title"
                >
                  {{ action.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="menu in group.menus"
                :key="menu.menu_key"
                class="border-t border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50"
              >
                <td class="px-4 py-2 text-gray-700 dark:text-gray-300">{{ menu.label }}</td>
                <td
                  v-for="action in ACTIONS"
                  :key="action.key"
                  class="px-3 py-2 text-center"
                  :class="isDirtyCell(menu.menu_key, action.key) ? 'bg-amber-50 dark:bg-amber-900/20' : ''"
                >
                  <input
                    type="checkbox"
                    :checked="hasAction(menu.menu_key, action.key)"
                    class="h-4 w-4 rounded border-gray-300 text-emerald-600 cursor-pointer"
                    @change="toggleAction(menu.menu_key, action.key as ActionKey, $event)"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>
```

> Note: If `api.get()` does not accept a params object as second argument, check `shared/api/client.ts` and use the correct calling convention (e.g., append query string manually: `` `/api/appadmin/role-menu-permission?role_id=${roleId}` ``).
> Note: If `api.post()` with `{ method: 'PUT' }` is not the project pattern, use `api.put()` or `POST()` from client.ts — adapt to the actual client API.

- [ ] **Step 3: TypeScript check**

```bash
cd apps_zakat/web-vue && npx tsc --noEmit 2>&1 | head -20
```

Expected: 0 errors

- [ ] **Step 4: Visual smoke test**

Start the dev server if not already running:
```bash
cd apps_zakat/web-vue && npm run dev
```

Navigate to `http://localhost:5173/appadmin/role-menu`. Verify:
- Role picker renders
- Selecting a role loads the accordion
- Accordion expands/collapses
- Checking/unchecking works (view rule enforced)
- "Aktifkan Semua" fills all checkboxes in a group
- Dirty cells highlight amber
- Save button sends PUT, success message appears
- Export Excel button downloads file

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/web-vue/src/modules/appadmin/views/role-menu/RoleMenuView.vue
git commit -m "[ROLE-MENU] feat(web-vue): redesign RoleMenuView — role-first + accordion + action checkboxes

Role picker → accordion domains → 5-column checkbox matrix (V/T/E/H/D).
View-action dependency enforced. Dirty amber highlight. Export Excel.
Backward-compat: existing auth.menus.includes() calls unaffected.

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Mirror to Wakaf + E2E Test

**Files:**
- Modify: `apps_wakaf/bff-api/app/services/auth_db.py`
- Modify: `apps_wakaf/bff-api/app/services/auth.py`
- Modify: `apps_wakaf/bff-api/app/modules/appadmin/admin.py`
- Modify: `apps_wakaf/api-python/app/modules/appadmin/schema.py`
- Modify: `apps_wakaf/api-python/app/modules/appadmin/service.py`
- Modify: `apps_wakaf/api-python/app/modules/appadmin/router.py`
- Modify: `apps_wakaf/web-vue/src/app/stores/auth.store.ts`
- Create: `apps_wakaf/web-vue/src/shared/composables/usePermission.ts`
- Modify: `apps_wakaf/web-vue/src/modules/appadmin/views/role-menu/RoleMenuView.vue`
- Create: `testing/e2e-role-menu-permission.sh`

- [ ] **Step 1: Mirror all zakat changes to wakaf**

For each file changed in Tasks 2–5, apply the identical change to `apps_wakaf/`. The logic is identical; only the DB names differ (already handled by environment config).

```bash
# Verify wakaf auth DB also has the new table (migration was applied in Task 1)
psql -U transaction -d isf_auth_wakaf -h localhost -c \
  "SELECT COUNT(*) FROM isf_auth.role_menu_permission;"
```

Expected: count > 0

- [ ] **Step 2: Write E2E test script**

Create `testing/e2e-role-menu-permission.sh`:

```bash
#!/usr/bin/env bash
# E2E smoke test: role-menu-permission endpoints (zakat portal)
set -euo pipefail

BASE="http://localhost:7000"
COOKIE="/tmp/e2e-rolemenu-$$.txt"
trap 'rm -f "$COOKIE"' EXIT

pass() { echo "  ✓ $1"; }
fail() { echo "  ✗ $1"; exit 1; }

echo "=== Role-Menu Permission E2E (zakat) ==="

# 1. Login as admin user
echo "[1] Login as HADI..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -c "$COOKIE" -X POST "$BASE/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"HADI","password":"test1234"}')
[ "$STATUS" = "200" ] && pass "Login OK" || fail "Login failed ($STATUS)"

# 2. GET permissions for role KEU
echo "[2] GET permissions for role KEU..."
BODY=$(curl -s -b "$COOKIE" "$BASE/api/appadmin/role-menu-permission?role_id=KEU")
echo "$BODY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
assert 'data' in d, 'missing data key'
assert 'roles' in d['data'], 'missing roles'
assert 'menus' in d['data'], 'missing menus'
assert 'permissions' in d['data'], 'missing permissions'
print('  data shape OK')
"
pass "GET permissions shape OK"

# 3. PUT - set view permission for finance.dashboard
echo "[3] PUT permission for KEU on finance.dashboard..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -b "$COOKIE" -X PUT \
  "$BASE/api/appadmin/role-menu-permission" \
  -H "Content-Type: application/json" \
  -d '{"role_id":"KEU","permissions":[{"menu_key":"finance.dashboard","actions":["view"]}]}')
[ "$STATUS" = "200" ] && pass "PUT permission OK" || fail "PUT permission failed ($STATUS)"

# 4. Verify the change persisted
echo "[4] Verify permission persisted..."
BODY=$(curl -s -b "$COOKIE" "$BASE/api/appadmin/role-menu-permission?role_id=KEU")
echo "$BODY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
perms = {p['menu_key']: p['actions'] for p in d['data']['permissions']}
assert 'view' in perms.get('finance.dashboard', []), 'view action not found for finance.dashboard'
print('  persistence OK')
"
pass "Permission persisted OK"

# 5. Export Excel
echo "[5] Export Excel..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -b "$COOKIE" \
  "$BASE/api/appadmin/role-menu-permission/export")
[ "$STATUS" = "200" ] && pass "Export Excel OK" || fail "Export Excel failed ($STATUS)"

# 6. Login check: menus field is action-aware
echo "[6] Login menus field is action-aware..."
BODY=$(curl -s -b "$COOKIE" "$BASE/api/auth/me")
echo "$BODY" | python3 -c "
import sys, json
d = json.load(sys.stdin)
menus = d['data']['user']['menus']
assert isinstance(menus, list), 'menus should be list'
if menus:
    first = menus[0]
    assert 'menu_key' in first, 'menus items should have menu_key'
    assert 'actions' in first, 'menus items should have actions'
    assert isinstance(first['actions'], list), 'actions should be list'
print('  menus format OK')
"
pass "Menus format is action-aware"

echo ""
echo "=== All tests passed ==="
```

```bash
chmod +x testing/e2e-role-menu-permission.sh
bash testing/e2e-role-menu-permission.sh
```

Expected: all 6 checks pass

- [ ] **Step 3: Commit**

```bash
git add apps_wakaf/ testing/e2e-role-menu-permission.sh
git commit -m "[ROLE-MENU] feat: mirror permission refactor to wakaf + E2E test script

Mirror all role-menu-permission changes to apps_wakaf (identical logic,
different DB). E2E test covers GET/PUT/export + login menus shape.

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review Checklist

- [x] **Spec coverage:**
  - DB migration: Task 1 ✓
  - api-python endpoints (GET/PUT/export): Task 2 ✓
  - BFF require_menu update + session menus: Task 3 ✓
  - Auth store MenuPermission type + menuActions: Task 4 ✓
  - usePermission composable: Task 4 ✓
  - RoleMenuView redesign (role-first + accordion + 5 actions): Task 5 ✓
  - Export Excel: Task 2 (api-python) + Task 3 (BFF) + Task 5 (FE button) ✓
  - Wake rule (uncheck view → clear all; check non-view → auto-check view): Task 5 ✓
  - Mirror to wakaf: Task 6 ✓
  - E2E test: Task 6 ✓

- [x] **Placeholder scan:** No TBD/TODO/incomplete sections — all code blocks are complete

- [x] **Type consistency:**
  - `MenuPermission` defined in Task 4 auth.store.ts; used consistently in Task 5 RoleMenuView
  - `get_menus_by_roles()` returns `list[dict]` in Task 3; consumed by `require_menu()` in same task
  - `RoleMenuPermissionSnapshot.permissions` is `list[MenuPermission]` — matches Task 2 schema and Task 5 API call
  - `api.post(..., { method: 'PUT' })` — note in Task 5 to verify against actual client.ts API

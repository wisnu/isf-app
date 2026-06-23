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

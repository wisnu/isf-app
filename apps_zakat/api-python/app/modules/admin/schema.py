from pydantic import BaseModel


class RoleInfo(BaseModel):
    id_peran: str
    nama_peran: str
    user_count: int


class MenuInfo(BaseModel):
    menu_key: str
    label: str
    group_label: str
    sort_order: int


class MappingPair(BaseModel):
    id_peran: str
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

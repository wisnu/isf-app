from __future__ import annotations

from pydantic import BaseModel


class RoleListItem(BaseModel):
    role_id: str
    role_name: str
    description: str | None
    status: str      # 'active' | 'inactive'
    user_count: int


class RoleDetail(BaseModel):
    role_id: str
    role_name: str
    description: str | None
    status: str
    user_count: int
    menu_keys: list[str]


class RoleCreateRequest(BaseModel):
    role_id: str
    role_name: str
    description: str | None = None
    created_by: str = "SYSTEM"


class RoleUpdateRequest(BaseModel):
    role_name: str
    description: str | None = None
    updated_by: str = "SYSTEM"


class RoleStatusRequest(BaseModel):
    status: str   # 'active' | 'inactive'
    updated_by: str = "SYSTEM"

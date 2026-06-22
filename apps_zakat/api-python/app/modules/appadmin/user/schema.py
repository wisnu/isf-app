from __future__ import annotations

from pydantic import BaseModel


class UserListItem(BaseModel):
    user_id: str
    display_name: str
    status: str          # 'active' | 'inactive'
    is_locked: bool
    primary_branch: str | None
    branch_access: str   # 'all' | 'single'
    role_ids: list[str]


class UserDetail(BaseModel):
    user_id: str
    display_name: str
    status: str
    is_locked: bool
    primary_branch: str | None
    branch_access: str
    roles: list[dict]
    allowed_branches: list[str]


class UserCreateRequest(BaseModel):
    user_id: str          # id_user (username) — uppercase
    display_name: str
    password_hash: str    # bcrypt hash — computed by BFF
    primary_branch: str
    branch_access: str = "single"  # 'all'=S, 'single'=T
    roles: list[str] = []
    branches: list[str] = []
    created_by: str = "SYSTEM"


class UserUpdateRequest(BaseModel):
    display_name: str
    primary_branch: str
    branch_access: str = "single"
    updated_by: str = "SYSTEM"


class UserPasswordRequest(BaseModel):
    password_hash: str    # bcrypt hash from BFF


class UserRolesRequest(BaseModel):
    roles: list[str]
    updated_by: str = "SYSTEM"


class UserBranchesRequest(BaseModel):
    branches: list[str]
    updated_by: str = "SYSTEM"


class UserStatusRequest(BaseModel):
    status: str   # 'active' | 'inactive'
    updated_by: str = "SYSTEM"

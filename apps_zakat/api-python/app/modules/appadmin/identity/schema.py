from pydantic import BaseModel


class RoleInfo(BaseModel):
    role_id: str
    role_name: str
    level: int | None = None


class BranchInfo(BaseModel):
    branch_code: str
    is_primary: bool = False


class ProfileResponse(BaseModel):
    user_id: str
    status: str
    roles: list[RoleInfo]
    branches: list[BranchInfo]
    menus: list[dict]
    # Cabang default user (userapp.kode_cabang) — independen dari daftar branches.
    primary_branch: str | None = None
    # Scope akses cabang: 'all' (tipe_akses_cabang='S' / Seluruh) atau
    # 'single' (='T' / Tunggal — hanya cabang default).
    branch_access: str = "single"

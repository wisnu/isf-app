from pydantic import BaseModel


class RoleInfo(BaseModel):
    id_peran: str
    nama_peran: str
    level: int | None = None


class BranchInfo(BaseModel):
    kode_cabang: str
    is_primary: bool = False


class ProfileResponse(BaseModel):
    user_id: str
    status: str
    roles: list[RoleInfo]
    branches: list[BranchInfo]
    menus: list[str]

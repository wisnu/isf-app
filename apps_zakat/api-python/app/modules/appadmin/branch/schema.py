"""Branch schema — Cabang management."""

from pydantic import BaseModel


class BranchListItem(BaseModel):
    branch_code: str
    branch_name: str
    branch_type: str | None = None
    branch_status: str | None = None
    parent_branch_code: str | None = None
    parent_branch_name: str | None = None
    is_active: bool


class BranchDetail(BranchListItem):
    office_name: str | None = None
    office_npwp: str | None = None
    office_address: str | None = None
    office_postal_code: str | None = None
    office_phone1: str | None = None
    office_phone2: str | None = None
    office_phone3: str | None = None
    access_status: str | None = None
    created_by: str | None = None
    created_at: str | None


class BranchCreateRequest(BaseModel):
    branch_code: str
    branch_name: str
    branch_type: str
    parent_branch_code: str | None = None
    office_name: str | None = None
    office_npwp: str | None = None
    office_address: str | None = None
    office_postal_code: str | None = None
    office_phone1: str | None = None
    office_phone2: str | None = None
    office_phone3: str | None = None
    user_input: str | None = None


class BranchUpdateRequest(BaseModel):
    branch_name: str
    branch_type: str
    parent_branch_code: str | None = None
    office_name: str | None = None
    office_npwp: str | None = None
    office_address: str | None = None
    office_postal_code: str | None = None
    office_phone1: str | None = None
    office_phone2: str | None = None
    office_phone3: str | None = None


class ParentBranchItem(BaseModel):
    branch_code: str
    branch_name: str

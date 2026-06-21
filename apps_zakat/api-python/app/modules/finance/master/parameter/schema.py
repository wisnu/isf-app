from __future__ import annotations

from pydantic import BaseModel


class BudgetOwnerRow(BaseModel):
    owner_id: int
    owner_code: str
    owner_name: str
    level: int
    is_detail: str
    parent_owner_id: int | None
    status: str


class BudgetOwnerDetail(BudgetOwnerRow):
    updated_date: str | None = None
    updated_by: str | None = None
    updated_terminal: str | None = None


class BudgetOwnerLookup(BaseModel):
    owner_id: int
    owner_code: str
    owner_name: str
    is_detail: str


class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class BudgetOwnerList(BaseModel):
    rows: list[BudgetOwnerRow]
    pagination: Pagination

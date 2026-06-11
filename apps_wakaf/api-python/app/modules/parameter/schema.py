from __future__ import annotations

from pydantic import BaseModel


class BudgetOwnerRow(BaseModel):
    ownerid: int
    ownercode: str
    ownername: str
    level: int
    is_detail: str
    parentownerid: int | None
    status: str


class BudgetOwnerDetail(BudgetOwnerRow):
    tglubah: str | None = None
    userpengubah: str | None = None
    terminalubah: str | None = None


class BudgetOwnerLookup(BaseModel):
    ownerid: int
    ownercode: str
    ownername: str
    is_detail: str


class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class BudgetOwnerList(BaseModel):
    rows: list[BudgetOwnerRow]
    pagination: Pagination

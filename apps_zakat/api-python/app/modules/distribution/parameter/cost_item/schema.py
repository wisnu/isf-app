from __future__ import annotations

from pydantic import BaseModel


class CostItemRow(BaseModel):
    cost_item_id: int
    code: str | None
    description: str | None


class CostItemDetail(BaseModel):
    cost_item_id: int
    code: str | None
    description: str | None


class CreateUpdateCostItemBody(BaseModel):
    code: str
    description: str


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class CostItemList(BaseModel):
    rows: list[CostItemRow]
    pagination: Pagination

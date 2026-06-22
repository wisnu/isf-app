from __future__ import annotations

from pydantic import BaseModel


class RegularProgramRow(BaseModel):
    program_id: int
    mustahiq_id: int
    mustahiq_name: str | None
    product_id: int
    product_name: str | None
    program_detail_name: str | None
    distribution_amount: float | None
    date_start: str | None   # ISO YYYY-MM-DD
    date_end: str | None     # ISO YYYY-MM-DD
    proposal_id: int | None
    branch_code: str | None
    ashnaf: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class RegularProgramList(BaseModel):
    rows: list[RegularProgramRow]
    pagination: Pagination


class RegularProgramDetail(BaseModel):
    program_id: int
    mustahiq_id: int
    mustahiq_name: str | None
    product_id: int
    product_name: str | None
    program_detail_name: str | None
    distribution_amount: float | None
    date_start: str | None
    date_end: str | None
    proposal_id: int | None
    proposal_no: str | None
    branch_code: str | None
    ashnaf: str | None


class CreateRegularProgramBody(BaseModel):
    mustahiq_id: int
    product_id: int
    program_detail_name: str
    distribution_amount: float
    date_start: str   # ISO YYYY-MM-DD
    date_end: str     # ISO YYYY-MM-DD
    proposal_id: int | None = None
    branch_code: str | None = None
    ashnaf: str | None = None


class UpdateRegularProgramBody(BaseModel):
    mustahiq_id: int
    product_id: int
    program_detail_name: str
    distribution_amount: float
    date_start: str   # ISO YYYY-MM-DD
    date_end: str     # ISO YYYY-MM-DD
    proposal_id: int | None = None
    ashnaf: str | None = None


class ProductLookupItem(BaseModel):
    product_id: int
    product_name: str | None


class MustahiqLookupItem(BaseModel):
    mustahiq_id: int
    mustahiq_name: str | None

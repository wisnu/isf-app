from __future__ import annotations

from pydantic import BaseModel


class RealizationDetailRow(BaseModel):
    realization_detail_id: int
    mustahiq_product_id: int
    product_name: str | None
    mustahiq_name: str | None
    program_detail_name: str | None
    account_no: str | None
    account_name: str | None
    memo_amount: float
    realization_amount: float
    ashnaf: str | None
    fund_product_id: int | None


class RealizationRow(BaseModel):
    realization_id: int
    realization_date: str | None  # ISO YYYY-MM-DD
    realization_description: str | None
    realization_location: str | None
    memo_number: str | None
    memo_id: int | None = None  # NEW: for edit form to track memo selection
    status_receivables: str | None  # 'T' or 'Y'
    status_reclpj: str | None  # NULL, 'Y'
    branch_code: str | None
    realization_amount: float | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class RealizationList(BaseModel):
    rows: list[RealizationRow]
    pagination: Pagination


class RealizationDetail(RealizationRow):
    details: list[RealizationDetailRow]
    budgets: list[int]  # List of budget IDs
    partners: list[int]  # List of partner IDs


class RealizationDetailInput(BaseModel):
    mustahiq_product_id: int
    realization_amount: float
    detail_description: str | None = None


class CreateRealizationBody(BaseModel):
    realization_date: str  # ISO YYYY-MM-DD
    description: str
    location: str
    memo_id: int
    status_receivables: str = 'T'  # 'T' or 'Y'
    employee_id: str | None = None
    branch_code: str | None = None
    details: list[RealizationDetailInput]
    budgets: list[int] | None = None
    partners: list[int] | None = None


class UpdateRealizationBody(BaseModel):
    realization_date: str  # ISO YYYY-MM-DD
    description: str
    location: str
    memo_id: int
    status_receivables: str = 'T'  # 'T' or 'Y'
    employee_id: str | None = None
    branch_code: str | None = None
    details: list[RealizationDetailInput]
    budgets: list[int] | None = None
    partners: list[int] | None = None


class MemoLookupItem(BaseModel):
    realization_memo_id: int
    realization_memo_number: str | None
    realization_memo_date: str | None
    realization_memo_amount: float | None
    realization_memo_subject: str | None


class MemoDetailItem(BaseModel):
    mustahiq_product_id: int
    product_name: str | None
    mustahiq_name: str | None
    program_detail_name: str | None
    account_no: str | None
    account_name: str | None
    memo_amount: float
    ashnaf: str | None
    fund_product_id: int | None
    proposal_date: str | None
    proposal_nominal: float | None
    proposal_reference_by: str | None

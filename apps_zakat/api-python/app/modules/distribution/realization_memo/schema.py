from __future__ import annotations

from pydantic import BaseModel


class MemoDetailRow(BaseModel):
    memo_detail_id: int
    mustahiq_product_id: int
    product_name: str | None
    mustahiq_name: str | None
    program_detail_name: str | None
    amount: float


class MemoRow(BaseModel):
    memo_id: int
    memo_number: str | None
    memo_subject: str | None
    memo_from: str | None
    memo_to: str | None
    memo_amount: float | None
    memo_date: str | None  # ISO YYYY-MM-DD
    branch_code: str | None
    user_input: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class MemoList(BaseModel):
    rows: list[MemoRow]
    pagination: Pagination


class MemoDetail(MemoRow):
    details: list[MemoDetailRow]


class MemoDetailInput(BaseModel):
    mustahiq_product_id: int
    amount: float


class CreateMemoBody(BaseModel):
    memo_number: str
    memo_subject: str
    memo_from: str
    memo_to: str
    memo_date: str  # ISO YYYY-MM-DD
    branch_code: str | None = None
    details: list[MemoDetailInput]


class UpdateMemoBody(BaseModel):
    memo_number: str
    memo_subject: str
    memo_from: str
    memo_to: str
    memo_date: str  # ISO YYYY-MM-DD
    details: list[MemoDetailInput]


class ProgramLookupItem(BaseModel):
    mustahiq_product_id: int
    mustahiq_product_name: str | None
    product_name: str | None
    mustahiq_name: str | None
    distribution_amount: float | None

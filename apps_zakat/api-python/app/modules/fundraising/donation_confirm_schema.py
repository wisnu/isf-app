from __future__ import annotations

from pydantic import BaseModel


class DonationTransactionRow(BaseModel):
    transaction_id: int
    transaction_no: str
    actual_date: str  # ISO YYYY-MM-DD
    donor_no: str | None
    donor_name: str | None
    amount: float
    description: str | None
    branch_code: str
    branch_name: str | None
    channel_name: str | None
    channel_code: str | None
    product_name: str | None
    auth_status: str   # 'F' or 'T'
    is_posted: str     # 'F' or 'T'
    transaction_item_id: int


class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class DonationTransactionListResponse(BaseModel):
    rows: list[DonationTransactionRow]
    pagination: Pagination


class UpdateDonorBody(BaseModel):
    donor_no: str
    donor_name: str

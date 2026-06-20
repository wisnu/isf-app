from __future__ import annotations
from pydantic import BaseModel


class TransactionRow(BaseModel):
    transaction_id: int
    transaction_no: str | None
    transaction_date: str   # ISO YYYY-MM-DD
    actual_date: str        # ISO YYYY-MM-DD
    amount: float
    donor_no: str | None
    donor_name: str | None
    reference_no: str | None
    description: str | None
    inputer: str | None
    auth_status: str | None
    is_posted: str | None
    auth_operation_mode: str | None
    branch_code: str | None
    channel_account_no: str | None
    channel_name: str | None
    external_transaction_id: int | None
    title_subsystem: str | None


class JournalItem(BaseModel):
    journalitem_no: int
    fl_account: str | None
    account_name: str | None
    branch_code: str | None
    currency_code: str | None
    amount_debit: float
    amount_credit: float
    description: str | None
    subaccount_code: str | None
    subaccount_name: str | None


class TransactionDetail(TransactionRow):
    journal_items: list[JournalItem]


class DeleteResult(BaseModel):
    deleted: bool
    pending_approval: bool
    message: str


class RepostResult(BaseModel):
    journal_no: str
    success: bool


class SearchPage(BaseModel):
    rows: list[TransactionRow]
    total: int
    page: int
    page_size: int
    total_pages: int

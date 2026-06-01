"""Report schemas."""

from __future__ import annotations

from pydantic import BaseModel


class JournalDailyRow(BaseModel):
    journal_date: str | None
    journal_no: str | None
    transactionno: str | None
    account_branch_code: str | None
    account_code: str | None
    account_name: str | None
    subaccountcode: str | None
    subaccountname: str | None
    description: str | None
    debit_ekuiv: float
    credit_ekuiv: float
    inputer: str | None


class JournalDailyPage(BaseModel):
    rows: list[JournalDailyRow]
    total: int
    capped: bool          # total > CAP — saran persempit rentang
    page: int
    page_size: int


class BranchOption(BaseModel):
    code: str
    name: str

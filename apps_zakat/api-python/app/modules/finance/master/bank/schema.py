from __future__ import annotations

from pydantic import BaseModel


class BankAccountRow(BaseModel):
    account_no: str
    account_name: str | None
    bank_name: str | None
    bank_account_no: str | None
    branch_code: str | None
    currency_code: str | None
    balance: float | None
    status: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class BankAccountList(BaseModel):
    rows: list[BankAccountRow]
    pagination: Pagination


# ── Lookup models ─────────────────────────────────────────────────────────────

class BankLookupItem(BaseModel):
    bank_code: str
    bank_short_name: str | None
    bank_name: str | None


class BranchLookupItem(BaseModel):
    branch_code: str
    branch_name: str | None


class CurrencyLookupItem(BaseModel):
    currency_code: str
    short_name: str | None
    full_name: str | None


class GlAccountLookupItem(BaseModel):
    account_code: str
    account_name: str | None


class ProductLookupItem(BaseModel):
    product_id: int
    product_code: str | None
    product_name: str | None


# ── Detail model ──────────────────────────────────────────────────────────────

class BankAccountDetail(BaseModel):
    account_no: str
    account_name: str | None
    bank_name: str | None
    bank_code: str | None
    bank_account_no: str | None
    branch_code: str | None
    currency_code: str | None
    balance: float | None
    account_interface: str | None
    opening_date: str | None  # ISO YYYY-MM-DD
    is_amil_account: bool
    product_id: int | None
    cash_code: str | None
    status: str | None

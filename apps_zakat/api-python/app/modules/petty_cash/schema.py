from __future__ import annotations

from pydantic import BaseModel


class PettyCashRow(BaseModel):
    account_no: str
    account_name: str | None
    cash_code: str | None
    branch_code: str | None
    currency_code: str | None
    balance: float | None
    status: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class PettyCashList(BaseModel):
    rows: list[PettyCashRow]
    pagination: Pagination


class PettyCashDetail(BaseModel):
    account_no: str
    account_name: str | None
    cash_code: str | None
    account_interface: str | None
    currency_code: str | None
    branch_code: str | None
    balance: float | None
    status: str | None
    opening_date: str | None  # ISO YYYY-MM-DD


class PettyCashCreate(BaseModel):
    account_name: str
    cash_code: str | None = None
    account_interface: str
    currency_code: str
    branch_code: str
    opening_date: str | None = None  # ISO YYYY-MM-DD


class PettyCashUpdate(BaseModel):
    account_name: str
    cash_code: str | None = None
    account_interface: str
    currency_code: str
    opening_date: str | None = None  # ISO YYYY-MM-DD


# ── Lookup models ─────────────────────────────────────────────────────────────

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

from __future__ import annotations

from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


# ── Owner/Period/Item lookup models ──────────────────────────────────────────

class BudgetOwnerItem(BaseModel):
    owner_id: int
    owner_code: str
    owner_name: str
    level: int
    is_detail: str  # 'T' or 'F'
    parent_owner_id: Optional[int] = None
    status: str


class BudgetPeriodItem(BaseModel):
    period_id: int
    period_value: int
    is_open: str  # 'T' or 'F'
    parent_period_id: Optional[int] = None


class BudgetItemRow(BaseModel):
    item_id: int
    budget_id: Optional[int] = None
    item_code: str
    item_name: str
    level: int  # 1 or 2
    parent_item_id: Optional[int] = None
    amount: Optional[Decimal] = None
    is_detail: str  # 'T' or 'F'


class BudgetRow(BaseModel):
    budget_id: int
    budget_code: str
    owner_id: int
    owner_name: Optional[str] = None
    period_id: int
    period_value: Optional[int] = None
    item_id: Optional[int] = None
    item_code: Optional[str] = None
    item_name: Optional[str] = None
    item_group: Optional[str] = None
    amount: Decimal
    realization: Decimal = Decimal(0)
    currency_code: str = "IDR"
    branch_code: str
    budget_type: str = "Y"
    is_detail: str = "F"
    created_date: Optional[str] = None
    created_by: Optional[str] = None


class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


# ── Request models ───────────────────────────────────────────────────────────

class BudgetNewRequest(BaseModel):
    owner_id: int
    period_id: int
    budget_code: str
    item_group: str
    item_name: str
    amount: Decimal = Field(gt=0, decimal_places=2)


class BudgetEditRequest(BaseModel):
    budget_code: str
    item_group: str
    item_name: str
    amount: Decimal = Field(gt=0, decimal_places=2)


class BudgetReviseItem(BaseModel):
    budget_id: int
    amount: Decimal = Field(gt=0, decimal_places=2)


class BudgetReviseRequest(BaseModel):
    items: list[BudgetReviseItem]


# ── Import models ────────────────────────────────────────────────────────────

class BudgetImportRow(BaseModel):
    row_number: int
    owner_code: str
    item_group: str
    item_name: str
    budget_code: str
    amount: Decimal = Field(ge=0, decimal_places=2)


class BudgetImportRequest(BaseModel):
    period_id: int
    rows: list[BudgetImportRow]


# ── Response models ──────────────────────────────────────────────────────────

class BudgetListResponse(BaseModel):
    rows: list[BudgetRow]
    pagination: Pagination


class BudgetDetailResponse(BaseModel):
    budget_id: int
    budget_code: str
    owner_id: int
    owner_name: Optional[str] = None
    period_id: int
    period_value: Optional[int] = None
    amount: Decimal
    realization: Decimal = Decimal(0)
    currency_code: str = "IDR"
    branch_code: str
    budget_type: str = "Y"
    is_detail: str = "F"
    items: list[BudgetItemRow] = []


class BudgetTransactionRow(BaseModel):
    transaction_item_id: int
    actual_date: str
    transaction_code: str
    transaction_no: Optional[str] = None
    item_name: Optional[str] = None
    realization_amount: Decimal = Decimal(0)
    return_amount: Decimal = Decimal(0)
    budget_trans_type: Optional[str] = None
    reference_no: Optional[str] = None
    inputer: Optional[str] = None


class BudgetTransactionListResponse(BaseModel):
    budget_id: int
    rows: list[BudgetTransactionRow]
    pagination: Pagination


class BudgetCodeSearchRow(BaseModel):
    budget_id: int
    budget_code: str
    budget_owner: str
    item_group: Optional[str] = None
    item_name: Optional[str] = None


# ── Parameter master models ──────────────────────────────────────────────────

class BudgetMasterItemRow(BaseModel):
    item_id: int
    item_code: str
    item_description: str
    level: int
    is_detail: str
    parent_item_id: Optional[int] = None
    parent_description: Optional[str] = None
    owner_id: Optional[int] = None
    owner_name: Optional[str] = None
    branch_code: Optional[str] = None


class BudgetMasterItemRequest(BaseModel):
    item_code: str
    item_description: str
    level: int = 2
    is_detail: str = 'T'
    parent_item_id: Optional[int] = None
    owner_id: Optional[int] = None
    branch_code: Optional[str] = None


class BudgetMasterPeriodRow(BaseModel):
    period_id: int
    period_value: int
    is_open: str
    child_count: int = 0


class BudgetOwnerSummaryRow(BaseModel):
    owner_id: int
    owner_name: str
    total_budget: Decimal
    total_realization: Decimal
    remaining: Decimal


class BudgetOwnerSummaryResponse(BaseModel):
    period_id: int
    period_value: int
    rows: list[BudgetOwnerSummaryRow]

"""Pydantic schemas for Uang Muka Penyerahan (Cash Advance)."""
from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CashAdvanceCreate(BaseModel):
    """Request to create Uang Muka Penyerahan transaction."""
    actual_date: str  # ISO YYYY-MM-DD
    employee_id: int  # Employee ID
    employee_name: str  # Employee name (for EmployeeCashAdvance account name)
    cash_account_no: str  # Cash account number
    amount: float = Field(gt=0)  # Must be positive
    reference_no: str = ""  # Optional reference
    description: str = ""  # Optional description
    received_from: str = ""  # Optional (default = inputer)
    budget_id: int = 0  # Optional, 0 = none
    real_memo_id: int = 0  # Optional, 0 = none
    fund_entity: int = 4  # Hardcoded Amil (do NOT change)


class CashAdvanceUpdate(BaseModel):
    """Request to update Uang Muka (only DRAFT/REJECTED)."""
    actual_date: Optional[str] = None  # ISO YYYY-MM-DD
    amount: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    reference_no: Optional[str] = None


class CashAdvanceListRow(BaseModel):
    """Single row in Uang Muka list."""
    transactionid: int
    transaction_no: str
    actual_date: str  # ISO YYYY-MM-DD
    amount: float
    auth_status: str  # 'T'=authorized, 'P'=pending, 'R'=rejected
    branch_code: str
    inputer: str
    description: str
    employee_name: str
    employee_id: int


class CashAdvanceDetail(BaseModel):
    """Full detail of Uang Muka transaction."""
    transactionid: int
    transaction_no: str
    actual_date: str  # ISO YYYY-MM-DD
    amount: float
    auth_status: str
    branch_code: str
    inputer: str
    description: str
    employee_id: int
    employee_name: str
    cash_account_no: str
    reference_no: Optional[str]
    has_return_trans: bool  # True if return transaction exists


class EmployeeLookupRow(BaseModel):
    """Employee lookup row."""
    employee_id: int
    employee_name: str
    employee_number: str


class CashAccountLookupRow(BaseModel):
    """Cash account lookup row."""
    cash_account_no: str
    cash_account_name: str
    accountno: str


class BudgetLookupRow(BaseModel):
    """Budget lookup row."""
    budget_id: int
    budget_code: str
    description: str
    owner_name: str

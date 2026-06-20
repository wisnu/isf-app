"""Pydantic schemas for Uang Muka Pengembalian / LPJ (Cash Advance Return)."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class CashAdvanceSettlementCreate(BaseModel):
    """Request to create Pengembalian Uang Muka via otorisasi."""
    actual_date: str          # ISO YYYY-MM-DD
    ref_transaction_no: str   # No transaksi penyerahan (CA), e.g. KK-2026-001-LAZ-0000289
    ref_transaction_item_id: int  # transactionitemid of original CA DEBIT item
    ref_amount: float         # Amount of original CA (for validation)
    employee_id: int          # Employee ID
    employee_name: str        # Employee name
    cash_account_no: str      # Cash/bank account (money returned to)
    amount: float = Field(gt=0)  # Amount being returned (usually = ref_amount)
    reference_no: str = ""    # Optional check/receipt number
    description: str = ""     # Optional description
    paid_to: str = ""         # Optional — who returned the money (default = employee_name)
    fund_entity: int = 4      # Hardcoded Amil (same as penyerahan)

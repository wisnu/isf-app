"""Pydantic schemas for Piutang (Pinjam/Bayar)."""
from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal


class ReceivableCreate(BaseModel):
    """Request to create Receivable (EAR=Pinjam or PEAR=Bayar) transaction."""
    actual_date: str  # ISO YYYY-MM-DD
    transaction_type: str  # 'P' = Pinjam (EAR), 'B' = Bayar (PEAR)
    channel_type: str  # 'C' = Kas/Bank, 'G' = GL Account
    cash_account_no: Optional[str] = None  # Required if channel_type='C'
    gl_account_code: Optional[str] = None  # Required if channel_type='G'
    debtor_id: str  # Debtor ID from DEBTOR_ALL (E#### or X####)
    debtor_type: str  # 'E' = Karyawan, 'X' = Non-Karyawan (auto from lookup, read-only in submission)
    amount: Decimal = Field(gt=0)  # Must be positive
    reference_no: Optional[str] = None  # Optional (e.g., check number)
    description: Optional[str] = None  # Optional notes
    casher: Optional[str] = None  # Optional (default = inputer)
    fund_entity: int = 4  # Hardcoded Dana Amil — do NOT change


class ReceivableListItem(BaseModel):
    """Single row in Receivable list."""
    id: int
    transaction_no: str
    transaction_code: str  # 'EAR' or 'PEAR'
    transaction_type: str  # 'P' or 'B'
    actual_date: str  # ISO YYYY-MM-DD
    branch_code: str
    inputer: str
    debtor_name: str
    debtor_type: str  # 'E' or 'X'
    account_name: str  # Account name (e.g., "Piutang Karyawan - Budi")
    amount: Decimal
    currency_code: str  # 'IDR'
    status: str  # Otorisasi status (AUTHORIZED, PENDING, etc.)
    reference_no: Optional[str]
    description: Optional[str]


class ReceivableListResponse(BaseModel):
    """Paginated list response for Receivable."""
    rows: list[ReceivableListItem]
    pagination: dict


class DebtorRow(BaseModel):
    """Debtor lookup row (from DEBTOR_ALL view)."""
    debtor_id: str  # E#### or X####
    debtor_code: str  # Employee code or external debtor code
    debtor_name: str  # Name
    debtor_type: str  # 'E' or 'X'
    branch_code: str


class ExternalDebtorRow(BaseModel):
    """External Debtor list row."""
    debtor_id: str
    debtor_code: str
    debtor_name: str
    debtor_phone: Optional[str]
    debtor_address: Optional[str]
    description: Optional[str]

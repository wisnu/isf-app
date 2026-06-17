"""Pydantic schemas for Piutang (Pinjam/Bayar)."""
from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from decimal import Decimal


class PiutangCreate(BaseModel):
    """Request to create Piutang (EAR=Pinjam or PEAR=Bayar) transaction."""
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


class PiutangListItem(BaseModel):
    """Single row in Piutang list."""
    id: int
    transactionno: str
    transactioncode: str  # 'EAR' or 'PEAR'
    transactiontype: str  # 'P' or 'B'
    actualdate: str  # ISO YYYY-MM-DD
    branchcode: str
    inputer: str
    debtorname: str
    debtortype: str  # 'E' or 'X'
    accountname: str  # Account name (e.g., "Piutang Karyawan - Budi")
    amount: Decimal
    currencycode: str  # 'IDR'
    status: str  # Otorisasi status (AUTHORIZED, PENDING, etc.)
    referenceno: Optional[str]
    description: Optional[str]


class PiutangListResponse(BaseModel):
    """Paginated list response for Piutang."""
    rows: list[PiutangListItem]
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

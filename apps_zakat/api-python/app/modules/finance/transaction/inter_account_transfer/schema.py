"""Pydantic schemas for Transfer Antar Rekening (transactioncode='TI')."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class InterAccountTransferCreate(BaseModel):
    """Request body to create Inter-Account Transfer via otorisasi save-and-submit."""
    actual_date: str               # ISO YYYY-MM-DD
    source_account_no: str         # cashaccount.cashaccountno (source account)
    dest_account_no: str           # cashaccount.cashaccountno (destination account)
    amount: float = Field(gt=0)    # must be positive
    description: str = ""
    reference_no: str = ""


class CashAccountLookupRow(BaseModel):
    cash_account_no: str
    account_no: str
    account_name: str
    branch_code: str
    balance: Optional[float]
    cash_account_type: str         # 'A'=bank, 'K'=petty cash, 'L'=cash


class TransferRow(BaseModel):
    transactionid: int
    transaction_no: Optional[str]
    actual_date: str               # YYYY-MM-DD string
    amount: float
    auth_status: str               # 'T'=authorized
    branch_code: str
    inputer: str
    description: str
    reference_no: Optional[str]
    source_account_name: Optional[str]
    source_cash_account_no: Optional[str]
    dest_account_name: Optional[str]
    dest_cash_account_no: Optional[str]


class TransferDetail(TransferRow):
    source_account_no: Optional[str]
    dest_account_no: Optional[str]

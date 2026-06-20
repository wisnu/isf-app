"""Pydantic schemas for Transfer Antar Rekening (transactioncode='TI')."""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class TransferAntarRekeningCreate(BaseModel):
    """Request body to create Transfer Antar Rekening via otorisasi save-and-submit."""
    actual_date: str               # ISO YYYY-MM-DD
    source_account_no: str         # cashaccount.cashaccountno (rekening sumber)
    dest_account_no: str           # cashaccount.cashaccountno (rekening tujuan)
    amount: float = Field(gt=0)    # harus positif
    description: str = ""
    reference_no: str = ""


class CashAccountLookupRow(BaseModel):
    cashaccountno: str
    accountno: str
    accountname: str
    branchcode: str
    balance: Optional[float]
    cashaccounttype: str           # 'A'=bank, 'K'=kas kecil, 'L'=kas


class TransferRow(BaseModel):
    transactionid: int
    transactionno: Optional[str]
    actualdate: str                # YYYY-MM-DD string
    amount: float
    authstatus: str                # 'T'=authorized
    branchcode: str
    inputer: str
    description: str
    reference_no: Optional[str]
    source_account_name: Optional[str]
    source_cashaccountno: Optional[str]
    dest_account_name: Optional[str]
    dest_cashaccountno: Optional[str]


class TransferDetail(TransferRow):
    source_accountno: Optional[str]
    dest_accountno: Optional[str]

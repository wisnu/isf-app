from __future__ import annotations
from pydantic import BaseModel


class AccountOption(BaseModel):
    account_no: str
    account_name: str
    branch_code: str
    ar_type: str  # 'E'=Karyawan, 'D'=Non Karyawan


class HistoryRow(BaseModel):
    transaction_item_id: int
    actual_date: str
    transaction_code: str | None
    mutation_type: str
    amount: float
    debet: float
    kredit: float
    running_balance: float
    reference_no: str | None
    description: str | None
    transaction_no: str | None
    inputer: str | None
    auth_status: str


class HistoryResult(BaseModel):
    account_no: str
    account_name: str
    branch_code: str
    ar_type: str
    beginning_balance: float
    total_debet: float
    total_kredit: float
    ending_balance: float
    rows: list[HistoryRow]

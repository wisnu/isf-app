from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, field_validator


CHANNEL_CODE_MAP: dict[str, str] = {'K': 'P', 'C': 'R', 'B': 'A', 'A': 'G'}


class PenghimpunanItem(BaseModel):
    product_id: int
    account_no: str
    amount: float
    description: str = ''
    fund_entity: int
    percentage_of_amil: float = 0.0

    @field_validator('amount')
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('amount harus > 0')
        return v


class PenghimpunanCreate(BaseModel):
    actual_date: str
    reference_no: str | None = None
    description: str = ''
    paid_to: str | None = None
    donor_id: int | None = None
    donor_no: str | None = None
    donor_name: str | None = None
    marketer_id: int | None = None
    sponsor_id: int | None = None
    volunteer_id: str | None = None
    payment_type: Literal['K', 'C', 'B', 'A']
    payment_account_no: str | None = None
    asset_code: str | None = None
    asset_currency: str | None = None
    rate: float = 1.0
    currency_code: str = 'IDR'
    product_branch_code: str
    items: list[PenghimpunanItem]

    @field_validator('items')
    @classmethod
    def items_not_empty(cls, v: list) -> list:
        if not v:
            raise ValueError('items tidak boleh kosong')
        return v

    @field_validator('actual_date')
    @classmethod
    def valid_date(cls, v: str) -> str:
        from datetime import date
        date.fromisoformat(v)
        return v


class PenghimpunanListRow(BaseModel):
    transaction_id: int
    transaction_no: str | None
    actual_date: str
    description: str | None
    amount: float
    channel_code: str | None
    channel_account_no: str | None
    channel_name: str | None
    inputer: str | None
    auth_status: str | None
    auth_action: str | None = None
    branch_code: str | None
    donor_name: str | None


class PenghimpunanCreateResult(BaseModel):
    transaction_id: int
    transaction_no: str

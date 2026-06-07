from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, field_validator


FUND_ENTITY_MAP: dict[str, int] = {'Z': 1, 'I': 2, 'T': 2, 'W': 3, 'A': 4, 'N': 5}

CHANNEL_CODE_MAP: dict[str, str] = {'K': 'P', 'C': 'R', 'B': 'A', 'A': 'G'}

ASHNAF_LIST = [
    {'code': 'F', 'name': 'Fakir'},
    {'code': 'M', 'name': 'Miskin'},
    {'code': 'A', 'name': 'Amil'},
    {'code': 'K', 'name': 'Mualaf'},
    {'code': 'R', 'name': 'Riqab'},
    {'code': 'G', 'name': 'Gharimin'},
    {'code': 'S', 'name': 'Fi Sabilillah'},
    {'code': 'I', 'name': 'Ibnu Sabil'},
]


class PenyaluranItem(BaseModel):
    product_id: int
    account_no: str
    ashnaf: str
    amount: float
    description: str = ''
    fund_entity: int
    dist_item_account: str | None = None
    budget_id: int | None = None
    budget_code: str | None = None
    distribution_category: str | None = None

    @field_validator('amount')
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('amount harus > 0')
        return v


class PenyaluranCreate(BaseModel):
    actual_date: str
    reference_no: str | None = None
    description: str = ''
    paid_to: str | None = None
    received_from: str | None = None
    payment_type: Literal['K', 'C', 'B', 'A']
    payment_account_no: str | None = None
    asset_code: str | None = None
    asset_currency: str | None = None
    rate: float = 1.0
    currency_code: str = 'IDR'
    fund_account_no: str
    product_branch_code: str
    donor_id: int | None = None
    sponsor_id: int | None = None
    volunteer_id: str | None = None
    items: list[PenyaluranItem]

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


class PenyaluranListRow(BaseModel):
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
    branch_code: str | None


class PenyaluranListPage(BaseModel):
    data: list[PenyaluranListRow]
    pagination: dict


class RekeningRow(BaseModel):
    account_no: str
    account_name: str
    account_interface: str | None
    currency_code: str | None
    branch_code: str | None
    bank_name: str | None = None
    bank_account_no: str | None = None
    cash_code: str | None = None
    product_id: int | None = None
    fund_category: str | None = None


class ProductRow(BaseModel):
    product_id: int
    product_name: str
    fund_category: str
    product_code: str | None
    account_no: str
    fund_entity: int


class FundProductAccountRow(BaseModel):
    account_no: str
    account_name: str
    product_id: int | None
    fund_category: str | None


class CreateResult(BaseModel):
    transaction_id: int
    transaction_no: str

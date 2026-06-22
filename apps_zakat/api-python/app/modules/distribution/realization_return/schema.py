from __future__ import annotations

from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional


class RealizationReturnDetailInput(BaseModel):
    realization_detail_id: int
    return_amount: Decimal = Field(ge=0)
    detail_description: Optional[str] = Field(None, max_length=200)
    mustahiq_product_id: int
    account_no: str


class RealizationReturnCostInput(BaseModel):
    cost_item_id: int
    cost_amount: Decimal = Field(ge=0)
    additional_description: Optional[str] = Field(None, max_length=200)


class CreateRealizationReturnBody(BaseModel):
    return_date: str  # ISO YYYY-MM-DD
    return_description: str = Field(max_length=200)
    realization_id: int
    branch_code: Optional[str] = None
    user_input: Optional[str] = None
    details: list[RealizationReturnDetailInput]
    costs: list[RealizationReturnCostInput] = []


class UpdateRealizationReturnBody(BaseModel):
    return_date: str  # ISO YYYY-MM-DD
    return_description: str = Field(max_length=200)
    realization_id: int
    details: list[RealizationReturnDetailInput]
    costs: list[RealizationReturnCostInput] = []


class RealizationReturnRow(BaseModel):
    return_id: int
    return_date: Optional[str]  # ISO YYYY-MM-DD
    return_description: Optional[str]
    return_amount: Optional[float]
    realization_amount: Optional[float]
    memo_number: Optional[str]
    branch_code: Optional[str]


class RealizationReturnDetailRow(BaseModel):
    return_detail_id: int
    realization_detail_id: int
    mustahiq_product_id: Optional[int]
    mustahiq_product_name: Optional[str]
    account_no: Optional[str]
    account_name: Optional[str]
    realization_amount: Optional[float]
    return_amount: Optional[float]
    detail_description: Optional[str]


class RealizationReturnCostRow(BaseModel):
    cost_id: int
    cost_item_id: Optional[int]
    cost_item_code: Optional[str]
    cost_item_description: Optional[str]
    cost_amount: Optional[float]


class RealizationReturnDetail(BaseModel):
    return_id: int
    return_date: Optional[str]  # ISO YYYY-MM-DD
    return_description: Optional[str]
    return_amount: Optional[float]
    cost_amount: Optional[float]
    realization_id: Optional[int]
    realization_date: Optional[str]  # ISO YYYY-MM-DD
    realization_description: Optional[str]
    realization_amount: Optional[float]
    memo_number: Optional[str]
    branch_code: Optional[str]
    details: list[RealizationReturnDetailRow]
    costs: list[RealizationReturnCostRow]


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class RealizationReturnList(BaseModel):
    rows: list[RealizationReturnRow]
    pagination: Pagination


class CostItem(BaseModel):
    cost_item_id: int
    cost_item_code: Optional[str]
    cost_item_description: Optional[str]


class RealizationLookupItem(BaseModel):
    realization_id: int
    realization_date: Optional[str]  # ISO YYYY-MM-DD
    realization_description: Optional[str]
    realization_amount: Optional[float]
    realization_type: Optional[str]
    memo_number: Optional[str]


class RealizationDetailLookupRow(BaseModel):
    realization_detail_id: int
    realization_amount: Optional[float]
    account_no: Optional[str]
    mustahiq_product_id: int
    mustahiq_product_name: Optional[str]
    account_name: Optional[str]

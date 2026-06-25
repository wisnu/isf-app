from __future__ import annotations

from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class ZakatObjectItem(BaseModel):
    id: int
    code: str
    name: str


class BszRow(BaseModel):
    bsz_id: int
    bsz_number: str
    donor_id: int
    donor_name: str
    donor_no: str
    bsz_date: str
    period_begin: str
    period_end: str
    total: float


class BszList(BaseModel):
    rows: list[BszRow]
    pagination: Pagination


class BszDetailItem(BaseModel):
    item: int
    zakat_object: str
    year: int
    percentage: float
    basic_value: float
    zakah_value: float


class BszTransactionItem(BaseModel):
    transaction_item_id: int
    transaction_no: str
    transaction_date: str
    amount: float
    account_name: str
    description: str | None
    zakah_object: str


class BszDetail(BaseModel):
    bsz_id: int
    bsz_number: str
    donor_id: int
    donor_name: str
    donor_no: str
    npwz: str | None
    npwp: str | None
    address: str | None
    bsz_date: str
    period_begin: str
    period_end: str
    items: list[BszDetailItem]
    transactions: list[BszTransactionItem]


class AvailableTransaction(BaseModel):
    transaction_item_id: int
    transaction_no: str
    transaction_date: str
    amount: float
    account_name: str
    description: str | None
    zakah_object: str


class CreateBszDetailItem(BaseModel):
    item: int
    year: int
    percentage: float
    basic_value: float
    zakah_value: float


class CreateBszTransactionItem(BaseModel):
    transaction_item_id: int
    zakah_object: str


class CreateBszBody(BaseModel):
    donor_id: int
    period_begin: str
    period_end: str
    items: list[CreateBszDetailItem]
    transactions: list[CreateBszTransactionItem]

from __future__ import annotations
from pydantic import BaseModel


class TransaksiRow(BaseModel):
    transactionid: int
    transactionno: str | None
    transactiondate: str   # ISO YYYY-MM-DD
    actualdate: str        # ISO YYYY-MM-DD
    amount: float
    donorno: str | None
    donorname: str | None
    referenceno: str | None
    description: str | None
    inputer: str | None
    authstatus: str | None
    isposted: str | None
    authoperationmode: str | None
    branchcode: str | None
    channelaccountno: str | None
    channelname: str | None
    exttransactionid: int | None
    titlesubsystem: str | None


class JournalItem(BaseModel):
    journalitem_no: int
    fl_account: str | None
    account_name: str | None
    branch_code: str | None
    valuta_code: str | None
    amount_debit: float
    amount_credit: float
    description: str | None
    subaccountcode: str | None
    subaccountname: str | None


class TransaksiDetail(TransaksiRow):
    journal_items: list[JournalItem]


class DeleteResult(BaseModel):
    deleted: bool
    pending_approval: bool
    message: str


class RepostResult(BaseModel):
    journal_no: str
    success: bool


class SearchPage(BaseModel):
    rows: list[TransaksiRow]
    total: int
    page: int
    page_size: int
    total_pages: int

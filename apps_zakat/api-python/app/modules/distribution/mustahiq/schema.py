from __future__ import annotations

from pydantic import BaseModel


class BankAccountItem(BaseModel):
    bank_account_id: int | None = None
    account_no: str | None = None
    account_name: str | None = None
    bank_code: str | None = None
    is_default: str = 'F'


class MustahiqRow(BaseModel):
    mustahiq_id: int
    no_mustahiq: str | None
    name: str | None
    address: str | None
    phone_number: str | None
    status: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class MustahiqList(BaseModel):
    rows: list[MustahiqRow]
    pagination: Pagination


class BankAccountDetail(BaseModel):
    bank_account_id: int
    account_no: str | None
    account_name: str | None
    bank_code: str | None
    is_default: str | None


class MustahiqCorporateDetail(BaseModel):
    mustahiq_id: int
    no_mustahiq: str | None
    name: str | None
    address: str | None
    address_kelurahan: str | None
    address_kecamatan: str | None
    province_id: int | None
    postal_code: str | None
    reference_by: str | None
    phone_number: str | None
    cp_name: str | None
    cp_phone_number: str | None
    cp_mobile_number: str | None
    status: str | None
    bank_accounts: list[BankAccountDetail]


class MustahiqPersonalDetail(BaseModel):
    mustahiq_id: int
    no_mustahiq: str | None
    name: str | None
    address: str | None
    address_kelurahan: str | None
    address_kecamatan: str | None
    province_id: int | None
    postal_code: str | None
    reference_by: str | None
    phone_number: str | None
    gender: str | None
    ashnaf: str | None
    birth_place: str | None
    birth_date: str | None  # ISO YYYY-MM-DD
    identity_number: str | None
    identity_type: str | None
    religion: int | None
    total_family: int | None
    formal_education: str | None  # varchar(1): '0'..'6'
    income: int | None
    marital: str | None
    work_sector: str | None
    status: str | None
    bank_accounts: list[BankAccountDetail]


class CreateUpdateCorporateBody(BaseModel):
    name: str
    address: str | None = None
    address_kelurahan: str | None = None
    address_kecamatan: str | None = None
    province_id: int | None = None
    postal_code: str | None = None
    reference_by: str | None = None
    phone_number: str | None = None
    cp_name: str | None = None
    cp_phone_number: str | None = None
    cp_mobile_number: str | None = None
    bank_accounts: list[BankAccountItem] = []


class CreateUpdatePersonalBody(BaseModel):
    name: str
    address: str | None = None
    address_kelurahan: str | None = None
    address_kecamatan: str | None = None
    province_id: int | None = None
    postal_code: str | None = None
    reference_by: str | None = None
    phone_number: str | None = None
    gender: str | None = None
    ashnaf: str | None = None
    birth_place: str | None = None
    birth_date: str | None = None  # ISO YYYY-MM-DD
    identity_number: str | None = None
    identity_type: str | None = None
    religion: int | None = None
    total_family: int | None = None
    formal_education: str | None = None  # varchar(1)
    income: int | None = None
    marital: str | None = None
    work_sector: str | None = None
    bank_accounts: list[BankAccountItem] = []


class ToggleStatusBody(BaseModel):
    status: str  # 'A' or 'N'


class ProvinceLookupItem(BaseModel):
    province_id: int
    province_name: str


class BankLookupItem(BaseModel):
    bank_code: str
    bank_short_name: str | None
    bank_name: str | None

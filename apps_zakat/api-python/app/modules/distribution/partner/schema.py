from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class PartnerRow(BaseModel):
    partner_id: int
    name: str | None
    address: str | None
    phone_number: str | None
    status: str | None


class PartnerDetail(BaseModel):
    partner_id: int
    name: str | None
    address: str | None
    address_kelurahan: str | None
    address_kecamatan: str | None
    address_city: str | None
    phone_number: str | None
    email: str | None
    cp_name: str | None
    cp_address: str | None
    cp_mobile_phone: str | None
    cp_email: str | None
    status: str | None


class CreateUpdatePartnerBody(BaseModel):
    name: str
    address: Optional[str] = None
    address_kelurahan: Optional[str] = None
    address_kecamatan: Optional[str] = None
    address_city: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    cp_name: Optional[str] = None
    cp_address: Optional[str] = None
    cp_mobile_phone: Optional[str] = None
    cp_email: Optional[str] = None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class PartnerList(BaseModel):
    rows: list[PartnerRow]
    pagination: Pagination

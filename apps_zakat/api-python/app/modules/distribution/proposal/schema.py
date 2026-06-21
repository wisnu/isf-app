from __future__ import annotations

from pydantic import BaseModel


class ProposalRow(BaseModel):
    proposal_id: int
    proposal_no: str | None
    proposal_date: str | None  # ISO YYYY-MM-DD
    received_date: str | None  # ISO YYYY-MM-DD
    description: str | None
    nominal: float | None
    received_by: str | None
    reference_by: str | None
    reference_position: int | None
    status: str | None  # 'B' or 'S'
    mustahiq_id: int | None
    mustahiq_name: str | None
    product_group_id: int | None
    product_group_name: str | None
    branch_code: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class ProposalList(BaseModel):
    rows: list[ProposalRow]
    pagination: Pagination


class ProposalDetail(BaseModel):
    proposal_id: int
    proposal_no: str | None
    proposal_date: str | None  # ISO YYYY-MM-DD
    received_date: str | None  # ISO YYYY-MM-DD
    description: str | None
    nominal: float | None
    received_by: str | None
    reference_by: str | None
    reference_position: int | None
    status: str | None  # 'B' or 'S'
    mustahiq_id: int | None
    mustahiq_name: str | None
    product_group_id: int | None
    product_group_name: str | None
    branch_code: str | None
    address_street: str | None
    address_kelurahan: str | None
    address_kecamatan: str | None


class CreateProposalBody(BaseModel):
    mustahiq_id: int
    product_group_id: int
    proposal_date: str  # ISO YYYY-MM-DD
    received_date: str  # ISO YYYY-MM-DD
    description: str
    nominal: float
    received_by: str | None = None
    reference_by: str | None = None
    reference_position: int | None = None
    branch_code: str


class UpdateProposalBody(BaseModel):
    mustahiq_id: int
    product_group_id: int
    proposal_date: str  # ISO YYYY-MM-DD
    received_date: str  # ISO YYYY-MM-DD
    description: str
    nominal: float
    received_by: str | None = None
    reference_by: str | None = None
    reference_position: int | None = None


class ProductGroupLookupItem(BaseModel):
    product_group_id: int
    product_group_code: str | None
    product_group_name: str | None


class MustahiqLookupItem(BaseModel):
    mustahiq_id: int
    mustahiq_name: str | None


class TotalByMustahiqRow(BaseModel):
    mustahiq_id: int
    mustahiq_name: str | None
    total_nominal: float


class TotalByMustahiqResponse(BaseModel):
    data: list[TotalByMustahiqRow]

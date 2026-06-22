from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


PROGRAM_TYPE_CHOICES = {'R': 'Rutin', 'N': 'Non Rutin'}
FUND_CATEGORY_CHOICES = {'Z': 'Zakat', 'I': 'Infaq', 'W': 'Wakaf', 'A': 'Amil', 'N': 'Non Halal'}
STATUS_CHOICES = {'A': 'Aktif', 'N': 'Non Aktif'}


class DistributionProgramRow(BaseModel):
    program_id: int
    code: str | None
    name: str | None
    program_type: str | None
    program_type_name: str | None
    program_group_id: int | None
    program_group_name: str | None
    fund_category: str | None
    fund_category_name: str | None
    status: str | None


class DistributionProgramDetail(BaseModel):
    program_id: int
    code: str | None
    name: str | None
    description: str | None
    program_type: str | None
    program_type_name: str | None
    program_group_id: int | None
    program_group_name: str | None
    fund_category: str | None
    fund_category_name: str | None
    status: str | None


class CreateUpdateDistributionProgramBody(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    program_type: str
    program_group_id: int
    fund_category: str
    status: Optional[str] = 'A'


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class DistributionProgramList(BaseModel):
    rows: list[DistributionProgramRow]
    pagination: Pagination

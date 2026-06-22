from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class WorkSectorRow(BaseModel):
    work_sector_id: int
    code: str | None
    name: str | None
    status: str | None


class WorkSectorDetail(BaseModel):
    work_sector_id: int
    code: str | None
    name: str | None
    status: str | None


class CreateUpdateWorkSectorBody(BaseModel):
    code: str
    name: str
    status: Optional[str] = 'A'


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class WorkSectorList(BaseModel):
    rows: list[WorkSectorRow]
    pagination: Pagination

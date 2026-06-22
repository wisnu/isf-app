from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class ProgramTypeRow(BaseModel):
    program_type_id: int
    code: str | None
    name: str | None
    description: str | None
    status: str | None


class ProgramTypeDetail(BaseModel):
    program_type_id: int
    code: str | None
    name: str | None
    description: str | None
    status: str | None


class CreateUpdateProgramTypeBody(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    status: Optional[str] = 'A'


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class ProgramTypeList(BaseModel):
    rows: list[ProgramTypeRow]
    pagination: Pagination


class ProgramTypeLookupItem(BaseModel):
    program_type_id: int
    name: str | None

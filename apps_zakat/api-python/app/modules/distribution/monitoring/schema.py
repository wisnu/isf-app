from __future__ import annotations

from pydantic import BaseModel, Field


class PersonInput(BaseModel):
    visit_person_name: str = Field(max_length=100)
    visit_person_position: str = Field(max_length=100)


class ItemInput(BaseModel):
    visit_item_annotation: str = Field(max_length=200)


class VisitPersonRow(BaseModel):
    visit_person_id: int
    visit_person_name: str
    visit_person_position: str


class VisitItemRow(BaseModel):
    visit_item_id: int
    visit_item_annotation: str


class MustahiqLookupItem(BaseModel):
    mustahiq_id: int
    mustahiq_name: str
    address: str | None


class ProgramLookupItem(BaseModel):
    mustahiq_product_id: int
    program_name: str | None
    mustahiq_product_name: str | None
    mustahiq_name: str | None


class VisitRow(BaseModel):
    visit_id: int
    visit_date: str  # ISO YYYY-MM-DD
    visit_location: str
    visit_address: str
    mustahiq_name: str | None
    program_name: str | None
    mustahiq_product_name: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class VisitList(BaseModel):
    rows: list[VisitRow]
    pagination: Pagination


class VisitDetail(VisitRow):
    visit_begin_time: str | None  # ISO time format or NULL
    visit_end_time: str | None  # ISO time format or NULL
    persons_amil: list[VisitPersonRow]
    persons_mustahiq: list[VisitPersonRow]
    purposes: list[VisitItemRow]
    results: list[VisitItemRow]
    followups: list[VisitItemRow]


class CreateVisitBody(BaseModel):
    mustahiq_id: int
    mustahiq_product_id: int | None = None
    visit_address: str = Field(max_length=200)
    visit_location: str = Field(max_length=200)
    visit_date: str  # ISO YYYY-MM-DD
    visit_begin_time: str | None = None
    visit_end_time: str | None = None
    persons_amil: list[PersonInput] = Field(min_length=1)
    persons_mustahiq: list[PersonInput] = Field(min_length=1)
    purposes: list[ItemInput] = Field(min_length=1)
    results: list[ItemInput] = Field(min_length=1)
    followups: list[ItemInput] = Field(min_length=1)


class UpdateVisitBody(BaseModel):
    mustahiq_id: int
    mustahiq_product_id: int | None = None
    visit_address: str = Field(max_length=200)
    visit_location: str = Field(max_length=200)
    visit_date: str  # ISO YYYY-MM-DD
    visit_begin_time: str | None = None
    visit_end_time: str | None = None
    persons_amil: list[PersonInput] = Field(min_length=1)
    persons_mustahiq: list[PersonInput] = Field(min_length=1)
    purposes: list[ItemInput] = Field(min_length=1)
    results: list[ItemInput] = Field(min_length=1)
    followups: list[ItemInput] = Field(min_length=1)

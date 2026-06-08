from __future__ import annotations
from typing import Any
from pydantic import BaseModel


class SubmissionIn(BaseModel):
    entity_type: str
    module: str
    payload: dict[str, Any]


class UpdatePayloadIn(BaseModel):
    payload: dict[str, Any]


class ApproveIn(BaseModel):
    notes: str | None = None


class RejectIn(BaseModel):
    notes: str


class BulkApproveIn(BaseModel):
    ids: list[int]
    notes: str | None = None


class BulkRejectIn(BaseModel):
    ids: list[int]
    notes: str


class SaveAndSubmitIn(BaseModel):
    entity_type: str
    module: str
    payload: dict[str, Any]


class UpdateAndSubmitIn(BaseModel):
    payload: dict[str, Any]

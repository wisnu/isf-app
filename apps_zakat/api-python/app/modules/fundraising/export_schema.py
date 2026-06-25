"""Schemas for fundraising export endpoints."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


# ── Dropdown / List Responses ─────────────────────────────────────────────────


class HCBatchOption(BaseModel):
    """HC Batch for dropdown selection."""
    id: int = Field(..., description="Batch ID")
    name: str = Field(..., description="Batch name/description")
    batch_date: date = Field(..., description="Batch date")


class HCBatchListResponse(BaseModel):
    """List of HC batches for dropdown."""
    rows: list[HCBatchOption]


# ── Export Parameters ─────────────────────────────────────────────────────────


class ExportHCBatchParams(BaseModel):
    """Parameters for HC Batch export."""
    batch_id: int = Field(..., gt=0, description="Batch ID to export")


class ExportWebsiteNewParams(BaseModel):
    """Parameters for Website (date-range) export."""
    date_from: date = Field(..., description="Start date (ISO YYYY-MM-DD)")
    date_to: date = Field(..., description="End date (ISO YYYY-MM-DD)")


# ── Export Row Models (for reference, not directly used in response) ──────────


class ExportHCBatchRow(BaseModel):
    """Single row from HC Batch export."""
    batch_id: int
    batch_name: str
    batch_date: date
    donor_number: str
    donor_name: str
    product_code: str
    product_name: str
    donation_amount: Decimal
    donation_date: date


class ExportWebsiteNewRow(BaseModel):
    """Single row from Website (date-range) export."""
    donor_number: str
    donor_name: str
    gender: Optional[str]
    gender_display: str
    marital_state: Optional[str]
    marital_display: str
    address: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    organization_name: Optional[str]
    is_internal_employee: Optional[str]
    employee_display: str
    total_donation: Decimal
    first_donation_date: Optional[date]
    last_donation_date: Optional[date]
    # Product pivot columns (8 products × 2 columns each = 16 columns)
    zis_amount: Optional[Decimal]
    zis_count: Optional[int]
    fitrah_amount: Optional[Decimal]
    fitrah_count: Optional[int]
    infaq_amount: Optional[Decimal]
    infaq_count: Optional[int]
    anak_asuh_amount: Optional[Decimal]
    anak_asuh_count: Optional[int]
    anak_yatim_amount: Optional[Decimal]
    anak_yatim_count: Optional[int]
    dpu_amount: Optional[Decimal]
    dpu_count: Optional[int]
    wakaf_amount: Optional[Decimal]
    wakaf_count: Optional[int]
    qurban_amount: Optional[Decimal]
    qurban_count: Optional[int]

"""Pydantic schemas for HC ZIS upload functionality."""
from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class HCZisItem(BaseModel):
    """Single row from HC ZIS file."""
    data_no: int
    business_area_code: str
    business_area_desc: str = ""
    employee_number: str
    employee_name: str
    birth_place: str = ""
    work_area_name: str = ""
    mobile_phone: str = ""
    birth_date: str = ""  # ISO YYYY-MM-DD or empty
    gender: str = ""  # 'L' or 'P'
    marital_status: str = ""  # 'K', 'B', 'S'
    position: str = ""
    organization_unit: str = ""
    zakat_amount: float = 0.0
    infaq_amount: float = 0.0
    anak_asuh_amount: float = 0.0
    anak_yatim_amount: float = 0.0
    wakaf_amount: float = 0.0  # stored but NOT processed
    taqurma_amount: float = 0.0  # Titipan Qurban
    total_amount: float = 0.0


class HCZisTotals(BaseModel):
    """Totals summary across all items."""
    zakat_amount: float = 0.0
    zakat_count: int = 0
    infaq_amount: float = 0.0
    infaq_count: int = 0
    anak_asuh_amount: float = 0.0
    anak_asuh_count: int = 0
    anak_yatim_amount: float = 0.0
    anak_yatim_count: int = 0
    wakaf_amount: float = 0.0
    wakaf_count: int = 0
    taqurma_amount: float = 0.0
    taqurma_count: int = 0
    grand_total: float = 0.0
    grand_count: int = 0


class HCZisParseResult(BaseModel):
    """Result of parsing HC ZIS file."""
    batch_period_desc: str
    tanggal_transaksi: str = ""  # ISO YYYY-MM-DD — echoed back for submit payload
    namafile: str = ""           # original filename — echoed back for submit payload
    totals: HCZisTotals
    items: list[HCZisItem]
    is_duplicate: bool = False


class HCZisSubmitRequest(BaseModel):
    """Request to submit HC ZIS batch."""
    batch_period_desc: str
    tanggal_transaksi: str  # ISO YYYY-MM-DD
    namafile: str
    totals: HCZisTotals
    items: list[HCZisItem]


class HCZisUpdateDateRequest(BaseModel):
    """Request to update batch transaction date."""
    tanggal_transaksi: str  # ISO YYYY-MM-DD


class HCZisBatchSummary(BaseModel):
    """Summary row for batch list."""
    batch_id: int
    batch_period_desc: str
    tanggal_transaksi: str  # ISO YYYY-MM-DD
    namafile: str
    upload_user_id: str
    upload_date: str  # ISO timestamp
    grand_total: float
    grand_count: int
    submission_id: Optional[int] = None
    submission_status: Optional[str] = None  # PENDING/PROCESSING/AUTHORIZED/REJECTED


class HCZisBatchDetail(BaseModel):
    """Detailed batch with all items."""
    batch_id: int
    batch_period_desc: str
    tanggal_transaksi: str
    namafile: str
    upload_user_id: str
    upload_date: str
    submission_id: Optional[int] = None
    submission_status: Optional[str] = None
    totals: HCZisTotals
    items: list[HCZisItem]


class HCZisSubmitResponse(BaseModel):
    """Response after submit."""
    submission_id: int
    status: str
    kode_entri: str
    entity_type: str

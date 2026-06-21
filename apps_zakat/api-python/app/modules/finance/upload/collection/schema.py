from __future__ import annotations
from pydantic import BaseModel


PRODUCT_ID_MAP: dict[str, int] = {
    'ZakatProfesi':    518,
    'ZakatMaal':       5,
    'ZakatFitrah':     141,
    'ZakatPerusahaan': 575,
    'Infaq':           95,
    'InfaqTerikat':    572,
    'DPU':             145,
    'AnakYatim':       143,
    'AnakAsuh':        142,
    'TitipanWakaf':    12,
    'TitipanQurban':   574,
    'Qurban':          144,
    'NonHalal':        516,
    'Fidyah':          569,
}

FUND_ENTITY_MAP: dict[str, int] = {
    'Z': 1, 'T': 2, 'I': 2, 'W': 3, 'A': 4, 'N': 5,
}

PRODUCT_KEYS = list(PRODUCT_ID_MAP.keys())


class ParsedRow(BaseModel):
    row_no: int
    no_rekening: str
    tanggal: str          # ISO YYYY-MM-DD
    keterangan: str
    no_ref: str
    total_kredit: float
    zakat_profesi: float
    zakat_maal: float
    zakat_fitrah: float
    zakat_perusahaan: float
    infaq: float
    infaq_terikat: float
    dpu: float
    anak_yatim: float
    anak_asuh: float
    titipan_wakaf: float
    titipan_qurban: float
    qurban: float
    non_halal: float
    fidyah: float
    status: str           # 'valid', 'warning', 'invalid'
    pesan: str


class DraftRequest(BaseModel):
    filename: str
    branch_code: str
    rows: list[ParsedRow]


class DraftResponse(BaseModel):
    batch_id: int
    total_valid: int
    total_warning: int


class BatchSummary(BaseModel):
    batch_id: int
    filename: str
    upload_date: str       # ISO
    upload_user: str
    branch_code: str
    total_record: int
    total_amount: float
    authstatus: str        # P / A


class BatchItem(BaseModel):
    batch_item_id: int
    row_no: int
    no_rekening: str
    tanggal: str           # ISO
    keterangan: str
    no_ref: str
    total_kredit: float
    zakat_profesi: float
    zakat_maal: float
    zakat_fitrah: float
    zakat_perusahaan: float
    infaq: float
    infaq_terikat: float
    dpu: float
    anak_yatim: float
    anak_asuh: float
    titipan_wakaf: float
    titipan_qurban: float
    qurban: float
    non_halal: float
    fidyah: float
    status: str
    pesan: str
    transaction_no: str | None


class BatchDetail(BaseModel):
    batch_id: int
    filename: str
    upload_date: str
    upload_user: str
    branch_code: str
    total_record: int
    total_amount: float
    authstatus: str
    authorized_user: str | None
    items: list[BatchItem]


class ApproveResult(BaseModel):
    batch_id: int
    total_committed: int

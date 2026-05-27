from pydantic import BaseModel


class KpiPair(BaseModel):
    total: float
    delta_pct: float


class Kpis(BaseModel):
    penerimaan: KpiPair
    penyaluran: KpiPair
    saldo: KpiPair
    donatur_baru: KpiPair


class Trend(BaseModel):
    labels: list[str]
    penerimaan: list[float]
    penyaluran: list[float]


class AsnafItem(BaseModel):
    label: str
    amount: float


class Channel(BaseModel):
    label: str
    actual: float
    target: float


class Transaction(BaseModel):
    id: str
    date: str
    type: str
    channel: str
    amount: float
    donor: str


class DashboardSummary(BaseModel):
    tenant_id: str
    tenant_name: str
    period: str
    kpis: Kpis
    trend: Trend
    asnaf_distribution: list[AsnafItem]
    fundraising_channels: list[Channel]
    recent_transactions: list[Transaction]


# ── Schema v2 — real-data endpoints ──────────────────────────────────────────

class KpiCardData(BaseModel):
    total: float
    delta_pct: float | None = None   # None = tidak ada data bulan lalu
    format: str = "currency"         # "currency" | "count"


class AsnafItem2(BaseModel):
    label: str
    count: int


class TrendPoint(BaseModel):
    label: str        # "2026-01"
    penerimaan: float
    penyaluran: float


class AnggaranItem(BaseModel):
    owner_id: int
    owner_name: str
    anggaran: float
    realisasi: float
    pct: float        # realisasi / anggaran * 100, capped at 999


class RekeningItem(BaseModel):
    account_no: str
    account_name: str
    account_type: str        # "Bank" | "Kas Besar" | "Kas Kecil" | "Lainnya"
    bank_name: str | None
    balance: float


class MemoItem(BaseModel):
    memo_id: int
    memo_number: str | None
    subject: str | None
    amount: float | None
    memo_type: str          # "R" = Rutin, "N" = Non Rutin
    memo_date: str | None   # "YYYY-MM-DD"


class DashboardKeuangan(BaseModel):
    period: str             # "2026-05"
    kpis: dict[str, KpiCardData]
    trend: list[TrendPoint]
    asnaf: list[AsnafItem2]
    anggaran: list[AnggaranItem]
    rekening: list[RekeningItem]


class DashboardPenyaluran(BaseModel):
    period: str
    kpis: dict[str, KpiCardData]
    anggaran: list[AnggaranItem]
    memo_terbaru: list[MemoItem]


class FundBreakdownItem(BaseModel):
    fund_entity: int
    fund_name: str
    total: float
    pct: float


class TrendFundPoint(BaseModel):
    label: str        # "2026-01"
    penerimaan: float


class TopDonorItem(BaseModel):
    donor_name: str
    donor_type: str         # "I" | "C"
    donor_type_label: str   # "Individu" | "Korporat"
    productname: str | None
    total_amount: float


class DashboardPenghimpunan(BaseModel):
    period: str
    kpis: dict[str, KpiCardData]
    trend: list[TrendFundPoint]
    fund_breakdown: list[FundBreakdownItem]
    top_donor: list[TopDonorItem]

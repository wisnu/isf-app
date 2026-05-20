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

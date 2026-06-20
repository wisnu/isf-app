from pydantic import BaseModel


class KpiPair(BaseModel):
    total: float
    delta_pct: float


class Kpis(BaseModel):
    collection: KpiPair
    distribution: KpiPair
    balance: KpiPair
    new_donors: KpiPair


class Trend(BaseModel):
    labels: list[str]
    collection: list[float]
    distribution: list[float]


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
    collection: float
    distribution: float


class BudgetItem(BaseModel):
    owner_id: int
    owner_name: str
    budget: float
    realization: float
    pct: float        # realization / budget * 100, capped at 999


class AccountItem(BaseModel):
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


class DashboardFinance(BaseModel):
    period: str             # "2026-05"
    kpis: dict[str, KpiCardData]
    trend: list[TrendPoint]
    asnaf: list[AsnafItem2]
    budget: list[BudgetItem]
    account: list[AccountItem]


class DashboardDistribution(BaseModel):
    period: str
    kpis: dict[str, KpiCardData]
    budget: list[BudgetItem]
    recent_memo: list[MemoItem]

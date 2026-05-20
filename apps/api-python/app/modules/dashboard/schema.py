from pydantic import BaseModel


class AmountSummary(BaseModel):
    total: int
    period: str


class DashboardSummary(BaseModel):
    tenant_id: str
    tenant_name: str
    penerimaan: AmountSummary
    penyaluran: AmountSummary

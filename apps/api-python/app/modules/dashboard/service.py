from app.modules.dashboard.schema import AmountSummary, DashboardSummary

_DUMMY: dict[str, DashboardSummary] = {
    "perusahaan_a": DashboardSummary(
        tenant_id="perusahaan_a",
        tenant_name="Lembaga ZISWAF A",
        penerimaan=AmountSummary(total=1_250_000_000, period="2026-05"),
        penyaluran=AmountSummary(total=875_000_000, period="2026-05"),
    ),
    "perusahaan_b": DashboardSummary(
        tenant_id="perusahaan_b",
        tenant_name="Lembaga ZISWAF B",
        penerimaan=AmountSummary(total=920_000_000, period="2026-05"),
        penyaluran=AmountSummary(total=640_000_000, period="2026-05"),
    ),
}


def get_summary(tenant_id: str) -> DashboardSummary | None:
    return _DUMMY.get(tenant_id)

from app.modules.dashboard.schema import (
    AsnafItem,
    Channel,
    DashboardSummary,
    Kpis,
    KpiPair,
    Trend,
    Transaction,
)


_DUMMY: dict[str, DashboardSummary] = {
    "perusahaan_a": DashboardSummary(
        tenant_id="perusahaan_a",
        tenant_name="Lembaga ZISWAF A",
        period="2026-05",
        kpis=Kpis(
            penerimaan=KpiPair(total=1_250_000_000, delta_pct=12.4),
            penyaluran=KpiPair(total=875_000_000, delta_pct=-3.2),
            saldo=KpiPair(total=4_800_000_000, delta_pct=8.1),
            donatur_baru=KpiPair(total=142, delta_pct=21.5),
        ),
        trend=Trend(
            labels=["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
            penerimaan=[820_000_000, 905_000_000, 980_000_000, 1_100_000_000, 1_112_000_000, 1_250_000_000],
            penyaluran=[610_000_000, 680_000_000, 740_000_000, 810_000_000, 905_000_000, 875_000_000],
        ),
        asnaf_distribution=[
            AsnafItem(label="Fakir", amount=245_000_000),
            AsnafItem(label="Miskin", amount=198_000_000),
            AsnafItem(label="Amil", amount=87_500_000),
            AsnafItem(label="Mualaf", amount=52_000_000),
            AsnafItem(label="Riqab", amount=0),
            AsnafItem(label="Gharimin", amount=78_000_000),
            AsnafItem(label="Fi Sabilillah", amount=132_000_000),
            AsnafItem(label="Ibnu Sabil", amount=82_500_000),
        ],
        fundraising_channels=[
            Channel(label="Transfer Bank", actual=720_000_000, target=800_000_000),
            Channel(label="Gerai & Booth", actual=240_000_000, target=200_000_000),
            Channel(label="Payroll", actual=180_000_000, target=250_000_000),
            Channel(label="E-Wallet", actual=110_000_000, target=150_000_000),
        ],
        recent_transactions=[
            Transaction(id="tx_a01", date="2026-05-19", type="Zakat Mal", channel="Transfer Bank", amount=15_000_000, donor="Budi Santoso"),
            Transaction(id="tx_a02", date="2026-05-19", type="Infaq", channel="E-Wallet", amount=250_000, donor="Siti Aminah"),
            Transaction(id="tx_a03", date="2026-05-18", type="Wakaf Uang", channel="Transfer Bank", amount=5_000_000, donor="Hamba Allah"),
            Transaction(id="tx_a04", date="2026-05-18", type="Zakat Fitrah", channel="Gerai & Booth", amount=160_000, donor="Keluarga Hidayat"),
            Transaction(id="tx_a05", date="2026-05-18", type="Sedekah", channel="E-Wallet", amount=100_000, donor="Anonim"),
            Transaction(id="tx_a06", date="2026-05-17", type="Zakat Mal", channel="Payroll", amount=2_500_000, donor="Rina Wijaya"),
            Transaction(id="tx_a07", date="2026-05-17", type="Infaq", channel="Transfer Bank", amount=750_000, donor="PT Berkah Sejahtera"),
            Transaction(id="tx_a08", date="2026-05-16", type="Wakaf Produktif", channel="Transfer Bank", amount=50_000_000, donor="Yayasan Cahaya"),
            Transaction(id="tx_a09", date="2026-05-16", type="Sedekah", channel="Gerai & Booth", amount=350_000, donor="Ibu Rini"),
            Transaction(id="tx_a10", date="2026-05-15", type="Zakat Mal", channel="Transfer Bank", amount=8_500_000, donor="Andi Pratama"),
        ],
    ),
    "perusahaan_b": DashboardSummary(
        tenant_id="perusahaan_b",
        tenant_name="Lembaga ZISWAF B",
        period="2026-05",
        kpis=Kpis(
            penerimaan=KpiPair(total=920_000_000, delta_pct=6.8),
            penyaluran=KpiPair(total=640_000_000, delta_pct=14.2),
            saldo=KpiPair(total=2_950_000_000, delta_pct=4.5),
            donatur_baru=KpiPair(total=89, delta_pct=-5.3),
        ),
        trend=Trend(
            labels=["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
            penerimaan=[640_000_000, 715_000_000, 760_000_000, 820_000_000, 861_000_000, 920_000_000],
            penyaluran=[420_000_000, 480_000_000, 525_000_000, 580_000_000, 560_000_000, 640_000_000],
        ),
        asnaf_distribution=[
            AsnafItem(label="Fakir", amount=178_000_000),
            AsnafItem(label="Miskin", amount=152_000_000),
            AsnafItem(label="Amil", amount=64_000_000),
            AsnafItem(label="Mualaf", amount=28_000_000),
            AsnafItem(label="Riqab", amount=0),
            AsnafItem(label="Gharimin", amount=56_000_000),
            AsnafItem(label="Fi Sabilillah", amount=98_000_000),
            AsnafItem(label="Ibnu Sabil", amount=64_000_000),
        ],
        fundraising_channels=[
            Channel(label="Transfer Bank", actual=520_000_000, target=600_000_000),
            Channel(label="Gerai & Booth", actual=145_000_000, target=180_000_000),
            Channel(label="Payroll", actual=98_000_000, target=120_000_000),
            Channel(label="E-Wallet", actual=157_000_000, target=140_000_000),
        ],
        recent_transactions=[
            Transaction(id="tx_b01", date="2026-05-19", type="Infaq", channel="E-Wallet", amount=500_000, donor="Dewi Lestari"),
            Transaction(id="tx_b02", date="2026-05-19", type="Zakat Mal", channel="Transfer Bank", amount=20_000_000, donor="PT Mulia Abadi"),
            Transaction(id="tx_b03", date="2026-05-18", type="Sedekah", channel="Gerai & Booth", amount=200_000, donor="Anonim"),
            Transaction(id="tx_b04", date="2026-05-18", type="Wakaf Uang", channel="Transfer Bank", amount=10_000_000, donor="Hamba Allah"),
            Transaction(id="tx_b05", date="2026-05-17", type="Zakat Fitrah", channel="Payroll", amount=160_000, donor="Karyawan A"),
            Transaction(id="tx_b06", date="2026-05-17", type="Infaq", channel="Transfer Bank", amount=1_000_000, donor="Fajar Hidayatullah"),
            Transaction(id="tx_b07", date="2026-05-16", type="Sedekah", channel="E-Wallet", amount=75_000, donor="Anonim"),
            Transaction(id="tx_b08", date="2026-05-16", type="Zakat Mal", channel="Gerai & Booth", amount=3_500_000, donor="Hj. Aminah"),
            Transaction(id="tx_b09", date="2026-05-15", type="Wakaf Produktif", channel="Transfer Bank", amount=25_000_000, donor="Yayasan Nurani"),
            Transaction(id="tx_b10", date="2026-05-15", type="Infaq", channel="E-Wallet", amount=300_000, donor="Lina M."),
        ],
    ),
}


def get_summary(tenant_id: str) -> DashboardSummary | None:
    return _DUMMY.get(tenant_id)

"""Dashboard service — gabungan dummy (summary lama) dan real-DB (v2)."""

from __future__ import annotations

import asyncio

from app.modules.dashboard.schema import (
    # Legacy
    AsnafItem, Channel, DashboardSummary, Kpis, KpiPair, Trend, Transaction,
    # v2
    BudgetItem, AsnafItem2, DashboardFinance, DashboardDistribution,
    KpiCardData, MemoItem, AccountItem, TrendPoint,
)
from app.shared.db import fetch_all, fetch_one, ping


# ── Helpers ──────────────────────────────────────────────────────────────────

def _prev_month(month: int, year: int) -> tuple[int, int]:
    if month == 1:
        return 12, year - 1
    return month - 1, year


def _last_6_months(month: int, year: int) -> list[tuple[int, int]]:
    """Returns [(month, year), ...] oldest→newest, length 6."""
    result = []
    for i in range(5, -1, -1):
        m = month - i
        y = year
        while m <= 0:
            m += 12
            y -= 1
        result.append((m, y))
    return result


def _pct(realization: float, budget: float) -> float:
    if budget <= 0:
        return 0.0
    return min(999.0, round(realization / budget * 100, 1))


_CASHTYPE_LABEL: dict[str, str] = {
    "B": "Bank",
    "G": "Kas Besar",
    "K": "Kas Kecil",
}


# ── Real-DB query functions ───────────────────────────────────────────────────

async def _sum_fund(month: int, year: int) -> float:
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(fund_amount), 0) AS total
        FROM dashboard.v_fund_monthyear_bycash
        WHERE fund_month = $1 AND fund_year = $2
        """,
        month, year,
    )
    return float(row["total"]) if row else 0.0


async def _sum_dist(month: int, year: int) -> float:
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(dist_amount), 0) AS total
        FROM dashboard.v_dist_monthyear_byproduct
        WHERE dist_month = $1 AND dist_year = $2
        """,
        month, year,
    )
    return float(row["total"]) if row else 0.0


async def _balance_total() -> float:
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(balance), 0) AS total
        FROM transaction.cashaccountall
        WHERE status = 'A'
        """
    )
    return float(row["total"]) if row else 0.0


async def _authorization_pending() -> int:
    row = await fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM transaction.transaction
        WHERE authstatus = 'O'
        """
    )
    return int(row["total"]) if row else 0


async def _kpi_card(current: float, prev: float, fmt: str = "currency") -> KpiCardData:
    if prev > 0:
        delta = round((current - prev) / prev * 100, 1)
    else:
        delta = None
    return KpiCardData(total=current, delta_pct=delta, format=fmt)


async def _trend_point(m: int, y: int) -> TrendPoint:
    fund, dist = await asyncio.gather(_sum_fund(m, y), _sum_dist(m, y))
    return TrendPoint(label=f"{y}-{m:02d}", collection=fund, distribution=dist)


async def _trend_6month(month: int, year: int) -> list[TrendPoint]:
    # Run all months concurrently — sequential awaits exceeded the BFF's 10s
    # read timeout (12 queries × ~1.6s). Pool max_size=10 absorbs the fan-out.
    months = _last_6_months(month, year)
    return list(await asyncio.gather(*(_trend_point(m, y) for m, y in months)))


async def _asnaf_dist(month: int, year: int) -> list[AsnafItem2]:
    rows = await fetch_all(
        """
        SELECT ashnaf_name AS label, COALESCE(SUM(count_ashnaf), 0)::int AS cnt
        FROM dashboard.v_ashnaf_bymonthyear
        WHERE realization_month = $1 AND realization_year = $2
        GROUP BY ashnaf_name
        ORDER BY cnt DESC
        """,
        month, year,
    )
    return [AsnafItem2(label=r["label"], count=r["cnt"]) for r in rows]


async def _budget_list(year: int) -> list[BudgetItem]:
    rows = await fetch_all(
        """
        SELECT
            ownerid,
            ownername,
            SUM(budget_amount)                          AS budget,
            SUM(COALESCE(budget_realization, 0))        AS realization
        FROM dashboard.v_budget_bymonthyear
        WHERE budget_year = $1
        GROUP BY ownerid, ownername
        ORDER BY budget DESC
        LIMIT 8
        """,
        year,
    )
    result: list[BudgetItem] = []
    for r in rows:
        ang = float(r["budget"] or 0)
        real = float(r["realization"] or 0)
        result.append(BudgetItem(
            owner_id=r["ownerid"],
            owner_name=r["ownername"] or "–",
            budget=ang,
            realization=real,
            pct=_pct(real, ang),
        ))
    return result


async def _account_list() -> list[AccountItem]:
    rows = await fetch_all(
        """
        SELECT
            accountno, accountname,
            cashaccounttype,
            bankname,
            balance
        FROM transaction.cashaccountall
        WHERE status = 'A'
        ORDER BY
            CASE cashaccounttype WHEN 'B' THEN 1 WHEN 'G' THEN 2 ELSE 3 END,
            accountname
        """
    )
    return [
        AccountItem(
            account_no=r["accountno"],
            account_name=r["accountname"] or "–",
            account_type=_CASHTYPE_LABEL.get(r["cashaccounttype"] or "", "Lainnya"),
            bank_name=r["bankname"],
            balance=float(r["balance"] or 0),
        )
        for r in rows
    ]


async def _recent_memo() -> list[MemoItem]:
    rows = await fetch_all(
        """
        SELECT
            realmemoid, realmemonumber, realmemosubject,
            realmemoamount, realizationmemotype,
            TO_CHAR(realmemodate, 'YYYY-MM-DD') AS memo_date
        FROM program.realizationmemo
        ORDER BY realmemodate DESC NULLS LAST
        LIMIT 5
        """
    )
    return [
        MemoItem(
            memo_id=r["realmemoid"],
            memo_number=r["realmemonumber"],
            subject=r["realmemosubject"],
            amount=float(r["realmemoamount"]) if r["realmemoamount"] is not None else None,
            memo_type=r["realizationmemotype"] or "N",
            memo_date=r["memo_date"],
        )
        for r in rows
    ]


async def _mustahiq_count(month: int, year: int) -> int:
    """Approx: sum count_ashnaf from distribution view for the period."""
    row = await fetch_one(
        """
        SELECT COALESCE(SUM(count_ashnaf), 0)::int AS total
        FROM dashboard.v_ashnaf_bymonthyear
        WHERE realization_month = $1 AND realization_year = $2
        """,
        month, year,
    )
    return int(row["total"]) if row else 0


# ── Public API ────────────────────────────────────────────────────────────────

async def get_finance(month: int, year: int) -> DashboardFinance | None:
    if not await ping():
        return None

    prev_m, prev_y = _prev_month(month, year)

    cur_fund   = await _sum_fund(month, year)
    prev_fund  = await _sum_fund(prev_m, prev_y)
    cur_dist   = await _sum_dist(month, year)
    prev_dist  = await _sum_dist(prev_m, prev_y)
    balance      = await _balance_total()
    otorisasi  = await _authorization_pending()

    return DashboardFinance(
        period=f"{year}-{month:02d}",
        kpis={
            "collection": await _kpi_card(cur_fund, prev_fund),
            "distribution": await _kpi_card(cur_dist, prev_dist),
            "balance": KpiCardData(total=balance, format="currency"),
            "authorization_pending": KpiCardData(total=otorisasi, format="count"),
        },
        trend=await _trend_6month(month, year),
        asnaf=await _asnaf_dist(month, year),
        budget=await _budget_list(year),
        account=await _account_list(),
    )


async def get_fund_distribution(month: int, year: int) -> DashboardDistribution | None:
    if not await ping():
        return None

    prev_m, prev_y = _prev_month(month, year)

    cur_dist  = await _sum_dist(month, year)
    prev_dist = await _sum_dist(prev_m, prev_y)
    mustahiq  = await _mustahiq_count(month, year)
    otorisasi = await _authorization_pending()

    return DashboardDistribution(
        period=f"{year}-{month:02d}",
        kpis={
            "distribution": await _kpi_card(cur_dist, prev_dist),
            "mustahiq": KpiCardData(total=mustahiq, format="count"),
            "authorization_pending": KpiCardData(total=otorisasi, format="count"),
        },
        budget=await _budget_list(year),
        recent_memo=await _recent_memo(),
    )


# ── Per-chart functions (FE fetches each widget independently) ───────────────
# Reuse the same helpers as the bundle composers above. Each returns the
# wrapped shape the frontend `useFetch` queries expect (period+kpis, trend,
# asnaf, budget, ...), or None when the DB is down (→ 503 in the router).

async def get_finance_kpis(month: int, year: int) -> dict | None:
    if not await ping():
        return None
    prev_m, prev_y = _prev_month(month, year)
    # Run the independent aggregates concurrently — sequential awaits pushed this
    # past the BFF's 10s read timeout under parallel widget load (pool contention).
    cur_fund, prev_fund, cur_dist, prev_dist, balance, otorisasi = await asyncio.gather(
        _sum_fund(month, year),
        _sum_fund(prev_m, prev_y),
        _sum_dist(month, year),
        _sum_dist(prev_m, prev_y),
        _balance_total(),
        _authorization_pending(),
    )
    return {
        "period": f"{year}-{month:02d}",
        "kpis": {
            "collection": (await _kpi_card(cur_fund, prev_fund)).model_dump(),
            "distribution": (await _kpi_card(cur_dist, prev_dist)).model_dump(),
            "balance": KpiCardData(total=balance, format="currency").model_dump(),
            "authorization_pending": KpiCardData(total=otorisasi, format="count").model_dump(),
        },
    }


async def get_finance_trend(month: int, year: int) -> dict | None:
    if not await ping():
        return None
    return {"trend": [p.model_dump() for p in await _trend_6month(month, year)]}


async def get_finance_asnaf(month: int, year: int) -> dict | None:
    if not await ping():
        return None
    return {"asnaf": [a.model_dump() for a in await _asnaf_dist(month, year)]}


async def get_finance_budget(year: int) -> dict | None:
    if not await ping():
        return None
    return {"budget": [a.model_dump() for a in await _budget_list(year)]}


async def get_finance_account() -> dict | None:
    if not await ping():
        return None
    return {"account": [r.model_dump() for r in await _account_list()]}


async def get_fund_distribution_kpis(month: int, year: int) -> dict | None:
    if not await ping():
        return None
    prev_m, prev_y = _prev_month(month, year)
    cur_dist, prev_dist, mustahiq, otorisasi = await asyncio.gather(
        _sum_dist(month, year),
        _sum_dist(prev_m, prev_y),
        _mustahiq_count(month, year),
        _authorization_pending(),
    )
    return {
        "period": f"{year}-{month:02d}",
        "kpis": {
            "distribution": (await _kpi_card(cur_dist, prev_dist)).model_dump(),
            "mustahiq": KpiCardData(total=mustahiq, format="count").model_dump(),
            "authorization_pending": KpiCardData(total=otorisasi, format="count").model_dump(),
        },
    }


async def get_fund_distribution_budget(year: int) -> dict | None:
    if not await ping():
        return None
    return {"budget": [a.model_dump() for a in await _budget_list(year)]}


async def get_fund_distribution_memo() -> dict | None:
    if not await ping():
        return None
    return {"recent_memo": [m.model_dump() for m in await _recent_memo()]}


# ── Legacy dummy (kept for existing /summary endpoint) ───────────────────────

_DUMMY: dict[str, DashboardSummary] = {
    "perusahaan_a": DashboardSummary(
        tenant_id="perusahaan_a",
        tenant_name="Lembaga ZISWAF A",
        period="2026-05",
        kpis=Kpis(
            collection=KpiPair(total=1_250_000_000, delta_pct=12.4),
            distribution=KpiPair(total=875_000_000, delta_pct=-3.2),
            balance=KpiPair(total=4_800_000_000, delta_pct=8.1),
            new_donors=KpiPair(total=142, delta_pct=21.5),
        ),
        trend=Trend(
            labels=["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
            collection=[820_000_000, 905_000_000, 980_000_000, 1_100_000_000, 1_112_000_000, 1_250_000_000],
            distribution=[610_000_000, 680_000_000, 740_000_000, 810_000_000, 905_000_000, 875_000_000],
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
        ],
    ),
    "perusahaan_b": DashboardSummary(
        tenant_id="perusahaan_b",
        tenant_name="Lembaga ZISWAF B",
        period="2026-05",
        kpis=Kpis(
            collection=KpiPair(total=920_000_000, delta_pct=6.8),
            distribution=KpiPair(total=640_000_000, delta_pct=14.2),
            balance=KpiPair(total=2_950_000_000, delta_pct=4.5),
            new_donors=KpiPair(total=89, delta_pct=-5.3),
        ),
        trend=Trend(
            labels=["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
            collection=[640_000_000, 715_000_000, 760_000_000, 820_000_000, 861_000_000, 920_000_000],
            distribution=[420_000_000, 480_000_000, 525_000_000, 580_000_000, 560_000_000, 640_000_000],
        ),
        asnaf_distribution=[
            AsnafItem(label="Fakir", amount=178_000_000),
            AsnafItem(label="Miskin", amount=152_000_000),
        ],
        fundraising_channels=[
            Channel(label="Transfer Bank", actual=520_000_000, target=600_000_000),
        ],
        recent_transactions=[
            Transaction(id="tx_b01", date="2026-05-19", type="Infaq", channel="E-Wallet", amount=500_000, donor="Dewi Lestari"),
        ],
    ),
}


def get_summary(tenant_id: str) -> DashboardSummary | None:
    return _DUMMY.get(tenant_id)

# ETL Rebuild Plan — apps_zakat/api-python/etl

Blueprint untuk rebuild ETL pipeline di `apps_zakat/api-python/etl/` yang hilang akibat NTFS corruption 2026-05-27. **Bukan implementation** — implementation harus dibuat manual karena business logic per `refresh_*` job butuh context yang hanya user yang tahu.

Sebagai referensi: schema target sudah ada di [`infra/db/migrations/dwh/recovered-schema-zakat.sql`](../infra/db/migrations/dwh/recovered-schema-zakat.sql) dan didokumentasi di [`docs/datadictionary/dwh.md`](datadictionary/dwh.md).

## Context dari reflog (74 commits hilang)

| Line | Commit | Relevansi |
|---|---|---|
| 108 | `[ETL-DATAMART] datamart schema + ETL runner end-to-end working` | Foundation runner orchestration |
| 110 | `[DATAMART-CABANG] Phase 1A — dim_cabang + cabang_key di facts (foundation)` | `dim_branch` + `branch_key` masuk ke semua dm/fact |
| 111 | `[DATAMART-CABANG] Phase 1B — refactor view-based ETL untuk populate cabang_key` | **Pattern: view-based ETL** — SELECT FROM view legacy → INSERT INTO dwh |
| 114 | `[DWH] rename schema datamart→dwh + standarisasi ETL naming + enrich PSAK 109` | Schema name akhir `dwh` (di zakat). Naming standardized. |
| 117 | `[ETL] fix f.fundentity → a.fundentity di SQL query (alias salah)` | Bug pattern — pakai alias yang benar |
| 118 | `[ETL] migration 007 — drop stale unique indexes superseded by 004/006` | Migration 7 = drop index lama tanpa `fund_entity` |

## File structure yang harus dibuat

```
apps_zakat/api-python/etl/
├── __init__.py          # (empty)
├── db.py                # Koneksi pool (re-export from app.shared.db)
├── utils.py             # Logger, watermark read/write, helpers
├── runner.py            # Orchestrator: panggil semua refresh_* sesuai dependency
├── scheduler.py         # APScheduler / cron registration (periodic)
│
├── refresh_dim_branch.py            # → dwh.dim_branch (SCD type 1, daily)
├── refresh_dim_donor.py             # → dwh.dim_donor
├── refresh_fact_fundraising.py      # → dwh.fact_fundraising_monthly (event-level)
│
├── refresh_dm_fund.py               # → dwh.dm_fund_monthly (per branch × fund_entity)
├── refresh_dm_donor_monthly.py      # → dwh.dm_donor_monthly
├── refresh_dm_dist.py               # → dwh.dm_dist_monthly (penyaluran)
├── refresh_dm_asnaf.py              # → dwh.dm_asnaf_monthly (8 asnaf)
├── refresh_dm_program_memo.py       # → dwh.dm_program_memo
├── refresh_dm_authorization.py      # → dwh.dm_authorization_summary
├── refresh_dm_account_balance.py    # → dwh.dm_account_balance
└── refresh_dm_budget_realization.py # → dwh.dm_budget_realization (anggaran vs realisasi)
```

## Implementation pattern

### Common skeleton untuk setiap `refresh_*.py`

```python
"""Refresh dwh.<table> dari source legacy via view-based ETL."""
from __future__ import annotations

import logging
from app.shared.db import execute, fetch_all
from .utils import write_watermark, log_run

logger = logging.getLogger(__name__)


async def refresh() -> dict:
    """Atomic refresh. Return {'rows': N, 'duration_ms': T} untuk etl_log."""
    # Pattern view-based:
    # 1. SELECT FROM legacy.view_or_source (SQL di-define dalam view di DB
    #    atau di string SQL di sini)
    # 2. UPSERT ke dwh.<table> dengan ON CONFLICT (unique_cols) DO UPDATE
    # 3. Update etl_watermark untuk source
    # 4. Insert etl_log entry

    sql = """
    INSERT INTO dwh.<table> (col1, col2, ...)
    SELECT col1, col2, ...
    FROM <source_view_or_legacy_table>
    WHERE <incremental_predicate>  -- watermark-based jika full refresh tidak feasible
    ON CONFLICT (<unique_index_cols>) DO UPDATE
    SET col2 = EXCLUDED.col2, ..., refreshed_at = now()
    """
    rows_affected = await execute(sql)
    await write_watermark("<table>", new_high_water_value)
    return {"rows": rows_affected}
```

### `runner.py` skeleton

```python
"""ETL runner — orchestrate semua refresh job sesuai dependency order."""
import asyncio
from . import (
    refresh_dim_branch,
    refresh_dim_donor,
    refresh_fact_fundraising,
    refresh_dm_fund,
    refresh_dm_donor_monthly,
    refresh_dm_dist,
    refresh_dm_asnaf,
    refresh_dm_program_memo,
    refresh_dm_authorization,
    refresh_dm_account_balance,
    refresh_dm_budget_realization,
)
from .utils import log_run

# Dependency order: dim sebelum fact sebelum dm
PIPELINE = [
    # Stage 1: dimensions (no dependencies)
    refresh_dim_branch,
    refresh_dim_donor,
    # Stage 2: facts (depend on dims)
    refresh_fact_fundraising,
    # Stage 3: aggregates (depend on facts + dims)
    refresh_dm_fund,
    refresh_dm_donor_monthly,
    refresh_dm_dist,
    refresh_dm_asnaf,
    refresh_dm_program_memo,
    refresh_dm_authorization,
    refresh_dm_account_balance,
    refresh_dm_budget_realization,
]


async def run_all() -> dict:
    results = {}
    for module in PIPELINE:
        name = module.__name__.split('.')[-1]
        try:
            result = await module.refresh()
            results[name] = {"status": "ok", **result}
            await log_run(name, status="ok", rows=result.get("rows", 0))
        except Exception as exc:
            results[name] = {"status": "error", "error": str(exc)}
            await log_run(name, status="error", error=str(exc))
            # Lanjut atau berhenti? Decision per business policy.
    return results
```

### `utils.py` helpers

```python
from __future__ import annotations
import time
from app.shared.db import execute, fetch_one


async def log_run(table_name: str, status: str, rows: int = 0, error: str | None = None):
    await execute(
        """INSERT INTO dwh.etl_log (table_name, status, rows_processed, error, run_at)
           VALUES ($1, $2, $3, $4, now())""",
        table_name, status, rows, error,
    )


async def read_watermark(table_name: str) -> dict | None:
    row = await fetch_one(
        "SELECT high_water_value, high_water_type FROM dwh.etl_watermark WHERE table_name=$1",
        table_name,
    )
    return dict(row) if row else None


async def write_watermark(table_name: str, value, value_type: str = "timestamp"):
    await execute(
        """INSERT INTO dwh.etl_watermark (table_name, high_water_value, high_water_type, updated_at)
           VALUES ($1, $2, $3, now())
           ON CONFLICT (table_name) DO UPDATE
           SET high_water_value = EXCLUDED.high_water_value, updated_at = now()""",
        table_name, str(value), value_type,
    )
```

### `scheduler.py` (APScheduler atau cron-based)

Option A — APScheduler in-process (untuk dev / single instance):
```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from .runner import run_all

def register_etl_jobs(scheduler: AsyncIOScheduler):
    # Daily 02:00 WIB: full pipeline
    scheduler.add_job(run_all, CronTrigger(hour=2, minute=0, timezone="Asia/Jakarta"),
                      id="etl_daily_full", replace_existing=True)
```

Option B — cron / k8s CronJob external (rekomen production): registrasi job runner sebagai endpoint atau CLI entry, di-trigger cron.

## Source legacy tables (di mziss_laz)

Dari query inventarisasi `information_schema.tables` schema `transaction`, `accounting`, `enterprise`, `fund`, `program`, `personalia`, `school` — ada banyak (>50) tabel legacy. Mapping spesifik per `refresh_*` job:

| Target dwh table | Probable source(s) |
|---|---|
| `dim_branch` | `enterprise.cabang` / `enterprise.branch` |
| `dim_donor` | `transaction.donatur` atau `accounting.kontak` |
| `dim_fund_type` | `fund.fund_master` atau hardcoded enum (8 asnaf + non-zakat) |
| `fact_fundraising_monthly` | `transaction.penerimaan` aggregated per month × branch × fund_entity |
| `dm_fund_monthly` | aggregate dari `fact_fundraising_monthly` per fund |
| `dm_donor_monthly` | aggregate per donor join dim_donor |
| `dm_dist_monthly` | `transaction.penyaluran` |
| `dm_asnaf_monthly` | aggregate `dm_dist_monthly` per asnaf |
| `dm_program_memo` | `program.memo` atau `program.program_memo` |
| `dm_authorization_summary` | `transaction.otorisasi` / `accounting.intrpicktransaction` |
| `dm_account_balance` | `accounting.dailybalance` / `accounting.fact_daily_balance` |
| `dm_budget_realization` | `fund.budget` + aggregate dari `fact_fundraising_monthly` |

> **PSAK 109 enrichment** (reflog line 114) — fund_entity mapping ke 8 asnaf (zakat) + infaq/sadaqah + waqaf untuk pelaporan sesuai PSAK 109.

## Testing strategy

1. **Unit test** per `refresh_*` module dengan mock DB pool — assert SQL pattern + watermark update
2. **Integration test** di-trigger via `testing/e2e-etl-datamart.sh` (juga hilang, rebuild bareng) — kosongkan dwh, jalankan runner, verify row counts match expected aggregates dari source.
3. **Idempotency test** — jalankan runner 2x, assert UPSERT tidak duplikasi rows.

## Implementation order (suggested)

1. Skeleton `utils.py` + `db.py` (helper foundation)
2. `dim_branch` (paling simple, foundation untuk semua dm/fact)
3. `dim_donor` + `dim_fund_type` (other dims)
4. `fact_fundraising_monthly` (depends on dims)
5. `dm_fund_monthly` + `dm_donor_monthly` (depend on fact)
6. Sisa `dm_*` satu per satu
7. `runner.py` orchestrator
8. `scheduler.py` registration
9. E2E test `testing/e2e-etl-datamart.sh`

## Sumber referensi tambahan

- Schema dump: `infra/db/migrations/dwh/recovered-schema-zakat.sql` — semua tabel target dengan kolom, indexes, constraints
- Datadict markdown: `docs/datadictionary/dwh.md` — column-level dokumentasi
- Reflog snapshot: `docs/recovery/reflog-main-118-entries.txt` — lihat lines 108-118 untuk detail commit ETL
- Existing dashboard backend: `apps_zakat/api-python/app/modules/dashboard/service.py` — referensi cara query dwh tables (read-side, complement ETL write-side)

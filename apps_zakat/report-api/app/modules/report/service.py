"""Report service — scaffold.

Report (laporan periodik, export, dsb.) membaca dari Data Warehouse via pool
**dwh** (`fetch_all_dwh`/`fetch_one_dwh` di app.shared.db), terpisah dari
dashboard yang membaca business views via pool business.

Belum ada endpoint fungsional — diisi saat spesifikasi report jelas.
"""

from __future__ import annotations

from app.shared.db import ping_dwh


async def dwh_health() -> bool:
    """Probe konektivitas Data Warehouse (pool dwh)."""
    return await ping_dwh()

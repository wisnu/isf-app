"""Async Postgres pool helper untuk isf_auth_<portal> database.

BFF owns auth; pool ini dipakai oleh AuthDB + AuditWriter.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

import asyncpg


_pool: asyncpg.Pool | None = None


async def init_pool(dsn: str | None = None) -> asyncpg.Pool | None:
    """Create pool dari ISF_AUTH_DATABASE_URL env (override via param untuk test).

    Retry up to 5x with 2s delay to handle container startup race with host network.
    """
    global _pool
    target = (dsn or os.getenv("ISF_AUTH_DATABASE_URL", "")).strip()
    if not target:
        return None
    # Append sslmode=disable if not already set — Postgres on this host doesn't
    # require SSL and asyncpg's default ssl=prefer causes spurious connection
    # failures on container startup when the SSL socket races with network setup.
    if "sslmode" not in target:
        sep = "&" if "?" in target else "?"
        target = f"{target}{sep}sslmode=disable"

    # Brief initial wait for container network routes to stabilize.
    await asyncio.sleep(3)

    last_exc: Exception | None = None
    for attempt in range(10):
        try:
            _pool = await asyncpg.create_pool(
                target,
                min_size=0,
                max_size=10,
                command_timeout=15,
                # statement_cache_size=0 hindari "relation does not exist" akibat prepared-statement
                # cache stale ketika schema di-recreate (mis. di test runner antar fixture).
                statement_cache_size=0,
            )
            return _pool
        except (OSError, asyncpg.PostgresConnectionFailureError) as e:
            last_exc = e
            await asyncio.sleep(2)
    raise RuntimeError(f"Cannot connect to DB after 10 attempts: {last_exc}") from last_exc


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("isf_auth pool not initialized — set ISF_AUTH_DATABASE_URL")
    return _pool


async def fetch_all(query: str, *args: Any) -> list[dict]:
    async with get_pool().acquire() as conn:
        rows = await conn.fetch(query, *args)
        return [dict(r) for r in rows]


async def fetch_one(query: str, *args: Any) -> dict | None:
    async with get_pool().acquire() as conn:
        row = await conn.fetchrow(query, *args)
        return dict(row) if row else None


async def execute(query: str, *args: Any) -> str:
    async with get_pool().acquire() as conn:
        return await conn.execute(query, *args)


async def ping() -> bool:
    try:
        async with get_pool().acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception:
        return False

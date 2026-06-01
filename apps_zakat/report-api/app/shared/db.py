"""Async Postgres connection pools for the reporting service.

Two read-only pools:
  • business pool (DATABASE_URL)   — dashboard reads (dashboard.v_*, transaction.*, program.*)
  • dwh pool      (DWH_DATABASE_URL) — report reads (dwh.*)

Both currently point at the same server/DB (mziss_laz); they are kept as
distinct pools/envs so the DWH can move to its own warehouse without touching
dashboard wiring. Both open read-only (default_transaction_read_only=on) —
this service never mutates data.
"""

from __future__ import annotations

import os
from typing import Any

import asyncpg

_READ_ONLY = {"default_transaction_read_only": "on"}

_pool: asyncpg.Pool | None = None
_dwh_pool: asyncpg.Pool | None = None


# ── business pool (dashboard) ─────────────────────────────────────────────────

async def init_pool() -> asyncpg.Pool | None:
    """Create the business read-only pool from DATABASE_URL. None if unset."""
    global _pool
    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        return None
    _pool = await asyncpg.create_pool(
        dsn,
        min_size=1,
        max_size=10,
        command_timeout=15,
        server_settings=_READ_ONLY,
    )
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Business pool not initialized — set DATABASE_URL and restart")
    return _pool


async def fetch_all(query: str, *args: Any) -> list[dict]:
    async with get_pool().acquire() as conn:
        rows = await conn.fetch(query, *args)
        return [dict(r) for r in rows]


async def fetch_one(query: str, *args: Any) -> dict | None:
    async with get_pool().acquire() as conn:
        row = await conn.fetchrow(query, *args)
        return dict(row) if row else None


async def ping() -> bool:
    """Quick health probe on the business pool — SELECT 1."""
    try:
        async with get_pool().acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception:
        return False


# ── DWH pool (report) ─────────────────────────────────────────────────────────

async def init_dwh_pool() -> asyncpg.Pool | None:
    """Create the DWH read-only pool from DWH_DATABASE_URL. None if unset."""
    global _dwh_pool
    dsn = os.getenv("DWH_DATABASE_URL", "").strip()
    if not dsn:
        return None
    _dwh_pool = await asyncpg.create_pool(
        dsn,
        min_size=1,
        max_size=10,
        command_timeout=30,
        server_settings=_READ_ONLY,
    )
    return _dwh_pool


async def close_dwh_pool() -> None:
    global _dwh_pool
    if _dwh_pool is not None:
        await _dwh_pool.close()
        _dwh_pool = None


def get_dwh_pool() -> asyncpg.Pool:
    if _dwh_pool is None:
        raise RuntimeError("DWH pool not initialized — set DWH_DATABASE_URL and restart")
    return _dwh_pool


async def fetch_all_dwh(query: str, *args: Any) -> list[dict]:
    async with get_dwh_pool().acquire() as conn:
        rows = await conn.fetch(query, *args)
        return [dict(r) for r in rows]


async def fetch_one_dwh(query: str, *args: Any) -> dict | None:
    async with get_dwh_pool().acquire() as conn:
        row = await conn.fetchrow(query, *args)
        return dict(row) if row else None


async def ping_dwh() -> bool:
    """Quick health probe on the DWH pool — SELECT 1."""
    try:
        async with get_dwh_pool().acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception:
        return False

"""Async Postgres connection pool helper."""

from __future__ import annotations

import os
from typing import Any

import asyncpg


_pool: asyncpg.Pool | None = None


async def init_pool() -> asyncpg.Pool | None:
    """Create pool from DATABASE_URL env. Returns None if unset."""
    global _pool
    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        return None
    _pool = await asyncpg.create_pool(
        dsn,
        min_size=1,
        max_size=10,
        command_timeout=15,
    )
    return _pool


async def close_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool not initialized — set DATABASE_URL and restart")
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
    """Quick health probe — SELECT 1."""
    try:
        async with get_pool().acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception:
        return False

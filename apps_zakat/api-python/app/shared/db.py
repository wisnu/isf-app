"""Async Postgres connection pool helper."""

from __future__ import annotations

import asyncio
import os
from typing import Any

import asyncpg


_pool: asyncpg.Pool | None = None
_isf_auth_pool: asyncpg.Pool | None = None


async def init_pool() -> asyncpg.Pool | None:
    """Create pool from DATABASE_URL env. Returns None if unset."""
    global _pool
    dsn = os.getenv("DATABASE_URL", "").strip()
    if not dsn:
        return None
    if "sslmode" not in dsn:
        sep = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{sep}sslmode=disable"
    last_exc: Exception | None = None
    for attempt in range(10):
        try:
            _pool = await asyncpg.create_pool(dsn, min_size=0, max_size=10, command_timeout=15)
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


async def execute(query: str, *args: Any) -> None:
    """Execute DML (INSERT/UPDATE/DELETE) without expecting a result row."""
    async with get_pool().acquire() as conn:
        await conn.execute(query, *args)


async def ping() -> bool:
    """Quick health probe — SELECT 1."""
    try:
        async with get_pool().acquire() as conn:
            await conn.fetchval("SELECT 1")
        return True
    except Exception:
        return False


# ── isf_auth pool ────────────────────────────────────────────────────────────
# Auth/RBAC (isf_auth.*) lives in a SEPARATE database (isf_auth_<portal>) since the
# auth-pg migration. Kept as a distinct pool so identity/admin modules can read &
# write isf_auth.* without crossing into the business (enterprise.*) pool.


async def init_isf_auth_pool() -> asyncpg.Pool | None:
    """Create pool from ISF_AUTH_DATABASE_URL env. Returns None if unset."""
    global _isf_auth_pool
    dsn = os.getenv("ISF_AUTH_DATABASE_URL", "").strip()
    if not dsn:
        return None
    if "sslmode" not in dsn:
        sep = "&" if "?" in dsn else "?"
        dsn = f"{dsn}{sep}sslmode=disable"
    last_exc: Exception | None = None
    for attempt in range(10):
        try:
            _isf_auth_pool = await asyncpg.create_pool(dsn, min_size=0, max_size=10, command_timeout=15)
            return _isf_auth_pool
        except (OSError, asyncpg.PostgresConnectionFailureError) as e:
            last_exc = e
            await asyncio.sleep(2)
    raise RuntimeError(f"Cannot connect to isf_auth DB after 10 attempts: {last_exc}") from last_exc


async def close_isf_auth_pool() -> None:
    global _isf_auth_pool
    if _isf_auth_pool is not None:
        await _isf_auth_pool.close()
        _isf_auth_pool = None


def get_isf_auth_pool() -> asyncpg.Pool:
    if _isf_auth_pool is None:
        raise RuntimeError(
            "isf_auth pool not initialized — set ISF_AUTH_DATABASE_URL and restart"
        )
    return _isf_auth_pool


async def fetch_all_isf_auth(query: str, *args: Any) -> list[dict]:
    async with get_isf_auth_pool().acquire() as conn:
        rows = await conn.fetch(query, *args)
        return [dict(r) for r in rows]

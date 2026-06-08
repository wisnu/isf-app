"""Async DB pool setup for otorisasi tests.

pytest-asyncio 1.4 + Python 3.14 keeps one event loop per test by default.
We create a fresh asyncpg pool per test function so the pool is always
bound to the current test's event loop.
"""
from __future__ import annotations
import os
import pytest_asyncio
from app.shared import db as _db


_DSN = os.getenv(
    "DATABASE_URL",
    "postgresql://transaction:solusi@localhost:5432/mziss_laz",
)


@pytest_asyncio.fixture(autouse=True)
async def db_pool():
    """Fresh pool per test — avoids cross-loop asyncpg errors."""
    os.environ.setdefault("DATABASE_URL", _DSN)
    pool = await _db.init_pool()
    yield pool
    await _db.close_pool()

"""SQLite access layer for portal authentication data."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncIterator
from uuid import uuid4

import aiosqlite


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS user_credentials (
  user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  password_hash TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS user_provider_links (
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider TEXT NOT NULL,
  external_id TEXT NOT NULL,
  email TEXT,
  linked_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (user_id, provider),
  UNIQUE (provider, external_id)
);

CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tenant_memberships (
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  is_default INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, tenant_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL DEFAULT (datetime('now')),
  event TEXT NOT NULL,
  user_id TEXT,
  tenant_id TEXT,
  ip TEXT,
  ua TEXT,
  payload_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_user_ts ON audit_log(user_id, ts);
CREATE INDEX IF NOT EXISTS idx_audit_event_ts ON audit_log(event, ts);
"""


class AuthDB:
    def __init__(self, path: str):
        self.path = path

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[aiosqlite.Connection]:
        async with aiosqlite.connect(self.path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("PRAGMA foreign_keys=ON")
            yield db

    async def init_schema(self) -> None:
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        async with self.connect() as db:
            await db.executescript(SCHEMA_SQL)
            await db.execute("PRAGMA journal_mode=WAL")
            await db.commit()

    # --- users -----------------------------------------------------------

    async def has_users(self) -> bool:
        async with self.connect() as db:
            async with db.execute("SELECT COUNT(*) AS c FROM users") as cur:
                row = await cur.fetchone()
                return (row["c"] if row else 0) > 0

    async def create_user(self, *, username: str, display_name: str, status: str = "active") -> str:
        user_id = f"usr_{uuid4().hex[:12]}"
        async with self.connect() as db:
            await db.execute(
                "INSERT INTO users (id, username, display_name, status) VALUES (?, ?, ?, ?)",
                (user_id, username, display_name, status),
            )
            await db.commit()
        return user_id

    async def get_user_by_id(self, user_id: str) -> dict | None:
        async with self.connect() as db:
            async with db.execute(
                "SELECT * FROM users WHERE id = ? AND status = 'active'", (user_id,)
            ) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    async def get_user_by_username(self, username: str) -> dict | None:
        async with self.connect() as db:
            async with db.execute(
                "SELECT * FROM users WHERE username = ? AND status = 'active'", (username,)
            ) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    # --- credentials -----------------------------------------------------

    async def set_password(self, user_id: str, password_hash: str) -> None:
        async with self.connect() as db:
            await db.execute(
                """
                INSERT INTO user_credentials (user_id, password_hash) VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                  password_hash = excluded.password_hash,
                  updated_at = datetime('now')
                """,
                (user_id, password_hash),
            )
            await db.commit()

    async def get_password_hash(self, user_id: str) -> str | None:
        async with self.connect() as db:
            async with db.execute(
                "SELECT password_hash FROM user_credentials WHERE user_id = ?", (user_id,)
            ) as cur:
                row = await cur.fetchone()
                return row["password_hash"] if row else None

    # --- provider links --------------------------------------------------

    async def get_provider_link(self, provider: str, external_id: str) -> dict | None:
        async with self.connect() as db:
            async with db.execute(
                "SELECT * FROM user_provider_links WHERE provider = ? AND external_id = ?",
                (provider, external_id),
            ) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    async def create_provider_link(
        self, user_id: str, provider: str, external_id: str, email: str | None
    ) -> None:
        async with self.connect() as db:
            await db.execute(
                "INSERT INTO user_provider_links (user_id, provider, external_id, email) VALUES (?, ?, ?, ?)",
                (user_id, provider, external_id, email),
            )
            await db.commit()

    # --- tenants ---------------------------------------------------------

    async def upsert_tenant(self, tenant_id: str, name: str) -> None:
        async with self.connect() as db:
            await db.execute(
                """
                INSERT INTO tenants (id, name) VALUES (?, ?)
                ON CONFLICT(id) DO UPDATE SET name = excluded.name
                """,
                (tenant_id, name),
            )
            await db.commit()

    async def get_tenant(self, tenant_id: str) -> dict | None:
        async with self.connect() as db:
            async with db.execute(
                "SELECT * FROM tenants WHERE id = ?", (tenant_id,)
            ) as cur:
                row = await cur.fetchone()
                return dict(row) if row else None

    async def add_tenant_membership(
        self, user_id: str, tenant_id: str, *, is_default: bool = False
    ) -> None:
        async with self.connect() as db:
            await db.execute(
                """
                INSERT INTO tenant_memberships (user_id, tenant_id, is_default) VALUES (?, ?, ?)
                ON CONFLICT(user_id, tenant_id) DO UPDATE SET is_default = excluded.is_default
                """,
                (user_id, tenant_id, 1 if is_default else 0),
            )
            await db.commit()

    async def get_user_tenants(self, user_id: str) -> list[dict]:
        async with self.connect() as db:
            async with db.execute(
                """
                SELECT t.id, t.name, tm.is_default
                FROM tenant_memberships tm
                JOIN tenants t ON tm.tenant_id = t.id
                WHERE tm.user_id = ?
                ORDER BY tm.is_default DESC, t.name
                """,
                (user_id,),
            ) as cur:
                rows = await cur.fetchall()
                return [dict(r) for r in rows]

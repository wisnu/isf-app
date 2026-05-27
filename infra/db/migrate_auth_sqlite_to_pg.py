"""One-shot migrator: SQLite (/data/auth.sqlite di BFF) → Postgres isf_auth_<portal>.

Jalankan di dalam container BFF (yang punya akses ke /data/auth.sqlite DAN ke PG host):

    podman exec -it isf-zakat-bff-api  python /scripts/migrate_auth_sqlite_to_pg.py
    podman exec -it isf-wakaf-bff-api  python /scripts/migrate_auth_sqlite_to_pg.py

Env yang dibaca:
    AUTH_DB_PATH            (default: /data/auth.sqlite)
    ISF_AUTH_DATABASE_URL   (wajib — DSN ke isf_auth_<portal>)

Idempotent: pakai ON CONFLICT DO NOTHING per tabel. Bisa di-rerun aman.
Tabel target di-prefix schema `isf_auth.`.

Mengasumsikan migrasi SQL 001..008 sudah di-apply ke target DB.
"""

from __future__ import annotations

import asyncio
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

import asyncpg


def _parse_ts(value):
    """SQLite menyimpan timestamp sebagai TEXT — asyncpg perlu datetime aware.
    Asumsi format 'YYYY-MM-DD HH:MM:SS' UTC (DEFAULT datetime('now') di SQLite)."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    try:
        # SQLite default: 'YYYY-MM-DD HH:MM:SS' tanpa TZ
        dt = datetime.fromisoformat(str(value).replace(" ", "T"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


SQLITE_PATH = os.getenv("AUTH_DB_PATH", "/data/auth.sqlite")
PG_DSN = os.getenv("ISF_AUTH_DATABASE_URL", "").strip()


def _read_sqlite() -> dict[str, list[dict]]:
    if not os.path.exists(SQLITE_PATH):
        print(f"[skip] SQLite file tidak ada: {SQLITE_PATH} — DB target diasumsikan fresh")
        return {t: [] for t in (
            "users", "user_credentials", "user_provider_links",
            "tenants", "tenant_memberships", "audit_log",
        )}

    con = sqlite3.connect(SQLITE_PATH)
    con.row_factory = sqlite3.Row
    out: dict[str, list[dict]] = {}
    for t in (
        "users", "user_credentials", "user_provider_links",
        "tenants", "tenant_memberships", "audit_log",
    ):
        try:
            rows = con.execute(f"SELECT * FROM {t}").fetchall()
            out[t] = [dict(r) for r in rows]
        except sqlite3.OperationalError as e:
            print(f"[warn] tabel {t} tidak ada di SQLite ({e}) — skip")
            out[t] = []
    con.close()
    return out


async def _insert_users(conn: asyncpg.Connection, rows: list[dict]) -> int:
    n = 0
    for r in rows:
        result = await conn.execute(
            """
            INSERT INTO isf_auth.users (id, username, display_name, status, created_at)
            VALUES ($1, $2, $3, $4, COALESCE($5::timestamptz, NOW()))
            ON CONFLICT (id) DO NOTHING
            """,
            r["id"], r["username"], r["display_name"],
            r.get("status", "active"), _parse_ts(r.get("created_at")),
        )
        if result.endswith(" 1"):
            n += 1
    return n


async def _insert_credentials(conn: asyncpg.Connection, rows: list[dict]) -> int:
    n = 0
    for r in rows:
        result = await conn.execute(
            """
            INSERT INTO isf_auth.user_credentials (user_id, password_hash, updated_at)
            VALUES ($1, $2, COALESCE($3::timestamptz, NOW()))
            ON CONFLICT (user_id) DO NOTHING
            """,
            r["user_id"], r["password_hash"], _parse_ts(r.get("updated_at")),
        )
        if result.endswith(" 1"):
            n += 1
    return n


async def _insert_provider_links(conn: asyncpg.Connection, rows: list[dict]) -> int:
    n = 0
    for r in rows:
        result = await conn.execute(
            """
            INSERT INTO isf_auth.user_provider_links (user_id, provider, external_id, email, linked_at)
            VALUES ($1, $2, $3, $4, COALESCE($5::timestamptz, NOW()))
            ON CONFLICT (user_id, provider) DO NOTHING
            """,
            r["user_id"], r["provider"], r["external_id"],
            r.get("email"), _parse_ts(r.get("linked_at")),
        )
        if result.endswith(" 1"):
            n += 1
    return n


async def _insert_tenants(conn: asyncpg.Connection, rows: list[dict]) -> int:
    n = 0
    for r in rows:
        result = await conn.execute(
            """
            INSERT INTO isf_auth.tenants (id, name, created_at)
            VALUES ($1, $2, COALESCE($3::timestamptz, NOW()))
            ON CONFLICT (id) DO NOTHING
            """,
            r["id"], r["name"], _parse_ts(r.get("created_at")),
        )
        if result.endswith(" 1"):
            n += 1
    return n


async def _insert_memberships(conn: asyncpg.Connection, rows: list[dict]) -> int:
    n = 0
    for r in rows:
        result = await conn.execute(
            """
            INSERT INTO isf_auth.tenant_memberships (user_id, tenant_id, is_default)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id, tenant_id) DO NOTHING
            """,
            r["user_id"], r["tenant_id"], bool(r.get("is_default", 0)),
        )
        if result.endswith(" 1"):
            n += 1
    return n


async def _insert_audit_log(conn: asyncpg.Connection, rows: list[dict]) -> int:
    """Audit log tidak punya unique key — kita batched insert tanpa de-dup.
    Hanya migrate kalau target audit_log kosong supaya tidak duplikat saat re-run."""
    existing = await conn.fetchval("SELECT COUNT(*) FROM isf_auth.audit_log")
    if existing and existing > 0:
        print(f"  [skip audit_log] target sudah ada {existing} row — tidak migrate ulang")
        return 0
    n = 0
    for r in rows:
        payload_json = r.get("payload_json")
        if payload_json:
            try:
                payload_obj = json.loads(payload_json)
            except (json.JSONDecodeError, TypeError):
                payload_obj = {"raw": payload_json}
        else:
            payload_obj = None
        await conn.execute(
            """
            INSERT INTO isf_auth.audit_log (ts, event, user_id, tenant_id, ip, ua, payload)
            VALUES (COALESCE($1::timestamptz, NOW()), $2, $3, $4, $5, $6, $7::jsonb)
            """,
            _parse_ts(r.get("ts")), r["event"], r.get("user_id"), r.get("tenant_id"),
            r.get("ip"), r.get("ua"),
            json.dumps(payload_obj) if payload_obj is not None else None,
        )
        n += 1
    return n


async def main() -> int:
    if not PG_DSN:
        print("ERROR: ISF_AUTH_DATABASE_URL belum di-set", file=sys.stderr)
        return 2

    print(f"Source SQLite: {SQLITE_PATH}")
    print(f"Target PG:     {PG_DSN.split('@')[-1]}")

    data = _read_sqlite()
    for k, v in data.items():
        print(f"  src.{k}: {len(v)} rows")

    conn = await asyncpg.connect(PG_DSN)
    try:
        users_n = await _insert_users(conn, data["users"])
        cred_n = await _insert_credentials(conn, data["user_credentials"])
        link_n = await _insert_provider_links(conn, data["user_provider_links"])
        ten_n = await _insert_tenants(conn, data["tenants"])
        mem_n = await _insert_memberships(conn, data["tenant_memberships"])
        audit_n = await _insert_audit_log(conn, data["audit_log"])
    finally:
        await conn.close()

    print()
    print("Migrated rows (only fresh inserts; existing rows skipped via ON CONFLICT):")
    print(f"  users:               {users_n}")
    print(f"  user_credentials:    {cred_n}")
    print(f"  user_provider_links: {link_n}")
    print(f"  tenants:             {ten_n}")
    print(f"  tenant_memberships:  {mem_n}")
    print(f"  audit_log:           {audit_n}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

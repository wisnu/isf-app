"""Test fixtures untuk BFF.

Auth DB sekarang Postgres (isf_auth schema). Fixture men-setup DB test
`isf_auth_test_zakat` sekali per session (create DB + schema + tables), lalu
truncate semua tabel sebelum tiap test supaya isolasi tetap kuat.
"""

from __future__ import annotations

import asyncio
import os

import asyncpg
import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.services.identity_client import IdentityUnavailable, IdentityUserNotFound
from app.shared.config import Settings


# DSN untuk admin (maintenance) connection — buat DB test kalau belum ada.
def _default_admin_dsn() -> str:
    return os.getenv(
        "PG_ADMIN_DATABASE_URL",
        "postgresql://transaction:solusi@host.containers.internal:5432/postgres",
    )


def _default_test_dsn() -> str:
    return os.getenv(
        "ISF_AUTH_TEST_DATABASE_URL",
        "postgresql://transaction:solusi@host.containers.internal:5432/isf_auth_test_zakat",
    )


# DDL inlined supaya test tidak bergantung ke infra/ di host filesystem (container BFF
# tidak mount infra/). Harus tetap sinkron dengan infra/db/migrations/isf_auth/006-008.
_SCHEMA_DDL = """
CREATE TABLE isf_auth.users (
    id            VARCHAR(20)  PRIMARY KEY,
    username      VARCHAR(120) UNIQUE NOT NULL,
    display_name  VARCHAR(200) NOT NULL,
    status        VARCHAR(20)  NOT NULL DEFAULT 'active',
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE TABLE isf_auth.user_credentials (
    user_id        VARCHAR(20)  PRIMARY KEY REFERENCES isf_auth.users(id) ON DELETE CASCADE,
    password_hash  TEXT         NOT NULL,
    updated_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE TABLE isf_auth.user_provider_links (
    user_id      VARCHAR(20)  NOT NULL REFERENCES isf_auth.users(id) ON DELETE CASCADE,
    provider     VARCHAR(40)  NOT NULL,
    external_id  TEXT         NOT NULL,
    email        VARCHAR(255),
    linked_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, provider),
    UNIQUE (provider, external_id)
);
CREATE TABLE isf_auth.tenants (
    id          VARCHAR(40)  PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE TABLE isf_auth.tenant_memberships (
    user_id     VARCHAR(20) NOT NULL REFERENCES isf_auth.users(id) ON DELETE CASCADE,
    tenant_id   VARCHAR(40) NOT NULL REFERENCES isf_auth.tenants(id) ON DELETE CASCADE,
    is_default  BOOLEAN     NOT NULL DEFAULT FALSE,
    PRIMARY KEY (user_id, tenant_id)
);
CREATE TABLE isf_auth.audit_log (
    id         BIGSERIAL    PRIMARY KEY,
    ts         TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    event      VARCHAR(80)  NOT NULL,
    user_id    VARCHAR(20),
    tenant_id  VARCHAR(40),
    ip         VARCHAR(64),
    ua         TEXT,
    payload    JSONB
);
CREATE INDEX idx_audit_user_ts  ON isf_auth.audit_log(user_id, ts);
CREATE INDEX idx_audit_event_ts ON isf_auth.audit_log(event, ts);
"""


async def _bootstrap_test_db() -> str:
    """Buat DB test (jika belum ada), drop+recreate schema isf_auth, apply migrations."""
    test_dsn = _default_test_dsn()
    admin_dsn = _default_admin_dsn()

    # Extract DB name dari test DSN
    db_name = test_dsn.rsplit("/", 1)[-1].split("?")[0]

    # Step 1: ensure DB exists (admin connection)
    admin = await asyncpg.connect(admin_dsn)
    try:
        exists = await admin.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )
        if not exists:
            await admin.execute(f'CREATE DATABASE "{db_name}"')
    finally:
        await admin.close()

    # Step 2: drop+create schema, apply inlined DDL
    conn = await asyncpg.connect(test_dsn)
    try:
        await conn.execute("DROP SCHEMA IF EXISTS isf_auth CASCADE")
        await conn.execute("CREATE SCHEMA isf_auth")
        await conn.execute(_SCHEMA_DDL)
    finally:
        await conn.close()

    return test_dsn


@pytest.fixture(scope="session")
def isf_auth_test_dsn() -> str:
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(_bootstrap_test_db())
    finally:
        loop.close()


async def _truncate_all(dsn: str) -> None:
    conn = await asyncpg.connect(dsn)
    try:
        await conn.execute(
            "TRUNCATE isf_auth.users, isf_auth.tenants, isf_auth.audit_log "
            "RESTART IDENTITY CASCADE"
        )
    finally:
        await conn.close()


@pytest.fixture
def fresh_isf_auth(isf_auth_test_dsn) -> str:
    """Function-scope sync fixture: truncate semua tabel + return DSN.
    Sync agar tidak bergantung pada event loop pytest-asyncio yang mungkin
    conflicts dengan TestClient's anyio loop."""
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_truncate_all(isf_auth_test_dsn))
    finally:
        loop.close()
    return isf_auth_test_dsn


@pytest.fixture
def settings(fresh_isf_auth):
    return Settings(
        app_env="test",
        api_python_base_url="http://api-python:8000",
        session_secret="test-secret-12345",
        cors_origin="http://localhost:5173",
        auth_providers="password,google",
        isf_auth_database_url=fresh_isf_auth,
        google_oauth_client_id="",
        google_oauth_client_secret="",
        google_oauth_redirect_url="http://localhost:7000/api/auth/google/callback",
        google_allowed_domains="ihsansolusi.co.id",
        google_allowed_emails="",
        frontend_base_url="http://localhost:5173",
    )


@pytest.fixture
def app(settings):
    return create_app(settings)


class _MockIdentityClient:
    """Mock IdentityClient untuk test BFF tanpa api-python real.

    Demo users (ADMIN, FINANCE.A, FINANCE.B) tidak ada di enterprise.usertbl
    di test environment, jadi mock ini seed profile mereka supaya existing
    auth/dashboard tests tetap jalan. Lookup case-insensitive — selaras dengan
    konvensi BFF (storage uppercase, comparison normalized).
    """

    def __init__(self):
        self.profiles: dict[str, dict] = {}
        self.behavior: str = "normal"  # "normal" | "unavailable"

    def set_profile(self, username: str, *, roles=None, branches=None, menus=None, status="active"):
        key = (username or "").strip().upper()
        self.profiles[key] = {
            "user_id": key,
            "status": status,
            "roles": roles or [],
            "branches": branches or [],
            "menus": menus or [],
        }

    def set_unavailable(self):
        self.behavior = "unavailable"

    async def fetch_profile(self, user_id: str) -> dict:
        if self.behavior == "unavailable":
            raise IdentityUnavailable("mocked")
        key = (user_id or "").strip().upper()
        if key not in self.profiles:
            raise IdentityUserNotFound(user_id)
        return self.profiles[key]


@pytest.fixture
def mock_identity():
    """Default mock dengan 3 demo user pre-seeded (ADMIN full akses,
    FINANCE.A/FINANCE.B terbatas dashboard.overview + dashboard.keuangan)."""
    m = _MockIdentityClient()
    m.set_profile(
        "ADMIN",
        menus=[
            "dashboard.overview", "dashboard.keuangan",
            "dashboard.penyaluran", "dashboard.penghimpunan",
            "keuangan.coa", "keuangan.kas", "keuangan.bank",
        ],
    )
    m.set_profile("FINANCE.A", menus=["dashboard.overview", "dashboard.keuangan"])
    m.set_profile("FINANCE.B", menus=["dashboard.overview", "dashboard.keuangan"])
    return m


@pytest.fixture
def client(app, mock_identity):
    """TestClient dengan mock_identity terinject ke app.state.identity_client
    (replace IdentityClient real yang biasanya dibuat di lifespan)."""
    with TestClient(app) as c:
        app.state.identity_client = mock_identity
        yield c

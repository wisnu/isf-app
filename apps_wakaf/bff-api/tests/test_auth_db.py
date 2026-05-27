"""Direct tests for the Postgres auth-data layer (schema isf_auth)."""

import bcrypt
import pytest

from app.services.auth_db import AuthDB
from app.shared.db import init_pool, close_pool


@pytest.fixture
async def db(fresh_isf_auth):
    """`fresh_isf_auth` melakukan TRUNCATE dulu, lalu init pool ke DSN tsb."""
    await init_pool(fresh_isf_auth)
    try:
        yield AuthDB()
    finally:
        await close_pool()


async def test_has_users_empty_initially(db):
    assert await db.has_users() is False


async def test_create_user_normalizes_username_to_uppercase(db):
    uid = await db.create_user(username="alice", display_name="Alice")
    assert uid.startswith("usr_")
    user = await db.get_user_by_username("alice")
    assert user is not None and user["id"] == uid
    assert user["username"] == "ALICE"

    by_id = await db.get_user_by_id(uid)
    assert by_id is not None and by_id["username"] == "ALICE"


async def test_get_user_by_username_is_case_insensitive(db):
    uid = await db.create_user(username="ALICE", display_name="Alice")
    for variant in ("alice", "Alice", "ALICE", "  alice  "):
        user = await db.get_user_by_username(variant)
        assert user is not None and user["id"] == uid


async def test_set_and_verify_password_via_hash(db):
    uid = await db.create_user(username="bob", display_name="Bob")
    hashed = bcrypt.hashpw(b"s3cret", bcrypt.gensalt()).decode()
    await db.set_password(uid, hashed)
    stored = await db.get_password_hash(uid)
    assert stored == hashed


async def test_provider_link_round_trip(db):
    uid = await db.create_user(username="carol@example.com", display_name="Carol")
    await db.create_provider_link(uid, "google", "google-sub-123", "carol@example.com")
    link = await db.get_provider_link("google", "google-sub-123")
    assert link is not None and link["user_id"] == uid and link["email"] == "carol@example.com"


async def test_tenant_membership_default_first(db):
    uid = await db.create_user(username="dave", display_name="Dave")
    await db.upsert_tenant("perusahaan_a", "A")
    await db.upsert_tenant("perusahaan_b", "B")
    await db.add_tenant_membership(uid, "perusahaan_b", is_default=False)
    await db.add_tenant_membership(uid, "perusahaan_a", is_default=True)

    tenants = await db.get_user_tenants(uid)
    assert tenants[0]["id"] == "perusahaan_a"
    assert {t["id"] for t in tenants} == {"perusahaan_a", "perusahaan_b"}


async def test_migrate_usernames_to_uppercase_is_idempotent(db, fresh_isf_auth):
    """Insert legacy lowercase rows langsung via asyncpg; verifikasi migrate idempotent."""
    import asyncpg
    conn = await asyncpg.connect(fresh_isf_auth)
    try:
        await conn.execute(
            "INSERT INTO isf_auth.users (id, username, display_name, status) VALUES ($1,$2,$3,$4)",
            "usr_legacy01", "old_admin", "Old Admin", "active",
        )
        await conn.execute(
            "INSERT INTO isf_auth.users (id, username, display_name, status) VALUES ($1,$2,$3,$4)",
            "usr_legacy02", "ALREADY_UPPER", "Already Upper", "active",
        )
    finally:
        await conn.close()

    migrated = await db.migrate_usernames_to_uppercase()
    assert migrated == 1

    user = await db.get_user_by_username("old_admin")
    assert user is not None and user["username"] == "OLD_ADMIN"

    migrated_again = await db.migrate_usernames_to_uppercase()
    assert migrated_again == 0

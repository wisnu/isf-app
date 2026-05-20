"""Direct tests for the SQLite auth-data layer."""

import bcrypt
import pytest

from app.services.auth_db import AuthDB


@pytest.fixture
async def db(tmp_path):
    instance = AuthDB(str(tmp_path / "auth.sqlite"))
    await instance.init_schema()
    return instance


async def test_init_schema_is_idempotent(db):
    await db.init_schema()
    await db.init_schema()
    assert await db.has_users() is False


async def test_create_user_and_lookup_by_username(db):
    uid = await db.create_user(username="alice", display_name="Alice")
    assert uid.startswith("usr_")
    user = await db.get_user_by_username("alice")
    assert user is not None and user["id"] == uid

    by_id = await db.get_user_by_id(uid)
    assert by_id is not None and by_id["username"] == "alice"


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
    assert tenants[0]["id"] == "perusahaan_a"  # default ordered first
    assert {t["id"] for t in tenants} == {"perusahaan_a", "perusahaan_b"}

"""Seed default tenants and demo users into a fresh portal database."""

from __future__ import annotations

import bcrypt

from app.services.auth_db import AuthDB


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def seed_defaults(db: AuthDB) -> None:
    await db.upsert_tenant("perusahaan_a", "Lembaga ZISWAF A")
    await db.upsert_tenant("perusahaan_b", "Lembaga ZISWAF B")

    admin = await db.create_user(username="admin", display_name="Administrator")
    await db.set_password(admin, _hash("admin123"))
    await db.add_tenant_membership(admin, "perusahaan_a", is_default=True)
    await db.add_tenant_membership(admin, "perusahaan_b", is_default=False)

    fa = await db.create_user(username="finance.a", display_name="Finance Perusahaan A")
    await db.set_password(fa, _hash("finance123"))
    await db.add_tenant_membership(fa, "perusahaan_a", is_default=True)

    fb = await db.create_user(username="finance.b", display_name="Finance Perusahaan B")
    await db.set_password(fb, _hash("finance123"))
    await db.add_tenant_membership(fb, "perusahaan_b", is_default=True)

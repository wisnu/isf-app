"""Postgres access layer for portal authentication data (schema `isf_auth`).

Pool dikelola di `app.shared.db`. Method signature + return shape sengaja
dipertahankan supaya caller (routers/auth, auth_providers/*, audit) tidak perlu
diubah saat migrasi dari aiosqlite.
"""

from __future__ import annotations

from uuid import uuid4

from app.shared.db import execute, fetch_all, fetch_one, get_pool


def normalize_username(value: str) -> str:
    """Login usernames are stored uppercase and trimmed; comparison case-insensitive di boundary."""
    return (value or "").strip().upper()


class AuthDB:
    """Façade tipis di atas pool isf_auth — agar lifespan + provider tetap pakai
    `app.state.auth_db` seperti sebelumnya."""

    # --- users -----------------------------------------------------------

    async def has_users(self) -> bool:
        async with get_pool().acquire() as conn:
            n = await conn.fetchval("SELECT COUNT(*) FROM isf_auth.users")
            return (n or 0) > 0

    async def create_user(self, *, username: str, display_name: str, status: str = "active") -> str:
        user_id = f"usr_{uuid4().hex[:12]}"
        await execute(
            """
            INSERT INTO isf_auth.users (id, username, display_name, status)
            VALUES ($1, $2, $3, $4)
            """,
            user_id, normalize_username(username), display_name, status,
        )
        return user_id

    async def get_user_by_id(self, user_id: str) -> dict | None:
        return await fetch_one(
            "SELECT * FROM isf_auth.users WHERE id = $1 AND status = 'active'",
            user_id,
        )

    async def get_user_by_username(self, username: str) -> dict | None:
        return await fetch_one(
            "SELECT * FROM isf_auth.users WHERE username = $1 AND status = 'active'",
            normalize_username(username),
        )

    async def migrate_usernames_to_uppercase(self) -> int:
        """Idempotent: rename legacy lowercase rows ke uppercase. Returns count migrated."""
        async with get_pool().acquire() as conn:
            pending = [
                dict(r) for r in await conn.fetch(
                    "SELECT id, username FROM isf_auth.users WHERE username <> UPPER(username)"
                )
            ]
            if not pending:
                return 0
            taken = {
                r["username"]
                for r in await conn.fetch("SELECT username FROM isf_auth.users")
            }
            migrated = 0
            for r in pending:
                target = normalize_username(r["username"])
                if target in taken and target != r["username"]:
                    continue
                await conn.execute(
                    "UPDATE isf_auth.users SET username = $1 WHERE id = $2",
                    target, r["id"],
                )
                taken.discard(r["username"])
                taken.add(target)
                migrated += 1
            return migrated

    # --- credentials -----------------------------------------------------

    async def set_password(self, user_id: str, password_hash: str) -> None:
        await execute(
            """
            INSERT INTO isf_auth.user_credentials (user_id, password_hash)
            VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET
              password_hash = EXCLUDED.password_hash,
              updated_at    = NOW()
            """,
            user_id, password_hash,
        )

    async def get_password_hash(self, user_id: str) -> str | None:
        async with get_pool().acquire() as conn:
            return await conn.fetchval(
                "SELECT password_hash FROM isf_auth.user_credentials WHERE user_id = $1",
                user_id,
            )

    # --- provider links --------------------------------------------------

    async def get_provider_link(self, provider: str, external_id: str) -> dict | None:
        return await fetch_one(
            "SELECT * FROM isf_auth.user_provider_links WHERE provider = $1 AND external_id = $2",
            provider, external_id,
        )

    async def create_provider_link(
        self, user_id: str, provider: str, external_id: str, email: str | None
    ) -> None:
        await execute(
            """
            INSERT INTO isf_auth.user_provider_links (user_id, provider, external_id, email)
            VALUES ($1, $2, $3, $4)
            """,
            user_id, provider, external_id, email,
        )

    # --- tenants ---------------------------------------------------------

    async def upsert_tenant(self, tenant_id: str, name: str) -> None:
        await execute(
            """
            INSERT INTO isf_auth.tenants (id, name) VALUES ($1, $2)
            ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name
            """,
            tenant_id, name,
        )

    async def get_tenant(self, tenant_id: str) -> dict | None:
        return await fetch_one("SELECT * FROM isf_auth.tenants WHERE id = $1", tenant_id)

    async def add_tenant_membership(
        self, user_id: str, tenant_id: str, *, is_default: bool = False
    ) -> None:
        await execute(
            """
            INSERT INTO isf_auth.tenant_memberships (user_id, tenant_id, is_default)
            VALUES ($1, $2, $3)
            ON CONFLICT (user_id, tenant_id) DO UPDATE SET is_default = EXCLUDED.is_default
            """,
            user_id, tenant_id, bool(is_default),
        )

    async def get_user_tenants(self, user_id: str) -> list[dict]:
        return await fetch_all(
            """
            SELECT t.id, t.name, tm.is_default
            FROM isf_auth.tenant_memberships tm
            JOIN isf_auth.tenants t ON tm.tenant_id = t.id
            WHERE tm.user_id = $1
            ORDER BY tm.is_default DESC, t.name
            """,
            user_id,
        )

    # --- menus -----------------------------------------------------------

    async def get_menus_by_roles(self, roles: list[str]) -> list[str]:
        """Return distinct active menu_keys for the given role ids."""
        if not roles:
            return []
        rows = await fetch_all(
            """
            SELECT DISTINCT rm.menu_key
            FROM isf_auth.role_menu rm
            JOIN isf_auth.menu m ON rm.menu_key = m.menu_key
            WHERE rm.id_peran = ANY($1)
              AND m.status = 'active'
            ORDER BY rm.menu_key
            """,
            roles,
        )
        return [r["menu_key"] for r in rows]

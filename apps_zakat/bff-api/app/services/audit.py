"""Audit log writer."""

from __future__ import annotations

import json
from typing import Any

from app.services.auth_db import AuthDB


class AuditWriter:
    def __init__(self, db: AuthDB):
        self.db = db

    async def log(
        self,
        event: str,
        *,
        user_id: str | None = None,
        tenant_id: str | None = None,
        ip: str | None = None,
        ua: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        async with self.db.connect() as conn:
            await conn.execute(
                """
                INSERT INTO audit_log (event, user_id, tenant_id, ip, ua, payload_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    event,
                    user_id,
                    tenant_id,
                    ip,
                    ua,
                    json.dumps(payload) if payload is not None else None,
                ),
            )
            await conn.commit()

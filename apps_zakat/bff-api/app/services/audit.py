"""Audit log writer — append ke isf_auth.audit_log (JSONB payload)."""

from __future__ import annotations

import json
from typing import Any

from app.shared.db import execute


class AuditWriter:
    """Tidak butuh state — semua write via shared pool. Konstruktor menerima
    AuthDB untuk backward-compat dengan caller (lifespan), tapi diabaikan."""

    def __init__(self, db: Any = None):
        # signature dipertahankan; tidak ada handle yang disimpan
        del db

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
        payload_text = json.dumps(payload) if payload is not None else None
        await execute(
            """
            INSERT INTO isf_auth.audit_log (event, user_id, tenant_id, ip, ua, payload)
            VALUES ($1, $2, $3, $4, $5, $6::jsonb)
            """,
            event, user_id, tenant_id, ip, ua, payload_text,
        )

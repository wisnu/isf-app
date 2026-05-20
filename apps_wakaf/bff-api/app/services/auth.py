"""Shared auth helpers (session lookup, public user shape)."""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from app.services.auth_db import AuthDB
from app.shared.response import err


async def build_user_public(db: AuthDB, user_id: str) -> dict | None:
    user = await db.get_user_by_id(user_id)
    if not user:
        return None
    tenants = await db.get_user_tenants(user_id)
    default_tenant = next(
        (t["id"] for t in tenants if t.get("is_default")),
        tenants[0]["id"] if tenants else None,
    )
    return {
        "username": user["username"],
        "name": user["display_name"],
        "tenants": [{"id": t["id"], "name": t["name"]} for t in tenants],
        "default_tenant": default_tenant,
    }


async def current_user_id_or_401(request: Request) -> tuple[str | None, JSONResponse | None]:
    user_id = request.session.get("user_id")
    if not user_id:
        return None, JSONResponse(
            status_code=401, content=err("UNAUTHORIZED", "Not authenticated")
        )
    db: AuthDB = request.app.state.auth_db
    user = await db.get_user_by_id(user_id)
    if not user:
        request.session.clear()
        return None, JSONResponse(
            status_code=401, content=err("UNAUTHORIZED", "Session invalid")
        )
    return user_id, None

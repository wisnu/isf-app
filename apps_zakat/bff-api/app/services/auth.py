"""Shared auth helpers (session lookup, public user shape, menu gating)."""

from __future__ import annotations

import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.auth_db import AuthDB
from app.shared.response import err

# ---------------------------------------------------------------------------
# In-process menu cache keyed by frozenset(roles), TTL 5 minutes.
# Avoids storing menus in the session cookie (which can exceed 4096 bytes for
# users with many roles such as ADM).
# ---------------------------------------------------------------------------
_menu_cache: dict[frozenset, tuple[list[dict], float]] = {}
_CACHE_TTL = 300.0  # seconds


async def get_menus_for_roles(roles: list[str], db: AuthDB) -> list[dict]:
    key = frozenset(roles)
    now = time.monotonic()
    cached = _menu_cache.get(key)
    if cached is not None and now - cached[1] < _CACHE_TTL:
        return cached[0]
    menus = await db.get_menus_by_roles(list(roles))
    _menu_cache[key] = (menus, now)
    return menus


class AppHTTPError(Exception):
    """Raise dari FastAPI dependency untuk short-circuit dengan body envelope kita.

    FastAPI default `HTTPException` mengirim `{"detail": ...}`, tidak match
    dengan envelope `{"error": {"code", "message"}, "meta": ...}`. Pakai exception
    custom ini, lalu register handler-nya via `register_exception_handlers(app)`
    di factory `create_app()`.
    """

    def __init__(self, status_code: int, content: dict) -> None:
        self.status_code = status_code
        self.content = content


async def _app_http_error_handler(request: Request, exc: AppHTTPError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.content)


def register_exception_handlers(app: FastAPI) -> None:
    """Daftarkan handler untuk AppHTTPError. Panggil sekali di create_app()."""
    app.add_exception_handler(AppHTTPError, _app_http_error_handler)


async def build_user_public(
    db: AuthDB,
    user_id: str,
    *,
    roles: list[str] | None = None,
    branches: list[str] | None = None,
    primary_branch: str | None = None,
    menus: list[dict] | None = None,
    branch_access: str = "single",
) -> dict | None:
    """Build the public user payload returned to the frontend.

    `menus` can be supplied by the caller (e.g. freshly fetched from identity).
    When omitted, it is resolved from the cache / DB via `roles`.
    """
    user = await db.get_user_by_id(user_id)
    if not user:
        return None
    tenants = await db.get_user_tenants(user_id)
    default_tenant = next(
        (t["id"] for t in tenants if t.get("is_default")),
        tenants[0]["id"] if tenants else None,
    )
    resolved_menus = menus if menus is not None else await get_menus_for_roles(roles or [], db)
    return {
        "username": user["username"],
        "name": user["display_name"],
        "tenants": [{"id": t["id"], "name": t["name"]} for t in tenants],
        "default_tenant": default_tenant,
        "roles": roles or [],
        "branches": branches or [],
        "primary_branch": primary_branch,
        "menus": resolved_menus,
        "branch_access": branch_access,
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


def require_menu(menu_key: str):
    """FastAPI dependency factory.

    Returns dependency yang:
      - 401 kalau user tidak login (delegate ke current_user_id_or_401)
      - 403 MENU_FORBIDDEN kalau menu_key tidak ada di cache/DB menus for session roles
        (audit_log: menu_denied)
      - else return user_id
    """
    async def _check(request: Request):
        user_id, error_response = await current_user_id_or_401(request)
        if error_response is not None:
            raise AppHTTPError(
                status_code=error_response.status_code,
                content=err("UNAUTHORIZED", "Not authenticated"),
            )
        roles = request.session.get("roles") or []
        db: AuthDB = request.app.state.auth_db
        menus = await get_menus_for_roles(roles, db)
        if not any(m["menu_key"] == menu_key for m in menus):
            audit = getattr(request.app.state, "audit", None)
            if audit is not None:
                await audit.log(
                    "menu_denied",
                    user_id=user_id,
                    payload={"menu_key": menu_key, "endpoint": str(request.url.path)},
                )
            raise AppHTTPError(
                status_code=403,
                content=err("MENU_FORBIDDEN", f"Menu '{menu_key}' tidak diizinkan"),
            )
        return user_id

    return _check

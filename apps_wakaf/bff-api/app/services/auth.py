"""Shared auth helpers (session lookup, public user shape, menu gating)."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.services.auth_db import AuthDB
from app.shared.response import err


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
    menus: list[str] | None = None,
) -> dict | None:
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
        "roles": roles or [],
        "branches": branches or [],
        "primary_branch": primary_branch,
        "menus": menus or [],
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
      - 403 MENU_FORBIDDEN kalau menu_key tidak ada di session["menus"]
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
        menus = request.session.get("menus") or []
        if menu_key not in menus:
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

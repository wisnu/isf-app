from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import build_user_public, current_user_id_or_401
from app.shared.response import err, ok

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginPayload(BaseModel):
    username: str
    password: str


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _user_agent(request: Request) -> str | None:
    return request.headers.get("user-agent")


@router.get("/providers")
def list_providers(request: Request):
    password = request.app.state.password_provider
    google = request.app.state.google_provider
    return ok(
        {
            "password": password.is_available,
            "google": google.is_available,
        }
    )


@router.post("/login")
async def login(payload: LoginPayload, request: Request):
    password_provider = request.app.state.password_provider
    db = request.app.state.auth_db
    audit = request.app.state.audit

    result = await password_provider.authenticate(payload.username, payload.password)
    if result is None:
        await audit.log(
            "login_failed",
            payload={"username": payload.username, "provider": "password"},
            ip=_client_ip(request),
            ua=_user_agent(request),
        )
        return JSONResponse(
            status_code=401,
            content=err("INVALID_CREDENTIALS", "Username or password is incorrect"),
        )

    memberships = await db.get_user_tenants(result.user_id)
    if not memberships:
        await audit.log(
            "login_blocked_no_tenant",
            user_id=result.user_id,
            payload={"provider": "password"},
        )
        return JSONResponse(
            status_code=403,
            content=err("NO_TENANT", "Account has no tenant access. Contact administrator."),
        )

    default = next((t for t in memberships if t.get("is_default")), memberships[0])

    request.session["user_id"] = result.user_id
    request.session["active_tenant_id"] = default["id"]

    user_public = await build_user_public(db, result.user_id)
    await audit.log(
        "login_success",
        user_id=result.user_id,
        tenant_id=default["id"],
        ip=_client_ip(request),
        ua=_user_agent(request),
        payload={"provider": "password"},
    )
    return ok({"user": user_public, "active_tenant_id": default["id"]})


@router.post("/logout")
async def logout(request: Request):
    user_id = request.session.get("user_id")
    audit = request.app.state.audit
    request.session.clear()
    if user_id:
        await audit.log(
            "logout", user_id=user_id, ip=_client_ip(request), ua=_user_agent(request)
        )
    return ok({"logged_out": True})


@router.get("/me")
async def me(request: Request):
    user_id, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    db = request.app.state.auth_db
    user_public = await build_user_public(db, user_id)
    if user_public is None:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))
    return ok(
        {
            "user": user_public,
            "active_tenant_id": request.session.get("active_tenant_id"),
        }
    )

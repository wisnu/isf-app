from __future__ import annotations

import bcrypt
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import build_user_public, current_user_id_or_401
from app.services.auth_db import normalize_username
from app.services.identity_client import IdentityTimeout, IdentityUnavailable, IdentityUserNotFound
from app.shared.response import err, ok

router = APIRouter(prefix="/auth", tags=["auth"])

MIN_PASSWORD_LENGTH = 8


class LoginPayload(BaseModel):
    username: str
    password: str


class ChangePasswordPayload(BaseModel):
    current_password: str
    new_password: str


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
    username = normalize_username(payload.username)

    result = await password_provider.authenticate(username, payload.password)
    if result is None:
        await audit.log(
            "login_failed",
            payload={"username": username, "provider": "password"},
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

    # Fetch profile (roles + branches + menus) dari api-python — fail-closed
    # Gunakan username sebagai identity key (matches enterprise.userapp.id_user)
    identity = request.app.state.identity_client
    try:
        profile = await identity.fetch_profile(username)
    except IdentityUserNotFound:
        await audit.log(
            "profile_fetch_failed",
            user_id=result.user_id,
            payload={"reason": "unknown_user"},
        )
        return JSONResponse(
            status_code=403,
            content=err("UNKNOWN_IDENTITY", "User tidak ditemukan di identity store"),
        )
    except IdentityTimeout:
        await audit.log(
            "profile_fetch_failed",
            user_id=result.user_id,
            payload={"reason": "timeout"},
        )
        return JSONResponse(
            status_code=503,
            content=err("IDENTITY_TIMEOUT", "Identity service timeout"),
        )
    except IdentityUnavailable:
        await audit.log(
            "profile_fetch_failed",
            user_id=result.user_id,
            payload={"reason": "unreachable"},
        )
        return JSONResponse(
            status_code=503,
            content=err("IDENTITY_UNAVAILABLE", "Identity service tidak tersedia"),
        )

    request.session["user_id"] = result.user_id
    request.session["active_tenant_id"] = default["id"]
    request.session["roles"] = [r["role_id"] for r in profile["roles"]]
    request.session["branches"] = [b["branch_code"] for b in profile["branches"]]
    primary = profile.get("primary_branch") or next(
        (b["branch_code"] for b in profile["branches"] if b.get("is_primary")), None
    )
    request.session["primary_branch"] = primary
    request.session["branch_access"] = profile.get("branch_access", "single")
    request.session["menus"] = list(profile["menus"])

    user_public = await build_user_public(
        db, result.user_id,
        roles=[r["role_id"] for r in profile["roles"]],
        branches=[b["branch_code"] for b in profile["branches"]],
        primary_branch=primary,
        menus=list(profile["menus"]),
        branch_access=profile.get("branch_access", "single"),
    )
    await audit.log(
        "login_success",
        user_id=result.user_id,
        tenant_id=default["id"],
        ip=_client_ip(request),
        ua=_user_agent(request),
        payload={
            "provider": "password",
            "role_count": len(profile["roles"]),
            "menu_count": len(profile["menus"]),
            "branch_count": len(profile["branches"]),
        },
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


@router.post("/refresh-profile")
async def refresh_profile(request: Request):
    user_id, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    db = request.app.state.auth_db
    user = await db.get_user_by_id(user_id)
    if not user:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))
    identity = request.app.state.identity_client
    audit = request.app.state.audit
    try:
        profile = await identity.fetch_profile(user["username"])
    except IdentityUserNotFound:
        await audit.log(
            "profile_fetch_failed",
            user_id=user_id,
            payload={"reason": "unknown_user", "context": "refresh"},
        )
        return JSONResponse(
            status_code=403, content=err("UNKNOWN_IDENTITY", "User tidak ditemukan")
        )
    except IdentityTimeout:
        await audit.log(
            "profile_fetch_failed",
            user_id=user_id,
            payload={"reason": "timeout", "context": "refresh"},
        )
        return JSONResponse(
            status_code=503, content=err("IDENTITY_TIMEOUT", "Identity timeout")
        )
    except IdentityUnavailable:
        await audit.log(
            "profile_fetch_failed",
            user_id=user_id,
            payload={"reason": "unreachable", "context": "refresh"},
        )
        return JSONResponse(
            status_code=503, content=err("IDENTITY_UNAVAILABLE", "Identity unavailable")
        )

    request.session["roles"] = [r["role_id"] for r in profile["roles"]]
    request.session["branches"] = [b["branch_code"] for b in profile["branches"]]
    request.session["primary_branch"] = next(
        (b["branch_code"] for b in profile["branches"] if b.get("is_primary")), None
    )
    request.session["menus"] = list(profile["menus"])

    await audit.log(
        "profile_refreshed",
        user_id=user_id,
        payload={
            "role_count": len(profile["roles"]),
            "menu_count": len(profile["menus"]),
            "branch_count": len(profile["branches"]),
        },
    )
    return ok({"refreshed": True, "menu_count": len(profile["menus"])})


@router.post("/change-password")
async def change_password(payload: ChangePasswordPayload, request: Request):
    # Personal action — setiap authenticated user dapat akses, tanpa menu gating.
    user_id, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    db = request.app.state.auth_db
    audit = request.app.state.audit
    user = await db.get_user_by_id(user_id)
    if not user:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))

    password_provider = request.app.state.password_provider
    verified = await password_provider.authenticate(user["username"], payload.current_password)
    if verified is None:
        await audit.log(
            "password_change_failed",
            user_id=user_id,
            payload={"reason": "invalid_current"},
            ip=_client_ip(request),
            ua=_user_agent(request),
        )
        return JSONResponse(
            status_code=401,
            content=err("INVALID_CURRENT_PASSWORD", "Password lama tidak sesuai"),
        )

    if len(payload.new_password) < MIN_PASSWORD_LENGTH:
        return JSONResponse(
            status_code=400,
            content=err(
                "WEAK_PASSWORD",
                f"Password baru minimal {MIN_PASSWORD_LENGTH} karakter",
            ),
        )
    if payload.new_password == payload.current_password:
        return JSONResponse(
            status_code=400,
            content=err("SAME_PASSWORD", "Password baru harus berbeda dari password lama"),
        )

    new_hash = bcrypt.hashpw(payload.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    await db.set_password(user_id, new_hash)
    await audit.log(
        "password_changed",
        user_id=user_id,
        ip=_client_ip(request),
        ua=_user_agent(request),
    )
    request.session.clear()
    return ok({"changed": True, "logged_out": True})


@router.get("/me")
async def me(request: Request):
    user_id, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    db = request.app.state.auth_db
    user_public = await build_user_public(
        db, user_id,
        roles=request.session.get("roles") or [],
        branches=request.session.get("branches") or [],
        primary_branch=request.session.get("primary_branch"),
        menus=request.session.get("menus") or [],
        branch_access=request.session.get("branch_access", "single"),
    )
    if user_public is None:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))
    return ok(
        {
            "user": user_public,
            "active_tenant_id": request.session.get("active_tenant_id"),
        }
    )

from __future__ import annotations

import secrets

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.services.auth_providers.google import make_pkce
from app.services.identity_client import IdentityTimeout, IdentityUnavailable, IdentityUserNotFound
from app.shared.response import err

router = APIRouter(prefix="/auth/google", tags=["auth"])


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _user_agent(request: Request) -> str | None:
    return request.headers.get("user-agent")


def _redirect_with_error(frontend_base: str, code: str) -> RedirectResponse:
    return RedirectResponse(f"{frontend_base}/login?sso_error={code}", status_code=302)


@router.get("/start")
async def google_start(request: Request, redirect: str = "/"):
    provider = request.app.state.google_provider
    if not provider.is_available:
        return JSONResponse(
            status_code=503,
            content=err("GOOGLE_NOT_CONFIGURED", "Google SSO is not configured"),
        )

    state = secrets.token_urlsafe(32)
    verifier, challenge = make_pkce()

    request.session["google_state"] = state
    request.session["google_pkce_verifier"] = verifier
    request.session["google_post_login_redirect"] = redirect

    url = provider.authorization_url(state, challenge)
    return RedirectResponse(url, status_code=302)


@router.get("/callback")
async def google_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
):
    settings = request.app.state.settings
    provider = request.app.state.google_provider
    db = request.app.state.auth_db
    audit = request.app.state.audit
    frontend_base = settings.frontend_base_url

    expected_state = request.session.pop("google_state", None)
    verifier = request.session.pop("google_pkce_verifier", None)
    post_login = request.session.pop("google_post_login_redirect", "/")

    if error:
        await audit.log(
            "sso_login_failed",
            payload={"reason": f"provider_error:{error}"},
            ip=_client_ip(request),
        )
        return _redirect_with_error(frontend_base, error)

    if not state or state != expected_state or not verifier or not code:
        await audit.log(
            "sso_login_failed",
            payload={"reason": "invalid_state_or_missing_params"},
            ip=_client_ip(request),
        )
        return _redirect_with_error(frontend_base, "invalid_state")

    try:
        tokens = await provider.exchange_code(code, verifier)
        id_token = tokens.get("id_token")
        if not id_token:
            raise ValueError("missing id_token")
        claims = provider.verify_id_token(id_token)
    except Exception as exc:  # noqa: BLE001 — boundary
        await audit.log(
            "sso_login_failed",
            payload={"reason": f"verify_failed:{type(exc).__name__}"},
            ip=_client_ip(request),
        )
        return _redirect_with_error(frontend_base, "verification_failed")

    email = (claims.get("email") or "").lower()
    if not provider.email_allowed(email):
        await audit.log(
            "sso_login_blocked",
            payload={"email": email, "reason": "email_not_allowed"},
            ip=_client_ip(request),
        )
        return _redirect_with_error(frontend_base, "email_not_allowed")

    user_id, jit = await provider.resolve_user(claims)
    if jit:
        await audit.log(
            "sso_jit_provisioned",
            user_id=user_id,
            payload={"email": email},
            ip=_client_ip(request),
            ua=_user_agent(request),
        )

    memberships = await db.get_user_tenants(user_id)

    # Fetch profile (roles + branches + menus) dari api-python — fail-closed
    # Gunakan email sebagai identity key (matches enterprise.userapp.id_user untuk SSO users)
    identity = request.app.state.identity_client
    try:
        profile = await identity.fetch_profile(email)
    except IdentityUserNotFound:
        await audit.log(
            "profile_fetch_failed",
            user_id=user_id,
            payload={"reason": "unknown_user"},
            ip=_client_ip(request),
        )
        return _redirect_with_error(frontend_base, "identity_user_not_found")
    except IdentityTimeout:
        await audit.log(
            "profile_fetch_failed",
            user_id=user_id,
            payload={"reason": "timeout"},
            ip=_client_ip(request),
        )
        return _redirect_with_error(frontend_base, "identity_timeout")
    except IdentityUnavailable:
        await audit.log(
            "profile_fetch_failed",
            user_id=user_id,
            payload={"reason": "unreachable"},
            ip=_client_ip(request),
        )
        return _redirect_with_error(frontend_base, "identity_unavailable")

    request.session["user_id"] = user_id
    request.session["roles"] = [r["role_id"] for r in profile["roles"]]
    request.session["branches"] = [b["branch_code"] for b in profile["branches"]]
    primary = next((b["branch_code"] for b in profile["branches"] if b.get("is_primary")), None)
    request.session["primary_branch"] = primary
    request.session["menus"] = list(profile["menus"])

    if memberships:
        default = next((t for t in memberships if t.get("is_default")), memberships[0])
        request.session["active_tenant_id"] = default["id"]
        await audit.log(
            "login_success",
            user_id=user_id,
            tenant_id=default["id"],
            ip=_client_ip(request),
            ua=_user_agent(request),
            payload={
                "provider": "google",
                "role_count": len(profile["roles"]),
                "menu_count": len(profile["menus"]),
                "branch_count": len(profile["branches"]),
            },
        )
        return RedirectResponse(f"{frontend_base}{post_login}", status_code=302)

    request.session["active_tenant_id"] = None
    await audit.log(
        "login_success_no_tenant",
        user_id=user_id,
        ip=_client_ip(request),
        ua=_user_agent(request),
        payload={"provider": "google"},
    )
    return RedirectResponse(f"{frontend_base}/no-tenant", status_code=302)

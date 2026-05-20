"""Google OAuth2 / OIDC provider for portal SSO."""

from __future__ import annotations

import base64
import hashlib
import secrets
from typing import Any
from urllib.parse import urlencode

import httpx
import jwt
from jwt import PyJWKClient

from app.services.auth_db import AuthDB
from app.shared.config import Settings


def make_pkce() -> tuple[str, str]:
    """Generate (verifier, challenge) pair for OAuth2 PKCE S256."""
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest())
        .rstrip(b"=")
        .decode("ascii")
    )
    return verifier, challenge


class GoogleOAuthProvider:
    name = "google"

    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    JWKS_URI = "https://www.googleapis.com/oauth2/v3/certs"
    ISSUERS = {"https://accounts.google.com", "accounts.google.com"}
    SCOPES = ("openid", "email", "profile")

    def __init__(self, db: AuthDB, settings: Settings):
        self.db = db
        self.settings = settings
        # PyJWKClient caches signing keys internally
        self._jwks = PyJWKClient(self.JWKS_URI)

    @property
    def is_available(self) -> bool:
        return bool(
            self.settings.google_oauth_client_id and self.settings.google_oauth_client_secret
        )

    def authorization_url(self, state: str, code_challenge: str) -> str:
        params = {
            "client_id": self.settings.google_oauth_client_id,
            "redirect_uri": self.settings.google_oauth_redirect_url,
            "response_type": "code",
            "scope": " ".join(self.SCOPES),
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "access_type": "online",
            "prompt": "select_account",
        }
        return f"{self.AUTH_URL}?{urlencode(params)}"

    async def exchange_code(self, code: str, code_verifier: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.settings.google_oauth_client_id,
                    "client_secret": self.settings.google_oauth_client_secret,
                    "code": code,
                    "code_verifier": code_verifier,
                    "redirect_uri": self.settings.google_oauth_redirect_url,
                    "grant_type": "authorization_code",
                },
                headers={"Accept": "application/json"},
            )
            r.raise_for_status()
            return r.json()

    def verify_id_token(self, id_token: str) -> dict[str, Any]:
        key = self._jwks.get_signing_key_from_jwt(id_token).key
        claims = jwt.decode(
            id_token,
            key,
            algorithms=["RS256"],
            audience=self.settings.google_oauth_client_id,
            options={"verify_exp": True, "require": ["iss", "aud", "exp", "iat", "sub"]},
        )
        if claims.get("iss") not in self.ISSUERS:
            raise ValueError("invalid issuer")
        return claims

    def email_allowed(self, email: str | None) -> bool:
        if not email:
            return False
        e = email.lower()
        emails = [
            x.strip().lower()
            for x in self.settings.google_allowed_emails.split(",")
            if x.strip()
        ]
        domains = [
            x.strip().lower()
            for x in self.settings.google_allowed_domains.split(",")
            if x.strip()
        ]
        if emails and e in emails:
            return True
        if domains and any(e.endswith("@" + d) for d in domains):
            return True
        return False

    async def resolve_user(self, claims: dict[str, Any]) -> tuple[str, bool]:
        """Find or JIT-provision user for verified Google claims.

        Returns (user_id, jit_provisioned).
        """
        sub = claims["sub"]
        email = (claims.get("email") or "").lower()

        link = await self.db.get_provider_link(self.name, sub)
        if link:
            return link["user_id"], False

        if email:
            existing = await self.db.get_user_by_username(email)
            if existing:
                await self.db.create_provider_link(existing["id"], self.name, sub, email)
                return existing["id"], False

        display_name = claims.get("name") or email or "(unnamed)"
        username = email or sub
        user_id = await self.db.create_user(username=username, display_name=display_name)
        await self.db.create_provider_link(user_id, self.name, sub, email or None)
        return user_id, True

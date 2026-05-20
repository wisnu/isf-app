"""Tests for the Google SSO router (mocked Google internals)."""

from unittest.mock import patch

import pytest

from app.services.auth_providers.google import GoogleOAuthProvider, make_pkce


def test_make_pkce_returns_different_values():
    v1, c1 = make_pkce()
    v2, c2 = make_pkce()
    assert v1 != v2 and c1 != c2
    assert v1.isascii() and c1.isascii()


def test_email_allowed_uses_domain_whitelist():
    from app.shared.config import Settings

    provider = GoogleOAuthProvider.__new__(GoogleOAuthProvider)
    provider.settings = Settings(
        google_oauth_client_id="x",
        google_oauth_client_secret="y",
        google_allowed_domains="ihsansolusi.co.id",
        google_allowed_emails="",
        auth_db_path="/tmp/ignored.sqlite",
    )

    assert provider.email_allowed("user@ihsansolusi.co.id") is True
    assert provider.email_allowed("user@evil.com") is False
    assert provider.email_allowed("") is False


def test_email_allowed_uses_emails_whitelist_takes_precedence():
    from app.shared.config import Settings

    provider = GoogleOAuthProvider.__new__(GoogleOAuthProvider)
    provider.settings = Settings(
        google_oauth_client_id="x",
        google_oauth_client_secret="y",
        google_allowed_domains="",
        google_allowed_emails="boss@external.com",
        auth_db_path="/tmp/ignored.sqlite",
    )

    assert provider.email_allowed("boss@external.com") is True
    assert provider.email_allowed("other@external.com") is False


def test_google_start_returns_503_when_unconfigured(client):
    response = client.get("/api/auth/google/start", follow_redirects=False)
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "GOOGLE_NOT_CONFIGURED"


def test_google_callback_rejects_missing_state(client):
    response = client.get(
        "/api/auth/google/callback?code=x&state=y", follow_redirects=False
    )
    assert response.status_code == 302
    assert "sso_error=invalid_state" in response.headers.get("location", "")


@pytest.fixture
def google_provider_enabled(settings, monkeypatch):
    """Override settings to simulate Google being configured + mock exchange/verify."""
    monkeypatch.setattr(settings, "google_oauth_client_id", "fake-client")
    monkeypatch.setattr(settings, "google_oauth_client_secret", "fake-secret")
    return settings


async def test_google_callback_blocks_disallowed_email(app, client, google_provider_enabled):
    # Force the provider to consider itself available even after app init
    app.state.google_provider.settings = google_provider_enabled

    # Prime the session with state+verifier (must do via two-step flow)
    with patch(
        "app.routers.auth_google.RedirectResponse",
        wraps=__import__("fastapi.responses", fromlist=["RedirectResponse"]).RedirectResponse,
    ):
        start_resp = client.get("/api/auth/google/start", follow_redirects=False)
    assert start_resp.status_code == 302  # redirect to Google
    state = None
    # The state is embedded in the redirect URL; parse it
    from urllib.parse import parse_qs, urlparse

    qs = parse_qs(urlparse(start_resp.headers["location"]).query)
    state = qs["state"][0]

    # Mock the token exchange and id_token verification
    fake_claims = {
        "iss": "https://accounts.google.com",
        "aud": "fake-client",
        "exp": 9999999999,
        "iat": 1,
        "sub": "google-sub-evil",
        "email": "intruder@evil.com",
        "name": "Intruder",
    }

    with patch(
        "app.services.auth_providers.google.GoogleOAuthProvider.exchange_code",
        return_value={"id_token": "fake.id.token"},
    ), patch(
        "app.services.auth_providers.google.GoogleOAuthProvider.verify_id_token",
        return_value=fake_claims,
    ):
        cb = client.get(
            f"/api/auth/google/callback?code=fakecode&state={state}",
            follow_redirects=False,
        )

    assert cb.status_code == 302
    assert "sso_error=email_not_allowed" in cb.headers["location"]

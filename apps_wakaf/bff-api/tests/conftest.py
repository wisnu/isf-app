from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.shared.config import Settings


@pytest.fixture
def settings(tmp_path):
    return Settings(
        app_env="test",
        api_python_base_url="http://api-python:8000",
        session_secret="test-secret-12345",
        cors_origin="http://localhost:5173",
        auth_providers="password,google",
        auth_db_path=str(tmp_path / "test_auth.sqlite"),
        google_oauth_client_id="",
        google_oauth_client_secret="",
        google_oauth_redirect_url="http://localhost:7000/api/auth/google/callback",
        google_allowed_domains="ihsansolusi.co.id",
        google_allowed_emails="",
        frontend_base_url="http://localhost:5173",
    )


@pytest.fixture
def app(settings):
    return create_app(settings)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c

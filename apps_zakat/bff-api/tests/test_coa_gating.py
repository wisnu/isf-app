"""Tests for menu-gating on COA endpoints (keuangan.coa)."""

from __future__ import annotations

import pytest


def test_coa_accounts_denied_when_menu_not_in_session(client, mock_identity):
    mock_identity.set_profile("finance.a", menus=["dashboard.overview"])  # no keuangan.coa
    client.post("/api/auth/login", json={"username": "finance.a", "password": "finance123"})
    response = client.get("/api/coa/accounts")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "MENU_FORBIDDEN"


def test_coa_accounts_xlsx_denied_when_menu_not_in_session(client, mock_identity):
    mock_identity.set_profile("finance.a", menus=["dashboard.overview"])  # no keuangan.coa
    client.post("/api/auth/login", json={"username": "finance.a", "password": "finance123"})
    response = client.get("/api/coa/accounts.xlsx")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "MENU_FORBIDDEN"


def test_coa_accounts_requires_auth(client):
    response = client.get("/api/coa/accounts")
    assert response.status_code == 401


def test_coa_accounts_allowed_when_menu_in_session(client, mock_identity):
    """admin has keuangan.coa — should reach proxy (we expect 503/downstream error, not 403)."""
    # admin is pre-seeded with keuangan.coa in mock_identity fixture
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.get("/api/coa/accounts")
    # admin has the menu; downstream (api-python) is not running, so we expect non-403
    assert response.status_code != 403

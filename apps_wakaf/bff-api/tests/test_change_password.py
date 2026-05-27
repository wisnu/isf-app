"""Tests untuk POST /api/auth/change-password.

Endpoint adalah personal action — semua authenticated user dapat akses
tanpa menu gating. Coverage:
- happy path: success → session cleared → old fail → new sukses login
- 401 saat tidak login
- 401 INVALID_CURRENT_PASSWORD saat current salah
- 400 WEAK_PASSWORD saat new < 8 chars
- 400 SAME_PASSWORD saat new == current
"""

from __future__ import annotations


def _login_admin(client):
    response = client.post(
        "/api/auth/login", json={"username": "ADMIN", "password": "admin123"}
    )
    assert response.status_code == 200, response.text


def test_change_password_requires_authentication(client):
    response = client.post(
        "/api/auth/change-password",
        json={"current_password": "admin123", "new_password": "newpass123"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_change_password_invalid_current(client):
    _login_admin(client)
    response = client.post(
        "/api/auth/change-password",
        json={"current_password": "wrong-old", "new_password": "newpass123"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CURRENT_PASSWORD"


def test_change_password_weak_new(client):
    _login_admin(client)
    response = client.post(
        "/api/auth/change-password",
        json={"current_password": "admin123", "new_password": "short"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "WEAK_PASSWORD"


def test_change_password_same_as_current(client):
    _login_admin(client)
    response = client.post(
        "/api/auth/change-password",
        json={"current_password": "admin123", "new_password": "admin123"},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "SAME_PASSWORD"


def test_change_password_success_auto_logout_and_new_works(client):
    _login_admin(client)

    response = client.post(
        "/api/auth/change-password",
        json={"current_password": "admin123", "new_password": "newpass123"},
    )
    assert response.status_code == 200, response.text
    body = response.json()["data"]
    assert body["changed"] is True
    assert body["logged_out"] is True

    # Session cleared
    assert client.get("/api/auth/me").status_code == 401

    # Password lama tidak bisa login
    bad = client.post(
        "/api/auth/login", json={"username": "ADMIN", "password": "admin123"}
    )
    assert bad.status_code == 401

    # Password baru bisa login
    good = client.post(
        "/api/auth/login", json={"username": "ADMIN", "password": "newpass123"}
    )
    assert good.status_code == 200

import asyncio
import json

import asyncpg
import httpx
import pytest


def test_admin_get_denied_when_not_authenticated(client):
    response = client.get("/api/admin/role-menu")
    assert response.status_code == 401


def test_admin_get_denied_when_not_admin(client, mock_identity):
    # finance.a default menus tidak punya admin.role_menu
    client.post("/api/auth/login", json={"username": "finance.a", "password": "finance123"})
    response = client.get("/api/admin/role-menu")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "MENU_FORBIDDEN"


def test_admin_get_allowed_when_admin(client, mock_identity, monkeypatch):
    mock_identity.set_profile("admin", menus=["admin.role_menu"])
    async def fake_get(path, params=None):
        return httpx.Response(
            200,
            json={
                "data": {"roles": [], "menus": [], "mapping": []},
                "meta": {"request_id": "req_test"},
            },
        )
    monkeypatch.setattr("app.routers.admin.get_api_python", fake_get)
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.get("/api/admin/role-menu")
    assert response.status_code == 200
    assert response.json()["data"] == {"roles": [], "menus": [], "mapping": []}


def test_admin_put_injects_updated_by_from_session(client, mock_identity, monkeypatch):
    mock_identity.set_profile("admin", menus=["admin.role_menu"])
    captured = {}
    async def fake_post(path, *, json_body, method="POST"):
        captured["body"] = json_body
        captured["method"] = method
        return httpx.Response(
            200,
            json={
                "data": {
                    "updated": True, "total_rows": 1,
                    "diff": {"added": [], "removed": []},
                },
                "meta": {"request_id": "x"},
            },
        )
    monkeypatch.setattr("app.routers.admin.post_api_python", fake_post)
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.put(
        "/api/admin/role-menu",
        json={"mapping": [{"id_peran": "ADM", "menu_key": "dashboard.overview"}]},
    )
    assert response.status_code == 200
    # updated_by harus di-inject BFF dari session.username, bukan dari client
    assert captured["body"]["updated_by"] == "ADMIN"
    assert captured["method"] == "PUT"


def test_admin_put_audits_on_success(client, mock_identity, monkeypatch, settings):
    mock_identity.set_profile("admin", menus=["admin.role_menu"])
    async def fake_post(path, *, json_body, method="POST"):
        return httpx.Response(
            200,
            json={
                "data": {
                    "updated": True, "total_rows": 2,
                    "diff": {
                        "added": [{"id_peran": "ADM", "menu_key": "dashboard.overview"}],
                        "removed": [{"id_peran": "KEU", "menu_key": "fake"}],
                    },
                },
                "meta": {"request_id": "x"},
            },
        )
    monkeypatch.setattr("app.routers.admin.post_api_python", fake_post)
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.put(
        "/api/admin/role-menu",
        json={"mapping": [{"id_peran": "ADM", "menu_key": "dashboard.overview"}]},
    )
    assert response.status_code == 200

    # Verify audit log row written (via asyncpg directly — DB is Postgres)
    async def get_audit():
        conn = await asyncpg.connect(settings.isf_auth_database_url)
        try:
            row = await conn.fetchrow(
                "SELECT event, payload FROM isf_auth.audit_log "
                "WHERE event='role_menu_updated' ORDER BY ts DESC LIMIT 1"
            )
            return row
        finally:
            await conn.close()

    row = asyncio.new_event_loop().run_until_complete(get_audit())
    assert row is not None
    assert row["event"] == "role_menu_updated"
    payload = row["payload"]
    # asyncpg returns JSONB as a dict or string depending on version
    if isinstance(payload, str):
        payload = json.loads(payload)
    assert "added_count" in payload

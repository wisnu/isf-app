from unittest.mock import AsyncMock, patch

import httpx
import pytest


def login(client, username="admin", password="admin123"):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def test_dashboard_summary_requires_auth(client):
    assert client.get("/api/dashboard/summary").status_code == 401


@pytest.fixture
def mock_downstream():
    payload = {
        "data": {
            "tenant_id": "perusahaan_a",
            "tenant_name": "Lembaga ZISWAF A",
            "penerimaan": {"total": 1_250_000_000, "period": "2026-05"},
            "penyaluran": {"total": 875_000_000, "period": "2026-05"},
        },
        "meta": {"request_id": "req_test"},
    }
    response = httpx.Response(200, json=payload)
    with patch(
        "app.routers.dashboard.get_api_python", new=AsyncMock(return_value=response)
    ) as m:
        yield m


def test_dashboard_summary_proxies_with_active_tenant(client, mock_downstream):
    login(client)
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["tenant_id"] == "perusahaan_a"
    mock_downstream.assert_called_once()
    args, kwargs = mock_downstream.call_args
    assert "/api/v1/dashboard/summary" in args[0]
    assert kwargs.get("params") == {"tenant_id": "perusahaan_a"}

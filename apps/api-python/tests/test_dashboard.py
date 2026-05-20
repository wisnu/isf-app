from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_summary_returns_data_for_tenant_a():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "perusahaan_a"})
    assert response.status_code == 200
    body = response.json()
    assert "data" in body and "meta" in body
    data = body["data"]
    assert data["tenant_id"] == "perusahaan_a"
    assert data["penerimaan"]["total"] > 0
    assert data["penyaluran"]["total"] > 0


def test_dashboard_summary_returns_data_for_tenant_b():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "perusahaan_b"})
    assert response.status_code == 200
    assert response.json()["data"]["tenant_id"] == "perusahaan_b"


def test_dashboard_summary_unknown_tenant_returns_404():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "nonexistent"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TENANT_NOT_FOUND"

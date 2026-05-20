from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_summary_returns_full_payload_for_tenant_a():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "perusahaan_a"})
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["tenant_id"] == "perusahaan_a"
    assert data["period"] == "2026-05"
    # KPIs
    assert set(data["kpis"].keys()) == {"penerimaan", "penyaluran", "saldo", "donatur_baru"}
    assert data["kpis"]["penerimaan"]["total"] > 0
    assert "delta_pct" in data["kpis"]["penerimaan"]
    # Trend
    assert len(data["trend"]["labels"]) == 6
    assert len(data["trend"]["penerimaan"]) == 6
    assert len(data["trend"]["penyaluran"]) == 6
    # Asnaf (8 categories)
    assert len(data["asnaf_distribution"]) == 8
    assert {item["label"] for item in data["asnaf_distribution"]} >= {
        "Fakir", "Miskin", "Amil", "Mualaf", "Riqab", "Gharimin", "Fi Sabilillah", "Ibnu Sabil"
    }
    # Channels
    assert len(data["fundraising_channels"]) >= 3
    for ch in data["fundraising_channels"]:
        assert "actual" in ch and "target" in ch
    # Recent transactions
    assert len(data["recent_transactions"]) == 10
    for tx in data["recent_transactions"]:
        assert {"id", "date", "type", "channel", "amount", "donor"} <= set(tx.keys())


def test_summary_for_tenant_b_returns_different_numbers():
    a = client.get("/api/v1/dashboard/summary", params={"tenant_id": "perusahaan_a"}).json()["data"]
    b = client.get("/api/v1/dashboard/summary", params={"tenant_id": "perusahaan_b"}).json()["data"]
    assert a["kpis"]["penerimaan"]["total"] != b["kpis"]["penerimaan"]["total"]
    assert a["recent_transactions"][0]["id"] != b["recent_transactions"][0]["id"]


def test_summary_unknown_tenant_returns_404():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "nonexistent"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TENANT_NOT_FOUND"

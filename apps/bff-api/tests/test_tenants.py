def login(client, username="admin", password="admin123"):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def test_tenants_list_requires_auth(client):
    response = client.get("/api/tenants")
    assert response.status_code == 401


def test_tenants_list_returns_user_tenants(client):
    login(client)
    response = client.get("/api/tenants")
    assert response.status_code == 200
    tenants = response.json()["data"]["tenants"]
    assert {t["id"] for t in tenants} == {"perusahaan_a", "perusahaan_b"}
    assert response.json()["data"]["active_tenant_id"] == "perusahaan_a"


def test_tenants_list_finance_a_only_sees_a(client):
    login(client, "finance.a", "finance123")
    response = client.get("/api/tenants")
    tenants = response.json()["data"]["tenants"]
    assert [t["id"] for t in tenants] == ["perusahaan_a"]


def test_tenants_switch_to_allowed_tenant(client):
    login(client)
    response = client.post("/api/tenants/switch", json={"tenant_id": "perusahaan_b"})
    assert response.status_code == 200
    assert response.json()["data"]["active_tenant_id"] == "perusahaan_b"
    assert client.get("/api/auth/me").json()["data"]["active_tenant_id"] == "perusahaan_b"


def test_tenants_switch_to_disallowed_tenant_rejected(client):
    login(client, "finance.a", "finance123")
    response = client.post("/api/tenants/switch", json={"tenant_id": "perusahaan_b"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "TENANT_FORBIDDEN"

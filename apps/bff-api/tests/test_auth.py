def test_providers_lists_password_only_when_google_unconfigured(client):
    response = client.get("/api/auth/providers")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["password"] is True
    assert data["google"] is False


def test_me_unauthenticated_returns_401(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_login_with_valid_credentials_returns_user_and_active_tenant(client):
    response = client.post(
        "/api/auth/login", json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["user"]["username"] == "admin"
    assert body["data"]["active_tenant_id"] == "perusahaan_a"


def test_login_invalid_credentials_returns_401(client):
    response = client.post(
        "/api/auth/login", json={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_unknown_user_returns_401(client):
    response = client.post(
        "/api/auth/login", json={"username": "ghost", "password": "whatever"}
    )
    assert response.status_code == 401


def test_me_after_login_returns_user(client):
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["data"]["user"]["username"] == "admin"


def test_logout_clears_session(client):
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    assert client.get("/api/auth/me").status_code == 401

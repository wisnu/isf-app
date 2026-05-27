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
        "/api/auth/login", json={"username": "ADMIN", "password": "admin123"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["user"]["username"] == "ADMIN"
    assert body["data"]["active_tenant_id"] == "perusahaan_a"


def test_login_is_case_insensitive_for_username(client):
    """Input dari frontend boleh case apapun, lookup tetap jalan."""
    response = client.post(
        "/api/auth/login", json={"username": "Admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["user"]["username"] == "ADMIN"


def test_login_trims_whitespace(client):
    response = client.post(
        "/api/auth/login", json={"username": "  admin  ", "password": "admin123"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["user"]["username"] == "ADMIN"


def test_login_invalid_credentials_returns_401(client):
    response = client.post(
        "/api/auth/login", json={"username": "ADMIN", "password": "wrong"}
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
    assert response.json()["data"]["user"]["username"] == "ADMIN"


def test_logout_clears_session(client):
    client.post("/api/auth/login", json={"username": "ADMIN", "password": "admin123"})
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_login_populates_session_with_menus(client, mock_identity):
    mock_identity.set_profile("ADMIN", menus=["dashboard.overview", "keuangan.coa"])
    response = client.post("/api/auth/login", json={"username": "ADMIN", "password": "admin123"})
    assert response.status_code == 200
    assert "user" in response.json()["data"]


def test_login_fails_closed_when_identity_unavailable(client, mock_identity):
    mock_identity.set_unavailable()
    response = client.post("/api/auth/login", json={"username": "ADMIN", "password": "admin123"})
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "IDENTITY_UNAVAILABLE"


def test_login_returns_403_when_user_unknown_in_identity(client, mock_identity):
    mock_identity.profiles.pop("ADMIN", None)
    response = client.post("/api/auth/login", json={"username": "ADMIN", "password": "admin123"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "UNKNOWN_IDENTITY"


def test_me_includes_roles_branches_menus(client, mock_identity):
    mock_identity.set_profile(
        "ADMIN",
        roles=[{"id_peran": "ADM", "nama_peran": "Admin", "level": 9}],
        branches=[
            {"kode_cabang": "CB01", "is_primary": True},
            {"kode_cabang": "CB02", "is_primary": False},
        ],
        menus=["dashboard.overview", "keuangan.coa"],
    )
    client.post("/api/auth/login", json={"username": "ADMIN", "password": "admin123"})
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    user = response.json()["data"]["user"]
    assert user["roles"] == ["ADM"]
    assert sorted(user["branches"]) == ["CB01", "CB02"]
    assert user["primary_branch"] == "CB01"
    assert sorted(user["menus"]) == ["dashboard.overview", "keuangan.coa"]


def test_refresh_profile_updates_session_menus(client, mock_identity):
    mock_identity.set_profile("ADMIN", menus=["dashboard.overview"])
    client.post("/api/auth/login", json={"username": "ADMIN", "password": "admin123"})
    mock_identity.set_profile("ADMIN", menus=["dashboard.overview", "keuangan.coa"])
    response = client.post("/api/auth/refresh-profile")
    assert response.status_code == 200
    me = client.get("/api/auth/me")
    assert sorted(me.json()["data"]["user"]["menus"]) == ["dashboard.overview", "keuangan.coa"]


def test_refresh_profile_requires_auth(client):
    response = client.post("/api/auth/refresh-profile")
    assert response.status_code == 401


def test_refresh_profile_returns_503_when_identity_unavailable(client, mock_identity):
    client.post("/api/auth/login", json={"username": "ADMIN", "password": "admin123"})
    mock_identity.set_unavailable()
    response = client.post("/api/auth/refresh-profile")
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "IDENTITY_UNAVAILABLE"

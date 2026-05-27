import pytest

from app.modules.identity import service as identity_service
from app.modules.identity.schema import ProfileResponse


class _FakeDB:
    """In-memory stand-in for asyncpg helpers. Routes by query substring."""

    def __init__(self, *, user=None, roles=None, branches=None, menus=None):
        self.user = user
        self.roles = roles or []
        self.branches = branches or []
        self.menus = menus or []

    async def fetch_one(self, query, *args):
        if "FROM enterprise.userapp" in query:
            return self.user
        raise AssertionError(f"unexpected fetch_one: {query!r}")

    async def fetch_all(self, query, *args):
        if "FROM enterprise.listperanuser" in query:
            return self.roles
        if "FROM enterprise.listcabangdiizinkan" in query:
            return self.branches
        if "FROM isf_auth.role_menu" in query:
            return self.menus
        raise AssertionError(f"unexpected fetch_all: {query!r}")


@pytest.fixture
def patch_db(monkeypatch):
    def _patch(fake: _FakeDB):
        monkeypatch.setattr(identity_service, "fetch_one", fake.fetch_one)
        monkeypatch.setattr(identity_service, "fetch_all", fake.fetch_all)
    return _patch


@pytest.mark.asyncio
async def test_profile_unknown_user_returns_none(patch_db):
    patch_db(_FakeDB(user=None))
    result = await identity_service.get_profile("GHOST")
    assert result is None


@pytest.mark.asyncio
async def test_profile_user_no_roles_returns_empty_menus(patch_db):
    patch_db(_FakeDB(
        user={"id_user": "U1", "status_profil": "A", "kode_cabang": "CB01"},
        roles=[],
        branches=[],
        menus=[],
    ))
    result = await identity_service.get_profile("U1")
    assert isinstance(result, ProfileResponse)
    assert result.user_id == "U1"
    assert result.status == "active"
    assert result.roles == []
    assert result.menus == []


@pytest.mark.asyncio
async def test_profile_normal_user_returns_menus(patch_db):
    patch_db(_FakeDB(
        user={"id_user": "U1", "status_profil": "A", "kode_cabang": "CB01"},
        roles=[
            {"id_peran": "FINANCE_HEAD", "nama_peran": "Finance Head", "level_peranuser": 9},
        ],
        branches=[{"kode_cabang": "CB01"}, {"kode_cabang": "CB02"}],
        menus=[{"menu_key": "dashboard.overview"}, {"menu_key": "keuangan.coa"}],
    ))
    result = await identity_service.get_profile("U1")
    assert result is not None
    assert [r.id_peran for r in result.roles] == ["FINANCE_HEAD"]
    assert result.roles[0].level == 9
    assert sorted(result.menus) == ["dashboard.overview", "keuangan.coa"]


@pytest.mark.asyncio
async def test_profile_marks_primary_branch_from_userapp(patch_db):
    patch_db(_FakeDB(
        user={"id_user": "U1", "status_profil": "A", "kode_cabang": "CB02"},
        roles=[],
        branches=[{"kode_cabang": "CB01"}, {"kode_cabang": "CB02"}],
        menus=[],
    ))
    result = await identity_service.get_profile("U1")
    primary = [b for b in result.branches if b.is_primary]
    assert len(primary) == 1
    assert primary[0].kode_cabang == "CB02"


@pytest.mark.asyncio
async def test_profile_dedupes_menus_across_roles(patch_db):
    patch_db(_FakeDB(
        user={"id_user": "U1", "status_profil": "A", "kode_cabang": "CB01"},
        roles=[
            {"id_peran": "R1", "nama_peran": "R1", "level_peranuser": 1},
            {"id_peran": "R2", "nama_peran": "R2", "level_peranuser": 1},
        ],
        branches=[],
        menus=[
            {"menu_key": "dashboard.overview"},
            {"menu_key": "dashboard.overview"},
            {"menu_key": "keuangan.coa"},
        ],
    ))
    result = await identity_service.get_profile("U1")
    assert sorted(result.menus) == ["dashboard.overview", "keuangan.coa"]


@pytest.mark.asyncio
async def test_profile_inactive_status_marked_inactive(patch_db):
    patch_db(_FakeDB(
        user={"id_user": "U1", "status_profil": "N", "kode_cabang": "CB01"},
        roles=[],
        branches=[],
        menus=[],
    ))
    result = await identity_service.get_profile("U1")
    assert result.status == "inactive"


from fastapi.testclient import TestClient

from app import main as api_main


def test_router_unknown_user_returns_404(monkeypatch):
    async def fake_get_profile(user_id: str):
        return None
    monkeypatch.setattr("app.modules.identity.router.get_profile", fake_get_profile)
    client = TestClient(api_main.app)
    response = client.get("/api/identity/GHOST/profile")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "USER_NOT_FOUND"


def test_router_normal_user_returns_envelope(monkeypatch):
    async def fake_get_profile(user_id: str):
        from app.modules.identity.schema import ProfileResponse
        return ProfileResponse(
            user_id=user_id, status="active",
            roles=[], branches=[], menus=["dashboard.overview"],
        )
    monkeypatch.setattr("app.modules.identity.router.get_profile", fake_get_profile)
    client = TestClient(api_main.app)
    response = client.get("/api/identity/U1/profile")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["user_id"] == "U1"
    assert body["data"]["menus"] == ["dashboard.overview"]
    assert "request_id" in body["meta"]

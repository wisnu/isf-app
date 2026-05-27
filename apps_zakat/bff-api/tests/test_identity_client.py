import httpx
import pytest

from app.services.identity_client import (
    IdentityClient,
    IdentityError,
    IdentityTimeout,
    IdentityUnavailable,
    IdentityUserNotFound,
)


@pytest.mark.asyncio
async def test_fetch_profile_returns_data_on_200():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/identity/U1/profile"
        return httpx.Response(
            200,
            json={
                "data": {
                    "user_id": "U1", "status": "active",
                    "roles": [], "branches": [], "menus": ["dashboard.overview"],
                },
                "meta": {"request_id": "req_test"},
            },
        )
    transport = httpx.MockTransport(handler)
    client = IdentityClient("http://api-python:8000", transport=transport)
    profile = await client.fetch_profile("U1")
    assert profile["user_id"] == "U1"
    assert profile["menus"] == ["dashboard.overview"]


@pytest.mark.asyncio
async def test_fetch_profile_404_raises_user_not_found():
    def handler(request):
        return httpx.Response(404, json={"error": {"code": "USER_NOT_FOUND", "message": "no"}, "meta": {}})
    transport = httpx.MockTransport(handler)
    client = IdentityClient("http://api-python:8000", transport=transport)
    with pytest.raises(IdentityUserNotFound):
        await client.fetch_profile("GHOST")


@pytest.mark.asyncio
async def test_fetch_profile_connect_error_raises_unavailable():
    def handler(request):
        raise httpx.ConnectError("nope")
    transport = httpx.MockTransport(handler)
    client = IdentityClient("http://api-python:8000", transport=transport)
    with pytest.raises(IdentityUnavailable):
        await client.fetch_profile("U1")


@pytest.mark.asyncio
async def test_fetch_profile_timeout_raises_timeout():
    def handler(request):
        raise httpx.ReadTimeout("slow")
    transport = httpx.MockTransport(handler)
    client = IdentityClient("http://api-python:8000", transport=transport)
    with pytest.raises(IdentityTimeout):
        await client.fetch_profile("U1")


@pytest.mark.asyncio
async def test_fetch_profile_5xx_raises_unavailable():
    def handler(request):
        return httpx.Response(503, json={"error": {"code": "DB_DOWN", "message": "x"}, "meta": {}})
    transport = httpx.MockTransport(handler)
    client = IdentityClient("http://api-python:8000", transport=transport)
    with pytest.raises(IdentityUnavailable):
        await client.fetch_profile("U1")

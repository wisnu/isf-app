"""HTTP client untuk fetch profile dari api-python identity module."""

from __future__ import annotations

import httpx


class IdentityError(Exception):
    """Base error untuk identity lookup."""


class IdentityUnavailable(IdentityError):
    """api-python unreachable atau 5xx."""


class IdentityTimeout(IdentityError):
    """Profile fetch timeout."""


class IdentityUserNotFound(IdentityError):
    """User tidak ada di enterprise.usertbl (api-python 404)."""


class IdentityClient:
    def __init__(self, base_url: str, *, timeout: float = 3.0, transport: httpx.AsyncBaseTransport | None = None):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._transport = transport

    async def fetch_profile(self, user_id: str) -> dict:
        url = f"{self._base_url}/api/identity/{user_id}/profile"
        try:
            async with httpx.AsyncClient(timeout=self._timeout, transport=self._transport) as client:
                response = await client.get(url)
        except httpx.TimeoutException as exc:
            raise IdentityTimeout(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise IdentityUnavailable(str(exc)) from exc

        if response.status_code == 404:
            raise IdentityUserNotFound(user_id)
        if response.status_code >= 500:
            raise IdentityUnavailable(f"upstream {response.status_code}")
        if response.status_code != 200:
            raise IdentityUnavailable(f"unexpected status {response.status_code}")

        payload = response.json()
        return payload["data"]

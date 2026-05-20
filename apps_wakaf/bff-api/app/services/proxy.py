import httpx

from app.shared.config import settings


async def get_api_python(path: str, params: dict | None = None) -> httpx.Response:
    url = f"{settings.api_python_base_url}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        return await client.get(url, params=params)

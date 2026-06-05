import httpx

from app.shared.config import settings


async def get_api_python(path: str, params: dict | None = None) -> httpx.Response:
    url = f"{settings.api_python_base_url}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        return await client.get(url, params=params)


async def get_report_api(path: str, params: dict | None = None) -> httpx.Response:
    """GET ke report-api (dashboard + report). Timeout sedikit lebih longgar
    karena query agregasi/reporting lebih berat dari CRUD."""
    url = f"{settings.report_api_base_url}{path}"
    async with httpx.AsyncClient(timeout=15.0) as client:
        return await client.get(url, params=params)


async def stream_report_api(path: str, params: dict | None = None) -> httpx.Response:
    """GET biner ke report-api (mis. export .xlsx). Timeout lebih longgar untuk
    generate file. Caller meneruskan content + headers (Content-Type/Disposition)."""
    url = f"{settings.report_api_base_url}{path}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        return await client.get(url, params=params)


async def post_api_python(
    path: str,
    *,
    json_body: dict,
    method: str = "POST",
) -> httpx.Response:
    """HTTP request dengan body JSON ke api-python. Default POST,
    override method untuk PUT/PATCH."""
    url = f"{settings.api_python_base_url}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        return await client.request(method, url, json=json_body)


async def post_multipart_api_python(
    path: str,
    *,
    data: dict,
    file_content: bytes,
    file_field: str = 'file',
    filename: str = 'upload',
    content_type: str = 'application/octet-stream',
) -> httpx.Response:
    """POST multipart/form-data ke api-python (untuk upload file)."""
    url = f"{settings.api_python_base_url}{path}"
    files = {file_field: (filename, file_content, content_type)}
    async with httpx.AsyncClient(timeout=30.0) as client:
        return await client.post(url, data=data, files=files)


async def stream_api_python(path: str, params: dict | None = None) -> httpx.Response:
    """GET biner ke api-python (mis. export .xlsx). Timeout lebih longgar untuk generate file."""
    url = f"{settings.api_python_base_url}{path}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        return await client.get(url, params=params)

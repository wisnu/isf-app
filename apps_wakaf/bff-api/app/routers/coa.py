from __future__ import annotations

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse, Response

from app.services.auth import current_user_id_or_401
from app.services.proxy import get_api_python

router = APIRouter(prefix="/coa", tags=["coa"])


@router.get("/accounts")
async def accounts(
    request: Request,
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params: dict[str, str | int] = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    downstream = await get_api_python("/api/v1/coa/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/accounts.xlsx")
async def accounts_xlsx(
    request: Request,
    search: str | None = Query(default=None),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params: dict[str, str] = {}
    if search:
        params["search"] = search
    downstream = await get_api_python(
        "/api/v1/coa/accounts.xlsx", params=params or None
    )
    if downstream.status_code != 200:
        try:
            return JSONResponse(
                status_code=downstream.status_code, content=downstream.json()
            )
        except Exception:
            return Response(
                content=downstream.content, status_code=downstream.status_code
            )
    return Response(
        content=downstream.content,
        media_type=downstream.headers.get(
            "content-type", "application/octet-stream"
        ),
        headers={
            "Content-Disposition": downstream.headers.get(
                "Content-Disposition", 'attachment; filename="coa.xlsx"'
            ),
        },
    )

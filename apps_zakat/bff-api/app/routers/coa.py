from __future__ import annotations

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse, Response

from app.services.auth import current_user_id_or_401
from app.services.proxy import get_api_python

router = APIRouter(prefix="/coa", tags=["coa"])


def _build_passthrough_params(
    search: str | None,
    type: str | None,
    is_detail: str | None,
    max_level: int | None,
) -> dict[str, str | int]:
    params: dict[str, str | int] = {}
    if search:
        params["search"] = search
    if type:
        params["type"] = type
    if is_detail:
        params["is_detail"] = is_detail
    if max_level is not None:
        params["max_level"] = max_level
    return params


@router.get("/accounts")
async def accounts(
    request: Request,
    search: str | None = Query(default=None),
    type: str | None = Query(default=None),
    is_detail: str | None = Query(default=None),
    max_level: int | None = Query(default=None, ge=0, le=10),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params = _build_passthrough_params(search, type, is_detail, max_level)
    params["page"] = page
    params["page_size"] = page_size
    downstream = await get_api_python("/api/v1/coa/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/accounts.xlsx")
async def accounts_xlsx(
    request: Request,
    search: str | None = Query(default=None),
    type: str | None = Query(default=None),
    is_detail: str | None = Query(default=None),
    max_level: int | None = Query(default=None, ge=0, le=10),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params = _build_passthrough_params(search, type, is_detail, max_level)
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

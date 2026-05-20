from __future__ import annotations

from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401
from app.services.proxy import get_api_python

router = APIRouter(prefix="/coa", tags=["coa"])


@router.get("/accounts")
async def accounts(
    request: Request,
    search: str | None = Query(default=None),
    limit: int = Query(default=1000, ge=1, le=5000),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params: dict[str, str | int] = {"limit": limit}
    if search:
        params["search"] = search
    downstream = await get_api_python("/api/v1/coa/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

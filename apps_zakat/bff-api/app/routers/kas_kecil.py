from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix="/kas-kecil", tags=["kas-kecil"])

_MENU = "keuangan.kas_kecil"


@router.get("/accounts")
async def accounts(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params: dict[str, str | int] = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search

    downstream = await get_api_python("/api/kas-kecil/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/accounts/{account_no}")
async def get_account(
    request: Request,
    account_no: str,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python(f"/api/kas-kecil/accounts/{account_no}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/accounts", status_code=201)
async def create_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    body = await request.json()
    downstream = await post_api_python("/api/kas-kecil/accounts", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/accounts/{account_no}")
async def update_account(
    request: Request,
    account_no: str,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    body = await request.json()
    downstream = await post_api_python(
        f"/api/kas-kecil/accounts/{account_no}",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete("/accounts/{account_no}")
async def delete_account(
    request: Request,
    account_no: str,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await post_api_python(
        f"/api/kas-kecil/accounts/{account_no}",
        json_body={},
        method="DELETE",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/lookup/branches")
async def lookup_branches(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python("/api/kas-kecil/lookup/branches")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/lookup/currencies")
async def lookup_currencies(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python("/api/kas-kecil/lookup/currencies")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/lookup/gl_accounts")
async def lookup_gl_accounts(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    search: str | None = Query(default=None),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params: dict[str, str] = {}
    if search:
        params["search"] = search

    downstream = await get_api_python("/api/kas-kecil/lookup/gl_accounts", params=params or None)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

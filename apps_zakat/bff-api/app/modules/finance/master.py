from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse, Response
from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python
from app.services.proxy import get_api_python, post_api_python

coa_router = APIRouter(prefix="/api/finance/master/coa", tags=["coa"])


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


@coa_router.get("/accounts")
async def accounts(
    request: Request,
    _: str = Depends(require_menu("finance.coa")),
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
    downstream = await get_api_python("/api/finance/master/coa/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@coa_router.get("/accounts.xlsx")
async def accounts_xlsx(
    request: Request,
    _: str = Depends(require_menu("finance.coa")),
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
        "/api/coa/accounts.xlsx", params=params or None
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

bank_router = APIRouter(prefix="/api/finance/master/bank", tags=["bank"])


@bank_router.get("/accounts")
async def accounts(
    request: Request,
    _: str = Depends(require_menu("finance.bank")),
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

    downstream = await get_api_python("/api/finance/master/bank/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@bank_router.get("/accounts/{account_no}")
async def get_account(
    request: Request,
    account_no: str,
    _: str = Depends(require_menu("finance.bank")),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python(f"/api/bank/accounts/{account_no}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@bank_router.get("/lookup/banks")
async def lookup_banks(
    request: Request,
    _: str = Depends(require_menu("finance.bank")),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python("/api/finance/master/bank/lookup/banks")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@bank_router.get("/lookup/branches")
async def lookup_branches(
    request: Request,
    _: str = Depends(require_menu("finance.bank")),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python("/api/finance/master/bank/lookup/branches")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@bank_router.get("/lookup/currencies")
async def lookup_currencies(
    request: Request,
    _: str = Depends(require_menu("finance.bank")),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python("/api/finance/master/bank/lookup/currencies")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@bank_router.get("/lookup/gl_accounts")
async def lookup_gl_accounts(
    request: Request,
    _: str = Depends(require_menu("finance.bank")),
    search: str | None = Query(default=None),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params: dict[str, str] = {}
    if search:
        params["search"] = search

    downstream = await get_api_python("/api/finance/master/bank/lookup/gl_accounts", params=params or None)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@bank_router.get("/lookup/products")
async def lookup_products(
    request: Request,
    _: str = Depends(require_menu("finance.bank")),
    search: str | None = Query(default=None),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    params: dict[str, str] = {}
    if search:
        params["search"] = search

    downstream = await get_api_python("/api/finance/master/bank/lookup/products", params=params or None)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

petty_cash_router = APIRouter(prefix="/api/finance/master/petty-cash", tags=["petty-cash"])

_MENU = "finance.petty_cash"


@petty_cash_router.get("/accounts")
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

    downstream = await get_api_python("/api/finance/master/petty-cash/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@petty_cash_router.get("/accounts/{account_no}")
async def get_account(
    request: Request,
    account_no: str,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python(f"/api/petty-cash/accounts/{account_no}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@petty_cash_router.post("/accounts", status_code=201)
async def create_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    body = await request.json()
    downstream = await post_api_python("/api/petty-cash/accounts", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@petty_cash_router.put("/accounts/{account_no}")
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
        f"/api/petty-cash/accounts/{account_no}",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@petty_cash_router.delete("/accounts/{account_no}")
async def delete_account(
    request: Request,
    account_no: str,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await post_api_python(
        f"/api/petty-cash/accounts/{account_no}",
        json_body={},
        method="DELETE",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@petty_cash_router.get("/lookup/branches")
async def lookup_branches(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python("/api/finance/master/petty-cash/lookup/branches")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@petty_cash_router.get("/lookup/currencies")
async def lookup_currencies(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    downstream = await get_api_python("/api/finance/master/petty-cash/lookup/currencies")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@petty_cash_router.get("/lookup/gl_accounts")
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

    downstream = await get_api_python("/api/finance/master/petty-cash/lookup/gl_accounts", params=params or None)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

parameter_router = APIRouter(prefix="/api/finance/master/parameter", tags=["parameter"])


@parameter_router.get("/budget-owner")
async def list_owners(
    request:  Request,
    _:        str       = Depends(require_menu("finance.parameter.budget_owner")),
    page:     int       = Query(default=1,    ge=1),
    limit:    int       = Query(default=25,   ge=1, le=100),
    q:        str | None = Query(default=None),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    params: dict = {"page": page, "limit": limit}
    if q:
        params["q"] = q
    downstream = await get_api_python("/api/finance/master/parameter/budget-owner", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@parameter_router.get("/budget-owner/lookup")
async def lookup_owners(
    request: Request,
    _:       str       = Depends(require_menu("finance.parameter.budget_owner")),
    q:       str | None = Query(default=None),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    params: dict = {}
    if q:
        params["q"] = q
    downstream = await get_api_python("/api/finance/master/parameter/budget-owner/lookup", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@parameter_router.get("/budget-owner/{owner_id}")
async def get_owner(
    request:  Request,
    owner_id:  int,
    _:        str = Depends(require_menu("finance.parameter.budget_owner")),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    downstream = await get_api_python(f"/api/parameter/budget-owner/{owner_id}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
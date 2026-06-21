from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, Response
from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python
from fastapi import APIRouter, Body, Depends, Query, Request
from fastapi.responses import JSONResponse
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
    downstream = await get_api_python("/api/coa/accounts", params=params)
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

parameter_router = APIRouter(prefix="/api/finance/master/parameter", tags=["parameter"])


@parameter_router.get("/pemilik-anggaran")
async def list_owners(
    request: Request,
    _:       str       = Depends(require_menu("finance.parameter.budget_owner")),
    page:    int       = Query(default=1,    ge=1),
    limit:   int       = Query(default=25,   ge=1, le=100),
    q:       str | None = Query(default=None),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    params: dict = {"page": page, "limit": limit}
    if q:
        params["q"] = q
    downstream = await get_api_python("/api/parameter/pemilik-anggaran", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@parameter_router.get("/pemilik-anggaran/lookup")
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
    downstream = await get_api_python("/api/parameter/pemilik-anggaran/lookup", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@parameter_router.get("/pemilik-anggaran/{ownerid}")
async def get_owner(
    request: Request,
    ownerid: int,
    _:       str = Depends(require_menu("finance.parameter.budget_owner")),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    downstream = await get_api_python(f"/api/parameter/pemilik-anggaran/{ownerid}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@parameter_router.post("/pemilik-anggaran")
async def create_owner(
    request: Request,
    _:       str  = Depends(require_menu("finance.parameter.budget_owner.create")),
    payload: dict = Body(...),
):
    user_id, err = await current_user_id_or_401(request)
    if err:
        return err
    downstream = await post_api_python("/api/parameter/pemilik-anggaran", json_body=payload)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@parameter_router.put("/pemilik-anggaran/{ownerid}")
async def update_owner(
    request: Request,
    ownerid: int,
    _:       str  = Depends(require_menu("finance.parameter.budget_owner.edit")),
    payload: dict = Body(...),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    downstream = await post_api_python(
        f"/api/parameter/pemilik-anggaran/{ownerid}", json_body=payload, method="PUT"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@parameter_router.delete("/pemilik-anggaran/{ownerid}")
async def delete_owner(
    request: Request,
    ownerid: int,
    _:       str = Depends(require_menu("finance.parameter.budget_owner.delete")),
):
    _, err = await current_user_id_or_401(request)
    if err:
        return err
    downstream = await post_api_python(
        f"/api/parameter/pemilik-anggaran/{ownerid}", json_body={}, method="DELETE"
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

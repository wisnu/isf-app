from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

# ── Corporate ─────────────────────────────────────────────────────────────────

corporate_router = APIRouter(
    prefix="/api/distribution/mustahiq/corporate",
    tags=["mustahiq-corporate"],
)
_CORP_MENU = "distribution.mustahiq.corporate"


@corporate_router.get("")
async def list_corporate(
    request: Request,
    _: str = Depends(require_menu(_CORP_MENU)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    downstream = await get_api_python("/distribution/mustahiq/corporate", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.get("/{mustahiq_id}")
async def get_corporate(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f"/distribution/mustahiq/corporate/{mustahiq_id}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.post("", status_code=201)
async def create_corporate(
    request: Request,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python("/distribution/mustahiq/corporate", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.put("/{mustahiq_id}")
async def update_corporate(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f"/distribution/mustahiq/corporate/{mustahiq_id}",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.delete("/{mustahiq_id}")
async def delete_corporate(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f"/distribution/mustahiq/corporate/{mustahiq_id}",
        json_body={},
        method="DELETE",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@corporate_router.put("/{mustahiq_id}/status")
async def toggle_corporate_status(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f"/distribution/mustahiq/corporate/{mustahiq_id}/status",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Personal ──────────────────────────────────────────────────────────────────

personal_router = APIRouter(
    prefix="/api/distribution/mustahiq/personal",
    tags=["mustahiq-personal"],
)
_PERS_MENU = "distribution.mustahiq.personal"


@personal_router.get("")
async def list_personal(
    request: Request,
    _: str = Depends(require_menu(_PERS_MENU)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {"page": page, "page_size": page_size}
    if search:
        params["search"] = search
    downstream = await get_api_python("/distribution/mustahiq/personal", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@personal_router.get("/{mustahiq_id}")
async def get_personal(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_PERS_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f"/distribution/mustahiq/personal/{mustahiq_id}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@personal_router.post("", status_code=201)
async def create_personal(
    request: Request,
    _: str = Depends(require_menu(_PERS_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python("/distribution/mustahiq/personal", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@personal_router.put("/{mustahiq_id}")
async def update_personal(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_PERS_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f"/distribution/mustahiq/personal/{mustahiq_id}",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@personal_router.delete("/{mustahiq_id}")
async def delete_personal(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_PERS_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f"/distribution/mustahiq/personal/{mustahiq_id}",
        json_body={},
        method="DELETE",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@personal_router.put("/{mustahiq_id}/status")
async def toggle_personal_status(
    request: Request,
    mustahiq_id: int,
    _: str = Depends(require_menu(_PERS_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f"/distribution/mustahiq/personal/{mustahiq_id}/status",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Lookup (shared) ───────────────────────────────────────────────────────────

mustahiq_lookup_router = APIRouter(
    prefix="/api/distribution/mustahiq",
    tags=["mustahiq-lookup"],
)


@mustahiq_lookup_router.get("/lookup/provinces")
async def lookup_provinces(
    request: Request,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python("/distribution/mustahiq/lookup/provinces")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@mustahiq_lookup_router.get("/lookup/banks")
async def lookup_banks(
    request: Request,
    _: str = Depends(require_menu(_CORP_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python("/distribution/mustahiq/lookup/banks")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

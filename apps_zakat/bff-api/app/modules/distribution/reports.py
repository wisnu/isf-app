from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_report_api, stream_report_api
from app.shared.response import err

router = APIRouter(prefix="/api/distribution/report", tags=["distribution-report"])

_PROPOSAL_MENU          = "distribution.report.proposal-incoming"
_MUSTAHIQ_LIST_MENU     = "distribution.report.mustahiq-list"
_REAL_REGULAR_MENU      = "distribution.report.realization-regular"
_REAL_NON_REGULAR_MENU  = "distribution.report.realization-non-regular"
_REAL_RECEIVABLE_MENU   = "distribution.report.realization-receivable"
_REAL_RETURN_MENU       = "distribution.report.realization-return"
_REAL_BY_MUSTAHIQ_MENU  = "distribution.report.realization-by-mustahiq"
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _resolve_branch(request: Request, branch: str | None) -> tuple[str | None, JSONResponse | None]:
    access = request.session.get("branch_access", "single")
    primary = request.session.get("primary_branch")
    bp = (branch or "").strip()
    is_all_req = bp == "" or bp.upper() == "ALL"

    if access == "all":
        return (None if is_all_req else bp), None

    if not primary:
        return None, JSONResponse(
            status_code=403, content=err("NO_BRANCH", "User tidak punya cabang default")
        )
    if bp == "" or bp == primary:
        return primary, None
    return None, JSONResponse(
        status_code=403,
        content=err("BRANCH_FORBIDDEN", "Anda hanya boleh mengakses cabang sendiri"),
    )


# ── Laporan Proposal Masuk ───────────────────────────────────────────────────

@router.get("/proposal-incoming")
async def proposal_incoming(
    request: Request,
    _: str = Depends(require_menu(_PROPOSAL_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    mustahiq_id: int | None = Query(default=None),
    product_group_id: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    params: dict = {
        "date_from": date_from, "date_to": date_to,
        "page": page, "page_size": page_size,
    }
    if mustahiq_id:
        params["mustahiq_id"] = mustahiq_id
    if product_group_id:
        params["product_group_id"] = product_group_id
    downstream = await get_report_api("/api/distribution/report/proposal-incoming", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/proposal-incoming/export.xlsx")
async def proposal_incoming_export(
    request: Request,
    _: str = Depends(require_menu(_PROPOSAL_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    mustahiq_id: int | None = Query(default=None),
    product_group_id: int | None = Query(default=None),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    params: dict = {"date_from": date_from, "date_to": date_to}
    if mustahiq_id:
        params["mustahiq_id"] = mustahiq_id
    if product_group_id:
        params["product_group_id"] = product_group_id
    downstream = await stream_report_api(
        "/api/distribution/report/proposal-incoming/export.xlsx", params=params
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": downstream.headers.get(
            "content-disposition", 'attachment; filename="laporan-proposal-masuk.xlsx"'
        )},
    )


# ── Laporan Daftar Mustahiq ──────────────────────────────────────────────────

@router.get("/mustahiq-list")
async def mustahiq_list(
    request: Request,
    _: str = Depends(require_menu(_MUSTAHIQ_LIST_MENU)),
    mustahiq_type: str | None = Query(default=None),
    product_id: int | None = Query(default=None),
    date_start_from: str | None = Query(default=None),
    date_start_to: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    params: dict = {"page": page, "page_size": page_size}
    if mustahiq_type:
        params["mustahiq_type"] = mustahiq_type
    if product_id:
        params["product_id"] = product_id
    if date_start_from:
        params["date_start_from"] = date_start_from
    if date_start_to:
        params["date_start_to"] = date_start_to
    downstream = await get_report_api("/api/distribution/report/mustahiq-list", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/mustahiq-list/export.xlsx")
async def mustahiq_list_export(
    request: Request,
    _: str = Depends(require_menu(_MUSTAHIQ_LIST_MENU)),
    mustahiq_type: str | None = Query(default=None),
    product_id: int | None = Query(default=None),
    date_start_from: str | None = Query(default=None),
    date_start_to: str | None = Query(default=None),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    params: dict = {}
    if mustahiq_type:
        params["mustahiq_type"] = mustahiq_type
    if product_id:
        params["product_id"] = product_id
    if date_start_from:
        params["date_start_from"] = date_start_from
    if date_start_to:
        params["date_start_to"] = date_start_to
    downstream = await stream_report_api(
        "/api/distribution/report/mustahiq-list/export.xlsx", params=params
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": downstream.headers.get(
            "content-disposition", 'attachment; filename="laporan-daftar-mustahiq.xlsx"'
        )},
    )


# ── Laporan Program Penyaluran Rutin ─────────────────────────────────────────

@router.get("/realization-regular")
async def realization_regular(
    request: Request,
    _: str = Depends(require_menu(_REAL_REGULAR_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    params = {"date_from": date_from, "date_to": date_to, "page": page, "page_size": page_size}
    downstream = await get_report_api("/api/distribution/report/realization-regular", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/realization-regular/export.xlsx")
async def realization_regular_export(
    request: Request,
    _: str = Depends(require_menu(_REAL_REGULAR_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/distribution/report/realization-regular/export.xlsx",
        params={"date_from": date_from, "date_to": date_to},
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": downstream.headers.get(
            "content-disposition", 'attachment; filename="laporan-realisasi-rutin.xlsx"'
        )},
    )


# ── Laporan Program Penyaluran Non Rutin ─────────────────────────────────────

@router.get("/realization-non-regular")
async def realization_non_regular(
    request: Request,
    _: str = Depends(require_menu(_REAL_NON_REGULAR_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    amount_min: float = Query(default=0.0),
    amount_max: float = Query(default=3000000.0),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    resolved, branch_error = _resolve_branch(request, branch)
    if branch_error is not None:
        return branch_error
    params: dict = {
        "date_from": date_from, "date_to": date_to,
        "amount_min": amount_min, "amount_max": amount_max,
        "page": page, "page_size": page_size,
    }
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api("/api/distribution/report/realization-non-regular", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/realization-non-regular/export.xlsx")
async def realization_non_regular_export(
    request: Request,
    _: str = Depends(require_menu(_REAL_NON_REGULAR_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    amount_min: float = Query(default=0.0),
    amount_max: float = Query(default=3000000.0),
    branch: str | None = Query(default=None),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    resolved, branch_error = _resolve_branch(request, branch)
    if branch_error is not None:
        return branch_error
    params: dict = {"date_from": date_from, "date_to": date_to, "amount_min": amount_min, "amount_max": amount_max}
    if resolved:
        params["branch"] = resolved
    downstream = await stream_report_api(
        "/api/distribution/report/realization-non-regular/export.xlsx", params=params
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": downstream.headers.get(
            "content-disposition", 'attachment; filename="laporan-realisasi-non-rutin.xlsx"'
        )},
    )


# ── Laporan Piutang Realisasi Penyaluran ──────────────────────────────────────

@router.get("/realization-receivable")
async def realization_receivable(
    request: Request,
    _: str = Depends(require_menu(_REAL_RECEIVABLE_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    params = {"date_from": date_from, "date_to": date_to, "page": page, "page_size": page_size}
    downstream = await get_report_api("/api/distribution/report/realization-receivable", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/realization-receivable/export.xlsx")
async def realization_receivable_export(
    request: Request,
    _: str = Depends(require_menu(_REAL_RECEIVABLE_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/distribution/report/realization-receivable/export.xlsx",
        params={"date_from": date_from, "date_to": date_to},
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": downstream.headers.get(
            "content-disposition", 'attachment; filename="laporan-piutang-realisasi.xlsx"'
        )},
    )


# ── Laporan Pengembalian Realisasi ────────────────────────────────────────────

@router.get("/realization-return")
async def realization_return(
    request: Request,
    _: str = Depends(require_menu(_REAL_RETURN_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    params = {"date_from": date_from, "date_to": date_to, "page": page, "page_size": page_size}
    downstream = await get_report_api("/api/distribution/report/realization-return", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/realization-return/export.xlsx")
async def realization_return_export(
    request: Request,
    _: str = Depends(require_menu(_REAL_RETURN_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/distribution/report/realization-return/export.xlsx",
        params={"date_from": date_from, "date_to": date_to},
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": downstream.headers.get(
            "content-disposition", 'attachment; filename="laporan-pengembalian-realisasi.xlsx"'
        )},
    )


# ── Laporan Penyaluran Per Mustahiq ──────────────────────────────────────────

@router.get("/realization-by-mustahiq")
async def realization_by_mustahiq(
    request: Request,
    _: str = Depends(require_menu(_REAL_BY_MUSTAHIQ_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    resolved, branch_error = _resolve_branch(request, branch)
    if branch_error is not None:
        return branch_error
    params: dict = {"date_from": date_from, "date_to": date_to, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api("/api/distribution/report/realization-by-mustahiq", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/realization-by-mustahiq/export.xlsx")
async def realization_by_mustahiq_export(
    request: Request,
    _: str = Depends(require_menu(_REAL_BY_MUSTAHIQ_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    branch: str | None = Query(default=None),
):
    _, error = await current_user_id_or_401(request)
    if error is not None:
        return error
    resolved, branch_error = _resolve_branch(request, branch)
    if branch_error is not None:
        return branch_error
    params: dict = {"date_from": date_from, "date_to": date_to}
    if resolved:
        params["branch"] = resolved
    downstream = await stream_report_api(
        "/api/distribution/report/realization-by-mustahiq/export.xlsx", params=params
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": downstream.headers.get(
            "content-disposition", 'attachment; filename="laporan-realisasi-per-mustahiq.xlsx"'
        )},
    )

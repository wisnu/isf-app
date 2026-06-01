from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_report_api, stream_report_api
from app.shared.response import err

router = APIRouter(prefix="/report", tags=["report"])

_JOURNAL_MENU = "keuangan.report.journal_daily"
_GT_MENU = "keuangan.report.general_transaction"
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@router.get("/ping")
async def ping(request: Request):
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api("/api/report/ping")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


async def _branches_for_session(request: Request):
    access = request.session.get("branch_access", "single")
    primary = request.session.get("primary_branch") or ""
    scope = "all" if access == "all" else primary
    return await get_report_api("/api/report/branches", params={"scope": scope})


def _resolve_branch(request: Request, branch: str | None) -> tuple[str | None, JSONResponse | None]:
    """Enforce scope cabang vs session.

    Return (branch, error):
      - branch=None berarti SEMUA cabang (hanya untuk user branch_access='all').
      - error != None → tolak (403).
    """
    access = request.session.get("branch_access", "single")
    primary = request.session.get("primary_branch")
    bp = (branch or "").strip()
    is_all_req = bp == "" or bp.upper() == "ALL"

    if access == "all":
        return (None if is_all_req else bp), None

    # single → terkunci ke cabang default
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


@router.get("/journal-daily")
async def journal_daily(
    request: Request,
    _: str = Depends(require_menu(_JOURNAL_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params: dict = {"begin": begin, "end": end, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api("/api/report/journal-daily", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/journal-daily/export.xlsx")
async def journal_daily_export(
    request: Request,
    _: str = Depends(require_menu(_JOURNAL_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params: dict = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    downstream = await stream_report_api("/api/report/journal-daily/export.xlsx", params=params)
    if downstream.status_code != 200:
        # error JSON dari report-api (mis. 422 REPORT_TOO_LARGE / 503) — teruskan apa adanya
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="jurnal-harian.xlsx"'
            )
        },
    )


@router.get("/journal-daily/branches")
async def journal_daily_branches(
    request: Request,
    _: str = Depends(require_menu(_JOURNAL_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── List Transaksi Umum (GT) ─────────────────────────────────────────────────

@router.get("/general-transaction/branches")
async def general_transaction_branches(
    request: Request,
    _: str = Depends(require_menu(_GT_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

@router.get("/general-transaction")
async def general_transaction(
    request: Request,
    _: str = Depends(require_menu(_GT_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params: dict = {"begin": begin, "end": end, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api("/api/report/general-transaction", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/general-transaction/export.xlsx")
async def general_transaction_export(
    request: Request,
    _: str = Depends(require_menu(_GT_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params: dict = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    downstream = await stream_report_api("/api/report/general-transaction/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="generaltransaction.xlsx"'
            )
        },
    )

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_report_api, stream_report_api
from app.shared.response import err

router = APIRouter(prefix="/report", tags=["report"])

_JOURNAL_MENU = "keuangan.report.journal_daily"
_GT_MENU = "keuangan.report.general_transaction"
_CASH_MENU = "keuangan.report.cash_daily"
_CASH_SUMMARY_MENU = "keuangan.report.cash_summary"
_CASH_MONTHLY_MENU = "keuangan.report.cash_monthly"
_TRIAL_BALANCE_MENU = "keuangan.report.trial_balance"
_NERACA_MENU = "keuangan.report.neraca"
_ARUSKAS_MENU = "keuangan.report.cash_flow"
_GL_MENU = "keuangan.report.general_ledger"
_PD_MENU = "keuangan.report.fund_changes"
_PDD_MENU = "keuangan.report.fund_changes_detail"
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


# ── Transaksi Kas/Bank Harian (fDailyCash) ───────────────────────────────────

@router.get("/cash-mutation/branches")
async def cash_branches(
    request: Request,
    _: str = Depends(require_menu(_CASH_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-accounts")
async def cash_accounts(
    request: Request,
    _: str = Depends(require_menu(_CASH_MENU)),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    if not resolved:
        # Laporan kas butuh cabang konkret (bukan "semua").
        return JSONResponse(
            status_code=400, content=err("BRANCH_REQUIRED", "Pilih satu cabang dulu")
        )
    downstream = await get_report_api("/api/report/cash-accounts", params={"branch": resolved})
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-mutation")
async def cash_mutation(
    request: Request,
    _: str = Depends(require_menu(_CASH_MENU)),
    account: str = Query(...),
    begin: str = Query(...),
    end: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    params = {"account": account, "begin": begin, "end": end, "page": page, "page_size": page_size}
    downstream = await get_report_api("/api/report/cash-mutation", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-mutation/export.xlsx")
async def cash_mutation_export(
    request: Request,
    _: str = Depends(require_menu(_CASH_MENU)),
    account: str = Query(...),
    begin: str = Query(...),
    end: str = Query(...),
):
    params = {"account": account, "begin": begin, "end": end}
    downstream = await stream_report_api("/api/report/cash-mutation/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="cashdaily.xlsx"'
            )
        },
    )


# ── Rekapitulasi Transaksi Kas/Bank (fSummaryCash) ───────────────────────────

@router.get("/cash-summary/branches")
async def cash_summary_branches(
    request: Request,
    _: str = Depends(require_menu(_CASH_SUMMARY_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-summary")
async def cash_summary(
    request: Request,
    _: str = Depends(require_menu(_CASH_SUMMARY_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    if not resolved:
        return JSONResponse(status_code=400, content=err("BRANCH_REQUIRED", "Pilih satu cabang dulu"))
    downstream = await get_report_api(
        "/api/report/cash-summary", params={"branch": resolved, "begin": begin, "end": end}
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-summary/export.xlsx")
async def cash_summary_export(
    request: Request,
    _: str = Depends(require_menu(_CASH_SUMMARY_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    if not resolved:
        return JSONResponse(status_code=400, content=err("BRANCH_REQUIRED", "Pilih satu cabang dulu"))
    downstream = await stream_report_api(
        "/api/report/cash-summary/export.xlsx", params={"branch": resolved, "begin": begin, "end": end}
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="cashsummary.xlsx"'
            )
        },
    )


# ── Monitoring Saldo Kas/Bank Bulanan (fSummaryCashMonthly) ──────────────────

@router.get("/cash-monthly/branches")
async def cash_monthly_branches(
    request: Request,
    _: str = Depends(require_menu(_CASH_MONTHLY_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-monthly")
async def cash_monthly(
    request: Request,
    _: str = Depends(require_menu(_CASH_MONTHLY_MENU)),
    year: int = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    if not resolved:
        return JSONResponse(status_code=400, content=err("BRANCH_REQUIRED", "Pilih satu cabang dulu"))
    downstream = await get_report_api(
        "/api/report/cash-monthly", params={"branch": resolved, "year": year}
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-monthly/export.xlsx")
async def cash_monthly_export(
    request: Request,
    _: str = Depends(require_menu(_CASH_MONTHLY_MENU)),
    year: int = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    if not resolved:
        return JSONResponse(status_code=400, content=err("BRANCH_REQUIRED", "Pilih satu cabang dulu"))
    downstream = await stream_report_api(
        "/api/report/cash-monthly/export.xlsx", params={"branch": resolved, "year": year}
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="cashmonthly.xlsx"'
            )
        },
    )


# ── Trial Balance ────────────────────────────────────────────────────────────
# branch None (resolved) → konsolidasi (hanya user branch_access='all').


def _tb_params(resolved: str | None, begin: str, end: str) -> dict:
    params: dict = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    return params


@router.get("/trial-balance/branches")
async def trial_balance_branches(
    request: Request,
    _: str = Depends(require_menu(_TRIAL_BALANCE_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/trial-balance")
async def trial_balance(
    request: Request,
    _: str = Depends(require_menu(_TRIAL_BALANCE_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await get_report_api(
        "/api/report/trial-balance", params=_tb_params(resolved, begin, end)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/trial-balance/export.xlsx")
async def trial_balance_export(
    request: Request,
    _: str = Depends(require_menu(_TRIAL_BALANCE_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/report/trial-balance/export.xlsx", params=_tb_params(resolved, begin, end)
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="trialbalance.xlsx"'
            )
        },
    )


# ── Neraca ───────────────────────────────────────────────────────────────────
# branch None (resolved) → konsolidasi (hanya user branch_access='all').


def _neraca_params(resolved: str | None, tanggal: str, jenisperiode: str, level: int) -> dict:
    params: dict = {"tanggal": tanggal, "jenisperiode": jenisperiode, "level": level}
    if resolved:
        params["branch"] = resolved
    return params


@router.get("/neraca/branches")
async def neraca_branches(
    request: Request,
    _: str = Depends(require_menu(_NERACA_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/neraca")
async def neraca(
    request: Request,
    _: str = Depends(require_menu(_NERACA_MENU)),
    tanggal: str = Query(...),
    jenisperiode: str = Query(default="T"),
    level: int = Query(default=0),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await get_report_api(
        "/api/report/neraca", params=_neraca_params(resolved, tanggal, jenisperiode, level)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/neraca/export.xlsx")
async def neraca_export(
    request: Request,
    _: str = Depends(require_menu(_NERACA_MENU)),
    tanggal: str = Query(...),
    jenisperiode: str = Query(default="T"),
    level: int = Query(default=0),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/report/neraca/export.xlsx",
        params=_neraca_params(resolved, tanggal, jenisperiode, level),
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="neraca.xlsx"'
            )
        },
    )


# ── Arus Kas ─────────────────────────────────────────────────────────────────


def _ak_params(resolved: str | None, begin: str, end: str) -> dict:
    params: dict = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    return params


@router.get("/aruskas/branches")
async def aruskas_branches(
    request: Request,
    _: str = Depends(require_menu(_ARUSKAS_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/aruskas")
async def aruskas(
    request: Request,
    _: str = Depends(require_menu(_ARUSKAS_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await get_report_api("/api/report/aruskas", params=_ak_params(resolved, begin, end))
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/aruskas/export.xlsx")
async def aruskas_export(
    request: Request,
    _: str = Depends(require_menu(_ARUSKAS_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/report/aruskas/export.xlsx", params=_ak_params(resolved, begin, end)
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="aruskas.xlsx"'
            )
        },
    )


# ── Buku Besar (General Ledger) ──────────────────────────────────────────────


def _gl_params(resolved: str | None, begin: str, end: str, account: str | None) -> dict:
    params: dict = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    if account:
        params["account"] = account
    return params


@router.get("/general-ledger/branches")
async def general_ledger_branches(
    request: Request,
    _: str = Depends(require_menu(_GL_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/general-ledger/accounts")
async def general_ledger_accounts(
    request: Request,
    _: str = Depends(require_menu(_GL_MENU)),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"branch": resolved} if resolved else {}
    downstream = await get_report_api("/api/report/general-ledger/accounts", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/general-ledger")
async def general_ledger(
    request: Request,
    _: str = Depends(require_menu(_GL_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
    account: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await get_report_api(
        "/api/report/general-ledger", params=_gl_params(resolved, begin, end, account)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/general-ledger/export.xlsx")
async def general_ledger_export(
    request: Request,
    _: str = Depends(require_menu(_GL_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
    account: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/report/general-ledger/export.xlsx",
        params=_gl_params(resolved, begin, end, account),
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="bukubesar.xlsx"'
            )
        },
    )


# ── Perubahan Dana ───────────────────────────────────────────────────────────


@router.get("/perubahan-dana/branches")
async def perubahan_dana_branches(
    request: Request,
    _: str = Depends(require_menu(_PD_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/perubahan-dana")
async def perubahan_dana(
    request: Request,
    _: str = Depends(require_menu(_PD_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await get_report_api(
        "/api/report/perubahan-dana", params=_tb_params(resolved, begin, end)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/perubahan-dana/export.xlsx")
async def perubahan_dana_export(
    request: Request,
    _: str = Depends(require_menu(_PD_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/report/perubahan-dana/export.xlsx", params=_tb_params(resolved, begin, end)
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="perubahandana.xlsx"'
            )
        },
    )


# ── Perubahan Dana Detail ────────────────────────────────────────────────────


@router.get("/perubahan-dana-detail/branches")
async def perubahan_dana_detail_branches(
    request: Request,
    _: str = Depends(require_menu(_PDD_MENU)),
):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/perubahan-dana-detail")
async def perubahan_dana_detail(
    request: Request,
    _: str = Depends(require_menu(_PDD_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await get_report_api(
        "/api/report/perubahan-dana-detail", params=_tb_params(resolved, begin, end)
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/perubahan-dana-detail/export.xlsx")
async def perubahan_dana_detail_export(
    request: Request,
    _: str = Depends(require_menu(_PDD_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    downstream = await stream_report_api(
        "/api/report/perubahan-dana-detail/export.xlsx", params=_tb_params(resolved, begin, end)
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", 'attachment; filename="perubahandanadetail.xlsx"'
            )
        },
    )

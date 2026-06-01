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
_AMIL_IN_MENU = "keuangan.report.amil_in"
_AMIL_OUT_MENU = "keuangan.report.amil_out"
_DIST_MENU = "keuangan.report.distribution"
_COLL_MENU = "keuangan.report.collection"
_AR_EMP_MENU = "keuangan.report.ar_employee"
_AR_EXT_MENU = "keuangan.report.ar_external"
_CA_EMP_MENU = "keuangan.report.ca_employee"
_CA_LIST_MENU = "keuangan.report.ca_list"
_PROG_AR_MENU = "keuangan.report.program_ar"
_MEMO_MENU = "keuangan.report.project_memo"
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


# ── Penerimaan / Pengeluaran Amil ────────────────────────────────────────────


@router.get("/amil-cashin/branches")
async def amil_cashin_branches(request: Request, _: str = Depends(require_menu(_AMIL_IN_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/amil-cashin")
async def amil_cashin(
    request: Request, _: str = Depends(require_menu(_AMIL_IN_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api("/api/report/amil-cashin", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/amil-cashin/export.xlsx")
async def amil_cashin_export(
    request: Request, _: str = Depends(require_menu(_AMIL_IN_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    downstream = await stream_report_api("/api/report/amil-cashin/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(content=downstream.content, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": downstream.headers.get("content-disposition", 'attachment; filename="penerimaanamil.xlsx"')})


@router.get("/amil-cashout/branches")
async def amil_cashout_branches(request: Request, _: str = Depends(require_menu(_AMIL_OUT_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/amil-cashout")
async def amil_cashout(
    request: Request, _: str = Depends(require_menu(_AMIL_OUT_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api("/api/report/amil-cashout", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/amil-cashout/export.xlsx")
async def amil_cashout_export(
    request: Request, _: str = Depends(require_menu(_AMIL_OUT_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    downstream = await stream_report_api("/api/report/amil-cashout/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(content=downstream.content, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": downstream.headers.get("content-disposition", 'attachment; filename="pengeluaranamil.xlsx"')})


# ── Penyaluran Dana ──────────────────────────────────────────────────────────


@router.get("/distribution/branches")
async def distribution_branches(request: Request, _: str = Depends(require_menu(_DIST_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/distribution")
async def distribution(
    request: Request, _: str = Depends(require_menu(_DIST_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    fund: str | None = Query(default=None), page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    if fund:
        params["fund"] = fund
    downstream = await get_report_api("/api/report/distribution", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/distribution/export.xlsx")
async def distribution_export(
    request: Request, _: str = Depends(require_menu(_DIST_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), fund: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    if fund:
        params["fund"] = fund
    downstream = await stream_report_api("/api/report/distribution/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(content=downstream.content, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": downstream.headers.get("content-disposition", 'attachment; filename="penyalurandana.xlsx"')})


# ── Penghimpunan Dana ────────────────────────────────────────────────────────


@router.get("/collection/branches")
async def collection_branches(request: Request, _: str = Depends(require_menu(_COLL_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/collection")
async def collection(
    request: Request, _: str = Depends(require_menu(_COLL_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    fund: str | None = Query(default=None), page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    if fund:
        params["fund"] = fund
    downstream = await get_report_api("/api/report/collection", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/collection/rekap")
async def collection_rekap(
    request: Request, _: str = Depends(require_menu(_COLL_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api("/api/report/collection/rekap", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/collection/export.xlsx")
async def collection_export(
    request: Request, _: str = Depends(require_menu(_COLL_MENU)),
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), fund: str | None = Query(default=None),
):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    if fund:
        params["fund"] = fund
    downstream = await stream_report_api("/api/report/collection/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(content=downstream.content, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": downstream.headers.get("content-disposition", 'attachment; filename="penghimpunandana.xlsx"')})


# ── Ringkasan Piutang / Uang Muka ────────────────────────────────────────────


async def _ar_proxy(request, menu, ep, begin, end, branch):
    _ = menu  # gating already applied via Depends
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    downstream = await get_report_api(f"/api/report/{ep}", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


async def _ar_proxy_export(request, ep, begin, end, branch, fallback):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    downstream = await stream_report_api(f"/api/report/{ep}/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(content=downstream.content, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": downstream.headers.get("content-disposition", f'attachment; filename="{fallback}"')})


@router.get("/employee-ar/branches")
async def employee_ar_branches(request: Request, _: str = Depends(require_menu(_AR_EMP_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/employee-ar")
async def employee_ar(request: Request, _: str = Depends(require_menu(_AR_EMP_MENU)),
                      begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy(request, _AR_EMP_MENU, "employee-ar", begin, end, branch)


@router.get("/employee-ar/export.xlsx")
async def employee_ar_export(request: Request, _: str = Depends(require_menu(_AR_EMP_MENU)),
                             begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy_export(request, "employee-ar", begin, end, branch, "piutangkaryawan.xlsx")


@router.get("/external-ar/branches")
async def external_ar_branches(request: Request, _: str = Depends(require_menu(_AR_EXT_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/external-ar")
async def external_ar(request: Request, _: str = Depends(require_menu(_AR_EXT_MENU)),
                      begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy(request, _AR_EXT_MENU, "external-ar", begin, end, branch)


@router.get("/external-ar/export.xlsx")
async def external_ar_export(request: Request, _: str = Depends(require_menu(_AR_EXT_MENU)),
                             begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy_export(request, "external-ar", begin, end, branch, "piutangnonkaryawan.xlsx")


@router.get("/cash-advance/branches")
async def cash_advance_branches(request: Request, _: str = Depends(require_menu(_CA_EMP_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cash-advance")
async def cash_advance(request: Request, _: str = Depends(require_menu(_CA_EMP_MENU)),
                       begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy(request, _CA_EMP_MENU, "cash-advance", begin, end, branch)


@router.get("/cash-advance/export.xlsx")
async def cash_advance_export(request: Request, _: str = Depends(require_menu(_CA_EMP_MENU)),
                              begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy_export(request, "cash-advance", begin, end, branch, "rekapuangmuka.xlsx")


# ── Grup C: List Uang Muka / Piutang Realisasi / Realisasi Memo ──────────────


@router.get("/cashadvance-list/branches")
async def cashadvance_list_branches(request: Request, _: str = Depends(require_menu(_CA_LIST_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cashadvance-list")
async def cashadvance_list(request: Request, _: str = Depends(require_menu(_CA_LIST_MENU)),
                           begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
                           lpj: str | None = Query(default=None), page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end, "page": page, "page_size": page_size}
    if resolved:
        params["branch"] = resolved
    if lpj:
        params["lpj"] = lpj
    downstream = await get_report_api("/api/report/cashadvance-list", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/cashadvance-list/export.xlsx")
async def cashadvance_list_export(request: Request, _: str = Depends(require_menu(_CA_LIST_MENU)),
                                  begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), lpj: str | None = Query(default=None)):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    if lpj:
        params["lpj"] = lpj
    downstream = await stream_report_api("/api/report/cashadvance-list/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(content=downstream.content, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": downstream.headers.get("content-disposition", 'attachment; filename="listuangmuka.xlsx"')})


@router.get("/program-realization/branches")
async def program_realization_branches(request: Request, _: str = Depends(require_menu(_PROG_AR_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/program-realization")
async def program_realization(request: Request, _: str = Depends(require_menu(_PROG_AR_MENU)),
                              begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy(request, _PROG_AR_MENU, "program-realization", begin, end, branch)


@router.get("/program-realization/export.xlsx")
async def program_realization_export(request: Request, _: str = Depends(require_menu(_PROG_AR_MENU)),
                                     begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_proxy_export(request, "program-realization", begin, end, branch, "piutangrealisasi.xlsx")


@router.get("/realization-memo/branches")
async def realization_memo_branches(request: Request, _: str = Depends(require_menu(_MEMO_MENU))):
    downstream = await _branches_for_session(request)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/realization-memo")
async def realization_memo(request: Request, _: str = Depends(require_menu(_MEMO_MENU)),
                           begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), q: str | None = Query(default=None)):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    if q:
        params["q"] = q
    downstream = await get_report_api("/api/report/realization-memo", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/realization-memo/export.xlsx")
async def realization_memo_export(request: Request, _: str = Depends(require_menu(_MEMO_MENU)),
                                  begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), q: str | None = Query(default=None)):
    resolved, error = _resolve_branch(request, branch)
    if error is not None:
        return error
    params = {"begin": begin, "end": end}
    if resolved:
        params["branch"] = resolved
    if q:
        params["q"] = q
    downstream = await stream_report_api("/api/report/realization-memo/export.xlsx", params=params)
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(content=downstream.content, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": downstream.headers.get("content-disposition", 'attachment; filename="realisasimemo.xlsx"')})

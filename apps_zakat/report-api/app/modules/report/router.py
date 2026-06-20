from datetime import date as _date, datetime

from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse

from app.modules.report.export import (
    build_cash_flow_xlsx,
    build_amil_cash_xlsx,
    build_distribution_xlsx,
    build_collection_xlsx,
    build_ar_summary_xlsx,
    build_cashadvance_xlsx,
    build_program_realization_xlsx,
    build_realization_memo_xlsx,
    build_upz_xlsx,
    build_cash_monthly_xlsx,
    build_general_ledger_xlsx,
    build_fund_changes_xlsx,
    build_fund_changes_detail_xlsx,
    build_cash_mutation_xlsx,
    build_cash_summary_xlsx,
    build_general_transaction_xlsx,
    build_journal_daily_xlsx,
    build_balance_sheet_xlsx,
    build_trial_balance_xlsx,
)
from app.modules.report.service import (
    CAP,
    ReportValidationError,
    cash_flow,
    amil_cash,
    amil_cash_count,
    amil_cash_rows,
    distribution_count,
    distribution_page,
    distribution_rows,
    collection_count,
    collection_page,
    collection_rows,
    collection_rekap,
    ar_summary,
    cashadvance_count,
    cashadvance_page,
    cashadvance_rows,
    program_realization,
    realization_memo,
    upz_trx,
    cash_account_label,
    cash_monthly,
    cash_mutation_export,
    cash_mutation_item_count,
    cash_mutation_page,
    cash_summary,
    dwh_health,
    general_transaction_item_count,
    general_transaction_page,
    general_transaction_rows,
    journal_daily_count,
    journal_daily_page,
    journal_daily_rows,
    general_ledger,
    list_branches,
    list_cash_accounts,
    list_detail_accounts,
    balance_sheet,
    fund_changes,
    fund_changes_detail,
    trial_balance,
)
from app.shared.response import err, ok

router = APIRouter(prefix="/report", tags=["report"])

_DB_UNAVAILABLE = err("DB_UNAVAILABLE", "Database tidak tersedia")
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


@router.get("/ping")
async def ping():
    return ok({"status": "ok", "dwh": await dwh_health()})


@router.get("/branches")
async def branches(scope: str = Query(default="all")):
    data = await list_branches(scope)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


def _dmy(iso: str) -> str:
    p = (iso or "").split("-")
    return f"{p[2]}-{p[1]}-{p[0]}" if len(p) == 3 else (iso or "")


def _period_label(begin: str, end: str) -> str:
    return _dmy(begin) if begin == end else f"{_dmy(begin)} s/d {_dmy(end)}"


@router.get("/journal-daily")
async def journal_daily(
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    data = await journal_daily_page(branch, begin, end, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/journal-daily/export.xlsx")
async def journal_daily_export(
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
    branch: str | None = Query(default=None),
):
    total = await journal_daily_count(branch, begin, end)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err(
                "REPORT_TOO_LARGE",
                f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal atau pilih satu cabang.",
            ),
        )

    rows = await journal_daily_rows(branch, begin, end)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)

    # Label cabang untuk header file
    if branch:
        binfo = await list_branches(branch)
        bname = binfo[0]["name"] if binfo else ""
        branch_label = f"{branch} - {bname}" if bname else branch
    else:
        branch_label = "Semua Cabang"

    xlsx = build_journal_daily_xlsx(rows, branch_label, _period_label(begin, end))
    filename = f"journaldaily-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


async def _branch_label(branch: str | None) -> str:
    if not branch:
        return "Semua Cabang"
    binfo = await list_branches(branch)
    bname = binfo[0]["name"] if binfo else ""
    return f"{branch} - {bname}" if bname else branch


@router.get("/general-transaction")
async def general_transaction(
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
):
    data = await general_transaction_page(branch, begin, end, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/general-transaction/export.xlsx")
async def general_transaction_export(
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
    branch: str | None = Query(default=None),
):
    total = await general_transaction_item_count(branch, begin, end)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err(
                "REPORT_TOO_LARGE",
                f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal atau pilih satu cabang.",
            ),
        )
    rows = await general_transaction_rows(branch, begin, end)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_general_transaction_xlsx(rows, await _branch_label(branch), _period_label(begin, end))
    filename = f"generaltransaction-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Transaksi Kas/Bank Harian (fDailyCash) ───────────────────────────────────

@router.get("/cash-accounts")
async def cash_accounts(branch: str = Query(...)):
    data = await list_cash_accounts(branch)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/cash-mutation")
async def cash_mutation(
    account: str = Query(...),
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    data = await cash_mutation_page(account, begin, end, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/cash-mutation/export.xlsx")
async def cash_mutation_xlsx(
    account: str = Query(...),
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
):
    total = await cash_mutation_item_count(account, begin, end)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err(
                "REPORT_TOO_LARGE",
                f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal.",
            ),
        )
    summary = await cash_mutation_export(account, begin, end)
    if summary is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    label = await cash_account_label(account)
    xlsx = build_cash_mutation_xlsx(summary, label, _period_label(begin, end))
    filename = f"cashdaily-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Rekapitulasi Transaksi Kas/Bank (fSummaryCash) ───────────────────────────

@router.get("/cash-summary")
async def cash_summary_ep(
    branch: str = Query(...),
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
):
    data = await cash_summary(branch, begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/cash-summary/export.xlsx")
async def cash_summary_xlsx(
    branch: str = Query(...),
    begin: str = Query(default_factory=lambda: _date.today().isoformat()),
    end: str = Query(default_factory=lambda: _date.today().isoformat()),
):
    data = await cash_summary(branch, begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    binfo = await list_branches(branch)
    label = f"{branch} - {binfo[0]['name']}" if binfo else branch
    xlsx = build_cash_summary_xlsx(data, label, _period_label(begin, end))
    filename = f"cashsummary-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Monitoring Saldo Kas/Bank Bulanan (fSummaryCashMonthly) ──────────────────

@router.get("/cash-monthly")
async def cash_monthly_ep(
    branch: str = Query(...),
    year: int = Query(default_factory=lambda: _date.today().year, ge=2000, le=2100),
):
    data = await cash_monthly(branch, year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/cash-monthly/export.xlsx")
async def cash_monthly_xlsx(
    branch: str = Query(...),
    year: int = Query(default_factory=lambda: _date.today().year, ge=2000, le=2100),
):
    data = await cash_monthly(branch, year)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    binfo = await list_branches(branch)
    label = f"{branch} - {binfo[0]['name']}" if binfo else branch
    xlsx = build_cash_monthly_xlsx(data, label, year)
    filename = f"cashmonthly-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Trial Balance ────────────────────────────────────────────────────────────
# branch kosong / 'ALL' → consolidated (semua cabang).


def _tb_branch(branch: str | None) -> str | None:
    return None if not branch or branch == "ALL" else branch


@router.get("/trial-balance")
async def trial_balance_ep(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    try:
        data = await trial_balance(_tb_branch(branch), begin, end, _date.today())
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/trial-balance/export.xlsx")
async def trial_balance_xlsx(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    try:
        data = await trial_balance(b, begin, end, _date.today())
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    if b:
        binfo = await list_branches(b)
        label = f"{b} - {binfo[0]['name']}" if binfo else b
    else:
        label = "KONSOLIDASI"
    xlsx = build_trial_balance_xlsx(data, label)
    filename = f"trialbalance-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Neraca ───────────────────────────────────────────────────────────────────


@router.get("/balance-sheet")
async def balance_sheet_ep(
    date: str = Query(...),
    period_type: str = Query(default="T"),
    level: int = Query(default=0),
    branch: str | None = Query(default=None),
):
    try:
        data = await balance_sheet(_tb_branch(branch), date, period_type, level, _date.today())
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/balance-sheet/export.xlsx")
async def balance_sheet_xlsx(
    date: str = Query(...),
    period_type: str = Query(default="T"),
    level: int = Query(default=0),
    branch: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    try:
        data = await balance_sheet(b, date, period_type, level, _date.today())
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    if b:
        binfo = await list_branches(b)
        label = f"{b} - {binfo[0]['name']}" if binfo else b
    else:
        label = "KONSOLIDASI"
    xlsx = build_balance_sheet_xlsx(data, label)
    filename = f"balance_sheet-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Arus Kas ─────────────────────────────────────────────────────────────────


@router.get("/cash-flow")
async def cash_flow_ep(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    try:
        data = await cash_flow(_tb_branch(branch), begin, end, _date.today())
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/cash-flow/export.xlsx")
async def cash_flow_xlsx(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    try:
        data = await cash_flow(b, begin, end, _date.today())
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    if b:
        binfo = await list_branches(b)
        label = f"{b} - {binfo[0]['name']}" if binfo else b
    else:
        label = "KONSOLIDASI"
    xlsx = build_cash_flow_xlsx(data, label)
    filename = f"cash_flow-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Buku Besar (General Ledger) ──────────────────────────────────────────────


@router.get("/general-ledger/accounts")
async def general_ledger_accounts(branch: str | None = Query(default=None)):
    data = await list_detail_accounts(_tb_branch(branch))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/general-ledger")
async def general_ledger_ep(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
    account: str | None = Query(default=None),
):
    try:
        data = await general_ledger(_tb_branch(branch), begin, end, account or None)
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/general-ledger/export.xlsx")
async def general_ledger_xlsx(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
    account: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    try:
        data = await general_ledger(b, begin, end, account or None)
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    if b:
        binfo = await list_branches(b)
        label = f"{b} - {binfo[0]['name']}" if binfo else b
    else:
        label = "KONSOLIDASI"
    xlsx = build_general_ledger_xlsx(data, label)
    filename = f"bukubesar-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Perubahan Dana ───────────────────────────────────────────────────────────


@router.get("/fund-changes")
async def fund_changes_ep(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    try:
        data = await fund_changes(_tb_branch(branch), begin, end)
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/fund-changes/export.xlsx")
async def fund_changes_xlsx(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    try:
        data = await fund_changes(b, begin, end)
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    if b:
        binfo = await list_branches(b)
        label = f"{b} - {binfo[0]['name']}" if binfo else b
    else:
        label = "KONSOLIDASI"
    xlsx = build_fund_changes_xlsx(data, label)
    filename = f"perubahandana-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Perubahan Dana Detail ────────────────────────────────────────────────────


@router.get("/fund-changes-detail")
async def fund_changes_detail_ep(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    try:
        data = await fund_changes_detail(_tb_branch(branch), begin, end)
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/fund-changes-detail/export.xlsx")
async def fund_changes_detail_xlsx(
    begin: str = Query(...),
    end: str = Query(...),
    branch: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    try:
        data = await fund_changes_detail(b, begin, end)
    except ReportValidationError as ex:
        return JSONResponse(status_code=422, content=err("INVALID_PARAM", str(ex)))
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    if b:
        binfo = await list_branches(b)
        label = f"{b} - {binfo[0]['name']}" if binfo else b
    else:
        label = "KONSOLIDASI"
    xlsx = build_fund_changes_detail_xlsx(data, label)
    filename = f"perubahandanadetail-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Penerimaan / Pengeluaran Amil ────────────────────────────────────────────

_AMIL_TITLE = {"in": "Laporan Penerimaan Amil", "out": "Laporan Pengeluaran Amil"}
_AMIL_FILE = {"in": "penerimaanamil", "out": "pengeluaranamil"}


async def _amil_list(kind, begin, end, branch, page, page_size):
    data = await amil_cash(kind, _tb_branch(branch), begin, end, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


async def _amil_export(kind, begin, end, branch):
    b = _tb_branch(branch)
    total = await amil_cash_count(kind, b, begin, end)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal."),
        )
    rows = await amil_cash_rows(kind, b, begin, end)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_amil_cash_xlsx(rows, await _branch_label(b), _period_label(begin, end), _AMIL_TITLE[kind], kind == "out")
    filename = f"{_AMIL_FILE[kind]}-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/amil-cashin")
async def amil_cashin(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
                      page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)):
    return await _amil_list("in", begin, end, branch, page, page_size)


@router.get("/amil-cashin/export.xlsx")
async def amil_cashin_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _amil_export("in", begin, end, branch)


@router.get("/amil-cashout")
async def amil_cashout(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
                       page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200)):
    return await _amil_list("out", begin, end, branch, page, page_size)


@router.get("/amil-cashout/export.xlsx")
async def amil_cashout_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _amil_export("out", begin, end, branch)


# ── Penyaluran Dana ──────────────────────────────────────────────────────────


@router.get("/distribution")
async def distribution(
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    fund: str | None = Query(default=None), page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    data = await distribution_page(_tb_branch(branch), begin, end, fund or None, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/distribution/export.xlsx")
async def distribution_export(
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    fund: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    total = await distribution_count(b, begin, end, fund or None)
    if total > CAP:
        return JSONResponse(status_code=422, content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit filter."))
    rows = await distribution_rows(b, begin, end, fund or None)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_distribution_xlsx(rows, await _branch_label(b), _period_label(begin, end))
    filename = f"penyalurandana-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


# ── Penghimpunan Dana ────────────────────────────────────────────────────────


@router.get("/collection")
async def collection(
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    fund: str | None = Query(default=None), page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200),
):
    data = await collection_page(_tb_branch(branch), begin, end, fund or None, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/collection/rekap")
async def collection_rekap_ep(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    data = await collection_rekap(_tb_branch(branch), begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/collection/export.xlsx")
async def collection_export(
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), fund: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    total = await collection_count(b, begin, end, fund or None)
    if total > CAP:
        return JSONResponse(status_code=422, content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit filter."))
    rows = await collection_rows(b, begin, end, fund or None)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    rekap = await collection_rekap(b, begin, end)
    xlsx = build_collection_xlsx(rows, rekap or {}, await _branch_label(b), _period_label(begin, end))
    filename = f"penghimpunandana-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


# ── Ringkasan Piutang / Uang Muka (AR Summary) ───────────────────────────────

_AR_PATH = {"E": "employee-ar", "D": "external-ar", "C": "cash-advance"}
_AR_FILE = {"E": "piutangkaryawan", "D": "piutangnonkaryawan", "C": "rekapuangmuka"}


async def _ar_data(ar_type, begin, end, branch):
    data = await ar_summary(ar_type, _tb_branch(branch), begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


async def _ar_export(ar_type, begin, end, branch):
    b = _tb_branch(branch)
    data = await ar_summary(ar_type, b, begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_ar_summary_xlsx(data, await _branch_label(b))
    filename = f"{_AR_FILE[ar_type]}-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/employee-ar")
async def employee_ar(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_data("E", begin, end, branch)


@router.get("/employee-ar/export.xlsx")
async def employee_ar_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_export("E", begin, end, branch)


@router.get("/external-ar")
async def external_ar(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_data("D", begin, end, branch)


@router.get("/external-ar/export.xlsx")
async def external_ar_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_export("D", begin, end, branch)


@router.get("/cash-advance")
async def cash_advance(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_data("C", begin, end, branch)


@router.get("/cash-advance/export.xlsx")
async def cash_advance_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    return await _ar_export("C", begin, end, branch)


# ── Grup C: List Uang Muka / Piutang Realisasi / Realisasi Memo ──────────────


@router.get("/cashadvance-list")
async def cashadvance_list(
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    employee: str | None = Query(default=None), lpj: str | None = Query(default=None),
    page: int = Query(default=1, ge=1), page_size: int = Query(default=50, ge=1, le=200),
):
    data = await cashadvance_page(_tb_branch(branch), begin, end, employee or None, lpj or None, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/cashadvance-list/export.xlsx")
async def cashadvance_list_export(
    begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None),
    employee: str | None = Query(default=None), lpj: str | None = Query(default=None),
):
    b = _tb_branch(branch)
    total = await cashadvance_count(b, begin, end, employee or None, lpj or None)
    if total > CAP:
        return JSONResponse(status_code=422, content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi {CAP:,}. Persempit filter."))
    rows = await cashadvance_rows(b, begin, end, employee or None, lpj or None)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_cashadvance_xlsx(rows, await _branch_label(b), _period_label(begin, end))
    filename = f"listuangmuka-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME, headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/program-realization")
async def program_realization_ep(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    data = await program_realization(_tb_branch(branch), begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/program-realization/export.xlsx")
async def program_realization_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    b = _tb_branch(branch)
    data = await program_realization(b, begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_program_realization_xlsx(data, await _branch_label(b))
    filename = f"piutangrealisasi-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME, headers={"Content-Disposition": f'attachment; filename="{filename}"'})


@router.get("/realization-memo")
async def realization_memo_ep(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), q: str | None = Query(default=None)):
    data = await realization_memo(_tb_branch(branch), begin, end, q or None)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/realization-memo/export.xlsx")
async def realization_memo_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None), q: str | None = Query(default=None)):
    b = _tb_branch(branch)
    data = await realization_memo(b, begin, end, q or None)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_realization_memo_xlsx(data, await _branch_label(b))
    filename = f"realisasimemo-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME, headers={"Content-Disposition": f'attachment; filename="{filename}"'})


# ── Grup D: List Transaksi UPZ ───────────────────────────────────────────────


@router.get("/upz")
async def upz(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    data = await upz_trx(_tb_branch(branch), begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/upz/export.xlsx")
async def upz_export(begin: str = Query(...), end: str = Query(...), branch: str | None = Query(default=None)):
    b = _tb_branch(branch)
    data = await upz_trx(b, begin, end)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_upz_xlsx(data, await _branch_label(b))
    filename = f"listupz-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(content=xlsx, media_type=_XLSX_MIME, headers={"Content-Disposition": f'attachment; filename="{filename}"'})

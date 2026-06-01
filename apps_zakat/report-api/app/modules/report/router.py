from datetime import date as _date, datetime

from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse

from app.modules.report.export import (
    build_cash_mutation_xlsx,
    build_cash_summary_xlsx,
    build_general_transaction_xlsx,
    build_journal_daily_xlsx,
)
from app.modules.report.service import (
    CAP,
    cash_account_label,
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
    list_branches,
    list_cash_accounts,
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


def _period_label(begin: str, end: str) -> str:
    return begin if begin == end else f"{begin} s/d {end}"


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

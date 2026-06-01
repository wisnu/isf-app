from datetime import date as _date, datetime

from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse

from app.modules.report.export import build_journal_daily_xlsx
from app.modules.report.service import (
    CAP,
    dwh_health,
    journal_daily_count,
    journal_daily_page,
    journal_daily_rows,
    list_branches,
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
    filename = f"journaldaily{datetime.now():%Y%m%d%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

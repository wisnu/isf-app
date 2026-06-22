"""Distribution reports router — 7 laporan penyaluran dengan data + export endpoints."""

from __future__ import annotations

from datetime import date as _date, datetime

from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse

from app.modules.distribution.export import (
    build_proposal_incoming_xlsx,
    build_mustahiq_list_xlsx,
    build_realization_regular_xlsx,
    build_realization_non_regular_xlsx,
    build_realization_receivable_xlsx,
    build_realization_return_xlsx,
    build_realization_by_mustahiq_xlsx,
)
from app.modules.distribution.service import (
    CAP,
    proposal_incoming_count,
    proposal_incoming_page,
    proposal_incoming_rows,
    mustahiq_list_count,
    mustahiq_list_page,
    mustahiq_list_rows,
    realization_regular_count,
    realization_regular_page,
    realization_regular_rows,
    realization_non_regular_count,
    realization_non_regular_page,
    realization_non_regular_rows,
    realization_receivable_count,
    realization_receivable_page,
    realization_receivable_rows,
    realization_return_count,
    realization_return_page,
    realization_return_rows,
    realization_by_mustahiq_count,
    realization_by_mustahiq_page,
    realization_by_mustahiq_rows,
)
from app.shared.response import err, ok

router = APIRouter(prefix="/distribution/report", tags=["distribution-report"])

_DB_UNAVAILABLE = err("DB_UNAVAILABLE", "Database tidak tersedia")
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _dmy(iso: str) -> str:
    p = (iso or "").split("-")
    return f"{p[2]}-{p[1]}-{p[0]}" if len(p) == 3 else (iso or "")


def _period_label(begin: str, end: str) -> str:
    return _dmy(begin) if begin == end else f"{_dmy(begin)} s/d {_dmy(end)}"


# ── 1. Laporan Proposal Masuk ─────────────────────────────────────────────────

@router.get("/proposal-incoming")
async def proposal_incoming(
    date_from: str = Query(...),
    date_to: str = Query(...),
    mustahiq_id: int | None = Query(default=None),
    product_group_id: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    data = await proposal_incoming_page(date_from, date_to, mustahiq_id, product_group_id, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/proposal-incoming/export.xlsx")
async def proposal_incoming_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
    mustahiq_id: int | None = Query(default=None),
    product_group_id: int | None = Query(default=None),
):
    total = await proposal_incoming_count(date_from, date_to, mustahiq_id, product_group_id)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal atau filter."),
        )
    rows = await proposal_incoming_rows(date_from, date_to, mustahiq_id, product_group_id)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_proposal_incoming_xlsx(rows, _period_label(date_from, date_to))
    filename = f"proposal-incoming-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── 2. Laporan Daftar Mustahiq ────────────────────────────────────────────────

@router.get("/mustahiq-list")
async def mustahiq_list(
    mustahiq_type: str | None = Query(default=None),
    product_id: int | None = Query(default=None),
    date_start_from: str | None = Query(default=None),
    date_start_to: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    data = await mustahiq_list_page(mustahiq_type, product_id, date_start_from, date_start_to, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/mustahiq-list/export.xlsx")
async def mustahiq_list_export(
    mustahiq_type: str | None = Query(default=None),
    product_id: int | None = Query(default=None),
    date_start_from: str | None = Query(default=None),
    date_start_to: str | None = Query(default=None),
):
    total = await mustahiq_list_count(mustahiq_type, product_id, date_start_from, date_start_to)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit filter."),
        )
    rows = await mustahiq_list_rows(mustahiq_type, product_id, date_start_from, date_start_to)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_mustahiq_list_xlsx(rows, "Laporan Daftar Mustahiq")
    filename = f"mustahiq-list-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── 3. Laporan Realisasi Rutin ────────────────────────────────────────────────

@router.get("/realization-regular")
async def realization_regular(
    date_from: str = Query(...),
    date_to: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    data = await realization_regular_page(date_from, date_to, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/realization-regular/export.xlsx")
async def realization_regular_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
):
    total = await realization_regular_count(date_from, date_to)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal."),
        )
    rows = await realization_regular_rows(date_from, date_to)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_realization_regular_xlsx(rows, _period_label(date_from, date_to))
    filename = f"realization-regular-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── 4. Laporan Realisasi Non Rutin ────────────────────────────────────────────

@router.get("/realization-non-regular")
async def realization_non_regular(
    date_from: str = Query(...),
    date_to: str = Query(...),
    amount_min: float = Query(default=0.0, ge=0),
    amount_max: float = Query(default=3000000.0, ge=0),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    data = await realization_non_regular_page(date_from, date_to, amount_min, amount_max, branch, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/realization-non-regular/export.xlsx")
async def realization_non_regular_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
    amount_min: float = Query(default=0.0, ge=0),
    amount_max: float = Query(default=3000000.0, ge=0),
    branch: str | None = Query(default=None),
):
    total = await realization_non_regular_count(date_from, date_to, amount_min, amount_max, branch)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit filter."),
        )
    rows = await realization_non_regular_rows(date_from, date_to, amount_min, amount_max, branch)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_realization_non_regular_xlsx(rows, _period_label(date_from, date_to))
    filename = f"realization-non-regular-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── 5. Laporan Piutang Realisasi ──────────────────────────────────────────────

@router.get("/realization-receivable")
async def realization_receivable(
    date_from: str = Query(...),
    date_to: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    data = await realization_receivable_page(date_from, date_to, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/realization-receivable/export.xlsx")
async def realization_receivable_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
):
    total = await realization_receivable_count(date_from, date_to)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal."),
        )
    rows = await realization_receivable_rows(date_from, date_to)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_realization_receivable_xlsx(rows, _period_label(date_from, date_to))
    filename = f"realization-receivable-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── 6. Laporan Pengembalian Realisasi ─────────────────────────────────────────

@router.get("/realization-return")
async def realization_return(
    date_from: str = Query(...),
    date_to: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    data = await realization_return_page(date_from, date_to, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/realization-return/export.xlsx")
async def realization_return_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
):
    total = await realization_return_count(date_from, date_to)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit rentang tanggal."),
        )
    rows = await realization_return_rows(date_from, date_to)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_realization_return_xlsx(rows, _period_label(date_from, date_to))
    filename = f"realization-return-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── 7. Laporan Penyaluran Per Mustahiq ────────────────────────────────────────

@router.get("/realization-by-mustahiq")
async def realization_by_mustahiq(
    date_from: str = Query(...),
    date_to: str = Query(...),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    data = await realization_by_mustahiq_page(date_from, date_to, branch, page, page_size)
    if data is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok(data)


@router.get("/realization-by-mustahiq/export.xlsx")
async def realization_by_mustahiq_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
    branch: str | None = Query(default=None),
):
    total = await realization_by_mustahiq_count(date_from, date_to, branch)
    if total > CAP:
        return JSONResponse(
            status_code=422,
            content=err("REPORT_TOO_LARGE", f"Hasil {total:,} baris melebihi batas {CAP:,}. Persempit filter."),
        )
    rows = await realization_by_mustahiq_rows(date_from, date_to, branch)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    xlsx = build_realization_by_mustahiq_xlsx(rows, _period_label(date_from, date_to))
    filename = f"realization-by-mustahiq-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

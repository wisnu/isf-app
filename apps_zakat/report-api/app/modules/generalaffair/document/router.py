"""General Affair document reports router — laporan dokumen masuk & keluar."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse

from app.modules.generalaffair.document.export import (
    build_incoming_document_xlsx,
    build_outgoing_document_xlsx,
)
from app.modules.generalaffair.document.service import (
    incoming_document_rows,
    outgoing_document_rows,
)
from app.shared.response import err, ok

router = APIRouter(prefix="/generalaffair/report", tags=["generalaffair-report"])

_DB_UNAVAILABLE = err("DB_UNAVAILABLE", "Database tidak tersedia")
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _dmy(iso: str) -> str:
    p = (iso or "").split("-")
    return f"{p[2]}-{p[1]}-{p[0]}" if len(p) == 3 else (iso or "")


def _period_label(begin: str, end: str) -> str:
    return _dmy(begin) if begin == end else f"{_dmy(begin)} s/d {_dmy(end)}"


@router.get("/incoming-document")
async def incoming_document(
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
    branch: str | None = Query(default=None),
):
    rows = await incoming_document_rows(date_from, date_to, id_jenis_dokumen, branch)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok({"rows": rows, "total": len(rows)})


@router.get("/incoming-document/export.xlsx")
async def incoming_document_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
    branch: str | None = Query(default=None),
):
    rows = await incoming_document_rows(date_from, date_to, id_jenis_dokumen, branch)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    period = _period_label(date_from, date_to)
    content = build_incoming_document_xlsx(rows, period)
    filename = f"laporan-dokumen-masuk-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/outgoing-document")
async def outgoing_document(
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
    branch: str | None = Query(default=None),
):
    rows = await outgoing_document_rows(date_from, date_to, id_jenis_dokumen, branch)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    return ok({"rows": rows, "total": len(rows)})


@router.get("/outgoing-document/export.xlsx")
async def outgoing_document_export(
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
    branch: str | None = Query(default=None),
):
    rows = await outgoing_document_rows(date_from, date_to, id_jenis_dokumen, branch)
    if rows is None:
        return JSONResponse(status_code=503, content=_DB_UNAVAILABLE)
    period = _period_label(date_from, date_to)
    content = build_outgoing_document_xlsx(rows, period)
    filename = f"laporan-dokumen-keluar-{datetime.now():%Y%m%d-%H%M%S}.xlsx"
    return Response(
        content=content,
        media_type=_XLSX_MIME,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

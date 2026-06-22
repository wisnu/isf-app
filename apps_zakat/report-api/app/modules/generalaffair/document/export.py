"""Excel export untuk laporan Dokumen (openpyxl)."""

from __future__ import annotations

from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


def _dmy(iso: str | None) -> str:
    if not iso:
        return ""
    parts = str(iso).split("-")
    return f"{parts[2]}-{parts[1]}-{parts[0]}" if len(parts) == 3 else str(iso)


def _header_row(ws, row_idx: int, title: str, period_label: str) -> int:
    ws.cell(row=row_idx, column=1, value=title).font = Font(bold=True, size=14)
    ws.cell(row=row_idx + 1, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=row_idx + 1, column=2, value=period_label)
    return row_idx + 3


def _setup_columns(ws, header_row: int, cols: list[tuple[str, int]]):
    for col_idx, (title, width) in enumerate(cols, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    ws.freeze_panes = f"A{header_row + 1}"


def build_incoming_document_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Dokumen Masuk"

    header_row = _header_row(ws, 1, "Laporan Dokumen Masuk", period_label)
    cols = [
        ("NO", 5),
        ("JENIS DOKUMEN", 20),
        ("NO DOKUMEN", 16),
        ("PENGIRIM", 24),
        ("PERIHAL", 32),
        ("TGL DOKUMEN", 13),
        ("TGL TERIMA", 13),
        ("KETERANGAN", 32),
    ]
    _setup_columns(ws, header_row, cols)

    for i, r in enumerate(rows, start=header_row + 1):
        values = [
            i - header_row,
            r.get("nama_jenis_dokumen"),
            r.get("nomor"),
            r.get("pengirim"),
            r.get("perihal"),
            _dmy(r.get("tanggal_dokumen")),
            _dmy(r.get("tanggal_terima")),
            r.get("keterangan"),
        ]
        for col_idx, val in enumerate(values, 1):
            ws.cell(row=i, column=col_idx, value=val)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


def build_outgoing_document_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Dokumen Keluar"

    header_row = _header_row(ws, 1, "Laporan Dokumen Keluar", period_label)
    cols = [
        ("NO", 5),
        ("JENIS DOKUMEN", 20),
        ("NO DOKUMEN", 16),
        ("TUJUAN", 24),
        ("PERIHAL", 32),
        ("TGL DOKUMEN", 13),
        ("TGL KIRIM", 13),
        ("STATUS KIRIM", 14),
        ("KETERANGAN", 32),
    ]
    _setup_columns(ws, header_row, cols)

    for i, r in enumerate(rows, start=header_row + 1):
        values = [
            i - header_row,
            r.get("nama_jenis_dokumen"),
            r.get("nomor"),
            r.get("tujuan"),
            r.get("perihal"),
            _dmy(r.get("tanggal_dokumen")),
            _dmy(r.get("tanggal_kirim")),
            r.get("statuskirim"),
            r.get("keterangan"),
        ]
        for col_idx, val in enumerate(values, 1):
            ws.cell(row=i, column=col_idx, value=val)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

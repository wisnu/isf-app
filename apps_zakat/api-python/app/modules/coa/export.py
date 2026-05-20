"""Excel export for Chart of Accounts."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

from app.modules.coa.schema import CoaRow


def build_coa_xlsx(rows: list[CoaRow], title: str = "Chart of Accounts") -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "COA"

    # Title (row 1) + meta (row 2)
    ws.cell(row=1, column=1, value=title).font = Font(bold=True, size=14)
    meta = f"Diekspor: {datetime.utcnow():%Y-%m-%d %H:%M UTC} · {len(rows)} baris"
    ws.cell(row=2, column=1, value=meta).font = Font(italic=True, color="6B6B70", size=10)

    # Header row at row 4 (skip row 3 as spacer)
    header_row = 4
    headers = ["Kode", "Nama Akun", "Tipe", "Level", "Parent", "Sifat"]
    for col_idx, h in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col_idx, value=h)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1A1A1C", end_color="1A1A1C", fill_type="solid")
        cell.alignment = Alignment(horizontal="left", vertical="center")

    # Data rows
    thin = Side(border_style="thin", color="E3E3E6")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for i, r in enumerate(rows, start=header_row + 1):
        ws.cell(row=i, column=1, value=r.code)
        ws.cell(row=i, column=2, value=r.name or "")
        ws.cell(row=i, column=3, value=r.type_label)
        ws.cell(row=i, column=4, value=r.level if r.level is not None else "")
        ws.cell(row=i, column=5, value=r.parent or "")
        ws.cell(row=i, column=6, value="Detail" if r.is_detail else "Grup")
        # Group rows: subtle background tint + bold
        if not r.is_detail:
            tint = PatternFill(start_color="F7F7F8", end_color="F7F7F8", fill_type="solid")
            for col_idx in range(1, len(headers) + 1):
                ws.cell(row=i, column=col_idx).fill = tint
                ws.cell(row=i, column=col_idx).font = Font(bold=True)
        # Light border on all cells
        for col_idx in range(1, len(headers) + 1):
            ws.cell(row=i, column=col_idx).border = border
            ws.cell(row=i, column=col_idx).alignment = Alignment(vertical="center")

    # Column widths
    widths = [14, 55, 16, 8, 14, 10]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # Freeze panes below header
    ws.freeze_panes = f"A{header_row + 1}"

    # Auto-filter on header
    if rows:
        ws.auto_filter.ref = (
            f"A{header_row}:"
            f"{get_column_letter(len(headers))}{header_row + len(rows)}"
        )

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

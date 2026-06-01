"""Excel export untuk Laporan Jurnal Harian (openpyxl)."""

from __future__ import annotations

from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

# (judul kolom, lebar, format angka opsional)
_COLS: list[tuple[str, int, str | None]] = [
    ("Nomor Transaksi", 24, None),
    ("Tanggal Jurnal", 14, None),
    ("Nominal Debet", 18, "#,##0.00"),
    ("Nominal Kredit", 18, "#,##0.00"),
    ("Kode Cabang", 12, None),
    ("Kode Account", 14, None),
    ("Nama Account", 30, None),
    ("Account Sub Sistem", 28, None),
    ("Keterangan", 40, None),
    ("Inputer", 16, None),
]


def build_journal_daily_xlsx(rows: list[dict], branch_label: str, period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"

    ws.cell(row=1, column=1, value="Daftar Jurnal Transaksi").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=period_label)

    header_row = 4
    for col_idx, (title, _w, _f) in enumerate(_COLS, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")

    for i, r in enumerate(rows, start=header_row + 1):
        sub = " - ".join(p for p in [r.get("subaccountcode"), r.get("subaccountname")] if p)
        values = [
            r.get("transactionno"),
            r.get("journal_date"),
            float(r.get("debit_ekuiv") or 0),
            float(r.get("credit_ekuiv") or 0),
            r.get("account_branch_code"),
            r.get("account_code"),
            r.get("account_name"),
            sub,
            r.get("description"),
            r.get("inputer"),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            num_fmt = _COLS[col_idx - 1][2]
            if num_fmt:
                cell.number_format = num_fmt

    for col_idx, (_t, width, _f) in enumerate(_COLS, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.freeze_panes = f"A{header_row + 1}"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

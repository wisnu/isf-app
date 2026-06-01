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


# ── List Transaksi Umum (grouped: header transaksi + item) ───────────────────

_GT_COLS: list[tuple[str, int, str | None]] = [
    ("No", 5, None),
    ("No Transaksi", 24, None),
    ("Tgl Transaksi", 13, None),
    ("Tgl Aktual", 13, None),
    ("Deskripsi", 36, None),
    ("Inputer", 14, None),
    ("Ref Account No", 16, None),
    ("Ref Account Name", 28, None),
    ("D/K", 6, None),
    ("Nominal", 18, "#,##0.00"),
    ("Keterangan", 32, None),
    ("Budget", 28, None),
]


def build_general_transaction_xlsx(rows: list[dict], branch_label: str, period_label: str) -> bytes:
    """rows = item-grain flat (punya field header + item), di-group per transactionid."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    ws.cell(row=1, column=1, value="Daftar Transaksi Umum").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=period_label)

    header_row = 5
    for col_idx, (title, _w, _f) in enumerate(_GT_COLS, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")

    for col_idx, (_t, width, _f) in enumerate(_GT_COLS, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    r = header_row
    idx = 0
    prev_tx = None
    for row in rows:
        txno = row.get("transactionno")
        if txno != prev_tx:
            idx += 1
            r += 1
            # baris header transaksi: kolom 1-6
            ws.cell(row=r, column=1, value=idx).font = Font(bold=True)
            ws.cell(row=r, column=2, value=txno).font = Font(bold=True)
            ws.cell(row=r, column=3, value=row.get("transactiondate"))
            ws.cell(row=r, column=4, value=row.get("actualdate"))
            ws.cell(row=r, column=5, value=row.get("header_description"))
            ws.cell(row=r, column=6, value=row.get("inputer"))
            prev_tx = txno
        # baris item: kolom 7-12
        r += 1
        sub_budget = " - ".join(
            p for p in [row.get("budget_code"), row.get("budget_item_description")] if p
        )
        ws.cell(row=r, column=7, value=row.get("refaccountno"))
        ws.cell(row=r, column=8, value=row.get("refaccountname"))
        ws.cell(row=r, column=9, value=row.get("mutationtype"))
        amt = ws.cell(row=r, column=10, value=float(row.get("amount") or 0))
        amt.number_format = "#,##0.00"
        ws.cell(row=r, column=11, value=row.get("item_description"))
        ws.cell(row=r, column=12, value=sub_budget)

    ws.freeze_panes = f"A{header_row + 1}"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Transaksi Kas/Bank Harian (summary + mutasi + running balance) ───────────

_AUTHSTATUS = {"T": "SUDAH OTORISASI", "F": "BELUM OTORISASI"}

_CASH_COLS: list[tuple[str, int, str | None]] = [
    ("Tanggal", 13, None),
    ("No Transaksi", 24, None),
    ("D/K", 6, None),
    ("Nominal", 18, "#,##0.00"),
    ("Saldo", 18, "#,##0.00"),
    ("Keterangan", 36, None),
    ("Referensi", 18, None),
    ("Inputer", 14, None),
    ("Status", 18, None),
]


def build_cash_mutation_xlsx(summary: dict, account_label: str, period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    ws.cell(row=1, column=1, value="Transaksi Kas/Bank Harian").font = Font(bold=True, size=14)
    meta = [
        ("Rekening", account_label),
        ("Periode", period_label),
        ("Saldo Awal", summary.get("begin_balance", 0)),
        ("Total Debet", summary.get("total_debit", 0)),
        ("Total Kredit", summary.get("total_credit", 0)),
        ("Saldo Akhir", summary.get("end_balance", 0)),
    ]
    for i, (label, val) in enumerate(meta, start=2):
        ws.cell(row=i, column=1, value=label).font = Font(bold=True)
        c = ws.cell(row=i, column=2, value=val)
        if isinstance(val, (int, float)):
            c.number_format = "#,##0.00"

    header_row = 9
    for col_idx, (title, width, _f) in enumerate(_CASH_COLS, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    for i, r in enumerate(summary.get("rows", []), start=header_row + 1):
        values = [
            r.get("actualdate"),
            r.get("transactionno"),
            r.get("mutationtype"),
            float(r.get("amount") or 0),
            float(r.get("balance") or 0),
            r.get("description"),
            r.get("reference_no"),
            r.get("inputer"),
            _AUTHSTATUS.get(r.get("auth_status"), r.get("auth_status") or ""),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            fmt = _CASH_COLS[col_idx - 1][2]
            if fmt:
                cell.number_format = fmt

    ws.freeze_panes = f"A{header_row + 1}"
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Rekapitulasi Kas/Bank (per akun, group valuta + subtotal) ────────────────

_SUMCASH_COLS: list[tuple[str, int]] = [
    ("Rekening", 40),
    ("Saldo Awal", 18),
    ("Debet", 18),
    ("Kredit", 18),
    ("Total", 18),
    ("Saldo Akhir", 18),
]


def build_cash_summary_xlsx(payload: dict, branch_label: str, period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    ws.cell(row=1, column=1, value="Rekapitulasi Transaksi Kas/Bank").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=period_label)
    g = payload.get("grand", {})
    grand_meta = [
        ("Total Saldo Awal", g.get("begin_balance", 0)),
        ("Total Debet", g.get("total_debit", 0)),
        ("Total Kredit", g.get("total_credit", 0)),
        ("Total Saldo Akhir", g.get("total_end", 0)),
    ]
    for i, (label, val) in enumerate(grand_meta, start=4):
        ws.cell(row=i, column=1, value=label).font = Font(bold=True)
        ws.cell(row=i, column=2, value=float(val or 0)).number_format = "#,##0.00"

    header_row = 9
    for col_idx, (title, width) in enumerate(_SUMCASH_COLS, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    def _num(cell, v):
        cell.value = float(v or 0)
        cell.number_format = "#,##0.00"

    r = header_row
    for grp in payload.get("groups", []):
        r += 1
        ws.cell(row=r, column=1, value=f"Valuta: {grp['currency']}").font = Font(bold=True, italic=True)
        for item in grp["rows"]:
            r += 1
            ws.cell(row=r, column=1, value=f"{item['account_no']} - {item.get('account_name') or ''}")
            _num(ws.cell(row=r, column=2), item["begin_balance"])
            _num(ws.cell(row=r, column=3), item["debit"])
            _num(ws.cell(row=r, column=4), item["credit"])
            _num(ws.cell(row=r, column=5), item["total"])
            _num(ws.cell(row=r, column=6), item["end_balance"])
        st = grp["subtotal"]
        r += 1
        sub_cell = ws.cell(row=r, column=1, value=f"SUBTOTAL {grp['currency']}")
        sub_cell.font = Font(bold=True)
        for col, key in ((2, "begin_balance"), (3, "debit"), (4, "credit"), (5, "total"), (6, "end_balance")):
            c = ws.cell(row=r, column=col)
            _num(c, st[key])
            c.font = Font(bold=True)

    ws.freeze_panes = f"A{header_row + 1}"
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

"""Excel export untuk Laporan Jurnal Harian (openpyxl)."""

from __future__ import annotations

from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter


def _dmy(iso) -> str:
    """ISO 'YYYY-MM-DD' → 'DD-MM-YYYY' untuk tampilan tanggal di Excel."""
    if not iso:
        return ""
    parts = str(iso).split("-")
    return f"{parts[2]}-{parts[1]}-{parts[0]}" if len(parts) == 3 else str(iso)

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
            _dmy(r.get("journal_date")),
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
            ws.cell(row=r, column=3, value=_dmy(row.get("transactiondate")))
            ws.cell(row=r, column=4, value=_dmy(row.get("actualdate")))
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


# ── Transaksi Kas/Bank Harian (summary + movement + running balance) ───────────

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
            _dmy(r.get("actualdate")),
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


# ── Monitoring Saldo Kas/Bank Bulanan (matriks akun × 12 bulan) ──────────────

def build_cash_monthly_xlsx(payload: dict, branch_label: str, year: int) -> bytes:
    months = payload.get("months", [])
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    ws.cell(row=1, column=1, value="Monitoring Saldo Kas/Bank Bulanan").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Tahun").font = Font(bold=True)
    ws.cell(row=3, column=2, value=year)

    header_row = 5
    headers = ["Rekening", *months]
    for col_idx, title in enumerate(headers, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")
    ws.column_dimensions["A"].width = 40
    for col_idx in range(2, 14):
        ws.column_dimensions[get_column_letter(col_idx)].width = 16

    def _bal_row(r, label, balances, bold=False):
        cell = ws.cell(row=r, column=1, value=label)
        if bold:
            cell.font = Font(bold=True)
        for m in range(12):
            c = ws.cell(row=r, column=m + 2, value=float(balances[m] or 0))
            c.number_format = "#,##0.00"
            if bold:
                c.font = Font(bold=True)

    r = header_row
    for grp in payload.get("groups", []):
        r += 1
        ws.cell(row=r, column=1, value=grp["type_label"]).font = Font(bold=True, italic=True)
        for item in grp["rows"]:
            r += 1
            _bal_row(r, f"{item['account_no']} - {item.get('account_name') or ''}", item["balances"])
        r += 1
        _bal_row(r, f"Total {grp['type_label']}", grp["totals"], bold=True)

    ws.freeze_panes = "B6"
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Trial Balance ────────────────────────────────────────────────────────────

_TB_COLS: list[tuple[str, int]] = [
    ("Kode Account", 14),
    ("Nama Account", 36),
    ("Cabang", 10),
    ("Saldo Awal", 18),
    ("Debet", 18),
    ("Kredit", 18),
    ("Saldo Akhir", 18),
]


def build_trial_balance_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"

    ws.cell(row=1, column=1, value="Trial Balance").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=f"{payload.get('begin')} s/d {payload.get('end')}")

    header_row = 4
    for col_idx, (title, width) in enumerate(_TB_COLS, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    def _money(r, col, val, bold=False):
        c = ws.cell(row=r, column=col, value=float(val or 0))
        c.number_format = "#,##0.00"
        if bold:
            c.font = Font(bold=True)

    r = header_row
    consolidated = payload.get("consolidated")
    for grp in payload.get("groups", []):
        r += 1
        ws.cell(row=r, column=1, value=grp["type_label"]).font = Font(bold=True, italic=True)
        for item in grp["rows"]:
            r += 1
            ws.cell(row=r, column=1, value=item["account_code"])
            ws.cell(row=r, column=2, value=item.get("account_name") or "")
            ws.cell(row=r, column=3, value="" if consolidated else (item.get("branch_code") or ""))
            _money(r, 4, item["opening_balance"])
            _money(r, 5, item["debit"])
            _money(r, 6, item["credit"])
            _money(r, 7, item["closing_balance"])
        r += 1
        st = grp["subtotal"]
        ws.cell(row=r, column=1, value=f"Total {grp['type_label']}").font = Font(bold=True)
        _money(r, 4, st["opening_balance"], bold=True)
        _money(r, 5, st["debit"], bold=True)
        _money(r, 6, st["credit"], bold=True)
        _money(r, 7, st["closing_balance"], bold=True)

    r += 2
    gt = payload.get("grand_total", {})
    ws.cell(row=r, column=1, value="GRAND TOTAL").font = Font(bold=True)
    _money(r, 4, gt.get("opening_balance"), bold=True)
    _money(r, 5, gt.get("debit"), bold=True)
    _money(r, 6, gt.get("credit"), bold=True)
    _money(r, 7, gt.get("closing_balance"), bold=True)

    ws.freeze_panes = "A5"
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Neraca ───────────────────────────────────────────────────────────────────


def build_balance_sheet_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"

    ws.cell(row=1, column=1, value="NERACA").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value=f"Per Tanggal {payload.get('date')} · Periode {payload.get('period_type')}")
    ws.cell(row=3, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=3, column=2, value=branch_label)

    header_row = 5
    ws.cell(row=header_row, column=1, value="Akun").font = Font(bold=True)
    c2 = ws.cell(row=header_row, column=6, value=f"Nilai per {payload.get('date')}")
    c3 = ws.cell(row=header_row, column=7, value=f"Nilai per {payload.get('date_prev')}")
    for c in (c2, c3):
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="right")
    ws.column_dimensions["A"].width = 4
    for col in ("B", "C", "D", "E"):
        ws.column_dimensions[col].width = 12
    ws.column_dimensions["F"].width = 20
    ws.column_dimensions["G"].width = 20

    def _acct_row(r, item):
        col = min(int(item.get("account_level", 0)) + 1, 5)
        ws.cell(row=r, column=col, value=f"{item['account_code']} {item.get('account_name') or ''}")
        for ci, key in ((6, "balance"), (7, "balance_prev")):
            cc = ws.cell(row=r, column=ci, value=float(item.get(key) or 0))
            cc.number_format = "#,##0.00"

    def _total_row(r, label, val, val_prev):
        ws.cell(row=r, column=1, value=label).font = Font(bold=True)
        for ci, v in ((6, val), (7, val_prev)):
            cc = ws.cell(row=r, column=ci, value=float(v or 0))
            cc.number_format = "#,##0.00"
            cc.font = Font(bold=True)

    r = header_row + 1
    ws.cell(row=r, column=1, value="AKTIVA").font = Font(bold=True, italic=True)
    for item in payload.get("aktiva", []):
        r += 1
        _acct_row(r, item)
    r += 1
    _total_row(r, "Total Aktiva", payload.get("total_aktiva"), payload.get("total_aktiva_prev"))

    r += 2
    ws.cell(row=r, column=1, value="PASIVA").font = Font(bold=True, italic=True)
    for item in payload.get("pasiva", []):
        r += 1
        _acct_row(r, item)
    r += 1
    _total_row(r, "Total Pasiva", payload.get("total_pasiva"), payload.get("total_pasiva_prev"))

    r += 2
    ws.cell(row=r, column=1, value="STATUS BALANCE").font = Font(bold=True)
    sc = ws.cell(row=r, column=6, value=float(payload.get("selisih") or 0))
    sc.number_format = "#,##0.00"
    sc.font = Font(bold=True)
    ws.cell(row=r, column=7, value=payload.get("status_balance")).font = Font(bold=True)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Arus Kas ─────────────────────────────────────────────────────────────────


def build_cash_flow_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"

    ws.cell(row=1, column=1, value="LAPORAN ARUS KAS").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value=f"Periode {payload.get('begin')} s/d {payload.get('end')}")
    ws.cell(row=3, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=3, column=2, value=branch_label)
    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 22

    def _money(r, val, bold=False):
        c = ws.cell(row=r, column=2, value=float(val or 0))
        c.number_format = "#,##0.00"
        if bold:
            c.font = Font(bold=True)

    r = 5
    for sec in payload.get("sections", []):
        ws.cell(row=r, column=1, value=sec["title"]).font = Font(bold=True, italic=True)
        r += 1
        for ln in sec["lines"]:
            ws.cell(row=r, column=1, value=f"   {ln['label']}")
            _money(r, ln["value"])
            r += 1
        ws.cell(row=r, column=1, value=f"Jumlah {sec['title']}").font = Font(bold=True)
        _money(r, sec["subtotal"], bold=True)
        r += 2

    ws.cell(row=r, column=1, value="Kenaikan (Penurunan) Kas Bersih").font = Font(bold=True)
    _money(r, payload.get("kenaikan_bersih"), bold=True)
    r += 1
    ws.cell(row=r, column=1, value="Saldo Kas & Setara Kas Awal Periode")
    _money(r, payload.get("opening_balance"))
    r += 1
    ws.cell(row=r, column=1, value="Saldo Kas & Setara Kas Akhir Periode").font = Font(bold=True)
    _money(r, payload.get("closing_balance"), bold=True)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Buku Besar (General Ledger) ──────────────────────────────────────────────

_GL_COLS: list[tuple[str, int]] = [
    ("Tanggal", 12),
    ("No. Transaksi", 22),
    ("Keterangan", 40),
    ("Sub Account", 26),
    ("Lawan Akun", 26),
    ("Debet", 18),
    ("Kredit", 18),
]


def build_general_ledger_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"

    ws.cell(row=1, column=1, value="Buku Besar").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=f"{payload.get('begin')} s/d {payload.get('end')}")
    for col_idx, (_t, width) in enumerate(_GL_COLS, 1):
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    def _money(r, col, val, bold=False):
        c = ws.cell(row=r, column=col, value=float(val or 0))
        c.number_format = "#,##0.00"
        if bold:
            c.font = Font(bold=True)

    r = 5
    for acc in payload.get("accounts", []):
        ws.cell(row=r, column=1, value=f"{acc['account_code']} - {acc.get('account_name') or ''}").font = Font(bold=True)
        r += 1
        ws.cell(row=r, column=1, value="Saldo Awal").font = Font(italic=True)
        _money(r, 7, acc["opening_balance"])
        r += 1
        # header kolom
        for col_idx, (title, _w) in enumerate(_GL_COLS, 1):
            c = ws.cell(row=r, column=col_idx, value=title)
            c.font = Font(bold=True, color="FFFF00")
            c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        r += 1
        for ln in acc["rows"]:
            ws.cell(row=r, column=1, value=_dmy(ln["journal_date"]))
            ws.cell(row=r, column=2, value=ln["transactionno"])
            ws.cell(row=r, column=3, value=ln["description"])
            ws.cell(row=r, column=4, value=ln["subaccount"])
            ws.cell(row=r, column=5, value=ln["lawan"])
            _money(r, 6, ln["debit"])
            _money(r, 7, ln["credit"])
            r += 1
        ws.cell(row=r, column=3, value="Total / Mutasi Bersih").font = Font(bold=True)
        _money(r, 6, acc["total_debit"], bold=True)
        _money(r, 7, acc["total_credit"], bold=True)
        r += 1
        ws.cell(row=r, column=3, value="Saldo Akhir").font = Font(bold=True)
        _money(r, 7, acc["closing_balance"], bold=True)
        r += 2

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Perubahan Dana ───────────────────────────────────────────────────────────


def build_fund_changes_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    ws.cell(row=1, column=1, value="LAPORAN PERUBAHAN DANA").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value=f"Periode {payload.get('begin')} s/d {payload.get('end')}")
    ws.cell(row=3, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=3, column=2, value=branch_label)
    ws.column_dimensions["A"].width = 52
    ws.column_dimensions["B"].width = 22

    def _money(r, val, bold=False):
        c = ws.cell(row=r, column=2, value=float(val or 0))
        c.number_format = "#,##0.00"
        if bold:
            c.font = Font(bold=True)

    r = 5
    for f in payload.get("funds", []):
        ws.cell(row=r, column=1, value=f["fund"]).font = Font(bold=True, size=12)
        r += 1
        ws.cell(row=r, column=1, value="Penerimaan").font = Font(bold=True, italic=True)
        r += 1
        for ln in f["collection"]:
            ws.cell(row=r, column=1, value=f"   {ln['label']}")
            _money(r, ln["value"])
            r += 1
        ws.cell(row=r, column=1, value="Jumlah Penerimaan").font = Font(bold=True)
        _money(r, f["total_collection"], bold=True)
        r += 1
        ws.cell(row=r, column=1, value="Penyaluran/Penggunaan").font = Font(bold=True, italic=True)
        r += 1
        for ln in f["distribution"]:
            ws.cell(row=r, column=1, value=f"   {ln['label']}")
            _money(r, ln["value"])
            r += 1
        ws.cell(row=r, column=1, value="Jumlah Penyaluran/Penggunaan").font = Font(bold=True)
        _money(r, f["total_distribution"], bold=True)
        r += 1
        ws.cell(row=r, column=1, value="Surplus (Defisit)").font = Font(bold=True)
        _money(r, f["surplus"], bold=True)
        r += 1
        ws.cell(row=r, column=1, value="Saldo Awal Dana")
        _money(r, f["opening_balance"])
        r += 1
        ws.cell(row=r, column=1, value="Saldo Akhir Dana").font = Font(bold=True)
        _money(r, f["closing_balance"], bold=True)
        r += 2

    ws.cell(row=r, column=1, value="TOTAL SALDO AKHIR SELURUH DANA").font = Font(bold=True)
    _money(r, payload.get("total_closing_balance"), bold=True)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Perubahan Dana Detail ────────────────────────────────────────────────────


def build_fund_changes_detail_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    ws.cell(row=1, column=1, value="LAPORAN PERUBAHAN DANA (RINCIAN PER AKUN)").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value=f"Periode {payload.get('begin')} s/d {payload.get('end')}")
    ws.cell(row=3, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=3, column=2, value=branch_label)
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 22

    def _money(r, col, val, bold=False):
        c = ws.cell(row=r, column=col, value=float(val or 0))
        c.number_format = "#,##0.00"
        if bold:
            c.font = Font(bold=True)

    r = 5
    for f in payload.get("funds", []):
        ws.cell(row=r, column=1, value=f["fund"]).font = Font(bold=True, size=12)
        r += 1
        for sec in f["sections"]:
            ws.cell(row=r, column=1, value=sec["title"]).font = Font(bold=True, italic=True)
            r += 1
            for row in sec["rows"]:
                ws.cell(row=r, column=1, value=row["account_code"])
                ws.cell(row=r, column=2, value=row.get("account_name") or "")
                _money(r, 3, row["value"])
                r += 1
            ws.cell(row=r, column=2, value=f"TOTAL {sec['title']}").font = Font(bold=True)
            _money(r, 3, sec["total"], bold=True)
            r += 2

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Penerimaan / Pengeluaran Amil ────────────────────────────────────────────


def build_amil_cash_xlsx(rows: list[dict], branch_label: str, period_label: str, title: str, with_budget: bool) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    ws.cell(row=1, column=1, value=title).font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=period_label)

    cols = [("Tanggal", 12), ("Kode Akun", 14), ("Nama Akun", 30), ("Keterangan", 40),
            ("Channel", 14), ("Nominal", 18), ("No. Referensi", 18), ("No. Transaksi", 24), ("Inputer", 16)]
    if with_budget:
        cols += [("Anggaran", 28)]
    hr = 5
    for ci, (t, w) in enumerate(cols, 1):
        c = ws.cell(row=hr, column=ci, value=t)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        ws.column_dimensions[get_column_letter(ci)].width = w

    total = 0.0
    r = hr
    for row in rows:
        r += 1
        ws.cell(row=r, column=1, value=_dmy(row["actualdate"]))
        ws.cell(row=r, column=2, value=row["account_code"])
        ws.cell(row=r, column=3, value=row.get("account_name") or "")
        ws.cell(row=r, column=4, value=row.get("description") or "")
        ws.cell(row=r, column=5, value=row.get("channel") or "")
        c = ws.cell(row=r, column=6, value=float(row.get("amount") or 0))
        c.number_format = "#,##0.00"
        ws.cell(row=r, column=7, value=row.get("referenceno") or "")
        ws.cell(row=r, column=8, value=row.get("transactionno") or "")
        ws.cell(row=r, column=9, value=row.get("inputer") or "")
        if with_budget:
            bud = " - ".join(p for p in [row.get("budgetcode"), row.get("budgetitemdescription")] if p)
            ws.cell(row=r, column=10, value=bud)
        total += float(row.get("amount") or 0)
    r += 1
    ws.cell(row=r, column=5, value="TOTAL").font = Font(bold=True)
    tc = ws.cell(row=r, column=6, value=total)
    tc.number_format = "#,##0.00"
    tc.font = Font(bold=True)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Penyaluran Dana ──────────────────────────────────────────────────────────

_DIST_COLS_X = [
    ("Tanggal", 12), ("Cabang", 16), ("Produk", 26), ("Akun", 28), ("Keterangan", 36),
    ("Ashnaf", 14), ("Kategori", 12), ("Dana", 10), ("Channel", 12), ("Penerima", 22),
    ("Anggaran", 24), ("No. Transaksi", 24), ("Inputer", 14), ("Nominal", 18),
]


def build_distribution_xlsx(rows: list[dict], branch_label: str, period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    ws.cell(row=1, column=1, value="Laporan Penyaluran Dana").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=period_label)
    hr = 5
    for ci, (t, w) in enumerate(_DIST_COLS_X, 1):
        c = ws.cell(row=hr, column=ci, value=t)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        ws.column_dimensions[get_column_letter(ci)].width = w
    total = 0.0
    r = hr
    for row in rows:
        r += 1
        vals = [_dmy(row["actualdate"]), row.get("branch_name") or "", row.get("product_name") or "",
                row.get("account_name") or "", row.get("description") or "", row.get("ashnaf_label") or "",
                row.get("category_label") or "", row.get("fund_label") or "", row.get("channel") or "",
                row.get("donorname") or "", row.get("budget") or "", row.get("transactionno") or "",
                row.get("inputer") or ""]
        for ci, v in enumerate(vals, 1):
            ws.cell(row=r, column=ci, value=v)
        c = ws.cell(row=r, column=14, value=float(row.get("amount") or 0))
        c.number_format = "#,##0.00"
        total += float(row.get("amount") or 0)
    r += 1
    ws.cell(row=r, column=13, value="TOTAL").font = Font(bold=True)
    tc = ws.cell(row=r, column=14, value=total)
    tc.number_format = "#,##0.00"
    tc.font = Font(bold=True)
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Penghimpunan Dana ────────────────────────────────────────────────────────

_COLL_COLS_X = [
    ("Tanggal", 12), ("Cabang", 16), ("Akun", 28), ("Keterangan", 36), ("Dana", 10),
    ("Channel", 12), ("Donatur", 24), ("No. Transaksi", 24), ("Inputer", 14), ("Nominal", 18),
]


def build_collection_xlsx(rows: list[dict], rekap: dict, branch_label: str, period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    ws.cell(row=1, column=1, value="Laporan Penghimpunan Dana").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=period_label)

    # Rekap per dana
    r = 5
    ws.cell(row=r, column=1, value="Rekapitulasi per Dana").font = Font(bold=True)
    r += 1
    for ci, t in enumerate(["Dana", "Saldo Awal", "Mutasi", "Saldo Akhir", "Jml Donatur"], 1):
        ws.cell(row=r, column=ci, value=t).font = Font(bold=True)
    r += 1
    for f in (rekap or {}).get("funds", []):
        ws.cell(row=r, column=1, value=f["fund_label"])
        for ci, k in ((2, "opening_balance"), (3, "movement"), (4, "closing_balance")):
            c = ws.cell(row=r, column=ci, value=float(f.get(k) or 0)); c.number_format = "#,##0.00"
        ws.cell(row=r, column=5, value=f.get("donors") or 0)
        r += 1
    r += 1

    # Detail
    hr = r
    for ci, (t, w) in enumerate(_COLL_COLS_X, 1):
        c = ws.cell(row=hr, column=ci, value=t)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        ws.column_dimensions[get_column_letter(ci)].width = w
    total = 0.0
    for row in rows:
        r += 1
        vals = [_dmy(row["actualdate"]), row.get("branch_name") or "", row.get("account_name") or "",
                row.get("description") or "", row.get("fund_label") or "", row.get("channel") or "",
                row.get("donorname") or "", row.get("transactionno") or "", row.get("inputer") or ""]
        for ci, v in enumerate(vals, 1):
            ws.cell(row=r, column=ci, value=v)
        c = ws.cell(row=r, column=10, value=float(row.get("amount") or 0)); c.number_format = "#,##0.00"
        total += float(row.get("amount") or 0)
    r += 1
    ws.cell(row=r, column=9, value="TOTAL").font = Font(bold=True)
    tc = ws.cell(row=r, column=10, value=total); tc.number_format = "#,##0.00"; tc.font = Font(bold=True)
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Ringkasan Piutang / Uang Muka ────────────────────────────────────────────


def build_ar_summary_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"
    with_debtor = payload.get("with_debtor")
    ws.cell(row=1, column=1, value=payload.get("title") or "Ringkasan Piutang").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=f"{payload.get('begin')} s/d {payload.get('end')}")

    cols = [("No. Akun", 22), ("Nama", 30)]
    if with_debtor:
        cols += [("Keterangan", 28)]
    cols += [("Saldo Awal", 18), ("Debet", 18), ("Kredit", 18), ("Saldo Akhir", 18)]
    hr = 5
    for ci, (t, w) in enumerate(cols, 1):
        c = ws.cell(row=hr, column=ci, value=t)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        ws.column_dimensions[get_column_letter(ci)].width = w
    base = 3 if with_debtor else 2

    def _money(r, col, val, bold=False):
        c = ws.cell(row=r, column=col, value=float(val or 0))
        c.number_format = "#,##0.00"
        if bold:
            c.font = Font(bold=True)

    r = hr
    for row in payload.get("rows", []):
        r += 1
        ws.cell(row=r, column=1, value=row["accountno"])
        ws.cell(row=r, column=2, value=row.get("accountname") or "")
        if with_debtor:
            ws.cell(row=r, column=3, value=row.get("debtor_description") or "")
        _money(r, base + 1, row["opening_balance"])
        _money(r, base + 2, row["debet"])
        _money(r, base + 3, row["kredit"])
        _money(r, base + 4, row["closing_balance"])
    r += 1
    gt = payload.get("grand_total", {})
    ws.cell(row=r, column=base, value="TOTAL").font = Font(bold=True)
    _money(r, base + 1, gt.get("opening_balance"), bold=True)
    _money(r, base + 2, gt.get("debet"), bold=True)
    _money(r, base + 3, gt.get("kredit"), bold=True)
    _money(r, base + 4, gt.get("closing_balance"), bold=True)
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Grup C: List Uang Muka / Piutang Realisasi / Realisasi Memo ──────────────


def _hdr(ws, cols, hr):
    for ci, (t, w) in enumerate(cols, 1):
        c = ws.cell(row=hr, column=ci, value=t)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        ws.column_dimensions[get_column_letter(ci)].width = w


def _money_cell(ws, r, col, val, bold=False):
    c = ws.cell(row=r, column=col, value=float(val or 0))
    c.number_format = "#,##0.00"
    if bold:
        c.font = Font(bold=True)


def build_cashadvance_xlsx(rows, branch_label, period_label):
    wb = Workbook(); ws = wb.active; ws.title = "data"
    ws.cell(row=1, column=1, value="List Transaksi Uang Muka Kegiatan").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True); ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True); ws.cell(row=3, column=2, value=period_label)
    cols = [("Tanggal", 12), ("Akun (Karyawan)", 30), ("No. Transaksi", 24), ("Keterangan", 36),
            ("Nominal", 18), ("Valuta", 10), ("Ekuivalen", 18), ("Status LPJ", 16), ("No. LPJ", 22), ("Inputer", 14)]
    _hdr(ws, cols, 5); r = 5
    for row in rows:
        r += 1
        ws.cell(row=r, column=1, value=_dmy(row.get("actualdate")))
        ws.cell(row=r, column=2, value=row.get("accountname") or "")
        ws.cell(row=r, column=3, value=row.get("transactionno") or "")
        ws.cell(row=r, column=4, value=row.get("description") or "")
        _money_cell(ws, r, 5, row.get("amount"))
        ws.cell(row=r, column=6, value=row.get("currencycode") or "")
        _money_cell(ws, r, 7, row.get("ekuiv"))
        ws.cell(row=r, column=8, value=row.get("lpj_label") or "")
        ws.cell(row=r, column=9, value=row.get("return_transactionno") or "")
        ws.cell(row=r, column=10, value=row.get("inputer") or "")
    buf = BytesIO(); wb.save(buf); return buf.getvalue()


def build_program_realization_xlsx(payload, branch_label):
    wb = Workbook(); ws = wb.active; ws.title = "data"
    ws.cell(row=1, column=1, value="Piutang Realisasi Penyaluran").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True); ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=f"{payload.get('begin')} s/d {payload.get('end')}")
    cols = [("Tanggal", 12), ("No. Memo", 22), ("Jenis", 12), ("Keterangan", 36), ("Realisasi", 18),
            ("Dilaporkan", 18), ("Outstanding", 18), ("Karyawan", 24), ("Inputer", 14)]
    _hdr(ws, cols, 5); r = 5
    for row in payload.get("rows", []):
        r += 1
        ws.cell(row=r, column=1, value=_dmy(row.get("realizationdate")))
        ws.cell(row=r, column=2, value=row.get("memo_number") or "")
        ws.cell(row=r, column=3, value=row.get("type_label") or "")
        ws.cell(row=r, column=4, value=row.get("description") or "")
        _money_cell(ws, r, 5, row.get("amount"))
        _money_cell(ws, r, 6, row.get("report_amount"))
        _money_cell(ws, r, 7, row.get("outstanding"))
        ws.cell(row=r, column=8, value=row.get("employee_name") or "")
        ws.cell(row=r, column=9, value=row.get("input_user") or "")
    r += 1
    gt = payload.get("grand_total", {})
    ws.cell(row=r, column=4, value="TOTAL").font = Font(bold=True)
    _money_cell(ws, r, 5, gt.get("amount"), bold=True)
    _money_cell(ws, r, 6, gt.get("report_amount"), bold=True)
    _money_cell(ws, r, 7, gt.get("outstanding"), bold=True)
    buf = BytesIO(); wb.save(buf); return buf.getvalue()


def build_realization_memo_xlsx(payload, branch_label):
    wb = Workbook(); ws = wb.active; ws.title = "data"
    ws.cell(row=1, column=1, value="Laporan Realisasi Project (Memo)").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True); ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=f"{payload.get('begin')} s/d {payload.get('end')}")
    cols = [("Tanggal", 12), ("No. Memo", 22), ("Subjek", 40), ("Nilai Memo", 18),
            ("Total Realisasi", 18), ("Total Pengembalian", 18), ("Outstanding", 18), ("Jml Realisasi", 12)]
    _hdr(ws, cols, 5); r = 5
    for row in payload.get("rows", []):
        r += 1
        ws.cell(row=r, column=1, value=_dmy(row.get("memo_date")))
        ws.cell(row=r, column=2, value=row.get("memo_number") or "")
        ws.cell(row=r, column=3, value=row.get("memo_subject") or "")
        _money_cell(ws, r, 4, row.get("memo_amount"))
        _money_cell(ws, r, 5, row.get("total_realisasi"))
        _money_cell(ws, r, 6, row.get("total_return"))
        _money_cell(ws, r, 7, row.get("outstanding"))
        ws.cell(row=r, column=8, value=row.get("realisasi_count") or 0)
    r += 1
    gt = payload.get("grand_total", {})
    ws.cell(row=r, column=3, value="TOTAL").font = Font(bold=True)
    _money_cell(ws, r, 4, gt.get("memo_amount"), bold=True)
    _money_cell(ws, r, 5, gt.get("total_realisasi"), bold=True)
    _money_cell(ws, r, 6, gt.get("total_return"), bold=True)
    _money_cell(ws, r, 7, gt.get("outstanding"), bold=True)
    buf = BytesIO(); wb.save(buf); return buf.getvalue()


# ── List Transaksi UPZ ───────────────────────────────────────────────────────

_UPZ_COLS = [
    ("Tanggal", 12), ("No. Transaksi", 24), ("Jenis", 18), ("Keterangan", 40),
    ("Sub Account", 26), ("Debet", 18), ("Kredit", 18),
]


def build_upz_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook(); ws = wb.active; ws.title = "data"
    ws.cell(row=1, column=1, value="List Transaksi UPZ").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value="Cabang").font = Font(bold=True); ws.cell(row=2, column=2, value=branch_label)
    ws.cell(row=3, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=3, column=2, value=f"{payload.get('begin')} s/d {payload.get('end')}")
    for ci, (_t, w) in enumerate(_UPZ_COLS, 1):
        ws.column_dimensions[get_column_letter(ci)].width = w
    r = 5
    for acc in payload.get("accounts", []):
        ws.cell(row=r, column=1, value=f"{acc['account_code']} - {acc.get('account_name') or ''}").font = Font(bold=True)
        r += 1
        for ci, (t, _w) in enumerate(_UPZ_COLS, 1):
            c = ws.cell(row=r, column=ci, value=t)
            c.font = Font(bold=True, color="FFFF00")
            c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        r += 1
        for ln in acc["rows"]:
            ws.cell(row=r, column=1, value=_dmy(ln["journal_date"]))
            ws.cell(row=r, column=2, value=ln["transactionno"])
            ws.cell(row=r, column=3, value=ln["trxtype"])
            ws.cell(row=r, column=4, value=ln["description"])
            ws.cell(row=r, column=5, value=ln["subaccount"])
            _money_cell(ws, r, 6, ln["debit"]); _money_cell(ws, r, 7, ln["credit"])
            r += 1
        ws.cell(row=r, column=3, value="Total").font = Font(bold=True)
        _money_cell(ws, r, 6, acc["total_debit"], bold=True); _money_cell(ws, r, 7, acc["total_credit"], bold=True)
        r += 2
    buf = BytesIO(); wb.save(buf); return buf.getvalue()

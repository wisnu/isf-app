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
    konsolidasi = payload.get("konsolidasi")
    for grp in payload.get("groups", []):
        r += 1
        ws.cell(row=r, column=1, value=grp["type_label"]).font = Font(bold=True, italic=True)
        for item in grp["rows"]:
            r += 1
            ws.cell(row=r, column=1, value=item["account_code"])
            ws.cell(row=r, column=2, value=item.get("account_name") or "")
            ws.cell(row=r, column=3, value="" if konsolidasi else (item.get("branch_code") or ""))
            _money(r, 4, item["saldo_awal"])
            _money(r, 5, item["debit"])
            _money(r, 6, item["credit"])
            _money(r, 7, item["saldo_akhir"])
        r += 1
        st = grp["subtotal"]
        ws.cell(row=r, column=1, value=f"Total {grp['type_label']}").font = Font(bold=True)
        _money(r, 4, st["saldo_awal"], bold=True)
        _money(r, 5, st["debit"], bold=True)
        _money(r, 6, st["credit"], bold=True)
        _money(r, 7, st["saldo_akhir"], bold=True)

    r += 2
    gt = payload.get("grand_total", {})
    ws.cell(row=r, column=1, value="GRAND TOTAL").font = Font(bold=True)
    _money(r, 4, gt.get("saldo_awal"), bold=True)
    _money(r, 5, gt.get("debit"), bold=True)
    _money(r, 6, gt.get("credit"), bold=True)
    _money(r, 7, gt.get("saldo_akhir"), bold=True)

    ws.freeze_panes = "A5"
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Neraca ───────────────────────────────────────────────────────────────────


def build_neraca_xlsx(payload: dict, branch_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "data"

    ws.cell(row=1, column=1, value="NERACA").font = Font(bold=True, size=14)
    ws.cell(row=2, column=1, value=f"Per Tanggal {payload.get('tanggal')} · Periode {payload.get('jenisperiode')}")
    ws.cell(row=3, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=3, column=2, value=branch_label)

    header_row = 5
    ws.cell(row=header_row, column=1, value="Akun").font = Font(bold=True)
    c2 = ws.cell(row=header_row, column=6, value=f"Nilai per {payload.get('tanggal')}")
    c3 = ws.cell(row=header_row, column=7, value=f"Nilai per {payload.get('tanggal_prev')}")
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


def build_aruskas_xlsx(payload: dict, branch_label: str) -> bytes:
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
    _money(r, payload.get("saldo_awal"))
    r += 1
    ws.cell(row=r, column=1, value="Saldo Kas & Setara Kas Akhir Periode").font = Font(bold=True)
    _money(r, payload.get("saldo_akhir"), bold=True)

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
        _money(r, 7, acc["saldo_awal"])
        r += 1
        # header kolom
        for col_idx, (title, _w) in enumerate(_GL_COLS, 1):
            c = ws.cell(row=r, column=col_idx, value=title)
            c.font = Font(bold=True, color="FFFF00")
            c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        r += 1
        for ln in acc["rows"]:
            ws.cell(row=r, column=1, value=ln["journal_date"])
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
        _money(r, 7, acc["saldo_akhir"], bold=True)
        r += 2

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Perubahan Dana ───────────────────────────────────────────────────────────


def build_perubahan_dana_xlsx(payload: dict, branch_label: str) -> bytes:
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
        for ln in f["penerimaan"]:
            ws.cell(row=r, column=1, value=f"   {ln['label']}")
            _money(r, ln["value"])
            r += 1
        ws.cell(row=r, column=1, value="Jumlah Penerimaan").font = Font(bold=True)
        _money(r, f["total_penerimaan"], bold=True)
        r += 1
        ws.cell(row=r, column=1, value="Penyaluran/Penggunaan").font = Font(bold=True, italic=True)
        r += 1
        for ln in f["penyaluran"]:
            ws.cell(row=r, column=1, value=f"   {ln['label']}")
            _money(r, ln["value"])
            r += 1
        ws.cell(row=r, column=1, value="Jumlah Penyaluran/Penggunaan").font = Font(bold=True)
        _money(r, f["total_penyaluran"], bold=True)
        r += 1
        ws.cell(row=r, column=1, value="Surplus (Defisit)").font = Font(bold=True)
        _money(r, f["surplus"], bold=True)
        r += 1
        ws.cell(row=r, column=1, value="Saldo Awal Dana")
        _money(r, f["saldo_awal"])
        r += 1
        ws.cell(row=r, column=1, value="Saldo Akhir Dana").font = Font(bold=True)
        _money(r, f["saldo_akhir"], bold=True)
        r += 2

    ws.cell(row=r, column=1, value="TOTAL SALDO AKHIR SELURUH DANA").font = Font(bold=True)
    _money(r, payload.get("total_saldo_akhir"), bold=True)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── Perubahan Dana Detail ────────────────────────────────────────────────────


def build_perubahan_dana_detail_xlsx(payload: dict, branch_label: str) -> bytes:
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

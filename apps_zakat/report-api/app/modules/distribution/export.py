"""Excel export untuk laporan Penyaluran (openpyxl)."""

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


def _header_row(ws, row_idx, title, branch_label, period_label):
    """Tulis header standar: judul + cabang + periode."""
    ws.cell(row=row_idx, column=1, value=title).font = Font(bold=True, size=14)
    ws.cell(row=row_idx + 1, column=1, value="Cabang").font = Font(bold=True)
    ws.cell(row=row_idx + 1, column=2, value=branch_label)
    ws.cell(row=row_idx + 2, column=1, value="Periode").font = Font(bold=True)
    ws.cell(row=row_idx + 2, column=2, value=period_label)
    return row_idx + 4


def _setup_columns(ws, header_row, cols: list[tuple[str, int, str | None]]):
    """Tulis header kolom dan set lebar."""
    for col_idx, (title, width, _fmt) in enumerate(cols, 1):
        c = ws.cell(row=header_row, column=col_idx, value=title)
        c.font = Font(bold=True, color="FFFF00")
        c.fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[get_column_letter(col_idx)].width = width
    ws.freeze_panes = f"A{header_row + 1}"


# ── 1. Laporan Proposal Masuk ─────────────────────────────────────────────────

_PROPOSAL_COLS: list[tuple[str, int, str | None]] = [
    ("Nama Mustahiq", 28),
    ("Jenis Program", 24),
    ("No Proposal", 20),
    ("Tgl Proposal", 14),
    ("Deskripsi", 36),
    ("Nominal", 18),
    ("Diterima Oleh", 18),
    ("Tgl Diterima", 14),
    ("Referensi", 18),
    ("Tgl Realisasi", 14),
    ("Nominal Realisasi", 18),
    ("No Memo", 16),
    ("Sumber Dana", 28),
]


def build_proposal_incoming_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    header_row = _header_row(ws, 1, "Laporan Proposal Masuk", "Semua", period_label)
    cols_short = [(t, w, None) for t, w in _PROPOSAL_COLS]
    _setup_columns(ws, header_row, cols_short)

    for i, r in enumerate(rows, start=header_row + 1):
        values = [
            r.get("mustahiq_name"),
            r.get("product_group_name"),
            r.get("proposal_no"),
            _dmy(r.get("proposal_date")),
            r.get("description"),
            float(r.get("nominal") or 0),
            r.get("received_by"),
            _dmy(r.get("received_date")),
            r.get("reference_by"),
            _dmy(r.get("realization_date")),
            float(r.get("realization_amount") or 0),
            r.get("memo_number"),
            " - ".join(p for p in [r.get("fund_source_no"), r.get("fund_source_name")] if p),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            if col_idx in [6, 11]:
                cell.number_format = "#,##0.00"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── 2. Laporan Daftar Mustahiq ────────────────────────────────────────────────

_MUSTAHIQ_COLS: list[tuple[str, int, str | None]] = [
    ("ID Mustahiq", 14),
    ("Nama", 28),
    ("Golongan", 14),
    ("Ashnaf", 18),
    ("Alamat", 32),
    ("Telepon", 16),
    ("Nama Kontak", 20),
    ("Telp Kontak", 16),
    ("HP Kontak", 16),
    ("Supervisor", 18),
    ("Tingkat Sekolah", 14),
    ("Sekolah", 28),
    ("Tgl Program", 13),
    ("Nama Program", 28),
    ("Rencana Distribusi", 18),
]


def build_mustahiq_list_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    header_row = _header_row(ws, 1, "Laporan Daftar Mustahiq", "Semua", period_label)
    cols_short = [(t, w, None) for t, w in _MUSTAHIQ_COLS]
    _setup_columns(ws, header_row, cols_short)

    for i, r in enumerate(rows, start=header_row + 1):
        values = [
            r.get("mustahiq_id"),
            r.get("customer_name"),
            r.get("mustahiq_type"),
            r.get("ashnaf_label"),
            " - ".join(p for p in [r.get("address_street"), r.get("address_kelurahan")] if p),
            r.get("phone_number"),
            r.get("cp_name"),
            r.get("cp_phone_number"),
            r.get("cp_mobile_number"),
            r.get("supervisor_name"),
            "",
            r.get("school_name"),
            _dmy(r.get("date_start")),
            r.get("product_name"),
            float(r.get("distribution_amount") or 0),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            if col_idx == 15:
                cell.number_format = "#,##0.00"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── 3. Laporan Realisasi Rutin (3 sheets) ────────────────────────────────────

_REAL_REG_COLS: list[tuple[str, int, str | None]] = [
    ("No", 5),
    ("Jenis Program", 24),
    ("Nama Program", 28),
    ("Tgl Realisasi", 14),
    ("Nama Mustahiq", 28),
    ("Alamat", 32),
    ("Nominal", 18),
    ("Piutang", 12),
    ("Status LPJ", 12),
    ("Nominal LPJ", 18),
    ("Anggaran", 28),
]


def build_realization_regular_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Detail"

    header_row = _header_row(ws, 1, "Laporan Program Penyaluran Rutin", "Semua", period_label)
    cols_short = [(t, w, None) for t, w in _REAL_REG_COLS]
    _setup_columns(ws, header_row, cols_short)

    for i, r in enumerate(rows, start=header_row + 1):
        values = [
            i - header_row,
            r.get("product_group_name"),
            r.get("product_name"),
            _dmy(r.get("realization_date")),
            r.get("customer_name"),
            r.get("address_street"),
            float(r.get("realization_amount") or 0),
            "Ya" if r.get("status_receivables") == "Y" else "Tidak",
            r.get("report_detail_status"),
            float(r.get("report_amount") or 0),
            " - ".join(p for p in [r.get("budget_code"), r.get("budget_item_description")] if p),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            if col_idx in [7, 10]:
                cell.number_format = "#,##0.00"

    # Sheet 2: Rekap per product_group
    ws_rekap = wb.create_sheet("Rekap")
    by_group = {}
    for r in rows:
        key = r.get("product_group_name")
        if key not in by_group:
            by_group[key] = 0.0
        by_group[key] += float(r.get("realization_amount") or 0)

    rekap_row = _header_row(ws_rekap, 1, "Rekap Program Penyaluran Rutin", "Semua", period_label)
    ws_rekap.cell(row=rekap_row, column=1, value="Jenis Program").font = Font(bold=True, color="FFFF00")
    ws_rekap.cell(row=rekap_row, column=1).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_rekap.cell(row=rekap_row, column=2, value="Jumlah").font = Font(bold=True, color="FFFF00")
    ws_rekap.cell(row=rekap_row, column=2).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_rekap.column_dimensions["A"].width = 32
    ws_rekap.column_dimensions["B"].width = 18

    for i, (group, total) in enumerate(sorted(by_group.items()), start=rekap_row + 1):
        ws_rekap.cell(row=i, column=1, value=group)
        c = ws_rekap.cell(row=i, column=2, value=total)
        c.number_format = "#,##0.00"

    # Sheet 3: Rekap Anggaran
    ws_anggaran = wb.create_sheet("RekapAnggaran")
    by_budget = {}
    for r in rows:
        key = " - ".join(p for p in [r.get("budget_code"), r.get("budget_item_description")] if p)
        if key not in by_budget:
            by_budget[key] = 0.0
        by_budget[key] += float(r.get("realization_amount") or 0)

    anggaran_row = _header_row(ws_anggaran, 1, "Rekap Anggaran Program Penyaluran Rutin", "Semua", period_label)
    ws_anggaran.cell(row=anggaran_row, column=1, value="Anggaran").font = Font(bold=True, color="FFFF00")
    ws_anggaran.cell(row=anggaran_row, column=1).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_anggaran.cell(row=anggaran_row, column=2, value="Jumlah").font = Font(bold=True, color="FFFF00")
    ws_anggaran.cell(row=anggaran_row, column=2).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_anggaran.column_dimensions["A"].width = 32
    ws_anggaran.column_dimensions["B"].width = 18

    for i, (budget, total) in enumerate(sorted(by_budget.items()), start=anggaran_row + 1):
        ws_anggaran.cell(row=i, column=1, value=budget)
        c = ws_anggaran.cell(row=i, column=2, value=total)
        c.number_format = "#,##0.00"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── 4. Laporan Realisasi Non Rutin (3 sheets) ─────────────────────────────────

_REAL_NONREG_COLS: list[tuple[str, int, str | None]] = [
    ("No", 5),
    ("Jenis Program", 24),
    ("Nama Program", 28),
    ("Tgl Realisasi", 14),
    ("Nama Mustahiq", 28),
    ("Alamat", 32),
    ("Nominal", 18),
    ("Sumber Dana", 16),
    ("Keterangan", 32),
    ("No Proposal", 18),
    ("Nilai Proposal", 18),
    ("Deskripsi Proposal", 28),
    ("Referensi", 18),
    ("Anggaran", 28),
]


def build_realization_non_regular_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Detail"

    header_row = _header_row(ws, 1, "Laporan Program Penyaluran Non Rutin", "Semua", period_label)
    cols_short = [(t, w, None) for t, w in _REAL_NONREG_COLS]
    _setup_columns(ws, header_row, cols_short)

    for i, r in enumerate(rows, start=header_row + 1):
        values = [
            i - header_row,
            r.get("product_group_name"),
            r.get("product_name"),
            _dmy(r.get("realization_date")),
            r.get("customer_name"),
            r.get("address_street"),
            float(r.get("realization_amount") or 0),
            r.get("account_name"),
            r.get("detail_description"),
            r.get("proposal_no"),
            float(r.get("proposal_nominal") or 0),
            r.get("proposal_description"),
            r.get("proposal_reference_by"),
            " - ".join(p for p in [r.get("budget_code"), r.get("budget_item_description")] if p),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            if col_idx in [7, 11]:
                cell.number_format = "#,##0.00"

    # Sheet 2: Rekap per product_group
    ws_rekap = wb.create_sheet("Rekap")
    by_group = {}
    for r in rows:
        key = r.get("product_group_name")
        if key not in by_group:
            by_group[key] = 0.0
        by_group[key] += float(r.get("realization_amount") or 0)

    rekap_row = _header_row(ws_rekap, 1, "Rekap Program Penyaluran Non Rutin", "Semua", period_label)
    ws_rekap.cell(row=rekap_row, column=1, value="Jenis Program").font = Font(bold=True, color="FFFF00")
    ws_rekap.cell(row=rekap_row, column=1).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_rekap.cell(row=rekap_row, column=2, value="Jumlah").font = Font(bold=True, color="FFFF00")
    ws_rekap.cell(row=rekap_row, column=2).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_rekap.column_dimensions["A"].width = 32
    ws_rekap.column_dimensions["B"].width = 18

    for i, (group, total) in enumerate(sorted(by_group.items()), start=rekap_row + 1):
        ws_rekap.cell(row=i, column=1, value=group)
        c = ws_rekap.cell(row=i, column=2, value=total)
        c.number_format = "#,##0.00"

    # Sheet 3: Rekap Anggaran
    ws_anggaran = wb.create_sheet("RekapAnggaran")
    by_budget = {}
    for r in rows:
        key = " - ".join(p for p in [r.get("budget_code"), r.get("budget_item_description")] if p)
        if key not in by_budget:
            by_budget[key] = 0.0
        by_budget[key] += float(r.get("realization_amount") or 0)

    anggaran_row = _header_row(ws_anggaran, 1, "Rekap Anggaran Program Penyaluran Non Rutin", "Semua", period_label)
    ws_anggaran.cell(row=anggaran_row, column=1, value="Anggaran").font = Font(bold=True, color="FFFF00")
    ws_anggaran.cell(row=anggaran_row, column=1).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_anggaran.cell(row=anggaran_row, column=2, value="Jumlah").font = Font(bold=True, color="FFFF00")
    ws_anggaran.cell(row=anggaran_row, column=2).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_anggaran.column_dimensions["A"].width = 32
    ws_anggaran.column_dimensions["B"].width = 18

    for i, (budget, total) in enumerate(sorted(by_budget.items()), start=anggaran_row + 1):
        ws_anggaran.cell(row=i, column=1, value=budget)
        c = ws_anggaran.cell(row=i, column=2, value=total)
        c.number_format = "#,##0.00"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── 5. Laporan Piutang Realisasi ──────────────────────────────────────────────

_RECEIVABLE_COLS: list[tuple[str, int, str | None]] = [
    ("No", 5),
    ("Tgl Realisasi", 14),
    ("No Memo", 16),
    ("Jenis", 14),
    ("Keterangan", 32),
    ("Nominal Realisasi", 18),
    ("Nominal LPJ", 18),
    ("Sisa Piutang", 18),
    ("Nama Karyawan", 20),
    ("Inputer Realisasi", 18),
    ("Inputer LPJ", 18),
]


def build_realization_receivable_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    header_row = _header_row(ws, 1, "Laporan Piutang Realisasi Penyaluran", "Semua", period_label)
    cols_short = [(t, w, None) for t, w in _RECEIVABLE_COLS]
    _setup_columns(ws, header_row, cols_short)

    for i, r in enumerate(rows, start=header_row + 1):
        realization_amt = float(r.get("realization_amount") or 0)
        report_amt = float(r.get("report_amount") or 0)
        sisa = realization_amt - report_amt
        values = [
            i - header_row,
            _dmy(r.get("realizationdate")),
            r.get("memo_number"),
            "Rutin" if r.get("realization_type") == "R" else "Non Rutin",
            r.get("realization_description"),
            realization_amt,
            report_amt,
            sisa,
            r.get("employee_name"),
            r.get("input_user"),
            r.get("report_user"),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            if col_idx in [6, 7, 8]:
                cell.number_format = "#,##0.00"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── 6. Laporan Pengembalian Realisasi ─────────────────────────────────────────

_RETURN_COLS: list[tuple[str, int, str | None]] = [
    ("No", 5),
    ("Tgl Pengembalian", 14),
    ("Nominal Realisasi", 18),
    ("Nominal Kembali", 18),
    ("Biaya", 32),
    ("No Memo", 16),
    ("Keterangan", 32),
    ("Input Oleh", 16),
]


def build_realization_return_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Data"

    header_row = _header_row(ws, 1, "Laporan Pengembalian Realisasi", "Semua", period_label)
    cols_short = [(t, w, None) for t, w in _RETURN_COLS]
    _setup_columns(ws, header_row, cols_short)

    # Group rows by return_id
    by_return = {}
    for r in rows:
        rid = r.get("return_id")
        if rid not in by_return:
            by_return[rid] = {"header": r, "costs": []}
        if r.get("cost_item_description"):
            by_return[rid]["costs"].append(r)

    row_num = 0
    for i, (return_id, data) in enumerate(by_return.items(), 1):
        row_num += 1
        r = data["header"]
        values = [
            i,
            _dmy(r.get("return_date")),
            float(r.get("realization_amount") or 0),
            float(r.get("return_amount") or 0),
            "",
            r.get("memo_number"),
            r.get("return_description"),
            r.get("input_user"),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=header_row + row_num, column=col_idx, value=val)
            if col_idx in [3, 4]:
                cell.number_format = "#,##0.00"

        for cost in data["costs"]:
            row_num += 1
            cost_values = [
                "",
                "",
                "",
                "",
                f"{cost.get('cost_item_description')} - {float(cost.get('cost_amount') or 0)}",
                "",
                "",
                "",
            ]
            for col_idx, val in enumerate(cost_values, 1):
                ws.cell(row=header_row + row_num, column=col_idx, value=val)

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ── 7. Laporan Penyaluran Per Mustahiq (2 sheets) ────────────────────────────

_MUSTAHIQ_DETAIL_COLS: list[tuple[str, int, str | None]] = [
    ("No", 5),
    ("Nama Mustahiq", 28),
    ("Alamat", 32),
    ("Tgl Realisasi", 14),
    ("Jenis Program", 24),
    ("Nama Program", 28),
    ("Nominal", 18),
    ("Sumber Dana", 16),
    ("Keterangan", 32),
    ("No Proposal", 18),
    ("Nilai Proposal", 18),
    ("Deskripsi Proposal", 28),
    ("Referensi", 18),
    ("Anggaran", 28),
]


def build_realization_by_mustahiq_xlsx(rows: list[dict], period_label: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Detail"

    header_row = _header_row(ws, 1, "Laporan Penyaluran Per Mustahiq", "Semua", period_label)
    cols_short = [(t, w, None) for t, w in _MUSTAHIQ_DETAIL_COLS]
    _setup_columns(ws, header_row, cols_short)

    for i, r in enumerate(rows, start=header_row + 1):
        values = [
            i - header_row,
            r.get("customer_name"),
            r.get("address_street"),
            _dmy(r.get("realization_date")),
            r.get("product_group_name"),
            r.get("product_name"),
            float(r.get("realization_amount") or 0),
            r.get("account_name"),
            r.get("detail_description"),
            r.get("proposal_no"),
            float(r.get("proposal_nominal") or 0),
            r.get("proposal_description"),
            r.get("proposal_reference_by"),
            " - ".join(p for p in [r.get("budget_code"), r.get("budget_item_description")] if p),
        ]
        for col_idx, val in enumerate(values, 1):
            cell = ws.cell(row=i, column=col_idx, value=val)
            if col_idx in [7, 11]:
                cell.number_format = "#,##0.00"

    # Sheet 2: Rekap per mustahiq
    ws_rekap = wb.create_sheet("Rekap")
    by_customer = {}
    for r in rows:
        key = r.get("customer_name")
        if key not in by_customer:
            by_customer[key] = 0.0
        by_customer[key] += float(r.get("realization_amount") or 0)

    rekap_row = _header_row(ws_rekap, 1, "Rekap Penyaluran Per Mustahiq", "Semua", period_label)
    ws_rekap.cell(row=rekap_row, column=1, value="Nama Mustahiq").font = Font(bold=True, color="FFFF00")
    ws_rekap.cell(row=rekap_row, column=1).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_rekap.cell(row=rekap_row, column=2, value="Jumlah").font = Font(bold=True, color="FFFF00")
    ws_rekap.cell(row=rekap_row, column=2).fill = PatternFill(start_color="0000FF", end_color="0000FF", fill_type="solid")
    ws_rekap.column_dimensions["A"].width = 32
    ws_rekap.column_dimensions["B"].width = 18

    for i, (customer, total) in enumerate(sorted(by_customer.items()), start=rekap_row + 1):
        ws_rekap.cell(row=i, column=1, value=customer)
        c = ws_rekap.cell(row=i, column=2, value=total)
        c.number_format = "#,##0.00"

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

from __future__ import annotations
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


HEADERS = [
    'NoRekening', 'Tanggal (DD/MM/YYYY)', 'Keterangan', 'NoRef', 'TotalKredit',
    'ZakatProfesi', 'ZakatMaal', 'ZakatFitrah', 'ZakatPerusahaan',
    'Infaq', 'InfaqTerikat', 'DPU', 'AnakYatim', 'AnakAsuh',
    'TitipanWakaf', 'TitipanQurban', 'Qurban', 'NonHalal', 'Fidyah',
]

# Contoh data — TotalKredit harus = sum semua kolom produk
_SAMPLE_ROWS = [
    # NoRekening, Tanggal, Keterangan, NoRef, TotalKredit,
    # ZakatProfesi, ZakatMaal, ZakatFitrah, ZakatPerusahaan,
    # Infaq, InfaqTerikat, DPU, AnakYatim, AnakAsuh,
    # TitipanWakaf, TitipanQurban, Qurban, NonHalal, Fidyah
    (
        'BANK0001', '01/06/2026', 'Zakat profesi bulan Mei', 'REF-001', 500_000,
        300_000, 200_000, 0, 0,
        0, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ),
    (
        'BANK0001', '02/06/2026', 'Infaq rutin', 'REF-002', 250_000,
        0, 0, 0, 0,
        250_000, 0, 0, 0, 0,
        0, 0, 0, 0, 0,
    ),
    (
        'BANK0002', '03/06/2026', 'Donasi campuran', 'REF-003', 1_000_000,
        500_000, 0, 0, 0,
        200_000, 0, 0, 150_000, 150_000,
        0, 0, 0, 0, 0,
    ),
    (
        'BANK0003', '04/06/2026', 'Titipan wakaf & qurban', '', 750_000,
        0, 0, 0, 0,
        0, 0, 0, 0, 0,
        500_000, 250_000, 0, 0, 0,
    ),
]


def build_template() -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = 'UploadPenghimpunan'

    # ── Baris instruksi (row 1) ──────────────────────────────────────────────
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(HEADERS))
    instr_cell = ws.cell(row=1, column=1,
        value=(
            'PETUNJUK: Isi data mulai baris 4. Hapus baris contoh (baris 3) sebelum upload. '
            'TotalKredit harus = jumlah seluruh kolom produk. Format tanggal: DD/MM/YYYY.'
        ))
    instr_cell.font = Font(italic=True, color='374151', size=9)
    instr_cell.fill = PatternFill('solid', fgColor='FEF9C3')  # kuning muda
    instr_cell.alignment = Alignment(wrap_text=True)
    ws.row_dimensions[1].height = 32

    # ── Header kolom (row 2) ─────────────────────────────────────────────────
    header_fill = PatternFill('solid', fgColor='1E40AF')
    header_font = Font(bold=True, color='FFFFFF')
    thin = Side(style='thin', color='FFFFFF')
    header_border = Border(left=thin, right=thin)
    for col_idx, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=2, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', wrap_text=True)
        cell.border = header_border
    ws.row_dimensions[2].height = 30

    # ── Baris contoh (row 3 dst) ─────────────────────────────────────────────
    sample_fill = PatternFill('solid', fgColor='EFF6FF')   # biru sangat muda
    sample_font = Font(color='1E3A8A', italic=True)        # biru gelap, italic
    label_font  = Font(color='9CA3AF', italic=True, size=8)

    for r_idx, row_data in enumerate(_SAMPLE_ROWS, 3):
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.fill = sample_fill
            cell.font = sample_font
            # Kolom angka: rata kanan + format ribuan
            if c_idx >= 5:
                cell.alignment = Alignment(horizontal='right')
                if isinstance(val, (int, float)):
                    cell.number_format = '#,##0'
        # Label "CONTOH" di kolom A baris pertama sample
        if r_idx == 3:
            ws.cell(row=r_idx, column=1).comment = None  # bersihkan kalau ada

    # Label kecil di kiri bawah area sample
    label_row = 3 + len(_SAMPLE_ROWS)
    lbl = ws.cell(row=label_row, column=1, value='↑ Hapus baris contoh sebelum upload')
    lbl.font = label_font

    # ── Lebar kolom ─────────────────────────────────────────────────────────
    ws.column_dimensions['A'].width = 20   # NoRekening
    ws.column_dimensions['B'].width = 20   # Tanggal
    ws.column_dimensions['C'].width = 35   # Keterangan
    ws.column_dimensions['D'].width = 15   # NoRef
    for col in range(5, len(HEADERS) + 1):
        ws.column_dimensions[chr(64 + col)].width = 14

    # Freeze panes: scroll ke kanan tapi header & rekening tetap
    ws.freeze_panes = 'E3'

    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

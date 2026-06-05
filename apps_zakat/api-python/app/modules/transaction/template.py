from __future__ import annotations
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


HEADERS = [
    'NoRekening', 'Tanggal (DD/MM/YYYY)', 'Keterangan', 'NoRef', 'TotalKredit',
    'ZakatProfesi', 'ZakatMaal', 'ZakatFitrah', 'ZakatPerusahaan',
    'Infaq', 'InfaqTerikat', 'DPU', 'AnakYatim', 'AnakAsuh',
    'TitipanWakaf', 'TitipanQurban', 'Qurban', 'NonHalal', 'Fidyah',
]


def build_template() -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = 'UploadPenghimpunan'
    header_fill = PatternFill('solid', fgColor='1E40AF')
    header_font = Font(bold=True, color='FFFFFF')
    for col_idx, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 35
    ws.column_dimensions['D'].width = 15
    for col in range(5, len(HEADERS) + 1):
        ws.column_dimensions[chr(64 + col)].width = 14
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

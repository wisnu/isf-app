from __future__ import annotations
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from app.modules.finance.inquiry.transaction_history.schema import TransactionRow

_HEADERS = [
    'No Transaksi', 'Rekening', 'Tgl Transaksi', 'Tgl Aktual',
    'Nominal', 'No Donatur', 'Nama Donatur', 'No Ref',
    'Keterangan', 'Inputer', 'Auth Status', 'Posted', 'Cabang',
]


def _dmy(iso: str | None) -> str:
    if not iso or len(iso) < 10:
        return iso or ''
    return f'{iso[8:10]}-{iso[5:7]}-{iso[:4]}'


def build_histori_xlsx(rows: list[TransactionRow], begin: str, end: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = 'HistoriTransaksi'
    hfill = PatternFill('solid', fgColor='1E40AF')
    hfont = Font(bold=True, color='FFFFFF')
    for ci, h in enumerate(_HEADERS, 1):
        cell = ws.cell(row=1, column=ci, value=h)
        cell.fill = hfill
        cell.font = hfont
        cell.alignment = Alignment(horizontal='center')
    for i, r in enumerate(rows, start=2):
        ws.cell(row=i, column=1,  value=r.transaction_no or '')
        ws.cell(row=i, column=2,  value=r.channel_name or r.channel_account_no or '')
        ws.cell(row=i, column=3,  value=_dmy(r.transaction_date))
        ws.cell(row=i, column=4,  value=_dmy(r.actual_date))
        ws.cell(row=i, column=5,  value=r.amount)
        ws.cell(row=i, column=6,  value=r.donor_no or '')
        ws.cell(row=i, column=7,  value=r.donor_name or '')
        ws.cell(row=i, column=8,  value=r.reference_no or '')
        ws.cell(row=i, column=9,  value=r.description or '')
        ws.cell(row=i, column=10, value=r.inputer or '')
        ws.cell(row=i, column=11, value=r.auth_status or '')
        ws.cell(row=i, column=12, value=r.is_posted or '')
        ws.cell(row=i, column=13, value=r.branch_code or '')
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()

from __future__ import annotations
import io
from .schema import HistoryResult

_AR_TYPE_LABEL = {'E': 'Karyawan', 'D': 'Non Karyawan'}


def build_xlsx(result: HistoryResult, begin: str, end: str) -> bytes:
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill
    except ImportError:
        raise RuntimeError('openpyxl not installed')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Riwayat Piutang'

    def bold(cell):
        cell.font = Font(bold=True)

    period = begin if begin == end else f'{begin} s/d {end}'
    ar_label = _AR_TYPE_LABEL.get(result.ar_type, result.ar_type)

    ws['A1'] = 'Rekening'
    ws['B1'] = f'{result.account_no} — {result.account_name} ({ar_label})'
    bold(ws['A1'])
    ws['A2'] = 'Periode'
    ws['B2'] = period
    bold(ws['A2'])
    ws['A3'] = 'Saldo Awal'
    ws['B3'] = result.beginning_balance
    bold(ws['A3'])

    headers = ['Tanggal', 'Kode Transaksi', 'No. Transaksi', 'Debet', 'Kredit', 'Saldo', 'Keterangan', 'Ref', 'Inputer', 'Status']
    header_row = 5
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col, value=h)
        cell.font = Font(bold=True)
        cell.fill = PatternFill('solid', fgColor='DDEEFF')

    for i, row in enumerate(result.rows, header_row + 1):
        ws.cell(row=i, column=1,  value=row.actual_date)
        ws.cell(row=i, column=2,  value=row.transaction_code or '')
        ws.cell(row=i, column=3,  value=row.transaction_no or '')
        ws.cell(row=i, column=4,  value=row.debet if row.debet else None)
        ws.cell(row=i, column=5,  value=row.kredit if row.kredit else None)
        ws.cell(row=i, column=6,  value=row.running_balance)
        ws.cell(row=i, column=7,  value=row.description or '')
        ws.cell(row=i, column=8,  value=row.reference_no or '')
        ws.cell(row=i, column=9,  value=row.inputer or '')
        ws.cell(row=i, column=10, value=row.auth_status)

    footer_row = header_row + len(result.rows) + 2
    ws.cell(row=footer_row, column=1, value='Total').font = Font(bold=True)
    ws.cell(row=footer_row, column=4, value=result.total_debet).font = Font(bold=True)
    ws.cell(row=footer_row, column=5, value=result.total_kredit).font = Font(bold=True)
    ws.cell(row=footer_row, column=6, value=result.ending_balance).font = Font(bold=True)

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()

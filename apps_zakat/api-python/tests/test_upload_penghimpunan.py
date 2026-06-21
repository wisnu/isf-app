from __future__ import annotations
import io
from openpyxl import Workbook
from app.modules.finance.transaction._shared.parse import parse_xlsx, parse_xls, _parse_date_dmy


def _make_xlsx(rows: list[list]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.append(['NoRek','Tanggal','Ket','Ref','Total','ZP','ZM','ZF','ZPer',
               'Infaq','InfaqT','DPU','AY','AA','TW','TQ','Qurban','NH','Fidyah'])
    for r in rows:
        ws.append(r)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_parse_date_dmy_valid():
    assert _parse_date_dmy('01/06/2026') == '2026-06-01'


def test_parse_date_dmy_invalid():
    assert _parse_date_dmy('2026-06-01') is None
    assert _parse_date_dmy('32/01/2026') is None
    assert _parse_date_dmy('') is None


def test_parse_xlsx_valid_row():
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Transfer zakat', 'REF001', 500000,
         300000, 200000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert len(rows) == 1
    assert rows[0].status == 'valid'
    assert rows[0].tanggal == '2026-06-01'
    assert rows[0].total_kredit == 500000
    assert rows[0].zakat_profesi == 300000
    assert rows[0].zakat_maal == 200000


def test_parse_xlsx_invalid_date():
    data = _make_xlsx([
        ['1234567890', 'bukan-tanggal', 'Transfer', 'REF001', 500000,
         500000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert rows[0].status == 'invalid'
    assert 'tanggal' in rows[0].pesan.lower()


def test_parse_xlsx_unknown_account():
    data = _make_xlsx([
        ['9999999', '01/06/2026', 'Transfer', 'REF001', 100000,
         100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts=set(), seen_refs=set())
    assert rows[0].status == 'invalid'
    assert 'rekening' in rows[0].pesan.lower()


def test_parse_xlsx_total_mismatch_gives_warning():
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Transfer', 'REF001', 500000,
         200000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert rows[0].status == 'warning'
    assert 'nominal' in rows[0].pesan.lower()


def test_parse_xlsx_skips_zero_kredit():
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Zero', 'REF001', 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert rows == []


def test_parse_xlsx_duplicate_ref_gives_warning():
    seen: set = {('REF001', '2026-06-01', 100000.0)}
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Transfer', 'REF001', 100000,
         100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=seen)
    assert rows[0].status == 'warning'
    assert 'pernah' in rows[0].pesan.lower()

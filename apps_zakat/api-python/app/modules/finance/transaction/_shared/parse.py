from __future__ import annotations

import re
from datetime import datetime
from io import BytesIO

from app.modules.finance.upload.collection.schema import PRODUCT_KEYS, ParsedRow


def _to_float(v: object) -> float:
    if v is None or v == '':
        return 0.0
    try:
        return float(str(v).replace(',', ''))
    except (ValueError, TypeError):
        return 0.0


def _parse_date_dmy(raw: object) -> str | None:
    """DD/MM/YYYY → ISO YYYY-MM-DD. Returns None if invalid."""
    s = str(raw).strip() if raw else ''
    m = re.fullmatch(r'(\d{1,2})/(\d{1,2})/(\d{4})', s)
    if not m:
        return None
    d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        datetime(y, mo, d)
        return f'{y:04d}-{mo:02d}-{d:02d}'
    except ValueError:
        return None


def _validate_row(
    row_no: int,
    cols: list,
    known_accounts: set[str],
    seen_refs: set[tuple],
) -> ParsedRow | None:
    """Parse + validate one row. Returns None if TotalKredit <= 0 (skip)."""
    def col(i: int) -> object:
        return cols[i] if i < len(cols) else None

    total_kredit = _to_float(col(4))
    if total_kredit <= 0:
        return None

    no_rekening = str(col(0) or '').strip()
    tanggal_raw = col(1)
    keterangan = str(col(2) or '').strip()
    no_ref = str(col(3) or '').strip()

    amounts = [_to_float(col(5 + i)) for i in range(14)]
    (zp, zm, zf, zper, infaq, infaq_t, dpu,
     ay, aa, tw, tq, qurban, nh, fidyah) = amounts

    status = 'valid'
    msgs: list[str] = []

    tanggal_iso = _parse_date_dmy(tanggal_raw)
    if tanggal_iso is None:
        status = 'invalid'
        msgs.append('Format tanggal tidak valid')

    if no_rekening not in known_accounts:
        status = 'invalid'
        msgs.append('Nomor rekening tidak terdaftar')

    detail_sum = sum(amounts)
    if abs(detail_sum - total_kredit) > 0.01:
        if status == 'valid':
            status = 'warning'
        msgs.append('Total detail tidak sesuai nominal')

    ref_key = (no_ref, tanggal_iso or '', total_kredit)
    if ref_key in seen_refs:
        if status == 'valid':
            status = 'warning'
        msgs.append('Sudah pernah di-upload')
    else:
        seen_refs.add(ref_key)

    pesan = '; '.join(msgs) if msgs else ''

    return ParsedRow(
        row_no=row_no,
        no_rekening=no_rekening,
        tanggal=tanggal_iso or '',
        keterangan=keterangan,
        no_ref=no_ref,
        total_kredit=total_kredit,
        zakat_profesi=zp, zakat_maal=zm, zakat_fitrah=zf,
        zakat_perusahaan=zper, infaq=infaq, infaq_terikat=infaq_t,
        dpu=dpu, anak_yatim=ay, anak_asuh=aa,
        titipan_wakaf=tw, titipan_qurban=tq,
        qurban=qurban, non_halal=nh, fidyah=fidyah,
        status=status, pesan=pesan,
    )


def parse_xlsx(data: bytes, known_accounts: set[str],
               seen_refs: set[tuple]) -> list[ParsedRow]:
    from openpyxl import load_workbook
    wb = load_workbook(BytesIO(data), read_only=True, data_only=True)
    ws = wb.active
    rows: list[ParsedRow] = []
    consecutive_empty = 0
    for excel_row_no, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        cols = list(row)
        if not cols or (cols[0] is None and (len(cols) < 2 or cols[1] is None)):
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break
            continue
        consecutive_empty = 0
        parsed = _validate_row(excel_row_no, cols, known_accounts, seen_refs)
        if parsed is not None:
            rows.append(parsed)
    wb.close()
    return rows


def parse_xls(data: bytes, known_accounts: set[str],
              seen_refs: set[tuple]) -> list[ParsedRow]:
    import xlrd
    wb = xlrd.open_workbook(file_contents=data)
    ws = wb.sheet_by_index(0)
    rows: list[ParsedRow] = []
    consecutive_empty = 0
    for r in range(1, ws.nrows):  # skip header row 0
        raw_cols = [ws.cell_value(r, c) for c in range(ws.ncols)]
        if not raw_cols or (raw_cols[0] == '' and (len(raw_cols) < 2 or raw_cols[1] == '')):
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break
            continue
        consecutive_empty = 0
        date_val = raw_cols[1] if len(raw_cols) > 1 else None
        if isinstance(date_val, float):
            try:
                t = xlrd.xldate_as_tuple(date_val, wb.datemode)
                raw_cols[1] = f'{t[2]:02d}/{t[1]:02d}/{t[0]:04d}'
            except Exception:
                pass
        parsed = _validate_row(r + 1, raw_cols, known_accounts, seen_refs)
        if parsed is not None:
            rows.append(parsed)
    return rows


def parse_file(filename: str, data: bytes,
               known_accounts: set[str],
               seen_refs: set[tuple]) -> list[ParsedRow]:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext == 'xlsx':
        return parse_xlsx(data, known_accounts, seen_refs)
    elif ext == 'xls':
        return parse_xls(data, known_accounts, seen_refs)
    else:
        raise ValueError(f'Format tidak didukung: {ext}. Gunakan .xls atau .xlsx')

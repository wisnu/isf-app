"""Parser for HC ZIS Excel upload files."""
from __future__ import annotations

from io import BytesIO
from openpyxl import load_workbook
import xlrd

from .schema import HCZisItem, HCZisTotals, HCZisParseResult


def _to_float(v: object) -> float:
    """Convert value to float, handling None and string formats."""
    if v is None or v == "":
        return 0.0
    try:
        return float(str(v).replace(",", ""))
    except (ValueError, TypeError):
        return 0.0


def _normalize_gender(raw: str) -> str:
    """Map MALE/FEMALE to L/P."""
    if not raw:
        return ""
    s = str(raw).strip().upper()
    if "MALE" in s:
        return "L" if "MALE" in s and "FEMALE" not in s else "P"
    return ""


def _normalize_marital_status(raw: str) -> str:
    """Map MARRD./SINGLE/DIVC./WIDOW/WDOWER to K/B/S."""
    if not raw:
        return ""
    s = str(raw).strip().upper()
    if "MARR" in s:
        return "K"
    elif "SINGLE" in s:
        return "B"
    elif "DIVC" in s or "WIDOW" in s or "WDOWER" in s:
        return "S"
    return ""


def parse_hc_zis_xlsx(data: bytes) -> HCZisParseResult:
    """Parse .xlsx file using openpyxl.

    Cell B2 = batch_period_desc
    Data rows start from ROW 8 (0-indexed: row 7)
    Columns are 0-indexed (col 0 = A, col 1 = B, etc.)
    """
    wb = load_workbook(BytesIO(data), data_only=True)
    ws = wb.active

    # Read batch_period_desc from cell B2 (row 2, col 1 in 0-indexed)
    batch_period_desc = str(ws.cell(2, 2).value or "").strip()
    if not batch_period_desc:
        raise ValueError("Periode batch (cell B2) tidak ditemukan di file")

    items: list[HCZisItem] = []
    data_no = 0

    # Start from row 8 (1-indexed) = row 7 (0-indexed) + 1
    for row_num in range(8, ws.max_row + 1):
        # Column 3 (1-indexed) = col 2 (0-indexed) = BusinessAreaCode
        # But employee_number is col 6 (1-indexed) = col 5 (0-indexed)
        # Stop if employee_number is empty
        employee_number_cell = ws.cell(row_num, 6).value
        if not employee_number_cell:
            break

        # Map columns (1-indexed, per spec):
        # col 3 = BusinessAreaCode, col 4 = BusinessAreaDesc
        # col 6 = EmployeeNumber (NIP), col 8 = EmployeeName
        # col 10 = BirthPlace, col 11 = WorkAreaName, col 12 = MobilePhone
        # col 13 = BirthDate, col 14 = Gender, col 15 = MaritalStatus
        # col 16 = Position, col 17 = OrganizationUnit
        # col 18-23 = amounts (Zakat, Infaq, AnakAsuh, AnakYatim, Wakaf, Taqurma)
        # All amounts are negated in file, so multiply by -1

        data_no += 1
        business_area_code = str(ws.cell(row_num, 3).value or "").strip()
        business_area_desc = str(ws.cell(row_num, 4).value or "").strip()
        employee_number = str(employee_number_cell or "").strip()
        employee_name = str(ws.cell(row_num, 8).value or "").strip()
        birth_place = str(ws.cell(row_num, 10).value or "").strip()
        work_area_name = str(ws.cell(row_num, 11).value or "").strip()
        mobile_phone = str(ws.cell(row_num, 12).value or "").strip()
        birth_date = str(ws.cell(row_num, 13).value or "").strip()
        gender = _normalize_gender(ws.cell(row_num, 14).value)
        marital_status = _normalize_marital_status(ws.cell(row_num, 15).value)
        position = str(ws.cell(row_num, 16).value or "").strip()
        organization_unit = str(ws.cell(row_num, 17).value or "").strip()

        # Amounts: cols 18-23 (1-indexed) = multiply by -1
        zakat_amount = _to_float(ws.cell(row_num, 18).value) * -1
        infaq_amount = _to_float(ws.cell(row_num, 19).value) * -1
        anak_asuh_amount = _to_float(ws.cell(row_num, 20).value) * -1
        anak_yatim_amount = _to_float(ws.cell(row_num, 21).value) * -1
        wakaf_amount = _to_float(ws.cell(row_num, 22).value) * -1
        taqurma_amount = _to_float(ws.cell(row_num, 23).value) * -1

        total_amount = (
            zakat_amount + infaq_amount + anak_asuh_amount +
            anak_yatim_amount + wakaf_amount + taqurma_amount
        )

        item = HCZisItem(
            data_no=data_no,
            business_area_code=business_area_code,
            business_area_desc=business_area_desc,
            employee_number=employee_number,
            employee_name=employee_name,
            birth_place=birth_place,
            work_area_name=work_area_name,
            mobile_phone=mobile_phone,
            birth_date=birth_date,
            gender=gender,
            marital_status=marital_status,
            position=position,
            organization_unit=organization_unit,
            zakat_amount=zakat_amount,
            infaq_amount=infaq_amount,
            anak_asuh_amount=anak_asuh_amount,
            anak_yatim_amount=anak_yatim_amount,
            wakaf_amount=wakaf_amount,
            taqurma_amount=taqurma_amount,
            total_amount=total_amount,
        )
        items.append(item)

    # Compute totals
    totals = HCZisTotals()
    for item in items:
        if item.zakat_amount != 0:
            totals.zakat_amount += item.zakat_amount
            totals.zakat_count += 1
        if item.infaq_amount != 0:
            totals.infaq_amount += item.infaq_amount
            totals.infaq_count += 1
        if item.anak_asuh_amount != 0:
            totals.anak_asuh_amount += item.anak_asuh_amount
            totals.anak_asuh_count += 1
        if item.anak_yatim_amount != 0:
            totals.anak_yatim_amount += item.anak_yatim_amount
            totals.anak_yatim_count += 1
        if item.wakaf_amount != 0:
            totals.wakaf_amount += item.wakaf_amount
            totals.wakaf_count += 1
        if item.taqurma_amount != 0:
            totals.taqurma_amount += item.taqurma_amount
            totals.taqurma_count += 1

    totals.grand_total = (
        totals.zakat_amount + totals.infaq_amount + totals.anak_asuh_amount +
        totals.anak_yatim_amount + totals.wakaf_amount + totals.taqurma_amount
    )
    totals.grand_count = len(items)

    return HCZisParseResult(
        batch_period_desc=batch_period_desc,
        totals=totals,
        items=items,
        is_duplicate=False,
    )


def parse_hc_zis_xls(data: bytes) -> HCZisParseResult:
    """Parse .xls file using xlrd.

    Same column mapping as .xlsx version.
    """
    book = xlrd.open_workbook(file_contents=data)
    sheet = book.sheet_by_index(0)

    # Read batch_period_desc from cell B2 (row 1, col 1 in 0-indexed)
    batch_period_desc = str(sheet.cell_value(1, 1) or "").strip()
    if not batch_period_desc:
        raise ValueError("Periode batch (cell B2) tidak ditemukan di file")

    items: list[HCZisItem] = []
    data_no = 0

    # Start from row 8 (1-indexed) = row 7 (0-indexed)
    for row_num in range(7, sheet.nrows):
        # Column 6 (1-indexed) = col 5 (0-indexed) = EmployeeNumber
        employee_number_cell = sheet.cell_value(row_num, 5)
        if not employee_number_cell:
            break

        data_no += 1
        business_area_code = str(sheet.cell_value(row_num, 2) or "").strip()
        business_area_desc = str(sheet.cell_value(row_num, 3) or "").strip()
        employee_number = str(employee_number_cell or "").strip()
        employee_name = str(sheet.cell_value(row_num, 7) or "").strip()
        birth_place = str(sheet.cell_value(row_num, 9) or "").strip()
        work_area_name = str(sheet.cell_value(row_num, 10) or "").strip()
        mobile_phone = str(sheet.cell_value(row_num, 11) or "").strip()
        birth_date = str(sheet.cell_value(row_num, 12) or "").strip()
        gender = _normalize_gender(sheet.cell_value(row_num, 13))
        marital_status = _normalize_marital_status(sheet.cell_value(row_num, 14))
        position = str(sheet.cell_value(row_num, 15) or "").strip()
        organization_unit = str(sheet.cell_value(row_num, 16) or "").strip()

        # Amounts: cols 18-23 (1-indexed) = cols 17-22 (0-indexed)
        zakat_amount = _to_float(sheet.cell_value(row_num, 17)) * -1
        infaq_amount = _to_float(sheet.cell_value(row_num, 18)) * -1
        anak_asuh_amount = _to_float(sheet.cell_value(row_num, 19)) * -1
        anak_yatim_amount = _to_float(sheet.cell_value(row_num, 20)) * -1
        wakaf_amount = _to_float(sheet.cell_value(row_num, 21)) * -1
        taqurma_amount = _to_float(sheet.cell_value(row_num, 22)) * -1

        total_amount = (
            zakat_amount + infaq_amount + anak_asuh_amount +
            anak_yatim_amount + wakaf_amount + taqurma_amount
        )

        item = HCZisItem(
            data_no=data_no,
            business_area_code=business_area_code,
            business_area_desc=business_area_desc,
            employee_number=employee_number,
            employee_name=employee_name,
            birth_place=birth_place,
            work_area_name=work_area_name,
            mobile_phone=mobile_phone,
            birth_date=birth_date,
            gender=gender,
            marital_status=marital_status,
            position=position,
            organization_unit=organization_unit,
            zakat_amount=zakat_amount,
            infaq_amount=infaq_amount,
            anak_asuh_amount=anak_asuh_amount,
            anak_yatim_amount=anak_yatim_amount,
            wakaf_amount=wakaf_amount,
            taqurma_amount=taqurma_amount,
            total_amount=total_amount,
        )
        items.append(item)

    # Compute totals
    totals = HCZisTotals()
    for item in items:
        if item.zakat_amount != 0:
            totals.zakat_amount += item.zakat_amount
            totals.zakat_count += 1
        if item.infaq_amount != 0:
            totals.infaq_amount += item.infaq_amount
            totals.infaq_count += 1
        if item.anak_asuh_amount != 0:
            totals.anak_asuh_amount += item.anak_asuh_amount
            totals.anak_asuh_count += 1
        if item.anak_yatim_amount != 0:
            totals.anak_yatim_amount += item.anak_yatim_amount
            totals.anak_yatim_count += 1
        if item.wakaf_amount != 0:
            totals.wakaf_amount += item.wakaf_amount
            totals.wakaf_count += 1
        if item.taqurma_amount != 0:
            totals.taqurma_amount += item.taqurma_amount
            totals.taqurma_count += 1

    totals.grand_total = (
        totals.zakat_amount + totals.infaq_amount + totals.anak_asuh_amount +
        totals.anak_yatim_amount + totals.wakaf_amount + totals.taqurma_amount
    )
    totals.grand_count = len(items)

    return HCZisParseResult(
        batch_period_desc=batch_period_desc,
        totals=totals,
        items=items,
        is_duplicate=False,
    )


def parse_hc_zis_file(filename: str, data: bytes) -> HCZisParseResult:
    """Parse HC ZIS file based on extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "xlsx":
        return parse_hc_zis_xlsx(data)
    elif ext == "xls":
        return parse_hc_zis_xls(data)
    else:
        raise ValueError(f"Format file tidak didukung: .{ext}")

"""Service for fundraising export operations.

Generates Excel files for two export types:
1. HC Batch export (9 columns)
2. Website (date-range) export (32 columns with product pivot)
"""

from __future__ import annotations

import io
from datetime import date
from decimal import Decimal

from fastapi import HTTPException

from app.modules.fundraising.export_schema import HCBatchOption
from app.shared.db import fetch_all, fetch_one, get_pool


# ── HC Batch Dropdown ──────────────────────────────────────────────────────────


async def list_hc_batches() -> list[HCBatchOption]:
    """List HC batches for dropdown selection.

    Query: fund.humancapitalbatch (transaction schema)
    Return: [id, name/description, batch_date] sorted by date DESC
    """
    rows = await fetch_all(
        """
        SELECT
          batchid AS id,
          COALESCE(batchperioddesc, description, 'Batch') AS name,
          CAST(transactiondate AS DATE) AS batch_date
        FROM transaction.humancapitalbatch
        ORDER BY transactiondate DESC, batchid DESC
        LIMIT 1000
        """
    )
    return [HCBatchOption(
        id=r["id"],
        name=r["name"],
        batch_date=r["batch_date"]
    ) for r in rows]


# ── HC Batch Export ───────────────────────────────────────────────────────────


async def export_hc_batch(batch_id: int) -> bytes:
    """Export HC Batch to Excel (9 columns) via dwh.v_export_penghimpunan_hc_batch."""
    batch = await fetch_one(
        "SELECT batchid FROM transaction.humancapitalbatch WHERE batchid = CAST($1 AS INTEGER)",
        batch_id
    )
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    rows = await fetch_all(
        """
        SELECT batch_id, batch_name, batch_date, donor_number, donor_name,
               product_code, product_name, donation_amount, donation_date
        FROM dwh.v_export_penghimpunan_hc_batch
        WHERE batch_id = CAST($1 AS INTEGER)
        ORDER BY donation_date, donor_number
        """,
        batch_id
    )

    # Generate Excel
    try:
        import openpyxl
        from openpyxl.styles import Alignment, Font, PatternFill
    except ImportError:
        raise RuntimeError("openpyxl not installed")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Donation List"

    # Header row
    headers = [
        "Batch ID",
        "Batch Name",
        "Batch Date",
        "Donor Number",
        "Donor Name",
        "Product Code",
        "Product Name",
        "Donation Amount",
        "Donation Date"
    ]
    ws.append(headers)

    # Header styling
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Data rows
    for row in rows:
        ws.append([
            row["batch_id"],
            row["batch_name"],
            row["batch_date"],
            row["donor_number"],
            row["donor_name"],
            row["product_code"],
            row["product_name"],
            float(row["donation_amount"]) if row["donation_amount"] else 0,
            row["donation_date"]
        ])

    # Column widths
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 25
    ws.column_dimensions["C"].width = 12
    ws.column_dimensions["D"].width = 15
    ws.column_dimensions["E"].width = 25
    ws.column_dimensions["F"].width = 12
    ws.column_dimensions["G"].width = 25
    ws.column_dimensions["H"].width = 18
    ws.column_dimensions["I"].width = 12

    # Save to BytesIO
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()


# ── Website (Date-Range) Export ───────────────────────────────────────────────


async def export_website_new(date_from: date, date_to: date) -> bytes:
    """Export Website donation data (32 columns with product pivot).

    Fixed columns (14):
    1. Donor Number
    2. Donor Name
    3. Gender
    4. Gender Display
    5. Marital State
    6. Marital Display
    7. Address
    8. Phone Number
    9. Email
    10. Organization Name
    11. Is Internal Employee
    12. Employee Display
    13. Total Donation
    14. First Donation Date
    15. Last Donation Date

    Product Pivot (8 products × 2 columns = 16):
    16-17: ZIS (amount, count)
    18-19: Fitrah (amount, count)
    20-21: Infaq (amount, count)
    22-23: Anak Asuh (amount, count)
    24-25: Anak Yatim (amount, count)
    26-27: DPU (amount, count)
    28-29: Wakaf (amount, count)
    30-31: Qurban (amount, count)

    DISCRIMINATOR: Only include donations in date range (donation_date BETWEEN $1 AND $2)
    """
    if date_from > date_to:
        raise ValueError("date_from must be <= date_to")

    rows = await fetch_all(
        """
        SELECT
          d.donorno                                  AS donor_number,
          d.donorname                                AS donor_name,
          COALESCE(id.gender, '')                    AS gender,
          CASE WHEN COALESCE(id.gender,'') = 'P' THEN 'Female' ELSE 'Male' END AS gender_display,
          COALESCE(id.maritalstate, '')              AS marital_state,
          CASE
            WHEN id.maritalstate = 'K' THEN 'Menikah'
            WHEN id.maritalstate = 'B' THEN 'Belum Menikah'
            WHEN id.maritalstate = 'J' THEN 'Cerai'
            ELSE ''
          END                                        AS marital_display,
          COALESCE(d.addressstreet, '')              AS address,
          COALESCE(d.phonenumber, '')                AS phone_number,
          COALESCE(id.email, '')                     AS email,
          COALESCE(id.corporatename, '')             AS organization_name,
          COALESCE(id.isinternalemployee, '')        AS is_internal_employee,
          CASE WHEN id.isinternalemployee = 'T' THEN 'Ya' ELSE 'Tidak' END AS employee_display,
          SUM(CAST(ti.amount AS NUMERIC(20,4)))      AS total_donation,
          MIN(CAST(t.actualdate AS DATE))            AS first_donation_date,
          MAX(CAST(t.actualdate AS DATE))            AS last_donation_date,
          COALESCE(SUM(CASE WHEN p.productcode IN ('0101','0103') THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0) AS nominal_zakat,
          COUNT(CASE WHEN p.productcode IN ('0101','0103') THEN 1 END)                                                  AS nominal_zakat_count,
          COALESCE(SUM(CASE WHEN p.productcode = '0102' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0)           AS nominal_fitrah,
          COUNT(CASE WHEN p.productcode = '0102' THEN 1 END)                                                            AS nominal_fitrah_count,
          COALESCE(SUM(CASE WHEN p.productcode = '02021' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0)          AS nominal_infak_sedekah,
          COUNT(CASE WHEN p.productcode = '02021' THEN 1 END)                                                           AS nominal_infak_sedekah_count,
          COALESCE(SUM(CASE WHEN p.productcode = '02011' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0)          AS nominal_anak_asuh,
          COUNT(CASE WHEN p.productcode = '02011' THEN 1 END)                                                           AS nominal_anak_asuh_count,
          COALESCE(SUM(CASE WHEN p.productcode = '02012' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0)          AS nominal_anak_yatim,
          COUNT(CASE WHEN p.productcode = '02012' THEN 1 END)                                                           AS nominal_anak_yatim_count,
          COALESCE(SUM(CASE WHEN p.productcode = '02014' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0)          AS nominal_dpu,
          COUNT(CASE WHEN p.productcode = '02014' THEN 1 END)                                                           AS nominal_dpu_count,
          COALESCE(SUM(CASE WHEN p.productcode = '0301' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0)           AS nominal_wakaf,
          COUNT(CASE WHEN p.productcode = '0301' THEN 1 END)                                                            AS nominal_wakaf_count,
          COALESCE(SUM(CASE WHEN p.productcode IN ('02013','0401') THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END),0) AS nominal_qurban,
          COUNT(CASE WHEN p.productcode IN ('02013','0401') THEN 1 END)                                                  AS nominal_qurban_count
        FROM transaction.transaction t
        INNER JOIN transaction.transactionitem ti ON t.transactionid = ti.transactionid
        INNER JOIN transaction.accounttransactionitem ati ON ti.transactionitemid = ati.transactionitemid
        INNER JOIN transaction.productaccount pa ON ati.accountno = pa.accountno
        INNER JOIN transaction.product p ON pa.productid = p.productid
        INNER JOIN fund.donor d ON t.donorid = d.donorid
        LEFT JOIN fund.individualdonor id ON d.donorid = id.donorid
        WHERE CAST(t.actualdate AS DATE) BETWEEN CAST($1 AS DATE) AND CAST($2 AS DATE)
        GROUP BY d.donorid, d.donorno, d.donorname, id.donorid, id.gender, id.maritalstate,
                 id.email, id.corporatename, id.isinternalemployee, d.addressstreet, d.phonenumber
        ORDER BY d.donorno
        """,
        date_from, date_to
    )

    # Generate Excel
    try:
        import openpyxl
        from openpyxl.styles import Alignment, Font, PatternFill
    except ImportError:
        raise RuntimeError("openpyxl not installed")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Donation Transactions"

    # Header row
    headers = [
        "Donor Number",
        "Donor Name",
        "Gender",
        "Gender Display",
        "Marital State",
        "Marital Display",
        "Address",
        "Phone Number",
        "Email",
        "Organization Name",
        "Is Internal Employee",
        "Employee Display",
        "Total Donation",
        "First Donation Date",
        "Last Donation Date",
        # ZIS
        "ZIS Amount",
        "ZIS Count",
        # Fitrah
        "Fitrah Amount",
        "Fitrah Count",
        # Infaq
        "Infaq Amount",
        "Infaq Count",
        # Anak Asuh
        "Anak Asuh Amount",
        "Anak Asuh Count",
        # Anak Yatim
        "Anak Yatim Amount",
        "Anak Yatim Count",
        # DPU
        "DPU Amount",
        "DPU Count",
        # Wakaf
        "Wakaf Amount",
        "Wakaf Count",
        # Qurban
        "Qurban Amount",
        "Qurban Count",
    ]
    ws.append(headers)

    # Header styling
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Data rows
    for row in rows:
        ws.append([
            row["donor_number"],
            row["donor_name"],
            row["gender"] or "",
            row["gender_display"],
            row["marital_state"] or "",
            row["marital_display"],
            row["address"],
            row["phone_number"],
            row["email"],
            row["organization_name"],
            row["is_internal_employee"] or "",
            row["employee_display"],
            float(row["total_donation"]) if row["total_donation"] else 0,
            row["first_donation_date"],
            row["last_donation_date"],
            float(row["nominal_zakat"]) if row["nominal_zakat"] else 0,
            int(row["nominal_zakat_count"]) if row["nominal_zakat_count"] else 0,
            float(row["nominal_fitrah"]) if row["nominal_fitrah"] else 0,
            int(row["nominal_fitrah_count"]) if row["nominal_fitrah_count"] else 0,
            float(row["nominal_infak_sedekah"]) if row["nominal_infak_sedekah"] else 0,
            int(row["nominal_infak_sedekah_count"]) if row["nominal_infak_sedekah_count"] else 0,
            float(row["nominal_anak_asuh"]) if row["nominal_anak_asuh"] else 0,
            int(row["nominal_anak_asuh_count"]) if row["nominal_anak_asuh_count"] else 0,
            float(row["nominal_anak_yatim"]) if row["nominal_anak_yatim"] else 0,
            int(row["nominal_anak_yatim_count"]) if row["nominal_anak_yatim_count"] else 0,
            float(row["nominal_dpu"]) if row["nominal_dpu"] else 0,
            int(row["nominal_dpu_count"]) if row["nominal_dpu_count"] else 0,
            float(row["nominal_wakaf"]) if row["nominal_wakaf"] else 0,
            int(row["nominal_wakaf_count"]) if row["nominal_wakaf_count"] else 0,
            float(row["nominal_qurban"]) if row["nominal_qurban"] else 0,
            int(row["nominal_qurban_count"]) if row["nominal_qurban_count"] else 0,
        ])

    # Column widths
    col_widths = {
        "A": 15,   # Donor Number
        "B": 25,   # Donor Name
        "C": 8,    # Gender
        "D": 15,   # Gender Display
        "E": 15,   # Marital State
        "F": 18,   # Marital Display
        "G": 25,   # Address
        "H": 15,   # Phone Number
        "I": 20,   # Email
        "J": 25,   # Organization Name
        "K": 20,   # Is Internal Employee
        "L": 18,   # Employee Display
        "M": 18,   # Total Donation
        "N": 18,   # First Donation Date
        "O": 18,   # Last Donation Date
        "P": 15,   # ZIS Amount
        "Q": 12,   # ZIS Count
        "R": 15,   # Fitrah Amount
        "S": 12,   # Fitrah Count
        "T": 15,   # Infaq Amount
        "U": 12,   # Infaq Count
        "V": 18,   # Anak Asuh Amount
        "W": 15,   # Anak Asuh Count
        "X": 18,   # Anak Yatim Amount
        "Y": 15,   # Anak Yatim Count
        "Z": 12,   # DPU Amount
        "AA": 10,  # DPU Count
        "AB": 15,  # Wakaf Amount
        "AC": 12,  # Wakaf Count
        "AD": 15,  # Qurban Amount
        "AE": 12,  # Qurban Count
    }
    for col, width in col_widths.items():
        ws.column_dimensions[col].width = width

    # Save to BytesIO
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf.getvalue()

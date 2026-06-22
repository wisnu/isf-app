"""Distribution reports service — laporan penyaluran dari DWH views.

7 laporan:
  1. Proposal Masuk (dwh.v_proposal_masuk)
  2. Daftar Mustahiq (dwh.v_report_mustahiq_list)
  3. Realisasi Rutin (dwh.v_report_realization_regular)
  4. Realisasi Non Rutin (dwh.v_report_realization_non_regular)
  5. Piutang Realisasi (dwh.v_program_realization)
  6. Pengembalian Realisasi (dwh.v_report_realization_return)
  7. Penyaluran Per Mustahiq (dwh.v_report_realization_by_mustahiq)
"""

from __future__ import annotations

from datetime import date

from app.shared.db import fetch_all_dwh, fetch_one_dwh, ping_dwh

CAP = 50_000


# ── 1. Laporan Proposal Masuk ─────────────────────────────────────────────────

async def proposal_incoming_count(
    date_from: str, date_to: str, mustahiq_id: int | None = None, product_group_id: int | None = None
) -> int:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt]
    clause = "proposal_date >= $1::date AND proposal_date < ($2::date + INTERVAL '1 day')"
    if mustahiq_id:
        args.append(mustahiq_id)
        clause += f" AND mustahiq_id = ${len(args)}"
    if product_group_id:
        args.append(product_group_id)
        clause += f" AND product_group_id = ${len(args)}"
    row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_proposal_masuk WHERE {clause}", *args
    )
    return int(row["n"]) if row else 0


async def proposal_incoming_rows(
    date_from: str, date_to: str, mustahiq_id: int | None = None, product_group_id: int | None = None
) -> list[dict]:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt]
    clause = "proposal_date >= $1::date AND proposal_date < ($2::date + INTERVAL '1 day')"
    if mustahiq_id:
        args.append(mustahiq_id)
        clause += f" AND mustahiq_id = ${len(args)}"
    if product_group_id:
        args.append(product_group_id)
        clause += f" AND product_group_id = ${len(args)}"
    return await fetch_all_dwh(
        f"""
        SELECT proposal_id, proposal_no, CAST(proposal_date AS VARCHAR) AS proposal_date,
               CAST(received_date AS VARCHAR) AS received_date, description, nominal,
               received_by, reference_by, CAST(realization_date AS VARCHAR) AS realization_date,
               realization_amount, memo_amount, memo_number, fund_source_no, fund_source_name,
               mustahiq_name, product_group_name
        FROM dwh.v_proposal_masuk
        WHERE {clause}
        ORDER BY proposal_date DESC, proposal_id DESC
        LIMIT {CAP}
        """,
        *args,
    )


async def proposal_incoming_page(
    date_from: str, date_to: str, mustahiq_id: int | None = None, product_group_id: int | None = None,
    page: int = 1, page_size: int = 25
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await proposal_incoming_count(date_from, date_to, mustahiq_id, product_group_id)
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt]
    clause = "proposal_date >= $1::date AND proposal_date < ($2::date + INTERVAL '1 day')"
    if mustahiq_id:
        args.append(mustahiq_id)
        clause += f" AND mustahiq_id = ${len(args)}"
    if product_group_id:
        args.append(product_group_id)
        clause += f" AND product_group_id = ${len(args)}"
    offset = (page - 1) * page_size
    args_page = [*args, page_size, offset]
    rows = await fetch_all_dwh(
        f"""
        SELECT proposal_id, proposal_no, CAST(proposal_date AS VARCHAR) AS proposal_date,
               CAST(received_date AS VARCHAR) AS received_date, description, nominal,
               received_by, reference_by, CAST(realization_date AS VARCHAR) AS realization_date,
               realization_amount, memo_amount, memo_number, fund_source_no, fund_source_name,
               mustahiq_name, product_group_name
        FROM dwh.v_proposal_masuk
        WHERE {clause}
        ORDER BY proposal_date DESC, proposal_id DESC
        LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}
        """,
        *args_page,
    )
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


# ── 2. Laporan Daftar Mustahiq ────────────────────────────────────────────────

async def mustahiq_list_count(
    mustahiq_type: str | None = None, product_id: int | None = None,
    date_start_from: str | None = None, date_start_to: str | None = None
) -> int:
    args: list = []
    clause = "1=1"
    if mustahiq_type:
        args.append(mustahiq_type)
        clause += f" AND mustahiq_type = ${len(args)}"
    if product_id:
        args.append(product_id)
        clause += f" AND product_id = ${len(args)}"
    if date_start_from:
        args.append(date.fromisoformat(date_start_from))
        clause += f" AND CAST(date_start AS date) >= ${len(args)}"
    if date_start_to:
        args.append(date.fromisoformat(date_start_to))
        clause += f" AND CAST(date_start AS date) <= ${len(args)}"
    row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_report_mustahiq_list WHERE {clause}", *args
    )
    return int(row["n"]) if row else 0


async def mustahiq_list_rows(
    mustahiq_type: str | None = None, product_id: int | None = None,
    date_start_from: str | None = None, date_start_to: str | None = None
) -> list[dict]:
    args: list = []
    clause = "1=1"
    if mustahiq_type:
        args.append(mustahiq_type)
        clause += f" AND mustahiq_type = ${len(args)}"
    if product_id:
        args.append(product_id)
        clause += f" AND product_id = ${len(args)}"
    if date_start_from:
        args.append(date.fromisoformat(date_start_from))
        clause += f" AND CAST(date_start AS date) >= ${len(args)}"
    if date_start_to:
        args.append(date.fromisoformat(date_start_to))
        clause += f" AND CAST(date_start AS date) <= ${len(args)}"
    return await fetch_all_dwh(
        f"""
        SELECT mustahiq_id, mustahiq_type, customer_name, address_street, address_kelurahan,
               address_kecamatan, address_city, phone_number, cp_name, cp_phone_number,
               cp_mobile_number, ashnaf_label, product_name, product_id,
               CAST(date_start AS VARCHAR) AS date_start, distribution_amount,
               school_name, supervisor_name
        FROM dwh.v_report_mustahiq_list
        WHERE {clause}
        ORDER BY customer_name, mustahiq_id
        LIMIT {CAP}
        """,
        *args,
    )


async def mustahiq_list_page(
    mustahiq_type: str | None = None, product_id: int | None = None,
    date_start_from: str | None = None, date_start_to: str | None = None,
    page: int = 1, page_size: int = 25
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await mustahiq_list_count(mustahiq_type, product_id, date_start_from, date_start_to)
    args: list = []
    clause = "1=1"
    if mustahiq_type:
        args.append(mustahiq_type)
        clause += f" AND mustahiq_type = ${len(args)}"
    if product_id:
        args.append(product_id)
        clause += f" AND product_id = ${len(args)}"
    if date_start_from:
        args.append(date.fromisoformat(date_start_from))
        clause += f" AND CAST(date_start AS date) >= ${len(args)}"
    if date_start_to:
        args.append(date.fromisoformat(date_start_to))
        clause += f" AND CAST(date_start AS date) <= ${len(args)}"
    offset = (page - 1) * page_size
    args_page = [*args, page_size, offset]
    rows = await fetch_all_dwh(
        f"""
        SELECT mustahiq_id, mustahiq_type, customer_name, address_street, address_kelurahan,
               address_kecamatan, address_city, phone_number, cp_name, cp_phone_number,
               cp_mobile_number, ashnaf_label, product_name, product_id,
               CAST(date_start AS VARCHAR) AS date_start, distribution_amount,
               school_name, supervisor_name
        FROM dwh.v_report_mustahiq_list
        WHERE {clause}
        ORDER BY customer_name, mustahiq_id
        LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}
        """,
        *args_page,
    )
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


# ── 3. Laporan Realisasi Rutin ────────────────────────────────────────────────

async def realization_regular_count(date_from: str, date_to: str) -> int:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    row = await fetch_one_dwh(
        "SELECT count(*) AS n FROM dwh.v_report_realization_regular "
        "WHERE realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day')",
        df, dt,
    )
    return int(row["n"]) if row else 0


async def realization_regular_rows(date_from: str, date_to: str) -> list[dict]:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    return await fetch_all_dwh(
        """
        SELECT product_id, product_name, product_group_name, mustahiq_product_name,
               customer_name, address_street, realization_id,
               CAST(realization_date AS VARCHAR) AS realization_date,
               status_receivables, realization_amount, report_amount, report_detail_status,
               budget_code, budget_item_description
        FROM dwh.v_report_realization_regular
        WHERE realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day')
        ORDER BY realization_date DESC, realization_id DESC
        LIMIT %d
        """ % CAP,
        df, dt,
    )


async def realization_regular_page(
    date_from: str, date_to: str, page: int = 1, page_size: int = 25
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await realization_regular_count(date_from, date_to)
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    offset = (page - 1) * page_size
    rows = await fetch_all_dwh(
        """
        SELECT product_id, product_name, product_group_name, mustahiq_product_name,
               customer_name, address_street, realization_id,
               CAST(realization_date AS VARCHAR) AS realization_date,
               status_receivables, realization_amount, report_amount, report_detail_status,
               budget_code, budget_item_description
        FROM dwh.v_report_realization_regular
        WHERE realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day')
        ORDER BY realization_date DESC, realization_id DESC
        LIMIT $3 OFFSET $4
        """,
        df, dt, page_size, offset,
    )
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


# ── 4. Laporan Realisasi Non Rutin ────────────────────────────────────────────

async def realization_non_regular_count(
    date_from: str, date_to: str, amount_min: float = 0.0, amount_max: float = 3000000.0, branch: str | None = None
) -> int:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt, amount_min, amount_max]
    clause = "realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day') AND realization_amount >= $3 AND realization_amount <= $4"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_report_realization_non_regular WHERE {clause}", *args
    )
    return int(row["n"]) if row else 0


async def realization_non_regular_rows(
    date_from: str, date_to: str, amount_min: float = 0.0, amount_max: float = 3000000.0, branch: str | None = None
) -> list[dict]:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt, amount_min, amount_max]
    clause = "realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day') AND realization_amount >= $3 AND realization_amount <= $4"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    return await fetch_all_dwh(
        f"""
        SELECT product_id, product_name, product_group_name, mustahiq_product_name,
               customer_name, address_street, realization_id,
               CAST(realization_date AS VARCHAR) AS realization_date,
               realization_amount, detail_description, proposal_no, proposal_description,
               proposal_nominal, proposal_reference_by, account_name, budget_code,
               budget_item_description, branch_code
        FROM dwh.v_report_realization_non_regular
        WHERE {clause}
        ORDER BY realization_date DESC, realization_id DESC
        LIMIT {CAP}
        """,
        *args,
    )


async def realization_non_regular_page(
    date_from: str, date_to: str, amount_min: float = 0.0, amount_max: float = 3000000.0,
    branch: str | None = None, page: int = 1, page_size: int = 25
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await realization_non_regular_count(date_from, date_to, amount_min, amount_max, branch)
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt, amount_min, amount_max]
    clause = "realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day') AND realization_amount >= $3 AND realization_amount <= $4"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    offset = (page - 1) * page_size
    args_page = [*args, page_size, offset]
    rows = await fetch_all_dwh(
        f"""
        SELECT product_id, product_name, product_group_name, mustahiq_product_name,
               customer_name, address_street, realization_id,
               CAST(realization_date AS VARCHAR) AS realization_date,
               realization_amount, detail_description, proposal_no, proposal_description,
               proposal_nominal, proposal_reference_by, account_name, budget_code,
               budget_item_description, branch_code
        FROM dwh.v_report_realization_non_regular
        WHERE {clause}
        ORDER BY realization_date DESC, realization_id DESC
        LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}
        """,
        *args_page,
    )
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


# ── 5. Laporan Piutang Realisasi ──────────────────────────────────────────────

async def realization_receivable_count(date_from: str, date_to: str) -> int:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    # dwh.v_program_realization: statusreceivables='Y' already baked in
    row = await fetch_one_dwh(
        "SELECT count(*) AS n FROM dwh.v_program_realization "
        "WHERE realizationdate >= $1::date AND realizationdate <= $2::date",
        df, dt,
    )
    return int(row["n"]) if row else 0


async def realization_receivable_rows(date_from: str, date_to: str) -> list[dict]:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    return await fetch_all_dwh(
        """
        SELECT realizationid, CAST(realizationdate AS VARCHAR) AS realizationdate,
               CAST(amount AS FLOAT8) AS realization_amount, input_user, realization_type,
               description AS realization_description, memo_number,
               employee_name, report_user, report_amount,
               CAST(report_date AS VARCHAR) AS report_date
        FROM dwh.v_program_realization
        WHERE realizationdate >= $1::date AND realizationdate <= $2::date
        ORDER BY realizationdate DESC, realizationid DESC
        LIMIT %d
        """ % CAP,
        df, dt,
    )


async def realization_receivable_page(
    date_from: str, date_to: str, page: int = 1, page_size: int = 25
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await realization_receivable_count(date_from, date_to)
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    offset = (page - 1) * page_size
    rows = await fetch_all_dwh(
        """
        SELECT realizationid, CAST(realizationdate AS VARCHAR) AS realizationdate,
               CAST(amount AS FLOAT8) AS realization_amount, input_user, realization_type,
               description AS realization_description, memo_number,
               employee_name, report_user, report_amount,
               CAST(report_date AS VARCHAR) AS report_date
        FROM dwh.v_program_realization
        WHERE realizationdate >= $1::date AND realizationdate <= $2::date
        ORDER BY realizationdate DESC, realizationid DESC
        LIMIT $3 OFFSET $4
        """,
        df, dt, page_size, offset,
    )
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


# ── 6. Laporan Pengembalian Realisasi ─────────────────────────────────────────

async def realization_return_count(date_from: str, date_to: str) -> int:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    row = await fetch_one_dwh(
        "SELECT count(DISTINCT return_id) AS n FROM dwh.v_report_realization_return "
        "WHERE return_date >= $1::date AND return_date < ($2::date + INTERVAL '1 day')",
        df, dt,
    )
    return int(row["n"]) if row else 0


async def realization_return_rows(date_from: str, date_to: str) -> list[dict]:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    # Flat rows (multiple per return if multiple cost items)
    return await fetch_all_dwh(
        """
        SELECT return_id, CAST(return_date AS VARCHAR) AS return_date,
               realization_amount, return_amount, memo_number, return_description,
               input_user, realization_id, cost_item_description, cost_amount
        FROM dwh.v_report_realization_return
        WHERE return_date >= $1::date AND return_date < ($2::date + INTERVAL '1 day')
        ORDER BY return_date DESC, return_id DESC
        LIMIT %d
        """ % CAP,
        df, dt,
    )


async def realization_return_page(
    date_from: str, date_to: str, page: int = 1, page_size: int = 25
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await realization_return_count(date_from, date_to)
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    offset = (page - 1) * page_size
    rows = await fetch_all_dwh(
        """
        SELECT return_id, CAST(return_date AS VARCHAR) AS return_date,
               realization_amount, return_amount, memo_number, return_description,
               input_user, realization_id, cost_item_description, cost_amount
        FROM dwh.v_report_realization_return
        WHERE return_date >= $1::date AND return_date < ($2::date + INTERVAL '1 day')
        ORDER BY return_date DESC, return_id DESC
        LIMIT $3 OFFSET $4
        """,
        df, dt, page_size, offset,
    )
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }


# ── 7. Laporan Penyaluran Per Mustahiq ────────────────────────────────────────

async def realization_by_mustahiq_count(
    date_from: str, date_to: str, branch: str | None = None
) -> int:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt]
    clause = "realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day')"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    row = await fetch_one_dwh(
        f"SELECT count(*) AS n FROM dwh.v_report_realization_by_mustahiq WHERE {clause}", *args
    )
    return int(row["n"]) if row else 0


async def realization_by_mustahiq_rows(
    date_from: str, date_to: str, branch: str | None = None
) -> list[dict]:
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt]
    clause = "realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day')"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    return await fetch_all_dwh(
        f"""
        SELECT customer_id, customer_name, address_street, product_id, product_name,
               product_group_name, CAST(realization_date AS VARCHAR) AS realization_date,
               realization_amount, detail_description, account_name, proposal_no,
               proposal_nominal, proposal_description, proposal_reference_by,
               budget_code, budget_item_description, branch_code
        FROM dwh.v_report_realization_by_mustahiq
        WHERE {clause}
        ORDER BY customer_name, customer_id, realization_date, product_name
        LIMIT {CAP}
        """,
        *args,
    )


async def realization_by_mustahiq_page(
    date_from: str, date_to: str, branch: str | None = None,
    page: int = 1, page_size: int = 25
) -> dict | None:
    if not await ping_dwh():
        return None
    total = await realization_by_mustahiq_count(date_from, date_to, branch)
    df = date.fromisoformat(date_from)
    dt = date.fromisoformat(date_to)
    args: list = [df, dt]
    clause = "realization_date >= $1::date AND realization_date < ($2::date + INTERVAL '1 day')"
    if branch:
        args.append(branch)
        clause += f" AND branch_code = ${len(args)}"
    offset = (page - 1) * page_size
    args_page = [*args, page_size, offset]
    rows = await fetch_all_dwh(
        f"""
        SELECT customer_id, customer_name, address_street, product_id, product_name,
               product_group_name, CAST(realization_date AS VARCHAR) AS realization_date,
               realization_amount, detail_description, account_name, proposal_no,
               proposal_nominal, proposal_description, proposal_reference_by,
               budget_code, budget_item_description, branch_code
        FROM dwh.v_report_realization_by_mustahiq
        WHERE {clause}
        ORDER BY customer_name, customer_id, realization_date, product_name
        LIMIT ${len(args) + 1} OFFSET ${len(args) + 2}
        """,
        *args_page,
    )
    return {
        "rows": rows,
        "total": total,
        "capped": total > CAP,
        "page": page,
        "page_size": page_size,
    }

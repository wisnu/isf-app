from __future__ import annotations

from datetime import date
from fastapi import HTTPException

from app.modules.fundraising.donation_confirm_schema import (
    DonationTransactionListResponse,
    DonationTransactionRow,
    Pagination,
)
from app.shared.db import fetch_all, fetch_one, get_pool


# ── List Transactions ─────────────────────────────────────────────────────────

async def list_transactions(
    begin_date: str,  # ISO YYYY-MM-DD
    end_date: str,    # ISO YYYY-MM-DD
    branch_code: str | None = None,
    is_all_branch: bool = False,
    search_category: int | None = None,  # 1=donor_no, 2=donor_name
    search_text: str | None = None,
    amount_from: float | None = None,
    amount_to: float | None = None,
    description: str | None = None,
    limit: int = 25,
    page: int = 1,
    user_branch_code: str | None = None,
    user_branch_access: str | None = None,
) -> DonationTransactionListResponse:
    """
    List donation transactions with DISCRIMINATOR:
    - mutationtype = 'C' (donation)
    - transactioncode IN ('SD001', 'SD002')
    """
    page = max(1, page)
    limit = max(1, min(500, limit))

    conds: list[str] = []
    params: list = []

    # DISCRIMINATOR — wajib ada
    conds.append("d2.mutationtype = 'C'")
    conds.append("a.transactioncode IN ('SD001', 'SD002')")

    # Date range — pass as datetime.date so asyncpg binds correctly
    params.append(date.fromisoformat(begin_date))
    params.append(date.fromisoformat(end_date))
    conds.append("CAST(a.actualdate AS DATE) BETWEEN $1 AND $2")

    # Branch access
    if not is_all_branch and user_branch_code:
        params.append(user_branch_code)
        conds.append(f"a.branchcode = ${len(params)}")

    # Search by donor_no or donor_name
    if search_text and search_text.strip():
        search_pattern = f"%{search_text.strip()}%"
        params.append(search_pattern)
        param_idx = len(params)
        if search_category == 1:
            # Search by donor_no
            conds.append(f"ati.donorid ILIKE ${param_idx}")
        elif search_category == 2:
            # Search by donor_name
            conds.append(f"d.donorname ILIKE ${param_idx}")

    # Amount range
    if amount_from is not None:
        params.append(amount_from)
        conds.append(f"d2.amount >= ${len(params)}")
    if amount_to is not None:
        params.append(amount_to)
        conds.append(f"d2.amount <= ${len(params)}")

    # Description
    if description and description.strip():
        search_desc = f"%{description.strip()}%"
        params.append(search_desc)
        conds.append(f"a.description ILIKE ${len(params)}")

    where_clause = "WHERE " + " AND ".join(conds) if conds else ""

    # Count total
    count_query = f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM transaction.accounttransactionitem ati
        JOIN transaction.transactionitem d2 ON ati.transactionitemid = d2.transactionitemid
        JOIN transaction.transaction a ON d2.transactionid = a.transactionid
        LEFT JOIN fund.donor d ON ati.donorid = d.donorid
        {where_clause}
    """
    count_row = await fetch_one(count_query, *params)
    total = int((count_row or {}).get("c", 0))

    # Fetch rows
    limit_param = len(params) + 1
    offset_param = len(params) + 2

    rows_query = f"""
        SELECT
            a.transactionid AS transaction_id,
            a.transactionno AS transaction_no,
            CAST(a.actualdate AS TEXT) AS actual_date,
            CAST(ati.donorid AS TEXT) AS donor_no,
            d.donorname AS donor_name,
            d2.amount AS amount,
            a.description AS description,
            a.branchcode AS branch_code,
            c.nama_cabang AS branch_name,
            fa_ch.accountname AS channel_name,
            a.channelaccountno AS channel_code,
            fa_pr.accountname AS product_name,
            a.authstatus AS auth_status,
            a.isposted AS is_posted,
            d2.transactionitemid AS transaction_item_id
        FROM transaction.accounttransactionitem ati
        JOIN transaction.transactionitem d2 ON ati.transactionitemid = d2.transactionitemid
        JOIN transaction.transaction a ON d2.transactionid = a.transactionid
        LEFT JOIN fund.donor d ON ati.donorid = d.donorid
        LEFT JOIN transaction.financialaccount fa_ch ON a.channelaccountno = fa_ch.accountno
        LEFT JOIN transaction.financialaccount fa_pr ON ati.accountno = fa_pr.accountno
        LEFT JOIN enterprise.cabang c ON a.branchcode = c.kode_cabang
        {where_clause}
        ORDER BY a.actualdate DESC, a.transactionid DESC
        LIMIT ${limit_param} OFFSET ${offset_param}
    """
    rows = await fetch_all(rows_query, *(params + [limit, (page - 1) * limit]))

    total_pages = (total + limit - 1) // limit if total else 0

    return DonationTransactionListResponse(
        rows=[
            DonationTransactionRow(
                transaction_id=r["transaction_id"],
                transaction_no=r["transaction_no"],
                actual_date=r["actual_date"][:10] if r["actual_date"] else None,
                donor_no=r["donor_no"],
                donor_name=r["donor_name"],
                amount=float(r["amount"]) if r["amount"] else 0.0,
                description=r["description"],
                branch_code=r["branch_code"],
                branch_name=r["branch_name"],
                channel_name=r["channel_name"],
                channel_code=r["channel_code"],
                product_name=r["product_name"],
                auth_status=r["auth_status"],
                is_posted=r["is_posted"],
                transaction_item_id=r["transaction_item_id"],
            )
            for r in rows
        ],
        pagination=Pagination(page=page, limit=limit, total=total, total_pages=total_pages),
    )


# ── Delete Transaction ────────────────────────────────────────────────────────

async def delete_transaction(
    transaction_id: int,
    user_branch_code: str | None = None,
    user_branch_access: str | None = None,
    user_roles: list[str] | None = None,
) -> None:
    """
    Cascade delete transaction (transaction, transactionitem, accounttransactionitem).

    Validasi:
    - Cross-branch: jika user_branch_access != 'all', cek branch_code
    - Auth: jika auth_status == 'T' dan 'SPVFUND' not in user_roles → 403
    """
    if user_roles is None:
        user_roles = []

    # Fetch transaction
    row = await fetch_one(
        """
        SELECT t.transactionid, t.branchcode, t.authstatus
        FROM transaction.transaction t
        WHERE t.transactionid = $1
        """,
        transaction_id,
    )
    if not row:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")

    trans_branch = row["branchcode"]
    auth_status = row["authstatus"]

    # Cross-branch validation
    if user_branch_access != "all" and user_branch_code:
        if trans_branch != user_branch_code:
            raise HTTPException(status_code=403, detail="Anda tidak memiliki akses ke cabang transaksi ini")

    # Auth validation
    if auth_status == "T" and "SPVFUND" not in user_roles:
        raise HTTPException(status_code=403, detail="Hanya supervisor fund yang dapat menghapus transaksi otorisasi")

    # Delete cascade
    async with get_pool().acquire() as conn:
        async with conn.transaction():
            # Delete accounttransactionitem & transactionitem
            await conn.execute(
                """
                DELETE FROM transaction.accounttransactionitem
                WHERE transactionitemid IN (
                    SELECT transactionitemid FROM transaction.transactionitem
                    WHERE transactionid = $1
                )
                """,
                transaction_id,
            )
            await conn.execute(
                "DELETE FROM transaction.transactionitem WHERE transactionid = $1",
                transaction_id,
            )
            # Delete transaction
            await conn.execute(
                "DELETE FROM transaction.transaction WHERE transactionid = $1",
                transaction_id,
            )


# ── Update Donor ──────────────────────────────────────────────────────────────

async def update_donor(
    transaction_item_id: int,
    donor_no: str,
    donor_name: str,
) -> None:
    """Update donor on a transaction item."""
    row = await fetch_one(
        "SELECT transactionitemid FROM transaction.transactionitem WHERE transactionitemid = $1",
        transaction_item_id,
    )
    if not row:
        raise HTTPException(status_code=404, detail="Item transaksi tidak ditemukan")

    async with get_pool().acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE transaction.accounttransactionitem
                SET donorid = $1
                WHERE transactionitemid = $2
                """,
                donor_no,
                transaction_item_id,
            )


# ── Post Journal (Placeholder) ────────────────────────────────────────────────

async def post_journal(transaction_id: int) -> None:
    """
    Placeholder — post_journal belum diimplementasi.
    Melibatkan subsistem akuntansi yang kompleks.
    """
    raise NotImplementedError("post_journal belum diimplementasi")


# ── Receipt (Placeholder) ─────────────────────────────────────────────────────

async def get_receipt(transaction_id: int) -> dict:
    """
    Placeholder — receipt generation belum diimplementasi.
    """
    raise NotImplementedError("get_receipt belum diimplementasi")

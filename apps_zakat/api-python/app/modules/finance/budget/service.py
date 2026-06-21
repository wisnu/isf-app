from __future__ import annotations

from decimal import Decimal
from typing import Optional

from app.modules.budget.schema import (
    BudgetCodeSearchRow,
    BudgetDetailResponse,
    BudgetImportRow,
    BudgetImportRequest,
    BudgetItemRow,
    BudgetListResponse,
    BudgetMasterItemRow,
    BudgetMasterItemRequest,
    BudgetMasterPeriodRow,
    BudgetNewRequest,
    BudgetOwnerItem,
    BudgetOwnerSummaryResponse,
    BudgetOwnerSummaryRow,
    BudgetPeriodItem,
    BudgetReviseRequest,
    BudgetRow,
    BudgetTransactionListResponse,
    BudgetTransactionRow,
    Pagination,
)
from app.shared.db import execute, fetch_all, fetch_one


# ── Lookups ───────────────────────────────────────────────────────────────────

async def get_budget_owners(include_parent: bool = False) -> list[BudgetOwnerItem]:
    """Get list of budget owners (leaf owners with is_detail='T')."""
    if include_parent:
        cond = ""
    else:
        cond = "WHERE is_detail = 'T' AND status = 'A'"

    rows = await fetch_all(
        f"""
        SELECT ownerid, ownercode, ownername, level, is_detail, parentownerid, status
        FROM transaction.budgetowner
        {cond}
        ORDER BY ownercode
        """
    )
    return [
        BudgetOwnerItem(
            owner_id=r["ownerid"],
            owner_code=r["ownercode"],
            owner_name=r["ownername"],
            level=r["level"],
            is_detail=r["is_detail"],
            parent_owner_id=r["parentownerid"],
            status=r["status"],
        )
        for r in rows
    ]


async def get_budget_periods() -> list[BudgetPeriodItem]:
    """Get list of budget periods (year root only: parentperiodid IS NULL)."""
    rows = await fetch_all(
        """
        SELECT periodid, periodvalue, isopen, parentperiodid
        FROM transaction.budgetperiod
        WHERE parentperiodid IS NULL
        ORDER BY periodvalue DESC
        """
    )
    return [
        BudgetPeriodItem(
            period_id=r["periodid"],
            period_value=r["periodvalue"],
            is_open=r["isopen"],
            parent_period_id=r["parentperiodid"],
        )
        for r in rows
    ]


async def get_budget_periods_for_owner(owner_id: int, branch_code: str) -> list[BudgetPeriodItem]:
    """Get periods that have budgets for a specific owner."""
    if branch_code:
        rows = await fetch_all(
            """
            SELECT DISTINCT bp.periodid, bp.periodvalue, bp.isopen, bp.parentperiodid
            FROM transaction.budgetperiod bp
            WHERE bp.parentperiodid IS NULL
              AND EXISTS (SELECT 1 FROM transaction.budget b
                          WHERE b.periodid = bp.periodid
                            AND b.ownerid = $1
                            AND b.branchcode = $2
                            AND b.budgettype = 'Y')
            ORDER BY bp.periodvalue DESC
            """,
            owner_id,
            branch_code,
        )
    else:
        rows = await fetch_all(
            """
            SELECT DISTINCT bp.periodid, bp.periodvalue, bp.isopen, bp.parentperiodid
            FROM transaction.budgetperiod bp
            WHERE bp.parentperiodid IS NULL
              AND EXISTS (SELECT 1 FROM transaction.budget b
                          WHERE b.periodid = bp.periodid
                            AND b.ownerid = $1
                            AND b.budgettype = 'Y')
            ORDER BY bp.periodvalue DESC
            """,
            owner_id,
        )
    return [
        BudgetPeriodItem(
            period_id=r["periodid"],
            period_value=r["periodvalue"],
            is_open=r["isopen"],
            parent_period_id=r["parentperiodid"],
        )
        for r in rows
    ]


# ── List ───────────────────────────────────────────────────────────────────────

async def list_budgets(
    page: int = 1,
    limit: int = 25,
    owner_id: Optional[int] = None,
    period_id: Optional[int] = None,
    branch_code: Optional[str] = None,
) -> BudgetListResponse:
    """List budgets with pagination."""
    page = max(1, page)
    limit = max(1, min(100, limit))

    conds = ["b.budgettype = 'Y'", "b.isdetail = 'F'"]
    params: list = []

    if owner_id is not None:
        params.append(owner_id)
        conds.append(f"b.ownerid = ${len(params)}")

    if period_id is not None:
        params.append(period_id)
        conds.append(f"b.periodid = ${len(params)}")

    if branch_code:
        params.append(branch_code)
        conds.append(f"b.branchcode = ${len(params)}")

    where_clause = "WHERE " + " AND ".join(conds)

    total_row = await fetch_one(
        f"SELECT CAST(COUNT(*) AS INTEGER) AS c FROM transaction.budget b {where_clause}",
        *params,
    )
    total = int((total_row or {}).get("c", 0))

    p_limit = len(params) + 1
    p_offset = len(params) + 2

    rows = await fetch_all(
        f"""
        SELECT
            b.budgetid,
            b.budgetcode,
            b.ownerid,
            bo.ownername,
            b.periodid,
            bp.periodvalue,
            b.itemid,
            bi.budgetitemcode,
            COALESCE(NULLIF(bi.budgetitemdescription, ''), bi_parent.budgetitemdescription) AS item_name,
            bi_parent.budgetitemdescription AS item_group,
            CAST(b.amount AS DECIMAL) AS amount,
            CAST(COALESCE(b.realization, 0) AS DECIMAL) AS realization,
            b.currencycode,
            b.branchcode,
            b.budgettype,
            b.isdetail
        FROM transaction.budget b
        LEFT JOIN transaction.budgetowner bo ON b.ownerid = bo.ownerid
        LEFT JOIN transaction.budgetperiod bp ON b.periodid = bp.periodid
        LEFT JOIN transaction.budgetitem bi ON b.itemid = bi.itemid AND bi.is_detail = 'T'
        LEFT JOIN transaction.budgetitem bi_parent ON bi_parent.itemid = bi.parentitemid AND bi_parent.is_detail = 'F'
        {where_clause}
        ORDER BY b.budgetid DESC
        LIMIT ${p_limit} OFFSET ${p_offset}
        """,
        *(params + [limit, (page - 1) * limit]),
    )

    total_pages = (total + limit - 1) // limit if total else 0

    budget_rows = [
        BudgetRow(
            budget_id=r["budgetid"],
            budget_code=r["budgetcode"],
            owner_id=r["ownerid"],
            owner_name=r["ownername"],
            period_id=r["periodid"],
            period_value=r["periodvalue"],
            item_id=r["itemid"],
            item_code=r["budgetitemcode"],
            item_name=r["item_name"],
            item_group=r["item_group"],
            amount=Decimal(str(r["amount"])) if r["amount"] else Decimal(0),
            realization=Decimal(str(r["realization"])) if r["realization"] else Decimal(0),
            currency_code=r["currencycode"] or "IDR",
            branch_code=r["branchcode"],
            budget_type=r["budgettype"],
            is_detail=r["isdetail"],
        )
        for r in rows
    ]

    return BudgetListResponse(
        rows=budget_rows,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


# ── Summary per Owner ─────────────────────────────────────────────────────────

async def get_budget_owner_summary(period_id: int, branch_code: str = "") -> BudgetOwnerSummaryResponse:
    """Summary anggaran per pemilik untuk satu tahun."""
    period = await fetch_one(
        "SELECT periodid, periodvalue FROM transaction.budgetperiod WHERE periodid = $1",
        period_id,
    )
    if branch_code:
        rows = await fetch_all(
            """
            SELECT
                bo.ownerid AS owner_id,
                bo.ownername AS owner_name,
                CAST(SUM(b.amount) AS DECIMAL) AS total_budget,
                CAST(SUM(COALESCE(b.realization, 0)) AS DECIMAL) AS total_realization
            FROM transaction.budget b
            JOIN transaction.budgetowner bo ON bo.ownerid = b.ownerid
            WHERE b.budgettype = 'Y'
              AND b.isdetail = 'F'
              AND b.periodid = $1
              AND b.branchcode = $2
            GROUP BY bo.ownerid, bo.ownername
            ORDER BY bo.ownername
            """,
            period_id,
            branch_code,
        )
    else:
        rows = await fetch_all(
            """
            SELECT
                bo.ownerid AS owner_id,
                bo.ownername AS owner_name,
                CAST(SUM(b.amount) AS DECIMAL) AS total_budget,
                CAST(SUM(COALESCE(b.realization, 0)) AS DECIMAL) AS total_realization
            FROM transaction.budget b
            JOIN transaction.budgetowner bo ON bo.ownerid = b.ownerid
            WHERE b.budgettype = 'Y'
              AND b.isdetail = 'F'
              AND b.periodid = $1
            GROUP BY bo.ownerid, bo.ownername
            ORDER BY bo.ownername
            """,
            period_id,
        )
    return BudgetOwnerSummaryResponse(
        period_id=period_id,
        period_value=period["periodvalue"] if period else 0,
        rows=[
            BudgetOwnerSummaryRow(
                owner_id=r["owner_id"],
                owner_name=r["owner_name"],
                total_budget=r["total_budget"],
                total_realization=r["total_realization"],
                remaining=r["total_budget"] - r["total_realization"],
            )
            for r in rows
        ],
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_budget_detail(budget_id: int) -> Optional[BudgetDetailResponse]:
    """Get budget detail with all related items."""
    budget_row = await fetch_one(
        """
        SELECT
            b.budgetid,
            b.budgetcode,
            b.ownerid,
            bo.ownername,
            b.periodid,
            bp.periodvalue,
            CAST(b.amount AS DECIMAL) AS amount,
            CAST(COALESCE(b.realization, 0) AS DECIMAL) AS realization,
            b.currencycode,
            b.branchcode,
            b.budgettype,
            b.isdetail
        FROM transaction.budget b
        LEFT JOIN transaction.budgetowner bo ON b.ownerid = bo.ownerid
        LEFT JOIN transaction.budgetperiod bp ON b.periodid = bp.periodid
        WHERE b.budgetid = $1 AND b.budgettype = 'Y' AND b.isdetail = 'F'
        """,
        budget_id,
    )

    if not budget_row:
        return None

    items_rows = await fetch_all(
        """
        SELECT
            bi.itemid,
            bi.budgetitemcode,
            bi.budgetitemdescription,
            bi.level,
            bi.parentitemid,
            bi.is_detail,
            CAST(COALESCE(sum_of_items.total_amount, 0) AS DECIMAL) AS amount
        FROM transaction.budgetitem bi
        LEFT JOIN (
            SELECT parentitemid, SUM(CAST(amount AS DECIMAL)) AS total_amount
            FROM transaction.budget b2
            WHERE b2.itemid = bi.itemid AND b2.budgetid = $1
            GROUP BY parentitemid
        ) sum_of_items ON bi.itemid = sum_of_items.parentitemid
        WHERE EXISTS (SELECT 1 FROM transaction.budget WHERE itemid = bi.itemid AND budgetid = $1)
        ORDER BY bi.itemid
        """,
        budget_id,
    )

    items = [
        BudgetItemRow(
            item_id=r["itemid"],
            budget_id=budget_id,
            item_code=r["budgetitemcode"],
            item_name=r["budgetitemdescription"],
            level=r["level"],
            parent_item_id=r["parentitemid"],
            amount=Decimal(str(r["amount"])) if r["amount"] else None,
            is_detail=r["is_detail"],
        )
        for r in items_rows
    ]

    return BudgetDetailResponse(
        budget_id=budget_row["budgetid"],
        budget_code=budget_row["budgetcode"],
        owner_id=budget_row["ownerid"],
        owner_name=budget_row["ownername"],
        period_id=budget_row["periodid"],
        period_value=budget_row["periodvalue"],
        amount=Decimal(str(budget_row["amount"])) if budget_row["amount"] else Decimal(0),
        realization=Decimal(str(budget_row["realization"])) if budget_row["realization"] else Decimal(0),
        currency_code=budget_row["currencycode"] or "IDR",
        branch_code=budget_row["branchcode"],
        budget_type=budget_row["budgettype"],
        is_detail=budget_row["isdetail"],
        items=items,
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def create_budget(
    data: BudgetNewRequest,
    branch_code: str,
    user_id: str,
) -> dict:
    """Create new budget (via otorisasi submission)."""
    # Check duplicate budget code
    existing = await fetch_one(
        """
        SELECT COUNT(*) AS c FROM transaction.budget
        WHERE budgettype = 'Y' AND periodid = $1 AND ownerid = $2
          AND branchcode = $3 AND LOWER(budgetcode) = LOWER($4)
        """,
        data.period_id,
        data.owner_id,
        branch_code,
        data.budget_code,
    )
    if existing and int(existing.get("c", 0)) > 0:
        raise ValueError(f"Budget code '{data.budget_code}' already exists for this owner/period/branch")

    # Create BudgetItem level-1 (group/category, is_detail='F')
    item_group_row = await fetch_one(
        """
        INSERT INTO transaction.budgetitem
            (budgetitemcode, budgetitemdescription, level, is_detail, ownerid, branchcode)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING itemid
        """,
        f"GRP_{data.budget_code}",
        data.item_group,
        1,
        "F",
        data.owner_id,
        branch_code,
    )
    item_group_id = int(item_group_row["itemid"])

    # Create BudgetItem level-2 (detail, is_detail='T')
    item_detail_row = await fetch_one(
        """
        INSERT INTO transaction.budgetitem
            (budgetitemcode, budgetitemdescription, level, is_detail, parentitemid, ownerid, branchcode)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING itemid
        """,
        f"{data.budget_code}",
        data.item_name,
        2,
        "T",
        item_group_id,
        data.owner_id,
        branch_code,
    )
    item_detail_id = int(item_detail_row["itemid"])

    # Create Budget record
    budget_row = await fetch_one(
        """
        INSERT INTO transaction.budget
            (periodid, ownerid, budgetcode, itemid, itemcode, itemname,
             currencycode, amount, realization, branchcode, budgettype, isdetail)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING budgetid
        """,
        data.period_id,
        data.owner_id,
        data.budget_code,
        item_detail_id,
        "",
        data.item_name,
        "IDR",
        float(data.amount),
        0.0,
        branch_code,
        "Y",
        "F",
    )
    budget_id = int(budget_row["budgetid"])

    return {
        "budget_id": budget_id,
        "budget_code": data.budget_code,
    }


# ── Edit ───────────────────────────────────────────────────────────────────────

async def edit_budget(
    budget_id: int,
    budget_code: str,
    item_group: str,
    item_name: str,
    amount: Decimal,
    user_id: str,
) -> dict:
    """Edit budget (via otorisasi submission)."""
    # Get current budget to find itemid
    budget_row = await fetch_one(
        "SELECT itemid FROM transaction.budget WHERE budgetid = $1",
        budget_id,
    )
    if not budget_row:
        raise ValueError(f"Budget {budget_id} not found")

    item_id = budget_row["itemid"]

    # Update budget
    await execute(
        """
        UPDATE transaction.budget
        SET budgetcode = $1, itemname = $2, amount = $3
        WHERE budgetid = $4
        """,
        budget_code,
        item_name,
        float(amount),
        budget_id,
    )

    # Update detail item (level=2)
    await execute(
        """
        UPDATE transaction.budgetitem
        SET budgetitemdescription = $1
        WHERE itemid = $2 AND level = 2
        """,
        item_name,
        item_id,
    )

    # Update parent item (level=1)
    parent_row = await fetch_one(
        "SELECT parentitemid FROM transaction.budgetitem WHERE itemid = $1",
        item_id,
    )
    if parent_row and parent_row["parentitemid"]:
        await execute(
            """
            UPDATE transaction.budgetitem
            SET budgetitemdescription = $1
            WHERE itemid = $2 AND level = 1
            """,
            item_group,
            parent_row["parentitemid"],
        )

    return {"budget_id": budget_id}


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_budget(budget_id: int) -> None:
    """Delete budget (soft-delete via deleteddate or hard delete)."""
    # Delete child budgets first
    await execute("DELETE FROM transaction.budget WHERE parentbudgetid = $1", budget_id)

    # Delete main budget
    await execute("DELETE FROM transaction.budget WHERE budgetid = $1", budget_id)


# ── Revise ────────────────────────────────────────────────────────────────────

async def revise_budget(
    data: BudgetReviseRequest,
    user_id: str,
) -> dict:
    """Revise budget amounts (direct commit, no otorisasi)."""
    revised_count = 0

    for item in data.items:
        # Create revision record
        rev_row = await fetch_one(
            """
            INSERT INTO transaction.budgetrevision (budgetid, amount, userid)
            VALUES ($1, $2, $3)
            RETURNING revisionid
            """,
            item.budget_id,
            float(item.amount),
            user_id,
        )
        revision_id = int(rev_row["revisionid"]) if rev_row else None

        # Update budget with new amount and revision ID
        await execute(
            """
            UPDATE transaction.budget
            SET amount = $1, revisionid = $2
            WHERE budgetid = $3
            """,
            float(item.amount),
            revision_id,
            item.budget_id,
        )
        revised_count += 1

    return {"revised_count": revised_count}


# ── Import ────────────────────────────────────────────────────────────────────

async def import_budgets(
    data: BudgetImportRequest,
    branch_code: str,
    user_id: str,
) -> dict:
    """Import budgets from Excel rows (via otorisasi submission)."""
    imported_count = 0
    errors: list[dict] = []

    for row in data.rows:
        try:
            # Look up owner by code
            owner_row = await fetch_one(
                "SELECT ownerid FROM transaction.budgetowner WHERE ownercode = $1 AND is_detail = 'T'",
                row.owner_code,
            )
            if not owner_row:
                errors.append(
                    {
                        "row": row.row_number,
                        "error": f"Owner code '{row.owner_code}' not found or not detail",
                    }
                )
                continue

            owner_id = owner_row["ownerid"]

            # Check duplicate
            dup_row = await fetch_one(
                """
                SELECT COUNT(*) AS c FROM transaction.budget
                WHERE budgettype = 'Y' AND periodid = $1 AND ownerid = $2
                  AND branchcode = $3 AND LOWER(budgetcode) = LOWER($4)
                """,
                data.period_id,
                owner_id,
                branch_code,
                row.budget_code,
            )
            if dup_row and int(dup_row.get("c", 0)) > 0:
                errors.append(
                    {
                        "row": row.row_number,
                        "error": f"Budget code '{row.budget_code}' already exists",
                    }
                )
                continue

            # Create BudgetItem level-1
            item_group_row = await fetch_one(
                """
                INSERT INTO transaction.budgetitem
                    (budgetitemcode, budgetitemdescription, level, is_detail, ownerid, branchcode)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING itemid
                """,
                f"GRP_{row.budget_code}",
                row.item_group,
                1,
                "F",
                owner_id,
                branch_code,
            )
            item_group_id = int(item_group_row["itemid"])

            # Create BudgetItem level-2
            item_detail_row = await fetch_one(
                """
                INSERT INTO transaction.budgetitem
                    (budgetitemcode, budgetitemdescription, level, is_detail, parentitemid, ownerid, branchcode)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING itemid
                """,
                f"{row.budget_code}",
                row.item_name,
                2,
                "T",
                item_group_id,
                owner_id,
                branch_code,
            )
            item_detail_id = int(item_detail_row["itemid"])

            # Create Budget
            await fetch_one(
                """
                INSERT INTO transaction.budget
                    (periodid, ownerid, budgetcode, itemid, itemcode, itemname,
                     currencycode, amount, realization, branchcode, budgettype, isdetail)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING budgetid
                """,
                data.period_id,
                owner_id,
                row.budget_code,
                item_detail_id,
                "",
                row.item_name,
                "IDR",
                float(row.amount),
                0.0,
                branch_code,
                "Y",
                "F",
            )
            imported_count += 1

        except Exception as e:
            errors.append(
                {
                    "row": row.row_number,
                    "error": str(e),
                }
            )

    return {
        "imported_count": imported_count,
        "errors": errors,
    }


# ── Transactions (Realisasi) ───────────────────────────────────────────────────

async def get_budget_transactions(
    budget_id: int,
    page: int = 1,
    limit: int = 25,
    begin_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> BudgetTransactionListResponse:
    """Get budget transactions (realisasi) for a budget."""
    page = max(1, page)
    limit = max(1, min(100, limit))

    conds = ["bt.budgetid = $1"]
    params: list = [budget_id]

    if begin_date:
        params.append(begin_date)
        conds.append(f"t.actualdate >= TO_DATE(${len(params)}, 'YYYY-MM-DD')")

    if end_date:
        params.append(end_date)
        conds.append(f"t.actualdate < TO_DATE(${len(params)}, 'YYYY-MM-DD') + INTERVAL '1 day'")

    where_clause = "WHERE " + " AND ".join(conds)

    total_row = await fetch_one(
        f"SELECT CAST(COUNT(*) AS INTEGER) AS c FROM transaction.budgettransaction bt "
        f"JOIN transaction.transactionitem ti ON ti.transactionitemid = bt.transactionitemid "
        f"JOIN transaction.transaction t ON t.transactionid = ti.transactionid "
        f"{where_clause}",
        *params,
    )
    total = int((total_row or {}).get("c", 0))

    p_limit = len(params) + 1
    p_offset = len(params) + 2

    rows = await fetch_all(
        f"""
        SELECT
            bt.transactionitemid,
            t.actualdate,
            t.transactioncode,
            tt.description      AS transaction_type_name,
            t.transactionno     AS no_transaksi,
            CASE WHEN bt.budgettranstype = 'A' THEN ti.amount ELSE 0 END AS realization_amount,
            CASE WHEN bt.budgettranstype != 'A' THEN ti.amount ELSE 0 END AS return_amount,
            bt.budgettranstype,
            t.referenceno       AS reference_no,
            t.description       AS description,
            t.inputer
        FROM transaction.budgettransaction bt
        JOIN transaction.transactionitem ti ON ti.transactionitemid = bt.transactionitemid
        JOIN transaction.transaction t ON t.transactionid = ti.transactionid
        LEFT JOIN transaction.transactiontype tt ON tt.transactioncode = t.transactioncode
        {where_clause}
        ORDER BY t.actualdate ASC, bt.transactionitemid ASC
        LIMIT ${p_limit} OFFSET ${p_offset}
        """,
        *(params + [limit, (page - 1) * limit]),
    )

    total_pages = (total + limit - 1) // limit if total else 0

    trans_rows = [
        BudgetTransactionRow(
            transaction_item_id=r["transactionitemid"],
            actual_date=str(r["actualdate"])[:10] if r["actualdate"] else "",
            transaction_code=r["transactioncode"],
            transaction_type_name=r["transaction_type_name"],
            transaction_no=r["no_transaksi"],
            realization_amount=Decimal(str(r["realization_amount"])) if r["realization_amount"] else Decimal(0),
            return_amount=Decimal(str(r["return_amount"])) if r["return_amount"] else Decimal(0),
            budget_trans_type=r["budgettranstype"],
            reference_no=r["reference_no"],
            description=r["description"],
            inputer=r["inputer"],
        )
        for r in rows
    ]

    return BudgetTransactionListResponse(
        budget_id=budget_id,
        rows=trans_rows,
        pagination=Pagination(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages,
        ),
    )


# ── Search ────────────────────────────────────────────────────────────────────

async def search_budget_codes(
    actual_date: str,
    branch_code: str,
    filter_category: Optional[str] = None,
    filter_text: Optional[str] = None,
) -> list[BudgetCodeSearchRow]:
    """Search budget codes based on transaction date and filters."""
    # Extract year from actual_date
    year = int(actual_date[:4]) if actual_date else 2026

    conds = [
        "b.budgettype = 'Y'",
        "b.isdetail = 'F'",
        "b.branchcode = $1",
        "bp.periodvalue = $2",
    ]
    params: list = [branch_code, year]

    # Add filter based on category
    if filter_text:
        filter_text_lower = f"%{filter_text.strip().lower()}%"

        if filter_category == "1":  # Code search
            params.append(filter_text_lower)
            conds.append(f"LOWER(b.budgetcode) LIKE ${len(params)}")
        elif filter_category == "2":  # Item group search
            params.append(filter_text_lower)
            conds.append(f"LOWER(bi_parent.budgetitemdescription) LIKE ${len(params)}")
        elif filter_category == "3":  # Item detail search
            params.append(filter_text_lower)
            conds.append(f"LOWER(bi.budgetitemdescription) LIKE ${len(params)}")
        else:  # All (default)
            params.append(filter_text_lower)
            params.append(filter_text_lower)
            params.append(filter_text_lower)
            conds.append(
                f"(LOWER(b.budgetcode) LIKE ${len(params) - 2} "
                f"OR LOWER(bi_parent.budgetitemdescription) LIKE ${len(params) - 1} "
                f"OR LOWER(bi.budgetitemdescription) LIKE ${len(params)})"
            )

    where_clause = "WHERE " + " AND ".join(conds)

    rows = await fetch_all(
        f"""
        SELECT
            b.budgetid,
            b.budgetcode,
            bo.ownername,
            bi_parent.budgetitemdescription AS item_group,
            bi.budgetitemdescription AS item_name
        FROM transaction.budget b
        JOIN transaction.budgetowner bo ON bo.ownerid = b.ownerid
        JOIN transaction.budgetitem bi ON bi.itemid = b.itemid AND bi.is_detail = 'T'
        LEFT JOIN transaction.budgetitem bi_parent ON bi_parent.itemid = bi.parentitemid
        JOIN transaction.budgetperiod bp ON bp.periodid = b.periodid AND bp.parentperiodid IS NULL
        {where_clause}
        LIMIT 50
        """,
        *params,
    )

    return [
        BudgetCodeSearchRow(
            budget_id=r["budgetid"],
            budget_code=r["budgetcode"],
            budget_owner=r["ownername"],
            item_group=r["item_group"],
            item_name=r["item_name"],
        )
        for r in rows
    ]


# ── Parameter Master: BudgetItem ──────────────────────────────────────────────

async def list_master_items(owner_id: Optional[int] = None, branch_code: Optional[str] = None) -> list[BudgetMasterItemRow]:
    """List all budget items (master data) with optional owner filter."""
    conds = []
    params: list = []
    if owner_id is not None:
        params.append(owner_id)
        conds.append(f"bi.ownerid = ${len(params)}")
    where = ("WHERE " + " AND ".join(conds)) if conds else ""
    rows = await fetch_all(
        f"""
        SELECT
            bi.itemid, bi.budgetitemcode, bi.budgetitemdescription,
            bi.level, bi.is_detail, bi.parentitemid, bi.ownerid, bi.branchcode,
            p.budgetitemdescription AS parent_description,
            bo.ownername
        FROM transaction.budgetitem bi
        LEFT JOIN transaction.budgetitem p ON p.itemid = bi.parentitemid
        LEFT JOIN transaction.budgetowner bo ON bo.ownerid = bi.ownerid
        {where}
        ORDER BY bi.level, bi.budgetitemcode
        """,
        *params,
    )
    return [
        BudgetMasterItemRow(
            item_id=r["itemid"],
            item_code=r["budgetitemcode"] or "",
            item_description=r["budgetitemdescription"] or "",
            level=r["level"],
            is_detail=r["is_detail"],
            parent_item_id=r["parentitemid"],
            parent_description=r["parent_description"],
            owner_id=r["ownerid"],
            owner_name=r["ownername"],
            branch_code=r["branchcode"],
        )
        for r in rows
    ]


async def create_master_item(data: BudgetMasterItemRequest) -> dict:
    """Create a new budget item (master data)."""
    row = await fetch_one(
        """
        INSERT INTO transaction.budgetitem
            (budgetitemcode, budgetitemdescription, level, is_detail, parentitemid, ownerid, branchcode)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING itemid
        """,
        data.item_code,
        data.item_description,
        data.level,
        data.is_detail,
        data.parent_item_id,
        data.owner_id,
        data.branch_code,
    )
    return {"item_id": row["itemid"]}


async def update_master_item(item_id: int, data: BudgetMasterItemRequest) -> dict:
    """Update a budget item (master data)."""
    row = await fetch_one(
        """
        UPDATE transaction.budgetitem
        SET budgetitemcode=$1, budgetitemdescription=$2, level=$3, is_detail=$4,
            parentitemid=$5, ownerid=$6, branchcode=$7
        WHERE itemid=$8
        RETURNING itemid
        """,
        data.item_code,
        data.item_description,
        data.level,
        data.is_detail,
        data.parent_item_id,
        data.owner_id,
        data.branch_code,
        item_id,
    )
    if not row:
        raise ValueError(f"Budget item {item_id} not found")
    return {"item_id": item_id}


async def delete_master_item(item_id: int) -> None:
    """Delete a budget item (master data). Raises if item has children or is used in budgets."""
    child_count = await fetch_one(
        "SELECT CAST(COUNT(*) AS INTEGER) AS c FROM transaction.budgetitem WHERE parentitemid=$1",
        item_id,
    )
    if int((child_count or {}).get("c", 0)) > 0:
        raise ValueError("Item memiliki sub-item. Hapus sub-item terlebih dahulu.")
    used_count = await fetch_one(
        "SELECT CAST(COUNT(*) AS INTEGER) AS c FROM transaction.budget WHERE itemid=$1",
        item_id,
    )
    if int((used_count or {}).get("c", 0)) > 0:
        raise ValueError("Item sudah digunakan di anggaran. Tidak bisa dihapus.")
    await execute("DELETE FROM transaction.budgetitem WHERE itemid=$1", item_id)


# ── Parameter Master: BudgetPeriod ────────────────────────────────────────────

async def list_master_periods() -> list[BudgetMasterPeriodRow]:
    """List all budget periods (year roots) with child count."""
    rows = await fetch_all(
        """
        SELECT
            bp.periodid, bp.periodvalue, bp.isopen,
            CAST(COUNT(c.periodid) AS INTEGER) AS child_count
        FROM transaction.budgetperiod bp
        LEFT JOIN transaction.budgetperiod c ON c.parentperiodid = bp.periodid
        WHERE bp.parentperiodid IS NULL
        GROUP BY bp.periodid, bp.periodvalue, bp.isopen
        ORDER BY bp.periodvalue DESC
        """
    )
    return [
        BudgetMasterPeriodRow(
            period_id=r["periodid"],
            period_value=r["periodvalue"],
            is_open=r["isopen"],
            child_count=r["child_count"],
        )
        for r in rows
    ]


async def create_master_period(year: int) -> dict:
    """Create a new budget period year + 12 months automatically."""
    existing = await fetch_one(
        "SELECT periodid FROM transaction.budgetperiod WHERE periodvalue=$1 AND parentperiodid IS NULL",
        year,
    )
    if existing:
        raise ValueError(f"Periode tahun {year} sudah ada.")
    root = await fetch_one(
        """
        INSERT INTO transaction.budgetperiod (periodvalue, isopen, parentperiodid)
        VALUES ($1, 'T', NULL)
        RETURNING periodid
        """,
        year,
    )
    root_id = root["periodid"]
    for month in range(1, 13):
        await execute(
            """
            INSERT INTO transaction.budgetperiod (periodvalue, isopen, parentperiodid)
            VALUES ($1, 'T', $2)
            """,
            month,
            root_id,
        )
    return {"period_id": root_id, "year": year, "months_created": 12}

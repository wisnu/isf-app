from __future__ import annotations

from datetime import date

from fastapi import HTTPException

from app.modules.finance.master.petty_cash.schema import (
    BranchLookupItem,
    CurrencyLookupItem,
    GlAccountLookupItem,
    PettyCashCreate,
    PettyCashDetail,
    PettyCashList,
    PettyCashRow,
    PettyCashUpdate,
    Pagination,
)
from app.shared.db import execute, fetch_all, fetch_one


# ── Helpers ───────────────────────────────────────────────────────────────────

def _parse_date(val: str | None) -> date | None:
    if not val:
        return None
    try:
        return date.fromisoformat(str(val)[:10])
    except (ValueError, TypeError):
        return None


def _to_row(r: dict) -> PettyCashRow:
    return PettyCashRow(
        account_no=r["accountno"] or "",
        account_name=r["accountname"],
        cash_code=r["cashcode"],
        branch_code=r["branchcode"],
        currency_code=r["currencycode"],
        balance=float(r["balance"]) if r["balance"] is not None else None,
        status=r["status"],
    )


# ── List ──────────────────────────────────────────────────────────────────────

def _build_where(search: str | None) -> tuple[str, list]:
    conds: list[str] = ["ca.cashaccounttype = 'P'"]
    params: list = []

    if search and search.strip():
        params.append(f"%{search.strip().lower()}%")
        p = len(params)
        conds.append(
            f"(LOWER(COALESCE(fa.accountno, '')) LIKE ${p}"
            f" OR LOWER(COALESCE(fa.accountname, '')) LIKE ${p}"
            f" OR LOWER(COALESCE(ca.cashcode, '')) LIKE ${p})"
        )

    return "WHERE " + " AND ".join(conds), params


async def list_petty_cash(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> PettyCashList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_where(search)

    total_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM transaction.financialaccount fa
        JOIN transaction.cashaccount ca ON ca.accountno = fa.accountno
        {where}
        """,
        *params,
    )
    total_count = int((total_row or {}).get("c", 0))

    limit_pos = len(params) + 1
    offset_pos = len(params) + 2
    page_rows = await fetch_all(
        f"""
        SELECT
            fa.accountno,
            fa.accountname,
            ca.cashcode,
            fa.branchcode,
            fa.currencycode,
            fa.balance,
            fa.status
        FROM transaction.financialaccount fa
        JOIN transaction.cashaccount ca ON ca.accountno = fa.accountno
        {where}
        ORDER BY fa.accountno
        LIMIT ${limit_pos} OFFSET ${offset_pos}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total_count + page_size - 1) // page_size if total_count else 0

    return PettyCashList(
        rows=[_to_row(r) for r in page_rows],
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total_count,
            total_pages=total_pages,
        ),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_petty_cash_detail(account_no: str) -> PettyCashDetail | None:
    row = await fetch_one(
        """
        SELECT
            fa.accountno,
            fa.accountname,
            ca.cashcode,
            ca.accountinterface,
            fa.currencycode,
            fa.branchcode,
            fa.balance,
            fa.status,
            fa.openingdate
        FROM transaction.financialaccount fa
        JOIN transaction.cashaccount ca ON ca.accountno = fa.accountno
        WHERE fa.accountno = $1 AND ca.cashaccounttype = 'P'
        """,
        account_no,
    )
    if not row:
        return None

    opening_date: str | None = None
    if row["openingdate"] is not None:
        try:
            opening_date = row["openingdate"].strftime("%Y-%m-%d")
        except AttributeError:
            opening_date = str(row["openingdate"])[:10]

    return PettyCashDetail(
        account_no=row["accountno"] or "",
        account_name=row["accountname"],
        cash_code=row["cashcode"],
        account_interface=row["accountinterface"],
        currency_code=row["currencycode"],
        branch_code=row["branchcode"],
        balance=float(row["balance"]) if row["balance"] is not None else None,
        status=row["status"],
        opening_date=opening_date,
    )


# ── Create ────────────────────────────────────────────────────────────────────

async def _validate_cash_code_unique(cash_code: str, exclude_account_no: str | None = None) -> None:
    if not cash_code:
        return
    if exclude_account_no:
        count_row = await fetch_one(
            """
            SELECT CAST(COUNT(*) AS INTEGER) AS c
            FROM transaction.cashaccount
            WHERE cashcode = $1 AND accountno <> $2
            """,
            cash_code,
            exclude_account_no,
        )
    else:
        count_row = await fetch_one(
            """
            SELECT CAST(COUNT(*) AS INTEGER) AS c
            FROM transaction.cashaccount
            WHERE cashcode = $1
            """,
            cash_code,
        )
    if int((count_row or {}).get("c", 0)) > 0:
        raise HTTPException(
            status_code=422,
            detail="Kode Kas sudah digunakan. Silakan ganti kode kas.",
        )


async def create_petty_cash(payload: PettyCashCreate) -> str:
    if payload.cash_code:
        await _validate_cash_code_unique(payload.cash_code)

    seq_row = await fetch_one("SELECT nextval('transaction.seq_pettycashid') AS seq")
    seq_num = int((seq_row or {}).get("seq", 0))
    account_no = f"PC.{payload.branch_code}.{payload.currency_code}.{seq_num:04d}"

    await execute(
        """
        INSERT INTO transaction.financialaccount
            (accountno, accountname, branchcode, currencycode,
             financialaccounttype, status, balance, openingdate)
        VALUES ($1, $2, $3, $4, 'C', 'A', 0, $5)
        """,
        account_no,
        payload.account_name,
        payload.branch_code,
        payload.currency_code,
        _parse_date(payload.opening_date),
    )

    await execute(
        """
        INSERT INTO transaction.cashaccount
            (accountno, cashaccounttype, accountinterface, cashcode, accountcurrency)
        VALUES ($1, 'P', $2, $3, $4)
        """,
        account_no,
        payload.account_interface,
        payload.cash_code or None,
        payload.currency_code,
    )

    return account_no


# ── Update ────────────────────────────────────────────────────────────────────

async def update_petty_cash(account_no: str, payload: PettyCashUpdate) -> None:
    if payload.cash_code:
        await _validate_cash_code_unique(payload.cash_code, exclude_account_no=account_no)

    await execute(
        """
        UPDATE transaction.financialaccount SET
            accountname  = $1,
            currencycode = $2,
            openingdate  = $3
        WHERE accountno = $4
        """,
        payload.account_name,
        payload.currency_code,
        _parse_date(payload.opening_date),
        account_no,
    )

    await execute(
        """
        UPDATE transaction.cashaccount SET
            accountinterface = $1,
            cashcode         = $2,
            accountcurrency  = $3
        WHERE accountno = $4
        """,
        payload.account_interface,
        payload.cash_code or None,
        payload.currency_code,
        account_no,
    )


# ── Delete ────────────────────────────────────────────────────────────────────

async def delete_petty_cash(account_no: str) -> None:
    await execute(
        "DELETE FROM transaction.cashaccount WHERE accountno = $1",
        account_no,
    )
    await execute(
        "DELETE FROM transaction.financialaccount WHERE accountno = $1",
        account_no,
    )


# ── Lookups ───────────────────────────────────────────────────────────────────

async def get_lookup_branches() -> list[BranchLookupItem]:
    rows = await fetch_all(
        "SELECT branchcode, branchname FROM transaction.branch WHERE isactive = 'T' ORDER BY branchcode"
    )
    return [
        BranchLookupItem(branch_code=r["branchcode"], branch_name=r["branchname"])
        for r in rows
    ]


async def get_lookup_currencies() -> list[CurrencyLookupItem]:
    rows = await fetch_all(
        "SELECT currency_code, short_name, full_name FROM transaction.currency ORDER BY currency_code"
    )
    return [
        CurrencyLookupItem(
            currency_code=r["currency_code"],
            short_name=r["short_name"],
            full_name=r["full_name"],
        )
        for r in rows
    ]


async def get_lookup_gl_accounts(search: str | None = None) -> list[GlAccountLookupItem]:
    if search and search.strip():
        p = f"%{search.strip().lower()}%"
        rows = await fetch_all(
            """
            SELECT account_code, account_name FROM transaction.account
            WHERE is_detail = 'T'
              AND (LOWER(COALESCE(account_code, '')) LIKE $1
                   OR LOWER(COALESCE(account_name, '')) LIKE $1)
            ORDER BY account_code LIMIT 50
            """,
            p,
        )
    else:
        rows = await fetch_all(
            """
            SELECT account_code, account_name FROM transaction.account
            WHERE is_detail = 'T'
            ORDER BY account_code LIMIT 50
            """
        )
    return [
        GlAccountLookupItem(account_code=r["account_code"], account_name=r["account_name"])
        for r in rows
    ]

from __future__ import annotations

from app.modules.bank.schema import (
    BankAccountDetail,
    BankAccountList,
    BankAccountRow,
    BankLookupItem,
    BranchLookupItem,
    CurrencyLookupItem,
    GlAccountLookupItem,
    Pagination,
    ProductLookupItem,
)
from app.shared.db import fetch_all, fetch_one


# ── List ──────────────────────────────────────────────────────────────────────

def _build_where(search: str | None) -> tuple[str, list]:
    conds: list[str] = ["b.cashaccounttype = 'A'"]
    params: list = []

    if search and search.strip():
        params.append(f"%{search.strip().lower()}%")
        p = len(params)
        conds.append(
            f"(LOWER(COALESCE(b.accountno, '')) LIKE ${p}"
            f" OR LOWER(COALESCE(f.accountname, '')) LIKE ${p}"
            f" OR LOWER(COALESCE(b.bankname, '')) LIKE ${p}"
            f" OR LOWER(COALESCE(b.bankaccountno, '')) LIKE ${p})"
        )

    return "WHERE " + " AND ".join(conds), params


def _to_row(r: dict) -> BankAccountRow:
    return BankAccountRow(
        account_no=r["accountno"] or "",
        account_name=r["accountname"],
        bank_name=r["bankname"],
        bank_account_no=r["bankaccountno"],
        branch_code=r["branchcode"],
        currency_code=r["currencycode"],
        balance=float(r["balance"]) if r["balance"] is not None else None,
        status=r["status"],
    )


async def list_bank_accounts(
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> BankAccountList:
    page = max(1, page)
    page_size = max(1, min(500, page_size))
    where, params = _build_where(search)

    total_row = await fetch_one(
        f"""
        SELECT CAST(COUNT(*) AS INTEGER) AS c
        FROM transaction.financialaccount f
        JOIN transaction.cashaccount b ON b.accountno = f.accountno
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
            b.accountno,
            f.accountname,
            b.bankname,
            b.bankaccountno,
            f.branchcode,
            f.currencycode,
            f.balance,
            f.status
        FROM transaction.financialaccount f
        JOIN transaction.cashaccount b ON b.accountno = f.accountno
        {where}
        ORDER BY b.accountno
        LIMIT ${limit_pos} OFFSET ${offset_pos}
        """,
        *(params + [page_size, (page - 1) * page_size]),
    )

    total_pages = (total_count + page_size - 1) // page_size if total_count else 0

    return BankAccountList(
        rows=[_to_row(r) for r in page_rows],
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total_count,
            total_pages=total_pages,
        ),
    )


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_bank_account_detail(account_no: str) -> BankAccountDetail | None:
    row = await fetch_one(
        """
        SELECT
            b.accountno,
            f.accountname,
            b.bankname,
            b.bankcode,
            b.bankaccountno,
            f.branchcode,
            f.currencycode,
            f.balance,
            f.status,
            f.openingdate,
            b.accountinterface,
            b.isamilaccount,
            b.productid,
            b.cashcode
        FROM transaction.financialaccount f
        JOIN transaction.cashaccount b ON b.accountno = f.accountno
        WHERE b.accountno = $1 AND b.cashaccounttype = 'A'
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

    return BankAccountDetail(
        account_no=row["accountno"] or "",
        account_name=row["accountname"],
        bank_name=row["bankname"],
        bank_code=row["bankcode"],
        bank_account_no=row["bankaccountno"],
        branch_code=row["branchcode"],
        currency_code=row["currencycode"],
        balance=float(row["balance"]) if row["balance"] is not None else None,
        account_interface=row["accountinterface"],
        opening_date=opening_date,
        is_amil_account=(row["isamilaccount"] or "").upper() == "T",
        product_id=row["productid"],
        cash_code=row["cashcode"],
        status=row["status"],
    )


# ── Lookups ───────────────────────────────────────────────────────────────────

async def get_lookup_banks() -> list[BankLookupItem]:
    rows = await fetch_all(
        "SELECT bankcode, bankshortname, bankname FROM transaction.bank ORDER BY bankshortname"
    )
    return [
        BankLookupItem(
            bank_code=r["bankcode"],
            bank_short_name=r["bankshortname"],
            bank_name=r["bankname"],
        )
        for r in rows
    ]


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


async def get_lookup_products(search: str | None = None) -> list[ProductLookupItem]:
    if search and search.strip():
        p = f"%{search.strip().lower()}%"
        rows = await fetch_all(
            """
            SELECT productid, productcode, productname FROM program.product
            WHERE isdetail = 'T'
              AND (LOWER(COALESCE(productcode, '')) LIKE $1
                   OR LOWER(COALESCE(productname, '')) LIKE $1)
            ORDER BY productname LIMIT 50
            """,
            p,
        )
    else:
        rows = await fetch_all(
            """
            SELECT productid, productcode, productname FROM program.product
            WHERE isdetail = 'T'
            ORDER BY productname LIMIT 50
            """
        )
    return [
        ProductLookupItem(
            product_id=r["productid"],
            product_code=r["productcode"],
            product_name=r["productname"],
        )
        for r in rows
    ]


# ── Otorisasi dispatcher ──────────────────────────────────────────────────────

async def create_from_payload(payload: dict, user_id: str, branch_code: str) -> str:
    action = payload.get("action", "create")

    if action == "create":
        seq_row = await fetch_one("SELECT nextval('seq_bankcash') AS seq")
        seq_num = int((seq_row or {}).get("seq", 0))
        account_no = f"BANK{seq_num:04d}"

        bank_row = await fetch_one(
            "SELECT bankshortname FROM transaction.bank WHERE bankcode = $1",
            payload.get("bank_code", ""),
        )
        bank_name = (bank_row or {}).get("bankshortname") or payload.get("bank_code", "")

        is_amil = "T" if payload.get("is_amil_account") else "F"

        # financialaccount: accountname, branchcode, currencycode, status, balance, openingdate
        await fetch_one(
            """
            INSERT INTO transaction.financialaccount
                (accountno, accountname, branchcode, currencycode,
                 financialaccounttype, status, balance, openingdate)
            VALUES ($1, $2, $3, $4, 'C', 'A', 0, $5)
            """,
            account_no,
            payload.get("account_name", ""),
            payload.get("branch_code", branch_code),
            payload.get("currency_code", "IDR"),
            payload.get("opening_date") or None,
        )

        # cashaccount: bank-specific fields
        await fetch_one(
            """
            INSERT INTO transaction.cashaccount
                (accountno, bankname, bankaccountno, accountcurrency, cashaccounttype,
                 bankcode, accountinterface, cashcode, productid, isamilaccount, isreconaccount)
            VALUES ($1, $2, $3, $4, 'A', $5, $6, $7, $8, $9, 'F')
            """,
            account_no,
            bank_name,
            payload.get("bank_account_no", ""),
            payload.get("currency_code", "IDR"),
            payload.get("bank_code", ""),
            payload.get("account_interface", ""),
            payload.get("cash_code") or None,
            payload.get("product_id") or None,
            is_amil,
        )
        return account_no

    elif action == "edit":
        account_no = payload["account_no"]

        bank_row = await fetch_one(
            "SELECT bankshortname FROM transaction.bank WHERE bankcode = $1",
            payload.get("bank_code", ""),
        )
        bank_name = (bank_row or {}).get("bankshortname") or payload.get("bank_code", "")
        is_amil = "T" if payload.get("is_amil_account") else "F"

        await fetch_one(
            """
            UPDATE transaction.financialaccount SET
                accountname  = $1,
                branchcode   = $2,
                currencycode = $3,
                openingdate  = $4
            WHERE accountno = $5
            """,
            payload.get("account_name", ""),
            payload.get("branch_code", branch_code),
            payload.get("currency_code", "IDR"),
            payload.get("opening_date") or None,
            account_no,
        )

        await fetch_one(
            """
            UPDATE transaction.cashaccount SET
                bankname         = $1,
                bankaccountno    = $2,
                accountcurrency  = $3,
                bankcode         = $4,
                accountinterface = $5,
                cashcode         = $6,
                productid        = $7,
                isamilaccount    = $8
            WHERE accountno = $9
            """,
            bank_name,
            payload.get("bank_account_no", ""),
            payload.get("currency_code", "IDR"),
            payload.get("bank_code", ""),
            payload.get("account_interface", ""),
            payload.get("cash_code") or None,
            payload.get("product_id") or None,
            is_amil,
            account_no,
        )
        return account_no

    elif action == "delete":
        account_no = payload["account_no"]
        await fetch_one(
            "DELETE FROM transaction.cashaccount WHERE accountno = $1",
            account_no,
        )
        await fetch_one(
            "DELETE FROM transaction.financialaccount WHERE accountno = $1",
            account_no,
        )
        return account_no

    else:
        raise ValueError(f"Unknown action: {action}")

from __future__ import annotations

from fastapi import HTTPException

from app.shared.db import execute, fetch_all, fetch_one


# ── List ──────────────────────────────────────────────────────────────────────

async def list_budget_owners(page: int = 1, limit: int = 25, q: str | None = None) -> dict:
    page  = max(1, page)
    limit = max(1, min(100, limit))

    where  = ""
    params: list = []
    if q and q.strip():
        params.append(f"%{q.strip().lower()}%")
        where = "WHERE LOWER(ownercode) LIKE $1 OR LOWER(ownername) LIKE $1"

    total_row = await fetch_one(
        f"SELECT CAST(COUNT(*) AS INTEGER) AS c FROM transaction.budgetowner {where}",
        *params,
    )
    total = int((total_row or {}).get("c", 0))

    p_limit  = len(params) + 1
    p_offset = len(params) + 2
    rows = await fetch_all(
        f"""
        SELECT ownerid, ownercode, ownername, level, is_detail, parentownerid, status
        FROM transaction.budgetowner
        {where}
        ORDER BY ownercode
        LIMIT ${p_limit} OFFSET ${p_offset}
        """,
        *(params + [limit, (page - 1) * limit]),
    )

    total_pages = (total + limit - 1) // limit if total else 0
    return {
        "rows": [dict(r) for r in rows],
        "pagination": {"page": page, "limit": limit, "total": total, "total_pages": total_pages},
    }


# ── Detail ────────────────────────────────────────────────────────────────────

async def get_budget_owner(ownerid: int) -> dict:
    row = await fetch_one(
        """
        SELECT ownerid, ownercode, ownername, level, is_detail, parentownerid, status,
               CAST(tglubah AS TEXT) AS tglubah, userpengubah, terminalubah
        FROM transaction.budgetowner
        WHERE ownerid = $1
        """,
        ownerid,
    )
    if not row:
        raise HTTPException(404, "Pemilik anggaran tidak ditemukan")
    return dict(row)


# ── Lookup ────────────────────────────────────────────────────────────────────

async def lookup_groups(q: str | None = None) -> list[dict]:
    if q and q.strip():
        p = f"%{q.strip().lower()}%"
        rows = await fetch_all(
            """
            SELECT ownerid, ownercode, ownername, is_detail
            FROM transaction.budgetowner
            WHERE is_detail = 'F' AND status = 'A'
              AND (LOWER(ownercode) LIKE $1 OR LOWER(ownername) LIKE $1)
            ORDER BY ownername
            LIMIT 50
            """,
            p,
        )
    else:
        rows = await fetch_all(
            """
            SELECT ownerid, ownercode, ownername, is_detail
            FROM transaction.budgetowner
            WHERE is_detail = 'F' AND status = 'A'
            ORDER BY ownername
            LIMIT 100
            """,
        )
    return [dict(r) for r in rows]


# ── Otorisasi dispatcher ──────────────────────────────────────────────────────

async def create_from_payload(payload: dict, user_id: str, branch_code: str) -> int | None:
    action = payload.get("action", "create")
    if action == "create":
        return await _create(payload, user_id, branch_code)
    elif action == "edit":
        await _update(payload, user_id, branch_code)
        return None
    elif action == "delete":
        await _delete(payload)
        return None
    raise ValueError(f"Unknown action: {action}")


async def _create(payload: dict, user_id: str, branch_code: str) -> int:
    ownercode     = (payload.get("ownercode") or "").strip()
    ownername     = (payload.get("ownername") or "").strip()
    is_detail     = payload.get("is_detail", "T")
    parentownerid = payload.get("parentownerid") or None
    status        = payload.get("status", "A")

    if not ownercode:
        raise HTTPException(422, "ownercode wajib diisi")
    if not ownername:
        raise HTTPException(422, "ownername wajib diisi")
    if is_detail == "T" and not parentownerid:
        raise HTTPException(422, "parentownerid wajib diisi untuk node detail")

    existing = await fetch_one(
        "SELECT ownerid FROM transaction.budgetowner WHERE ownercode = $1", ownercode
    )
    if existing:
        raise HTTPException(409, f"Kode pemilik '{ownercode}' sudah digunakan")

    level = 1
    if parentownerid:
        parent = await fetch_one(
            "SELECT level, is_detail FROM transaction.budgetowner WHERE ownerid = $1",
            parentownerid,
        )
        if not parent:
            raise HTTPException(422, "Parent tidak ditemukan")
        if parent["is_detail"] == "T":
            raise HTTPException(422, "Parent harus bertipe Induk (is_detail='F')")
        level = int(parent["level"]) + 1

    row = await fetch_one(
        """
        INSERT INTO transaction.budgetowner
            (ownercode, ownername, level, is_detail, parentownerid, status, userpengubah, terminalubah)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        RETURNING ownerid
        """,
        ownercode, ownername, level, is_detail, parentownerid, status, user_id, branch_code,
    )
    ownerid = int(row["ownerid"])
    await _insert_hierarchy(ownerid, parentownerid)
    return ownerid


async def _insert_hierarchy(ownerid: int, parentownerid: int | None) -> None:
    await execute(
        "INSERT INTO transaction.budgetownerhierarchy (childownerid, parentownerid, level) VALUES ($1, $1, 0)",
        ownerid,
    )
    if not parentownerid:
        return
    ancestors = await fetch_all(
        """
        SELECT parentownerid, level
        FROM transaction.budgetownerhierarchy
        WHERE childownerid = $1
        ORDER BY level
        """,
        parentownerid,
    )
    for anc in ancestors:
        await execute(
            "INSERT INTO transaction.budgetownerhierarchy (childownerid, parentownerid, level) VALUES ($1, $2, $3)",
            ownerid, anc["parentownerid"], int(anc["level"]) + 1,
        )


async def _update(payload: dict, user_id: str, branch_code: str) -> None:
    ownerid   = payload.get("ownerid")
    ownername = (payload.get("ownername") or "").strip()
    status    = payload.get("status", "A")

    if not ownerid:
        raise HTTPException(422, "ownerid wajib diisi")
    if not ownername:
        raise HTTPException(422, "ownername wajib diisi")

    existing = await fetch_one(
        "SELECT ownerid FROM transaction.budgetowner WHERE ownerid = $1", ownerid
    )
    if not existing:
        raise HTTPException(404, "Pemilik anggaran tidak ditemukan")

    await execute(
        """
        UPDATE transaction.budgetowner
        SET ownername = $1, status = $2, userpengubah = $3, terminalubah = $4,
            tglubah = CURRENT_TIMESTAMP
        WHERE ownerid = $5
        """,
        ownername, status, user_id, branch_code, ownerid,
    )


async def _delete(payload: dict) -> None:
    ownerid = payload.get("ownerid")
    if not ownerid:
        raise HTTPException(422, "ownerid wajib diisi")

    has_children = await fetch_one(
        "SELECT EXISTS(SELECT 1 FROM transaction.budgetowner WHERE parentownerid = $1) AS x",
        ownerid,
    )
    if has_children and has_children["x"]:
        raise HTTPException(409, "Tidak bisa dihapus — ada pemilik anggaran child")

    try:
        has_budget = await fetch_one(
            "SELECT EXISTS(SELECT 1 FROM transaction.budget WHERE budgetownerid = $1) AS x",
            ownerid,
        )
        if has_budget and has_budget["x"]:
            raise HTTPException(409, "Tidak bisa dihapus — ada data anggaran yang merujuk record ini")
    except HTTPException:
        raise
    except Exception as exc:
        if "does not exist" not in str(exc).lower():
            raise

    await execute(
        "DELETE FROM transaction.budgetownerhierarchy WHERE childownerid = $1", ownerid
    )
    await execute(
        "DELETE FROM transaction.budgetowner WHERE ownerid = $1", ownerid
    )

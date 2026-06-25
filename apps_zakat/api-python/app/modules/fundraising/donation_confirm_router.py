from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.fundraising.donation_confirm_schema import UpdateDonorBody
from app.modules.fundraising.donation_confirm_service import (
    delete_transaction,
    get_receipt,
    list_transactions,
    post_journal,
    update_donor,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix="/fundraising/donation-confirm", tags=["fundraising-donation-confirm"])


# ── List Transactions ─────────────────────────────────────────────────────────

@router.get("")
async def list_donation_transactions(
    begin_date: str = Query(..., description="ISO YYYY-MM-DD"),
    end_date: str = Query(..., description="ISO YYYY-MM-DD"),
    branch_code: str | None = Query(default=None),
    is_all_branch: bool = Query(default=False),
    search_category: int | None = Query(default=None, description="1=donor_no, 2=donor_name"),
    search_text: str | None = Query(default=None),
    amount_from: float | None = Query(default=None),
    amount_to: float | None = Query(default=None),
    description: str | None = Query(default=None),
    limit: int = Query(default=25, ge=1, le=500),
    page: int = Query(default=1, ge=1),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    try:
        result = await list_transactions(
            begin_date=begin_date,
            end_date=end_date,
            branch_code=branch_code,
            is_all_branch=is_all_branch,
            search_category=search_category,
            search_text=search_text,
            amount_from=amount_from,
            amount_to=amount_to,
            description=description,
            limit=limit,
            page=page,
        )
        return ok({
            "rows": [r.model_dump() for r in result.rows],
            "pagination": result.pagination.model_dump(),
        })
    except ValueError as e:
        return JSONResponse(status_code=400, content=err("VALIDATION_ERROR", str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))


# ── Delete Transaction ────────────────────────────────────────────────────────

@router.delete("/{transaction_id}")
async def delete_donation_transaction(
    transaction_id: int,
    user_branch_code: str | None = Query(default=None),
    user_branch_access: str = Query(default="single"),
    user_roles: str | None = Query(default=None),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    roles = [r.strip() for r in user_roles.split(",")] if user_roles else []

    try:
        await delete_transaction(
            transaction_id=transaction_id,
            user_branch_code=user_branch_code,
            user_branch_access=user_branch_access,
            user_roles=roles,
        )
        return ok({"status": "deleted", "transaction_id": transaction_id})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=err("HTTP_ERROR", e.detail))
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))


# ── Update Donor ──────────────────────────────────────────────────────────────

@router.put("/{transaction_item_id}/donor")
async def update_donation_donor(
    transaction_item_id: int,
    body: UpdateDonorBody,
):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    try:
        await update_donor(
            transaction_item_id=transaction_item_id,
            donor_no=body.donor_no,
            donor_name=body.donor_name,
        )
        return ok({"status": "updated", "transaction_item_id": transaction_item_id})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=err("HTTP_ERROR", e.detail))
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))


# ── Post Journal (Placeholder) ────────────────────────────────────────────────

@router.post("/{transaction_id}/post-journal")
async def post_donation_journal(transaction_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    try:
        await post_journal(transaction_id)
        return ok({"status": "posted", "transaction_id": transaction_id})
    except NotImplementedError as e:
        return JSONResponse(
            status_code=501,
            content=err("NOT_IMPLEMENTED", "Fitur post_journal belum diimplementasi"),
        )
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))


# ── Receipt (Placeholder) ─────────────────────────────────────────────────────

@router.get("/{transaction_id}/receipt")
async def get_donation_receipt(transaction_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    try:
        receipt = await get_receipt(transaction_id)
        return ok({"receipt": receipt})
    except NotImplementedError as e:
        return JSONResponse(
            status_code=501,
            content=err("NOT_IMPLEMENTED", "Fitur receipt belum diimplementasi"),
        )
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))

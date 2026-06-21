from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.finance.budget import service
from app.modules.finance.budget.schema import (
    BudgetEditRequest,
    BudgetImportRequest,
    BudgetMasterItemRequest,
    BudgetNewRequest,
    BudgetReviseRequest,
)

from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix="/finance/budget", tags=["budget"])


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get("/owners")
async def list_budget_owners(
    include_parent: bool = Query(default=False),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await service.get_budget_owners(include_parent=include_parent)
    return ok({"data": [item.model_dump() for item in data]})


@router.get("/periods")
async def list_budget_periods():
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await service.get_budget_periods()
    return ok({"data": [item.model_dump() for item in data]})


@router.get("/periods/{owner_id}")
async def list_periods_for_owner(
    owner_id: int,
    branch_code: str | None = Query(default=None),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await service.get_budget_periods_for_owner(owner_id, branch_code or "")
    return ok({"data": [item.model_dump() for item in data]})


# ── Summary per Owner ─────────────────────────────────────────────────────────

@router.get("/summary")
async def get_budget_summary(
    period_id: int = Query(...),
    branch_code: str | None = Query(default=None),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))
    data = await service.get_budget_owner_summary(period_id, branch_code or "")
    return ok(data.model_dump())


# ── List ───────────────────────────────────────────────────────────────────────

@router.get("")
async def list_budgets(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=500),
    owner_id: int | None = Query(default=None),
    period_id: int | None = Query(default=None),
    branch_code: str | None = Query(default=None),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await service.list_budgets(
        page=page,
        limit=limit,
        owner_id=owner_id,
        period_id=period_id,
        branch_code=branch_code,
    )
    return ok(data.model_dump())


# ── Detail ────────────────────────────────────────────────────────────────────

@router.get("/{budget_id}")
async def get_budget_detail(budget_id: int):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await service.get_budget_detail(budget_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return ok(data.model_dump())


# ── Create ────────────────────────────────────────────────────────────────────

@router.post("")
async def create_budget(
    payload: BudgetNewRequest,
    branch_code: str = Query(...),
    user_id: str = Query(...),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    try:
        result = await service.create_budget(payload, branch_code, user_id)
        return ok(result)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


# ── Edit ───────────────────────────────────────────────────────────────────────

@router.put("/{budget_id}")
async def edit_budget(
    budget_id: int,
    payload: BudgetEditRequest,
    user_id: str = Query(...),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    try:
        result = await service.edit_budget(
            budget_id,
            payload.budget_code,
            payload.item_group,
            payload.item_name,
            payload.amount,
            user_id,
        )
        return ok(result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Delete ────────────────────────────────────────────────────────────────────

@router.delete("/{budget_id}")
async def delete_budget(budget_id: int):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    await service.delete_budget(budget_id)
    return ok({"budget_id": budget_id, "deleted": True})


# ── Revise ────────────────────────────────────────────────────────────────────

@router.post("/revise")
async def revise_budget(
    payload: BudgetReviseRequest,
    user_id: str = Query(...),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    result = await service.revise_budget(payload, user_id)
    return ok(result)


# ── Import ────────────────────────────────────────────────────────────────────

@router.post("/import")
async def import_budgets(
    payload: BudgetImportRequest,
    branch_code: str = Query(...),
    user_id: str = Query(...),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    result = await service.import_budgets(payload, branch_code, user_id)
    return ok(result)


# ── Transactions ───────────────────────────────────────────────────────────────

@router.get("/{budget_id}/transactions")
async def get_budget_transactions(
    budget_id: int,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=100),
    begin_date: str | None = Query(default=None),
    end_date: str | None = Query(default=None),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await service.get_budget_transactions(
        budget_id,
        page=page,
        limit=limit,
        begin_date=begin_date,
        end_date=end_date,
    )
    return ok(data.model_dump())


# ── Search ────────────────────────────────────────────────────────────────────

# ── Parameter: BudgetItem master ──────────────────────────────────────────────

@router.get("/parameter/items")
async def list_parameter_items(
    owner_id: int | None = Query(default=None),
    branch_code: str | None = Query(default=None),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))
    data = await service.list_master_items(owner_id=owner_id, branch_code=branch_code)
    return ok({"data": [item.model_dump() for item in data]})


@router.post("/parameter/items")
async def create_parameter_item(payload: BudgetMasterItemRequest):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))
    result = await service.create_master_item(payload)
    return ok(result)


@router.put("/parameter/items/{item_id}")
async def update_parameter_item(item_id: int, payload: BudgetMasterItemRequest):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))
    try:
        result = await service.update_master_item(item_id, payload)
        return ok(result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/parameter/items/{item_id}")
async def delete_parameter_item(item_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))
    try:
        await service.delete_master_item(item_id)
        return ok({"item_id": item_id, "deleted": True})
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


# ── Parameter: BudgetPeriod master ────────────────────────────────────────────

@router.get("/parameter/periods")
async def list_parameter_periods():
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))
    data = await service.list_master_periods()
    return ok({"data": [item.model_dump() for item in data]})


@router.post("/parameter/periods")
async def create_parameter_period(year: int = Query(...)):
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))
    try:
        result = await service.create_master_period(year)
        return ok(result)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


# ── Search ────────────────────────────────────────────────────────────────────

@router.get("/search/codes")
async def search_budget_codes(
    actual_date: str = Query(...),
    branch_code: str = Query(...),
    filter_category: str | None = Query(default=None),
    filter_text: str | None = Query(default=None),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await service.search_budget_codes(
        actual_date,
        branch_code,
        filter_category=filter_category,
        filter_text=filter_text,
    )
    return ok({"data": [item.model_dump() for item in data]})

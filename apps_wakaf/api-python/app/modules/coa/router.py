from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from app.modules.coa.service import list_accounts
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix="/coa", tags=["coa"])


@router.get("/accounts")
async def accounts(
    search: str | None = Query(default=None, max_length=100),
    limit: int = Query(default=1000, ge=1, le=5000),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await list_accounts(search=search, limit=limit)
    return ok(data.model_dump())

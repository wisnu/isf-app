import os
from datetime import datetime

from fastapi import APIRouter, Query, Response
from fastapi.responses import JSONResponse

from app.modules.coa.export import build_coa_xlsx
from app.modules.coa.service import list_accounts, list_all_rows
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix="/coa", tags=["coa"])


@router.get("/accounts")
async def accounts(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    data = await list_accounts(search=search, page=page, page_size=page_size)
    return ok(data.model_dump())


@router.get("/accounts.xlsx")
async def export_xlsx(
    search: str | None = Query(default=None, max_length=100),
):
    if not await ping():
        return JSONResponse(
            status_code=503,
            content=err("DB_UNAVAILABLE", "Database connection not ready"),
        )
    rows = await list_all_rows(search=search)
    domain = os.getenv("DOMAIN", "").strip().lower()
    suffix = f"-{domain}" if domain else ""
    filename = f"coa{suffix}-{datetime.utcnow():%Y%m%d}.xlsx"
    title = "Chart of Accounts" + (f" · {domain.upper()}" if domain else "")
    xlsx_bytes = build_coa_xlsx(rows, title=title)
    return Response(
        content=xlsx_bytes,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )

"""Router for fundraising export endpoints.

Endpoints:
- GET /api/fundraising/export/hc-batches — List HC batches for dropdown
- GET /api/fundraising/export/hc-batch — Export HC Batch to Excel
- GET /api/fundraising/export/date-range — Export Website (date-range) to Excel
"""

from __future__ import annotations

import io
from datetime import date

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse

from app.modules.fundraising.export_service import (
    export_hc_batch,
    export_website_new,
    list_hc_batches,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix="/fundraising/export", tags=["fundraising-export"])


# ── HC Batch Dropdown ──────────────────────────────────────────────────────────


@router.get("/hc-batches")
async def get_hc_batches_list():
    """List HC batches for dropdown selection.

    Returns list of { id, name, batch_date } sorted by date DESC.
    """
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    try:
        batches = await list_hc_batches()
        return ok([b.model_dump(mode="json") for b in batches])
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))


# ── HC Batch Export ───────────────────────────────────────────────────────────


@router.get("/hc-batch")
async def download_hc_batch_export(
    batch_id: int = Query(..., gt=0, description="Batch ID to export")
):
    """Download HC Batch export as Excel.

    Query params:
    - batch_id (int, required, > 0): Batch ID to export

    Returns: Excel file (application/vnd.ms-excel)
    Content-Disposition: attachment; filename="DonationList_BATCH_001.xlsx"
    """
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    try:
        xlsx_bytes = await export_hc_batch(batch_id)
        batch_id_padded = str(batch_id).zfill(3)
        filename = f"DonationList_BATCH_{batch_id_padded}.xlsx"
        return StreamingResponse(
            io.BytesIO(xlsx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=err("NOT_FOUND", e.detail))
    except ValueError as e:
        return JSONResponse(status_code=400, content=err("VALIDATION_ERROR", str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))


# ── Website (Date-Range) Export ───────────────────────────────────────────────


@router.get("/date-range")
async def download_website_new_export(
    date_from: str = Query(..., description="Start date (ISO YYYY-MM-DD)"),
    date_to: str = Query(..., description="End date (ISO YYYY-MM-DD)"),
):
    """Download Website donation data export as Excel (date-range with product pivot).

    Query params:
    - date_from (string, required): Start date in ISO format YYYY-MM-DD
    - date_to (string, required): End date in ISO format YYYY-MM-DD

    Returns: Excel file (application/vnd.ms-excel)
    Content-Disposition: attachment; filename="DonorTransactionList_YYYY-MM-DD_to_YYYY-MM-DD.xlsx"
    """
    if not await ping():
        return JSONResponse(status_code=503, content=err("DB_UNAVAILABLE", "Database not ready"))

    try:
        # Parse date strings
        date_from_obj = date.fromisoformat(date_from)
        date_to_obj = date.fromisoformat(date_to)

        xlsx_bytes = await export_website_new(date_from_obj, date_to_obj)
        filename = f"DonorTransactionList_{date_from}_{date_to}.xlsx"
        return StreamingResponse(
            io.BytesIO(xlsx_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except ValueError as e:
        return JSONResponse(status_code=422, content=err("VALIDATION_ERROR", str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err("INTERNAL_ERROR", str(e)))

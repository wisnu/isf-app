from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, Response

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, stream_api_python

_HC_BATCH_MENU = "fundraising.report.export-penghimpunan-website-hc-batch"
_DATE_RANGE_MENU = "fundraising.report.export-penghimpunan-website-new"
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

router = APIRouter(
    prefix="/api/fundraising/export-penghimpunan-website",
    tags=["fundraising-export"],
)


# ── GET /api/fundraising/export-penghimpunan-website/hc-batches ─────────────────
# List HC batches for dropdown
@router.get("/hc-batches")
async def list_hc_batches(
    request: Request,
    _: str = Depends(require_menu(_HC_BATCH_MENU)),
):
    """List HC batches for dropdown selection.

    Returns JSON list of { id, name, batch_date }.
    """
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    downstream = await get_api_python("/api/fundraising/export/hc-batches")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── GET /api/fundraising/export-penghimpunan-website/hc-batch ──────────────────
# Download HC Batch export as Excel
@router.get("/hc-batch")
async def download_hc_batch(
    request: Request,
    batch_id: int = Query(..., gt=0, description="Batch ID to export"),
    _: str = Depends(require_menu(_HC_BATCH_MENU)),
):
    """Download HC Batch export as Excel (9 columns).

    Query params:
    - batch_id (int, required, > 0): Batch ID to export

    Returns: Excel file (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
    Content-Disposition: attachment; filename="DonationList_BATCH_001.xlsx"
    """
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    downstream = await stream_api_python(
        "/api/fundraising/export/hc-batch",
        params={"batch_id": batch_id},
    )

    if downstream.status_code != 200:
        # Error response from api-python (404, 422, etc.)
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition", f'attachment; filename="DonationList_BATCH_{batch_id:03d}.xlsx"'
            )
        },
    )


# ── GET /api/fundraising/export-penghimpunan-website/date-range ────────────────
# Download Website (date-range) export as Excel
@router.get("/date-range")
async def download_date_range(
    request: Request,
    date_from: str = Query(..., description="Start date (ISO YYYY-MM-DD)"),
    date_to: str = Query(..., description="End date (ISO YYYY-MM-DD)"),
    _: str = Depends(require_menu(_DATE_RANGE_MENU)),
):
    """Download Website donation data export as Excel (date-range with product pivot, 32 columns).

    Query params:
    - date_from (string, required): Start date in ISO format YYYY-MM-DD
    - date_to (string, required): End date in ISO format YYYY-MM-DD

    Returns: Excel file (application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
    Content-Disposition: attachment; filename="DonorTransactionList_YYYY-MM-DD_YYYY-MM-DD.xlsx"
    """
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp

    downstream = await stream_api_python(
        "/api/fundraising/export/date-range",
        params={"date_from": date_from, "date_to": date_to},
    )

    if downstream.status_code != 200:
        # Error response from api-python (422, 503, etc.)
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())

    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={
            "Content-Disposition": downstream.headers.get(
                "content-disposition",
                f'attachment; filename="DonorTransactionList_{date_from}_{date_to}.xlsx"'
            )
        },
    )

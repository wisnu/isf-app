"""FastAPI router for HC ZIS upload endpoints."""
from __future__ import annotations

from fastapi import APIRouter, File, Query, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse

from app.shared.response import ok, err
from . import hc_zis_service
from .hc_zis_schema import HCZisSubmitRequest, HCZisUpdateDateRequest


router = APIRouter(prefix="/transaction", tags=["transaction-hc-zis"])


@router.post("/upload/hc-zis/parse")
async def parse_upload(
    file: UploadFile = File(...),
    tanggal_transaksi: str = Query(...),
):
    """Parse HC ZIS Excel file and return preview.

    POST /api/transaksi/upload/hc-zis/parse
    Content-Type: multipart/form-data
    - file: .xlsx or .xls
    - tanggal_transaksi: ISO YYYY-MM-DD

    Returns: {batch_period_desc, totals, items[], is_duplicate}
    """
    filename = file.filename or "upload"
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ("xls", "xlsx"):
        return JSONResponse(
            status_code=400,
            content=err("INVALID_FORMAT", "Hanya file .xls dan .xlsx yang diterima"),
        )

    try:
        data = await file.read()
        result = await hc_zis_service.parse_and_validate(filename, data, tanggal_transaksi)

        response_data = result.model_dump()
        if result.is_duplicate:
            # Still return 200 with is_duplicate=True flag for UI to show warning
            pass

        return ok(response_data)

    except ValueError as exc:
        return JSONResponse(
            status_code=400,
            content=err("PARSE_ERROR", str(exc)),
        )
    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=err("SERVER_ERROR", str(exc)),
        )


@router.post("/upload/hc-zis/submit")
async def submit_upload(
    req: HCZisSubmitRequest,
    user_id: str = Query(default=''),
    branch_code: str = Query(default=''),
):

    try:
        result = await hc_zis_service.submit_upload(req, user_id, branch_code)
        return ok({
            "submission_id": result["id"],
            "status": result["status"],
            "kode_entri": "TRANS041",
            "entity_type": "hc_zis_upload",
        })
    except Exception as exc:
        return JSONResponse(
            status_code=400,
            content=err("SUBMIT_ERROR", str(exc)),
        )


@router.get("/upload/hc-zis/batches")
async def list_batches(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    batch_period_desc: str | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    branch_code: str = Query(default=''),
):
    """List all HC ZIS batches.

    GET /api/transaksi/upload/hc-zis/batches?page=1&limit=25&batch_period_desc=...&date_from=...&date_to=...

    Returns: {rows: [{batch_id, batch_period_desc, tanggal_transaksi, ...}], pagination: {...}}
    """
    try:
        rows, total = await hc_zis_service.list_batches(
            branch_code=branch_code,
            page=page,
            limit=limit,
            batch_period_desc=batch_period_desc,
            date_from=date_from,
            date_to=date_to,
        )

        return ok({
            "rows": [r.model_dump() for r in rows],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": -(-total // limit),
            },
        })

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=err("LIST_ERROR", str(exc)),
        )


@router.get("/upload/hc-zis/batches/{batch_id}")
async def get_batch_detail(batch_id: int):
    """Get batch detail with all items.

    GET /api/transaksi/upload/hc-zis/batches/{batch_id}

    Returns: {batch_id, batch_period_desc, items: [...], totals: {...}}
    """
    try:
        detail = await hc_zis_service.get_batch_detail(batch_id)
        if not detail:
            return JSONResponse(
                status_code=404,
                content=err("NOT_FOUND", f"Batch {batch_id} tidak ditemukan"),
            )

        return ok(detail.model_dump())

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content=err("DETAIL_ERROR", str(exc)),
        )


@router.put("/upload/hc-zis/batches/{batch_id}/date")
async def update_batch_date(
    batch_id: int,
    req: HCZisUpdateDateRequest,
    user_id: str = Query(default=''),
    branch_code: str = Query(default=''),
):

    try:
        result = await hc_zis_service.submit_update_date(
            batch_id, req, user_id, branch_code
        )

        return ok({
            "submission_id": result["id"],
            "status": result["status"],
            "kode_entri": "TRANS044",
            "entity_type": "hc_zis_update_date",
        })

    except ValueError as exc:
        return JSONResponse(
            status_code=404,
            content=err("NOT_FOUND", str(exc)),
        )
    except Exception as exc:
        return JSONResponse(
            status_code=400,
            content=err("UPDATE_ERROR", str(exc)),
        )


@router.delete("/upload/hc-zis/batches/{batch_id}")
async def delete_batch(
    batch_id: int,
    user_id: str = Query(default=''),
    branch_code: str = Query(default=''),
):

    try:
        result = await hc_zis_service.submit_delete(batch_id, user_id, branch_code)

        return ok({
            "submission_id": result["id"],
            "status": result["status"],
            "kode_entri": "TRANS043",
            "entity_type": "hc_zis_delete",
        })

    except ValueError as exc:
        return JSONResponse(
            status_code=404,
            content=err("NOT_FOUND", str(exc)),
        )
    except Exception as exc:
        return JSONResponse(
            status_code=400,
            content=err("DELETE_ERROR", str(exc)),
        )

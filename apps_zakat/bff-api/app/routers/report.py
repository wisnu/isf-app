from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401
from app.services.proxy import get_report_api

router = APIRouter(prefix="/report", tags=["report"])


@router.get("/ping")
async def ping(request: Request):
    """Scaffold — proxy ke report-api /report/ping (auth-gated).
    Endpoint report fungsional ditambahkan di sini saat dibangun."""
    _, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    downstream = await get_report_api("/api/report/ping")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

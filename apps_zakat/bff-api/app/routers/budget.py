from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import (
    get_api_python,
    post_api_python,
    post_multipart_api_python,
)
from app.shared.config import settings
from app.shared.response import ok

router = APIRouter(prefix="/budget", tags=["budget"])

_MENU_INQUIRY = "finance.budget.inquiry"
_MENU_REVISI = "finance.budget.revise"
_MENU_IMPORT = "finance.budget.import"


def _session(request: Request) -> dict:
    """Extract user_id and branch from session, respecting branch access rules."""
    user_id = request.session.get("user_id", "")
    access = request.session.get("branch_access", "single")
    primary = request.session.get("primary_branch") or ""
    # If branch_access='all', pass empty string (api-python will decide)
    # If branch_access='single', pass primary_branch
    branch = "" if access == "all" else primary
    return {"user_id": user_id, "branch": branch}


# ---------------------------------------------------------------------------
# Lookup endpoints (used by forms)
# ---------------------------------------------------------------------------


@router.get("/owners")
async def get_owners(
    request: Request,
    _: str = Depends(require_menu(_MENU_INQUIRY)),
):
    """List BudgetOwner (is_detail='T'). Lookup endpoint, no pagination."""
    downstream = await get_api_python("/api/budget/owners")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/periods")
async def get_periods(
    request: Request,
    _: str = Depends(require_menu(_MENU_INQUIRY)),
):
    """List tahun anggaran (parentperiodid IS NULL). Lookup endpoint, no pagination."""
    downstream = await get_api_python("/api/budget/periods")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/periods/{owner_id}")
async def get_periods_by_owner(
    request: Request,
    owner_id: int,
    _: str = Depends(require_menu(_MENU_INQUIRY)),
):
    """List periode per owner (query: branch_code). Lookup endpoint, no pagination."""
    s = _session(request)
    params: dict = {}
    if s["branch"]:
        params["branch_code"] = s["branch"]
    downstream = await get_api_python(f"/api/budget/periods/{owner_id}", params=params or None)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/search/codes")
async def search_codes(
    request: Request,
    actual_date: str = Query(...),
    filter_category: str | None = Query(default=None),
    filter_text: str | None = Query(default=None),
    _: str = Depends(require_menu(_MENU_INQUIRY)),
):
    """Lookup kode anggaran berdasar tanggal transaksi."""
    s = _session(request)
    params: dict = {"actual_date": actual_date}
    if s["branch"]:
        params["branch_code"] = s["branch"]
    if filter_category:
        params["filter_category"] = filter_category
    if filter_text:
        params["filter_text"] = filter_text
    downstream = await get_api_python("/api/budget/search/codes", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# Parameter master endpoints (BudgetItem + BudgetPeriod)
# ---------------------------------------------------------------------------

_MENU_PARAM = "finance.parameter.budget.item"
_MENU_PERIOD = "finance.parameter.budget.period"


@router.get("/parameter/items")
async def get_parameter_items(
    request: Request,
    owner_id: int | None = Query(default=None),
    _: str = Depends(require_menu(_MENU_PARAM)),
):
    """List master BudgetItem."""
    s = _session(request)
    params: dict = {}
    if owner_id:
        params["owner_id"] = owner_id
    if s["branch"]:
        params["branch_code"] = s["branch"]
    downstream = await get_api_python("/api/budget/parameter/items", params=params or None)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/parameter/items")
async def create_parameter_item(
    request: Request,
    _: str = Depends(require_menu(_MENU_PARAM)),
):
    """Buat BudgetItem baru."""
    body = await request.json()
    downstream = await post_api_python("/api/budget/parameter/items", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/parameter/items/{item_id}")
async def update_parameter_item(
    request: Request,
    item_id: int,
    _: str = Depends(require_menu(_MENU_PARAM)),
):
    """Update BudgetItem."""
    body = await request.json()
    downstream = await post_api_python(f"/api/budget/parameter/items/{item_id}", json_body=body, method="PUT")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete("/parameter/items/{item_id}")
async def delete_parameter_item(
    request: Request,
    item_id: int,
    _: str = Depends(require_menu(_MENU_PARAM)),
):
    """Hapus BudgetItem."""
    downstream = await post_api_python(f"/api/budget/parameter/items/{item_id}", json_body={}, method="DELETE")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/parameter/periods")
async def get_parameter_periods(
    request: Request,
    _: str = Depends(require_menu(_MENU_PERIOD)),
):
    """List master BudgetPeriod (tahun root)."""
    downstream = await get_api_python("/api/budget/parameter/periods")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/parameter/periods")
async def create_parameter_period(
    request: Request,
    year: int = Query(...),
    _: str = Depends(require_menu(_MENU_PERIOD)),
):
    """Buat tahun anggaran baru + 12 bulan otomatis."""
    downstream = await post_api_python(f"/api/budget/parameter/periods?year={year}", json_body={})
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# Summary per owner (inquiry)
# ---------------------------------------------------------------------------


@router.get("/summary")
async def get_budget_summary(
    request: Request,
    period_id: int = Query(...),
    _: str = Depends(require_menu(_MENU_INQUIRY)),
):
    """Summary anggaran per pemilik untuk satu tahun."""
    s = _session(request)
    params: dict = {"period_id": period_id}
    if s["branch"]:
        params["branch_code"] = s["branch"]
    downstream = await get_api_python("/api/budget/summary", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# List & Detail endpoints (inquiry + revisi)
# ---------------------------------------------------------------------------


@router.get("/")
async def list_budgets(
    request: Request,
    _: str = Depends(require_menu(_MENU_INQUIRY)),
    owner_id: int | None = Query(default=None),
    period_id: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=25, ge=1, le=500),
):
    """List BudgetYear dengan filter owner_id, period_id, dan branch_code."""
    s = _session(request)
    params: dict = {"page": page, "limit": limit}
    if owner_id:
        params["owner_id"] = owner_id
    if period_id:
        params["period_id"] = period_id
    if s["branch"]:
        params["branch_code"] = s["branch"]
    downstream = await get_api_python("/api/budget", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/{budget_id}")
async def get_budget(
    request: Request,
    budget_id: int,
    _: str = Depends(require_menu(_MENU_INQUIRY)),
):
    """Detail satu anggaran (BudgetYear + items)."""
    downstream = await get_api_python(f"/api/budget/{budget_id}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/{budget_id}/transactions")
async def get_budget_transactions(
    request: Request,
    budget_id: int,
    _: str = Depends(require_menu(_MENU_INQUIRY)),
):
    """Histori transaksi yang meng-reference anggaran ini."""
    downstream = await get_api_python(f"/api/budget/{budget_id}/transactions")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# Create (POST /) — dengan otorisasi TRANS038
# ---------------------------------------------------------------------------


@router.post("/", status_code=201)
async def create_budget(
    request: Request,
    _: str = Depends(require_menu(_MENU_IMPORT)),
):
    """Buat anggaran baru. Menggunakan otorisasi save-and-submit (TRANS038)."""
    s = _session(request)
    body = await request.json()
    # Inject session info
    body["inputer_id"] = s["user_id"]
    if s["branch"]:
        body["branch_code"] = s["branch"]

    # Submit via otorisasi save-and-submit
    params = {"user_id": s["user_id"], "branch_code": s["branch"] or "001"}
    url = f"{settings.api_python_base_url}/api/otorisasi/save-and-submit/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            url,
            json={
                "entity_type": "budget",
                "payload": body,
            },
            params=params,
        )
    return JSONResponse(status_code=resp.status_code, content=resp.json())


# ---------------------------------------------------------------------------
# Update (PUT /{budget_id}) — dengan otorisasi TRANS037
# ---------------------------------------------------------------------------


@router.put("/{budget_id}")
async def update_budget(
    request: Request,
    budget_id: int,
    _: str = Depends(require_menu(_MENU_REVISI)),
):
    """Edit anggaran. Menggunakan otorisasi save-and-submit (TRANS037)."""
    s = _session(request)
    body = await request.json()
    # Inject session info
    body["inputer_id"] = s["user_id"]
    if s["branch"]:
        body["branch_code"] = s["branch"]

    # Submit via otorisasi save-and-submit (update existing submission)
    params = {"user_id": s["user_id"]}
    url = f"{settings.api_python_base_url}/api/otorisasi/save-and-submit/{budget_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.put(
            url,
            json={
                "entity_type": "budget",
                "payload": body,
            },
            params=params,
        )
    return JSONResponse(status_code=resp.status_code, content=resp.json())


# ---------------------------------------------------------------------------
# Delete (DELETE /{budget_id}) — langsung (tidak via otorisasi)
# ---------------------------------------------------------------------------


@router.delete("/{budget_id}")
async def delete_budget(
    request: Request,
    budget_id: int,
    _: str = Depends(require_menu(_MENU_REVISI)),
):
    """Hapus anggaran. Langsung ke api-python (tidak via otorisasi)."""
    downstream = await post_api_python(
        f"/api/budget/{budget_id}",
        json_body={},
        method="DELETE",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# Batch revise (POST /revise) — langsung (tidak via otorisasi)
# ---------------------------------------------------------------------------


@router.post("/revise")
async def revise_batch(
    request: Request,
    _: str = Depends(require_menu(_MENU_REVISI)),
):
    """Revisi amount batch. Langsung ke api-python (tidak via otorisasi)."""
    s = _session(request)
    body = await request.json()
    # Inject session info
    body["inputer_id"] = s["user_id"]
    if s["branch"]:
        body["branch_code"] = s["branch"]

    downstream = await post_api_python(
        "/api/budget/revise",
        json_body=body,
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ---------------------------------------------------------------------------
# Import Excel (POST /import) — dengan otorisasi TRANS036
# Menggunakan multipart/form-data
# ---------------------------------------------------------------------------


@router.post("/import")
async def import_budget(
    request: Request,
    _: str = Depends(require_menu(_MENU_IMPORT)),
    file: UploadFile = File(...),
):
    """Import anggaran dari Excel. Menggunakan otorisasi save-and-submit (TRANS036)."""
    s = _session(request)
    file_data = await file.read()

    # Prepare multipart data dengan session info
    data_fields = {
        "user_id": s["user_id"],
    }
    if s["branch"]:
        data_fields["branch_code"] = s["branch"]

    # Wrap payload dalam entity_type untuk otorisasi
    data_fields["entity_type"] = "budget_import"

    downstream = await post_multipart_api_python(
        "/api/otorisasi/save-and-submit/",
        data=data_fields,
        file_content=file_data,
        file_field="file",
        filename=file.filename or "import.xlsx",
        content_type=file.content_type or "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python, get_report_api, stream_report_api
from app.shared.response import err

router = APIRouter(prefix="/api/generalaffair", tags=["generalaffair"])

_DOC_TYPE_MENU = "generalaffair.parameter.document-type"
_INCOMING_MENU = "generalaffair.document.incoming"
_OUTGOING_MENU = "generalaffair.document.outgoing"
_REPORT_INCOMING_MENU = "generalaffair.report.incoming-document"
_REPORT_OUTGOING_MENU = "generalaffair.report.outgoing-document"
_XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _resolve_branch(request: Request, branch: str | None) -> tuple[str | None, JSONResponse | None]:
    """Resolve branch dari session berdasarkan branch_access."""
    access = request.session.get("branch_access", "single")
    primary = request.session.get("primary_branch")
    bp = (branch or "").strip()
    is_all_req = bp == "" or bp.upper() == "ALL"

    if access == "all":
        return (None if is_all_req else bp), None

    if not primary:
        return None, JSONResponse(
            status_code=403, content=err("NO_BRANCH", "User tidak punya cabang default")
        )
    if bp == "" or bp == primary:
        return primary, None
    return None, JSONResponse(
        status_code=403,
        content=err("BRANCH_FORBIDDEN", "Anda hanya boleh mengakses cabang sendiri"),
    )


# ── Jenis Dokumen (Parameter) ─────────────────────────────────────────────────

@router.get("/document-types")
async def list_document_types(
    request: Request,
    _: str = Depends(require_menu(_DOC_TYPE_MENU)),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params = {"page": page, "page_size": page_size}
    downstream = await get_api_python("/generalaffair/document-types", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/document-types", status_code=201)
async def create_document_type(
    request: Request,
    _: str = Depends(require_menu(_DOC_TYPE_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python("/generalaffair/document-types", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/document-types/{type_id}")
async def update_document_type(
    request: Request,
    type_id: int,
    _: str = Depends(require_menu(_DOC_TYPE_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f"/generalaffair/document-types/{type_id}",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.delete("/document-types/{type_id}")
async def delete_document_type(
    request: Request,
    type_id: int,
    _: str = Depends(require_menu(_DOC_TYPE_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f"/generalaffair/document-types/{type_id}",
        json_body={},
        method="DELETE",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Work Units Lookup (No Auth) ───────────────────────────────────────────────

@router.get("/document/work-units")
async def list_work_units(request: Request):
    """Lookup work units — tidak perlu menu permission."""
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python("/generalaffair/document/work-units")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Dokumen Masuk ────────────────────────────────────────────────────────────

@router.get("/document/incoming")
async def list_incoming_documents(
    request: Request,
    _: str = Depends(require_menu(_INCOMING_MENU)),
    search: str | None = Query(default=None),
    id_jenis_dokumen: int | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    params: dict = {"page": page, "page_size": page_size}
    if branch_code:
        params["branch"] = branch_code
    if search:
        params["search"] = search
    if id_jenis_dokumen:
        params["id_jenis_dokumen"] = id_jenis_dokumen
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    downstream = await get_api_python("/generalaffair/document/incoming", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/document/incoming/{doc_id}")
async def get_incoming_document(
    request: Request,
    doc_id: int,
    _: str = Depends(require_menu(_INCOMING_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f"/generalaffair/document/incoming/{doc_id}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/document/incoming", status_code=201)
async def create_incoming_document(
    request: Request,
    _: str = Depends(require_menu(_INCOMING_MENU)),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    body = await request.json()
    body["user_input"] = user_id
    body["branch_code"] = branch_code
    downstream = await post_api_python("/generalaffair/document/incoming", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/document/incoming/{doc_id}")
async def update_incoming_document(
    request: Request,
    doc_id: int,
    _: str = Depends(require_menu(_INCOMING_MENU)),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    body["user_input"] = user_id
    downstream = await post_api_python(
        f"/generalaffair/document/incoming/{doc_id}",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Dokumen Keluar ───────────────────────────────────────────────────────────

@router.get("/document/outgoing")
async def list_outgoing_documents(
    request: Request,
    _: str = Depends(require_menu(_OUTGOING_MENU)),
    search: str | None = Query(default=None),
    id_jenis_dokumen: int | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    params: dict = {"page": page, "page_size": page_size}
    if branch_code:
        params["branch"] = branch_code
    if search:
        params["search"] = search
    if id_jenis_dokumen:
        params["id_jenis_dokumen"] = id_jenis_dokumen
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    downstream = await get_api_python("/generalaffair/document/outgoing", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/document/outgoing/{doc_id}")
async def get_outgoing_document(
    request: Request,
    doc_id: int,
    _: str = Depends(require_menu(_OUTGOING_MENU)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f"/generalaffair/document/outgoing/{doc_id}")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post("/document/outgoing", status_code=201)
async def create_outgoing_document(
    request: Request,
    _: str = Depends(require_menu(_OUTGOING_MENU)),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    body = await request.json()
    body["user_input"] = user_id
    body["branch_code"] = branch_code
    downstream = await post_api_python("/generalaffair/document/outgoing", json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/document/outgoing/{doc_id}")
async def update_outgoing_document(
    request: Request,
    doc_id: int,
    _: str = Depends(require_menu(_OUTGOING_MENU)),
):
    user_id, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    body["user_input"] = user_id
    downstream = await post_api_python(
        f"/generalaffair/document/outgoing/{doc_id}",
        json_body=body,
        method="PUT",
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Laporan Dokumen Masuk ────────────────────────────────────────────────────

@router.get("/report/incoming-document")
async def report_incoming_documents(
    request: Request,
    _: str = Depends(require_menu(_REPORT_INCOMING_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    params: dict = {
        "date_from": date_from,
        "date_to": date_to,
        "page": page,
        "page_size": page_size,
        "branch": branch_code,
    }
    if id_jenis_dokumen:
        params["id_jenis_dokumen"] = id_jenis_dokumen
    downstream = await get_report_api("/api/generalaffair/report/incoming-document", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/report/incoming-document/export.xlsx")
async def export_incoming_documents(
    request: Request,
    _: str = Depends(require_menu(_REPORT_INCOMING_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    params: dict = {
        "date_from": date_from,
        "date_to": date_to,
        "branch": branch_code,
    }
    if id_jenis_dokumen:
        params["id_jenis_dokumen"] = id_jenis_dokumen
    return await stream_report_api(
        "/api/generalaffair/report/incoming-document/export.xlsx", params=params
    )


# ── Laporan Dokumen Keluar ───────────────────────────────────────────────────

@router.get("/report/outgoing-document")
async def report_outgoing_documents(
    request: Request,
    _: str = Depends(require_menu(_REPORT_OUTGOING_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    params: dict = {
        "date_from": date_from,
        "date_to": date_to,
        "page": page,
        "page_size": page_size,
        "branch": branch_code,
    }
    if id_jenis_dokumen:
        params["id_jenis_dokumen"] = id_jenis_dokumen
    downstream = await get_report_api("/api/generalaffair/report/outgoing-document", params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get("/report/outgoing-document/export.xlsx")
async def export_outgoing_documents(
    request: Request,
    _: str = Depends(require_menu(_REPORT_OUTGOING_MENU)),
    date_from: str = Query(...),
    date_to: str = Query(...),
    id_jenis_dokumen: int | None = Query(default=None),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    branch_code, err_branch = _resolve_branch(request, None)
    if err_branch:
        return err_branch
    params: dict = {
        "date_from": date_from,
        "date_to": date_to,
        "branch": branch_code,
    }
    if id_jenis_dokumen:
        params["id_jenis_dokumen"] = id_jenis_dokumen
    return await stream_report_api(
        "/api/generalaffair/report/outgoing-document/export.xlsx", params=params
    )

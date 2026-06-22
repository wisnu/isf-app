from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query  # Query used in list endpoints
from fastapi.responses import JSONResponse

from app.modules.generalaffair.document.schema import (
    CreateDocumentTypeBody,
    CreateIncomingBody,
    CreateOutgoingBody,
    UpdateIncomingBody,
    UpdateOutgoingBody,
)
from app.modules.generalaffair.document.service import (
    create_document_type,
    create_incoming,
    create_outgoing,
    delete_document_type,
    get_incoming_detail,
    get_outgoing_detail,
    list_document_types,
    list_incoming,
    list_outgoing,
    lookup_work_units,
    update_document_type,
    update_incoming,
    update_outgoing,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/generalaffair', tags=['generalaffair'])


# ── Document Types ────────────────────────────────────────────────────────────

@router.get('/document-types')
async def list_document_types_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_document_types(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.post('/document-types', status_code=201)
async def create_document_type_endpoint(body: CreateDocumentTypeBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await create_document_type(body.kode_jenis_dokumen, body.nama_jenis_dokumen)
        return ok(result)
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/document-types/{type_id}')
async def update_document_type_endpoint(type_id: int, body: CreateDocumentTypeBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await update_document_type(type_id, body.kode_jenis_dokumen, body.nama_jenis_dokumen)
        return ok(result)
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/document-types/{type_id}')
async def delete_document_type_endpoint(type_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_document_type(type_id)
        return ok({'type_id': type_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get('/document/work-units')
async def get_lookup_work_units():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_work_units()
    return ok({'data': [item.model_dump() for item in data]})


# ── Incoming Documents ────────────────────────────────────────────────────────

@router.get('/document/incoming')
async def list_incoming_endpoint(
    search: str | None = Query(default=None, max_length=100),
    id_jenis_dokumen: int | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
    branch: str | None = Query(default=None, max_length=10),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_incoming(
        search=search,
        id_jenis_dokumen=id_jenis_dokumen,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size,
        branch=branch,
    )
    return ok(result.model_dump())


@router.get('/document/incoming/{doc_id}')
async def get_incoming_endpoint(doc_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_incoming_detail(doc_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Dokumen masuk tidak ditemukan')
    return ok(detail.model_dump())


@router.post('/document/incoming', status_code=201)
async def create_incoming_endpoint(body: CreateIncomingBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await create_incoming(body, body.user_input, body.branch_code)
        return ok(result)
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/document/incoming/{doc_id}')
async def update_incoming_endpoint(doc_id: int, body: UpdateIncomingBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await update_incoming(doc_id, body, body.user_input)
        return ok(result)
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── Outgoing Documents ────────────────────────────────────────────────────────

@router.get('/document/outgoing')
async def list_outgoing_endpoint(
    search: str | None = Query(default=None, max_length=100),
    id_jenis_dokumen: int | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
    branch: str | None = Query(default=None, max_length=10),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_outgoing(
        search=search,
        id_jenis_dokumen=id_jenis_dokumen,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size,
        branch=branch,
    )
    return ok(result.model_dump())


@router.get('/document/outgoing/{doc_id}')
async def get_outgoing_endpoint(doc_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_outgoing_detail(doc_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Dokumen keluar tidak ditemukan')
    return ok(detail.model_dump())


@router.post('/document/outgoing', status_code=201)
async def create_outgoing_endpoint(body: CreateOutgoingBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await create_outgoing(body, body.user_input, body.branch_code)
        return ok(result)
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/document/outgoing/{doc_id}')
async def update_outgoing_endpoint(doc_id: int, body: UpdateOutgoingBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        result = await update_outgoing(doc_id, body, body.user_input)
        return ok(result)
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

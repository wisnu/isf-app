from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.fundraising.donors.schema import (
    CreateUpdateCorporateBody,
    CreateUpdateIndividualBody,
    ToggleStatusBody,
)
from app.modules.fundraising.donors.service import (
    create_corporate,
    create_individual,
    get_corporate,
    get_individual,
    list_corporate,
    list_individual,
    lookup_countries,
    lookup_field_of_work,
    lookup_marketers,
    lookup_provinces,
    lookup_work_areas,
    toggle_status,
    update_corporate,
    update_individual,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/fundraising/donors', tags=['fundraising-donors'])


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get('/lookup/provinces')
async def get_lookup_provinces():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_provinces()
    return ok({'data': [i.model_dump() for i in data]})


@router.get('/lookup/countries')
async def get_lookup_countries():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_countries()
    return ok({'data': [i.model_dump() for i in data]})


@router.get('/lookup/marketers')
async def get_lookup_marketers():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_marketers()
    return ok({'data': [i.model_dump() for i in data]})


@router.get('/lookup/field-of-work')
async def get_lookup_field_of_work():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_field_of_work()
    return ok({'data': [i.model_dump() for i in data]})


@router.get('/lookup/work-areas')
async def get_lookup_work_areas():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_work_areas()
    return ok({'data': [i.model_dump() for i in data]})


# ── Corporate ─────────────────────────────────────────────────────────────────

@router.get('/corporate')
async def list_corporate_donors(
    search: str | None = Query(default=None),
    search_by: str | None = Query(default=None),
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_corporate(search=search, search_by=search_by, status=status, page=page, page_size=page_size)
    return ok({'rows': [r.model_dump() for r in result.rows], 'pagination': result.pagination.model_dump()})


@router.get('/corporate/{donor_id}')
async def get_corporate_donor(donor_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    item = await get_corporate(donor_id)
    if not item:
        raise HTTPException(status_code=404, detail='Donatur Korporat tidak ditemukan')
    return ok({'data': item.model_dump()})


@router.post('/corporate', status_code=201)
async def create_corporate_donor(body: CreateUpdateCorporateBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    donor_id = await create_corporate(body)
    return ok({'donor_id': donor_id})


@router.put('/corporate/{donor_id}')
async def update_corporate_donor(donor_id: int, body: CreateUpdateCorporateBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    await update_corporate(donor_id, body)
    return ok({'donor_id': donor_id})


@router.patch('/corporate/{donor_id}/status')
async def toggle_corporate_status(donor_id: int, body: ToggleStatusBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    await toggle_status(donor_id, body.status)
    return ok({'donor_id': donor_id, 'status': body.status})


# ── Individual ────────────────────────────────────────────────────────────────

@router.get('/individual')
async def list_individual_donors(
    search: str | None = Query(default=None),
    search_by: str | None = Query(default=None),
    status: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_individual(search=search, search_by=search_by, status=status, page=page, page_size=page_size)
    return ok({'rows': [r.model_dump() for r in result.rows], 'pagination': result.pagination.model_dump()})


@router.get('/individual/{donor_id}')
async def get_individual_donor(donor_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    item = await get_individual(donor_id)
    if not item:
        raise HTTPException(status_code=404, detail='Donatur Individu tidak ditemukan')
    return ok({'data': item.model_dump()})


@router.post('/individual', status_code=201)
async def create_individual_donor(body: CreateUpdateIndividualBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    donor_id = await create_individual(body)
    return ok({'donor_id': donor_id})


@router.put('/individual/{donor_id}')
async def update_individual_donor(donor_id: int, body: CreateUpdateIndividualBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    await update_individual(donor_id, body)
    return ok({'donor_id': donor_id})


@router.patch('/individual/{donor_id}/status')
async def toggle_individual_status(donor_id: int, body: ToggleStatusBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    await toggle_status(donor_id, body.status)
    return ok({'donor_id': donor_id, 'status': body.status})

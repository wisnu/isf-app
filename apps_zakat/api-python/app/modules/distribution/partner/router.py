from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.partner.schema import CreateUpdatePartnerBody
from app.modules.distribution.partner.service import (
    create_partner,
    delete_partner,
    get_partner,
    list_partners,
    update_partner,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/partner', tags=['partner'])


@router.get('')
async def list_partners_endpoint(
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_partners(search=search, page=page, page_size=page_size)
    return ok(result.model_dump())


@router.get('/{partner_id}')
async def get_partner_endpoint(partner_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_partner(partner_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Mitra tidak ditemukan')
    return ok(detail.model_dump())


@router.post('', status_code=201)
async def create_partner_endpoint(body: CreateUpdatePartnerBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        partner_id = await create_partner(body)
        return ok({'partner_id': partner_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.put('/{partner_id}')
async def update_partner_endpoint(partner_id: int, body: CreateUpdatePartnerBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_partner(partner_id, body)
        return ok({'partner_id': partner_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


@router.delete('/{partner_id}')
async def delete_partner_endpoint(partner_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_partner(partner_id)
        return ok({'partner_id': partner_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

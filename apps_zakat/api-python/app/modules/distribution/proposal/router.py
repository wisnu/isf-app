from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.modules.distribution.proposal.schema import (
    CreateProposalBody,
    UpdateProposalBody,
)
from app.modules.distribution.proposal.service import (
    create_proposal,
    delete_proposal,
    get_proposal,
    get_total_by_mustahiq,
    list_proposals,
    lookup_mustahiq,
    lookup_product_groups,
    update_proposal,
)
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/distribution/proposal', tags=['proposal'])


# ── Lookups ───────────────────────────────────────────────────────────────────

@router.get('/lookup/product-groups')
async def get_lookup_product_groups():
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_product_groups()
    return ok({'data': [item.model_dump() for item in data]})


@router.get('/lookup/mustahiq')
async def get_lookup_mustahiq(search: str | None = Query(default=None, max_length=100)):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    data = await lookup_mustahiq(search=search)
    return ok({'data': [item.model_dump() for item in data]})


# ── Total by Mustahiq ─────────────────────────────────────────────────────────

@router.get('/total-by-mustahiq')
async def get_total_by_mustahiq_endpoint(mustahiq_id: int = Query(..., gt=0)):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        total = await get_total_by_mustahiq(mustahiq_id)
        return ok({'total': total})
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── List ──────────────────────────────────────────────────────────────────────

@router.get('')
async def list_proposals_endpoint(
    date_from: str | None = Query(default=None, max_length=10),
    date_to: str | None = Query(default=None, max_length=10),
    branch_code: str | None = Query(default=None, max_length=10),
    status: str | None = Query(default=None, max_length=1),
    mustahiq_id: int | None = Query(default=None, gt=0),
    product_group_id: int | None = Query(default=None, gt=0),
    search: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await list_proposals(
        date_from=date_from,
        date_to=date_to,
        branch_code=branch_code,
        status=status,
        mustahiq_id=mustahiq_id,
        product_group_id=product_group_id,
        search=search,
        page=page,
        page_size=page_size,
    )
    return ok(result.model_dump())


# ── Detail ────────────────────────────────────────────────────────────────────

@router.get('/{proposal_id}')
async def get_proposal_endpoint(proposal_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    detail = await get_proposal(proposal_id)
    if detail is None:
        raise HTTPException(status_code=404, detail='Proposal tidak ditemukan')
    return ok(detail.model_dump())


# ── Create ────────────────────────────────────────────────────────────────────

@router.post('', status_code=201)
async def create_proposal_endpoint(body: CreateProposalBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        proposal_id = await create_proposal(body)
        return ok({'proposal_id': proposal_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── Update ────────────────────────────────────────────────────────────────────

@router.put('/{proposal_id}')
async def update_proposal_endpoint(proposal_id: int, body: UpdateProposalBody):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await update_proposal(proposal_id, body)
        return ok({'proposal_id': proposal_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))


# ── Delete ────────────────────────────────────────────────────────────────────

@router.delete('/{proposal_id}')
async def delete_proposal_endpoint(proposal_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    try:
        await delete_proposal(proposal_id)
        return ok({'proposal_id': proposal_id})
    except ValueError as e:
        return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(e)))
    except Exception as e:
        return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', str(e)))

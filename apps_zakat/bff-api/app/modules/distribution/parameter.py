from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python

# ── Jenis Program (ProductGroup) ──────────────────────────────────────────────

_MENU_PROGRAM_TYPE = 'distribution.parameter.program-type'

router_program_type = APIRouter(
    prefix='/api/distribution/parameter/program-type',
    tags=['distribution-parameter'],
)


@router_program_type.get('/lookup')
async def get_program_type_lookup(
    request: Request,
    _: str = Depends(require_menu(_MENU_PROGRAM_TYPE)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python('/api/distribution/parameter/program-type/lookup')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program_type.get('')
async def list_program_types(
    request: Request,
    _: str = Depends(require_menu(_MENU_PROGRAM_TYPE)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/parameter/program-type', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program_type.get('/{program_type_id}')
async def get_program_type(
    request: Request,
    program_type_id: int,
    _: str = Depends(require_menu(_MENU_PROGRAM_TYPE)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/parameter/program-type/{program_type_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program_type.post('', status_code=201)
async def create_program_type(
    request: Request,
    _: str = Depends(require_menu(_MENU_PROGRAM_TYPE)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python('/api/distribution/parameter/program-type', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program_type.put('/{program_type_id}')
async def update_program_type(
    request: Request,
    program_type_id: int,
    _: str = Depends(require_menu(_MENU_PROGRAM_TYPE)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/parameter/program-type/{program_type_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program_type.delete('/{program_type_id}')
async def delete_program_type(
    request: Request,
    program_type_id: int,
    _: str = Depends(require_menu(_MENU_PROGRAM_TYPE)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/parameter/program-type/{program_type_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Program Penyaluran (Product) ──────────────────────────────────────────────

_MENU_PROGRAM = 'distribution.parameter.program'

router_program = APIRouter(
    prefix='/api/distribution/parameter/program',
    tags=['distribution-parameter'],
)


@router_program.get('')
async def list_programs(
    request: Request,
    _: str = Depends(require_menu(_MENU_PROGRAM)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/parameter/program', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program.get('/{program_id}')
async def get_program(
    request: Request,
    program_id: int,
    _: str = Depends(require_menu(_MENU_PROGRAM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/parameter/program/{program_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program.post('', status_code=201)
async def create_program(
    request: Request,
    _: str = Depends(require_menu(_MENU_PROGRAM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python('/api/distribution/parameter/program', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program.put('/{program_id}')
async def update_program(
    request: Request,
    program_id: int,
    _: str = Depends(require_menu(_MENU_PROGRAM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/parameter/program/{program_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_program.delete('/{program_id}')
async def delete_program(
    request: Request,
    program_id: int,
    _: str = Depends(require_menu(_MENU_PROGRAM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/parameter/program/{program_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Bidang Pekerjaan (WorkSector) ─────────────────────────────────────────────

_MENU_WORK_SECTOR = 'distribution.parameter.work-sector'

router_work_sector = APIRouter(
    prefix='/api/distribution/parameter/work-sector',
    tags=['distribution-parameter'],
)


@router_work_sector.get('')
async def list_work_sectors(
    request: Request,
    _: str = Depends(require_menu(_MENU_WORK_SECTOR)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/parameter/work-sector', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_work_sector.get('/{work_sector_id}')
async def get_work_sector(
    request: Request,
    work_sector_id: int,
    _: str = Depends(require_menu(_MENU_WORK_SECTOR)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/parameter/work-sector/{work_sector_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_work_sector.post('', status_code=201)
async def create_work_sector(
    request: Request,
    _: str = Depends(require_menu(_MENU_WORK_SECTOR)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python('/api/distribution/parameter/work-sector', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_work_sector.put('/{work_sector_id}')
async def update_work_sector(
    request: Request,
    work_sector_id: int,
    _: str = Depends(require_menu(_MENU_WORK_SECTOR)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/parameter/work-sector/{work_sector_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_work_sector.delete('/{work_sector_id}')
async def delete_work_sector(
    request: Request,
    work_sector_id: int,
    _: str = Depends(require_menu(_MENU_WORK_SECTOR)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/parameter/work-sector/{work_sector_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


# ── Rincian Biaya Realisasi (CostItem) ────────────────────────────────────────

_MENU_COST_ITEM = 'distribution.parameter.cost-item'

router_cost_item = APIRouter(
    prefix='/api/distribution/parameter/cost-item',
    tags=['distribution-parameter'],
)


@router_cost_item.get('')
async def list_cost_items(
    request: Request,
    _: str = Depends(require_menu(_MENU_COST_ITEM)),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=500),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    params: dict = {'page': page, 'page_size': page_size}
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/distribution/parameter/cost-item', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_cost_item.get('/{cost_item_id}')
async def get_cost_item(
    request: Request,
    cost_item_id: int,
    _: str = Depends(require_menu(_MENU_COST_ITEM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await get_api_python(f'/api/distribution/parameter/cost-item/{cost_item_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_cost_item.post('', status_code=201)
async def create_cost_item(
    request: Request,
    _: str = Depends(require_menu(_MENU_COST_ITEM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python('/api/distribution/parameter/cost-item', json_body=body)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_cost_item.put('/{cost_item_id}')
async def update_cost_item(
    request: Request,
    cost_item_id: int,
    _: str = Depends(require_menu(_MENU_COST_ITEM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    body = await request.json()
    downstream = await post_api_python(
        f'/api/distribution/parameter/cost-item/{cost_item_id}',
        json_body=body,
        method='PUT',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router_cost_item.delete('/{cost_item_id}')
async def delete_cost_item(
    request: Request,
    cost_item_id: int,
    _: str = Depends(require_menu(_MENU_COST_ITEM)),
):
    _, err_resp = await current_user_id_or_401(request)
    if err_resp:
        return err_resp
    downstream = await post_api_python(
        f'/api/distribution/parameter/cost-item/{cost_item_id}',
        json_body={},
        method='DELETE',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

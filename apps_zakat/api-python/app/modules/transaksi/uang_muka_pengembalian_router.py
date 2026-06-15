"""FastAPI router for Uang Muka Pengembalian (Cash Advance Return, CAR)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from app.core.auth import require_menu
from app.core.db import get_db
from app.shared.response import ok
from . import uang_muka_pengembalian_service
from .uang_muka_pengembalian_schema import UangMukaPengembalianCreate

router = APIRouter(prefix="/transaksi/uang-muka-pengembalian", tags=["transaksi-uang-muka-pengembalian"])

_MENU = "keuangan.transaksi.uang-muka-pengembalian"


@router.get("")
async def list_pengembalian(
    page: int = 1,
    limit: int = 25,
    date_from: str = "",
    date_to: str = "",
    employee_id: int = 0,
    branch_code: str = "",
    db=Depends(get_db),
    _=Depends(require_menu(_MENU)),
):
    rows, total = await uang_muka_pengembalian_service.list_pengembalian(
        db,
        branch_code=branch_code,
        page=page,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
        employee_id=employee_id,
    )
    return ok({
        "rows": rows,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": -(-total // limit) if total else 0,
        },
    })


@router.post("")
async def create_pengembalian(
    payload: UangMukaPengembalianCreate,
    request: Request,
    _=Depends(require_menu(_MENU)),
):
    from app.modules.otorisasi import service as otorisasi_svc

    session = request.state.session
    user_id = session["user_id"]
    branch_code = session.get("primary_branch", "")

    result = await otorisasi_svc.save_and_submit(
        entity_type='uang_muka_pengembalian',
        module='keuangan.transaksi.uang-muka-pengembalian',
        payload=payload.model_dump(),
        user_id=user_id,
        branch_code=branch_code,
    )
    return ok(result)


@router.get("/lookup/open-uang-muka")
async def lookup_open_uang_muka(
    employee_id: int,
    branch_code: str = "",
    _=Depends(require_menu(_MENU)),
):
    """List open (belum di-LPJ) CA transactions for a given employee."""
    rows = await uang_muka_pengembalian_service.lookup_open_uang_muka(
        employee_id=employee_id,
        branch_code=branch_code,
    )
    return ok({"rows": rows})

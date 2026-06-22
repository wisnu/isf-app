from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.modules.appadmin.branch import router as branch_router
from app.modules.appadmin.role import router as role_router
from app.modules.appadmin.user import router as user_router
from app.modules.appadmin.schema import RoleMenuUpdateRequest
from app.modules.appadmin.service import (
    ValidationError,
    list_role_menu,
    replace_role_menu,
)
from app.shared.response import err, ok

router = APIRouter(prefix="/appadmin", tags=["appadmin"])
router.include_router(branch_router.router)
router.include_router(user_router.router)
router.include_router(role_router.router)


@router.get("/role-menu")
async def get_role_menu():
    snapshot = await list_role_menu()
    return ok(snapshot.model_dump())


@router.put("/role-menu")
async def put_role_menu(payload: RoleMenuUpdateRequest):
    try:
        result = await replace_role_menu(payload.mapping, payload.updated_by)
    except ValidationError as exc:
        return JSONResponse(
            status_code=400,
            content=err(exc.code, exc.message, details=exc.details),
        )
    return ok(result.model_dump())

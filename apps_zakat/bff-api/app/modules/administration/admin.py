from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix="/api/administration", tags=["admin"])


class MappingPairIn(BaseModel):
    role_id: str
    menu_key: str


class RoleMenuUpdateIn(BaseModel):
    mapping: list[MappingPairIn]


@router.get("/role-menu")
async def get_role_menu(
    request: Request,
    user_id: str = Depends(require_menu("admin.role_menu")),
):
    downstream = await get_api_python("/api/administration/role-menu")
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put("/role-menu")
async def put_role_menu(
    payload: RoleMenuUpdateIn,
    request: Request,
    user_id: str = Depends(require_menu("admin.role_menu")),
):
    body = {
        "mapping": [p.model_dump() for p in payload.mapping],
        "updated_by": user_id,
    }
    downstream = await post_api_python(
        "/api/admin/role-menu", json_body=body, method="PUT"
    )

    audit = getattr(request.app.state, "audit", None)
    if audit is not None and downstream.status_code == 200:
        try:
            result = downstream.json()
            diff = result.get("data", {}).get("diff", {})
            await audit.log(
                "role_menu_updated",
                user_id=user_id,
                payload={
                    "total_rows": result.get("data", {}).get("total_rows"),
                    "added_count": len(diff.get("added", [])),
                    "removed_count": len(diff.get("removed", [])),
                },
            )
        except Exception:
            pass

    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import TENANTS, get_user, tenant_public
from app.shared.response import err, ok

router = APIRouter(prefix="/tenants", tags=["tenants"])


class SwitchPayload(BaseModel):
    tenant_id: str


def _current_user_or_401(request: Request):
    username = request.session.get("user_id")
    if not username:
        return None, JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Not authenticated"))
    user = get_user(username)
    if user is None:
        request.session.clear()
        return None, JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))
    return user, None


@router.get("")
def list_tenants(request: Request):
    user, error = _current_user_or_401(request)
    if error is not None:
        return error
    tenants = [tenant_public(TENANTS[t]) for t in user.tenants]
    return ok({
        "tenants": tenants,
        "active_tenant_id": request.session.get("active_tenant_id", user.default_tenant),
    })


@router.post("/switch")
def switch_tenant(payload: SwitchPayload, request: Request):
    user, error = _current_user_or_401(request)
    if error is not None:
        return error
    if payload.tenant_id not in user.tenants:
        return JSONResponse(
            status_code=403,
            content=err("TENANT_FORBIDDEN", f"User cannot access tenant '{payload.tenant_id}'"),
        )
    request.session["active_tenant_id"] = payload.tenant_id
    return ok({"active_tenant_id": payload.tenant_id})

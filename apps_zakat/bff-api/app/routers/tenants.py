from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import current_user_id_or_401
from app.shared.response import err, ok

router = APIRouter(prefix="/tenants", tags=["tenants"])


class SwitchPayload(BaseModel):
    tenant_id: str


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("")
async def list_tenants(request: Request):
    user_id, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response
    db = request.app.state.auth_db
    tenants = await db.get_user_tenants(user_id)
    return ok(
        {
            "tenants": [{"id": t["id"], "name": t["name"]} for t in tenants],
            "active_tenant_id": request.session.get("active_tenant_id"),
        }
    )


@router.post("/switch")
async def switch_tenant(payload: SwitchPayload, request: Request):
    user_id, error_response = await current_user_id_or_401(request)
    if error_response is not None:
        return error_response

    db = request.app.state.auth_db
    audit = request.app.state.audit
    tenants = await db.get_user_tenants(user_id)
    allowed = {t["id"] for t in tenants}

    if payload.tenant_id not in allowed:
        return JSONResponse(
            status_code=403,
            content=err(
                "TENANT_FORBIDDEN",
                f"User cannot access tenant '{payload.tenant_id}'",
            ),
        )

    previous = request.session.get("active_tenant_id")
    request.session["active_tenant_id"] = payload.tenant_id

    await audit.log(
        "tenant_switch",
        user_id=user_id,
        tenant_id=payload.tenant_id,
        ip=_client_ip(request),
        payload={"from": previous, "to": payload.tenant_id},
    )
    return ok({"active_tenant_id": payload.tenant_id})

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.auth import get_user
from app.services.proxy import get_api_python
from app.shared.response import err

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def summary(request: Request):
    username = request.session.get("user_id")
    if not username:
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Not authenticated"))
    user = get_user(username)
    if user is None:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))

    active_tenant = request.session.get("active_tenant_id", user.default_tenant)
    downstream = await get_api_python("/api/v1/dashboard/summary", params={"tenant_id": active_tenant})
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())

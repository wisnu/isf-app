from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.modules.administration.identity.service import get_profile
from app.shared.response import err, ok

router = APIRouter(prefix="/identity", tags=["identity"])


@router.get("/{user_id}/profile")
async def profile(user_id: str):
    data = await get_profile(user_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=err("USER_NOT_FOUND", f"User '{user_id}' tidak ditemukan"),
        )
    return ok(data.model_dump())

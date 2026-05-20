from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import authenticate, get_user, user_public
from app.shared.response import err, ok

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginPayload(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(payload: LoginPayload, request: Request):
    user = authenticate(payload.username, payload.password)
    if user is None:
        return JSONResponse(
            status_code=401,
            content=err("INVALID_CREDENTIALS", "Username or password is incorrect"),
        )
    request.session["user_id"] = user.username
    request.session["active_tenant_id"] = user.default_tenant
    return ok({"user": user_public(user), "active_tenant_id": user.default_tenant})


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return ok({"logged_out": True})


@router.get("/me")
def me(request: Request):
    username = request.session.get("user_id")
    if not username:
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Not authenticated"))
    user = get_user(username)
    if user is None:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))
    return ok({
        "user": user_public(user),
        "active_tenant_id": request.session.get("active_tenant_id", user.default_tenant),
    })

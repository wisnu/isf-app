from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.tenants import router as tenants_router
from app.shared.config import settings
from app.shared.request_id import RequestIDMiddleware
from app.shared.response import ok

app = FastAPI(title="isf-app bff-api", version="0.1.0")

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    session_cookie="isf_session",
    same_site="lax",
    https_only=False,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return ok({"status": "ok"})


app.include_router(auth_router, prefix="/api")
app.include_router(tenants_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")

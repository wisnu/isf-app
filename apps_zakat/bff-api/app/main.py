from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers.auth import router as auth_router
from app.routers.auth_google import router as google_router
from app.routers.dashboard import router as dashboard_router
from app.routers.tenants import router as tenants_router
from app.services.audit import AuditWriter
from app.services.auth_db import AuthDB
from app.services.auth_providers.google import GoogleOAuthProvider
from app.services.auth_providers.password import PasswordProvider
from app.services.auth_seed import seed_defaults
from app.shared.config import Settings, settings as default_settings
from app.shared.request_id import RequestIDMiddleware
from app.shared.response import ok


def create_app(settings: Settings | None = None) -> FastAPI:
    cfg = settings or default_settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db = AuthDB(cfg.auth_db_path)
        await db.init_schema()
        if not await db.has_users():
            await seed_defaults(db)
        app.state.auth_db = db
        app.state.audit = AuditWriter(db)
        app.state.settings = cfg
        app.state.password_provider = PasswordProvider(db)
        app.state.google_provider = GoogleOAuthProvider(db, cfg)
        yield

    app = FastAPI(title="isf-app bff-api", version="0.2.0", lifespan=lifespan)

    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(
        SessionMiddleware,
        secret_key=cfg.session_secret,
        session_cookie="isf_session",
        same_site="lax",
        https_only=False,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[cfg.cors_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict:
        return ok({"status": "ok"})

    app.include_router(auth_router, prefix="/api")
    app.include_router(google_router, prefix="/api")
    app.include_router(tenants_router, prefix="/api")
    app.include_router(dashboard_router, prefix="/api")
    return app


app = create_app()

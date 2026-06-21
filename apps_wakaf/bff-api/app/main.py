from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.modules.core.auth import router as auth_router
from app.modules.core.auth_google import router as google_router
from app.modules.core.tenants import router as tenants_router
from app.modules.finance.master import coa_router, parameter_router
from app.modules.finance.dashboard import router as dashboard_router
from app.modules.finance.reports import router as report_router
from app.modules.administration.admin import router as admin_router

from app.services.auth import register_exception_handlers
from app.services.auth_db import AuthDB
from app.services.auth_providers.google import GoogleOAuthProvider
from app.services.auth_providers.password import PasswordProvider
from app.services.auth_seed import seed_defaults
from app.shared import db as auth_pool
from app.shared.config import Settings, settings as default_settings
from app.shared.request_id import RequestIDMiddleware
from app.shared.response import ok


def create_app(settings: Settings | None = None) -> FastAPI:
    cfg = settings or default_settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        pool = await auth_pool.init_pool(cfg.isf_auth_database_url or None)
        if pool is None:
            raise RuntimeError("ISF_AUTH_DATABASE_URL belum di-set")
        db = AuthDB()
        await db.migrate_usernames_to_uppercase()
        if not await db.has_users():
            await seed_defaults(db)
        app.state.auth_db = db
        app.state.settings = cfg
        app.state.password_provider = PasswordProvider(db)
        app.state.google_provider = GoogleOAuthProvider(db, cfg)
        from app.services.identity_client import IdentityClient
        app.state.identity_client = IdentityClient(
            cfg.api_python_base_url, timeout=cfg.identity_timeout
        )
        try:
            yield
        finally:
            await auth_pool.close_pool()

    app = FastAPI(title="isf-app bff-api (wakaf)", version="0.2.0", lifespan=lifespan)

    register_exception_handlers(app)

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
        allow_origins=cfg.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )

    @app.get("/health")
    def health() -> dict:
        return ok({"status": "ok"})

    app.include_router(auth_router,    prefix="/api")
    app.include_router(google_router,  prefix="/api")
    app.include_router(tenants_router, prefix="/api")
    app.include_router(coa_router)
    app.include_router(parameter_router)
    app.include_router(dashboard_router)
    app.include_router(report_router)
    app.include_router(admin_router)

    return app


app = create_app()

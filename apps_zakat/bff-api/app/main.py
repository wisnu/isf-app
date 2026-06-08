from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router
from app.routers.bank import router as bank_router
from app.routers.kas_kecil import router as kas_kecil_router
from app.routers.auth_google import router as google_router
from app.routers.coa import router as coa_router
from app.routers.dashboard import router as dashboard_router
from app.routers.report import router as report_router
from app.routers.tenants import router as tenants_router
from app.routers.histori_transaksi import router as histori_transaksi_router
from app.routers.penyaluran import router as penyaluran_router
from app.routers.penghimpunan import router as penghimpunan_router
from app.routers.otorisasi import router as otorisasi_router
from app.routers.transaction import router as transaction_router
from app.services.audit import AuditWriter
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
            raise RuntimeError(
                "ISF_AUTH_DATABASE_URL belum di-set — BFF butuh koneksi ke isf_auth_<portal> DB"
            )
        db = AuthDB()
        await db.migrate_usernames_to_uppercase()
        if not await db.has_users():
            await seed_defaults(db)
        app.state.auth_db = db
        app.state.audit = AuditWriter()
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

    app = FastAPI(title="isf-app bff-api", version="0.2.0", lifespan=lifespan)

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
        # Agar nama file export (.xlsx) terbaca oleh fetch lintas-origin di FE.
        expose_headers=["Content-Disposition"],
    )

    @app.get("/health")
    def health() -> dict:
        return ok({"status": "ok"})

    app.include_router(auth_router, prefix="/api")
    app.include_router(google_router, prefix="/api")
    app.include_router(tenants_router, prefix="/api")
    app.include_router(dashboard_router, prefix="/api")
    app.include_router(report_router, prefix="/api")
    app.include_router(bank_router, prefix="/api")
    app.include_router(kas_kecil_router, prefix="/api")
    app.include_router(coa_router, prefix="/api")
    app.include_router(admin_router, prefix="/api")
    app.include_router(transaction_router, prefix="/api")
    app.include_router(histori_transaksi_router, prefix="/api")
    app.include_router(penyaluran_router, prefix="/api")
    app.include_router(penghimpunan_router, prefix="/api")
    app.include_router(otorisasi_router, prefix="/api")
    return app


app = create_app()

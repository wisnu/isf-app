from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

# ── Core (auth, session) ──────────────────────────────────────────────────────
from app.modules.core.auth import router as auth_router
from app.modules.core.auth_google import router as google_router
from app.modules.core.tenants import router as tenants_router

# ── Finance — Master Data ─────────────────────────────────────────────────────
from app.modules.finance.master import (
    coa_router, bank_router, petty_cash_router, parameter_router,
)

# ── Finance — Budget ──────────────────────────────────────────────────────────
from app.modules.finance.budget import router as budget_router

# ── Finance — Transaction ─────────────────────────────────────────────────────
from app.modules.finance.transaction import (
    fund_collection_router, fund_distribution_router,
    amil_income_router, amil_expense_router,
    cash_advance_router, cash_advance_settlement_router,
    inter_account_transfer_router, general_transaction_router,
    receivable_router,
)

# ── Finance — Upload ──────────────────────────────────────────────────────────
from app.modules.finance.upload import upload_collection_router, hc_zis_router

# ── Finance — Inquiry ─────────────────────────────────────────────────────────
from app.modules.finance.inquiry import router as transaction_history_router, ca_router as ca_inquiry_router, ar_router as ar_inquiry_router

# ── Finance — Monitoring ──────────────────────────────────────────────────────
from app.modules.finance.monitoring import router as authorization_router

# ── Finance — Reports + Dashboard ────────────────────────────────────────────
from app.modules.finance.reports import router as report_router
from app.modules.finance.dashboard import router as dashboard_router

# ── Distribution ─────────────────────────────────────────────────────────────
from app.modules.distribution.mustahiq import (
    corporate_router as mustahiq_corporate_router,
    personal_router as mustahiq_personal_router,
    mustahiq_lookup_router,
)
from app.modules.distribution.proposal import router as proposal_router
from app.modules.distribution.partner import router as partner_router
from app.modules.distribution.regular_program import router as regular_program_router
from app.modules.distribution.non_regular_program import router as non_regular_program_router
from app.modules.distribution.realization_memo import (
    regular_router as realization_memo_regular_router,
    non_regular_router as realization_memo_non_regular_router,
)

# ── Administration ────────────────────────────────────────────────────────────
from app.modules.administration.admin import router as admin_router

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
        expose_headers=["Content-Disposition"],
    )

    @app.get("/health")
    def health() -> dict:
        return ok({"status": "ok"})

    # Core — needs /api prefix (router prefix is /auth, /tenants)
    app.include_router(auth_router,    prefix="/api")
    app.include_router(google_router,  prefix="/api")
    app.include_router(tenants_router, prefix="/api")

    # Finance — routers already carry full /api/finance/... prefix
    app.include_router(coa_router)
    app.include_router(bank_router)
    app.include_router(petty_cash_router)
    app.include_router(parameter_router)
    app.include_router(budget_router)
    app.include_router(fund_collection_router)
    app.include_router(fund_distribution_router)
    app.include_router(amil_income_router)
    app.include_router(amil_expense_router)
    app.include_router(cash_advance_router)
    app.include_router(cash_advance_settlement_router)
    app.include_router(inter_account_transfer_router)
    app.include_router(general_transaction_router)
    app.include_router(receivable_router)
    app.include_router(upload_collection_router)
    app.include_router(hc_zis_router)
    app.include_router(transaction_history_router)
    app.include_router(ca_inquiry_router)
    app.include_router(ar_inquiry_router)
    app.include_router(authorization_router)
    app.include_router(report_router)
    app.include_router(dashboard_router)

    # Distribution — routers carry full /api/distribution/... prefix
    app.include_router(mustahiq_corporate_router)
    app.include_router(mustahiq_personal_router)
    app.include_router(mustahiq_lookup_router)
    app.include_router(proposal_router)
    app.include_router(partner_router)
    app.include_router(regular_program_router)
    app.include_router(non_regular_program_router)
    app.include_router(realization_memo_regular_router)
    app.include_router(realization_memo_non_regular_router)

    # Administration — router carries full /api/administration/... prefix
    app.include_router(admin_router)

    return app


app = create_app()

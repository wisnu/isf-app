from contextlib import asynccontextmanager

from fastapi import FastAPI

# ── Finance — Master Data ─────────────────────────────────────────────────────
from app.modules.finance.master.coa.router import router as coa_router
from app.modules.finance.master.bank.router import router as bank_router
from app.modules.finance.master.petty_cash.router import router as petty_cash_router
from app.modules.finance.master.parameter.router import router as parameter_router

# ── Finance — Budget ──────────────────────────────────────────────────────────
from app.modules.finance.budget.router import router as budget_router

# ── Finance — Transaction ─────────────────────────────────────────────────────
from app.modules.finance.transaction.fund_collection.router import router as fund_collection_router
from app.modules.finance.transaction.fund_distribution.router import router as fund_distribution_router
from app.modules.finance.transaction.amil_income.router import router as amil_income_router
from app.modules.finance.transaction.amil_expense.router import router as amil_expense_router
from app.modules.finance.transaction.cash_advance.router import router as cash_advance_router
from app.modules.finance.transaction.cash_advance_settlement.router import router as cash_advance_settlement_router
from app.modules.finance.transaction.inter_account_transfer.router import router as inter_account_transfer_router
from app.modules.finance.transaction.general.router import router as general_transaction_router
from app.modules.finance.transaction.receivable.router import router as receivable_router

# ── Finance — Upload ──────────────────────────────────────────────────────────
from app.modules.finance.upload.collection.router import router as upload_collection_router
from app.modules.finance.upload.hc_zis.router import router as hc_zis_router

# ── Finance — Inquiry ─────────────────────────────────────────────────────────
from app.modules.finance.inquiry.transaction_history.router import router as transaction_history_router

# ── Finance — Monitoring ──────────────────────────────────────────────────────
from app.modules.finance.monitoring.authorization.router import router as authorization_router
from app.modules.finance.monitoring.authorization.service import _register_defaults

# ── Administration ────────────────────────────────────────────────────────────
from app.modules.administration.router import router as admin_router
from app.modules.administration.identity.router import router as identity_router

# ── Shared ────────────────────────────────────────────────────────────────────
from app.shared.db import close_pool, init_isf_auth_pool, init_pool, ping
from app.shared.response import ok


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await init_pool()
    isf_auth_pool = await init_isf_auth_pool()
    app.state.db_pool = pool
    app.state.isf_auth_pool = isf_auth_pool
    _register_defaults()
    yield
    await close_pool()


app = FastAPI(title="isf-app api-python", version="0.2.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return ok({"status": "ok"})


@app.get("/ready")
async def ready() -> dict:
    db_ok = await ping() if app.state.db_pool else False
    return ok({"status": "ready", "db": db_ok})


# ── Finance — Master Data ─────────────────────────────────────────────────────
app.include_router(coa_router,        prefix="/api")
app.include_router(bank_router,       prefix="/api")
app.include_router(petty_cash_router, prefix="/api")
app.include_router(parameter_router,  prefix="/api")

# ── Finance — Budget ──────────────────────────────────────────────────────────
app.include_router(budget_router, prefix="/api")

# ── Finance — Transaction ─────────────────────────────────────────────────────
app.include_router(fund_collection_router,         prefix="/api")
app.include_router(fund_distribution_router,       prefix="/api")
app.include_router(amil_income_router,             prefix="/api")
app.include_router(amil_expense_router,            prefix="/api")
app.include_router(cash_advance_router,            prefix="/api")
app.include_router(cash_advance_settlement_router, prefix="/api")
app.include_router(inter_account_transfer_router,  prefix="/api")
app.include_router(general_transaction_router,     prefix="/api")
app.include_router(receivable_router,              prefix="/api")

# ── Finance — Upload ──────────────────────────────────────────────────────────
app.include_router(upload_collection_router, prefix="/api")
app.include_router(hc_zis_router,            prefix="/api")

# ── Finance — Inquiry ─────────────────────────────────────────────────────────
app.include_router(transaction_history_router, prefix="/api")

# ── Finance — Monitoring ──────────────────────────────────────────────────────
app.include_router(authorization_router, prefix="/api")

# ── Administration ────────────────────────────────────────────────────────────
app.include_router(admin_router,    prefix="/api")
app.include_router(identity_router, prefix="/api")

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.admin.router import router as admin_router
from app.modules.bank.router import router as bank_router
from app.modules.budget.router import router as budget_router
from app.modules.petty_cash.router import router as petty_cash_router
from app.modules.coa.router import router as coa_router
from app.modules.identity.router import router as identity_router
from app.modules.authorization.router import router as otorisasi_router
from app.modules.authorization.service import _register_defaults
from app.modules.transaction.router import router as transaction_router
from app.modules.transaction.hc_zis_router import router as transaksi_router
from app.modules.transaction.cash_advance_router import router as cash_advance_router
from app.modules.transaction.cash_advance_settlement_router import router as cash_advance_settlement_router
from app.modules.transaction.inter_account_transfer_router import router as inter_account_transfer_router
from app.modules.transaction.receivable_router import router as receivable_router
from app.modules.transaction.general_router import router as general_router
from app.modules.transaction.amil_income_router import router as amil_income_router
from app.modules.transaction.amil_expense_router import router as amil_expense_router
from app.modules.transaction_history.router import router as transaksi_histori_router
from app.modules.parameter.router import router as parameter_router
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


app.include_router(admin_router, prefix="/api")
app.include_router(bank_router, prefix="/api")
app.include_router(budget_router, prefix="/api")
app.include_router(petty_cash_router, prefix="/api")
app.include_router(coa_router, prefix="/api")
app.include_router(identity_router, prefix="/api")
app.include_router(otorisasi_router, prefix="/api")
app.include_router(transaction_router, prefix="/api")
app.include_router(transaksi_router, prefix="/api")
app.include_router(cash_advance_router, prefix="/api")
app.include_router(cash_advance_settlement_router, prefix="/api")
app.include_router(inter_account_transfer_router, prefix="/api")
app.include_router(receivable_router, prefix="/api")
app.include_router(general_router, prefix="/api")
app.include_router(amil_income_router, prefix="/api")
app.include_router(amil_expense_router, prefix="/api")
app.include_router(transaksi_histori_router, prefix="/api")
app.include_router(parameter_router, prefix="/api")

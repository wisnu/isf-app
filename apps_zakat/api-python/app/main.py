from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.admin.router import router as admin_router
from app.modules.bank.router import router as bank_router
from app.modules.budget.router import router as budget_router
from app.modules.kas_kecil.router import router as kas_kecil_router
from app.modules.coa.router import router as coa_router
from app.modules.identity.router import router as identity_router
from app.modules.otorisasi.router import router as otorisasi_router
from app.modules.otorisasi.service import _register_defaults
from app.modules.transaction.router import router as transaction_router
from app.modules.transaksi.router import router as transaksi_router
from app.modules.transaksi.uang_muka_router import router as uang_muka_router
from app.modules.transaksi.uang_muka_pengembalian_router import router as uang_muka_pengembalian_router
from app.modules.transaksi.transfer_antar_rekening_router import router as transfer_antar_rekening_router
from app.modules.transaksi.piutang_router import router as piutang_router
from app.modules.transaksi.transaksi_umum_router import router as transaksi_umum_router
from app.modules.transaksi_histori.router import router as transaksi_histori_router
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
app.include_router(kas_kecil_router, prefix="/api")
app.include_router(coa_router, prefix="/api")
app.include_router(identity_router, prefix="/api")
app.include_router(otorisasi_router, prefix="/api")
app.include_router(transaction_router, prefix="/api")
app.include_router(transaksi_router, prefix="/api")
app.include_router(uang_muka_router, prefix="/api")
app.include_router(uang_muka_pengembalian_router, prefix="/api")
app.include_router(transfer_antar_rekening_router, prefix="/api")
app.include_router(piutang_router, prefix="/api")
app.include_router(transaksi_umum_router, prefix="/api")
app.include_router(transaksi_histori_router, prefix="/api")
app.include_router(parameter_router, prefix="/api")

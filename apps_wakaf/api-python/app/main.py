from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.finance.master.coa.router import router as coa_router
from app.modules.finance.master.parameter.router import router as parameter_router
from app.modules.administration.router import router as admin_router
from app.modules.administration.identity.router import router as identity_router
from app.shared.db import close_pool, init_isf_auth_pool, init_pool, ping
from app.shared.response import ok


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await init_pool()
    isf_auth_pool = await init_isf_auth_pool()
    app.state.db_pool = pool
    app.state.isf_auth_pool = isf_auth_pool
    yield
    await close_pool()


app = FastAPI(title="isf-app api-python (wakaf)", version="0.2.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return ok({"status": "ok"})


@app.get("/ready")
async def ready() -> dict:
    db_ok = await ping() if app.state.db_pool else False
    return ok({"status": "ready", "db": db_ok})


# Finance routers carry full /api/finance/... prefix
app.include_router(coa_router)
app.include_router(parameter_router)

# Administration
app.include_router(admin_router)
app.include_router(identity_router, prefix="/api")

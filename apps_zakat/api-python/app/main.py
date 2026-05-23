from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.coa.router import router as coa_router
from app.modules.dashboard.router import router as dashboard_router
from app.shared.db import close_pool, init_pool, ping
from app.shared.response import ok


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await init_pool()
    app.state.db_pool = pool
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


app.include_router(dashboard_router, prefix="/api")
app.include_router(coa_router, prefix="/api")

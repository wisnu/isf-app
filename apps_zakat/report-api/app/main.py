from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.finance.dashboard.router import router as dashboard_router
from app.modules.finance.reports.router import router as report_router
from app.shared.db import (
    close_dwh_pool,
    close_pool,
    init_dwh_pool,
    init_pool,
    ping,
    ping_dwh,
)
from app.shared.response import ok


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await init_pool()
    app.state.dwh_pool = await init_dwh_pool()
    yield
    await close_pool()
    await close_dwh_pool()


app = FastAPI(title="isf-app report-api", version="0.2.0", lifespan=lifespan)


@app.get("/health")
def health() -> dict:
    return ok({"status": "ok"})


@app.get("/ready")
async def ready() -> dict:
    db_ok = await ping() if app.state.db_pool else False
    dwh_ok = await ping_dwh() if app.state.dwh_pool else False
    return ok({"status": "ready", "db": db_ok, "dwh": dwh_ok})


app.include_router(dashboard_router, prefix="/api")
app.include_router(report_router, prefix="/api")

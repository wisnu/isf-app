from fastapi import FastAPI

from app.modules.dashboard.router import router as dashboard_router
from app.shared.response import ok

app = FastAPI(title="isf-app api-python", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return ok({"status": "ok"})


@app.get("/ready")
def ready() -> dict:
    return ok({"status": "ready"})


app.include_router(dashboard_router, prefix="/api/v1")

from typing import Any
from uuid import uuid4


def make_meta(request_id: str | None = None) -> dict[str, Any]:
    return {"request_id": request_id or f"req_{uuid4().hex[:12]}"}


def ok(data: Any, *, request_id: str | None = None) -> dict[str, Any]:
    return {"data": data, "meta": make_meta(request_id)}


def err(code: str, message: str, *, details: Any = None, request_id: str | None = None) -> dict[str, Any]:
    return {
        "error": {"code": code, "message": message, "details": details},
        "meta": make_meta(request_id),
    }

from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient
from starlette.middleware.sessions import SessionMiddleware

from app.services.auth import register_exception_handlers, require_menu


def _make_minimal_app():
    """Standalone FastAPI app dengan session middleware, untuk test 401 path
    yang tidak butuh AuthDB."""
    app = FastAPI()
    register_exception_handlers(app)
    app.add_middleware(SessionMiddleware, secret_key="test-secret")

    @app.get("/gated")
    async def gated(user_id: str = Depends(require_menu("dashboard.overview"))):
        return {"user_id": user_id}

    return app


def test_require_menu_denies_when_not_authenticated():
    app = _make_minimal_app()
    client = TestClient(app)
    response = client.get("/gated")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"

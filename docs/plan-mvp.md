# MVP Implementation Plan — `isf-app` Fase 1

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the Fase 1 MVP defined in `docs/prd.md` §11 — dummy login, dashboard skeleton with 2 widgets, and tenant switcher — runnable end-to-end via `docker compose up`.

**Architecture:** Three services per `docs/architecture.md`: Vue + Vite SPA (`web-vue`) → FastAPI BFF (`bff-api`) → FastAPI backend (`api-python`). Dummy auth via in-memory user list + cookie session at the BFF. No database in this fase; dashboard data is hardcoded in `api-python`. All three services run in **development mode** (hot reload) inside docker-compose with bind-mounted source.

**Tech Stack:**
- Frontend: Vue 3 + Vite + TypeScript, Vue Router 4, Pinia, vanilla CSS.
- BFF: FastAPI, uvicorn, httpx, Starlette `SessionMiddleware`, Pydantic v2, pytest.
- Backend: FastAPI, uvicorn, Pydantic v2, pytest.
- Containers: docker-compose (dev mode, bind-mount source, hot reload).

---

## Locked decisions

- **UI styling:** vanilla CSS (no Tailwind, no UI component library). Easy to swap later.
- **No Postgres in MVP.** Added in Fase 2 along with first DB-backed endpoint.
- **Dummy users (in-memory, BFF):**
  - `admin` / `admin123` — member of both `perusahaan_a` & `perusahaan_b`, default `perusahaan_a`.
  - `finance.a` / `finance123` — `perusahaan_a` only.
  - `finance.b` / `finance123` — `perusahaan_b` only.
- **Session:** Starlette `SessionMiddleware`. Cookie name `isf_session`, `httpOnly`, `samesite=lax`. Payload: `{ user_id, active_tenant_id }`.
- **Tenants (hardcoded):**
  - `perusahaan_a` → "Lembaga ZISWAF A"
  - `perusahaan_b` → "Lembaga ZISWAF B"
- **Dashboard widgets (MVP):**
  1. Ringkasan Penerimaan periode berjalan (per tenant aktif).
  2. Ringkasan Penyaluran periode berjalan (per tenant aktif).
- **API response format** matches `docs/architecture.md` §12 — `{ data, meta }` for success, `{ error, meta }` for error. Helper modules in each service.
- **Ports:** web-vue `5173`, bff-api `7000`, api-python `8000`.
- **CORS:** BFF allows origin `http://localhost:5173` with credentials.
- **TDD scope:** pytest for BFF and api-python endpoints (test-first). Frontend has no unit tests at MVP; verified manually via browser smoke test in Task 14.

---

## File inventory

### `apps/web-vue/`

| File | Responsibility |
| --- | --- |
| `package.json` | Deps, scripts |
| `tsconfig.json`, `tsconfig.node.json` | TS config |
| `vite.config.ts` | Vite + alias `@` → `src` |
| `index.html` | Root HTML |
| `Dockerfile.dev` | Node 20 image, `npm run dev -- --host` |
| `src/main.ts` | App bootstrap + router + Pinia |
| `src/App.vue` | Root layout (header + `<router-view/>`) |
| `src/styles.css` | Global CSS variables |
| `src/router/index.ts` | Routes + auth guard |
| `src/stores/auth.ts` | Pinia store (user, active tenant, login/logout/switch) |
| `src/lib/api/client.ts` | `fetch` wrapper (credentials, JSON, error normalization) |
| `src/components/AppHeader.vue` | Header with tenant switcher + logout |
| `src/components/SummaryWidget.vue` | Widget card |
| `src/pages/LoginPage.vue` | Login form |
| `src/pages/DashboardPage.vue` | Dashboard with 2 widgets |

### `apps/bff-api/`

| File | Responsibility |
| --- | --- |
| `pyproject.toml` | Deps (FastAPI, uvicorn, httpx, itsdangerous, pydantic-settings, pytest) |
| `Dockerfile.dev` | Python 3.12 + uvicorn `--reload` |
| `app/main.py` | App wiring, CORS, SessionMiddleware, routers |
| `app/shared/config.py` | `Settings` (pydantic-settings) |
| `app/shared/response.py` | `ok()`, `err()` helpers — `{ data, meta }` / `{ error, meta }` |
| `app/shared/request_id.py` | Request-ID middleware |
| `app/services/auth.py` | Hardcoded users + tenants + auth helpers |
| `app/services/proxy.py` | Generic forward helper to api-python |
| `app/routers/auth.py` | `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me` |
| `app/routers/tenants.py` | `GET /api/tenants`, `POST /api/tenants/switch` |
| `app/routers/dashboard.py` | `GET /api/dashboard/summary` (proxy) |
| `tests/conftest.py` | TestClient fixture |
| `tests/test_auth.py` | Login/logout/me |
| `tests/test_tenants.py` | List/switch |
| `tests/test_dashboard.py` | Proxy roundtrip with mocked downstream |

### `apps/api-python/`

| File | Responsibility |
| --- | --- |
| `pyproject.toml` | Deps |
| `Dockerfile.dev` | Python 3.12 + uvicorn `--reload` |
| `app/main.py` | App wiring |
| `app/shared/config.py` | `Settings` |
| `app/shared/response.py` | `ok()` / `err()` helpers |
| `app/modules/dashboard/router.py` | `GET /api/v1/dashboard/summary` |
| `app/modules/dashboard/schema.py` | Pydantic models |
| `app/modules/dashboard/service.py` | Dummy data per tenant |
| `tests/test_dashboard.py` | Endpoint test |

### `infra/`

| File | Responsibility |
| --- | --- |
| `docker-compose.yml` | 3-service compose (dev mode) |
| `.env.example` | Sample env per service |

### Repo root

| File | Responsibility |
| --- | --- |
| `.gitignore` | node_modules, `__pycache__`, `.venv`, etc. |

Pre-existing scaffold (modules `donors/zakat/waqf` in `apps/api-python/app/modules/`, multiple stub files) **stays untouched** — those slots are for Fase 2/3. MVP only adds the `dashboard/` module.

---

## Tasks

### Task 1: Repo `.gitignore`

**Files:** Create `.gitignore`

- [ ] **Step 1:** Create `.gitignore` with:

```gitignore
# Node
node_modules/
dist/
.vite/
*.local

# Python
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
*.egg-info/

# Editor / OS
.DS_Store
.idea/
.vscode/

# Env
.env
.env.local

# Logs
*.log
```

- [ ] **Step 2:** Commit.

```bash
git add .gitignore
git commit -m "chore: add .gitignore"
```

---

### Task 2: `api-python` — dependencies & app skeleton

**Files:**
- Create: `apps/api-python/pyproject.toml`
- Modify: `apps/api-python/app/main.py` (was empty stub)
- Create: `apps/api-python/app/shared/response.py`
- Modify: `apps/api-python/app/shared/config.py` (was empty stub)

- [ ] **Step 1:** Create `apps/api-python/pyproject.toml`:

```toml
[project]
name = "api-python"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115",
  "uvicorn[standard]>=0.30",
  "pydantic>=2.7",
  "pydantic-settings>=2.4",
]

[project.optional-dependencies]
dev = ["pytest>=8", "httpx>=0.27"]

[tool.pytest.ini_options]
pythonpath = ["."]
```

- [ ] **Step 2:** Write `apps/api-python/app/shared/config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
```

- [ ] **Step 3:** Write `apps/api-python/app/shared/response.py`:

```python
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
```

- [ ] **Step 4:** Write `apps/api-python/app/main.py`:

```python
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
```

- [ ] **Step 5:** Commit.

```bash
git add apps/api-python
git commit -m "feat(api-python): bootstrap FastAPI app + response helpers"
```

---

### Task 3: `api-python` — dashboard module (TDD)

**Files:**
- Create: `apps/api-python/tests/test_dashboard.py`
- Create: `apps/api-python/app/modules/dashboard/__init__.py`
- Create: `apps/api-python/app/modules/dashboard/service.py`
- Create: `apps/api-python/app/modules/dashboard/schema.py`
- Create: `apps/api-python/app/modules/dashboard/router.py`

- [ ] **Step 1:** Write failing test `apps/api-python/tests/test_dashboard.py`:

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_summary_returns_data_for_tenant_a():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "perusahaan_a"})
    assert response.status_code == 200
    body = response.json()
    assert "data" in body and "meta" in body
    data = body["data"]
    assert data["tenant_id"] == "perusahaan_a"
    assert data["penerimaan"]["total"] > 0
    assert data["penyaluran"]["total"] > 0


def test_dashboard_summary_returns_data_for_tenant_b():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "perusahaan_b"})
    assert response.status_code == 200
    assert response.json()["data"]["tenant_id"] == "perusahaan_b"


def test_dashboard_summary_unknown_tenant_returns_404():
    response = client.get("/api/v1/dashboard/summary", params={"tenant_id": "nonexistent"})
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "TENANT_NOT_FOUND"
```

- [ ] **Step 2:** Run, expect FAIL (module not found).

```bash
cd apps/api-python && python -m pytest tests/test_dashboard.py -v
```

- [ ] **Step 3:** Create empty `apps/api-python/app/modules/dashboard/__init__.py`.

- [ ] **Step 4:** Write `apps/api-python/app/modules/dashboard/schema.py`:

```python
from pydantic import BaseModel


class AmountSummary(BaseModel):
    total: int
    period: str


class DashboardSummary(BaseModel):
    tenant_id: str
    tenant_name: str
    penerimaan: AmountSummary
    penyaluran: AmountSummary
```

- [ ] **Step 5:** Write `apps/api-python/app/modules/dashboard/service.py`:

```python
from app.modules.dashboard.schema import AmountSummary, DashboardSummary

_DUMMY: dict[str, DashboardSummary] = {
    "perusahaan_a": DashboardSummary(
        tenant_id="perusahaan_a",
        tenant_name="Lembaga ZISWAF A",
        penerimaan=AmountSummary(total=1_250_000_000, period="2026-05"),
        penyaluran=AmountSummary(total=875_000_000, period="2026-05"),
    ),
    "perusahaan_b": DashboardSummary(
        tenant_id="perusahaan_b",
        tenant_name="Lembaga ZISWAF B",
        penerimaan=AmountSummary(total=920_000_000, period="2026-05"),
        penyaluran=AmountSummary(total=640_000_000, period="2026-05"),
    ),
}


def get_summary(tenant_id: str) -> DashboardSummary | None:
    return _DUMMY.get(tenant_id)
```

- [ ] **Step 6:** Write `apps/api-python/app/modules/dashboard/router.py`:

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.modules.dashboard.service import get_summary
from app.shared.response import err, ok

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(tenant_id: str):
    data = get_summary(tenant_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=err("TENANT_NOT_FOUND", f"Tenant '{tenant_id}' not found"),
        )
    return ok(data.model_dump())
```

- [ ] **Step 7:** Run tests, expect PASS.

```bash
cd apps/api-python && python -m pytest tests/test_dashboard.py -v
```

- [ ] **Step 8:** Commit.

```bash
git add apps/api-python
git commit -m "feat(api-python): dashboard summary endpoint with dummy data"
```

---

### Task 4: `bff-api` — dependencies & app skeleton

**Files:**
- Create: `apps/bff-api/pyproject.toml`
- Modify: `apps/bff-api/app/main.py`
- Modify: `apps/bff-api/app/shared/config.py`
- Create: `apps/bff-api/app/shared/response.py`
- Modify: `apps/bff-api/app/shared/request_id.py`

- [ ] **Step 1:** Create `apps/bff-api/pyproject.toml`:

```toml
[project]
name = "bff-api"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115",
  "uvicorn[standard]>=0.30",
  "httpx>=0.27",
  "itsdangerous>=2.2",
  "pydantic>=2.7",
  "pydantic-settings>=2.4",
]

[project.optional-dependencies]
dev = ["pytest>=8"]

[tool.pytest.ini_options]
pythonpath = ["."]
```

- [ ] **Step 2:** Write `apps/bff-api/app/shared/config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_python_base_url: str = "http://localhost:8000"
    session_secret: str = "dev-secret-change-me"
    cors_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
```

- [ ] **Step 3:** Write `apps/bff-api/app/shared/response.py` (same shape as api-python's):

```python
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
```

- [ ] **Step 4:** Write `apps/bff-api/app/shared/request_id.py`:

```python
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or f"req_{uuid4().hex[:12]}"
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
```

- [ ] **Step 5:** Write `apps/bff-api/app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers.auth import router as auth_router
from app.routers.dashboard import router as dashboard_router
from app.routers.tenants import router as tenants_router
from app.shared.config import settings
from app.shared.request_id import RequestIDMiddleware
from app.shared.response import ok

app = FastAPI(title="isf-app bff-api", version="0.1.0")

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    session_cookie="isf_session",
    same_site="lax",
    https_only=False,  # dev only — flip to True in prod
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return ok({"status": "ok"})


app.include_router(auth_router, prefix="/api")
app.include_router(tenants_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")
```

- [ ] **Step 6:** Commit.

```bash
git add apps/bff-api
git commit -m "feat(bff-api): bootstrap FastAPI app + middleware"
```

---

### Task 5: `bff-api` — auth service + endpoints (TDD)

**Files:**
- Modify: `apps/bff-api/app/services/auth.py`
- Modify: `apps/bff-api/app/routers/auth.py`
- Create: `apps/bff-api/tests/conftest.py`
- Create: `apps/bff-api/tests/test_auth.py`

- [ ] **Step 1:** Write `apps/bff-api/tests/conftest.py`:

```python
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)
```

- [ ] **Step 2:** Write failing tests `apps/bff-api/tests/test_auth.py`:

```python
def test_me_unauthenticated_returns_401(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_login_with_valid_credentials_returns_user_and_active_tenant(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["user"]["username"] == "admin"
    assert body["data"]["active_tenant_id"] == "perusahaan_a"


def test_login_invalid_credentials_returns_401(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_me_after_login_returns_user(client):
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.get("/api/auth/me")
    assert response.status_code == 200
    assert response.json()["data"]["user"]["username"] == "admin"


def test_logout_clears_session(client):
    client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
    response = client.post("/api/auth/logout")
    assert response.status_code == 200
    assert client.get("/api/auth/me").status_code == 401
```

- [ ] **Step 3:** Run; expect FAIL.

```bash
cd apps/bff-api && python -m pytest tests/test_auth.py -v
```

- [ ] **Step 4:** Write `apps/bff-api/app/services/auth.py`:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    name: str
    password: str
    tenants: list[str]
    default_tenant: str


@dataclass(frozen=True)
class Tenant:
    id: str
    name: str


TENANTS: dict[str, Tenant] = {
    "perusahaan_a": Tenant(id="perusahaan_a", name="Lembaga ZISWAF A"),
    "perusahaan_b": Tenant(id="perusahaan_b", name="Lembaga ZISWAF B"),
}

USERS: dict[str, User] = {
    "admin": User(
        username="admin",
        name="Administrator",
        password="admin123",
        tenants=["perusahaan_a", "perusahaan_b"],
        default_tenant="perusahaan_a",
    ),
    "finance.a": User(
        username="finance.a",
        name="Finance Perusahaan A",
        password="finance123",
        tenants=["perusahaan_a"],
        default_tenant="perusahaan_a",
    ),
    "finance.b": User(
        username="finance.b",
        name="Finance Perusahaan B",
        password="finance123",
        tenants=["perusahaan_b"],
        default_tenant="perusahaan_b",
    ),
}


def authenticate(username: str, password: str) -> User | None:
    user = USERS.get(username)
    if user is None or user.password != password:
        return None
    return user


def get_user(username: str) -> User | None:
    return USERS.get(username)


def user_public(user: User) -> dict:
    return {
        "username": user.username,
        "name": user.name,
        "tenants": [tenant_public(TENANTS[t]) for t in user.tenants],
        "default_tenant": user.default_tenant,
    }


def tenant_public(t: Tenant) -> dict:
    return {"id": t.id, "name": t.name}
```

- [ ] **Step 5:** Write `apps/bff-api/app/routers/auth.py`:

```python
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import authenticate, get_user, user_public
from app.shared.response import err, ok

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginPayload(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(payload: LoginPayload, request: Request):
    user = authenticate(payload.username, payload.password)
    if user is None:
        return JSONResponse(
            status_code=401,
            content=err("INVALID_CREDENTIALS", "Username or password is incorrect"),
        )
    request.session["user_id"] = user.username
    request.session["active_tenant_id"] = user.default_tenant
    return ok({"user": user_public(user), "active_tenant_id": user.default_tenant})


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return ok({"logged_out": True})


@router.get("/me")
def me(request: Request):
    username = request.session.get("user_id")
    if not username:
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Not authenticated"))
    user = get_user(username)
    if user is None:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))
    return ok({
        "user": user_public(user),
        "active_tenant_id": request.session.get("active_tenant_id", user.default_tenant),
    })
```

- [ ] **Step 6:** Run tests, expect PASS.

```bash
cd apps/bff-api && python -m pytest tests/test_auth.py -v
```

- [ ] **Step 7:** Commit.

```bash
git add apps/bff-api
git commit -m "feat(bff-api): dummy auth + session"
```

---

### Task 6: `bff-api` — tenant endpoints (TDD)

**Files:**
- Modify: `apps/bff-api/app/routers/tenants.py`
- Create: `apps/bff-api/tests/test_tenants.py`

- [ ] **Step 1:** Write failing tests `apps/bff-api/tests/test_tenants.py`:

```python
def login(client, username="admin", password="admin123"):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def test_tenants_list_requires_auth(client):
    response = client.get("/api/tenants")
    assert response.status_code == 401


def test_tenants_list_returns_user_tenants(client):
    login(client)
    response = client.get("/api/tenants")
    assert response.status_code == 200
    tenants = response.json()["data"]["tenants"]
    assert {t["id"] for t in tenants} == {"perusahaan_a", "perusahaan_b"}
    assert response.json()["data"]["active_tenant_id"] == "perusahaan_a"


def test_tenants_list_finance_a_only_sees_a(client):
    login(client, "finance.a", "finance123")
    response = client.get("/api/tenants")
    tenants = response.json()["data"]["tenants"]
    assert [t["id"] for t in tenants] == ["perusahaan_a"]


def test_tenants_switch_to_allowed_tenant(client):
    login(client)
    response = client.post("/api/tenants/switch", json={"tenant_id": "perusahaan_b"})
    assert response.status_code == 200
    assert response.json()["data"]["active_tenant_id"] == "perusahaan_b"
    assert client.get("/api/auth/me").json()["data"]["active_tenant_id"] == "perusahaan_b"


def test_tenants_switch_to_disallowed_tenant_rejected(client):
    login(client, "finance.a", "finance123")
    response = client.post("/api/tenants/switch", json={"tenant_id": "perusahaan_b"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "TENANT_FORBIDDEN"
```

- [ ] **Step 2:** Write `apps/bff-api/app/routers/tenants.py`:

```python
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.auth import TENANTS, get_user, tenant_public
from app.shared.response import err, ok

router = APIRouter(prefix="/tenants", tags=["tenants"])


class SwitchPayload(BaseModel):
    tenant_id: str


def _current_user_or_401(request: Request):
    username = request.session.get("user_id")
    if not username:
        return None, JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Not authenticated"))
    user = get_user(username)
    if user is None:
        request.session.clear()
        return None, JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))
    return user, None


@router.get("")
def list_tenants(request: Request):
    user, error = _current_user_or_401(request)
    if error is not None:
        return error
    tenants = [tenant_public(TENANTS[t]) for t in user.tenants]
    return ok({
        "tenants": tenants,
        "active_tenant_id": request.session.get("active_tenant_id", user.default_tenant),
    })


@router.post("/switch")
def switch_tenant(payload: SwitchPayload, request: Request):
    user, error = _current_user_or_401(request)
    if error is not None:
        return error
    if payload.tenant_id not in user.tenants:
        return JSONResponse(
            status_code=403,
            content=err("TENANT_FORBIDDEN", f"User cannot access tenant '{payload.tenant_id}'"),
        )
    request.session["active_tenant_id"] = payload.tenant_id
    return ok({"active_tenant_id": payload.tenant_id})
```

- [ ] **Step 3:** Run, expect PASS.

```bash
cd apps/bff-api && python -m pytest tests/test_tenants.py -v
```

- [ ] **Step 4:** Commit.

```bash
git add apps/bff-api
git commit -m "feat(bff-api): tenant list + switch"
```

---

### Task 7: `bff-api` — dashboard proxy (TDD)

**Files:**
- Modify: `apps/bff-api/app/services/proxy.py`
- Modify: `apps/bff-api/app/routers/dashboard.py`
- Create: `apps/bff-api/tests/test_dashboard.py`

- [ ] **Step 1:** Write `apps/bff-api/app/services/proxy.py`:

```python
import httpx

from app.shared.config import settings


async def get_api_python(path: str, params: dict | None = None) -> httpx.Response:
    url = f"{settings.api_python_base_url}{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        return await client.get(url, params=params)
```

- [ ] **Step 2:** Write failing test `apps/bff-api/tests/test_dashboard.py`:

```python
from unittest.mock import AsyncMock, patch

import httpx
import pytest


def login(client, username="admin", password="admin123"):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def test_dashboard_summary_requires_auth(client):
    assert client.get("/api/dashboard/summary").status_code == 401


@pytest.fixture
def mock_downstream():
    payload = {
        "data": {
            "tenant_id": "perusahaan_a",
            "tenant_name": "Lembaga ZISWAF A",
            "penerimaan": {"total": 1_250_000_000, "period": "2026-05"},
            "penyaluran": {"total": 875_000_000, "period": "2026-05"},
        },
        "meta": {"request_id": "req_test"},
    }
    response = httpx.Response(200, json=payload)
    with patch("app.routers.dashboard.get_api_python", new=AsyncMock(return_value=response)) as m:
        yield m


def test_dashboard_summary_proxies_with_active_tenant(client, mock_downstream):
    login(client)
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["tenant_id"] == "perusahaan_a"
    mock_downstream.assert_called_once()
    args, kwargs = mock_downstream.call_args
    assert "/api/v1/dashboard/summary" in args[0]
    assert kwargs.get("params") == {"tenant_id": "perusahaan_a"}
```

- [ ] **Step 3:** Write `apps/bff-api/app/routers/dashboard.py`:

```python
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.auth import get_user
from app.services.proxy import get_api_python
from app.shared.response import err

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
async def summary(request: Request):
    username = request.session.get("user_id")
    if not username:
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Not authenticated"))
    user = get_user(username)
    if user is None:
        request.session.clear()
        return JSONResponse(status_code=401, content=err("UNAUTHORIZED", "Session invalid"))

    active_tenant = request.session.get("active_tenant_id", user.default_tenant)
    downstream = await get_api_python("/api/v1/dashboard/summary", params={"tenant_id": active_tenant})
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
```

- [ ] **Step 4:** Run, expect PASS.

```bash
cd apps/bff-api && python -m pytest tests/ -v
```

- [ ] **Step 5:** Commit.

```bash
git add apps/bff-api
git commit -m "feat(bff-api): dashboard proxy to api-python"
```

---

### Task 8: `web-vue` — package.json + Vite/TS config

**Files:**
- Modify: `apps/web-vue/package.json`
- Modify: `apps/web-vue/vite.config.ts`
- Create: `apps/web-vue/tsconfig.json`
- Create: `apps/web-vue/tsconfig.node.json`
- Modify: `apps/web-vue/index.html`

- [ ] **Step 1:** Write `apps/web-vue/package.json`:

```json
{
  "name": "web-vue",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "pinia": "^2.2.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.1.0",
    "typescript": "~5.6.0",
    "vite": "^5.4.0",
    "vue-tsc": "^2.1.0"
  }
}
```

- [ ] **Step 2:** Write `apps/web-vue/vite.config.ts`:

```ts
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) },
  },
  server: { host: true, port: 5173 },
})
```

- [ ] **Step 3:** Write `apps/web-vue/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "jsx": "preserve",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "noEmit": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 4:** Write `apps/web-vue/tsconfig.node.json`:

```json
{
  "compilerOptions": {
    "composite": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "allowSyntheticDefaultImports": true,
    "skipLibCheck": true,
    "noEmit": true
  },
  "include": ["vite.config.ts"]
}
```

- [ ] **Step 5:** Write `apps/web-vue/index.html`:

```html
<!DOCTYPE html>
<html lang="id">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>isf-app · Portal ZISWAF</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

- [ ] **Step 6:** Commit.

```bash
git add apps/web-vue
git commit -m "feat(web-vue): project config + tsconfig"
```

---

### Task 9: `web-vue` — bootstrap, router, styles

**Files:**
- Modify: `apps/web-vue/src/main.ts`
- Modify: `apps/web-vue/src/App.vue`
- Create: `apps/web-vue/src/styles.css`
- Modify: `apps/web-vue/src/router/index.ts`

- [ ] **Step 1:** Write `apps/web-vue/src/styles.css`:

```css
:root {
  --color-bg: #f7f7f8;
  --color-surface: #ffffff;
  --color-border: #e3e3e6;
  --color-text: #1a1a1c;
  --color-text-muted: #6b6b70;
  --color-primary: #0f766e;
  --color-primary-hover: #115e59;
  --color-danger: #b91c1c;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.06);
  --radius: 8px;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}

* { box-sizing: border-box; }
html, body, #app { margin: 0; padding: 0; height: 100%; }
body { background: var(--color-bg); color: var(--color-text); }

button {
  font: inherit;
  cursor: pointer;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
}
button.primary { background: var(--color-primary); color: white; border-color: var(--color-primary); }
button.primary:hover { background: var(--color-primary-hover); }

input, select {
  font: inherit;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  width: 100%;
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
}
```

- [ ] **Step 2:** Write `apps/web-vue/src/router/index.ts`:

```ts
import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'login', component: () => import('@/pages/LoginPage.vue'), meta: { public: true } },
    { path: '/', name: 'dashboard', component: () => import('@/pages/DashboardPage.vue') },
    { path: '/:catchAll(.*)', redirect: '/' },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.initialized) await auth.bootstrap()
  if (!to.meta.public && !auth.user) return { name: 'login', query: { redirect: to.fullPath } }
  if (to.name === 'login' && auth.user) return { name: 'dashboard' }
})

export default router
```

- [ ] **Step 3:** Write `apps/web-vue/src/main.ts`:

```ts
import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import router from '@/router'
import '@/styles.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

- [ ] **Step 4:** Write `apps/web-vue/src/App.vue`:

```vue
<script setup lang="ts">
import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth'
import { computed } from 'vue'

const auth = useAuthStore()
const showHeader = computed(() => Boolean(auth.user))
</script>

<template>
  <AppHeader v-if="showHeader" />
  <main class="main">
    <router-view />
  </main>
</template>

<style scoped>
.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}
</style>
```

- [ ] **Step 5:** Commit.

```bash
git add apps/web-vue
git commit -m "feat(web-vue): bootstrap, router, styles, App shell"
```

---

### Task 10: `web-vue` — API client + auth store

**Files:**
- Modify: `apps/web-vue/src/lib/api/client.ts`
- Create: `apps/web-vue/src/stores/auth.ts`

- [ ] **Step 1:** Write `apps/web-vue/src/lib/api/client.ts`:

```ts
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:7000'

export class ApiError extends Error {
  constructor(public code: string, message: string, public status: number) {
    super(message)
  }
}

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    method,
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    const code = payload?.error?.code ?? 'UNKNOWN_ERROR'
    const message = payload?.error?.message ?? response.statusText
    throw new ApiError(code, message, response.status)
  }
  return payload.data as T
}

export const api = {
  get: <T>(path: string) => request<T>('GET', path),
  post: <T>(path: string, body?: unknown) => request<T>('POST', path, body),
}
```

- [ ] **Step 2:** Write `apps/web-vue/src/stores/auth.ts`:

```ts
import { defineStore } from 'pinia'

import { api, ApiError } from '@/lib/api/client'

export interface Tenant { id: string; name: string }
export interface User {
  username: string
  name: string
  tenants: Tenant[]
  default_tenant: string
}

interface State {
  initialized: boolean
  user: User | null
  activeTenantId: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): State => ({ initialized: false, user: null, activeTenantId: null }),
  getters: {
    activeTenant(state): Tenant | null {
      if (!state.user || !state.activeTenantId) return null
      return state.user.tenants.find((t) => t.id === state.activeTenantId) ?? null
    },
  },
  actions: {
    async bootstrap() {
      try {
        const me = await api.get<{ user: User; active_tenant_id: string }>('/api/auth/me')
        this.user = me.user
        this.activeTenantId = me.active_tenant_id
      } catch (e) {
        if (e instanceof ApiError && e.status === 401) {
          this.user = null
          this.activeTenantId = null
        } else {
          throw e
        }
      } finally {
        this.initialized = true
      }
    },
    async login(username: string, password: string) {
      const result = await api.post<{ user: User; active_tenant_id: string }>(
        '/api/auth/login',
        { username, password },
      )
      this.user = result.user
      this.activeTenantId = result.active_tenant_id
    },
    async logout() {
      await api.post('/api/auth/logout')
      this.user = null
      this.activeTenantId = null
    },
    async switchTenant(tenantId: string) {
      const result = await api.post<{ active_tenant_id: string }>(
        '/api/tenants/switch',
        { tenant_id: tenantId },
      )
      this.activeTenantId = result.active_tenant_id
      const event = new CustomEvent('tenant-switched', { detail: tenantId })
      window.dispatchEvent(event)
      console.log('[audit] tenant switched', { tenant_id: tenantId, at: new Date().toISOString() })
    },
  },
})
```

- [ ] **Step 3:** Commit.

```bash
git add apps/web-vue
git commit -m "feat(web-vue): api client + auth store"
```

---

### Task 11: `web-vue` — Login page + AppHeader + SummaryWidget + Dashboard

**Files:**
- Modify: `apps/web-vue/src/pages/LoginPage.vue`
- Modify: `apps/web-vue/src/pages/DashboardPage.vue`
- Create: `apps/web-vue/src/components/AppHeader.vue`
- Create: `apps/web-vue/src/components/SummaryWidget.vue`

- [ ] **Step 1:** Write `apps/web-vue/src/pages/LoginPage.vue`:

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { ApiError } from '@/lib/api/client'

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const submitting = ref(false)
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

async function submit() {
  error.value = null
  submitting.value = true
  try {
    await auth.login(username.value, password.value)
    const target = (route.query.redirect as string) ?? '/'
    router.replace(target)
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Login gagal'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="login-shell">
    <form class="card login-card" @submit.prevent="submit">
      <h1>Portal ZISWAF</h1>
      <p class="muted">Masuk dengan akun demo</p>
      <label>
        <span>Username</span>
        <input v-model="username" autocomplete="username" required />
      </label>
      <label>
        <span>Password</span>
        <input v-model="password" type="password" autocomplete="current-password" required />
      </label>
      <p v-if="error" class="error">{{ error }}</p>
      <button class="primary" type="submit" :disabled="submitting">
        {{ submitting ? 'Memproses…' : 'Masuk' }}
      </button>
      <details class="hint">
        <summary>Akun demo</summary>
        <ul>
          <li><code>admin</code> / <code>admin123</code> — 2 perusahaan</li>
          <li><code>finance.a</code> / <code>finance123</code> — Perusahaan A</li>
          <li><code>finance.b</code> / <code>finance123</code> — Perusahaan B</li>
        </ul>
      </details>
    </form>
  </div>
</template>

<style scoped>
.login-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.5rem;
}
.login-card {
  width: 100%;
  max-width: 380px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.login-card h1 { margin: 0; font-size: 1.4rem; }
.muted { color: var(--color-text-muted); margin: -0.5rem 0 0; font-size: 0.9rem; }
label { display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.85rem; color: var(--color-text-muted); }
.error { color: var(--color-danger); margin: 0; font-size: 0.9rem; }
.hint { font-size: 0.8rem; color: var(--color-text-muted); }
.hint ul { margin: 0.5rem 0 0 1rem; padding: 0; }
.hint code { background: var(--color-bg); padding: 0.05rem 0.3rem; border-radius: 4px; }
</style>
```

- [ ] **Step 2:** Write `apps/web-vue/src/components/AppHeader.vue`:

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function onSwitch(event: Event) {
  const tenantId = (event.target as HTMLSelectElement).value
  if (tenantId && tenantId !== auth.activeTenantId) {
    await auth.switchTenant(tenantId)
  }
}

async function logout() {
  await auth.logout()
  router.replace({ name: 'login' })
}
</script>

<template>
  <header class="header">
    <div class="brand">
      <strong>isf-app</strong>
      <span class="muted">· Portal ZISWAF</span>
    </div>
    <div class="actions" v-if="auth.user">
      <label class="tenant-switcher">
        <span class="muted">Perusahaan</span>
        <select :value="auth.activeTenantId ?? ''" @change="onSwitch">
          <option v-for="t in auth.user.tenants" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
      </label>
      <span class="user muted">{{ auth.user.name }}</span>
      <button @click="logout">Logout</button>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.brand { display: flex; gap: 0.4rem; align-items: baseline; }
.muted { color: var(--color-text-muted); font-size: 0.85rem; }
.actions { display: flex; align-items: center; gap: 1rem; }
.tenant-switcher { display: flex; flex-direction: column; gap: 0.2rem; font-size: 0.75rem; }
.tenant-switcher select { width: auto; min-width: 200px; }
.user { white-space: nowrap; }
</style>
```

- [ ] **Step 3:** Write `apps/web-vue/src/components/SummaryWidget.vue`:

```vue
<script setup lang="ts">
defineProps<{
  label: string
  amount: number
  period: string
  accent?: 'in' | 'out'
}>()

function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(n)
}
</script>

<template>
  <article class="widget card" :class="accent">
    <header class="widget-head">
      <span class="muted">{{ label }}</span>
      <span class="period">{{ period }}</span>
    </header>
    <p class="amount">{{ formatIdr(amount) }}</p>
  </article>
</template>

<style scoped>
.widget { display: flex; flex-direction: column; gap: 0.5rem; min-height: 130px; }
.widget-head { display: flex; justify-content: space-between; align-items: baseline; }
.muted { color: var(--color-text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
.period { font-size: 0.75rem; color: var(--color-text-muted); }
.amount { font-size: 1.6rem; font-weight: 600; margin: 0; }
.widget.in .amount { color: var(--color-primary); }
.widget.out .amount { color: #ad6800; }
</style>
```

- [ ] **Step 4:** Write `apps/web-vue/src/pages/DashboardPage.vue`:

```vue
<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import SummaryWidget from '@/components/SummaryWidget.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface AmountSummary { total: number; period: string }
interface DashboardSummary {
  tenant_id: string
  tenant_name: string
  penerimaan: AmountSummary
  penyaluran: AmountSummary
}

const auth = useAuthStore()
const data = ref<DashboardSummary | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)

async function load() {
  loading.value = true
  error.value = null
  try {
    data.value = await api.get<DashboardSummary>('/api/dashboard/summary')
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Gagal memuat dashboard'
    data.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => auth.activeTenantId, () => { if (auth.activeTenantId) load() })
</script>

<template>
  <section class="dashboard">
    <header>
      <h1>Dashboard</h1>
      <p class="muted" v-if="data">{{ data.tenant_name }}</p>
    </header>

    <div v-if="loading" class="muted">Memuat…</div>
    <div v-else-if="error" class="card error">{{ error }}</div>
    <div v-else-if="data" class="widgets">
      <SummaryWidget
        label="Penerimaan"
        :amount="data.penerimaan.total"
        :period="data.penerimaan.period"
        accent="in"
      />
      <SummaryWidget
        label="Penyaluran"
        :amount="data.penyaluran.total"
        :period="data.penyaluran.period"
        accent="out"
      />
    </div>
  </section>
</template>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 1.5rem; }
.dashboard header h1 { margin: 0; }
.muted { color: var(--color-text-muted); margin: 0.3rem 0 0; }
.widgets {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}
.error { color: var(--color-danger); }
</style>
```

- [ ] **Step 5:** Commit.

```bash
git add apps/web-vue
git commit -m "feat(web-vue): login + dashboard + tenant switcher"
```

---

### Task 12: Dockerfiles (dev mode)

**Files:**
- Modify: `apps/web-vue/Dockerfile.dev` (new path)
- Modify: `apps/bff-api/Dockerfile.dev`
- Modify: `apps/api-python/Dockerfile.dev`

- [ ] **Step 1:** Write `apps/web-vue/Dockerfile.dev`:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

- [ ] **Step 2:** Write `apps/bff-api/Dockerfile.dev`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]"
COPY . .
EXPOSE 7000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000", "--reload"]
```

- [ ] **Step 3:** Write `apps/api-python/Dockerfile.dev`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[dev]"
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

- [ ] **Step 4:** Commit.

```bash
git add apps/web-vue/Dockerfile.dev apps/bff-api/Dockerfile.dev apps/api-python/Dockerfile.dev
git commit -m "feat(docker): dev Dockerfiles for all 3 services"
```

---

### Task 13: `infra/docker-compose.yml` + `.env.example`

**Files:**
- Modify: `infra/docker-compose.yml`
- Create: `infra/.env.example`

- [ ] **Step 1:** Write `infra/docker-compose.yml`:

```yaml
services:
  api-python:
    build:
      context: ../apps/api-python
      dockerfile: Dockerfile.dev
    container_name: isf-api-python
    environment:
      APP_ENV: development
    ports:
      - "8000:8000"
    volumes:
      - ../apps/api-python:/app
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 10s
      timeout: 3s
      retries: 5

  bff-api:
    build:
      context: ../apps/bff-api
      dockerfile: Dockerfile.dev
    container_name: isf-bff-api
    environment:
      APP_ENV: development
      API_PYTHON_BASE_URL: http://api-python:8000
      SESSION_SECRET: ${SESSION_SECRET:-dev-secret-change-me}
      CORS_ORIGIN: http://localhost:5173
    ports:
      - "7000:7000"
    volumes:
      - ../apps/bff-api:/app
    depends_on:
      api-python:
        condition: service_healthy

  web-vue:
    build:
      context: ../apps/web-vue
      dockerfile: Dockerfile.dev
    container_name: isf-web-vue
    environment:
      VITE_API_BASE_URL: http://localhost:7000
    ports:
      - "5173:5173"
    volumes:
      - ../apps/web-vue:/app
      - /app/node_modules
    depends_on:
      - bff-api
```

- [ ] **Step 2:** Write `infra/.env.example`:

```env
# Copy to .env in the same folder. docker-compose picks it up automatically.
SESSION_SECRET=dev-secret-change-me
```

- [ ] **Step 3:** Commit.

```bash
git add infra/docker-compose.yml infra/.env.example
git commit -m "feat(docker): compose for dev mode (web-vue + bff-api + api-python)"
```

---

### Task 14: Smoke test — bring up compose & verify end-to-end

- [ ] **Step 1:** Bring stack up.

```bash
cd infra && docker compose up --build -d && docker compose ps
```

Expected: all 3 services running, ports 5173/7000/8000 exposed.

- [ ] **Step 2:** Health checks (curl).

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:7000/health
```

Expected: both return `{"data":{"status":"ok"}, "meta":{...}}`.

- [ ] **Step 3:** Auth flow (curl, persistent cookie jar).

```bash
COOKIE=/tmp/isf-cookie.txt
curl -s -c "$COOKIE" -X POST http://localhost:7000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}'

curl -s -b "$COOKIE" http://localhost:7000/api/tenants
curl -s -b "$COOKIE" http://localhost:7000/api/dashboard/summary

curl -s -b "$COOKIE" -c "$COOKIE" -X POST http://localhost:7000/api/tenants/switch \
  -H 'Content-Type: application/json' \
  -d '{"tenant_id":"perusahaan_b"}'

curl -s -b "$COOKIE" http://localhost:7000/api/dashboard/summary
```

Expected: dashboard `tenant_id` changes from `perusahaan_a` → `perusahaan_b` after switch.

- [ ] **Step 4:** Browser verification.

Open `http://localhost:5173`:
1. Redirected to `/login`.
2. Submit `admin` / `admin123`.
3. Redirected to `/`, dashboard shows 2 widgets for "Lembaga ZISWAF A".
4. Open header dropdown → pick "Lembaga ZISWAF B" → widgets update.
5. Click "Logout" → redirected to `/login`.

- [ ] **Step 5:** Tear down (optional).

```bash
cd infra && docker compose down
```

- [ ] **Step 6:** Final commit (only if anything changed during smoke test).

If no changes: skip. If config tweaks were needed: commit them with a clear message.

---

## Self-review

- **Spec coverage vs PRD §11:** Login (Task 5 + 11) ✓ — Tenant default after login (Task 5) ✓ — Switcher in header (Task 11) ✓ — Switch without logout (Tasks 6 + 10 + 11) ✓ — Active tenant indicator (Task 11) ✓ — Dashboard min 2 widgets (Task 11) ✓ — Logout (Tasks 5 + 11) ✓ — Tenant switch logged (`console.log` in auth store, Task 10) ✓ — Standard `{ data, meta }` response (Tasks 2 + 4) ✓ — Modern browser, 1280×800+ (Tasks 9–11 use CSS Grid, responsive) ✓.
- **Placeholder scan:** none.
- **Type/name consistency:** `active_tenant_id` consistent across BFF, store, components. `tenants` array shape consistent. `perusahaan_a` / `perusahaan_b` consistent in BFF, api-python, tests.
- **Out-of-MVP slots untouched:** scaffolded `donors/zakat/waqf` modules, `infra/db/`, `infra/kong/`, `packages/api-contract/`, Go service — all untouched in this plan.

# Auth Layer + Google SSO

> Combined spec + plan. Scope: `apps/bff-api/` + `apps/web-vue/` + `infra/docker-compose.yml` + `docs/runbook-local.md`. No `api-python` changes.

## Context

Auth saat ini: hardcoded user dict di `bff-api/app/services/auth.py`, session via Starlette signed cookie. Cocok untuk MVP demo tapi:
- Tidak persistent (lost on container restart).
- Tidak ada audit trail.
- Tidak ada jalur ke SSO.
- Password plaintext di source code.

Target iterasi ini: **pluggable auth provider layer** + **persistent user store (SQLite)** + **Google OAuth2 end-to-end** (creds stub sampai diisi user). Backward compatible: 3 user demo (`admin`, `finance.a`, `finance.b`) tetap bisa login via password setelah refactor.

## Locked decisions

- **Cakupan**: provider layer + Google SSO end-to-end.
- **User store**: SQLite di `/data/auth.sqlite`, named volume `bff-data`.
- **Mode**: Hybrid — password & Google co-exist.
- **Google creds**: stub sampai user paste. Provider melaporkan `is_available=false` saat kosong; UI disable tombol Google.
- **Whitelist Google default**: `GOOGLE_ALLOWED_DOMAINS=ihsansolusi.co.id`.
- **JIT provisioning**: user Google baru lulus whitelist → di-create di DB **tanpa tenant** → di-redirect ke halaman `/no-tenant` ("tunggu admin assign"). Tidak ditolak.
- **Session storage**: tetap signed cookie (Starlette SessionMiddleware), bukan server-side. Catatan rotation di runbook.

## Arsitektur

```
bff-api/app/services/
  auth_db.py                    — SQLite access (aiosqlite)
  auth_seed.py                  — seed default tenants + 3 demo user on first boot
  audit.py                      — audit_log writer
  auth_providers/
    __init__.py
    base.py                     — AuthResult dataclass, shared types
    password.py                 — PasswordProvider (bcrypt verify)
    google.py                   — GoogleOAuthProvider (OAuth2 + PKCE + id_token verify)
  auth.py                       — (slim) shared helpers: build_user_public, get_current_user_or_401

bff-api/app/routers/
  auth.py                       — refactored: /login (password) /logout /me /providers
  auth_google.py                — new: /google/start, /google/callback
  tenants.py                    — refactored: query SQLite
```

**Lifespan** di `main.py`: open DB → run schema → seed jika kosong → register providers di `app.state`.

## SQLite schema

```sql
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS user_credentials (
  user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  password_hash TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS user_provider_links (
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider TEXT NOT NULL,
  external_id TEXT NOT NULL,
  email TEXT,
  linked_at TEXT NOT NULL DEFAULT (datetime('now')),
  PRIMARY KEY (user_id, provider),
  UNIQUE (provider, external_id)
);

CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tenant_memberships (
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  is_default INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, tenant_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL DEFAULT (datetime('now')),
  event TEXT NOT NULL,
  user_id TEXT,
  tenant_id TEXT,
  ip TEXT,
  ua TEXT,
  payload_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_user_ts ON audit_log(user_id, ts);
CREATE INDEX IF NOT EXISTS idx_audit_event_ts ON audit_log(event, ts);

PRAGMA journal_mode=WAL;
```

## Configuration (env)

Tambahan di `bff-api`:

```env
# Auth
AUTH_PROVIDERS=password,google
AUTH_DB_PATH=/data/auth.sqlite

# Google OAuth (kosong = provider disabled di UI)
GOOGLE_OAUTH_CLIENT_ID=
GOOGLE_OAUTH_CLIENT_SECRET=
GOOGLE_OAUTH_REDIRECT_URL=http://localhost:7000/api/auth/google/callback
GOOGLE_ALLOWED_DOMAINS=ihsansolusi.co.id
GOOGLE_ALLOWED_EMAILS=

# Frontend tujuan setelah login SSO
FRONTEND_BASE_URL=http://localhost:5173
```

## Flow

**Password (existing endpoint, refactored):**
```
POST /api/auth/login {username, password}
  → PasswordProvider.authenticate(username, password)
     → SELECT users WHERE username=? AND status='active'
     → SELECT password_hash FROM user_credentials WHERE user_id=?
     → bcrypt.checkpw
     → AuthResult(user_id, "password")
  → SELECT memberships; tolak 403 NO_TENANT kalau kosong
  → session set user_id + active_tenant_id (default)
  → audit_log login_success
```

**Google SSO (new):**
```
GET /api/auth/google/start?redirect=/
  → generate state + PKCE verifier+challenge, simpan session
  → 302 → https://accounts.google.com/o/oauth2/v2/auth?...

[user authenticates di Google]

GET /api/auth/google/callback?code=&state=
  → pop state & verifier dari session; reject jika tidak cocok
  → POST https://oauth2.googleapis.com/token (exchange code + verifier)
  → fetch JWKS (PyJWKClient, cached), verify id_token RS256
     issuer ∈ ("https://accounts.google.com", "accounts.google.com")
     audience == GOOGLE_OAUTH_CLIENT_ID
     exp not expired
  → ekstrak email + sub
  → email_allowed(email)? jika tidak:
     audit sso_login_blocked → 302 FRONTEND/login?sso_error=email_not_allowed
  → resolve_user(claims):
     existing link (provider=google, external_id=sub)? → user_id
     else: username==email exists? → link to existing → user_id
     else: JIT create user(username=email, display_name=claims.name) + link
            audit sso_jit_provisioned
  → load memberships
     ada: session set; redirect FRONTEND + ?redirect
     kosong: session set tanpa active_tenant_id; redirect FRONTEND/no-tenant
  → audit login_success(provider=google)
```

## Endpoints summary

| Method + Path | Status | Behaviour |
| --- | --- | --- |
| `GET /api/auth/providers` | **new** | `{ password: bool, google: bool }` |
| `POST /api/auth/login` | refactor | password via PasswordProvider |
| `POST /api/auth/logout` | refactor | clear session + audit |
| `GET /api/auth/me` | refactor | query DB, return user + active_tenant_id |
| `GET /api/auth/google/start` | **new** | initiate Google OAuth (302) |
| `GET /api/auth/google/callback` | **new** | handle Google return (302 ke frontend) |
| `GET /api/tenants` | refactor | dari SQLite |
| `POST /api/tenants/switch` | refactor | DB-validated + audit |
| `GET /api/dashboard/summary` | tidak berubah | (session masih sumber tenant) |

## Audit events

`login_success`, `login_failed`, `logout`, `tenant_switch`, `sso_login_blocked`, `sso_login_failed`, `sso_jit_provisioned`, `sso_link_created`, `login_blocked_no_tenant`.

Belum ada UI viewer (Fase 4). Inspect manual via `sqlite3 /data/auth.sqlite "SELECT * FROM audit_log ORDER BY ts DESC LIMIT 20"`.

## Dependencies baru di `bff-api/pyproject.toml`

```toml
"bcrypt>=4.2",
"pyjwt[crypto]>=2.9",
"aiosqlite>=0.20",
```

## Frontend changes (`apps/web-vue`)

- `src/stores/auth.ts` — tambah state `providers: { password: bool, google: bool }` + action `loadProviders()`.
- `src/pages/LoginPage.vue` — di bawah submit, divider "atau" + tombol `Continue with Google` (variant outline, icon globe dari lucide karena lucide tidak punya Google brand icon). Disabled + helper text kalau `providers.google === false`. Klik = `window.location.assign(\`${BASE}/api/auth/google/start?redirect=${...}\`)`.
- `src/pages/NoTenantPage.vue` — **new**: Card "Akun belum punya akses tenant. Hubungi administrator." + tombol Logout.
- `src/router/index.ts` — tambah route `/no-tenant`. Guard: kalau `auth.user && !auth.activeTenantId && to.name !== 'no-tenant'`, redirect ke `no-tenant`.
- Pesan error SSO di URL query `?sso_error=...` di-render di LoginPage sebagai Alert destructive.

## Container changes

`infra/docker-compose.yml`:

```yaml
services:
  bff-api:
    # ... existing
    environment:
      # ... existing
      AUTH_PROVIDERS: password,google
      AUTH_DB_PATH: /data/auth.sqlite
      GOOGLE_OAUTH_CLIENT_ID: ${GOOGLE_OAUTH_CLIENT_ID:-}
      GOOGLE_OAUTH_CLIENT_SECRET: ${GOOGLE_OAUTH_CLIENT_SECRET:-}
      GOOGLE_OAUTH_REDIRECT_URL: ${GOOGLE_OAUTH_REDIRECT_URL:-http://localhost:7000/api/auth/google/callback}
      GOOGLE_ALLOWED_DOMAINS: ${GOOGLE_ALLOWED_DOMAINS:-ihsansolusi.co.id}
      GOOGLE_ALLOWED_EMAILS: ${GOOGLE_ALLOWED_EMAILS:-}
      FRONTEND_BASE_URL: ${FRONTEND_BASE_URL:-http://localhost:5173}
    volumes:
      - ../apps/bff-api:/app
      - bff-data:/data

volumes:
  bff-data:
```

`infra/.env.example` ditambah variabel di atas.

## Runbook addendum (`docs/runbook-local.md`)

Tambah dua section di akhir:

### "Mengaktifkan Google SSO"
Langkah di Google Cloud Console: create OAuth 2.0 Client ID (Web application), authorized redirect URIs = `http://localhost:7000/api/auth/google/callback`, scope default OIDC. Tempel client_id + secret ke `infra/.env`, restart bff-api.

### "Rotate SESSION_SECRET (force logout semua)"
Edit `infra/.env`, set `SESSION_SECRET` ke nilai baru (random 32+ char), `podman-compose restart bff-api`. Semua session cookie lama jadi invalid.

## File inventory

### Modify

| File | Catatan |
| --- | --- |
| `apps/bff-api/pyproject.toml` | + bcrypt, pyjwt[crypto], aiosqlite |
| `apps/bff-api/app/shared/config.py` | + env vars di atas |
| `apps/bff-api/app/main.py` | refactor pakai `create_app()` + lifespan; init DB + seed; register state |
| `apps/bff-api/app/services/auth.py` | jadi tipis: helper `build_user_public(db, user_id)`, hapus hardcoded TENANTS/USERS dict |
| `apps/bff-api/app/routers/auth.py` | refactor pakai provider; tambah `/providers` |
| `apps/bff-api/app/routers/tenants.py` | refactor pakai `auth_db.get_user_tenants` |
| `apps/bff-api/tests/conftest.py` | temp SQLite per test, factory `create_app(settings)` |
| `apps/bff-api/tests/test_auth.py` | adapt (assertion sama, mekanisme baru) |
| `apps/bff-api/tests/test_tenants.py` | adapt |
| `apps/bff-api/tests/test_dashboard.py` | adapt (sedikit, mock downstream tetap) |
| `apps/web-vue/src/stores/auth.ts` | + providers + loadProviders |
| `apps/web-vue/src/pages/LoginPage.vue` | + Google button + sso_error banner |
| `apps/web-vue/src/router/index.ts` | + /no-tenant route + guard |
| `infra/docker-compose.yml` | + bff-data volume + env vars |
| `infra/.env.example` | + google + frontend base |
| `docs/runbook-local.md` | + 2 section (GCP setup, session rotation) |

### Add

```
apps/bff-api/app/services/auth_db.py
apps/bff-api/app/services/auth_seed.py
apps/bff-api/app/services/audit.py
apps/bff-api/app/services/auth_providers/__init__.py
apps/bff-api/app/services/auth_providers/base.py
apps/bff-api/app/services/auth_providers/password.py
apps/bff-api/app/services/auth_providers/google.py
apps/bff-api/app/routers/auth_google.py
apps/bff-api/tests/test_auth_db.py
apps/bff-api/tests/test_google_oauth.py
apps/web-vue/src/pages/NoTenantPage.vue
```

## Kunci kode

### `auth_providers/base.py`

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class AuthResult:
    user_id: str
    provider: str
    external_id: str | None = None
```

### `auth_db.py` skeleton

`AuthDB` class dengan `aiosqlite`. Method utama:
- `init_schema()` — `executescript(SCHEMA_SQL)` (idempotent)
- `has_users() -> bool`
- `get_user_by_id(user_id) -> dict | None`
- `get_user_by_username(username) -> dict | None`
- `get_password_hash(user_id) -> str | None`
- `set_password(user_id, password_hash)`
- `get_provider_link(provider, external_id) -> dict | None`
- `create_provider_link(user_id, provider, external_id, email)`
- `create_user(username, display_name) -> user_id`
- `upsert_tenant(id, name)`
- `get_tenant(id) -> dict | None`
- `get_user_tenants(user_id) -> list[dict]`
- `add_tenant_membership(user_id, tenant_id, is_default)`

### `password.py`

```python
import bcrypt
from app.services.auth_db import AuthDB
from app.services.auth_providers.base import AuthResult


class PasswordProvider:
    name = "password"

    def __init__(self, db: AuthDB):
        self.db = db

    @property
    def is_available(self) -> bool:
        return True

    async def authenticate(self, username: str, password: str) -> AuthResult | None:
        user = await self.db.get_user_by_username(username)
        if not user:
            return None
        h = await self.db.get_password_hash(user["id"])
        if not h:
            return None
        if not bcrypt.checkpw(password.encode(), h.encode()):
            return None
        return AuthResult(user_id=user["id"], provider="password")
```

### `google.py` (sketch)

```python
import base64, hashlib, secrets
from urllib.parse import urlencode

import httpx
import jwt
from jwt import PyJWKClient

from app.services.auth_db import AuthDB
from app.services.auth_providers.base import AuthResult


def make_pkce() -> tuple[str, str]:
    v = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
    c = base64.urlsafe_b64encode(hashlib.sha256(v.encode()).digest()).rstrip(b"=").decode()
    return v, c


class GoogleOAuthProvider:
    name = "google"
    AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    JWKS_URI = "https://www.googleapis.com/oauth2/v3/certs"
    ISSUERS = {"https://accounts.google.com", "accounts.google.com"}
    SCOPES = ("openid", "email", "profile")

    def __init__(self, db: AuthDB, settings):
        self.db = db
        self.settings = settings
        self._jwks = PyJWKClient(self.JWKS_URI)

    @property
    def is_available(self) -> bool:
        return bool(self.settings.google_oauth_client_id and self.settings.google_oauth_client_secret)

    def authorization_url(self, state: str, challenge: str) -> str:
        return self.AUTH_URL + "?" + urlencode({
            "client_id": self.settings.google_oauth_client_id,
            "redirect_uri": self.settings.google_oauth_redirect_url,
            "response_type": "code",
            "scope": " ".join(self.SCOPES),
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "access_type": "online",
            "prompt": "select_account",
        })

    async def exchange_code(self, code: str, verifier: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(self.TOKEN_URL, data={
                "client_id": self.settings.google_oauth_client_id,
                "client_secret": self.settings.google_oauth_client_secret,
                "code": code,
                "code_verifier": verifier,
                "redirect_uri": self.settings.google_oauth_redirect_url,
                "grant_type": "authorization_code",
            })
            r.raise_for_status()
            return r.json()

    def verify_id_token(self, id_token: str) -> dict:
        key = self._jwks.get_signing_key_from_jwt(id_token).key
        claims = jwt.decode(id_token, key, algorithms=["RS256"],
                            audience=self.settings.google_oauth_client_id,
                            options={"verify_exp": True})
        if claims.get("iss") not in self.ISSUERS:
            raise ValueError("invalid issuer")
        return claims

    def email_allowed(self, email: str) -> bool:
        if not email: return False
        e = email.lower()
        emails = [x.strip().lower() for x in self.settings.google_allowed_emails.split(",") if x.strip()]
        domains = [x.strip().lower() for x in self.settings.google_allowed_domains.split(",") if x.strip()]
        if emails and e in emails: return True
        if domains and any(e.endswith("@" + d) for d in domains): return True
        return False

    async def resolve_user(self, claims: dict) -> tuple[str, bool]:
        sub = claims["sub"]
        email = claims.get("email", "")
        link = await self.db.get_provider_link("google", sub)
        if link:
            return link["user_id"], False
        existing = await self.db.get_user_by_username(email) if email else None
        if existing:
            await self.db.create_provider_link(existing["id"], "google", sub, email)
            return existing["id"], False
        display = claims.get("name") or email or "(unnamed)"
        user_id = await self.db.create_user(username=email or sub, display_name=display)
        await self.db.create_provider_link(user_id, "google", sub, email)
        return user_id, True
```

### `routers/auth_google.py`

Implementasi sesuai flow §"Google SSO". Detail di file aktual.

### `main.py` (factory)

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.routers.auth import router as auth_router
from app.routers.auth_google import router as google_router
from app.routers.dashboard import router as dashboard_router
from app.routers.tenants import router as tenants_router
from app.services.audit import AuditWriter
from app.services.auth_db import AuthDB
from app.services.auth_providers.google import GoogleOAuthProvider
from app.services.auth_providers.password import PasswordProvider
from app.services.auth_seed import seed_defaults
from app.shared.config import Settings, settings as default_settings
from app.shared.request_id import RequestIDMiddleware
from app.shared.response import ok


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or default_settings

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        db = AuthDB(settings.auth_db_path)
        await db.init_schema()
        if not await db.has_users():
            await seed_defaults(db)
        app.state.auth_db = db
        app.state.audit = AuditWriter(db)
        app.state.settings = settings
        app.state.password_provider = PasswordProvider(db)
        app.state.google_provider = GoogleOAuthProvider(db, settings)
        yield

    app = FastAPI(title="isf-app bff-api", version="0.2.0", lifespan=lifespan)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=settings.session_secret,
                       session_cookie="isf_session", same_site="lax", https_only=False)
    app.add_middleware(CORSMiddleware, allow_origins=[settings.cors_origin],
                       allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

    @app.get("/health")
    def health(): return ok({"status": "ok"})

    app.include_router(auth_router, prefix="/api")
    app.include_router(google_router, prefix="/api")
    app.include_router(tenants_router, prefix="/api")
    app.include_router(dashboard_router, prefix="/api")
    return app


app = create_app()
```

## Eksekusi (urutan)

1. Update `apps/bff-api/pyproject.toml` (+bcrypt, pyjwt, aiosqlite).
2. Update `apps/bff-api/app/shared/config.py` (env vars).
3. Tulis `auth_db.py`, `audit.py`.
4. Tulis `auth_providers/{__init__,base,password,google}.py`.
5. Tulis `auth_seed.py`.
6. Refactor `main.py` (lifespan + create_app).
7. Refactor `services/auth.py` (slim helpers).
8. Refactor `routers/auth.py`, tambah `/providers`.
9. Tulis `routers/auth_google.py`.
10. Refactor `routers/tenants.py`.
11. Refactor `tests/conftest.py` (factory + temp DB).
12. Adapt `tests/test_auth.py`, `test_tenants.py`, `test_dashboard.py`.
13. Tambah `tests/test_auth_db.py`, `tests/test_google_oauth.py`.
14. Update `infra/docker-compose.yml` (volume + env).
15. Update `infra/.env.example`.
16. Tulis `apps/web-vue/src/pages/NoTenantPage.vue`.
17. Update `apps/web-vue/src/stores/auth.ts` (+ providers).
18. Update `apps/web-vue/src/pages/LoginPage.vue` (Google button + sso_error).
19. Update `apps/web-vue/src/router/index.ts` (no-tenant route + guard).
20. Update `docs/runbook-local.md` (GCP setup + session rotation).
21. `podman-compose down -v && podman-compose up -d --build bff-api` (volume baru `bff-data` + image baru).
22. Verifikasi.

## Verifikasi

1. Container running, healthcheck api-python OK, /health bff-api OK.
2. `GET /api/auth/providers` → `{ data: { password: true, google: false }, meta }`.
3. `POST /api/auth/login admin/admin123` → 200, session cookie diset (existing behavior).
4. `GET /api/auth/me` → user + tenant.
5. `POST /api/tenants/switch` → 200 (admin), 403 untuk finance.a→perusahaan_b.
6. `GET /api/auth/google/start` → 503 `GOOGLE_NOT_CONFIGURED` (karena creds kosong).
7. Browser di `http://localhost:5173/login`: form password tampil, tombol Google disabled + helper text "Google SSO belum dikonfigurasi".
8. Login admin → dashboard.
9. SQLite inspect: `podman exec isf-bff-api sqlite3 /data/auth.sqlite "SELECT username, status FROM users; SELECT COUNT(*) FROM audit_log"` → 3 users, audit log >0.
10. **Restart container**: `podman-compose restart bff-api` → state persistent (login lagi tetap jalan).
11. (Opsional) Set `GOOGLE_OAUTH_CLIENT_ID/SECRET` di `infra/.env` valid → restart → `/providers` lapor google=true → tombol Google enabled.

## Risiko

| # | Risiko | Mitigasi |
| --- | --- | --- |
| 1 | bcrypt wheel di python:3.12-slim gagal | Wheel resmi tersedia. Fallback: install build-essential di Dockerfile.dev. |
| 2 | aiosqlite concurrency saat banyak request | WAL mode enable; cukup untuk dev/MVP. Postgres bila scale. |
| 3 | JWKS network outage saat callback | `PyJWKClient` cache key; saat fetch gagal & cache kosong → 502 + audit. |
| 4 | State CSRF / replay | state single-use (pop dari session), PKCE wajib. |
| 5 | Volume `bff-data` belum dibuat saat pertama up | `docker-compose down -v` clean state, `up` auto-create volume. |
| 6 | Bcrypt cost factor terlalu tinggi (slow login) | Default cost=12 cukup. |

## Out of scope

- Admin UI user/tenant management (Fase 4 BRD).
- Refresh token / silent re-auth.
- MFA / WebAuthn / TOTP.
- Password reset / verifikasi email.
- LDAP / SAML.
- API key untuk service-to-service.
- Audit log viewer UI.
- Server-side session store (Redis).
- Migrasi existing DB (Fase 2).

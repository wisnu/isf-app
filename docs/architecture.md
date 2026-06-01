# Desain Teknikal Aplikasi Vue.js + Vite + Python Backend + Go Backend

Dokumen ini menjadi acuan desain teknikal untuk proses vibe coding aplikasi dengan FrontEnd Vue.js + Vite, Backend awal menggunakan Python, dan migrasi bertahap ke Go. Desain ini juga menyiapkan jalur evolusi ke Kong atau API Gateway sejenis ketika kebutuhan sistem mulai kompleks.

## 1. Tujuan Arsitektur

Tujuan utama arsitektur ini adalah membuat FrontEnd tetap stabil meskipun implementasi Backend berubah dari Python ke Go secara bertahap.

Prinsip utama:

- FrontEnd tidak boleh bergantung pada bahasa Backend.
- Kontrak API harus stabil dan terdokumentasi.
- Backend Python dan Go harus mengikuti spesifikasi API yang sama.
- Migrasi dilakukan per endpoint atau per module, bukan rewrite total.
- Vue.js + Vite digunakan sebagai FrontEnd murni.
- BFF/API Facade dipisahkan dari FrontEnd, bukan menggunakan Next.js.
- Core business logic tetap berada di Backend Python atau Go.
- Kong/API Gateway belum wajib di awal, tetapi arsitektur disiapkan agar mudah ditambahkan nanti.

Target awal:

```text
Browser
  ↓
Vue.js + Vite FrontEnd
  ↓
API Facade / BFF ringan
  ↓
Python Backend / Go Backend
  ↓
Database / Cache / Queue / Storage
```

Target masa depan:

```text
Browser / Mobile / Partner / Internal Tools
  ↓
Kong / API Gateway sejenis
  ├── Domain Services langsung untuk endpoint generic
  │     ├── Python Backend legacy
  │     └── Go Backend services
  └── API Facade / BFF hanya untuk endpoint UI-composition
        └── Python Backend / Go Backend
```

Catatan penting: pada target mature, API Facade/BFF **bukan jalur wajib untuk semua endpoint**. Facade hanya dipertahankan untuk kebutuhan khusus UI seperti dashboard aggregation, page bootstrap, user context, menu/navigation, atau transformasi response yang spesifik untuk FrontEnd.

## 2. Ringkasan Keputusan Arsitektur

| Area | Keputusan |
|---|---|
| FrontEnd | Vue.js + Vite + TypeScript |
| FrontEnd role | SPA/static frontend, tidak menjadi BFF |
| BFF/API Facade awal | Service terpisah, disarankan Python FastAPI |
| Backend awal | Python FastAPI |
| Backend migrasi | Go service/module |
| API contract | OpenAPI-first |
| Client API | Generated TypeScript client dari OpenAPI |
| Database awal | PostgreSQL |
| Cache | Redis jika dibutuhkan |
| Queue | RabbitMQ/NATS/Redis Streams jika butuh async |
| API Gateway | Tidak digunakan di awal; Kong atau sejenis ditambahkan nanti |
| Deployment awal | Docker Compose untuk local/dev |
| Testing utama | Contract test + integration test |
| Target mature routing | Kong langsung ke domain services; Facade hanya untuk UI-composition |

## 3. Peran Tiap Komponen

### 3.1 Vue.js + Vite FrontEnd

Vue.js + Vite berperan sebagai:

- UI utama.
- SPA atau static frontend.
- Konsumen API melalui generated TypeScript client.
- Pengelola state UI.
- Pengelola routing client-side jika menggunakan Vue Router.
- Pengelola validasi ringan di sisi UI.

Vue.js + Vite tidak digunakan untuk:

- BFF server-side.
- Proxy utama ke backend.
- Core business logic.
- Database ownership.
- Workflow transaksi kompleks.
- Background job.
- Queue consumer.
- Secret handling yang sensitif.

Aturan penting:

- Jangan hardcode URL Python dan Go di banyak file FrontEnd.
- FrontEnd sebaiknya hanya mengenal satu base URL API publik, misalnya `VITE_API_BASE_URL`.
- FrontEnd tidak perlu tahu apakah endpoint dilayani Python atau Go.
- Semua akses API sebaiknya lewat generated client dari OpenAPI.

### 3.2 API Facade / BFF Ringan

Karena FrontEnd menggunakan Vue.js + Vite, BFF tidak lagi berada di Next.js. Jika tetap membutuhkan BFF, buat sebagai service terpisah.

Rekomendasi awal:

```text
Vue.js + Vite
  ↓
API Facade / BFF FastAPI
  ↓
Python Backend / Go Backend
```

API Facade/BFF berperan sebagai:

- Stable public API untuk FrontEnd.
- Routing ke Python atau Go berdasarkan module/endpoint.
- Aggregator data untuk kebutuhan halaman tertentu.
- Session/cookie/token adapter jika dibutuhkan.
- Normalizer response agar format konsisten.
- Tempat menerapkan request ID dan header standar.
- Lapisan transisi sebelum Kong/API Gateway digunakan.

API Facade/BFF tidak digunakan untuk:

- Core business logic berat.
- Database ownership utama.
- Workflow transaksi kompleks.
- Background job berat.
- Queue consumer utama.
- Logic domain yang seharusnya berada di Python/Go backend.

Pilihan implementasi BFF awal:

| Opsi | Kapan dipakai |
|---|---|
| Python FastAPI BFF | Paling cocok untuk fase awal karena tim sudah familiar Python |
| Go BFF | Cocok jika ingin performa tinggi dan tim mulai nyaman dengan Go |
| Nginx/Traefik reverse proxy | Cocok jika hanya butuh routing sederhana tanpa logic agregasi |
| Kong/API Gateway | Cocok jika kebutuhan gateway sudah kompleks |

Rekomendasi untuk fase awal: gunakan **Python FastAPI sebagai API Facade/BFF ringan**, karena konsisten dengan skill awal dan mudah diubah nanti.

### 3.3 Python Backend

Python Backend adalah Backend utama pada versi awal.

Disarankan menggunakan FastAPI karena cocok untuk:

- REST API.
- OpenAPI generation.
- Pydantic schema validation.
- Modular monolith.
- Development cepat.

Python Backend bertanggung jawab untuk:

- Business logic awal.
- Database access.
- Validasi domain.
- Auth validation jika tidak dilakukan di BFF/API Facade.
- Integrasi eksternal.
- Background task ringan.

### 3.4 Go Backend

Go Backend digunakan sebagai target migrasi bertahap.

Go Backend bertanggung jawab untuk:

- Module yang sudah dimigrasi dari Python.
- Service baru yang membutuhkan performa lebih baik.
- Endpoint yang sudah stabil kontraknya.

Go Backend wajib mengikuti kontrak API yang sama dengan Python Backend.

### 3.5 API Gateway/Kong

Kong tidak digunakan di fase awal kecuali sudah ada kebutuhan nyata.

Kong baru dipertimbangkan jika:

- Ada banyak client: web, mobile, partner, third-party.
- Backend service sudah banyak.
- Butuh centralized rate limiting.
- Butuh API key management.
- Butuh traffic splitting/canary release.
- Butuh policy/security terpusat.
- Butuh API analytics terpusat.
- Butuh route management yang tidak ideal lagi jika diletakkan di BFF.

Fase awal cukup menggunakan API Facade/BFF ringan sebagai routing layer.

## 4. Rencana Evolusi ke Kong atau API Gateway Sejenis

Walaupun fase awal tidak menggunakan Kong, desain arsitektur harus tetap disiapkan agar mudah berevolusi ke API Gateway di masa depan. Artinya, sejak awal endpoint, service boundary, auth, logging, dan routing harus dibuat seolah-olah nanti akan berada di belakang gateway.

### Fase 1 - Awal / MVP

```text
Browser
  ↓
Vue.js + Vite FrontEnd
  ↓
API Facade / BFF FastAPI
  ↓
Python Backend
  ↓
PostgreSQL / Redis
```

Tujuan fase ini:

- Membuat aplikasi cepat berjalan.
- Menjaga FrontEnd hanya mengenal satu API base URL.
- Menaruh business logic utama di Python Backend.
- Menyiapkan OpenAPI contract.
- Menyiapkan struktur migrasi ke Go.

### Fase 2 - Migrasi Bertahap ke Go

```text
Browser
  ↓
Vue.js + Vite FrontEnd
  ↓
API Facade / BFF FastAPI
  ├── Python Backend
  └── Go Backend
       ↓
PostgreSQL / Redis / Queue
```

Tujuan fase ini:

- Module tertentu mulai dipindahkan ke Go.
- API Facade/BFF mengarahkan endpoint tertentu ke Python atau Go.
- FrontEnd tidak berubah.
- Contract test memastikan Python dan Go mengikuti OpenAPI yang sama.

### Fase 3 - API Gateway Mulai Diperkenalkan

Pada fase ini, Kong/API Gateway mulai masuk sebagai pintu masuk utama API. Namun, route tidak semuanya harus melewati API Facade. Route generic dapat langsung diarahkan ke domain service. Route yang membutuhkan komposisi/transformasi UI tetap diarahkan ke API Facade.

```text
Browser
  ↓
Vue.js + Vite FrontEnd
  ↓
Kong / API Gateway sejenis
  ├── /api/customers/*  -> Python/Go Customer Service
  ├── /api/orders/*     -> Python/Go Order Service
  ├── /api/reports/*    -> Go Report Service
  └── /api/dashboard    -> API Facade / BFF
                            ├── Python Backend
                            └── Go Backend
```

Pada fase ini, Kong mulai menangani:

- Centralized routing.
- Rate limiting.
- API key management.
- Centralized auth policy.
- Observability di level gateway.
- Canary release/traffic split.
- Public routing untuk Web, Mobile, Partner, atau Internal Tools.

API Facade/BFF hanya dipakai untuk endpoint yang memang membutuhkan:

- Aggregation khusus kebutuhan web UI.
- Adaptasi response khusus FrontEnd.
- Page bootstrap atau user context.
- Logic presentational yang tidak cocok masuk core backend.

### Fase 4 - Banyak Consumer / API Platform

```text
Web / Mobile / Partner / Internal Tools
  ↓
Kong / API Gateway sejenis
  ├── Customer Service
  ├── Order Service
  ├── Report Service
  ├── Python Backend legacy
  └── API Facade / BFF hanya untuk endpoint UI-composition
       ↓
Database / Cache / Queue / Object Storage
```

Tujuan memasukkan Kong/API Gateway di roadmap:

- Menyiapkan jalur untuk centralized routing.
- Menyiapkan rate limiting dan quota per client.
- Menyiapkan API key management untuk partner atau integrasi eksternal.
- Menyiapkan observability, audit log, dan analytics di level gateway.
- Menyiapkan canary deployment dan traffic split saat migrasi Python ke Go.
- Menyiapkan security policy terpusat untuk banyak client dan banyak service.

Prinsip penting:

- Vue.js + Vite tetap hanya sebagai FrontEnd.
- Kong/API Gateway menjadi entrypoint utama saat sistem mature.
- Endpoint domain generic diarahkan oleh Kong langsung ke Python/Go service terkait.
- API Facade/BFF tidak menjadi jalur wajib semua traffic.
- API Facade/BFF hanya digunakan untuk kebutuhan spesifik Web UI atau client tertentu.
- Kong tidak menjadi tempat business logic.
- Kong tidak menggantikan BFF untuk kebutuhan UI-composition, tetapi dapat menggantikan Facade untuk route generic.
- Semua service tetap wajib mengikuti OpenAPI contract yang sama.

## 5. Arsitektur Fase Awal

```text
Browser
  ↓
Vue.js + Vite FrontEnd
  ↓
API Facade / BFF FastAPI
  ↓
Python FastAPI Backend
  ↓
PostgreSQL
```

Contoh request:

```text
Browser -> GET https://app.example.com/api/customers/123
API Facade/BFF -> GET http://api-python:8000/api/v1/customers/123
Python Backend -> PostgreSQL
```

## 6. Arsitektur Saat Migrasi ke Go

```text
Browser
  ↓
Vue.js + Vite FrontEnd
  ↓
API Facade / BFF FastAPI
  ├── /api/customers -> Python Backend
  ├── /api/orders    -> Python Backend
  └── /api/reports   -> Go Backend
```

Contoh routing:

```text
/api/customers/* -> Python /api/v1/customers/*
/api/orders/*    -> Python /api/v1/orders/*
/api/reports/*   -> Go     /api/v1/reports/*
```

Saat module `customers` selesai dimigrasi:

```text
/api/customers/* -> Go /api/v1/customers/*
```

FrontEnd tetap tidak berubah.

## 7. Prinsip OpenAPI-First

OpenAPI adalah sumber kebenaran utama untuk kontrak API.

File utama:

```text
packages/api-contract/openapi.yaml
```

Kontrak API harus mendefinisikan:

- Path.
- Method.
- Request body.
- Response body.
- Error response.
- Auth requirement.
- Pagination.
- Filtering.
- Sorting.
- Status code.

Aturan:

- FrontEnd generate TypeScript client dari OpenAPI.
- API Facade/BFF harus mengikuti OpenAPI publik.
- Python Backend harus mengikuti OpenAPI internal atau kontrak module yang sama.
- Go Backend harus mengikuti OpenAPI internal atau kontrak module yang sama.
- Perubahan API harus dimulai dari update OpenAPI.
- Breaking change harus menggunakan versioning.

## 8. API Versioning

Gunakan versioning pada Backend internal:

```text
/api/v1/customers
/api/v1/orders
/api/v1/reports
```

Endpoint publik dari API Facade/BFF dapat dibuat lebih pendek:

```text
/api/customers
/api/orders
/api/reports
```

Mapping dilakukan di BFF/API Facade.

Jika terjadi breaking change besar, gunakan:

```text
/api/v2/...
```

## 9. Struktur Monorepo

> **v0.3 (split portal per domain):** struktur `apps/` di-clone menjadi `apps_zakat/` dan `apps_wakaf/`. Lihat `docs/plan-split-deployment.md`. Skeleton di bawah berlaku **dalam tiap clone** (`apps_zakat/web-vue/`, `apps_wakaf/web-vue/`, dst). Saat ini wakaf masih identik dengan zakat — akan diverge seiring fitur wakaf bertambah.

```text
isf-app/
  apps_zakat/                  ← portal Zakat (default)
    web-vue/
    bff-api/
    api-python/                 ← CRUD/management (coa, admin, identity, donors, zakat, waqf)
    report-api/                 ← read/agregasi (dashboard + report); pool read-only business + DWH
    api-go/
  apps_wakaf/                  ← portal Wakaf (clone, akan diverge; report-api menyusul)
    web-vue/
    bff-api/
    api-python/
    api-go/
  packages/
    api-contract/
    api-client-ts/
  infra/
    docker-compose.zakat.yml         ← zakat (default)
    docker-compose.wakaf.yml   ← wakaf
    db/, kong/, nginx/, .env.example
  docs/
    prd.md
    architecture.md
    runbook-local.md
    plan-*.md
```

Skeleton internal tiap aplikasi (`apps_<domain>/`):

```text
apps_<domain>/
  web-vue/
    index.html
    vite.config.ts
    package.json
    public/favicon.svg
    src/
      main.ts
      App.vue
      styles.css
      router/index.ts
      pages/             # DashboardPage, LoginPage, NoTenantPage, keuangan/{Coa,Kas,Bank}Page
      components/        # AppHeader, AppSidebar, NotificationBell, UserMenu, SystemDate, AppLogo, widgets/*
      components/ui/     # Button, Card, Input, Alert, DropdownMenu, Label, ... (shadcn-vue)
      stores/            # auth, theme, sidebar, notifications
      lib/               # utils (cn), format, charts (Chart.js register), api/client

  bff-api/
    pyproject.toml
    Dockerfile.dev
    app/
      main.py
      routers/           # auth, auth_google, tenants, dashboard
      services/
        auth_db.py       # SQLite layer (users, tenants, links, audit_log)
        audit.py
        auth_seed.py
        proxy.py
        auth_providers/  # base, password (bcrypt), google (OIDC + PKCE)
      shared/            # config, errors, request_id, response
    tests/

  api-python/              # CRUD / management / write-model
    pyproject.toml
    Dockerfile.dev
    app/
      main.py
      modules/
        coa/, admin/, identity/  # active
        donors/, zakat/, waqf/   # scaffold per modul Fase 2+
      shared/            # config, db (business + isf_auth pool), response
    tests/

  report-api/            # read / agregasi / reporting (service terpisah, zakat)
    pyproject.toml
    Dockerfile.dev
    app/
      main.py            # init pool business + dwh (read-only); /health, /ready
      modules/
        dashboard/       # router, schema, service — DIPINDAH dari api-python
        report/          # scaffold (router /report, service, schema); query via pool dwh
      shared/            # config, db (business + dwh pool, read-only), response
    tests/

  api-go/
    cmd/api/main.go
    internal/
      modules/<feature>/ # handler, service, repository, dto
      shared/            # db, auth, errors, config
```

Module-internal pattern (router/service/repository/dto) tetap berlaku — lihat §16 (Python) & §17 (Go).

## 10. Struktur API Facade / BFF

Contoh route BFF:

```text
apps/bff-api/app/routers/customers.py
```

Tanggung jawab route ini:

- Membaca cookie/session/token jika diperlukan.
- Meneruskan request ke Python atau Go.
- Menambahkan Authorization header jika diperlukan.
- Menambahkan request ID.
- Melakukan transformasi ringan jika diperlukan.
- Mengembalikan response dengan format stabil ke Browser.

Contoh pseudo-code FastAPI BFF:

```python
from fastapi import APIRouter, Request, Response
import httpx

router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.get("/{customer_id}")
async def get_customer(customer_id: str, request: Request):
    target_base_url = request.app.state.route_config.customers_base_url
    request_id = request.headers.get("X-Request-ID") or generate_request_id()

    async with httpx.AsyncClient() as client:
        backend_response = await client.get(
            f"{target_base_url}/api/v1/customers/{customer_id}",
            headers={
                "Authorization": request.headers.get("Authorization", ""),
                "X-Request-ID": request_id,
            },
        )

    return Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        media_type=backend_response.headers.get("content-type", "application/json"),
        headers={"X-Request-ID": request_id},
    )
```

## 11. Environment Variable

### Vue.js + Vite FrontEnd

```env
VITE_API_BASE_URL=http://localhost:7000
VITE_APP_ENV=development
```

Catatan:

- Variable Vite yang diekspos ke browser harus diawali `VITE_`.
- Jangan simpan secret sensitif di environment variable FrontEnd.
- Secret harus berada di BFF/API Facade atau Backend.

### API Facade / BFF

```env
API_PYTHON_BASE_URL=http://api-python:8000
REPORT_API_BASE_URL=http://report-api:8000   # dashboard + report upstream
API_GO_BASE_URL=http://api-go:8080
CUSTOMERS_BACKEND=python
ORDERS_BACKEND=python
REPORTS_BACKEND=go
JWT_PUBLIC_KEY=...
APP_ENV=development
```

### Python Backend

```env
DATABASE_URL=postgresql://app:password@postgres:5432/app_db
REDIS_URL=redis://redis:6379/0
JWT_PUBLIC_KEY=...
APP_ENV=development
```

### Report Service (report-api)

Service read/agregasi terpisah. Dua koneksi read-only — `DATABASE_URL` untuk
dashboard (business views) dan `DWH_DATABASE_URL` untuk report (schema `dwh`).
Saat ini keduanya menunjuk DB yang sama (`mziss_laz`); dipisah env agar DWH bisa
pindah ke warehouse sendiri tanpa mengubah dashboard.

```env
DATABASE_URL=postgresql://user:pass@host:5432/mziss_laz
DWH_DATABASE_URL=postgresql://user:pass@host:5432/mziss_laz
APP_ENV=development
```

> Catatan: `report-api` adalah realisasi awal "Report Service" (lihat §4 Fase 3–4
> & §23A) sebagai FastAPI. Jalur migrasi bertahap ke Go tetap mengikuti §18.

### Go Backend

```env
DATABASE_URL=postgresql://app:password@postgres:5432/app_db
REDIS_URL=redis://redis:6379/0
JWT_PUBLIC_KEY=...
APP_ENV=development
```

## 12. Format Response Standar

### 12.1 Success Response

```json
{
  "data": {
    "id": "cus_123",
    "name": "Budi"
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

### 12.2 List Response

```json
{
  "data": [
    {
      "id": "cus_123",
      "name": "Budi"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

### 12.3 Error Response

```json
{
  "error": {
    "code": "CUSTOMER_NOT_FOUND",
    "message": "Customer not found",
    "details": null
  },
  "meta": {
    "request_id": "req_123"
  }
}
```

## 13. Error Code Guideline

Gunakan error code yang eksplisit dan konsisten.

Contoh:

```text
VALIDATION_ERROR
UNAUTHORIZED
FORBIDDEN
CUSTOMER_NOT_FOUND
ORDER_NOT_FOUND
DUPLICATE_RESOURCE
INTERNAL_SERVER_ERROR
SERVICE_UNAVAILABLE
```

Mapping HTTP status:

| HTTP Status | Penggunaan |
|---|---|
| 200 | Success |
| 201 | Created |
| 204 | No content |
| 400 | Bad request / validation error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict |
| 422 | Semantic validation error |
| 500 | Internal server error |
| 503 | Service unavailable |

## 14. Auth Design

Karena Vue.js + Vite adalah frontend murni, ada dua opsi auth yang realistis.

### Opsi A - Token di FrontEnd

```text
Browser login
  ↓
Frontend menerima access token
  ↓
Frontend mengirim Authorization: Bearer <token>
  ↓
API Facade/BFF meneruskan token ke Backend
  ↓
Python/Go memvalidasi token
```

Cocok jika:

- Menggunakan OAuth/OIDC provider.
- Token lifetime pendek.
- Refresh token ditangani dengan aman.
- Risiko XSS dimitigasi dengan baik.

### Opsi B - Cookie httpOnly via BFF

```text
Browser login
  ↓
API Facade/BFF menyimpan secure httpOnly cookie
  ↓
Browser request ke API Facade/BFF
  ↓
BFF membaca session/token
  ↓
BFF meneruskan Authorization header ke Backend
  ↓
Python/Go memvalidasi token atau trusted internal token
```

Cocok jika:

- Ingin access token tidak terekspos ke JavaScript.
- Ingin session handling lebih aman di sisi server.
- BFF memang menjadi entrypoint utama semua request FrontEnd.

Rekomendasi:

- Untuk aplikasi internal/serius, pilih Opsi B jika memungkinkan.
- Backend Python dan Go harus menggunakan mekanisme auth yang sama.
- Hindari Python memakai session sendiri dan Go memakai token berbeda.

## 15. Database Design

> **v0.2 (PRD pivot):** Strategi multi-tenant memakai **database-per-tenant** — setiap perusahaan ZISWAF punya Postgres DB sendiri (existing). Lihat §15.0. Pedoman intra-DB di §15.1+ tetap berlaku untuk struktur dalam masing-masing DB.

### 15.0 DB-per-Tenant Pattern

Sejak v0.2, multi-tenant memakai **database-per-tenant**:

- **DB existing per perusahaan**: `mziss_laz` (Perusahaan 1 — LAZ), `mzis_wakaf` (Perusahaan 2 — Wakaf).
- Tidak ada kolom `tenant_id` di tabel bisnis — isolasi di level DB.
- Schema antar DB **boleh berbeda** (independen); portal mengakomodasi via adapter/view di backend.

#### Konfigurasi (env / config file)

```env
# Per-tenant DSN map di api-python
TENANT_DB__perusahaan_a=postgresql://user:pass@host:5432/mziss_laz
TENANT_DB__perusahaan_b=postgresql://user:pass@host:5432/mzis_wakaf
```

Alternatif: YAML/JSON config terbaca saat boot (lebih sesuai bila DSN sensitif disimpan di secret manager).

#### Connection routing di `api-python`

```python
# app/shared/db_router.py
import asyncpg

class TenantDbRouter:
    def __init__(self, dsn_map: dict[str, str]):
        self._dsn = dsn_map
        self._pools: dict[str, asyncpg.Pool] = {}

    async def pool_for(self, tenant_id: str) -> asyncpg.Pool:
        if tenant_id not in self._dsn:
            raise UnknownTenantError(tenant_id)
        if tenant_id not in self._pools:
            self._pools[tenant_id] = await asyncpg.create_pool(self._dsn[tenant_id])
        return self._pools[tenant_id]

    async def close_all(self):
        for pool in self._pools.values():
            await pool.close()
```

FastAPI dependency injection:

```python
# app/shared/deps.py
from fastapi import Header, Depends

async def get_tenant_db(
    x_tenant_id: str = Header(..., alias="X-Tenant-Id"),
    router: TenantDbRouter = Depends(get_router),
):
    pool = await router.pool_for(x_tenant_id)
    async with pool.acquire() as conn:
        yield conn
```

Tiap endpoint module bergantung pada `get_tenant_db` — koneksi sesuai tenant aktif otomatis.

#### Komunikasi BFF → Backend

`bff-api` meneruskan `tenant_id` ke `api-python` via header `X-Tenant-Id`:

```python
# bff-api/app/services/proxy.py (Fase 2 onwards)
headers = {
    "X-Tenant-Id": request.session["active_tenant_id"],
    "X-Branch-Id": request.session.get("active_branch_id", ""),
    "Authorization": request.headers.get("Authorization", ""),
    "X-Request-ID": request_id,
}
```

Backend menolak request tanpa `X-Tenant-Id` (atau dengan tenant yang DSN-nya tidak terdaftar).

#### Konsolidasi lintas perusahaan

Bukan first-class feature. Bila perlu di kemudian hari: query DB per tenant secara paralel di service layer (mis. `asyncio.gather`), normalize, dan merge. Di luar scope fase awal (per PRD §7.2).

#### Migrasi schema

Independen per DB. Portal MVP & Fase 2 **tidak melakukan migration** ke existing DB (read-mostly). Bila kemudian portal perlu menulis (Fase 4 ke atas), buat tabel khusus portal di schema terpisah (atau gunakan portal-owned database) untuk menghindari benturan dengan struktur existing.

### 15.1 Ownership per module dalam tiap DB

Dalam masing-masing DB existing, ownership data harus jelas per module.

Contoh:

```text
customers
customer_addresses
orders
order_items
reports
```

Aturan:

- Setiap module hanya mengakses tabel miliknya.
- Jangan membuat dependency antar module terlalu dalam.
- Repository layer wajib dipisah.
- Hindari query lintas domain yang sulit dimigrasi.

Jika nanti service sudah terpisah matang, pertimbangkan:

```text
- separate schema per service
- separate database per service
- komunikasi antar service via API/event
```

## 15A. Workflow Approval / Otorisasi

Beberapa proses input (penyaluran, posting jurnal, master data, program, wakaf, user provisioning) wajib lewat workflow approval per PRD §7.8. Bagian ini mendefinisikan tabel pendukung dan pola service.

### 15A.1 Tabel umum

Ditempatkan di portal DB (atau existing DB ketika Fase 2 mulai). Generik agar bisa di-reuse lintas modul.

```sql
CREATE TABLE approval_requests (
  id            UUID PRIMARY KEY,
  tenant_id     TEXT NOT NULL,
  record_type   TEXT NOT NULL,    -- 'disbursement', 'journal', 'coa_change', 'program', 'wakaf', 'user_provisioning', ...
  record_id     TEXT NOT NULL,    -- ID record yang di-approve
  status        TEXT NOT NULL,    -- draft|submitted|approved|rejected|recalled|posted
  amount        NUMERIC NULL,     -- untuk threshold check; null bila non-finansial
  maker_id      TEXT NOT NULL,
  approver_id   TEXT NULL,
  reason        TEXT NULL,        -- alasan reject
  submitted_at  TIMESTAMP NULL,
  decided_at    TIMESTAMP NULL,
  posted_at     TIMESTAMP NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT now(),
  updated_at    TIMESTAMP NOT NULL DEFAULT now()
);

CREATE INDEX idx_approval_status ON approval_requests(tenant_id, status);
CREATE INDEX idx_approval_record ON approval_requests(record_type, record_id);
CREATE INDEX idx_approval_maker  ON approval_requests(maker_id, status);
```

```sql
CREATE TABLE approval_rules (
  id                       UUID PRIMARY KEY,
  tenant_id                TEXT NOT NULL,
  record_type              TEXT NOT NULL,
  -- threshold: opsional. NULL berarti tidak diskip (selalu butuh approval).
  auto_approve_below       NUMERIC NULL,
  required_approver_role   TEXT NOT NULL,    -- role yang wajib approve
  escalate_to_role         TEXT NULL,
  escalate_above           NUMERIC NULL,
  sla_hours                INTEGER NULL,
  is_active                BOOLEAN NOT NULL DEFAULT TRUE,
  updated_by               TEXT NOT NULL,
  updated_at               TIMESTAMP NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, record_type)
);
```

### 15A.2 Service layer (shared)

Setiap modul yang butuh approval memanggil `ApprovalService` dengan kontrak:

- `submit(record_type, record_id, maker_id, tenant_id, amount?)` — cek rules → create `approval_requests` dengan status `submitted`. Kalau `amount < auto_approve_below`, langsung set `approved`.
- `approve(request_id, approver_id)` — validasi:
  1. `approver_id != maker_id` (self-approval prevention)
  2. approver punya role `required_approver_role` (atau eskalasi) untuk tenant
  3. status saat ini `submitted`
  4. Jika lulus → update status `approved`, set `approver_id`, `decided_at`. Trigger callback ke modul (posting hook).
- `reject(request_id, approver_id, reason)` — validasi serupa, set status `rejected`, simpan `reason`.
- `recall(request_id, maker_id)` — hanya maker bisa recall, hanya bila status masih `submitted`.
- `list_pending(approver_id, tenant_id)` — daftar request yang user bisa approve.

### 15A.3 Endpoint pattern (BFF + Backend)

```text
POST /api/<module>/<record>/submit        # maker submit; create approval_request
POST /api/<module>/<record>/approve       # checker approve; trigger posting hook
POST /api/<module>/<record>/reject        # checker reject dengan alasan
POST /api/<module>/<record>/recall        # maker tarik balik
GET  /api/approvals/pending               # daftar pending untuk user yang request
GET  /api/approvals/{id}/history          # audit history per request
```

Endpoint generik `/api/approvals/*` di BFF; tiap modul punya endpoint domain-specific `/api/<module>/<record>/*` yang internally memanggil ApprovalService.

### 15A.4 Frontend pattern

- Form record baru: dua tombol — **"Simpan Draft"** (status `draft`) dan **"Submit untuk Approval"** (status `submitted`).
- Detail record: badge status (Draft/Submitted/Approved/Rejected/Posted) + action buttons sesuai role + status.
- Halaman **"Persetujuan Pending"**: list `approval_requests` untuk approver, filter per modul.
- Notification bell muncul saat ada `submitted` baru yang user-nya berwenang approve.
- Modal approve butuh konfirmasi; modal reject wajib isi `reason`.

### 15A.5 Anti-pattern

- **Self-approval**: enforce di backend, jangan hanya UI.
- **Mutate-then-approve**: record yang sudah `submitted` tidak boleh diubah field bisnisnya sampai `rejected` atau `recalled`. Lock di backend.
- **Skip-state**: tidak boleh langsung `draft → posted`; wajib lewat `submitted` + `approved`.
- **Hardcode threshold/role per modul**: gunakan `approval_rules` agar Back Office bisa adjust tanpa rilis.
- **Lupa audit**: tiap transisi state wajib catat di `audit_log` (siapa, kapan, alasan).

### 15A.6 Implementasi awal

Fase 2 dimulai dengan dua flow: **posting jurnal** dan **penyaluran dana**. Pola yang sama di-reuse untuk modul lain saat fase berikutnya. Rule awal disetel "selalu butuh approval" untuk semua tipe, pelonggaran via Back Office (Fase 4) saat workflow stabil.

## 16. Pola Module Python

Contoh struktur module:

```text
customers/
  router.py
  schema.py
  service.py
  repository.py
```

Tanggung jawab:

| File | Tanggung jawab |
|---|---|
| router.py | HTTP endpoint |
| schema.py | Request/response model |
| service.py | Business logic |
| repository.py | Database access |

Aturan:

- Router tidak boleh berisi business logic berat.
- Service tidak boleh bergantung pada framework HTTP.
- Repository tidak boleh mengandung logic domain kompleks.
- Schema harus sinkron dengan OpenAPI.

## 17. Pola Module Go

Contoh struktur module:

```text
reports/
  handler.go
  service.go
  repository.go
  dto.go
```

Tanggung jawab:

| File | Tanggung jawab |
|---|---|
| handler.go | HTTP handler |
| dto.go | Request/response model |
| service.go | Business logic |
| repository.go | Database access |

Aturan:

- Handler harus tipis.
- Service memegang logic domain.
- Repository hanya mengurus persistence.
- DTO harus mengikuti OpenAPI.

## 18. Strategi Migrasi Python ke Go

Gunakan Strangler Fig Pattern.

### Fase 1: Semua endpoint core di Python

```text
API Facade/BFF -> Python Backend
```

### Fase 2: Module baru dibuat di Go

```text
/api/reports -> Go
/api/customers -> Python
/api/orders -> Python
```

### Fase 3: Endpoint lama mulai dipindahkan

```text
GET /api/customers/{id} -> Go
POST /api/customers -> Python
```

### Fase 4: Satu module sepenuhnya pindah ke Go

```text
/api/customers/* -> Go
```

### Fase 5: Python dikurangi bertahap

```text
Remaining legacy modules -> Python
Migrated modules -> Go
```

## 19. Checklist Sebelum Endpoint Dipindahkan ke Go

Sebelum route API Facade/BFF diarahkan dari Python ke Go, pastikan:

- [ ] OpenAPI sudah final untuk endpoint tersebut.
- [ ] Go response sama dengan kontrak OpenAPI.
- [ ] Error format sama.
- [ ] HTTP status code sama.
- [ ] Auth behavior sama.
- [ ] Pagination behavior sama.
- [ ] Filtering/sorting behavior sama.
- [ ] Contract test lulus.
- [ ] Integration test lulus.
- [ ] Logging sudah ada.
- [ ] Metrics sudah ada jika diperlukan.
- [ ] Rollback path jelas.

## 20. Testing Strategy

### 20.1 Unit Test

Digunakan untuk:

- Business logic.
- Validation.
- Utility function.

### 20.2 Integration Test

Digunakan untuk:

- API dengan database.
- Repository.
- External service mock.

### 20.3 Contract Test

Digunakan untuk memastikan Python dan Go mengikuti OpenAPI yang sama.

Wajib untuk endpoint yang akan dimigrasi.

### 20.4 End-to-End Test

Digunakan untuk user flow penting:

- Login.
- Create order.
- Update customer.
- Generate report.

## 21. Observability

Setiap service wajib memiliki:

```text
GET /health
GET /ready
```

Jika sudah perlu metrics:

```text
GET /metrics
```

Log harus structured JSON.

Contoh:

```json
{
  "timestamp": "2026-05-12T10:00:00Z",
  "level": "INFO",
  "service": "api-python",
  "request_id": "req_123",
  "method": "GET",
  "path": "/api/v1/customers/123",
  "status": 200,
  "duration_ms": 42
}
```

Request ID harus dikirim dari API Facade/BFF ke Backend:

```text
X-Request-ID: req_123
```

## 22. Local Development

Gunakan Docker Compose untuk local environment.

Komponen minimal:

```text
- web-vue
- bff-api
- api-python
- api-go
- postgres
- redis
```

Contoh service:

```text
web-vue      -> localhost:5173
bff-api      -> localhost:7000
api-python   -> localhost:8000
report-api   -> localhost:8010   # dashboard + report (zakat)
api-go       -> localhost:8080
postgres     -> localhost:5432
redis        -> localhost:6379
```

## 23. Deployment Guideline

Fase awal:

```text
- Build Vue.js + Vite menjadi static assets
- Deploy static assets ke Nginx/CDN/static hosting
- Deploy API Facade/BFF
- Deploy Python Backend
- Deploy PostgreSQL
```

Fase migrasi:

```text
- Deploy Vue.js + Vite static frontend
- Deploy API Facade/BFF
- Deploy Python Backend
- Deploy Go Backend
- Routing dikontrol di API Facade/BFF via env/config
```

Jika nanti menggunakan Kong:

```text
- Vue.js + Vite tetap sebagai FrontEnd static
- Kong menjadi entrypoint utama API
- Route generic diarahkan langsung ke Python/Go domain services
- API Facade/BFF hanya digunakan untuk UI-specific aggregation/composition
- Kong tidak menjadi tempat business logic
```

## 23A. Route Ownership Saat Kong Sudah Digunakan

Saat Kong/API Gateway sudah digunakan, setiap endpoint harus dikategorikan sebagai salah satu dari dua jenis route.

### 23A.1 Domain Route

Domain route adalah endpoint generic yang merepresentasikan resource/domain bisnis dan dapat dipakai oleh Web, Mobile, Partner, atau internal service. Route ini sebaiknya diarahkan langsung oleh Kong ke service pemilik domain.

Contoh:

```text
GET  /api/customers/{id}      -> Kong -> Customer Service
POST /api/orders              -> Kong -> Order Service
GET  /api/reports/monthly     -> Kong -> Report Service
```

Ciri domain route:

- Kontrak API stabil dan reusable.
- Tidak spesifik ke satu halaman UI.
- Tidak hanya berguna untuk Vue Web.
- Business logic berada di service pemilik domain.
- Cocok dipanggil langsung oleh banyak consumer melalui Kong.

### 23A.2 UI-Composition Route

UI-composition route adalah endpoint yang dibuat untuk menyederhanakan kebutuhan satu halaman atau flow di FrontEnd. Route ini boleh diarahkan Kong ke API Facade/BFF.

Contoh:

```text
GET /api/dashboard       -> Kong -> API Facade -> Customer + Order + Report Service
GET /api/page-bootstrap  -> Kong -> API Facade -> User + Menu + Permission Service
GET /api/user-context    -> Kong -> API Facade -> Auth + Profile + Preference Service
```

Ciri UI-composition route:

- Spesifik untuk kebutuhan tampilan atau flow FrontEnd.
- Menggabungkan beberapa service.
- Melakukan transformasi response agar lebih mudah dikonsumsi UI.
- Tidak menyimpan business logic utama.
- Bisa berubah mengikuti kebutuhan UI.

Rule praktis:

```text
Generic domain API       -> Kong -> Domain Service langsung
UI-specific composition  -> Kong -> API Facade/BFF -> Domain Services
```

## 24. Routing Configuration

Agar routing mudah diubah, jangan hardcode terlalu banyak.

Gunakan config di API Facade/BFF:

```python
backend_routes = {
    "customers": os.getenv("CUSTOMERS_BACKEND", "python"),
    "orders": os.getenv("ORDERS_BACKEND", "python"),
    "reports": os.getenv("REPORTS_BACKEND", "go"),
}
```

Contoh env:

```env
CUSTOMERS_BACKEND=python
ORDERS_BACKEND=python
REPORTS_BACKEND=go
```

Saat migrasi:

```env
CUSTOMERS_BACKEND=go
ORDERS_BACKEND=python
REPORTS_BACKEND=go
```

FrontEnd hanya perlu base URL:

```env
VITE_API_BASE_URL=http://localhost:7000
```

## 25. Coding Rules untuk Vibe Coding

Gunakan aturan berikut saat melakukan vibe coding:

1. Mulai dari OpenAPI contract.
2. Generate atau buat tipe TypeScript berdasarkan kontrak.
3. Buat API Facade/BFF route jika endpoint perlu dipublikasikan ke FrontEnd.
4. Buat endpoint Python terlebih dahulu.
5. Pastikan response/error format konsisten.
6. Tambahkan test minimal.
7. Jika module sudah stabil, buat versi Go.
8. Jalankan contract test untuk Python dan Go.
9. Ubah routing API Facade/BFF dari Python ke Go.
10. Jangan ubah FrontEnd jika kontrak tidak berubah.

## 26. Prompt Template untuk Vibe Coding

### 26.1 Membuat Endpoint Baru

```text
Buat endpoint baru berdasarkan arsitektur berikut:
- FrontEnd: Vue.js + Vite + TypeScript
- BFF/API Facade: Python FastAPI service terpisah
- Backend awal: Python FastAPI
- Target migrasi: Go
- API contract: OpenAPI-first
- Format response harus menggunakan { data, meta }
- Format error harus menggunakan { error, meta }

Endpoint:
[METHOD] [PATH]

Business requirement:
[ISI REQUIREMENT]

Buat:
1. OpenAPI spec
2. API Facade/BFF route
3. Python FastAPI router/service/repository/schema
4. Unit test minimal
5. Contoh request/response
```

### 26.2 Migrasi Endpoint ke Go

```text
Migrasikan endpoint berikut dari Python FastAPI ke Go tanpa mengubah kontrak API.

Endpoint:
[METHOD] [PATH]

OpenAPI contract:
[LAMPIRKAN SPEC]

Existing behavior:
[JELASKAN BEHAVIOR PYTHON]

Buat:
1. Go handler/service/repository/dto
2. Response format yang sama
3. Error format yang sama
4. Contract test
5. Update mapping API Facade/BFF agar endpoint dapat diarahkan ke Go
```

### 26.3 Membuat API Facade / BFF Route

```text
Buat FastAPI BFF route untuk endpoint berikut:

Public route:
/api/[RESOURCE]

Backend target:
Python: http://api-python:8000/api/v1/[RESOURCE]
Go: http://api-go:8080/api/v1/[RESOURCE]

Requirement:
- baca session/cookie/token jika tersedia
- forward Authorization header jika tersedia
- tambahkan X-Request-ID
- preserve status code
- preserve response body
- handle backend error dengan format standar
- routing target bisa dikontrol via env/config
```

### 26.4 Membuat Halaman Vue

```text
Buat halaman Vue.js + Vite + TypeScript untuk resource berikut:

Resource:
[RESOURCE]

API:
[METHOD] [PATH]

Requirement:
- gunakan generated TypeScript client dari OpenAPI
- jangan hardcode URL backend Python/Go
- gunakan VITE_API_BASE_URL
- tampilkan loading state
- tampilkan empty state
- tampilkan error state sesuai format { error, meta }
```

## 27. Anti-Pattern yang Harus Dihindari

Hindari:

- FrontEnd memanggil Python dan Go langsung tanpa API Facade/BFF atau Gateway.
- Secret sensitif disimpan di Vite env yang terekspos ke browser.
- Business logic besar ditaruh di BFF/API Facade.
- Response Python dan Go berbeda format.
- Error code tidak konsisten.
- Database table diakses bebas oleh semua module.
- Migrasi dilakukan tanpa contract test.
- Endpoint Go dibuat tanpa mengikuti OpenAPI.
- Hardcode URL backend di banyak file FrontEnd.
- Menggunakan Kong terlalu awal tanpa kebutuhan nyata.
- Menjadikan Kong sebagai tempat business logic.

## 28. Roadmap Implementasi

### Milestone 1: Foundation

- [ ] Setup monorepo.
- [ ] Setup Vue.js + Vite app.
- [ ] Setup API Facade/BFF FastAPI.
- [ ] Setup Python FastAPI app.
- [ ] Setup PostgreSQL.
- [ ] Setup Docker Compose.
- [ ] Buat OpenAPI awal.
- [ ] Buat format response/error standar.

### Milestone 2: First Module

- [ ] Buat module pertama di Python.
- [ ] Buat route di API Facade/BFF.
- [ ] Generate TypeScript client.
- [ ] Buat test dasar.
- [ ] Hubungkan halaman Vue ke API Facade/BFF.

### Milestone 3: Migration Readiness

- [ ] Tambahkan request ID.
- [ ] Tambahkan structured logging.
- [ ] Tambahkan contract test.
- [ ] Tambahkan health/readiness endpoint.
- [ ] Rapikan repository/service boundary.

### Milestone 4: First Go Module

- [ ] Setup Go service.
- [ ] Implement satu endpoint/module.
- [ ] Ikuti OpenAPI yang sama.
- [ ] Jalankan contract test.
- [ ] Arahkan API Facade/BFF route ke Go.
- [ ] Pastikan FrontEnd tidak berubah.

### Milestone 5: API Gateway Readiness

- [ ] Evaluasi kebutuhan Kong/API Gateway.
- [ ] Pisahkan route yang generic dan route yang UI-specific.
- [ ] Pastikan semua service punya health/readiness endpoint.
- [ ] Pastikan auth dan request ID sudah konsisten.
- [ ] Siapkan folder `infra/kong` untuk konfigurasi awal jika dibutuhkan.

### Milestone 6: Scale

- [ ] Tambahkan Kong/API Gateway jika kebutuhan sudah nyata.
- [ ] Evaluasi service separation.
- [ ] Evaluasi queue/event bus.
- [ ] Evaluasi database ownership per service.
- [ ] Evaluasi API untuk mobile/partner jika ada.

## 29. Kesimpulan Desain

Desain yang digunakan:

```text
Vue.js + Vite FrontEnd
  ↓
API Facade / BFF FastAPI
  ↓
Python FastAPI Backend untuk versi awal
  ↓
Go Backend untuk migrasi bertahap
  ↓
PostgreSQL / Redis / Queue
```

Keputusan penting:

- Gunakan Vue.js + Vite sebagai FrontEnd murni.
- Jangan menggunakan Next.js BFF karena FrontEnd sudah berubah ke Vue/Vite.
- Gunakan API Facade/BFF terpisah, disarankan FastAPI.
- Gunakan OpenAPI sebagai kontrak utama.
- Gunakan generated TypeScript client.
- Buat Python Backend sebagai modular monolith.
- Migrasikan ke Go per module/endpoint.
- Pastikan semua migrasi dilindungi contract test.
- Tambahkan Kong/API Gateway hanya jika kebutuhan gateway sudah nyata.
- Siapkan arsitektur sejak awal agar Kong bisa masuk tanpa rewrite besar.

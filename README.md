# isf-app

> Islamic Social Finance — a zakat & waqf management platform.

> **Status:** design phase. Source code is not yet scaffolded; [`docs/architecture.md`](docs/architecture.md) is the source of truth for every decision in this README.

## What is this?

`isf-app` is the foundation of a modular platform for **Islamic Social Finance (ISF)** instruments — primarily **zakat** and **waqf**, with room for related instruments such as infaq and sadaqah. The repository follows a stack designed for stable API contracts and incremental migration: the frontend stays unchanged while the backend evolves from Python to Go on a per-module basis.

## Stack

| Layer | Technology | Role | Phase |
| --- | --- | --- | --- |
| Frontend | Vue.js + Vite + TypeScript | SPA / static frontend | from day one |
| API Facade / BFF | Python FastAPI (separate service) | Stable public API, routing, request-ID, response normalization | from day one |
| Backend (initial) | Python FastAPI | Business logic, persistence | from day one |
| Backend (migration target) | Go | Per-module migration once contracts are stable | phased |
| Database | PostgreSQL | Primary store | from day one |
| Cache | Redis | Optional | when needed |
| API Gateway | Kong (or similar) | Centralized routing, rate limit, API keys | future |
| API contract | OpenAPI-first | Single source of truth | from day one |

## Architecture at a glance

Initial / MVP topology:

```text
Browser
  ↓
Vue.js + Vite frontend
  ↓
API Facade / BFF (FastAPI)
  ↓
Python FastAPI backend
  ↓
PostgreSQL
```

Migration target: per-endpoint move from Python to Go behind the same API Facade — the frontend doesn't change. The future Kong-based topology and full migration phases are detailed in [`docs/architecture.md`](docs/architecture.md).

## Monorepo layout (v0.3 — split portal per domain)

```text
isf-app/
  apps_zakat/                # Portal LAZ (zakat, infaq, sadaqah) — DB: mziss_laz
    web-vue/                 # Vue 3 + Vite + TS + Tailwind + shadcn-vue
    bff-api/                 # FastAPI BFF (auth, session, proxy)
    api-python/              # FastAPI backend
    api-go/                  # Go service (per-module migration target)
  apps_wakaf/                # Portal Wakaf — DB: mzis_wakaf (clone, akan diverge)
    web-vue/
    bff-api/
    api-python/
    api-go/
  packages/
    api-contract/            # OpenAPI single source of truth
    api-client-ts/           # generated TypeScript client
  infra/
    docker-compose.zakat.yml       # zakat stack (default)
    docker-compose.wakaf.yml # wakaf stack (separate ports, namespace)
    .env.example
    db/
      migrations/
    nginx/
    kong/
  docs/
    prd.md                   # Product Requirements (was BRD)
    architecture.md          # Technical design
    runbook-local.md         # Local dev guide
    plan-*.md                # iteration plans (mvp, quasar, tailwind-shadcn, auth, dashboard-widgets, split-deployment)
```

## Running locally

```bash
cd infra

# Portal Zakat (default)
podman-compose -f docker-compose.zakat.yml up -d --build
# → http://localhost:5173

# Portal Wakaf (independent stack)
podman-compose -f docker-compose.wakaf.yml up -d --build
# → http://localhost:5174
```

Demo akun (sama di kedua portal): `admin/admin123`, `finance.a/finance123`, `finance.b/finance123`.

## Roadmap

Detail di [`docs/prd.md`](docs/prd.md) §10. Highlight:

1. **Fase 1 — MVP**: login + dashboard skeleton + tenant switcher (selesai untuk portal zakat).
2. **Fase 2 — Dashboard & Laporan**: koneksi ke existing DB (`mziss_laz`, `mzis_wakaf`); multi-cabang switcher; laporan rich + export.
3. **Fase 3 — Manajemen User + Production Auth**: cookie httpOnly, role-cabang, audit log viewer.
4. **Fase 4 — Input Pertama (Penyaluran)** dengan workflow maker–checker (PRD §7.8).
5. **Fase 5 — Input Lanjutan** (program, wakaf, posting jurnal, master data).
6. **Fase 6+ — Scale** (API gateway, migrasi Go, mobile/partner).

## Documentation

- [`docs/prd.md`](docs/prd.md) — Product Requirements Document.
- [`docs/architecture.md`](docs/architecture.md) — Technical architecture & design.
- [`docs/runbook-local.md`](docs/runbook-local.md) — Local development & deployment guide.
- [`docs/plan-split-deployment.md`](docs/plan-split-deployment.md) — Split deployment plan (zakat vs wakaf).

# isf-app

> Islamic Social Finance — a zakat & waqf management platform.

> **Status:** active development. Two portals live — Zakat (`:5173`) and Wakaf (`:5174`).

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

Use `make help` to list all available targets.

### Fresh checkout (first time)

```bash
# 1. Create & seed isf_auth_zakat + isf_auth_wakaf databases
make migrate

# 2. Pre-build all images (required once; repeat when pyproject.toml / package.json changes)
make build

# 3. Start both stacks
make run
#    → Zakat:  http://localhost:5173  (bff-api :7000, api-python :8000, report-api :8010)
#    → Wakaf:  http://localhost:5174  (bff-api :7001, api-python :8001, report-api :8011)

# 4. Smoke-test all services
make health
```

> **Note (SELinux / Fedora):** `podman build` inside `podman-compose up --build` fails due to MCS
> mprotect blocks. Always pre-build with `make build` first, then `make run` without `--build`.

### Day-to-day

```bash
make run          # start both portals
make run-zakat    # start zakat only
make run-wakaf    # start wakaf only

make stop         # stop both
make restart      # stop + run

make ps           # show isf-* container status
make logs         # tail both stacks (Ctrl+C to exit)
make logs-zakat   # tail zakat only
make logs-wakaf   # tail wakaf only

make health       # curl /health on all BFFs + api-pythons
```

### Database management

```bash
make migrate      # create DBs + apply schema + seed (safe to re-run)
make db-create    # create isf_auth_zakat + isf_auth_wakaf if absent
make db-apply     # apply schema dumps (idempotent)
make db-seed      # seed menu + role_menu rows

make db-drop      # DESTRUCTIVE — prompts "yes" before dropping both auth DBs
```

Override DB credentials (defaults: `postgres` / `solusi`):

```bash
make PG_USER=postgres PG_PASS=mypass migrate
```

### Cleanup

```bash
make clean        # stop + remove named volumes (PG data on host persists)
                  # use db-drop separately to also drop the auth databases
```

### Dev accounts

| Username | Password | Roles | Portal |
|----------|----------|-------|--------|
| `HADI`   | `test1234` | DIST / SPVDIST (branch_access=all) | Zakat |
| `RAIS`   | `test1234` | ACC / KEU (branch_access=single, branch 001) | Zakat |
| `ADM`    | `test1234` | Admin | Zakat |

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

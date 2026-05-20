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

## Planned monorepo layout

```text
isf-app/
  apps/
    web-vue/        # Vue.js + Vite SPA
    bff-api/        # FastAPI API Facade / BFF
    api-python/     # Python FastAPI backend (initial)
    api-go/         # Go backend (migration target)
  packages/
    api-contract/   # openapi.yaml — single source of truth
    api-client-ts/  # Generated TypeScript client
  infra/
    docker-compose.yml
    nginx/
    kong/
    db/
      migrations/
  docs/
    architecture.md
```

## Roadmap

High-level milestones (full checklist in [`docs/architecture.md` §28](docs/architecture.md)):

1. **Foundation** — monorepo, Vue app, BFF, Python backend, PostgreSQL, Docker Compose, baseline OpenAPI, standard response/error format.
2. **First module** — first Python module exposed through the BFF, consumed by Vue via generated TypeScript client.
3. **Migration readiness** — request ID, structured logging, contract tests, health/ready endpoints, clean module boundaries.
4. **First Go module** — implement one module in Go against the same OpenAPI, switch BFF routing.
5. **API gateway readiness** — separate generic vs UI-composition routes, prepare `infra/kong/`.
6. **Scale** — introduce Kong when demand is real; evaluate per-service separation and event bus.

## Documentation

- [`docs/architecture.md`](docs/architecture.md) — full technical design: principles, phase-by-phase topology, OpenAPI workflow, response/error format, auth options, migration checklist, anti-patterns, and prompt templates for vibe coding.

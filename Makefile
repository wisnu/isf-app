# isf-app — local dev orchestration
# Usage: `make help` to list targets.
#
# Override compose runtime: `make COMPOSE='docker compose' run`
# Override PG creds:        `make PG_USER=postgres PG_PASS=solusi migrate`

SHELL    := /bin/bash
COMPOSE  ?= podman-compose
INFRA    := infra
PORTALS  := zakat wakaf
SERVICES := api-python bff-api web-vue

PG_HOST  ?= localhost
PG_USER  ?= postgres
PG_PASS  ?= solusi

ZAKAT_COMPOSE := $(INFRA)/docker-compose.zakat.yml
WAKAF_COMPOSE := $(INFRA)/docker-compose.wakaf.yml

.DEFAULT_GOAL := help

.PHONY: help run run-zakat run-wakaf stop stop-zakat stop-wakaf restart \
        build build-zakat build-wakaf \
        migrate db-create db-apply db-seed db-drop \
        ps logs logs-zakat logs-wakaf health clean

help: ## List available targets
	@awk 'BEGIN{FS=":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo
	@echo "Common flow on fresh checkout:"
	@echo "  1. make migrate    # create + apply schema + seed (isf_auth DBs)"
	@echo "  2. make build      # podman build with SELinux workaround"
	@echo "  3. make run        # podman-compose up -d (both portals)"
	@echo "  4. make health     # smoke test"

# ── Compose lifecycle ───────────────────────────────────────────────────────

run: run-zakat run-wakaf ## Start both stacks (zakat:5173 + wakaf:5174)

run-zakat: ## Start zakat stack only
	cd $(INFRA) && $(COMPOSE) -f docker-compose.zakat.yml up -d

run-wakaf: ## Start wakaf stack only
	cd $(INFRA) && $(COMPOSE) -f docker-compose.wakaf.yml up -d

stop: stop-zakat stop-wakaf ## Stop both stacks

stop-zakat: ## Stop zakat stack only
	cd $(INFRA) && $(COMPOSE) -f docker-compose.zakat.yml down

stop-wakaf: ## Stop wakaf stack only
	cd $(INFRA) && $(COMPOSE) -f docker-compose.wakaf.yml down

restart: stop run ## stop && run

# ── Image build (manual, SELinux label workaround) ──────────────────────────

build: build-zakat build-wakaf ## Pre-build all 6 images (--security-opt label=disable)

# Zakat carries an extra reporting service (report-api); wakaf belum.
ZAKAT_SERVICES := api-python report-api bff-api web-vue

build-zakat: ## Pre-build zakat images (incl. report-api)
	@for svc in $(ZAKAT_SERVICES); do \
	  echo ">>> building isf-zakat-$$svc:dev"; \
	  (cd apps_zakat/$$svc && \
	   podman build --security-opt label=disable -t isf-zakat-$$svc:dev -f Dockerfile.dev .) || exit 1; \
	done

build-wakaf: ## Pre-build 3 wakaf images
	@for svc in $(SERVICES); do \
	  echo ">>> building isf-wakaf-$$svc:dev"; \
	  (cd apps_wakaf/$$svc && \
	   podman build --security-opt label=disable -t isf-wakaf-$$svc:dev -f Dockerfile.dev .) || exit 1; \
	done

# ── DB migration ────────────────────────────────────────────────────────────

migrate: db-create db-apply db-seed ## Create isf_auth_<portal> DBs + apply schema + seed menu/role_menu

db-create: ## Create isf_auth_zakat + isf_auth_wakaf DBs if absent
	@for portal in $(PORTALS); do \
	  exists=$$(PGPASSWORD=$(PG_PASS) psql -h $(PG_HOST) -U $(PG_USER) -tAc "SELECT 1 FROM pg_database WHERE datname='isf_auth_$$portal'"); \
	  if [ "$$exists" = "1" ]; then \
	    echo ">>> DB isf_auth_$$portal already exists"; \
	  else \
	    echo ">>> creating isf_auth_$$portal"; \
	    PGPASSWORD=$(PG_PASS) createdb -h $(PG_HOST) -U $(PG_USER) "isf_auth_$$portal"; \
	  fi; \
	done

db-apply: ## Apply isf_auth schema dumps (idempotent — CREATE SCHEMA IF NOT EXISTS etc.)
	@for portal in $(PORTALS); do \
	  echo ">>> applying schema to isf_auth_$$portal"; \
	  PGPASSWORD=$(PG_PASS) psql -h $(PG_HOST) -U $(PG_USER) -d "isf_auth_$$portal" \
	    -v ON_ERROR_STOP=1 -q \
	    -f $(INFRA)/db/migrations/isf_auth/recovered-schema-$$portal.sql; \
	done

db-seed: ## Seed isf_auth.menu (9 keys) + role_menu (45 rows, 14 roles)
	@for portal in $(PORTALS); do \
	  echo ">>> seeding isf_auth_$$portal"; \
	  PGPASSWORD=$(PG_PASS) psql -h $(PG_HOST) -U $(PG_USER) -d "isf_auth_$$portal" \
	    -v ON_ERROR_STOP=1 \
	    -f $(INFRA)/db/migrations/isf_auth/seed-menu-and-rolemenu.sql; \
	done

db-drop: ## DESTRUCTIVE — drop both isf_auth DBs (prompts confirmation)
	@read -r -p "Drop isf_auth_zakat & isf_auth_wakaf? Type 'yes': " ans; \
	if [ "$$ans" = "yes" ]; then \
	  for portal in $(PORTALS); do \
	    PGPASSWORD=$(PG_PASS) dropdb -h $(PG_HOST) -U $(PG_USER) --if-exists "isf_auth_$$portal"; \
	  done; \
	else \
	  echo "aborted"; \
	fi

# ── Inspect & cleanup ───────────────────────────────────────────────────────

ps: ## Show isf-* container status
	@podman ps -a --filter "name=isf-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

logs: ## Tail logs for both stacks (Ctrl+C to exit)
	cd $(INFRA) && $(COMPOSE) -f docker-compose.zakat.yml logs -f & \
	cd $(INFRA) && $(COMPOSE) -f docker-compose.wakaf.yml logs -f

logs-zakat: ## Tail zakat logs only
	cd $(INFRA) && $(COMPOSE) -f docker-compose.zakat.yml logs -f

logs-wakaf: ## Tail wakaf logs only
	cd $(INFRA) && $(COMPOSE) -f docker-compose.wakaf.yml logs -f

health: ## Curl /health on all BFFs + api-pythons
	@printf "  zakat api-python :8000  "; curl -fsS http://localhost:8000/health 2>/dev/null | head -c 80 || echo "DOWN"; echo
	@printf "  zakat report-api :8010  "; curl -fsS http://localhost:8010/health 2>/dev/null | head -c 80 || echo "DOWN"; echo
	@printf "  zakat bff-api    :7000  "; curl -fsS http://localhost:7000/health 2>/dev/null | head -c 80 || echo "DOWN"; echo
	@printf "  wakaf api-python :8001  "; curl -fsS http://localhost:8001/health 2>/dev/null | head -c 80 || echo "DOWN"; echo
	@printf "  wakaf bff-api    :7001  "; curl -fsS http://localhost:7001/health 2>/dev/null | head -c 80 || echo "DOWN"; echo
	@printf "  zakat web-vue    :5173  "; curl -fsS -o /dev/null -w "HTTP %{http_code}" http://localhost:5173/ 2>/dev/null || echo "DOWN"; echo
	@printf "  wakaf web-vue    :5174  "; curl -fsS -o /dev/null -w "HTTP %{http_code}" http://localhost:5174/ 2>/dev/null || echo "DOWN"; echo

clean: ## Stop + remove named volumes (PG data persists — use db-drop separately)
	cd $(INFRA) && $(COMPOSE) -f docker-compose.zakat.yml down -v
	cd $(INFRA) && $(COMPOSE) -f docker-compose.wakaf.yml down -v

# Plan — Backend Domain Refactor (BFF + api-python + report-api)

**Slug:** `2026-06-21-002-backend-domain-refactor`
**Portal:** Zakat first → Wakaf after
**See:** [`specs.md`](./specs.md)
**Commit tag:** `[BACKEND-DOMAIN-REFACTOR]`
**Strategy:** One service at a time, bottom-up (api-python → report-api → BFF → frontend). Each phase ends with `make health` before proceeding. All phases are pure structural — zero logic changes.

> **Invariant throughout:** Business logic, SQL, Pydantic field names, auth decorators, and BFF session handling never change.

---

## Phase 0 — Scaffold new api-python directories

- [x] Create `app/modules/finance/master/{coa,bank,petty_cash,parameter}/`
- [x] Create `app/modules/finance/budget/`
- [x] Create `app/modules/finance/transaction/{_shared,fund_collection,fund_distribution,amil_income,amil_expense,cash_advance,cash_advance_settlement,inter_account_transfer,general,receivable}/`
- [x] Create `app/modules/finance/upload/{collection,hc_zis}/`
- [x] Create `app/modules/finance/inquiry/transaction_history/`
- [x] Create `app/modules/finance/monitoring/authorization/`
- [x] Create `app/modules/finance/zakat/`
- [x] Create `app/modules/finance/waqf/`
- [x] Create `app/modules/administration/identity/`
- [x] Create `app/modules/fundraising/donors/`
- [x] Verify: only new empty dirs, no file changes

---

## Phase 1 — api-python: flat modules → domain hierarchy

Move files per specs §5 table. All moves are pure `git mv` — content unchanged.

### 1a — Finance master
- [x] `git mv modules/coa/* modules/finance/master/coa/`
- [x] `git mv modules/bank/* modules/finance/master/bank/`
- [x] `git mv modules/petty_cash/* modules/finance/master/petty_cash/`
- [x] `git mv modules/parameter/* modules/finance/master/parameter/`

### 1b — Finance budget
- [x] `git mv modules/budget/* modules/finance/budget/`

### 1c — Finance transaction (split from flat files)
- [x] Split `modules/transaction/fund_collection_{router,service,schema,repo}.py` → `modules/finance/transaction/fund_collection/{router,service,schema,repo}.py`
- [x] Split `modules/transaction/fund_distribution_{router,service,schema,repo}.py` → `modules/finance/transaction/fund_distribution/`
- [x] Split `modules/transaction/amil_income_{router,service,schema}.py` → `modules/finance/transaction/amil_income/`
- [x] Split `modules/transaction/amil_expense_{router,service,schema}.py` → `modules/finance/transaction/amil_expense/`
- [x] Split `modules/transaction/cash_advance_{router,service,schema}.py` → `modules/finance/transaction/cash_advance/`
- [x] Split `modules/transaction/cash_advance_settlement_{router,service,schema}.py` → `modules/finance/transaction/cash_advance_settlement/`
- [x] Split `modules/transaction/inter_account_transfer_{router,service,schema}.py` → `modules/finance/transaction/inter_account_transfer/`
- [x] Split `modules/transaction/general_{router,service,schema}.py` → `modules/finance/transaction/general/`
- [x] Split `modules/transaction/receivable_{router,service,schema}.py` → `modules/finance/transaction/receivable/`
- [x] `git mv modules/transaction/{commit,parse,template,repository}.py modules/finance/transaction/_shared/`

### 1d — Finance upload
- [x] Split `modules/transaction/hc_zis_{router,service,schema,parse,commit}.py` → `modules/finance/upload/hc_zis/`
- [x] `git mv modules/transaction/{router,service,schema}.py modules/finance/upload/collection/`
- [x] Delete empty `modules/transaction/`

### 1e — Finance inquiry + monitoring
- [x] `git mv modules/transaction_history/* modules/finance/inquiry/transaction_history/`
- [x] `git mv modules/authorization/* modules/finance/monitoring/authorization/`

### 1f — Finance specific + other domains
- [x] `git mv modules/waqf/* modules/finance/waqf/`
- [x] `git mv modules/zakat/* modules/finance/zakat/`
- [x] `git mv modules/admin/* modules/administration/`
- [x] `git mv modules/identity/* modules/administration/identity/`
- [x] `git mv modules/donors/* modules/fundraising/donors/`
- [x] Delete now-empty old module dirs

---

## Phase 2 — api-python: update imports + router prefixes + main.py

- [x] Add `__init__.py` to all new module dirs
- [x] Update intra-module imports (e.g., `from app.modules.transaction._shared.commit import ...`)
- [x] Update each `router.py` `APIRouter(prefix=...)` per specs §5 URL table
- [x] Rewrite `app/main.py` to import from new module paths
- [x] Run: `python -c "import app.main"` → zero import errors
- [x] `make health` (zakat) → api-python `:8000` responds ok

---

## Phase 3 — report-api: reorganize + update prefixes

- [x] Create `app/modules/finance/reports/` and `app/modules/finance/dashboard/`
- [x] `git mv modules/report/* modules/finance/reports/`
- [x] `git mv modules/dashboard/* modules/finance/dashboard/`
- [x] Update `APIRouter(prefix=...)` in each: `/report` → `/finance/report`, `/dashboard` → `/finance/dashboard`
- [x] Update `app/main.py` imports
- [x] `make health` → report-api `:8010` responds ok

---

## Phase 4 — BFF: reorganize routers → modules

### 4a — Scaffold
- [x] Create `app/modules/core/`, `app/modules/finance/`, `app/modules/administration/`, `app/modules/fundraising/`

### 4b — Core (move, no content change)
- [x] `git mv routers/auth.py modules/core/auth.py`
- [x] `git mv routers/auth_google.py modules/core/auth_google.py`
- [x] `git mv routers/tenants.py modules/core/tenants.py`

### 4c — Finance: merge multi-file groups into single group files
- [x] Create `modules/finance/master.py` — merge coa + bank + petty_cash + parameter routers (all routes, update sub-router prefixes to `/api/finance/master/{resource}`)
- [x] Create `modules/finance/budget.py` — from `routers/budget.py`, update prefix to `/api/finance/budget`
- [x] Create `modules/finance/transaction.py` — merge 9 transaction routers, update prefixes to `/api/finance/transaction/{resource}`
- [x] Create `modules/finance/upload.py` — merge transaction + hc_zis, update prefixes to `/api/finance/upload/{collection|hc-zis}`
- [x] Create `modules/finance/inquiry.py` — from `routers/transaction_history.py`, prefix → `/api/finance/inquiry/transaction-history`
- [x] Create `modules/finance/monitoring.py` — from `routers/authorization.py`, prefix → `/api/finance/monitoring/authorization`
- [x] Create `modules/finance/reports.py` — from `routers/report.py`, prefix → `/api/finance/report`
- [x] Create `modules/finance/dashboard.py` — from `routers/dashboard.py`, prefix → `/api/finance/dashboard`
- [x] Move `routers/zakat.py` → `modules/finance/zakat.py` (if exists), update prefix
- [x] Move `routers/waqf.py` → `modules/finance/waqf.py` (if exists), update prefix

### 4d — Other domains
- [x] Create `modules/administration/admin.py` — from `routers/admin.py`, prefix → `/api/administration`
- [x] Move `routers/donors.py` → `modules/fundraising/donors.py` (if exists)
- [x] Delete `routers/` directory

---

## Phase 5 — BFF: update downstream call paths + main.py

- [x] Update all `proxy.get()`/`proxy.post()`/`proxy.delete()` call strings inside new BFF module files to match new api-python URL prefixes (specs §6 downstream changes)
- [x] Update BFF report proxy target: `/report/` → `/finance/report/`, `/dashboard/` → `/finance/dashboard/`
- [x] Rewrite `app/main.py`: import from `app.modules.*` instead of `app.routers.*`
- [x] Run: `python -c "import app.main"` → zero errors
- [x] `make health` → all 3 zakat services healthy

---

## Phase 6 — Frontend: update BFF call strings

- [x] Grep all `GET(`, `POST(`, `blob(`, `DELETE(` in `apps_zakat/web-vue/src/` view files
- [x] Replace each URL per specs §4 table (24 prefix changes)
- [x] Verify 0 stale old prefixes remain
- [x] Browser smoke test: login → dashboard → Chart of Accounts → Fund Collection → Authorization → Report

---

## Phase 7 — Wakaf portal mirror

- [x] Apply phases 0–6 to `apps_wakaf/` (fewer modules, same structure)
- [x] Wakaf api-python has simpler transaction set — only map what exists
- [x] `make health` → wakaf `:5174` HTTP 200, all backend ok

---

## Post-refactor

- [x] Update `CLAUDE.md` — backend folder structure section
- [x] Update `nuwis-bff-builder` + `nuwis-python-builder` skill path references
- [x] Single commit per phase with tag `[BACKEND-DOMAIN-REFACTOR]`

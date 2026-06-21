# Specs — Backend Domain Refactor (BFF + api-python + report-api)

**Slug:** `2026-06-21-002-backend-domain-refactor`
**Type:** Structural Refactor (backend only, contract-changing)
**Portal:** Zakat first, mirror to Wakaf after
**Companion:** [`plan.md`](./plan.md)

---

## 1. Problem Statement

The three backend services have inconsistent, non-domain-oriented structures:

- **BFF** — `routers/` is a flat directory of 27 files, one per entity. No domain grouping. Adding a new domain means adding more flat files. `main.py` imports 25 routers individually.
- **api-python** — `modules/transaction/` contains 13 entity-prefixed files (`fund_collection_router.py`, `fund_distribution_router.py`, …) instead of sub-folders per entity. Other modules (`bank/`, `coa/`, `petty_cash/`) exist as separate flat dirs with no domain parent.
- **report-api** — `modules/report/` is monolithic (all reports in one `service.py`). No domain separation.
- **URL surface** — completely flat: `/api/coa`, `/api/fund-collection`, `/api/authorization`. Domain and group context are invisible in the URL.

---

## 2. Goals

1. Reorganize all three services into `modules/{domain}/{group}/{entity}/` hierarchy
2. URL surface gains domain + group prefix: `/api/finance/master/coa`, `/api/finance/transaction/fund-collection`
3. Each entity is self-contained (router, service, schema, repo all in one folder)
4. `modules/transaction/` god-folder in api-python is eliminated
5. report-api gains domain structure for future multi-domain reports
6. Zero logic changes — pure structural + URL rename

---

## 3. Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| URL scheme | `/api/{domain}/{group}/{resource}` | Full semantic hierarchy; matches frontend sidebar groups |
| File grouping | One sub-folder per entity | Each entity owns its router/service/schema/repo |
| BFF module files | One file per group (e.g., `finance/transaction.py`) | Reduces file count; group = natural unit of change |
| Shared transaction utilities | `finance/transaction/_shared/` | `commit.py`, `parse.py`, `template.py`, `repository.py` are used by multiple transaction entities |
| Auth/tenants | `core/` — no domain prefix, URL unchanged | Auth is cross-cutting, not domain-specific |
| report-api | `modules/finance/reports/` + `modules/finance/dashboard/` | Prepares for future multi-domain reports |

---

## 4. URL Change Table (Complete)

### BFF — All URL changes (frontend-facing)

| Current URL prefix | New URL prefix | BFF file |
|---|---|---|
| `/api/auth` | `/api/auth` (unchanged) | `core/auth.py` |
| `/api/auth/google` | `/api/auth/google` (unchanged) | `core/auth_google.py` |
| `/api/tenants` | `/api/tenants` (unchanged) | `core/tenants.py` |
| `/api/dashboard` | `/api/finance/dashboard` | `finance/dashboard.py` |
| `/api/report` | `/api/finance/report` | `finance/reports.py` |
| `/api/coa` | `/api/finance/master/coa` | `finance/master.py` |
| `/api/bank` | `/api/finance/master/bank` | `finance/master.py` |
| `/api/petty-cash` | `/api/finance/master/petty-cash` | `finance/master.py` |
| `/api/parameter` | `/api/finance/master/parameter` | `finance/master.py` |
| `/api/budget` | `/api/finance/budget` | `finance/budget.py` |
| `/api/fund-collection` | `/api/finance/transaction/fund-collection` | `finance/transaction.py` |
| `/api/fund-distribution` | `/api/finance/transaction/fund-distribution` | `finance/transaction.py` |
| `/api/amil-income` | `/api/finance/transaction/amil-income` | `finance/transaction.py` |
| `/api/amil-expense` | `/api/finance/transaction/amil-expense` | `finance/transaction.py` |
| `/api/transaction/cash-advance` | `/api/finance/transaction/cash-advance` | `finance/transaction.py` |
| `/api/transaction/cash-advance-settlement` | `/api/finance/transaction/cash-advance-settlement` | `finance/transaction.py` |
| `/api/transaction/inter-account-transfer` | `/api/finance/transaction/inter-account-transfer` | `finance/transaction.py` |
| `/api/general-transaction` | `/api/finance/transaction/general` | `finance/transaction.py` |
| `/api/receivable` | `/api/finance/transaction/receivable` | `finance/transaction.py` |
| `/api/transaction` (batch upload) | `/api/finance/upload/collection` | `finance/upload.py` |
| `/api/transaction` (hc-zis) | `/api/finance/upload/hc-zis` | `finance/upload.py` |
| `/api/transaction-history` | `/api/finance/inquiry/transaction-history` | `finance/inquiry.py` |
| `/api/authorization` | `/api/finance/monitoring/authorization` | `finance/monitoring.py` |
| `/api/admin` | `/api/administration` | `administration/admin.py` |

---

## 5. api-python — Full Module Restructure

### Target structure

```
app/modules/
  finance/
    master/
      coa/          router.py  service.py  schema.py  export.py
      bank/         router.py  service.py  schema.py
      petty_cash/   router.py  service.py  schema.py
      parameter/    router.py  service.py  schema.py
    budget/         router.py  service.py  schema.py
    transaction/
      _shared/      commit.py  parse.py  template.py  repository.py
      fund_collection/         router.py  service.py  schema.py  repo.py
      fund_distribution/       router.py  service.py  schema.py  repo.py
      amil_income/             router.py  service.py  schema.py
      amil_expense/            router.py  service.py  schema.py
      cash_advance/            router.py  service.py  schema.py
      cash_advance_settlement/ router.py  service.py  schema.py
      inter_account_transfer/  router.py  service.py  schema.py
      general/                 router.py  service.py  schema.py
      receivable/              router.py  service.py  schema.py
    upload/
      collection/   router.py  service.py  schema.py  (batch upload)
      hc_zis/       router.py  service.py  schema.py  parse.py  commit.py
    inquiry/
      transaction_history/  router.py  service.py  schema.py  repo.py  export.py  delete.py
    monitoring/
      authorization/  router.py  service.py  schema.py  repo.py
    zakat/            router.py  service.py  schema.py  repo.py
    waqf/             router.py  service.py  schema.py  repo.py
  administration/
    router.py  service.py  schema.py
    identity/   router.py  service.py  schema.py
  fundraising/
    donors/     router.py  service.py  schema.py  repo.py
  shared/       db.py  config.py  response.py  (unchanged)
```

### File moves (from → to)

| From | To | Rename |
|---|---|---|
| `modules/coa/{router,service,schema,export}.py` | `modules/finance/master/coa/` | no rename |
| `modules/bank/{router,service,schema}.py` | `modules/finance/master/bank/` | no rename |
| `modules/petty_cash/{router,service,schema}.py` | `modules/finance/master/petty_cash/` | no rename |
| `modules/parameter/{router,service,schema}.py` | `modules/finance/master/parameter/` | no rename |
| `modules/budget/{router,service,schema}.py` | `modules/finance/budget/` | no rename |
| `modules/authorization/{router,service,schema,repo}.py` | `modules/finance/monitoring/authorization/` | no rename |
| `modules/transaction_history/*.py` | `modules/finance/inquiry/transaction_history/` | no rename |
| `modules/transaction/fund_collection_{router,service,schema,repo}.py` | `modules/finance/transaction/fund_collection/` | drop prefix: `fund_collection_` |
| `modules/transaction/fund_distribution_{router,service,schema,repo}.py` | `modules/finance/transaction/fund_distribution/` | drop prefix |
| `modules/transaction/amil_income_{router,service,schema}.py` | `modules/finance/transaction/amil_income/` | drop prefix |
| `modules/transaction/amil_expense_{router,service,schema}.py` | `modules/finance/transaction/amil_expense/` | drop prefix |
| `modules/transaction/cash_advance_{router,service,schema}.py` | `modules/finance/transaction/cash_advance/` | drop prefix |
| `modules/transaction/cash_advance_settlement_{router,service,schema}.py` | `modules/finance/transaction/cash_advance_settlement/` | drop prefix |
| `modules/transaction/inter_account_transfer_{router,service,schema}.py` | `modules/finance/transaction/inter_account_transfer/` | drop prefix |
| `modules/transaction/general_{router,service,schema}.py` | `modules/finance/transaction/general/` | drop prefix |
| `modules/transaction/receivable_{router,service,schema}.py` | `modules/finance/transaction/receivable/` | drop prefix |
| `modules/transaction/hc_zis_{router,service,schema,parse,commit}.py` | `modules/finance/upload/hc_zis/` | drop prefix |
| `modules/transaction/{router,service,schema}.py` (batch) | `modules/finance/upload/collection/` | no rename |
| `modules/transaction/{commit,parse,template,repository}.py` | `modules/finance/transaction/_shared/` | no rename |
| `modules/waqf/{router,service,schema,repo}.py` | `modules/finance/waqf/` | no rename |
| `modules/zakat/{router,service,schema,repo}.py` | `modules/finance/zakat/` | no rename |
| `modules/admin/{router,service,schema}.py` | `modules/administration/` | no rename |
| `modules/identity/{router,service,schema}.py` | `modules/administration/identity/` | no rename |
| `modules/donors/{router,service,schema,repo}.py` | `modules/fundraising/donors/` | no rename |

### URL prefix changes in api-python routers

Same hierarchy as BFF but without `/api` — api-python serves the BFF directly:

| Current router prefix | New router prefix |
|---|---|
| `/coa` | `/finance/master/coa` |
| `/bank` | `/finance/master/bank` |
| `/petty-cash` | `/finance/master/petty-cash` |
| `/parameter` | `/finance/master/parameter` |
| `/budget` | `/finance/budget` |
| `/fund-collection` | `/finance/transaction/fund-collection` |
| `/fund-distribution` | `/finance/transaction/fund-distribution` |
| `/amil-income` | `/finance/transaction/amil-income` |
| `/amil-expense` | `/finance/transaction/amil-expense` |
| `/transaction/cash-advance` | `/finance/transaction/cash-advance` |
| `/transaction/cash-advance-settlement` | `/finance/transaction/cash-advance-settlement` |
| `/transaction/inter-account-transfer` | `/finance/transaction/inter-account-transfer` |
| `/general-transaction` | `/finance/transaction/general` |
| `/receivable` | `/finance/transaction/receivable` |
| `/transaction` (batch) | `/finance/upload/collection` |
| `/transaction` (hc-zis routes) | `/finance/upload/hc-zis` |
| `/transaction-history` | `/finance/inquiry/transaction-history` |
| `/authorization` | `/finance/monitoring/authorization` |
| `/admin` | `/administration` |

### `main.py` — include pattern changes

```python
# Before
from app.modules.coa.router import router as coa_router
from app.modules.transaction.fund_collection_router import router as fund_collection_router

# After
from app.modules.finance.master.coa.router import router as coa_router
from app.modules.finance.transaction.fund_collection.router import router as fund_collection_router
```

---

## 6. BFF — Full Restructure

### Target structure

```
app/
  modules/
    core/
      auth.py         (was routers/auth.py)
      auth_google.py  (was routers/auth_google.py)
      tenants.py      (was routers/tenants.py)
    finance/
      master.py       (was: coa.py + bank.py + petty_cash.py + parameter.py)
      budget.py       (was: budget.py)
      transaction.py  (was: fund_collection.py + fund_distribution.py + amil_income.py +
                            amil_expense.py + cash_advance.py + cash_advance_settlement.py +
                            inter_account_transfer.py + general_transaction.py + receivable.py)
      upload.py       (was: transaction.py + hc_zis.py)
      inquiry.py      (was: transaction_history.py)
      monitoring.py   (was: authorization.py)
      reports.py      (was: report.py)
      dashboard.py    (was: dashboard.py)
      zakat.py        (was: zakat.py — if exists)
      waqf.py         (was: waqf.py — if exists)
    administration/
      admin.py        (was: admin.py)
    fundraising/
      donors.py       (was: donors.py — if exists)
  routers/ → deleted
```

### Merged files — structure inside each group file

Each merged BFF module file uses sub-routers with their own prefix:

```python
# finance/master.py
from fastapi import APIRouter

coa_router = APIRouter(prefix="/api/finance/master/coa")
bank_router = APIRouter(prefix="/api/finance/master/bank")
petty_cash_router = APIRouter(prefix="/api/finance/master/petty-cash")
parameter_router = APIRouter(prefix="/api/finance/master/parameter")

# All route functions from the 4 old files go here
# main.py includes all 4 sub-routers
```

### `main.py` import pattern

```python
# Before (25 individual imports)
from app.routers.coa import router as coa_router

# After (one import per module file, expose sub-routers)
from app.modules.finance.master import coa_router, bank_router, petty_cash_router, parameter_router
from app.modules.finance.transaction import (
    fund_collection_router, fund_distribution_router, ...
)
```

### BFF downstream call path changes

All `proxy.get()`/`proxy.post()` calls inside BFF routers that call api-python must match the new api-python URL prefixes:

```python
# Before
await proxy.get("/coa", ...)
await proxy.post("/fund-collection", ...)

# After
await proxy.get("/finance/master/coa", ...)
await proxy.post("/finance/transaction/fund-collection", ...)
```

---

## 7. report-api — Domain Grouping

### Target structure

```
app/modules/
  finance/
    reports/    router.py  service.py  schema.py  export.py
    dashboard/  router.py  service.py  schema.py
  shared/       db.py  config.py  response.py  (unchanged)
```

### URL changes (BFF proxy target)

| Current | New |
|---|---|
| `/report/*` (api-python call from BFF) | `/finance/report/*` |
| `/dashboard/*` | `/finance/dashboard/*` |

BFF `reports.py` proxy target URL also updates to `/finance/report/`.

---

## 8. Frontend — Call String Updates

All call strings in view files that go through the BFF must be updated. Pattern: grep all `GET(`, `POST(`, `blob(` calls in `apps_zakat/web-vue/src/` and replace prefixes per the URL table in §4.

Impact estimate: ~150 call strings across ~50 view files. All are mechanical grep-replace.

---

## 9. What Does NOT Change

- All business logic inside service/repo files
- Database query SQL
- Pydantic schemas (field names unchanged)
- Auth/session handling
- CORS, middleware configuration
- `shared/db.py`, `shared/config.py`, `shared/response.py`
- Named route names in Vue router
- `meta.menu_key` values
- BFF auth decorators (`require_session`, `require_menu`)

---

## 10. Wakaf Portal

Apply same restructure to `apps_wakaf/`. Wakaf has a simpler api-python (fewer transaction modules). Apply after zakat is verified green.

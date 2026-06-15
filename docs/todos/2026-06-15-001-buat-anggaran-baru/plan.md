# Plan: Buat Anggaran Baru (Budget Management)
**Dibuat**: 2026-06-15
**Target Portal**: zakat
**Reference**: 001-buat-anggaran-baru
**Kompleksitas**: TINGGI (8 tabel, 6 halaman, 16+ endpoint, maker-checker workflow)
**Estimasi**: 8-10 sprint days (parallel layers 1-3)

---

## Urutan Eksekusi

**Dependency flow**:
- Layer 1 (DB) → Layer 2 (API) → Layer 3 (BFF) → Layer 4 (Seed) → Layer 5 (UI) → Layer 6 (Test)
- Layers 2-3 bisa paralel jika schema sudah ready (layer 1 complete)
- Layer 4 (seed) harus after layer 3 (BFF routes define menu keys)

---

## Layer 1 — DB/DWH (nuwis-db-migrator, haiku)

**Status**: 8 tabel sudah ada di legacy schema. Migrasi = copy-paste existing DDL + adjust untuk isf-app conventions (CAST instead of ::, nullable fields, soft-delete columns, audit fields).

- [ ] `infra/db/migrations/V026_20260615__budget_create_tables.sql` 
  - Create `budget.budget` dengan fields: id, owner_id, period_id, budget_type, is_detail, created_date, created_by, updated_date, updated_by, deleted_date, deleted_by
  - Create `budget.budgetitem` (master + per-budget items): id, budget_id, item_code, item_name, level, parent_item_id, amount, amount_01...12, created_date, deleted_date
  - Create `budget.budgetitemhierarchy`: id, parent_item_id, child_item_id
  - Create `budget.budgetowner`: id, name, is_detail, created_date, deleted_date
  - Create `budget.budgetownerhierarchy`: id, parent_owner_id, child_owner_id
  - Create `budget.budgetperiod`: id, year, start_date, end_date, period_type, parent_period_id, is_active, created_date, deleted_date
  - Create `budget.budgetrevision`: id, budget_id, revision_number, revision_date, revision_by, notes
  - Create `budget.budgettransaction`: id, budget_id, transaction_id, item_id, amount, created_date
  - Add FKs, indexes on (owner_id, period_id), (parent_item_id), (parent_owner_id), (parent_period_id)
  - Add soft-delete check: `WHERE deleted_date IS NULL`

- [ ] `infra/db/migrations/V027_20260615__budget_alter_otorisasi.sql`
  - Ensure `otorisasi.submission.entity_type` supports value `'budget_import'`
  - Add to `otorisasi.entity_config` (if using per-entity dispatcher registry): entity_type='budget_import', limit=null (unlimited), action='IMPORT'

- [ ] `infra/db/migrations/dwh/v_budget_summary.sql`
  - Create `dwh.v_budget_summary` — aggregated budget by owner/period with item count and total amount
  - Used for dashboard / quick overview

- [ ] `infra/db/migrations/dwh/v_budget_inquiry.sql`
  - Create `dwh.v_budget_inquiry` — budget items with realisasi breakdown and variance calculation
  - Used for inquiry/laporan

**Apply order**:
```bash
# After Layer 1 complete, apply migrations to mziss_zakat
cd /home/wishnew/workshop/isf-app
psql -U transaction -d mziss_zakat -f infra/db/migrations/V026_20260615__budget_create_tables.sql
psql -U transaction -d mziss_zakat -f infra/db/migrations/V027_20260615__budget_alter_otorisasi.sql
psql -U transaction -d mziss_zakat -f infra/db/migrations/dwh/v_budget_summary.sql
psql -U transaction -d mziss_zakat -f infra/db/migrations/dwh/v_budget_inquiry.sql
```

---

## Layer 2 — Python API (nuwis-python-builder, haiku)

**Base path**: `apps_zakat/api-python/app/modules/budget/`

### Router & Service Structure

- [ ] `apps_zakat/api-python/app/modules/budget/__init__.py` — module init (empty or re-export router)

- [ ] `apps_zakat/api-python/app/modules/budget/router.py`
  - Endpoint group: `/api/budget/` (transaction routes)
  - Routes:
    - `GET /api/budget` — list budgets (pagination, filters)
    - `GET /api/budget/{id}` — detail budget with items
    - `GET /api/budget/{id}/items` — list items for budget
    - `GET /api/budget/{id}/transactions` — list realisasi transactions
    - `POST /api/budget/import` — upload Excel (multipart)
    - `PUT /api/budget/{id}/revise` — revise amount (bypass otorisasi)
    - `DELETE /api/budget/{id}` — soft-delete budget (bypass otorisasi)
    - `GET /api/budget/submission/{id}/approve` — approve submission (otorisasi callback)
    - `GET /api/budget/select/budget-owners` — dropdown helper
  - Auth decorators: `@require_menu("keuangan.anggaran.*")`

- [ ] `apps_zakat/api-python/app/modules/budget/service.py`
  - Class `BudgetService`:
    - `list_budgets(page, limit, owner_id, period_id, status)` → Pydantic list response
    - `get_budget(id)` → detail with nested items
    - `get_budget_items(budget_id)` → sorted by level, parent_item_id
    - `get_budget_transactions(budget_id)` → realisasi JOIN
    - `import_budget(file, owner_id, period_id)` → parse Excel, validate, return submission_id
    - `revise_budget_amount(budget_id, items: list[{item_id, amount}])` → direct UPDATE, increment revision_number
    - `delete_budget(budget_id)` → soft-delete
    - `get_budget_owners_dropdown(include_parent=False)` → filter is_detail or all
    - `create_budget_from_import(submission_id)` → dispatcher called by otorisasi async (background task)
  - Async methods: all service methods `async def` (use asyncpg pool)

- [ ] `apps_zakat/api-python/app/modules/budget/schema.py`
  - Pydantic models:
    - `BudgetItemSchema` (id, budget_id, item_code, item_name, level, parent_item_id, amount, created_date)
    - `BudgetSchema` (id, owner_id, owner_name, period_id, period_year, budget_type, is_detail, total_amount, item_count, status, created_date, created_by)
    - `BudgetDetailSchema` (BudgetSchema + items: list[BudgetItemSchema])
    - `BudgetOwnerSelectSchema` (id, name, is_detail)
    - `BudgetRevisionSchema` (id, budget_id, revision_number, revision_date, revision_by, notes)
    - `BudgetTransactionSchema` (id, transaction_id, item_id, item_name, amount, created_date)
    - `BudgetImportRequestSchema` (file: UploadFile, owner_id, period_id, description)
    - `BudgetImportResponseSchema` (submission_id, status, row_count, timestamp)
    - `BudgetReviseRequestSchema` (items: list[{item_id, amount}])
    - `BudgetInquirySchema` (budget_id, owner_name, period_year, item_id, item_code, item_name, budget_amount, realisasi_amount, variance, variance_percent, status)

- [ ] `apps_zakat/api-python/app/modules/budget/repo.py` (optional, if complex queries)
  - `select_budget_by_id(pool, budget_id)` → row with owner/period name JOINs
  - `select_budget_items_by_budget(pool, budget_id)` → list with parent_name resolution
  - `select_budget_inquiry(pool, filters)` → dwh.v_budget_inquiry with optional WHERE clauses

- [ ] Register router in `apps_zakat/api-python/app/main.py`:
  ```python
  from app.modules.budget.router import router as budget_router
  app.include_router(budget_router, prefix="/api", tags=["budget"])
  ```

### Parameter Routes (Master Data)

- [ ] `apps_zakat/api-python/app/modules/parameter/budget_owner_router.py` (or extend existing parameter router)
  - Routes:
    - `GET /api/parameter/budget/owners` — list (pagination)
    - `POST /api/parameter/budget/owners` — create
    - `PUT /api/parameter/budget/owners/{id}` — update
    - `DELETE /api/parameter/budget/owners/{id}` — soft-delete with constraint check
  - Auth: `@require_menu("parameter.anggaran.pemilik*")`

- [ ] `apps_zakat/api-python/app/modules/parameter/budget_item_router.py`
  - Routes:
    - `GET /api/parameter/budget/items` — list (pagination, parent_id filter)
    - `POST /api/parameter/budget/items` — create
    - `PUT /api/parameter/budget/items/{id}` — update
    - `DELETE /api/parameter/budget/items/{id}` — soft-delete with constraint check

- [ ] `apps_zakat/api-python/app/modules/parameter/budget_period_router.py`
  - Routes:
    - `GET /api/parameter/budget/periods` — list (year root only, pagination)
    - `POST /api/parameter/budget/periods` — create (auto-create months if flag)
    - `PUT /api/parameter/budget/periods/{id}` — update
    - `DELETE /api/parameter/budget/periods/{id}` — soft-delete with constraint check

### Excel Processing

- [ ] `apps_zakat/api-python/app/modules/budget/excel_parser.py`
  - Class `BudgetExcelParser`:
    - `parse(file: UploadFile) → list[dict]` — read xlsx, extract rows, validate schema (Item Code, Item Name, Amount)
    - `validate_rows(rows, owner_id, period_id) → (valid_rows, errors)` — check duplicates, FK, amount >= 0
  - Use `openpyxl` or `pandas` (check existing project convention)

### Dispatcher Registration

- [ ] Add to `apps_zakat/api-python/app/modules/otorisasi/service.py:_register_defaults()`:
  ```python
  register_dispatcher(
      entity_type='budget_import',
      dispatcher_func=BudgetService.create_budget_from_import,
      limit=None  # no limit; all imports go PENDING then background approval
  )
  ```

---

## Layer 3 — BFF (nuwis-bff-builder, haiku)

**Base path**: `apps_zakat/bff-api/app/routers/budget.py` + parameter extension

- [ ] `apps_zakat/bff-api/app/routers/budget.py`
  - Proxy routes to api-python:
    - `GET /api/budget` → proxy + handle pagination response shape
    - `GET /api/budget/{id}` → proxy
    - `POST /api/budget/import` → multipart proxy (stream form-data to api-python)
    - `PUT /api/budget/{id}/revise` → proxy
    - `DELETE /api/budget/{id}` → proxy
    - `GET /api/budget/submit/{id}/approve` → proxy + otorisasi callback
    - `GET /api/budget/select/budget-owners` → proxy
  - Auth: use `@require_menu()` decorators from isf-auth
  - Inject `inputer_id` + `branch_id` from session into headers or body

- [ ] Extend `apps_zakat/bff-api/app/routers/parameter.py` (or create new)
  - Proxy parameter routes:
    - `GET /api/parameter/budget/owners` → proxy
    - `POST /api/parameter/budget/owners` → proxy + auth
    - `PUT /api/parameter/budget/owners/{id}` → proxy + auth
    - `DELETE /api/parameter/budget/owners/{id}` → proxy + auth
    - (repeat for items and periods)

- [ ] Register routers in `apps_zakat/bff-api/app/main.py`:
  ```python
  from app.routers.budget import router as budget_router
  from app.routers.parameter import router as parameter_router
  app.include_router(budget_router)
  app.include_router(parameter_router)
  ```

---

## Layer 4 — Seed (nuwis-seed-gen, haiku)

**Target DB**: `isf_auth_zakat`

- [ ] `infra/db/migrations/seed/budget-menu-and-rolemenu.sql`
  - Insert into `isf_auth.menu`:
    - `keuangan.anggaran.import` (label: "Import Anggaran")
    - `keuangan.anggaran.revisi` (label: "Revisi Anggaran")
    - `keuangan.anggaran.inquiry` (label: "Inquiry Anggaran")
    - `parameter.anggaran.pemilik`, `.pemilik.tambah`, `.pemilik.ubah`, `.pemilik.hapus`
    - `parameter.anggaran.item`, `.item.tambah`, `.item.ubah`, `.item.hapus`
    - `parameter.anggaran.periode`, `.periode.tambah`, `.periode.ubah`, `.periode.hapus`
  - Insert into `isf_auth.role_menu`:
    - SPVKEU, ADMSYS → `keuangan.anggaran.*` (import, revisi, inquiry)
    - SPVDIST → `keuangan.anggaran.inquiry` (read-only)
    - ADMSYS → `parameter.anggaran.*` (full CRUD for all masters)

- [ ] `infra/db/migrations/seed/budget-initial-masters.sql`
  - Insert default `budget.budgetowner` entries (e.g., "Kepala Keuangan", "Koordinator", "Asisten")
  - Insert default `budget.budgetperiod` for 2024, 2025, 2026 (year root)
  - Insert master `budget.budgetitem` level-1 categories (e.g., "Operasional", "Investasi", "Lainnya")
  - Insert level-2 items under each category

- [ ] `infra/db/migrations/seed/budget-test-data.sql` (optional, for dev/demo)
  - Insert sample budgets for testing

**Apply order** (after Layer 3 BFF routes defined):
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/budget-menu-and-rolemenu.sql
psql -U transaction -d mziss_zakat -f infra/db/migrations/seed/budget-initial-masters.sql
psql -U transaction -d mziss_zakat -f infra/db/migrations/seed/budget-test-data.sql
```

---

## Layer 5 — UI (nuwis-ui-builder, haiku)

**Base path**: `apps_zakat/web-vue/src/pages/keuangan/`

### Main Transaction Pages

- [ ] `apps_zakat/web-vue/src/pages/keuangan/BudgetImportPage.vue`
  - Layout: form to select owner, period, upload Excel file
  - Fields:
    - Pemilik Anggaran (dropdown, `select/budget-owners`)
    - Periode Anggaran (dropdown, `select/budget-periods`)
    - File Excel (file input, accept .xlsx, .xls)
    - Keterangan (textarea, optional)
  - Button: "Unggah" (POST /api/budget/import)
  - On success: navigate to OtorisasiPage, toast "Upload berhasil, menunggu approval"
  - On error: show error toast with details
  - No pagination (single upload per visit)

- [ ] `apps_zakat/web-vue/src/pages/keuangan/BudgetRevisiPage.vue`
  - Layout: search + list + inline edit
  - Toolbar: SearchSelect for owner + period filters, "Cari" button
  - Table: paginated list of budgets (columns: owner, period, item_count, total_amount, status, actions)
  - Action "Detail" → open drawer showing BudgetDetailDrawer with items in nested list (level-1 → level-2)
  - In drawer: each item shows amount (editable), can change values
  - Button "Simpan Revisi" → PUT /api/budget/{id}/revise with item_amounts
  - On success: close drawer, refresh list, toast "Revisi berhasil"

- [ ] `apps_zakat/web-vue/src/pages/keuangan/BudgetInquiryPage.vue`
  - Layout: filter + table (report)
  - Toolbar: 
    - SearchSelect owner (optional)
    - SearchSelect period (optional, year root only)
    - SearchSelect item (optional, parent first, then child)
    - Button "Tampilkan"
  - Table: paginated, columns: Owner, Period, Item Code, Item Name, Budget Amount, Realisasi Amount, Variance, Variance %, Status
  - Button "Export" (post-design, if needed) → download as xlsx
  - Default state: empty, prompt "Pilih filter dan klik Tampilkan"

### Master Data Pages

- [ ] `apps_zakat/web-vue/src/pages/parameter/BudgetOwnerPage.vue`
  - CRUD table for `budget.budgetowner`
  - Toolbar: search input, "Tambah" button
  - Table: id, name, is_detail (badge), parent_name, created_date, actions (edit, delete)
  - Modal "Tambah/Ubah Pemilik Anggaran": form with fields: name, is_detail (checkbox), parent_id (SearchSelect, show only is_detail=false)
  - Constraint validation: if is_detail=true, parent required; if is_detail=false, parent optional
  - Delete: confirm modal with read-only detail form before delete
  - Pagination: top-placed standalone Paginator (default 25 rows)

- [ ] `apps_zakat/web-vue/src/pages/parameter/BudgetItemPage.vue`
  - CRUD table for `budget.budgetitem` (master items, not per-budget)
  - Toolbar: search, "Tambah" button
  - Table with expand icon for level-1 items → click expands to show level-2 children (nested structure, not separate pagination)
  - Or: standard flat list with level indicator, level-2 indented
  - Modal "Tambah/Ubah Item": form with fields: code, name, parent_id (SearchSelect, show only level-1), level (read-only, auto-set based on parent)
  - Delete: confirm before delete (with constraint check: "Cannot delete if used in active budgets")
  - Pagination: for level-1 items only; level-2 shown as children

- [ ] `apps_zakat/web-vue/src/pages/parameter/BudgetPeriodPage.vue`
  - CRUD table for `budget.budgetperiod` (year root only, parent_period_id IS NULL)
  - Toolbar: search, "Tambah" button
  - Table: year, start_date, end_date, is_active (toggle?), created_date, actions
  - Modal "Tambah/Ubah Periode": form with fields: year, start_date, end_date, create_months (checkbox, auto-create monthly periods)
  - Delete: confirm, constraint check "Cannot delete if budgets attached"
  - Pagination: top-placed

### Supporting Components

- [ ] `src/components/budget/BudgetDetailDrawer.vue` (reusable)
  - Props: `budget_id`, `budget_detail` (object)
  - Display budget header (owner, period, status)
  - Nested item list (level-1 with level-2 children shown below, indented)
  - If in edit mode (revisi): show amount inputs for each item
  - Action buttons: "Simpan Revisi", "Batal", or "Tutup" (based on mode)

- [ ] `src/components/budget/BudgetOwnerSelect.vue` (reusable SearchSelect wrapper)
  - Props: `model-value`, `label`, `placeholder`, `include-parent`
  - Fetch options from `GET /api/budget/select/budget-owners`
  - Emit `update:modelValue`

- [ ] `src/components/budget/BudgetItemSelect.vue` (similar)
  - Props: `model-value`, `label`, `parent-id` (optional, to filter children)
  - Hierarchical: show level-1, then level-2 under selection

### Router & Menu Registry

- [ ] Entry in `src/router/index.ts`:
  ```typescript
  {
    path: '/keuangan/budget/import',
    name: 'BudgetImport',
    component: () => import('@/pages/keuangan/BudgetImportPage.vue'),
    meta: { menu_key: 'keuangan.anggaran.import' }
  },
  {
    path: '/keuangan/budget/revisi',
    name: 'BudgetRevisi',
    component: () => import('@/pages/keuangan/BudgetRevisiPage.vue'),
    meta: { menu_key: 'keuangan.anggaran.revisi' }
  },
  {
    path: '/keuangan/budget/inquiry',
    name: 'BudgetInquiry',
    component: () => import('@/pages/keuangan/BudgetInquiryPage.vue'),
    meta: { menu_key: 'keuangan.anggaran.inquiry' }
  },
  {
    path: '/parameter/budget/owner',
    name: 'BudgetOwner',
    component: () => import('@/pages/parameter/BudgetOwnerPage.vue'),
    meta: { menu_key: 'parameter.anggaran.pemilik' }
  },
  // ... items, periods similarly
  ```

- [ ] Entry in `src/lib/menu/registry.ts`:
  ```typescript
  export const MENU_KEYS = {
    // ... existing
    'keuangan.anggaran': {
      label: 'Anggaran',
      children: {
        'keuangan.anggaran.import': { label: 'Import Anggaran' },
        'keuangan.anggaran.revisi': { label: 'Revisi Anggaran' },
        'keuangan.anggaran.inquiry': { label: 'Inquiry Anggaran' },
      }
    },
    'parameter.anggaran': {
      label: 'Anggaran',
      children: {
        'parameter.anggaran.pemilik': { label: 'Master Pemilik Anggaran' },
        'parameter.anggaran.item': { label: 'Master Item Anggaran' },
        'parameter.anggaran.periode': { label: 'Master Periode Anggaran' },
      }
    },
  } satisfies MenuRegistry;
  ```

- [ ] Update `src/components/AppSidebar.vue`:
  - Add menu group "Anggaran" under "Keuangan" (if not already visible)
  - Add items: "Import Anggaran", "Revisi Anggaran", "Inquiry Anggaran"
  - (Parameter masters: already under "Parameter" → "Anggaran")

---

## Layer 6 — Test (nuwis-test-gen, haiku)

- [ ] `testing/e2e-budget-import.sh`
  - Smoke test: upload Excel file, verify submission created, approve, verify import
  - Setup: create budget owner, period, item categories
  - Test cases:
    1. Upload valid Excel → verify submission_id, status='PENDING'
    2. Approve submission → verify status='PROCESSING' then 'AUTHORIZED' (with polling)
    3. Verify budgets created in DB
  - Cleanup: delete test data

- [ ] `testing/e2e-budget-revise.sh`
  - Test: revise budget amounts
  - Setup: import a budget first (or seed test budget)
  - Test cases:
    1. GET budget detail → verify items
    2. PUT revise with new amounts → verify revision_number incremented
    3. Verify amounts updated in DB

- [ ] `testing/e2e-budget-inquiry.sh`
  - Test: inquiry with filters
  - Setup: seed budget + transactions (realisasi)
  - Test cases:
    1. GET inquiry no filters → verify response shape
    2. GET inquiry with owner_id → verify filtered rows
    3. Verify variance calculation (budget_amount - realisasi_amount)

- [ ] `testing/e2e-budget-master.sh`
  - Test: CRUD master data (owners, items, periods)
  - Test cases:
    1. POST owner → verify created
    2. PUT owner → verify updated
    3. DELETE owner (fail if has budgets, success if orphan)
    4. Repeat for items, periods

- [ ] `apps_zakat/api-python/tests/test_budget.py` (pytest unit tests)
  - Test BudgetService methods: list, get, import, revise, delete
  - Test Excel parser: validate schema, duplicates, FK constraints
  - Test permission checks (menu key auth)
  - Fixture: test DB with sample data

---

## Verifikasi & Integration

### Pre-Deploy Checklist

- [ ] All migrations applied to both test + prod `mziss_zakat` and `isf_auth_zakat`
  ```bash
  cd /home/wishnew/workshop/isf-app/infra
  
  # Layer 1
  psql -U transaction -d mziss_zakat -f db/migrations/V026_20260615__budget_create_tables.sql
  psql -U transaction -d mziss_zakat -f db/migrations/V027_20260615__budget_alter_otorisasi.sql
  psql -U transaction -d mziss_zakat -f db/migrations/dwh/v_budget_summary.sql
  psql -U transaction -d mziss_zakat -f db/migrations/dwh/v_budget_inquiry.sql
  
  # Layer 4
  psql -U transaction -d isf_auth_zakat -f db/migrations/seed/budget-menu-and-rolemenu.sql
  psql -U transaction -d mziss_zakat -f db/migrations/seed/budget-initial-masters.sql
  ```

### Manual Testing (QA)

- [ ] Start containers (all 3 services: api-python, bff-api, web-vue)
  ```bash
  cd /home/wishnew/workshop/isf-app/infra
  podman-compose -f docker-compose.zakat.yml up -d
  ```

- [ ] Wait for services ready (check logs)
  ```bash
  podman-compose -f docker-compose.zakat.yml logs -f api-python bff-api web-vue
  ```

- [ ] Login as SPVKEU (Supervisor Keuangan) with password `test1234`
  - User should see menu "Keuangan" → "Anggaran" → "Import Anggaran", "Revisi Anggaran", "Inquiry Anggaran"

- [ ] Test Import Anggaran flow
  - Navigate to "Import Anggaran"
  - Select Pemilik, Periode
  - Upload sample Excel (use template with headers: Item Code, Item Name, Amount)
  - Verify: toast "Upload berhasil", redirects to Otorisasi page
  - In Otorisasi page, verify submission appears with status PENDING
  - Click "Otorisasi" → approve submission
  - Wait (auto-refresh) for status → PROCESSING → AUTHORIZED
  - Check DB: verify `budget.budget` and `budget.budgetitem` rows created

- [ ] Test Revisi Anggaran flow
  - Navigate to "Revisi Anggaran"
  - Search/filter for the imported budget
  - Click "Detail" → drawer shows items with amounts
  - Edit an amount
  - Click "Simpan Revisi"
  - Verify: toast success, drawer closes, list refreshes
  - Check DB: verify `budget.budgetrevision` row created, amounts updated

- [ ] Test Inquiry Anggaran flow
  - Navigate to "Inquiry Anggaran"
  - Set filters (owner, period, item)
  - Click "Tampilkan"
  - Verify: table shows rows with budget_amount, realisasi_amount, variance
  - If realisasi data exists (from seed), verify variance calculation

- [ ] Test Master Data CRUD (Parameter)
  - Login as ADMSYS (Admin)
  - Navigate to "Parameter" → "Anggaran" → "Master Pemilik Anggaran"
  - Test: Create new owner, update, delete (with constraint check)
  - Verify: list refreshes, confirm modal shows before delete

- [ ] Browser console: check for JavaScript errors (none expected)

- [ ] Postman / curl: test API endpoints directly (if time permits)
  ```bash
  # Example: import
  curl -X POST http://localhost:7000/api/budget/import \
    -H "Authorization: Bearer <token>" \
    -F "file=@sample.xlsx" \
    -F "owner_id=10" \
    -F "period_id=5"
  
  # Example: list
  curl -X GET http://localhost:7000/api/budget?page=1&limit=25 \
    -H "Authorization: Bearer <token>"
  ```

### Post-Deploy

- [ ] Run E2E scripts in order
  ```bash
  bash testing/e2e-budget-import.sh
  bash testing/e2e-budget-revise.sh
  bash testing/e2e-budget-inquiry.sh
  bash testing/e2e-budget-master.sh
  ```

- [ ] All scripts pass (exit code 0)

- [ ] No error logs in containers:
  ```bash
  podman-compose -f docker-compose.zakat.yml logs --tail=100 | grep -i error
  ```

- [ ] Database integrity check (no orphaned FKs, soft-delete flags correct)
  ```sql
  -- Check for orphaned budget.budgetitem entries
  SELECT COUNT(*) FROM budget.budgetitem WHERE budget_id IS NOT NULL AND budget_id NOT IN (SELECT id FROM budget.budget WHERE deleted_date IS NULL);
  
  -- Verify no active budgets with deleted items
  SELECT COUNT(*) FROM budget.budgetitem WHERE deleted_date IS NOT NULL AND budget_id IN (SELECT id FROM budget.budget WHERE deleted_date IS NULL);
  ```

---

## Estimated Sprint Breakdown

| Layer | Task | Est. Hours | Parallel? |
|---|---|---|---|
| 1 | DB migrations (8 tables + DWH) | 4 | no |
| 2 | Python API (router + service + schema + excel parser) | 6 | yes (after L1) |
| 3 | BFF proxy routes | 3 | yes (parallel with L2) |
| 4 | Seed SQL (menu + role_menu + initial data) | 2 | no (after L3) |
| 5 | Vue pages (6 pages + components + router entries) | 8 | yes (parallel with L2-3) |
| 6 | E2E tests + pytest | 3 | no (after L5) |
| **Total** | | **26 hrs** | ~10 sprint days |

**Recommended order**:
1. Day 1: Complete Layer 1 (DB) → quick manual validation
2. Days 2-3: Parallel L2 (API) + L5 (UI stub/skeleton)
3. Days 4-5: Parallel L3 (BFF) + L5 (complete UI)
4. Day 6: Layer 4 (Seed) → integrate with layers 2-3
5. Days 7-8: Layer 6 (Test) + manual QA
6. Days 9-10: Bug fixes, refinements, go-live prep

---

## Known Risks & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Revisi/Delete bypass otorisasi (inconsistent with CREATE) | Audit trail gap | Document in code, add ADR, plan v2 refactoring |
| Hierarki 2-level (item parent_id) + budget items overlap | Complex query logic | Keep simple for v1, test FK constraints, plan normalization |
| Monthly breakdown columns inactive (amount_01...12) | Confusion during dev | Add TODO comments in schema, skip UI logic for now |
| Excel import can be slow (5000+ rows) | UX timeout | Background async processing via otorisasi.submission (existing pattern) |
| Realisasi calculation via budgettransaction join | May miss edge cases | Verify with legacy DAF behavior, add test data with realisasi |

---

## Next Steps (Post-Go-Live)

- [ ] ADR-001: Decide on revisi/delete otorisasi inconsistency → v2 refactoring
- [ ] ADR-002: Consider BudgetYear subclass inheritance → future refactor
- [ ] ADR-003: Consider separate tables for item categories vs details → future refactor
- [ ] Activate monthly breakdown (amount_01...12) → new feature request
- [ ] Laporan anggaran (dwh.v_budget_summary → MkDocs + export) → next sprint
- [ ] Mobile-responsive UI polish → UX review


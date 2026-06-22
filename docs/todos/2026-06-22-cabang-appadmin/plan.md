# Plan: Manajemen Cabang

**Dibuat:** 2026-06-22
**Target Portal:** zakat
**Domain:** appadmin (Pengaturan Akses)
**Feature Type:** CRUD (List, Create, Edit, Toggle Status, Detail)

---

## Ringkasan Feature

Implementasi CRUD Manajemen Cabang di isf-app untuk menggantikan legacy DAF enterprise.cabang UI.
Fitur mencakup:
- List cabang dengan filter status_aktif + keyword search
- Create cabang baru dengan validasi kode unik + auto-set status
- Edit cabang (kode readonly)
- Detail view (read-only)
- Toggle status (activate/deactivate)

**Scope awal:** CRUD master data cabang saja.
**Out of scope (sprint berikutnya):** Tab GL Interface & Limit Operasi (TabVisible=false di legacy), GenerateInstanceByBranch cross-service call (investigasi terpisah).

---

## Urutan Eksekusi

Layer 1 (DB) dan Layer 2 (Python API) dapat berjalan paralel jika verifikasi schema sudah selesai.

---

## Layer 1 — DB/DWH (nuwis-db-migrator)

**Prioritas:** HIGH — harus selesai terlebih dahulu sebelum implementasi API.

### Checklist

- [ ] **Verifikasi Tabel Existing:**
  - File: `infra/db/migrations/` (cek apakah ada migrationVerifying enterprise.cabang structure
  - Tugas: `SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='enterprise' AND table_name='cabang' ORDER BY ordinal_position;`
  - Output: Dokumentasi kolom aktual vs specs.md. Jika ada mismatch, tentukan apakah perlu migration atau hanya docs.

- [ ] **Migration (jika ada delta):**
  - File: `infra/db/migrations/V{NNN}__add_missing_branch_columns.sql` (jika perlu)
  - Isi: ALTER TABLE enterprise.cabang ADD COLUMN (jika ada kolom missing di actual schema)
  - Pattern: Harus menggunakan CAST(x AS type), bukan x::type
  - Verify: Semua kolom di specs "Kolom kunci" ada di tabel

- [ ] **Constraints & Indexes:**
  - PK: kode_cabang (CHAR/VARCHAR(20), not null)
  - FK: kode_cabang_induk → kode_cabang (self-ref, allow null)
  - FK: kode_wilayah → enterprise.areacabang.kode_wilayah (allow null)
  - Unique: kode_cabang
  - Index: status_aktif (untuk filter list)
  - Check constraint: tipe_cabang IN ('CP', 'CU', 'GM', 'KS', 'NO', 'PO')
  - Check constraint: status_cabang IN ('B', 'S')

- [ ] **No DWH View Needed (bukan laporan)**
  - Manajemen Cabang adalah master data CRUD, bukan report
  - DWH view hanya jika ada laporan yang memerlukan enterprise.cabang join

---

## Layer 2 — Python API (nuwis-python-builder)

**Prioritas:** HIGH — core business logic.

### Checklist — Module Structure

- [ ] `apps_zakat/api-python/app/modules/appadmin/__init__.py`
  - Buat folder `modules/appadmin/` jika belum ada
  - File __init__.py: kosong atau `# appadmin module`

- [ ] `apps_zakat/api-python/app/modules/appadmin/router.py`
  - Import: FastAPI, get_pool, require_menu, _resolve_branch
  - Endpoints:
    - GET /api/appadmin/branches — list dengan filter
    - POST /api/appadmin/branches — create
    - GET /api/appadmin/branches/{branch_code} — detail
    - PUT /api/appadmin/branches/{branch_code} — edit
    - PATCH /api/appadmin/branches/{branch_code}/deactivate — deactivate
    - PATCH /api/appadmin/branches/{branch_code}/activate — activate
    - GET /api/appadmin/branches/check-code/{branch_code} — check unique code

- [ ] `apps_zakat/api-python/app/modules/appadmin/service.py`
  - Class: BranchService
  - Methods:
    - list_branches(pool, status_aktif, keyword, page, limit) → Tuple[List[dict], int]
    - create_branch(pool, user_id, payload) → dict (dengan auto fields)
    - get_branch(pool, branch_code) → dict
    - update_branch(pool, branch_code, payload) → dict
    - deactivate_branch(pool, branch_code) → dict
    - activate_branch(pool, branch_code) → dict
    - check_code_exists(pool, branch_code) → bool
  - Validasi:
    - kode_cabang: required, unique (via check_code_exists)
    - nama_cabang: required, max 30 char
    - tipe_cabang: required, IN ('CP', 'CU', 'GM', 'KS', 'NO', 'PO')
    - status_cabang: auto dari tipe_cabang (tidak user-input)
    - kode_cabang_induk: validasi jika status_cabang='S' (must exist di tabel)
    - Circular reference check: A → B → A (prevention)
  - Auto-set fields:
    - status_aktif = 'T' (create)
    - status_otorisasi = '1' (create)
    - status_akses = 'O' (create)
    - status_cabang dari tipe_cabang (create & update)
    - user_input = user_id dari session
    - tanggal_input = today (create)
    - terminal_input = dari header atau default

- [ ] `apps_zakat/api-python/app/modules/appadmin/schema.py`
  - Pydantic models:
    - BranchListItem (kode_cabang, nama_cabang, tipe_cabang, status_cabang, cabang_induk, kantor_nama, status_aktif, zona_waktu)
    - BranchDetail (semua field dari DB)
    - BranchCreateRequest (kode_cabang, nama_cabang, tipe_cabang, kantor_* fields, zona_waktu optional)
    - BranchUpdateRequest (nama_cabang, kantor_* fields, kode_cabang_induk optional)
    - BranchResponse (data: BranchDetail)
    - BranchListResponse (data: List[BranchListItem], pagination)
    - CodeCheckResponse (data: {exists: bool, message: str})

- [ ] `apps_zakat/api-python/app/modules/appadmin/repo.py` (jika ada query kompleks)
  - Optional file jika service.py queries terlalu kompleks
  - Methods: sama dengan service, tapi tugas DB query saja

- [ ] Daftarkan router di `apps_zakat/api-python/app/main.py`
  - Import: `from app.modules.appadmin import router`
  - Tambah: `app.include_router(router.router, prefix='/api/appadmin', tags=['appadmin'])`

### Checklist — Dependencies & Utilities

- [ ] Koneksi database:
  - Pakai asyncpg pool dari main.py (get_pool())
  - Pattern: async with pool.acquire() as conn

- [ ] Auth decorators:
  - @require_menu("appadmin.branch.list") untuk GET list
  - @require_menu("appadmin.branch.create") untuk POST
  - @require_menu("appadmin.branch.edit") untuk PUT
  - @require_menu("appadmin.branch.toggle-status") untuk PATCH
  - @require_menu("appadmin.branch.detail") untuk GET detail

- [ ] Session injection:
  - user_id dari JWT token atau session context
  - branch_id (primary) dari session (untuk audit trail)
  - terminal_input: optional, default ke hostname atau "isf-app"

---

## Layer 3 — BFF (nuwis-bff-builder)

**Prioritas:** MEDIUM — proxy + auth layer.

### Checklist

- [ ] `apps_zakat/bff-api/app/routers/appadmin.py`
  - Import: FastAPI, HTTPException, require_menu, _resolve_branch
  - Endpoints (proxy ke api-python):
    - GET /api/appadmin/branches
    - POST /api/appadmin/branches
    - GET /api/appadmin/branches/{branch_code}
    - PUT /api/appadmin/branches/{branch_code}
    - PATCH /api/appadmin/branches/{branch_code}/deactivate
    - PATCH /api/appadmin/branches/{branch_code}/activate
    - GET /api/appadmin/branches/check-code/{branch_code}
  - Pattern: `await self.api_client.get(f'/api/appadmin/branches', params=...)`
  - Auth: @require_menu per endpoint
  - Branch resolution: _resolve_branch untuk create/update (inject primary branch)

- [ ] Daftarkan router di `apps_zakat/bff-api/app/main.py`
  - Import: `from app.routers import appadmin`
  - Tambah: `app.include_router(appadmin.router, prefix='/api', tags=['appadmin'])`

### Notes BFF

- List endpoint tidak perlu branch filter (cabang adalah master data shared)
- Create/edit memerlukan audit fields (user_id, branch_id dari session) — BFF pass via header ke api-python

---

## Layer 4 — Seed (nuwis-seed-gen)

**Prioritas:** HIGH — menu keys wajib ada sebelum UI testing.

### Checklist

- [ ] `infra/db/migrations/seed/{YYYYMMDD}-menu-cabang-appadmin.sql`
  - Target DB: isf_auth_zakat
  - Isi:
    - INSERT INTO isf_auth.menu (menu_key, menu_name, parent_key, icon, order_num, is_active)
      - appadmin.branch.list — "Inquiry Cabang" — parent: appadmin.branch — icon: lucide-icon
      - appadmin.branch.create — "Input Data Cabang Baru" — parent: appadmin.branch
      - appadmin.branch.edit — "Koreksi Data Cabang" — parent: appadmin.branch
      - appadmin.branch.detail — "Lihat Data Cabang" — parent: appadmin.branch
      - appadmin.branch.toggle-status — "Kelola Status Cabang" — parent: appadmin.branch
    - INSERT INTO isf_auth.role_menu (role_id, menu_key) — assign ke role ADMIN (atau check role_id di isf_auth_zakat)

- [ ] Verifikasi 3-way consistency:
  - Seed SQL: menu keys yang di-insert
  - Registry: shared/constants/menu-keys.ts di web-vue (MENU_KEYS object)
  - Route: Vue route meta.menu_key harus match
  - Jika ada mismatch, update seed atau docs

- [ ] Apply seed:
  ```bash
  psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/{YYYYMMDD}-menu-cabang-appadmin.sql
  ```

---

## Layer 5 — UI (nuwis-ui-builder)

**Prioritas:** MEDIUM — frontend implementation.

### Checklist

- [ ] `apps_zakat/web-vue/src/modules/appadmin/views/BranchPage.vue`
  - Layout: 3-part (Toolbar | Pagination | DataTable)
  - Toolbar:
    - Status filter dropdown (ALL, Aktif, Tidak Aktif)
    - Keyword search input
    - Button "Tambah Cabang"
  - Pagination: standalone Paginator above table, default 25 rows
  - DataTable (lazy, no built-in paginator):
    - Columns: kode_cabang, nama_cabang, cabang_induk, kantor_nama, status_aktif, zona_waktu
    - Row actions: View, Edit, Deactivate/Activate (kondisional)
  - Modals:
    - CreateBranchModal.vue (form create)
    - EditBranchModal.vue (form edit, kode readonly)
    - DetailBranchModal.vue (read-only view)

- [ ] Form components:
  - CreateBranchModal.vue:
    - Fields: kode_cabang (required, async validation via check-code), nama_cabang, tipe_cabang (dropdown), kantor_* fields
    - Conditional: kode_cabang_induk (visible hanya jika tipe_cabang='S', dropdown cabang utama)
    - Buttons: Simpan, Batal
    - Toast feedback: success/error
  - EditBranchModal.vue:
    - Load: GET /api/appadmin/branches/{branch_code}
    - Fields: kode_cabang (readonly), nama_cabang, kantor_* fields, kode_cabang_induk (conditional)
    - Buttons: Simpan, Batal
  - DetailBranchModal.vue:
    - Read-only display
    - Show: All fields termasuk status_aktif, user_input, tanggal_input, terminal_input (audit trail)

- [ ] API client usage:
  - `GET()`, `POST()`, `PUT()`, `PATCH()` dari shared/api/client.ts
  - Base URL: VITE_API_BASE_URL (bff-api)
  - Handle error codes: UNAUTHORIZED (redirect), MENU_DENIED (alert), VALIDATION_ERROR (field-level)

- [ ] Routing:
  - Entry di `apps_zakat/web-vue/src/router/index.ts`
  - Route path: `/appadmin/branches`
  - Meta: `menu_key: "appadmin.branch.list"`, `domain: "appadmin"`
  - Guard: beforeEach check menu access

- [ ] Menu registry:
  - Tambah ke `apps_zakat/web-vue/src/shared/constants/menu-keys.ts`
    ```ts
    export const MENU_KEYS = {
      APPADMIN: {
        BRANCH: {
          LIST: 'appadmin.branch.list',
          CREATE: 'appadmin.branch.create',
          EDIT: 'appadmin.branch.edit',
          DETAIL: 'appadmin.branch.detail',
          TOGGLE_STATUS: 'appadmin.branch.toggle-status',
        }
      }
    }
    ```

- [ ] Sidebar entry:
  - Daftarkan di `apps_zakat/web-vue/src/modules/appadmin/menu.ts` (DomainConfig)
  - Menu group: "Manajemen Data" atau "Data Master"
  - Child items:
    - "Inquiry Cabang" → link: `/appadmin/branches`, menu_key: appadmin.branch.list
    - "Input Data Cabang Baru" → action: open create modal, menu_key: appadmin.branch.create (hidden, akses via Inquiry)
    - "Koreksi Data Cabang" → action: edit selected, menu_key: appadmin.branch.edit (hidden, akses via context menu)

### UI Conventions (Non-negotiable)

- Pagination: ALWAYS standalone `<Paginator>` above table, default rows_per_page=25
- Date display: use dmy() dari shared/utils/date.ts (format DD-MM-YYYY)
- Date input: use DateField.vue v-model (store ISO internally)
- Dropdown dengan banyak items: use SearchSelect.vue (tidak DataTable combobox)
- Delete flow: modal dengan read-only data + confirm, bukan inline confirm
- Async feedback: loading state + success toast + error toast + finally reset
- Styling: Tailwind v4 classes only (no inline style), reka-ui + PrimeVue unstyled, Lucide icons
- Icons: Lucide (e.g., lucide-plus, lucide-pencil, lucide-trash2)

---

## Layer 6 — Testing (nuwis-test-gen)

**Prioritas:** MEDIUM — E2E + optional unit tests.

### Checklist

- [ ] `testing/e2e-branch-appadmin.sh`
  - E2E smoke test script (curl-based)
  - Cases:
    1. Login (bfi auth endpoint)
    2. GET /api/appadmin/branches (list, status_aktif=T)
    3. GET /api/appadmin/branches/check-code/999 (check code doesn't exist)
    4. POST /api/appadmin/branches (create new branch)
    5. GET /api/appadmin/branches/{code} (detail)
    6. PUT /api/appadmin/branches/{code} (edit)
    7. PATCH /api/appadmin/branches/{code}/deactivate (deactivate)
    8. PATCH /api/appadmin/branches/{code}/activate (activate)
    9. Verify response shapes (data, pagination, meta)
  - Target: localhost ports (5173 for web-vue, 7000 for bff-api, 8000 for api-python)

- [ ] `apps_zakat/api-python/tests/test_appadmin_branch.py` (optional, kompleks logic)
  - Unit tests jika ada validasi kompleks (circular reference, status_cabang auto-set, dll)
  - Pakai pytest + asyncpg test fixture

### Run E2E

```bash
# Setelah semua layer selesai, restart container
cd infra && podman-compose -f docker-compose.zakat.yml down
podman-compose -f docker-compose.zakat.yml up -d

# Jalankan E2E
bash testing/e2e-branch-appadmin.sh
```

---

## Verification Checklist (Pre-launch)

- [ ] Database:
  - [ ] Tabel enterprise.cabang verified (schema match specs)
  - [ ] Constraints & indexes in place
  - [ ] Sample data (minimal 3 cabang: 1 utama, 2 pembantu)

- [ ] API (api-python):
  - [ ] All 7 endpoints implemented + tested (curl)
  - [ ] Validasi: unique code, required fields, circular ref prevention
  - [ ] Auto-set fields: status_aktif='T', status_akses='O', status_cabang dari tipe
  - [ ] Auth decorators: @require_menu per endpoint
  - [ ] Error responses: 400 (validation), 403 (menu denied), 404 (not found), 500 (server error)

- [ ] BFF (bff-api):
  - [ ] All endpoints proxy correctly
  - [ ] Session injection: user_id, branch_id dari auth context
  - [ ] Auth: @require_menu propagates to api-python

- [ ] UI (web-vue):
  - [ ] List page loads dengan data
  - [ ] Create form validates + submit
  - [ ] Edit form loads + update
  - [ ] Detail modal read-only
  - [ ] Toggle status (activate/deactivate)
  - [ ] Filter status_aktif + search keyword works
  - [ ] Pagination (top-placed, standalone)
  - [ ] Error handling: show toast on failure
  - [ ] Menu keys registered + sidebar entry visible (ADMIN role)

- [ ] Seed:
  - [ ] Menu SQL applied to isf_auth_zakat
  - [ ] Menu keys match registry.ts + route meta.menu_key
  - [ ] Role ADMIN has access to appadmin.branch.* keys

- [ ] E2E:
  - [ ] testing/e2e-branch-appadmin.sh passed
  - [ ] Manual browser test: login → navigate → CRUD flow works

---

## Implementation Notes

### Critical Dependencies

1. **GenerateInstanceByBranch Cross-Service Call:**
   - Legacy melakukan rexecscript saat create branch
   - **Status: PENDING INVESTIGATION**
   - Awal implementasi: SKIP cross-service call, fokus CRUD cabang saja
   - Jika diperlukan, bisa ditambah di sprint berikutnya setelah analisis
   - Koordinasi dengan nuwis-architect untuk investigasi

2. **Circular Reference Prevention:**
   - Saat create/edit kode_cabang_induk, cegah A → B → A
   - Algoritma: traverse parent chain ke atas, pastikan kode_cabang tidak ada di chain
   - Implementasi: di service.py validate_parent_branch()

3. **Schema Verification is Prerequisite:**
   - Layer 1 HARUS selesai terlebih dahulu
   - Jika ada kolom missing atau mismatch, bisa block API implementation
   - Timeline: 1-2 hari untuk verifikasi + migration (jika ada)

### Out of Scope (Deferred)

- **Tab GL Interface:** Edit enterprise.glinterface per cabang (hidden di legacy, TabVisible=false)
- **Tab Limit Operasi:** Edit enterprise.limitoperasi per cabang (hidden di legacy)
- Kedua tab bisa diimplementasi di sprint berikutnya jika ada business requirement

### Estimated Timeline

| Layer | Duration | Start | End |
|---|---|---|---|
| Layer 1 (DB) | 1-2 days | Day 1 | Day 2 |
| Layer 2 (API-Python) | 2-3 days | Day 2 | Day 4 |
| Layer 3 (BFF) | 1 day | Day 4 | Day 5 |
| Layer 4 (Seed) | 0.5 day | Day 5 | Day 5 |
| Layer 5 (UI) | 2-3 days | Day 3 (parallel) | Day 5 |
| Layer 6 (Testing) | 1 day | Day 5 | Day 6 |
| **Total** | **~6-7 days** | | |

*Note: Layer 2 & 5 dapat berjalan paralel setelah Layer 1 selesai.*

---

## Command References

### Apply DB Migration (jika ada)
```bash
psql -U transaction -d mziss_zakat -f infra/db/migrations/V{NNN}__add_missing_branch_columns.sql
```

### Apply Seed Menu
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/{YYYYMMDD}-menu-cabang-appadmin.sql
```

### Run E2E Script
```bash
bash testing/e2e-branch-appadmin.sh
```

### Restart App Services
```bash
cd infra
podman-compose -f docker-compose.zakat.yml down
podman-compose -f docker-compose.zakat.yml up -d
# Wait for services to be healthy
sleep 10
curl http://localhost:5173  # web-vue
curl http://localhost:7000/health  # bff-api
curl http://localhost:8000/health  # api-python
```

---

## Links to Specs & Supporting Docs

- **Specs:** /home/wishnew/workshop/isf-app/docs/todos/2026-06-22-cabang-appadmin/specs.md
- **Migration Analysis:** /home/wishnew/workshop/isf-app/docs/todos/2026-06-22-cabang-appadmin/MIGRATION_ANALYSIS.md
- **Legacy Enterprise:** /home/wishnew/workshop/isf-app/docs/legacy-apps/enterprise/
- **isf-app CLAUDE.md:** /home/wishnew/workshop/isf-app/CLAUDE.md
- **Menu Registry:** shared/constants/menu-keys.ts
- **Auth Module:** apps_zakat/api-python/app/modules/appadmin/

---

## Questions & Escalations

### For nuwis-architect
1. GenerateInstanceByBranch — apakah perlu di-implement atau bisa skip?
2. Dropdown cabang_induk — hanya cabang utama (status_cabang='B') atau ada batasan lain?
3. enterprise.cabang shared di kedua portal atau per-portal? (affects seed strategy)

### For Database Team (if applicable)
- Verifikasi kolom tabel enterprise.cabang di production mziss_zakat vs specs.md
- Backup tabel sebelum migration (jika ada ALTER)

---

## Related Issues / PRs (to be filled post-implementation)

- [ ] Migration PR: DB layer
- [ ] Feature PR: API-Python + BFF + UI + Seed
- [ ] Testing PR: E2E script

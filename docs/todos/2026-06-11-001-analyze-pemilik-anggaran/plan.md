# Plan: Pemilik Anggaran (Budget Owner)
**Dibuat**: 2026-06-11  
**Target Portal**: Zakat + Wakaf (dual)

---

## Urutan Eksekusi

**Layer 0 dan 1 bisa paralel** jika migration SQL sudah stabil.
**Layer 2 (BFF) bergantung ke Layer 1 (Python API).**
**Layer 3 (UI) baru dimulai setelah Layer 2 siap.**
**Layer 4 (Seed) & Layer 5 (Test) bisa last.**

---

## Layer 0 — DB Migration (nuwis-db-migrator, haiku)

Buat/verify migration SQL di `infra/db/migrations/` untuk kedua portal.

### Tabel `transaction.budgetowner`

- [ ] **V{NNN}__create_budgetowner_table.sql**
  - Create `transaction.budgetowner` dengan kolom:
    - `ownerid SERIAL PRIMARY KEY`
    - `ownercode VARCHAR(10) UNIQUE NOT NULL`
    - `ownername VARCHAR(100) NOT NULL`
    - `level INTEGER NOT NULL DEFAULT 1`
    - `is_detail VARCHAR(1) NOT NULL DEFAULT 'T'` (CHECK 'T'|'F')
    - `parentownerid INTEGER REFERENCES transaction.budgetowner(ownerid)`
    - `status VARCHAR(1) NOT NULL DEFAULT 'A'` (CHECK 'A'|'N')
    - `tglubah TIMESTAMP DEFAULT CURRENT_TIMESTAMP`
    - `userpengubah VARCHAR(30)`
    - `terminalubah VARCHAR(30)`
    - `branch_id INTEGER REFERENCES enterprise.branch(branchid)`
  - Constraints: CHECK (is_detail='T' AND parentownerid NOT NULL) OR is_detail='F'
  - Constraints: CHECK status IN ('A', 'N')
  - **Terapkan ke**: `mziss_laz` dan `mziss_wakaf`

### Tabel `transaction.budgetownerhierarchy`

- [ ] **V{NNN}__create_budgetownerhierarchy_table.sql**
  - Create `transaction.budgetownerhierarchy`:
    - `childownerid INTEGER NOT NULL FK to budgetowner(ownerid)`
    - `parentownerid INTEGER NOT NULL FK to budgetowner(ownerid)`
    - `level INTEGER NOT NULL` (0=self, 1=parent, 2+=ancestor)
    - PRIMARY KEY (`childownerid`, `parentownerid`)
  - **Terapkan ke**: `mziss_laz` dan `mziss_wakaf`

### Verifikasi

```bash
# Zakat
psql -U transaction -d mziss_laz -c "\d transaction.budgetowner"
psql -U transaction -d mziss_laz -c "\d transaction.budgetownerhierarchy"

# Wakaf
psql -U transaction -d mziss_wakaf -c "\d transaction.budgetowner"
psql -U transaction -d mziss_wakaf -c "\d transaction.budgetownerhierarchy"
```

---

## Layer 1 — Python API (nuwis-python-builder, haiku)

Buat modul `transaction.budgetowner` di `apps_{portal}/api-python/app/modules/transaction/`.

### File: `schema.py` — Pydantic Models

- [ ] `PemilikAnggaranRead` — for GET responses
  - `ownerid: int`
  - `ownercode: str`
  - `ownername: str`
  - `level: int`
  - `is_detail: str` (Literal['T', 'F'])
  - `parentownerid: int | None`
  - `status: str` (Literal['A', 'N'])
  - `tglubah: datetime`
  - `userpengubah: str | None`
  - `terminalubah: str | None`

- [ ] `PemilikAnggaranCreate` — for POST create
  - `ownercode: str` (min_length=1, max_length=10)
  - `ownername: str` (min_length=1, max_length=100)
  - `parentownerid: int | None`
  - `is_detail: str` (Literal['T', 'F'])
  - `status: str = 'A'` (Literal['A', 'N'])
  - Validators: if is_detail='T' then parentownerid required

- [ ] `PemilikAnggaranUpdate` — for POST update
  - `ownerid: int` (required)
  - `ownername: str` (only mutable field)
  - `status: str` (Literal['A', 'N'])
  - Note: ownercode, parentownerid, is_detail must be ReadOnly

- [ ] `PemilikAnggaranDelete` — for POST delete
  - `ownerid: int` (required)

- [ ] `PemilikAnggaranLookup` — for GET /lookup response
  - `ownerid: int`
  - `ownercode: str`
  - `ownername: str`
  - `is_detail: str`

### File: `repo.py` — Database Access

- [ ] `class BudgetOwnerRepository`:

  - [ ] `async def list_all(page: int, limit: int) -> tuple[list[dict], int]`
    - Query: `SELECT * FROM transaction.budgetowner ORDER BY ownercode LIMIT ? OFFSET ?`
    - Return: (rows, total_count)

  - [ ] `async def get_by_id(ownerid: int) -> dict`
    - Query: `SELECT * FROM transaction.budgetowner WHERE ownerid = ?`
    - Raise 404 if not found

  - [ ] `async def lookup_groups(search_q: str | None = None) -> list[dict]`
    - Query: `SELECT ownerid, ownercode, ownername, is_detail FROM transaction.budgetowner WHERE is_detail='F' ORDER BY ownername`
    - Optional: filter by ownercode ILIKE or ownername ILIKE if search_q provided
    - Return: list untuk dropdown (only groups/induk)

  - [ ] `async def get_parent_level(parentownerid: int) -> int`
    - Query: `SELECT level FROM transaction.budgetowner WHERE ownerid = ?`
    - Return: parent.level (untuk auto-calc level child)

  - [ ] `async def check_has_children(ownerid: int) -> bool`
    - Query: `SELECT EXISTS(SELECT 1 FROM transaction.budgetowner WHERE parentownerid = ?)`
    - Return: True if has children, False otherwise

  - [ ] `async def check_referenced_by_budget(ownerid: int) -> bool`
    - Query: `SELECT EXISTS(SELECT 1 FROM transaction.budget WHERE budgetownerid = ?)`
    - Return: True if referenced, False otherwise

  - [ ] `async def insert_budget_owner(payload: dict, inputer_id: str, branch_id: int) -> int`
    - INSERT ke `transaction.budgetowner`
    - Return: new ownerid (LAST_INSERT_ID)

  - [ ] `async def update_budget_owner(ownerid: int, ownername: str, status: str, updater_id: str) -> None`
    - UPDATE `transaction.budgetowner` SET ownername, status, tglubah, userpengubah WHERE ownerid
    - Only update mutable fields

  - [ ] `async def delete_budget_owner(ownerid: int) -> None`
    - DELETE FROM `transaction.budgetowner` WHERE ownerid
    - (Constraint check di service)

  - [ ] `async def insert_hierarchy_rows(ownerid: int, parentownerid: int | None) -> None`
    - INSERT self-reference: `(ownerid, ownerid, 0)`
    - If parentownerid: walk parent chain (recursive query atau iterative)
    - For each ancestor, INSERT `(ownerid, ancestor.ownerid, level_distance)`

### File: `service.py` — Business Logic

- [ ] `class BudgetOwnerService`:

  - [ ] `async def create_from_payload(payload: dict, inputer_id: str, branch_id: int) -> int`
    - Validate: ownercode not duplicated
    - Validate: if is_detail='T' then parentownerid required
    - Validate: if parentownerid provided, parent.is_detail must be 'F'
    - Auto-calc: level = parent.level + 1 (atau 1 jika no parent)
    - INSERT to budgetowner
    - Return: new ownerid
    - **Note**: SetHierarchy NOT called here — done by dispatcher after AUTHORIZED

  - [ ] `async def update_from_payload(ownerid: int, payload: dict, updater_id: str) -> None`
    - Validate: only ownername, status are mutable
    - Reject if trying to change ownercode, parentownerid, is_detail
    - Call repo.update_budget_owner

  - [ ] `async def delete_from_payload(ownerid: int) -> None`
    - Validate: no children (check_has_children)
    - Validate: not referenced by budget (check_referenced_by_budget)
    - If validation fails, raise 409 Conflict with message
    - Call repo.delete_budget_owner
    - Also DELETE rows from budgetownerhierarchy WHERE childownerid = ?

  - [ ] **DISPATCHER** `async def dispatcher_create_budget_owner(payload: dict, inputer_id: str, branch_id: int) -> None`
    - Called by otorisasi when submission AUTHORIZED
    - Call create_from_payload
    - ownerid = returned id
    - Call repo.insert_hierarchy_rows(ownerid, payload.get('parentownerid'))
    - Update otorisasi.submission SET result_entity_id = ownerid WHERE submission_id

  - [ ] **DISPATCHER** `async def dispatcher_update_budget_owner(payload: dict, updater_id: str) -> None`
    - Called by otorisasi when submission AUTHORIZED
    - Call update_from_payload

  - [ ] **DISPATCHER** `async def dispatcher_delete_budget_owner(payload: dict) -> None`
    - Called by otorisasi when submission AUTHORIZED
    - Call delete_from_payload

### File: `router.py` — HTTP Endpoints

- [ ] `GET /api/parameter/pemilik-anggaran`
  - Auth: `require_menu("parameter.pemilik-anggaran")`
  - Query: page (default=1), limit (default=25)
  - Response: {data: [{...}], pagination: {...}, meta: {...}}

- [ ] `GET /api/parameter/pemilik-anggaran/{id}`
  - Auth: `require_menu("parameter.pemilik-anggaran")`
  - Response: {data: {...}, meta: {...}}
  - Return 404 if not found

- [ ] `GET /api/parameter/pemilik-anggaran/lookup`
  - Auth: `require_menu("parameter.pemilik-anggaran")`
  - Query: q (optional search)
  - Response: {data: [{ownerid, ownercode, ownername, is_detail}], meta: {...}}

### Registration

- [ ] Daftarkan router di `apps_{portal}/api-python/app/main.py`:
  ```python
  from app.modules.transaction.budgetowner.router import router
  app.include_router(router, prefix="/api/parameter", tags=["parameter"])
  ```

- [ ] Daftarkan dispatcher di `apps_{portal}/api-python/app/modules/otorisasi/service.py`:
  ```python
  def _register_defaults():
    self.register_dispatcher(
      'budget_owner',
      'create',
      lambda payload, inputer_id, branch_id: 
        BudgetOwnerService.dispatcher_create_budget_owner(payload, inputer_id, branch_id)
    )
    self.register_dispatcher(
      'budget_owner',
      'update',
      lambda payload, updater_id:
        BudgetOwnerService.dispatcher_update_budget_owner(payload, updater_id)
    )
    self.register_dispatcher(
      'budget_owner',
      'delete',
      lambda payload:
        BudgetOwnerService.dispatcher_delete_budget_owner(payload)
    )
  ```

---

## Layer 2 — BFF-API (nuwis-bff-builder, haiku)

Buat router di `apps_{portal}/bff-api/app/routers/parameter.py` (atau extend jika sudah ada).

### File: `routers/parameter.py`

- [ ] `GET /api/parameter/pemilik-anggaran`
  - Auth: `@require_menu("parameter.pemilik-anggaran")`
  - Proxy ke api-python
  - Call: `await api_client.get("/api/parameter/pemilik-anggaran?page={page}&limit={limit}")`
  - Return response as-is

- [ ] `GET /api/parameter/pemilik-anggaran/{id}`
  - Auth: `@require_menu("parameter.pemilik-anggaran")`
  - Proxy ke api-python
  - Call: `await api_client.get(f"/api/parameter/pemilik-anggaran/{id}")`
  - Return 404 if not found

- [ ] `GET /api/parameter/pemilik-anggaran/lookup`
  - Auth: `@require_menu("parameter.pemilik-anggaran")`
  - Proxy ke api-python
  - Call: `await api_client.get("/api/parameter/pemilik-anggaran/lookup", params={"q": q})`
  - Return response with dropdown list

### Notes on CREATE/UPDATE/DELETE

- CREATE, UPDATE, DELETE go through **shared `/api/otorisasi/save-and-submit/`** endpoint
- BFF does **not** have separate POST/PUT/DELETE for pemilik-anggaran
- Otorisasi router already handles: entity_type='budget_owner', inject inputer_id + branch_id

### Registration

- [ ] Daftarkan di `apps_{portal}/bff-api/app/main.py`:
  ```python
  from app.routers import parameter
  app.include_router(parameter.router, prefix="/api", tags=["parameter"])
  ```

---

## Layer 3 — Frontend Vue (nuwis-ui-builder, haiku)

### File: `lib/menu/registry.ts` — Menu Key Registration

- [ ] Add constants:
  ```typescript
  PEMILIK_ANGGARAN: "parameter.pemilik-anggaran",
  PEMILIK_ANGGARAN_TAMBAH: "parameter.pemilik-anggaran.tambah",
  PEMILIK_ANGGARAN_UBAH: "parameter.pemilik-anggaran.ubah",
  PEMILIK_ANGGARAN_HAPUS: "parameter.pemilik-anggaran.hapus",
  PEMILIK_ANGGARAN_APPROVE: "parameter.pemilik-anggaran.approve",
  ```

### File: `router/index.ts` — Route Definition

- [ ] Add named route for list page:
  ```typescript
  {
    path: "/parameter/pemilik-anggaran",
    name: "PemilikAnggaranPage",
    component: () => import("@/pages/parameter/PemilikAnggaranPage.vue"),
    meta: {
      menu_key: MENU_KEYS.PEMILIK_ANGGARAN,
      title: "Pemilik Anggaran"
    }
  }
  ```

### File: `components/AppSidebar.vue` — Sidebar Entry

- [ ] Add menu item under "Parameter" group:
  ```vue
  {
    label: "Pemilik Anggaran",
    icon: "lucide:users",
    to: { name: "PemilikAnggaranPage" },
    menu_key: MENU_KEYS.PEMILIK_ANGGARAN
  }
  ```

### File: `pages/parameter/PemilikAnggaranPage.vue` — List Page

- [ ] Create new page component with:
  - Header: "Daftar Pemilik Anggaran"
  - Toolbar: [Search input] [Add button] (if has permission)
  - **Pagination component** (above table, not below)
  - DataTable (lazy) with columns:
    - ownercode
    - ownername
    - level
    - is_detail (display as "Tipe" → "Induk" if F, "Detail" if T)
    - status (badge "Active"/"Not Active")
    - Actions: [Edit] [Delete] (if has permission)
  - useFetch hook untuk GET /api/parameter/pemilik-anggaran

- [ ] Implement:
  - `onPageChange(page)` → refetch with new page
  - `onAddClick()` → open PemilikAnggaranFormModal(mode="create")
  - `onEditClick(row)` → open PemilikAnggaranFormModal(mode="edit", data=row)
  - `onDeleteClick(row)` → open PemilikAnggaranDeleteModal(data=row)

### File: `components/parameter/PemilikAnggaranFormModal.vue` — Create/Edit Form

- [ ] Create modal component:
  - Title: "Tambah Pemilik Anggaran" / "Ubah Pemilik Anggaran"
  - Form fields:
    - `ownercode` — TextInput (ReadOnly if mode="edit")
    - `ownername` — TextInput (required)
    - `parentownerid` — SearchSelect (lookup groups, required if is_detail='T')
    - `is_detail` — Radio/Select "Induk" ('F') / "Detail" ('T') (ReadOnly if mode="edit")
    - `status` — Select ['A', 'N'] (default='A')

  - Validation: if is_detail='T' then parentownerid required
  - On submit:
    - POST /api/otorisasi/save-and-submit/ with entity_type='budget_owner'
    - Show loading spinner
    - On success: show toast, close modal, refetch list
    - On error: show error toast with details
    - If status='PENDING': show info toast "Menunggu approval"

### File: `components/parameter/PemilikAnggaranDeleteModal.vue` — Delete Confirmation

- [ ] Create modal component:
  - Title: "Hapus Pemilik Anggaran"
  - Display read-only form dengan data lengkap:
    - ownercode
    - ownername
    - parentownerid (display parent name)
    - is_detail
    - status
  - Warning message: "Data ini akan dihapus. Tindakan ini tidak dapat dibatalkan."
  - Buttons: [Batal] [Hapus]
  - On delete:
    - POST /api/otorisasi/save-and-submit/ with entity_type='budget_owner', entity_subtype='delete'
    - Show loading
    - On success: toast, close modal, refetch list
    - On error (409): show error "Tidak bisa dihapus — ada data detail atau referensi"

### File: `components/ui/SearchSelect.vue` Usage

- [ ] For parentownerid field:
  - Use existing `SearchSelect` component
  - Props: `:options="parentLookup"`, `:modelValue="form.parentownerid"`
  - Fetch parentLookup via: GET /api/parameter/pemilik-anggaran/lookup
  - Display: ownercode + ownername

---

## Layer 4 — Seed (nuwis-seed-gen, haiku)

Buat seeder di `infra/db/migrations/seed/` untuk kedua portal.

### File: `seed-pemilik-anggaran-menu.sql`

- [ ] Insert menu rows untuk zakat + wakaf:
  ```sql
  -- Zakat
  INSERT INTO isf_auth_zakat.menu (menu_key, menu_name, is_active)
  VALUES
    ('parameter.pemilik-anggaran', 'Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.tambah', 'Tambah Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.ubah', 'Ubah Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.hapus', 'Hapus Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.approve', 'Approve Pemilik Anggaran', true)
  ON CONFLICT DO NOTHING;

  -- Wakaf
  INSERT INTO isf_auth_wakaf.menu (menu_key, menu_name, is_active)
  VALUES
    ('parameter.pemilik-anggaran', 'Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.tambah', 'Tambah Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.ubah', 'Ubah Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.hapus', 'Hapus Pemilik Anggaran', true),
    ('parameter.pemilik-anggaran.approve', 'Approve Pemilik Anggaran', true)
  ON CONFLICT DO NOTHING;
  ```

### File: `seed-pemilik-anggaran-rolemenu.sql`

- [ ] Insert role_menu rows:
  ```sql
  -- Zakat: KEU, SPVKEU, ACC, ADMIN dapat view + CRUD; SPVADM dapat approve
  INSERT INTO isf_auth_zakat.role_menu (role_id, menu_id)
  SELECT r.role_id, m.menu_id
  FROM isf_auth_zakat.menu m
  CROSS JOIN (
    SELECT role_id FROM isf_auth_zakat.roles 
    WHERE role_name IN ('KEU', 'SPVKEU', 'ACC', 'ADMIN', 'SPVADM')
  ) r
  WHERE m.menu_key LIKE 'parameter.pemilik-anggaran%'
  ON CONFLICT DO NOTHING;

  -- Wakaf: same
  INSERT INTO isf_auth_wakaf.role_menu (role_id, menu_id)
  SELECT r.role_id, m.menu_id
  FROM isf_auth_wakaf.menu m
  CROSS JOIN (
    SELECT role_id FROM isf_auth_wakaf.roles 
    WHERE role_name IN ('KEU', 'SPVKEU', 'ACC', 'ADMIN', 'SPVADM')
  ) r
  WHERE m.menu_key LIKE 'parameter.pemilik-anggaran%'
  ON CONFLICT DO NOTHING;
  ```

### File: `seed-pemilik-anggaran-entity-config.sql`

- [ ] Insert otorisasi entity_config (jika limit check ada):
  ```sql
  INSERT INTO mziss_laz.otorisasi.entity_config (entity_type, entity_name, limit_checker_fn)
  VALUES ('budget_owner', 'Pemilik Anggaran', NULL)  -- NULL = no limit, direct AUTHORIZED
  ON CONFLICT DO NOTHING;

  INSERT INTO mziss_wakaf.otorisasi.entity_config (entity_type, entity_name, limit_checker_fn)
  VALUES ('budget_owner', 'Pemilik Anggaran', NULL)
  ON CONFLICT DO NOTHING;
  ```

### Apply Seeders

- [ ] Zakat:
  ```bash
  psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-pemilik-anggaran-menu.sql
  psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-pemilik-anggaran-rolemenu.sql
  psql -U transaction -d mziss_laz -f infra/db/migrations/seed/seed-pemilik-anggaran-entity-config.sql
  ```

- [ ] Wakaf:
  ```bash
  psql -U transaction -d isf_auth_wakaf -f infra/db/migrations/seed/seed-pemilik-anggaran-menu.sql
  psql -U transaction -d isf_auth_wakaf -f infra/db/migrations/seed/seed-pemilik-anggaran-rolemenu.sql
  psql -U transaction -d mziss_wakaf -f infra/db/migrations/seed/seed-pemilik-anggaran-entity-config.sql
  ```

---

## Layer 5 — Testing (nuwis-test-gen, haiku)

### File: `testing/e2e-pemilik-anggaran.sh`

- [ ] Create E2E smoke test script:
  - [ ] Test 1: GET /api/parameter/pemilik-anggaran (list)
  - [ ] Test 2: POST /api/otorisasi/save-and-submit/ (create, expect AUTHORIZED or PENDING)
  - [ ] Test 3: GET /api/parameter/pemilik-anggaran/{id} (verify created data)
  - [ ] Test 4: POST /api/otorisasi/save-and-submit/ (update ownername only)
  - [ ] Test 5: GET /api/parameter/pemilik-anggaran/lookup (filter is_detail='F')
  - [ ] Test 6: POST /api/otorisasi/save-and-submit/ (delete, check constraint)
  - [ ] Test 7: If submission PENDING, test POST /api/otorisasi/submission/{id}/approve

**Template structure:**
```bash
#!/bin/bash
set -e

BFF_URL="http://localhost:7000"
TOKEN="<test-token>"

echo "Test 1: GET list..."
curl -s -H "Authorization: Bearer $TOKEN" \
  "$BFF_URL/api/parameter/pemilik-anggaran?page=1&limit=25" | jq .

echo "Test 2: Create new..."
# POST to /api/otorisasi/save-and-submit/

...
```

### Unit Tests (Optional, if complex logic)

- [ ] `apps_{portal}/api-python/tests/test_budgetowner.py` (if service logic warrants testing)

---

## Verifikasi Akhir

```bash
# Restart containers setelah semua layer selesai
cd infra
podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue
podman-compose -f docker-compose.wakaf.yml restart api-python bff-api web-vue

# Tunggu ~10 detik
sleep 10

# Jalankan E2E
bash testing/e2e-pemilik-anggaran.sh

# Manual testing di browser
# - Login dengan user KEU (e.g., HADI atau RAIS)
# - Navigate to Pemilik Anggaran di sidebar
# - Klik "Tambah" → isi form
# - Submit → check Monitoring Otorisasi jika PENDING
# - Test edit (verify ownercode ReadOnly)
# - Test delete dengan data yang ada child (check error)
```

---

## Catatan Penting

### 1. SetHierarchy di Dispatcher, Bukan Submit
Penyimpanan `budgetownerhierarchy` **harus di background dispatcher** setelah AUTHORIZED.
Ini penting untuk consistency — jika dispatcher gagal, tidak ada orphan rows di hierarki table.

**Urutan di dispatcher:**
1. Create owner record di `budgetowner`
2. Get new ownerid
3. Insert self-reference + parent chain ke `budgetownerhierarchy`
4. Update submission.result_entity_id = ownerid
5. Update submission.status = 'AUTHORIZED'

### 2. ReadOnly Fields pada Edit
Ketika user buka form edit, fields berikut harus ReadOnly (disabled + non-submittable):
- `ownercode` — kunci otorisasi, tidak boleh berubah
- `parentownerid` — bisa break existing hierarki
- `is_detail` — bisa break constraint parent-child

Hanya `ownername` dan `status` boleh diedit.

### 3. Approver adalah SPVADM
Role approver untuk semua otorisasi adalah **SPVADM**. Tidak ada role-specific approval untuk modul ini.
Pastikan role_menu setup menempatkan `parameter.pemilik-anggaran.approve` → SPVADM role.

### 4. Portal Isolation — Dual DB
- Zakat: `mziss_laz` + `isf_auth_zakat`
- Wakaf: `mziss_wakaf` + `isf_auth_wakaf`

Setiap portal punya tabel budgetowner terpisah. BFF inject branch_id dan portal context otomatis.

### 5. Delete Validation — Two Checks
Sebelum DELETE, query untuk:
1. **Ada child owner**: `SELECT COUNT(*) FROM transaction.budgetowner WHERE parentownerid = ?`
2. **Direferensi budget**: `SELECT COUNT(*) FROM transaction.budget WHERE budgetownerid = ?`

Jika ada, return 409 Conflict. Message: "Tidak bisa dihapus — ada data detail atau referensi"

### 6. Verify Migration exists
Sebelum implement Layer 1+, **verify** bahwa tabel `transaction.budgetowner` dan `transaction.budgetownerhierarchy`
sudah exist di `mziss_laz` dan `mziss_wakaf`. Jika belum, create migration di Layer 0 dulu.

### 7. Approver Flow di OtorisasiPage
Menu key `parameter.pemilik-anggaran.approve` harus ada di sidebar untuk user SPVADM.
Di halaman `/keuangan/monitoring/otorisasi`, filter submissions dengan:
- `entity_type = 'budget_owner'`
- `status IN ('PENDING', 'PROCESSING')`

Display submission detail + tombol "Otorisasi" → POST /api/otorisasi/submission/{id}/approve

---

## Status Checklist

**Not Started** — 0 / 5 layers complete

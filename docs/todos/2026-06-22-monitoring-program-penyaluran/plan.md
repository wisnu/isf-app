# Plan: Monitoring Program Penyaluran

**Dibuat**: 2026-06-22
**Target Portal**: zakat
**Domain**: distribution (distribution.monitoring.*)
**Kompleksitas**: Sedang (CRUD dengan 4 sub-entities, 6 discriminators, no approval workflow)

## Urutan Eksekusi

**Layer 1–2 bisa paralel** (DB migration tidak block Python API, Python tidak block BFF).
**Layer 3 harus after Layer 2** (BFF proxy).
**Layer 4 harus after Layer 3** (BFF endpoint harus ready).
**Layer 5 parallel dengan 4** (E2E smoke test bisa run saat semua layer online).

---

## Layer 1 — Database (nuwis-db-migrator, haiku)

Tabel sudah ada di schema `program` (verifikasi + index).

### Task 1.1: Verifikasi Tabel Exist + Kolom Lengkap
**File**: `/home/wishnew/workshop/isf-app/infra/db/migrations/` (cek V006 atau sebelumnya)

- [ ] Verifikasi `program.visit` ada dengan kolom:
  - `visitid SERIAL PRIMARY KEY`
  - `visittype VARCHAR(1)` — discriminator untuk 'P' = Program Penyaluran
  - `visitdate DATE`
  - `visitaddress VARCHAR(200)`
  - `visitlocation VARCHAR(200)`
  - `visitbegintime TIMESTAMP` (nullable)
  - `visitendtime TIMESTAMP` (nullable)
  - `mustahiqid INTEGER` — FK → program.mustahiq
  - `mustahiqproductid INTEGER` — FK → program.mustahiqproduct (nullable)

- [ ] Verifikasi `program.visitperson` ada dengan kolom:
  - `visitpersonid SERIAL PRIMARY KEY`
  - `visitid INTEGER` — FK → program.visit
  - `visitpersontype VARCHAR(1)` — discriminator: 'A'=Amil, 'S'=Mustahiq
  - `visitpersonname VARCHAR(100)`
  - `visitpersonposition VARCHAR(100)`

- [ ] Verifikasi `program.visititem` ada dengan kolom:
  - `visititemid SERIAL PRIMARY KEY`
  - `visitid INTEGER` — FK → program.visit
  - `visititemtype VARCHAR(1)` — discriminator: 'P'=Purpose, 'R'=Result, 'F'=FollowUp
  - `visititemannotation VARCHAR(200)`

**Catatan**: Jika kolom ada tapi FK missing, tambahkan FK di migration baru.

### Task 1.2: Tambah Index (jika belum ada)
**File**: `infra/db/migrations/V008__add_monitoring_visit_indexes.sql` (atau sesuaikan nomor)

```sql
-- Cek apakah index sudah ada, jika belum buat:
CREATE INDEX IF NOT EXISTS idx_visit_type_date 
  ON program.visit(visittype, visitdate);

CREATE INDEX IF NOT EXISTS idx_visitperson_visit_type 
  ON program.visitperson(visitid, visitpersontype);

CREATE INDEX IF NOT EXISTS idx_visititem_visit_type 
  ON program.visititem(visitid, visititemtype);
```

**Apply setelah selesai**:
```bash
cd /home/wishnew/workshop/isf-app/infra && \
psql -U transaction -d mziss_zakat -f db/migrations/V008__add_monitoring_visit_indexes.sql
```

### Task 1.3: Verifikasi DWH View (opsional, jika laporan dibutuhkan nanti)
- [ ] Cek apakah `dwh.v_monitoring_visit` perlu dibuat sekarang (tanyakan ke BA)
  - Jika ya: buat di `infra/db/migrations/dwh/v_monitoring_visit.sql`
  - Jika tidak: simpan untuk tahap laporan berikutnya

---

## Layer 2 — Python API (nuwis-python-builder, haiku)

**Path**: `/home/wishnew/workshop/isf-app/apps_zakat/api-python/app/modules/distribution/`

Buat modul baru `monitoring_visit/` dengan 4 file.

### Task 2.1: schema.py — Pydantic Models

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/api-python/app/modules/distribution/monitoring_visit/schema.py`

Definisikan models untuk:
- `VisitPersonRow` — visit_person_id, visit_person_name, visit_person_position
- `VisitItemRow` — visit_item_id, visit_item_annotation
- `MonitoringVisitRow` — list view: visit_id, visit_date, visit_location, mustahiq_name, program_name, etc
- `Pagination` — page, limit, total, total_pages
- `MonitoringVisitList` — rows[], pagination
- `MonitoringVisitDetail` — visit data + persons_amil[], persons_mustahiq[], purposes[], results[], followups[]
- `CreateMonitoringVisitBody` — mustahiq_id, mustahiq_product_id, visit_address, visit_location, visit_date, visit_begin_time?, visit_end_time?, persons_amil[], persons_mustahiq[], purposes[], results[], followups[]

**Catatan**: Semua field name gunakan `snake_case` (Python convention).

### Task 2.2: service.py — Business Logic

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/api-python/app/modules/distribution/monitoring_visit/service.py`

Implementasikan function:

#### List
```python
async def list_monitoring_visits(
    begin_date: str,  # YYYY-MM-DD
    end_date: str,    # YYYY-MM-DD
    page: int = 1,
    limit: int = 25
) -> MonitoringVisitList:
```

**Query SQL** (gunakan CAST not ::):
```sql
SELECT
  a.visitid,
  a.visitdate,
  a.visitlocation,
  a.visitaddress,
  f.customername,
  d.productname,
  e.mustahiqproductname,
  a.mustahiqid,
  a.mustahiqproductid,
  COALESCE(g.usernm, 'SYSTEM') AS user_input
FROM program.visit a
LEFT JOIN program.mustahiq b ON a.mustahiqid = b.mustahiqid
LEFT JOIN program.customer f ON b.customerid = f.customerid
LEFT JOIN program.mustahiqproduct e ON a.mustahiqproductid = e.mustahiqproductid
LEFT JOIN program.product d ON e.productid = d.productid
LEFT JOIN isf_auth.users g ON a.inputer_id = g.userid
WHERE a.visittype = 'P'  -- KRITIS: discriminator
  AND CAST(a.visitdate AS DATE) >= CAST($1 AS DATE)
  AND CAST(a.visitdate AS DATE) < CAST($2 AS DATE) + INTERVAL '1 day'
ORDER BY a.visitdate DESC, a.visitid
LIMIT $3 OFFSET ($4-1)*$3
```

**Catatan**:
- Discriminator `visittype = 'P'` WAJIB ada
- Gunakan CAST() for PostgreSQL compatibility
- Offset = (page - 1) * limit

#### Get Detail
```python
async def get_monitoring_visit(visit_id: int) -> MonitoringVisitDetail:
```

Fetch:
1. Main visit record
2. VISITPERSON WHERE visitid={id} AND visitpersontype='A' → persons_amil[]
3. VISITPERSON WHERE visitid={id} AND visitpersontype='S' → persons_mustahiq[]
4. VISITITEM WHERE visitid={id} AND visititemtype='P' → purposes[]
5. VISITITEM WHERE visitid={id} AND visititemtype='R' → results[]
6. VISITITEM WHERE visitid={id} AND visititemtype='F' → followups[]

#### Create
```python
async def create_monitoring_visit(
    branch_id: int,  # from BFF session
    inputer_id: int,  # from BFF session
    body: CreateMonitoringVisitBody
) -> int:  # return visit_id
```

**Logic**:
1. Validasi (server-side):
   - mustahiq_id > 0
   - visit_address, visit_location, visit_date ≠ ""
   - len(persons_amil) ≥ 1
   - len(persons_mustahiq) ≥ 1
   - len(purposes) ≥ 1
   - len(results) ≥ 1
   - len(followups) ≥ 1

2. START TRANSACTION
3. INSERT INTO program.visit (visittype='P', visitdate, visitaddress, visitlocation, visitbegintime?, visitendtime?, mustahiqid, mustahiqproductid, branch_id?, inputer_id) → get visitid
4. INSERT visitperson × len(persons_amil) with visitpersontype='A'
5. INSERT visitperson × len(persons_mustahiq) with visitpersontype='S'
6. INSERT visititem × len(purposes) with visititemtype='P'
7. INSERT visititem × len(results) with visititemtype='R'
8. INSERT visititem × len(followups) with visititemtype='F'
9. COMMIT
10. Return visit_id

#### Update
```python
async def update_monitoring_visit(
    visit_id: int,
    branch_id: int,
    inputer_id: int,
    body: CreateMonitoringVisitBody
) -> int:
```

**Logic** (bulk replace pattern):
1. START TRANSACTION
2. UPDATE program.visit SET ... WHERE visitid={id}
3. DELETE FROM program.visitperson WHERE visitid={id}
4. DELETE FROM program.visititem WHERE visitid={id}
5. Re-insert all persons + items (same as create)
6. COMMIT
7. Return visit_id

#### Delete
```python
async def delete_monitoring_visit(visit_id: int) -> None:
```

**Logic**:
1. START TRANSACTION
2. DELETE FROM program.visititem WHERE visitid={id}
3. DELETE FROM program.visitperson WHERE visitid={id}
4. DELETE FROM program.visit WHERE visitid={id}
5. COMMIT

### Task 2.3: router.py — FastAPI Endpoints

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/api-python/app/modules/distribution/monitoring_visit/router.py`

Endpoints:
- `GET /api/distribution/monitoring-visits` → list_monitoring_visits(begin_date, end_date, page, limit)
- `GET /api/distribution/monitoring-visits/{visit_id}` → get_monitoring_visit(visit_id)
- `POST /api/distribution/monitoring-visits` → create_monitoring_visit(branch_id, inputer_id, body)
- `PUT /api/distribution/monitoring-visits/{visit_id}` → update_monitoring_visit(visit_id, branch_id, inputer_id, body)
- `DELETE /api/distribution/monitoring-visits/{visit_id}` → delete_monitoring_visit(visit_id)

**Response wrapper**: Gunakan `ok()` helper dari `app.shared.response`.

### Task 2.4: Register Router

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/api-python/app/main.py`

Daftarkan router di app startup:
```python
from app.modules.distribution.monitoring_visit.router import router as monitoring_visit_router

app.include_router(monitoring_visit_router)
```

---

## Layer 3 — BFF API (nuwis-bff-builder, haiku)

**Path**: `/home/wishnew/workshop/isf-app/apps_zakat/bff-api/app/routers/`

### Task 3.1: distribution.py — BFF Route Handler

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/bff-api/app/routers/distribution.py` (buat atau update jika sudah ada)

Buat route untuk proxy:
- `GET /api/distribution/monitoring-visits`
- `GET /api/distribution/monitoring-visits/{visit_id}`
- `POST /api/distribution/monitoring-visits` — inject inputer_id, branch_id dari session
- `PUT /api/distribution/monitoring-visits/{visit_id}`
- `DELETE /api/distribution/monitoring-visits/{visit_id}`

**Pattern** (lihat mustahiq router sebagai referensi):
- `@require_menu("distribution.monitoring.list")` untuk GET list
- `@require_menu("distribution.monitoring.view")` untuk GET detail
- `@require_menu("distribution.monitoring.create")` untuk POST
- `@require_menu("distribution.monitoring.update")` untuk PUT
- `@require_menu("distribution.monitoring.delete")` untuk DELETE
- Gunakan `_resolve_branch(request)` untuk inject branch_id
- Proxy ke `http://api-python:8000/api/distribution/monitoring-visits`

### Task 3.2: Register BFF Router

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/bff-api/app/main.py`

```python
from app.routers.distribution import router as distribution_router

app.include_router(distribution_router)
```

---

## Layer 4 — Menu & Auth (nuwis-seed-gen, haiku)

### Task 4.1: Tambah Menu Key ke Registry

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/shared/constants/menu-keys.ts`

Tambahkan 5 menu key baru:
```typescript
'distribution.monitoring.list',
'distribution.monitoring.create',
'distribution.monitoring.view',
'distribution.monitoring.update',
'distribution.monitoring.delete',
```

### Task 4.2: Seed Menu + Role_Menu

**File**: `/home/wishnew/workshop/isf-app/infra/db/migrations/seed/distribution-monitoring-seed.sql`

Buat seed SQL untuk insert ke `isf_auth_zakat.menu` dan `isf_auth_zakat.role_menu`:

```sql
-- Insert menu keys (di transaction mode, cek tabel isf_auth.menu apakah ada kolom lain)
INSERT INTO isf_auth.menu (menu_key, label, parentmenukey, priority, icon, section)
VALUES
  ('distribution.monitoring.list', 'Monitoring Program Penyaluran', 'distribution', 1, 'icon-monitor', NULL),
  ('distribution.monitoring.create', 'Tambah Monitoring', 'distribution.monitoring.list', 1, NULL, NULL),
  ('distribution.monitoring.view', 'Lihat Monitoring', 'distribution.monitoring.list', 2, NULL, NULL),
  ('distribution.monitoring.update', 'Ubah Monitoring', 'distribution.monitoring.list', 3, NULL, NULL),
  ('distribution.monitoring.delete', 'Hapus Monitoring', 'distribution.monitoring.list', 4, NULL, NULL);

-- Assign ke roles DIST dan SPVDIST (cek role_id di isf_auth.role terlebih dahulu)
INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.role_id, 'distribution.monitoring.list' FROM isf_auth.role r WHERE r.role_code IN ('DIST', 'SPVDIST');
INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.role_id, 'distribution.monitoring.create' FROM isf_auth.role r WHERE r.role_code = 'DIST';
INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.role_id, 'distribution.monitoring.view' FROM isf_auth.role r WHERE r.role_code IN ('DIST', 'SPVDIST');
INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.role_id, 'distribution.monitoring.update' FROM isf_auth.role r WHERE r.role_code = 'DIST';
INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.role_id, 'distribution.monitoring.delete' FROM isf_auth.role r WHERE r.role_code IN ('DIST', 'SPVDIST');
```

**Apply setelah selesai**:
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/distribution-monitoring-seed.sql
```

### Task 4.3: Update Distribution Menu Config

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/modules/distribution/menu.ts`

Tambahkan group "Monitoring" ke menu config jika belum ada, atau tambahkan item ke group yang sesuai.

---

## Layer 5 — UI (nuwis-ui-builder, haiku)

**Path**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/modules/distribution/views/`

### Task 5.1: Create MonitoringVisitListView.vue

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/modules/distribution/views/monitoring-visit/MonitoringVisitListView.vue`

**Layout** (3-part: toolbar | pagination | table):
1. **Toolbar**:
   - 2 DateField inputs: begin_date, end_date (default both = today)
   - Button "Tampilkan Data" (fetch list)
   - Button "Tambah" (hanya jika role dapat create, buka modal form)

2. **Pagination**:
   - Standalone Paginator above table
   - "Showing X–Y of Z records"

3. **Table** (DataTable, lazy=true):
   - Columns: visit_date (dmy format), visit_location, mustahiq_name, program_name, mustahiq_product_name
   - Row actions: Edit, Lihat, Hapus (sesuai role)
   - Edit/Lihat → buka modal form
   - Hapus → modal confirm dengan form read-only, lalu DELETE

**States**:
- Default (before click Tampilkan): empty message "Pilih periode tanggal dan klik Tampilkan Data"
- Loading: spinner
- Success: table dengan data
- Error: toast + error message

### Task 5.2: Create MonitoringVisitFormModal.vue

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/modules/distribution/views/monitoring-visit/MonitoringVisitFormModal.vue`

**Modal dengan 5 tab** (menggunakan PrimeVue Tabs):

#### Tab 1: Data Utama
- SearchSelect: `mustahiq` (lookup via API `/api/distribution/mustahiq`)
  - Saat pilih: auto-fill visit_address dari customer.address
  - Hidden: mustahiq_id
- SearchSelect: `mustahiq_product` (optional, lookup via `/api/distribution/mustahiq-products?mustahiq_id=X`)
  - Hidden: mustahiq_product_id
  - Auto-fill product_name saat pilih
- Input: `visit_address` (read-only auto-fill, bisa di-edit)
- Input: `visit_location` (required, max 200)
- DateField: `visit_date` (required, v-model ISO string, display DD-MM-YYYY)
- Hidden: `visit_begin_time`, `visit_end_time` (accept dari body tapi jangan render)

#### Tab 2: Pihak Yang Bertemu
- Sub-grid 1: Pihak BPZIS (visitpersontype='A')
  - Columns: visit_person_name, visit_person_position
  - Add/Edit/Delete per row (minimal 1)
- Sub-grid 2: Pihak Mustahiq / Yayasan (visitpersontype='S')
  - Columns: visit_person_name, visit_person_position
  - Add/Edit/Delete per row (minimal 1)

#### Tab 3: Tujuan Kunjungan
- Sub-grid: purpose list
  - Column: visit_item_annotation (textarea, required, max 200)
  - Add/Edit/Delete per row (minimal 1)

#### Tab 4: Hasil Kunjungan
- Sub-grid: result list
  - Column: visit_item_annotation (textarea, required, max 200)
  - Add/Edit/Delete per row (minimal 1)

#### Tab 5: Tindak Lanjut
- Sub-grid: followup list
  - Column: visit_item_annotation (textarea, required, max 200)
  - Add/Edit/Delete per row (minimal 1)

**Mode Form**:
- `mode: 'New'` — semua field editable, submit = POST
- `mode: 'Edit'` — semua field editable, submit = PUT
- `mode: 'View'` — semua field readonly, tombol Simpan hidden, tombol Hapus visible (dengan confirm form modal terpisah)

**Validasi client-side** (sebelum POST/PUT):
1. mustahiq_id ≠ 0
2. visit_address ≠ ""
3. visit_location ≠ ""
4. visit_date ≠ ""
5. persons_amil.length ≥ 1
6. persons_mustahiq.length ≥ 1
7. purposes.length ≥ 1
8. results.length ≥ 1
9. followups.length ≥ 1

**Feedback**:
- Show loading spinner saat submit
- Toast success/error setelah submit
- Emit `@submitted` event ke parent untuk refresh list

### Task 5.3: Create Delete Confirm Modal

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/modules/distribution/views/monitoring-visit/MonitoringVisitDeleteConfirmModal.vue`

Modal show form read-only + 2 button (Cancel, Delete).
Saat Delete: call DELETE endpoint, show loading, toast success/error, emit @deleted.

### Task 5.4: Add Route

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/modules/distribution/routes.ts`

Tambahkan route:
```typescript
{
  path: '/distribution/monitoring-visit',
  name: 'distribution-monitoring-visit-list',
  component: () => import('@/modules/distribution/views/monitoring-visit/MonitoringVisitListView.vue'),
  meta: { 
    title: 'Monitoring Program Penyaluran', 
    menu_key: 'distribution.monitoring.list', 
    domain: 'distribution' 
  },
}
```

### Task 5.5: Update Sidebar Menu Config

**File**: `/home/wishnew/workshop/isf-app/apps_zakat/web-vue/src/modules/distribution/menu.ts`

Pastikan group "Monitoring" ada dan link ke route di atas dengan menu_key `distribution.monitoring.list`.

---

## Layer 6 — E2E Test (nuwis-test-gen, haiku)

### Task 6.1: Create Smoke Test Script

**File**: `/home/wishnew/workshop/isf-app/testing/e2e-monitoring-visit.sh`

Bash script dengan curl calls:
1. `GET /api/distribution/monitoring-visits?begin_date=...&end_date=...` — list
2. `POST /api/distribution/monitoring-visits` — create 1 record
3. `GET /api/distribution/monitoring-visits/{visit_id}` — get detail
4. `PUT /api/distribution/monitoring-visits/{visit_id}` — update
5. `DELETE /api/distribution/monitoring-visits/{visit_id}` — delete

**Env vars**:
- `BFF_URL=http://localhost:7000`
- `AUTH_TOKEN` (ambil dari `/api/auth/login` dengan user DIST)

**Run**:
```bash
bash testing/e2e-monitoring-visit.sh
```

---

## Verifikasi Akhir

```bash
# 1. Restart all containers setelah Layer 1-4 selesai
cd /home/wishnew/workshop/isf-app/infra
podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue

# 2. Verifikasi API endpoint (Layer 2+3)
curl -X GET "http://localhost:7000/api/distribution/monitoring-visits?begin_date=2026-06-22&end_date=2026-06-22" \
  -H "Authorization: Bearer $TOKEN"

# 3. Open browser (Layer 5)
# Navigate to http://localhost:5173/distribution/monitoring-visit
# Login dengan user DIST (username: DIST_USER, password: test1234)
# Coba: Tampilkan Data → Tambah → Fill 5 tab → Simpan → Lihat → Edit → Hapus

# 4. Run E2E (Layer 6)
bash testing/e2e-monitoring-visit.sh
```

---

## Checklist Implementasi

- [ ] Layer 1: DB migration (verifikasi tabel + index)
- [ ] Layer 2: Python API (schema.py + service.py + router.py + main.py register)
- [ ] Layer 3: BFF routes (distribution.py + main.py register)
- [ ] Layer 4: Menu seed (menu-keys.ts + distribution-monitoring-seed.sql)
- [ ] Layer 5: Vue pages (list + form modal + delete confirm)
- [ ] Layer 5: Routes (routes.ts update)
- [ ] Layer 5: Sidebar menu (menu.ts update)
- [ ] Layer 6: E2E smoke test (e2e-monitoring-visit.sh)
- [ ] Manual verify: browser login → CRUD flow works
- [ ] E2E script passes
- [ ] Discriminators verified (visittype='P', visitpersontype='A'/'S', visititemtype='P'/'R'/'F')
- [ ] No validation errors (9-field rule on client + server)

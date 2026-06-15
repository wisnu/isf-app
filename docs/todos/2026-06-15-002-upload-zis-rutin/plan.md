# Plan: Upload Data Penerimaan ZIS Rutin
**Dibuat**: 2026-06-15
**Target Portal**: zakat
**Kompleksitas**: TINGGI (5 dialog saling-terhubung, multi-entity write, auto-create donor, delete dengan temp table, background dispatcher)

## Urutan Eksekusi

Layer dapat dikerjakan secara paralel **HANYA** antara DB ↔ Seed (tidak ada dependency satu sama lain).
Namun Python, BFF, dan UI harus urut karena dependency ke schema + API.

---

## Layer 1 — DB/DWH (nuwis-db-migrator, haiku)

Verifikasi terlebih dahulu apakah tabel HC sudah ada di `mziss_laz`:
```bash
psql -U transaction -d mziss_laz -c "SELECT table_name FROM information_schema.tables WHERE table_schema='transaction' AND table_name LIKE 'humancapital%';"
```

- [ ] Jika **belum ada**: buat `infra/db/migrations/V###__create_humancapital_tables.sql`
  - `transaction.humancapitalbatch` (batch_id SERIAL PK, batch_period_desc UNIQUE, etc.)
  - `transaction.humancapitalbatchitem` (batch_item_id SERIAL PK, batch_id FK, etc.)
  - `transaction.humancapitalpassedreport` (report_id SERIAL PK, batch_id FK, etc.)
  - Index: `batch_period_desc` (untuk cek duplikat), `batch_id`, `donor_id`
  - FK constraints ke `fund.donor`, `transaction.transaction`

- [ ] Jika **sudah ada**: skip migration, verifikasi kolom sesuai specs.md

**Apply setelah selesai**:
```bash
psql -U transaction -d mziss_laz -f infra/db/migrations/V###__create_humancapital_tables.sql
```

---

## Layer 2 (Parallel) — Python API (nuwis-python-builder, haiku)

Lokasi: `apps_zakat/api-python/app/modules/transaksi/`

### Router & Service Structure

- [ ] `apps_zakat/api-python/app/modules/transaksi/__init__.py` — init modul
- [ ] `apps_zakat/api-python/app/modules/transaksi/router.py` — 6 endpoints (parse, submit, list, detail, update date, delete)
- [ ] `apps_zakat/api-python/app/modules/transaksi/service.py` — business logic
- [ ] `apps_zakat/api-python/app/modules/transaksi/schema.py` — Pydantic models (request/response)
- [ ] `apps_zakat/api-python/app/modules/transaksi/repo.py` — DB queries (jika logic kompleks)

### Endpoints (sesuai specs.md)

- [ ] `POST /api/transaksi/upload/hc-zis/parse` — openpyxl parse, cek duplikat BatchPeriodDesc, return totals + items preview
- [ ] `POST /api/transaksi/upload/hc-zis/submit` — save-and-submit ke otorisasi.submission (PENDING, kode_entri=TRANS041)
- [ ] `GET /api/transaksi/upload/hc-zis/batches` — list batches + status otorisasi (paginated)
- [ ] `GET /api/transaksi/upload/hc-zis/batches/{batch_id}` — detail batch + items
- [ ] `PUT /api/transaksi/upload/hc-zis/batches/{batch_id}/date` — save-and-submit update tanggal (TRANS044)
- [ ] `DELETE /api/transaksi/upload/hc-zis/batches/{batch_id}` — save-and-submit hapus batch (TRANS043)

### Business Logic (Dispatcher Services)

Daftarkan di `otorisasi/service.py:_register_defaults()`:

- [ ] `hc_zis_service.create_from_payload(submission_id)` — async background task utama
  - Step 1: Get/create `transaction.transaction_batch` (BatchTag='OPR', tanggal transaksi)
  - Step 2: Load parameter bank dari `enterprise.parameter_global`
  - Step 3: INSERT `humancapitalbatch` + `humancapitalbatchitem` (dari payload JSONB)
  - Step 4: Sinkronisasi donor existing (update field yang berubah + insert `fund.donor_field_history`)
  - Step 5: Auto-create donor baru (SQL batch: `SET_FLAG_NEWDONOR` → `CREATE_NEWDONOR` → `CREATE_NEWDONORINDIVIDUAL` → `UPDATE_DONOR_CUSTOM_IDGEN` → `SET_DONORID`)
  - Step 6: Update `fund.donor_commitment` (upsert per account parameter per donor + insert history)
  - Step 7: Loop items, buat transaksi per jenis dana (TransactionCode='SD002', ChannelCode='A', prefix 'BPZIS') + journal
  - Step 8: INSERT `fund.donor_total_fund` update, UPDATE `transaction.financial_account` balance
  - Step 9: INSERT `humancapitalpassedreport` (donor internal absen)
  - Final: UPDATE `otorisasi.submission` status='AUTHORIZED'

- [ ] `hc_zis_service.delete_from_payload(submission_id)` — async background task
  - CREATE TEMP TABLE untuk efisiensi
  - SELECT FOR UPDATE NOWAIT `fund.donor_total_fund`, `transaction.financial_account`
  - UPDATE balance (reverse semua amount)
  - DELETE dalam urutan: journal → journal_item → journal_block → transaction → transaction_item → humancapitalbatchitem → humancapitalbatch
  - INSERT `transaction.trans_history_of_changes` (ChangeType='D')
  - Final: UPDATE `otorisasi.submission` status='AUTHORIZED'

- [ ] `hc_zis_service.update_date_from_payload(submission_id)` — async background task
  - CREATE TEMP TABLE
  - SELECT FOR UPDATE NOWAIT `transaction.transaction`, `transaction.journal`
  - UPDATE `transaction.transaction` SET actual_date = new_date
  - UPDATE `transaction.journal` SET journal_date, fl_accountingperiode, fl_accountingyear (penting!)
  - UPDATE `humancapitalbatch` SET transaction_date = new_date
  - INSERT `transaction.trans_history_of_changes` (ChangeType='E')
  - Final: UPDATE `otorisasi.submission` status='AUTHORIZED'

### Validasi & Error Handling

- [ ] **Parse**: File format, cell B2 tidak kosong, rows mulai row 8, cek duplikat batch_period_desc
- [ ] **Amount handling**: Nilai di XLS negatif → dikali -1 (normal jadi positif)
- [ ] **FundEntity mapping**: Zakat=1, Infaq/AnakAsuh/AnakYatim/Qurban=2, Wakaf=3 (SKIP)
- [ ] **Discriminator fields**: transactioncode='SD002', channelcode='A', prefix 'BPZIS', account_ti_type='D'/'C', donor_group='R', donor_type='I', donor_no prefix='P'
- [ ] **Limit check**: Jika ada limit entity transaksi di `otorisasi.entity_limit`, cek `grand_total` saat parse (validate preview)
- [ ] **Parameter cek**: BANKZAKAT, BANKINFAQ, BANKASUH, BANKYATIM, BANKQURBAN harus semua exist, jika tidak → error

### Registrasi di Main

- [ ] Daftarkan router di `apps_zakat/api-python/app/main.py`
- [ ] Daftarkan dispatcher di `apps_zakat/api-python/app/modules/otorisasi/service.py:_register_defaults()`

---

## Layer 2 (Parallel) — Seed Menu & Role (nuwis-seed-gen, haiku)

Lokasi: `infra/db/migrations/seed/`

- [ ] `infra/db/migrations/seed/menu-zis-upload-zakat.sql`
  - INSERT `isf_auth.menu` (3 rows):
    1. `transaksi.upload` (parent group) — jika belum ada
    2. `transaksi.upload.zis-rutin` — "Upload Data Penerimaan ZIS Rutin"
    3. `transaksi.upload.zis-rutin-list` — "List Upload Data Penerimaan ZIS Rutin"
  - INSERT `isf_auth.role_menu` (rows × roles):
    - ACC role: akses `transaksi.upload.zis-rutin` + `transaksi.upload.zis-rutin-list`
    - SPVKEU role: akses `keuangan.monitoring.otorisasi` (sudah ada)

**Verifikasi 3-way consistency**:
- Menu key di `lib/menu/registry.ts` (Vue)
- Route `meta.menu_key` di `router/index.ts` (Vue)
- Seed SQL menu rows (Auth DB)

**Apply setelah selesai**:
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/menu-zis-upload-zakat.sql
```

---

## Layer 3 — BFF (nuwis-bff-builder, haiku)

Lokasi: `apps_zakat/bff-api/app/routers/`

- [ ] `apps_zakat/bff-api/app/routers/transaksi.py` — proxy routes
  - [ ] `POST /api/transaksi/upload/hc-zis/parse` — auth + multipart file handling, proxy ke api-python
  - [ ] `POST /api/transaksi/upload/hc-zis/submit` — auth + require_menu, inject branch_id + inputer_id, proxy
  - [ ] `GET /api/transaksi/upload/hc-zis/batches` — auth + pagination params
  - [ ] `GET /api/transaksi/upload/hc-zis/batches/{batch_id}` — auth
  - [ ] `PUT /api/transaksi/upload/hc-zis/batches/{batch_id}/date` — auth + require_menu, inject session
  - [ ] `DELETE /api/transaksi/upload/hc-zis/batches/{batch_id}` — auth + require_menu, inject session

- [ ] Daftarkan router di `apps_zakat/bff-api/app/main.py`

**Pattern**:
- Auth decorator `@require_menu("transaksi.upload.zis-rutin")`
- Session injection `_resolve_branch` → branch_id
- Session injection `security_context.user_id` → inputer_id
- Proxy via `api_client.post/get/put/delete`
- Handle response shape: `{data: {...}, meta: {...}}`

---

## Layer 4 — UI (nuwis-ui-builder, haiku)

Lokasi: `apps_zakat/web-vue/src/`

### Pages

- [ ] `pages/transaksi/UploadHCZisPage.vue`
  - File picker input + DateField TanggalTransaksi
  - Button "Proses Baca File" → `POST /api/transaksi/upload/hc-zis/parse`
  - Show totals summary (BatchPeriodDesc + tabel 2-kolom)
  - Show preview DataTable (lazy, read-only)
  - Button "Simpan" → `POST /api/transaksi/upload/hc-zis/submit` (save-and-submit)
  - Async loading state + error toast

- [ ] `pages/transaksi/UploadHCZisListPage.vue`
  - Toolbar (search BatchPeriodDesc + date range filter)
  - Standalone Paginator di atas (default 25 rows)
  - DataTable lazy (columns: BatchPeriodDesc, TanggalTransaksi, UploadUserId, StatusOtorisasi, GrandTotal, GrandCount)
  - Row actions: [View] → Drawer, [Edit Tanggal] → Modal, [Hapus] → Modal
  - Showing X–Y of Z records

### Drawers / Modals / Components

- [ ] `components/transaksi/UploadHCZisDetailDrawer.vue`
  - Slide panel header + detail batch info
  - DataTable items (read-only)

- [ ] `components/transaksi/UploadHCZisUpdateDateModal.vue`
  - Read-only: BatchPeriodDesc, old date
  - Editable: DateField new date
  - Button "Simpan" → `PUT /api/transaksi/upload/hc-zis/batches/{id}/date`

- [ ] `components/transaksi/UploadHCZisDeleteModal.vue`
  - Read-only form: BatchPeriodDesc, TanggalTransaksi, totals summary
  - Confirm message
  - Button "Hapus" → `DELETE /api/transaksi/upload/hc-zis/batches/{id}`

### Router Entry

- [ ] `router/index.ts`: Tambah 2 named routes
  ```ts
  {
    path: '/transaksi/upload/zis-rutin',
    name: 'UploadHCZis',
    component: () => import('@/pages/transaksi/UploadHCZisPage.vue'),
    meta: { menu_key: 'transaksi.upload.zis-rutin' }
  },
  {
    path: '/transaksi/upload/zis-rutin/list',
    name: 'UploadHCZisList',
    component: () => import('@/pages/transaksi/UploadHCZisListPage.vue'),
    meta: { menu_key: 'transaksi.upload.zis-rutin-list' }
  }
  ```

### Menu Registry

- [ ] `lib/menu/registry.ts`: Tambah 2 menu keys
  ```ts
  export const MENU_KEYS = {
    // ... existing ...
    'transaksi.upload.zis-rutin': 'Upload Data Penerimaan ZIS Rutin',
    'transaksi.upload.zis-rutin-list': 'List Upload Data Penerimaan ZIS Rutin',
  }
  ```

### Sidebar Entry (AppSidebar.vue)

- [ ] Verifikasi "Transaksi → Upload" menu group ada
- [ ] Tambah 2 child items:
  - Icon: Upload icon (lucide)
  - Label: "Upload Data Penerimaan ZIS Rutin"
  - Route: `/transaksi/upload/zis-rutin`
  - Menu key: `transaksi.upload.zis-rutin`
  - (List item optional atau bersembunyi, hanya akses dari halaman utama)

### Styling & Components

- [ ] Gunakan `vue-primevue-zakat-ui` conventions:
  - Pagination standalone di atas table
  - DateField.vue untuk semua date input (v-model = ISO string)
  - SearchSelect.vue untuk long dropdowns (jika ada)
  - Tailwind v4 classes, no inline styles
  - Lucide icons (bukan PrimeIcons)
  - PrimeVue unstyled mode + reka-ui for buttons/inputs

---

## Layer 5 — Test (nuwis-test-gen, haiku)

- [ ] `testing/e2e-upload-zis-rutin.sh` — smoke test template (curl-based)
  - Login sebagai ACC user
  - Upload XLS file (sample)
  - Parse preview
  - Submit ke otorisasi
  - (As SPVKEU) Approve otorisasi
  - Polling untuk check status AUTHORIZED
  - Verify data di DB (batch items, transaksi dibuat, jurnal dibuat)
  - (Optional) Delete batch

- [ ] `apps_zakat/api-python/tests/test_transaksi_hc_zis.py` (jika logic kompleks)
  - Unit test openpyxl parse
  - Unit test dispatcher (create, delete, update date)
  - Mock DB calls

---

## Verifikasi Sebelum Go-Live

```bash
# Step 1: Restart containers setelah Layer 1 selesai
cd infra
podman-compose -f docker-compose.zakat.yml restart api-python

# Step 2: Verify DB tables exist
psql -U transaction -d mziss_laz -c "\dt transaction.humancapital*"

# Step 3: Verify seed applied
psql -U transaction -d isf_auth_zakat -c "SELECT menu_key, label FROM isf_auth.menu WHERE menu_key LIKE 'transaksi.upload.zis%';"

# Step 4: Restart BFF + Web setelah Layer 3, 4 selesai
podman-compose -f docker-compose.zakat.yml restart bff-api web-vue

# Step 5: Login manual di browser
# http://localhost:5173 → login sebagai ACC user
# Navigasi ke menu "Transaksi → Upload → Upload Data Penerimaan ZIS Rutin"

# Step 6: Jalankan E2E test
bash testing/e2e-upload-zis-rutin.sh

# Step 7: Manual test di browser
# - Upload file XLS, verify parse output
# - Submit, cek otorisasi status = PENDING
# - Login sebagai SPVKEU, approve di halaman Otorisasi
# - Polling, verifikasi status = AUTHORIZED
# - Cek data batch + items + transaksi dibuat di DB
# - Cek jurnal dibuat
# - Test delete batch
# - Test update tanggal
```

- [ ] E2E script passed
- [ ] Manual browser test passed (upload, parse, submit, approve, authorize)
- [ ] DB data verified (batch, items, transaksi, jurnal)
- [ ] Otorisasi workflow (DRAFT → PENDING → AUTHORIZED)
- [ ] Background dispatcher tidak error
- [ ] Delete + rollback balance bekerja
- [ ] Update tanggal mengubah jurnal period
- [ ] Menu keys accessible sesuai role

---

## Catatan Penting Implementasi

1. **openpyxl parse**: Gunakan bukan pyFlexcel. Cell B2 untuk BatchPeriodDesc, rows mulai row 8, negate amount.
2. **SQL batch untuk donor**: Performa kritis — jangan loop ORM per-row.
3. **Temp table untuk delete**: `SELECT FOR UPDATE NOWAIT` + balance reverse mandatory.
4. **Journal period update**: `fl_accountingperiode` + `fl_accountingyear` harus ikut saat update tanggal.
5. **Discriminators kritis**: SD002, A, BPZIS, D/C, FundEntity 1/2/3, R/I/P prefix, T flag.
6. **Background task async**: Return PROCESSING segera, eksekusi dispatcher belakangan.
7. **Parameter global**: BANKZAKAT, BANKINFAQ, BANKASUH, BANKYATIM, BANKQURBAN wajib terisi.
8. **Wakaf skip**: Field ada tapi amount tidak menghasilkan transaksi.
9. **Session injection**: branch_id + inputer_id dari BFF, bukan frontend.
10. **Pagination**: Standalone Paginator, DataTable lazy, never built-in paginator.

---

## Timeline Estimasi

(Bergantung parallelisasi layer):

- **Layer 1 (DB)**: 2 jam (migrasi + index)
- **Layer 2 (Python + Seed)**: 8 jam (parse service kompleks, dispatcher multi-step, seed SQL)
- **Layer 3 (BFF)**: 2 jam (proxy routes)
- **Layer 4 (UI)**: 6 jam (5 components, file picker, modals, loader states)
- **Layer 5 (Test)**: 2 jam (E2E script + pytest)
- **Verifikasi**: 4 jam (manual testing, DB validation, workflow testing)

**Total**: ~20 jam development + testing

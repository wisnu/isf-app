# Plan: Pengembalian Realisasi Program
**Dibuat**: 2026-06-22
**Target Portal**: zakat
**Legacy Ref**: `docs/legacy-apps/program/QRealizationReturn` + `fRealizationReturn`

## Urutan Eksekusi

Layer 1 (DWH) dan Layer 2 (Seed) bisa paralel.
Layer 3 (api-python) dan Layer 4 (BFF) saling dependent — harus berurutan.
Layer 5 (UI) bisa mulai saat Layer 3 selesai (endpoint siap).
Layer 6 (E2E Test) paling akhir.

---

## Layer 1 — DWH (nuwis-db-migrator, haiku)

- [ ] `infra/db/migrations/dwh/v_realization_return.sql` — DWH view untuk laporan pengembalian realisasi program
  - Kolom: return_id, return_date, return_description, realization_id, realization_date, total_realization, total_return, total_cost, branch_code, status (dari otorisasi.submission)
  - Join: `program.realizationreturn` ← `otorisasi.submission` (entity_type='realization_return') — ambil status dari submission

**Catatan**: Tabel `program.realizationreturn`, `program.realizationreturndetail`, `program.realizationcost` sudah ada, tidak perlu migration baru.

---

## Layer 2 — Seed (nuwis-seed-gen, haiku)

- [ ] `infra/db/migrations/seed/menu-realization-return.sql` — daftarkan menu keys & role_menu
  - Menu level 3: `distribution.realization-return.list` → parent `distribution.penyaluran`
  - Assign ke roles: DIST, SPVDIST (list), DIST (add/edit/delete)
  - Otorisasi entity_config: entity_type='realization_return', max_amount=NULL (no limit check), limit_approval_level=NULL

**Apply setelah selesai**:
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/menu-realization-return.sql
```

---

## Layer 3 — Python API (nuwis-python-builder, haiku)

Target path: `apps_zakat/api-python/app/modules/distribution/`

- [ ] `realization_return_schema.py` — Pydantic schemas
  - `RealizationReturnDetailIn` — detail form grid (realization_detail_id, return_amount, detail_description)
  - `RealizationReturnCostIn` — cost form grid (cost_item_id, cost_amount, additional_description)
  - `RealizationReturnIn` — POST body (return_date, return_description, realization_id, cost_amount, details[], costs[])
  - `RealizationReturnOut` — GET response (id, return_date, ..., details[], costs[], status)

- [ ] `realization_return_repo.py` — Database queries
  - `get_realization_return_list(page, limit, search, realization_id, branch_id)` — list with pagination
  - `get_realization_return_by_id(id, branch_id)` — get detail + embedded details[] & costs[]
  - `get_realization_details(realization_id, branch_id)` — fetch realization header + details (untuk populate form saat pilih)
  - `check_realization_return_exists(realization_id, branch_id)` — guard: cek apakah realisasi sudah ada pengembalian
  - `create_realization_return(payload)` — INSERT + details + costs
  - `update_realization_return(id, payload)` — UPDATE (guard: only if DRAFT)
  - `delete_realization_return(id)` — DELETE (guard: only if DRAFT)

- [ ] `realization_return_service.py` — Business logic
  - `list_realization_returns(page, limit, search, realization_id, branch_id)` → list dari repo
  - `get_realization_return(id, branch_id)` → detail dari repo
  - `get_realization_details(realization_id, branch_id)` → untuk dialog pilih realisasi
  - `create_realization_return(payload, branch_id, input_user)` → validasi + INSERT otorisasi.submission (entity_type='realization_return', status='PENDING')
  - `update_realization_return(id, payload, branch_id)` → validasi + UPDATE (guard DRAFT)
  - `delete_realization_return(id, branch_id)` → DELETE (guard DRAFT)
  - `create_from_payload(submission_payload)` — **dispatcher untuk otorisasi** → INSERT realizationreturn + details + costs + create transaction (DD002)
  - `validate_realization_return(payload, realization)` → cek ReturnDate ≥ RealizationDate, TotalReturn + TotalCost == TotalRealization, ReturnAmount per baris

- [ ] `realization_return_router.py` — FastAPI routes
  - `GET /api/distribution/realization-return` → list
  - `GET /api/distribution/realization-return/{id}` → detail
  - `GET /api/distribution/realization-return/realization/{id}/details` → untuk dialog
  - `POST /api/distribution/realization-return` → save-and-submit (masuk otorisasi)
  - `PUT /api/distribution/realization-return/{id}` → update (guard DRAFT)
  - `DELETE /api/distribution/realization-return/{id}` → delete (guard DRAFT)
  - `GET /api/distribution/cost-items` → lookup cost items

- [ ] Daftarkan router di `apps_zakat/api-python/app/main.py`
  - `from app.modules.distribution.realization_return_router import router as rr_router`
  - `app.include_router(rr_router)`

- [ ] Daftarkan dispatcher di `apps_zakat/api-python/app/modules/otorisasi/service.py:_register_defaults()`
  - Tambah entry ke dispatcher registry: `'realization_return': ('distribution', realization_return_service.create_from_payload)`

- [ ] `cost_items_repo.py` + `cost_items_service.py` (jika belum ada)
  - Endpoint lookup GET `/api/distribution/cost-items` untuk dropdown di form

**Test**: `apps_zakat/api-python/tests/test_distribution_realization_return.py`
- Test list, get, create, update, delete
- Test validation: ReturnDate ≥ RealizationDate, TotalReturn + TotalCost == TotalRealization
- Test guard: tidak bisa edit/delete jika PENDING/AUTHORIZED

---

## Layer 4 — BFF (nuwis-bff-builder, haiku)

Target path: `apps_zakat/bff-api/app/routers/distribution.py`

- [ ] Route proxy untuk semua endpoint api-python
  - `GET /api/distribution/realization-return` → proxy ke api-python (with _resolve_branch)
  - `GET /api/distribution/realization-return/{id}` → proxy ke api-python (with _resolve_branch)
  - `GET /api/distribution/realization-return/realization/{id}/details` → proxy ke api-python
  - `POST /api/distribution/realization-return` → inject branch_id + input_user dari session, proxy (save-and-submit)
  - `PUT /api/distribution/realization-return/{id}` → inject branch_id, proxy
  - `DELETE /api/distribution/realization-return/{id}` → proxy
  - `GET /api/distribution/cost-items` → proxy ke api-python

- [ ] Dekorator `require_menu('distribution.realization-return.list')` di semua endpoint

- [ ] Helper `_resolve_branch(session, id)` — validate branch access (guard against cross-branch access)

**Test**: manual via curl atau E2E script

---

## Layer 5 — UI (nuwis-ui-builder, haiku)

Target path: `apps_zakat/web-vue/src/modules/distribution/`

- [ ] Menu key registry — `shared/constants/menu-keys.ts`
  - Tambah: `DISTRIBUTION_REALIZATION_RETURN_LIST = 'distribution.realization-return.list'`
  - Tambah: `DISTRIBUTION_REALIZATION_RETURN_ADD = 'distribution.realization-return.add'`
  - Tambah: `DISTRIBUTION_REALIZATION_RETURN_EDIT = 'distribution.realization-return.edit'`
  - Tambah: `DISTRIBUTION_REALIZATION_RETURN_DELETE = 'distribution.realization-return.delete'`

- [ ] Route — `modules/distribution/routes.ts`
  - Tambah route `/distribution/realization-return` → `RealizationReturnListView.vue`
  - Tambah route `/distribution/realization-return/create` → `RealizationReturnFormView.vue` (mode: create)
  - Tambah route `/distribution/realization-return/:id/edit` → `RealizationReturnFormView.vue` (mode: edit)
  - Meta: `{ domain: 'distribution', menu_key: 'distribution.realization-return.list' }`

- [ ] Sidebar — `modules/distribution/menu.ts` (DomainConfig)
  - Parent group: `penyaluran` (sudah ada)
  - Child item baru: `realization-return` → label "Pengembalian Realisasi", path `/distribution/realization-return`

- [ ] `components/SearchRealizationDialog.vue` — Dialog untuk pilih realisasi
  - Input: search filter (realization_description, memo_number)
  - Guard: hanya tampilkan realisasi dengan status AUTHORIZED yang belum ada pengembalian
  - Output: emit realization object + detail rows

- [ ] `views/RealizationReturnListView.vue` — List page
  - Struktur: Toolbar (search, filter, add button) + Paginator (top) + DataTable
  - Kolom: return_date, realization_description, total_return, status (from otorisasi), actions (view/edit/delete)
  - Edit/Delete hanya enabled jika status == DRAFT
  - Loading state, error handling, empty state

- [ ] `views/RealizationReturnFormView.vue` — Form page (create & edit)
  - Tab 1: "Pilih Realisasi" — SearchRealizationDialog untuk select realization
  - Tab 2: "Detail Pengembalian" — auto-fill header + detail grid (readonly columns: realization_detail_id, mustahiq_product_name, customer_name, account_name, realization_amount)
    - Editable columns: return_amount (numeric, ≤ realization_amount), detail_description
    - Grid tidak bisa tambah/hapus rows, only fill
  - Tab 3: "Rincian Biaya" — cost items grid (add/edit/remove enabled)
    - Columns: cost_item_code (SearchSelect lookup), cost_item_description (readonly), cost_amount, additional_description
  - Footer: validation message (TotalReturn + TotalCost == TotalRealization), buttons (Cancel, Save, Submit otorisasi)
  - Mode create: show "Simpan & Kirim Otorisasi" button → POST (save-and-submit)
  - Mode edit: show "Simpan" (if DRAFT) + "Hapus" (if DRAFT)
  - Async feedback: loading toast, success/error toast

- [ ] `views/RealizationReturnDetailView.vue` (optional) — Detail read-only page
  - Tampilkan semua data + status dari otorisasi.submission
  - Jika PENDING/PROCESSING: show status badge + "Menunggu persetujuan" message
  - Jika AUTHORIZED: show approval date + auth_user

- [ ] Type definitions — `types/distribution.ts`
  - `RealizationReturn`, `RealizationReturnDetail`, `RealizationReturnCost` interfaces

**CSS/Styling**: Tailwind v4 + reka-ui buttons + PrimeVue unstyled components (DataTable, Dialog, etc.)

---

## Layer 6 — Test (nuwis-test-gen, haiku)

- [ ] `testing/e2e-realization-return.sh` — smoke test script (curl-based)
  - Scenario 1: Login DIST → list realization-return → filter by realization
  - Scenario 2: Pilih realisasi yang belum ada return → auto-fill detail grid
  - Scenario 3: Isi return_amount + cost → validasi total == realisasi → submit (save-and-submit)
  - Scenario 4: Cek submission masuk antrian otorisasi (status PENDING)
  - Scenario 5: Login SPVDIST → approve submission → cek status berubah AUTHORIZED
  - Scenario 6: Cek realization_return + realization_returndetail + realization_cost inserted
  - Scenario 7: Cek jurnal DD002 created di program.transaction
  - Scenario 8: Delete realization-return (hanya bisa jika DRAFT)

**Apply setelah semua layer selesai**:
```bash
bash testing/e2e-realization-return.sh
```

---

## Verifikasi Keseluruhan

```bash
# 1. Restart container setelah semua layer selesai
cd infra && podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue

# 2. Jalankan E2E smoke test
bash testing/e2e-realization-return.sh

# 3. Manual testing di browser
# - Login sebagai DIST (user: DIST, password: test1234)
# - Navigasi ke /distribution/realization-return
# - Klik "Tambah"
# - Pilih realisasi dari dialog
# - Isi return_amount, cost
# - Klik "Simpan & Kirim Otorisasi"
# - Login sebagai SPVDIST
# - Pergi ke /keuangan/monitoring/otorisasi
# - Cari submission entity_type='realization_return'
# - Approve
# - Cek status berubah AUTHORIZED

- [ ] E2E passed
- [ ] Manual test: CRUD dari UI berhasil
- [ ] Manual test: Otorisasi 2-tahap (DIST submit → SPVDIST approve)
- [ ] Manual test: Jurnal DD002 tercipta di program.transaction
- [ ] Manual test: Realisasi yang sudah ada return tidak bisa diubah (guard aktif)
```

---

## Dependency Checklist

Pastikan sebelum mulai implementasi:

- [ ] Tabel `program.realizationreturn`, `program.realizationreturndetail`, `program.realizationcost` sudah ada di `mziss_laz` (verify dengan DBA)
- [ ] `otorisasi.submission` + `otorisasi.entity_config` sudah ada (dari feature otorisasi sebelumnya)
- [ ] Endpoint list realisasi `/api/distribution/realization` sudah siap (untuk SearchRealizationDialog)
- [ ] Menu hierarchy `distribution.penyaluran` (parent) sudah ada di seed
- [ ] Role DIST + SPVDIST sudah ada di `isf_auth_zakat.role`

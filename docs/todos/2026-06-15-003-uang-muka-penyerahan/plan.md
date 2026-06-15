# Plan: Transaksi Penyerahan Uang Muka

**Dibuat**: 2026-06-15
**Target Portal**: zakat
**Fitur Slug**: uang-muka-penyerahan
**Kompleksitas**: Sedang
**Workflow**: Approval (otorisasi maker-checker + auto-limit check)

## Urutan Eksekusi

Layer 1 dan 2 bisa paralel. Layer 3–5 sekuensial (BFF harus tunggu API, UI harus tunggu BFF selesai).

---

## Layer 1 — DB/DWH (nuwis-db-migrator, haiku)

- [ ] `infra/db/migrations/V004__uang-muka-penyerahan-dwh.sql`
  - Buat DWH view `dwh.v_uang_muka_penyerahan` (JOIN transaction + accounttransactionitem + financialaccount + accountreceivable)
  - Filter diskriminator: `transactioncode='CA'`, `accounttitype='C'`, `cattype='D'`, `accountreceivabletype='C'`
  - Include kolom: transaction_id, transaction_no, actual_date, employee_id, employee_name, cash_account_no, amount, auth_status, has_return_trans (LEFT JOIN ke CAReturnTransactItem)
  - Note: Tabel sudah ada — hanya buat view, tidak ada migration tabel baru

**Apply setelah selesai**:
```bash
psql -U transaction -d mziss_laz -f infra/db/migrations/V004__uang-muka-penyerahan-dwh.sql
```

---

## Layer 1.5 — Otorisasi Config (nuwis-seed-gen, haiku)

- [ ] `infra/db/migrations/seed/seed-otorisasi-uang-muka.sql`
  - INSERT ke `otorisasi.entity_config` (entity_type='uang_muka', ...) jika belum ada
  - Deskripsi: "Penyerahan Uang Muka Karyawan"

**Apply setelah selesai**:
```bash
psql -U transaction -d mziss_laz -f infra/db/migrations/seed/seed-otorisasi-uang-muka.sql
```

---

## Layer 2 — Python API (nuwis-python-builder, haiku)

- [ ] `apps_zakat/api-python/app/modules/transaksi/__init__.py` — pastikan package init sudah ada
- [ ] `apps_zakat/api-python/app/modules/transaksi/uang_muka_schema.py`
  - Pydantic models:
    - `CreateUangMukaRequest` (actual_date, employee_id, cash_account_no, amount, reference_no, description, received_from, budget_id, real_memo_id)
    - `UpdateUangMukaRequest` (subset field yg bisa diupdate)
    - `UangMukaResponse` (response shape dari GET)
    - `UangMukaListResponse` (rows + pagination)
  - Validators: amount > 0, employee_id & cash_account_no tidak boleh kosong

- [ ] `apps_zakat/api-python/app/modules/transaksi/uang_muka_service.py`
  - Import dari `modules.otorisasi.service` — `save_and_submit` function
  - Fungsi-fungsi:
    - `list_uang_muka(pool, user_id, branch_code, page, limit, filters)` — query dwh.v_uang_muka_penyerahan dengan pagination
    - `get_uang_muka_detail(pool, transaction_id)` — select + check `has_return_trans` (cek apakah ada CAReturnTransactItem)
    - `create_uang_muka_submission(pool, user_id, branch_code, payload)` — call `save_and_submit` dgn entity_type='uang_muka'
    - `update_uang_muka_submission(pool, submission_id, payload)` — update otorisasi.submission jika status DRAFT/REJECTED
    - `delete_uang_muka_submission(pool, submission_id)` — soft/hard delete jika DRAFT/REJECTED
    - `create_uang_muka_from_payload(pool, payload)` — **dispatcher** — called saat AUTHORIZED:
      - Auto-create EmployeeCashAdvance jika belum ada (INSERT ke ACCOUNTRECEIVABLE with accountreceivabletype='C')
      - INSERT transaction record (transactioncode='CA')
      - INSERT 2 transaction items (debit UM karyawan, kredit kas/bank) dengan accounttitype='C', cattype='D'
      - INSERT CASHADVANCEMEMOINFO jika real_memo_id != 0
      - CREATE journal entries (debit & kredit)
      - Return transaction_id, transaction_no
    - `lookup_employee(pool, search, branch_code)` — SELECT dari employee/personalia tabel
    - `lookup_cash_account(pool, branch_code, search)` — SELECT dari CashAccount dengan tipe aktif
    - `lookup_budget(pool, search, actual_date)` — SELECT dari budget tabel yg aktif pada actual_date

- [ ] `apps_zakat/api-python/app/modules/transaksi/uang_muka_router.py`
  - POST /api/transaksi/uang-muka/ (require_menu, _resolve_branch, call save_and_submit)
  - PUT /api/transaksi/uang-muka/{id} (require_menu.ubah, update submission)
  - GET /api/transaksi/uang-muka/ (require_menu, list dengan filter & pagination)
  - GET /api/transaksi/uang-muka/{id} (require_menu, detail + has_return_trans)
  - DELETE /api/transaksi/uang-muka/{id} (require_menu.hapus, soft delete DRAFT/REJECTED)
  - GET /api/lookup/employee (require_menu, SearchSelect data)
  - GET /api/lookup/cash-account (require_menu, SearchSelect data)
  - GET /api/lookup/budget (require_menu, SearchSelect data)

- [ ] `apps_zakat/api-python/app/modules/otorisasi/service.py`
  - Daftarkan dispatcher di `_register_defaults()` function:
    ```python
    dispatcher_registry['uang_muka'] = uang_muka_service.create_uang_muka_from_payload
    ```
  - Import: `from modules.transaksi import uang_muka_service`

- [ ] `apps_zakat/api-python/app/main.py`
  - Tambahkan: `from modules.transaksi import uang_muka_router`
  - Include router: `app.include_router(uang_muka_router.router, prefix="/api/transaksi", tags=["transaksi"])`

---

## Layer 3 — BFF (nuwis-bff-builder, haiku)

- [ ] `apps_zakat/bff-api/app/routers/uang_muka.py`
  - Proxy routes ke api-python:
    - POST /api/transaksi/uang-muka/ → inject session user_id, branch_code, fund_entity=4
    - PUT /api/transaksi/uang-muka/{id} → same inject
    - GET /api/transaksi/uang-muka/ → forward query params
    - GET /api/transaksi/uang-muka/{id} → forward id
    - DELETE /api/transaksi/uang-muka/{id} → forward id
    - GET /api/lookup/employee → forward query, inject branch_code
    - GET /api/lookup/cash-account → forward query, inject branch_code
    - GET /api/lookup/budget → forward query
  - Auth decorator: `require_menu("keuangan.transaksi.uang-muka-penyerahan")`
  - Note: fund_entity=4 ditambah di BFF saat inject payload, atau di API saat create?
    → Recommendation: API handle di uang_muka_service.create_uang_muka_submission() → set di payload sebelum save_and_submit

- [ ] `apps_zakat/bff-api/app/main.py`
  - Tambahkan: `from app.routers import uang_muka`
  - Include router: `app.include_router(uang_muka.router, prefix="/api", tags=["transaksi"])`

---

## Layer 4 — Seed (nuwis-seed-gen, haiku)

- [ ] `infra/db/migrations/seed/seed-menu-uang-muka-penyerahan.sql`
  - INSERT ke `isf_auth.menu` (keuangan.transaksi.uang-muka-penyerahan, label='Penyerahan Uang Muka')
  - INSERT ke `isf_auth.role_menu` (assign ke role 'ACC')
  - Verifikasi 3-way consistency dengan registry.ts + router meta.menu_key

**Apply setelah selesai**:
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-menu-uang-muka-penyerahan.sql
```

---

## Layer 5 — UI (nuwis-ui-builder, haiku)

- [ ] `apps_zakat/web-vue/src/lib/menu/registry.ts`
  - Tambahkan: `'keuangan.transaksi.uang-muka-penyerahan': { label: 'Penyerahan Uang Muka', parent: 'keuangan.transaksi', action: 'tambah' }`

- [ ] `apps_zakat/web-vue/src/router/index.ts`
  - Tambahkan route:
    ```ts
    {
      path: '/keuangan/transaksi/uang-muka-penyerahan',
      component: () => import('@/pages/keuangan/UangMukaPenyerahanPage.vue'),
      meta: {
        layout: 'AppLayout',
        menu_key: 'keuangan.transaksi.uang-muka-penyerahan',
        title: 'Penyerahan Uang Muka'
      }
    }
    ```

- [ ] `apps_zakat/web-vue/src/components/AppSidebar.vue`
  - Cari menu group "Transaksi" (anak dari "Keuangan")
  - Tambahkan entry:
    ```html
    <li v-if="hasMenuAccess('keuangan.transaksi.uang-muka-penyerahan')">
      <RouterLink to="/keuangan/transaksi/uang-muka-penyerahan">
        Penyerahan Uang Muka
      </RouterLink>
    </li>
    ```

- [ ] `apps_zakat/web-vue/src/pages/keuangan/UangMukaPenyerahanPage.vue`
  - Komponen 2-tab atau toggle: TAB LIST (histori) + TAB FORM (input baru)
  - TAB LIST:
    - Toolbar: SearchSelect employee, DateField begin_date/end_date, Select return_status, Button Tampilkan
    - Pagination (standalone, top-placed)
    - DataTable: columns = transaction_no, actual_date, employee_name, cash_account_name, amount, auth_status (badge), has_return_trans
    - Actions: Klik row → drawer detail (read-only atau edit if DRAFT/REJECTED), Klik Edit button → form edit, Delete button (soft/hard)
    - Auto-refresh bila ada submission dengan status PROCESSING (5s interval, polling)
  - TAB FORM:
    - Sections:
      - pTransaction (utama):
        - actual_date: DateField.vue (required, editable)
        - cash_account: SearchSelect.vue (required, /api/lookup/cash-account, readonly if has_return_trans)
        - employee: SearchSelect.vue (required, /api/lookup/employee, readonly if has_return_trans)
        - amount: Input type=number (required, > 0, readonly if has_return_trans)
        - reference_no: Input (optional)
        - description: Textarea (optional)
        - received_from: Input (optional, default = logged-in user)
      - pMemo (optional):
        - real_memo_number: Input (readonly, dari dialog pencarian)
        - real_memo_subject: Input (readonly)
        - real_memo_date: Input (readonly)
      - pBudget (optional):
        - budget_code: Input (readonly)
        - budget_owner: Input (readonly)
    - Buttons:
      - Simpan (POST /api/transaksi/uang-muka/)
      - Perbarui (PUT /api/transaksi/uang-muka/{id}, if DRAFT/REJECTED)
      - Batalkan (DELETE /api/transaksi/uang-muka/{id}, if DRAFT/REJECTED)
      - Bersihkan (clear form for new entry)
    - Feedback:
      - Loading spinner saat POST/PUT
      - Success toast: "Uang Muka berhasil disimpan. Status: [PENDING|AUTHORIZED]"
      - Error toast dengan detail message
      - Jika PENDING: "Menunggu approval supervisor" (badge kuning)
      - Jika AUTHORIZED: "Sudah tercatat di sistem" (badge hijau)
  - CSS: Tailwind v4 + PrimeVue unstyled + reka-ui untuk button/input primitives
  - Icons: Lucide (not PrimeIcons)

---

## Layer 6 — Test (nuwis-test-gen, haiku)

- [ ] `testing/e2e-uang-muka-penyerahan.sh`
  - Smoke test curl-based:
    - POST /api/transaksi/uang-muka (create)
    - GET /api/transaksi/uang-muka (list)
    - GET /api/transaksi/uang-muka/{id} (detail)
    - PUT /api/transaksi/uang-muka/{id} (update if DRAFT)
    - GET /api/lookup/employee (lookup)
    - GET /api/lookup/cash-account (lookup)
  - Scenarios:
    - Happy path: create AUTHORIZED (amount <= limit)
    - Create PENDING (amount > limit)
    - Update DRAFT → PENDING
    - Delete DRAFT
    - Check has_return_trans disables edit

- [ ] `apps_zakat/api-python/tests/test_uang_muka.py` (opsional — jika logic kompleks)
  - Unit test untuk dispatcher create_uang_muka_from_payload
  - Test auto-create EmployeeCashAdvance
  - Test limit check logic
  - Test discriminator queries (accounttitype='C', cattype='D')

---

## Verifikasi

```bash
# 1. Migrasi DB selesai
psql -U transaction -d mziss_laz -c "SELECT COUNT(*) FROM dwh.v_uang_muka_penyerahan;"

# 2. Rebuild images (jika ada pyproject.toml/package.json changes)
cd infra && podman build --security-opt label=disable -t isf-zakat-api-python:dev apps_zakat/api-python
cd infra && podman build --security-opt label=disable -t isf-zakat-bff-api:dev apps_zakat/bff-api
cd infra && podman build --security-opt label=disable -t isf-zakat-web-vue:dev apps_zakat/web-vue

# 3. Restart container
cd infra && podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue

# 4. Jalankan E2E smoke test
bash testing/e2e-uang-muka-penyerahan.sh

# 5. Manual verification di browser
# - Login dengan role ACC (e.g., HADI)
# - Navigasi ke Keuangan > Transaksi > Penyerahan Uang Muka
# - Buat transaksi baru (amount <= limit → auto AUTHORIZED, > limit → PENDING)
# - List transaksi → verify pagination, filter, status badge
# - Detail transaksi → verify has_return_trans disables edit
# - Edit transaksi (DRAFT/REJECTED) → verify fields & changes
```

- [ ] E2E smoke test passed
- [ ] Manual test completed:
  - [ ] Login OK, menu visible
  - [ ] Create transaksi OK (AUTHORIZED or PENDING per limit)
  - [ ] List dengan filter & pagination OK
  - [ ] Detail menampilkan has_return_trans status OK
  - [ ] Edit DRAFT/REJECTED OK
  - [ ] Delete DRAFT OK
  - [ ] All toasts + error handling OK
  - [ ] SearchSelect lookups OK (employee, cash-account, budget)

---

## Dependency Notes

- Fitur ini mengandalkan **otorisasi system** sudah diimplementasi (save-and-submit, dispatcher registry)
- Menu seed HARUS sinkron dengan registry.ts + router meta.menu_key (3-way consistency check)
- DWH view MUST filter dengan 4 discriminator: transactioncode='CA', accounttitype='C', cattype='D', accountreceivabletype='C'
- SearchSelect lookups (employee, cash-account) HARUS filter by branch_code dari session
- Test E2E HARUS cover both limit scenarios: <= limit (AUTHORIZED auto) dan > limit (PENDING manual)

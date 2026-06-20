# Plan: Implementasi Transaksi Penerimaan Amil

**Tanggal:** 2026-06-20  
**Berdasarkan Specs:** `docs/todos/2026-06-20-001-penerimaan-amil/specs.md`  
**Status:** In Progress

---

## RINGKASAN

Migrasi fitur input transaksi penerimaan amil (kas masuk pendapatan amil) dari legacy DAF
ke isf-app web-vue. Fitur ini setara dengan `fCashIn` di legacy core module, dengan transaction code `CI`,
accessible oleh role `ACC` (Accountant).

Penerimaan Amil mencatat kas yang masuk ke organisasi sebagai pendapatan operasional amil, via 3 channel:
1. Kas Kecil (Petty Cash)
2. Kas Cabang
3. Bank (channel utama)

---

## URUTAN EKSEKUSI

Implementasi akan dilakukan per layer, dari database → backend API → BFF → Frontend.
Layer 1-3 bisa paralel jika tidak ada dependency; Layer 4-5 tergantung Layer 1-3 selesai.

---

## LAYER 1 — DB / DWH (nuwis-db-migrator, haiku)

**Status:** Pending  
**Model:** Haiku

Tabel utama `transaction.TRANSACTION`, `TRANSACTIONITEM`, `ACCOUNTTRANSACTIONITEM` sudah ada
(dari migrasi penghimpunan dana & penyaluran dana sebelumnya).
Task di layer ini: verifikasi struktur, seed entity_config, dan (optional) buat DWH view.

### Checklist

- [ ] **V###__amil-income-entity-config.sql** — Seed entry ke `otorisasi.entity_config`
  - `entity_type='amil_income'`
  - `dispatcher_module='amil_income_service'`
  - `dispatcher_function='create_from_payload'`
  - `limit_entity='ENTITY_AMIL_INCOME'` (atau per corp config)

- [ ] Verifikasi tabel `transaction.TRANSACTION` kolom:
  - `transactioncode` — untuk filter CI
  - `auth_status` — untuk approval workflow
  - Kolom lain per specs.md (sudah ada dari migrasi sebelumnya)

- [ ] Verifikasi tabel `transaction.TRANSACTIONITEM`:
  - `transaction_item_type` — untuk filter 'G' (GL) dan 'A' (Account)
  - `mutation_type` — untuk 'C' (kredit GL) dan 'D' (debit kas)
  - `parameter_journal_id` — untuk '10' dan 'C20'

- [ ] Verifikasi tabel `transaction.CASHACCOUNT` kolom:
  - `is_amil_account` — **KRITIS** untuk filter dropdown rekening

- [ ] Verifikasi tabel `transaction.TRANSACTIONTYPE` punya row:
  - `transaction_code='CI'`, `voucher_code='KM'`
  - Jika belum ada: INSERT row baru

- [ ] (Optional) Buat DWH view `dwh.v_amil_income`
  - Query: `SELECT * FROM transaction.TRANSACTION t JOIN transaction.TRANSACTIONITEM ti USING (transaction_id) WHERE t.transactioncode='CI' AND ti.transaction_item_type='G'`
  - Digunakan jika ada laporan penerimaan amil di fase mendatang

**Apply Seed:**
```bash
psql -U transaction -d mziss_laz -f infra/db/migrations/V###__amil-income-entity-config.sql
```

---

## LAYER 2 — API PYTHON (nuwis-python-builder, haiku)

**Status:** Pending  
**Model:** Haiku  
**Path:** `apps_zakat/api-python/app/modules/amil_income/`

Buat modul baru untuk handle business logic penerimaan amil.
Dispatcher harus terdaftar di `otorisasi/service.py` untuk maker-checker flow.

### Checklist

- [ ] **router.py**
  - `GET /api/transaction/amil-income` — list dengan filter + pagination
  - `POST /api/transaction/amil-income/save-and-submit` — create + dispatch ke otorisasi
  - `GET /api/transaction/amil-income/{transaction_id}` — detail transaksi
  - `PUT /api/transaction/amil-income/{transaction_id}` — update (DRAFT only)
  - `DELETE /api/transaction/amil-income/{transaction_id}` — delete (DRAFT only)
  - `GET /api/transaction/amil-income/lookup/kas-account` — dropdown rekening bank amil
  - `GET /api/transaction/amil-income/lookup/gl-account` — dropdown GL account (parent 310301)
  - `GET /api/transaction/amil-income/next-number` — nomor transaksi berikutnya

- [ ] **schema.py**
  - Pydantic model: `AmilIncomeCreateRequest` (input form)
  - Pydantic model: `AmilIncomeItemRequest` (per item di grid)
  - Pydantic model: `AmilIncomeResponse` (output response)
  - Pydantic model: `AmilIncomeDetailResponse` (full detail + items)
  - Pydantic model: `KasAccountLookupResponse` (dropdown rekening)
  - Pydantic model: `GLAccountLookupResponse` (dropdown GL account)

- [ ] **service.py**
  - `create_amil_income(req, user_id, branch_code)`:
    - Validasi items tidak kosong
    - Resolve payment type → bank_account_no / cash_type
    - Validate rekening bank punya `is_amil_account='T'`
    - Generate transaction_no format `KM-YYYY-branch-cashCode-seq`
    - INSERT transaction (transactioncode='CI', authstatus='F')
    - INSERT transactionbatch (GetOrCreateBatch)
    - INSERT transactionitem per item:
      - GLTransactionItem (mutationtype='C', parameterjournalid='10')
      - AccountTransactionItem (mutationtype='D', parameterjournalid='10' or 'C20')
    - INSERT otorisasi.submission (entity_type='amil_income')
    - Cek limit automatic approval
    - Return transaction_no + status

  - `get_amil_income_list(date_from, date_to, branch_code, page, limit)`:
    - Query `transaction.TRANSACTION` WHERE transactioncode='CI'
    - Join TRANSACTIONITEM untuk total amount
    - Pagination

  - `get_amil_income_detail(transaction_id)`:
    - Query TRANSACTION + TRANSACTIONITEM + ACCOUNTTRANSACTIONITEM
    - Return full detail dengan items

  - `update_amil_income(transaction_id, req, user_id)`:
    - Check authstatus='F' or DRAFT
    - Delete old items
    - Re-run create logic
    - Return updated transaction

  - `delete_amil_income(transaction_id)`:
    - Check authstatus='F' or DRAFT
    - DELETE transactionitem, accounttransactionitem
    - DELETE transaction
    - DELETE otorisasi.submission (if exists)

  - `get_kas_accounts_lookup(branch_code, payment_type)`:
    - Query CASHACCOUNT WHERE is_amil_account='T' AND status='A'
    - Filter by payment_type jika ada

  - `get_gl_accounts_lookup(branch_code, search)`:
    - Query COA WHERE account_type='I' AND parent_account_code='310301' AND status='A'
    - Optional search filter

  - `get_next_transaction_number(payment_type, branch_code, bank_account_no)`:
    - Lookup voucher_code dari TRANSACTIONTYPE WHERE transactioncode='CI' → 'KM'
    - Resolve cash_code dari rekening
    - Call customidgenAPI dengan prefix "TRANSACTION-KM-{YYYY}-{branch}-{cashCode}"
    - Return formatted number

  - `amil_income_dispatcher(payload)`:
    - **Registered di otorisasi/service.py**
    - Callback saat submission disetujui (AUTHORIZED)
    - INPUT: payload JSONB dari otorisasi.submission
    - Logic:
      - Re-validate items
      - CREATE journal entries (via accounting subsystem)
      - UPDATE financial account balances
      - SET transaction authstatus='T', isposted='T'
    - OUTPUT: { success, transaction_id, journal_no }

- [ ] **repo.py** (jika query kompleks)
  - Raw SQL queries untuk list, detail, lookup
  - Menggunakan asyncpg pool.acquire()

### Notes

- Semua query gunakan CAST(x AS type), bukan x::type
- Pakai `_resolve_branch()` dari BFF untuk single-branch users
- No hardcoding channel_code, parameter_journal_id — di-set di service berdasar payment_type
- Batch handling: `_get_or_create_batch()` internal (tidak di-expose)
- FundAccountNo resolve fallback (opsional untuk MVP)
- Journal posting hanya saat status='AUTHORIZED' (via dispatcher)

---

## LAYER 3 — BFF API (nuwis-bff-builder, haiku)

**Status:** Pending  
**Model:** Haiku  
**Path:** `apps_zakat/bff-api/app/routers/amil_income.py`

Buat router BFF yang proxy ke api-python + auth guard + branch resolution.

### Checklist

- [ ] **amil_income.py**
  - Router untuk semua 8 endpoint (list, create, detail, update, delete, lookup kas, lookup gl, next-number)
  - Auth guard: `require_menu('keuangan.transaksi.penerimaan-amil')`
  - Sub-guards untuk create/update/delete (menu key with .tambah/.ubah/.hapus)
  - Inject `inputer_id` + `branch_id` dari session ke request body (create/update)
  - Call `_resolve_branch(session, req)` untuk single-branch restriction
  - Proxy semua ke `api-python` base URL
  - Handle error: UNAUTHORIZED (401), MENU_DENIED (403), VALIDATION_ERROR (422)

- [ ] **apps_zakat/bff-api/app/main.py**
  - Import & register `amil_income_router`:
    ```python
    from app.routers import amil_income
    app.include_router(amil_income.router, prefix="/api", tags=["amil_income"])
    ```

### Notes

- BFF tidak buat logic bisnis — hanya proxy + auth
- Session data: `inputer_id` dari `request.user.user_id`, `branch_id` dari `request.user.branch_id`
- Jangan panggil api-python `:8000` langsung dari browser — semua via BFF

---

## LAYER 4 — SEED / AUTH (nuwis-seed-gen, haiku)

**Status:** Pending  
**Model:** Haiku  
**Path:** `infra/db/migrations/seed/`

Seed menu entry, role_menu assignment, dan auth config ke `isf_auth_zakat`.

### Checklist

- [ ] **seed-menu-amil-income.sql** atau `seed-auth-menu.sql` (append ke file existing)
  - INSERT `isf_auth.menu`:
    ```sql
    ('keuangan.transaksi.penerimaan-amil', 'Penerimaan Amil', 'keuangan.transaksi', 'cash-in', 'transaksi-penerimaan-amil')
    ('keuangan.transaksi.penerimaan-amil.tambah', 'Tambah', 'keuangan.transaksi.penerimaan-amil', 'plus-circle', null)
    ('keuangan.transaksi.penerimaan-amil.ubah', 'Ubah', 'keuangan.transaksi.penerimaan-amil', 'edit', null)
    ('keuangan.transaksi.penerimaan-amil.hapus', 'Hapus', 'keuangan.transaksi.penerimaan-amil', 'trash', null)
    ```

  - INSERT `isf_auth.role_menu`:
    ```sql
    (role_id='ACC', menu_key='keuangan.transaksi.penerimaan-amil')
    (role_id='ACC', menu_key='keuangan.transaksi.penerimaan-amil.tambah')
    (role_id='ACC', menu_key='keuangan.transaksi.penerimaan-amil.ubah')
    (role_id='ACC', menu_key='keuangan.transaksi.penerimaan-amil.hapus')
    (role_id='SPVACC', menu_key='keuangan.transaksi.penerimaan-amil') — supervisor approve hanya view
    ```

  - **Apply:**
    ```bash
    psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-menu-amil-income.sql
    ```

### Notes

- Menu key consistency: wajib sama di registry.ts, seed, dan route meta.menu_key
- Icon: gunakan lucide icon name ('cash-in', 'plus-circle', dll)
- Parent: 'keuangan.transaksi' untuk menu level utama
- Role assignment: ACC untuk full CRUD, SPVACC untuk view only

---

## LAYER 5 — FRONTEND VUE (nuwis-ui-builder, haiku)

**Status:** Pending  
**Model:** Haiku  
**Path:** `apps_zakat/web-vue/src/`

Buat halaman Vue 3 untuk list dan form input transaksi penerimaan amil.

### Checklist

#### Daftar File Baru

- [ ] **src/pages/transaksi/AmilIncomePage.vue** (list view)
  - Toolbar: date filter (from/to), branch filter (jika branch_access='all'), search
  - Button: "Tambah Transaksi Baru"
  - Pagination: top-placed standalone Paginator (default 25 rows)
  - Table columns: transaction_no, actual_date, bank_account_name, total_amount, status, actions
  - Actions: [Lihat], [Edit (jika draft)], [Hapus (jika draft)]
  - Fetch: GET /api/transaction/amil-income
  - Loading state + error handling

- [ ] **src/pages/transaksi/AmilIncomeFormPage.vue** (create + edit mode)
  - Header section:
    - `actual_date` — DateField.vue [Required]
    - `paid_to` — Input [Optional, pre-fill username]
    - `received_from` — Input [Optional]
  - Payment type tabs:
    - **Tab Kas** (payment_type='K'/'C')
      - `cash_type` — Select [Required, default 'C']
      - `reference_no` — Input [Optional]
      - `description` — Input [Optional]
    - **Tab Bank** (payment_type='B', default active)
      - `bank_account_no` — SearchSelect [Required]
        - Fetch: GET /api/transaction/amil-income/lookup/kas-account
      - `reference_no` — Input [Optional]
      - `description` — Input [Optional]
      - `rate` — Input number [Optional, default 1.0]
  - Grid Detail (uipTransactionItem):
    - Inline editable rows
    - Columns: account_code (lookup), account_name (readonly), amount, cash_account_no (lookup), cash_account_name (readonly), description, fund_product_code (lookup), fund_product_name (readonly)
    - Actions: [Add], [Delete]
    - Validation: account_code required, amount > 0
  - Footer (readonly):
    - `transaction_no` — pre-filled jika edit mode
    - `total_amount` — computed dari sum(items.amount)
  - Buttons: [Simpan & Kirim Persetujuan], [Batal]
  - Async feedback: loading, success toast, error toast

- [ ] **src/lib/menu/registry.ts**
  - Daftarkan 4 menu keys:
    ```typescript
    KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL: 'keuangan.transaksi.penerimaan-amil',
    KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL_TAMBAH: 'keuangan.transaksi.penerimaan-amil.tambah',
    KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL_UBAH: 'keuangan.transaksi.penerimaan-amil.ubah',
    KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL_HAPUS: 'keuangan.transaksi.penerimaan-amil.hapus',
    ```

#### Daftar File Modifikasi

- [ ] **src/router/index.ts**
  - Route untuk list:
    ```typescript
    {
      path: '/keuangan/transaksi/penerimaan-amil',
      name: 'AmilIncome',
      component: () => import('@/pages/transaksi/AmilIncomePage.vue'),
      meta: { menu_key: MENU_KEYS.KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL }
    }
    ```
  - Route untuk form create:
    ```typescript
    {
      path: '/keuangan/transaksi/penerimaan-amil/baru',
      name: 'AmilIncomeCreate',
      component: () => import('@/pages/transaksi/AmilIncomeFormPage.vue'),
      meta: { menu_key: MENU_KEYS.KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL_TAMBAH }
    }
    ```
  - Route untuk form edit (optional):
    ```typescript
    {
      path: '/keuangan/transaksi/penerimaan-amil/:id/edit',
      name: 'AmilIncomeEdit',
      component: () => import('@/pages/transaksi/AmilIncomeFormPage.vue'),
      meta: { menu_key: MENU_KEYS.KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL_UBAH }
    }
    ```

- [ ] **src/components/AppSidebar.vue**
  - Tambah icon import: `import { CashIn } from 'lucide-vue-next'` (atau cash-in icon yg sesuai)
  - Tambah menu entry di sidebar tree (dalam section "Keuangan" > "Transaksi"):
    ```vue
    <li :key="MENU_KEYS.KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL">
      <Link
        :to="{ name: 'AmilIncome' }"
        :icon="CashIn"
        :text="`Penerimaan Amil`"
        :active="sidebarStore.activeMenu === MENU_KEYS.KEUANGAN_TRANSAKSI_PENERIMAAN_AMIL"
      />
    </li>
    ```

### Notes

- Gunakan `vue-primevue-zakat-ui` skill untuk UI patterns
- Pagination: ALWAYS top-placed, NEVER use DataTable paginator
- DateField.vue untuk semua date input (display DD-MM-YYYY, internal ISO)
- SearchSelect.vue untuk dropdown panjang (rekening bank, GL account)
- Async operation: loading state + toast (no alert/confirm)
- Delete: form modal (read-only) + confirm button, bukan inline confirm
- Menu key consistency: lihat registry.ts + route meta.menu_key + seed SQL
- Icon: lucide-vue-next (CashIn atau similar, lihat app sidebar patterns)

---

## LAYER 6 — TESTING (nuwis-test-gen, haiku)

**Status:** Pending  
**Model:** Haiku  
**Path:** `testing/`

Buat E2E smoke test script untuk memverifikasi implementasi.

### Checklist

- [ ] **testing/e2e-amil-income.sh**
  - Setup: login as ACC user (HADI)
  - Test sequence:
    1. GET /api/transaction/amil-income (list empty/with data)
    2. GET /api/transaction/amil-income/lookup/kas-account (dropdown populate)
    3. GET /api/transaction/amil-income/lookup/gl-account (dropdown populate)
    4. POST /api/transaction/amil-income/save-and-submit (create transaksi)
    5. GET /api/transaction/amil-income/{id} (detail created transaksi)
    6. Verify status=PENDING (jika amount > limit) atau AUTHORIZED (jika <= limit)
    7. (Optional) PUT /api/transaction/amil-income/{id} (update if DRAFT)
    8. (Optional) DELETE /api/transaction/amil-income/{id} (delete if DRAFT)
  - Assertions: status codes, response shape, discriminator fields (transactioncode='CI', authstatus, mutation_type)

- [ ] **apps_zakat/api-python/tests/test_amil_income.py** (jika logic kompleks)
  - Unit test per function di service.py
  - Test cases:
    - Create dengan amount <= limit (auto-approve)
    - Create dengan amount > limit (PENDING)
    - Update DRAFT transaksi
    - Delete DRAFT transaksi
    - Validasi items tidak kosong
    - Validasi amount > 0
    - Lookup rekening bank filter is_amil_account='T'
    - Lookup GL account filter account_type='I' AND parent='310301'

### Run Test

```bash
# E2E smoke test
cd /home/wishnew/workshop/isf-app
bash testing/e2e-amil-income.sh

# Unit tests (jika ada)
cd apps_zakat/api-python
pytest tests/test_amil_income.py -v
```

---

## VERIFIKASI FINAL

Setelah semua layer selesai:

```bash
# 1. Rebuild & restart containers
cd infra
podman-compose -f docker-compose.zakat.yml down
podman-compose -f docker-compose.zakat.yml up -d

# 2. Wait for health
sleep 10
make -C infra health

# 3. Apply DB migrations (jika ada)
make -C infra migrate

# 4. Apply seed
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -f infra/db/migrations/seed/seed-menu-amil-income.sql

# 5. Run E2E
bash testing/e2e-amil-income.sh

# 6. Manual test di browser
# - Login as ACC (user: HADI, pass: test1234)
# - Navigasi ke menu "Penerimaan Amil"
# - Create transaksi baru
# - Verify list & detail
```

### Checklist Final

- [ ] E2E script passed (all assertions green)
- [ ] Manual login + navigate to menu berhasil
- [ ] Create transaksi berhasil, transaction_no auto-generated
- [ ] List transaksi tampil dengan data benar
- [ ] Detail transaksi tampil lengkap
- [ ] Status approval sesuai limit (AUTHORIZED jika <= limit, PENDING jika > limit)
- [ ] Lookup dropdowns populate benar
- [ ] Form validasi (items wajib, amount > 0)
- [ ] Delete DRAFT transaksi berhasil
- [ ] Error message tampil untuk invalid input

---

## KOMPLEKSITAS & ESTIMASI

### Per Layer

| Layer | Kompleksitas | Estimasi | Model |
|---|---|---|---|
| DB (L1) | **Rendah** | 30 min | Haiku |
| API Python (L2) | **Sedang** | 2-3 jam | Haiku |
| BFF (L3) | **Rendah** | 30 min | Haiku |
| Seed (L4) | **Rendah** | 20 min | Haiku |
| Vue Frontend (L5) | **Sedang** | 2-3 jam | Haiku |
| Testing (L6) | **Rendah-Sedang** | 1 jam | Haiku |

**Total Estimasi:** 6-8 jam implementasi (parallelable: L1-3 bisa concurrent, L4-5 sequential)

### Kompleksitas Overall

**LEVEL:** Sedang (Medium)

**Alasan:**
- 2 tabel utama (TRANSACTION + TRANSACTIONITEM) + 1 tabel subtype (ACCOUNTTRANSACTIONITEM)
- 3 payment type (Kas Kecil, Kas Cabang, Bank) dengan sedikit logika berbeda
- Auto-generate nomor transaksi (format KM-YYYY-branch-cashCode-seq)
- Dual-mode save (insert vs update)
- Maker-checker workflow (save-and-submit → PENDING/AUTHORIZED auto)
- Limit-based auto-approval
- Journal posting via subsystem terpisah (async)
- No perubahan schema — tabel existing
- Form 1 dialog utama (tidak seperti penghimpunan yang multi-dialog)

---

## DEPENDENCIES

- Layer 1 (DB) **dependency:** Tabel transaction.* sudah ada (dari penghimpunan/penyaluran sebelumnya)
- Layer 2 (API) **depends on:** Layer 1 selesai
- Layer 3 (BFF) **depends on:** Layer 2 selesai
- Layer 4 (Seed) **depends on:** Layer 1 selesai, bisa paralel dengan L2-3
- Layer 5 (Vue) **depends on:** Layer 3 selesai
- Layer 6 (Test) **depends on:** Layer 5 selesai untuk E2E, atau L2 untuk unit test

**Recommended execution order:**
1. Start L1 + L2 + L3 + L4 in parallel
2. After L3 done → start L5
3. After L5 done → start L6

---

## NEXT STEPS (Post Implementation)

- [ ] Integration test dengan supervisor approval (otorisasi page)
- [ ] Verify journal posting (accounting subsystem)
- [ ] Load test dengan batch create (100+ transaksi)
- [ ] Manual user acceptance test dengan ACC + SPVACC roles
- [ ] Laporan penerimaan amil (DWH view + report-api) — phase 2

---


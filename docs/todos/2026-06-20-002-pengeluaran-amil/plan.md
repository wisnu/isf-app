# Plan: Implementasi Transaksi Pengeluaran Amil

**Tanggal:** 2026-06-20  
**Berdasarkan Specs:** `docs/todos/2026-06-20-002-pengeluaran-amil/specs.md`  
**Referensi Sibling:** `docs/todos/2026-06-20-001-penerimaan-amil/plan.md` (amil-income mirror)  
**Status:** In Progress

---

## RINGKASAN

Migrasi fitur input transaksi pengeluaran amil (kas keluar beban amil) dari legacy DAF
ke isf-app web-vue. Fitur ini adalah **cash-out mirror** dari penerimaan amil (yang sudah selesai),
dengan transaction code `'CO'` (FROZEN), accessible oleh role `ACC` (Accountant).

Pengeluaran Amil mencatat kas yang dikeluarkan organisasi sebagai beban operasional amil, via 3 channel:
1. Kas Kecil (Petty Cash) — default tab di form
2. Kas Cabang
3. Bank

**KUNCI DELTA vs Amil-Income:**
- Journal direction REVERSED: GL='D' (Debit Beban), Account='C' (Kredit Kas)
- Account_type='X' (Expense, bukan 'I' Income)
- No `isamilaccount` filter untuk bank account lookup (semua rekening aktif boleh)
- Grid lebih sederhana: TANPA cash_account_no, fund_product_code
- Default tab = Kas (bukan Bank)

---

## URUTAN EKSEKUSI

Implementasi per layer, dari database → backend API → BFF → Frontend.
**Layer 1-4 bisa paralel** (db + python + bff + seed independent), **Layer 5 tergantung L3 selesai**, **Layer 6 tergantung L5 selesai**.

---

## LAYER 1 — DB / DWH (nuwis-db-migrator, haiku)

**Status:** Pending  
**Model:** Haiku  
**Estimasi:** 20-30 min

Tidak ada tabel baru — amil-expense pakai schema `transaction.*` existing (dari amil-income).
Task: verifikasi struktur tabel, seed entity_config, dan (optional) buat DWH view.

### Checklist

- [ ] **Verifikasi tabel** `transaction.transaction` kolom:
  - `transactioncode` — untuk filter 'CO'
  - `authstatus` — untuk approval workflow
  - Semua kolom lain per specs.md (existing dari migrasi sebelumnya)

- [ ] **Verifikasi tabel** `transaction.transactionitem`:
  - `transactionitemtype` — untuk filter 'G' (GL) dan 'A' (Account)
  - `mutationtype` — untuk 'D' (debit GL beban) dan 'C' (kredit kas)
  - `parameterjournalid` — untuk '10' (semua item, TIDAK ada 'C20')

- [ ] **Verifikasi tabel** `transaction.cashaccount` kolom:
  - `accountno`, `accountname`, `branchcode`, `currencycode`, `status`, `cashcode`
  - `isamilaccount` — EXISTS tapi TIDAK difilter untuk amil-expense (perbedaan kunci)

- [ ] **Verifikasi tabel** `transaction.transactiontype`:
  - Row punya entry: `transactioncode='CO'`, `transactionname='Cash Out Amil'`, `vouchercode='KK'`
  - Jika belum ada: INSERT row baru

- [ ] **V###__amil-expense-entity-config.sql** — Seed entry ke `otorisasi.entity_config`
  ```sql
  INSERT INTO otorisasi.entity_config (entity_type, dispatcher_module, dispatcher_function, limit_entity)
  VALUES ('amil_expense', 'amil_expense_service', 'create_from_payload', 'ENTITY_AMIL_EXPENSE');
  ```

- [ ] (Optional) **dwh.v_amil_expense** — DWH view untuk laporan (phase 2)
  ```sql
  CREATE OR REPLACE VIEW dwh.v_amil_expense AS
  SELECT
    t.transactionid, t.transactionno, t.actualdate, t.branchcode, t.amount,
    ti.accountcode, ti.accountname, ti.mutationtype, ti.amount AS item_amount
  FROM transaction.transaction t
  JOIN transaction.transactionitem ti ON ti.transactionid = t.transactionid
  WHERE t.transactioncode = 'CO' AND ti.transactionitemtype = 'G';
  ```

**Apply Migration:**
```bash
# Migration file
infra/db/migrations/V###__amil-expense-entity-config.sql

# Apply
cd infra && psql -U transaction -d mziss_laz -f db/migrations/V###__amil-expense-entity-config.sql
```

---

## LAYER 2 — API PYTHON (nuwis-python-builder, haiku)

**Status:** Pending  
**Model:** Haiku  
**Estimasi:** 2-3 jam  
**Path:** `apps_zakat/api-python/app/modules/transaction/`

Buat modul baru `amil_expense_*` untuk handle business logic. Dispatcher harus terdaftar di `otorisasi/service.py`.

### Checklist

- [ ] **router.py** — 8 endpoints
  - `GET /api/transaction/amil-expense` — list dengan filter + pagination
  - `POST /api/transaction/amil-expense/save-and-submit` — create + dispatch ke otorisasi
  - `GET /api/transaction/amil-expense/{transaction_id}` — detail transaksi
  - `PUT /api/transaction/amil-expense/{transaction_id}` — update (DRAFT only)
  - `DELETE /api/transaction/amil-expense/{transaction_id}` — delete (DRAFT only)
  - `GET /api/transaction/amil-expense/lookup/bank-account` — dropdown rekening (TANPA isamilaccount filter)
  - `GET /api/transaction/amil-expense/lookup/gl-account` — dropdown GL account (account_type='X', parent='310301')
  - `GET /api/transaction/amil-expense/lookup/petty-cash-account` — dropdown kas kecil

- [ ] **schema.py** — Pydantic models
  - `AmilExpenseCreateRequest` — input form
  - `AmilExpenseItemRequest` — per item di grid
  - `AmilExpenseResponse` — output response
  - `AmilExpenseDetailResponse` — full detail + items
  - `BankAccountLookupResponse` — dropdown rekening
  - `GLAccountLookupResponse` — dropdown GL account

- [ ] **service.py** — Business logic
  - `create_amil_expense(req, user_id, branch_code)`:
    - Validasi items tidak kosong
    - Resolve payment_type → bank_account_no / cash_type / petty_cash_account_no
    - **Validate rekening:** TANPA filter isamilaccount (berbeda dari amil-income)
    - Generate transaction_no format `KK-YYYY-branch-cashCode-seq`
    - INSERT transaction (transactioncode='CO', authstatus='F')
    - INSERT transactionbatch (GetOrCreateBatch)
    - Loop items:
      - GLTransactionItem: mutationtype='D' (Debit), parameterjournalid='10'
      - AccountTransactionItem: mutationtype='C' (Kredit), parameterjournalid='10'
    - INSERT otorisasi.submission (entity_type='amil_expense')
    - Cek limit automatic approval
    - Return transaction_no + status

  - `list_amil_expense(date_from, date_to, branch_code, page, limit)`:
    - Query `transaction.transaction WHERE transactioncode='CO'`
    - Pagination

  - `get_amil_expense(transaction_id)`:
    - Query TRANSACTION + TRANSACTIONITEM
    - Return full detail dengan items

  - `update_amil_expense(transaction_id, req, user_id)`:
    - Check authstatus='F'
    - Delete old items
    - Re-run create logic
    - Return updated transaction

  - `delete_amil_expense(transaction_id)`:
    - Check authstatus='F'
    - DELETE transactionitem, accounttransactionitem
    - DELETE transaction
    - DELETE otorisasi.submission

  - `get_bank_accounts_lookup(branch_code)`:
    - Query CASHACCOUNT WHERE status='A' AND branchcode=:branch
    - **NO isamilaccount filter**

  - `get_petty_cash_accounts_lookup(branch_code)`:
    - Query CASHACCOUNT WHERE status='A' AND branchcode=:branch (filter untuk kas kecil)

  - `get_gl_accounts_lookup(branch_code, search)`:
    - Query account WHERE account_type='X' AND parent_account='310301' AND status='A'
    - **account_type='X' (Expense), BUKAN 'I'**

  - `get_next_transaction_number(payment_type, branch_code, bank_account_no)`:
    - Lookup vouchercode dari TRANSACTIONTYPE WHERE transactioncode='CO' → 'KK'
    - Resolve cashcode dari rekening
    - Call customidgenAPI
    - Return formatted number

  - **KRITIS:** `amil_expense_dispatcher(payload)`:
    - **Register di otorisasi/service.py** (MANDATORY)
    - Callback saat submission disetujui (AUTHORIZED)
    - Logic:
      - Re-validate items
      - CREATE journal: GL Debit Beban | Kas Kredit (mutationtype D & C)
      - UPDATE financial account balances
      - SET transaction authstatus='T', isposted='T'

- [ ] **repo.py** (jika query kompleks) — raw SQL queries

- [ ] **CRITICAL:** Register dispatcher di `apps_zakat/api-python/app/modules/otorisasi/service.py`:
  ```python
  # Add to _register_defaults()
  from app.modules.transaction.amil_expense_service import amil_expense_dispatcher
  registry['amil_expense'] = amil_expense_dispatcher
  ```

### Notes

- Semua query: `CAST(x AS type)`, bukan `x::type`
- Batch handling: internal, tidak di-expose UI
- Journal posting hanya saat status='AUTHORIZED' (via dispatcher)
- **KUNCI DELTA:** GL item mutationtype='D' (Debit), Account item='C' (Kredit) — reversed vs amil-income
- **KUNCI DELTA:** account_type='X' (Expense), bukan 'I'
- **KUNCI DELTA:** NO isamilaccount filter untuk bank lookup

---

## LAYER 3 — BFF API (nuwis-bff-builder, haiku)

**Status:** Pending  
**Model:** Haiku  
**Estimasi:** 30-45 min  
**Path:** `apps_zakat/bff-api/app/routers/`

Buat router BFF yang proxy ke api-python + auth guard + branch resolution.

### Checklist

- [ ] **amil_expense.py** — 8 endpoints
  - Router prefix: `/amil-expense`
  - Auth guard: `require_menu('finance.transactions.amil_expense')`
  - Sub-guards untuk create/update/delete (menu key dengan .tambah/.ubah/.hapus)
  - Inject `inputer_id` + `branch_id` dari session ke request body
  - Call `_resolve_branch(session, req)` untuk single-branch restriction
  - Proxy semua ke api-python `:8000`
  - Error handling: UNAUTHORIZED (401), MENU_DENIED (403), VALIDATION_ERROR (422)

- [ ] **apps_zakat/bff-api/app/main.py** — register router
  ```python
  from app.routers import amil_expense
  app.include_router(amil_expense.router, prefix="/api", tags=["amil_expense"])
  ```

### Notes

- BFF tidak buat logic bisnis — hanya proxy + auth
- Session data: `inputer_id` dari `request.user.user_id`, `branch_id` dari `request.user.branch_id`

---

## LAYER 4 — SEED / AUTH (nuwis-seed-gen, haiku)

**Status:** Pending  
**Model:** Haiku  
**Estimasi:** 20-30 min  
**Path:** `infra/db/migrations/seed/`

Seed menu entry, role_menu assignment ke `isf_auth_zakat`. **3-way consistency check required.**

### Checklist

- [ ] **seed-menu-amil-expense.sql** (atau append ke existing seed-auth-menu.sql)
  ```sql
  INSERT INTO isf_auth.menu (menu_key, label, parent_key, icon, route_path)
  VALUES
    ('finance.transactions.amil_expense', 'Pengeluaran Amil', 'finance.transactions', 'cash-out', 'amil-expense'),
    ('finance.transactions.amil_expense.tambah', 'Tambah', 'finance.transactions.amil_expense', 'plus-circle', null),
    ('finance.transactions.amil_expense.ubah', 'Ubah', 'finance.transactions.amil_expense', 'edit', null),
    ('finance.transactions.amil_expense.hapus', 'Hapus', 'finance.transactions.amil_expense', 'trash', null);

  INSERT INTO isf_auth.role_menu (role_id, menu_key)
  VALUES
    ('ACC', 'finance.transactions.amil_expense'),
    ('ACC', 'finance.transactions.amil_expense.tambah'),
    ('ACC', 'finance.transactions.amil_expense.ubah'),
    ('ACC', 'finance.transactions.amil_expense.hapus'),
    ('SPVACC', 'finance.transactions.amil_expense');  -- view only
  ```

- [ ] **3-WAY CONSISTENCY CHECK** (MANDATORY):
  - ✓ Menu key di registry.ts (L5 task)
  - ✓ Menu key di route meta.menu_key (L5 task)
  - ✓ Menu key di seed SQL (this task)
  - All three MUST match: `finance.transactions.amil_expense`

- [ ] **Apply Seed:**
  ```bash
  psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-menu-amil-expense.sql
  ```

### Notes

- Icon: gunakan lucide icon name ('cash-out', 'plus-circle', etc.)
- Parent: 'finance.transactions' untuk menu level utama
- Role assignment: ACC untuk full CRUD, SPVACC untuk view only (supervisor approve di otorisasi page)

---

## LAYER 5 — FRONTEND VUE (nuwis-ui-builder, haiku)

**Status:** Pending  
**Model:** Haiku  
**Estimasi:** 2-3 jam  
**Path:** `apps_zakat/web-vue/src/`

Buat halaman Vue 3 untuk list dan form input transaksi pengeluaran amil.

### Checklist — New Files

- [ ] **src/pages/finance/amil-expense/AmilExpensePage.vue** (list view)
  - Toolbar: date filter (from/to), branch filter (jika branch_access='all')
  - Button: "Tambah Transaksi Baru"
  - Pagination: top-placed standalone Paginator (default 25 rows)
  - Table columns: transaction_no, actual_date, bank_account_name, total_amount, status, actions
  - Actions: [Lihat], [Edit (jika DRAFT)], [Hapus (jika DRAFT)]
  - Fetch: GET /api/transaction/amil-expense
  - Loading state + error handling

- [ ] **src/pages/finance/amil-expense/AmilExpenseFormPage.vue** (create + edit mode)
  - Header section:
    - `actual_date` — DateField.vue [Required]
    - `paid_to` — Input [Optional]
    - `received_from` — Input [Optional, pre-fill username]
  - Payment type tabs (Tab component or Radio group):
    - **Tab Kas** (payment_type='K'/'C', DEFAULT ACTIVE):
      - `cash_type` — Select [Required, default='K']
      - `petty_cash_account_no` — SearchSelect [Optional, muncul jika cash_type='K']
        - Fetch: GET /api/transaction/amil-expense/lookup/petty-cash-account
      - `reference_no` — Input [Optional]
      - `description` — Input [Optional]
    - **Tab Bank** (payment_type='B'):
      - `bank_account_no` — SearchSelect [Required]
        - Fetch: GET /api/transaction/amil-expense/lookup/bank-account (TANPA isamilaccount filter)
      - `reference_no` — Input [Optional]
      - `description` — Input [Optional]
      - `rate` — Input number [Optional, default 1.0]
  - Grid Detail (inline editable rows):
    - Columns: account_code (lookup), account_name (readonly), amount, description, budget_code (lookup), budget_owner (readonly)
    - **NO cash_account_no / fund_product columns** (delta vs amil-income)
    - Actions: [Add row], [Delete row]
    - Validation: account_code required, amount > 0
    - Fetch GL accounts: GET /api/transaction/amil-expense/lookup/gl-account (account_type='X')
  - Footer (readonly):
    - `transaction_no` — pre-filled jika edit mode
    - `total_amount` — computed dari sum(items[].amount)
  - Buttons: [Simpan & Kirim Persetujuan], [Batal]
  - Async feedback: loading state, success toast, error toast

- [ ] **src/lib/menu/registry.ts** — daftarkan 4 menu keys
  ```typescript
  FINANCE_TRANSACTIONS_AMIL_EXPENSE: 'finance.transactions.amil_expense',
  FINANCE_TRANSACTIONS_AMIL_EXPENSE_TAMBAH: 'finance.transactions.amil_expense.tambah',
  FINANCE_TRANSACTIONS_AMIL_EXPENSE_UBAH: 'finance.transactions.amil_expense.ubah',
  FINANCE_TRANSACTIONS_AMIL_EXPENSE_HAPUS: 'finance.transactions.amil_expense.hapus',
  ```

### Checklist — File Modifications

- [ ] **src/router/index.ts** — 3 routes
  - Route list:
    ```typescript
    {
      path: '/finance/transactions/amil-expense',
      name: 'AmilExpense',
      component: () => import('@/pages/finance/amil-expense/AmilExpensePage.vue'),
      meta: { menu_key: MENU_KEYS.FINANCE_TRANSACTIONS_AMIL_EXPENSE }
    }
    ```
  - Route create:
    ```typescript
    {
      path: '/finance/transactions/amil-expense/baru',
      name: 'AmilExpenseCreate',
      component: () => import('@/pages/finance/amil-expense/AmilExpenseFormPage.vue'),
      meta: { menu_key: MENU_KEYS.FINANCE_TRANSACTIONS_AMIL_EXPENSE_TAMBAH }
    }
    ```
  - Route edit (optional):
    ```typescript
    {
      path: '/finance/transactions/amil-expense/:id/edit',
      name: 'AmilExpenseEdit',
      component: () => import('@/pages/finance/amil-expense/AmilExpenseFormPage.vue'),
      meta: { menu_key: MENU_KEYS.FINANCE_TRANSACTIONS_AMIL_EXPENSE_UBAH }
    }
    ```

- [ ] **src/components/AppSidebar.vue** — tambah menu entry
  - Import icon: `import { CashOut } from 'lucide-vue-next'` (atau cash-out icon)
  - Tambah menu entry di sidebar tree (section "Keuangan" > "Transaksi"):
    ```vue
    <li :key="MENU_KEYS.FINANCE_TRANSACTIONS_AMIL_EXPENSE">
      <Link
        :to="{ name: 'AmilExpense' }"
        :icon="CashOut"
        :text="`Pengeluaran Amil`"
        :active="sidebarStore.activeMenu === MENU_KEYS.FINANCE_TRANSACTIONS_AMIL_EXPENSE"
      />
    </li>
    ```

### Notes

- Gunakan `vue-primevue-zakat-ui` skill untuk UI patterns
- Pagination: ALWAYS top-placed, NEVER use DataTable paginator
- DateField.vue untuk semua date input (display DD-MM-YYYY, internal ISO)
- SearchSelect.vue untuk dropdown panjang (rekening bank, GL account)
- **Tab default = Kas** (berbeda dari amil-income yang default Bank)
- Grid: NO cash_account_no / fund_product columns
- Delete: form modal (read-only) + confirm button, bukan inline confirm
- Menu key consistency: registry.ts + route meta.menu_key + seed SQL harus sinkron

---

## LAYER 6 — TESTING (nuwis-test-gen, haiku)

**Status:** Pending  
**Model:** Haiku  
**Estimasi:** 1 jam  
**Path:** `testing/`

Buat E2E smoke test script untuk memverifikasi implementasi.

### Checklist

- [ ] **testing/e2e-amil-expense.sh** (curl-based template)
  - Setup: health check + login as ACC user (HADI)
  - Test sequence:
    1. GET /api/transaction/amil-expense (list)
    2. GET /api/transaction/amil-expense/lookup/bank-account (dropdown, TANPA isamilaccount filter)
    3. GET /api/transaction/amil-expense/lookup/gl-account (dropdown expense accounts)
    4. POST /api/transaction/amil-expense/save-and-submit (create transaksi)
    5. GET /api/transaction/amil-expense/{id} (detail created transaksi)
    6. Verify status=PENDING (jika amount > limit) atau AUTHORIZED (jika <= limit)
    7. (Optional) PUT /api/transaction/amil-expense/{id} (update if DRAFT)
    8. (Optional) DELETE /api/transaction/amil-expense/{id} (delete if DRAFT)
  - Assertions:
    - Status codes (200, 201, 404, 403)
    - Response shape (data, pagination, meta)
    - Discriminator fields: transactioncode='CO', mutationtype ('D' for GL, 'C' for account), parameterjournalid='10'
    - account_type='X' (expense, NOT 'I')
    - channelcode='R' (regular) or 'P' (petty)

- [ ] (Optional) **apps_zakat/api-python/tests/test_amil_expense.py** (unit tests)
  - Test create dengan amount <= limit (auto-approve)
  - Test create dengan amount > limit (PENDING)
  - Test update DRAFT transaksi
  - Test delete DRAFT transaksi
  - Test validasi items tidak kosong
  - Test lookup bank account (NO isamilaccount filter)
  - Test lookup GL account (account_type='X' only)

### Run Tests

```bash
# E2E smoke test
cd /home/wishnew/workshop/isf-app
bash testing/e2e-amil-expense.sh

# Unit tests (optional)
cd apps_zakat/api-python
pytest tests/test_amil_expense.py -v
```

---

## VERIFIKASI FINAL (Post-Implementation)

Setelah semua layer selesai:

```bash
# 1. Restart containers
cd infra
podman-compose -f docker-compose.zakat.yml down
podman-compose -f docker-compose.zakat.yml up -d
sleep 15

# 2. Health check
make -C infra health

# 3. Apply DB migration (jika ada)
make -C infra migrate

# 4. Apply seed to auth DB
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -f infra/db/migrations/seed/seed-menu-amil-expense.sql

# 5. Run E2E test
bash testing/e2e-amil-expense.sh

# 6. Manual browser test
# - Login as ACC (user: HADI, pass: test1234)
# - Navigate to sidebar > Keuangan > Transaksi > Pengeluaran Amil
# - Create transaksi baru
# - Verify list & detail
```

### Checklist Final

- [ ] E2E script passed (all assertions green)
- [ ] Manual login + navigate to menu berhasil
- [ ] Create transaksi berhasil, transaction_no auto-generated (KK-YYYY-...)
- [ ] List transaksi tampil dengan data benar
- [ ] Detail transaksi tampil lengkap dengan items
- [ ] Status approval sesuai limit (AUTHORIZED jika <= limit, PENDING jika > limit)
- [ ] Lookup dropdowns populate benar (bank: TANPA isamilaccount, GL: account_type='X')
- [ ] Form validasi (items wajib, amount > 0)
- [ ] Tab default = Kas (bukan Bank)
- [ ] Grid TANPA cash_account_no / fund_product columns
- [ ] Journal direction correct: GL item mutationtype='D', Account item='C'
- [ ] Delete DRAFT transaksi berhasil
- [ ] Error message tampil untuk invalid input

---

## KOMPLEKSITAS & ESTIMASI

### Per Layer

| Layer | Kompleksitas | Estimasi | Model | Status |
|---|---|---|---|---|
| DB (L1) | **Rendah** | 20-30 min | Haiku | Pending |
| API Python (L2) | **Sedang** | 2-3 jam | Haiku | Pending |
| BFF (L3) | **Rendah** | 30-45 min | Haiku | Pending |
| Seed (L4) | **Rendah** | 20-30 min | Haiku | Pending |
| Vue Frontend (L5) | **Sedang** | 2-3 jam | Haiku | Pending |
| Testing (L6) | **Rendah-Sedang** | 1 jam | Haiku | Pending |

**Total Estimasi:** 6-8 jam implementasi  
**Parallelizable:** L1-4 bisa concurrent; L5 sequential setelah L3; L6 setelah L5

### Kompleksitas Overall

**LEVEL:** Sedang (Medium)

**Alasan:**
- 2 tabel utama (TRANSACTION + TRANSACTIONITEM) + 1 tabel subtype (ACCOUNTTRANSACTIONITEM) — existing, tidak perlu migrasi
- 3 payment type (Kas Kecil, Kas Cabang, Bank) dengan logika mirip amil-income
- Auto-generate nomor transaksi (format KK-YYYY-branch-cashCode-seq)
- Dual-mode save (insert vs update)
- Maker-checker workflow (save-and-submit → PENDING/AUTHORIZED auto)
- Limit-based auto-approval
- Journal posting via dispatcher (async)
- **Berbeda dari amil-income:** Grid lebih sederhana (no fund_product), account_type='X' (no 'I'), journal direction reversed, no isamilaccount filter
- Form 1 dialog utama (tidak multi-dialog)

---

## DEPENDENCIES & EXECUTION ORDER

| Layer | Depends On | Start When |
|---|---|---|
| **L1 (DB)** | None | Immediate |
| **L2 (API)** | L1 | L1 health check pass |
| **L3 (BFF)** | L2 | L2 health check pass |
| **L4 (Seed)** | L1 | L1 health check pass (parallel with L2-3) |
| **L5 (Vue)** | L3 | L3 health check pass |
| **L6 (Test)** | L5 (E2E) or L2 (unit) | L5 done for E2E, or L2 for unit |

**Recommended Execution:**
1. **Start L1 + L2 + L3 + L4 in parallel** — ~2-4 hours total
2. **After L3 health pass → start L5** — ~2-3 hours
3. **After L5 done → start L6** — ~1 hour
4. **Total time: ~5-8 hours** (less if perfect parallelization)

---

## KRITIS DELTA CHECKLIST

Pastikan tidak ada yang terlewat:

- [ ] **Journal direction REVERSED vs amil-income:**
  - GL item: mutationtype='D' (Debit Beban)
  - Account item: mutationtype='C' (Kredit Kas)

- [ ] **account_type='X' (Expense), BUKAN 'I':**
  - GL account filter: WHERE account_type='X' AND parent_account='310301'
  - Endpoint: `/api/transaction/amil-expense/lookup/gl-account`

- [ ] **NO isamilaccount filter untuk bank lookup:**
  - Bank account filter: WHERE status='A' AND branchcode=:branch (TANPA isamilaccount='T')
  - Endpoint: `/api/transaction/amil-expense/lookup/bank-account`

- [ ] **Tab default = Kas (NOT Bank):**
  - Form open: set payment_type='K' (cash type), NOT 'B'

- [ ] **Grid TANPA cash_account_no / fund_product columns:**
  - Only: account_code, account_name, amount, description, budget_code, budget_owner
  - Deleted from form: cash_account_no, cash_account_name, fund_product_code, fund_product_name

- [ ] **parameterjournalid='10' everywhere (NO 'C20'):**
  - GL item: '10'
  - Account item: '10' (NOT 'C20' like amil-income)

- [ ] **entity_type='amil_expense' registered di dispatcher:**
  - otorisasi/service.py: _register_defaults() harus punya amil_expense entry
  - TANPA ini, transaksi stuck di PENDING

- [ ] **3-way menu key consistency:**
  - registry.ts: 'finance.transactions.amil_expense'
  - route meta.menu_key: 'finance.transactions.amil_expense'
  - seed SQL: 'finance.transactions.amil_expense'
  - ALL THREE MUST MATCH

---

## NEXT STEPS (Post Implementation)

- [ ] Integration test dengan supervisor approval (otorisasi page)
- [ ] Verify journal posting (accounting subsystem) — GL Debit | Kas Kredit
- [ ] Load test dengan batch create (100+ transaksi)
- [ ] Manual user acceptance test dengan ACC + SPVACC roles
- [ ] Laporan pengeluaran amil (DWH view + report-api) — phase 2
- [ ] Tab Non Tunai (Aktiva) — phase 2

---

## HANDOFF TEMPLATE (To Agents)

When delegating to nuwis-* builders, pass:

**To nuwis-python-builder:**
```
Build modules for transaction code 'CO' (Pengeluaran Amil).
Key specs:
- Journal direction REVERSED vs CI: GL mutationtype='D', Account='C'
- account_type='X' (Expense), NOT 'I'
- NO isamilaccount filter for bank lookup
- NO parameterjournalid 'C20' — only '10'
- entity_type='amil_expense' register in otorisasi dispatcher
Specs: docs/todos/2026-06-20-002-pengeluaran-amil/specs.md
```

**To nuwis-ui-builder:**
```
Build Vue pages for /finance/transactions/amil-expense.
Key specs:
- Default tab = Kas (NOT Bank like amil-income)
- Grid: NO cash_account_no / fund_product columns
- Bank account lookup: TANPA isamilaccount filter
- GL account lookup: account_type='X' only
- Menu key: finance.transactions.amil_expense
Specs: docs/todos/2026-06-20-002-pengeluaran-amil/specs.md
```

---

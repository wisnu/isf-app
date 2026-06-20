# Plan: Piutang (Pinjam & Bayar)

**Dibuat**: 2026-06-17  
**Target Portal**: zakat  
**Type**: CRUD + Approval Workflow

---

## Urutan Eksekusi

Layer 1 dan 2 bisa paralel jika tidak ada dependency.  
Layer 3-6 sequential (masing-masing depends output layer sebelumnya).

---

## Layer 1 — DB/DWH (nuwis-db-migrator, haiku)

Verifikasi tabel legacy sudah ada; buat DWH view baru.

- [ ] **Verify existing tables**
  - `transaction.TRANSACTION` (transactioncode, actualdate, amount, branchcode, inputer)
  - `transaction.ACCOUNTRECEIVABLE` (accountno, accountreceivabletype, employeeidnumber, debtorid)
  - `transaction.FINANCIALACCOUNT` (accountno, balance, accountname)
  - `transaction.EXTERNALDEBTOR` (debtorid, debtorcode, debtorname)
  - `transaction.TRANSACTIONBATCH` (batchid, batchdate)
  - `transaction.DEBTOR_ALL` view (UNION employee + externaldebtor)

- [ ] `infra/db/migrations/V###__piutang-views.sql`
  - `dwh.v_piutang_karyawan` — transaction + accounttransactionitem + accountreceivable (type='E') + personalia.employee
  - `dwh.v_piutang_non_karyawan` — transaction + accounttransactionitem + accountreceivable (type='D') + externaldebtor
  - Both views: JOIN with transaction.TRANSACTION WHERE transactioncode IN ('EAR', 'PEAR')
  - Columns: transactionno, transactioncode, actualdate, branchcode, inputer, amount, accountno, {employee/debtorname}, accountname, balance, description, referenceno

**SQL hints**:
- Use `CAST(x AS type)`, NOT `x::type`
- Filter: `transactioncode IN ('EAR', 'PEAR')`
- Portal isolation: zakat only (no wakaf equivalent yet)

**Apply after layer 1 complete**:
```bash
psql -U transaction -d mziss_laz -f infra/db/migrations/V###__piutang-views.sql
```

---

## Layer 2 — Python API (nuwis-python-builder, haiku)

Build transaction/piutang module with save-and-submit approval flow.

- [ ] `apps_zakat/api-python/app/modules/transaction/piutang/__init__.py`
- [ ] `apps_zakat/api-python/app/modules/transaction/piutang/router.py`
  - `GET /api/transaction/piutang/` — list (paginated, filters: date_from/to, transaction_type, debtor_type)
  - `POST /api/transaction/piutang/` — create EAR/PEAR with otorisasi.save-and-submit()
  - `PUT /api/transaction/piutang/{transactionno}` — update (delete journal + cancel + recreate)
  - `GET /api/transaction/piutang/debitur/` — lookup DEBTOR_ALL

- [ ] `apps_zakat/api-python/app/modules/transaction/piutang/service.py`
  - `create_piutang()` → INSERT transaction, accountreceivable (if EAR), accounttransactionitem
  - `update_piutang()` → delete journal, cancel transaction, recreate
  - `get_piutang_list()` → query with pagination + filters
  - `lookup_debitur()` → query DEBTOR_ALL + EXTERNALDEBTOR
  - `create_from_payload()` — dispatcher for otorisasi (auto-execute when AUTHORIZED)

- [ ] `apps_zakat/api-python/app/modules/transaction/piutang/schema.py`
  - `PiutangCreateSchema` — actualdate, transactiontype, channeltype, cashaccountno/glaccount, debtorid, amount, referenceno, description, casher
  - `PiutangResponse` — id, transactionno, transactiontype, actualdate, branchcode, inputer, debtorname, accountname, amount, status, ...

- [ ] Register router in `apps_zakat/api-python/app/main.py`
  - `app.include_router(piutang_router, prefix="/api/transaction/piutang", tags=["piutang"])`

- [ ] **Otorisasi integration**
  - Register `entity_type='piutang'` dispatcher in `apps_zakat/api-python/app/modules/otorisasi/service.py:_register_defaults()`
  - Dispatcher calls `piutang_service.create_from_payload(payload)` when submission status → AUTHORIZED
  - Submission flow: API calls `otorisasi.save_and_submit()` internally, auto-checks limit, sets status PENDING/AUTHORIZED

**Save Logic hints**:
- EAR (Pinjam): auto-create AccountReceivable (type='E' for employee, type='D' for external)
- PEAR (Bayar): lookup only, error if not found
- SetMutation: piutang DEBIT amount, channel (kas/ledger) CREDIT amount
- FundEntity hardcoded=4 (Dana Amil)
- GenerateTransactionNumber (backend)
- CreateJournal (debit piutang, kredit kas/ledger)

---

## Layer 3 — BFF (nuwis-bff-builder, haiku)

Proxy API endpoints with auth decorator + branch injection.

- [ ] `apps_zakat/bff-api/app/routers/piutang.py`
  - `GET /api/transaction/piutang/` — `require_menu("keuangan.piutang.pinjam-bayar")` + `_resolve_branch()` + proxy
  - `POST /api/transaction/piutang/` — `require_menu("keuangan.piutang.pinjam-bayar")` + `_resolve_branch()` + proxy
  - `PUT /api/transaction/piutang/{transactionno}` — `require_menu("keuangan.piutang.pinjam-bayar")` + proxy
  - `GET /api/transaction/piutang/debitur/` — `require_menu("keuangan.piutang.pinjam-bayar")` + proxy

- [ ] Register router in `apps_zakat/bff-api/app/main.py`
  - `app.include_router(piutang_router, prefix="/api/transaction", tags=["transaction"])`

**BFF hints**:
- All endpoints must go through `require_menu()` check
- `_resolve_branch()` injects `branch_id` from session
- Proxy requests to api-python with base URL from env
- Return api-python response as-is (don't re-wrap)

---

## Layer 4 — Seed (nuwis-seed-gen, haiku)

Create menu + role_menu + otorisasi entity config.

- [ ] `infra/db/migrations/seed/piutang-seed.sql`
  - INSERT menu: `keuangan.piutang.pinjam-bayar`, label="Piutang (Pinjam/Bayar)", menu_type='form'
  - INSERT role_menu: `menu_key='keuangan.piutang.pinjam-bayar'`, roles=['ACC']
  - INSERT otorisasi.entity_config: `entity_type='piutang'`, entity_name='Piutang Karyawan/Non-Karyawan'

**Apply after complete**:
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/piutang-seed.sql
```

---

## Layer 5 — UI (nuwis-ui-builder, haiku)

Create Vue page + form modal + sidebar entry.

- [ ] `apps_zakat/web-vue/src/pages/keuangan/PiutangPage.vue`
  - List table: transactionno, transactiontype (P/B badge), actualdate (dmy format), debtorname, amount (IDR format), status badge, actions (edit/delete)
  - Toolbar: [Search debtorname] + [Filter date] + [Add Piutang button]
  - Pagination: standalone Paginator at top (default 25 rows)
  - On Add: open FormModal
  - On Edit: open FormModal pre-filled

- [ ] `components/PiutangFormModal.vue`
  - Fields: actualdate (DateField), transactiontype (radio P/B), debtorname (SearchSelect from `/debitur/`), channeltype (toggle C/G)
  - Conditional fields: LCashAccount (if C), LGLAccount (if G)
  - amount, referenceno (optional), description (optional), casher (default session)
  - On Save: POST/PUT to `/api/transaction/piutang/`
  - Status feedback: loading state + success/error toast
  - If status=PENDING: show "Menunggu otorisasi supervisor"

- [ ] Entry in `apps_zakat/web-vue/src/router/index.ts`
  - Route: `/keuangan/piutang`, component=PiutangPage, meta.menu_key='keuangan.piutang.pinjam-bayar'

- [ ] Entry in `apps_zakat/web-vue/src/lib/menu/registry.ts`
  - MENU_KEYS.KEUANGAN_PIUTANG_PINJAM_BAYAR = 'keuangan.piutang.pinjam-bayar'

- [ ] Sidebar entry in `components/AppSidebar.vue`
  - Add child under "Keuangan" > "Piutang" menu group (new group if not exist)
  - Label: "Pinjam/Bayar", icon=CreditCard (Lucide)

**UI hints**:
- Use `dmy()` from `lib/date.ts` for actualdate display
- Use `lib/format.ts` currency formatter for amount
- SearchSelect.vue for debtorname lookup (auto-call GET /debitur/)
- DateField.vue for actualdate (v-model=ISO string)
- PrimeVue DataTable unstyled with Tailwind layout
- Status badge colors: AUTHORIZED=green, PENDING=amber, REJECTED=red
- TransactionType badge: P=blue, B=green
- Modal delete confirmation (read-only form before confirm)

---

## Layer 6 — Test (nuwis-test-gen, haiku)

Create E2E smoke test script.

- [ ] `testing/e2e-piutang.sh`
  - Smoke test: POST create EAR (Pinjam), POST create PEAR (Bayar), GET list, PUT update
  - Test both transaction types (P/B)
  - Test limit check (auto-approval vs PENDING)
  - Test debitur lookup (employee vs external)
  - Validate response shape + data integrity

- [ ] `apps_zakat/api-python/tests/test_piutang.py` (if complex logic)
  - Unit test: auto-create accountreceivable for EAR
  - Unit test: lookup-only validation for PEAR
  - Unit test: channel type validation (C vs G)
  - Unit test: transaction number generation
  - Unit test: otorisasi dispatcher integration

---

## Verifikasi

Jalankan setelah semua layer selesai:

```bash
# 1. Restart containers
cd infra
podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue

# 2. Wait for startup (30s)
sleep 30

# 3. Run E2E test
bash testing/e2e-piutang.sh

# 4. Manual verification
# - Login as RAIS (ACC role, zakat portal)
# - Navigate to Keuangan → Piutang → Pinjam/Bayar
# - Create new Piutang (Pinjam), select debitur, submit
# - Check if auto-approved or PENDING (depends on limit)
# - If PENDING, approve via Keuangan → Otorisasi page
# - Verify transaction appears in list
# - Check DWH view: SELECT * FROM dwh.v_piutang_karyawan
```

- [ ] E2E test passed
- [ ] Manual CRUD works from UI
- [ ] Auto-approval works for amount ≤ limit
- [ ] Manual approval (PENDING) works for amount > limit
- [ ] DWH views return correct data
- [ ] Menu key + role access verified (ACC only)


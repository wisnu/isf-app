# Plan: Transaksi Umum (General Transaction)
**Dibuat**: 2026-06-17
**Target Portal**: zakat
**Kompleksitas**: TINGGI — composite form + 4 item types + auto journal generation
**Rekomendasi Model**: Opus untuk API layer (logic kompleks), Haiku untuk BFF/UI/seed

---

## Urutan Eksekusi

Layer 1 bisa berjalan paralel dengan Layer 2. Layer 3+ bergantung pada Layer 2.

---

## Layer 0 — Preparation (nuwis-db-migrator, sonnet atau opus)

- [ ] **Verifikasi sequence `seq_transactionnumber`** — pastikan ada di schema `transaction` dan berfungsi
- [ ] **Review tabel existing** — TRANSACTION, TRANSACTIONITEM, ACCOUNTTRANSACTIONITEM, struktur sudah final, tidak perlu migration baru (reuse)
- [ ] **Plan DWH view** — `dwh.v_general_transaction` akan dibuat di Layer 0.5 setelah migrasi

**Tidak perlu:**
- Migration baru V{NNN}__transaksi_umum.sql — tabel sudah ada
- Kolom tambahan — semua field sudah tersedia

---

## Layer 0.5 — DWH View (nuwis-db-migrator, haiku)

- [ ] `infra/db/migrations/dwh/v_general_transaction.sql` — JOIN TRANSACTION + TRANSACTIONITEM + ACCOUNTTRANSACTIONITEM WHERE TRANSACTIONCODE='GT'
  - Kolom output minimal: transactionid, transactionno, actualdate, branchcode, referenceno, description, inputer, authstatus, amount, transactionitemid, transactionitemtype, accounttitype, mutationtype, item_amount, fundentity, accountno, accountcode

**Tidak termasuk seed** — ini hanya view, bukan data.

---

## Layer 1 — Python API (nuwis-python-builder, opus recommended)

**CRITICAL: Complexity tinggi — rekomendasi pakai model Opus untuk logic ini.**

- [ ] `apps_zakat/api-python/app/modules/transaction/` — buat/review struktur package
- [ ] `apps_zakat/api-python/app/modules/transaction/schemas.py` — Pydantic classes:
  - `ItemBase` — fields bersama semua item type
  - `ItemPenghimpunan` (item_type='C') — discriminator field
  - `ItemPenyaluran` (item_type='D') — discriminator field
  - `ItemKasBank` (item_type='B') — discriminator field
  - `ItemLedger` (item_type='G') — discriminator field
  - `Items` = `Annotated[ItemBase, Field(discriminator='item_type')]` (union)
  - `TransaksiUmumCreate` — header + items[]
  - `TransaksiUmumUpdate` — transaction_no + header + items[]
  - `RekeningInfo` — response struktur
  - `KursInfo` — response struktur
  - `LimitCheckRequest`, `LimitCheckResponse`
  - `OverrideCheckRequest`, `OverrideCheckResponse`

- [ ] `apps_zakat/api-python/app/modules/transaction/service.py` — Business logic:
  - `class GeneralTransactionService:`
    - `async def create_transaction(payload, session, branch_id, inputer_id)` → call CreateJournal, return transaction_no
    - `async def update_transaction(transaction_no, payload, session, ...)` → DeleteJournal + re-create + CreateJournal
    - `async def get_list(page, limit, date_from, date_to, status, branch_id, session)` → paginate
    - `async def get_detail(transaction_no, session)` → return header + items
    - `async def get_rekening_info(account_no, session)` → lookup + return name, currency, type
    - `async def get_kurs_info(currency_code, tanggal, session)` → lookup master kurs
    - `async def cek_limit(amount_debit, branch_id, session)` → call corporate limit check
    - `async def cek_override(user_override, password_override, amount_debit, branch_id, session)` → verify user + password, call limit check with override
  - **Memanggil CreateJournal** — ekstrak dari modul jurnal yang sudah ada atau buat baru
  - **Discriminator hardcoded**: TRANSACTIONCODE='GT', TRANSACTIONITEMTYPE='A'/'G', ACCOUNTTITYPE='D'/'Z'/'A', FUNDENTITY, MUTATIONTYPE, PARAMETERJOURNALID='10'

- [ ] `apps_zakat/api-python/app/modules/transaction/repository.py` — DB queries:
  - `get_transaction_by_no(transaction_no, session)`
  - `insert_transaction(payload, session) → transaction_id`
  - `insert_transaction_items(transaction_id, items[], session) → item_ids[]`
  - `insert_account_transaction_items(item_data, session) → row`
  - `delete_transaction_items(transaction_id, session)`
  - `get_next_transaction_number(branch_code, session)` → call nextval('seq_transactionnumber'), format GT-YYYY-BC-BPZIS-{7digit}
  - `lookup_rekening(account_no, session)` → UNION query kas/bank + product account
  - `lookup_kurs(currency_code, tanggal, session)` → query masterkurs

- [ ] `apps_zakat/api-python/app/modules/transaction/router.py` — FastAPI endpoints (8 total):
  - `POST /api/transaction/general-transaction/create` — require_menu('keuangan.transaksi.umum.tambah')
  - `POST /api/transaction/general-transaction/update` — require_menu('keuangan.transaksi.umum.ubah')
  - `GET /api/transaction/general-transaction/list` — require_menu('keuangan.transaksi.umum')
  - `GET /api/transaction/general-transaction/{transaction_no}` — require_menu('keuangan.transaksi.umum')
  - `GET /api/transaction/general-transaction/rekening-info` — require_menu('keuangan.transaksi.umum')
  - `GET /api/transaction/general-transaction/kurs-info` — require_menu('keuangan.transaksi.umum')
  - `POST /api/transaction/general-transaction/cek-limit` — require_menu('keuangan.transaksi.umum')
  - `POST /api/transaction/general-transaction/cek-override` — require_menu('keuangan.transaksi.umum.override')

- [ ] Daftarkan router di `apps_zakat/api-python/app/main.py` — `app.include_router(general_transaction_router, prefix='/api/transaction', tags=['general_transaction'])`

---

## Layer 2 — BFF (nuwis-bff-builder, haiku)

- [ ] `apps_zakat/bff-api/app/routers/general_transaction.py` — BFF router:
  - Proxy semua 8 endpoint ke api-python
  - Decorator: `require_menu('keuangan.transaksi.umum')` base, `require_menu('{action}')` per endpoint
  - `_resolve_branch()` inject ke payload sebelum proxy
  - `_resolve_inputer_id()` inject ke payload sebelum proxy
  - Handle response wrapping dan error translation

- [ ] Daftarkan router di `apps_zakat/bff-api/app/main.py` — `app.include_router(general_transaction_router, tags=['general_transaction'])`

---

## Layer 3 — Seed (nuwis-seed-gen, haiku)

- [ ] `infra/db/migrations/seed/transaksi-umum-menu-and-rolemenu.sql` — seed ke `isf_auth_zakat`:
  - INSERT ke `isf_auth.menu` (6 rows): keuangan.transaksi.umum (base), .tambah, .ubah, .hapus, .override
  - INSERT ke `isf_auth.role_menu` (6 rows per role): ACC untuk read+create+update+delete, SUP untuk override
  - Verifikasi 3-way consistency: menu_key di registry.ts, route meta.menu_key, seed SQL

**Apply setelah selesai**:
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/transaksi-umum-menu-and-rolemenu.sql
```

- [ ] Update `apps_zakat/web-vue/src/lib/menu/registry.ts` — daftarkan MENU_KEYS:
  ```typescript
  export const MENU_KEYS = {
    // ... existing keys
    KEUANGAN_TRANSAKSI_UMUM: 'keuangan.transaksi.umum',
    KEUANGAN_TRANSAKSI_UMUM_TAMBAH: 'keuangan.transaksi.umum.tambah',
    KEUANGAN_TRANSAKSI_UMUM_UBAH: 'keuangan.transaksi.umum.ubah',
    KEUANGAN_TRANSAKSI_UMUM_HAPUS: 'keuangan.transaksi.umum.hapus',
    KEUANGAN_TRANSAKSI_UMUM_OVERRIDE: 'keuangan.transaksi.umum.override',
  }
  ```

---

## Layer 4 — Vue UI (nuwis-ui-builder, haiku)

- [ ] `apps_zakat/web-vue/src/pages/keuangan/TransaksiUmumPage.vue` — main form page
  - Header section: actual_date (read-only), reference_no, description
  - Item type selector + dynamic form (C/D/B/G conditional rendering)
  - Items DataTable with edit/delete actions
  - Summary row: Total Debit | Total Kredit (warning badge if ≠)
  - Balance validation alert
  - Override section (conditional visibility)
  - Action buttons: Simpan Sebagai Draft, Submit Otorisasi, Batal

- [ ] `apps_zakat/web-vue/src/pages/keuangan/TransaksiUmumListPage.vue` — list page (optional, atau gabung dalam satu page)
  - Pagination di atas tabel
  - Filter: date_from, date_to, status
  - Columns: TransactionNo, ActualDate, Description, Amount, AuthStatus, Inputer
  - Row actions: View Detail, Edit, Delete

- [ ] Entry router di `apps_zakat/web-vue/src/router/index.ts`:
  ```typescript
  {
    path: '/keuangan/transaksi-umum',
    name: 'TransaksiUmum',
    component: () => import('@/pages/keuangan/TransaksiUmumPage.vue'),
    meta: { menu_key: 'keuangan.transaksi.umum' },
  },
  {
    path: '/keuangan/transaksi-umum/list',
    name: 'TransaksiUmumList',
    component: () => import('@/pages/keuangan/TransaksiUmumListPage.vue'),
    meta: { menu_key: 'keuangan.transaksi.umum' },
  },
  ```

- [ ] Entry di `apps_zakat/web-vue/src/components/AppSidebar.vue` — daftarkan menu item di grup Keuangan:
  ```vue
  <MenuItem label="Transaksi Umum" icon="icon-transaksi" to="/keuangan/transaksi-umum" 
            :visible="auth.hasMenu('keuangan.transaksi.umum')" />
  ```

---

## Layer 5 — Test (nuwis-test-gen, haiku)

- [ ] `testing/e2e-transaksi-umum.sh` — E2E smoke test:
  - Login sebagai ACC user
  - POST /api/transaction/general-transaction/create dengan 2 items (C + B)
  - Verify TransactionNo format GT-YYYY-BC-BPZIS-{7digit}
  - GET /api/transaction/general-transaction/{transaction_no} — verify items terekspor dengan benar
  - GET /api/transaction/general-transaction/list — verify transaksi ada di list
  - Cleanup (optional)

- [ ] `apps_zakat/api-python/tests/test_general_transaction.py` (optional) — unit tests:
  - Test create_transaction logic
  - Test item discriminators
  - Test CreateJournal integration
  - Test balance validation

---

## Verifikasi & Integration

```bash
# 1. Restart containers (setelah semua layer selesai)
cd infra
podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue

# 2. Verifikasi DWH view
psql -U transaction -d mziss_laz -c "SELECT * FROM dwh.v_general_transaction LIMIT 1;"

# 3. Apply seed
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/transaksi-umum-menu-and-rolemenu.sql

# 4. Jalankan E2E
bash testing/e2e-transaksi-umum.sh

# 5. Manual test di browser
# - Login sebagai ACC
# - Navigasi ke Keuangan > Transaksi Umum
# - Isi form, submit
# - Verifikasi TransactionNo di list dan detail
```

---

## Catatan Kompleksitas

1. **CreateJournal sangat kompleks** — melibatkan ParameterJournal lookup, pasangan debet-kredit otomatis, dan balance validation. Jika sudah ada implementasi CreateJournal di api-python → reuse. Jika belum → escalate ke Opus untuk implementasi.

2. **Discriminator hierarki 3-level** (TRANSACTIONITEMTYPE → ACCOUNTTITYPE) — mudah salah. Setup validation di schema Pydantic untuk mencegah kombinasi invalid.

3. **RAK otomatis antar cabang** — handle di service layer setelah create_transaction utama.

4. **Item types 4 macam dengan field berbeda** — use discriminated union di Pydantic untuk type safety.

5. **Balance validation menjadi critical** — frontend warning, backend CreateJournal check, keduanya harus berjalan.

---

*Plan created: 2026-06-17*

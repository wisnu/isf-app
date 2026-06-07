# Penyaluran Dana — Design Spec

**Date:** 2026-06-07
**Source:** Migrasi legacy `fFundDistribution` (DAF/Jython) → isf-app zakat portal
**Status:** Approved

---

## 1. Background

`fFundDistribution` adalah dialog input transaksi penyaluran dana (TranCode `DD001`) di sistem legacy DAF. Data sudah ada di DB (`mziss_laz`): 3.368 transaksi DD001 per 2026-06-07. Yang belum ada adalah UI dan API untuk membuat transaksi baru dari isf-app.

Ruang lingkup: **portal Zakat saja** (apps_zakat). Portal Wakaf dikecualikan karena COA dan produk berbeda.

---

## 2. Scope

**In scope:**
- Halaman list penyaluran dana (read, filter by date range + no transaksi)
- Halaman form create penyaluran baru
- 4 jenis pembayaran: Kas Kecil (K), Kas Cabang (C), Bank (B), Aset/GL (A)
- Integrasi budget (BudgetOwner + BudgetCode + DistributionItem) per item — opsional, bisa diisi atau dikosongkan
- API endpoints (api-python + BFF)
- Seed menu + role_menu

**Out of scope (versi pertama):**
- Edit transaksi → gunakan HistoriTransaksiPage yang sudah ada
- Hapus/cancel transaksi → HistoriTransaksiPage
- Cetak kwitansi (print) → belum di-scope
- Portal Wakaf

---

## 3. Legacy Reference Summary

File: `docs/legacy-apps/core/dialogs/Transaksi/fFundDistribution.*`
Server script: `docs/legacy-apps/core/scripts/Transaction/Distribution.py`

### Form Datasets

**Header (`uipTransaction`):**
| Field | Tipe | Keterangan |
|---|---|---|
| `ActualDate` | date | Tanggal posting — wajib |
| `ReferenceNo` | varchar(30) | No. referensi |
| `Description` | varchar(100) | Keterangan |
| `PaidTo` | varchar(30) | Dibayarkan kepada |
| `ReceivedFrom` | varchar(30) | Diterima dari (default: user inputer) |
| `BranchCode` | varchar(10) | Cabang user (dari session) |
| `TotalAmount` | double | Auto-computed dari sum items |
| `PaymentType` | varchar(1) | K/C/B/A |
| `CashType` | varchar(1) | K=Kas Kecil, C=Kas Cabang |
| `Rate` | double | Kurs mata uang |
| `CurrencyCode` | varchar(20) | Kode mata uang |
| `DonorId` | integer | Opsional |
| `SponsorId` | integer | Opsional |
| `VolunteerId` | varchar(10) | Opsional |
| `ProductBranchCode` | varchar(20) | Cabang produk penghimpunan |
| `FundAccountNo` | varchar(20) | Account produk penghimpunan (sumber dana) |

**Per PaymentType:**
| Kode | Nama | Field Tambahan |
|---|---|---|
| K | Kas Kecil | `LPettyCash.AccountNo` (rekening petty cash) |
| C | Kas Cabang | Otomatis dari BranchCode + CurrencyCode (tidak ada pilihan) |
| B | Bank | `LBank.AccountNo` (rekening bank) |
| A | Aset/GL | `LAsset.Account_Code` + `LValuta.Currency_Code` |

**Items (`uipTransactionItem`, multi-row):**
| Field | Tipe | Keterangan |
|---|---|---|
| `LProduct.ProductId` | integer | Produk penyaluran — wajib |
| `LProduct.FundCategory` | varchar(1) | Z/I/W/A/N |
| `Ashnaf` | varchar(1) | Kode ashnaf — wajib jika FundEntity=1 (Zakat) |
| `Amount` | double | Nilai — wajib, harus > 0 |
| `Description` | varchar(100) | Keterangan item |
| `FundEntity` | integer | 1=Z, 2=I/T, 3=W, 4=A, 5=N |
| `AccountNo` | varchar(30) | Product account penyaluran |
| `DistItemCode` | varchar(20) | Budget item account — opsional |
| `DistItemName` | varchar(60) | Budget item name |
| `OwnerId` | integer | Budget owner ID — opsional |
| `OwnerName` | varchar(30) | Budget owner name |
| `BudgetId` | integer | Budget ID — opsional |
| `BudgetCode` | varchar(10) | Budget code |
| `DistributionCategory` | varchar(1) | Kategori distribusi |

### FundEntity Mapping (legacy + isf-app)
```
'Z' → 1 (Zakat)
'I' → 2 (Infaq)
'T' → 2 (Titipan → maps to Infaq entity)
'W' → 3 (Wakaf)
'A' → 4 (Amil)
'N' → 5 (Non-halal)
```

### Journal Code Logic
- `JournalCode = '10'` jika `ProductBranchCode == BranchCode` (same branch)
- `JournalCode = '15'` jika `ProductBranchCode != BranchCode` (cross-branch)

### Channel Code per PaymentType
| PaymentType | ChannelCode | Keterangan |
|---|---|---|
| K | P | Petty Cash |
| C | R | Branch Cash |
| B | A | Bank Account |
| A | G | GL Asset |

---

## 4. Architecture

### Strategy
Extend modul `transaction/` yang ada di api-python. Buat BFF router baru. Tambah 2 halaman Vue.

### File Changes

**api-python (new files di `app/modules/transaction/`):**
```
penyaluran_schema.py    — Pydantic models
penyaluran_repo.py      — DB queries (lookup + list + detail)
penyaluran_service.py   — Business logic + journaling
```

**api-python (modify):**
```
app/modules/transaction/router.py  — tambah endpoint penyaluran
app/main.py                        — tidak perlu, sudah include transaction router
```

**bff-api (new):**
```
app/routers/penyaluran.py          — router baru
```

**bff-api (modify):**
```
app/main.py                        — include router baru
```

**web-vue (new):**
```
src/pages/keuangan/PenyaluranDanaPage.vue
src/pages/keuangan/PenyaluranDanaFormPage.vue
```

**web-vue (modify):**
```
src/router/index.ts                — tambah 2 route baru
src/lib/menu/registry.ts          — tambah menu key
src/components/AppSidebar.vue     — tambah sidebar entry
```

**infra/db/migrations/seed/ (new):**
```
seed-menu-penyaluran.sql
```

---

## 5. API Endpoints

### api-python: Lookup Endpoints

**GET `/api/transaction/penyaluran/lookup/rekening`**
- Query param: `type` = `bank` | `petty` | `cabang`
- `bank`: list BankCash accounts (financialaccount WHERE financialaccounttype='B')
- `petty`: list PettyCash accounts WHERE financialaccounttype='K'
- `cabang`: BranchCash untuk branch user (financialaccounttype='R')
- Response: `[{account_no, account_name, currency_code, bank_name?}]`

**GET `/api/transaction/penyaluran/lookup/produk`**
- Query param: `branch_code`
- Source: `transaction.productaccount pa JOIN fund.product p ON p.productid = pa.productid`
- Filter: produk yang tipe penyaluran (accounttitype='Z' di transactionitem legacy = produk distribusi)
- Response: `[{product_id, product_name, fund_category, account_no}]`

**GET `/api/transaction/penyaluran/lookup/product-account`**
- Query params: `product_id`, `branch_code`, `currency_code`
- Source: `transaction.productaccount` JOIN `fund.product`
- Response: `{account_no, account_name, fund_category, product_code}`

**GET `/api/transaction/penyaluran/lookup/anggaran`**
- Query param: `actual_date` (ISO), `branch_code`
- Source: `program.budget` (atau tabel anggaran yang relevan)
- Response: `[{budget_id, budget_code, budget_owner, owner_id}]`

**GET `/api/transaction/penyaluran/lookup/ashnaf`**
- Static response: list kode ashnaf zakat (Fakir, Miskin, Amil, Mualaf, Riqab, Gharimin, Fisabilillah, Ibnu Sabil)
- Response: `[{code, name}]`

**GET `/api/transaction/penyaluran/lookup/fund-product-account`**
- Query params: `branch_code`, `currency_code`
- Source: product accounts untuk produk penghimpunan (sumber dana distribusi)
- Response: `[{account_no, account_name, product_code, fund_category}]`

### api-python: CRUD Endpoints

**GET `/api/transaction/penyaluran/`**
- Query params: `begin`, `end` (ISO), `search` (no transaksi), `page`, `page_size`
- Filter: `transactioncode = 'DD001'`
- Response: `{data: [...], pagination: {page, limit, total, total_pages}}`

**GET `/api/transaction/penyaluran/{transaction_id}`**
- Response: header + items detail

**POST `/api/transaction/penyaluran/`**
- Body: `PenyaluranCreate` (lihat Section 6)
- Response: `{transaction_no, transaction_id}`

### BFF Endpoints (proxy dengan auth)

```
GET  /api/penyaluran/                        → proxy /api/transaction/penyaluran/
GET  /api/penyaluran/{id}                    → proxy /api/transaction/penyaluran/{id}
POST /api/penyaluran/                        → proxy /api/transaction/penyaluran/
GET  /api/penyaluran/lookup/rekening         → proxy lookup
GET  /api/penyaluran/lookup/produk           → proxy lookup
GET  /api/penyaluran/lookup/product-account  → proxy lookup
GET  /api/penyaluran/lookup/anggaran         → proxy lookup
GET  /api/penyaluran/lookup/ashnaf           → proxy lookup
GET  /api/penyaluran/lookup/fund-product-account → proxy lookup
```

Semua endpoint BFF: `require_menu('keuangan.transaksi.penyaluran')`.
`POST /api/penyaluran/`: field `inputer` diambil dari session user (tidak dari request body).

---

## 6. Data Models (Pydantic)

```python
class PenyaluranItem(BaseModel):
    product_id: int
    account_no: str
    ashnaf: str                    # wajib jika fund_entity == 1
    amount: float                  # harus > 0
    description: str
    fund_entity: int               # 1-5
    dist_item_account: str | None  # opsional
    budget_id: int | None          # opsional
    budget_code: str | None
    distribution_category: str | None

class PenyaluranCreate(BaseModel):
    actual_date: str               # ISO YYYY-MM-DD, wajib
    reference_no: str | None
    description: str
    paid_to: str | None
    received_from: str | None
    payment_type: Literal['K', 'C', 'B', 'A']
    payment_account_no: str | None # wajib untuk K dan B
    asset_code: str | None         # wajib untuk A
    asset_currency: str | None     # wajib untuk A
    rate: float = 1.0
    currency_code: str = 'IDR'
    fund_account_no: str           # wajib
    product_branch_code: str       # wajib (untuk journal code)
    donor_id: int | None
    items: list[PenyaluranItem]    # minimal 1

class PenyaluranListRow(BaseModel):
    transaction_id: int
    transaction_no: str | None
    actual_date: str               # ISO
    description: str | None
    amount: float
    payment_type: str
    channel_account_no: str | None
    channel_name: str | None
    inputer: str | None
    auth_status: str | None
    branch_code: str | None
```

---

## 7. Business Logic (Create)

### Alur `POST /api/transaction/penyaluran/` → `penyaluran_service.py`

```
1. Validasi input:
   - actual_date wajib
   - items minimal 1
   - tiap item: amount > 0, product_id wajib
   - jika fund_entity == 1: ashnaf wajib dan bukan 'L'
   - payment_type K atau B: payment_account_no wajib
   - payment_type A: asset_code + asset_currency wajib

2. BEGIN TRANSACTION

3. Get/create TransactionBatch untuk (actual_date, user):
   SELECT dari transaction.transactionbatch WHERE batchdate = actual_date AND inputer = user
   Jika tidak ada: INSERT batch baru

4. Generate transaction_no:
   Format: KK-YYYY-{branch}-{cash_code}-{7-digit-seq}
   Sequence dari transaction.seq_transaction (atau existing generator)

5. INSERT transaction.transaction:
   transactioncode = 'DD001'
   channelcode = per payment_type (P/R/A/G)
   channelaccountno = payment_account_no
   amount = sum(item.amount)
   actualdate = actual_date
   branchcode = branch_code (dari session)
   inputer = user_id (dari session)
   authstatus = 'P' (pending) — auto approval dikecualikan di versi pertama

6. journal_code = '10' jika product_branch_code == branch_code else '15'

7. Untuk tiap item di items:
   a. Lookup productaccount WHERE accountno = item.account_no
   b. INSERT transaction.transactionitem
   c. INSERT transaction.accounttransactionitem:
      - accounttitype = 'Z' (penyaluran)
      - mutation = 'D' (debit — mengurangi saldo produk)
      - amount = item.amount
      - fundentity = item.fund_entity
   d. Jika item.budget_id tidak null:
      INSERT transaction.budgettransaction

8. INSERT item pembayaran (kas/bank credit):
   INSERT transaction.accounttransactionitem:
   - accountno = payment_account_no (atau branch cash untuk type C)
   - mutation = 'C' (credit — mengurangi saldo kas/bank)
   - amount = total_amount

9. INSERT transaction.journal + journalitem (double-entry):
   - Debit: product accounts (penyaluran)
   - Credit: payment account (kas/bank)
   - Gunakan journal_code dari langkah 6

10. INSERT transaction.transhistoryofchanges (changetype='I')

11. COMMIT

12. Return {transaction_no, transaction_id}
```

### Validasi Error Codes:
| Kondisi | Error Code | HTTP |
|---|---|---|
| actual_date kosong | VALIDATION_ERROR | 422 |
| Items kosong | VALIDATION_ERROR | 422 |
| Amount <= 0 | VALIDATION_ERROR | 422 |
| Ashnaf kosong (Zakat) | VALIDATION_ERROR | 422 |
| Account tidak ditemukan | NOT_FOUND | 404 |
| DB error | SERVER_ERROR | 500 |

---

## 8. Frontend Design

### Route Configuration

```ts
// router/index.ts — di dalam children keuangan
{
  path: 'transaksi/penyaluran',
  name: 'keuangan-transaksi-penyaluran',
  component: () => import('@/pages/keuangan/PenyaluranDanaPage.vue'),
  meta: { title: 'Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
},
{
  path: 'transaksi/penyaluran/baru',
  name: 'keuangan-transaksi-penyaluran-baru',
  component: () => import('@/pages/keuangan/PenyaluranDanaFormPage.vue'),
  meta: { title: 'Input Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
},
```

### PenyaluranDanaPage.vue — List Page

Struktur: 3-part layout (toolbar → paginator-top → DataTable).

**Toolbar:**
- `DateField` Dari + `DateField` Sampai
- `Input` No. Transaksi (search)
- Button "Tampilkan" + Button "+ Input Penyaluran" (router-link ke `/baru`)

**Paginator** (standalone, di atas tabel, default 25 rows):
- "Showing X–Y of Z records"

**DataTable** (lazy, no built-in paginator):
| Kolom | Field | Format |
|---|---|---|
| No. Transaksi | transaction_no | — |
| Tanggal | actual_date | dmy() |
| Keterangan | description | — |
| Jenis Bayar | payment_type | badge (K/C/B/A) |
| Rekening | channel_name | — |
| Jumlah | amount | currency format |
| Status | auth_status | badge (P=Pending/A=Approved) |
| Inputer | inputer | — |

Klik baris → `router-push` ke HistoriTransaksiDetail dengan transaction_id.

### PenyaluranDanaFormPage.vue — Create Form

**Section Header:**
```
Tanggal Transaksi*   [DateField]          Cabang: {from session, read-only}
No. Referensi        [Input text]
Keterangan           [Input text]
Dibayarkan Kepada    [Input text]
Diterima Dari        [Input text]         Donatur (opt) [SearchSelect]
```

**Section Jenis Pembayaran (Tabs):**
```
[Kas Kecil] [Kas Cabang] [Bank] [Aset/GL]

Tab Kas Kecil (K):
  Rekening Kas Kecil* [SearchSelect ← GET /lookup/rekening?type=petty]
  Mata Uang: {auto dari rekening}  Rate: {editable jika non-IDR}

Tab Kas Cabang (C):
  Info: "Menggunakan kas cabang {branch_code}"
  Sumber Dana* [SearchSelect ← GET /lookup/fund-product-account]
  Cabang Produk [SearchSelect — bisa beda cabang]

Tab Bank (B):
  Rekening Bank* [SearchSelect ← GET /lookup/rekening?type=bank]
  Sumber Dana* [SearchSelect ← GET /lookup/fund-product-account, auto-fill dari bank]
  Cabang Produk [SearchSelect]
  Mata Uang: {auto}  Rate: {editable jika non-IDR}

Tab Aset/GL (A):
  Kode Aset* [Input text]
  Nama Aset  [Input text]
  Mata Uang* [SearchSelect]
  Rate       [Input number]
  Sumber Dana* [SearchSelect]
  Cabang Produk [SearchSelect]
```

**Section Items / Detail Distribusi:**
```
[+ Tambah Item]

DataTable editable (inline):
Produk*           Ashnaf*†    Anggaran     Jumlah*    Keterangan
[SearchSelect]    [Select]    [Opt Select] [Input]    [Input]

† Ashnaf hanya tampil/wajib jika produk FundCategory='Z'
```

**Footer:**
```
Total: Rp {auto-computed sum items}          [Batal] [Simpan]
```

**UX Rules:**
- Loading state pada setiap fetch lookup
- Toast sukses: "Transaksi DD001-... berhasil dibuat"
- Toast error: pesan dari API
- `finally` reset loading
- Tidak ada `alert()` atau `console.log`
- Redirect ke list page setelah save berhasil

### Komponen yang Dipakai (existing):
- `DateField.vue` — semua date input
- `SearchSelect.vue` — semua dropdown (rekening, produk, ashnaf, anggaran, donatur)
- `TablePagination.vue` — list page
- `Button.vue`, `Card.vue` dari `components/ui/`
- `DataTable` (PrimeVue unstyled) — items grid dan list table

---

## 9. Menu & Authorization

### Menu Key
```ts
// lib/menu/registry.ts
'keuangan.transaksi.penyaluran'
```

### Sidebar Entry
Grup "Transaksi" → child baru: "Input Penyaluran Dana"

### Role Access (dari legacy `AllowedGroups`):
- Legacy: `SPVDIST`, `DIST` (lihat fFundDistribution.bdl / menus/Transaksi.mnu)
- isf-app: seed ke `SPVDIST`, `DIST` (dan `ADM` untuk admin)

### Seed SQL (`infra/db/migrations/seed/seed-menu-penyaluran.sql`):
```sql
-- Menu entry
INSERT INTO isf_auth.menu (menu_key, menu_name, menu_group, sort_order, is_active)
VALUES ('keuangan.transaksi.penyaluran', 'Input Penyaluran Dana', 'keuangan.transaksi', 40, true)
ON CONFLICT (menu_key) DO NOTHING;

-- Role mapping
INSERT INTO isf_auth.role_menu (role_code, menu_key) VALUES
  ('SPVDIST', 'keuangan.transaksi.penyaluran'),
  ('DIST',    'keuangan.transaksi.penyaluran'),
  ('ADM',     'keuangan.transaksi.penyaluran')
ON CONFLICT DO NOTHING;
```

---

## 10. Testing

File: `testing/e2e-penyaluran.sh`

Coverage:
1. `GET /api/penyaluran/lookup/rekening?type=bank` — expect list rekening
2. `GET /api/penyaluran/lookup/produk?branch_code=001` — expect list produk
3. `GET /api/penyaluran/` — expect list DD001 paginated
4. `POST /api/penyaluran/` dengan PaymentType=B — expect transaction_no
5. `GET /api/penyaluran/{id}` — expect detail transaksi yang dibuat

---

## 11. Implementation Order

1. **api-python**: `penyaluran_schema.py` + `penyaluran_repo.py` (lookup + list)
2. **api-python**: `penyaluran_service.py` (create DD001)
3. **api-python**: extend `router.py` dengan endpoint baru
4. **bff-api**: `routers/penyaluran.py` + include ke `main.py`
5. **web-vue**: menu registry + route + sidebar
6. **web-vue**: `PenyaluranDanaPage.vue` (list)
7. **web-vue**: `PenyaluranDanaFormPage.vue` (form create)
8. **seed**: `seed-menu-penyaluran.sql`
9. **testing**: `testing/e2e-penyaluran.sh`

# Specs: Migrasi Menu TR0020 — Transaksi Penghimpunan Dana

**Tanggal:** 2026-06-08  
**Source:** `docs/legacy-apps/core/menus/Transaksi.mnu` — `Name='TR0020'`  
**Event:** Migrasi menu legacy ke isf-app web-vue  

---

## ==== HASIL ANALISIS MIGRASI ====

**FITUR:** Transaksi Penghimpunan Dana  
**MODUL:** `docs/legacy-apps/core/`  
**SOURCE:** `core/menus/Transaksi.mnu` — `Caption='Transaksi penghimpunan dana...'`, `OnClick='FundCollectionClick'`

---

## AKSES

| Legacy AllowedGroups | isf-app role_code |
|---|---|
| `ACC` | `ACC` |

**Menu key:** `keuangan.transaksi.penghimpunan`  
**Route:** `/keuangan/transaksi/penghimpunan`

---

## FORM

**Dialog path:** `dialogs/Transaksi/fFundCollection.*`  
**Handler:** `core/menus/Transaksi.py` → `FundCollectionClick()` → `app.CreateForm('Transaksi/fFundCollection', ...)`

### Datasets (dari `.svr`)

**`uipDonor`** — single row:
- `DonorId` (integer)
- `DonorNo` (varchar 20)
- `DonorName` (varchar 50)
- `DonorType` (varchar 20)
- `PhoneNumber` (varchar 30)
- `Address` (varchar 200)
- `LMarketer.MarketerId` (integer)
- `LMarketer.MarketerName` (varchar 40)

**`uipTransaction`** — single row (header):
- `TransactionDate` / `ActualDate` (timestamp) — tanggal transaksi
- `ReferenceNo` (varchar 30) — no. referensi, wajib kecuali Kas Cabang
- `Description` (varchar 100) — keterangan
- `TotalAmount` (double) — total otomatis dari item
- `Rate` (double) — kurs, default 1.0
- `CurrencyCode` (varchar 10) — default IDR
- `PaymentType` (varchar 1): `K`=Kas Kecil, `C`=Kas Cabang, `B`=Bank, `A`=Aset/GL
- `CashType` (varchar 1): `C`=Kas Cabang, `K`=Kas Kecil
- `BranchCode` (varchar 10) — auto dari session
- `LProductBranch.Kode_Cabang` — cabang produk
- `LBank.AccountNo/AccountName/BankName` — jika PaymentType='B'
- `LPettyCash.AccountNo` — jika PaymentType='K'
- `Inputer` — auto dari session
- `PaidTo` — penyetor (default: inputer)
- `SponsorId` (integer) — opsional
- `VolunteerId` (varchar 10) — opsional
- `TransactionNo` — auto-generated

**`uipTransactionItem`** — multi row (detail produk):
- `LProduct.ProductId` (integer) — produk dana
- `LProduct.ProductName` (varchar 30)
- `Amount` (double) — jumlah per produk
- `Description` (varchar 100) — keterangan item
- `FundEntity` (integer): 1=Zakat, 2=Infaq, 3=Wakaf, 4=Amil, 5=Non-halal
- `PercentageOfAmil` (double) — % dana amil
- `AccountNo` (varchar 30) — rekening produk

### Layout (dari `.dfr`)

- **Info Donatur**: DonorNo (lookup), DonorName (readonly), PhoneNumber (readonly), Address (readonly), Marketer
- **Tanggal Posting** + **Inputer** (readonly)
- **Jenis Pembayaran** (tab): Kas/Petty Cash | Bank | Aset
  - Tab Kas: Jenis Kas (Cabang/Kecil), Pilih Kas Kecil, Kode Valuta, Nilai Kurs, No. Referensi, Keterangan, Total Amount
  - Tab Bank: Rekening Bank, Nilai Kurs, No. Referensi, Keterangan, Total Amount
  - Tab Aset: Rekening Aktiva, Kode Valuta, Nilai Kurs, No. Referensi/FSZ, Keterangan, Total Amount
- **Detail Produk** (grid): Produk, Nilai, Keterangan, Jenis Dana, (%) Dana Amil
- **Mitra** + **Sponsor**

---

## UI FLOW (`fFundCollection_intr.py`)

**Saat form dibuka:**
- `BranchCode` ← session user (index 4)
- `Inputer` ← session user ID
- `PaidTo` ← inputer
- `TransactionDate` / `ActualDate` ← hari ini
- `CurrencyCode` ← IDR (default dari `ParameterGlobal`)
- `Rate` ← 1.0
- `CashType` ← 'C' (Kas Cabang default)
- Default Donor ← `ParameterGlobal.DEF_DONOR`

**Cari Donatur:**
- Manual input `DonorNo` → `CallServerMethod('GetDonorDataByNo', {DonorNo})` → isi DonorName, Phone, Address
- Tombol "Cari Donatur" → popup `Donatur/fSearchDonor`

**Pilih Bank → `LBankExit`:**
- Update `CurrencyCode`, `Rate`, `ProductId`, `ProductAccountNo`
- Populate `FundAccountNo` melalui `CallServerMethod('GetProductAccount', {ProductId, BranchCode, CurrencyCode})`

**Item produk:**
- Klik item → popup `Transaksi/fSelectProduct` → isi `ProductId`, `ProductName`, `FundEntity`, `PercentageOfAmil`, `AccountNo`
- Setiap item post → update `TotalAmount` += item.Amount

**Simpan:**
- Validasi: `ActualDate` wajib, minimal 1 item, `ReferenceNo` wajib (kecuali Kas Cabang), rekening pembayaran wajib
- `CommitBuffer()` → `CallServerMethod('SimpanData', DataPacket)`
- Backend dispatch ke: `scripts/Transaction/Collection.py` → `CollectionNew()`
- Setelah berhasil: tawarkan cetak kwitansi

---

## SAVE LOGIC (`scripts/Transaction/Collection.py`)

**Entry function:** `CollectionNew(config, srequest, params)` | `CollectionUpdate(...)`

**Payload dari form:**
```json
{
  "ActualDate": "...",
  "ReferenceNo": "...",
  "Description": "...",
  "PaidTo": "...",
  "DonorId": 0,
  "DonorNo": "...",
  "DonorName": "...",
  "MarketerId": 0,
  "SponsorId": 0,
  "VolunteerId": "...",
  "PaymentType": "B|K|C|A",
  "BankAccountNo": "...",
  "PettyCashAccountNo": "...",
  "AssetCode": "...",
  "AssetCurrency": "...",
  "CashCurrency": "IDR",
  "Rate": 1.0,
  "BranchCode": "...",
  "ProductBranchCode": "...",
  "Items": [
    { "ProductId": 0, "Amount": 0.0, "Description": "...",
      "FundEntity": 2, "PercentageOfAmil": 0.0, "AccountNo": "..." }
  ]
}
```

**Alur:**
1. `GetBatchUser(ActualDate)` — cari/buat batch harian user
2. `NewTransaction('SD001')` — buat transaksi header
3. Dispatch ke fungsi payment:
   - `'K'` → `PettyCashCollection()` — channel `'P'`
   - `'C'` → `BranchCashCollection()` — channel `'R'`
   - `'B'` → `BankCollection()` — channel `'A'`
   - `'A'` → `AssetCollection()` — channel `'G'`
4. Setiap fungsi: set data transaksi, loop items → `CreateDonorTransactionItem()`, `SetMutation()`, `SetJournalParameter()`
5. Buat item kas/bank: `CreateAccountTransactionItem()`, `SetMutation('D', total)`
6. Journal: `oTran.CreateJournal()`
7. `config.Commit()`

**Journal code:**
- `ProductBranchCode == BranchCode` → `'10'` (intra-branch)
- `ProductBranchCode != BranchCode` → `'15'` (inter-branch)

---

## SCHEMA DB (dari `app.mdt` + datadictionary)

**`transaction.transaction`** (header):
- `transactioncode = 'SD001'` — kode penghimpunan
- `channelcode`: K→'P', C→'R', B→'A', A→'G'
- `donorno`, `donorname`, `donorid`, `marketerid`, `sponsorid`, `volunteerid`
- `channelaccountno` — rekening kas/bank

**`transaction.transactionitem`** (item per produk + item kas):
- Product items: `mutationtype='C'` (credit — uang masuk ke dana)
- Payment item: `mutationtype='D'` (debit — uang diterima di kas)

**`transaction.accounttransactionitem`** (detail akuntansi):
- Product items: `accounttitype='D'` (discriminator penghimpunan)
- Payment item: no accounttitype (null)

**`transaction.journal`** + **`journalitem`**:
- Product items: `amount_credit = item_amount`, `amount_debit = 0`
- Payment item: `amount_debit = total_amount`, `amount_credit = 0`

**Balance update** (`transaction.financialaccount`):
- Semua akun yang terlibat: `balance = balance + amount` (uang masuk)

**Transaction number format:** `KM-{YYYY}-{branch}-{cashCode}-{seq:07d}`

---

## HANDOFF KE AGENT LAIN

```
→ isf-agent-seed:
  MENU_KEY: keuangan.transaksi.penghimpunan
  LABEL: Input Penghimpunan Dana
  ROLES: ACC
  SOURCE: core/menus/Transaksi.mnu — AllowedGroups='ACC'

→ isf-agent-python:
  MODULE: penghimpunan (di transaction module)
  TRANSACTION_CODE: SD001
  ENDPOINTS:
    GET  /transaction/penghimpunan/lookup/rekening?type={bank|petty|cabang}
    GET  /transaction/penghimpunan/lookup/produk?branch_code=&currency=
    GET  /transaction/penghimpunan/lookup/donor?q=
    GET  /transaction/penghimpunan/
    GET  /transaction/penghimpunan/{id}
    POST /transaction/penghimpunan/

→ isf-agent-bff:
  ROUTER: app/routers/penghimpunan.py
  MENU_KEY: keuangan.transaksi.penghimpunan
  PREFIX: /penghimpunan

→ isf-agent-ui:
  PAGE_LIST: PenghimpunanDanaPage.vue
  PAGE_FORM: PenghimpunanDanaFormPage.vue
  ROUTE_LIST: /keuangan/transaksi/penghimpunan
  ROUTE_FORM: /keuangan/transaksi/penghimpunan/baru
  SIDEBAR_SECTION: Transaksi
```

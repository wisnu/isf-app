# Migration Analysis — Transaksi Umum (General Transaction)

> **CATATAN KOMPLEKSITAS TINGGI**: Modul ini mengandung jurnal akuntansi bertingkat
> (CreateJournal dipanggil di level Transaction), 4 jenis item mutasi dengan
> discriminator hierarkis, tabel ACCOUNTTRANSACTIONITEM dengan inheritance 3-level
> (AccountTransactionItem → DonorTransactionItem / ZakahDistTransactItem), dan
> logika override otorisasi. Rekomendasi: gunakan model `opus` untuk implementation
> sprint ini.

---

## Overview

| Key | Value |
|---|---|
| **Modul** | `docs/legacy-apps/core/` |
| **Portal** | zakat |
| **Scope** | Transaksi Umum (General Transaction) — `transactioncode = 'GT'` |
| **Tanggal** | 2026-06-17 |
| **Kompleksitas** | TINGGI |
| **Workflow** | Custom (composite form: header + 4 jenis item mutasi) |

### Fitur List

| No. | Caption | Roles | Dialog | Menu Key Kandidat |
|---|---|---|---|---|
| 1 | Transaksi Umum | ACC | `dialogs/TransaksiUmum/fTransaksiUmum.*` | `keuangan.transaksi.umum` |

**Sumber menu**: `menus/Transaksi.mnu`, Caption='Transaksi umum...', `OnClick='GeneralTransactionClick'`, `AllowedGroups='ACC'`

**Catatan arsitektur**: `GeneralTransactionClick` (menus/Transaksi.py baris 184) membuka
`dialogs/Transaksi/fGeneralTransaction/` — bukan `dialogs/TransaksiUmum/` secara langsung.
`fTransaksiUmum` adalah dialog mutasi rekening yang dipakai sebagai child dari
`fGeneralTransaction` melalui mekanisme `MutExExecute` (accounting form interaction).
Di isf-app, ini harus menjadi satu form terpadu.

---

## Form Fields (per item type)

### Header Transaksi

> Source: `dialogs/TransaksiUmum/fTransaksiUmum.svr` (uipTransaksi) + `fTransaksiUmum_data.py`

| Field | DataType | Required | Caption | Keterangan |
|---|---|---|---|---|
| `no_referensi` | String(30) | Optional | Nomor Referensi | Nomor cek/kwitansi eksternal |
| `keterangan` | String(50) | Optional | Keterangan | Keterangan transaksi keseluruhan |
| `user_override` | String(20) | Conditional | User Override | Hidden; muncul jika melebihi limit |
| `password_override` | String(20) | Conditional | Password Override | Hidden; muncul jika melebihi limit |

**Read-Only (auto-fill dari session)**:
- `branch_code` — dari `config.SecurityContext.GetUserInfo()[4]`
- `inputer` — dari session user
- `actual_date` — dari batch user hari ini

### Item Mutasi — Semua Jenis (fields bersama)

| Field | DataType | Required | Caption |
|---|---|---|---|
| `item_type` | String(1) | Required | Jenis Mutasi ('C'/'D'/'B'/'G') |
| `kode_valuta` | String(3) | Required | Kode Valuta |
| `nilai_mutasi` | Double | Required | Nilai / Amount |
| `nilai_kurs` | Double | Conditional | Nilai Kurs (wajib jika non-default currency) |
| `kode_kurs` | String(20) | Conditional | Kode Kurs |
| `keterangan` | String(50) | Optional | Keterangan baris |

### Item Mutasi 'C' — Penghimpunan (Collection)

> Source: `scripts/Transaction/GeneralTransaction.py` baris 167-201

| Field | DataType | Required | Caption |
|---|---|---|---|
| `product_id` | Integer | Required | ID Produk ZIS |
| `donor_id` | Integer | Required | ID Donatur |
| `mutation_type` | String(1) | Required | 'C'=Kredit ke produk |
| `fund_entity` | Integer | Required | Jenis Dana (1=Zakat,2=Infaq,3=Wakaf,4=Amil,5=Non-halal) |

### Item Mutasi 'D' — Penyaluran (Distribution)

> Source: `scripts/Transaction/GeneralTransaction.py` baris 203-244

| Field | DataType | Required | Caption |
|---|---|---|---|
| `dist_account_no` | String(30) | Required | Nomor Rekening Program Penyaluran |
| `fund_account_no` | String(30) | Required | Nomor Rekening Sumber Dana |
| `ashnaf` | String(1) | Required | Golongan Asnaf (F/M/U/H/G/S/I/A) |
| `mutation_type` | String(1) | Required | 'D'=Debet atau 'C'=Kredit |
| `fund_entity` | Integer | Required | Jenis Dana |

### Item Mutasi 'B' — Kas/Bank (Cash/Bank Account)

> Source: `scripts/Transaction/GeneralTransaction.py` baris 246-270

| Field | DataType | Required | Caption |
|---|---|---|---|
| `account_no` | String(30) | Required | Nomor Rekening Kas/Bank |
| `mutation_type` | String(1) | Required | 'D'=Debet / 'C'=Kredit |
| `jenis_aplikasi_giro` | String(1) | Conditional | 'A'=Aplikasi/'B'=Bilyet Giro/'C'=Cek (aktif jika rekening Giro) |
| `no_referensi_giro` | String(7) | Conditional | Nomor warkat giro |

### Item Mutasi 'G' — Ledger / GL Accounting

> Source: `scripts/Transaction/GeneralTransaction.py` baris 272-310

| Field | DataType | Required | Caption |
|---|---|---|---|
| `account_code` | String(20) | Required | Kode Akun COA |
| `account_name` | String(100) | Required | Nama Akun (RefAccountName) |
| `mutation_type` | String(1) | Required | 'D'=Debet / 'C'=Kredit |
| `budget_id` | Integer | Optional | ID Budget (0 = tidak ada) |

**Sections** (dari `.dfr`): MultiPages: 'Input mutasi rekening' (tab 0) + 'Daftar mutasi' (tab 1)

**Hidden fields** (tersimpan di dataset, tidak tampil):
- `is_default_currency`, `akun_gl_interface`, `jns_rek_liab`, `is_virtual_account`,
  `actual_account_no`, `branch_code_rekening`
- `user_override`, `password_override` — visible=false kecuali limit terlampaui

---

## DB Schema Mapping

### Entitas Utama

#### `Transaction` → tabel: `TRANSACTION`

| Kolom DB | Type | Keterangan |
|---|---|---|
| `TRANSACTIONID` | PK autoincrement | |
| `TRANSACTIONNO` | VARCHAR(30) | Format: `GT-{year}-{branch}-BPZIS-{7digit}` |
| `TRANSACTIONCODE` | VARCHAR(10) | Selalu `'GT'` untuk modul ini |
| `TRANSACTIONDATE` | TIMESTAMP | Tanggal input |
| `ACTUALDATE` | TIMESTAMP | Tanggal posting (dari batch user) |
| `REFERENCENO` | VARCHAR(30) | no_referensi |
| `DESCRIPTION` | VARCHAR(100) | keterangan |
| `INPUTER` | VARCHAR(20) | user session |
| `BRANCHCODE` | VARCHAR(5) | branch session |
| `AUTHSTATUS` | VARCHAR(1) | 'T'=Otorisasi / 'F'=Belum |
| `ISPOSTED` | VARCHAR(1) | 'T'/'F' |
| `AMOUNT` | DOUBLE | Total kredit |
| `CURRENCYCODE` | VARCHAR(20) | |
| `RATE` | DOUBLE | Kurs |
| `AUTHUSER` | VARCHAR(20) | User yang otorisasi |
| `AUTHDATE` | TIMESTAMP | |
| `JOURNALBLOCKID` | INTEGER | Link ke jurnal akuntansi |
| `JOURNALNO` | VARCHAR(30) | Nomor jurnal |

#### `TransactionItem` → tabel: `TRANSACTIONITEM`

| Kolom DB | Type | Keterangan |
|---|---|---|
| `TRANSACTIONITEMID` | PK autoincrement | |
| `TRANSACTIONID` | FK → TRANSACTION | |
| `TRANSACTIONITEMTYPE` | VARCHAR(1) | **DISCRIMINATOR**: 'A'=AccountItem, 'G'=GLItem |
| `BRANCHCODE` | VARCHAR(5) | |
| `CURRENCYCODE` | VARCHAR(20) | |
| `MUTATIONTYPE` | VARCHAR(1) | 'D'=Debet / 'C'=Kredit |
| `AMOUNT` | DOUBLE | Nilai item |
| `RATE` | DOUBLE | Kurs |
| `EKUIVALENAMOUNT` | DOUBLE | Nilai ekuivalen (Amount × Rate) |
| `DESCRIPTION` | VARCHAR(100) | Keterangan item |
| `REFACCOUNTNO` | VARCHAR(30) | Nomor rekening referensi |
| `REFACCOUNTNAME` | VARCHAR(100) | Nama rekening referensi |
| `ACCOUNTCODE` | VARCHAR(20) | Kode akun COA |
| `PARAMETERJOURNALID` | VARCHAR(5) | ID parameter jurnal (selalu '10' untuk GT) |

#### `AccountTransactionItem` → tabel: `ACCOUNTTRANSACTIONITEM`

| Kolom DB | Type | Keterangan |
|---|---|---|
| `TRANSACTIONITEMID` | PK, FK → TRANSACTIONITEM | |
| `ACCOUNTNO` | FK → FINANCIALACCOUNT | |
| `ACCOUNTTITYPE` | VARCHAR(1) | **DISCRIMINATOR**: 'A'=base, 'D'=Donor, 'Z'=ZakahDist |
| `FUNDENTITY` | INTEGER | 1=Zakat,2=Infaq,3=Wakaf,4=Amil,5=Non-halal |
| `ISUPDATEBALANCE` | VARCHAR(1) | 'T'/'F' |
| `FUNDACCOUNTNO` | VARCHAR(30) | |

#### `DonorTransactionItem` (extends AccountTransactionItem, `ACCOUNTTITYPE='D'`)

Kolom tambahan di `ACCOUNTTRANSACTIONITEM`:

| Kolom DB | Type | Keterangan |
|---|---|---|
| `DONORID` | INTEGER | ID Donatur |
| `MARKETERID` | INTEGER | ID Marketer |
| `AMOUNTPERUNIT` | DOUBLE | |
| `TOTALUNIT` | INTEGER | |
| `PERCENTAGEOFAMIL` | DOUBLE | Default 0.0 |

#### `ZakahDistTransactItem` (extends AccountTransactionItem, `ACCOUNTTITYPE='Z'`)

Kolom tambahan di `ACCOUNTTRANSACTIONITEM`:

| Kolom DB | Type | Keterangan |
|---|---|---|
| `ASHNAF` | VARCHAR(1) | F/M/U/H/G/S/I/A |
| `DISTRIBUTIONITEMACCOUNT` | VARCHAR(20) | |
| `FUNDACCOUNTNO` | VARCHAR(30) | Nomor rekening sumber dana |
| `MUSTAHIQID` | INTEGER | |
| `DISTRIBUTIONCATEGORY` | VARCHAR(1) | |
| `PRODUCTACCOUNTNO` | FK → PRODUCTACCOUNT | |

#### `GLTransactionItem` (extends TransactionItem, `TRANSACTIONITEMTYPE='G'`)

Kolom tambahan di `TRANSACTIONITEM`:

| Kolom DB | Type | Keterangan |
|---|---|---|
| `GLNUMBER` | VARCHAR(30) | = account_code |
| `GLNAME` | VARCHAR(100) | = account_name |

### Relasi

```
TRANSACTION (1) ──< TRANSACTIONITEM (N)
TRANSACTIONITEM ──> ACCOUNTTRANSACTIONITEM  [when TRANSACTIONITEMTYPE='A']
TRANSACTIONITEM ──> [juga TRANSACTIONITEM itu sendiri untuk GLItem, dengan GLNUMBER/GLNAME]
ACCOUNTTRANSACTIONITEM ──> DonorTransactionItem    [when ACCOUNTTITYPE='D']
ACCOUNTTRANSACTIONITEM ──> ZakahDistTransactItem   [when ACCOUNTTITYPE='Z']
ACCOUNTTRANSACTIONITEM.ACCOUNTNO ──> FINANCIALACCOUNT
```

### Autonumber GT

**Format**: `GT-{year}-{branchCode}-BPZIS-{7digit_seq}`
**Contoh**: `GT-2026-001-BPZIS-0000001`
**Source**: `scripts/Transaction/TransactionHelper.py` baris 26-47 + `GeneralTransaction.py` baris 265
**Sequence**: `nextval('seq_transactionnumber')` di schema `transaction`
**Cash code**: `'BPZIS'`

---

## Save Logic (per item type)

### Entry Point

**Via form UI**: `menus/Transaksi.py` baris 184 → `app.CreateForm('Transaksi/fGeneralTransaction')` → `fTransaksiUmum.showTransactionDialog()` → `bSimpanClick` → `accForm.MutExExecute(ph)` → `_data.py baris 139` → `processTransaction()`

**Via ExecuteScript (standalone)**: `scripts/Transaction/GeneralTransaction.py` → `CreateTransaction('GT', config, srequest, params)`

### Alur Utama `CreateTransaction` (GeneralTransaction.py baris 61-97)

1. `simplejson.loads(srequest)` → parse request JSON
2. `GetBatch(helper, request['ActualDate'])` → `helper.CreateObject('BatchHelper').GetBatchUser()` — 1 batch per user per hari
3. `oBatch.NewTransaction('GT')` → buat Transaction baru, set `TransactionCode='GT'`
4. `helper.CreatePObject('TransHistoryOfChanges')` → log riwayat perubahan
5. `ExecFunction('GT', helper, oTran, oBatch, request, params)` → dispatch ke `GeneralTransaction()`
6. `corporate.CheckLimitOtorisasi(oTran.Amount * request['Rate'])` → cek limit otorisasi
   - Jika lolos: `oTran.AutoApproval()` → set `AuthStatus='T'`
7. `oTran.CreateJournal()` → generate journal entries via ParameterJournal='10'
   - Jika `status==2`: raise Exception (balance mismatch)
8. `config.Commit()` — atau `config.Rollback()` on exception

### Alur `GeneralTransaction()` (baris 148-268)

1. Set header: Inputer, BranchCode, ReferenceNo, Description, Amount=TotalCredit, ActualDate=BatchDate
2. Loop setiap item dalam `request['Items']` — dispatch per `aItemType`
3. `oTran.GenerateTransactionNumber('BPZIS')` → format autonumber GT
4. `oTran.SaveInbox(params)` → simpan ke inbox notifikasi
5. `oTran.GetKwitansi()` → generate nomor kwitansi

### Item Type 'C' — Penghimpunan

> Source: `GeneralTransaction.py` baris 167-201

1. Lookup `ProductAccount WHERE ProductId=:pid AND BranchCode=:bc AND CurrencyCode=:valuta`
2. Lookup `Donor WHERE DonorId=:did`
3. `oTran.CreateDonorTransactionItem(oProductAccount, DonorId, DonorType)` → INSERT ke TRANSACTIONITEM + ACCOUNTTRANSACTIONITEM dengan ACCOUNTTITYPE='D'
4. `SetMutation(Amount, Rate)` atau `SetReverseMutation(Amount, Rate)`
5. `SetCollectionEntity(FundEntity)` → set FUNDENTITY
6. `PercentageOfAmil = 0.0`
7. `SetJournalParameter('10')`
8. Setelah semua item: `oTran.CreateJournal()` → ParameterJournal='10'

### Item Type 'D' — Penyaluran

> Source: `GeneralTransaction.py` baris 203-244

1. Lookup `ProductAccount(DistAccountNo)` → program penyaluran
2. Lookup `ProductAccount(FundAccountNo)` → sumber dana
3. `oTran.CreateZakahDistTransactItem(oDistProductAccount, Ashnaf)` → INSERT ACCOUNTTRANSACTIONITEM dengan ACCOUNTTITYPE='Z'
4. `SetMutation(MutationType, Amount, Rate)`
5. `oItemPA.FundEntity = FundEntity`
6. `oItemPA.AccountCode = oFundProductAccount.GetDistributionInterface(Ashnaf, oDistProduct)`
7. `oItemPA.FundAccountNo = FundAccountNo`
8. `SetJournalParameter('10')`

### Item Type 'B' — Kas/Bank

> Source: `GeneralTransaction.py` baris 246-270

1. Lookup `CashAccount WHERE AccountNo=:no` → `CastToLowestDescendant` (bisa BankCash/BranchCash/PettyCash)
2. `oTran.CreateAccountTransactionItem(oAccount)` → INSERT ACCOUNTTRANSACTIONITEM dengan ACCOUNTTITYPE='A'
3. `SetMutation(MutationType, Amount, Rate)`
4. `SetJournalParameter('10')`
5. Update saldo: `UPDATE financialaccount SET saldo = saldo ± amount`

### Item Type 'G' — Ledger / GL

> Source: `GeneralTransaction.py` baris 272-310

1. `oTran.CreateGLTransactionItem(AccountCode, Valuta)` → INSERT TRANSACTIONITEM dengan TRANSACTIONITEMTYPE='G', GLNUMBER=AccountCode, GLNAME=AccountName
2. `oItemGL.RefAccountName = AccountName`
3. `SetMutation(MutationType, Amount, Rate)`
4. `SetJournalParameter('10')`
5. Jika `BudgetId != 0`:
   - Lookup `Budget WHERE BudgetId=:id`
   - Jika `AccountType in ['L','X','A','I'] AND MutationType='D'`: `oItemGL.CreateBudgetTransaction(BudgetId)` → INSERT BUDGETTRANSACTION
   - Jika `MutationType='C'`: `oItemGL.CreateBudgetTransactionReturn(BudgetId)`

### Update Transaksi (UpdateTransaction, baris 99-144)

1. Ambil transaksi existing via `TransactionNo`
2. `oTran.DeleteJournal()` → hapus jurnal lama (DeleteTransactionJournal)
3. `oTran.CancelTransaction()` → batalkan transaksi lama
4. Reassign `BatchId + TransactionCode`
5. `ExecFunction()` ulang → re-create semua items
6. `CreateJournal()` ulang
7. `oTran.AutoApprovalUpdate()`

---

## Discriminators (KRITIS)

> **JANGAN HILANGKAN** discriminator ini saat implementasi. Salah discriminator = data corrupt di seluruh laporan.

| Tabel | Kolom | Nilai | Artinya |
|---|---|---|---|
| `TRANSACTION` | `TRANSACTIONCODE` | `'GT'` | Transaksi Umum (General Transaction) |
| `TRANSACTIONITEM` | `TRANSACTIONITEMTYPE` | `'A'` | AccountTransactionItem (kas/bank/produk) |
| `TRANSACTIONITEM` | `TRANSACTIONITEMTYPE` | `'G'` | GLTransactionItem (ledger langsung) |
| `ACCOUNTTRANSACTIONITEM` | `ACCOUNTTITYPE` | `'D'` | DonorTransactionItem (Penghimpunan) |
| `ACCOUNTTRANSACTIONITEM` | `ACCOUNTTITYPE` | `'Z'` | ZakahDistTransactItem (Penyaluran) |
| `ACCOUNTTRANSACTIONITEM` | `ACCOUNTTITYPE` | `'A'` | AccountTransactionItem base (Kas/Bank) |
| `TRANSACTION` | `AUTHSTATUS` | `'T'` | Sudah otorisasi |
| `TRANSACTION` | `AUTHSTATUS` | `'F'` | Belum otorisasi |
| `TRANSACTION` | `ISPOSTED` | `'T'` | Sudah diposting ke jurnal |
| `TRANSACTIONITEM` | `MUTATIONTYPE` | `'D'` | Debet |
| `TRANSACTIONITEM` | `MUTATIONTYPE` | `'C'` | Kredit |
| `ACCOUNTTRANSACTIONITEM` | `FUNDENTITY` | `1` | Zakat |
| `ACCOUNTTRANSACTIONITEM` | `FUNDENTITY` | `2` | Infaq |
| `ACCOUNTTRANSACTIONITEM` | `FUNDENTITY` | `3` | Wakaf |
| `ACCOUNTTRANSACTIONITEM` | `FUNDENTITY` | `4` | Amil |
| `ACCOUNTTRANSACTIONITEM` | `FUNDENTITY` | `5` | Non-halal |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'F'` | Fakir |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'M'` | Miskin |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'U'` | Mualaf |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'H'` | Hamba Sahaya |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'G'` | Gharimin |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'S'` | Fisabillillah |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'I'` | Ibnu Sabil |
| `ACCOUNTTRANSACTIONITEM` | `ASHNAF` | `'A'` | Amil |

---

## Jurnal Rules

### Mekanisme

- **Semua** 4 jenis mutasi menggunakan `SetJournalParameter('10')` → referensi ke `PARAMETERJOURNAL` di DB dengan kode `'10'`
- Setelah semua item selesai diinsert, `oTran.CreateJournal()` dipanggil sekali
- `CreateJournal()` membaca `PARAMETERJOURNAL` untuk menentukan pasangan debet-kredit COA otomatis
- Jika `status==2` dari `CreateJournal()`: raise Exception → rollback (balance mismatch)
- Source: `GeneralTransaction.py` baris 88-90

### Validasi Balance

- Tidak ada validasi D=K di sisi client (konfirmasi dari `fTransaksiUmum_intr.py`)
- Balance check dipercayakan ke `oTran.CreateJournal()` di backend
- **Untuk isf-app**: tambahkan validasi D=K di frontend sebelum submit (warning, bukan blocker)
- Untuk import massal (`scripts/importmassal/TransaksiUmum.py` baris 257): `apiJournal.CheckBalance()` dipanggil eksplisit

### RAK Otomatis Antar Cabang

- Jika rekening kas/bank milik cabang berbeda (`buat_RAK_otomatis=1`): `CreateJournal()` memanggil `CreateJournalItemsRAK()` → generate entry RAK di kedua cabang
- Source: `fTransaksiUmum_intr.py` baris 78-82 (flag detection) + `_data.py` baris 190-195

---

## API Endpoints Target

| Method | Path | Logika |
|---|---|---|
| `POST` | `/api/transaction/general-transaction/create` | CreateTransaction('GT') → ExecFunction → CreateJournal → return TransactionNo |
| `POST` | `/api/transaction/general-transaction/update` | UpdateTransaction → DeleteJournal + Cancel + re-create |
| `GET` | `/api/transaction/general-transaction/rekening-info` | Query param: `no_rekening` — lookup CashAccount atau RekeningLiabilitas, return nama/valuta/jenis |
| `GET` | `/api/transaction/general-transaction/kurs-info` | Query param: `kode_kurs`, `currency_code` — query masterkurs |
| `POST` | `/api/transaction/general-transaction/cek-limit` | CekLimitTransaksi — Corporate.CheckLimitTransaksi(maxDebetAmount) |
| `POST` | `/api/transaction/general-transaction/cek-override` | CekOverride — Corporate.OverrideCheck(userOverride, password, '22131') |

### Request Shape `POST /create`

```json
{
  "actual_date": "2026-06-17",
  "reference_no": "KWT-001",
  "description": "Keterangan transaksi",
  "rate": 1.0,
  "items": [
    {
      "item_type": "C",
      "product_id": 1,
      "donor_id": 42,
      "valuta": "IDR",
      "amount": 500000,
      "rate": 1.0,
      "mutation_type": "C",
      "fund_entity": 1,
      "description": "Zakat mal dari donatur"
    },
    {
      "item_type": "B",
      "account_no": "KAS-001-IDR",
      "mutation_type": "D",
      "valuta": "IDR",
      "amount": 500000,
      "rate": 1.0,
      "description": "Terima tunai"
    }
  ]
}
```

---

## Roles & Menu Key

| Key | Value |
|---|---|
| **Menu Key** | `keuangan.transaksi.umum` |
| **Label** | Transaksi Umum |
| **Roles** | `ACC` |
| **ISF-App Role Code** | `ACC` (mapping 1:1 dari legacy) |

---

## Handoff ke nuwis-* Builders

### → nuwis-seed-gen

```
MENU_KEY: keuangan.transaksi.umum
LABEL:    Transaksi Umum
ROLES:    ACC
```

### → nuwis-db-migrator

```
DWH_VIEWS:
  - dwh.v_general_transaction
    JOIN: TRANSACTION + TRANSACTIONITEM + ACCOUNTTRANSACTIONITEM
    WHERE: TRANSACTION.TRANSACTIONCODE = 'GT'
    Kolom minimal:
      transactionid, transactionno, actualdate, branchcode,
      referenceno, description, inputer, authstatus, amount,
      transactionitemid, transactionitemtype, accounttitype, mutationtype,
      item_amount, fundentity, accountno, accountcode

MIGRATIONS:
  Tidak ada tabel baru. Gunakan skema existing:
  - transaction.TRANSACTION
  - transaction.TRANSACTIONITEM
  - transaction.ACCOUNTTRANSACTIONITEM
  - transaction.TRANSITEMGLINTERFACE
  Pastikan seq_transactionnumber ada di schema transaction.
```

### → nuwis-python-builder

```
ENDPOINTS: (lihat tabel API Endpoints di atas)

DISCRIMINATORS yang harus di-hardcode:
  - TRANSACTIONCODE = 'GT' selalu di setiap INSERT TRANSACTION
  - TRANSACTIONITEMTYPE: 'A' untuk item kas/bank/produk; 'G' untuk GL
  - ACCOUNTTITYPE: 'D'=Penghimpunan, 'Z'=Penyaluran, 'A'=Kas/Bank base
  - FUNDENTITY: 1=Zakat, 2=Infaq, 3=Wakaf, 4=Amil, 5=Non-halal
  - MUTATIONTYPE: 'D'=Debet, 'C'=Kredit
  - PARAMETERJOURNALID: '10' untuk semua item GT

POLA PYTHON 2 → ISF-APP:
  - raise Exception, 'msg' → raise HTTPException(400, detail='msg')
  - simplejson.loads(srequest) → json.loads() / pydantic schema
  - config.BeginTransaction() → asyncpg transaction context manager
  - config.Now() → date.today().isoformat()
  - config.SecurityContext.UserId → BFF session → inputer_id di payload
  - Hardcoded branch di form → BFF _resolve_branch() dari session
```

### → nuwis-ui-builder

```
PAGE_TYPE: form (composite — header + multi-item lines; bukan list/laporan)

FIELDS HEADER:
  - reference_no: Input [optional] — Nomor Referensi/Kwitansi
  - description: Input [optional] — Keterangan Transaksi

ITEM LINES (repeatable, toggle per item_type):
  Semua jenis: item_type selector, valuta, amount, rate, description
  item_type='C' (Penghimpunan): + product_id (SearchSelect), donor_id (SearchSelect),
                                  mutation_type, fund_entity (dropdown)
  item_type='D' (Penyaluran):   + dist_account_no, fund_account_no, ashnaf (dropdown),
                                  mutation_type, fund_entity
  item_type='B' (Kas/Bank):     + account_no (SearchSelect), mutation_type,
                                  jenis_aplikasi_giro (conditional), no_referensi_giro (conditional)
  item_type='G' (Ledger):       + account_code, account_name (ReadOnly auto-fill),
                                  mutation_type, budget_id (optional)

DISPLAY GRID (ReadOnly setelah item ditambah):
  Kolom: Jenis, No Rekening, Nama, D/K, Nilai, Valuta, Kurs, Ekuivalen, Keterangan
  Baris summary: Total Debit | Total Kredit (highlight merah jika tidak balance)

UI BEHAVIOR:
  - Tombol "Tambah Item" → buka panel/dialog input item baru
  - Tombol "Edit" → edit item yang dipilih
  - Tombol "Hapus" → hapus item yang dipilih
  - Warning sebelum submit jika Total Debit ≠ Total Kredit
  - Jika override limit: tampilkan input user_override + password_override
```

---

## Catatan Implementasi Kritis

1. **fTransaksiUmum bukan standalone** — di legacy ia adalah sub-dialog yang dipanggil oleh `fGeneralTransaction` via `MutExExecute`. Di isf-app ini harus menjadi **satu form terpadu** yang menangani semua 4 item type dalam satu halaman.

2. **CreateJournal ada di layer Transaction module** — bukan di `GeneralTransaction.py`. Implementasi api-python harus memanggil service CreateJournal yang sudah ada (atau diimplementasi ulang sebagai service terpisah).

3. **Validasi D=K tidak ada di legacy client** — harus ditambahkan di isf-app frontend sebagai warning sebelum submit.

4. **`_data_alternater.py` menggunakan `BatchTransaksi2`** (pendekatan alternatif) — implementasi isf-app harus menggunakan satu jalur yang konsisten. Rekomendasi: ikuti path `_data.py` (MutasiEksternalProcessor).

5. **RAK antar cabang** — jika rekening kas/bank milik cabang berbeda, jurnal RAK dibuat otomatis. Ini harus dihandle di layer service, bukan UI.

6. **Import massal** (`scripts/importmassal/TransaksiUmum.py`) memiliki jalur terpisah dari form input. Dapat diimplementasi sebagai endpoint upload CSV terpisah.

---

*Sumber file yang dibaca:*
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/menus/Transaksi.mnu` — AllowedGroups='ACC', baris 285-288
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/menus/Transaksi.py` — baris 184-188
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/dialogs/TransaksiUmum/fTransaksiUmum.svr`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/dialogs/TransaksiUmum/fTransaksiUmum.dfr`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/dialogs/TransaksiUmum/fTransaksiUmum_intr.py`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/dialogs/TransaksiUmum/fTransaksiUmum_data.py`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/dialogs/TransaksiUmum/fTransaksiUmum_data_alternater.py`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/scripts/Transaction/GeneralTransaction.py`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/scripts/Transaction/TransactionHelper.py`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/scripts/importmassal/TransaksiUmum.py`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/script_modules/FormTransaksi.py`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/app.mdt`
- `/home/wishnew/workshop/isf-app/docs/legacy-apps/core/default.mcf`

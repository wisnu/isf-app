# MIGRATION_ANALYSIS: Upload Data Penerimaan ZIS Rutin

## Overview

- **Legacy form:** dialogs/Transaksi/fUploadHCTrans (+ List, View, Update, Delete)
- **Workflow type:** Upload/Batch (File XLS → Preview → Submit → Otorisasi SPVKEU → Authorize → Batch Transaksi)
- **Portal:** zakat
- **Tanggal analisis:** 2026-06-15

---

## Fitur List

| # | Caption | Roles | Dialog | Menu Key Kandidat |
|---|---|---|---|---|
| 1 | Upload Data Penerimaan ZIS Rutin | ACC | dialogs/Transaksi/fUploadHCTrans.* | transaksi.upload.zis-rutin |
| 2 | List Upload Data Penerimaan ZIS Rutin | ACC | dialogs/Transaksi/fUploadHCTransList.* | transaksi.upload.zis-rutin-list |
| 3 | Detail / View Batch | ACC (dari List) | dialogs/Transaksi/fUploadHCTransView.* | (sub-dialog, tidak perlu menu key terpisah) |
| 4 | Update Tanggal Transaksi Batch | ACC (dari List) | dialogs/Transaksi/fUploadHCTransUpdate.* | (sub-dialog, tidak perlu menu key terpisah) |
| 5 | Hapus Batch + Rollback Transaksi | ACC (dari List) | dialogs/Transaksi/fUploadHCTransDelete.* | (sub-dialog, tidak perlu menu key terpisah) |

---

## Form Fields (dari _data.py / _intr.py / .svr)

### BATCH HEADER (uipBatch — SingleRow)

| Field | Type | Required | Notes |
|---|---|---|---|
| NamaFile | varchar(200) | Required | Path/nama file .xls di workstation — input file picker |
| TanggalTransaksi | timestamp | Required | Tanggal efektif transaksi; default = config.Now() |
| IsSendSMS | varchar(1) | Optional | HIDDEN — T/F kirim SMS; di-force 'F' sebelum authorize loop |
| BatchPeriodDesc | varchar(50) | Read-only | Diisi dari Cell B2 file XLS; harus unik di DB |
| ZakatTotal | double | Read-only | Computed dari parse XLS |
| InfaqTotal | double | Read-only | Computed dari parse XLS |
| AnakAsuhTotal | double | Read-only | Computed dari parse XLS |
| AnakYatimTotal | double | Read-only | Computed dari parse XLS |
| WakafTotal | double | Read-only | Computed (TIDAK diproses ke transaksi — dinonaktifkan) |
| TaqurmaTotal | double | Read-only | Computed dari parse XLS (Qurban) |
| GrandTotal | double | Read-only | Sum semua total amount |
| ZakatTotalRecord | integer | Read-only | Count baris donatur per jenis |
| InfaqTotalRecord | integer | Read-only | Count baris donatur infaq |
| AnakAsuhTotalRecord | integer | Read-only | Count baris donatur anak asuh |
| AnakYatimTotalRecord | integer | Read-only | Count baris donatur anak yatim |
| WakafTotalRecord | integer | Read-only | Count baris donatur wakaf |
| TaqurmaTotalRecord | integer | Read-only | Count baris donatur qurban |
| GrandTotalRecord | integer | Read-only | Total seluruh baris data |

### ITEM DATA (uipItem — MultiRow, read-only grid setelah parse)

| Field | Type | Required | Notes |
|---|---|---|---|
| DataNo | integer | — | Nomor urut baris |
| EmployeeNumber | varchar(20) | — | NIP — kolom 6 XLS |
| EmployeeName | varchar(100) | — | Nama karyawan — kolom 8 XLS |
| BusinessAreaCode | varchar(10) | — | Kode area — kolom 3 XLS |
| BusinessAreaDesc | varchar(200) | — | Deskripsi area — kolom 4 XLS |
| BirthPlace | varchar(200) | — | Tempat lahir — kolom 10 XLS |
| WorkAreaName | varchar(100) | — | Nama area kerja — kolom 11 XLS |
| MobilePhone | varchar(20) | — | HP — kolom 12 XLS |
| BirthDate | timestamp | — | Tanggal lahir — kolom 13 XLS |
| Gender | varchar(1) | — | L/P (MALE→L, FEMALE→P) — kolom 14 XLS |
| MaritalStatus | varchar(1) | — | K/B/S (MARRD.→K, SINGLE→B, DIVC./WIDOW/WDOWER→S) — kolom 15 XLS |
| Position | varchar(200) | — | Jabatan — kolom 16 XLS |
| OrganizationUnit | varchar(200) | — | Unit organisasi — kolom 17 XLS |
| ZakatAmount | double | — | Nominal zakat — kolom 18 XLS × -1 |
| InfaqAmount | double | — | Nominal infaq — kolom 19 XLS × -1 |
| AnakAsuhAmount | double | — | Nominal anak asuh — kolom 20 XLS × -1 |
| AnakYatimAmount | double | — | Nominal anak yatim — kolom 21 XLS × -1 |
| WakafAmount | double | — | Nominal wakaf — kolom 22 XLS × -1 (TIDAK diproses) |
| TaqurmaAmount | double | — | Nominal qurban — kolom 23 XLS × -1 |
| TotalAmount | double | — | Sum semua amount per baris |
| Description | varchar(200) | — | Keterangan (HIDDEN di grid) |
| ValidationDesc | varchar(120) | — | Keterangan validasi (HIDDEN di grid) |

**HIDDEN fields (tidak ditampilkan ke user):** WorkAreaId, WorkUnitId, WorkPositionId, WorkBussinessAreaId, BatchPeriodDesc

**SECTIONS:** pUpload (header file + tanggal), pTotal (totals summary), gRecon (grid items)

**READ_ONLY:** Semua field kolom summary + BatchPeriodDesc (otomatis dari file XLS)

---

## File Upload Spec

- **Format:** Excel (.xls) — diparse server-side via `pyFlexcel` (legacy) → ganti dengan `openpyxl` di isf-app baru
- **Cell B2 (row=2, col=1):** `BatchPeriodDesc` — identifier unik periode batch
- **Data rows:** mulai dari **ROW 8**, iterasi sampai kolom 1 kosong

### Mapping Kolom XLS (1-based)

| Kolom | Field |
|---|---|
| 3 | BusinessAreaCode |
| 4 | BusinessAreaDesc |
| 6 | EmployeeNumber (NIP) |
| 8 | EmployeeName |
| 10 | BirthPlace |
| 11 | WorkAreaName |
| 12 | MobilePhone |
| 13 | BirthDate |
| 14 | Gender: `MALE`→`L`, `FEMALE`→`P` |
| 15 | MaritalStatus: `MARRD.`→`K`, `SINGLE`→`B`, `DIVC.`/`WIDOW`/`WDOWER`→`S` |
| 16 | Position |
| 17 | OrganizationUnit |
| 18 | ZakatAmount (nilai di file negatif, dikali -1) |
| 19 | InfaqAmount (nilai di file negatif, dikali -1) |
| 20 | AnakAsuhAmount (nilai di file negatif, dikali -1) |
| 21 | AnakYatimAmount (nilai di file negatif, dikali -1) |
| 22 | WakafAmount (nilai di file negatif, dikali -1 — **TIDAK diproses ke transaksi**) |
| 23 | TaqurmaAmount / Qurban (nilai di file negatif, dikali -1) |

---

## DB Schema

### Tabel Target (schema: transaction)

#### `transaction.humancapitalbatch`

| Kolom | Tipe | Keterangan |
|---|---|---|
| batchid | INTEGER PK | Auto sequence |
| description | VARCHAR(200) | Deskripsi batch |
| batchperioddesc | VARCHAR(50) | UNIQUE — dari cell B2 XLS |
| uploaddate | TIMESTAMP | Waktu upload |
| uploaduserid | VARCHAR(50) | User yang upload |
| transactiondate | TIMESTAMP | Tanggal efektif transaksi |

#### `transaction.humancapitalbatchitem`

| Kolom | Tipe | Keterangan |
|---|---|---|
| batchitemid | INTEGER PK | Auto sequence |
| batchid | INTEGER FK | → humancapitalbatch.batchid |
| description | VARCHAR(200) | Keterangan |
| transactionid | INTEGER | Link ke Transaction setelah authorize |
| businessareacode | VARCHAR(10) | |
| businessareadescription | VARCHAR(200) | |
| employeenumber | VARCHAR(30) | NIP |
| name | VARCHAR(200) | Nama karyawan |
| birthdate | TIMESTAMP | |
| birthplace | VARCHAR(150) | |
| gender | VARCHAR(10) | |
| maritalstatus | VARCHAR(20) | |
| position | VARCHAR(200) | |
| organizationalunit | VARCHAR(200) | |
| amountzakat | DOUBLE | |
| amountinfaq | DOUBLE | |
| amountanakyatim | DOUBLE | |
| amountanakasuh | DOUBLE | |
| amountwakaf | DOUBLE | |
| amountqurban | DOUBLE | |
| iscreateemployeedata | VARCHAR(1) | T/F: apakah donor baru dibuat dari baris ini |
| donorid | INTEGER FK | → fund.donor.donorid |
| workareaname | VARCHAR(100) | |
| mobilephone | VARCHAR(20) | |
| smslog_id | INTEGER | |
| smslog_time | TIMESTAMP | |

#### `transaction.humancapitalpassedreport`

| Kolom | Tipe | Keterangan |
|---|---|---|
| reportid | INTEGER PK | Auto sequence |
| batchid | INTEGER FK | → humancapitalbatch.batchid |
| employeenumber | VARCHAR(30) | |
| donorid | INTEGER FK | → fund.donor.donorid |

Catatan: tabel ini menyimpan donatur internal yang **tidak ada** di file upload (absen dari batch).

### Tabel yang Dimodifikasi (tidak dibuat ulang)

| Tabel | Operasi | Keterangan |
|---|---|---|
| `fund.donor` | INSERT | Donor baru: DonorGroup='R', DonorType='I', DonorNo='P'+7digit |
| `fund.individualdonor` | INSERT/UPDATE | IsInternalEmployee='T' — karyawan internal |
| `fund.donorcommitment` | INSERT/UPDATE (upsert) | Komitmen rutin per rekening per donor |
| `fund.donorcommitmenthistory` | INSERT | Trail perubahan komitmen |
| `fund.donorfieldhistory` | INSERT | Trail perubahan field data donatur |
| `fund.custom_idgen` | UPDATE | Counter ID donatur ('DONOR', prefix 'P') |
| `transaction.transaction` | INSERT | 1 per jenis dana aktif per baris karyawan |
| `transaction.transactionitem` | INSERT | 2 per transaksi (product + bank/kas) |
| `transaction.accounttransactionitem` | INSERT | Item akuntansi |
| `transaction.donortotalfund` | UPDATE | Saldo total donasi per donor per fundentity |
| `transaction.financialaccount` | UPDATE | Saldo rekening bank + product account |
| `transaction.journal` | INSERT | 1 per transaksi |
| `transaction.journalitem` | INSERT | Items jurnal akuntansi |
| `transaction.journalblock` | INSERT | Block jurnal |
| `transaction.transactionbatch` | GET/CREATE | Batch harian (BatchTag='OPR') |
| `transaction.transhistoryofchanges` | INSERT | Audit trail Create/Edit/Delete |

---

## Save Logic (dari _data.py / scripts)

### Upload + Simpan ke Otorisasi (fUploadHCTrans_data.py)

```python
# ON OPEN (FormSetDataEx, DatasetCount == 0):
TanggalTransaksi = config.Now()
IsSendSMS = 'T'  # akan di-force 'F' sebelum authorize loop

# PROSES BACA FILE (UploadClick → server):
file_stream = upload ke server
period_desc = cell B2 XLS  # BatchPeriodDesc
if GetObjectByNames('HumanCapitalBatch', {'BatchPeriodDesc': period_desc}):
    raise Exception, 'Periode sudah ada'
items = parse rows from row 8 sampai kolom 1 kosong
  amount *= -1  # nilai di XLS negatif
compute totals per jenis dana

# SIMPAN (bSimpanClick → save()):
# Validasi: TanggalTransaksi tidak kosong, uipItem.RecordCount > 0
kode_entri = 'TRANS041'
id_peran = 'SPVKEU'
enterprise.api.otorisasi.storeDataPacket(packet) → PENDING otorisasi
```

### Authorize Flow (fUploadHCTrans_data.py → authorize())

```python
# Sumber: dialogs/Transaksi/fUploadHCTrans_data.py → authorize()
# Dipanggil dari halaman Otorisasi saat SPVKEU approve

# Step 1: Get/create batch harian
oBatch = GetBatchUser(config, TanggalTransaksi)
# → scripts/Transaction/Batch.py → GetBatchUser()
# → GET/CREATE TransactionBatch(BatchTag='OPR', IsPosted='T', IsClosed='F')

# Step 2: Load parameter bank dari enterprise.ParameterGlobal
params = {
    'BANKZAKAT': GetProductParamByBankAccount('BANKZAKAT'),
    'BANKINFAQ': GetProductParamByBankAccount('BANKINFAQ'),
    'BANKASUH':  GetProductParamByBankAccount('BANKASUH'),
    'BANKYATIM': GetProductParamByBankAccount('BANKYATIM'),
    'BANKQURBAN':GetProductParamByBankAccount('BANKQURBAN'),
    # BANKWAKAF tidak diproses
}

# Step 3: Buat HumanCapitalBatch header
oHCBatch = CreatePObject('HumanCapitalBatch')
oHCBatch.UploadDate = now()
oHCBatch.UploadUserId = config.SecurityContext.UserId
oHCBatch.BatchPeriodDesc = BatchPeriodDesc
oHCBatch.TransactionDate = TanggalTransaksi
# → INSERT transaction.humancapitalbatch

# Step 4: Buat semua HumanCapitalBatchItem
for item in uipItem:
    oItem = CreatePObject('HumanCapitalBatchItem')
    oItem.BatchId = oHCBatch.BatchId
    oItem.EmployeeNumber = item.EmployeeNumber
    oItem.Name = item.EmployeeName
    # ... semua field amount ...
    oItem.IsCreateEmployeeData = 'F'
    # → INSERT transaction.humancapitalbatchitem

config.FlushUpdates()  # INSERT batch + items ke DB

# Step 5: Sinkronisasi data donatur existing
UpdateDonorData():  # per item yang ada donornya
    for field in [MARITALSTATE, WORKPOSITION, WORKUNIT, MOBILEPHONE, DONORNAME]:
        if field berubah:
            INSERT fund.donorfieldhistory
            UPDATE fund.individualdonor / fund.donor

# Step 6: Generate donor baru (via SQL batch — bukan ORM per-row)
SQL: SET_FLAG_NEWDONOR
    UPDATE humancapitalbatchitem SET IsCreateEmployeeData='T', DonorId=nextval('donor_seq')
    WHERE NOT EXISTS (SELECT 1 FROM fund.individualdonor WHERE WorkIdentityNumber = employeenumber)

SQL: CREATE_NEWDONOR
    INSERT INTO fund.donor (DonorGroup='R', Status='A', DonorType='I', DonorNo='P'+7digit, ...)

SQL: CREATE_NEWDONORINDIVIDUAL
    INSERT INTO fund.individualdonor (IsInternalEmployee='T', ...)

SQL: UPDATE_DONOR_CUSTOM_IDGEN
    UPDATE fund.custom_idgen counter

SQL: SET_DONORID
    UPDATE humancapitalbatchitem.donorid via JOIN fund.individualdonor

# Step 7: Update DonorCommitment (komitmen rutin)
UpdateDonorCommitment():  # per account parameter
    for account in [BANKZAKAT, BANKINFAQ, BANKASUH, BANKYATIM, BANKWAKAF, BANKQURBAN]:
        for item in batch:
            if INSERT DonorCommitment baru, atau amount berbeda:
                INSERT fund.donorcommitmenthistory
                INSERT/UPDATE fund.donorcommitment

config.FlushUpdates()

# Step 8: Buat transaksi per baris × per jenis dana (IsSendSMS di-force 'F')
SQL: SELECT humancapitalbatchitem JOIN fund.donor ORDER BY BatchItemId
for row in query:
    for dana_type in [Zakat, Infaq, AnakAsuh, AnakYatim, Qurban]:  # Wakaf SKIP
        if amount[dana_type] != 0:
            oTran = oBatch.NewTransaction('SD002')
            oTran.ChannelCode = 'A'          # auto/payroll
            oTran.HCBatchItemId = BatchItemId
            oTran.GenerateTransactionNumber('BPZIS')  # → BPZIS-xxxx
            CreateDonorTransactionItem(oTran, FundEntity[dana_type], amount)
            # → INSERT transaction.transactionitem (accounttitype='D')
            CreateAccountTransactionItem(oTran, bank_param, amount)
            # → INSERT transaction.accounttransactionitem
            oTran.AutoApproval()             # authorizationstatus = 'A'
            oTran.CreateJournal()
            # → INSERT transaction.journal + journalitem + journalblock

config.FlushUpdates()

# Step 9: Catat donatur absen dari batch ini
INSERT transaction.humancapitalpassedreport
    WHERE karyawan internal (IsInternalEmployee='T') TIDAK ADA di batch ini
```

### Delete Flow (fUploadHCTransDelete_data.py → authorize())

```python
# Menggunakan temp table untuk efisiensi — BUKAN cascade ORM
preparetmptable()  # CREATE TEMP TABLE tmp_HCTransactionGroup

HC_PrepareHCTransactionGroup:
    INSERT tmp dari Transaction WHERE transactioncode='SD002' AND HCBatchItem.batchid=BatchId

HC_SelectDonorFundForUpdate:   SELECT FOR UPDATE NOWAIT DonorTotalFund
HC_SelectFinAccountForUpdate:  SELECT FOR UPDATE NOWAIT FinancialAccount

HC_UpdateDonorFundEntity:      UPDATE DonorTotalFund.totalamount -= amount per fundentity
HC_UpdateDonorFundEntityTotal: UPDATE DonorTotalFund.totalamount -= amount (fundentity=0)
HC_UpdateBankAccountBalance:   UPDATE FinancialAccount.balance -= amount (bank)
HC_UpdateProductAccountBalance:UPDATE FinancialAccount.balance -= amount (product)

HC_DeleteJournal / JournalItem / JournalBlock  # DELETE jurnal (cascade order)
HC_DeleteTransaction / TransactionItem / AccountTransactionItem  # DELETE transaksi
HC_DeleteBatch         # DELETE humancapitalbatch
HC_DeleteBatchItem     # DELETE humancapitalbatchitem
HC_DeleteReportItem    # DELETE humancapitalpassedreport
HC_CreateTransHistoryOfChanges: INSERT transhistoryofchanges (ChangeType='D')
```

### Update Tanggal Flow (fUploadHCTransUpdate_data.py → authorize())

```python
preparetmptable()
HC_PrepareHCTransactionGroup        # isi temp table
HC_SelectTransactionForUpdate       # SELECT FOR UPDATE NOWAIT
HC_SelectJournalForUpdate           # SELECT FOR UPDATE NOWAIT

HC_UpdateTransactionDate:  UPDATE transaction.transaction SET actualdate = new_date
HC_UpdateJournalDate:      UPDATE transaction.journal SET
                               journal_date = new_date,
                               periode_code = DAY(new_date),
                               fl_accountingperiode = MONTH(new_date),
                               fl_accountingyear = YEAR(new_date)
HC_UpdateHCBatchDate:      UPDATE humancapitalbatch.transactiondate = new_date
HC_CreateTransHistoryOfChanges: INSERT transhistoryofchanges (ChangeType='E')
```

---

## Discriminators

| Kolom | Value | Keterangan |
|---|---|---|
| `transaction.transactioncode` | `'SD002'` | **KRITIS** — identifikasi transaksi HC/payroll; bukan SD001 atau kode lain |
| `transaction.channelcode` | `'A'` | **KRITIS** — channel "auto/payroll" |
| `transaction.transactionnumber` prefix | `'BPZIS'` | **KRITIS** — nomor transaksi format BPZIS-xxxx |
| `transactionitem.accounttitype` | `'D'` | Product account (sisi donor/penghimpunan) |
| `transactionitem.accounttitype` | `'C'` | Lawan akun (sisi bank/kas) |
| `fundentity` | `1` | Zakat |
| `fundentity` | `2` | Infaq/Sedekah (juga AnakAsuh, AnakYatim, Qurban) |
| `fundentity` | `3` | Wakaf — **DINONAKTIFKAN**, tidak diproses |
| `individualdonor.isinternalemployee` | `'T'` | Karyawan perusahaan (bukan donatur umum) |
| `donor.donorgroup` | `'R'` | Donatur rutin (dibuat dari HC batch) |
| `donor.donortype` | `'I'` | Individual |
| `donor.donorno` prefix | `'P'` | Kode donatur karyawan: P + 7 digit |
| `humancapitalbatchitem.iscreateemployeedata` | `'T'` | Donor baru dibuat dari baris ini |
| `humancapitalbatchitem.iscreateemployeedata` | `'F'` | Donor sudah ada sebelumnya |
| `transactionbatch.batchtag` | `'OPR'` | Batch operasional harian |
| `transhistoryofchanges.changetype` | `'N'` | Buat baru |
| `transhistoryofchanges.changetype` | `'E'` | Edit (update tanggal) |
| `transhistoryofchanges.changetype` | `'D'` | Delete |
| `ParameterGlobal.key` | `'BANKZAKAT'` | Rekening bank zakat |
| `ParameterGlobal.key` | `'BANKINFAQ'` | Rekening bank infaq |
| `ParameterGlobal.key` | `'BANKASUH'` | Rekening bank anak asuh |
| `ParameterGlobal.key` | `'BANKYATIM'` | Rekening bank anak yatim |
| `ParameterGlobal.key` | `'BANKQURBAN'` | Rekening bank qurban |

---

## Status / Approval Flow

Fitur ini sepenuhnya melewati sistem otorisasi maker-checker isf-app.

### Otorisasi Codes (dari legacy → mapping ke isf-app)

| Operasi | Kode Entri | Approver |
|---|---|---|
| Upload baru | `TRANS041` | SPVKEU |
| Hapus batch | `TRANS043` | SPVKEU |
| Update tanggal | `TRANS044` | SPVKEU |

### Lifecycle Status di isf-app (menggunakan `otorisasi.submission`)

```
DRAFT → PENDING (setelah save-and-submit) → PROCESSING (saat SPVKEU approve)
      ↘ AUTHORIZED (background task selesai)
      ↘ PENDING kembali (jika background task gagal + dispatch_error terisi)
      ↘ REJECTED → DRAFT (bisa revisi)
```

Dispatcher yang perlu didaftarkan di `otorisasi/service.py:_register_defaults()`:
- `hc_zis_upload` → `hc_zis_service.create_from_payload`
- `hc_zis_delete` → `hc_zis_service.delete_from_payload`
- `hc_zis_update_date` → `hc_zis_service.update_date_from_payload`

---

## Menu Access

| Field | Value |
|---|---|
| Menu Label | Upload Data Penerimaan ZIS Rutin |
| Menu Key Kandidat | `transaksi.upload.zis-rutin` |
| List Menu Key Kandidat | `transaksi.upload.zis-rutin-list` |
| AllowedGroups (legacy) | `ACC` |
| Roles isf-app | `ACC` |
| Parent menu | Transaksi → Upload |

---

## Catatan Penting

### 1. Parse XLS — openpyxl bukan pyFlexcel
Legacy menggunakan `pyFlexcel` (Jython). Di isf-app baru harus menggunakan `openpyxl`. Nilai amount di XLS sudah negatif, wajib dikali -1 saat parse.

### 2. Satu baris karyawan = hingga 5 transaksi
Setiap baris karyawan menghasilkan transaksi terpisah per jenis dana yang amount != 0:
Zakat (FundEntity=1), Infaq (FundEntity=2), AnakAsuh (FundEntity=2), AnakYatim (FundEntity=2), Qurban (FundEntity=2). **Wakaf DINONAKTIFKAN.**

### 3. BatchPeriodDesc harus unik
Cek duplikat wajib dilakukan saat parse: `SELECT * FROM humancapitalbatch WHERE batchperioddesc = ?`. Jika sudah ada, tolak upload.

### 4. Delete menggunakan temp table + balance reverse
Delete tidak bisa menggunakan ORM cascade biasa. Harus menggunakan pendekatan SQL:
- SELECT FOR UPDATE NOWAIT untuk locking
- UPDATE balance DonorTotalFund dan FinancialAccount
- DELETE dalam urutan yang benar (jurnal → transaksi → batch)

### 5. Auto-create donor menggunakan SQL batch
Pembuatan donor baru menggunakan SQL langsung (`SET_FLAG_NEWDONOR` → `CREATE_NEWDONOR` → dst) bukan loop ORM per-row. Ini penting untuk performa saat file berisi ratusan baris.

### 6. Update tanggal mengubah accounting period di jurnal
`fl_accountingperiode` (MONTH) dan `fl_accountingyear` (YEAR) di `transaction.journal` harus ikut diupdate saat tanggal transaksi berubah. Ini kritis untuk laporan keuangan per periode.

### 7. IsSendSMS dinonaktifkan
Meskipun field ada, nilai `IsSendSMS` di-force `'F'` sebelum loop authorize. Di isf-app baru, field ini dapat diabaikan atau dihapus.

### 8. Urutan event kritis saat authorize
Urutan eksekusi tidak boleh diubah:
1. FlushUpdates setelah insert batch items
2. Sinkronisasi donor existing
3. Generate donor baru (SQL batch)
4. Update DonorCommitment
5. FlushUpdates lagi
6. Buat transaksi + jurnal per item

---

## Kompleksitas

- **Level:** TINGGI
- **Alasan:** 5 dialog saling terhubung; multi-entity write (7+ tabel); auto-create donor baru dengan SQL batch; update DonorCommitment upsert; per baris hingga 5 transaksi + jurnal; delete menggunakan temp table + balance reverse; update date mempengaruhi accounting period di jurnal; semua operasi melewati otorisasi maker-checker
- **Workflow:** Upload (File → Preview → Submit → Otorisasi SPVKEU → Authorize Background → Batch Transaksi)

---

## Handoff ke nuwis-* Builders

### nuwis-seed-gen

```
MENU_KEY_1: transaksi.upload.zis-rutin
LABEL_1:    Upload Data Penerimaan ZIS Rutin
ROLES_1:    ACC

MENU_KEY_2: transaksi.upload.zis-rutin-list
LABEL_2:    List Upload Data Penerimaan ZIS Rutin
ROLES_2:    ACC

Parent: Transaksi → Upload (buat group jika belum ada)
```

### nuwis-db-migrator

```
VERIFIKASI terlebih dahulu apakah tabel berikut sudah ada di mziss_laz:
  - transaction.humancapitalbatch
  - transaction.humancapitalbatchitem
  - transaction.humancapitalpassedreport

Jika belum ada → buat migration:
  V###__create_humancapital_tables.sql

Pertimbangkan: apakah menggunakan tabel HC legacy terpisah,
atau mengintegrasikan ke transaction.batchupload yang sudah ada di isf-app.
Rekomendasi: gunakan tabel HC terpisah agar discriminator tetap eksplisit.
```

### nuwis-python-builder

```
ENDPOINTS:
  POST   /api/transaction/upload/hc-zis/parse
         — Upload file XLS, parse preview (batch header + items), cek duplikat BatchPeriodDesc
         — Return: { batch_period_desc, totals, items[] }

  POST   /api/transaction/upload/hc-zis/submit
         — Simpan ke otorisasi.submission (save-and-submit → langsung PENDING)
         — payload: { tanggal_transaksi, batch_period_desc, items[], totals }
         — kode_entri: TRANS041, id_peran: SPVKEU

  GET    /api/transaction/upload/hc-zis/batches
         — List semua batch (paginated), dengan status otorisasi
         — Filter: batch_period_desc, date range

  GET    /api/transaction/upload/hc-zis/batches/{id}
         — Detail batch + semua items

  PUT    /api/transaction/upload/hc-zis/batches/{id}/date
         — Update tanggal (via save-and-submit → PENDING, kode_entri TRANS044)

  DELETE /api/transaction/upload/hc-zis/batches/{id}
         — Hapus batch (via save-and-submit → PENDING, kode_entri TRANS043)

  POST   /api/transaction/upload/hc-zis/batches/{id}/approve
         — Background task: jalankan full authorize flow
         — Return: { status: "PROCESSING" } segera, background eksekusi langkah 1-9

DISCRIMINATORS KRITIS (jangan hilangkan):
  - transaction.transactioncode = 'SD002'
  - transaction.channelcode = 'A'
  - transaction.transactionnumber prefix = 'BPZIS'
  - transactionitem.accounttitype = 'D' (product/donor side)
  - individualdonor.isinternalemployee = 'T'
  - donor.donorgroup = 'R', donor.donortype = 'I'
  - donor.donorno prefix = 'P' (+ 7 digit dari custom_idgen)
  - FundEntity: Zakat=1, Infaq/AnakAsuh/AnakYatim/Qurban=2, Wakaf=3 (SKIP)
  - ParameterGlobal keys: BANKZAKAT, BANKINFAQ, BANKASUH, BANKYATIM, BANKQURBAN

LOGIKA KHUSUS:
  - openpyxl parse: cell B2, rows mulai row 8, amount *= -1
  - Auto-create donor: SQL batch (bukan ORM per-row) — kritis untuk performa
  - Delete: SELECT FOR UPDATE NOWAIT + balance reverse + cascade manual
  - Update date: update journal.fl_accountingperiode + fl_accountingyear
```

### nuwis-ui-builder

```
PAGE_TYPE: Upload dengan file picker + preview table + summary totals → submit ke otorisasi

HALAMAN 1 — UploadHCZisPage.vue
  Route: /transaksi/upload/zis-rutin
  SECTION HEADER:
    - Input file (.xlsx/.xls only): NamaFile
    - DateField: TanggalTransaksi (ISO string, default = today)
    - Button "Proses Baca File" → POST /parse → isi preview
  SECTION TOTALS (read-only, muncul setelah parse):
    - BatchPeriodDesc (label dari file)
    - Tabel: Zakat | Infaq | Anak Asuh | Anak Yatim | Wakaf | Taqurma | Grand Total
    - Baris: Nominal + Jumlah Donatur
  SECTION PREVIEW TABLE (DataTable, read-only):
    Kolom: No, NIP, Nama, Zakat, Infaq, Anak Asuh, Anak Yatim, Wakaf, Taqurma, Total, HP
  ACTIONS: Button "Simpan" (disabled sebelum parse berhasil) + Button "Batal"
  STATE: empty state sebelum file dipilih

HALAMAN 2 — UploadHCZisListPage.vue
  Route: /transaksi/upload/zis-rutin/list
  TOOLBAR: search BatchPeriodDesc, filter date range
  PAGINATOR (standalone, di atas, default 25 rows)
  DataTable lazy:
    Kolom: Deskripsi Periode | Tanggal Transaksi | User Upload | Status Otorisasi
    Row actions: [View] [Edit Tanggal] [Hapus]
  Showing X-Y of Z records

DIALOG View — UploadHCZisDetailDrawer.vue (slide dari kanan)
  Header: BatchPeriodDesc, TanggalTransaksi, UploadUserId
  DataTable items read-only: kolom sama dengan preview

DIALOG Update Tanggal — Modal
  Show read-only: BatchPeriodDesc
  DateField editable: TanggalTransaksi baru
  Sesuai rule MEMORY.md: tampilkan data lengkap batch sebelum confirm

DIALOG Hapus — Modal
  Sesuai rule MEMORY.md "delete via form modal":
  Tampilkan form read-only: BatchPeriodDesc, TanggalTransaksi, summary totals
  Confirm: "Anda yakin akan menghapus data transaksi penghimpunan ZIS rutin ini?"

FILTERS: batch_period_desc (text), tanggal_mulai, tanggal_sampai
```

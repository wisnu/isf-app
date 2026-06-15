# Parity Report: Upload Data Penerimaan ZIS Rutin

**Fitur:** Upload Data Penerimaan ZIS Rutin (HC Batch)
**Portal:** zakat
**Tanggal:** 2026-06-15
**Validator:** nuwis-validator

---

## Status: PARTIAL

Implementasi inti sudah ada dan fungsional. Terdapat 2 bug kritis (data corruption risk),
4 gap medium, dan 3 gap low yang harus ditangani sebelum go-live.

---

## Discriminator Check

| Discriminator | Expected | Ditemukan di | Status |
|---|---|---|---|
| `transaction.transactioncode` | `'SD002'` | `hc_zis_commit.py` line 188 | PASS |
| `transaction.channelcode` | `'A'` | `hc_zis_commit.py` line 188 | PASS |
| `transaction.transactionnumber` prefix | `'BPZIS'` | `hc_zis_commit.py` line 176 `f'BPZIS-{year}-{seq:07d}'` | PASS |
| `transactionitem.accounttitype` | `'D'` (product) | `hc_zis_commit.py` line 228 | PASS |
| `transactionitem.accounttitype` | `'C'` (bank) | `hc_zis_commit.py` line 258-259 — `'A'` bukan `'C'` | FAIL |
| `individualdonor.isinternalemployee` | `'T'` | `hc_zis_commit.py` line 78 | PASS |
| `donor.donorgroup` | `'R'` | `hc_zis_commit.py` line 71 | PASS |
| `donor.donortype` | `'I'` | `hc_zis_commit.py` line 70 — kolom `donortype` HILANG dari INSERT | FAIL |
| `donor.donorno` prefix | `'P'` | `hc_zis_commit.py` line 65 `f'P{donor_no}'` | PASS |
| `fundentity` Zakat=1 | `1` | `_HC_ZIS_FUNDS` `fund_entity: 1` | PASS |
| `fundentity` Infaq/AnakAsuh/AnakYatim/Qurban=2 | `2` | `_HC_ZIS_FUNDS` `fund_entity: 2` | PASS |
| `fundentity` Wakaf=3 SKIP | skip | `amountwakaf` tidak ada di `_HC_ZIS_FUNDS` | PASS |
| `ParameterGlobal.BANKZAKAT` | `'BANKZAKAT'` | `_load_bank_params` keys list | PASS |
| `ParameterGlobal.BANKINFAQ` | `'BANKINFAQ'` | `_load_bank_params` keys list | PASS |
| `ParameterGlobal.BANKASUH` | `'BANKASUH'` | `_load_bank_params` keys list | PASS |
| `ParameterGlobal.BANKYATIM` | `'BANKYATIM'` | `_load_bank_params` keys list | PASS |
| `ParameterGlobal.BANKQURBAN` | `'BANKQURBAN'` | `_load_bank_params` keys list | PASS |
| `transactionbatch.batchtag` | `'OPR'` | Tidak digunakan — transaksi langsung tanpa daily batch | SKIP (acceptable) |

---

## Bug Kritis

### BUG-1: `accounttitype` bank item salah — `'A'` seharusnya `'C'`

**File:** `apps_zakat/api-python/app/modules/transaksi/hc_zis_commit.py` line 258–259

```python
# Implementasi saat ini (SALAH):
await conn.execute(
    """INSERT INTO transaction.accounttransactionitem
       (transactionitemid, accounttitype, accountno, isupdatebalance)
       VALUES ($1, 'A', $2, 'T')""",
    bank_item_id, cash_accountno,
)
```

Legacy mendefinisikan dua jenis:
- `'D'` = sisi product/donor (donor credit item) — sudah benar di line 228
- `'C'` = sisi bank/kas (counter account) — di ISF ditulis `'A'`

Nilai `'A'` bukan nilai valid menurut discriminator MIGRATION_ANALYSIS. Ini akan menyebabkan
laporan dan filter berdasarkan `accounttitype` tidak menemukan sisi bank, atau memasukkan
transaksi ini ke bucket yang salah dalam laporan keuangan.

**Severity: CRITICAL** — data corruption pada accounttransactionitem, berdampak ke laporan.

---

### BUG-2: `donor.donortype = 'I'` tidak di-INSERT saat buat donor baru

**File:** `apps_zakat/api-python/app/modules/transaksi/hc_zis_commit.py` line 68–72

```python
# Implementasi saat ini (TIDAK LENGKAP):
await conn.execute(
    """INSERT INTO fund.donor
       (donorid, donorno, donorname, donorgroup, status, branchcode, created_at)
       VALUES ($1, $2, $3, 'R', 'A', $4, NOW())""",
    donor_id, donor_no_str, name, branch_code,
)
```

Kolom `donortype` tidak disertakan. Legacy selalu set `DonorType='I'` (Individual) untuk
karyawan. Tanpa ini donor baru tidak akan dikenali sebagai Individual oleh sistem laporan
dan lookup yang filter `donortype='I'`.

**Severity: CRITICAL** — donor baru tidak punya tipe, berdampak ke filter laporan penghimpunan.

---

### BUG-3: `HCZisParseResult` tidak mengembalikan `tanggal_transaksi` dan `namafile`

**File:** `apps_zakat/api-python/app/modules/transaksi/hc_zis_schema.py` line 51–56

`HCZisParseResult` hanya punya: `batch_period_desc`, `totals`, `items`, `is_duplicate`.
Tidak ada `tanggal_transaksi` dan `namafile`.

**File:** `apps_zakat/web-vue/src/pages/keuangan/UploadHCZisPage.vue` line 118–119

Vue page membaca `parseResult.value.tanggal_transaksi` dan `parseResult.value.namafile`
untuk menyusun submit payload, tapi nilai ini tidak ada di response parse API.

Akibatnya: `tanggal_transaksi` dan `namafile` akan selalu `undefined` saat submit,
sehingga batch tersimpan tanpa tanggal transaksi dan nama file yang benar.

**Severity: CRITICAL** — tanggal transaksi tidak tersimpan, seluruh workflow rusak.

---

## Gap Medium

### GAP-M1: `namafile` kolom tidak ada di tabel `humancapitalbatch`

**File:** `infra/db/migrations/transaction/012_create_humancapital_tables.sql`

Kolom `namafile` tidak didefinisikan di migration SQL, tapi:
- `hc_zis_service.py` queries `h.namafile`
- `hc_zis_commit.py` INSERT menyertakan `namafile`
- `HCZisBatchSummary` dan `HCZisBatchDetail` schema punya field `namafile`

Migration perlu ditambah kolom `namafile VARCHAR(200)` di tabel `humancapitalbatch`.
Saat ini service akan error runtime `column "namafile" does not exist`.

**Severity: MEDIUM** — service akan crash saat query list/detail batch.

---

### GAP-M2: `DonorCommitment` upsert tidak diimplementasi

Legacy `authorize()` Step 7 menjalankan `UpdateDonorCommitment()`:
per account parameter (BANKZAKAT/BANKINFAQ/dll), per baris karyawan,
INSERT/UPDATE `fund.donorcommitment` dan INSERT `fund.donorcommitmenthistory`.

Tidak ada referensi ke `fund.donorcommitment` atau `fund.donorcommitmenthistory`
di seluruh `hc_zis_commit.py`. Ini adalah mekanisme tracking komitmen rutin donatur
yang penting untuk laporan donasi rutin.

**Severity: MEDIUM** — data komitmen rutin tidak terupdate, laporan komitmen tidak akurat.

---

### GAP-M3: `transhistoryofchanges` audit trail tidak diimplementasi

Legacy `authorize()`, `delete()`, dan `update_date()` semua INSERT ke
`transaction.transhistoryofchanges` dengan `changetype='N'`/`'E'`/`'D'`.

Tidak ada INSERT ke `transhistoryofchanges` di `hc_zis_commit.py`.

**Severity: MEDIUM** — tidak ada audit trail untuk Create/Edit/Delete batch ZIS rutin.

---

### GAP-M4: XLS parser stop condition berbeda dari spec

**File:** `apps_zakat/api-python/app/modules/transaksi/hc_zis_parse.py` line 68–70

MIGRATION_ANALYSIS spec: "iterasi sampai **kolom 1** kosong" (kolom A = nomor urut baris).

Implementasi berhenti ketika **kolom 6** (EmployeeNumber/NIP) kosong:
```python
employee_number_cell = ws.cell(row_num, 6).value
if not employee_number_cell:
    break
```

Ini berarti baris yang punya nomor urut (kolom A) tapi NIP kosong akan menghentikan
parsing sebelum waktunya, sementara baris dengan NIP tapi tanpa nomor di kolom A
tidak akan berhenti. Bergantung pada format file aktual, ini bisa menyebabkan
row yang valid ter-skip atau baris kosong di-parse.

**Severity: MEDIUM** — parsing bisa gagal/terpotong untuk file non-standar.

---

## Gap Low

### GAP-L1: `humancapitalpassedreport` INSERT tidak diimplementasi di `create_from_payload`

Legacy Step 9: setelah semua transaksi dibuat, INSERT ke `humancapitalpassedreport`
untuk karyawan internal yang **tidak ada** di batch (absen dari file).

`create_from_payload` di `hc_zis_commit.py` tidak melakukan query
"karyawan internal yang tidak ada di batch ini" dan tidak INSERT ke `humancapitalpassedreport`.
Tabel ini di-CREATE di migration, di-DELETE saat delete, tapi tidak pernah di-INSERT.

**Severity: LOW** — fungsionalitas laporan donatur absen tidak berjalan.

---

### GAP-L2: `donorfieldhistory` sync tidak diimplementasi

Legacy Step 5 (`UpdateDonorData`): untuk donor yang sudah ada, jika field berubah
(MARITALSTATE, WORKPOSITION, MOBILEPHONE, DONORNAME, dll), INSERT ke
`fund.donorfieldhistory` lalu UPDATE `fund.individualdonor`/`fund.donor`.

`hc_zis_commit.py` tidak melakukan sync data karyawan existing, hanya buat donor baru.
Perubahan data karyawan dari file baru tidak akan memperbarui data donor yang sudah ada.

**Severity: LOW** — data karyawan lama tidak ter-update dari file baru.

---

### GAP-L3: Menu key namespace berbeda dari MIGRATION_ANALYSIS

MIGRATION_ANALYSIS menyebut `transaksi.upload.zis-rutin` sebagai menu key kandidat.
Semua implementasi aktual menggunakan `keuangan.upload.zis-rutin` (BFF, seed, registry.ts, router).

Ini adalah perbedaan yang **disengaja dan konsisten** di semua layer — bukan bug.
Dicatat di sini untuk dokumentasi saja.

**Severity: LOW** — bukan issue, hanya perlu dicatat sebagai intentional deviation.

---

## Implementasi yang Sudah Benar (Parity Confirmed)

- Parse XLS/XLSX dengan openpyxl + xlrd (dual format support)
- Cell B2 sebagai `batch_period_desc` (row=2, col=2 di openpyxl 1-indexed = B2)
- Data rows mulai row 8
- Amount dikali -1 (nilai negatif di file)
- Semua mapping kolom XLS (3,4,6,8,10-23) sesuai spec
- Gender normalization: `MALE`→`L`, `FEMALE`→`P` (bug-safe logic)
- Marital status normalization: `MARRD.`→`K`, `SINGLE`→`B`, `DIVC./WIDOW/WDOWER`→`S`
- Duplikat check via `batchperioddesc` UNIQUE constraint + runtime query
- Otorisasi entity types terdaftar: `hc_zis_upload`/`hc_zis_delete`/`hc_zis_update_date`
- Save-and-submit pattern (langsung PENDING, bukan DRAFT)
- Fund entity mapping: Zakat=1, Infaq/AnakAsuh/AnakYatim/Qurban=2, Wakaf SKIP
- Bank parameters BANKZAKAT/BANKINFAQ/BANKASUH/BANKYATIM/BANKQURBAN dimuat dari DB
- Donor auto-create: `donorgroup='R'`, `isinternalemployee='T'`, `donorno='P'+7digit`
- `transactioncode='SD002'` hardcoded di INSERT
- `transactionnumber` format `BPZIS-{year}-{seq:07d}`
- Journal: header + items + block semua ter-INSERT
- `fl_accountingperiode` (MONTH) dan `fl_accountingyear` (YEAR) diupdate saat update tanggal
- Delete flow: reverse balance `financialaccount` + `donortotalfund`, cascade delete dalam urutan benar
- Transaction wrap (`async with conn.transaction()`) per item
- Parse Preview UI: BatchPeriodDesc, totals per jenis dana, items grid (UploadHCZisPage.vue)
- List UI: paginator di atas, filter periode + date range (UploadHCZisListPage.vue)
- Detail modal dengan items table
- Update tanggal modal dengan form read-only sebelum edit
- Delete modal menampilkan data batch lengkap sebelum konfirmasi
- 3-way consistency: registry.ts / router meta.menu_key / seed SQL semuanya `keuangan.upload.zis-rutin`
- SPVKEU diberi akses ke list menu (monitoring)
- DB migration: semua 3 tabel (humancapitalbatch, humancapitalbatchitem, humancapitalpassedreport) ada

---

## Role Coverage

| Legacy Role | ISF Role Code | Di seed SQL | Di role_menu | Status |
|---|---|---|---|---|
| ACC (upload) | ACC | `seed-menu-upload-hc-zis.sql` line 39-41 | keuangan.upload.zis-rutin | PASS |
| ACC (list) | ACC | `seed-menu-upload-hc-zis.sql` line 39-41 | keuangan.upload.zis-rutin-list | PASS |
| SPVKEU (monitoring) | SPVKEU | `seed-menu-upload-hc-zis.sql` line 46-48 | keuangan.upload.zis-rutin-list | PASS (bonus) |

MIGRATION_ANALYSIS menyebut hanya role ACC. Penambahan SPVKEU untuk list adalah value-add
yang logis (supervisor perlu monitoring) dan tidak merugikan.

---

## 3-Way Consistency Check

| Layer | Key | Status |
|---|---|---|
| `lib/menu/registry.ts` line 40-41 | `keuangan.upload.zis-rutin`, `keuangan.upload.zis-rutin-list` | PASS |
| `router/index.ts` line 318, 324 | `meta.menu_key: 'keuangan.upload.zis-rutin'` | PASS |
| `seed-menu-upload-hc-zis.sql` | `keuangan.upload.zis-rutin` | PASS |
| DB runtime | Tidak bisa diverifikasi (DB unavailable) | UNKNOWN |

---

## Ringkasan Gap

| # | Severity | Gap | File | Fix |
|---|---|---|---|---|
| BUG-1 | CRITICAL | `accounttitype` bank item `'A'` seharusnya `'C'` | `hc_zis_commit.py` line 259 | Ganti `'A'` dengan `'C'` |
| BUG-2 | CRITICAL | `donortype='I'` tidak di-INSERT donor baru | `hc_zis_commit.py` line 70 | Tambah `donortype` ke INSERT kolom + nilai `'I'` |
| BUG-3 | CRITICAL | Parse response tidak return `tanggal_transaksi` dan `namafile` | `hc_zis_schema.py:HCZisParseResult` + `hc_zis_parse.py` | Tambah kedua field ke `HCZisParseResult`, isi dari parameter di router |
| GAP-M1 | MEDIUM | Kolom `namafile` tidak ada di migration SQL | `012_create_humancapital_tables.sql` | Tambah `namafile VARCHAR(200)` ke tabel `humancapitalbatch` via migration baru |
| GAP-M2 | MEDIUM | DonorCommitment upsert tidak diimplementasi | `hc_zis_commit.py` | Tambah step `UpdateDonorCommitment` per bank param per item |
| GAP-M3 | MEDIUM | `transhistoryofchanges` audit trail tidak diimplementasi | `hc_zis_commit.py` | Tambah INSERT di create/delete/update_date dispatcher |
| GAP-M4 | MEDIUM | XLS stop condition: col 6 (NIP) vs spec col 1 (nomor) | `hc_zis_parse.py` line 68 | Evaluasi format file aktual; kemungkinkan ganti ke col A |
| GAP-L1 | LOW | `humancapitalpassedreport` tidak di-INSERT | `hc_zis_commit.py` | Tambah query donatur absen + INSERT setelah loop transaksi |
| GAP-L2 | LOW | Sync `donorfieldhistory` untuk donor existing tidak ada | `hc_zis_commit.py` | Tambah `UpdateDonorData` step sebelum create transaksi |
| GAP-L3 | LOW | Menu key namespace berbeda dari MIGRATION_ANALYSIS | (semua file) | Intentional — tidak perlu difix |

**CRITICAL: 3 items (BUG-1, BUG-2, BUG-3) — harus fix sebelum deploy**
**MEDIUM: 4 items — harus fix sebelum release**
**LOW: 3 items — bisa fix iterasi berikut**

---

## Field Coverage

### Batch Header Fields

| Field Legacy | Schema ISF | DB Kolom | Status |
|---|---|---|---|
| NamaFile | `HCZisSubmitRequest.namafile` | `namafile` (HILANG dari migration) | PARTIAL |
| TanggalTransaksi | `HCZisSubmitRequest.tanggal_transaksi` | `transactiondate` | PASS |
| IsSendSMS | (tidak ada) | (tidak ada) | ACCEPTABLE — dinonaktifkan di legacy |
| BatchPeriodDesc | `batch_period_desc` | `batchperioddesc` UNIQUE | PASS |
| ZakatTotal..GrandTotal | `HCZisTotals.*` | `totalzakat`..`grandtotal` | PASS |
| ZakatTotalRecord..GrandTotalRecord | `HCZisTotals.*_count` | `totalrecord` (agregat) | PARTIAL — per-jenis count ada di schema, DB hanya grand count |

### Item Fields

| Field Legacy | Schema ISF | DB Kolom | Status |
|---|---|---|---|
| DataNo | `data_no` | `datano` | PASS |
| EmployeeNumber | `employee_number` | `employeenumber` | PASS |
| EmployeeName | `employee_name` | `name` | PASS |
| BusinessAreaCode | `business_area_code` | `businessareacode` | PASS |
| BusinessAreaDesc | `business_area_desc` | `businessareadescription` | PASS |
| BirthPlace | `birth_place` | `birthplace` | PASS |
| WorkAreaName | `work_area_name` | `workareaname` | PASS |
| MobilePhone | `mobile_phone` | `mobilephone` | PASS |
| BirthDate | `birth_date` | `birthdate` | PASS |
| Gender | `gender` | `gender` | PASS |
| MaritalStatus | `marital_status` | `maritalstatus` | PASS |
| Position | `position` | `position` | PASS |
| OrganizationUnit | `organization_unit` | `organizationalunit` | PASS |
| ZakatAmount..TaqurmaAmount | `zakat_amount`..`taqurma_amount` | `amountzakat`..`amountqurban` | PASS |
| WakafAmount | `wakaf_amount` | `amountwakaf` | PASS (stored, not processed) |
| TotalAmount | `total_amount` | `totalamount` | PASS |
| Description | `description` (schema only) | `description` | PARTIAL — di schema tidak, di DB ada |
| ValidationDesc | (tidak ada) | `validationdesc` | LOW — optional field |

**Field coverage: 19/21 fields fully covered, 2 partial, 0 missing critical fields**

---

## E2E Test

Script tersedia:

```bash
bash /home/wishnew/workshop/isf-app/testing/e2e-upload-zis-rutin.sh
```

Catatan: BUG-3 (tanggal_transaksi missing dari parse response) akan menyebabkan
E2E submit step gagal karena payload yang dikirim ke `/submit` tidak punya `tanggal_transaksi`.

---

## Rekomendasi Tindakan

### Sebelum Deploy (CRITICAL)

1. **Fix BUG-1** (`hc_zis_commit.py` line 259): ganti `'A'` menjadi `'C'` di INSERT `accounttransactionitem` untuk bank item.

2. **Fix BUG-2** (`hc_zis_commit.py` line 70): tambah `donortype` ke kolom INSERT fund.donor:
   ```python
   """INSERT INTO fund.donor
      (donorid, donorno, donorname, donorgroup, donortype, status, branchcode, created_at)
      VALUES ($1, $2, $3, 'R', 'I', 'A', $4, NOW())"""
   ```

3. **Fix BUG-3**: Tambah `tanggal_transaksi: str` dan `namafile: str` ke `HCZisParseResult`.
   Di router `parse_upload`, isi kedua field dari query param `tanggal_transaksi`
   dan `file.filename` sebelum return response.

### Sebelum Release (MEDIUM)

4. **Fix GAP-M1**: Buat migration baru `V013__add_namafile_to_humancapitalbatch.sql`:
   ```sql
   ALTER TABLE transaction.humancapitalbatch ADD COLUMN namafile VARCHAR(200);
   ```

5. **Fix GAP-M2**: Implementasi `UpdateDonorCommitment` di `hc_zis_commit.py` setelah
   loop item — per bank param, per donor, upsert `fund.donorcommitment` + INSERT history.

6. **Fix GAP-M3**: Tambah INSERT `transaction.transhistoryofchanges` di akhir masing-masing
   dispatcher (`create_from_payload`, `delete_from_payload`, `update_date_from_payload`).

7. **Evaluasi GAP-M4**: Konfirmasi dengan sample file XLS aktual — apakah kolom A
   (col 1) selalu berisi nomor urut. Jika ya, ubah stop condition ke `ws.cell(row_num, 1).value`.

### Iterasi Berikutnya (LOW)

8. Implementasi `humancapitalpassedreport` INSERT (GAP-L1).
9. Implementasi sync `donorfieldhistory` untuk donor existing (GAP-L2).

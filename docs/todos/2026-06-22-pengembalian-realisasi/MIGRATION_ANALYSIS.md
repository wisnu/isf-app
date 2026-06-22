==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/program/
PORTAL:  zakat
SCOPE:   Pengembalian Realisasi Program (QRealizationReturn / fRealizationReturn)
TANGGAL: 2026-06-22

---

## MODULE OVERVIEW

Pengembalian Realisasi Program adalah fitur pencatatan sisa dana yang dikembalikan dari kegiatan penyaluran (realisasi) yang sudah terjadi. Alur bisnis:

1. Operator (DIST) mencari data Realisasi yang sudah diinput sebelumnya melalui popup `fSelectRealization`.
2. Sistem otomatis mengisi detail pengembalian (per `RealizationDetail` — per mustahiq per sumber dana).
3. Operator mengisi `ReturnAmount` per baris detail dan opsional menambah baris Rincian Biaya (potongan administrasi, biaya lain) via tab terpisah.
4. Validasi: total pengembalian + total biaya harus sama dengan total pencairan realisasi.
5. Data masuk ke antrian otorisasi (DIST050/DIST051/DIST052) — supervisor (SPVDIST) menyetujui.
6. Saat otorisasi, sistem membuat `RealizationReturn`, `RealizationReturnDetail`, `RealizationReturnCost`, lalu memanggil `RR.CreateTransaction()` yang menghasilkan transaksi jurnal dengan TransactionCode `'DD002'` ke modul `transaction`.

---

## FITUR LIST

1. **List Pengembalian Realisasi Program** (QRealizationReturn)
   - ROLES: DIST, SPVDIST
   - DIALOG: `dialogs/Kegiatan/QRealizationReturn.*`
   - MENU_KEY_KANDIDAT: `distribution.realization-return.list`
   - Sumber: `docs/legacy-apps/program/menus/Penyaluran.mnu` baris 113–116

2. **Tambah Pengembalian Realisasi Program** (fRealizationReturn mode=New)
   - ROLES: DIST
   - DIALOG: `dialogs/Kegiatan/fRealizationReturn.*`
   - MENU_KEY_KANDIDAT: `distribution.realization-return.create`
   - Sumber: `menus/popupmenus/Kegiatan/mnuRealizationReturn.mnu` baris 11–14

3. **Ubah Pengembalian Realisasi Program** (fRealizationReturn mode=Edit)
   - ROLES: DIST
   - MENU_KEY_KANDIDAT: `distribution.realization-return.update`
   - Sumber: `mnuRealizationReturn.mnu` baris 15–18

4. **Tampilkan Pengembalian Realisasi Program** (fRealizationReturn mode=View)
   - ROLES: DIST, SPVDIST
   - MENU_KEY_KANDIDAT: tidak perlu key terpisah (sub-action dari list)
   - Sumber: `mnuRealizationReturn.mnu` baris 19–22

5. **Hapus Pengembalian Realisasi Program** (fRealizationReturn mode=Delete)
   - ROLES: DIST
   - MENU_KEY_KANDIDAT: `distribution.realization-return.delete`
   - Sumber: `mnuRealizationReturn.mnu` baris 23–26

6. **Laporan Pengembalian Realisasi** (fReportRealizationReturn)
   - ROLES: DIST, SPVDIST, QAC (**AMBIGU** — `QAC` tidak ada di mapping role legacy→isf-app, laporkan ke nuwis-architect)
   - DIALOG: `dialogs/Laporan/fReportRealizationReturn.*`
   - MENU_KEY_KANDIDAT: `distribution.reports.realization-return`
   - Sumber: `Penyaluran.mnu` baris 162–166

---

## FORM FIELDS (per dialog)

### DIALOG: `dialogs/Kegiatan/QRealizationReturn` (List/Filter)

Sumber: `QRealizationReturn.dfr` + `QRealizationReturn_intr.py` + `QRealizationReturn_data.py`

FILTER FIELDS (uipFilter):
```
- BeginDate   : timestamp  [Required] — Periode Tanggal (dari)
- EndDate     : timestamp  [Required] — s/d (sampai dengan)
- Incolumn    : integer    [Optional, Hidden] — kolom filter enum: 0=Seluruh, 1=Nama Mustahik, 2=Alamat
- Description : varchar(30)[Optional, Hidden] — Deskripsi
```

COLUMNS DITAMPILKAN:
```
- RealizationReturn.ReturnDate         — Tanggal Realisasi
- RealizationReturn.ReturnDescription  — Deskripsi
- RealizationReturn.RealMemoNumber     — Nomor Memo (via LRealization.LRealizationMemo)
- RealizationReturn.RealizationAmount  — Nilai Realisasi (via LRealization)
- RealizationReturn.ReturnAmount       — Nilai Pengembalian
```

OQL Query (dari `QRealizationReturn_intr.py:DisplayList()` baris 31–41):
```
Select from RealizationReturn
 [ ReturnDate >= :BeginDate and ReturnDate < :EndDate ]
 ( ReturnDate, ReturnDescription, LRealization.LRealizationMemo.RealMemoNumber,
   LRealization.RealizationAmount, ReturnAmount, self )
 then order by ReturnDate;
```

---

### DIALOG: `dialogs/Kegiatan/fRealizationReturn` (Add/Edit/View/Delete)

Sumber: `fRealizationReturn.dfr` + `fRealizationReturn.svr`

**Panel pData — Header Form (uipR → RealizationReturn):**
```
- ReturnDate            : timestamp  [Required]      — Tgl Transaksi Pengembalian     (editable)
- ReturnDescription     : varchar    [Required]      — Keterangan Pengembalian         (editable)
- RealizationDate       : timestamp  [ReadOnly, virtual] — Tanggal Realisasi           (auto-fill dari realisasi dipilih)
- RealizationDescription: varchar    [ReadOnly, virtual] — Keterangan Realisasi        (auto-fill)
- RealizationMemoNumber : varchar    [ReadOnly, virtual] — Nomor Memo                  (auto-fill)
- TotalDropping         : double     [Hidden, ReadOnly]  — Total Pengajuan             (tidak aktif)
- RealizationId         : integer    [Hidden]            — FK ke Realization            (auto-fill)
```

**Panel pDetail — Summary Total (uipR, ReadOnly):**
```
- TotalRealization : double [ReadOnly] — Total Pencairan Realisasi (kalkulasi dari grid detail)
- TotalReturn      : double [ReadOnly] — Total Pengembalian        (kalkulasi dari uipGD.ReturnAmount)
- TotalCost        : double [ReadOnly] — Total Rincian Biaya       (kalkulasi dari uipLsCost)
```

**Custom fields hidden (uipR, tidak di DB RealizationReturn):**
```
- Mode          : varchar(10)  [Hidden] — mode operasi form (New/Edit/Delete/View)
- UserInput     : varchar(50)  [Hidden] — dari config.SecurityContext.UserId (auto-fill)
- DateInput     : timestamp    [Hidden] — dari config.Now() (auto-fill)
```

**Grid Tab "Detail Realisasi" (uipGD → RealizationReturnDetail, ListName=LsReturnDetail):**
```
- LMustahiqProduct.MustahiqProductName : varchar [ReadOnly] — Nama Program
- LMustahiqProduct.MustahiqProductId   : integer [Hidden]   — ID Program
- RealizationAmount    : decimal [ReadOnly] — Nominal Realisasi (dari data realisasi asli)
- LCashAccount.AccountNo    : varchar [ReadOnly] — Sumber Dana (nomor rekening)
- LCashAccount.AccountName  : varchar [ReadOnly] — Sumber Dana (nama rekening)
- ReturnAmount    : decimal [Required] — Nominal Pengembalian (editable, ≥0 dan ≤RealizationAmount)
- DetailDescription: varchar [Hidden]  — Keterangan detail
- NamaMustahiq    : varchar [ReadOnly, virtual] — Nama Mustahiq (dari customer via mustahiq)
- DataId          : integer [Hidden]   — urutan lokal untuk kalkulasi total
```

**Grid Tab "Rincian Biaya" (uipLsCost → RealizationReturnCost, ListName=LsCostDetail):**
```
- LCostItem.CostItemCode       : varchar [Lookup] — Kode Rincian Biaya
- LCostItem.CostItemDescription: varchar [ReadOnly] — Deskripsi Rincian Biaya
- CostAmount      : decimal [Required] — Nominal Biaya (≥0)
- AdditionalDescription: varchar [Hidden] — Deskripsi tambahan
- DataId          : integer [Hidden]   — urutan lokal
```

SECTIONS (dari `.dfr`):
- `pData` — data header pengembalian
- `pDetail` — ringkasan total (TotalRealization, TotalReturn, TotalCost)
- `multipages1` — tabs: "Detail Realisasi" (`gridDetail`), "Rincian Biaya" (`gridDetailCost`)
- `pAction` — tombol Simpan / Batal

READ_ONLY (auto-fill, tidak boleh diubah user):
- `RealizationDate`, `RealizationDescription`, `RealizationMemoNumber` — dari realisasi yang dipilih
- `TotalRealization`, `TotalCost` — calculated
- `NamaMustahiq`, `LMustahiqProduct.MustahiqProductName`, `LCashAccount.*` — dari data realisasi asli

HIDDEN (tersimpan di payload otorisasi tapi tidak ditampilkan):
- `RealizationId`, `Mode`, `UserInput`, `DateInput`, `TotalDropping`
- `MustahiqProductId`, `DetailDescription`, `DataId` (di grid)

---

## UI FLOW

**ON OPEN (List QRealizationReturn):**
- `FormSetDataEx` mengisi `uipFilter.BeginDate = Now` dan `uipFilter.EndDate = Now`
- Sumber: `QRealizationReturn_data.py:FormSetDataEx()` baris 6–11

**ON OPEN (Form fRealizationReturn mode=New):**
- `FormSetDataEx` membuat record baru dengan `ReturnDate = Now`, `DateInput = Now`, `UserInput = config.SecurityContext.UserId`
- Sumber: `fRealizationReturn_data.py:FormSetDataEx()` baris 20–27

**ON OPEN (Form fRealizationReturn mode=Edit/View/Delete):**
- `FormSetDataEx` memuat data `RealizationReturn` berdasarkan `key` (ReturnId)
- Mengisi virtual fields: `RealizationId`, `RealizationDate`, `RealizationDescription`, `RealizationMemoNumber`
- Sumber: `fRealizationReturn_data.py:FormSetDataEx()` baris 43–56

**PILIH REALISASI (bSearchRealizationOnClick):**
- Membuka popup `fSelectRealization`
- Setelah dipilih, memanggil `ShowListRealizationDetail(RealizationId)` → `SetReturnDetailByRealization()` di `_data.py`
- Query langsung ke DB: join `RealizationDetail`, `Mustahiq`, `Customer`, `MustahiqProduct`, `CashAccount`, `Proposal`
- Mengisi grid `uipGD` dengan baris per mustahiq, `ReturnAmount = 0.0` (user harus mengisi)
- Sumber: `fRealizationReturn_intr.py:bSearchRealizationOnClick()` baris 147–159; `fRealizationReturn_data.py:SetReturnDetailByRealization()` baris 59–123

**ON SAVE (bSaveOnClick):**
1. `CommitBuffer()` untuk flush pending edits
2. `CekInput()` — validasi client-side (lihat Business Rules)
3. `CallServerMethod("save", ph)` — memanggil fungsi `save()` di `fRealizationReturn_data.py`
4. `save()` menyiapkan paket otorisasi dan memanggil `app.rexecscript("enterprise", "api/otorisasi.storeDataPacket", ph)` — 1 ExecuteScript call = 1 endpoint API
5. Setelah berhasil: "Data Berhasil Diproses. Silahkan diotorisasi"
- Sumber: `fRealizationReturn_intr.py:bSaveOnClick()` baris 185–200; `fRealizationReturn_data.py:save()` baris 199–242

---

## SAVE LOGIC

### Jalur Otorisasi — `save()` di `fRealizationReturn_data.py:save()` baris 199–242

**ENTRY:** `fRealizationReturn_data.py` → fungsi `save(config, params, returns)`

**ALUR (pre-otorisasi):**
1. `BeginTransaction()`
2. Baca `params.uipR.GetRecord(0)` — data header pengembalian
3. `otorisasi.prepareParameterOtorisasi(params)` — siapkan record otorisasi
4. Set kode_entri berdasarkan mode:
   - New → `kode_entri = 'DIST050'`, `keterangan = 'Tambah Data Pengembalian Realisasi'`
   - Edit → `kode_entri = 'DIST051'`, `keterangan = 'Ubah Data Pengembalian Realisasi'`
   - Delete → `kode_entri = 'DIST052'`, `keterangan = 'Hapus Data Pengembalian Realisasi'`
5. Set `id_peran = 'SPVDIST'` — supervisor yang akan mengotorisasi
6. Set `nama_tabel = 'RealizationReturn'`, `tipe_target = 0`, `tipe_key = 1`
7. Kirim via `app.rexecscript("enterprise", "api/otorisasi.storeDataPacket", ph)` — menyimpan payload ke tabel otorisasi enterprise
8. `Commit()` atau `Rollback()`

### Jalur Otorisasi — `authorize()` di `fRealizationReturn_data.py:authorize()` baris 128–195

**ENTRY:** `fRealizationReturn_data.py` → fungsi `authorize(config, parameter, returnpacket)`
(dipanggil oleh sistem otorisasi enterprise saat SPVDIST menyetujui)

**ALUR (post-otorisasi, mode New atau Edit):**
1. Cek `recParam.Mode in ['New','Edit']`
2. Jika `New`: `RR = helper.CreatePObject('RealizationReturn')` → class di `script_modules/Realisasi.py`
3. Jika `Edit`: `RR = helper.GetObject('RealizationReturn', recParam.ReturnId)` → hapus semua detail dan cost dulu: `RR.LsReturnDetail.DeleteAllPObjs()`, `RR.LsCostDetail.DeleteAllPObjs()`
4. `config.FlushUpdates()`
5. Set field header: `RealizationId`, `ReturnDate`, `ReturnAmount` (= `TotalReturn`), `CostAmount` (= `TotalCost`), `ReturnDescription`, `InputUser`, `InputDate`, `AuthDate`, `AuthUser`
6. `RR.BranchCode = config.SecurityContext.GetUserInfo()[4]` — branch dari session
7. Loop `parameter.uipGD` → untuk setiap baris detail:
   - `oDetail = helper.CreatePObject('RealizationReturnDetail')`
   - Set: `ReturnId`, `RealizationAmount`, `ReturnAmount`, `DetailDescription`, `RealizationDetailId`, `MustahiqProductId`, `AccountNo`
8. Loop `parameter.uipLsCost` → untuk setiap baris rincian biaya:
   - `oCostDetail = helper.CreatePObject('RealizationReturnCost')`
   - Set: `RealizationId`, `ReturnId`, `CostItemId`, `CostAmount`
9. `config.FlushUpdates()` — INSERT ke DB
10. `RR.CreateTransaction()` → membuat transaksi jurnal dengan `TransactionCode = 'DD002'`

**ALUR CreateTransaction() (`Realisasi.py:RealizationReturn.CreateTransaction()` baris 310–406):**
1. Query `program.transaction WHERE ReturnId = ?` — hapus/update item lama
2. OQL query ke `RealizationReturnDetail`: mengambil `AccountNo`, `Ashnaf`, `FundProductId`, `TransactionProductId`, `ProductId`, `ReturnAmount`, per baris
3. Per `AccountNo` unik → buat `RealizationReturnTransaction` (TransactionCode=`'DD002'`, BranchCode, TransactionDate, Description, ReferenceNo dari memo, ChannelAccountNo)
4. Per baris detail → buat `RealizationTransactionItem` (Ashnaf, FundProductId, BudgetId, TransactionProductId, Amount=ReturnAmount)
5. `config.FlushUpdates()` → INSERT ke `program.transaction` + item
6. `oTransaction.SendTransaction()` → kirim ke modul `transaction` via `app.rexecscript('transaction', 'AppInterface/ExternalTransaction.CreateTransaction', ph)` — membuat jurnal akuntansi di core

**ALUR (mode Delete):**
1. `RR = helper.GetObject('RealizationReturn', recParam.ReturnId)`
2. `RR.DeleteTransaction()`:
   - Query `program.transaction WHERE ReturnId = ?`
   - Untuk tiap transaksi: `oTransaction.Ls_TransactionItem.DeleteAllPObjs()` + `oTransaction.DeleteCoreTransaction()` → rexecscript ke `transaction.AppInterface/ExternalTransaction.DeleteTransaction`
3. `DELETE FROM RealizationReturn WHERE ReturnId = ?`
4. `DELETE FROM RealizationReturnDetail WHERE ReturnId = ?`
5. `DELETE FROM Transaction WHERE ReturnId = ?`
- Sumber: `fRealizationReturn_data.py:authorize()` baris 180–195 + `Realisasi.py:RealizationReturn.DeleteTransaction()` baris 408–434

---

## SCHEMA DB

### ENTITIES

**RealizationReturn** → tabel: `program.realizationreturn`
```
- returnid          : integer         PK (dari seq_realizationreturn)
- returndate        : timestamp
- returndescription : varchar(200)
- returnamount      : numeric(30,8)   — total pengembalian
- costamount        : numeric(30,4)   — total rincian biaya
- realizationid     : integer         FK → program.realization.realizationid
- branchcode        : varchar(5)
- inputuser         : varchar(50)
- inputdate         : timestamp
- authuser          : varchar(50)
- authdate          : timestamp
- transactionid     : integer         FK → program.transaction.transactionid (legacy, tidak aktif)
```
Sumber: `docs/reference/datadictionary/ddl_all_schema.sql` baris 12924–12937

**RealizationReturnDetail** → tabel: `program.realizationreturndetail`
```
- returndetailid       : integer       PK (dari seq_realizationreturndetail)
- returnid             : integer       FK → program.realizationreturn.returnid
- realizationdetailid  : integer       FK → program.realizationdetail.realizationdetailid
- mustahiqproductid    : integer       FK → program.mustahiqproduct.mustahiqproductid
- accountno            : varchar(30)   FK → transaction.cashaccount (sumber dana)
- returnamount         : numeric(30,8)
- realizationamount    : numeric(30,8) — snapshot nominal realisasi asli
- detaildescription    : varchar(200)
- transactionid        : integer       FK → program.transaction
```
Sumber: `ddl_all_schema.sql` baris 12946–12956

**RealizationReturnCost** → tabel: `program.realizationcost` (SHARED dengan RealizationCost biasa)
```
- realizationcostid     : integer       PK
- returnid              : integer       FK → program.realizationreturn.returnid  [KRITIS: NOT NULL = biaya pengembalian]
- realizationid         : integer       FK → program.realization.realizationid
- costitemid            : integer       FK → program.costitem
- costamount            : numeric(30,4)
- additionaldescription : varchar(200)
- realizationcosttype   : varchar(1)    — nilai tidak diset secara eksplisit saat create
```
Sumber: `ddl_all_schema.sql` baris 12820–12828

**RealizationReturnTransaction** → tabel: `program.transaction` (TransactionCode=`'DD002'`)
- Subclass dari `Transaction` di `script_modules/Transaction.py` baris 142–145

**CostItem** → tabel: `program.costitem`
```
- costitemid         : integer       PK
- costitemcode       : varchar(3)
- costitemdescription: varchar(200)
```

### RELASI

```
program.realizationreturn.realizationid    → program.realization.realizationid
program.realizationreturndetail.returnid   → program.realizationreturn.returnid
program.realizationreturndetail.realizationdetailid → program.realizationdetail.realizationdetailid
program.realizationreturndetail.mustahiqproductid   → program.mustahiqproduct.mustahiqproductid
program.realizationreturndetail.accountno           → transaction.cashaccount.accountno
program.realizationcost.returnid           → program.realizationreturn.returnid  (jika returnid NOT NULL)
program.realizationcost.realizationid      → program.realization.realizationid
program.realizationcost.costitemid         → program.costitem.costitemid
```

---

## DISCRIMINATORS

**KRITIS — jangan hilangkan saat implementasi:**

1. **`program.realizationcost.returnid IS NOT NULL`** → ini adalah biaya pengembalian (RealizationReturnCost)
   - `returnid IS NULL` → biaya realisasi biasa (RealizationCost)
   - Kedua jenis disimpan di tabel yang sama `program.realizationcost`
   - Sumber: `ddl_all_schema.sql` baris 12826; `Realisasi.py:RealizationReturnCost` baris 447–450

2. **`program.transaction.transactioncode = 'DD002'`** → jurnal transaksi pengembalian realisasi
   - Dibuat oleh `RealizationReturn.CreateTransaction()` di `Realisasi.py` baris 370
   - Kebalikan dari `'DD001'` yang dipakai realisasi biasa

3. **`program.transaction.transactioncode = 'DD001'`** → jurnal realisasi biasa (konteks pembanding)

4. **`program.realization.realizationtype`**
   - `'R'` = Program Rutin
   - `'N'` = Program Non-Rutin
   - Pengembalian melayani keduanya; filter ini dipakai di popup `fSelectRealization` via parameter `MemoType`

5. **`QAC` role — AMBIGU**
   - Muncul di `Penyaluran.mnu` baris 163 untuk laporan
   - Tidak ada padanan di mapping role Legacy → ISF-App
   - Laporkan ke nuwis-architect sebelum implementasi seed laporan

---

## LINKED MODULES

1. **program.realization** — entitas induk yang dikembalikan
   - Sudah diimplementasi: `apps_zakat/api-python/app/modules/distribution/realization/service.py`
   - Guard sudah ada: baris 504–510 cek `COUNT(realizationreturn)` sebelum allow update realisasi

2. **program.realizationmemo** — nomor memo jadi referensi pengembalian
   - Sudah diimplementasi (modul memo penyaluran)

3. **program.realizationdetail** — detail per mustahiq dari realisasi asli
   - Diakses via join di service realisasi; belum ada endpoint terpisah di isf-app

4. **transaction.cashaccount** — sumber dana (rekening)

5. **program.mustahiqproduct** — produk/program mustahiq

6. **enterprise otorisasi system** — di isf-app: `otorisasi.submission`
   - Entity type baru `realization_return` perlu didaftarkan di dispatcher registry

7. **transaction module ExternalTransaction** — cross-module journal entry
   - `CreateTransaction` / `DeleteTransaction` via `rexecscript('transaction', 'AppInterface/ExternalTransaction.*')`
   - Di isf-app dikerjakan oleh `api-python/app/modules/finance/*` via core transaction logic

---

## ROLES

| Aksi | Legacy AllowedGroups | ISF-App role_code |
|---|---|---|
| Lihat List | DIST;SPVDIST | DIST, SPVDIST |
| Tambah | DIST | DIST |
| Ubah | DIST | DIST |
| Hapus | DIST | DIST |
| Tampilkan (View) | DIST;SPVDIST | DIST, SPVDIST |
| Otorisasi (approve) | SPVDIST | SPVDIST |
| Laporan Pengembalian | DIST;SPVDIST;QAC | DIST, SPVDIST, **QAC=AMBIGU** |

Sumber: `Penyaluran.mnu` baris 113–116; `mnuRealizationReturn.mnu` per-item

---

## BUSINESS RULES

Sumber: `fRealizationReturn_intr.py:CekInput()` baris 204–220 dan event handlers baris 222–237

1. `ReturnDate` tidak boleh kosong — "Tanggal Pengembalan belum diinputkan!!"
2. `ReturnDescription` tidak boleh kosong/spasi — "Keterangan pengembalian belum di input !!"
3. `RealizationId` harus sudah dipilih — "Data Realisasi belum di pilih !!"
4. `ReturnDate >= RealizationDate` — "Tanggal Pengembalian tidak boleh lebih kecil dari Tanggal Realisasi!!"
5. `TotalReturn` tidak boleh nol/kosong — "Jumlah pengembalian belum diinputkan"
6. Jika ada detail grid (RecordCount > 0): `TotalCost + TotalReturn HARUS == TotalRealization` — "Jumlah rincian biaya dan pengembalian belum sesuai dengan jumlah pencairan realisasi"
7. `ReturnAmount` per baris tidak boleh negatif (AfterPost) — "Nilai yang diinputkan tidak boleh negatif"
8. `ReturnAmount` per baris TIDAK BOLEH > `RealizationAmount` baris yang sama (BeforePost) — "Nominal pengembalian tidak boleh lebih besar dari nominal realisasi"
9. `CostAmount` tidak boleh negatif (LsCostAfterPost) — "Nilai yang diinputkan tidak boleh negatif"
10. Baris detail tidak boleh dihapus dari grid (BeforeDelete) — "Data Detail tidak boleh dihapus"
11. Tambah baris baru ke grid detail tidak diizinkan (AfterNewRecord memanggil Delete) — detail hanya diisi dari hasil pilih realisasi
12. Realisasi yang sudah memiliki pengembalian tidak bisa diubah (guard di `realization/service.py` baris 504–510)

---

## KOMPLEKSITAS

LEVEL:    SEDANG-TINGGI

ALASAN:
- 3 tabel utama yang diinput sekaligus (RealizationReturn + RealizationReturnDetail + RealizationReturnCost/realizationcost)
- Cross-module transaction creation via `TransactionCode='DD002'` ke modul `transaction` (jurnal akuntansi)
- Otorisasi 2-tahap (save → otorisasi → authorize() → CreateTransaction)
- Discriminator `returnid IS NULL/NOT NULL` pada tabel `realizationcost` (shared tabel antara RealizationCost dan RealizationReturnCost)
- Popup search (`fSelectRealization`) yang mengisi grid detail secara otomatis dengan SQL 6-tabel join
- Validasi kalkulatif strict: TotalCost + TotalReturn = TotalRealization

WORKFLOW:  Approval (Maker-Checker via sistem otorisasi)

---

## HANDOFF

### nuwis-seed-gen

```
MENU_KEY: distribution.realization-return.list
LABEL:    Pengembalian Realisasi Program
ROLES:    DIST, SPVDIST
ROUTE:    /distribution/realization-return

MENU_KEY: distribution.reports.realization-return
LABEL:    Laporan Pengembalian Realisasi
ROLES:    DIST, SPVDIST  (QAC AMBIGU — pending clarification dari nuwis-architect)
ROUTE:    /distribution/reports/realization-return
```

Sort order: letakkan setelah `distribution.realization.non-regular.list` (sort_order 334), gunakan sort_order 335.

Daftarkan entity_config baru:
```sql
INSERT INTO otorisasi.entity_config (entity_type, description, approver_role)
VALUES ('realization_return', 'Pengembalian Realisasi Program', 'SPVDIST');
```

### nuwis-db-migrator

**DWH_VIEWS baru:**

`dwh.v_realization_return` untuk list page dan laporan:
```sql
SELECT
    rr.returnid,
    rr.returndate,
    rr.returndescription,
    rr.returnamount,
    rr.costamount,
    rr.branchcode,
    rr.inputuser,
    rr.authuser,
    rr.authdate,
    r.realizationamount,
    r.realizationdate,
    r.realizationdescription,
    m.realmemonumber AS memo_number
FROM program.realizationreturn rr
JOIN program.realization r ON r.realizationid = rr.realizationid
JOIN program.realizationmemo m ON m.realmemoid = r.realmemoid
```

**MIGRATIONS baru:**
- Tidak ada tabel baru — semua tabel sudah ada di schema `program`
- Tabel `program.realizationreturn`, `program.realizationreturndetail`, `program.realizationcost` sudah ada
- Kolom `costamount` di `realizationreturn` sudah ada (`ddl_all_schema.sql` baris 12936)
- Kolom `returnid` di `realizationcost` sudah ada (`ddl_all_schema.sql` baris 12827)
- Yang perlu ditambah: row baru di `otorisasi.entity_config` untuk `entity_type = 'realization_return'`

### nuwis-python-builder

```
ENDPOINTS:

GET    /api/distribution/realization-return
       Query params: begin_date, end_date, page, limit
       Logic: SELECT FROM program.realizationreturn JOIN realization JOIN realizationmemo
              Filter: returndate BETWEEN begin_date AND end_date, ORDER BY returndate
       Response: {rows: [...], pagination: {...}}

GET    /api/distribution/realization-return/{return_id}
       Logic: get single realizationreturn + JOIN realizationreturndetail + realizationcost WHERE returnid=?
       Response: header + detail list + cost list

GET    /api/distribution/realization-return/realization/{realization_id}/details
       Logic: SELECT FROM realizationdetail JOIN mustahiqproduct JOIN customer/mustahiq JOIN cashaccount
              (raw query dari fRealizationReturn_data.py:SetReturnDetailByRealization() baris 63–98)
       Purpose: populate grid detail saat memilih realisasi
       Response: {rows: [{realization_detail_id, realization_amount, mustahiq_product_name,
                          mustahiq_product_id, account_no, account_name/bankname, customer_name}]}

POST   /api/distribution/realization-return
       Body: {return_date, return_description, realization_id,
              details: [{realization_detail_id, return_amount, detail_description, mustahiq_product_id, account_no}],
              costs: [{cost_item_id, cost_amount}]}
       Logic: validasi → INSERT ke otorisasi.submission (entity_type='realization_return') via save-and-submit
       Guards: return_date >= realization_date; total_return+total_cost == total_realization; return_amount <= realization_amount per baris

PUT    /api/distribution/realization-return/{return_id}
       Body: sama seperti POST
       Guards: sama + cek record ada + cek belum AUTHORIZED

DELETE /api/distribution/realization-return/{return_id}
       Logic: POST ke otorisasi.submission (mode='Delete', entity_type='realization_return')

GET    /api/distribution/cost-items
       Logic: SELECT FROM program.costitem ORDER BY costitemcode
       Response: {rows: [{cost_item_id, cost_item_code, cost_item_description}]}
```

**DISCRIMINATORS untuk service.py:**
```python
# TransactionCode untuk jurnal pengembalian realisasi
RETURN_TRANSACTION_CODE = 'DD002'

# program.realizationcost: membedakan cost realisasi vs cost pengembalian
# WHERE returnid IS NOT NULL → RealizationReturnCost (biaya pengembalian)
# WHERE returnid IS NULL     → RealizationCost (biaya realisasi biasa)

# Saat delete: urutan harus DELETE realizationreturndetail dulu, baru realizationreturn
# Dan: DELETE FROM realizationcost WHERE returnid = ?
```

**Dispatcher otorisasi yang perlu didaftarkan:**
```python
# Di otorisasi/service.py:_register_defaults():
register_dispatcher('realization_return', realization_return_service.create_from_payload)
```

### nuwis-ui-builder

```
PAGE_TYPE: list + form (terpisah, seperti pola realisasi program)

FIELDS (List):
  Filters: begin_date (DateField), end_date (DateField)
  Columns: return_date, memo_number, return_description, realization_amount, return_amount

FIELDS (Form Add/Edit):
  Header:
    - return_date          : DateField    [Required]
    - return_description   : Input        [Required]
    - realization_id       : hidden (auto dari pilih realisasi)
    - realization_date     : Input readonly (auto-fill)
    - realization_description: Input readonly (auto-fill)
    - memo_number          : Input readonly (auto-fill)
  Tombol: [Pilih Realisasi] → membuka dialog/modal pencarian realisasi

  Summary panel (read-only):
    - total_realization    : number readonly
    - total_return         : number readonly (calculated)
    - total_cost           : number readonly (calculated)

  Tabs:
    Tab "Detail Realisasi" (grid, tidak bisa tambah/hapus baris):
      - mustahiq_product_name : readonly
      - customer_name         : readonly (nama mustahiq)
      - realization_amount    : number readonly
      - account_name          : readonly (sumber dana)
      - return_amount         : number [Required, editable, 0 ≤ x ≤ realization_amount]
      - detail_description    : Input (optional)

    Tab "Rincian Biaya" (grid, bisa tambah/hapus):
      - cost_item_code        : SearchSelect lookup dari /api/distribution/cost-items
      - cost_item_description : readonly
      - cost_amount           : number [Required, ≥0]

FILTERS (di list page):
  - begin_date : DateField
  - end_date   : DateField

DIALOG PILIH REALISASI (SearchRealizationDialog.vue):
  Filter: begin_date, end_date, memo_type (R/N dropdown)
  Columns: realmemonumber, realizationdate, realizationdescription, realizationamount
  Action: pilih 1 baris → tutup dialog → isi header form + load detail grid via GET /realization/{id}/details
```

---

## CATATAN FILE SUMBER

File yang dibaca:
- `docs/legacy-apps/program/menus/Penyaluran.mnu`
- `docs/legacy-apps/program/menus/popupmenus/Kegiatan/mnuRealizationReturn.mnu`
- `docs/legacy-apps/program/menus/popupmenus/Kegiatan/mnuRealizationReturn_server.py` (kosong, 1 baris)
- `docs/legacy-apps/program/dialogs/Kegiatan/QRealizationReturn_data.py`
- `docs/legacy-apps/program/dialogs/Kegiatan/QRealizationReturn_intr.py`
- `docs/legacy-apps/program/dialogs/Kegiatan/QRealizationReturn.dfr`
- `docs/legacy-apps/program/dialogs/Kegiatan/fRealizationReturn_data.py`
- `docs/legacy-apps/program/dialogs/Kegiatan/fRealizationReturn_intr.py`
- `docs/legacy-apps/program/dialogs/Kegiatan/fRealizationReturn.dfr`
- `docs/legacy-apps/program/dialogs/Kegiatan/fRealizationReturn.svr`
- `docs/legacy-apps/program/dialogs/Laporan/fReportRealizationReturn_data.py`
- `docs/legacy-apps/program/dialogs/Kegiatan/fSelectRealization_intr.py`
- `docs/legacy-apps/program/default.mcf`
- `docs/legacy-apps/program/script_modules/Realisasi.py`
- `docs/legacy-apps/program/script_modules/Transaction.py`
- `docs/reference/datadictionary/ddl_all_schema.sql`

File tidak ditemukan / catatan:
- `dialogs/Kegiatan/fRealization_data.py` dan `fRealization_intr.py` — tidak ada file dengan nama persis itu; realisasi menggunakan `fRealizationProgramReguler` dan `fRealizationProgramNonReguler`. Data yang relevan sudah diperoleh dari `Realisasi.py` dan service.py yang sudah ada.
- `dbchk__ref.sql` dan `dbchk__referr.sql` — hanya berisi COUNT query referential checks, bukan DDL. Skema diperoleh dari `ddl_all_schema.sql`.

==== END MIGRATION_ANALYSIS ====

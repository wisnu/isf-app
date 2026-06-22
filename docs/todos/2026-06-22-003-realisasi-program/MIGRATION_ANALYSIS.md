==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/program/
PORTAL:  zakat
SCOPE:   Realisasi Program Penyaluran — Rutin dan Non Rutin
TANGGAL: 2026-06-22

## Catatan Penting

Modul ini berbeda dari modul Memo Penyaluran (`realizationmemo`) yang sudah
selesai diimplementasi. Realisasi Program adalah pencatatan EKSEKUSI distribusi
yang sesungguhnya berdasarkan memo yang sudah disetujui. Struktur data utama
adalah tabel `program.realization` (bukan `realizationmemo`).

Data existing di DB: R=242 baris, N=8033 baris (kolom `realizationtype`).

──────────────────────────────────────────────────────────────────────────────
── FITUR LIST ────────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

  1. Realisasi Program Penyaluran Rutin (List)
     ROLES:           DIST, SPVDIST
     DIALOG:          dialogs/Kegiatan/QRealisasiRutin.*
     MENU_KEY_KANDIDAT: distribution.realization.regular.list
     SUMBER_MENU:     Penyaluran.mnu — Caption='Realisasi Program Rutin', OnClick='ShowFormClick',
                      StringTag='Kegiatan/QRealisasiRutin'

  2. Tambah/Ubah/Lihat/Hapus Realisasi Program Penyaluran Rutin (Form)
     ROLES:           Tambah/Ubah/Hapus = DIST; Lihat = DIST, SPVDIST
     DIALOG:          dialogs/Kegiatan/fRealizationProgramReguler.*
     MENU_KEY_KANDIDAT: distribution.realization.regular.create /
                        distribution.realization.regular.edit /
                        distribution.realization.regular.delete /
                        distribution.realization.regular.view

  3. Realisasi Program Penyaluran Non Rutin (List)
     ROLES:           DIST, SPVDIST
     DIALOG:          dialogs/Kegiatan/QRealisasiNonRutin.*
     MENU_KEY_KANDIDAT: distribution.realization.non-regular.list
     SUMBER_MENU:     Penyaluran.mnu — Caption='Realisasi Program Non Rutin', OnClick='ShowFormClick',
                      AllowedGroups='DIST;SPVDIST', StringTag='Kegiatan/QRealisasiNonRutin'

  4. Tambah/Ubah/Lihat/Hapus Realisasi Program Penyaluran Non Rutin (Form)
     ROLES:           Tambah/Ubah/Hapus = DIST; Lihat = DIST, SPVDIST
     DIALOG:          dialogs/Kegiatan/fRealizationProgramNonReguler.*
     MENU_KEY_KANDIDAT: distribution.realization.non-regular.create /
                        distribution.realization.non-regular.edit /
                        distribution.realization.non-regular.delete /
                        distribution.realization.non-regular.view

  5. Input/Hapus LPJ Realisasi (sub-dialog, Rutin dan Non Rutin)
     ROLES:           DIST
     DIALOG:          dialogs/Kegiatan/fLPJStatReceivableReguler.* (dipakai untuk keduanya)
     CATATAN:         Hanya aktif jika StatusReceivables='Y' (diproses sebagai piutang).
                      Di-scope Fase 2 — skip dahulu, tapi JANGAN hilangkan kolom statusreclpj.

  6. Pengelolaan Foto Realisasi (sub-dialog)
     ROLES:           DIST
     DIALOG:          dialogs/Kegiatan/fRealizationPhoto.*
     CATATAN:         Pengelolaan file foto — tidak perlu diimplementasi di web (skip Fase 1).

──────────────────────────────────────────────────────────────────────────────
── DISCRIMINATORS (KRITIS) ───────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

Kolom `realizationtype` di `program.realization`:
  - `'R'` → Realisasi Program Rutin (RealizationReguler)
  - `'N'` → Realisasi Program Non Rutin (RealizationNonReguler)

Kolom `realizationmemotype` di `program.realizationmemo`:
  - `'R'` → Memo Rutin (dipakai saat fRealizationProgramReguler memilih memo)
  - `'N'` → Memo Non Rutin (dipakai saat fRealizationProgramNonReguler memilih memo)

Kolom `mustahiqproducttype` di `program.mustahiqproduct`:
  - `'R'` → Program Rutin
  - `'N'` → Program Non Rutin (sudah dikonfirmasi di service existing)

Kolom `statusreceivables` di `program.realization`:
  - `'T'` → Tidak diproses sebagai piutang (default)
  - `'Y'` → Diproses sebagai piutang penyaluran (memerlukan employeeid)

Kolom `statusreclpj` di `program.realization`:
  - `NULL` → Tidak ada LPJ
  - `'Y'` → Sudah ada LPJ

SUMBER:
- `fRealizationProgramReguler_data.py` baris 26: `recRealization.StatusReceivables = 'T'`
- `fRealizationProgramReguler_data.py` baris 278–287: `if RR.StatusReceivables == 'Y': RR.CreateCashAdvanceTransaction()`
- `regular_program/service.py` baris 87: `mp.mustahiqproducttype = 'R'`
- DB actual: `SELECT realizationtype, COUNT(*) FROM program.realization GROUP BY realizationtype;` → R=242, N=8033

──────────────────────────────────────────────────────────────────────────────
── FORM FIELDS ───────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

### DIALOG: dialogs/Kegiatan/QRealisasiRutin (List View — sama struktur dengan QRealisasiNonRutin)

Filter panel (visible):
  - BeginDate : timestamp [Required] — Periode Tanggal (awal)
  - EndDate   : timestamp [Required] — s/d (akhir)

Filter panel (hidden — tidak dipakai):
  - Incolumn    : integer — pilihan kolom pencarian
  - Description : varchar(30) — deskripsi (hanya QRealisasiRutin)
  - keywords    : varchar(30) — keyword (hanya QRealisasiNonRutin)

Kolom grid:
  - RealizationDate        — Tanggal Realisasi
  - RealizationDescription — Deskripsi
  - RealMemoNumber         — Nomor Memo (dari LRealizationMemo)
  - StatusReceivables      — Status Piutang Penyaluran (computed $)
  - StatusRecLPJ           — Status LPJ (computed $)

SUMBER: `QRealisasiRutin.dfr` baris 43–75, `QRealisasiNonRutin.dfr` baris 42–65

### DIALOG: dialogs/Kegiatan/fRealizationProgramReguler (Form Rutin)
### DIALOG: dialogs/Kegiatan/fRealizationProgramNonReguler (Form Non Rutin)

Kedua form IDENTIK secara struktur. Perbedaan hanya:
- Rutin: ClassTypeName='RealizationReguler', memo type='R'
- Non Rutin: ClassTypeName='RealizationNonReguler', memo type='N'

HEADER FIELDS (panel pData, uipR):
  - RealizationDate        : timestamp [Required] — Tanggal Realisasi (editable)
  - RealizationDescription : varchar   [Required] — Deskripsi (editable)
  - RealizationLocation    : varchar   [Required] — Lokasi (editable)
  - LRealizationMemo       : FK lookup [Required] — Nomor Memo (pilih via dialog fSelectMemo)
  - MemoDate               : timestamp [ReadOnly] — Tanggal Memo (auto-fill dari memo)
  - StatusReceivables      : varchar   [Required] — Status Piutang Penyaluran (combo: T/Y)
  - LEmployee              : FK lookup [Conditional] — Karyawan PJ Piutang (visible only jika StatusReceivables=Y)
  - LBudget                : FK lookup [Hidden di form header] — Anggaran (ada di tab Detail Anggaran)

HIDDEN FIELDS (tersimpan tapi tidak ditampilkan di header):
  - Mode             : varchar(10) — operasi (New/Edit/Delete/View)
  - UserInput        : varchar(50) — userId dari session, auto-fill
  - DefaultEmployeeId   : varchar(30) — default employee dari session
  - DefaultEmployeeName : varchar(200) — default employee name dari session
  - RealizationId    : integer — PK (tersembunyi di mode New)

DETAIL TAB — "Detail Realisasi" (grid, uipGD):
  - LMustahiqProduct.MustahiqProductName [ReadOnly] — Nama Program
  - NamaMustahiq                         [ReadOnly] — Nama Mustahiq
  - MemoAmount                           [ReadOnly] — Nominal Memo (dari memo detail)
  - LCashAccount.AccountName             [ReadOnly] — Sumber Dana
  - RealizationAmount                    [Editable] — Nominal Realisasi
  - DetailDescription                    [Editable] — Keterangan
  - ProposalDate                         [ReadOnly] — Tgl Terima Proposal (dari proposal)
  - ProposalNominal                      [ReadOnly] — Nominal Permohonan
  - ProposalReferenceBy                  [ReadOnly] — Pemberi Referensi
  - ProposalReferencePosition            [ReadOnly] — Muzakki/Non Muzakki

  Summary (panel pDetail, uipDR):
  - TotalDropping    [ReadOnly] — Total Pengajuan Memo (sum MemoAmount)
  - TotalRealization [ReadOnly] — Total Realisasi (sum RealizationAmount)

MITRA TAB — "Mitra" (grid gPartner, uipLsPartner):
  - LPartner.LCustomer.CustomerName [Editable lookup] — Nama Mitra
  CATATAN: Fitur mitra disebut "tidak dipakai dulu" di kode comment

DETAIL ANGGARAN TAB — "Detail Anggaran" (grid gBudget, uipLsBudget):
  - LProduct.ProductCode [ReadOnly] — Kode Program
  - LProduct.ProductName [ReadOnly] — Nama Program
  - LBudget.BudgetCode   [Editable] — Kode Anggaran
  - LBudget.ItemName     [ReadOnly] — Nama Anggaran
  CATATAN: Auto-populated dari memo detail saat memo dipilih

FOTO TAB — "Photo/Foto" (diabaikan untuk implementasi web Fase 1)

SUMBER: `fRealizationProgramReguler.svr` baris 9–221, `fRealizationProgramReguler.dfr` baris 26–1073,
        `fRealizationProgramNonReguler.svr` baris 9–215

──────────────────────────────────────────────────────────────────────────────
── DB SCHEMA ─────────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

### program.realization (tabel master realisasi)

```
realizationid          integer          PK
realizationdate        timestamp        Tanggal realisasi
realmemoid             integer          FK → program.realizationmemo.realmemoid
realizationtype        varchar(1)       DISCRIMINATOR: 'R'=Rutin, 'N'=Non Rutin
realizationdescription varchar(200)     Deskripsi
realizationinputdate   timestamp(6)     Tanggal input (auto NOW())
realizationinputuser   varchar(100)     User input (dari session)
realizationlocation    varchar(200)     Lokasi
memoamount             numeric(30,8)    Jumlah memo (tidak dipakai di save baru)
transactionid          integer          FK → transaction (dibuat oleh CreateRealizationTransaction)
branchcode             varchar(5)       Kode cabang (dari session)
budgetid               integer          FK → transaction.Budget (deprecated, pakai realizationbudget)
realizationamount      numeric(30,8)    Total realisasi (sum dari detail)
partnerid              integer          Deprecated (dipakai di versi lama)
employeeid             varchar(20)      FK → VEmployee (diisi jika statusreceivables='Y')
statusreceivables      varchar(1)       'T'=Tidak/'Y'=Ya (piutang penyaluran)
statusreclpj           varchar(1)       NULL=Tidak Ada/'Y'=Ada LPJ
```

### program.realizationdetail (detail per mustahiq/program)

```
realizationdetailid    integer          PK
realizationid          integer          FK → program.realization
mustahiqproductid      integer          FK → program.mustahiqproduct
memoamount             numeric(30,8)    Nominal dari memo (reference)
realizationamount      double precision Nominal realisasi aktual
detaildescription      varchar(200)     Keterangan detail
accountno              varchar(30)      Rekening kas sumber dana
branchcode             varchar(5)       Kode cabang
ashnaf                 varchar(1)       Ashnaf (dari mustahiqproduct)
fundproductid          integer          FK → fund product (dari mustahiqproduct)
```

### program.realizationbudget (anggaran per realisasi)

```
realbudgetid           integer          PK
realizationid          integer          FK → program.realization
budgetid               integer          FK → transaction.budget
productid              integer          FK → program.product
```

### program.realizationpartner (mitra per realisasi)

```
realizationpartnerid   integer          PK
realizationid          integer          FK → program.realization
partnerid              integer          FK → program.partner
```

### program.realizationphoto (foto realisasi — Fase 2)

```
photoid                integer          PK
photofilename          varchar(100)     Nama file
realizationid          integer          FK → program.realization
photodescription       varchar(200)     Deskripsi foto
```

### program.realizationmemo (sudah ada, referensi)

```
realmemoid             integer          PK
realmemonumber         varchar(100)     Nomor memo
realmemosubject        varchar(100)     Perihal
realmemoamount         double precision Total nominal
realmemofrom           varchar(100)     Pengirim
realmemoto             varchar(100)     Penerima
realizationmemotype    varchar(1)       DISCRIMINATOR: 'R'=Rutin, 'N'=Non Rutin
userinput              varchar(30)      User yang input
realmemodate           timestamp        Tanggal memo
branchcode             varchar(10)      Kode cabang
```

### program.realizationmemodetail (detail per memo — reference only)

```
realmemodetailid       integer          PK
realmemoid             integer          FK → program.realizationmemo
mustahiqproductid      integer          FK → program.mustahiqproduct
productid              integer          FK → program.product
realmemodetailamount   numeric          Nominal per program
```

──────────────────────────────────────────────────────────────────────────────
── UI FLOW ───────────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

### ON OPEN (List View)
- Filter default: BeginDate = EndDate = today (dari FormSetDataEx)
- Grid kosong — user klik "Tampilkan Data" untuk load
- SUMBER: `QRealisasiRutin_data.py` baris 5–11

### ON OPEN (Form — New)
- RealizationDate = today (config.Now())
- UserInput = session UserId
- StatusReceivables = 'T' (default tidak jadi piutang)
- DefaultEmployeeId/Name = dari Enterprise.User berdasarkan Nomor_Karyawan session user
- LEmployee field: visible=false (hanya tampil jika StatusReceivables=Y)
- Detail grid: kosong — user harus pilih memo terlebih dahulu
- SUMBER: `fRealizationProgramReguler_data.py` baris 18–34

### ON OPEN (Form — Edit/View/Delete)
- Load semua field dari `RealizationReguler` (atau NonReguler) berdasarkan key
- Auto-fill MemoDate dari `RealizationMemoReguler.RealMemoDate`
- Load detail dari `RealizationMemoDetail` via SQL query (SetRealizationDetailByMemo)
- Load partner, budget, foto
- Jika Edit/Delete: validasi StatusReceivables + StatusRecLPJ (keduanya Y = tidak bisa diubah)
- Jika Edit/Delete: cek apakah ada data di `realizationreturn` (tidak bisa diubah jika ada)
- SUMBER: `fRealizationProgramReguler_data.py` baris 62–90

### ON SELECT MEMO
- User klik tombol "Pilih Memo" → buka fSelectMemo dengan filter type='R' atau 'N'
- Setelah memo dipilih: jalankan SQL JOIN ke RealizationMemoDetail+MustahiqProduct+Customer
  untuk populate grid detail dengan semua program dari memo
- RealizationAmount default = MemoAmount (editable untuk penyesuaian)
- Auto-populate tab Detail Anggaran dengan product dari memo
- SUMBER: `fRealizationProgramReguler_intr.py` baris 120–129, `_data.py` baris 92–172

### ON STATUS RECEIVABLES CHANGE
- Jika StatusReceivables = 'Y': tampilkan field LEmployee
- Jika StatusReceivables = 'T': sembunyikan field LEmployee
- SUMBER: `fRealizationProgramReguler_intr.py` baris 435–444

### ON SAVE (client-side validasi via CekInput)
1. Tanggal tidak boleh kosong
2. Memo belum dipilih (RealMemoId = null/0)
3. Deskripsi belum diinput
4. Lokasi belum diinput
5. Jika StatusReceivables='Y' maka LEmployee.EmployeeId wajib diisi
6. Cek duplikasi mitra (tidak boleh mitra sama dua kali)
- SUMBER: `fRealizationProgramReguler_intr.py` baris 249–272

──────────────────────────────────────────────────────────────────────────────
── SAVE LOGIC ────────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

### ALUR (save function di _data.py, baris 344–397)

Data dikirim ke otorisasi legacy (enterprise.api/otorisasi.storeDataPacket),
bukan langsung save. Di isf-app BARU, simpan langsung ke DB (tidak pakai otorisasi
modul program — program tidak masuk ke otorisasi.submission seperti keuangan).

SUMBER: `fRealizationProgramReguler_data.py` baris 344–397

Kode otorisasi legacy:
- Mode New:    kode_entri='DIST019' (Rutin), kode_entri='DIST026' (Non Rutin)
- Mode Edit:   kode_entri='DIST020' (Rutin), kode_entri='DIST027' (Non Rutin)
- Mode Delete: kode_entri='DIST039' (Rutin), kode_entri='DIST040' (Non Rutin)
- id_peran = "SPVDIST" (supervisor distribution approves)

### authorize() — eksekusi setelah otorisasi disetujui (baris 209–341)

MODE NEW (baris 216–288):
1. `helper.CreatePObject('RealizationReguler')` → INSERT ke `program.realization` dengan:
   - realizationtype = 'R' (Rutin) atau 'N' (Non Rutin) — KRITIS discriminator
   - realizationdate = RealizationDate
   - realmemoid = LRealizationMemo.RealMemoId
   - budgetid = LBudget.BudgetId (deprecated, dulu main budget, sekarang pakai realizationbudget)
   - realizationdescription = RealizationDescription
   - realizationlocation = RealizationLocation
   - statusreceivables = StatusReceivables
   - realizationinputuser = UserInput (session userId)
   - branchcode = dari session GetUserInfo()[4]
2. INSERT ke `program.realizationdetail` untuk setiap baris detail:
   - realizationid, mustahiqproductid, memoamount, realizationamount
   - detaildescription, accountno
   - ashnaf, fundproductid (dari MustahiqProduct)
3. Sum TotalRealization → set realization.realizationamount
4. INSERT ke `program.realizationpartner` per mitra
5. INSERT ke `program.realizationbudget` per baris anggaran
6. FlushUpdates()
7. Jika StatusReceivables = 'Y':
   - Set employeeid
   - `RR.CreateCashAdvanceTransaction()` → INSERT ke tabel transaction (cash advance)
8. Jika StatusReceivables = 'T':
   - Set employeeid = None, statusreclpj = None
   - `RR.CreateRealizationTransaction()` → INSERT ke tabel transaction (penyaluran biasa)

MODE EDIT:
1. GetObject RealizationReguler/NonReguler
2. `RR.DeleteListBySQL()` → hapus detail, partner, budget
3. `RR.DeleteTransaction()` → hapus transaksi yang terkait
4. FlushUpdates()
5. Re-set semua field
6. Re-INSERT detail, partner, budget
7. Buat ulang transaksi

MODE DELETE (baris 326–340):
1. `RR.DeleteTransaction()` → hapus transaksi
2. DELETE FROM realization WHERE RealizationId=...
3. DELETE FROM realizationdetail WHERE RealizationId=...
4. DELETE FROM realizationphoto WHERE RealizationId=... (jika ada)
SUMBER: `fRealizationProgramReguler_data.py` baris 326–341

──────────────────────────────────────────────────────────────────────────────
── LIST/QUERY LOGIC ──────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

OQL (Rutin): `Select from RealizationReguler [RealizationDate >= :BeginDate and RealizationDate < :EndDate]`
OQL (NonRutin): `Select from RealizationNonReguler [RealizationDate >= :BeginDate and RealizationDate < :EndDate]`

Kolom yang ditampilkan:
- RealizationDate, RealizationDescription
- LRealizationMemo.RealMemoNumber (Nomor Memo)
- StatusRecLPJ (computed)
- StatusReceivables (computed)
- RealizationId, self

EndDate di-increment +1 hari (inklusif): `intEndDate + 1`

SQL ISF-APP equivalent:
```sql
SELECT
    r.realizationid,
    r.realizationdate,
    r.realizationdescription,
    m.realmemonumber,
    r.statusreceivables,
    r.statusreclpj,
    r.branchcode
FROM program.realization r
LEFT JOIN program.realizationmemo m ON m.realmemoid = r.realmemoid
WHERE r.realizationtype = 'R'  -- atau 'N'
  AND r.realizationdate >= :begin_date
  AND r.realizationdate < :end_date + INTERVAL '1 day'
  AND r.branchcode = :branch_code  -- dari session BFF
ORDER BY r.realizationdate
```

SUMBER: `QRealisasiRutin_intr.py` baris 31–56, `QRealisasiNonRutin_intr.py` baris 31–56

──────────────────────────────────────────────────────────────────────────────
── VALIDATION RULES ──────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

CLIENT-SIDE (dari CekInput, _intr.py baris 249–272):
1. RealizationDate tidak boleh null
2. LRealizationMemo.RealMemoId tidak boleh null/0
3. RealizationDescription tidak boleh kosong (setelah .strip())
4. RealizationLocation tidak boleh kosong (setelah .strip())
5. Jika StatusReceivables='Y': LEmployee.EmployeeId wajib (tidak boleh 0)
6. Tidak boleh ada mitra duplikat (CekDuplikasiMitra)

SERVER-SIDE (dari FormSetDataEx _data.py, baris 74–84):
7. Jika Edit/Delete: tidak bisa jika StatusReceivables='Y' DAN StatusRecLPJ='Y'
   (sudah ada LPJ dan piutang, tidak bisa diubah)
8. Jika Edit/Delete: tidak bisa jika ada data di `realizationreturn` untuk RealizationId ini
   (harus hapus pengembalian dulu)

FILTER-SIDE (dari QRealisasiRutin_intr.py baris 22–29):
9. BeginDate wajib diisi
10. EndDate wajib diisi
11. BeginDate tidak boleh lebih besar dari EndDate

──────────────────────────────────────────────────────────────────────────────
── RELATED ENTITIES ──────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

RELASI:
- program.realization.realmemoid        → program.realizationmemo.realmemoid
- program.realization.branchcode        → branch (dari session, tidak FK hard)
- program.realizationdetail.realizationid → program.realization.realizationid
- program.realizationdetail.mustahiqproductid → program.mustahiqproduct.mustahiqproductid
- program.mustahiqproduct.mustahiqid    → program.mustahiq.mustahiqid
- program.mustahiq.customerid           → program.customer.customerid
- program.mustahiqproduct.proposalid    → program.proposal.proposalid (optional)
- program.realizationdetail.accountno   → transaction.cashaccount.accountno
- program.realizationbudget.realizationid → program.realization.realizationid
- program.realizationbudget.budgetid    → transaction.budget.budgetid
- program.realizationbudget.productid   → program.product.productid
- program.realizationpartner.realizationid → program.realization.realizationid
- program.realizationpartner.partnerid  → program.partner.partnerid
- program.realization.transactionid     → transaction.transaction (dibuat oleh CreateRealizationTransaction)

──────────────────────────────────────────────────────────────────────────────
── KOMPLEKSITAS ──────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

LEVEL:    TINGGI
ALASAN:
- 7 entitas DB terlibat (realization, realizationdetail, realizationbudget,
  realizationpartner, realizationmemo, mustahiqproduct, cashaccount)
- 6+ JOIN dalam query detail
- Conditional logic: StatusReceivables menentukan jenis transaksi yang dibuat
  (CreateCashAdvanceTransaction vs CreateRealizationTransaction)
- Dua mode realisasi (R/N) dengan form identik tetapi entity class berbeda
- Validasi berlapis: client + server + pre-condition check
- Cascade delete manual (3 tabel dihapus manual, bukan FK CASCADE)
- Auto-populate detail dari memo saat memo dipilih

WORKFLOW: Custom (bukan pure CRUD — ada business logic transaksi)

Catatan Rekomendasi Model: Modul ini memiliki >5 relasi DB, logic transaksi
bercabang, dan query JOIN kompleks. Untuk implementasi, model `opus` direkomendasikan
jika nuwis-python-builder perlu generate logic transaksi lengkap.

──────────────────────────────────────────────────────────────────────────────
── STATUS IMPLEMENTASI EXISTING ─────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

SUDAH ADA (tidak perlu diimplementasi ulang):
- `apps_zakat/api-python/app/modules/distribution/realization_memo/` — Memo Penyaluran (CRUD)
- `apps_zakat/api-python/app/modules/distribution/regular_program/` — Program Rutin (CRUD mustahiqproduct)
- `apps_zakat/api-python/app/modules/distribution/non_regular_program/` — Program Non Rutin (CRUD mustahiqproduct)
- `apps_zakat/api-python/app/modules/distribution/mustahiq/` — Data Mustahiq
- `apps_zakat/api-python/app/modules/distribution/partner/` — Data Mitra
- `apps_zakat/api-python/app/modules/distribution/proposal/` — Proposal

BELUM ADA (yang perlu diimplementasi untuk fitur ini):
- Modul Realisasi Program Rutin dan Non Rutin (tabel `program.realization`)
- Endpoint CRUD untuk `program.realizationdetail`, `realizationbudget`, `realizationpartner`
- Lookup memo (filter by type, sudah belum dipakai di realisasi lain)
- Lookup mustahiq product untuk dropdown detail

──────────────────────────────────────────────────────────────────────────────
── HANDOFF ───────────────────────────────────────────────────────────────────
──────────────────────────────────────────────────────────────────────────────

→ nuwis-seed-gen:
  MENU_KEY: distribution.realization.regular.list
  LABEL:    Realisasi Program Rutin
  ROLES:    DIST, SPVDIST

  MENU_KEY: distribution.realization.non-regular.list
  LABEL:    Realisasi Program Non Rutin
  ROLES:    DIST, SPVDIST

  Catatan: Tambahkan ke sidebar domain 'distribution' pada group "Kegiatan"

→ nuwis-db-migrator:
  MIGRATIONS:
  - Tidak ada tabel baru. Tabel `program.realization`, `realizationdetail`,
    `realizationbudget`, `realizationpartner`, `realizationphoto` sudah ada.
  - Perlu cek: apakah ada sequence untuk realizationid, realizationdetailid, dll.
    Jalankan: SELECT * FROM information_schema.sequences WHERE sequence_schema='program';

  SEQUENCES YANG DIBUTUHKAN (cek dulu):
  - program.seq_realization (untuk realization.realizationid)
  - program.seq_realizationdetail (untuk realizationdetail.realizationdetailid)
  - program.seq_realizationbudget (untuk realizationbudget.realbudgetid)
  - program.seq_realizationpartner (untuk realizationpartner.realizationpartnerid)

  DWH_VIEWS: Tidak diperlukan untuk Fase 1. Laporan pakai report-api langsung.

→ nuwis-python-builder:
  Module path: apps_zakat/api-python/app/modules/distribution/realization/

  ENDPOINTS:
  GET    /distribution/realization?type=R&date_from=&date_to=&page=&page_size=
    - List realisasi dengan filter type (R/N), tanggal, branch dari session
    - Return: realizationid, realizationdate, realizationdescription,
              realmemonumber, statusreceivables, statusreclpj, branchcode

  POST   /distribution/realization?type=R
    - Create realisasi baru
    - Body: RealizationBody (date, description, location, memo_id, status_receivables,
            employee_id, details[], budgets[], partners[])
    - Logic: INSERT realization + detail + budget + partner
    - PENTING: jangan panggil CreateRealizationTransaction dari Python — transaksi
      di modul program legacy tidak diimplementasi di isf-app (belum ada integrasi jurnal).
      Simpan ke program.realization + detail saja. Tambahkan TODO comment.

  GET    /distribution/realization/{id}?type=R
    - Detail realisasi: header + detail grid (JOIN ke mustahiqproduct, customer)
    - Tambahkan: budget list, partner list

  PUT    /distribution/realization/{id}?type=R
    - Update realisasi: DELETE detail lama + INSERT baru
    - Validasi: tidak bisa edit jika statusreceivables='Y' AND statusreclpj='Y'
    - Validasi: tidak bisa edit jika ada baris di realizationreturn

  DELETE /distribution/realization/{id}?type=R
    - Delete: hapus realizationdetail, realizationpartner, realizationbudget, lalu realization
    - Validasi sama dengan PUT

  GET    /distribution/realization/lookup/memos?type=R&search=
    - Lookup memo yang bisa dipilih (untuk dropdown "Pilih Memo")
    - Pakai program.realizationmemo dengan realizationmemotype = type
    - Return: realmemoid, realmemonumber, realmemodate, realmemoamount

  GET    /distribution/realization/lookup/memo-detail/{memo_id}
    - Ambil detail dari sebuah memo (auto-populate grid saat memo dipilih)
    - JOIN: realizationmemodetail + mustahiqproduct + customer + cashaccount
    - Return: mustahiqproductid, mustahiqproductname, customername, accountno,
              accountname, realmemodetailamount, ashnaf, fundproductid,
              proposaldate, proposalnominal, proposalreferenceby

  DISCRIMINATORS (KRITIS — jangan hilangkan):
  - realization.realizationtype = 'R' atau 'N'
  - realizationmemo.realizationmemotype = 'R' atau 'N' (untuk filter lookup memo)
  - realization.statusreceivables = 'T' atau 'Y' (T=default)
  - realization.statusreclpj = NULL atau 'Y'

→ nuwis-bff-builder:
  Route prefix: /api/distribution/realization
  menu_key: distribution.realization.regular.list dan distribution.realization.non-regular.list
  _resolve_branch: wajib — filter berdasarkan branchcode dari session
  Catatan: type (R/N) harus di-validate di BFF juga (hanya 'R' atau 'N' yang valid)

→ nuwis-ui-builder:
  PAGE_TYPE: list + form (dua halaman: regular dan non-regular)

  HALAMAN LIST:
  - Route: /distribution/realization/regular dan /distribution/realization/non-regular
  - Filter: DateField (BeginDate), DateField (EndDate), tombol "Tampilkan"
  - Tabel: Tanggal Realisasi, Deskripsi, Nomor Memo, Status Piutang, Status LPJ
  - Actions: Tambah, Ubah, Lihat, Hapus (sesuai role DIST/SPVDIST)
  - Pagination: standalone Paginator di atas tabel (default 25 baris)

  HALAMAN FORM:
  - Route: /distribution/realization/regular/new, /regular/:id/edit, /regular/:id/view
  - Header fields: DateField (RealizationDate), Input (RealizationDescription, RealizationLocation)
  - Memo picker: SearchSelect + tombol "Pilih Memo" → dialog/modal fSelectMemo equivalent
    (lookup dari /lookup/memos?type=R)
  - MemoDate: auto-fill readonly setelah memo dipilih
  - StatusReceivables: dropdown (Tidak/Ya) — nilai T/Y
  - LEmployee: SearchSelect, visible HANYA jika StatusReceivables=Y
  - Tab "Detail Realisasi": DataTable readonly dengan kolom Nama Program, Nama Mustahiq,
    Nominal Memo, Sumber Dana; kolom editable: Nominal Realisasi, Keterangan
  - Tab "Detail Anggaran": DataTable readonly (auto-populated dari memo)
  - Tab "Mitra": DataTable editable dengan SearchSelect untuk nama mitra (opsional, skip Fase 1)
  - Footer summary: Total Pengajuan Memo, Total Realisasi

  FILTERS:
  - date_from: DateField
  - date_to: DateField
  - type discriminator (R/N) dikodekan per halaman, tidak di UI

  NOTE untuk ui-builder:
  - Saat memo dipilih → call GET /lookup/memo-detail/{memo_id} → populate tabel detail
  - RealizationAmount default = MemoAmount per baris (editable)
  - Validation sebelum submit: tanggal, memo, deskripsi, lokasi, employee (if receivables)

==== END MIGRATION_ANALYSIS ====

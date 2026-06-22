==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/program/
PORTAL:  zakat
SCOPE:   Monitoring Program Penyaluran (kunjungan lapangan ke mustahiq)
TANGGAL: 2026-06-22

── FITUR LIST ──────────────────────────────────────────────────
  1. List Monitoring Program Penyaluran (QMonotoringProgramPenyaluran)
     ROLES:           DIST, SPVDIST
     DIALOG:          dialogs/Kegiatan/QMonotoringProgramPenyaluran.*
     MENU_KEY_KANDIDAT: distribution.monitoring.list
     CATATAN: Typo pada nama file legacy "Monotoring" (bukan "Monitoring") —
              isf-app HARUS menggunakan ejaan benar "monitoring"

  2. Tambah Data Monitoring (fMonitoringProgram — mode New)
     ROLES:           DIST
     DIALOG:          dialogs/Kegiatan/fMonitoringProgram.*
     MENU_KEY_KANDIDAT: distribution.monitoring.create
     CATATAN: Diakses via context menu (popup) dari list, bukan menu utama

  3. Ubah Data Monitoring (fMonitoringProgram — mode Edit)
     ROLES:           DIST
     DIALOG:          dialogs/Kegiatan/fMonitoringProgram.*
     MENU_KEY_KANDIDAT: distribution.monitoring.update

  4. Lihat Detail Monitoring (fMonitoringProgram — mode View)
     ROLES:           DIST, SPVDIST
     DIALOG:          dialogs/Kegiatan/fMonitoringProgram.*
     MENU_KEY_KANDIDAT: distribution.monitoring.view
     CATATAN: View mode = semua field ReadOnly, tombol Simpan disembunyikan

  5. Hapus Data Monitoring
     ROLES:           DIST, SPVDIST
     DIALOG:          inline (via popup menu, tidak ada form terpisah)
     MENU_KEY_KANDIDAT: distribution.monitoring.delete
     CATATAN: Konfirmasi dialog lalu DeleteMonitoring server call


── FORM FIELDS (per dialog) ────────────────────────────────────

DIALOG: dialogs/Kegiatan/QMonotoringProgramPenyaluran (list + filter)
FILTER FIELDS:
  - BeginDate  : Date  [Required] — Periode Tanggal (dari)
  - EndDate    : Date  [Required] — s/d (sampai dengan)
  - Incolumn   : Integer [Hidden]  — enum filter kolom (0=Seluruh Data, 1=Nama Mustahik, 2=Alamat)
  - keywords   : String [Hidden]   — kata kunci pencarian

LIST COLUMNS:
  - VisitDate          : Date   — Tanggal Monitoring
  - VisitLocation      : String — Lokasi
  - CustomerName       : String — Nama Mustahiq (dari tabel CUSTOMER via MUSTAHIQ)
  - ProductName        : String — Nama Program (dari tabel PRODUCT via MUSTAHIQPRODUCT)
  - MustahiqProductName: String — Program Detail (nama spesifik per mustahiq)
  - VisitId            : Integer [Hidden] — primary key, digunakan untuk drill-down


DIALOG: dialogs/Kegiatan/fMonitoringProgram (form detail)
SECTIONS: pMustahiqProductVisit | multipages1 (4 tabs)
TABS: Pihak Yang Bertemu | Tujuan Kunjungan | Hasil Kunjungan | Tindak Lanjut

MAIN FIELDS (pMustahiqProductVisit):
  - LMustahiq.LCustomer.CustomerName : String  [Required] — Nama Mustahiq (lookup)
  - LMustahiq.MustahiqId             : Integer [Required, Hidden] — FK ke MUSTAHIQ
  - LMustahiq.LCustomer.AddressStreet: String  [Auto-fill, Hidden] — Alamat Jalan
  - LMustahiq.LCustomer.AddressKelurahan : String [Auto-fill, Hidden] — Kelurahan
  - LMustahiq.LCustomer.AddressKecamatan : String [Auto-fill, Hidden] — Kecamatan
  - LMustahiqProduct.MustahiqProductName : String [Optional] — Program Penyaluran (lookup)
  - LMustahiqProduct.MustahiqProductId   : Integer [Optional, Hidden] — FK ke MUSTAHIQPRODUCT
  - LMustahiqProduct.LProduct.ProductName: String [Auto-fill, Hidden] — Nama Program
  - VisitAddress    : String  [Required, max=100] — Alamat (auto-fill dari mustahiq, bisa di-edit)
  - VisitLocation   : String  [Required, max=200] — Tempat Pertemuan
  - VisitDate       : Date    [Required] — Tanggal Pelaksanaan
  - VisitBeginTime  : Date/Time [Hidden] — Waktu Mulai (ada di .svr, tersembunyi di UI)
  - VisitEndTime    : Date/Time [Hidden] — Waktu Akhir (ada di .svr, tersembunyi di UI)

HIDDEN FIELDS (tersimpan tapi tak tampil):
  - Mode    : String  — 'New' | 'Edit' | 'View' (control mode form)
  - FollowUpId  : Integer — pointer ke baris tindak lanjut yang sedang diedit
  - ResultId    : Integer — pointer ke baris hasil kunjungan yang sedang diedit
  - PurposeId   : Integer — pointer ke baris tujuan kunjungan yang sedang diedit
  - VisitId     : Integer — PK record (mode View/Edit)

TAB: Pihak Yang Bertemu — sub-grid dua kolom (BPZIS dan Mustahiq/Yayasan)
  gridVPAmil (Pihak BPZIS):
    - VisitPersonName     : String [Required] — Nama
    - VisitPersonPosition : String [Required] — Unit Kerja / Bidang
    - VisitPersonId       : Integer [Hidden]  — PK
  gridVPMustahiq (Pihak Mustahiq / Yayasan Pengelola):
    - VisitPersonName     : String [Required] — Nama
    - VisitPersonPosition : String [Required] — Jabatan
    - VisitPersonId       : Integer [Hidden]  — PK

TAB: Tujuan Kunjungan
  gridTujuan:
    - VisitItemAnnotation : String [Required] — Tujuan Kunjungan (multiline, max=200)
    - VisitItemId         : Integer [Hidden]  — PK

TAB: Hasil Kunjungan
  gridHasil:
    - VisitItemAnnotation : String [Required] — Hasil Kunjungan (multiline, max=200)
    - VisitItemId         : Integer [Hidden]  — PK

TAB: Tindak Lanjut
  gridTindakLanjut:
    - VisitItemAnnotation : String [Required] — Tindak Lanjut (multiline, max=200)
    - VisitItemId         : Integer [Hidden]  — PK

READ_ONLY (auto-fill):
  - VisitAddress   — pre-fill dari AddressStreet mustahiq saat pilih mustahiq
  - LMustahiq.LCustomer.AddressStreet / Kelurahan / Kecamatan — auto-fill
  - LMustahiqProduct.LProduct.ProductName — auto-fill saat pilih program

HIDDEN (tersimpan tapi tak tampil di UI):
  - VisitBeginTime, VisitEndTime — ada di DB tapi form menyembunyikannya


── UI FLOW ─────────────────────────────────────────────────────

ON OPEN (list — QMonotoringProgramPenyaluran):
  - Default BeginDate dan EndDate = hari ini (config.Now() di FormSetDataEx)
  - Tidak auto-load data — user harus klik "Tampilkan Data" untuk memuat list
  - Validasi: BeginDate dan EndDate wajib, BeginDate <= EndDate

ON FILTER (FilterClick):
  - Panggil server method: CallServerMethod("initQuery", ph)
  - Server executes SQL query dengan filter VISITDATE >= BeginDate AND < (EndDate+1)
  - Filter tambahan: VISITTYPE = 'P' (hanya Program Penyaluran, bukan tipe visit lain)
  - Hasil ditampilkan di QryVisit grid (QueryColumn/DataTable)

ON ADD (AddData di _intr.py):
  - Buka form fMonitoringProgram dengan mode 'New'
  - Refresh grid setelah form ditutup dengan OK

ON EDIT (EditData di _intr.py):
  - Ambil key: 'PObj:MustahiqProductVisit#VisitID=' + VisitId
  - Buka form fMonitoringProgram dengan mode 'Edit' + params berisi key

ON VIEW (ViewData di _intr.py):
  - Sama dengan Edit tapi mode 'View' — semua control ReadOnly, Simpan disembunyikan

ON DELETE (DeleteData di _intr.py):
  - ConfirmDialog lalu CallServerMethod('DeleteMonitoring', {key})
  - Server: config.AccessPObject(key).Delete() dalam transaction

ON OPEN (form detail — fMonitoringProgram):
  - Mode New: field mustahiq dan program di-set ke '?' (placeholder)
  - Mode Edit/View: FormSetDataEx load record via PObject key
    - uipMPV: load MustahiqProductVisit record
    - uipGVPAmil: load dari VISITPERSON WHERE visitid=X AND VisitPersonType='A'
    - uipGVPMustahiq: load dari VISITPERSON WHERE visitid=X AND VisitPersonType='S'
    - uipGTujuan: load dari VISITITEM WHERE visitid=X AND VisitItemType='P'
    - uipTindakLanjut: load dari VISITITEM WHERE visitid=X AND VisitItemType='F'
    - uipGHasil: load dari VISITITEM WHERE visitid=X AND VisitItemType='R'

ON SAVE (bSimpanClick):
  Validasi client-side (IsRequiredComplete):
    1. MustahiqId != 0 (mustahiq wajib dipilih)
    2. VisitAddress tidak kosong
    3. VisitLocation tidak kosong
    4. VisitDate tidak kosong
    5. gridVPAmil.RecordCount > 0 (minimal 1 pihak BPZIS)
    6. gridVPMustahiq.RecordCount > 0 (minimal 1 pihak mustahiq)
    7. gridTujuan.RecordCount > 0 (minimal 1 tujuan kunjungan)
    8. gridHasil.RecordCount > 0 (minimal 1 hasil kunjungan)
    9. gridTindakLanjut.RecordCount > 0 (minimal 1 tindak lanjut)
  Setelah validasi pass: CallServerMethod("Simpan", dataPacket)


── SAVE LOGIC ──────────────────────────────────────────────────

ENTRY:   dialogs/Kegiatan/fMonitoringProgram_data.py → Simpan()
ALUR:
  1. Baca recMPV.Mode (New atau Edit)
  2. Mode New: helper.CreatePObject('MustahiqProductVisit')
     Mode Edit: helper.GetObject('MustahiqProductVisit', recMPV.VisitId)
                + DeleteAllPObjs() pada LsVisitPerson dan LsVisitItem (replace all)
  3. Set field: VisitAddress, VisitDate, VisitBeginTime, VisitEndTime,
                VisitLocation, MustahiqId, MustahiqProductId (boleh 0)
  4. Loop uipGVPAmil: CreatePObject('VisitPersonAmil') per baris
     Set: VisitPersonName, VisitPersonPosition, VisitId = MPV.VisitId
  5. Loop uipGVPMustahiq: CreatePObject('VisitPersonMustahiq') per baris
     Set: VisitPersonName, VisitPersonPosition, VisitId = MPV.VisitId
  6. Loop uipGTujuan: CreatePObject('VisitPurpose')
     Set: VisitItemAnnotation, VisitId = MPV.VisitId
  7. Loop uipGHasil: CreatePObject('VisitResult')
     Set: VisitItemAnnotation, VisitId = MPV.VisitId
  8. Loop uipTindakLanjut: CreatePObject('VisitFollowUp')
     Set: VisitItemAnnotation, VisitId = MPV.VisitId
  9. config.Commit() — sukses
     except: config.Rollback() + Is_Err = 1

DELETE LOGIC:   dialogs/Kegiatan/QMonotoringProgramPenyaluran_data.py → DeleteMonitoring()
  1. AccessPObject(recParam.key) — akses record via PObject reference
  2. oMonitoring.Delete() — framework menghapus cascade (VISITPERSON, VISITITEM)
  3. config.Commit() dalam try/except + rollback


── SCHEMA DB ───────────────────────────────────────────────────

ENTITIES:

  - Visit (base class) → tabel: VISIT
    kolom: visitid (PK, INTEGER), visitdate (TIMESTAMP), visitlocation (VARCHAR 200),
           visitbegintime (TIMESTAMP), visitendtime (TIMESTAMP),
           visitaddress (VARCHAR 200), visittype (VARCHAR 1, classifier)
    list: LsVisitPerson → VISITPERSON, LsVisitItem → VISITITEM

  - MustahiqProductVisit (subtype Visit) → tabel: VISIT (single-table inheritance)
    kolom tambahan: mustahiqid (FK → MUSTAHIQ), mustahiqproductid (FK → MUSTAHIQPRODUCT, nullable)
    discriminator: visittype = 'P'

  - VisitPerson (base) → tabel: VISITPERSON
    kolom: visitpersonid (PK, INTEGER), visitid (FK → VISIT),
           visitpersonname (VARCHAR 100), visitpersonposition (VARCHAR 100),
           visitpersontype (VARCHAR 1, classifier)

  - VisitPersonAmil (subtype VisitPerson) → tabel: VISITPERSON
    discriminator: visitpersontype = 'A'

  - VisitPersonMustahiq (subtype VisitPerson) → tabel: VISITPERSON
    discriminator: visitpersontype = 'S'

  - VisitItem (base) → tabel: VISITITEM
    kolom: visititemid (PK, INTEGER), visitid (FK → VISIT),
           visititemtype (VARCHAR 1, classifier), visititemannotation (VARCHAR 200)

  - VisitPurpose (subtype VisitItem) → tabel: VISITITEM
    discriminator: visititemtype = 'P'

  - VisitResult (subtype VisitItem) → tabel: VISITITEM
    discriminator: visititemtype = 'R'

  - VisitFollowUp (subtype VisitItem) → tabel: VISITITEM
    discriminator: visititemtype = 'F'

RELASI:
  - VISIT.mustahiqid → MUSTAHIQ (FK)
  - VISIT.mustahiqproductid → MUSTAHIQPRODUCT (FK, nullable/optional)
  - VISITPERSON.visitid → VISIT (FK)
  - VISITITEM.visitid → VISIT (FK)
  - MUSTAHIQPRODUCT.mustahiqid → MUSTAHIQ (FK)
  - MUSTAHIQPRODUCT.productid → PRODUCT (FK)
  - MUSTAHIQ.customerid → CUSTOMER (FK)

QUERY LIST (initQuery di _data.py):
  SELECT A.VISITDATE, A.VISITLOCATION, A.VISITBEGINTIME, A.VISITENDTIME,
         A.VISITADDRESS, B.PRODUCTNAME, B.MUSTAHIQPRODUCTNAME, G.CUSTOMERNAME, A.VISITID
  FROM VISIT A
  LEFT JOIN (
    SELECT C.MUSTAHIQPRODUCTID, C.MUSTAHIQPRODUCTNAME, D.PRODUCTNAME
    FROM MUSTAHIQPRODUCT C, PRODUCT D
    WHERE C.PRODUCTID = D.PRODUCTID
  ) B ON (A.MUSTAHIQPRODUCTID = B.MUSTAHIQPRODUCTID)
  , MUSTAHIQ F, CUSTOMER G
  WHERE A.VISITTYPE = 'P'
    AND F.CUSTOMERID = G.CUSTOMERID
    AND A.MUSTAHIQID = F.MUSTAHIQID
    AND (A.VISITDATE >= {BeginDate} AND A.VISITDATE < {EndDate})
  ORDER BY VISITDATE DESC, VISITID

  JOIN count: 3 explicit JOIN (MUSTAHIQPRODUCT+PRODUCT inline subquery, MUSTAHIQ, CUSTOMER)
  + 1 subquery join → total 4 join paths


── DISCRIMINATORS ──────────────────────────────────────────────
  - VISIT.visittype = 'P' → MustahiqProductVisit (Program Penyaluran)
    KRITIS — query list selalu filter ini; tanpa filter ini semua jenis visit ikut
    File sumber: dialogs/Kegiatan/QMonotoringProgramPenyaluran_data.py baris 61 (WHEREClause)
    Comment di kode: "SEMENTARA, HANYA tipe_target = 0 yang disupport"

  - VISITPERSON.visitpersontype = 'A' → VisitPersonAmil (pihak BPZIS/organisasi)
    KRITIS — saat load form: WHERE visitid=X AND VisitPersonType='A'
    File sumber: dialogs/Kegiatan/fMonitoringProgram_data.py baris 18

  - VISITPERSON.visitpersontype = 'S' → VisitPersonMustahiq (pihak mustahiq/yayasan)
    KRITIS — saat load form: WHERE visitid=X AND VisitPersonType='S'
    File sumber: dialogs/Kegiatan/fMonitoringProgram_data.py baris 30

  - VISITITEM.visititemtype = 'P' → VisitPurpose (Tujuan Kunjungan)
    KRITIS — WHERE visitid=X AND VisitItemType='P'
    File sumber: dialogs/Kegiatan/fMonitoringProgram_data.py baris 41

  - VISITITEM.visititemtype = 'R' → VisitResult (Hasil Kunjungan)
    KRITIS — WHERE visitid=X AND VisitItemType='R'
    File sumber: dialogs/Kegiatan/fMonitoringProgram_data.py baris 61

  - VISITITEM.visititemtype = 'F' → VisitFollowUp (Tindak Lanjut)
    KRITIS — WHERE visitid=X AND VisitItemType='F'
    File sumber: dialogs/Kegiatan/fMonitoringProgram_data.py baris 51

  RINGKASAN SEMUA DISCRIMINATOR:
  | Tabel       | Kolom           | Nilai | Arti                        |
  |-------------|-----------------|-------|-----------------------------|
  | VISIT       | visittype       | 'P'   | Program Penyaluran          |
  | VISITPERSON | visitpersontype | 'A'   | Pihak Amil (BPZIS)          |
  | VISITPERSON | visitpersontype | 'S'   | Pihak Mustahiq/Yayasan      |
  | VISITITEM   | visititemtype   | 'P'   | Tujuan Kunjungan (Purpose)  |
  | VISITITEM   | visititemtype   | 'R'   | Hasil Kunjungan (Result)    |
  | VISITITEM   | visititemtype   | 'F'   | Tindak Lanjut (Follow-up)   |


── KOMPLEKSITAS ────────────────────────────────────────────────
LEVEL:    SEDANG
ALASAN:
  - 2 dialog utama (list + form) dengan 4 tab di form detail
  - 6 discriminator fields (KRITIS untuk semua operasi baca/tulis)
  - 4 child entities per record kunjungan (visitperson amil, visitperson mustahiq,
    visititem purpose, visititem result, visititem followup = 5 sub-entities)
  - Pola bulk-replace saat edit (DeleteAllPObjs sebelum re-insert)
  - Tidak ada akuntansi/jurnal — murni data operasional
  - Tidak ada approval workflow (DIST input langsung, tidak via otorisasi)
  - 3-4 JOIN di query list (masih threshold SEDANG, bukan TINGGI)
WORKFLOW: CRUD (list + form detail, tanpa approval)

CATATAN TAMBAHAN:
  - `fEditMonotoringProgram` adalah versi lama/alternatif dari `fMonitoringProgram`
    (lebih sederhana, validasi lebih longgar — tidak cek jumlah pihak BPZIS/mustahiq)
    isf-app HARUS mengikuti validasi versi baru (`fMonitoringProgram_intr.py`)
  - MustahiqProduct bersifat OPTIONAL (MustahiqProductId boleh 0)
  - VisitBeginTime / VisitEndTime ada di DB tapi tersembunyi di semua UI
    → tetap migrasi kolom ini ke schema baru agar tidak ada data loss


── HANDOFF ─────────────────────────────────────────────────────

→ nuwis-seed-gen:
  MENU_KEY: distribution.monitoring.list / LABEL: Monitoring Program Penyaluran
            ROLES: DIST, SPVDIST
  MENU_KEY: distribution.monitoring.create / LABEL: Tambah Monitoring / ROLES: DIST
  MENU_KEY: distribution.monitoring.view   / LABEL: Detail Monitoring / ROLES: DIST, SPVDIST
  MENU_KEY: distribution.monitoring.update / LABEL: Ubah Monitoring  / ROLES: DIST
  MENU_KEY: distribution.monitoring.delete / LABEL: Hapus Monitoring  / ROLES: DIST, SPVDIST

→ nuwis-db-migrator:
  DWH_VIEWS: dwh.v_monitoring_visit (jika dibutuhkan laporan)
    kolom: visitid, visitdate, customername, mustahiqid, productname,
           mustahiqproductname, mustahiqproductid, visitlocation, visitaddress,
           branch_id (tambah jika VISIT punya kolom cabang)
  MIGRATIONS:
    - Pastikan tabel VISIT, VISITPERSON, VISITITEM sudah ada di schema program
    - Konfirmasi apakah ada kolom branchid di VISIT (tidak terlihat di .mdt — perlu cek DB aktual)
    - Index: VISIT(visittype, visitdate), VISITPERSON(visitid, visitpersontype),
             VISITITEM(visitid, visititemtype)

→ nuwis-python-builder:
  ENDPOINTS:
    GET  /api/program/monitoring-visits
         params: begin_date, end_date, page, limit
         WHERE: visittype='P' AND visitdate BETWEEN
         JOIN: MUSTAHIQPRODUCT, PRODUCT, MUSTAHIQ, CUSTOMER

    POST /api/program/monitoring-visits
         body: {mustahiq_id, mustahiq_product_id?, visit_address, visit_location,
                visit_date, visit_begin_time?, visit_end_time?,
                persons_amil: [{name, position}],
                persons_mustahiq: [{name, position}],
                purposes: [{annotation}],
                results: [{annotation}],
                followups: [{annotation}]}

    GET  /api/program/monitoring-visits/{visit_id}
         Fetch single + sub-entities (VISITPERSON + VISITITEM dengan discriminator)

    PUT  /api/program/monitoring-visits/{visit_id}
         body: sama dengan POST
         Logic: delete all VISITPERSON + VISITITEM terkait, re-insert (pola legacy)

    DELETE /api/program/monitoring-visits/{visit_id}
           Cascade delete VISITPERSON + VISITITEM via FK atau manual

  DISCRIMINATORS (wajib ada di service.py):
    VISIT.visittype = 'P'       — selalu difilter di list dan save
    VISITPERSON.visitpersontype = 'A'   — pihak amil
    VISITPERSON.visitpersontype = 'S'   — pihak mustahiq
    VISITITEM.visititemtype = 'P'       — tujuan
    VISITITEM.visititemtype = 'R'       — hasil
    VISITITEM.visititemtype = 'F'       — tindak lanjut

→ nuwis-ui-builder:
  PAGE_TYPE: list (dengan dialog/drawer untuk form detail)
  FIELDS: lihat bagian FORM FIELDS di atas
  FILTERS:
    - begin_date : DateField.vue [Required] — "Periode Tanggal"
    - end_date   : DateField.vue [Required] — "s/d"
    - Default: both = today (ISO date)
    - Tidak auto-load — user klik "Tampilkan Data" dahulu

  FORM DETAIL (Modal/Dialog, bukan halaman terpisah):
    Tab 1 — Data Utama: mustahiq (SearchSelect), program penyaluran (SearchSelect, optional),
             alamat (Input, auto-fill dari mustahiq), tempat pertemuan (Input), tanggal (DateField)
    Tab 2 — Pihak Yang Bertemu: 2 sub-table (BPZIS dan Mustahiq) dengan inline add/delete
    Tab 3 — Tujuan Kunjungan: sub-table dengan textarea per item
    Tab 4 — Hasil Kunjungan: sub-table dengan textarea per item
    Tab 5 — Tindak Lanjut: sub-table dengan textarea per item

  VALIDASI di frontend (sebelum submit):
    1. mustahiq_id wajib dipilih
    2. visit_address tidak kosong
    3. visit_location tidak kosong
    4. visit_date tidak kosong
    5. persons_amil.length >= 1
    6. persons_mustahiq.length >= 1
    7. purposes.length >= 1
    8. results.length >= 1
    9. followups.length >= 1

  TOMBOL AKSI di list (sesuai role):
    - DIST: Tambah (kiri toolbar) | Ubah | Lihat | Hapus (per baris)
    - SPVDIST: Lihat | Hapus (per baris) — tidak ada Tambah/Ubah

==== END MIGRATION_ANALYSIS ====

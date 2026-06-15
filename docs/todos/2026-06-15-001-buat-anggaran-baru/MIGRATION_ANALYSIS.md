==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/core/dialogs/Budget/
PORTAL:  zakat
SCOPE:   Manajemen Anggaran (Budget) — master data + CRUD + import + view
TANGGAL: 2026-06-15

CATATAN KOMPLEKSITAS:
  Modul ini memiliki 9+ dialog saling-linked dengan hierarki ganda
  (BudgetOwner tree + BudgetItem tree), maker-checker otorisasi pada
  setiap operasi tulis, dan OQL multi-level join. Model opus digunakan
  untuk analisis ini sesuai kebijakan eskalasi.

── FITUR LIST ──────────────────────────────────────────────────

  1. Buat Anggaran Baru (Import Excel)
     ROLES:           ADMIN, KEU, SPVKEU
     DIALOG:          dialogs/Budget/fBudgetImport.*
     MENU_KEY_KANDIDAT: keuangan.anggaran.import
     ENTRI_MENU:      Caption='Buat Anggaran Baru', OnClick='NewBudgetClick'
                      File: menus/Transaksi.mnu, handler: menus/Transaksi.py
     OTORISASI:       kode_entri='TRANS036', id_peran='SPVKEU'
     CATATAN:         Menu "Buat Anggaran Baru" TIDAK membuka fBudgetNew.
                      Ia membuka fBudgetImport — form upload Excel batch.
                      fBudgetNew adalah sub-dialog yang dibuka dari dalam
                      fBudgetEditList (Revisi Anggaran) via tombol "Baru".

  2. Revisi Anggaran (Edit Daftar Anggaran)
     ROLES:           ADMIN, KEU, SPVKEU
     DIALOG:          dialogs/Budget/fBudgetEditList.*
     MENU_KEY_KANDIDAT: keuangan.anggaran.revisi
     ENTRI_MENU:      Caption='Revisi Anggaran', OnClick='BudgetRevisionClick'
                      File: menus/Transaksi.mnu, handler: menus/Transaksi.py
     SUB-DIALOG BARU: dialogs/Budget/fBudgetNew.* (kode_entri='TRANS038', SPVKEU)
     SUB-DIALOG EDIT: dialogs/Budget/fBudgetEdit.* (kode_entri='TRANS037', SPVKEU)
     SUB-DIALOG DEL:  DeleteBudget langsung SQL — tidak melalui otorisasi

  3. Inquiry Anggaran (Lihat Daftar + Detail + Histori Transaksi)
     ROLES:           ADMIN, KEU, SPVKEU, ACC, SPVACC
     DIALOG:          dialogs/Budget/fBudgetViewList.*
                      dialogs/Budget/fBudgetViewDetail.*
                      dialogs/Budget/fBudgetViewTransaction.*
     MENU_KEY_KANDIDAT: keuangan.anggaran.inquiry
     ENTRI_MENU:      Caption='Inquiry Anggaran', OnClick='BudgetViewClick'
                      File: menus/Transaksi.mnu, handler: menus/Transaksi.py

  4. Pemilik Anggaran (Master BudgetOwner — CRUD)
     ROLES:           ADMIN, KEU, SPVKEU, ACC, SPVADM
     DIALOG:          dialogs/Parameter/fDaftarBudgetOwner.* (list)
                      dialogs/Parameter/fBudgetOwner.* (CRUD form)
     MENU_KEY_KANDIDAT: parameter.anggaran.pemilik
     ENTRI_MENU:      Caption='Pemilik Anggaran', OnClick='ShowQueryClick'
                      StringTag='parameter/fDaftarBudgetOwner'
                      File: menus/Transaksi.mnu
     OTORISASI:       New=TRANS031, Edit=TRANS032, Delete=TRANS033, id_peran='SPVADM'

  5. Item Anggaran (Master BudgetItem — TANPA OTORISASI)
     ROLES:           AMBIGU — AllowedGroups tidak ditemukan di menu yang terbaca
     DIALOG:          dialogs/Parameter/fDaftarBudgetItem.*
                      dialogs/Parameter/fBudgetItem.*
     MENU_KEY_KANDIDAT: parameter.anggaran.item
     CATATAN:         SimpanData di fBudgetItem_data.py langsung BeginTransaction/Commit,
                      tidak menggunakan otorisasi.

  6. Periode Anggaran (Master BudgetPeriod — TANPA OTORISASI)
     ROLES:           AMBIGU — tidak ditemukan AllowedGroups
     DIALOG:          dialogs/Parameter/fDaftarBudgetPeriod.*
                      dialogs/Parameter/fBudgetPeriodNew.*
     MENU_KEY_KANDIDAT: parameter.anggaran.periode
     CATATAN:         CreateBudgetPeriod langsung commit. Membuat 1 record tahun
                      + 12 record bulan otomatis.

  7. Pilih Kode Anggaran (Lookup — bukan menu mandiri)
     DIALOG:          dialogs/Transaksi/fSelectBudgetCode.*
     MENU_KEY_KANDIDAT: — (hanya lookup, tidak ada halaman mandiri)

── FORM FIELDS (per dialog) ────────────────────────────────────

DIALOG: dialogs/Budget/fBudgetImport (Buat Anggaran Baru via Excel)
FIELDS uipData:
  - BranchCode   : String  [ReadOnly] — dari session SecurityContext
  - Tahun        : Integer [Required] — dropdown, pilih dari BudgetPeriod
FIELDS uipBudgetDetail (grid preview hasil parse Excel):
  - RowNumber    : Integer — nomor urut dari Excel
  - OwnerCode    : String  — kode pemilik anggaran (lookup ke BudgetOwner)
  - OwnerName    : String  — diisi otomatis dari OwnerCode
  - ItemGroup    : String  — nama kelompok kegiatan (BudgetItem level=1)
  - ItemName     : String  — nama rincian kebutuhan (BudgetItem level=2)
  - BudgetCode   : String  — kode anggaran (unique per owner+period+branch)
  - Amount       : Currency — nilai anggaran tahunan
EXCEL FORMAT: header baris 1-11, data mulai row 12
  col1=No, col2=OwnerCode, col3=ItemGroup, col4=ItemName,
  col5=BudgetCode, col6=Amount
SECTIONS:     pInput (filter Tahun + upload), gBudgetDetail (grid)
READ_ONLY:    BranchCode
HIDDEN:       —

---

DIALOG: dialogs/Budget/fBudgetEditList (Revisi Anggaran)
FIELDS uipBudget (header filter):
  - LBudgetOwner.OwnerId   : Integer [Required] — pilih via lookup
  - LBudgetOwner.OwnerName : String  [ReadOnly]
  - LBudgetOwner.OwnerCode : String  [ReadOnly]
  - PeriodID               : Integer [Required] — pilih via fSelectPeriodRevision
  - Bulan                  : Integer [ReadOnly] — dari periode terpilih
  - Tahun                  : Integer [ReadOnly]
FIELDS uipBudgetItem (grid, multi-row):
  - BudgetCode   : String   — kode anggaran
  - ItemGroup    : String   — nama kelompok kegiatan
  - ItemName     : String   — nama rincian kebutuhan
  - Amount       : Currency [Editable] — nilai anggaran (bisa direvisi)
  - OriAmount    : Currency [Hidden]  — nilai asli sebelum revisi (snapshot)
  - AccountCode  : String   [Hidden]  — field lama, tidak dipakai
  - CurrencyCode : String
  - Realization  : Currency [ReadOnly]
  - BudgetId     : Integer  [Hidden]
SECTIONS:     pBudget (filter), grid item, pAction
READ_ONLY:    Bulan, Tahun, Realization, OriAmount
HIDDEN:       AccountCode, AccountName, OriAmount, BudgetId, PeriodID

---

DIALOG: dialogs/Budget/fBudgetNew (sub-dialog: Input Budget Baru)
FIELDS uipBudget:
  - BudgetCode      : String(20)  [Required] — diuppercase, unik per owner+period+branch
  - InputGroupType  : Char(1)    [Hidden]   — 'N'=Kegiatan Baru (default)
  - NewGroupName    : String(200) [Required] — nama kelompok baru
  - LGroupItem      : Link       [Hidden]   — jika pilih kegiatan existing (not used aktif)
  - ItemName        : String(60)  [Required] — nama rincian kebutuhan
  - TotalAmount     : Currency    [Required] — nilai anggaran total
  - Amount1..12     : Currency    [Hidden]   — breakdown bulan (tidak aktif)
  - BudgetId        : Integer     [Hidden]   — PK, diisi post-save
  - PeriodId        : Integer     [Hidden]   — dari parent
  - OwnerId         : Integer     [Hidden]   — dari parent
SECTIONS:     pBudget, pAction (Simpan/Batal)
READ_ONLY:    PeriodId, OwnerId
HIDDEN:       InputGroupType, Amount1-12, BudgetId, PeriodId, OwnerId

---

DIALOG: dialogs/Budget/fBudgetEdit (Edit Budget)
FIELDS uipBudget:
  - BudgetId     : Integer   [Hidden]    — PK yang diedit
  - BudgetCode   : String    [Required]
  - ItemGroup    : String    [Optional]  — nama kelompok (editable)
  - ItemName     : String    [Optional]  — nama rincian (editable)
  - Amount       : Currency  [Required]  — nilai total
  - Amount1..12  : Currency  [Hidden]    — tidak aktif
  - PeriodId     : Integer   [Hidden]
  - OwnerId      : Integer   [Hidden]
SECTIONS:     pBudget, pAction
READ_ONLY:    PeriodId, OwnerId
HIDDEN:       BudgetId, Amount1-12, PeriodId, OwnerId

---

DIALOG: dialogs/Budget/fBudgetViewList (Inquiry Anggaran)
FIELDS uipBudget (filter):
  - LBudgetOwner.OwnerId/OwnerName/OwnerCode : filter owner [Required]
  - PeriodID   : Integer [Required]
  - Bulan/Tahun : ReadOnly
  - BranchCode/BranchName : ReadOnly (dari session)
FIELDS uipBudgetItem (grid read-only):
  - BudgetCode, ItemGroup, ItemName
  - Amount, Realization, SalvageValue (= Amount - Realization, computed)
  - BudgetId [Hidden]
FIELDS uipInfo (footer totals):
  - TotalBudget, TotalRealization, TotalSalvage
SECTIONS:     filter panel, grid, footer summary
READ_ONLY:    Semua (inquiry/view only), ExportExcel tersedia

---

DIALOG: dialogs/Budget/fBudgetViewDetail (Detail satu Budget)
FIELDS uipBudget:
  - BudgetCode, ItemGroup, ItemName, TotalAmount [ReadOnly]
  - Amount1..12 : Currency [ReadOnly] — breakdown bulanan (jika ada)
  - OwnerId, PeriodId [Hidden]
READ_ONLY:    Semua

---

DIALOG: dialogs/Budget/fBudgetViewTransaction (Histori Transaksi Budget)
FIELDS uipBudget (header info):
  - OwnerName, Tahun, BudgetCode, ItemGroup, ItemName [ReadOnly]
  - BudgetId [Hidden]
  - BeginDate, EndDate : Date [Required]
OUTPUT dsHistori:
  - TransactionItemId, TransactionDate, TransactionDateStr
  - TransactionCode, TransactionType, MutationType
  - Amount (jika BudgetTransType='A'), ReturnAmount (jika bukan 'A')
  - ReferenceNo, Description, Inputer, NoTransaksi

---

DIALOG: dialogs/Transaksi/fSelectBudgetCode (Lookup kode anggaran)
FIELDS uipFilter:
  - ActualDate      : Date    — menentukan tahun periode
  - FilterCategory  : Char(1) — '0'=semua, '1'=kode, '2'=kelompok, '3'=rincian
  - FilterText      : String  — teks pencarian
FIELDS uipBudget (hasil):
  - BudgetId, BudgetCode, BudgetOwner, ItemGroup, Description

── UI FLOW ─────────────────────────────────────────────────────

=== fBudgetImport (Buat Anggaran Baru) ===

ON OPEN:
  - CallServerMethod('GetRefData') → load dropdown Tahun dari budgetperiod
    WHERE parentperiodid IS NULL
  - BranchCode diisi dari session

ON BROWSE FILE:
  - User pilih .xls → upload via StreamWrapper
  - FormSetDataEx membaca Excel row 12+:
    Validasi OwnerCode → GetObjectByNames('BudgetOwner', {OwnerCode})
    Jika tidak valid → Exception "Kode Pemilik tidak valid"
  - Preview tampil di grid uipBudgetDetail

ON SAVE (OkClick):
  - Validasi Tahun wajib dipilih
  - Validasi grid tidak kosong
  - CallServerMethod('save') → otorisasi storeDataPacket (TRANS036, SPVKEU)
  - Pesan: "Data Berhasil Disimpan. Silahkan diotorisasi"

=== fBudgetEditList (Revisi Anggaran) ===

ON OPEN:
  - CallServerMethod('GetPeriodYear') → load dropdown cbPeriod
    SELECT * FROM budgetperiod WHERE parentperiodid IS NULL

ON PILIH OWNER:
  - Lookup LBudgetOwner → filter Is_Detail='T' (hanya leaf owner)

ON PILIH PERIODE (PilihPeriodeClick):
  - Buka fSelectPeriodRevision dengan OwnerId
  - Query: SELECT budgetperiod WHERE EXISTS (SELECT 1 FROM budget
    WHERE periodid=budgetperiod.periodid AND ownerid=:OwnerId)
    AND parentperiodid IS NOT NULL
  - Setelah pilih → SetDataWithParameters(PeriodId, OwnerId)

ON LOAD DATA (FormSetDataEx):
  - OQL: SELECT FROM BudgetYear WHERE OwnerId=:o AND PeriodId=:p AND BranchCode=:b
         JOIN LBudgetItem.LParent.BudgetItemDescription (ItemGroup)
         JOIN LBudgetItem.BudgetItemDescription (ItemDetail)
    ORDER BY ASC ItemId, ASC BudgetCode, ASC PeriodId

ON NEW → buka fBudgetNew (TRANS038, SPVKEU)
ON EDIT → buka fBudgetEdit (TRANS037, SPVKEU)
ON DELETE → DeleteBudget (LANGSUNG SQL, tanpa otorisasi)
ON SAVE REVISI → SimpanData: loop, jika Amount != OriAmount → CreateRevision
  (LANGSUNG COMMIT, tanpa otorisasi)

=== fBudgetNew (sub-form) ===

ON OPEN:
  - GetNewData(OwnerId, PeriodId) dari parent
  - Set InputGroupType='N'

ON SAVE (SaveClick → save() → TRANS038):
  - Cek duplikat: SELECT COUNT FROM budget WHERE periodid=:p AND ownerid=:o
    AND branchcode=:b AND budgettype='Y' AND LOWER(budgetcode)=LOWER(:bc)
  - Jika ada → Exception "Kode Budget telah terdaftar"
  - Jika lolos → otorisasi storeDataPacket
  ON APPROVE (authorize):
    1. CreatePObject('BudgetItem') level=1, is_detail='F', SetHierarchy()
    2. CreatePObject('BudgetItem') level=2, is_detail='T', SetHierarchy()
    3. CreatePObject('BudgetYear') → INSERT budget budgettype='Y'

── SAVE LOGIC ──────────────────────────────────────────────────

ENTRY (Import): dialogs/Budget/fBudgetImport_data.py → save() → otorisasi TRANS036
ENTRY (New):    dialogs/Budget/fBudgetNew_data.py → save() → otorisasi TRANS038
ENTRY (Edit):   dialogs/Budget/fBudgetEdit_data.py → save() → otorisasi TRANS037
ENTRY (Revisi): dialogs/Budget/fBudgetEditList_data.py → SimpanData() [LANGSUNG]
ENTRY (Delete): dialogs/Budget/fBudgetEditList_data.py → DeleteBudget() [LANGSUNG]

ALUR CREATE BUDGET (authorize setelah TRANS036/038 disetujui SPVKEU):
  1. Ambil YearPeriodId, OwnerId, BranchCode
  2. Cek duplikat BudgetCode: SELECT COUNT FROM budget WHERE
     budgettype='Y' AND periodid=:p AND ownerid=:o AND branchcode=:b
     AND LOWER(budgetcode)=LOWER(:bc) → jika >0 → Exception
  3. Jika InputGroupType='N' (atau import: ItemGroup berubah):
     CreatePObject('BudgetItem') → INSERT budgetitem
       {is_detail='F', level=1, budgetitemdescription=NewGroupName/ItemGroup, ownerid}
     SetHierarchy() → INSERT budgetitemhierarchy (self-ref dengan level=0)
  4. CreatePObject('BudgetItem') → INSERT budgetitem
       {is_detail='T', level=2, budgetitemdescription=ItemName,
        parentitemid=GroupItemId, ownerid, branchcode}
     SetHierarchy() → INSERT budgetitemhierarchy (parent→child dengan level diff)
  5. CreatePObject('BudgetYear') → INSERT budget
       {budgettype='Y', periodid, ownerid, budgetcode, itemid=oItemDetail.ItemId,
        itemcode='', itemname=ItemName, currencycode='IDR', realization=0.0,
        branchcode, isdetail='F', amount=TotalAmount}
  6. Commit

ALUR EDIT BUDGET (authorize setelah TRANS037 disetujui SPVKEU):
  1. GetObject('BudgetYear', YearBudgetId) → UPDATE budget set budgetcode=:bc
  2. GetObject('BudgetItem', oBudgetYear.ItemId) → UPDATE budgetitemdescription=:ItemName
  3. oBudgetItem.LParent.BudgetItemDescription = :ItemGroup (UPDATE parent budgetitem)
  4. oBudgetYear.Amount = :Amount → UPDATE budget set amount=:a
  5. Commit

ALUR REVISI AMOUNT (langsung, tanpa otorisasi):
  1. Loop uipBudgetItem: jika Amount != OriAmount:
     GetObject('Budget', BudgetId)
     CreateRevision(Amount):
       CreatePObject('BudgetRevision') → INSERT budgetrevision
         {budgetid, amount=Amount, userid=SecurityContext.InitUser}
       UPDATE budget SET revisionid = oRevision.RevisionId
  2. Commit

ALUR DELETE BUDGET (langsung SQL):
  DELETE FROM budget WHERE parentbudgetid = :BudgetId
  DELETE FROM budget WHERE budgetid = :BudgetId
  Commit

── SCHEMA DB ───────────────────────────────────────────────────

ENTITIES:

  1. Budget → tabel: transaction.budget
     Kolom:
       budgetid        INTEGER PK
       periodid        INTEGER FK→budgetperiod.periodid
       ownerid         INTEGER FK→budgetowner.ownerid
       itemid          INTEGER FK→budgetitem.itemid (WeakLink)
       budgetcode      VARCHAR(20)
       itemcode        VARCHAR(30) — field lama, umumnya ''
       itemname        VARCHAR(60) — field lama
       currencycode    VARCHAR(5)  — 'IDR'
       amount          DOUBLE
       realization     DOUBLE
       branchcode      VARCHAR(5)
       isdetail        VARCHAR(1)  — 'F'=header, 'T'=detail
       budgettype      VARCHAR(1)  — 'Y'=tahun (discriminator BudgetYear)
       parentbudgetid  INTEGER FK→budget.budgetid
       revisionid      INTEGER FK→budgetrevision.revisionid
       level           INTEGER

  2. BudgetItem → tabel: transaction.budgetitem
     Kolom:
       itemid                INTEGER PK
       budgetitemcode        VARCHAR(20)
       budgetitemdescription VARCHAR(250)
       budgetitemname        VARCHAR(200)
       level                 INTEGER — 1=kelompok, 2=rincian
       is_detail             VARCHAR(1) — 'F'=kelompok, 'T'=rincian
       parentitemid          INTEGER FK→budgetitem.itemid
       ownerid               INTEGER FK→budgetowner.ownerid
       branchcode            VARCHAR(5)

  3. BudgetItemHierarchy → tabel: transaction.budgetitemhierarchy
     Kolom: hierarchyid, parentitemid, childitemid, level

  4. BudgetOwner → tabel: transaction.budgetowner
     Kolom: ownerid, ownercode VARCHAR(10), ownername VARCHAR(100),
            level, is_detail VARCHAR(1), parentownerid, status VARCHAR(1)

  5. BudgetOwnerHierarchy → tabel: transaction.budgetownerhierarchy
     Kolom: hierarchyid, parentownerid, childownerid, level

  6. BudgetPeriod → tabel: transaction.budgetperiod
     Kolom: periodid, periodvalue INTEGER (tahun atau bulan 1-12),
            isopen VARCHAR(1), parentperiodid INTEGER (NULL=tahun root)

  7. BudgetRevision → tabel: transaction.budgetrevision
     Kolom: revisionid, budgetid FK→budget, amount DOUBLE,
            userid VARCHAR(20), lastamount DOUBLE

  8. BudgetTransaction → tabel: transaction.budgettransaction
     Kolom: transactionitemid INTEGER PK FK→transactionitem,
            budgetid INTEGER FK→budget, budgettranstype VARCHAR(1)

RELASI:
  - budget.periodid → budgetperiod.periodid
  - budget.ownerid → budgetowner.ownerid
  - budget.itemid → budgetitem.itemid (WeakLink)
  - budget.parentbudgetid → budget.budgetid (self-ref)
  - budget.revisionid → budgetrevision.revisionid
  - budgetitem.parentitemid → budgetitem.itemid (self-ref, max 2 level)
  - budgetitem.ownerid → budgetowner.ownerid
  - budgetowner.parentownerid → budgetowner.ownerid (self-ref tree)
  - budgetperiod.parentperiodid → budgetperiod.periodid (self-ref tree)
  - budgetrevision.budgetid → budget.budgetid
  - budgettransaction.transactionitemid → transactionitem.transactionitemid
  - budgettransaction.budgetid → budget.budgetid

── DISCRIMINATORS ──────────────────────────────────────────────

  - budget.budgettype = 'Y'
    → BudgetYear (record tahun, IsDetail='F')
    → KRITIS: SEMUA query budget harus filter budgettype='Y'
      untuk mendapatkan record BudgetYear yang valid

  - budget.isdetail = 'F'
    → Header/induk (BudgetYear, atau induk bulan — tidak aktif saat ini)
    → isdetail = 'T' → detail per bulan (kode pembuatan di-comment out)

  - budgetitem.is_detail = 'F' AND level = 1
    → Kelompok Kegiatan (induk)
    → budgetitem.is_detail = 'T' AND level = 2 → Rincian Kebutuhan (leaf)

  - budgetowner.is_detail = 'T'
    → BudgetOwner yang bisa dipilih pada form anggaran (leaf owner)
    → Lookup pada fBudgetEditList/fBudgetViewList filter Is_Detail='T'

  - budgetperiod.parentperiodid IS NULL
    → Record adalah tahun anggaran (root)
    → parentperiodid IS NOT NULL → record bulan (anak tahun)

  - budgettransaction.budgettranstype = 'A'
    → Realisasi anggaran (penggunaan)
    → budgettranstype != 'A' → pengembalian/retur

── KOMPLEKSITAS ────────────────────────────────────────────────

LEVEL:    TINGGI
ALASAN:   9+ dialog saling-linked; hierarki ganda BudgetOwner + BudgetItem;
          maker-checker otorisasi (TRANS036/037/038) + inkonsistensi (revisi
          dan delete bypass otorisasi); BudgetYear subclass via discriminator
          budgettype='Y'; OQL multi-hop join (BudgetYear→LBudgetItem→LParent);
          import Excel batch (pyFlexcel); integrasi ke TransactionItem melalui
          BudgetTransaction; 5+ JOIN path di fSelectBudgetCode OQL.
WORKFLOW:  Approval (Maker-Checker) + CRUD + Laporan (export Excel)

── HANDOFF ─────────────────────────────────────────────────────

→ nuwis-seed-gen:
  MENU_KEY: keuangan.anggaran.import   / LABEL: Buat Anggaran Baru / ROLES: ADMIN,KEU,SPVKEU
  MENU_KEY: keuangan.anggaran.revisi   / LABEL: Revisi Anggaran    / ROLES: ADMIN,KEU,SPVKEU
  MENU_KEY: keuangan.anggaran.inquiry  / LABEL: Inquiry Anggaran   / ROLES: ADMIN,KEU,SPVKEU,ACC,SPVACC
  MENU_KEY: parameter.anggaran.pemilik / LABEL: Pemilik Anggaran   / ROLES: ADMIN,KEU,SPVKEU,ACC,SPVADM
  MENU_KEY: parameter.anggaran.item    / LABEL: Item Anggaran      / ROLES: AMBIGU — konfirmasi
  MENU_KEY: parameter.anggaran.periode / LABEL: Periode Anggaran   / ROLES: AMBIGU — konfirmasi

→ nuwis-db-migrator:
  DWH_VIEWS:
    dwh.v_budget_summary — kolom:
      budget_id, budget_code, owner_id, owner_name, owner_code,
      period_id, period_year, branch_code,
      item_group (budgetitem level=1), item_name (budgetitem level=2),
      amount, realization, salvage_value
      FILTER WAJIB: budget.budgettype='Y'

    dwh.v_budget_transaction — kolom:
      budget_id, budget_code, transaction_item_id, actual_date,
      transaction_code, transaction_no, amount, budget_trans_type,
      trans_type_label, mutation_type, inputer, reference_no

  MIGRATIONS:
    Pastikan tabel-tabel berikut ada di schema transaction:
    budget, budgetitem, budgetitemhierarchy,
    budgetowner, budgetownerhierarchy,
    budgetperiod, budgetrevision, budgettransaction

→ nuwis-python-builder:
  ENDPOINTS:
    GET  /api/budget/owners              — daftar BudgetOwner is_detail='T'
    GET  /api/budget/periods             — tahun anggaran (parentperiodid IS NULL)
    GET  /api/budget/periods/{owner_id}  — periode yang ada budget untuk owner ini
    GET  /api/budget/items               — BudgetYear per owner+period+branch (budgettype='Y')
    POST /api/budget/                    — buat anggaran baru → otorisasi TRANS038
    PUT  /api/budget/{budget_id}         — edit anggaran → otorisasi TRANS037
    DELETE /api/budget/{budget_id}       — hapus anggaran (langsung, tanpa otorisasi)
    POST /api/budget/revise              — revisi amount batch (langsung, tanpa otorisasi)
    POST /api/budget/import              — import Excel → otorisasi TRANS036
    GET  /api/budget/{budget_id}/transactions — histori BudgetTransaction
    GET  /api/budget/select              — lookup kode anggaran (query aktif berdasar tanggal)
    GET  /api/budget/budget-owners       — CRUD master BudgetOwner
    POST /api/budget/budget-owners       — TRANS031, SPVADM
    PUT  /api/budget/budget-owners/{id}  — TRANS032, SPVADM
    DELETE /api/budget/budget-owners/{id}— TRANS033, SPVADM
    POST /api/budget/budget-periods      — buat tahun + 12 bulan otomatis
    GET/POST/PUT /api/budget/budget-items — master BudgetItem (tanpa otorisasi)

  DISCRIMINATORS (copy ke service.py, JANGAN hilangkan):
    budget.budget_type = 'Y'          → BudgetYear (filter wajib)
    budget.is_detail = 'F'            → header record
    budgetitem.is_detail = 'F', level=1 → kelompok kegiatan
    budgetitem.is_detail = 'T', level=2 → rincian kebutuhan
    budgetowner.is_detail = 'T'       → leaf owner, bisa dipilih di form
    budgetperiod.parent_period_id IS NULL → tahun (root)
    budgettransaction.budget_trans_type = 'A' → realisasi
    budgettransaction.budget_trans_type != 'A' → pengembalian

→ nuwis-ui-builder:
  PAGE_TYPE:
    keuangan.anggaran.import  → form (stepper: pilih tahun + upload Excel + preview + submit)
    keuangan.anggaran.revisi  → list + inline edit + Modal baru/edit
    keuangan.anggaran.inquiry → laporan (filter required, ExportExcel)
    parameter.anggaran.pemilik → list + CRUD Modal

  FIELDS Buat Anggaran Baru (Import):
    Filter: Tahun (dropdown GET /api/budget/periods)
    Upload: file .xlsx (drag-drop atau browse)
    Preview Grid (read-only):
      No | OwnerCode | Kelompok Kegiatan | Rincian Kebutuhan | Kode Budget | Nilai
    Action: Simpan → otorisasi (status PENDING)

  FIELDS Revisi Anggaran:
    Filter: Pemilik Anggaran (SearchSelect.vue) + Periode (dropdown)
    Grid (editable Amount saja):
      Kode Budget | Kelompok | Rincian | Anggaran (editable) | Realisasi | Sisa
    Tombol: Tambah (Modal) | Edit (Modal) | Hapus | Simpan Revisi

  FIELDS Inquiry Anggaran:
    Filter (wajib): Pemilik Anggaran (SearchSelect.vue) + Tahun Anggaran
    Grid (read-only): Kode Budget | Kelompok | Rincian | Anggaran | Realisasi | Sisa
    Footer: Total Anggaran | Total Realisasi | Total Sisa
    Export Excel

  FILTERS:
    Inquiry: owner_id (required), period_id (required), branch_code (dari session)
    Select Budget Code: actual_date (required), filter_category, filter_text
    Histori Transaksi: begin_date, end_date

── CATATAN TAMBAHAN ─────────────────────────────────────────────

1. INKONSISTENSI OTORISASI (perlu ADR di isf-app):
   CREATE (fBudgetNew/fBudgetImport) → melalui otorisasi (TRANS036/038)
   EDIT (fBudgetEdit) → melalui otorisasi (TRANS037)
   REVISI AMOUNT (fBudgetEditList bSimpanClick) → LANGSUNG COMMIT, tanpa otorisasi
   DELETE (fBudgetEditList DeleteClick) → LANGSUNG SQL DELETE, tanpa otorisasi
   Master BudgetOwner → melalui otorisasi (TRANS031/032/033, SPVADM)
   Master BudgetItem → LANGSUNG COMMIT, tanpa otorisasi
   Master BudgetPeriod → LANGSUNG COMMIT, tanpa otorisasi

2. BUG COPY-PASTE di fBudgetImport_data.py baris 241:
   recOtor.nama_tabel = 'BranchCashAccount'   ← SALAH
   Seharusnya: recOtor.nama_tabel = 'Budget'
   Implementasi isf-app harus diperbaiki.

3. AMOUNT1-12 TIDAK AKTIF:
   Field breakdown per bulan ada di schema tapi kode INSERT-nya di-comment out.
   Implementasi isf-app: cukup Amount total. Jangan buat breakdown bulanan
   kecuali ada kebutuhan eksplisit.

4. OTORISASI ENTRY CODES:
   TRANS031 = Registrasi pemilik anggaran (New BudgetOwner)  — SPVADM
   TRANS032 = Edit pemilik anggaran (Edit BudgetOwner)       — SPVADM
   TRANS033 = Hapus pemilik anggaran (Delete BudgetOwner)    — SPVADM
   TRANS036 = Buat Anggaran Baru batch/import (fBudgetImport)— SPVKEU
   TRANS037 = Edit Anggaran (fBudgetEdit)                    — SPVKEU
   TRANS038 = Tambah Anggaran single entry (fBudgetNew)      — SPVKEU
   TRANS034, TRANS035 tidak ditemukan di modul ini.

5. MENU ENTRY KRITIS:
   "Buat Anggaran Baru" (menu item) → membuka fBudgetImport (upload Excel)
   fBudgetNew hanya sub-dialog dari "Revisi Anggaran" (fBudgetEditList)
   Ini bukan kekeliruan — ini desain intentional di legacy.

6. DEFAULT CURRENCY:
   Legacy: config.SysVarIntf.GetStringSysVar('OPTION','DefaultCurrency')
   Implementasi isf-app: hardcode 'IDR' atau ambil dari config tabel.

==== END MIGRATION_ANALYSIS ====

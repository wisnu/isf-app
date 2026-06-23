==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/program/
PORTAL:  zakat
SCOPE:   Laporan Penyaluran (Laporan domain)
TANGGAL: 2026-06-22

── FITUR LIST ──────────────────────────────────────────────────
  1. Laporan Proposal Masuk
     ROLES:             DIST, SPVDIST, QAC
     DIALOG:            dialogs/Laporan/QLapProposal.*
                        dialogs/Laporan/fLapProposal.*
     CATATAN:           Ada DUA form untuk laporan ini. QLapProposal
                        (lebih baru, memiliki _data.py + FormSetDataEx)
                        adalah versi utama yang aktif di menu. fLapProposal
                        adalah versi lama (tidak ada FormSetDataEx, query
                        lebih sederhana langsung ke proposal WHERE
                        proposalstatus='B'). QAC adalah kode AMBIGU — tidak
                        ada di mapping role isf-app. Laporkan ke
                        nuwis-architect.
     MENU_KEY_KANDIDAT: distribution.report.proposal-incoming

  2. Laporan Daftar Mustahiq
     ROLES:             DIST, SPVDIST, QAC
     DIALOG:            dialogs/Laporan/QLapMustahiq.*
     MENU_KEY_KANDIDAT: distribution.report.mustahiq-list

  3. Laporan Program Penyaluran Rutin
     ROLES:             DIST, SPVDIST, QAC
     DIALOG:            dialogs/Laporan/fReportRealizationRegular.*
     MENU_KEY_KANDIDAT: distribution.report.realization-regular

  4. Laporan Program Penyaluran Non Rutin
     ROLES:             DIST, SPVDIST, QAC
     DIALOG:            dialogs/Laporan/fReportRealizationNonRegular.*
     MENU_KEY_KANDIDAT: distribution.report.realization-non-regular

  5. Laporan Piutang Realisasi Penyaluran
     ROLES:             DIST, SPVDIST, QAC
     DIALOG:            dialogs/Laporan/fReportRealizationReceivable.*
     MENU_KEY_KANDIDAT: distribution.report.realization-receivable

  6. Laporan Pengembalian Realisasi
     ROLES:             DIST, SPVDIST, QAC
     DIALOG:            dialogs/Laporan/fReportRealizationReturn.*
     MENU_KEY_KANDIDAT: distribution.report.realization-return

  7. Laporan Penyaluran Per Mustahiq
     ROLES:             AMBIGU — tidak ada AllowedGroups di .mnu (OnClick tanpa AllowedGroups)
                        Kemungkinan bisa diakses semua roles atau ada restriksi tersembunyi.
                        Laporkan ke nuwis-architect.
     DIALOG:            dialogs/Laporan/fReportRealizationByMustahiq.*
     MENU_KEY_KANDIDAT: distribution.report.realization-by-mustahiq

── FORM FIELDS (per dialog) ────────────────────────────────────

DIALOG: dialogs/Laporan/QLapProposal.*
FIELDS (filter):
  - tglproposal_a  : timestamp [Optional] — Tanggal Proposal (awal)
  - tglproposal_b  : timestamp [Optional] — Tanggal Proposal (akhir, s/d)
  - LMustahiq.MustahiqId             : INTEGER     [Optional] — FK Mustahiq (hidden, diisi via lookup)
  - LMustahiq.LCustomer.CustomerName : VARCHAR(50) [Optional] — Nama Mustahiq (label lookup)
  - LProductGroup.ProductGroupId     : INTEGER     [Optional] — FK Jenis Program (hidden)
  - LProductGroup.ProductGroupName   : VARCHAR(50) [Optional] — Nama Jenis Program
  - Incolumn  : INTEGER     [Hidden] — kolom filter internal
  - keywords  : VARCHAR(30) [Hidden] — keyword filter internal
SECTIONS:     satu panel (pFilter) + query grid (QryMustahik)
READ_ONLY:    LMustahiq.LCustomer.AddressStreet, AddressKelurahan, AddressKecamatan
              (auto-fill dari lookup mustahiq)
HIDDEN:       Incolumn, keywords, LMustahiq.MustahiqId (nilai FK),
              LProductGroup.ProductGroupId (nilai FK)
KOLOM GRID:   Nama Mustahiq, Jenis Program, No Proposal, Tanggal Proposal,
              Deskripsi, Nominal, Diterima Oleh, Tgl_Diterima, Referensi Oleh
SUMBER:       QLapProposal.svr baris 11-62, QLapProposal.dfr baris 41-258

─────
DIALOG: dialogs/Laporan/fLapProposal.*  (versi lama — less featured)
FIELDS (filter):
  - tgla : timestamp [Optional] — Tanggal Proposal (awal)
  - tglb : timestamp [Optional] — Tanggal Proposal (akhir)
  - LMustahiq.LCustomer.CustomerName : VARCHAR(50) [Optional] — Nama Mustahiq (lookup)
SECTIONS:     panel1 (filter), panel2 (action buttons)
HIDDEN:       LMustahiq.MustahiqId (FK)
SUMBER:       fLapProposal.svr baris 11-42, fLapProposal.dfr baris 39-134

─────
DIALOG: dialogs/Laporan/QLapMustahiq.*
FIELDS (filter):
  - IsAllMustahiqType : VARCHAR(2) [Optional, checkbox] — Seluruh Golongan Mustahiq (T/F)
  - MustahiqType      : VARCHAR(2) [Optional, enum]     — Golongan: MP=Individu, MC=Lembaga
  - IsAllProgram      : VARCHAR(1) [Optional, checkbox] — Seluruh Program (T/F)
  - LProgram.ProductId   : INTEGER  [Optional, hidden]  — FK Program
  - LProgram.ProductName : VARCHAR(30) [Optional]       — Nama Program
  - IsAllProgramDate  : VARCHAR(1) [Optional, checkbox] — Seluruh Tgl Rencana Program (T/F)
  - ProgramBeginDate  : timestamp [Optional]            — Tgl Rencana Program (awal)
  - ProgramEndDate    : timestamp [Optional]            — Tgl Rencana Program (akhir)
SECTIONS:     satu panel (pFilter)
READ_ONLY:    tidak ada
HIDDEN:       LProgram.ProductId (FK diisi via lookup)
DEFAULT SAAT OPEN: IsAllProgram='T', IsAllMustahiqType='T', IsAllProgramDate='T'
                   (semua checkbox checked) — dari QLapMustahiq_intr.py Show() baris 11-13
SUMBER:       QLapMustahiq.svr baris 11-55, QLapMustahiq.dfr baris 35-210

─────
DIALOG: dialogs/Laporan/fReportRealizationRegular.*
FIELDS (filter):
  - BeginDate  : timestamp [Required via default] — Periode Tanggal (awal)
  - EndDate    : timestamp [Required via default] — Periode Tanggal (akhir, s/d)
  - LMustahiq  : Mustahiq lookup [Hidden] — tersedia di .svr tapi Hidden=true di .dfr
  - ReportType : VARCHAR(20) [Hidden] — nilai hardcode '1' saat Show()
                 enum: 1=Detil Per Program, 2=Rekap Per Grup Program
DEFAULT SAAT OPEN: BeginDate = EndDate = today (config.Now())
                   ReportType = '1' — dari fReportRealizationRegular_intr.py Show() baris 7
SUMBER:       fReportRealizationRegular.svr baris 11-47,
              fReportRealizationRegular.dfr baris 39-150

─────
DIALOG: dialogs/Laporan/fReportRealizationNonRegular.*
FIELDS (filter):
  - BeginDate   : timestamp [Optional] — Periode Tanggal (awal)
  - EndDate     : timestamp [Optional] — Periode Tanggal (akhir)
  - BeginAmount : DOUBLE    [Required] — Nominal penyaluran (awal), default 0
  - EndAmount   : DOUBLE    [Required] — Nominal penyaluran (akhir), default 3000000
  - LMustahiq   : Mustahiq lookup [Hidden]
  - ReportType  : VARCHAR(20) [Hidden]
VALIDASI CLIENT: BeginAmount != None, EndAmount != None, BeginAmount <= EndAmount
                 (fReportRealizationNonRegular_intr.py IsRequiredComplete() baris 17-28)
DEFAULT SAAT OPEN: BeginDate = EndDate = today, BeginAmount=0, EndAmount=3000000
                   (fReportRealizationNonRegular_data.py FormSetDataEx baris 13-14)
SUMBER:       fReportRealizationNonRegular.svr baris 11-55,
              fReportRealizationNonRegular.dfr baris 39-182

─────
DIALOG: dialogs/Laporan/fReportRealizationReceivable.*
FIELDS (filter):
  - BeginDate  : timestamp [Optional] — Periode Tanggal (awal)
  - EndDate    : timestamp [Optional] — Periode Tanggal (akhir)
  - LMustahiq  : Mustahiq lookup [Hidden]
  - ReportType : VARCHAR(20) [Hidden]
DEFAULT SAAT OPEN: BeginDate = EndDate = today
CATATAN:      EndDate di query di-increment +1 hari (fReportRealizationReceivable_data.py
              baris 34: rec.EndDate + 1) untuk inklusif — BERBEDA dari laporan lain yang
              pakai < EndDate eksklusif. Implementasi baru: pakai EndDate <= date_to
              atau date_to + 1 interval day.
SUMBER:       fReportRealizationReceivable.svr baris 11-47,
              fReportRealizationReceivable.dfr baris 39-150

─────
DIALOG: dialogs/Laporan/fReportRealizationReturn.*
FIELDS (filter):
  - BeginDate  : timestamp [Optional] — Periode Tanggal (awal)
  - EndDate    : timestamp [Optional] — Periode Tanggal (akhir)
  - LMustahiq  : Mustahiq lookup [Hidden]
  - ReportType : VARCHAR(20) [Hidden]
DEFAULT SAAT OPEN: BeginDate = EndDate = today
SUMBER:       fReportRealizationReturn.svr baris 11-47,
              fReportRealizationReturn.dfr baris 39-150

─────
DIALOG: dialogs/Laporan/fReportRealizationByMustahiq.*
FIELDS (filter):
  - BeginDate   : timestamp [Optional] — Periode Tanggal (awal)
  - EndDate     : timestamp [Optional] — Periode Tanggal (akhir)
  - BeginAmount : DOUBLE    [Hidden — tersedia di .svr tapi Hidden=true di .dfr]
  - EndAmount   : DOUBLE    [Hidden]
  - LMustahiq   : Mustahiq lookup [Hidden]
  - ReportType  : VARCHAR(20) [Hidden]
DEFAULT SAAT OPEN: BeginDate = EndDate = today, BeginAmount=0, EndAmount=3000000
                   (fReportRealizationByMustahiq_data.py FormSetDataEx baris 12-14)
CATATAN:      BeginAmount/EndAmount ada di .svr dan kode backend, tapi
              Hidden=true di .dfr — filter nominal tidak ditampilkan ke user
              meskipun tetap dikirim ke server. Range nominal TIDAK divalidasi
              di client. Implementasi baru: tidak perlu expose filter ini ke UI.
SUMBER:       fReportRealizationByMustahiq.svr baris 11-55,
              fReportRealizationByMustahiq.dfr baris 39-166

── UI FLOW ─────────────────────────────────────────────────────

=== QLapProposal (Laporan Proposal Masuk — versi utama) ===
ON OPEN:
  - FormSetDataEx mengisi: tglproposal_a = awal bulan ini, tglproposal_b = hari ini
    (QLapProposal_data.py FormSetDataEx baris 6-13)
  - Grid langsung menampilkan proposal (proposalstatus is not null) sesuai range tanggal
ON TAMPILKAN (FilterClick / tombol "Tampilkan Data"):
  - Membangun OQL query ke tabel Proposal dengan filter dinamis:
    proposaldate, mustahiqid, ProductGroupId
  - DisplayList() → QryMustahik.DisplayData()
    (QLapProposal_intr.py DisplayList() baris 59-114)
ON EXPORT (tombol "Export ke Excel"):
  - CommitBuffer() → GetDataPacket() → CallServerMethod('GenerateFile', ph)
  - Server mengeksekusi GenerateFile di QLapProposal_data.py
  - Output: file Excel 'LaporanProposal.xls' dikirim sebagai stream

=== QLapMustahiq (Laporan Daftar Mustahiq) ===
ON OPEN:
  - Tidak ada FormSetDataEx — default diset di Show() handler:
    IsAllProgram='T', IsAllMustahiqType='T', IsAllProgramDate='T'
    (QLapMustahiq_intr.py Show() baris 10-15)
  - Kontrol MustahiqType, LProgram, ProgramBeginDate, ProgramEndDate
    di-disable saat checkbox 'Seluruh' = checked
ON EXPORT (tombol "Export Excel"):
  - Validasi client: IsFilterValid() — cek apakah filter konsisten dengan checkbox
    (QLapMustahiq_intr.py IsFilterValid() baris 38-63)
  - CommitBuffer() → GetDataPacket() → CallServerMethod('GenerateFile', ph)
  - Output: file Excel 'DaftarMustahiq.xls' dikirim sebagai stream

=== fReportRealizationRegular/NonRegular/ByMustahiq/Receivable/Return ===
ON OPEN:
  - FormSetDataEx mengisi: BeginDate = EndDate = today (integer timestamp)
  - Khusus NonRegular dan ByMustahiq: BeginAmount=0, EndAmount=3000000 juga diisi
ON CETAK (tombol "Cetak"):
  - CommitBuffer() → GetDataPacket() → CallServerMethod('GenerateFile', ph)
  - Validasi NonRegular: cek BeginAmount, EndAmount tidak null dan valid range
  - Output: file Excel dikirim sebagai stream

── SAVE LOGIC ──────────────────────────────────────────────────
Semua dialog laporan ini adalah READ-ONLY — tidak ada SimpanData.
Logic utama adalah QUERY LOGIC di dalam fungsi GenerateFile di _data.py masing-masing.

=== QLapProposal — GenerateFile (QLapProposal_data.py baris 14-153) ===
QUERY UTAMA (5 tabel, 1 subquery dengan RANK):
  Tabel: proposal (p), productgroup (pg), mustahiq (m), customer (c)
  Subquery LEFT JOIN: program.realizationdetail (rd), program.realization (r),
    program.realizationmemo (rm), program.mustahiqproduct (mp),
    transaction.financialaccount (f)
  Window function: RANK() OVER (PARTITION BY rd.mustahiqproductid ORDER BY rd.realizationamount DESC)
    → ambil realization terbesar per mustahiqproduct (data_rank=1)
  JOIN COUNT: 5 tabel eksplisit + subquery 5 join internal = TOTAL 7 JOIN
  FILTER DINAMIS: proposaldate >= tglawal, proposaldate < tglakhir,
    m.MustahiqId (opsional), pg.ProductGroupId (opsional)
  TIDAK ADA filter branch — laporan ini cross-branch
  OUTPUT: Excel 1 sheet, kolom: CustomerName, ProductGroupName, ProposalNo,
    ProposalDate, ProposalDescription, ProposalNominal, ProposalReceivedBy,
    ProposalReceivedDate, ProposalReferenceBy, RealizationDate, RealizationAmount,
    RealMemoNumber, FundSourceNo+FundSourceName
  TEMPLATE: 'template_proposal'

=== QLapMustahiq — GenerateFile (QLapMustahiq_data.py baris 203-317) ===
QUERY UTAMA (banyak JOIN, termasuk subquery nested):
  Tabel: mustahiq (m), customer (c), customercorporate (cc), customerpersonal (cp)
  Subquery LEFT JOIN: product (pr), mustahiqproduct (mp),
    MustahiqAdditionalInfo (i), v_mustahiqdata (vm — VIEW)
  LEFT JOIN enum_varchar (e) untuk ashnaf
  JOIN COUNT: 4 join luar + subquery 4 join = TOTAL 8 JOIN
  FILTER DINAMIS:
    - ProductId (jika IsAllProgram='F')
    - mustahiqtype = 'MP' atau 'MC' (jika IsAllMustahiqType='F')
    - datestart range (jika IsAllProgramDate='F')
  OUTPUT: Excel 1 sheet, kolom per mustahiq: MustahiqId, CustomerName,
    MustahiqType (Individu/Lembaga), Ashnaf, Alamat, PhoneNumber,
    CPName, CPPhoneNumber, CPMobileNumber, SupervisorName, Tingkat beasiswa,
    Achievement, SchoolName, Tgl beasiswa, ProductName, DateStart,
    DistributionAmount, RealizationAmount
  TEMPLATE: 'tplDaftarMustahiq'
  CATATAN: Output mengiterasi per mustahiq, data beasiswa diambil dari
    MustahiqAdditionalInfo (SD/SMP/SMA/Universitas), satu row Excel per
    kombinasi mustahiq+program.

=== fReportRealizationRegular — GenerateFile (fReportRealizationRegular_data.py baris 15-282) ===
QUERY UTAMA Sheet "Detail" (9 tabel + 1 subquery budget):
  Tabel: product (p), program (g), productgroup (pg), mustahiq (m), customer (c),
    realization (r), realizationdetail (rd), realizationmemo (rm), mustahiqproduct (mp)
  LEFT JOIN: STATUSRECREPDETAIL (s) on rd.realizationdetailid = s.realizationdetailid
  Subquery LEFT JOIN: transaction.Budget (bdg), realizationbudget (rb),
    transaction.BudgetItem (bdi), transaction.BudgetItem (bdip) — self-join BudgetItem
  JOIN COUNT: 9 inner + 1 left + subquery 4 = TOTAL 14 JOIN
  DISCRIMINATOR KRITIS: g.programtype = 'R'  <- WAJIB: hanya program RUTIN
  FILTER: r.realizationdate >= BeginDate AND r.realizationdate < EndDate
  TIDAK ADA filter BranchCode di query ini (berbeda dengan NonRegular!)
  OUTPUT: 3 sheet Excel:
    - "Detail": per baris realisasi, grouped by ProductName (dengan sub-total)
      kolom: No, ProductGroupName, ProductName, RealizationDate, CustomerName,
      AddressStreet, [kosong], RealizationAmount, StatusReceivables (Ya/Tidak),
      ReportDetailStatus (Belum/Sudah/Batal), ReportAmount, BudgetCode-BudgetDesc
    - "Rekap": per ProductGroupName, sum RealizationAmount
    - "RekapAnggaran": per BudgetCode, sum RealizationAmount
  TEMPLATE: 'tplRealProgramRegular'

=== fReportRealizationNonRegular — GenerateFile (fReportRealizationNonRegular_data.py baris 16-296) ===
QUERY UTAMA Sheet "Detail" (8 tabel + LEFT JOINs):
  Tabel: product (p), program (g), productgroup (pg), mustahiq (m), customer (c),
    realization (r), realizationdetail (rd), realizationmemo (rm), mustahiqproduct (mp)
  LEFT JOIN: proposal (po) on mp.proposalid = po.proposalid
  LEFT JOIN: transaction.financialaccount (fa) on fa.accountno = mp.accountno
  Subquery LEFT JOIN: transaction.Budget, realizationbudget, transaction.BudgetItem (x2)
  JOIN COUNT: 9 inner + 2 left + subquery 4 = TOTAL 15 JOIN
  DISCRIMINATOR KRITIS: g.programtype = 'N'  <- WAJIB: hanya program NON RUTIN
  FILTER: r.realizationdate range, rd.RealizationAmount range (BeginAmount..EndAmount),
          mp.BranchCode = '{BranchCode}'  <- FILTER CABANG AKTIF
  OUTPUT: 3 sheet Excel (Detail, Rekap, RekapAnggaran) — sama dengan Regular
  TEMPLATE: 'tplRealProgramNonRegular'
  CATATAN: Ada filter nominal (BeginAmount/EndAmount), ada filter BranchCode

=== fReportRealizationReceivable — GenerateFile (fReportRealizationReceivable_data.py baris 15-212) ===
QUERY UTAMA (4 tabel + 1 subquery aggregate):
  Tabel: realizationmemo (m), realization (r), vemployee (e)
  Subquery LEFT JOIN: StatusReceivableReport (t), StatusRecRepDetail (d)
    WHERE d.ReportDetailStatus IN ('1','2')
    GROUP BY realizationid, ReceivableReportUserInput, ReceivableReportDate
  JOIN COUNT: 3 inner + subquery 2 = TOTAL 5 JOIN
  DISCRIMINATOR KRITIS: r.statusreceivables = 'Y'  <- WAJIB: hanya realisasi berpiutang
  FILTER: r.realizationdate range (EndDate + 1 hari — inklusif, baris 34 _data.py)
  TIDAK ADA filter BranchCode, TIDAK ADA filter programtype
  OUTPUT: 1 sheet "Detail"
    kolom: No, RealizationDate, RealMemoNumber, RealizationType (Rutin/Non Rutin),
    RealizationDescription, RealizationAmount, ReportAmount,
    (RealizationAmount - ReportAmount) = sisa piutang,
    EmployeeName, RealizationInputUser, ReceivableReportUserInput
  TEMPLATE: 'tplRealizationReceivable'
  CATATAN: EndDate logic BERBEDA — fmtEndDate = EndDate + 1 (baris 34)

=== fReportRealizationReturn — GenerateFile (fReportRealizationReturn_data.py baris 15-219) ===
QUERY UTAMA (3 tabel + subquery per baris untuk biaya):
  Tabel: program.realization (r), program.realizationreturn (t), program.realizationmemo (m)
  JOIN COUNT: 3 inner joins (top-level)
  FILTER: t.returndate range (>= BeginDate AND < EndDate) — filter pada returndate, BUKAN realizationdate
  OUTPUT: 1 sheet "Detail"
    Per baris: No, ReturnDate, RealizationAmount, ReturnAmount,
    [kolom 5 kosong untuk rincian biaya], RealMemoNumber, ReturnDescription, InputUser
    Per sub-baris biaya (subquery loop): CostAmount, CostItemDescription
    dari: program.realizationcost JOIN program.costitem WHERE returnid = X
  TEMPLATE: 'tplRealizationReturn'
  CATATAN: Ada nested loop — per baris return, ada subquery ke realizationcost+costitem
    untuk menampilkan rincian biaya.

=== fReportRealizationByMustahiq — GenerateFile (fReportRealizationByMustahiq_data.py baris 16-297) ===
QUERY UTAMA Sheet "Detail" (sama dengan NonRegular — 8 tabel + LEFT JOINs):
  Tabel: product (p), program (g), productgroup (pg), mustahiq (m), customer (c),
    realization (r), realizationdetail (rd), realizationmemo (rm), mustahiqproduct (mp)
  LEFT JOIN: proposal (po) on mp.proposalid = po.proposalid
  LEFT JOIN: transaction.financialaccount (fa) on fa.accountno = mp.accountno
  Subquery LEFT JOIN: transaction.Budget, realizationbudget, transaction.BudgetItem (x2)
  JOIN COUNT: 9 inner + 2 left + subquery 4 = TOTAL 15 JOIN
  TIDAK ADA filter programtype (menampilkan R dan N sekaligus — cross-type)
  FILTER: r.realizationdate range, mp.BranchCode = '{BranchCode}'
  ORDER BY: customername, customerid, realizationdate, productname
  OUTPUT: 2 sheet Excel:
    - "Detail": grouped by customerId/customerName (sub-total per mustahiq)
      kolom: No, CustomerName, AddressStreet, RealizationDate, ProductGroupName,
      ProductName, RealizationAmount, AccountName, DetailDescription,
      ProposalNo, ProposalNominal, ProposalDescription, ProposalReferenceBy,
      BudgetCode-BudgetDesc
    - "Rekap": per CustomerName, sum RealizationAmount
  TEMPLATE: 'tplRealizationByMustahiq'

── SCHEMA DB ───────────────────────────────────────────────────
(Semua tabel di schema program.* kecuali yang prefix transaction.*)

ENTITIES:
  - Proposal → tabel: program.PROPOSAL
    kolom: proposalid (PK), proposaldate, proposaldescription, proposalno,
    proposalnominal, proposalreceivedby, proposalreceiveddate, proposalreferenceby,
    mustahiqid (FK), productgroupid (FK), proposalstatus
    Sumber: program.mdt baris 9549-9636

  - ProductGroup → tabel: program.PRODUCTGROUP
    kolom: productgroupid (PK), productgroupname, productgroupcode
    Sumber: program.mdt baris 5105

  - Mustahiq → tabel: program.MUSTAHIQ
    kolom: mustahiqid (PK), customerid (FK), mustahiqtype ('MP'=Individu, 'MC'=Lembaga), ashnaf
    Sumber: default.mcf baris 73, program.mdt

  - Customer → tabel: program.CUSTOMER
    kolom: customerid (PK), customername, addressstreet, addresskelurahan,
    addresskecamatan, addresscity, phonenumber
    Sumber: QLapMustahiq_data.py baris 9-27

  - CustomerCorporate → tabel: program.CUSTOMERCORPORATE
    kolom: customerid (FK), CPName, CPPhoneNumber, CPMobileNumber
    Sumber: QLapMustahiq_data.py baris 26

  - MustahiqProduct → tabel: program.MUSTAHIQPRODUCT
    kolom: mustahiqproductid (PK), mustahiqid (FK), productid (FK), proposalid (FK),
    accountno (FK ke financialaccount), branchcode, datestart, distributionamount,
    mustahiqproductname
    Sumber: program.mdt baris 3556-3557

  - Product → tabel: program.PRODUCT
    kolom: productid (PK), productname, productgroupid (FK)
    Sumber: program.mdt baris 356-417

  - Program → tabel: program.PROGRAM
    kolom: productid (FK), programtype ('R'=Rutin, 'N'=Non Rutin), ...
    Sumber: program.mdt baris 534-535

  - Realization → tabel: program.REALIZATION
    kolom: realizationid (PK), realmemoid (FK), realizationdate, realizationtype
    ('R'=Rutin, 'N'=Non Rutin), realizationdescription, realizationinputdate,
    realizationinputuser, realizationamount, statusreceivables ('Y'=Piutang, default lain),
    transactionid, branchcode, employeeid
    Sumber: program.mdt baris 10278-10399

  - RealizationMemo → tabel: program.REALIZATIONMEMO
    kolom: realmemoid (PK), realmemonumber, ...
    Sumber: program.mdt baris 10184-10251

  - RealizationDetail → tabel: program.REALIZATIONDETAIL
    kolom: realizationdetailid (PK), realizationid (FK), mustahiqproductid (FK),
    realizationamount, detaildescription
    Sumber: program.mdt baris 10428-10490

  - RealizationReturn → tabel: program.REALIZATIONRETURN
    kolom: returnid (PK), realizationid (FK), returndate, returndescription,
    returnamount, costamount, branchcode, inputuser, inputdate, authuser, authdate,
    transactionid
    Sumber: program.mdt baris 10775-10840

  - RealizationCost → tabel: program.REALIZATIONCOST
    kolom: costitemid (FK ke CostItem), returnid (FK), costamount
    Sumber: program.mdt baris 11033-11064

  - CostItem → tabel: program.COSTITEM
    kolom: costitemid (PK), costitemdescription
    Sumber: fReportRealizationReturn_data.py baris 107-114

  - StatusReceivableReport → tabel: program.STATUSRECEIVABLEREPORT
    kolom: statusreceivableid (PK), realizationid (FK), receivablereportuserinput,
    receivablereportdate
    Sumber: program.mdt baris 53 (classlist)

  - StatusRecRepDetail → tabel: program.STATUSRECREPDETAIL
    kolom: statusreceivableid (FK), realizationdetailid (FK), reportdetailstatus
    ('0'=Belum, '1'=Sudah, '2'=Batal), reportamount
    Sumber: fReportRealizationRegular_data.py baris 67 (LEFT JOIN)

  - RealizationBudget → tabel: program.REALIZATIONBUDGET
    kolom: realizationid (FK), productid (FK), budgetid (FK ke transaction.Budget)
    Sumber: program.mdt baris 10954

  [Tabel cross-schema dari transaction.*]:
  - transaction.FinancialAccount → tabel: transaction.FINANCIALACCOUNT
    kolom: accountno (PK), accountname
  - transaction.Budget → tabel: transaction.BUDGET
    kolom: budgetid (PK), budgetcode, itemid (FK ke BudgetItem)
  - transaction.BudgetItem → tabel: transaction.BUDGETITEM
    kolom: itemid (PK), itemname, parentitemid (FK ke BudgetItem self-join), budgetitemdescription
  - MustahiqAdditionalInfo → tabel: program.MUSTAHIQADDITIONALINFO
    kolom: mustahiqproductid (FK), mustahiqidsupervisor (FK ke mustahiq),
    schoolname, sd_kelas/sd_tahunawal/sd_tahunakhir,
    smp_kelas/smp_tahunawal/smp_tahunakhir,
    sma_kelas/sma_tahunawal/sma_tahunakhir,
    universitas_kelas/universitas_tahunawal/universitas_tahunakhir, achievement
  - VEmployee / vemployee → VIEW program.VEMPLOYEE
    kolom: employeeid (PK), employeename
  - v_mustahiqdata → VIEW program.V_MUSTAHIQDATA
    kolom: mustahiqid (PK), customername
  - enum_varchar → tabel shared: enum_name, enum_value, enum_description
    Dipakai untuk ashnaf: enum_name='eAshnaf'

RELASI:
  - Proposal.mustahiqid → Mustahiq (FK)
  - Proposal.productgroupid → ProductGroup (FK)
  - MustahiqProduct.mustahiqid → Mustahiq (FK)
  - MustahiqProduct.productid → Product (FK)
  - MustahiqProduct.proposalid → Proposal (FK, optional)
  - MustahiqProduct.accountno → transaction.FinancialAccount (FK, optional)
  - Product.productgroupid → ProductGroup (FK)
  - Program.productid → Product (FK) — Program extends Product
  - Realization.realmemoid → RealizationMemo (FK)
  - Realization.employeeid → VEmployee (FK ke view)
  - RealizationDetail.realizationid → Realization (FK)
  - RealizationDetail.mustahiqproductid → MustahiqProduct (FK)
  - RealizationReturn.realizationid → Realization (FK)
  - RealizationCost.returnid → RealizationReturn (FK)
  - RealizationCost.costitemid → CostItem (FK)
  - RealizationBudget.realizationid → Realization (FK)
  - RealizationBudget.budgetid → transaction.Budget (FK cross-schema)
  - StatusReceivableReport.realizationid → Realization (FK)
  - StatusRecRepDetail.statusreceivableid → StatusReceivableReport (FK)
  - MustahiqAdditionalInfo.mustahiqproductid → MustahiqProduct (FK)

── DISCRIMINATORS ──────────────────────────────────────────────
  KRITIS — jangan hilangkan saat implementasi:

  - program.programtype = 'R'  → Program RUTIN
    Dipakai di: fReportRealizationRegular (_data.py baris 94)
    Query WHERE: AND g.programtype = 'R'

  - program.programtype = 'N'  → Program NON RUTIN
    Dipakai di: fReportRealizationNonRegular (_data.py baris 104)
    Query WHERE: AND g.programtype = 'N'

  - realization.realizationtype = 'R'  → Realisasi Rutin (label output: 'Rutin')
    Dipakai di: fReportRealizationReceivable (_data.py baris 113)
    {'R' : 'Rutin', 'N' : 'Non Rutin'}[rSQL.RealizationType]

  - realization.realizationtype = 'N'  → Realisasi Non Rutin (label: 'Non Rutin')

  - realization.statusreceivables = 'Y'  → Realisasi berpiutang (ada piutang LPJ)
    Dipakai di: fReportRealizationReceivable (_data.py baris 73)
    Query WHERE: AND r.statusreceivables = 'Y'

  - statusrecrepdetail.reportdetailstatus = '0'  → LPJ Belum
  - statusrecrepdetail.reportdetailstatus = '1'  → LPJ Sudah
  - statusrecrepdetail.reportdetailstatus = '2'  → LPJ Batal
    Dipakai di: fReportRealizationRegular (_data.py baris 152) dan
    fReportRealizationReceivable subquery (baris 64)
    IN ('1','2') → dikategorikan sudah/batal (ReportAmount yang dihitung)

  - mustahiq.mustahiqtype = 'MP'  → Mustahiq Individu
  - mustahiq.mustahiqtype = 'MC'  → Mustahiq Lembaga
    Dipakai di: QLapMustahiq (_data.py baris 119-120)
    MapMustahiqType = {'MP' : 'Individu' , 'MC' : 'Lembaga' }

  - proposal.proposalstatus = 'B'  → Proposal masuk/diterima (aktif)
    Dipakai di: fLapProposal _data.py (baris 44), QLapProposal _intr.py
    OQLText baris 46: [ proposalstatus='B' ] — hanya proposal berstatus 'B'

  - enum_varchar.enum_name = 'eAshnaf'  → lookup enum golongan ashnaf
    Dipakai di: QLapMustahiq (_data.py baris 191) — join untuk label ashnaf

── KOMPLEKSITAS ────────────────────────────────────────────────
LEVEL:    TINGGI
ALASAN:
  - fReportRealizationRegular: 14 JOIN termasuk cross-schema ke transaction.*
    dan self-join pada BudgetItem
  - fReportRealizationNonRegular dan fReportRealizationByMustahiq: 15 JOIN masing-masing
  - QLapProposal: window function RANK() OVER — tidak umum di report sederhana
  - QLapMustahiq: 8+ JOIN + subquery nested + aggregate SUM
  - fReportRealizationReturn: nested loop (per baris return → subquery biaya)
  - Output multi-sheet Excel dengan grouping dan sub-total manual
  - Cross-schema query: program.* JOIN transaction.*
  - 7 dialog laporan, masing-masing independent dengan query berbeda
WORKFLOW: Laporan
REKOMENDASI MODEL: Modul ini memenuhi kriteria >5 dialog dengan query 5+ JOIN.
  Gunakan model OPUS untuk implementasi DWH views di fase nuwis-db-migrator.

── HANDOFF ─────────────────────────────────────────────────────
→ nuwis-seed-gen:
  MENU_KEY: distribution.report.proposal-incoming       / LABEL: Laporan Proposal Masuk              / ROLES: DIST,SPVDIST  [QAC=AMBIGU]
  MENU_KEY: distribution.report.mustahiq-list           / LABEL: Laporan Daftar Mustahiq             / ROLES: DIST,SPVDIST  [QAC=AMBIGU]
  MENU_KEY: distribution.report.realization-regular     / LABEL: Laporan Program Penyaluran Rutin    / ROLES: DIST,SPVDIST  [QAC=AMBIGU]
  MENU_KEY: distribution.report.realization-non-regular / LABEL: Laporan Program Penyaluran Non Rutin/ ROLES: DIST,SPVDIST  [QAC=AMBIGU]
  MENU_KEY: distribution.report.realization-receivable  / LABEL: Laporan Piutang Realisasi Penyaluran/ ROLES: DIST,SPVDIST  [QAC=AMBIGU]
  MENU_KEY: distribution.report.realization-return      / LABEL: Laporan Pengembalian Realisasi      / ROLES: DIST,SPVDIST  [QAC=AMBIGU]
  MENU_KEY: distribution.report.realization-by-mustahiq / LABEL: Laporan Penyaluran Per Mustahiq     / ROLES: AMBIGU (tidak ada AllowedGroups di .mnu)
  KONFIRMASI DIPERLUKAN:
    [1] QAC — tidak ada di mapping role isf-app. Konfirmasi ke nuwis-architect
        apakah QAC = QC (Quality Control) atau mapping ke role yang sudah ada
    [2] Laporan Penyaluran Per Mustahiq — tidak ada AllowedGroups, konfirmasi
        apakah accessible semua role atau butuh pembatasan

→ nuwis-db-migrator:
  DWH_VIEWS (7 views — schema dwh.* di mziss_laz):

  1. dwh.v_report_proposal_incoming
     Kolom: proposalid, proposaldate, proposaldescription, proposalno,
     proposalnominal, proposalreceivedby, proposalreceiveddate, proposalreferenceby,
     customer_name, product_group_name, realization_date, realization_amount,
     memo_amount, realmemo_number, fund_source_no, fund_source_name,
     mustahiq_id, proposalstatus
     JOIN: proposal → productgroup, mustahiq → customer,
     LEFT JOIN subquery(realizationdetail+realization+realizationmemo+mustahiqproduct
     +financialaccount dengan RANK() OVER window function)
     NOTES: Pertahankan RANK() OVER logic; filter proposalstatus='B' bisa dilakukan di query BFF

  2. dwh.v_report_mustahiq_list
     Kolom: mustahiq_id, mustahiq_type, customer_name, address_street,
     address_kelurahan, address_kecamatan, address_city, phone_number,
     cp_name, cp_phone_number, cp_mobile_number, ashnaf_label,
     product_name, product_id, date_start, distribution_amount,
     school_name, sd_kelas, sd_tahun_awal, sd_tahun_akhir,
     smp_kelas, smp_tahun_awal, smp_tahun_akhir,
     sma_kelas, sma_tahun_awal, sma_tahun_akhir,
     universitas_kelas, universitas_tahun_awal, universitas_tahun_akhir,
     achievement, supervisor_name
     JOIN: mustahiq → customer, LEFT JOIN customercorporate,
     LEFT JOIN subquery(mustahiqproduct+product+MustahiqAdditionalInfo+v_mustahiqdata),
     LEFT JOIN enum_varchar(eAshnaf)
     FILTER PARAMS: terima product_id, mustahiq_type, date_start_from, date_start_to

  3. dwh.v_report_realization_regular
     Kolom: product_id, product_name, product_group_name, mustahiq_product_name,
     customer_name, address_street, realization_id, realization_date,
     status_receivables, realization_amount, report_amount, report_detail_status,
     budget_code, budget_item_description
     JOIN: product+program+productgroup+mustahiq+customer+realization+
     realizationdetail LEFT JOIN statusrecrepdetail + subquery budget
     DISCRIMINATOR WAJIB: program.programtype = 'R'
     FILTER PARAMS: date_from, date_to

  4. dwh.v_report_realization_non_regular
     Kolom: product_id, product_name, product_group_name, mustahiq_product_name,
     customer_name, address_street, realization_id, realization_date,
     realization_amount, detail_description, proposal_no, proposal_description,
     proposal_nominal, proposal_reference_by, account_name, budget_code,
     budget_item_description, branch_code
     DISCRIMINATOR WAJIB: program.programtype = 'N'
     FILTER PARAMS: branch_code (dari session), date_from, date_to,
     amount_min (default 0), amount_max (default 3000000)

  5. dwh.v_report_realization_receivable
     Kolom: realization_id, realization_date, realization_amount,
     realization_input_user, realization_type, realization_description,
     realmemo_number, employee_name, receivable_report_user_input,
     report_amount, receivable_report_date
     JOIN: realizationmemo + realization + vemployee
     LEFT JOIN subquery(statusreceivablereport+statusrecrepdetail
     WHERE reportdetailstatus IN ('1','2'))
     DISCRIMINATOR WAJIB: realization.statusreceivables = 'Y'
     FILTER PARAMS: date_from, date_to (inklusif akhir — pakai <= atau date_to+1)

  6. dwh.v_report_realization_return
     Kolom header: return_id, return_date, realization_amount, return_amount,
     realmemo_number, return_description, input_user, realizationid
     Kolom biaya (join terpisah/nested): cost_item_description, cost_amount
     JOIN: realizationreturn + realization + realizationmemo
     Sub-detail: LEFT JOIN realizationcost + costitem ON returnid
     FILTER PARAMS: date_from, date_to (filter pada returndate — bukan realizationdate)

  7. dwh.v_report_realization_by_mustahiq
     Kolom: customer_id, customer_name, address_street, product_id,
     product_name, product_group_name, realization_date, realization_amount,
     detail_description, account_name, proposal_no, proposal_nominal,
     proposal_description, proposal_reference_by, budget_code,
     budget_item_description, branch_code
     TIDAK ADA filter programtype (semua jenis)
     FILTER PARAMS: branch_code (dari session), date_from, date_to

→ nuwis-python-builder:
  ENDPOINTS (semua di report-api, domain: distribution):

  1. GET /api/report/distribution/proposal-incoming
     Params: date_from (str ISO), date_to (str ISO), mustahiq_id (int, opt), product_group_id (int, opt)
     Logic: SELECT FROM dwh.v_report_proposal_incoming WHERE proposaldate BETWEEN ... AND proposalstatus='B' + filter opsional
     Export: GET /api/report/distribution/proposal-incoming/export → xlsx 1 sheet

  2. GET /api/report/distribution/mustahiq-list
     Params: mustahiq_type (str 'MP'/'MC', opt), product_id (int, opt),
             date_start_from (str ISO, opt), date_start_to (str ISO, opt)
     Logic: SELECT FROM dwh.v_report_mustahiq_list + filter dinamis
     Export: GET /api/report/distribution/mustahiq-list/export → xlsx 1 sheet

  3. GET /api/report/distribution/realization-regular
     Params: date_from (str ISO, required), date_to (str ISO, required)
     Logic: SELECT FROM dwh.v_report_realization_regular WHERE realizationdate BETWEEN
     TIDAK perlu branch_code (Regular tidak pakai BranchCode di query legacy)
     Export: GET /api/report/distribution/realization-regular/export → xlsx 3 sheet (Detail, Rekap, RekapAnggaran)

  4. GET /api/report/distribution/realization-non-regular
     Params: date_from, date_to, amount_min (float, default 0), amount_max (float, default 3000000)
     BFF: _resolve_branch() → branch_code ke report-api sebagai header/param
     Logic: SELECT FROM dwh.v_report_realization_non_regular WHERE ... AND branch_code = :branch AND realization_amount BETWEEN :min AND :max
     Export: GET /api/report/distribution/realization-non-regular/export → xlsx 3 sheet

  5. GET /api/report/distribution/realization-receivable
     Params: date_from, date_to
     Logic: SELECT FROM dwh.v_report_realization_receivable WHERE realizationdate >= :from AND realizationdate <= :to
     PERHATIAN: ubah logika EndDate+1 legacy → pakai <= date_to alih-alih < date_to+1
     Export: GET /api/report/distribution/realization-receivable/export → xlsx 1 sheet

  6. GET /api/report/distribution/realization-return
     Params: date_from, date_to
     Logic: SELECT header FROM dwh.v_report_realization_return WHERE returndate BETWEEN
     + nested query ke realizationcost per return_id (atau flat JOIN dengan multiple rows)
     Export: GET /api/report/distribution/realization-return/export → xlsx 1 sheet (nested)

  7. GET /api/report/distribution/realization-by-mustahiq
     Params: date_from, date_to
     BFF: _resolve_branch() → branch_code
     Logic: SELECT FROM dwh.v_report_realization_by_mustahiq WHERE realizationdate BETWEEN AND branch_code = :branch ORDER BY customer_name, customer_id
     Export: GET /api/report/distribution/realization-by-mustahiq/export → xlsx 2 sheet (Detail, Rekap)

  DISCRIMINATORS WAJIB DI SETIAP QUERY:
    Endpoint 3: WHERE programtype = 'R'  (sudah di DWH view, cukup select)
    Endpoint 4: WHERE programtype = 'N'  (sudah di DWH view, cukup select)
    Endpoint 5: WHERE statusreceivables = 'Y'  (sudah di DWH view, cukup select)
    Endpoint 6: filter pada returndate BUKAN realizationdate
    Endpoint 4 dan 7: WAJIB pakai BranchCode dari session (via BFF _resolve_branch)
    Endpoint 3: TIDAK pakai BranchCode

→ nuwis-ui-builder:
  PAGE_TYPE: laporan (semua 7 halaman)
  DOMAIN: distribution
  POLA UMUM:
    - Filter panel di atas, data TIDAK auto-load saat mount (Rule 7 isf-app)
    - Tombol "Tampilkan" untuk fetch data, tombol "Export Excel" disabled sebelum data ada
    - DateField.vue untuk semua filter tanggal
    - SearchSelect.vue untuk dropdown mustahiq dan program
    - dmy() untuk tampilan tanggal di tabel
    - Pagination standar (Paginator di atas DataTable)

  PAGE 1: LaporanProposalIncomingView.vue
    ROUTE: /distribution/report/proposal-incoming
    MENU_KEY: distribution.report.proposal-incoming
    FILTERS: date_from (DateField, default awal bulan), date_to (DateField, default hari ini),
             mustahiq_id (SearchSelect — lookup mustahiq opsional),
             product_group_id (SearchSelect — dropdown ProductGroup opsional)
    KOLOM TABLE: Nama Mustahiq, Jenis Program, No Proposal, Tgl Proposal,
      Deskripsi, Nominal, Diterima Oleh, Tgl Diterima, Referensi,
      Tgl Realisasi, Nominal Realisasi, No Memo, Sumber Dana

  PAGE 2: LaporanMustahiqListView.vue
    ROUTE: /distribution/report/mustahiq-list
    MENU_KEY: distribution.report.mustahiq-list
    FILTERS: mustahiq_type (select: Semua/Individu/Lembaga, default Semua),
             product_id (SearchSelect opsional), date_start_from (DateField opt),
             date_start_to (DateField opt)
    KOLOM TABLE: ID, Nama, Golongan, Ashnaf, Alamat, Telepon,
      Nama Kontak, Telp Kontak, HP Kontak, Supervisor, Tingkat, Sekolah, Achievement,
      Tgl Program, Nama Program, Rencana Distribusi, Realisasi

  PAGE 3: LaporanRealizationRegularView.vue
    ROUTE: /distribution/report/realization-regular
    MENU_KEY: distribution.report.realization-regular
    FILTERS: date_from (DateField, required, default today), date_to (DateField, required, default today)
    KOLOM TABLE: No, Jenis Program, Nama Program, Tgl Realisasi, Nama Mustahiq,
      Alamat, Nominal, Piutang (Ya/Tidak), Status LPJ, Nominal LPJ, Anggaran
    EXPORT: 3-sheet xlsx (Detail, Rekap, RekapAnggaran)

  PAGE 4: LaporanRealizationNonRegularView.vue
    ROUTE: /distribution/report/realization-non-regular
    MENU_KEY: distribution.report.realization-non-regular
    FILTERS: date_from (DateField), date_to (DateField),
             amount_min (Input number, default 0), amount_max (Input number, default 3000000)
    VALIDASI CLIENT: amount_min <= amount_max sebelum fetch
    KOLOM TABLE: No, Jenis Program, Nama Program, Tgl Realisasi, Nama Mustahiq,
      Alamat, Nominal, Sumber Dana, Keterangan, No Proposal, Nilai Proposal,
      Deskripsi Proposal, Referensi, Anggaran
    EXPORT: 3-sheet xlsx (Detail, Rekap, RekapAnggaran)

  PAGE 5: LaporanRealizationReceivableView.vue
    ROUTE: /distribution/report/realization-receivable
    MENU_KEY: distribution.report.realization-receivable
    FILTERS: date_from (DateField, default today), date_to (DateField, default today)
    KOLOM TABLE: No, Tgl Realisasi, No Memo, Jenis (Rutin/Non Rutin), Keterangan,
      Nominal Realisasi, Nominal LPJ, Sisa Piutang, Nama Karyawan,
      Inputer Realisasi, Inputer LPJ
    FORMULA UI: Sisa Piutang = realization_amount - report_amount (computed di frontend)

  PAGE 6: LaporanRealizationReturnView.vue
    ROUTE: /distribution/report/realization-return
    MENU_KEY: distribution.report.realization-return
    FILTERS: date_from (DateField, default today), date_to (DateField, default today)
    KOLOM TABLE: No, Tgl Pengembalian, Nominal Realisasi, Nominal Kembali,
      Rincian Biaya (expandable row atau flat), No Memo, Keterangan, Input Oleh
    CATATAN UI: Rincian biaya ditampilkan sebagai expandable sub-row per return_id,
      atau sebagai flat rows dengan colspan/rowspan manual

  PAGE 7: LaporanRealizationByMustahiqView.vue
    ROUTE: /distribution/report/realization-by-mustahiq
    MENU_KEY: distribution.report.realization-by-mustahiq
    FILTERS: date_from (DateField, default today), date_to (DateField, default today)
    KOLOM TABLE: No, Nama Mustahiq, Alamat, Tgl Realisasi, Jenis Program, Nama Program,
      Nominal, Sumber Dana, Keterangan, No Proposal, Nilai Proposal,
      Deskripsi Proposal, Referensi, Anggaran
    UI NOTE: Grouped by mustahiq — bisa pakai DataTable rowGroupMode atau sorted by customer_name
    EXPORT: 2-sheet xlsx (Detail, Rekap)

==== END MIGRATION_ANALYSIS ====

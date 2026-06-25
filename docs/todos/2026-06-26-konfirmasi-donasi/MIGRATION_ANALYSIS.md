==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/fund/
PORTAL:  zakat
SCOPE:   Konfirmasi Transaksi Donasi
TANGGAL: 2026-06-26

── FITUR LIST ──────────────────────────────────────────────────
  1. Konfirmasi Transaksi Donasi
     ROLES:           ADMIN, FUND, SPVFUND
     DIALOG:          dialogs/Donatur/fDonaturTransactionConfirm.*
     MENU_KEY_KANDIDAT: fundraising.donation.confirm

── FORM FIELDS (per dialog) ────────────────────────────────────
DIALOG: Donatur/fDonaturTransactionConfirm

PANEL FILTER (uipData — filter/search parameters, tidak disimpan ke DB):

  - BeginDate            : Date      [Required] — Tanggal Transaksi (mulai)
  - EndDate              : Date      [Required] — Tanggal Transaksi (akhir)
  - LBranch.Kode_Cabang  : String    [Required] — Kode Cabang (lookup ke enterprise.Cabang)
  - LBranch.Nama_Cabang  : String    [ReadOnly] — Nama Cabang (display dari lookup)
  - IsAllCabang          : Boolean   [Optional] — Seluruh Cabang (checkbox; 'T'/'F')
  - SearchCategory       : Integer   [Optional] — Filter Donatur (0=Semua, 1=No Donatur, 2=Nama Donatur)
  - SearchText           : String    [Optional] — Teks pencarian (enabled hanya jika SearchCategory != 0)
  - AmountFrom           : Currency  [Optional] — Nominal Transaksi (min; default 0)
  - AmountTo             : Currency  [Optional] — Nominal Transaksi (max; default 10.000.000)
  - IsAllBank            : Boolean   [Optional] — Seluruh Kas/Bank (HIDDEN di UI, Visible=false)
  - Description          : String    [Optional] — Keterangan Transaksi (max 100 karakter)
  - LimitData            : Integer   [Optional] — Jumlah transaksi yang ditampilkan (default 50)
  - UserId               : String    [ReadOnly] — Id User (auto-fill dari session)
  - IsSPV                : Integer   [Hidden]   — Mode supervisor (0=biasa, 1=SPV; dari parameter Show())
  - BranchCode           : String    [Hidden]   — Kode cabang user aktif (dari session)
  - BeginItemNo          : Integer   [Hidden]   — Nomor awal tampilan (sementara tidak dipakai)

GRID HASIL (uipTransaction — read-only, multirow, tidak diedit langsung):

  - TransactionId        : Integer   [Hidden]   — PK transaksi (key PObject Transaction)
  - TransactionNo        : String    [ReadOnly] — Nomor Transaksi
  - ActualDate           : Date      [ReadOnly] — Tanggal Transaksi Aktual
  - DonorNo              : String    [Editable] — ID Donatur (dapat diubah via Edit Donatur)
  - DonorName            : String    [Editable] — Nama Donatur (dapat diubah via Edit Donatur)
  - Amount               : Currency  [ReadOnly] — Nominal Transaksi
  - Description          : String    [ReadOnly] — Keterangan
  - BranchCode           : String    [Hidden]   — Kode Cabang (tersimpan, dipakai untuk validasi cross-branch)
  - ChannelName          : String    [ReadOnly] — Nama Kas/Bank (dari financialaccount.accountname via accountno)
  - BranchName           : String    [ReadOnly] — Nama Cabang (dari enterprise.cabang)
  - ChannelCode          : String    [Hidden]   — Kode Kas/Bank (account no; tersimpan, tidak tampil di grid)
  - ProductName          : String    [ReadOnly] — Nama Produk (dari financialaccount via accountno produk)
  - TransactionItemId    : Integer   [Hidden]   — PK transactionitem (dipakai untuk EditDonor/ViewDonor)

SECTIONS: Tidak ada tab — layout DualSplit:
  - Panel filter atas (pBatch)
  - Grid hasil bawah (gTransaction)
  - Panel aksi (pTranAction)

READ_ONLY (auto-fill dari session):
  UserId (dari config.securitycontext.InitUser),
  BranchCode (dari config.securitycontext.GetUserInfo()[4]),
  LBranch.Kode_Cabang & Nama_Cabang (dari session),
  BranchName (lookup dari enterprise.cabang),
  ChannelName (lookup dari financialaccount)

HIDDEN (tersimpan tapi tidak tampil):
  IsSPV, BranchCode (uipData), TransactionId, BranchCode (grid),
  ChannelCode, TransactionItemId, BeginItemNo, IsAllBank (Visible=false)

── UI FLOW ─────────────────────────────────────────────────────
ON OPEN:
  - Pre-fill: UserId dari session (config.securitycontext.InitUser)
  - Pre-fill: BranchCode & LBranch dari session (config.securitycontext.GetUserInfo()[4] & [5])
  - BeginDate dan EndDate di-set ke hari ini (config.Now())
  - Default: IsAllCabang='F', SearchCategory=0, IsSPV=0, LimitData=50, AmountFrom=0, AmountTo=10.000.000, IsAllBank='T'
  - Checkbox IsAllCabang: jika BranchCode bukan '001' atau bukan mode SPV, disembunyikan (pBatch_IsAllCabang.visible=0)
  - SearchText: disabled sampai SearchCategory dipilih (non-zero)
  - Sumber kode: _intr.py → Show(), _data.py → FormSetDataEx()

ON SEARCH / TAMPILKAN:
  - Tombol "Tampilkan daftar transaksi" → bLihatTransaksiClick → CreateTransactionParam → form.SetDataWithParameters → FormSetDataEx (server) → RunSQLTransactionList
  - RunSQLTransactionList: query 5 tabel dengan JOIN:
      accounttransactionitem
      JOIN transactionitem
      JOIN transaction
      LEFT JOIN financialaccount (channel)
      LEFT JOIN financialaccount (product)
  - DISCRIMINATOR KRITIS: "and d.MutationType='C' and a.TransactionCode in ('SD001','SD002')"
    — hanya tampilkan transaksi penghimpunan donatur (kredit kas, kode SD001/SD002)
  - Filter dinamis: date range, branch, donor search (no/nama), amount range, description text, bank account
  - Hasil dimuat ke uipTransaction (grid)
  - Sumber kode: _data.py → RunSQLTransactionList

ON ACTIONS (per baris terpilih di grid):
  - "Ubah Donatur Transaksi" (bEditTrans) → EditDonor() → buka sub-dialog Donatur/fEditTransactionDonatur
    → update DonorNo/DonorName di grid
  - "Peragaan Transaksi" (bViewTrans, hidden di default) → ViewDonor() → buka Donatur/fViewTransactionDonatur (read-only)
  - "Hapus Transaksi" (bDeleteTrans) → DeleteTransaction() → validasi cross-branch + validasi AuthStatus
    → ExecuteScript('Transaction/S_DeleteTransaction', ph)
  - "Cetak Kwitansi" (bPrintVoucher, hidden di default) → PrintVoucher()
    → ExecuteScript('Transaction/S_Kwitansi.Print', ph)
  - "Export Excel" (hidden, Visible=false) → ExportExcelClick
    → form.CallServerMethod('GetTransactionList', ph) → Excel via template tplHistTransList.xls

VALIDASI CLIENT-SIDE:
  - DeleteTransaction: cek BranchCode baris == BranchCode user (cross-branch check)
  - DeleteTransaction: cek AuthStatus == 'T' dan bukan SPV → tolak hapus
  - bPostingClick (dari _data.py): cek IsPosted == 'T' → tolak posting ulang
  - JurnalTransaksi (server method): cek IsPosted sebelum CreateJournal
  - Sumber kode: _intr.py → DeleteTransaction(), _data.py → bPostingClick()

── SAVE LOGIC ──────────────────────────────────────────────────

### Aksi 1: Hapus Transaksi
ENTRY:   scripts/Transaction/S_DeleteTransaction.py → DAFScriptMain
ALUR:
  1. Validasi client: BranchCode baris == BranchCode user (dari _intr.py DeleteTransaction)
  2. Validasi client: AuthStatus != 'T' ATAU user adalah SPV (dari _intr.py DeleteTransaction)
  3. Server: config.BeginTransaction()
  4. helper.GetObject('Transaction', param.TransactionId) — lookup PObject Transaction
  5. oTran.Delete() — memanggil Transaction.OnDelete() di script_modules/Transaction.py:
     a. Hapus InboxTransaction terkait (helper.GetObjectByNames('InboxTransaction', ...))
     b. DeleteTransactionItem() → loop semua TransactionItem:
        - Setiap item: item.CancelTransaction() → reverse MutationType, hapus SponsorTransaction,
          VolunteerTransaction, BudgetTransaction, CashAdvanceReturnInfo, CashAdvanceProgramInfo,
          CashAdvanceMemoInfo, DistributionTransferInfo, LsGLInterface
        - oItems.DeleteAllPObjs() → DELETE transaction.accounttransactionitem, transaction.transactionitem
  6. config.Commit() / config.Rollback() pada exception
  TABEL TERPENGARUH:
    transaction.transaction (DELETE),
    transaction.transactionitem (DELETE),
    transaction.accounttransactionitem (DELETE),
    tabel pendukung (inboxtransaction, sponsortransaction, volunteertransaction, budgettransaction, dll)

### Aksi 2: Cetak Kwitansi / Voucher
ENTRY:   scripts/Transaction/S_Kwitansi.py → Print (ExecuteScript('Transaction/S_Kwitansi.Print', ph))
ALUR:
  1. helper.GetObject('Transaction', data.TransactionId)
  2. oTran.GetKwitansi() → dispatch ke Voucher.GetKwitansiVoucherDebet (SD001/SD002/SDULBA/CI/PEAR/PXAR/INVP)
     atau GetKwitansiVoucherKredit (selain itu) — dari script_modules/Transaction.py GetKwitansi()
  3. Buat stream file (RTF/DOC), tambahkan ke returns sebagai AddStreamWrapper
  4. Kembalikan Stream_Name ke client untuk dicetak
  TIDAK ada perubahan DB — read-only

### Aksi 3: Posting / Jurnal
ENTRY:   _data.py → JurnalTransaksi (CallServerMethod 'JurnalTransaksi')
ALUR:
  1. helper.GetObject('Transaction', data.TransactionId)
  2. Cek IsPosted != 'T'
  3. oTran.CreateJournal() → dari script_modules/Transaction.py:
     a. Cek AuthStatus == 'T'
     b. CreateJournalData() → susun journal block + items dari Ls_TransactionItem
     c. Kirim ke services.transaction_handler via modman.getModule
     d. Response: set IsPosted='T', JournalNo, JournalBlockId di transaction
  TABEL TERPENGARUH:
    transaction.transaction (UPDATE isposted, journalblockid, journalno, journalerrordescription)
    Jurnal tersimpan di sistem akuntansi (terpisah via services/transaction_handler)

### Aksi 4: Ubah Donatur Transaksi
ENTRY:   Sub-dialog Donatur/fEditTransactionDonatur (file terpisah — tidak dianalisis detail di sini)
ALUR:
  Buka dialog fEditTransactionDonatur dengan TransactionItemId, DonorNo, DonorName, Amount, ChannelCode/Name.
  Setelah simpan, hasil baru (DonorNo, DonorName) di-update ke grid uipTransaction di memory.

### Aksi 5: Export Excel
ENTRY:   _data.py → GetTransactionList (CallServerMethod 'GetTransactionList')
ALUR:
  RunSQLTransactionList → loop hasil → tulis ke workbook Excel template tplHistTransList.xls.
  TIDAK ada perubahan DB — read-only.

── SCHEMA DB ───────────────────────────────────────────────────
ENTITIES (dari core/app.mdt + script_modules/Transaction.py):

  - Transaction → tabel: transaction.transaction
    kolom: transactionid (PK), transactiondate, actualdate, referenceno, description,
           inputer, transactioncode, branchcode, authuser, transactiontime, authdate,
           authstatus, isposted, authaction, journalblockid, channelcode, channelaccountno,
           sponsorid, donorid, volunteerid, transactionno, paidto, currencycode,
           receivedfrom, marketerid, rate, journalno, hcbatchitemid, authoperationmode,
           updatedate, journalerrordescription, sourcetransactionid, revtransactionid,
           transactionitemid, batchid

  - TransactionItem → tabel: transaction.transactionitem
    kolom: transactionitemid (PK), transactionid (FK), mutationtype, amount, branchcode,
           currencycode, ekuivalenamount, rate, parameterjournalid, rc_code

  - AccountTransactionItem → tabel: transaction.accounttransactionitem
    kolom: transactionitemid (PK/FK ke transactionitem), accountno, branchcode, currencycode,
           refaccountno, refaccountname, isupdatebalance, accountcode, fundentity

  - DonorTransactionItem → tabel: transaction.accounttransactionitem
    kolom: sama dengan AccountTransactionItem + donorid, amountperunit, totalunit
    CATATAN: DonorTransactionItem mewarisi AccountTransactionItem, disimpan ke tabel SAMA
             (accounttransactionitem) dengan discriminator dari PClass

  - FinancialAccount → tabel: transaction.financialaccount
    kolom: accountno (PK), accountname, branchcode, currencycode, balance
           (dan turunannya: CashAccount, BankAccount, ProductAccount, dll.)

RELASI:
  - Transaction.BatchId → TransactionBatch (FK)
  - TransactionItem.TransactionId → Transaction (FK)
  - AccountTransactionItem.TransactionItemId → TransactionItem (FK)
  - AccountTransactionItem.AccountNo → FinancialAccount (FK)
  - Transaction.ChannelAccountNo → FinancialAccount.AccountNo (FK)
  - DonorTransactionItem.DonorId → fund.donor (FK)

── DISCRIMINATORS ──────────────────────────────────────────────
  KRITIS:
  - mutationtype = 'C' (di transactionitem) → hanya transaksi kredit (penerimaan/penghimpunan donasi)
    Sumber: _data.py RunSQLTransactionList: "and d.MutationType='C' and a.TransactionCode in ('SD001','SD002')"

  KRITIS:
  - transactioncode = 'SD001' → Setoran Donatur (penghimpunan reguler via kas/bank)
  - transactioncode = 'SD002' → Setoran Donatur (varian kedua, misal autodebet/HC)
    Sumber: _data.py RunSQLTransactionList + core/script_modules/Transaction.py GetDataDonor()

  PENTING:
  - authstatus = 'F' → belum diotorisasi (dapat dihapus oleh FUND own-branch)
  - authstatus = 'T' → sudah diotorisasi (hanya SPVFUND yang bisa hapus)
    Sumber: _intr.py DeleteTransaction(), Transaction.SetAuth(), Transaction.Approval()

  PENTING:
  - isposted = 'T' → sudah dijurnal ke akuntansi (tidak bisa posting ulang)
  - isposted = 'F' → belum dijurnal
    Sumber: _intr.py bPostingClick(), _data.py JurnalTransaksi(), Transaction.CreateJournal()

  INFO:
  - IsSPV = 1 → mode supervisor (tampilkan tombol extra, bisa hapus transaksi yang sudah diotorisasi,
    bisa lihat semua cabang)
    Sumber: _intr.py Show(SPVMode), DeleteTransaction(), logika pBatch_IsAllCabang visibility

── KOMPLEKSITAS ────────────────────────────────────────────────
LEVEL:    SEDANG
ALASAN:   Query utama melibatkan 5 tabel (accounttransactionitem, transactionitem, transaction,
          financialaccount x2) dengan 4 JOIN; logika hapus cascade melalui PObject hierarchy
          (Transaction.OnDelete → DeleteTransactionItem → loop item.CancelTransaction);
          5 aksi berbeda (hapus, posting/jurnal, cetak kwitansi, edit donatur, export excel);
          validasi RBAC per baris (cross-branch + authstatus + SPV mode).
          Tidak ada dialog jurnal bertingkat sendiri — jurnal dikirim ke subsistem akuntansi
          via services.transaction_handler.
WORKFLOW: Custom (list + filter + per-row actions: delete, post, print, edit-donor)

── HANDOFF ─────────────────────────────────────────────────────
→ nuwis-seed-gen:
  MENU_KEY: fundraising.donation.confirm
  LABEL:    Konfirmasi Transaksi Donasi
  ROLES:    ADMIN, FUND, SPVFUND
  Catatan:  Perlu 2 level aksi di role_menu_permission —
            FUND: view + delete (own-branch, unauth only)
            SPVFUND: view + delete (all-branch, termasuk auth) + post + print

→ nuwis-db-migrator:
  DWH_VIEWS: Opsional — dwh.v_donor_transaction_confirm dengan kolom:
    transactionid, transactionno, actualdate, transactiondate,
    donorid, donor_name, amount, channel_account_no, channel_name,
    product_name, auth_status, is_posted, branch_code, branch_name, inputer
  MIGRATIONS: Tidak ada tabel baru — semua entitas sudah ada di schema transaction.

→ nuwis-python-builder:
  ENDPOINTS:

    GET  /api/fundraising/donation-confirm
         Query params: begin_date, end_date, branch_code, is_all_branch,
                       search_category, search_text, amount_from, amount_to,
                       description, limit
         Logic: RunSQLTransactionList dengan DISCRIMINATOR
                mutationtype='C' AND transactioncode IN ('SD001','SD002')
         Response: list transaksi — transaction_id, transaction_no, actual_date,
                   donor_no, donor_name, amount, description, branch_code,
                   branch_name, channel_name, channel_code, product_name,
                   auth_status, is_posted, transaction_item_id

    DELETE /api/fundraising/donation-confirm/{transaction_id}
         Validasi: branch_code baris == branch user (kecuali branch_access='all')
         Validasi: auth_status != 'T' ATAU user adalah SPVFUND (role check)
         Logic: DELETE cascade transaction + transactionitem + accounttransactionitem
                + inbox + sponsor/volunteer/budget/ca records
         Pattern: BeginTransaction / Commit / Rollback

    POST /api/fundraising/donation-confirm/{transaction_id}/post-journal
         Validasi: is_posted != 'T'
         Validasi: auth_status == 'T' (harus sudah diotorisasi sebelum dijurnal)
         Logic: CreateJournal → kirim ke services/transaction_handler (accounting subsystem)
         Result: UPDATE transaction SET is_posted='T', journal_no, journal_block_id

    GET /api/fundraising/donation-confirm/{transaction_id}/receipt
         Logic: Generate kwitansi (Voucher Debet untuk SD001/SD002)
         Response: file stream (PDF/RTF) untuk diunduh

  DISCRIMINATORS:
    - mutationtype = 'C' → hanya transaksi penerimaan (KRITIS — filter wajib di WHERE)
    - transactioncode IN ('SD001','SD002') → hanya penghimpunan donatur (KRITIS)
    - auth_status = 'F' → bisa dihapus oleh FUND (own branch)
    - auth_status = 'T' → hanya SPVFUND yang bisa hapus; is_posted bisa di-set 'T'
    - is_posted = 'T' → tidak bisa posting ulang (guard di endpoint post-journal)

→ nuwis-ui-builder:
  PAGE_TYPE: list (filter panel di atas, DataTable di bawah, aksi per baris)

  FIELDS (filter panel):
    - begin_date         : DateField.vue (v-model ISO) — Tanggal Transaksi mulai
    - end_date           : DateField.vue (v-model ISO) — Tanggal Transaksi akhir
    - branch_code        : SearchSelect.vue — Cabang (disabled jika branch_access='single')
    - is_all_branch      : Checkbox — Seluruh Cabang (visible hanya SPVFUND / branch_access='all')
    - search_category    : dropdown (0=Semua Donatur, 1=No Donatur, 2=Nama Donatur)
    - search_text        : Input (enabled hanya jika search_category != 0)
    - amount_from        : Input format angka — Nominal min (default 0)
    - amount_to          : Input format angka — Nominal max (default 10.000.000)
    - description        : Input — Keterangan Transaksi
    - limit              : Input number — Jumlah data (default 50)
    - Tombol "Tampilkan" — fetch data (tidak auto-load on mount; ikuti Rule #7)

  FIELDS (kolom DataTable):
    - transaction_no     : Nomor Transaksi
    - actual_date        : Tgl Transaksi → dmy()
    - donor_no           : ID Donatur
    - donor_name         : Nama Donatur
    - channel_name       : Nama Kas/Bank
    - product_name       : Nama Produk
    - amount             : Nominal Transaksi (format angka)
    - description        : Keterangan
    - branch_name        : Nama Cabang
    - auth_status        : badge — 'F'=Belum Otorisasi (warning), 'T'=Sudah Otorisasi (success)
    - is_posted          : badge — 'F'=Belum Posting (info), 'T'=Sudah Posting (success)
    - Kolom aksi         : [Hapus] [Jurnal] [Kwitansi] [Edit Donatur] — conditional per role

  ROLE-GATED UI:
    - Hapus:       FUND (own-branch, auth_status='F') + SPVFUND (semua branch, semua auth_status)
    - Jurnal/Post: SPVFUND only (auth_status='T', is_posted='F')
    - Edit Donatur: FUND/SPVFUND (own branch atau SPVFUND all)
    - Kwitansi:    semua yang punya akses (auth_status='T')
    - "Seluruh Cabang" checkbox: visible hanya SPVFUND / branch_access='all'

  FILTERS: date range, branch (all/single), donor search (no/nama), amount range, keterangan, limit

==== END MIGRATION_ANALYSIS ====

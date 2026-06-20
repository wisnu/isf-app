==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/core/
PORTAL:  zakat
SCOPE:   Transaksi Penerimaan Amil (Cash-In Amil) — form input transaksi
TANGGAL: 2026-06-20

── FITUR LIST ──────────────────────────────────────────────────
  1. Transaksi Penerimaan Amil
     ROLES:           ACC
     DIALOG:          dialogs/Transaksi/fCashIn.*
     MENU_KEY_KANDIDAT: keuangan.transaksi.penerimaan-amil

     Sumber:
       Transaksi.mnu baris 291-294:
         Name='TR0024A'
         Caption='Transaksi Penerimaan Amil...'
         OnClick='ShowFormClick'
         AllowedGroups='ACC'
         StringTag='Transaksi/fCashIn'

── FORM FIELDS (per dialog) ────────────────────────────────────
DIALOG: dialogs/Transaksi/fCashIn

HEADER PANEL (pBatch) — data umum transaksi:
FIELDS:
  - TransactionNo   : String [ReadOnly]  — Nomor Transaksi (auto-generate)
  - ActualDate      : Date   [Required]  — Tanggal Posting
  - PaidTo          : String [Optional]  — Kasir (default = UserId dari session)
  - ReceivedFrom    : String [Optional]  — Terima Dari

HIDDEN FIELDS (disimpan ke DB, tidak tampil di form utama):
  - Inputer         : String [ReadOnly]  — dari session (config.SecurityContext.UserId)
  - BranchCode      : String [ReadOnly]  — dari session (GetUserInfo()[4])
  - TransactionDate : Date   [ReadOnly]  — tanggal hari ini (config.Now())
  - FloatTransactionDate : Double [ReadOnly] — integer representation of today
  - Rate            : Double [ReadOnly]  — default 1.0
  - TotalAmount     : Double [ReadOnly]  — total dihitung otomatis dari item rows
  - PaymentType     : String [Hidden]    — 'K'=Kas Kecil, 'C'=Kas Cabang, 'B'=Bank, 'A'=Non Tunai; ditentukan dari tab aktif saat save
  - PeriodId        : Integer [Hidden]   — dari query budgetperiod berdasar bulan/tahun hari ini
  - SaveMode        : Integer [Hidden]   — internal (1=Simpan & Lanjut, 2=Simpan & Tutup)
  - ShowMode        : Integer [Hidden]   — 1=Insert, lainnya=Edit
  - DefaultCurrency : String [Hidden]    — dari SysVar OPTION.DefaultCurrency
  - DefaultCurrencyName : String [Hidden] — dari SysVar OPTION.DefaultCurrencyName

TAB KAS (pCashTransaction — PaymentType = 'C' atau 'K'):
FIELDS:
  - CashType        : String [Required]  — 'K'=Kas Kecil, 'C'=Kas Cabang (default='C')
  - ReferenceNo     : String [Optional]  — No. Kwitansi
  - Description     : String [Optional]  — Keterangan
  (TransactionDate, TotalAmount, Inputer ditampilkan ReadOnly)

TAB BANK (pBankTransaction — PaymentType = 'B') — DEFAULT ACTIVE:
FIELDS:
  - LBank (AccountNo) : Lookup [Required] — Rekening Bank (filter: Status='A', BranchCode=session, IsAmilAccount='T')
  - ReferenceNo     : String [Optional]  — No. Cek
  - Description     : String [Optional]  — Keterangan
  - Rate            : Double [Optional]  — Nilai Kurs (default 1.0)
  (TransactionDate, TotalAmount, Inputer ditampilkan ReadOnly)

TAB NON TUNAI/AKTIVA (pAssetTransaction — PaymentType = 'A', hidden tab):
FIELDS:
  - LAsset (Account_Code) : Lookup [Required] — Rekening Aktiva (akun 14xx/15xx/16xx)
  - LValuta (Currency_Code) : Lookup [Required] — Kode Valuta
  - ActualDate      : Date   [Optional]  — Tgl Aktual
  - ReferenceNo     : String [Optional]  — No. Referensi / FSZ
  - Description     : String [Optional]  — Keterangan
  - Rate            : Double [Optional]  — Nilai Kurs

GRID DETAIL (uipTransactionItem — multi-row, sama untuk semua tab kas/bank):
  Kolom yang TAMPIL:
  - AccountCode     : String [Required]  — Account No (lookup via fSelectAccount, filter: fl_cpa_AccountCode='310301' AND account_type='I')
  - AccountName     : String [ReadOnly]  — Name Account (auto dari lookup AccountCode)
  - Amount          : Double [Required]  — Nilai (> 0.0)
  - CashAccountNo   : String [Optional]  — Rek. Sumber (lookup via fSelectCANonAmil)
  - CashAccountName : String [ReadOnly]  — Nama Rek. Sumber (auto dari lookup)
  - Description     : String [Optional]  — Keterangan
  - FundProductCode : String [Optional]  — Sumber Dana (lookup via fSelectProductAccount,
                                            filter: ProductType='Z' atau 'C', FundCategory matched)
  - FundProductName : String [ReadOnly]  — Nama Sumber Dana (auto dari lookup)

  Kolom HIDDEN di grid (tersimpan):
  - FundCategory    : String — dari CashAccount yang dipilih (auto-fill dari fSelectCANonAmil)
  - FundAccountNo   : String — AccountNo ProductAccount; auto-resolve jika CashAccountNo diisi tapi FundAccountNo kosong
  - FundProductId   : Integer — dari lookup fSelectProductAccount
  - BudgetCode      : String — Kode Budget (hidden, lookup via fSelectBudgetCode)
  - BudgetOwner     : String — Pemilik Budget (hidden, auto dari Budget)
  - BudgetId        : Integer — (hidden)
  - ItemIdx         : Integer — urutan item (auto-increment)
  - Rate            : Double — kurs per item (default 1.0)
  - Ekuivalen       : Double — Amount * Rate (auto-calculate di ItemBeforePost)
  - LCurrency (Currency_Code) : String — valuta per item (default = DefaultCurrency session)

SECTIONS:    Header (pBatch), PaymentType toggle, Tab Kas/Bank/NonTunai, Grid Detail
READ_ONLY:   TransactionNo, Inputer, BranchCode, TransactionDate, TotalAmount, AccountName, CashAccountName, FundProductName
HIDDEN:      PaymentType, PeriodId, SaveMode, ShowMode, DefaultCurrency, DefaultCurrencyName, FloatTransactionDate,
             FundCategory, FundAccountNo, FundProductId, BudgetId, BudgetOwner, ItemIdx, Ekuivalen

Sumber: fCashIn.dfr, fCashIn.svr, fCashIn_intr.py

── UI FLOW ─────────────────────────────────────────────────────
ON OPEN (FormSetDataEx — fCashIn_data.py baris 37-69):
  - Inputer          ← config.SecurityContext.UserId
  - PaidTo           ← sama dengan Inputer
  - BranchCode       ← config.SecurityContext.GetUserInfo()[4]
  - TransactionDate  ← config.Now() (integer timestamp)
  - ActualDate       ← sama dengan TransactionDate
  - FloatTransactionDate ← config.Now()
  - Rate             ← 1.0
  - TotalAmount      ← 0.0
  - CashType         ← 'C' (Kas Cabang)
  - TransactionNo    ← '<AUTOGENERATED>' (placeholder, diisi saat save)
  - DefaultCurrency  ← dari SysVar OPTION.DefaultCurrency
  - DefaultCurrencyName ← dari SysVar OPTION.DefaultCurrencyName
  - LValuta.Currency_Code ← DefaultCurrency
  - PeriodId         ← query: SELECT periodid FROM budgetperiod WHERE parentperiodid=bulan/tahun

  Default tab aktif: pgBank (Tab Bank, baris 77 fCashIn_intr.py)

ON SAVE (Simpan() — fCashIn_intr.py baris 235-283):
  VALIDASI CLIENT-SIDE (sebelum CallServerMethod):
  1. FormObject.CommitBuffer() — flush semua perubahan grid
  2. CheckRequiredGeneral(): uipTransactionItem.RecordCount > 0 (minimal 1 item)
  3. Konfirmasi dialog: "Yakin simpan transaksi ?"
  4. Menentukan PaymentType dari tab aktif:
     - Tab 0 (Kas) → PaymentType = CashType ('K' atau 'C')
     - Tab 1 (Bank) → PaymentType = 'B' + CheckRequiredBank (LBank.AccountNo harus terisi)
     - Tab 2 (Non Tunai) → PaymentType = 'A' + CheckRequiredAsset (LAsset.Account_Code dan LValuta.Currency_Code harus terisi)
  5. CallServerMethod("SimpanData", ph) → ke fCashIn_data.SimpanData
  6. Jika IsErr=1: tampilkan ErrMessage
  7. Jika IsErr=0/2: tampilkan nomor transaksi; tawarkan cetak kwitansi

  VALIDASI CLIENT-SIDE di GRID (ItemBeforePost — fCashIn_intr.py baris 151-166):
  - AccountCode tidak boleh kosong/None/0
  - Amount > 0.0
  - Ekuivalen = Amount * Rate (dihitung otomatis)

  ExecuteScript calls: TIDAK ADA ExecuteScript langsung.
  SimpanData dipanggil via CallServerMethod("SimpanData", ph).

── SAVE LOGIC ──────────────────────────────────────────────────
ENTRY:   dialogs/Transaksi/fCashIn_data.py → SimpanData()
         → modman.getModule(config, 'scripts#Transaction.CashIn')
         → CashInNew() atau CashInUpdate() berdasarkan ShowMode

---
ALUR CashInNew (scripts/Transaction/CashIn.py baris 15-55):

  1. Ambil/buat TransactionBatch untuk hari ini:
     scripts/Transaction/Batch.py → GetBatchUser(config, ActualDate)
     - Cari batch (Inputer=userId, BatchDate=ActualDate, BatchTag='OPR', IsPosted='T', IsClosed='F')
     - Jika tidak ada: buat batch baru (INSERT transaction.transactionbatch)

  2. Buat Transaction baru:
     oBatch.NewTransaction('CI')
     - INSERT ke transaction.TRANSACTION
     - TransactionCode = 'CI'  ← DISCRIMINATOR UTAMA
     - AuthStatus = 'F' (belum otorisasi)
     - TransactionDate = config.Now()
     - Inputer = dari session

  3. Buat riwayat perubahan:
     helper.CreatePObject('TransHistoryOfChanges')
     - INSERT ke transaction.TRANSHISTORYOFCHANGES
     - ChangeType = 'I' (insert baru)

  4. Dispatch berdasarkan PaymentType:
     - 'K' (Kas Kecil)  → PettyCashIn()
     - 'C' (Kas Cabang) → BranchCashIn()
     - 'B' (Bank)       → BankIn()
     - 'A' (Non Tunai)  → TIDAK diimplementasi di CashIn.py (raise Exception)

     Untuk setiap PaymentType, logika umum:
     a. Set field-field Transaction: Inputer, BranchCode, ReferenceNo, Description,
        ChannelCode, CurrencyCode, Rate, PaidTo, ReceivedFrom, ActualDate
     b. Loop items dari request['Items']:
        - CreateGLTransactionItem(AccountCode, Valuta)
          → INSERT transaction.TRANSACTIONITEM (TransactionItemType='G')
          → oItemGL.SetMutation('C', amount, rate) → MutationType='C' (Kredit)
          → oItemGL.SetJournalParameter('10')
        - Jika BudgetId != 0: CreateBudgetTransaction
        - Tambah totalAmount
     c. Set oTran.Amount = totalAmount
     d. Buat AccountTransactionItem untuk rekening kas/bank (sisi Debit):
        - CreateAccountTransactionItem(oAccount)
          → INSERT transaction.TRANSACTIONITEM (TransactionItemType='A')
          → INSERT transaction.ACCOUNTTRANSACTIONITEM
          → oItemBA.SetMutation('D', totalAmount, rate) → MutationType='D' (Debit)
          → oItemBA.SetJournalParameter('10')
     e. GenerateTransactionNumber(CashCode)
        → Format: KM-{YYYY}-{branchCode}-{cashCode}-{7digit}
          (VoucherCode='KM' untuk TransactionCode='CI', dari TransactionType lookup)
     f. SaveInbox(params) → INSERT transaction.INBOX + INBOXTRANSACTION
     g. GetKwitansi() → generate file kwitansi (Voucher.GetKwitansiVoucherDebet)

  5. Cek limit otorisasi:
     corporate.CheckLimitOtorisasi(Amount * Rate)
     - Jika nominal <= limit['O']: oTran.AutoApproval() → AuthStatus = 'T'
     - Jika nominal > limit['O']: AuthStatus tetap 'F' (perlu otorisasi manual)

  6. CreateJournal():
     - Hanya berjalan jika AuthStatus == 'T'
     - Mengirim data jurnal ke accounting subsystem (services.transaction_handler)
     - Jika berhasil: IsPosted='T', set JournalBlockId, JournalNo

  7. Commit jika semua sukses; Rollback jika ada exception.

ALUR CashInUpdate (scripts/Transaction/CashIn.py baris 57-107):
  - Ambil Transaction existing by TransactionNo
  - DeleteTransactionJournal → oTran.DeleteJournal() (ke accounting subsystem)
  - CancelTransaction() → IsPosted='F', ChannelAccountNo='', delete semua TransactionItems
  - Re-run PettyCashIn/BranchCashIn/BankIn dengan data baru
  - AutoApprovalUpdate(): jika sebelumnya sudah otorisasi, approve ulang
  - CreateJournal() ulang

KHUSUS BankIn (baris 257-349) — perbedaan dari Cash:
  - Rekening bank diambil via helper.GetObject('BankCash', BankAccountNo)
    Filter saat lookup: IsAmilAccount='T' (hanya rekening bank yang ditandai Amil)
  - CurrencyCode dari rekening bank (bukan default)
  - TransactionNo di-generate setelah loop items
  - Jika item punya CashAccountNo:
    - CreateAccountTransactionItem untuk source account juga (Kredit)
    - oItemSource.SetJournalParameter('C20') → beda parameter jurnal!
    - oItemSource.FundAccountNo = FundAccountNo

── SCHEMA DB ───────────────────────────────────────────────────
ENTITIES (dari app.mdt):

  - Transaction → tabel: transaction.TRANSACTION
    kolom penting: transactionid (PK), transactiondate, actualdate, referenceno,
    description, inputer, transactioncode, branchcode, authuser, authstatus,
    isposted, authaction, authdate, journalblockid, journalno, channelcode,
    donorid, sponsorid, amount, currencycode, receivedfrom, marketerid,
    channelaccountno, rate, paidto, transactionno, transactiontime,
    hcbatchitemid, authoperationmode, updatedate, journalerrordescription

  - TransactionBatch → tabel: transaction.TRANSACTIONBATCH
    kolom: batchid (PK), batchdate, branchcode, inputer, description,
    batchtag, isclosed, isposted, batchno

  - TransactionItem (base) → tabel: transaction.TRANSACTIONITEM
    kolom: transactionitemid (PK), transactionid (FK), branchcode, currencycode,
    mutationtype ('D'=Debit/'C'=Kredit), amount, rate, ekuivalenamount,
    transactionitemtype (classifier: 'G'=GL, 'A'=Account, dll),
    description, refaccountno, refaccountname, accountcode, parameterjournalid, rc_code

  - GLTransactionItem (extends TransactionItem, TransactionItemType='G') → tabel: transaction.TRANSACTIONITEM
    kolom tambahan: glnumber, glname

  - AccountTransactionItem (extends TransactionItem, TransactionItemType='A') → tabel: transaction.TRANSACTIONITEM + transaction.ACCOUNTTRANSACTIONITEM
    kolom di ACCOUNTTRANSACTIONITEM: transactionitemid (PK, FK ke transactionitem),
    accountno (FK ke cashaccount), accounttitype (classifier), fundentity (integer),
    isupdatebalance, fundaccountno

  - TransHistoryOfChanges → tabel: transaction.TRANSHISTORYOFCHANGES
    kolom: historyid (PK), transactionid, transactionno, newtransactionno, changetype ('I'/'E'/'D'), userid, processtime

  - BankCash (CashAccount subtype) → tabel: transaction.CASHACCOUNT
    kolom penting: accountno (PK), accountname, branchcode, currencycode,
    bankname, bankaccountno, status, cashcode, isamilaccount, fundcategory, productid

RELASI:
  - Transaction.BatchId (FK) → TransactionBatch.BatchId
  - TransactionItem.TransactionId (FK) → Transaction.TransactionId
  - AccountTransactionItem.TransactionItemId (FK) → TransactionItem.TransactionItemId
  - AccountTransactionItem.AccountNo (FK) → CashAccount/BankCash.AccountNo
  - Transaction.TransactionCode → TransactionType.TransactionCode (lookup VoucherCode='KM')

── DISCRIMINATORS ──────────────────────────────────────────────
KRITIS — jangan hilangkan saat implementasi:

  1. TransactionCode = 'CI'
     Tabel: transaction.TRANSACTION kolom transactioncode
     Artinya: Cash In Amil (Transaksi Penerimaan Amil)
     Membedakan dari: 'SD001'/'SD002'=Penghimpunan, 'DD001'=Penyaluran, 'CO'=Cash Out Amil,
                      'CA'=Cash Advance, 'GT'=General Transaction, dll.

  2. VoucherCode = 'KM' (dari tabel TransactionType di-lookup via TransactionCode='CI')
     Tabel: transaction.TRANSACTIONTYPE kolom vouchercode
     Artinya: Kas Masuk — digunakan sebagai PREFIX nomor transaksi
     Format nomor: KM-{YYYY}-{branchCode}-{cashCode}-{7digit}
     Contoh: KM-2026-001-BCA001-0001234

  3. IsAmilAccount = 'T' (pada lookup rekening bank di LBank)
     Tabel: transaction.CASHACCOUNT kolom isamilaccount
     Artinya: Hanya rekening bank yang ditandai sebagai "Rekening Amil"
     yang bisa dipilih. BERBEDA dari form fFundCollection yang tidak filter ini.
     Filter OQL: [Status = 'A' and BranchCode = :BranchCode and IsAmilAccount='T']
     Sumber: fCashIn.dfr baris 353

  4. AccountCode filter = '310301' AND account_type = 'I' (untuk lookup GL Account di grid)
     Artinya: Akun yang dipilih di grid harus bertipe Income ('I') dengan parent akun 310301.
     Ini adalah akun-akun Pendapatan Amil.
     Sumber: fCashIn_intr.py baris 103:
       GetAccount(" and fl_cpa_AccountCode ='310301' and account_type='I' ")

  5. GLTransactionItem.MutationType = 'C' (Kredit) untuk item-item GL
     AccountTransactionItem.MutationType = 'D' (Debit) untuk rekening kas/bank
     Artinya: Penerimaan = sisi kas/bank Debit, sisi pendapatan Kredit

  6. ChannelCode = 'R' untuk BranchCashIn dan BankIn, 'P' untuk PettyCashIn
     Tabel: transaction.TRANSACTION kolom channelcode
     Artinya: 'R'=Regular, 'P'=Petty Cash

  7. ParameterJournalId = '10' untuk semua item kas/bank (Debit maupun Kredit)
     = 'C20' untuk AccountTransactionItem source account pada BankIn
     Tabel: transaction.TRANSACTIONITEM kolom parameterjournalid
     Artinya: Kode parameter jurnal untuk menentukan template jurnal akuntansi.
     KRITIS: jika salah, jurnal akuntansi tidak akan terbentuk benar.

  8. AuthStatus = 'F' → 'T' (auto-approval jika <= limit user)
     Tabel: transaction.TRANSACTION kolom authstatus
     Artinya: Sama seperti flow isf-app — jika nominal di bawah limit,
     langsung AUTHORIZED; jika di atas, perlu approval manual via Otorisasi.

── CATATAN FORMAT NOMOR TRANSAKSI ──────────────────────────────
Format: {VoucherCode}-{YYYY}-{branchCode}-{cashCode}-{seq7digit}

Contoh untuk BranchCashIn cabang 001, rekening kas cabang IDR:
  KM-2026-001-IDR-0001234

Dimana cashCode berasal dari:
  - BranchCashIn: oBranchCash.CashCode (dari rekening kas cabang)
  - BankIn:       oBankAccount.CashCode (dari rekening bank)
  - PettyCashIn:  hardcoded 'BMI'

VoucherCode='KM' didapat dari TransactionType dimana TransactionCode='CI'.
Sequence dikelola oleh customidgenAPI dengan prefix "TRANSACTION-KM-{YYYY}-{branch}-{cashCode}".

Sumber: scripts/Transaction/TransactionHelper.py baris 26-47,
        script_modules/Transaction.py baris 207-282

── ISF-APP: MAPPING KE OTORISASI ──────────────────────────────
Form ini memiliki flow otorisasi (maker-checker) bawaan DAF legacy:
  - AutoApproval jika nominal <= limit['O'] user
  - Jika di atas limit: AuthStatus='F', perlu supervisor approve

REKOMENDASI untuk isf-app:
  - entity_type: 'amil_income'
  - Gunakan endpoint save-and-submit (langsung PENDING)
  - Limit check via otorisasi.entity_config
  - Dispatcher: amil_income_service.create_from_payload()

── KOMPLEKSITAS ────────────────────────────────────────────────
LEVEL:    SEDANG
ALASAN:
  - 2 tabel utama (TRANSACTION + TRANSACTIONITEM) + 2 tabel subtype (ACCOUNTTRANSACTIONITEM, GLTRANSACTIONITEM)
  - 3 payment type (Kas Kecil, Kas Cabang, Bank) dengan logika berbeda
  - Auto-generate nomor transaksi berdasarkan CashCode dari rekening yang dipilih
  - Dual-mode save (insert vs update)
  - Jurnal akuntansi via subsystem terpisah (services.transaction_handler)
  - Auto-approval berdasarkan limit user
  - Kwitansi cetak setelah save
  - Budget reference (hidden, optional)
  - FundAccountNo resolve logic (fallback ke ProductAccount lookup)
  - Tab Non Tunai (Aktiva) ada di form tapi tersembunyi (TabVisible=false) — tidak perlu diimplementasi untuk MVP

WORKFLOW: Approval (maker-checker dengan auto-approval)

JUMLAH DIALOG TERKAIT: 1 dialog utama (fCashIn) + 4 dialog lookup sub:
  - fSelectAccount (lookup GL account)
  - fSelectCANonAmil (lookup cash account non-amil)
  - fSelectBudgetCode (lookup budget)
  - fSelectProductAccount (lookup product account / sumber dana)
  Total 5 dialog → memenuhi threshold rekomendasi opus, namun logika core
  tidak berlapis banyak. Model sonnet cukup untuk analisis ini.

── HANDOFF ─────────────────────────────────────────────────────
→ nuwis-seed-gen:
  MENU_KEY: keuangan.transaksi.penerimaan-amil
  LABEL:    Transaksi Penerimaan Amil
  ROLES:    ACC

→ nuwis-db-migrator:
  MIGRATIONS:
    - Tidak ada tabel baru — data masuk ke schema transaction.* yang sudah ada
    - Pastikan kolom transaction.CASHACCOUNT.isamilaccount ada (sudah ada, dari migrasi bank)
    - Pastikan transaction.TRANSACTIONTYPE berisi row TransactionCode='CI', VoucherCode='KM'
    - Pastikan transaction.CASHACCOUNT memiliki setidaknya satu row IsAmilAccount='T'
      untuk cabang yang digunakan
  DWH_VIEWS:
    - Jika diperlukan laporan: dwh.v_amil_income menggunakan filter
      transactioncode='CI', transactionitemtype='G', mutationtype='C'

→ nuwis-python-builder:
  ENDPOINTS:
    POST /api/transaction/amil-income/
      Body: { actual_date, reference_no, description, payment_type, bank_account_no,
              cash_type, rate, paid_to, received_from,
              items: [{ account_code, account_name, amount, valuta, rate, description,
                        cash_account_no, fund_account_no, fund_product_id, budget_id }] }
      Logic: amil_income_service.create_amil_income() →
        1. Resolve branch dari session
        2. Validate items tidak kosong
        3. Validate bank_account_no via BankCash.is_amil_account='T' jika payment_type='B'
        4. Generate transaction_no format KM-{YYYY}-{branch}-{cashCode}-{seq}
        5. INSERT transaction.transaction (transactioncode='CI')
        6. INSERT transaction.transactionitem per item (transactionitemtype='G', mutationtype='C', parameterjournalid='10')
        7. INSERT transaction.transactionitem + transaction.accounttransactionitem untuk kas/bank (mutationtype='D')
        8. Dispatch via otorisasi (entity_type='amil_income')

    GET /api/transaction/amil-income/
      Query params: date_from, date_to, branch_code, page, limit
      Filter: transactioncode='CI'

    GET /api/transaction/amil-income/{transaction_no}
      Detail transaksi beserta items

    PUT /api/transaction/amil-income/{transaction_no}
      Update: delete items lama, insert ulang (CashInUpdate pattern)

    GET /api/transaction/bank-accounts/amil
      Daftar rekening bank yang IsAmilAccount='T' untuk branch user
      Dipakai untuk dropdown LBank di form

    GET /api/transaction/cash-accounts/non-amil
      Daftar cash account non-amil untuk dropdown CashAccountNo di grid item

  DISCRIMINATORS (wajib diteruskan ke implementasi):
    - transactioncode = 'CI'
    - vouchercode = 'KM' (untuk format nomor transaksi)
    - isamilaccount = 'T' (filter lookup rekening bank)
    - account_type = 'I' AND parent akun '310301' (filter lookup GL Account di item)
    - transactionitemtype = 'G' untuk GLTransactionItem (item pendapatan)
    - transactionitemtype = 'A' untuk AccountTransactionItem (item kas/bank)
    - mutationtype = 'C' untuk sisi pendapatan (GLTransactionItem)
    - mutationtype = 'D' untuk sisi kas/bank (AccountTransactionItem)
    - parameterjournalid = '10' (semua item standar)
    - parameterjournalid = 'C20' (AccountTransactionItem source account saat BankIn)
    - channelcode = 'R' untuk Kas Cabang/Bank, 'P' untuk Kas Kecil
    - entity_type = 'amil_income' (otorisasi dispatcher)

→ nuwis-ui-builder:
  PAGE_TYPE: form
  NAMA VUE: AmilIncomePage.vue (atau AmilIncomeFormPage.vue)
  ROUTE: /keuangan/transaksi/penerimaan-amil

  FIELDS:
    Header:
      - actual_date        : DateField.vue [Required] — Tanggal Posting
      - payment_type       : Tab/Radio — Kas / Bank (default: Bank)
      - paid_to            : Input [Optional] — Kasir (pre-fill dari session username)
      - received_from      : Input [Optional] — Terima Dari
    Saat payment_type = Bank:
      - bank_account_no    : SearchSelect.vue [Required] — Rekening Bank (endpoint: GET /api/transaction/bank-accounts/amil)
      - reference_no       : Input [Optional] — No. Cek
      - description        : Input [Optional] — Keterangan
      - rate               : Input number [Optional, default 1.0] — Nilai Kurs
    Saat payment_type = Kas (Cabang / Kecil):
      - cash_type          : Select [Required] — 'C'=Kas Cabang, 'K'=Kas Kecil (default 'C')
      - reference_no       : Input [Optional] — No. Kwitansi
      - description        : Input [Optional] — Keterangan
    Grid Detail (minimal 1 row):
      - account_code       : Lookup / Input [Required] — Account No (pilih dari GET /api/transaction/gl-accounts?filter=amil-income)
      - account_name       : Input ReadOnly — Name Account
      - amount             : Input number [Required, > 0] — Nilai
      - cash_account_no    : SearchSelect.vue [Optional] — Rek. Sumber
      - cash_account_name  : Input ReadOnly — Nama Rek. Sumber
      - description        : Input [Optional] — Keterangan per item
      - fund_product_code  : SearchSelect.vue [Optional] — Sumber Dana
      - fund_product_name  : Input ReadOnly — Nama Sumber Dana
    Footer ReadOnly:
      - transaction_no     : Input ReadOnly — Nomor Transaksi (kosong sebelum save)
      - total_amount       : Computed dari sum(items[].amount) — Total Amount

  FILTERS (halaman list):
    - date_from, date_to (DateField.vue)
    - branch_code (hanya jika branch_access='all')

── GAP / CATATAN IMPLEMENTASI ──────────────────────────────────
1. Tab Non Tunai (Aktiva, PaymentType='A') — TabVisible=false di legacy.
   REKOMENDASI: tidak diimplementasi di MVP isf-app. Jika diperlukan, buka
   sebagai phase 2.

2. Batch TransactionBatch — di legacy ada sistem batching per user per tanggal.
   Di isf-app, batch tidak di-expose ke UI. Pada implementasi service.py, batch
   perlu di-handle internal (GetOrCreateBatch per userId+date+branchCode).

3. Kwitansi cetak — di legacy: GetKwitansi() menghasilkan file .doc via Voucher module.
   Di isf-app: implementasi cetak/print receipt sebagai fitur terpisah (phase 2).
   Response API cukup kembalikan transaction_no.

4. FundAccountNo resolve fallback:
   fCashIn_data.py baris 127-138 — jika CashAccountNo diisi tapi FundAccountNo kosong,
   auto-resolve dari ProductAccount (ProductId, BranchCode, CurrencyCode).
   Service.py harus mengimplementasikan logika ini.

5. Budget reference — kolom BudgetCode/BudgetId/BudgetOwner di grid item bersifat hidden
   di legacy. REKOMENDASI: tidak diimplementasi di MVP, simpan sebagai nullable.

6. file FinancialAccount.py di script_modules bisa dibaca untuk memahami tabel CASHACCOUNT
   lebih dalam jika diperlukan (tidak dibaca dalam sesi ini karena tidak referenced langsung
   dari CashIn flow).

==== END MIGRATION_ANALYSIS ====

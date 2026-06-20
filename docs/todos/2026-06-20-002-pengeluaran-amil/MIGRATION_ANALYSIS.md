==== MIGRATION_ANALYSIS ====

MODUL:   docs/legacy-apps/core/
PORTAL:  zakat
SCOPE:   Transaksi Pengeluaran Amil (Cash-Out Amil) — form input transaksi
TANGGAL: 2026-06-20

── FITUR LIST ──────────────────────────────────────────────────
  1. Transaksi Pengeluaran Amil
     ROLES:           ACC
     DIALOG:          dialogs/Transaksi/fCashOut.*
     MENU_KEY_KANDIDAT: finance.transactions.amil_expense

     Sumber:
       Transaksi.mnu baris 296-300:
         Name='TR0024B'
         Caption='Transaksi Pengeluaran Amil...'
         OnClick='ShowFormClick'
         AllowedGroups='ACC'
         StringTag='Transaksi/fCashOut'

  2. Laporan Pengeluaran Amil (report — prioritas sekunder)
     ROLES:           ADM, KEU, ACC, SPVKEU, QAC, SPVACC
     DIALOG:          dialogs/Report/fCashOutReport.*
     MENU_KEY_KANDIDAT: finance.report.amil_expense

     Sumber:
       Transaksi.mnu baris 481-485:
         Name='TR0030'
         Caption='Pengeluaran Amil'
         OnClick='ShowReportClick'
         AllowedGroups='ADM;KEU;ACC;SPVKEU;QAC;SPVACC'
         StringTag='fCashOutReport'

     Catatan: Role 'QAC' dan 'SPVACC' tidak ada di tabel mapping role ISF-App.
     Status: AMBIGU — laporkan ke nuwis-architect. Kemungkinan besar QAC=AUDIT,
     SPVACC=SPVKEU tetapi harus dikonfirmasi.

── FORM FIELDS (per dialog) ────────────────────────────────────
DIALOG: dialogs/Transaksi/fCashOut

HEADER PANEL (pBatch) — data umum transaksi:
FIELDS:
  - TransactionNo   : String [ReadOnly]  — Nomor Transaksi (auto-generate)
  - ActualDate      : Date   [Required]  — Tanggal Posting
  - Inputer         : String [ReadOnly]  — dari session (config.SecurityContext.UserId)
  - ReceivedFrom    : String [Optional]  — Kasir (label: "Kasir", default = UserId)
  - PaidTo          : String [Optional]  — Penerima

HIDDEN FIELDS (disimpan ke DB, tidak tampil di form utama):
  - BranchCode      : String [ReadOnly]  — dari session (GetUserInfo()[4])
  - TransactionDate : Date   [ReadOnly]  — tanggal hari ini (config.Now())
  - FloatTransactionDate : Double [ReadOnly] — integer representation of today
  - Rate            : Double [ReadOnly]  — default 1.0
  - TotalAmount     : Double [ReadOnly]  — total dihitung otomatis dari item rows
  - PaymentType     : String [Hidden]    — 'K'=Kas Kecil, 'C'=Kas Cabang, 'B'=Bank, 'A'=Non Tunai;
                                           ditentukan dari tab aktif saat save
  - PeriodId        : Integer [Hidden]   — (field terdaftar, tidak diisi di FormSetDataEx CashOut)
  - SaveMode        : Integer [Hidden]   — internal (1=Simpan & Lanjut, 2=Simpan & Tutup)
  - ShowMode        : Integer [Hidden]   — 1=Insert, lainnya=Edit
  - DefaultCurrency : String [Hidden]    — dari SysVar OPTION.DefaultCurrency
  - DefaultCurrencyName : String [Hidden] — dari SysVar OPTION.DefaultCurrencyName
  - LBatch.BatchId/BatchNo : [Hidden]    — batch transaksi harian

DELTA vs fCashIn:
  Header fCashOut memiliki field 'PaidTo' (Penerima) yang wajib, sedangkan fCashIn
  memiliki 'ReceivedFrom' (Terima Dari). Keduanya ada di kedua form, tetapi label
  bertukar signifikansi: di CashOut, 'PaidTo' = penerima dana (yang dibayar), sementara
  'ReceivedFrom' berubah label menjadi 'Kasir' (orang yang mengeluarkan kas).
  Sumber: fCashOut.dfr pBatch section baris 1146-1160.

TAB KAS (pCashTransaction — PaymentType = 'C' atau 'K') — DEFAULT ACTIVE:
FIELDS:
  - CashType        : String [Required]  — 'K'=Kas Kecil, 'C'=Kas Cabang (default='K')
  - LPettyCash (AccountNo) : Lookup [Optional] — Nama Kas (tampil saat CashType='K',
                                                   filter: seluruh PettyCash)
  - LCurrency (Currency_Code) : Lookup [Optional] — Kode Valuta (tampil saat CashType='C')
  - ReferenceNo     : String [Optional]  — No. Kwitansi
  - Description     : String [Optional]  — Keterangan
  - Rate            : Double [Optional]  — Nilai Kurs

  DELTA vs fCashIn:
  - fCashOut default tab aktif = pgCash (Kas), bukan pgBank seperti fCashIn.
    Sumber: fCashOut_intr.py baris 71: uipTran.CashType = 'K' (set di InsertMode Show).
  - fCashOut tab Kas menampilkan LPettyCash + LCurrency (toggle), bukan hanya CashType.
  - fCashOut PettyCash perlu pilih rekening kas kecil secara eksplisit (LPettyCash lookup).
  - Tidak ada filter IsAmilAccount di lookup PettyCash (berbeda dari LBank di fCashIn).

TAB BANK (pBankTransaction — PaymentType = 'B'):
FIELDS:
  - LBank (AccountNo) : Lookup [Required] — Rekening Bank
                                            OQL: [Status = 'A' and BranchCode = :BranchCode]
                                            TIDAK ada filter IsAmilAccount='T'
  - ReferenceNo     : String [Optional]  — No. Cek
  - Description     : String [Optional]  — Keterangan
  - Rate            : Double [Optional]  — Nilai Kurs (default 1.0)

  DELTA vs fCashIn — KRITIS:
  fCashOut LBank OQL TIDAK memfilter IsAmilAccount='T'.
  fCashIn LBank OQL: [Status = 'A' and BranchCode = :BranchCode and IsAmilAccount='T']
  fCashOut LBank OQL: [Status = 'A' and BranchCode = :BranchCode] (tanpa IsAmilAccount filter)
  Sumber: fCashOut.dfr baris 305-316 (pBankTransaction Elements).
  Artinya: untuk pengeluaran amil, semua rekening bank cabang bisa dipilih
  (bukan hanya rekening yang ditandai amil). Ini berbeda dari penerimaan.

TAB NON TUNAI/AKTIVA (pAssetTransaction — PaymentType = 'A', hidden tab):
FIELDS:
  - LAsset (Account_Code) : Lookup [Required] — Rekening Aktiva
                            OQL: Account [Is_Detail = 'T' and (Account_Code llike '14%'
                                 or Account_Code llike '15%' or Account_Code llike '16%')]
  - LValuta (Currency_Code) : Lookup [Required] — Kode Valuta
  - ReferenceNo     : String [Optional]  — No. Referensi / FSZ
  - Description     : String [Optional]  — Keterangan
  - Rate            : Double [Optional]  — Nilai Kurs

  Catatan: TabVisible=false di legacy — tidak perlu diimplementasi untuk MVP.

GRID DETAIL (uipTransactionItem — multi-row, sama untuk semua tab kas/bank):
  Kolom yang TAMPIL (dari gBankTransactionItem dan gCashTransactionItem):
  - AccountCode     : String [Required]  — Account No
                      (lookup via fSelectAccount,
                       filter: fl_cpa_AccountCode='310301' AND account_type='X')
  - AccountName     : String [ReadOnly]  — Name Account (auto dari lookup AccountCode)
  - Amount          : Double [Required]  — Nilai (> 0.0)
  - Description     : String [Optional]  — Keterangan
  - BudgetCode      : String [Optional]  — Kode Budget (lookup via fSelectBudgetCode)
  - BudgetOwner     : String [ReadOnly]  — Pemilik Budget (auto dari Budget lookup)

  DELTA vs fCashIn — KRITIS:
  - fCashIn grid memiliki kolom CashAccountNo, FundProductCode, FundProductName.
    fCashOut grid TIDAK memiliki kolom-kolom ini sama sekali.
  - fCashIn filter akun GL: account_type='I' (Income). fCashOut: account_type='X' (Expense).
    Sumber: fCashOut_intr.py baris 109:
      GetAccount(" and fl_cpa_AccountCode ='310301' and account_type='X' ")
  - account_type='X' = Expense account (Debit-positive, P&L category).
    Berbeda dari 'I' (Income, Kredit-positive) di fCashIn.
    Sumber: script_modules/accountingapi.py baris 1535-1536 (IsDebetPositive includes 'X').
  - fCashOut tidak memiliki kolom LCurrency di gBankTransactionItem (beda dari fCashIn).
    Valuta untuk BankOut diambil langsung dari CurrencyCode rekening bank, bukan per item.

  Kolom HIDDEN di grid (tersimpan ke DB):
  - FundEntity      : Integer [Hidden]   — Jenis Dana (1-9, enum di dfr)
  - PercentageOfAmil : Double [Hidden]   — tidak diisi dari UI
  - Unit            : Integer [Hidden]
  - AmountPerUnit   : Double [Hidden]
  - BudgetId        : Integer [Hidden]   — dari lookup BudgetCode
  - ItemIdx         : Integer [Hidden]   — urutan item (auto-increment)
  - Rate            : Double [Hidden]    — default 1.0
  - Ekuivalen       : Double [Hidden]    — Amount * Rate (auto-calculate di ItemBeforePost)
  - LCurrency.Currency_Code : String [Hidden] — valuta per item (default = DefaultCurrency)
    (hanya di gCashTransactionItem, tidak di gBankTransactionItem)

SECTIONS:    Header (pBatch), PaymentType toggle, Tab Kas/Bank/NonTunai, Grid Detail
READ_ONLY:   TransactionNo, Inputer, TotalAmount, AccountName
HIDDEN:      PaymentType, PeriodId, SaveMode, ShowMode, DefaultCurrency, DefaultCurrencyName,
             FloatTransactionDate, FundEntity, BudgetId, BudgetOwner, ItemIdx, Ekuivalen

Sumber: fCashOut.dfr, fCashOut_intr.py

── UI FLOW ─────────────────────────────────────────────────────
ON OPEN (FormSetDataEx — fCashOut_data.py baris 37-65):
  - Inputer          ← config.SecurityContext.UserId
  - ReceivedFrom     ← sama dengan Inputer (label "Kasir")
  - BranchCode       ← config.SecurityContext.GetUserInfo()[4]
  - TransactionDate  ← config.Now() (integer timestamp)
  - ActualDate       ← sama dengan TransactionDate
  - FloatTransactionDate ← config.Now()
  - Rate             ← 1.0
  - TotalAmount      ← 0.0
  - CashType         ← 'C' (Kas Cabang) — default field; namun Show() mode=1 override ke 'K'
    DELTA: fCashOut_intr.py baris 71 set CashType='K' dan SetCashType('K') di insert mode.
    Artinya: default tab aktif fCashOut adalah TAB KAS (bukan Tab Bank seperti fCashIn).
  - TransactionNo    ← '<AUTOGENERATED>' (placeholder, diisi saat save)
  - DefaultCurrency  ← dari SysVar OPTION.DefaultCurrency
  - DefaultCurrencyName ← dari SysVar OPTION.DefaultCurrencyName
  - LValuta.Currency_Code ← DefaultCurrency

ON SAVE (Simpan() — fCashOut_intr.py baris 230-280):
  VALIDASI CLIENT-SIDE (sebelum CallServerMethod):
  1. FormObject.CommitBuffer() — flush semua perubahan grid
  2. CheckRequiredGeneral(): uipTransactionItem.RecordCount > 0 (minimal 1 item)
  3. Konfirmasi dialog: "Yakin simpan transaksi ?"
  4. Menentukan PaymentType dari tab aktif:
     - Tab 0 (Kas) → PaymentType = CashType ('K' atau 'C')
     - Tab 1 (Bank) → PaymentType = 'B' + CheckRequiredBank (LBank.AccountNo harus terisi)
     - Tab 2 (Non Tunai) → PaymentType = 'A' + CheckRequiredAsset (LAsset.Account_Code
       dan LValuta.Currency_Code harus terisi)
  5. CallServerMethod("SimpanData", ph) → ke fCashOut_data.SimpanData
  6. Jika IsErr=1: tampilkan ErrMessage
  7. Jika IsErr=0/2: tampilkan nomor transaksi; tawarkan cetak kwitansi

  VALIDASI CLIENT-SIDE di GRID (ItemBeforePost — fCashOut_intr.py baris 146-167):
  - AccountCode tidak boleh kosong/None/0
  - Amount > 0.0
  - Ekuivalen = Amount * Rate (dihitung otomatis)

  ExecuteScript calls: TIDAK ADA ExecuteScript langsung.
  SimpanData dipanggil via CallServerMethod("SimpanData", ph).

── SAVE LOGIC ──────────────────────────────────────────────────
ENTRY:   dialogs/Transaksi/fCashOut_data.py → SimpanData()
         → modman.getModule(config, 'scripts#Transaction.CashOut')
         → CashOutNew() atau CashOutUpdate() berdasarkan ShowMode

---
ALUR CashOutNew (scripts/Transaction/CashOut.py baris 15-56):

  1. Ambil/buat TransactionBatch untuk hari ini:
     scripts/Transaction/Batch.py → GetBatchUser(config, ActualDate)
     - Sama dengan fCashIn

  2. Buat Transaction baru:
     oBatch.NewTransaction('CO')
     - INSERT ke transaction.TRANSACTION
     - TransactionCode = 'CO'  ← DISCRIMINATOR UTAMA
     - AuthStatus = 'F' (belum otorisasi)
     Sumber: CashOut.py baris 25

  3. Buat riwayat perubahan:
     helper.CreatePObject('TransHistoryOfChanges')
     - INSERT ke transaction.TRANSHISTORYOFCHANGES
     - SetAsNew() (ChangeType = 'I')

  4. Dispatch berdasarkan PaymentType:
     - 'K' (Kas Kecil)  → PettyCashOut()
     - 'C' (Kas Cabang) → BranchCashOut()
     - 'B' (Bank)       → BankOut()
     - 'A' (Non Tunai)  → raise Exception 'Jenis Pembayaran Tidak Terdaftar'
       (tidak diimplementasi, sama seperti fCashIn)

  PERBEDAAN JURNAL DENGAN fCashIn (DELTA KRITIS):

  fCashIn (Penerimaan):
    GL item:    SetMutation('C', amount, rate) → sisi Kredit (Pendapatan)
    Account item: SetMutation('D', totalAmount, rate) → sisi Debit (Kas/Bank masuk)
    Artinya: Debit Kas/Bank | Kredit Pendapatan Amil

  fCashOut (Pengeluaran):
    GL item:    SetMutation('D', amount, rate) → sisi Debit (Beban/Expense)
    Account item: SetMutation('C', totalAmount, rate) → sisi Kredit (Kas/Bank keluar)
    Artinya: Debit Beban Amil | Kredit Kas/Bank

  Sumber: CashOut.py baris 141 (PettyCashOut), 208 (BranchCashOut), 288 (BankOut)
  semua menggunakan SetMutation('D', ...) untuk GL item.
  CashOut.py baris 162 (PettyCashOut), 229 (BranchCashOut), 304 (BankOut)
  semua menggunakan SetMutation('C', ...) untuk AccountTransactionItem.

  Untuk setiap PaymentType, logika umum:
    a. Set field-field Transaction: Inputer, BranchCode, ReferenceNo, Description,
       ChannelCode, CurrencyCode, Rate, PaidTo, ReceivedFrom, ActualDate
    b. Loop items dari request['Items']:
       - CreateGLTransactionItem(AccountCode, Valuta)
         → INSERT transaction.TRANSACTIONITEM (TransactionItemType='G')
         → oItemGL.SetMutation('D', amount, rate) → MutationType='D' (Debit)
         → oItemGL.SetJournalParameter('10')
       - Jika BudgetId != 0: CreateBudgetTransaction
       - Tambah totalAmount
    c. Set oTran.Amount = totalAmount
    d. Buat AccountTransactionItem untuk rekening kas/bank (sisi Kredit):
       - CreateAccountTransactionItem(oAccount)
         → INSERT transaction.TRANSACTIONITEM (TransactionItemType='A')
         → INSERT transaction.ACCOUNTTRANSACTIONITEM
         → oItemBA.SetMutation('C', totalAmount, rate) → MutationType='C' (Kredit)
         → oItemBA.SetJournalParameter('10')
    e. GenerateTransactionNumber(CashCode)
       Format: KK-{YYYY}-{branchCode}-{cashCode}-{7digit}
       (VoucherCode='KK' untuk TransactionCode='CO', dari TransactionHelper)
       Sumber: TransactionHelper.py baris 35: 'CO' : 'KK'
    f. SaveInbox(params) → INSERT transaction.INBOX + INBOXTRANSACTION
    g. GetKwitansi() → generate file kwitansi

  PERBEDAAN PER PAYMENT TYPE:

  PettyCashOut (baris 109-172):
    - ChannelCode = 'P'
    - CurrencyCode hardcoded 'IDR'
    - Rate = 1 (hardcoded)
    - LPettyCash harus dipilih eksplisit (tidak ada default)
    - oItemPC: CreateAccountTransactionItem(oPettyCash) → Kredit Kas Kecil

  BranchCashOut (baris 174-239):
    - ChannelCode = 'R'
    - CurrencyCode dari SysVar OPTION.DefaultCurrency
    - oBranchCash: lookup via BranchCode + CurrencyCode (dari valuta item pertama)
    - oItemBC: CreateAccountTransactionItem(oBranchCash) → Kredit Kas Cabang

  BankOut (baris 241-310):
    - ChannelCode = 'R'
    - CurrencyCode dari rekening bank (oBankAccount.CurrencyCode)
    - Lookup rekening: helper.GetObject('BankCash', BankAccountNo) — tanpa filter IsAmilAccount
    - oItemBA: CreateAccountTransactionItem(oBankAccount) → Kredit Bank
    - TIDAK ada CashAccountNo/FundAccountNo logic (berbeda dari BankIn fCashIn)
    - TransactionNo di-generate SEBELUM loop items (berbeda urutan dari BankIn fCashIn)
    - ParameterJournalId = '10' untuk AccountTransactionItem (sama; tidak ada 'C20')

  5. Cek limit otorisasi:
     corporate.CheckLimitOtorisasi(request['Amount'] * request['Rate'])
     - Jika nominal <= limit['O']: oTran.AutoApproval() → AuthStatus = 'T'
     - Jika nominal > limit['O']: AuthStatus tetap 'F' (perlu otorisasi manual)

  6. CreateJournal():
     - Hanya berjalan jika AutoApproval berhasil
     - Mengirim data jurnal ke accounting subsystem
     - Jika berhasil: IsPosted='T', set JournalBlockId, JournalNo
     - status==2 → raise Exception (jurnal gagal)

  7. Commit jika semua sukses; Rollback jika ada exception.

ALUR CashOutUpdate (CashOut.py baris 58-107):
  - Ambil Transaction existing by TransactionNo
  - DeleteTransactionJournal → oTran.DeleteJournal()
  - CancelTransaction() → IsPosted='F', delete semua TransactionItems
  - Re-run PettyCashOut/BranchCashOut/BankOut dengan data baru
  - AutoApprovalUpdate(): jika sebelumnya sudah otorisasi, approve ulang
  - CreateJournal() ulang

── SCHEMA DB ───────────────────────────────────────────────────
ENTITIES: Identik dengan fCashIn — tidak ada tabel baru.

  - Transaction → tabel: transaction.TRANSACTION
    kolom penting: transactionid, transactiondate, actualdate, referenceno,
    description, inputer, transactioncode ('CO'), branchcode, authstatus,
    isposted, channelcode ('R'/'P'), amount, currencycode, paidto,
    receivedfrom, rate, transactionno, journalblockid, journalno

  - TransactionBatch → tabel: transaction.TRANSACTIONBATCH
    (sama dengan fCashIn)

  - TransactionItem (base) → tabel: transaction.TRANSACTIONITEM
    kolom: transactionitemid, transactionid, branchcode, currencycode,
    mutationtype ('D' untuk GL item / 'C' untuk Account item),
    amount, rate, ekuivalenamount, transactionitemtype ('G'=GL / 'A'=Account),
    description, refaccountno, refaccountname, accountcode, parameterjournalid='10'

  - AccountTransactionItem → tabel: transaction.ACCOUNTTRANSACTIONITEM
    (sama dengan fCashIn, mutationtype='C' untuk Cash-Out)

  - TransHistoryOfChanges → tabel: transaction.TRANSHISTORYOFCHANGES
    (sama dengan fCashIn)

  - PettyCash / BranchCash / BankCash → tabel: transaction.CASHACCOUNT
    (sama dengan fCashIn; BankOut TIDAK filter IsAmilAccount='T')

RELASI: Identik dengan fCashIn.

── DISCRIMINATORS ──────────────────────────────────────────────
KRITIS — jangan hilangkan saat implementasi:

  1. TransactionCode = 'CO'
     Tabel: transaction.TRANSACTION kolom transactioncode
     Artinya: Cash Out Amil (Transaksi Pengeluaran Amil)
     FROZEN — tidak boleh diubah.
     Membedakan dari: 'CI'=Cash In Amil, 'SD001'=Penghimpunan, 'DD001'=Penyaluran, dll.
     Sumber: CashOut.py baris 25; fCashOut_data.py (dcpy) GenerateTransactionNumber baris 64.

  2. VoucherCode = 'KK' (dari tabel TransactionType di-lookup via TransactionCode='CO')
     Tabel: transaction.TRANSACTIONTYPE kolom vouchercode
     Artinya: Kas Keluar — digunakan sebagai PREFIX nomor transaksi
     Format nomor: KK-{YYYY}-{branchCode}-{cashCode}-{7digit}
     Contoh: KK-2026-001-IDR-0001234
     Sumber: scripts/Transaction/TransactionHelper.py baris 35: 'CO' : 'KK'

  3. IsAmilAccount = TIDAK DIFILTER untuk lookup rekening bank di LBank
     DELTA KRITIS: fCashOut LBank filter hanya [Status='A' and BranchCode=:BranchCode]
     — tidak ada IsAmilAccount='T'.
     Implikasi: endpoint GET /api/transaction/bank-accounts/amil-expense TIDAK perlu
     filter IsAmilAccount='T'. Atau reuse endpoint bank-accounts biasa (non-amil).
     Sumber: fCashOut.dfr baris 305-316.

  4. account_type = 'X' (untuk lookup GL Account di grid item)
     Artinya: Akun Expense (Beban/Pengeluaran Amil), Debit-positive, kategori P&L.
     Berbeda dari fCashIn yang menggunakan account_type='I' (Income, Kredit-positive).
     Filter lengkap: fl_cpa_AccountCode='310301' AND account_type='X'
     Sumber: fCashOut_intr.py baris 109.
     Cross-check accounthierarchy report: filter '55','514000','524000' di fCashOutReport_data.py baris 178.

  5. GLTransactionItem.MutationType = 'D' (Debit) untuk item-item GL (Beban)
     AccountTransactionItem.MutationType = 'C' (Kredit) untuk rekening kas/bank
     Artinya: Pengeluaran = sisi beban Debit, sisi kas/bank Kredit
     BERLAWANAN DENGAN fCashIn (CashIn: GL='C', Account='D')
     Sumber: CashOut.py baris 141, 162, 208, 229, 288, 304.

  6. ChannelCode = 'R' untuk BranchCashOut dan BankOut, 'P' untuk PettyCashOut
     Tabel: transaction.TRANSACTION kolom channelcode
     (sama dengan fCashIn)

  7. ParameterJournalId = '10' untuk semua item (GL Debit dan Account Kredit)
     Tidak ada 'C20' — fCashOut tidak punya CashAccountNo source item logic.
     Sumber: CashOut.py baris 143, 165, 210, 231, 290, 306.

  8. AuthStatus = 'F' → 'T' (auto-approval jika <= limit user)
     (sama dengan fCashIn)

  9. Report discriminator (fCashOutReport_data.py baris 78):
     WHERE t.transactioncode = 'CO' AND i.mutationtype='D'
     Artinya: laporan hanya mengambil GL items (Debit = beban amil yang dikeluarkan).
     Ini mirror dari fCashIn report yang filter mutationtype='C'.

── CATATAN FORMAT NOMOR TRANSAKSI ──────────────────────────────
Format: {VoucherCode}-{YYYY}-{branchCode}-{cashCode}-{seq7digit}

Contoh untuk BranchCashOut cabang 001, rekening kas cabang IDR:
  KK-2026-001-IDR-0001234

Dimana cashCode berasal dari:
  - BranchCashOut: oBranchCash.CashCode (dari rekening kas cabang)
  - BankOut:       oBankAccount.CashCode (dari rekening bank)
  - PettyCashOut:  oPettyCash.CashCode (dari rekening kas kecil yang dipilih)

VoucherCode='KK' didapat dari TransactionType dimana TransactionCode='CO'.
Sumber: scripts/Transaction/TransactionHelper.py baris 35.

── ISF-APP: MAPPING KE OTORISASI ──────────────────────────────
Form ini memiliki flow otorisasi (maker-checker) bawaan DAF legacy:
  - AutoApproval jika nominal <= limit['O'] user
  - Jika di atas limit: AuthStatus='F', perlu supervisor approve

REKOMENDASI untuk isf-app:
  - entity_type: 'amil_expense' (kandidat baru, belum terdaftar di dispatcher)
  - Gunakan endpoint save-and-submit (langsung PENDING)
  - Limit check via otorisasi.entity_config
  - Dispatcher: amil_expense_service.create_from_payload()

── KOMPLEKSITAS ────────────────────────────────────────────────
LEVEL:    SEDANG
ALASAN:
  - Sama dengan fCashIn: 2 tabel utama + 2 subtype
  - 3 payment type dengan logika berbeda
  - Auto-generate nomor transaksi
  - Dual-mode save (insert vs update)
  - Jurnal akuntansi via subsystem terpisah
  - Auto-approval berdasarkan limit user
  - LEBIH SEDERHANA dari fCashIn: tidak ada CashAccountNo/FundProduct logic di grid
  - Grid item lebih sederhana: hanya AccountCode, Amount, Description, BudgetCode
WORKFLOW: Approval (maker-checker dengan auto-approval)

JUMLAH DIALOG TERKAIT: 1 dialog utama (fCashOut) + 2 dialog lookup sub:
  - fSelectAccount (lookup GL expense account)
  - fSelectBudgetCode (lookup budget)
  Total 3 dialog — lebih sedikit dari fCashIn (5 dialog).
  Model sonnet cukup untuk analisis ini.

── HANDOFF ─────────────────────────────────────────────────────
→ nuwis-seed-gen:
  MENU_KEY: finance.transactions.amil_expense
  LABEL:    Transaksi Pengeluaran Amil
  ROLES:    ACC

  MENU_KEY: finance.report.amil_expense
  LABEL:    Pengeluaran Amil
  ROLES:    ADM, KEU, ACC, SPVKEU
  (QAC dan SPVACC AMBIGU — konfirmasi ke nuwis-architect sebelum seed)

→ nuwis-db-migrator:
  MIGRATIONS:
    - Tidak ada tabel baru — data masuk ke schema transaction.* yang sudah ada
    - Pastikan transaction.TRANSACTIONTYPE berisi row TransactionCode='CO', VoucherCode='KK'
    - Pastikan transaction.CASHACCOUNT punya rekening kas kecil (PettyCash) untuk cabang
    - Tidak perlu constraint IsAmilAccount untuk Cash-Out
  DWH_VIEWS:
    - Jika diperlukan laporan: dwh.v_amil_expense menggunakan filter
      transactioncode='CO', transactionitemtype='G', mutationtype='D'
    - Kolom tambahan untuk laporan: accounthierarchy filter '55'/'514000'/'524000'
      (dari fCashOutReport_data.py baris 178-180)

→ nuwis-python-builder:
  Referensi implementasi: apps_zakat/api-python/app/modules/transaction/amil_income_service.py
  ENDPOINTS:
    POST /api/transaction/amil-expense/
      Body: { actual_date, reference_no, description, payment_type,
              bank_account_no, petty_cash_account_no, cash_type, rate,
              paid_to, received_from,
              items: [{ account_code, account_name, amount, valuta, rate,
                        description, budget_id }] }
      Logic: amil_expense_service.create_amil_expense() →
        1. Resolve branch dari session
        2. Validate items tidak kosong
        3. Validate bank_account_no jika payment_type='B' (filter: status='A', branchcode=branch)
           CATATAN: tidak perlu filter isamilaccount='T' untuk Cash-Out
        4. Generate transaction_no format KK-{YYYY}-{branch}-{cashCode}-{seq}
        5. INSERT transaction.transaction (transactioncode='CO')
        6. INSERT transaction.transactionitem per item
           (transactionitemtype='G', mutationtype='D', parameterjournalid='10')
        7. INSERT transaction.transactionitem + transaction.accounttransactionitem
           untuk kas/bank (mutationtype='C', parameterjournalid='10')
        8. Dispatch via otorisasi (entity_type='amil_expense')

    GET /api/transaction/amil-expense/
      Query params: date_from, date_to, branch_code, page, limit
      Filter: transactioncode='CO'

    GET /api/transaction/amil-expense/{transaction_no}
      Detail transaksi beserta items

    PUT /api/transaction/amil-expense/{transaction_no}
      Update: delete items lama, insert ulang (CashOutUpdate pattern)

    GET /api/transaction/bank-accounts/
      Daftar rekening bank aktif untuk branch user (TANPA filter isamilaccount)
      Atau reuse endpoint yang sudah ada jika tersedia.
      Catatan: berbeda dari amil-income yang butuh /bank-accounts/amil

    GET /api/transaction/petty-cash-accounts/
      Daftar rekening kas kecil (PettyCash) untuk branch user
      Dipakai untuk dropdown LPettyCash di form saat CashType='K'

    GET /api/transaction/gl-accounts?filter=amil-expense
      Daftar akun GL expense (account_type='X', parent '310301')
      Berbeda dari amil-income yang filter account_type='I'

  DISCRIMINATORS (wajib diteruskan ke implementasi):
    - transactioncode = 'CO'
    - vouchercode = 'KK' (untuk format nomor transaksi KK-YYYY-branch-cash-seq)
    - account_type = 'X' (filter lookup GL Account di item — EXPENSE, bukan 'I' Income)
    - parent_account = '310301' (filter parent akun untuk expense amil)
    - transactionitemtype = 'G' untuk GLTransactionItem (item beban)
    - transactionitemtype = 'A' untuk AccountTransactionItem (item kas/bank)
    - mutationtype = 'D' untuk sisi beban (GLTransactionItem) — BERLAWANAN DARI amil_income
    - mutationtype = 'C' untuk sisi kas/bank (AccountTransactionItem) — BERLAWANAN DARI amil_income
    - parameterjournalid = '10' (semua item, tidak ada 'C20')
    - channelcode = 'R' untuk Kas Cabang/Bank, 'P' untuk Kas Kecil
    - entity_type = 'amil_expense' (otorisasi dispatcher — perlu didaftarkan)
    - Tidak ada filter IsAmilAccount untuk lookup rekening bank/kas

→ nuwis-ui-builder:
  PAGE_TYPE: form
  NAMA VUE: AmilExpensePage.vue (atau AmilExpenseFormPage.vue)
  ROUTE: /finance/transactions/amil-expense

  Referensi implementasi sibling: apps_zakat/web-vue/src/pages/finance/amil-income/

  FIELDS:
    Header:
      - actual_date        : DateField.vue [Required] — Tanggal Posting
      - payment_type       : Tab/Radio — Kas / Bank (default: KAS, bukan Bank)
                             DELTA: default tab = Kas, bukan Bank seperti amil-income
      - received_from      : Input [Optional] — Kasir (pre-fill dari session username)
      - paid_to            : Input [Optional] — Penerima
    Saat payment_type = Kas:
      - cash_type          : Select [Required] — 'C'=Kas Cabang, 'K'=Kas Kecil (default 'K')
      - petty_cash_account_no : SearchSelect.vue [Conditional, muncul saat cash_type='K']
                               — Nama Kas (endpoint: GET /api/transaction/petty-cash-accounts)
      - reference_no       : Input [Optional] — No. Kwitansi
      - description        : Input [Optional] — Keterangan
    Saat payment_type = Bank:
      - bank_account_no    : SearchSelect.vue [Required] — Rekening Bank
                             (endpoint: GET /api/transaction/bank-accounts — TANPA filter amil)
      - reference_no       : Input [Optional] — No. Cek
      - description        : Input [Optional] — Keterangan
      - rate               : Input number [Optional, default 1.0] — Nilai Kurs
    Grid Detail (minimal 1 row):
      - account_code       : Lookup / Input [Required] — Account No
                             (pilih dari GET /api/transaction/gl-accounts?filter=amil-expense)
                             Filter: account_type='X', parent '310301'
                             DELTA: berbeda dari amil-income yang filter account_type='I'
      - account_name       : Input ReadOnly — Name Account
      - amount             : Input number [Required, > 0] — Nilai
      - description        : Input [Optional] — Keterangan per item
      - budget_code        : SearchSelect.vue [Optional] — Kode Budget
      - budget_owner       : Input ReadOnly — Pemilik Budget (dari lookup budget)
      TIDAK ADA: cash_account_no, fund_product_code — ini delta utama dari amil-income grid
    Footer ReadOnly:
      - transaction_no     : Input ReadOnly — Nomor Transaksi (kosong sebelum save)
      - total_amount       : Computed dari sum(items[].amount) — Total Amount

  FILTERS (halaman list):
    - date_from, date_to (DateField.vue)
    - branch_code (hanya jika branch_access='all')

── GAP / CATATAN IMPLEMENTASI ──────────────────────────────────
1. entity_type 'amil_expense' belum terdaftar di otorisasi dispatcher.
   Wajib: daftarkan di otorisasi/service.py _register_defaults() sebelum live.
   KRITIKAL — tanpa ini, transaksi tidak akan pernah AUTHORIZED.

2. Tab Non Tunai (Aktiva, PaymentType='A') — TabVisible=false di legacy.
   REKOMENDASI: tidak diimplementasi di MVP isf-app. Sama seperti fCashIn.

3. Batch TransactionBatch — di legacy ada sistem batching per user per tanggal.
   Di isf-app, batch tidak di-expose ke UI. Handle internal di service.py
   (GetOrCreateBatch per userId+date+branchCode). Sama seperti amil-income.

4. Kwitansi cetak — di legacy: GetKwitansi() menghasilkan file .doc.
   Di isf-app: response cukup kembalikan transaction_no. Cetak = phase 2.

5. Budget reference — BudgetCode/BudgetId/BudgetOwner ada di grid item legacy
   dan TAMPIL (tidak hidden sepenuhnya, ada kolom BudgetCode dan BudgetOwner di grid).
   Berbeda dari fCashIn dimana budget juga ada tapi tidak terlalu prominent.
   REKOMENDASI MVP: simpan BudgetId sebagai nullable, tampilkan BudgetCode dan
   BudgetOwner di grid tapi opsional.

6. Bank account lookup perbedaan penting:
   - amil-income: GET /api/transaction/bank-accounts/amil (filter isamilaccount='T')
   - amil-expense: GET /api/transaction/bank-accounts/ (TANPA filter isamilaccount)
   Jangan reuse endpoint bank-accounts/amil untuk amil-expense — akan keliru.

7. GL Account lookup perbedaan penting:
   - amil-income: account_type='I' (Income/Pendapatan Amil, Kredit-positive)
   - amil-expense: account_type='X' (Expense/Beban Amil, Debit-positive)
   Dua endpoint terpisah atau satu endpoint dengan query param type='I'/'X'.

8. CashOut BranchCashOut mengambil valuta dari item PERTAMA (aValuta di loop terakhir
   sebelum lookup BranchCash). Ini potential bug di legacy jika multi-valuta.
   Di isf-app: gunakan DefaultCurrency dari session atau rekening kas cabang.
   Sumber: CashOut.py baris 223-224.

9. QAC dan SPVACC di AllowedGroups laporan — AMBIGU:
   Tidak ada di mapping role isf-app. Laporkan ke nuwis-architect.
   Tidak blokir implementasi form transaksi (hanya laporan).

==== END MIGRATION_ANALYSIS ====

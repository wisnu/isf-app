# MIGRATION_ANALYSIS: Piutang (Pinjam/Bayar)

**MODUL:** docs/legacy-apps/core/
**PORTAL:** zakat
**SCOPE:** Piutang — Pinjam & Bayar
**TANGGAL:** 2026-06-17

---

## Fitur List

### 1. (Pinjam/Bayar) Piutang
- **ROLES:** ACC
- **DIALOG:** dialogs/Transaksi/fAccountReceivable.*
- **MENU_KEY_KANDIDAT:** `keuangan.piutang.pinjam-bayar`
- **SUMBER:** Transaksi.mnu → AccountReceivableClick → menus/Transaksi.py → app.CreateForm('Transaksi/fAccountReceivable')

### 2. Daftar Nama Piutang Non Karyawan
- **ROLES:** SPVKEU, KEU, ACC, SPVACC
- **DIALOG:** dialogs/parameter/fDaftarExternalDebtor.*
- **MENU_KEY_KANDIDAT:** `keuangan.piutang.daftar-debitur-external`
- **TYPE:** Query/list read-only (ShowQueryClick)

### 3. Laporan Piutang pada Karyawan
- **ROLES:** ADMIN, SPVKEU, ACC, KEU, SPVACC
- **MENU_KEY_KANDIDAT:** `keuangan.laporan.piutang-karyawan`
- **CATATAN:** Kemungkinan sudah ada di isf-app — verifikasi dulu

### 4. Laporan Piutang pada Non Karyawan
- **ROLES:** ADMIN, SPVKEU, ACC, KEU, SPVACC
- **MENU_KEY_KANDIDAT:** `keuangan.laporan.piutang-non-karyawan`
- **CATATAN:** Kemungkinan sudah ada di isf-app — verifikasi dulu

> [TIDAK DIMIGRASI] fEmployeeAR — AllowedGroups=HIDDEN, sudah digantikan fAccountReceivable

---

## Workflow Type

**Approval** (via CheckLimitOtorisasi → AutoApproval atau manual otorisasi)

---

## Form Fields

**DIALOG:** dialogs/Transaksi/fAccountReceivable
**SUMBER:** fAccountReceivable.svr + .dfr + _intr.py + _data.py

| Field | Type | Required | Keterangan |
|---|---|---|---|
| ActualDate | Date | Yes | Tanggal Posting |
| TransactionNo | String | ReadOnly | Nomor Transaksi (auto-generated) |
| Casher | String | Optional | Kasir (default dari session userId) |
| ChannelType | String | Yes | Jenis Channel: C=Kas/Bank \| G=Rekening Ledger |
| LCashAccount | Link | Conditional (ChannelType=C) | Kas/Bank |
| LGLAccount | Link | Conditional (ChannelType=G) | Kode Ledger |
| LDebtor | Link | Yes | Nama Debitur (dari DEBTOR_ALL) |
| DebtorType | String | ReadOnly | Kategori Debitur: E=Karyawan \| X=Non Karyawan |
| TransactionType | String | Yes | Jenis Transaksi: P=Pinjam \| B=Bayar |
| Amount | Currency | Yes | Nominal (> 0) |
| ReferenceNo | String | Optional | Nomor Cek/Kwitansi |
| Description | String | Optional | Keterangan |

**HIDDEN (session-injected):** BranchCode, Inputer, FloatTransactionDate, TransactionDate, DebtorId, EmployeeId, EmployeeName, FundEntity (HARDCODED=4)

---

## UI Flow

### ON OPEN (mode INSERT)
- Inputer ← config.SecurityContext.UserId
- Casher ← config.SecurityContext.UserId
- BranchCode ← config.SecurityContext.GetUserInfo()[4]
- ActualDate ← config.Now()
- Amount ← 0.0
- TransactionType ← 'P' (default Pinjam)
- ChannelType ← 'C' (default Kas/Bank)
- FundEntity ← 4 (Amil — hardcoded di InitValues)

**Toggle real-time (ChannelTypeOnChange):**
- ChannelType='C' → tampil LCashAccount, sembunyikan LGLAccount
- ChannelType='G' → tampil LGLAccount, sembunyikan LCashAccount

**Lookup Debitur (fSearchDebtor popup):**
- Tab 0 = Employee → set EmployeeId, DebtorType='E'
- Tab 1 = ExternalDebtor → set DebtorId, DebtorType='X'

### ON SAVE

**Validasi client (CheckRequired):**
1. ActualDate tidak boleh 0 atau None
2. ChannelType='C' → LCashAccount.AccountNo wajib ada
3. ChannelType='G' → LGLAccount.Account_Code wajib ada
4. LDebtor.DebtorCode wajib ada
5. Amount > 0.0

Setelah validasi → ConfirmDialog → CallServerMethod("SimpanData")
→ modman.getModule(config, 'scripts#Transaction.GeneralTransaction')
→ CreateTransaction('EAR') atau CreateTransaction('PEAR')

---

## Save Logic

**ALUR (mode INSERT — EAR = Pinjam):**
1. Load JSON request params
2. config.BeginTransaction()
3. oBatch = BatchHelper.GetBatchUser(ActualDate) → batch harian otomatis
4. oTran = oBatch.NewTransaction('EAR') → INSERT ke TRANSACTION
5. ExecFunction('EAR') → AccountReceivable():
   - Set field: ReferenceNo, Description, Inputer, BranchCode, Amount, CurrencyCode, ReceivedFrom=Casher
   - ActualDate = oBatch.BatchDate (BUKAN input user langsung)
   - Lookup/Create ACCOUNTRECEIVABLE:
     - DebtorType='E' → Lookup EmployeeAccountReceivable → Jika tidak ada: CREATE (accountreceivabletype='E')
     - DebtorType='X' → Lookup ExternalAccountReceivable → Jika tidak ada: CREATE (accountreceivabletype='D')
   - oItemAR = oTran.CreateAccountTransactionItem(oAccount)
   - oItemAR.SetMutation('D', Amount, 1.0) ← Piutang DEBET
   - oItemAR.SetFundEntity(4) ← Dana Amil (hardcoded)
   - Item counter-entry (Kredit): ChannelType='C' → CashAccount; 'G' → GLAccountCode
   - GenerateTransactionNumber(CashCode, IsChangeTransactionNo)
   - SaveInbox → cek apakah perlu otorisasi
6. CheckLimitOtorisasi(Amount):
   - ≤ limit → AutoApproval() (langsung AUTHORIZED)
   - > limit → tunggu otorisasi manual
7. CreateJournal() → generate jurnal akuntansi
8. config.Commit()

**ALUR (PEAR = Bayar):**
- Sama kecuali: LOOKUP SAJA (tidak create baru) → error jika rekening belum ada
- Mutasi terbalik: AR SetMutation('C', ...), Kas SetMutation('D', ...)

**ALUR (UPDATE/Edit):**
1. GetBatch → Lookup Transaction by TransactionNo
2. DeleteTransactionJournal → hapus jurnal lama
3. CancelTransaction → set status cancelled
4. Re-execute CreateTransaction (sama dengan INSERT)
5. AutoApprovalUpdate + CreateJournal + Commit

---

## DB Schema

### Tables

**FINANCIALACCOUNT**
- accountno (PK), accountname, balance, branchcode, currencycode
- financialaccounttype ('R'=piutang), status, openingdate, accountcode

**ACCOUNTRECEIVABLE** (extends FINANCIALACCOUNT)
- inherit + accountreceivabletype ('E'|'D'|'P'), employeeidnumber, debtorid

**EXTERNALDEBTOR**
- debtorid (PK), debtorcode, branchcode, debtorname
- debtorphone, debtoraddress, description

**DEBTOR_ALL** (view: UNION Employee + ExternalDebtor)
- debtorid, debtorcode, debtorname, debtortype ('E'|'X'), branchcode

**TRANSACTION**
- transactionid (PK), transactionno, transactioncode ('EAR'|'PEAR')
- branchcode, inputer, amount, currencycode, actualdate, receivedfrom
- referenceno, description, batchid (FK→TRANSACTIONBATCH)

### Relations
- ACCOUNTRECEIVABLE.employeeidnumber → Employee (saat type='E')
- ACCOUNTRECEIVABLE.debtorid → EXTERNALDEBTOR (saat type='D')
- ACCOUNTRECEIVABLE.accountno → FINANCIALACCOUNT.accountno (shared PK)
- TRANSACTION.batchid → TRANSACTIONBATCH.batchid

---

## Discriminators

| Discriminator | Value | Arti |
|---|---|---|
| financialaccounttype | 'R' | AccountReceivable (filter piutang) |
| accountreceivabletype | 'E' | Piutang Karyawan |
| accountreceivabletype | 'D' | Piutang Non Karyawan |
| accountreceivabletype | 'P' | Piutang Realisasi Penyaluran (BUKAN modul ini) |
| transactioncode | 'EAR' | Pinjam |
| transactioncode | 'PEAR' | Bayar |
| fund_entity | 4 | Dana Amil (HARDCODED — jangan expose ke user) |
| debtortype | 'E' | Karyawan |
| debtortype | 'X' | Non Karyawan |
| channel_type | 'C' | Kas/Bank |
| channel_type | 'G' | Rekening Ledger |

---

## Business Rules

1. FundEntity selalu 4 (Dana Amil) — hardcoded, tidak bisa diubah user
2. EAR (Pinjam) → auto-create rekening piutang jika belum ada
3. PEAR (Bayar) → hanya lookup, error jika rekening belum ada
4. ActualDate yang dipakai adalah BatchDate (batch harian), bukan input langsung
5. ChannelType mengontrol field kas/ledger secara mutual exclusive
6. Amount harus > 0
7. CheckLimitOtorisasi: di bawah limit → AutoApproval; di atas → manual
8. DebtorType otomatis dari lookup (tidak bisa diubah manual)

---

## Roles/Permissions

| Menu | Roles |
|---|---|
| (Pinjam/Bayar) Piutang | ACC |
| Daftar Debitur Non Karyawan | SPVKEU, KEU, ACC, SPVACC |
| Laporan Piutang Karyawan | ADMIN, SPVKEU, ACC, KEU, SPVACC |
| Laporan Piutang Non Karyawan | ADMIN, SPVKEU, ACC, KEU, SPVACC |

---

## API Endpoints Needed

| Method | Path | Fungsi |
|---|---|---|
| POST | /api/transaction/piutang/ | Create EAR atau PEAR |
| PUT | /api/transaction/piutang/{no} | Update (delete journal + cancel + recreate) |
| GET | /api/transaction/piutang/ | List (filter: date, type P/B, debtor_type E/X) |
| GET | /api/transaction/piutang/debitur/ | Lookup DEBTOR_ALL |
| GET | /api/transaction/piutang/debitur-external/ | List ExternalDebtor |

---

## DWH Views Needed

**dwh.v_piutang_karyawan**
- JOIN: transaction + accounttransactionitem + accountreceivable (type='E') + employee
- Kolom: transactionno, transactioncode, actualdate, branchcode, inputer, amount, accountno, employeeid, employeename, accountname, balance, description, referenceno

**dwh.v_piutang_non_karyawan**
- JOIN: transaction + accounttransactionitem + accountreceivable (type='D') + externaldebtor
- Kolom: transactionno, transactioncode, actualdate, branchcode, inputer, amount, accountno, debtorid, debtorname, accountname, balance, description, referenceno

> MIGRATIONS: Tidak ada tabel baru. Verifikasi EXTERNALDEBTOR + DEBTOR_ALL view.

---

## Complexity Assessment

- **LEVEL:** SEDANG
- **ALASAN:** 3 dialog (fAccountReceivable, fEmployeeAR legacy, fSearchDebtor) — di bawah threshold 5 dialog. 1 backend script utama dengan 2 fungsi piutang (AccountReceivable + PayAccountReceivable). Logika percabangan: DebtorType × ChannelType × TransactionType = 4 kombinasi path jurnal. Auto-create rekening piutang (lazy creation). Mekanisme otorisasi terintegrasi. 1 CreateJournal call.
- **WORKFLOW:** Approval (via CheckLimitOtorisasi → AutoApproval atau manual)

---

## Migration Notes

1. Gunakan otorisasi `save-and-submit` (bukan submission/) agar langsung PENDING
2. entity_type baru: `piutang` — perlu daftarkan dispatcher di otorisasi/service.py
3. Auto-create AccountReceivable hanya untuk EAR (Pinjam), bukan PEAR (Bayar)
4. v-show (bukan v-if) untuk toggle ChannelType di UI
5. TransactionNo di-generate backend, tampilkan setelah save sukses
6. Laporan piutang (karyawan & non karyawan) sudah ada di isf-app — verifikasi dulu sebelum buat baru

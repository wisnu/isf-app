# MIGRATION_ANALYSIS — Uang Muka Kegiatan

**Portal:** Zakat
**Tanggal:** 2026-06-21
**Type:** Inquiry (read-only — tidak ada CRUD)
**Status:** ✅ Implemented

---

## Module Overview

Modul **Uang Muka Kegiatan** di legacy DAF adalah inquiry untuk melihat histori mutasi rekening uang muka karyawan. Rekening uang muka ini berbeda dari piutang karyawan biasa:

| Discriminator | Nilai | Tabel |
|---|---|---|
| `accountreceivabletype` | `'C'` | `transaction.accountreceivable` |
| `accounttitype` | `'C'` | `transaction.accounttransactionitem` |
| `cattype` | `'D'` (disbursement) | `transaction.accounttransactionitem` |
| `status` | `'A'` | `transaction.financialaccount` |

Legacy roles: `ADM;SPVKEU;KEU;ACC;QAC;SPVACC`
isf-app roles: `ADM`, `SPVKEU`, `KEU`, `ACC` (QAC/SPVACC tidak ada)

---

## Form Analysis

### 1. fEmployeeCashAdvance (Rekening/fEmployeeCashAdvance)

**Type:** Inquiry per-rekening
**isf-app page:** `CashAdvanceInquiryView.vue`
**Route:** `/finance/inquiry/cash-advance`
**Menu key:** `finance.inquiry.cash_advance`

**User flow:**
1. Pilih rekening uang muka (select dari list financialaccount WHERE accountreceivabletype='C')
2. Set rentang tanggal (BeginDate, EndDate — default: awal tahun → hari ini)
3. Klik Tampilkan → fetch histori dari accounttransactionitem
4. Tampilkan: saldo awal, tabel mutasi (Debet/Kredit/Saldo berjalan), saldo akhir
5. Export ke Excel opsional

**DB Query (fEmployeeCashAdvance_data.py):**
```sql
SELECT FROM AccountTransactionItem
WHERE AccountNo = :AccountNo
  AND LTransaction.ActualDate >= :BeginDate
  AND LTransaction.ActualDate < :EndDate
ORDER BY ActualDate ASC, TransactionItemId ASC
```

**Columns:** TransactionItemId, ActualDate, TransactionCode, MutationType, Amount, ReferenceNo, Description, Inputer, TransactionNo, AuthStatus

**Computed:** BeginningBalance via `AccountReceivable.GetBalanceByDate(BeginDate)` — diimplementasi sebagai subquery CTE di service.py

---

### 2. fListEmployeeCA (Report/fListEmployeeCA)

**Type:** Report — list transaksi multi-rekening
**isf-app page:** `ReportCashAdvanceListView.vue` ← **SUDAH ADA**
**Route:** `/finance/reports/cash-advance-list`
**Menu key:** `finance.reports.cash_advance_list`
**Status:** ✅ Already implemented

**Discriminators:**
- `ACCOUNTTITYPE = 'C'`
- `CATTYPE = 'D'` (disbursement only)

**Filter:** EmployeeId (optional), BeginDate, EndDate, ReturnStatus (S=ada LPJ, B=belum), BranchCode

---

### 3. fSummaryEmpCA (Report/fSummaryEmpCA)

**Type:** Report — rekapitulasi saldo per rekening
**isf-app page:** `ReportARSummaryView.vue` (reused) ← **SUDAH ADA**
**Route:** `/finance/reports/activity-cash-advance`
**Menu key:** `finance.reports.activity_cash_advance`
**Status:** ✅ Already implemented

**Discriminator:** `accountreceivabletype = 'C'`

**N+1 problem dari legacy:** `GetBalanceByDate()` dipanggil per baris. isf-app mengimplementasi sebagai subquery agregasi SQL, bukan per-baris ORM call.

---

## Implementation Files (baru)

### api-python
- `apps_zakat/api-python/app/modules/finance/inquiry/cash_advance/__init__.py`
- `apps_zakat/api-python/app/modules/finance/inquiry/cash_advance/schema.py`
- `apps_zakat/api-python/app/modules/finance/inquiry/cash_advance/service.py`
- `apps_zakat/api-python/app/modules/finance/inquiry/cash_advance/router.py`
- `apps_zakat/api-python/app/modules/finance/inquiry/cash_advance/export.py`

### BFF
- `apps_zakat/bff-api/app/modules/finance/inquiry.py` (extended: `ca_router`)

### Frontend
- `apps_zakat/web-vue/src/shared/constants/menu-keys.ts` (+1 key)
- `apps_zakat/web-vue/src/modules/finance/routes.ts` (+1 route)
- `apps_zakat/web-vue/src/modules/finance/menu.ts` (+1 item di Inquiry group)
- `apps_zakat/web-vue/src/modules/finance/views/inquiry/cash-advance/CashAdvanceInquiryView.vue`

### Seed
- `infra/db/migrations/seed/seed-menu-uang-muka-inquiry.sql`

---

## Apply Instructions

```bash
# Apply seed to auth DB
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/seed-menu-uang-muka-inquiry.sql

# Restart services
cd infra && podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue
```

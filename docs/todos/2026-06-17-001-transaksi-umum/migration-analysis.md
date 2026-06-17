# MIGRATION_ANALYSIS — Transaksi Umum (GT)
**Portal:** zakat  
**Tanggal:** 2026-06-17  
**Legacy file:** docs/legacy-apps/core/scripts/Transaction/GeneralTransaction.py  
**Workflow type:** Approval (Otorisasi save-and-submit)

---

## Scope

Fitur **Transaksi Umum** = General Journal Entry dengan `transactioncode = 'GT'`.
Digunakan untuk input jurnal umum manual (penyesuaian, biaya, dll).

Fitur lain dari file yang sama sudah diimplementasi terpisah:
- TI → TransferAntarRekeningPage.vue
- CA → UangMukaPenyerahanPage.vue  
- EAR/PEAR/XAR/PXAR → PiutangPage.vue

---

## Form Fields (Header)

| Field | Legacy | Tipe | Notes |
|---|---|---|---|
| `actual_date` | `request['ActualDate']` | date | dari batch date |
| `description` | `request['Description']` | text | deskripsi transaksi |
| `reference_no` | `request['ReferenceNo']` | text | nomor referensi opsional |
| `branch_code` | `request['BranchCode']` | injected | dari session |

## Form Fields (Items — G type)

| Field | Legacy | Tipe | Notes |
|---|---|---|---|
| `account_code` | `item['AccountCode']` | string | kode akun COA |
| `account_name` | `item['AccountName']` | string | nama akun COA |
| `mutation_type` | `item['MutationType']` | 'D'/'C' | Debet/Kredit |
| `amount` | `item['Amount']` | decimal | |
| `description` | `item['Description']` | text | opsional |

**Validasi kritis:** sum(Debet) == sum(Kredit) → balanced journal

---

## DB Tables

| Tabel | Operasi | Notes |
|---|---|---|
| `transaction.transaction` | INSERT | header, transactioncode='GT' |
| `transaction.transactionitem` | INSERT per item | refaccountno, refaccountname, mutationtype, amount |
| `transaction.journalblock` | INSERT | journal block |
| `transaction.journal` | INSERT | journal header |
| `transaction.journalitem` | INSERT per item | debit/credit GL entries |
| `transaction.transhistoryofchanges` | INSERT | audit trail |

---

## Discriminators

| Kolom | Nilai | Artinya |
|---|---|---|
| `transaction.transactioncode` | `'GT'` | Transaksi Umum |
| `transactionitem.transactionitemtype` | `'G'` | GL item |
| `transaction.authstatus` | `'T'`/`'A'` | Pending/Authorized |
| `journal.journal_type` | `'GT'` | General Transaction journal |

---

## Endpoints yang Diimplementasi

| Method | Path | Fungsi |
|---|---|---|
| GET | `/api/transaksi/umum` | List GT transactions |
| POST | `/api/transaksi/umum` | Create via otorisasi save-and-submit |
| GET | `/api/transaksi/umum/{id}` | Detail by transaction_id |

---

## Menu

| Key | Label | Roles |
|---|---|---|
| `keuangan.transaksi.umum` | Transaksi Umum | ACC |

---

## Files yang Dibuat

### api-python
- `transaksi_umum_schema.py`
- `transaksi_umum_service.py` (+ create_from_payload dispatcher)
- `transaksi_umum_router.py`

### BFF
- `routers/transaksi_umum.py`

### Seed
- `seed/seed-menu-transaksi-umum.sql`

### Vue
- `pages/keuangan/TransaksiUmumPage.vue`

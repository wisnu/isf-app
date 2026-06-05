# Histori Transaksi — Design Spec

**Date**: 2026-06-05  
**Status**: Approved — ready for implementation  
**Legacy ref**: `docs/legacy-apps/core/dialogs/Transaksi/fTransactionHistory`

---

## Overview

Menu pencarian histori transaksi penghimpunan ZIS. Berbeda dari "List Transaksi Umum" yang pakai DWH — fitur ini query langsung ke `transaction.transaction` sehingga real-time. Mencakup pencarian, detail dengan jurnal, hapus (dua jalur), re-posting jurnal, dan export XLSX.

**Mode SPV**: user dengan role SPVKEU melihat semua transaksi (bisa filter cabang); role lain hanya melihat transaksi milik sendiri (filter `inputer = user_id`).

---

## Architecture

```
Frontend (web-vue)
  ↕ BFF (bff-api) — session gating + inject is_spv dari session roles
    ↕ api-python (modul baru transaksi_histori)
      ↕ PostgreSQL mziss_laz — transaction.* langsung (bukan DWH)
```

Report-api tidak disentuh. Semua read + write di api-python.

---

## api-python: Modul Baru

### Lokasi: `apps_zakat/api-python/app/modules/transaksi_histori/`

```
transaksi_histori/
  __init__.py
  schema.py      # Pydantic models: SearchParams, TransaksiRow, TransaksiDetail, JournalItem, DeleteResult, RepostResult
  repository.py  # DB queries asyncpg
  service.py     # business logic: search, detail, delete_tx, repost_journal
  router.py      # FastAPI APIRouter
  export.py      # openpyxl export
  delete.py      # delete dua jalur + reverse journal/balance
```

### Endpoints (prefix `/transaksi-histori`)

| Method | Path | Deskripsi |
|---|---|---|
| `GET` | `/search` | Search + list dengan filter |
| `GET` | `/transactions/{id}` | Detail transaksi + journal items |
| `POST` | `/transactions/{id}/delete` | Hapus dua jalur |
| `POST` | `/transactions/{id}/repost` | Re-posting jurnal |
| `GET` | `/search/export.xlsx` | Export hasil search ke XLSX |

---

## Search Filter Parameters

Query parameters untuk `GET /search` dan `GET /search/export.xlsx`:

| Param | Tipe | Default | Keterangan |
|---|---|---|---|
| `begin` | string ISO | required | Tanggal awal |
| `end` | string ISO | required | Tanggal akhir |
| `date_type` | `actual`\|`transaction` | `actual` | Kolom tanggal yang dipakai untuk filter date range |
| `sort_by` | enum | `actual_date` | actual_date / transaction_date / transaction_no / donor_no / donor_name / channel_name |
| `search_category` | enum | `none` | none / transno / donorno / donorname / description / refno |
| `search_text` | string | — | Aktif bila search_category != none; case-insensitive LIKE |
| `cash_account_no` | string | — | Optional — filter ke nomor rekening kas/bank tertentu |
| `limit` | int | 50 | Batas baris hasil, max 500 |
| `branch` | string | injected BFF | Kode cabang dari session |
| `is_spv` | bool | injected BFF | True bila user punya role SPVKEU |
| `user_id` | string | injected BFF | user_id dari session (untuk filter inputer bila !is_spv) |

**SPV logic**: bila `is_spv=False`, tambahkan `AND inputer = $user_id` ke WHERE. Bila `is_spv=True`, tidak ada filter inputer; `branch` berlaku (sama seperti `_resolve_branch` di laporan).

### SQL Dasar

```sql
SELECT
  t.transactionid, t.transactionno,
  to_char(t.transactiondate, 'YYYY-MM-DD') AS transactiondate,
  to_char(t.actualdate,      'YYYY-MM-DD') AS actualdate,
  t.amount, t.donorno, t.donorname, t.referenceno,
  t.description, t.inputer, t.authstatus, t.isposted,
  t.branchcode, t.authoperationmode, t.channelaccountno,
  f.accountname AS channelname,
  e.exttransactionid, s.titlesubsystem
FROM transaction.transaction t
LEFT JOIN transaction.financialaccount   f ON f.accountno = t.channelaccountno
LEFT JOIN transaction.externaltransaction e ON e.transactionid = t.transactionid
LEFT JOIN transaction.accsubsystem       s ON s.subsystemcode = e.subsystemcode
WHERE <filter>
ORDER BY <sort_by> ASC
LIMIT <limit>
```

---

## Response Models (Pydantic)

### TransaksiRow (list item)
```
transactionid, transactionno, transactiondate (ISO), actualdate (ISO),
amount, donorno, donorname, referenceno, description, inputer,
authstatus, isposted, authoperationmode, branchcode, channelaccountno,
channelname, exttransactionid, titlesubsystem
```

### TransaksiDetail (detail + journal)
Sama dengan TransaksiRow + field:
```
items: list[JournalItem]
```

### JournalItem
```
journalitem_no, fl_account, account_name, branch_code, valuta_code,
amount_debit, amount_credit, description, subaccountcode, subaccountname
```

Join: `journalitem ji LEFT JOIN transaction.account a ON a.account_code = ji.fl_account` — `fl_account` di journalitem adalah account_code. Bila tidak ada join match, tampilkan `fl_account` apa adanya sebagai kode akun.

---

## Delete Logic (`delete.py`)

`delete_transaction(conn, transaction_id, user_id, branch_code, is_spv) -> DeleteResult`

```
Validasi:
  1. Fetch transaction — raise LookupError bila tidak ada
  2. Branch check: bila !is_spv → branchcode harus == branch_code user (raise 403)
  3. exttransactionid check: bila tidak null → raise ValueError "Transaksi dari sistem eksternal tidak dapat dihapus"
  4. Double-delete check: authstatus='F' AND authoperationmode='D' → raise ValueError "Sudah dalam proses hapus"

Kasus A — authstatus='F' (belum otorisasi → hapus langsung):
  async with conn.transaction():
    Bila isposted='T':
      DELETE journal WHERE journal_no = t.journalno
      DELETE journalitem WHERE fl_journal = t.journalno
      DELETE journalblock WHERE journal_no = t.journalno
      Reverse balances:
        SELECT transactionitem → accounttransactionitem untuk ambil accountno + amount
        UPDATE financialaccount:
          - Untuk accounttitype='D' (product): balance -= amount (kredit balik)
          - Untuk accounttitype='A' (bank): balance -= amount (debit balik)
        UPDATE donortotalfund: totalamount -= amount per (donorid, fundentity)
    DELETE accounttransactionitem WHERE transactionitemid IN (items transaksi ini)
    DELETE transactionitem WHERE transactionid = $id
    DELETE transaction WHERE transactionid = $id
    INSERT transhistoryofchanges (changetype='D', transactionno, userid, processtime)
  → DeleteResult(deleted=True, pending_approval=False)

Kasus B — authstatus='T' (sudah otorisasi → tandai, perlu approval):
  UPDATE transaction SET authstatus='F', authoperationmode='D' WHERE transactionid=$id
  → DeleteResult(deleted=False, pending_approval=True)
```

---

## Re-post Jurnal Logic (`service.py`)

`repost_journal(conn, transaction_id, user_id, branch_code) -> RepostResult`

```
Validasi:
  1. Fetch transaction — raise LookupError bila tidak ada
  2. isposted='T' → raise ValueError "Transaksi sudah di-posting"
  3. Branch check sama seperti delete

Query: fetch semua transactionitem + accounttransactionitem untuk transaksi ini
Buat journal entries:
  INSERT journal (journal_no = J{branch}-{year}-{nextval('transaction.seq_transactionnumber')},
                  journal_date = transactiondate, source_app='isf-app', is_posted='T')
  Per product item (accounttitype='D'):
    INSERT journalitem (fl_journal, journalitem_no, fl_account=accountno,
                        amount_credit=amount, amount_debit=0, ...)
  Bank item (accounttitype='A'):
    INSERT journalitem (fl_journal, journalitem_no, fl_account=accountno,
                        amount_debit=amount, amount_credit=0, ...)
  INSERT journalblock (journal_no, key_id=transactionid, class_id='Transaction')
  UPDATE transaction SET journalno = journal_no, isposted = 'T'
→ RepostResult(journal_no=..., success=True)
```

⚠️ **Catatan**: Format `journal_no` (`J{branch}-{year}-{seq}`) berbeda dari legacy. GL account pada `fl_account` menggunakan `accountno` dari `accounttransactionitem`, bukan GL code dari `parameterjournal` subsystem (sama dengan limitasi di `commit.py`).

---

## Export XLSX (`export.py`)

Kolom Excel (13 kolom):
`TransactionNo | ChannelName | TglTransaksi | TglAktual | Nominal | NoDonatur | NamaDonatur | NoRef | Keterangan | Inputer | AuthStatus | IsPosted | Cabang`

Format tanggal: DD-MM-YYYY (via helper `_dmy`).  
Cap: 500 baris (sama dengan limit max).  
Nama file: `histori-transaksi-{begin}-{end}.xlsx`.

---

## BFF Router

### Lokasi: `apps_zakat/bff-api/app/routers/histori_transaksi.py`

- Satu menu key: `keuangan.transaksi.histori`
- Untuk setiap request: inject `is_spv`, `user_id`, `branch_code` dari session sebelum forward ke api-python
- **SPV check**: `is_spv = 'SPVKEU' in (session.get('roles') or [])`
- Branch resolve: pakai `_resolve_branch` yang sudah ada di `report.py` — user `branch_access='single'` dikunci ke `primary_branch`
- Export XLSX: stream ke frontend dengan header `Content-Disposition`

Endpoints BFF (`prefix=/transaksi-histori`):
```
GET  /search              → get_api_python
GET  /transactions/{id}   → get_api_python
POST /transactions/{id}/delete  → post_api_python (json body: {user_id, branch_code, is_spv})
POST /transactions/{id}/repost  → post_api_python (json body: {user_id, branch_code})
GET  /search/export.xlsx  → `stream_api_python` (fungsi baru di proxy.py, mirip `stream_report_api` tapi target `api_python_base_url`)
```

Wire di `bff-api/app/main.py`.

---

## Frontend: Dua Halaman

### 1. `HistoriTransaksiPage.vue` — `/keuangan/transaksi/histori`

**Filter bar** (tidak auto-load):
- DateField begin / end
- Dropdown `Tipe Tanggal`: Aktual / Transaksi
- Dropdown `Urut Berdasar`: Tgl Aktual / Tgl Transaksi / No Transaksi / No Donatur / Nama Donatur / Rekening
- Dropdown `Kategori Cari`: (Semua) / No Transaksi / No Donatur / Nama Donatur / Keterangan / No Referensi
- Input teks cari (disabled bila kategori = Semua)
- Input `Rekening Kas/Bank` (opsional)
- Input `Max Baris` (default 50)
- Tombol "Tampilkan"

**Tabel hasil** (klik baris → navigasi ke detail):
`No | No Transaksi | Rekening | Tgl Aktual | Tgl Transaksi | Nominal | No Donatur | Nama Donatur | No Ref | Keterangan | Inputer | Status | Posted | Cabang | Aksi`

Status chip: `T`=hijau "Terotorisasi", `F`=kuning "Pending"  
Posted chip: `T`=biru "Posted", `F`=abu "Belum"

**Tombol Hapus** per baris (aktif bila: bukan transaksi eksternal `exttransactionid=null`; antrean hapus belum ada; branch match atau is_spv=True)  
→ konfirmasi dialog → POST delete → reload baris atau hapus dari list

**Tombol Export XLSX** (aktif setelah ada data)

### 2. `HistoriTransaksiDetailPage.vue` — `/keuangan/transaksi/histori/:id`

**Header card**: semua field transaksi  
**Tabel journal items**: Nomor | Kode Akun | Nama Akun | Debit | Kredit | Keterangan

**Action buttons** (semua hidden bila `exttransactionid != null`):
- Tombol **Re-post Jurnal** (enabled bila `isposted='F'`) → POST repost → reload halaman
- Tombol **Hapus** (enabled berdasarkan kondisi) → konfirmasi → POST delete → kembali ke list

---

## Menu & Auth Wiring

### `registry.ts` — tambah 1 key

```typescript
'keuangan.transaksi.histori',
```

### `AppSidebar.vue` — di bawah Keuangan children (setelah Bank, sebelum section Upload)

```typescript
{ section: 'Transaksi' },
{ label: 'Histori Transaksi', to: '/keuangan/transaksi/histori', icon: Clock },
```

### `router/index.ts` — 2 route baru

```typescript
{ path: '/keuangan/transaksi/histori',
  name: 'keuangan-transaksi-histori',
  component: () => import('@/pages/keuangan/HistoriTransaksiPage.vue'),
  meta: { title: 'Histori Transaksi', menu_key: 'keuangan.transaksi.histori' } },
{ path: '/keuangan/transaksi/histori/:id',
  name: 'keuangan-transaksi-histori-detail',
  component: () => import('@/pages/keuangan/HistoriTransaksiDetailPage.vue'),
  meta: { title: 'Detail Transaksi', menu_key: 'keuangan.transaksi.histori' } },
```

### `seed-menu-and-rolemenu.sql` — tambah menu + role_menu

```sql
INSERT INTO isf_auth.menu (key, label)
VALUES ('keuangan.transaksi.histori', 'Histori Transaksi')
ON CONFLICT (key) DO NOTHING;

INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.id_peran, 'keuangan.transaksi.histori'
FROM enterprise.peran r
WHERE r.id_peran IN ('KEU','SPVKEU','ADM','ACC')
ON CONFLICT DO NOTHING;
```

---

## Error Handling

| Kondisi | HTTP | Error code |
|---|---|---|
| Transaksi tidak ditemukan | 404 | `NOT_FOUND` |
| Branch bukan milik user (non-SPV) | 403 | `BRANCH_FORBIDDEN` |
| Transaksi dari sistem eksternal | 400 | `EXTERNAL_TX` |
| Sudah dalam antrean hapus | 409 | `ALREADY_PENDING_DELETE` |
| Jurnal sudah ada (re-post) | 409 | `ALREADY_POSTED` |
| DB unavailable | 503 | `DB_UNAVAILABLE` |

---

## Testing

**Unit test**: `apps_zakat/api-python/tests/test_histori_transaksi.py`
- `test_search_filter_builds_correct_sql()` — verify WHERE clause generation
- `test_delete_unauth_transaction()` — mock conn, verify DELETE called
- `test_delete_auth_transaction_marks_pending()` — verify UPDATE authstatus
- `test_repost_journal_already_posted_raises()` — verify 409

**E2E script**: `testing/e2e-histori-transaksi.sh`
- GET search → 200 + list
- GET detail → 200 + journal items
- Double-delete attempt → 409

---

## Out of Scope (fase ini)

- Print kwitansi / cetak voucher (butuh template RTF/XLSX yang belum dipindahkan)
- Edit transaksi (opens form lain di legacy, terlalu kompleks)
- Portal wakaf (mirror setelah zakat stable)
- Real-time refresh / WebSocket

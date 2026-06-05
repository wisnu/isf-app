# Upload Penghimpunan Multi-Bank — Design Spec

**Date**: 2026-06-05  
**Status**: Approved — ready for implementation  
**Legacy ref**: `docs/legacy-apps/core/dialogs/Transaksi/fFundCollectionUploadMulti`

---

## Overview

Fitur upload transaksi penghimpunan (penerimaan zakat/infaq/wakaf) dari file Excel multi-bank. Menggantikan dialog `fFundCollectionUploadMulti` dari sistem legacy DAF.

Alur dua-tahap:
1. **Uploader** (role KEU/SPVKEU) — upload XLS/XLSX, lihat preview, simpan draft
2. **Supervisor** (role SPVKEU) — lihat list batch pending, otorisasi → transaksi terbentuk

---

## Architecture

```
Frontend (web-vue)
  ↕ BFF (bff-api) — session gating + menu key check
    ↕ api-python  — parse / validate / store draft / approve
      ↕ PostgreSQL (mziss_laz)
```

Semua operasi write (draft, approve) masuk ke `api-python`. Report-api tetap read-only — tidak disentuh.

---

## DB Schema Changes

### Migration file: `infra/db/migrations/transaction/009_upload_penghimpunan.sql`

```sql
-- Kolom yang ada di legacy tapi belum di schema dump
ALTER TABLE transaction.batchuploaditem
  ADD COLUMN IF NOT EXISTS amountzakatperusahaan numeric(30,6) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS amountinfaqterikat     numeric(30,6) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS amounttitipanqurban    numeric(30,6) DEFAULT 0;

-- Status otorisasi batch (belum ada di schema dump)
ALTER TABLE transaction.batchupload
  ADD COLUMN IF NOT EXISTS authstatus character varying(1) DEFAULT 'P';
  -- P = pending, A = approved
```

> ⚠️ Nomor migration 009 perlu diverifikasi — cek file terakhir di `infra/db/migrations/transaction/`.

---

## Excel Format

File diterima: `.xls` (xlrd) dan `.xlsx` (openpyxl). Parsing mulai baris ke-2 (baris 1 = header).

| Kolom | Field | Keterangan |
|---|---|---|
| 1 | NoRekening | Nomor rekening bank |
| 2 | Tanggal | Format DD/MM/YYYY |
| 3 | Keterangan | Deskripsi transaksi |
| 4 | NoRef | Nomor referensi |
| 5 | TotalKredit | Total kredit (hanya baris > 0 yang diproses) |
| 6 | ZakatProfesi | |
| 7 | ZakatMaal | |
| 8 | ZakatFitrah | |
| 9 | ZakatPerusahaan | |
| 10 | Infaq | |
| 11 | InfaqTerikat | |
| 12 | DPU | |
| 13 | AnakYatim | |
| 14 | AnakAsuh | |
| 15 | TitipanWakaf | |
| 16 | TitipanQurban | |
| 17 | Qurban | |
| 18 | NonHalal | |
| 19 | Fidyah | |

Parsing berhenti ketika 2 baris berturut-turut kosong di kolom 1.

---

## Validasi Per Baris

Setiap baris dievaluasi:
1. `TotalKredit <= 0` → baris dilewati (tidak masuk preview)
2. Format tanggal DD/MM/YYYY tidak valid → status `INVALID`, pesan `"Format tanggal tidak valid"`
3. Sum 14 kolom produk ≠ TotalKredit → status `WARNING`, pesan `"Total detail tidak sesuai nominal"`
4. NoRekening tidak ada di `transaction.bankcash` → status `INVALID`, pesan `"Nomor rekening tidak terdaftar"`
5. (NoRef, Tanggal, Amount) duplikat di `transaction.batchuploaditem` → status `WARNING`, pesan `"Sudah pernah di-upload"`

Status `INVALID` = baris **tidak disimpan ke draft**. Jika semua baris invalid → tombol "Simpan Draft" disabled.  
Status `WARNING` = baris tetap disimpan ke draft; supervisor melihat pesan warning di halaman detail sebelum otorisasi.  
Status valid = disimpan ke draft, tampil hijau di preview.

---

## Product ID Mapping

Hardcoded sesuai legacy (product ID di `mziss_laz`):

```python
PRODUCT_ID_MAP = {
    'ZakatProfesi':   518,
    'ZakatMaal':      5,
    'ZakatFitrah':    141,
    'ZakatPerusahaan': 575,
    'Infaq':          95,
    'InfaqTerikat':   572,
    'DPU':            145,
    'AnakYatim':      143,
    'AnakAsuh':       142,
    'TitipanWakaf':   12,
    'TitipanQurban':  574,
    'Qurban':         144,
    'NonHalal':       516,
    'Fidyah':         569,
}

FUND_ENTITY_MAP = {'Z': 1, 'T': 2, 'I': 2, 'W': 3, 'A': 4, 'N': 5}
```

Setiap produk di-lookup ke `transaction.productaccount` (JOIN `transaction.product`) by `productid` + `branchcode` + `currencycode='IDR'`.

---

## api-python: Modul Baru

### Lokasi: `apps_zakat/api-python/app/modules/transaction/`

```
transaction/
  __init__.py
  router.py      # FastAPI APIRouter
  schema.py      # Pydantic models: ParseRow, BatchSummary, BatchDetail, ApproveResult
  service.py     # parse_file(), save_draft(), list_batches(), get_batch(), approve_batch()
  repository.py  # DB queries: insert/update asyncpg
  parse.py       # Excel parsing (xlrd + openpyxl), validation logic
  commit.py      # Transaction commit logic (approve flow)
  template.py    # Generate template XLS kosong
```

### Endpoints

| Method | Path | Menu key required | Deskripsi |
|---|---|---|---|
| `POST` | `/transaction/upload/penghimpunan/parse` | `keuangan.upload.penghimpunan` | Terima file, return preview rows — tidak tulis DB |
| `POST` | `/transaction/upload/penghimpunan/draft` | `keuangan.upload.penghimpunan` | Simpan batch + items (status='P') |
| `GET` | `/transaction/upload/penghimpunan/template` | `keuangan.upload.penghimpunan` | Download template XLSX kosong |
| `GET` | `/transaction/upload/penghimpunan/batches` | `keuangan.upload.penghimpunan.approve` | List batch (filter: begin, end, status) |
| `GET` | `/transaction/upload/penghimpunan/batches/{id}` | `keuangan.upload.penghimpunan.approve` | Detail batch + items |
| `POST` | `/transaction/upload/penghimpunan/batches/{id}/approve` | `keuangan.upload.penghimpunan.approve` | Commit transaksi penuh |

Endpoint `parse` menerima `multipart/form-data` dengan field `file` (binary). `branch_code` **tidak dikirim dari frontend** — BFF menginject dari session (`primary_branch` untuk user `branch_access=single`, empty string untuk `all` yang berarti gunakan cabang default user).

---

## BFF: Router Baru

### Lokasi: `apps_zakat/bff-api/app/routers/transaction.py`

- Proxy semua endpoint ke `api-python` via `post_api_python` / `get_api_python`
- `parse` endpoint: terima multipart dari FE, forward ke api-python (perlu `httpx` multipart forwarding)
- Branch resolve: ambil `branch_code` dari session (`primary_branch`) bila user `branch_access='single'`
- Expose di `main.py`: `app.include_router(transaction_router, prefix="/api")`

---

## Transaction Commit Logic (`commit.py`)

Dieksekusi dalam satu `async with conn.transaction()`:

```
Untuk setiap batchuploaditem (sorted by transactiondate):

  1. Lookup product accounts
     - Query: productaccount JOIN product WHERE productid = ? AND branchcode = ? AND currencycode = 'IDR'
     - Untuk 14 produk; skip yang amount = 0

  2. Lookup donor
     - Coba match nama dari keterangan: regex DARI/TRANSFER DARI/TRF DARI
     - Jika nama match di fund.donor → pakai donor tersebut
     - Else → pakai DEF_DONOR (dari transaction.parameterglobal WHERE paramcode='DEF_DONOR')

  3. INSERT transaction.transaction
     - transactioncode = 'SDMULTI'
     - channelcode = 'A'
     - branchcode dari session
     - transactiondate = item.transactiondate
     - amount = item.amount

  4. Untuk setiap produk (amount > 0):
     INSERT transactionitem (transactionid, mutationtype='C', amount)
     INSERT accounttransactionitem (transactionitemid, accountno=productaccount.accountno,
       accounttitype='D', fundentity, donorid)

  5. Bank debit:
     INSERT transactionitem (transactionid, mutationtype='D', amount=total)
     INSERT accounttransactionitem (transactionitemid, accountno=bankcash.accountno,
       accounttitype='A')

  6. Generate transactionno
     - Format: SDMULTI-{YYYY}-{branchcode}-{cashcode}-{7-digit-seq}
     - Sequence dari nextval('transaction.seq_transaction')

  7. UPDATE financialaccount
     - Setiap product accountno: balance += amount
     - Bank accountno: balance -= total_amount

  8. UPDATE fund.donortotalfund
     - Per (donorid, fundentity): totalamount += amount
     - Total: fundentity=0, totalamount += sum_all

  9. INSERT transaction.journal (journal_no = GENERATED)
     INSERT transaction.journalitem (per kredit/debet pair)
     INSERT transaction.journalblock
     UPDATE transaction.transaction SET journalno = ...

 10. UPDATE batchuploaditem SET transactionid=..., transactionno=...

 11. INSERT transhistoryofchanges (changetype='I', transactionno, userid)

UPDATE batchupload SET authstatus='A', totalamount=..., totalrecord=...,
  authorizeduser=..., uploaddate=now() WHERE batchid=...
```

> ⚠️ **Journal schema** (kolom exact `transaction.journal`, `journalitem`, `journalblock`) belum lengkap di `ddl_all_schema.sql`. Saat implementasi wajib inspect tabel aktual di DB lokal (`\d transaction.journal` dll.) sebelum menulis insert logic. Ini satu-satunya bagian yang belum bisa di-spec fully tanpa akses DB.

---

## Donor Auto-Registration

Legacy membuat donatur baru bila nama ditemukan di description tapi tidak ada di `fund.donor`. Di sistem baru ini, **skip donor auto-registration** — baris dengan nama donor tidak ditemukan menggunakan DEF_DONOR. Alasan: membuat donor baru butuh INSERT ke beberapa tabel (`fund.donor`, `fund.individualdonor`, dll.) yang berisiko. Bisa ditambahkan sebagai enhancement di sprint berikutnya.

---

## Frontend: Tiga Halaman

### 1. `UploadPenghimpunanPage.vue` — `/keuangan/upload/penghimpunan`

**State flow:**
- Fase `idle` → user pilih rekening + upload file
- Fase `preview` → setelah parse berhasil, tampilkan tabel
- Fase `submitted` → setelah draft disimpan, tampilkan konfirmasi

**Komponen:**
- `SearchSelect` untuk pilih rekening bank (load dari `/api/coa/accounts?type=A&is_detail=T`)
- `<input type="file" accept=".xls,.xlsx">` + tombol "Download Template"
- Tombol "Parse File" (disabled bila belum pilih rekening + file)
- Preview table (scrollable horizontal, 19+ kolom) dengan chip status per baris
- Summary bar: `N baris valid · M baris invalid · Total Rp X`
- Tombol "Simpan Draft" (disabled bila semua baris invalid)

### 2. `UploadPenghimpunanListPage.vue` — `/keuangan/upload/penghimpunan/list`

**Mengikuti konvensi laporan:** tidak auto-load, user klik "Tampilkan".

**Komponen:**
- Filter: `DateField` begin/end + dropdown status (Semua/Pending/Approved)
- Tabel: BatchId, Filename, TanggalUpload (DD-MM-YYYY), Uploader, TotalRecord, TotalAmount, Status chip
- Klik baris → navigate ke detail

### 3. `UploadPenghimpunanDetailPage.vue` — `/keuangan/upload/penghimpunan/:id`

**Komponen:**
- Header card: Batch info (filename, tanggal upload, uploader, status chip, total)
- Tabel items: No, Tanggal, Keterangan, NoRef, Nominal, Status, TransactionNo (jika sudah approved)
- Tombol "Otorisasi" (visible dan enabled hanya bila `authstatus === 'P'` + user punya menu key approve)
- Dialog konfirmasi sebelum otorisasi
- Setelah approve → reload halaman, status jadi Approved

---

## Menu & Auth Wiring

### `registry.ts` — tambah 2 key

```typescript
'keuangan.upload.penghimpunan',
'keuangan.upload.penghimpunan.approve',
```

### `AppSidebar.vue` — di bawah Keuangan children (setelah Bank)

```typescript
{ section: 'Upload' },
{ label: 'Upload Penghimpunan', to: '/keuangan/upload/penghimpunan', icon: Upload },
{ label: 'Otorisasi Upload', to: '/keuangan/upload/penghimpunan/list', icon: ClipboardCheck },
```

### `router/index.ts` — 3 route baru

```typescript
{ path: '/keuangan/upload/penghimpunan', component: UploadPenghimpunanPage,
  meta: { menu_key: 'keuangan.upload.penghimpunan' } },
{ path: '/keuangan/upload/penghimpunan/list', component: UploadPenghimpunanListPage,
  meta: { menu_key: 'keuangan.upload.penghimpunan.approve' } },
{ path: '/keuangan/upload/penghimpunan/:id', component: UploadPenghimpunanDetailPage,
  meta: { menu_key: 'keuangan.upload.penghimpunan.approve' } },
```

### `seed-menu-and-rolemenu.sql` — tambah menu + role_menu

```sql
INSERT INTO isf_auth.menu (key, label, parent_key) VALUES
  ('keuangan.upload.penghimpunan', 'Upload Penghimpunan', 'keuangan'),
  ('keuangan.upload.penghimpunan.approve', 'Otorisasi Upload Penghimpunan', 'keuangan')
ON CONFLICT (key) DO NOTHING;

INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.id_peran, m.key
FROM enterprise.peran r
CROSS JOIN (VALUES
  ('KEU',    'keuangan.upload.penghimpunan'),
  ('SPVKEU', 'keuangan.upload.penghimpunan'),
  ('SPVKEU', 'keuangan.upload.penghimpunan.approve')
) AS m(role, key)
WHERE r.id_peran = m.role
ON CONFLICT DO NOTHING;
```

---

## Error Handling

- Parse gagal (file corrupt) → `400 Bad Request` dengan pesan
- File bukan XLS/XLSX → `422 Unprocessable Entity`
- Draft dengan semua baris invalid tidak boleh disimpan → `400`
- Approve batch yang sudah approved → `409 Conflict`
- DB unavailable → `503`
- Approve gagal di tengah jalan (DB error) → rollback full, return `500` dengan detail

---

## Testing

File E2E: `testing/e2e-upload-penghimpunan.sh`

Test cases:
1. Parse file valid → 200 + daftar rows
2. Parse file kosong / format salah → error response sesuai
3. Simpan draft → batch_id returned, cek DB
4. List batches → filter date range bekerja
5. Approve → cek transaction/journal/balance terbentuk di DB
6. Double approve → 409

Python unit test: `apps_zakat/api-python/tests/test_upload_penghimpunan.py`
- `test_parse_valid_xlsx()`
- `test_parse_invalid_date()`
- `test_validate_total_mismatch()`

---

## Out of Scope (fase ini)

- Donor auto-registration (nama baru dari description)
- Delete/rollback batch yang sudah approved
- Support portal wakaf (mirror setelah zakat stable)
- Upload via channel selain file (API, drag-drop, dsb.)
- Notifikasi real-time ke supervisor saat draft baru masuk

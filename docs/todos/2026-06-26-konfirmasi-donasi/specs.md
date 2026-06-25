# Specs: Konfirmasi Transaksi Donasi
**Portal**: zakat
**Domain**: `fundraising` (menu key prefix)
**Tipe**: CRUD (list + filter + per-row actions: delete, post journal, print receipt, edit donor)
**Legacy Ref**: docs/legacy-apps/fund/dialogs/Donatur/fDonaturTransactionConfirm
**Tanggal**: 2026-06-26

## Konteks

Fitur Konfirmasi Transaksi Donasi memungkinkan FUND dan SPVFUND untuk mengelola transaksi penghimpunan donasi yang sudah dicatat. 
User dapat mencari transaksi berdasarkan tanggal, cabang, donatur, nominal, dan keterangan; kemudian melakukan aksi per transaksi: 
hapus (untuk transaksi belum otorisasi), posting ke jurnal akuntansi (untuk transaksi sudah otorisasi), cetak kwitansi, 
atau ubah data donatur. Validasi RBAC ketat: FUND hanya bisa hapus transaksi own-branch yang belum otorisasi; 
SPVFUND bisa mengelola semua cabang dan transaksi sudah otorisasi.

## Alur Data

```mermaid
sequenceDiagram
  actor User
  participant Vue as web-vue (:5173)
  participant BFF as bff-api (:7000)
  participant API as api-python (:8000)
  participant DB as mziss_laz

  User->>Vue: Buka halaman Konfirmasi Donasi
  Vue->>User: Tampilkan filter panel (empty state)

  User->>Vue: Isi filter (tanggal, cabang, donatur, dll) + klik "Tampilkan"
  Vue->>BFF: GET /api/fundraising/donation-confirm?begin_date=2026-06-01&end_date=2026-06-26&branch_code=001&...
  BFF->>API: proxy GET /api/fundraising/donation-confirm?...
  Note over BFF: Inject branch_code dari session (jika branch_access='single')
  API->>DB: SELECT transaction, transactionitem, accounttransactionitem, financialaccount<br/>WHERE mutationtype='C' AND transactioncode IN ('SD001','SD002')<br/>AND actual_date BETWEEN ? AND ?<br/>AND branch_code = ? (atau semua jika is_all_branch=true)
  DB-->>API: rows
  API-->>BFF: {data: [{transaction_id, transaction_no, actual_date, donor_no, donor_name,<br/>amount, description, branch_name, channel_name, product_name,<br/>auth_status, is_posted, transaction_item_id}],<br/>pagination: {page, limit, total, total_pages}}
  BFF-->>Vue: {data, pagination}
  Vue-->>User: Tampilkan DataTable dengan hasil + action buttons per baris

  Note over User: Klik tombol aksi per baris

  rect rgb(200, 150, 255)
    Note over User,DB: Scenario A: Hapus Transaksi
    User->>Vue: Klik [Hapus] pada baris
    Vue->>Vue: Tampilkan confirmation dialog (read-only data)
    User->>Vue: Klik "Hapus" di dialog
    Vue->>BFF: DELETE /api/fundraising/donation-confirm/{transaction_id}
    BFF->>API: proxy DELETE /api/fundraising/donation-confirm/{transaction_id}
    Note over API: Validasi: branch_code baris == user branch (kecuali branch_access='all')<br/>Validasi: auth_status != 'T' ATAU user adalah SPVFUND
    API->>DB: BEGIN TRANSACTION
    API->>DB: DELETE FROM transaction.accounttransactionitem WHERE transactionitem_id IN (...)<br/>DELETE FROM transaction.transactionitem WHERE transaction_id = ?<br/>DELETE FROM transaction.inboxtransaction WHERE transaction_id = ?<br/>DELETE FROM transaction.transaction WHERE transaction_id = ?
    Note over API: Cascade delete: sponsortransaction, volunteertransaction, budgettransaction, dll
    DB-->>API: OK
    API->>DB: COMMIT
    API-->>BFF: {data: {id: transaction_id}, message: "Transaksi dihapus"}
    BFF-->>Vue: success
    Vue-->>User: Toast "Transaksi berhasil dihapus" + refresh tabel
  end

  rect rgb(200, 200, 150)
    Note over User,DB: Scenario B: Post Jurnal (Posting)
    User->>Vue: Klik [Jurnal] pada baris dengan auth_status='T' dan is_posted='F'
    Vue->>Vue: Tampilkan confirmation dialog
    User->>Vue: Klik "Post"
    Vue->>BFF: POST /api/fundraising/donation-confirm/{transaction_id}/post-journal
    BFF->>API: proxy POST /api/fundraising/donation-confirm/{transaction_id}/post-journal
    Note over API: Validasi: is_posted != 'T'<br/>Validasi: auth_status == 'T'
    API->>API: CreateJournal() → susun journal block + items
    API->>API: Kirim ke services/transaction_handler (accounting subsystem)
    API->>DB: UPDATE transaction SET is_posted='T', journal_no=?, journal_block_id=?
    DB-->>API: OK
    API-->>BFF: {data: {journal_no: "...", is_posted: 'T'}}
    BFF-->>Vue: success
    Vue-->>User: Toast "Jurnal berhasil diposting" + refresh tabel
  end

  rect rgb(150, 200, 150)
    Note over User,DB: Scenario C: Cetak Kwitansi (Receipt)
    User->>Vue: Klik [Kwitansi] pada baris dengan auth_status='T'
    Vue->>BFF: GET /api/fundraising/donation-confirm/{transaction_id}/receipt
    BFF->>API: proxy GET /api/fundraising/donation-confirm/{transaction_id}/receipt
    API->>DB: SELECT transaction, transactionitem, accounttransactionitem, donor<br/>WHERE transaction_id = ?
    DB-->>API: row
    Note over API: GetKwitansi() → dispatch ke Voucher.GetKwitansiVoucherDebet<br/>(SD001/SD002 → debet format)
    API->>API: Generate RTF/PDF stream
    API-->>BFF: Content-Type: application/pdf, Content-Disposition: attachment; filename=kwitansi_*.pdf
    BFF-->>Vue: binary stream
    Vue-->>User: Download file (browser trigger)
  end

  rect rgb(150, 150, 200)
    Note over User,DB: Scenario D: Edit Donatur
    User->>Vue: Klik [Edit Donatur] pada baris
    Vue->>Vue: Tampilkan sub-dialog (fEditTransactionDonatur)<br/>Dengan DonorNo, DonorName, Amount, ChannelCode/Name
    User->>Vue: Ubah DonorNo/DonorName + Simpan
    Vue->>BFF: PUT /api/fundraising/donation-confirm/{transaction_item_id}/donor
    BFF->>API: proxy PUT /api/fundraising/donation-confirm/{transaction_item_id}/donor<br/>Body: {donor_no, donor_name}
    API->>DB: UPDATE transaction.accounttransactionitem SET donorid=?, ... WHERE transactionitemid=?
    DB-->>API: OK
    API-->>BFF: {data: {donor_no, donor_name}}
    BFF-->>Vue: success
    Vue->>Vue: Update grid baris terkait (donor_no, donor_name)
    Vue-->>User: Toast "Donatur berhasil diubah"
  end
```

## Endpoint Contract

### GET /api/fundraising/donation-confirm
**Auth**: `require_menu('fundraising.donation.confirm')`
**Query params**:
- `begin_date` (string ISO YYYY-MM-DD, required) — tanggal transaksi mulai
- `end_date` (string ISO YYYY-MM-DD, required) — tanggal transaksi akhir
- `branch_code` (string, optional) — kode cabang (auto-filled dari session jika branch_access='single')
- `is_all_branch` (boolean, default=false) — query semua cabang (hanya untuk SPVFUND/branch_access='all')
- `search_category` (int, default=0) — filter donatur: 0=semua, 1=no donatur, 2=nama donatur
- `search_text` (string, optional) — teks pencarian donatur (aktif jika search_category != 0)
- `amount_from` (float, default=0) — nominal transaksi minimum
- `amount_to` (float, default=10000000) — nominal transaksi maksimum
- `description` (string, optional) — filter keterangan transaksi (LIKE substring)
- `limit` (int, default=50) — jumlah transaksi per halaman
- `page` (int, default=1) — halaman pagination

**Response**:
```json
{
  "data": [
    {
      "transaction_id": 1001,
      "transaction_no": "SD001-2026-06-001",
      "actual_date": "2026-06-15",
      "donor_no": "D001",
      "donor_name": "PT ABC Donasi",
      "amount": 5000000,
      "description": "Donasi reguler bulan Juni",
      "branch_code": "001",
      "branch_name": "Kantor Pusat",
      "channel_name": "Rekening Zakat Bank Mandiri",
      "channel_code": "BA001",
      "product_name": "Penghimpunan Donasi",
      "auth_status": "T",
      "is_posted": "F",
      "transaction_item_id": 2001
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 342,
    "total_pages": 7
  },
  "meta": { "request_id": "req-..." }
}
```

### DELETE /api/fundraising/donation-confirm/{transaction_id}
**Auth**: `require_menu('fundraising.donation.confirm.delete')`
**Validasi**:
- branch_code di baris == branch_code user (kecuali `branch_access='all'`)
- `auth_status != 'T'` ATAU user role includes `SPVFUND`

**Response**:
```json
{
  "data": { "id": 1001 },
  "meta": { "request_id": "..." }
}
```

**Error cases**:
- `BRANCH_DENIED` (403) — transaksi cabang lain, user bukan SPV
- `AUTHORIZATION_REQUIRED` (403) — transaksi sudah otorisasi, user bukan SPVFUND
- `VALIDATION_ERROR` (422) — cascade delete gagal

### POST /api/fundraising/donation-confirm/{transaction_id}/post-journal
**Auth**: `require_menu('fundraising.donation.confirm.post')`
**Validasi**:
- `auth_status == 'T'` — transaksi harus sudah diotorisasi
- `is_posted != 'T'` — belum dijurnal

**Response**:
```json
{
  "data": {
    "transaction_id": 1001,
    "journal_no": "JD001-2026-06-001",
    "journal_block_id": 5001,
    "is_posted": "T"
  },
  "meta": { "request_id": "..." }
}
```

**Error cases**:
- `ALREADY_POSTED` (422) — `is_posted == 'T'` sudah dijurnal
- `NOT_AUTHORIZED` (422) — `auth_status != 'T'` belum diotorisasi
- `ACCOUNTING_ERROR` (500) — services/transaction_handler gagal

### GET /api/fundraising/donation-confirm/{transaction_id}/receipt
**Auth**: `require_menu('fundraising.donation.confirm.print')`
**Validasi**:
- `auth_status == 'T'` — hanya kwitansi transaksi otorisasi

**Response**:
- Content-Type: `application/pdf` (atau `application/rtf`)
- Content-Disposition: `attachment; filename=kwitansi_{transaction_no}_{actual_date}.pdf`
- Body: binary file stream (RTF/PDF voucher)

### PUT /api/fundraising/donation-confirm/{transaction_item_id}/donor
**Auth**: `require_menu('fundraising.donation.confirm.edit_donor')`
**Body**:
```json
{
  "donor_no": "D001",
  "donor_name": "PT ABC Donasi"
}
```

**Validasi**:
- `donor_no` harus ada di `fund.donor`
- `transaction_item_id` harus ada dan own-branch (atau SPVFUND)

**Response**:
```json
{
  "data": {
    "transaction_item_id": 2001,
    "donor_no": "D001",
    "donor_name": "PT ABC Donasi"
  },
  "meta": { "request_id": "..." }
}
```

## Database

**Tabel utama**: 
- `transaction.transaction` — master transaksi (PK: transactionid)
- `transaction.transactionitem` — item transaksi (PK: transactionitemid, FK: transactionid)
- `transaction.accounttransactionitem` — posting ke akun (PK: transactionitemid, FK: transactionitemid)
- `transaction.financialaccount` — rekening kas/bank (PK: accountno)
- `fund.donor` — data donatur (PK: donorid)
- `enterprise.cabang` — data cabang (PK: kodecabang)

**Kolom kunci**:
| Kolom | Tabel | Type | Keterangan |
|---|---|---|---|
| `transactionid` | transaction.transaction | SERIAL | PK transaksi |
| `transactionno` | transaction.transaction | VARCHAR | nomor transaksi unik per periode |
| `actualdate` | transaction.transaction | DATE | tanggal transaksi |
| `transactiondate` | transaction.transaction | DATE | tanggal input |
| `branchcode` | transaction.transaction | VARCHAR(3) | FK ke enterprise.cabang |
| `authstatus` | transaction.transaction | CHAR(1) | 'F'=belum otorisasi, 'T'=sudah otorisasi |
| `isposted` | transaction.transaction | CHAR(1) | 'F'=belum dijurnal, 'T'=sudah dijurnal |
| `transactionitemid` | transaction.transactionitem | SERIAL | PK item |
| `mutationtype` | transaction.transactionitem | CHAR(1) | 'C'=kredit (penerimaan), 'D'=debet (pengeluaran) |
| `transactioncode` | transaction.transaction | VARCHAR(10) | 'SD001'/'SD002' untuk donasi penghimpunan |
| `donorid` | transaction.accounttransactionitem | VARCHAR | FK ke fund.donor |
| `amount` | transaction.transactionitem | DECIMAL | nominal transaksi |
| `channelaccountno` | transaction.transaction | VARCHAR | FK ke transaction.financialaccount.accountno |
| `journalblockid` | transaction.transaction | INTEGER | FK ke jurnal akuntansi (setelah posting) |
| `journalno` | transaction.transaction | VARCHAR | nomor jurnal (setelah posting) |

**Discriminators** (KRITIS — wajib di WHERE):
- `mutationtype = 'C'` → hanya transaksi kredit (penerimaan/penghimpunan donasi)
- `transactioncode IN ('SD001','SD002')` → hanya penghimpunan donatur (bukan transaksi lain)
- Sumber query: JOIN transaction.transactionitem d
  JOIN transaction.transaction a ON d.transactionid = a.transactionid
  WHERE d.mutationtype='C' AND a.transactioncode IN ('SD001','SD002')

**DWH View** (opsional, untuk laporan):
```sql
CREATE OR REPLACE VIEW dwh.v_donor_transaction_confirm AS
SELECT
  t.transactionid,
  t.transactionno,
  t.actualdate,
  t.transactiondate,
  ti.transactionitemid,
  ati.donorid AS donor_no,
  d.donorname AS donor_name,
  ti.amount,
  fa.accountno AS channel_account_no,
  fa.accountname AS channel_name,
  fa_product.accountname AS product_name,
  t.authstatus AS auth_status,
  t.isposted AS is_posted,
  t.branchcode,
  c.namacabang AS branch_name,
  t.inputer
FROM transaction.transaction t
JOIN transaction.transactionitem ti ON t.transactionid = ti.transactionid
JOIN transaction.accounttransactionitem ati ON ti.transactionitemid = ati.transactionitemid
JOIN fund.donor d ON ati.donorid = d.donorid
JOIN transaction.financialaccount fa ON t.channelaccountno = fa.accountno
LEFT JOIN transaction.financialaccount fa_product ON ati.accountno = fa_product.accountno
LEFT JOIN enterprise.cabang c ON t.branchcode = c.kodecabang
WHERE ti.mutationtype = 'C' AND t.transactioncode IN ('SD001','SD002');
```

## Menu Key

| Key | Label | Roles | Aksi |
|---|---|---|---|
| `fundraising.donation.confirm` | Konfirmasi Transaksi Donasi | ADMIN, FUND, SPVFUND | view |
| `fundraising.donation.confirm.delete` | Hapus Transaksi | FUND (own-branch, auth_status='F'), SPVFUND (all-branch) | delete |
| `fundraising.donation.confirm.post` | Post Jurnal | SPVFUND | create journal |
| `fundraising.donation.confirm.print` | Cetak Kwitansi | FUND, SPVFUND | print |
| `fundraising.donation.confirm.edit_donor` | Edit Donatur | FUND, SPVFUND | update |

## Catatan Implementasi

- **No Auto-Load**: Filter panel menampilkan empty state pada mount — data hanya di-fetch saat user klik "Tampilkan" (ikuti Rule #7 laporan)
- **Pagination Manual**: Gunakan standalone `<Paginator>` di atas DataTable, bukan `:paginator="true"` di DataTable
- **Date Display**: Gunakan `dmy()` dari `shared/utils/date.ts` untuk menampilkan actualdate (internal tetap ISO YYYY-MM-DD)
- **Branch Filtering**: Jika `branch_access='single'`, BFF inject `branch_code` dari session dan disable dropdown cabang di UI. Jika `branch_access='all'`, tampilkan checkbox "Seluruh Cabang"
- **RBAC per Baris**: Tombol aksi (delete, post, kwitansi) conditional berdasarkan role user + auth_status + is_posted transaksi
- **Cross-Branch Validation**: DELETE endpoint reject jika branch_code baris != user branch_code (kecuali SPVFUND)
- **Cascade Delete**: Hapus transaksi otomatis cascade ke transactionitem, accounttransactionitem, inboxtransaction, dan tabel pendukung lain via Transaction.OnDelete() di API Python
- **Journal Posting**: Endpoint POST post-journal tidak blocking — di-trigger background task di FastAPI, client menerima response segera dengan status PROCESSING (jika akuntansi kompleks). Update is_posted='T' setelah dispatcher selesai.
- **Menu Key Konsistensi**: Semua menu_key di URL harus terdaftar di `shared/constants/menu-keys.ts` (MENU_KEYS) dan di seed SQL
- **SQL Convention**: Semua migration + query pakai `CAST(x AS type)` bukan `x::type`

# Product Requirements Document (PRD)
## Transaksi Umum — Sistem Aplikasi ZISWAF

| | |
|---|---|
| **Versi** | 1.1 |
| **Status** | Active |
| **Tanggal** | 2026-06-19 |
| **Modul** | Keuangan / Transaksi |
| **Kode Transaksi** | `GT` (General Transaction) |
| **Portal** | Zakat + Wakaf (mirrored) |

---

## 1. Latar Belakang

Lembaga ZISWAF memiliki kebutuhan pencatatan transaksi keuangan yang tidak dapat dikategorikan secara langsung ke dalam modul khusus (Penghimpunan, Penyaluran, atau Kas/Bank murni). Modul **Transaksi Umum** hadir untuk mengakomodasi transaksi-transaksi ini dengan tetap mempertahankan integritas jurnal akuntansi (double-entry bookkeeping).

Modul ini menggantikan fungsi "General Transaction" (GT) dari sistem DAF lama, dengan perluasan dukungan empat jenis item mutasi dalam satu transaksi, alur maker-checker melalui sistem otorisasi, dan isolasi cabang yang ketat.

---

## 2. Tujuan Produk

- Menyediakan mekanisme pencatatan transaksi campuran (GL, Kas/Bank, Penghimpunan, Penyaluran) dalam satu dokumen transaksi.
- Memastikan setiap transaksi melewati validasi balance (Debet = Kredit) sebelum tersimpan.
- Mengintegrasikan alur maker-checker (otorisasi) untuk menjaga segregation of duties.
- Mendukung multi-cabang dengan isolasi data berbasis `branch_code`.
- Menyediakan UX modern: input detail via drawer slide-in, ringkasan real-time, dan filter list yang fleksibel.

---

## 3. Pengguna (User Roles)

| Role | Kode | Akses |
|------|------|-------|
| Administrasi | `ADM` | Input transaksi (maker), lihat list, lihat detail |
| Distribusi | `DIST` | Input transaksi (maker), lihat list, lihat detail |
| Akuntansi | `ACC` | Input transaksi (maker), lihat list, lihat detail |
| Supervisor Distribusi | `SPVDIST` | Lihat list, lihat detail, approve/reject di halaman Otorisasi |
| Keuangan | `KEU` | Lihat list, lihat detail, approve/reject di halaman Otorisasi |
| Supervisor Akuntansi | `SPVACC` | Lihat list, lihat detail, approve/reject di halaman Otorisasi |

**Branch Access:**
- `branch_access = 'S'` (Seluruh): melihat transaksi semua cabang.
- `branch_access = 'T'` (Tunggal): hanya melihat transaksi cabang sendiri (`primary_branch`).

---

## 4. Konsep Utama

### 4.1 Jenis Item Transaksi

Setiap transaksi GT terdiri dari minimal 2 item dengan jumlah total Debet = Kredit. Tersedia empat jenis item:

| Jenis | Kode | Deskripsi | Dampak Saldo |
|-------|------|-----------|--------------|
| GL Accounting | `G` | Entri jurnal murni (rekening buku besar) | Tidak ada (pure ledger) |
| Kas / Bank | `B` | Mutasi rekening kas atau bank | Update `financialaccount.balance` |
| Penghimpunan Dana | `C` | Penerimaan/reversal penerimaan donasi | Selalu Kredit secara akuntansi |
| Penyaluran Dana | `D` | Penyaluran/reversal penyaluran program | Debet (penyaluran) atau Kredit (reversal) |

### 4.2 Alur Kerja (Maker-Checker)

```
Inputer (ADM/DIST/ACC)
    │
    ▼
[Input form] → POST /api/transaksi-umum/
    │
    ▼ via save-and-submit
┌─────────────────────────────────────┐
│ Cek limit otorisasi per entity_type │
│                                     │
│  ≤ limit → AUTHORIZED otomatis      │
│  > limit → PENDING (menunggu SPV)   │
└─────────────────────────────────────┘
    │
    ▼ (jika PENDING)
Supervisor lihat di halaman Otorisasi
    │
    ├── Approve → status PROCESSING
    │              └── Background task: insert ke DB
    │                  └── status AUTHORIZED
    │
    └── Reject → status REJECTED
                  └── Inputer bisa revisi → DRAFT → submit ulang
```

### 4.3 Nomor Transaksi

Format: `GT-{YYYY}-{branch_code}-{seq:07d}`
Contoh: `GT-2026-001-0000042`

Format Nomor Jurnal: `GT001.{YYYY}.{MM}.{jseq:07d}`

---

## 5. Fitur yang Diperlukan

### 5.1 Halaman List (TransaksiUmumListPage)

| No | Fitur | Prioritas |
|----|-------|-----------|
| F01 | Filter periode (dari–sampai tanggal) | Must Have |
| F02 | Filter status (Semua / Posted / Draft) | Must Have |
| F03 | Pencarian by nomor transaksi / deskripsi | Must Have |
| F04 | Tabel dengan kolom: No. Transaksi, Tanggal, Deskripsi, Nilai, Status, Inputer, Aksi | Must Have |
| F05 | Detail transaksi (modal view) dengan baris jurnal | Must Have |
| F06 | Hapus transaksi (dengan konfirmasi modal berisi data lengkap) | Must Have |
| F07 | Draft/Pending dari otorisasi tampil berdampingan | Should Have |
| F08 | Pagination standar ISF (di atas tabel) | Must Have |

### 5.2 Halaman Input (TransaksiUmumCreatePage)

| No | Fitur | Prioritas |
|----|-------|-----------|
| F09 | Header form: Tanggal, Deskripsi, No. Referensi | Must Have |
| F10 | Ringkasan real-time: Total Debet, Kredit, Selisih, Status Balance | Must Have |
| F11 | Layout split: header+ringkasan (sticky left) + tabel item (right) | Must Have |
| F12 | Input detail via drawer slide-from-right | Must Have |
| F13 | Detail GL: pilih COA, Kode Anggaran, Ket. Anggaran | Must Have |
| F14 | Detail Kas/Bank: lookup rekening, Jenis Mutasi | Must Have |
| F15 | Detail Penghimpunan: Donatur (kode+nama terpisah), Produk, Jenis Dana | Must Have |
| F16 | Detail Penyaluran: Program, Sumber Dana, Ashnaf, Jenis Dana | Must Have |
| F17 | Nominal panel: Jenis Mutasi, Valuta, Nilai, Kurs, Ekuivalen IDR | Must Have |
| F18 | Validasi balance sebelum submit (sisi frontend + backend) | Must Have |
| F19 | Edit item dalam tabel (re-open drawer dengan data terpopulasi) | Must Have |
| F20 | Hapus item individual dari tabel | Must Have |
| F21 | Submit ke otorisasi, redirect ke list setelah sukses | Must Have |
| F22 | Dukungan multi-currency (IDR, USD, EUR, MYR, SGD, SAR) | Should Have |

---

## 6. Aturan Bisnis (Business Rules)

| No | Aturan |
|----|--------|
| BR01 | Minimal 2 item per transaksi |
| BR02 | Total Debet harus sama dengan Total Kredit (toleransi ±0.01) |
| BR03 | Item tipe C (Penghimpunan) selalu Kredit secara akuntansi, bukan Debet — reversal ditandai `is_reversal=true` |
| BR04 | Item tipe D (Penyaluran) default Debet; reversal/koreksi = Kredit, tandai `is_correction=true` |
| BR05 | Balance check dilakukan di level schema Pydantic sebelum menyentuh DB |
| BR06 | Semua item tipe B/C/D mengupdate `accounttransactionitem` dan berdampak ke saldo `financialaccount` |
| BR07 | Item tipe G hanya mengisi jurnal, tidak ada dampak ke saldo rekening |
| BR08 | `fund_entity` valid: 1=Zakat, 2=Infaq, 3=Wakaf, 4=Amil, 5=Non-halal |
| BR09 | `ashnaf` valid: F=Fakir, M=Miskin, U=Mualaf, H=Riqab, G=Gharimin, S=Fisabilillah, I=Ibnu Sabil, A=Amil |
| BR10 | Transaksi yang sudah AUTHORIZED tidak bisa dihapus/diedit langsung — perlu transaksi koreksi baru |
| BR11 | Single-branch user: `branch_code` selalu diisi oleh BFF dari `primary_branch` |
| BR12 | All-branch user: melihat semua cabang tanpa filter |
| BR13 | Discriminator lookup: produk penghimpunan = `accountno` prefix angka; penyaluran = prefix huruf |
| BR14 | Transaksi melewati otorisasi via `save_and_submit`; bypass ke AUTHORIZED jika nilai ≤ limit |

---

## 7. Kriteria Penerimaan (Acceptance Criteria)

### AC01 — Input & Submit
- User dapat membuat transaksi dengan minimal 1 item GL + 1 item Kas/Bank yang balance
- User mendapat toast sukses dan diarahkan ke list setelah submit
- Transaksi muncul di halaman Otorisasi dengan status PENDING (atau AUTHORIZED jika below limit)

### AC02 — Validasi Balance
- Tombol Simpan disabled jika Debet ≠ Kredit
- Error message jelas jika user mencoba bypass: "Jurnal belum balance: Debet X ≠ Kredit Y"

### AC03 — Lookup Berfungsi
- Cari rekening Kas/Bank mengembalikan hasil dalam ≤ 20 rows
- Cari donatur berfungsi dengan nama parsial
- Cari produk penghimpunan hanya menampilkan produk dengan `accountno` prefix angka
- Cari program penyaluran hanya menampilkan dengan `accountno` prefix huruf

### AC04 — Detail View
- Klik baris di list membuka modal dengan header + tabel baris jurnal
- Semua item termasuk account code, account name, D/K, dan jumlah tampil

### AC05 — Filter & Search
- Filter status "Posted" hanya tampilkan transaksi AUTHORIZED
- Filter status "Draft" hanya tampilkan submission DRAFT/PENDING dari otorisasi
- Search by nomor transaksi bekerja (partial match)

### AC06 — Delete Confirmation
- Klik tombol Hapus membuka modal konfirmasi dengan data lengkap (no, tanggal, deskripsi, nilai, status)
- Konfirmasi mengirim DELETE request ke API
- List direfresh otomatis setelah hapus berhasil

### AC07 — Branch Isolation
- User single-branch tidak melihat transaksi cabang lain
- User all-branch melihat semua transaksi tanpa filter cabang

---

## 8. Di Luar Scope

- Edit transaksi yang sudah AUTHORIZED (gunakan transaksi koreksi baru)
- Bulk input / upload CSV untuk Transaksi Umum
- Export laporan dari halaman ini (lihat Laporan List Transaksi Umum)
- Approval di halaman ini (approval ada di modul Otorisasi)
- Integrasi langsung dengan modul Anggaran untuk validasi Kode Anggaran

---

## 9. Dependensi Teknis

| Sistem | Digunakan Untuk |
|--------|----------------|
| `otorisasi.submission` | Penyimpanan sementara sebelum AUTHORIZED |
| `transaction.transaction` | Tabel utama setelah AUTHORIZED |
| `transaction.transactionitem` | Detail item per transaksi |
| `transaction.accounttransactionitem` | Dampak ke rekening (tipe B, C, D) |
| `transaction.financialaccount` | Saldo rekening kas/bank |
| `transaction.journalblock` + `journal` | Jurnal akuntansi |
| `fund.donor` | Data donatur untuk tipe C |
| `transaction.productaccount` | Produk penghimpunan dan program penyaluran |
| `transaction.financialaccount` | Rekening kas/bank untuk lookup |

---

## 10. Riwayat Perubahan

| Versi | Tanggal | Perubahan |
|-------|---------|-----------|
| 1.0 | 2026-06-17 | Versi awal (split page list + create) |
| 1.1 | 2026-06-19 | Tambah multi-currency, Kode Anggaran, Kode Donatur terpisah, drawer layout, status filter |

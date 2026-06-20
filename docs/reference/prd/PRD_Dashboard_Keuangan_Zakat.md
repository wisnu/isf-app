# Product Requirements Document (PRD)
## Dashboard Keuangan — Sistem Aplikasi Zakat

| | |
|---|---|
| **Versi** | 1.0 |
| **Status** | Draft |
| **Tanggal** | 23 Mei 2025 |
| **Modul** | Dashboard / Read-Only View |

---

## 1. Latar Belakang

Sistem aplikasi zakat yang sudah berjalan memiliki modul lengkap mencakup Penghimpunan Dana (ZIS), Penyaluran Dana, Kas/Bank, Anggaran, Laporan Keuangan, dan Otorisasi. Namun seluruh data tersebar di masing-masing menu laporan sehingga pengguna harus membuka banyak halaman untuk mendapat gambaran kondisi keuangan secara keseluruhan.

Dashboard ini dirancang sebagai halaman ringkasan eksekutif yang menyajikan data paling kritis dari seluruh modul dalam satu tampilan, tanpa memerlukan navigasi manual ke setiap laporan.

---

## 2. Tujuan Produk

- Memberikan gambaran kondisi keuangan lembaga secara real-time dalam satu halaman.
- Mempercepat pengambilan keputusan oleh supervisor dan manajemen.
- Menyediakan early warning untuk kondisi yang memerlukan tindakan segera (transaksi pending otorisasi, uang muka belum LPJ, realisasi anggaran kritis).
- Menjadi entry point utama saat pengguna pertama kali masuk ke aplikasi.

---

## 3. Pengguna (User Roles)

| Role | Kode | Akses Dashboard |
|---|---|---|
| Administrator | ADM | Semua widget |
| Supervisor Keuangan | SPVKEU | Semua widget |
| Akunting/Kasir | ACC | Semua widget kecuali ringkasan anggaran |
| Keuangan | KEU | Semua widget kecuali otorisasi pending |
| Supervisor Accounting | SPVACC | Semua widget |
| Quality Assurance | QAC | View only, semua widget |

---

## 4. Ruang Lingkup

### 4.1 Dalam Ruang Lingkup (In Scope)
- Halaman dashboard read-only dengan data agregat
- Filter periode (bulan/tahun)
- 6 widget utama (dijabarkan di seksi 6)
- Refresh data manual dan otomatis
- Penyesuaian tampilan berdasarkan role pengguna

### 4.2 Di Luar Ruang Lingkup (Out of Scope)
- Input atau edit data dari dashboard
- Drill-down ke level transaksi (akan menjadi fase berikutnya)
- Dashboard per cabang (fase berikutnya)
- Export dashboard ke PDF/Excel

---

## 5. Asumsi dan Dependensi

- Data bersumber dari database yang sudah digunakan modul-modul existing (tidak ada sumber data baru).
- Autentikasi dan manajemen role menggunakan sistem yang sudah ada (`AllowedGroups`).
- Periode default dashboard adalah bulan berjalan.
- Mata uang default adalah Rupiah (IDR).

---

## 6. Spesifikasi Fitur

### 6.1 Header & Filter Periode

**Deskripsi:** Bagian atas dashboard menampilkan judul dan kontrol filter waktu.

**Komponen:**
- Label judul: "Dashboard Keuangan Zakat"
- Dropdown filter: Bulan dan Tahun
- Tombol Refresh data
- Timestamp "Terakhir diperbarui: [waktu]"

**Aturan bisnis:**
- Default periode = bulan dan tahun berjalan
- Perubahan filter langsung memperbarui semua widget di halaman

---

### 6.2 Widget 1 — Kartu Metrik Utama

**Deskripsi:** Empat kartu ringkasan di baris paling atas yang menampilkan KPI terpenting.

| No | Kartu | Sumber Data | Keterangan |
|---|---|---|---|
| 1 | Total Penghimpunan | Transaksi penghimpunan dana | Akumulasi bulan berjalan, perbandingan vs bulan lalu |
| 2 | Total Penyaluran | Transaksi penyaluran dana | Akumulasi bulan berjalan, perbandingan vs bulan lalu |
| 3 | Saldo Kas/Bank | Rekening bank + kas besar + kas kecil | Total saldo semua rekening aktif |
| 4 | Transaksi Belum Otorisasi | List data belum otorisasi | Jumlah transaksi pending, tampil merah jika > 0 |

**Aturan bisnis:**
- Perbandingan bulan lalu ditampilkan sebagai persentase dengan indikator naik (hijau) / turun (merah)
- Kartu "Transaksi Belum Otorisasi" hanya tampil untuk role: ADM, SPVKEU, SPVACC
- Jika nilai 0, indikator perbandingan tidak ditampilkan

---

### 6.3 Widget 2 — Tren Penghimpunan vs Penyaluran

**Deskripsi:** Grafik kombinasi (bar + line) yang menampilkan tren 6 bulan terakhir.

**Spesifikasi grafik:**
- Tipe: Bar chart (penghimpunan) + Line chart (penyaluran) pada satu sumbu
- Sumbu X: 6 bulan terakhir (label singkat: Jan, Feb, dst.)
- Sumbu Y: Nilai dalam jutaan Rupiah
- Warna bar penghimpunan: biru
- Warna garis penyaluran: hijau teal

**Sumber data:** Rekapitulasi transaksi kas/bank + laporan penghimpunan + laporan penyaluran

**Aturan bisnis:**
- Rentang waktu selalu 6 bulan ke belakang dari bulan yang dipilih di filter
- Tooltip saat hover menampilkan nilai nominal lengkap (format Rp X.XXX.XXX)

---

### 6.4 Widget 3 — Komposisi Produk Penghimpunan

**Deskripsi:** Donut chart yang menampilkan proporsi penghimpunan berdasarkan produk/jenis dana.

**Spesifikasi grafik:**
- Tipe: Donut chart
- Segmen: Sesuai dengan daftar Produk Penghimpunan yang aktif (Zakat, Infaq, Sedekah, Wakaf, dll.)
- Nilai tengah: Total penghimpunan periode berjalan
- Legenda: Di bawah/samping grafik, menampilkan nama produk + persentase

**Sumber data:** Master Produk Penghimpunan + Transaksi Penghimpunan Dana

**Aturan bisnis:**
- Hanya menampilkan produk yang memiliki transaksi pada periode terpilih
- Produk dengan nilai < 1% dikelompokkan menjadi "Lainnya"

---

### 6.5 Widget 4 — Realisasi Anggaran Penyaluran

**Deskripsi:** Progress bar per program penyaluran yang menunjukkan persentase realisasi terhadap anggaran.

**Komponen:**
- Setiap baris = satu Program Penyaluran
- Label kiri: Nama program
- Label kanan: Persentase realisasi (%)
- Progress bar berwarna dengan threshold visual

**Threshold warna progress bar:**

| Rentang | Warna | Arti |
|---|---|---|
| 0–50% | Abu-abu | Normal, masih awal |
| 51–80% | Biru | Berjalan baik |
| 81–95% | Amber/kuning | Mendekati batas |
| > 95% | Merah | Kritis, hampir habis |

**Sumber data:** Modul Anggaran (Inquiry Anggaran) + Laporan Penyaluran Dana

**Aturan bisnis:**
- Hanya program dengan anggaran aktif periode berjalan yang ditampilkan
- Maksimal 8 program ditampilkan; jika lebih, tampilkan tombol "Lihat semua"
- Widget ini hanya tampil untuk role: ADM, SPVKEU, KEU, SPVACC

---

### 6.6 Widget 5 — Monitoring Uang Muka Kegiatan

**Deskripsi:** Daftar uang muka kegiatan yang masih outstanding (belum di-LPJ atau belum dikembalikan).

**Kolom tabel:**
- Nama penerima
- Nama program/kegiatan
- Nominal
- Status (badge berwarna)

**Status badge:**

| Status | Warna | Kondisi |
|---|---|---|
| Belum LPJ | Amber | Sudah lewat tanggal, belum ada pertanggungjawaban |
| Proses | Biru | Dalam proses LPJ |
| Lunas | Hijau | Sudah dikembalikan/di-LPJ |

**Sumber data:** Transaksi Penyerahan Uang Muka + Transaksi Pengembalian/LPJ Uang Muka

**Aturan bisnis:**
- Hanya menampilkan uang muka dengan status Belum LPJ dan Proses
- Diurutkan berdasarkan tanggal terlama terlebih dahulu
- Maksimal 5 baris; jika lebih tampilkan link "Lihat semua"

---

### 6.7 Widget 6 — Saldo per Rekening Kas/Bank

**Deskripsi:** Daftar ringkas saldo terkini semua rekening kas dan bank yang aktif.

**Kolom tabel:**
- Nama rekening / bank
- Jenis (Bank / Kas Besar / Kas Kecil) — ditampilkan sebagai badge
- Saldo terkini

**Sumber data:** Rekening Bank + Rekening Kas Besar + Rekening Kas Kecil (dari modul Informasi → Kas/Bank)

**Aturan bisnis:**
- Hanya rekening dengan status aktif yang ditampilkan
- Diurutkan: Bank terlebih dahulu, lalu Kas Besar, lalu Kas Kecil
- Total saldo ditampilkan di baris paling bawah (bold)

---

## 7. Tata Letak Halaman (Layout)

```
┌─────────────────────────────────────────────────────────────────┐
│  Header: Judul + Filter Periode + Tombol Refresh                │
├───────────┬───────────┬───────────┬─────────────────────────────┤
│  Total    │  Total    │  Saldo    │  Transaksi Belum            │
│  Penghim. │  Penyalur.│  Kas/Bank │  Otorisasi                  │
├───────────────────────────────┬─────────────────────────────────┤
│  Tren Penghimpunan vs         │  Komposisi Produk               │
│  Penyaluran (6 bulan)         │  Penghimpunan (Donut)           │
├───────────────┬───────────────┬─────────────────────────────────┤
│  Realisasi    │  Uang Muka    │  Saldo per                      │
│  Anggaran     │  Kegiatan     │  Rekening                       │
└───────────────┴───────────────┴─────────────────────────────────┘
```

---

## 8. Ketentuan Non-Fungsional

| Aspek | Ketentuan |
|---|---|
| Performa | Data dashboard termuat dalam ≤ 3 detik pada koneksi normal |
| Refresh otomatis | Setiap 5 menit (dapat diatur oleh ADM) |
| Responsif | Mendukung resolusi minimal 1280×768 |
| Keamanan | Data yang ditampilkan mengikuti hak akses role yang sudah ada |
| Audit | Akses ke halaman dashboard dicatat di Auditrail |

---

## 9. Kriteria Penerimaan (Acceptance Criteria)

- [ ] Semua 6 widget menampilkan data yang konsisten dengan laporan existing di menu Laporan
- [ ] Filter periode mengubah data di semua widget secara bersamaan
- [ ] Widget Otorisasi Pending tidak tampil untuk role KEU dan ACC
- [ ] Widget Anggaran tidak tampil untuk role ACC dan QAC
- [ ] Kartu metrik menampilkan indikator perbandingan yang akurat
- [ ] Tidak ada widget yang menampilkan data dari periode berbeda secara bersamaan
- [ ] Halaman dapat dimuat ulang tanpa kehilangan filter yang sedang dipilih

---

## 10. Fase Pengembangan Selanjutnya (Out of Scope v1)

- **v1.1** — Drill-down dari widget ke detail transaksi
- **v1.2** — Dashboard per cabang dengan filter cabang
- **v1.3** — Export dashboard ke PDF / ringkasan cetak
- **v1.4** — Notifikasi push untuk transaksi pending otorisasi

---

*Dokumen ini merupakan dasar diskusi awal dan terbuka untuk revisi sebelum masuk tahap development.*

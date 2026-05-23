# Product Requirements Document (PRD)
## Dashboard Penghimpunan ZIS — Sistem Aplikasi Zakat

| | |
|---|---|
| **Versi** | 1.1 |
| **Status** | Draft |
| **Tanggal** | 23 Mei 2025 |
| **Perubahan v1.1** | Widget Saluran Penghimpunan, Ranking ZIS AM, dan Pencapaian Target per Produk dipindahkan ke pending (ditunda ke fase berikutnya) |
| **Modul Referensi** | Penghimpunan → Kegiatan, Laporan, ZIS Account Manager |

---

## 1. Latar Belakang

Modul Penghimpunan memiliki ekosistem data yang lebih kaya dari modul lain: ada target penghimpunan per produk, ZIS Account Manager (AM) internal dan independen dengan target individual, data donatur korporat dan individu yang terpisah, saluran penghimpunan yang beragam (transfer bank, HC/payroll, tunai, website, UPZ), serta infrastruktur komunikasi donatur (SMS Gateway dan Email Gateway).

Semua data ini tersebar di sub-menu yang berbeda sehingga tim penghimpunan (role `PHP` dan `SPVPHP`) tidak punya satu tampilan terpadu untuk memantau kinerja fundraising secara keseluruhan. Dashboard ini mengisi kekosongan tersebut dengan fokus pada pertanyaan utama yang dibutuhkan tim penghimpunan setiap hari:

1. Seberapa jauh kita dari target bulan ini?
2. Produk mana yang paling berkontribusi terhadap total penghimpunan?
3. Donatur mana yang perlu diperhatikan, dan bagaimana tren segmentasi donatur?

---

## 2. Tujuan Produk

- Memantau pencapaian target penghimpunan secara real-time per periode.
- Memberikan visibilitas atas komposisi donatur (individu, korporat, HC/payroll) dan tren kontribusinya.
- Menampilkan alert untuk konfirmasi transaksi yang tertunda dan donatur autodebet yang non-aktif.
- Menjadi halaman utama yang dibuka tim PHP setiap pagi kerja.

> **Catatan v1.1:** Fitur Ranking ZIS Account Manager, Pencapaian Target per Produk, dan Distribusi per Saluran Penghimpunan ditunda ke fase berikutnya — belum masuk scope v1.

---

## 3. Pengguna (User Roles)

| Role | Kode | Akses Dashboard | Catatan |
|---|---|---|---|
| Administrator | ADM | Semua widget | — |
| Supervisor Penghimpunan | SPVPHP | Semua widget | — |
| Staf Penghimpunan | PHP | Semua widget | — |
| Supervisor Admin | SPVADM | Widget target & ringkasan saja | Tidak melihat detail donatur |

---

## 4. Ruang Lingkup

### 4.1 Dalam Ruang Lingkup (In Scope)
- Halaman dashboard read-only khusus modul penghimpunan
- Filter periode (bulan/tahun)
- 5 widget aktif (dijabarkan di seksi 6)
- Tampilan responsif terhadap role pengguna

### 4.2 Di Luar Ruang Lingkup (Out of Scope v1)
- Input target dari dashboard
- Kirim SMS/email notifikasi dari dashboard
- Analitik retensi donatur (cohort analysis)
- Peta sebaran donatur geografis
- Perbandingan kinerja antar cabang
- Export dari dashboard (sudah dicakup PRD Menu Laporan)
- **[Pending]** Ranking ZIS Account Manager
- **[Pending]** Pencapaian Target per Produk
- **[Pending]** Distribusi per Saluran Penghimpunan

---

## 5. Asumsi dan Dependensi

- Master Target Penghimpunan sudah ter-entry via menu `Kegiatan → Target Penghimpunan` sebelum dashboard digunakan (digunakan untuk Widget 1 kartu realisasi vs target dan Widget 2 tren).
- Data donatur korporat dan individu sudah terpisah di master data.
- Data HC/payroll sudah ter-upload via menu Upload Data Penerimaan ZIS Rutin.
- Mata uang default: Rupiah (IDR).
- Jika target belum di-entry untuk periode tertentu, kartu dan grafik tren realisasi vs target menampilkan pesan "Target belum ditetapkan."

---

## 6. Spesifikasi Fitur

### 6.1 Header & Filter Periode

**Deskripsi:** Navigasi waktu dan kontrol filter di bagian atas dashboard.

**Komponen:**
- Judul: "Dashboard Penghimpunan ZIS"
- Dropdown filter: Bulan + Tahun
- Tombol Refresh
- Timestamp "Terakhir diperbarui: [waktu]"

**Aturan bisnis:**
- Default periode = bulan dan tahun berjalan
- Perubahan filter memperbarui semua widget serentak

---

### 6.2 Widget 1 — Kartu Metrik Utama (4 Kartu)

**Deskripsi:** Empat kartu KPI paling penting untuk tim penghimpunan di baris teratas.

| No | Kartu | Sumber Data | Keterangan |
|---|---|---|---|
| 1 | Realisasi vs target | Target Penghimpunan + Transaksi | Persentase pencapaian + nominal aktual vs target |
| 2 | Total donatur aktif | Data Donatur Korporat + Individu | Donatur yang bertransaksi di periode berjalan + jumlah donatur baru |
| 3 | Donatur rutin HC | Upload Data HC | Jumlah donatur aktif via payroll + persentase dari total |
| 4 | Konfirmasi pending | Konfirmasi Transaksi Donasi | Jumlah transaksi menunggu konfirmasi, tampil amber jika > 0 |

**Aturan bisnis:**
- Kartu realisasi vs target menampilkan warna hijau jika ≥ 100%, amber jika 70–99%, merah jika < 70%
- Kartu donatur baru menampilkan delta positif (hijau) atau negatif (merah) vs bulan lalu
- Kartu konfirmasi pending hanya tampil untuk role ADM, SPVPHP, PHP

---

### 6.3 Widget 2 — Tren Realisasi vs Target (6 Bulan)

**Deskripsi:** Grafik kombinasi yang membandingkan realisasi penghimpunan aktual dengan target bulanan selama 6 bulan terakhir.

**Spesifikasi grafik:**
- Tipe: Grouped bar chart (realisasi = biru, target = abu-abu)
- Sumbu X: 6 bulan terakhir dari periode yang dipilih
- Sumbu Y: Nilai dalam jutaan Rupiah
- Garis referensi horizontal pada nilai target jika target sama setiap bulan

**Sumber data:** Master Target Penghimpunan + Laporan Target Penghimpunan + Transaksi Penghimpunan

**Aturan bisnis:**
- Jika target bulan tertentu belum diset, bar target tidak muncul dan diberi keterangan "–"
- Tooltip menampilkan nilai realisasi, nilai target, dan persentase pencapaian

---

### 6.4 Widget 3 — Komposisi per Produk ZIS

**Deskripsi:** Donut chart proporsi penghimpunan berdasarkan produk (Zakat Maal, Zakat Fitrah, Infaq, Sedekah, Wakaf, dll.).

**Sumber data:** Master Produk Penghimpunan + Transaksi Penghimpunan

**Aturan bisnis:**
- Segmen sesuai produk aktif yang memiliki transaksi pada periode terpilih
- Produk < 2% dari total dikelompokkan sebagai "Lainnya"
- Nilai tengah donut: total nominal penghimpunan periode berjalan
- Legenda mencantumkan nama produk + persentase

---

### 6.5 Widget 4 — Pencapaian Target per Produk ⏸ PENDING

> **Status:** Ditunda. Widget ini tidak masuk scope v1. Akan dikerjakan setelah proses validasi struktur data target per produk selesai.

**Deskripsi rencana:** Progress bar per produk penghimpunan yang menunjukkan serapan terhadap target masing-masing produk, dengan threshold warna (biru / biru tua / amber / hijau).

**Alasan ditunda:** Perlu konfirmasi apakah master target sudah di-entry per produk secara konsisten, atau hanya target total per periode. Jika target hanya tersedia di level total, widget ini tidak bisa dihitung per produk dengan akurat.

---

### 6.6 Widget 5 — Ranking ZIS Account Manager ⏸ PENDING

> **Status:** Ditunda. Widget ini tidak masuk scope v1. Akan dikerjakan setelah asosiasi transaksi ke masing-masing AM terverifikasi di sistem.

**Deskripsi rencana:** Leaderboard top 5 AM berdasarkan total penghimpunan yang dikumpulkan di periode berjalan, disertai mini bar proporsional dan persentase pencapaian target individual.

**Alasan ditunda:** Perlu konfirmasi bahwa setiap transaksi penghimpunan sudah ter-tag ke AM yang bersangkutan secara konsisten. Jika tagging belum lengkap, ranking akan menyesatkan.

---

### 6.7 Widget 6 — Distribusi per Saluran Penghimpunan ⏸ PENDING

> **Status:** Ditunda. Widget ini tidak masuk scope v1. Akan dikerjakan setelah distingsi saluran (transfer bank, HC, tunai, website, UPZ) terverifikasi tersedia di level data transaksi.

**Deskripsi rencana:** Bar chart yang menampilkan kontribusi nominal dari setiap saluran penghimpunan, diurutkan dari terbesar ke terkecil.

**Alasan ditunda:** Perlu konfirmasi apakah flag saluran sudah konsisten ter-record di setiap transaksi, atau masih perlu mapping manual.

---

### 6.8 Widget 7 — Segmentasi Donatur (Stacked Bar Tren)

**Deskripsi:** Stacked bar chart 6 bulan yang memperlihatkan komposisi donatur (individu, korporat, HC/payroll) dan kontribusi nominalnya dari waktu ke waktu.

**Spesifikasi grafik:**
- Tipe: Stacked bar chart
- Tiga segmen per bar: Individu (biru muda), Korporat (ungu muda), HC/Payroll (teal muda)
- Sumbu Y: Nilai dalam jutaan Rupiah

**Sumber data:** Data Donatur Korporat + Data Donatur Individu + Laporan Rekap Data HC

**Aturan bisnis:**
- Donatur yang bertransaksi melalui lebih dari satu saluran dihitung sesuai segmentnya (individu/korporat)
- HC/Payroll dihitung tersendiri karena merupakan saluran khusus dengan mekanisme berbeda

---

### 6.9 Widget 8 — Top Donatur Bulan Ini

**Deskripsi:** Daftar 5 donatur dengan nominal transaksi terbesar di periode berjalan.

**Kolom tampilan:**
- Nama donatur (korporat atau individu)
- Jenis donatur + produk yang disumbangkan
- Nominal transaksi

**Sumber data:** Laporan Top Donatur + Laporan Transaksi Per Donatur

**Aturan bisnis:**
- Menampilkan donatur korporat dan individu dalam satu daftar, diurutkan nominal terbesar
- Badge "Korporat" atau "Individu" ditampilkan pada setiap baris
- Untuk role PHP: nama donatur ditampilkan penuh. Untuk role SPVADM: nama disamarkan sebagian (privasi)
- Tombol "Lihat semua" menuju Laporan Top Donatur

---

### 6.10 Widget 9 (Opsional) — Status SMS & Email Gateway

**Deskripsi:** Ringkasan aktivitas komunikasi donatur untuk periode berjalan — berapa notifikasi donasi yang terkirim, berapa yang gagal, dan berapa yang pending.

**Komponen:**
- Total SMS terkirim vs gagal (dari SMS Log)
- Total email notifikasi terkirim
- Jumlah donatur ulang tahun yang sudah/belum mendapat ucapan (dari SMS/Email Milad)

**Sumber data:** SMS Log + Email Gateway Log

**Aturan bisnis:**
- Widget ini bersifat opsional dan dapat di-toggle on/off oleh ADM
- Hanya tampil untuk role ADM dan SPVPHP
- Jika SMS Gateway tidak aktif/terhubung, widget menampilkan status "Gateway tidak aktif"

---

## 7. Tata Letak Halaman (Layout)

```
┌──────────────────────────────────────────────────────────────────┐
│  Header: Judul + Filter Periode + Refresh                        │
├──────────┬──────────┬──────────┬───────────────────────────────  │
│ Realisasi│  Total   │  Donatur │  Konfirmasi                     │
│ vs Target│ Donatur  │  Rutin HC│  Pending                        │
├──────────────────────────────┬───────────────────────────────────┤
│  Tren Realisasi vs Target    │  Komposisi per Produk ZIS         │
│  (6 bulan, bar chart)        │  (Donut)                          │
├──────────────────────────────┬───────────────────────────────────┤
│  Segmentasi Donatur          │  Top Donatur Bulan Ini            │
│  (Stacked bar 6 bulan)       │                                   │
└──────────────────────────────┴───────────────────────────────────┘
  [Widget Gateway — opsional, baris terpisah di bawah]

  ⏸ Pending (belum ditampilkan di v1):
  [ Pencapaian Target/Produk ] [ Ranking ZIS AM ] [ Saluran Penghimpunan ]
```

---

## 8. Perbedaan Dashboard Penghimpunan vs Dashboard Keuangan

Kedua dashboard menampilkan data penghimpunan, namun dengan perspektif yang berbeda:

| Aspek | Dashboard Keuangan | Dashboard Penghimpunan |
|---|---|---|
| Audiens utama | Supervisor Keuangan, Akuntansi | Tim Fundraising (PHP, SPVPHP) |
| Fokus | Posisi keuangan lembaga | Kinerja operasional fundraising |
| Data penghimpunan | Total nominal, komposisi produk | Target vs realisasi, tren 6 bulan |
| Data donatur | Tidak ada | Ada (segmentasi, top donatur, HC) |
| Kinerja individu AM | Tidak ada | Pending (v1 belum ada) |
| Per saluran | Tidak ada | Pending (v1 belum ada) |
| Komunikasi donatur | Tidak ada | Ada (gateway status, opsional) |
| Anggaran | Ya (semua program) | Tidak (hanya target penghimpunan) |

---

## 9. Ketentuan Non-Fungsional

| Aspek | Ketentuan |
|---|---|
| Performa | Data termuat ≤ 3 detik pada koneksi normal |
| Refresh otomatis | Setiap 5 menit |
| Responsif | Resolusi minimal 1280×768 |
| Privasi data donatur | Nama donatur di widget Top Donatur disamarkan untuk SPVADM |
| Audit | Akses dashboard dicatat di Auditrail |

---

## 10. Kriteria Penerimaan (Acceptance Criteria)

- [ ] Widget realisasi vs target menampilkan persentase akurat dari data target yang sudah di-entry
- [ ] Jika target belum di-entry, widget menampilkan pesan "Target belum ditetapkan" alih-alih angka 0%
- [ ] Tren 6 bulan menampilkan bar realisasi dan target per bulan secara akurat
- [ ] Donut komposisi produk hanya menampilkan produk yang memiliki transaksi di periode terpilih
- [ ] Widget segmentasi donatur menampilkan tiga segmen (individu, korporat, HC) dengan warna berbeda
- [ ] Top donatur diurutkan berdasarkan nominal terbesar
- [ ] Filter periode memperbarui semua widget aktif secara bersamaan
- [ ] Widget gateway ditampilkan hanya jika SMS/Email Gateway aktif dan terhubung
- [ ] Konfirmasi pending tampil amber segera setelah ada transaksi baru yang belum dikonfirmasi

---

## 11. Keterkaitan dengan Dokumen PRD Lain

| Fitur | Keterkaitan |
|---|---|
| Total penghimpunan | Konsisten dengan Widget 1 di Dashboard Keuangan |
| Komposisi produk ZIS | Versi detail dari donut di Dashboard Keuangan |
| Target penghimpunan | Data diambil dari master yang sama dengan Laporan Target Penghimpunan |
| Top donatur | Versi ringkas dari Laporan Top Donatur di menu Penghimpunan |
| Segmentasi donatur | Berkaitan dengan Laporan Data Donatur dan Laporan Rekap HC |

---

## 12. Fase Pengembangan Selanjutnya

### Prioritas Tinggi — Lanjutan v1 (sudah didefinisikan, menunggu validasi data)

- **v1.1** — Widget Pencapaian Target per Produk (pending dari v1 — menunggu konfirmasi struktur data target per produk)
- **v1.1** — Widget Ranking ZIS Account Manager (pending dari v1 — menunggu konfirmasi tagging AM pada transaksi)
- **v1.1** — Widget Distribusi per Saluran Penghimpunan (pending dari v1 — menunggu konfirmasi flag saluran di data transaksi)

### Pengembangan Lanjutan

- **v1.2** — Drill-down dari widget top donatur ke riwayat lengkap transaksi donatur
- **v1.3** — Analitik retensi donatur: aktif vs lapsed vs baru per periode
- **v1.4** — Peta sebaran donatur per wilayah (berbasis Kantor Wilayah Bank Mandiri yang sudah ada di parameter)
- **v1.5** — Target AM individual yang bisa di-set langsung dari dashboard
- **v1.6** — Notifikasi push ke PHP jika konfirmasi transaksi menumpuk > N item
- **v1.7** — Dashboard versi mobile untuk monitoring AM di lapangan

---

*Dokumen ini merupakan dasar diskusi awal dan terbuka untuk revisi sebelum masuk tahap development.*

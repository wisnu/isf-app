# Product Requirements Document (PRD)
## Dashboard Penyaluran Dana — Sistem Aplikasi Zakat

| | |
|---|---|
| **Versi** | 1.0 |
| **Status** | Draft |
| **Tanggal** | 23 Mei 2025 |
| **Modul Referensi** | Penyaluran → Kegiatan, Laporan, Otorisasi |

---

## 1. Latar Belakang

Modul Penyaluran memiliki alur kerja yang panjang: mulai dari penerimaan proposal, verifikasi mustahiq, pembuatan memo penyaluran, eksekusi program (rutin dan non rutin), hingga realisasi dan pengembalian. Data-data ini tersebar di beberapa sub-menu sehingga tim distribusi (DIST) dan supervisor (SPVDIST) harus berpindah-pindah halaman untuk mendapat gambaran utuh kondisi penyaluran.

Dashboard ini menyajikan ringkasan operasional penyaluran dalam satu tampilan — dari pipeline proposal hingga realisasi program dan monitoring piutang — sehingga mempercepat respons dan pengambilan keputusan.

---

## 2. Tujuan Produk

- Memberikan visibilitas penuh atas siklus penyaluran dalam satu halaman.
- Memantau pipeline proposal: masuk → verifikasi → disetujui → tersalur → ditolak.
- Melacak realisasi program rutin dan non rutin terhadap anggaran secara real-time.
- Menyediakan alert dini untuk piutang realisasi yang jatuh tempo dan memo yang tertunda.
- Memonitor distribusi mustahiq per program dan per jenis program.

---

## 3. Pengguna (User Roles)

| Role | Kode | Akses Dashboard |
|---|---|---|
| Administrator | ADM | Semua widget |
| Supervisor Distribusi | SPVDIST | Semua widget |
| Staf Distribusi | DIST | Semua widget kecuali ringkasan otorisasi |
| Quality Assurance | QAC | View only — widget laporan saja |
| Supervisor Admin | SPVADM | Semua widget |

---

## 4. Ruang Lingkup

### 4.1 Dalam Ruang Lingkup (In Scope)
- Halaman dashboard read-only khusus modul penyaluran
- Filter periode (bulan/tahun)
- 7 widget utama (dijabarkan di seksi 6)
- Penyesuaian tampilan berdasarkan role pengguna

### 4.2 Di Luar Ruang Lingkup (Out of Scope)
- Input atau edit data dari dashboard
- Drill-down ke detail transaksi individual (fase berikutnya)
- Dashboard per cabang atau per mitra
- Notifikasi push / email alert
- Export dashboard

---

## 5. Asumsi dan Dependensi

- Data bersumber dari database modul Penyaluran yang sudah berjalan — tidak ada sumber data baru.
- Status proposal (masuk, verifikasi, disetujui, tersalur, ditolak) sudah terdefinisi di sistem existing.
- Program Rutin dan Non Rutin sudah terdistingtif di master data.
- Anggaran per program sudah ter-entry melalui modul Anggaran.
- Mata uang default: Rupiah (IDR).

---

## 6. Spesifikasi Fitur

### 6.1 Header & Filter Periode

**Deskripsi:** Bagian atas dashboard dengan kontrol navigasi waktu.

**Komponen:**
- Judul: "Dashboard Penyaluran Dana"
- Dropdown filter: Bulan + Tahun
- Tombol Refresh
- Timestamp "Terakhir diperbarui: [waktu]"

**Aturan bisnis:**
- Default = bulan dan tahun berjalan
- Perubahan filter memperbarui semua widget secara serentak

---

### 6.2 Widget 1 — Kartu Metrik Utama (4 Kartu)

**Deskripsi:** Empat kartu KPI paling kritis di baris teratas.

| No | Kartu | Sumber Data | Keterangan |
|---|---|---|---|
| 1 | Total penyaluran | Realisasi Program Rutin + Non Rutin | Akumulasi bulan berjalan + % vs bulan lalu |
| 2 | Total mustahiq | Laporan Penyaluran Per Mustahiq | Jumlah penerima manfaat periode berjalan |
| 3 | Proposal masuk | Proposal Bantuan Dana | Total + highlight jumlah yang belum diproses |
| 4 | Data belum otorisasi | List Data Belum Otorisasi | Jumlah item pending, tampil amber jika > 0 |

**Aturan bisnis:**
- Kartu "Belum Otorisasi" hanya tampil untuk role: ADM, SPVDIST, SPVADM
- Indikator naik/turun pada kartu Total Penyaluran: hijau jika meningkat, merah jika menurun
- Kartu "Proposal masuk" menampilkan badge merah jika ada proposal > 7 hari belum diproses

---

### 6.3 Widget 2 — Realisasi Penyaluran per Program

**Deskripsi:** Bar chart pengelompokan realisasi nominal per program, dibedakan antara rutin dan non rutin.

**Spesifikasi grafik:**
- Tipe: Grouped bar chart
- Sumbu X: Nama program penyaluran aktif
- Sumbu Y: Nilai realisasi dalam ribuan/jutaan Rupiah
- Dataset 1 (biru): Program Rutin
- Dataset 2 (hijau teal): Program Non Rutin

**Sumber data:** Realisasi Program Rutin + Realisasi Program Non Rutin

**Aturan bisnis:**
- Hanya program yang memiliki realisasi pada periode terpilih ditampilkan
- Tooltip menampilkan nilai nominal lengkap saat hover
- Jika tidak ada realisasi rutin pada suatu program, bar biru tidak muncul (dan sebaliknya)

---

### 6.4 Widget 3 — Komposisi Penyaluran per Jenis Program

**Deskripsi:** Donut chart proporsi penyaluran berdasarkan jenis program (Pendidikan, Kesehatan, Ekonomi, Dakwah, Sosial, dll.).

**Sumber data:** Master Jenis Program + Realisasi Program

**Aturan bisnis:**
- Segmen sesuai dengan data master Jenis Program yang aktif
- Jenis program dengan proporsi < 2% dikelompokkan sebagai "Lainnya"
- Nilai tengah donut menampilkan total penyaluran periode berjalan

---

### 6.5 Widget 4 — Realisasi vs Anggaran per Program

**Deskripsi:** Progress bar horizontal per program yang memperlihatkan serapan anggaran.

**Komponen per baris:**
- Label kiri: Nama program
- Label kanan: Persentase realisasi
- Progress bar dengan warna threshold

**Threshold warna:**

| Rentang | Warna | Makna |
|---|---|---|
| 0–50% | Biru | Normal |
| 51–80% | Biru tua | Berjalan baik |
| 81–95% | Amber | Mendekati batas |
| > 95% | Merah | Kritis |

**Sumber data:** Inquiry Anggaran + Realisasi Program

**Aturan bisnis:**
- Hanya program dengan anggaran aktif yang ditampilkan
- Maksimal 8 program; jika lebih tampilkan tombol "Lihat semua"
- Widget hanya tampil untuk role: ADM, SPVDIST, DIST, SPVADM

---

### 6.6 Widget 5 — Funnel Proposal Penyaluran

**Deskripsi:** Visualisasi funnel horizontal yang menampilkan jumlah proposal di setiap tahap proses.

**Tahapan funnel:**

| Tahap | Sumber | Keterangan |
|---|---|---|
| Masuk | Proposal Bantuan Dana | Semua proposal yang diterima |
| Diverifikasi | Proposal dengan status terverifikasi | Sudah dicek kelengkapan |
| Disetujui | Memo Penyaluran diterbitkan | Sudah ada memo |
| Disalurkan | Realisasi Program | Dana sudah diterima mustahiq |
| Ditolak | Proposal status ditolak | Tidak memenuhi syarat |

**Sumber data:** Proposal Bantuan Dana + Memo Penyaluran + Realisasi Program

**Aturan bisnis:**
- Setiap tahap menampilkan jumlah proposal (bukan nominal)
- Proposal "Belum diproses" (masuk tapi belum diverifikasi > 7 hari) dicatat sebagai info tambahan di bawah funnel
- Conversion rate dari Masuk → Disalurkan ditampilkan sebagai persentase

---

### 6.7 Widget 6 — Memo Penyaluran Terbaru

**Deskripsi:** Daftar 5 memo penyaluran terakhir beserta statusnya sebagai activity feed.

**Kolom tampilan:**
- Nama program / kegiatan
- Jenis (Rutin / Non Rutin) — badge
- Tanggal memo
- Status

**Status badge:**

| Status | Warna | Kondisi |
|---|---|---|
| Tersalur | Hijau | Realisasi sudah selesai |
| Proses | Biru | Sedang dalam eksekusi |
| Pending | Amber | Belum ada tindak lanjut |
| Otorisasi | Ungu | Menunggu persetujuan supervisor |

**Sumber data:** List Memo Program Penyaluran Rutin + List Memo Program Penyaluran Non Rutin

**Aturan bisnis:**
- Diurutkan berdasarkan tanggal terbaru
- Link "Lihat semua" mengarahkan ke halaman Memo Penyaluran

---

### 6.8 Widget 7 — Piutang Realisasi Penyaluran

**Deskripsi:** Daftar mitra/lembaga yang masih memiliki piutang realisasi outstanding.

**Kolom tabel:**
- Nama mitra / mustahiq lembaga
- Nominal piutang
- Status

**Status:**

| Status | Warna | Kondisi |
|---|---|---|
| Jatuh tempo | Amber | Sudah melewati tanggal jatuh tempo |
| Berjalan | Biru | Belum jatuh tempo |

**Sumber data:** Laporan Piutang Realisasi Penyaluran

**Aturan bisnis:**
- Total outstanding ditampilkan di baris footer tabel
- Piutang yang sudah jatuh tempo diberi tanda visual lebih menonjol
- Maksimal 5 baris; link "Lihat semua" ke laporan lengkap
- Diurutkan: jatuh tempo terlebih dahulu, lalu berdasarkan nominal terbesar

---

### 6.9 Widget 8 — Tren Penyaluran 6 Bulan (Rutin vs Non Rutin)

**Deskripsi:** Line chart perbandingan tren penyaluran rutin vs non rutin selama 6 bulan terakhir.

**Spesifikasi grafik:**
- Tipe: Line chart dual series
- Series 1 (biru, garis penuh): Program Rutin
- Series 2 (hijau, garis putus-putus): Program Non Rutin
- Sumbu X: 6 bulan terakhir
- Sumbu Y: Nilai dalam jutaan Rupiah

**Sumber data:** Laporan Program Penyaluran Rutin + Laporan Program Penyaluran Non Rutin

---

## 7. Tata Letak Halaman (Layout)

```
┌──────────────────────────────────────────────────────────────────┐
│  Header: Judul + Filter Periode + Tombol Refresh                 │
├──────────┬──────────┬──────────┬───────────────────────────────  │
│  Total   │  Total   │ Proposal │  Data Belum                     │
│  Penyalur│ Mustahiq │  Masuk   │  Otorisasi                      │
├──────────────────────────────┬───────────────────────────────────┤
│  Realisasi per Program       │  Komposisi per Jenis              │
│  (Grouped Bar)               │  Program (Donut)                  │
├───────────────┬──────────────┬───────────────────────────────────┤
│  Realisasi vs │  Funnel      │  Memo Penyaluran                  │
│  Anggaran     │  Proposal    │  Terbaru                          │
├──────────────────────────────┬───────────────────────────────────┤
│  Tren 6 Bulan                │  Piutang Realisasi                │
│  (Rutin vs Non Rutin)        │  Penyaluran                       │
└──────────────────────────────┴───────────────────────────────────┘
```

---

## 8. Ketentuan Non-Fungsional

| Aspek | Ketentuan |
|---|---|
| Performa | Data termuat ≤ 3 detik pada koneksi normal |
| Refresh otomatis | Setiap 5 menit |
| Responsif | Resolusi minimal 1280×768 |
| Keamanan | Data mengikuti hak akses role yang sudah ada |
| Audit | Akses dashboard tercatat di Auditrail |

---

## 9. Kriteria Penerimaan (Acceptance Criteria)

- [ ] Semua widget menampilkan data konsisten dengan laporan di menu Laporan Penyaluran
- [ ] Filter periode mengubah data seluruh widget secara bersamaan
- [ ] Funnel proposal menampilkan jumlah yang akurat sesuai status masing-masing tahap
- [ ] Widget Otorisasi Pending tidak tampil untuk role DIST
- [ ] Widget Anggaran tidak tampil untuk role QAC
- [ ] Progress bar anggaran berubah warna sesuai threshold yang ditentukan
- [ ] Piutang jatuh tempo muncul di urutan teratas daftar
- [ ] Memo terbaru diurutkan berdasarkan tanggal terbaru secara akurat

---

## 10. Keterkaitan dengan Dashboard Keuangan

Dashboard Penyaluran ini bersifat operasional dan melengkapi Dashboard Keuangan yang sudah didefinisikan sebelumnya. Hubungan antar keduanya:

| Data | Dashboard Keuangan | Dashboard Penyaluran |
|---|---|---|
| Total penyaluran (nominal) | ✓ Ringkasan | ✓ Detail per program |
| Realisasi vs anggaran | ✓ Semua program | ✓ Focus penyaluran |
| Piutang realisasi | — | ✓ Detail per mitra |
| Funnel proposal | — | ✓ |
| Mustahiq | — | ✓ |
| Memo penyaluran | — | ✓ |

---

## 11. Fase Pengembangan Selanjutnya (Out of Scope v1)

- **v1.1** — Drill-down dari widget realisasi ke detail transaksi per mustahiq
- **v1.2** — Filter tambahan per jenis program dan per mitra
- **v1.3** — Dashboard per cabang/wilayah distribusi
- **v1.4** — Notifikasi otomatis untuk piutang jatuh tempo dan proposal terbengkalai

---

*Dokumen ini merupakan dasar diskusi awal dan terbuka untuk revisi sebelum masuk tahap development.*

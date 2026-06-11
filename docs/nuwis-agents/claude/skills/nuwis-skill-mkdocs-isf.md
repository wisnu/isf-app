# Skill: nuwis-skill-mkdocs-isf
## Template MkDocs untuk Panduan Pengguna isf-app ZISWAF

---

## mkdocs.yml (konfigurasi utama)

Simpan di `docs/panduan/mkdocs.yml`:

```yaml
site_name: Panduan isf-app ZISWAF
site_description: Panduan penggunaan aplikasi ZISWAF untuk operator lembaga zakat
site_author: Tim ISF
docs_dir: docs
site_dir: site

theme:
  name: material
  language: id
  palette:
    - scheme: default
      primary: teal
      accent: teal
      toggle:
        icon: material/brightness-7
        name: Mode gelap
    - scheme: slate
      primary: teal
      accent: teal
      toggle:
        icon: material/brightness-4
        name: Mode terang
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.suggest
    - content.code.copy
    - toc.follow

plugins:
  - search:
      lang: id

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - attr_list
  - md_in_html
  - tables
  - toc:
      permalink: true

nav:
  - Beranda: index.md
  - Memulai:
    - Login: memulai/login.md
    - Navigasi Aplikasi: memulai/navigasi.md
    - Profil & Password: memulai/profil.md
  - Keuangan:
    - Transaksi:
      - Penghimpunan Dana: keuangan/transaksi/penghimpunan.md
      - Penyaluran Dana: keuangan/transaksi/penyaluran.md
      - Kas Masuk/Keluar: keuangan/transaksi/kas.md
    - Laporan:
      - keuangan/laporan/index.md
    - Master Data:
      - COA (Kode Akun): keuangan/master/coa.md
      - Kas: keuangan/master/kas.md
      - Bank: keuangan/master/bank.md
    - Monitoring Otorisasi: keuangan/otorisasi.md
  - Admin:
    - Manajemen User: admin/users.md
    - Role & Menu: admin/role-menu.md
```

---

## Template: Beranda (`docs/index.md`)

```markdown
# Panduan Pengguna isf-app ZISWAF

Selamat datang di panduan penggunaan **isf-app**, aplikasi manajemen ZISWAF
(Zakat, Infaq, Sedekah, dan Wakaf) untuk lembaga amil zakat.

## Mulai dari Sini

<div class="grid cards" markdown>

- :material-login: **Belum pernah login?**

    Pelajari cara login dan navigasi aplikasi.

    [:octicons-arrow-right-24: Cara Login](memulai/login.md)

- :material-cash-multiple: **Input Transaksi**

    Catat penghimpunan dan penyaluran dana.

    [:octicons-arrow-right-24: Transaksi](keuangan/transaksi/penghimpunan.md)

- :material-file-chart: **Lihat Laporan**

    Akses laporan keuangan dan transaksi.

    [:octicons-arrow-right-24: Laporan](keuangan/laporan/index.md)

- :material-check-circle: **Otorisasi**

    Setujui atau tolak transaksi yang menunggu.

    [:octicons-arrow-right-24: Monitoring Otorisasi](keuangan/otorisasi.md)

</div>

## Butuh Bantuan?

Hubungi administrator sistem di lembaga Anda jika menemui kendala
yang tidak tercakup dalam panduan ini.
```

---

## Template: Halaman CRUD (List + Form)

Gunakan untuk: Penghimpunan, Penyaluran, Kas, COA, Bank, dll.

```markdown
# {Nama Fitur}

!!! info "Siapa yang bisa mengakses"
    Halaman ini dapat diakses oleh: **{Nama Peran 1}**, **{Nama Peran 2}**.

{Satu paragraf singkat: apa fungsi halaman ini dan kapan digunakan.}

---

## Melihat Daftar {Nama}

Buka menu **{Nama Menu Utama}** → **{Sub Menu}** → **{Nama Fitur}**.

![(Daftar {nama fitur})](../assets/screenshots/{fitur}-daftar.png)

Halaman menampilkan daftar {nama} dengan informasi:

| Kolom | Keterangan |
|---|---|
| {Kolom 1} | {Penjelasan singkat} |
| {Kolom 2} | {Penjelasan singkat} |

**Mencari data:** Ketik kata kunci di kolom pencarian lalu tekan **Enter**.

---

## Menambah {Nama} Baru

1. Klik tombol **Tambah** di pojok kanan atas.

    ![(Form tambah {nama})](../assets/screenshots/{fitur}-tambah.png)

2. Isi kolom-kolom berikut:

    | Kolom | Keterangan | Wajib? |
    |---|---|---|
    | {Field 1} | {Penjelasan} | Ya |
    | {Field 2} | {Penjelasan} | Ya |
    | {Field 3} | {Penjelasan} | Tidak |

3. Klik **Simpan**.

!!! tip "Tips"
    {Tips relevan, misal: tanggal otomatis terisi hari ini, bisa diubah jika perlu.}

---

## Mengubah {Nama}

1. Klik ikon **Edit** (ikon pensil) pada baris data yang ingin diubah.
2. Ubah kolom yang diperlukan.
3. Klik **Simpan**.

---

## Menghapus {Nama}

1. Klik ikon **Hapus** (ikon tempat sampah) pada baris yang ingin dihapus.
2. Periksa data yang ditampilkan di jendela konfirmasi.
3. Klik **Hapus** untuk mengkonfirmasi.

!!! warning "Perhatian"
    Data yang sudah dihapus tidak dapat dipulihkan. Pastikan data yang dipilih sudah benar.

---

## Catatan Penting

- {Catatan bisnis penting 1}
- {Catatan bisnis penting 2}

---

## Pertanyaan Umum

**{Pertanyaan umum 1?}**
{Jawaban singkat.}

**{Pertanyaan umum 2?}**
{Jawaban singkat.}
```

---

## Template: Halaman Laporan

Gunakan untuk: semua halaman laporan yang punya filter periode + tombol Tampilkan + Export Excel.

```markdown
# Laporan {Nama Laporan}

!!! info "Siapa yang bisa mengakses"
    Laporan ini dapat diakses oleh: **{Nama Peran 1}**, **{Nama Peran 2}**.

{Satu kalimat: laporan ini menampilkan data apa.}

---

## Cara Menampilkan Laporan

1. Buka menu **Keuangan** → **Laporan** → **{Nama Laporan}**.

2. Isi filter periode:
    - **Tanggal Awal** — tanggal mulai data yang ingin ditampilkan
    - **Tanggal Akhir** — tanggal akhir data
    {- Filter tambahan jika ada}

    ![(Filter laporan {nama})](../assets/screenshots/laporan-{nama}-filter.png)

3. Klik tombol **Tampilkan**.

4. Laporan akan muncul di bawah filter.

    ![(Hasil laporan {nama})](../assets/screenshots/laporan-{nama}-hasil.png)

---

## Mengunduh ke Excel

Setelah laporan ditampilkan:

1. Klik tombol **Export Excel**.
2. File `.xlsx` akan otomatis terunduh ke komputer Anda.

!!! info "Informasi"
    Tombol **Export Excel** hanya aktif setelah laporan ditampilkan.

---

## Penjelasan Kolom

| Kolom | Keterangan |
|---|---|
| {Kolom 1} | {Penjelasan} |
| {Kolom 2} | {Penjelasan} |

---

## Catatan Penting

- {Catatan relevan, misal: laporan ini hanya menampilkan transaksi yang sudah diotorisasi.}
```

---

## Template: Halaman Otorisasi

Gunakan untuk halaman Monitoring Otorisasi.

```markdown
# Monitoring Otorisasi

!!! info "Siapa yang bisa mengakses"
    Halaman ini dapat diakses oleh: **Supervisor Keuangan**, **Supervisor Distribusi**.

Halaman ini menampilkan daftar transaksi yang menunggu persetujuan Anda.
Setiap transaksi yang dibuat oleh staf input akan masuk ke sini sebelum
benar-benar tersimpan ke sistem.

---

## Memahami Status Transaksi

| Status | Arti |
|---|---|
| **Menunggu** | Transaksi baru masuk, belum ditinjau |
| **Diproses** | Sedang diproses oleh sistem (tunggu sebentar) |
| **Terotorisasi** | Transaksi disetujui dan sudah tersimpan |
| **Ditolak** | Transaksi ditolak, dapat direvisi oleh pembuat |

---

## Menyetujui Transaksi

1. Buka menu **Keuangan** → **Monitoring** → **Otorisasi**.

    ![(Daftar transaksi menunggu)](../assets/screenshots/otorisasi-daftar.png)

2. Klik baris transaksi yang ingin ditinjau untuk melihat detailnya.

    ![(Detail transaksi)](../assets/screenshots/otorisasi-detail.png)

3. Periksa data transaksi dengan teliti.

4. Klik **Setujui** untuk menyetujui, atau **Tolak** untuk menolak.

---

## Menyetujui Beberapa Transaksi Sekaligus

1. Centang kotak di sebelah kiri setiap transaksi yang ingin disetujui.
2. Klik tombol **Otorisasi (N)** yang muncul di bagian atas.

!!! warning "Perhatian"
    Pastikan setiap transaksi sudah Anda tinjau sebelum menyetujui secara massal.

---

## Transaksi Menampilkan Status "Diproses" Lama

Jika sebuah transaksi menampilkan status **Diproses** lebih dari beberapa menit,
hubungi administrator sistem. Status ini seharusnya berubah otomatis.

---

## Catatan Penting

- Transaksi yang sudah **Terotorisasi** tidak dapat diubah atau dibatalkan.
- Transaksi yang **Ditolak** dapat direvisi dan diajukan ulang oleh pembuat.
```

---

## Template: Halaman Login (`memulai/login.md`)

```markdown
# Login ke Aplikasi

## Cara Login

1. Buka aplikasi melalui browser di alamat yang diberikan administrator.

2. Masukkan **Nama Pengguna** dan **Kata Sandi** Anda.

    ![(Halaman login)](../assets/screenshots/login.png)

3. Klik tombol **Masuk**.

!!! tip "Tips"
    Nama pengguna tidak membedakan huruf besar/kecil.
    `wisnu`, `WISNU`, dan `Wisnu` akan masuk ke akun yang sama.

---

## Lupa Kata Sandi

Hubungi administrator sistem di lembaga Anda untuk mereset kata sandi.

---

## Keluar dari Aplikasi

Klik nama pengguna di pojok kanan atas, lalu pilih **Keluar**.
```

---

## Template: Halaman Dashboard

```markdown
# Dashboard {Nama Dashboard}

!!! info "Siapa yang bisa mengakses"
    Halaman ini dapat diakses oleh: **{Nama Peran}**.

Dashboard ini menampilkan ringkasan {domain} secara real-time.

---

## Widget yang Tersedia

### {Nama Widget 1}

Menampilkan {deskripsi singkat}. Data diperbarui setiap kali halaman dimuat.

### {Nama Widget 2}

Menampilkan {deskripsi singkat}.

---

## Catatan

- Setiap widget memuat data secara independen. Jika satu widget gagal,
  widget lain tetap menampilkan datanya.
- Klik **Refresh** di browser untuk memperbarui semua widget.
```

---

## Konvensi Screenshot Placeholder

Format nama file screenshot:

```
{fitur}-{aksi}.png

Contoh:
  penghimpunan-daftar.png       ← tampilan daftar
  penghimpunan-tambah.png       ← form tambah terbuka
  penghimpunan-edit.png         ← form edit terbuka
  penghimpunan-hapus.png        ← konfirmasi hapus
  laporan-kas-filter.png        ← bagian filter laporan
  laporan-kas-hasil.png         ← hasil laporan ditampilkan
  otorisasi-daftar.png          ← daftar menunggu otorisasi
  otorisasi-detail.png          ← drawer detail transaksi
  login.png                     ← halaman login
```

Semua screenshot disimpan di: `docs/panduan/docs/assets/screenshots/`

---

## Cara Menjalankan MkDocs Secara Lokal

```bash
# Install MkDocs Material:
pip install mkdocs-material

# Jalankan dev server:
cd docs/panduan
mkdocs serve
# → buka http://localhost:8000

# Build static site:
mkdocs build
# → output di docs/panduan/site/
```

---

## Cara Deploy ke GitHub Pages (opsional)

```bash
cd docs/panduan
mkdocs gh-deploy
```

Pastikan repository memiliki akses GitHub Pages yang aktif.

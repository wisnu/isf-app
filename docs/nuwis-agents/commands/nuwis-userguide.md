---
description: "Generate panduan MkDocs untuk operator — /nuwis-userguide <fitur|--setup|--all> [--portal=zakat|wakaf]"
---

Generate panduan pengguna MkDocs untuk: $ARGUMENTS

Tentukan mode dari argumen:

---

## Mode 1: Satu Fitur (`/nuwis-userguide <nama-fitur>`)

Jika $ARGUMENTS adalah nama fitur (bukan flag `--setup` atau `--all`):

@nuwis-userguide — generate satu halaman panduan:

1. Temukan Vue page yang cocok di `apps_{portal}/web-vue/src/pages/`
   - Cari berdasarkan nama: misal "penghimpunan" → `PenghimpunanPage.vue` atau `PenghimpunanDanaPage.vue`
   - Jika portal tidak disebutkan, default ke zakat

2. Baca context dari kode:
   - Vue page (label, field, tombol)
   - `router/index.ts` (path, menu_key)
   - Seed SQL di `infra/db/migrations/seed/` (roles yang punya akses)
   - MIGRATION_ANALYSIS di `docs/todos/` jika ada

3. Gunakan skill `.claude/skills/nuwis-skill-mkdocs-isf.md`:
   - Tentukan tipe template (CRUD / Laporan / Otorisasi)
   - Tulis halaman panduan lengkap dalam Bahasa Indonesia

4. Tulis file ke `docs/panduan/docs/{section}/{fitur}.md`

5. Tampilkan:
   - Path file yang dibuat
   - Cuplikan isi halaman (20 baris pertama)
   - Instruksi menambahkan ke nav di `mkdocs.yml`

---

## Mode 2: Setup Struktur Baru (`/nuwis-userguide --setup`)

Jika $ARGUMENTS mengandung `--setup`:

@nuwis-userguide — buat struktur MkDocs isf-app dari nol:

1. Buat semua folder:
   ```
   docs/panduan/
   docs/panduan/docs/
   docs/panduan/docs/memulai/
   docs/panduan/docs/keuangan/
   docs/panduan/docs/keuangan/transaksi/
   docs/panduan/docs/keuangan/laporan/
   docs/panduan/docs/keuangan/master/
   docs/panduan/docs/admin/
   docs/panduan/docs/assets/
   docs/panduan/docs/assets/screenshots/
   ```

2. Tulis `docs/panduan/mkdocs.yml` (template dari skill)

3. Tulis halaman wajib:
   - `docs/panduan/docs/index.md` (beranda)
   - `docs/panduan/docs/memulai/login.md`
   - `docs/panduan/docs/memulai/navigasi.md` (placeholder)
   - `docs/panduan/docs/keuangan/laporan/index.md` (placeholder)

4. Tulis `docs/panduan/docs/assets/screenshots/.gitkeep`

5. Tampilkan ringkasan semua file yang dibuat dan instruksi `mkdocs serve`

---

## Mode 3: Semua Fitur (`/nuwis-userguide --all`)

Jika $ARGUMENTS mengandung `--all`:

@nuwis-userguide — generate docs untuk semua fitur:

1. Scan `apps_{portal}/web-vue/src/pages/` — daftar semua `.vue` files
   - Skip: `LoginPage.vue`, file di `dashboard/` yang berisi widgets saja
   - Default portal: zakat (atau gunakan `--portal=wakaf` jika disebutkan)

2. Untuk setiap page yang valid:
   - Jalankan proses yang sama dengan Mode 1
   - Tulis file ke lokasi yang tepat

3. Update nav di `docs/panduan/mkdocs.yml` dengan semua halaman baru
   - Grup sesuai section (keuangan/transaksi, keuangan/laporan, dll)

4. Tampilkan:
   - Daftar semua file yang dibuat
   - Ringkasan: N halaman dibuat, N halaman dilewati
   - Instruksi `mkdocs serve` untuk preview

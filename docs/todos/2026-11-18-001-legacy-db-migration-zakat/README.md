# Migrasi DB Legacy → isf-app (Portal Zakat)

**Tanggal analisis:** 2026-11-18
**Sumber:** `db/mziss_laz_2026-11-17_22.00.backup` (dump produksi legacy, nama DB asal `isocial_laz`, PostgreSQL **12.22**)
**Restore ke:** `mziss_laz_origin` @ localhost:5432 (PG 18.6) — restore bersih, 1 error wajar (`schema "public" already exists`)
**Pembanding (struktur isf-app):** `mziss_laz` (DB dev isf-app)
**Skrip migrasi:** [`infra/db/legacy-migration/zakat/`](../../../infra/db/legacy-migration/zakat/) — lihat [README eksekusi](../../../infra/db/legacy-migration/README.md)

---

## 1. Kesimpulan

1. **Struktur isf-app = struktur legacy + tambahan.** Tidak ada objek legacy yang
   di-drop, di-rename, atau berubah tipe di `mziss_laz`. Seluruh perbedaan bersifat
   **aditif**, jadi aplikasi legacy (DAF) tetap bisa berjalan di DB yang sama setelah migrasi.
2. Perbedaannya kecil: **2 schema baru** (`otorisasi`, `dwh`), **7 kolom baru** di 6
   tabel legacy, **1 default** kolom, **9 index** baru di tabel legacy.
3. Migrasi sudah diuji pada backup produksi di **PG 12.22** (versi server produksi)
   dan **PG 18.6**: selesai ±5 detik, postcheck lolos, lalu katalog hasil migrasi
   dibandingkan dengan `mziss_laz` → **0 objek hilang/berlebih, 0 kolom berbeda**.
   Sisa selisih hanya format *deparse* `IN (...)` di 4 view + 3 CHECK (semantik identik).
4. Ada **satu jebakan data penting**: `transaction.batchupload.authstatus` (kolom baru,
   default `'P'`). Seluruh 2.456 batch produksi sudah diotorisasi di sistem lama; tanpa
   penanganan khusus semuanya tampil *pending* dan bisa di-approve ulang → **posting ganda**.
   Skrip migrasi menyetelnya ke `'A'` bila `authorizeduser` terisi.
5. **Auth DB (`isf_auth_zakat`) dibangun baru** (§6): schema + menu/RBAC dari isf-app,
   user dari `enterprise.userapp` produksi. Password legacy tidak bisa dikonversi →
   32 user aktif mendapat password sementara (CSV 0600). Login user produksi sudah
   diuji end-to-end melalui BFF + api-python terhadap DB hasil migrasi.

## 2. Ringkasan volume

| | `mziss_laz_origin` (produksi) | `mziss_laz` (dev isf-app) |
|---|---:|---:|
| Ukuran DB | 2.399 MB | 2.232 MB |
| `transaction.transaction` | 267.816 (s.d. **2026-11-17**) | 197.464 (s.d. 2026-06-20) |
| `transaction.journalitem` | 543.149 | 398.480 |
| `fund.donor` | 73.049 | 70.222 |
| `enterprise.userapp` | 82 (32 aktif) | 83 |

DB dev adalah snapshot legacy yang lebih lama (±Juni 2026) + data uji isf-app.
Produksi adalah sumber kebenaran untuk seluruh data bisnis.

## 3. Diff struktur (`mziss_laz_origin` → `mziss_laz`)

Hasil `tools/compare_schema.py` ([ringkasan](artifacts/schema-diff-summary.txt), [detail JSON](artifacts/schema-diff.json)):

| Objek | Hanya di isf-app | Hanya di legacy | Berubah |
|---|---:|---:|---:|
| Extension | 0 | 0 | – |
| Schema | **2** | 0 | – |
| Tabel | **17** | 0 | – |
| Kolom (tabel yang sama) | **7** | 0 | 1 (default) |
| Sequence | **14** | 0 | – |
| Constraint | **31** | 0 | 0 |
| Index | **33** | 0 | 0 |
| View | **29** | 0 | 0 |
| Function | 0 | 0 | 0 |
| Trigger | 0 | 0 | 0 |
| Type/Domain | 0 | 0 | – |

### 3.1 Schema baru

| Schema | Isi | Fungsi di isf-app |
|---|---|---|
| `otorisasi` | `submission`, `approval_log`, `entity_config` + 2 sequence, 6 index | Maker-checker: semua transaksi & master sensitif masuk sini dulu (DRAFT/PENDING/PROCESSING/AUTHORIZED/REJECTED) |
| `dwh` | 14 tabel (`dim_branch`, `dim_donor`, `dim_fund_type`, `dm_*`, `fact_fundraising_monthly`, `etl_log`, `etl_watermark`) + 12 sequence + **29 view** `v_*` | View laporan (report-api) & datamart dashboard |

29 view `dwh.v_*` adalah fondasi **semua laporan** report-api (jurnal harian, buku besar,
neraca, arus kas, penghimpunan, penyaluran, piutang, uang muka, export penghimpunan, dll.).
View ini hanya membaca tabel legacy — tidak menyimpan data.

### 3.2 Kolom baru di tabel legacy

| Tabel | Kolom | Tipe / default | Asal (repo) | Dipakai oleh |
|---|---|---|---|---|
| `fund.individualdonor` | `donorgroup` | `varchar(1)` | `fund/V001` | Data Donatur Individu |
| `transaction.batchupload` | `authstatus` | `varchar(1)` default `'P'` | `transaction/009` | Upload Penghimpunan (P/Q/A/F) |
| `transaction.budgetowner` | `tglubah`, `userpengubah`, `terminalubah` | `timestamp` default `now`, `varchar(30)` ×2 | `transaction/011` | Pemilik Anggaran (audit) |
| `transaction.humancapitalbatch` | `namafile` | `varchar(200)` | `transaction/012` | Upload ZIS Rutin (HC) |
| `transaction.transactiontype` | `jenis_limit` | `varchar(1)`, diisi `'O'` | `transaction/add_jenis_limit…` | Cek limit otorisasi |
| `transaction.batchuploaditem` | `amountzakatperusahaan` | **default** `NULL → 0` | `transaction/009` | Upload Penghimpunan |

Catatan: tabel `transaction.budgetowner`, `budgetownerhierarchy`, `humancapitalbatch*`
**sudah ada di produksi** (dibuat oleh legacy), jadi migrasi `010`/`012` cukup
menambah kolom + index, bukan `CREATE TABLE`.

### 3.3 Index baru di tabel legacy
9 index pada `transaction.humancapitalbatch`, `humancapitalbatchitem`,
`humancapitalpassedreport` (batchid, donorid, transactionid, employeenumber,
transactiondate, batchperioddesc, uploaduserid). Sisa 24 index ada di schema baru.

## 4. Diff data (tabel kecil ≤ 20.000 baris)

Hasil `tools/data_diff.py` ([JSON](artifacts/data-diff.json)) — 62 tabel berbeda isinya.
Interpretasi per kategori:

| Kategori | Contoh | Keputusan |
|---|---|---|
| **Produksi lebih baru** (baris hanya di legacy) | `program.*` (mustahiq, proposal, realization…), `personalia.dokumen*`, `transaction.batchupload`, `account`, `accounthierarchy` | Ikuti produksi. Tidak ada tindakan. |
| **Data uji isf-app** (baris hanya di dev) | `enterprise.peran` `TESTRL01`, `userapp` `TESTUSR01`, `cashaccount`/`financialaccount` `BANK0061–63`, `account` `530900/530901`, `fund.corporatedonor` 87377, `program.realization*` uji | **Tidak dibawa.** |
| **Counter ID isf-app** | `personalia.id_gen` (DOKUMEN, DISPOSISI, JENISDOKUMEN), `fund.custom_idgen` (BSZ,2026) | **Tidak dibawa** — kode isf-app meng-inisialisasi otomatis dari `MAX(pk)` bila baris belum ada. Menyalin nilai dev justru berbahaya (nilai lebih kecil dari data produksi → bentrok PK). |
| **Config isf-app di schema baru** | `otorisasi.entity_config` (16), `dwh.dim_fund_type` (5), `dwh.dim_branch` | **Dibawa** oleh `04_reference_data.sql` (`dim_branch` diturunkan dari `enterprise.cabang` produksi). |
| **Config legacy yang berbeda** | `transaction.balancesumitemmember`: dev punya 2 mapping (`520200→item 13`, `520100→item 7`) yang **tidak ada** di produksi; produksi punya 56 mapping yang tidak ada di dev. `transaction.parameter.CorporateName`: prod `MAI`, dev `BPZIS`. `glinterface` 7274 accountcode: prod `420204`, dev kosong. | Produksi = sumber kebenaran. **Tidak ditimpa.** Lihat catatan §5.4. |
| **Data transaksional dev** | `otorisasi.submission` (29), `approval_log` (23), `dwh.dm_*`/`fact_*`/`etl_log` | **Tidak dibawa** (data uji / output ETL dari data lama). |

## 5. Catatan yang perlu dilakukan untuk migrasi

### 5.1 Wajib — urutan go-live

- [ ] **Freeze aplikasi legacy** (atau tetapkan cut-over) sebelum backup final, agar tidak ada transaksi yang tertinggal.
- [ ] Ambil **backup final** produksi (`pg_dump -Fc`), restore ke server target isf-app dengan `--no-owner --no-acl` sebagai role aplikasi.
- [ ] Jalankan `run_migration.sh <db> --dry-run`, lalu `run_migration.sh <db>`.
- [ ] Bila restore **tidak** memakai `--no-owner` (objek tetap dimiliki role `program`, `fund`, dst.), jalankan `90_grants_optional.sql -v app_role=<role>` — dump produksi **tidak berisi GRANT**, dan isf-app memakai satu role lintas schema.
- [ ] Arahkan `DATABASE_URL_ZAKAT` (api-python, report-api, bff-api) ke DB hasil migrasi; restart service.
- [ ] Smoke test: login, dashboard, 1 laporan per kelompok (jurnal harian, neraca, penghimpunan), Upload Penghimpunan (pastikan batch lama tampil **Authorized**), halaman Otorisasi (kosong).

### 5.2 Wajib — auth DB (`isf_auth_zakat`) — skrip: `run_auth_migration.sh`

Legacy tidak punya auth DB; `isf_auth_<portal>` dibuat **baru** di server target.
Login isf-app butuh user di **dua** tempat: `enterprise.userapp` (business DB: peran,
cabang, `tipe_akses_cabang`) **dan** `isf_auth.users` + `user_credentials` +
`tenant_memberships` (auth DB). Lihat §6.

- [ ] `createdb` auth DB (owner = role aplikasi), lalu `run_auth_migration.sh init <business_db> <auth_db> --out <csv>`.
- [ ] **Bagikan password sementara** dari CSV (0600) lewat jalur aman, lalu **hapus CSV**. Minta user mengganti password (Profil → Ganti Password).
- [ ] Arahkan `ISF_AUTH_DATABASE_URL_ZAKAT` ke auth DB baru. **Jangan start bff-api sebelum init selesai** (users kosong → BFF men-seed `ADMIN/admin123`).
- [ ] Menjelang cut-over: `run_auth_migration.sh sync-users …` untuk user baru di legacy (password yang sudah ada tidak berubah).
- [ ] 4 user aktif **tanpa peran** di legacy → login berhasil tapi menu kosong: `IKA`, `MAYA`, `MELVA`, `SYAFII`. Beri peran via Pengelolaan User atau biarkan.
- [ ] `AZZAM`: `status_profil='A'` tapi `kunci_akses='T'` di legacy → di isf-app tetap **aktif** (isf-app hanya memetakan `status_profil`, sama seperti `update_user_status`). Nonaktifkan manual bila memang terkunci.
- [ ] Peran **`IMZ` (SOP VENDOR)** belum punya `role_menu_permission` → user aktif `ARIS` hanya mendapat menu dari peran lain.
- [ ] Akun demo/dev (`ADMIN`, `FINANCE.A`, `FINANCE.B`, `TESTUSR01`) **tidak ikut** — auth DB dibangun dari `userapp` produksi; `13_postcheck.sql` menolak bila ada yang aktif.

### 5.3 Wajib — DWH / ETL

- [ ] Tabel `dwh.dm_*`, `fact_*`, `dim_donor` dibuat **kosong**. ETL belum dibangun ulang pasca insiden NTFS (lihat `docs/reference/history/etl-rebuild-plan.md`). Saat ini **tidak ada kode** yang membaca tabel-tabel ini (dashboard & laporan memakai view `dwh.v_*`), jadi aman — tapi isi setelah ETL tersedia.
- [ ] `dim_branch` di-seed dari `enterprise.cabang` produksi (5 cabang + `UNKNOWN`).

### 5.4 Perlu keputusan bisnis

- [ ] **`transaction.balancesumitemmember`** (config Arus Kas / Perubahan Dana): produksi tidak memiliki mapping `520200→InfaqTakTerikatDist` dan `520100→InfaqTerikatDist` yang ada di dev, dan punya 56 mapping lain. Skrip **tidak** mengubahnya. Validasi laporan Perubahan Dana isf-app terhadap produksi; **jangan** menjalankan `infra/db/migrations/seed/balancesum-config-zakat.sql` ke DB produksi (memberid eksplisit dari snapshot lama → bisa menambah/menabrak mapping produksi).
- [ ] **`transaction.parameter.CorporateName`** produksi = `MAI` (dev `BPZIS`) — pastikan label/kop laporan memakai nilai yang benar.
- [ ] **Paralel run legacy + isf-app?** Bila keduanya menulis ke DB yang sama, counter ID harus satu sumber. isf-app memakai `*.id_gen`/`custom_idgen`/`seq_*` yang sama dengan legacy untuk sebagian besar entitas, tetapi beberapa counter isf-app (DOKUMEN, DISPOSISI, JENISDOKUMEN, BSZ) dibuat sendiri dari `MAX(pk)` — jika legacy menulis ke tabel yang sama tanpa counter ini, bisa terjadi bentrok PK. Rekomendasi: **cut-over penuh**, bukan paralel.

### 5.5 Sudah ditangani oleh skrip (untuk referensi)

- `batchupload.authstatus` historis → `'A'` bila `authorizeduser` terisi (2.456 batch), selain itu `'P'`.
- `transactiontype.jenis_limit` → `'O'` untuk semua kode (33 kode, sama dengan dev).
- `entity_config.menu_key` dinormalisasi ke `finance.monitoring.authorization` (di dev masih campur dengan key lama `keuangan.monitoring.otorisasi`). **Catatan untuk dev:** DB `mziss_laz` sendiri juga masih punya 14 baris dengan key lama.
- DDL `otorisasi`/`dwh` dibersihkan agar jalan di PG12 (`\restrict`, `SET transaction_timeout`, named `NOT NULL` constraint PG18 dihapus).

### 5.6 Berikutnya

- [ ] Portal **Wakaf**: backup `db/mziss_wakaf_2026-11-17_21.00.backup` sudah tersedia — ulangi alur yang sama (`compare_schema.py` → `data_diff.py` → `gen_new_schema_ddl.sh` dengan `mziss_wakaf`). Config balancesum wakaf berbeda (lihat memory *BalanceSum config per-portal*).
- [ ] Seluruh perubahan schema isf-app ke depan sebaiknya ditulis sebagai migrasi bernomor di repo, lalu `05_postcheck.sql` diperbarui — supaya diff berikutnya tetap nol.

## 6. Migrasi auth DB (`isf_auth_zakat`)

### 6.1 Apa yang dibawa

| Objek | Sumber | Keterangan |
|---|---|---|
| Schema `isf_auth` (8 tabel, 2 sequence) | `isf_auth_zakat` dev (generated, PG12-clean) | `users`, `user_credentials`, `user_provider_links`, `tenants`, `tenant_memberships`, `menu`, `role_menu_permission`, `audit_log` |
| `tenants` (2), `menu` (105), `role_menu_permission` (377) | snapshot dev 2026-11-18 | config RBAC — id peran (`ACC`, `KEU`, `SPVKEU`, …) sama dengan `enterprise.peran` produksi |
| `users`, `tenant_memberships` | `enterprise.userapp` **produksi** | 82 user: `status_profil='A'` → `active` (32), lainnya `inactive` (50); `id = username = UPPER(id_user)`; tenant default `perusahaan_a` |
| `user_credentials` | **dibuat baru** | password sementara acak 12 karakter, bcrypt (library sama dengan BFF), hanya untuk user aktif |
| `audit_log`, `user_provider_links` | — | tidak dibawa (log dev / belum ada link Google) |

### 6.2 Kenapa password legacy tidak bisa dipakai
Password legacy disimpan oleh server "Corporate" DAF (`Function_Code='LOGIN'`/`'CHPASS'`
di `docs/legacy-apps/program/script_modules/Corporate.py`) dengan encoding sendiri
(bukan plaintext/hex/base64, 8–11 karakter) — tidak dapat dikonversi ke bcrypt.
Karena itu semua user aktif diberi password sementara.

### 6.3 Temuan & perbaikan saat menyiapkan auth
- **Menu `finance.transactions.fund_transfer` (Transfer Antar Rekening) tidak ada** di `isf_auth.menu` dev padahal dipakai FE + BFF: seed-nya masih menulis ke tabel `isf_auth.role_menu` yang sudah di-drop. Seed diperbaiki (`role_menu_permission`, aksi `view` untuk KEU/ACC/SPVKEU/ADM) dan diterapkan ke `isf_auth_zakat` dev → ikut snapshot.
- Menu key lama yang masih tersisa di `isf_auth.menu` tapi tidak dipakai FE/BFF: `finance.monitoring`, `finance.receivable` (label grup), dan duplikat `finance.parameter.budget.owner` vs `finance.parameter.budget_owner(.create/.edit/.delete)`. Tidak berbahaya; kandidat cleanup.
- `infra/db/migrations/isf_auth/recovered-schema-*.sql` sudah usang (masih punya `role_menu`, belum `role_menu_permission`). Acuan schema auth sekarang = `zakat/auth/11_schema_isf_auth.sql` (generated).

## 7. Bukti uji

| Uji | Hasil |
|---|---|
| Dry-run di `mziss_laz_origin` (PG18) | PREFLIGHT OK → POSTCHECK OK → ROLLBACK; origin tetap pristine |
| Migrasi penuh di container `postgres:12-alpine` (restore backup yang sama) | OK, 6 detik |
| Jalankan ulang | Ditolak preflight (`schema otorisasi/dwh sudah ada`) |
| `90_grants_optional.sql` di PG12 | OK |
| Migrasi penuh di `mziss_laz_migtest` (PG18) + `compare_schema.py` vs `mziss_laz` | 0 tabel/kolom/index/sequence/schema berbeda; 4 view + 3 CHECK beda format deparse saja |
| Semua 29 view `dwh` dieksekusi terhadap data produksi (postcheck) | OK |

**Auth DB:**

| Uji | Hasil |
|---|---|
| `run_auth_migration.sh init … --dry-run` | SQL valid, ROLLBACK |
| `init` ke `isf_auth_migtest` (PG18) dari `mziss_laz_migtest` | 82 user (32 aktif + password), postcheck OK |
| `sync-users` ulang | insert 0, update 82, password baru 0 (idempoten) |
| `bcrypt.checkpw` (image bff-api) untuk 32 password CSV | 32 OK / 0 gagal |
| `compare_schema.py` `isf_auth_migtest` vs `isf_auth_zakat` | 0 selisih (1 CHECK beda format deparse) |
| 10–12 di container `postgres:12-alpine` | OK |
| **Login nyata**: bff-api + api-python sementara diarahkan ke `mziss_laz_migtest` + `isf_auth_migtest`, login user produksi `RAIS` | OK — peran `ACC,KEU`, cabang `001`, `branch_access=single`, 48 menu (termasuk `fund_transfer`); RBAC menolak menu di luar peran (`MENU_FORBIDDEN`); batch upload produksi 13-11-2026 tampil `authstatus=A` |

DB `mziss_laz_migtest` + `isf_auth_migtest` (PG18, sudah ter-migrasi) dibiarkan untuk uji aplikasi isf-app
terhadap data produksi. Hapus bila tidak perlu:
`dropdb -U transaction mziss_laz_migtest && dropdb -U transaction isf_auth_migtest`.

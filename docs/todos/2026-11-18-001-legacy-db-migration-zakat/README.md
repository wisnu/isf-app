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

### 5.2 Wajib — auth DB (`isf_auth_zakat`), di luar skrip ini

Login isf-app butuh user di **dua** tempat: `enterprise.userapp` (business DB: peran,
cabang, `tipe_akses_cabang`) **dan** `isf_auth.users` + `user_credentials` +
`tenant_memberships` (auth DB).

- [x] Dicek 2026-11-18: **ke-32 user aktif produksi sudah ada** di `isf_auth_zakat.users`.
- [ ] Hapus/nonaktifkan akun dev di `isf_auth_zakat` sebelum go-live: `ADMIN`, `FINANCE.A`, `FINANCE.B`, `TESTUSR01` (tidak ada di `userapp` produksi → login akan gagal `UNKNOWN_IDENTITY` anyway). Juga reset password dev `test1234` (HADI, RAIS, ADM).
- [ ] Peran **`IMZ` (SOP VENDOR)** ada di produksi tapi **tidak punya baris `role_menu_permission`** → user aktif `ARIS` hanya mendapat menu dari peran lain. Tentukan menu untuk IMZ atau biarkan.
- [ ] Ulangi pengecekan user saat backup final (user baru di legacy setelah 2026-11-17 harus diprovisikan ke `isf_auth`).

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

## 6. Bukti uji

| Uji | Hasil |
|---|---|
| Dry-run di `mziss_laz_origin` (PG18) | PREFLIGHT OK → POSTCHECK OK → ROLLBACK; origin tetap pristine |
| Migrasi penuh di container `postgres:12-alpine` (restore backup yang sama) | OK, 6 detik |
| Jalankan ulang | Ditolak preflight (`schema otorisasi/dwh sudah ada`) |
| `90_grants_optional.sql` di PG12 | OK |
| Migrasi penuh di `mziss_laz_migtest` (PG18) + `compare_schema.py` vs `mziss_laz` | 0 tabel/kolom/index/sequence/schema berbeda; 4 view + 3 CHECK beda format deparse saja |
| Semua 29 view `dwh` dieksekusi terhadap data produksi (postcheck) | OK |

DB `mziss_laz_migtest` (PG18, sudah ter-migrasi) dibiarkan untuk uji aplikasi isf-app
terhadap data produksi. Hapus bila tidak perlu: `dropdb -U transaction mziss_laz_migtest`.

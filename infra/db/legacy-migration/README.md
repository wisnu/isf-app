# Legacy DB → isf-app migration

Membawa DB produksi aplikasi legacy (DAF, PostgreSQL 12) ke struktur yang dibutuhkan isf-app.
Analisis, diff, dan checklist go-live: [`docs/todos/2026-11-18-001-legacy-db-migration-zakat/`](../../../docs/todos/2026-11-18-001-legacy-db-migration-zakat/README.md).

```
legacy-migration/
├── tools/
│   ├── compare_schema.py      diff katalog 2 DB (schema/tabel/kolom/constraint/index/view/function/trigger)
│   ├── data_diff.py           diff isi tabel kecil per primary key (cari config isf-app vs data prod)
│   └── gen_new_schema_ddl.sh  regenerate 02/03 dari DB referensi isf-app, dibersihkan agar PG12-compatible
└── zakat/
    ├── 00_preflight.sql       guard read-only (DB benar? sudah pernah dimigrasi?)
    ├── 01_legacy_tables.sql   kolom/default/index tambahan di tabel legacy + backfill data
    ├── 02_schema_otorisasi.sql  GENERATED
    ├── 03_schema_dwh.sql        GENERATED (14 tabel + 29 view laporan)
    ├── 04_reference_data.sql  entity_config, dim_fund_type, dim_branch
    ├── 05_postcheck.sql       assert hasil (gagal → seluruh migrasi rollback)
    ├── 90_grants_optional.sql GRANT ke role aplikasi (jalankan terpisah bila perlu)
    ├── 99_rollback.sql        batalkan migrasi
    └── run_migration.sh       runner: 00–05 dalam SATU transaksi
```

## Menjalankan

```bash
# 1. Restore backup produksi (sebagai role aplikasi, tanpa owner/ACL asli)
createdb -h localhost -U transaction mziss_laz_origin
pg_restore -h localhost -U transaction -d mziss_laz_origin --no-owner --no-acl -j 4 \
  db/mziss_laz_YYYY-MM-DD_HH.MM.backup
#   error "schema public already exists" = wajar, abaikan

# 2. Dry-run (semua langkah lalu ROLLBACK)
PGPASSWORD=... infra/db/legacy-migration/zakat/run_migration.sh mziss_laz_origin --dry-run

# 3. Migrasi
PGPASSWORD=... infra/db/legacy-migration/zakat/run_migration.sh mziss_laz_origin

# 4. (Opsional) bila objek masih dimiliki role legacy per-schema
psql -d mziss_laz_origin -v app_role=transaction -f infra/db/legacy-migration/zakat/90_grants_optional.sql
```

Env: `PGHOST` (localhost), `PGPORT` (5432), `PGUSER` (transaction), `PGPASSWORD`.
Durasi pada backup 2026-11-17 (2,4 GB): ±5 detik.

## Memverifikasi / mengulang diff

```bash
cd infra/db/legacy-migration
# struktur
python3 tools/compare_schema.py --source mziss_laz_origin --target mziss_laz --out-dir /tmp/cmp
# isi tabel config/master
python3 tools/data_diff.py --source mziss_laz_origin --target mziss_laz \
  --diff-json /tmp/cmp/diff.json --out /tmp/cmp/data-diff.json
# setelah migrasi, harusnya: semua only_target/only_source = 0
```

Server berbeda: `--source-port` / `--target-port`.

## Bila struktur isf-app berubah

1. Tambahkan migrasi bernomor seperti biasa di `infra/db/migrations/`.
2. Perubahan di schema `otorisasi`/`dwh` → `tools/gen_new_schema_ddl.sh` (regenerate 02/03).
3. Perubahan di tabel legacy → tambahkan ke `01_legacy_tables.sql` (aditif, `IF NOT EXISTS`).
4. Perbarui angka ekspektasi di `05_postcheck.sql`, lalu ulangi dry-run + `compare_schema.py`.

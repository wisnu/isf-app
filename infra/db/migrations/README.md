# Migration files — recovered 2026-05-27

## Konteks

Migration files asli (numbered SQL sequence) hilang akibat NTFS corruption pada partisi workshop tanggal 2026-05-27. Lihat audit trail di `~/rescue/git-metadata-snapshot/`.

74 commit lokal yang berisi migration scripts asli — termasuk:
- Migration auth (`[MIGRATE-AUTHDB]` series, reflog lines 87-92)
- Migration datamart (`[ETL-DATAMART]`, `[DATAMART-CABANG]`, `[DWH]` series, lines 108-114)
- Migration 007 (`[ETL] migration 007 — drop stale unique indexes`, line 118)

— semua file SQL-nya hilang permanen dari disk.

## File yang ada di sini

| File | Sumber | Berisi |
|---|---|---|
| `isf_auth/recovered-schema-zakat.sql` | `pg_dump isf_auth_zakat -n isf_auth` | Schema auth final state (8 tabel: users, menu, role_menu, tenants, dll) |
| `isf_auth/recovered-schema-wakaf.sql` | `pg_dump isf_auth_wakaf -n isf_auth` | Identical dengan zakat (kedua portal pakai schema sama) |
| `dwh/recovered-schema-zakat.sql` | `pg_dump mziss_laz -n dwh` | Datamart schema final (14 tabel dim/dm/fact + etl_log, etl_watermark) — sudah include perubahan migration 007 (drop stale unique indexes) |
| `dwh/recovered-schema-wakaf-datamart-legacy.sql` | `pg_dump mziss_wakaf -n datamart` | **PERHATIAN**: schema di mziss_wakaf masih bernama `datamart` (legacy), belum di-rename ke `dwh`. Commit `[DWH] rename schema datamart→dwh` (reflog line 114) belum di-apply ke DB wakaf. |

## Bagaimana file ini dibuat

Setelah corruption, schema diserap balik dari database server lokal Postgres yang masih hidup:

```bash
pg_dump --schema-only -n <schema> --no-owner --no-privileges --no-comments <db> > <output>.sql
```

## Cara apply ke DB fresh

File-file ini adalah **snapshot final state**, bukan sequential migrations. Jadi pilihan:

**Option A — fresh install** (rekomen untuk dev environment baru):
```bash
createdb -U transaction isf_auth_<portal>
psql -U transaction -d isf_auth_<portal> -f infra/db/migrations/isf_auth/recovered-schema-<portal>.sql
```

**Option B — match existing DB**: tidak perlu apply ulang. DB current sudah punya schema ini (file ini di-extract dari DB tersebut).

## Outstanding work (post-recovery)

- [ ] Rename schema `datamart` → `dwh` di `mziss_wakaf` agar konsisten dengan `mziss_laz`. Pesan reflog: line 114 `[DWH] rename schema datamart→dwh + standarisasi ETL naming + enrich PSAK 109`.
- [ ] Pecah `recovered-schema-*.sql` jadi sequential migrations 001-NNN sesuai grouping reflog kalau diperlukan untuk replay-ability di environment lain. Atau adopt tool seperti Alembic/Sqitch untuk versi ke depan.
- [ ] Restore `migrate_auth_sqlite_to_pg.py` masih ada di `infra/db/` (tidak hilang) — script untuk migrate auth dari SQLite ke Postgres dipakai di reflog line 87 `[MIGRATE-AUTHDB]`.

## Reflog commit messages terkait migration

Dari `~/rescue/git-metadata-snapshot/logs/refs/heads/main` (74 commits unpushed):

| Line | Commit message |
|---|---|
| 48 | `feat: add isf_auth schema with menu and role_menu tables` |
| 51 | `feat: seed isf_auth.menu with MVP menu keys` |
| 55 | `feat: seed role-menu mapping for 14 active roles (zakat + wakaf)` |
| 76 | `feat: add admin.role_menu menu_key + seed ADM mapping` |
| 87 | `[MIGRATE-AUTHDB] feat: pindahkan auth DB dari SQLite ke Postgres isf_auth_<portal>` |
| 90 | `[MIGRATE-AUTHDB] feat: mirror migrasi auth ke apps_wakaf` |
| 91 | `[MIGRATE-AUTHDB] fix(admin): tulis/baca role_menu via pool isf_auth (bukan enterprise)` |
| 108 | `[ETL-DATAMART] datamart schema + ETL runner end-to-end working` |
| 110 | `[DATAMART-CABANG] Phase 1A — dim_cabang + cabang_key di facts (foundation)` |
| 111 | `[DATAMART-CABANG] Phase 1B — refactor view-based ETL untuk populate cabang_key` |
| 114 | `[DWH] rename schema datamart→dwh + standarisasi ETL naming + enrich PSAK 109` |
| 117 | `[ETL] fix f.fundentity → a.fundentity di SQL query (alias salah)` |
| 118 | `[ETL] migration 007 — drop stale unique indexes superseded by 004/006` |

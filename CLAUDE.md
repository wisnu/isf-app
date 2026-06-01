# CLAUDE.md — isf-app orientation

Konteks tambahan untuk Claude di luar yang ada di [README.md](README.md), [docs/architecture.md](docs/architecture.md), dan [docs/runbook-local.md](docs/runbook-local.md). Fokus pada hal yang **tidak obvious dari kode**.

## ⚠️ Recovery state (2026-05-27)

Repo ini di-rebuild setelah NTFS corruption tanggal 2026-05-27 menghapus 74 commit lokal yang belum di-push. Working tree dipulihkan dari rescue snapshot + base commit `ac3056` + DB schema dump. Audit trail di `~/rescue/git-metadata-snapshot/` dan branch `recovery/2026-05-27-ntfs-corruption`.

**Yang masih outstanding** lihat [`docs/recovery/README.md`](docs/recovery/README.md) §"Still TODO" — singkatnya: ETL runners (14 file), admin/profile pages frontend, beberapa test admin. (Rename schema `datamart`→`dwh` di `mziss_wakaf` **sudah selesai** 2026-06-01.)

## Topologi 2 portal × 2 database

Setiap portal (zakat & wakaf) punya **DUA database terpisah**:

| Portal | Business DB | Auth DB | Schemas |
|---|---|---|---|
| Zakat | `mziss_laz` | `isf_auth_zakat` | business: `transaction`/`accounting`/`enterprise`/`fund`/`program`/`personalia`/`school` (legacy) + `dwh` (datamart final). auth: `isf_auth` |
| Wakaf | `mziss_wakaf` | `isf_auth_wakaf` | sama legacy + schema `dwh` (di-rename dari `datamart` 2026-06-01, konsisten dgn zakat). auth: `isf_auth` |

**Env vars**:
- `DATABASE_URL_ZAKAT` / `DATABASE_URL_WAKAF` → business DB (di `infra/.env`)
- `ISF_AUTH_DATABASE_URL_ZAKAT` / `ISF_AUTH_DATABASE_URL_WAKAF` → auth DB

User & kredensial DB lokal: `transaction:solusi` (lihat `.env.example`).

## Auth & RBAC

- **Auth DB schema** (`isf_auth.*`): `users`, `user_credentials`, `user_provider_links`, `tenants`, `tenant_memberships`, `menu`, `role_menu`, `audit_log`
- **Identity service** di `apps_*/api-python/app/modules/identity/`: lookup profile + roles + menus per user
- **IdentityClient** di `apps_*/bff-api/app/services/identity_client.py`: httpx wrapper untuk panggil identity service dari BFF
- **Login flow** (BFF): authenticate → fetch profile via IdentityClient → populate session dengan `user_id`, `active_tenant_id`, `roles[]`, `branches[]`, `primary_branch`, `branch_access`, `menus[]`. Frontend baca lewat `stores/auth.ts`. Fail-closed kalau identity service down (HTTP 503 `IDENTITY_UNAVAILABLE`).
- **Branch RBAC**: `branch_access` = `'all'` bila `enterprise.userapp.tipe_akses_cabang='S'` (Seluruh), else `'single'` (`T`=Tunggal — hanya cabang default). BFF `_resolve_branch` (routers/report.py) kunci user 'single' ke `primary_branch` & tolak cabang lain (403); user 'all' boleh pilih cabang / semua.
- **⚠️ Session menus snapshot saat login**: `session["menus"]` diisi waktu login. Nambah row `role_menu` baru **tidak** berlaku utk session aktif → user harus **logout + login** ulang (kalau tidak, router guard redirect `?denied=`).
- **Gating endpoint backend**: `require_menu("menu.key")` FastAPI dependency, audit di-tulis ke `isf_auth.audit_log` saat deny
- **Gating sidebar/router frontend**: `auth.menus[]` array, sidebar di-filter, router guard cek `meta.menu_key`
- **MENU_KEYS** constant di `apps_*/web-vue/src/lib/menu/registry.ts` — single source of truth untuk semua menu key
- **⚠️ Demo user gotcha**: `auth_seed.py` hanya seed `ADMIN/FINANCE.A/FINANCE.B` ke `isf_auth.users`. Identity lookup ke `enterprise.userapp` (mziss_*) akan 404 untuk username itu → login fail dengan `UNKNOWN_IDENTITY`. Untuk E2E pakai script `testing/setup-e2e-users.sh` yang pilih user nyata dari `enterprise.userapp` — **catatan**: script masih reference SQLite (predates auth-pg migration), perlu port ke asyncpg sebelum bisa dipakai.
- **isf_auth seed**: `infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql` populates semua menu key (match `MENU_KEYS` registry) + `role_menu` per role aktif di `enterprise.peran`. Idempotent (`ON CONFLICT`) — re-apply tiap nambah menu. Refine via admin UI `/admin/role-menu`.

## Independent chart load

- Dashboard pages (`DashboardPage`, `DashboardKeuanganPage`, `DashboardPenyaluranPage`) tidak ada shared loading state — tiap widget load sendiri lewat `useFetch(fetcher)` di `apps_*/web-vue/src/lib/useFetch.ts`. Failed widget tampil error sendiri, widget lain tetap render normal.
- `Toast.vue` + `useToast.ts` sudah ada baseline (top-right, accent left-border) tapi **belum di-mount** di `App.vue`. Wire `<Toast />` saat rebuild fitur yang butuh, mis. PasswordPage / UsersPage.

## Username convention

**Input case-insensitive, storage uppercase.** Normalisasi di boundary BFF (sebelum query DB). Login dengan `wisnu`, `WISNU`, atau `Wisnu` semua match record dengan `username = 'WISNU'`. Pattern ini dipakai di kedua portal (apps_zakat + apps_wakaf).

## Datamart / DWH

- Schema `dwh.*` di kedua DB: `mziss_laz` (zakat) & `mziss_wakaf` (wakaf, di-rename dari `datamart` 2026-06-01)
- Tabel utama: `dim_branch`, `dim_donor`, `dim_fund_type`, `dm_*_monthly` (aggregates per bulan × cabang × fund_entity), `fact_fundraising_monthly`, `etl_log`, `etl_watermark`
- ETL runner di `apps_zakat/api-python/etl/` (untuk wakaf belum di-mirror full)
- Grain agregasi: tahun-bulan × (branch_key, fund_entity, ...) — `fund_entity` part of unique key sejak migration 007

## Laporan (report-api service)

- **report-api** = service FastAPI **terpisah** per portal (read/agregasi: dashboard + report), read-only ke business DB + DWH. Port host: zakat **:8010**, wakaf **:8011**. api-python **tak lagi** serve `/api/dashboard/*` (pindah ke report-api). Lihat `docs/architecture.md` §9.
- **Standar UX laporan**: halaman laporan **TIDAK auto-load data** saat dibuka — `onMounted` hanya siapkan filter (cabang/rekening). Data baru di-load saat user klik **"Tampilkan"**. (Export disabled sampai ada data.)
- **Pola tambah laporan** (semua laporan keuangan pakai ini): (1) view `dwh.v_<name>` di `mziss_*` membungkus query legacy — agregasi/running-balance dihitung di report-api, bukan di view; (2) `report-api/app/modules/report/` → `service.py` + `router.py` (`/report/<name>` + `/<name>/export.xlsx`) + `export.py` (openpyxl); (3) BFF `routers/report.py` → route `require_menu('keuangan.report.<key>')` + `_resolve_branch` + `stream_report_api` utk xlsx; (4) frontend `pages/keuangan/Laporan*Page.vue` + key di `lib/menu/registry.ts` + child di sidebar grup "Laporan" + route `meta.menu_key`; (5) tambah menu+role_menu di `seed-menu-and-rolemenu.sql`, apply ke `isf_auth_zakat`.
- **Referensi legacy**: query asli di `docs/legacy-apps/core/dialogs/Report/f<Name>_data.py`. **AllowedGroups** di menu legacy (`.dfr`/`.mnu`) → daftar role utk `role_menu` (mis. fDailyCash/fSummaryCash/fSummaryCashMonthly → `ADM;KEU;ACC;SPVKEU;QAC;SPVACC`).
- **Export xlsx**: report-api set header `Content-Disposition`; BFF CORS **wajib** `expose_headers=["Content-Disposition"]` agar nama file kebaca lintas-origin; `downloadBlob` (FE) **tunda** `revokeObjectURL` (else Chrome simpan nama UUID). Cap 50k baris; async + menu "Hasil Laporan" = fase 2.
- Laporan aktif **zakat + wakaf** (di-mirror 2026-06-01): Jurnal Harian, List Transaksi Umum, Transaksi Kas/Bank Harian, Rekapitulasi Kas/Bank, Monitoring Saldo Bulanan. View DWH portal-neutral (`infra/db/migrations/dwh/v_*.sql`, apply ke `mziss_laz` **dan** `mziss_wakaf`). Catatan: sidebar wakaf **di-filter** `auth.menus` (children punya `menu_key`); sidebar zakat tidak.
- Laporan akuntansi **zakat-only** (belum di-mirror ke wakaf): **Trial Balance** & **Neraca** (legacy-faithful: `dailybalance`+`accounthierarchy`, view `dwh.v_daily_balance`; ⚠️ dailybalance s/d 2025-12-31 → data 2026 belum akurat), **Arus Kas** (config-driven `BalanceSumItem`/`Member`, view `dwh.v_aruskas_item_account`; closing cash rekonsiliasi ke saldo 110100). Spec: `docs/superpowers/specs/2026-06-01-trial-balance-neraca-design.md`.
- **Config Arus Kas/Perubahan Dana portal-specific** (`transaction.balancesum*`, tak ada di schema dump): seeder per-portal `infra/db/migrations/seed/balancesum-config-{zakat,wakaf}.sql` — **jangan cross-apply** (zakat 31 item AK_MUT, wakaf 6 item beda COA). Layout Arus Kas di `aruskas()` saat ini zakat-specific.

## Konvensi commit

**Format wajib**: setiap commit diawali prefix `[TAG]` lalu conventional-commit:

```
[TAG] type(scope): subject
```

- `[TAG]` = tag singkat (UPPER-KEBAB) yang **relevan dengan enhancement/perubahan** yang dilakukan, mis. `[INDEPENDENT-LOAD]`, `[AUTH-PG]`, `[DASHBOARD]`. Pilih yang deskriptif tapi ringkas; reuse tag aktif di bawah kalau cocok, atau buat baru kalau perlu.
- Lanjutkan dengan conventional-commit (`feat`, `fix`, `chore`, `docs`, `refactor`) + scope yang menyebut feature/context, mis. `feat(dashboard):`, `chore(infra):`.
- Cari contoh di history: `git log --grep='\['`.

Scope/tag yang aktif:
- `INDEPENDENT-LOAD`, `auth-pg`, `admin+ui`, `dwh`, `recovery` — recent post-recovery work
- `MIGRATE-AUTHDB`, `ADMIN-USERS`, `CHANGE-PASSWORD`, `UX`, `ETL-DATAMART`, `DATAMART-CABANG`, `DASHBOARD`, `DASHBOARD-KEUANGAN`, `ETL`, `USERNAME-UPPER`, `DOCS`, `RECOVERY` — legacy from reflog

## Konvensi testing

Setiap fitur baru → buat E2E script reusable di `testing/`:
- `testing/e2e-<feature>.sh` (curl-based, run ke localhost ports)
- Contoh: `testing/e2e-admin-users.sh`, `testing/e2e-etl-datamart.sh`

Per-service punya `test.sh` wrapper:
- `apps_*/api-python/test.sh`
- `apps_*/bff-api/test.sh`

Tests Python di `tests/` dengan pytest. TDD untuk service code yang punya logic non-trivial.

## First-time DB setup

Apply schema + seed ke dua DB auth (DBs sudah harus exist di Postgres lokal — buat via `createdb` di bawah):

```bash
for portal in zakat wakaf; do
  PGPASSWORD=solusi createdb -h localhost -U postgres "isf_auth_$portal"
  PGPASSWORD=solusi psql -h localhost -U postgres -d "isf_auth_$portal" \
    -f infra/db/migrations/isf_auth/recovered-schema-$portal.sql
  PGPASSWORD=solusi psql -h localhost -U postgres -d "isf_auth_$portal" \
    -f infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql
done
```

Business DB (`mziss_laz`, `mziss_wakaf`) diasumsikan sudah ada — repo tidak ship schema-nya (legacy), cuma `docs/datadictionary/ddl_all_schema.sql` referensi.

## Dev workflow

**Host caveat (Fedora 44 / kernel 6.19 / crun 1.27 / SELinux Enforcing)**: `podman build` di dalam `podman-compose up --build` gagal di langkah `RUN pip install` / `RUN npm install` dengan `cannot apply additional memory protection after relocation: Permission denied` — SELinux MCS label block `libc` mprotect. Workaround: pre-build manual dengan `--security-opt label=disable`, baru `up -d` tanpa `--build`. Compose runtime sudah carry `security_opt: [label=disable]` per-service.

Ada **`Makefile`**: `make build` (pre-build semua image incl **report-api**), `make run`, `make health`, `make migrate`. Pakai ini ketimbang loop manual.

```bash
# 1. Pre-build images (only when pyproject.toml / package.json changes — source di bind-mount auto-reload)
for portal in zakat wakaf; do
  for svc in api-python report-api bff-api web-vue; do
    (cd apps_$portal/$svc && \
     podman build --security-opt label=disable -t isf-$portal-$svc:dev -f Dockerfile.dev .)
  done
done

# 2. Start (no --build)
cd infra
podman-compose -f docker-compose.zakat.yml up -d   # → http://localhost:5173
podman-compose -f docker-compose.wakaf.yml up -d   # → http://localhost:5174
```

`.env` opsional — compose pakai defaults di `${VAR:-...}` untuk dev. Copy `.env.example → .env` kalau perlu override (HOST_IP, Google OAuth, dst).

Demo akun seeded ke `isf_auth.users`: `ADMIN/admin123`, `FINANCE.A/finance123`, `FINANCE.B/finance123`. **Lihat warning di §Auth & RBAC** — username ini bisa authenticate tapi gagal identity lookup ke `enterprise.userapp`. Untuk login berhasil end-to-end, port `testing/setup-e2e-users.sh` ke asyncpg, atau manual insert: pilih row dari `enterprise.userapp` yang punya role+menu mapping, lalu `INSERT INTO isf_auth.users (id, username, display_name, status) VALUES (...)` + `set_password`.

**Dev E2E users** (user nyata di `enterprise.userapp`, password lokal `test1234` di-set manual ke `isf_auth_zakat.user_credentials`): `HADI` (DIST/SPVDIST, `branch_access=all`) utk dashboard/jurnal/transaksi-umum; `RAIS` (ACC/KEU, single-branch 001) utk laporan kas/finance. Pilih user yang role-nya cocok dgn AllowedGroups menu yang diuji. Set password: `UPDATE isf_auth.user_credentials SET password_hash=<bcrypt> WHERE user_id=(SELECT id FROM isf_auth.users WHERE username='<U>')`.

## Hindari working repo di NTFS

Repo asli pernah di-host di partisi NTFS Windows (D:) via ntfs-3g. **JANGAN ULANGI** — partisi NTFS rawan corruption setelah unsafe shutdown, dan ntfs-3g tidak full implement journal replay. Working repo sekarang di `~/workshop/isf-app/` (ext4). Partisi NTFS D: hanya untuk file sharing dengan Windows.

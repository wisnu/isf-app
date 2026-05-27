# CLAUDE.md — isf-app orientation

Konteks tambahan untuk Claude di luar yang ada di [README.md](README.md), [docs/architecture.md](docs/architecture.md), dan [docs/runbook-local.md](docs/runbook-local.md). Fokus pada hal yang **tidak obvious dari kode**.

## ⚠️ Recovery state (2026-05-27)

File ini di-rebuild setelah NTFS corruption pada partisi workshop tanggal 2026-05-27 menghapus 74 commit lokal yang belum di-push. Lihat audit trail di `~/rescue/git-metadata-snapshot/` dan branch `recovery/2026-05-27-ntfs-corruption`. Working tree dipulihkan dari rescue snapshot + base commit `ac3056` + DB schema dump.

File yang masih TODO post-recovery (truly missing, harus rebuild manual):
- `apps_zakat/api-python/etl/*` (14 file ETL runner — runner, scheduler, refresh_dim_*, refresh_dm_*, refresh_fact_*)
- `apps_*/api-python/app/modules/admin/router.py & service.py`
- `apps_*/web-vue/src/components/ui/Toast.vue`, `lib/useFetch.ts`, `lib/useToast.ts`
- `apps_*/web-vue/src/pages/admin/`, `pages/profile/`
- `docs/datadictionary/dwh.md`
- `testing/e2e-admin-users.sh`, `testing/e2e-etl-datamart.sh`

Lihat `~/rescue/git-metadata-snapshot/truly-missing-51.txt` untuk daftar lengkap.

## Topologi 2 portal × 2 database

Setiap portal (zakat & wakaf) punya **DUA database terpisah**:

| Portal | Business DB | Auth DB | Schemas |
|---|---|---|---|
| Zakat | `mziss_laz` | `isf_auth_zakat` | business: `transaction`/`accounting`/`enterprise`/`fund`/`program`/`personalia`/`school` (legacy) + `dwh` (datamart final). auth: `isf_auth` |
| Wakaf | `mziss_wakaf` | `isf_auth_wakaf` | sama legacy + schema `datamart` (legacy name, belum di-rename ke `dwh` — lihat outstanding di `infra/db/migrations/README.md`) |

**Env vars**:
- `DATABASE_URL_ZAKAT` / `DATABASE_URL_WAKAF` → business DB (di `infra/.env`)
- `ISF_AUTH_DATABASE_URL_ZAKAT` / `ISF_AUTH_DATABASE_URL_WAKAF` → auth DB

User & kredensial DB lokal: `transaction:solusi` (lihat `.env.example`).

## Auth & RBAC

- **Auth DB schema** (`isf_auth.*`): `users`, `user_credentials`, `user_provider_links`, `tenants`, `tenant_memberships`, `menu`, `role_menu`, `audit_log`
- **Identity service** di `apps_*/api-python/app/modules/identity/`: lookup profile + roles + menus per user
- **IdentityClient** di `apps_*/bff-api/app/services/identity_client.py`: httpx wrapper untuk panggil identity service dari BFF
- **Login flow** (BFF): authenticate → fetch profile via IdentityClient → populate session dengan `roles[]`, `branches[]`, `menus[]` (fail-closed kalau identity service down)
- **Gating endpoint backend**: `require_menu("menu.key")` FastAPI dependency, audit di-tulis ke `isf_auth.audit_log` saat deny
- **Gating sidebar/router frontend**: `auth.menus[]` array, sidebar di-filter, router guard cek `meta.menu_key`
- **MENU_KEYS** constant di `apps_*/web-vue/src/lib/menu/registry.ts` — single source of truth untuk semua menu key

## Username convention

**Input case-insensitive, storage uppercase.** Normalisasi di boundary BFF (sebelum query DB). Login dengan `wisnu`, `WISNU`, atau `Wisnu` semua match record dengan `username = 'WISNU'`. Pattern ini dipakai di kedua portal (apps_zakat + apps_wakaf).

## Datamart / DWH

- Schema `dwh.*` di `mziss_laz` (zakat) — schema `datamart.*` di `mziss_wakaf` (legacy, harus rename ke `dwh`)
- Tabel utama: `dim_branch`, `dim_donor`, `dim_fund_type`, `dm_*_monthly` (aggregates per bulan × cabang × fund_entity), `fact_fundraising_monthly`, `etl_log`, `etl_watermark`
- ETL runner di `apps_zakat/api-python/etl/` (untuk wakaf belum di-mirror full)
- Grain agregasi: tahun-bulan × (branch_key, fund_entity, ...) — `fund_entity` part of unique key sejak migration 007

## Konvensi commit

Commit message diawali `[PREFIX]` per feature group. Contoh dari history:
- `[MIGRATE-AUTHDB]` — migrasi auth DB
- `[ADMIN-USERS]` — admin user management
- `[CHANGE-PASSWORD]` — self-service ganti password
- `[UX]` — frontend polish/redesign
- `[ETL-DATAMART]`, `[DATAMART-CABANG]`, `[DWH]` — datamart
- `[DASHBOARD]`, `[DASHBOARD-KEUANGAN]` — dashboard
- `[ETL]` — ETL bugfix / migration
- `[DOCS]` — dokumentasi
- `[USERNAME-UPPER]` — convention enforcement
- `[RECOVERY]` — recovery work

Bisa pakai conventional commit prefix juga (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`) untuk commit yang lebih kecil/tidak grouped.

## Konvensi testing

Setiap fitur baru → buat E2E script reusable di `testing/`:
- `testing/e2e-<feature>.sh` (curl-based, run ke localhost ports)
- Contoh: `testing/e2e-admin-users.sh`, `testing/e2e-etl-datamart.sh`

Per-service punya `test.sh` wrapper:
- `apps_*/api-python/test.sh`
- `apps_*/bff-api/test.sh`

Tests Python di `tests/` dengan pytest. TDD untuk service code yang punya logic non-trivial.

## Dev workflow

```bash
cd infra

# Pastikan infra/.env sudah ada (copy dari .env.example, isi credentials)
cp .env.example .env  # edit credentials

# Portal Zakat
podman-compose -f docker-compose.zakat.yml up -d --build
# → http://localhost:5173

# Portal Wakaf
podman-compose -f docker-compose.wakaf.yml up -d --build
# → http://localhost:5174
```

Demo akun (sama di kedua portal): `admin/admin123`, `finance.a/finance123`, `finance.b/finance123`.

## Hindari working repo di NTFS

Repo asli pernah di-host di partisi NTFS Windows (D:) via ntfs-3g. **JANGAN ULANGI** — partisi NTFS rawan corruption setelah unsafe shutdown, dan ntfs-3g tidak full implement journal replay. Working repo sekarang di `~/workshop/isf-app/` (ext4). Partisi NTFS D: hanya untuk file sharing dengan Windows.

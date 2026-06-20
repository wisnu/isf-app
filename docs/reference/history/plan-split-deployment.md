# Plan: Split Deployment — Portal Zakat vs Portal Wakaf

> Combined spec + plan. Scope: restructure folder + dual compose file. Doc updates di PRD §1.2 / §7.2 / §15.

## Context

Per PRD v0.3, portal ZISWAF dipecah menjadi dua aplikasi independen karena domain berbeda (zakat vs wakaf) dan akan bercabang luas. Backend dan DB sudah terpisah per domain (`mziss_laz` vs `mzis_wakaf`). Frontend dan backend juga dipisah deploymentnya — tidak ada multi-tenant routing di tingkat aplikasi tunggal.

## Layout monorepo setelah split

```
isf-app/
  apps_zakat/                 ← rename dari apps/
    web-vue/
    bff-api/
    api-python/
    api-go/
  apps_wakaf/                 ← clone dari apps_zakat (Fase awal: identik; divergen seiring waktu)
    web-vue/
    bff-api/
    api-python/
    api-go/
  packages/                   (shared — tidak diubah)
    api-contract/
    api-client-ts/
  infra/
    docker-compose.zakat.yml        ← zakat (default)
    docker-compose.wakaf.yml  ← wakaf (run dengan -f flag)
    .env.example
    db/
    kong/
    nginx/
  docs/
```

## Pemetaan port

| Service | Zakat (default) | Wakaf |
| --- | --- | --- |
| web-vue | 5173 | 5174 |
| bff-api | 7000 | 7001 |
| api-python | 8000 | 8001 |

Browser akses:
- Zakat: http://localhost:5173
- Wakaf: http://localhost:5174

## Compose project namespacing

Setiap compose file pakai `name:` directive eksplisit supaya volume/network tidak collision:
- `name: isf-zakat` → volume `isf-zakat_bff-data`, network `isf-zakat_default`
- `name: isf-wakaf` → volume `isf-wakaf_bff-data`, network `isf-wakaf_default`

Setiap stack independen — bisa stop/start/rebuild tanpa pengaruh ke stack lain.

## Container naming

```
isf-zakat-web-vue, isf-zakat-bff-api, isf-zakat-api-python
isf-wakaf-web-vue, isf-wakaf-bff-api, isf-wakaf-api-python
```

## Domain config

Tiap container env var `DOMAIN={zakat|wakaf}` dan `VITE_PORTAL_DOMAIN={zakat|wakaf}` — kode tinggal baca env untuk:
- Branding (logo color, title)
- Conditional menu (sidebar item domain-specific)
- Tenant default config

Domain-aware customization akan ditambah di iterasi berikutnya saat fitur wakaf mulai divergen.

## Konsekuensi terhadap fitur existing

- **Auth (SQLite per portal)**: setiap portal punya `/data/auth.sqlite` sendiri. Initial seed sama (admin/admin123 dst.). Untuk SSO lintas portal, andalkan Google OAuth (token Google diverifikasi mandiri tiap portal).
- **Tenant switcher di header**: tidak relevan lagi (single tenant per portal). Tetap ada slot di UI untuk menampilkan nama perusahaan/lembaga aktif (bukan switcher).
- **Multi-cabang**: tetap relevan, dikerjakan **di dalam tiap portal** saat Fase 2 mulai connect ke existing DB.
- **Dashboard, COA, Kas, Bank, dst**: di portal zakat → full feature seperti sekarang. Di portal wakaf → simpler scope, di-stub awalnya (clone identik dulu, modify saat tim wakaf garap).

## Cara menjalankan

```bash
# Zakat (default compose)
cd infra
podman-compose -f docker-compose.zakat.yml up -d
# atau: docker compose -f docker-compose.zakat.yml up -d

# Wakaf
podman-compose -f docker-compose.wakaf.yml up -d
# atau: docker compose -f docker-compose.wakaf.yml up -d

# Stop semua
podman-compose -f docker-compose.zakat.yml down                              # zakat
podman-compose -f docker-compose.wakaf.yml down  # wakaf
```

## Verifikasi setelah split

1. `podman ps --filter name=isf-zakat-` → 3 container running.
2. Browser http://localhost:5173 → portal zakat tampil normal (semua fitur existing).
3. End-to-end auth flow tetap jalan (login admin/admin123, switch cabang Fase 2+, dashboard, dll).
4. **Wakaf belum diverifikasi running** — saat ini hanya clone identik dari zakat. Tim wakaf bisa start dengan `-f docker-compose.wakaf.yml up -d` dan akan dapat tampilan identik di port 5174. Customization wakaf-specific menyusul.

## Risiko & catatan

- **Code drift**: clone identik berarti dua copy code yang awalnya sama. Bila ada bug fix di zakat, pastikan apply di wakaf juga sampai diverging cukup banyak. Jangka panjang: extract komponen umum ke `packages/`.
- **Volume `bff-data` collision** dihindari via `name:` directive di compose — volume sudah project-scoped.
- **Port collision**: hanya bisa run dua stack simultan kalau port berbeda (sudah). Untuk single-stack-at-a-time, tidak ada constraint.
- **Google OAuth redirect URL**: tiap portal butuh redirect URI terdaftar di GCP Console (`http://localhost:7000/...` untuk zakat, `http://localhost:7001/...` untuk wakaf). Lihat runbook §13.
- **Existing DB credentials** belum tersambung di kedua portal — Fase 2 dimulai setelah `TenantDbRouter` (§15.0 architecture.md) dikoneksi ke `mziss_laz` (zakat) dan `mzis_wakaf` (wakaf) masing-masing.

## Out of scope (untuk plan ini)

- Shared `packages/` untuk komponen UI / auth — defer sampai duplikasi mulai painful.
- Differentiating wakaf UI (warna, logo, menu) — manual, tim wakaf garap.
- CI/CD setup untuk dua deployment terpisah.
- Mobile app per domain.

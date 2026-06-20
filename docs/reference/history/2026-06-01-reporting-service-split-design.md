# Reporting sebagai service terpisah (report-api) — zakat

**Date:** 2026-06-01
**Status:** Approved (design)

## Problem

Logic read/agregasi (dashboard, dan nanti report) saat ini hidup di `api-python`
bersama modul CRUD/management (coa, donors, zakat, waqf, admin, identity). Read
model (query views, agregasi, DWH) dan write model (transaksi/CRUD) punya pola
akses, skala, dan sumber data berbeda. Mencampurnya menyulitkan evolusi —
khususnya saat DWH dipindah ke warehouse sendiri dan saat Report Service
akhirnya dimigrasi ke Go (lihat `docs/architecture.md` Fase 3–4 yang sudah
menyebut "Report Service" sebagai domain service tersendiri).

## Goal

Pisahkan reporting menjadi **service FastAPI tersendiri** (`report-api`) yang
menampung read/agregasi (dashboard sekarang, report nanti), terpisah dari
`api-python` yang fokus CRUD/management. Siapkan boundary DB: koneksi DWH khusus,
walau fisiknya masih satu server/DB (`mziss_laz`) untuk saat ini.

## Keputusan (hasil brainstorming)

- **Cakupan:** portal **zakat dulu**; wakaf menyusul di langkah terpisah.
- **Isi service baru:** modul `dashboard` **dipindah utuh** + **scaffold** modul
  `report` (skeleton, belum ada endpoint fungsional).
- **Sumber data:** **koneksi DWH khusus** (`DWH_DATABASE_URL`) untuk report, di
  samping koneksi business (`DATABASE_URL`) untuk dashboard. Keduanya saat ini
  menunjuk `mziss_laz` (schema `dwh` ada di DB yang sama) — dipisah env supaya
  siap saat DWH dipindah server.
- **Topologi:** FastAPI app baru, port host **8010** (internal 8000).
- **Koneksi report-api:** kedua pool dibuka **read-only**
  (`default_transaction_read_only=on`) — enforce boundary di level koneksi.
- **Shared helper:** **diduplikasi** ke report-api (konsisten dgn pola
  api-python/bff yang masing-masing punya `shared/`), bukan package bersama.
- **Frontend:** tidak berubah — tetap panggil BFF; hanya upstream BFF berubah.

## Topologi baru (zakat)

```
web-vue :5173
   ↓
bff-api :7000
   ├── /api/dashboard/*, /api/report/*  → report-api :8010  ┐ read-only
   │                                          ├ business pool (DATABASE_URL → mziss_laz)
   │                                          └ dwh pool      (DWH_DATABASE_URL → mziss_laz, schema dwh)
   └── /api/{coa,admin,...}/*           → api-python :8000   (CRUD/management, tetap)
```

## Komponen

### 1. Service baru `apps_zakat/report-api/` (mirror layout api-python)

```
apps_zakat/report-api/
  pyproject.toml            # deps: fastapi, uvicorn, pydantic(-settings), asyncpg, openpyxl
  Dockerfile.dev            # python:3.12-slim, EXPOSE 8000, uvicorn --reload
  test.sh
  app/
    main.py                 # lifespan init business+dwh pool; /health, /ready (+ dwh ready); include dashboard_router + report_router
    shared/
      config.py             # Settings: database_url, dwh_database_url, app_env
      db.py                 # dual-pool: business (fetch_all/fetch_one/ping) + dwh (fetch_all_dwh/fetch_one_dwh/ping_dwh); pools read-only
      response.py           # ok()/err() — sama dgn api-python
    modules/
      dashboard/            # DIPINDAH utuh dari api-python (router, service, schema) — tanpa ubah logic
      report/               # SCAFFOLD: router (prefix /report, /report/ping health), service stub, schema stub; query report baca via pool dwh
```

- `db.py` mengikuti pola dual-pool `api-python` (yang punya business + isf_auth);
  di sini business + dwh. Read-only via asyncpg `server_settings`.
- Dashboard service tidak menyentuh isf_auth (auth digate di BFF) → report-api
  **tidak** butuh pool isf_auth.

### 2. `api-python` — buang dashboard

- Hapus folder `app/modules/dashboard/`.
- Hapus import + `include_router(dashboard_router, ...)` di `app/main.py`.
- api-python menyisakan admin/coa/identity/donors/zakat/waqf. Single source —
  dashboard tidak diduplikasi.

### 3. BFF — upstream kedua

- `app/shared/config.py`: tambah `report_api_base_url: str = "http://localhost:8010"`.
- `app/services/proxy.py`: tambah `get_report_api(path, params=None)` (mirror
  `get_api_python`, pakai `settings.report_api_base_url`).
- `app/routers/dashboard.py`: ganti semua `get_api_python` → `get_report_api`.
- `app/routers/report.py` (baru): scaffold auth-gated, proxy `/report/*` ke
  report-api; daftarkan di `main.py`.

### 4. Infra `infra/docker-compose.zakat.yml`

- Service `report-api`: image `isf-zakat-report-api:dev`, build context
  `../apps_zakat/report-api`, `ports: "8010:8000"`, `security_opt: [label=disable]`,
  env `DATABASE_URL`=mziss_laz + `DWH_DATABASE_URL`=mziss_laz, healthcheck
  (`/health`).
- `bff-api`: tambah env `REPORT_API_BASE_URL: http://report-api:8000` +
  `depends_on: report-api (service_healthy)`.

### 5. Makefile

- `build-zakat`: tambah build image `report-api`.
- `health`: tambah cek `report-api :8010 /health`.
- (SERVICES var portal-aware atau target khusus zakat — wakaf belum punya report-api.)

### 6. `docs/architecture.md` (update — diminta user)

- §9 skeleton monorepo: tambah `report-api/` di pohon `apps_<domain>/` dengan
  catatan "read/agregasi (dashboard, report), koneksi read-only business + DWH".
- §22 Local Development: tambahkan `report-api -> localhost:8010` ke daftar service.
- §11 Environment Variable: dokumentasikan `REPORT_API_BASE_URL` (BFF) dan
  `DWH_DATABASE_URL` (report-api).
- Catatan singkat: report-api adalah realisasi awal "Report Service" (Fase 3–4)
  sebagai FastAPI; jalur migrasi ke Go tetap sesuai §18.

## Data flow

```
GET bff /api/dashboard/keuangan/kpis
  → report-api /api/dashboard/keuangan/kpis
    → business pool (mziss_laz): dashboard.v_*, transaction.*, program.*
GET bff /api/report/...   (nanti)
  → report-api /api/report/...
    → dwh pool (mziss_laz schema dwh): dwh.*
```

## Error handling

- report-api: 503 `DB_UNAVAILABLE` saat pool down (sama spt sekarang, per pool).
- BFF: 401 tanpa session (helper existing), else passthrough status+body.
- Read-only pool: query tulis akan ditolak DB — by design (reporting read-only).

## Testing / verification

1. Build image `report-api`; `make run`; `make health` → semua service up
   termasuk report-api :8010.
2. Smoke: 8 endpoint dashboard via report-api langsung (:8010) + via BFF (:7000,
   authenticated) → 200, data benar (regresi dari refactor sebelumnya).
3. `GET /api/report/ping` (BFF→report-api) → 200 scaffold.
4. api-python tak lagi serve `/api/dashboard/*` (404) — buktikan dashboard benar
   pindah.
5. Browser drive (login HADI): dashboard zakat tetap render normal (independent
   load utuh).
6. Verifikasi pool dwh: `/ready` report-api melaporkan business+dwh OK.

## Di luar scope

- Endpoint report fungsional (cukup scaffold + pool dwh siap).
- Portal wakaf (menyusul).
- Migrasi schema `datamart`→`dwh` di wakaf.
- Migrasi reporting ke Go (roadmap §18).

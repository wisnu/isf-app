# Runbook — Local Deployment

> Cara membawa stack `isf-app` (Portal Zakat & Portal Wakaf, split deployment per PRD v0.3) sampai jalan di laptop pengembang. Lihat [`docs/prd.md`](./prd.md) untuk konteks fitur, [`docs/architecture.md`](./architecture.md) untuk arsitektur, [`docs/plan-split-deployment.md`](./plan-split-deployment.md) untuk strategi split.

## Daftar isi

1. [Prasyarat](#1-prasyarat)
2. [Topologi & port](#2-topologi--port)
3. [First-time setup](#3-first-time-setup)
4. [Menjalankan stack](#4-menjalankan-stack)
5. [Verifikasi cepat](#5-verifikasi-cepat)
6. [Akun demo](#6-akun-demo)
7. [Hot reload & iterasi kode](#7-hot-reload--iterasi-kode)
8. [Stop & teardown](#8-stop--teardown)
9. [Logs & inspeksi container](#9-logs--inspeksi-container)
10. [Menjalankan unit test](#10-menjalankan-unit-test)
11. [Alternatif: native dev tanpa container](#11-alternatif-native-dev-tanpa-container)
12. [Troubleshooting](#12-troubleshooting)
13. [Mengaktifkan Google SSO](#13-mengaktifkan-google-sso)
14. [Rotate `SESSION_SECRET` (force logout)](#14-rotate-session_secret-force-logout)
15. [Inspect audit log](#15-inspect-audit-log)

---

## 1. Prasyarat

| Tool | Versi | Catatan |
| --- | --- | --- |
| Docker (Engine + Compose v2) | terbaru | atau Podman ≥ 4 + `podman-compose` ≥ 1.0.3 |
| Git | apa saja | |
| Browser modern | evergreen | Chrome / Edge / Firefox / Safari |

Tidak perlu Python atau Node terinstal di host — semua dijalankan dalam container.

Pada dokumen ini, perintah ditulis dengan `docker compose` (Docker v2). Pengguna Podman tinggal ganti dengan `podman-compose` — argumen-flag identik.

## 2. Topologi & port

Sejak v0.3, **dua portal independen** berjalan paralel:

| Portal | Web | BFF | Backend | DB target (Fase 2+) | Compose file |
| --- | --- | --- | --- | --- | --- |
| **Zakat** | `:5173` | `:7000` | `:8000` | `mziss_laz` | `infra/docker-compose.zakat.yml` |
| **Wakaf** | `:5174` | `:7001` | `:8001` | `mzis_wakaf` | `infra/docker-compose.wakaf.yml` |

Diagram per portal:

```
Browser
  └─ http://localhost:5173   web-vue   (Vite dev)
       └─ fetch              bff-api   (FastAPI + SQLite session)
                                 └─ proxy   api-python  (FastAPI dummy / existing DB Fase 2+)
```

Tiap stack punya **project namespace sendiri** (`isf-zakat`, `isf-wakaf`) → volume + network terisolasi.

Pastikan port-port di atas kosong sebelum start:

```bash
ss -ltn '( sport = :5173 or sport = :5174 or sport = :7000 or sport = :7001 or sport = :8000 or sport = :8001 )'
```

## 3. First-time setup

```bash
git clone <repo-url> isf-app
cd isf-app/infra
cp .env.example .env       # opsional; default sudah cukup untuk dev
```

`.env` di-load otomatis oleh **kedua** compose file (`env_file:` directive). Isi `.env` berlaku untuk zakat dan wakaf.

Tidak perlu `npm install` atau `pip install` di host — container yang mengurusnya.

## 4. Menjalankan stack

### 4.1 Zakat (default)

```bash
cd infra
docker compose -f docker-compose.zakat.yml up -d --build              # atau: podman-compose -f docker-compose.zakat.yml up -d --build
```

Open: <http://localhost:5173>

### 4.2 Wakaf

```bash
cd infra
docker compose -f docker-compose.wakaf.yml up -d --build
# atau: podman-compose -f docker-compose.wakaf.yml up -d --build
```

Open: <http://localhost:5174>

### 4.3 Kedua stack paralel

Kedua compose file di-namespace lewat `name:` directive (`isf-zakat` / `isf-wakaf`) → tidak ada konflik volume/network. Bisa di-`up` bergiliran atau bersamaan.

```bash
docker compose -f docker-compose.zakat.yml up -d --build
docker compose -f docker-compose.wakaf.yml up -d --build
docker ps --filter "name=isf-"            # → 6 container running (3 per stack)
```

Build pertama kali per stack men-download:

- `python:3.12-slim` + deps (bff-api, api-python).
- `node:20-alpine` + deps (web-vue).

Estimasi 3–8 menit per stack tergantung jaringan. Build kedua dst pakai cache (cepat).

## 5. Verifikasi cepat

### 5.1 Health checks

```bash
# Zakat
curl -s http://localhost:8000/health      # api-python
curl -s http://localhost:7000/health      # bff-api

# Wakaf
curl -s http://localhost:8001/health      # api-python
curl -s http://localhost:7001/health      # bff-api
```

Semua harus respons `{"data":{"status":"ok"},"meta":{...}}`.

### 5.2 End-to-end auth + dashboard (zakat)

```bash
COOKIE=/tmp/c-zakat.txt
curl -s -c "$COOKIE" -X POST http://localhost:7000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}' | jq .

curl -s -b "$COOKIE" http://localhost:7000/api/dashboard/summary | jq .
```

Untuk wakaf, ganti `:7000` → `:7001` dan `c-zakat.txt` → `c-wakaf.txt`. **Session terisolasi per stack** — cookie zakat tidak valid di wakaf, dan sebaliknya.

### 5.3 Via browser

| Portal | URL | Tampilan |
| --- | --- | --- |
| Zakat | <http://localhost:5173> | Login → dashboard "Lembaga ZISWAF A" (data dummy) |
| Wakaf | <http://localhost:5174> | Sama (data dummy identik untuk sekarang — wakaf akan diverge) |

## 6. Akun demo

Sama di kedua portal (data seed identik karena wakaf masih clone identik dari zakat).

| Username | Password | Akses tenant |
| --- | --- | --- |
| `admin` | `admin123` | Perusahaan A + Perusahaan B |
| `finance.a` | `finance123` | Perusahaan A saja |
| `finance.b` | `finance123` | Perusahaan B saja |

`finance.a` mencoba switch ke `perusahaan_b` akan ditolak (HTTP 403 `TENANT_FORBIDDEN`).

> Catatan: setelah split deployment, multi-tenant switcher kehilangan relevansi (tiap portal single-tenant). Akun demo masih kelihatan punya akses ke 2 perusahaan karena seed belum disesuaikan — akan dirapikan saat tim wakaf garap. Untuk Fase 2+ tiap portal akan punya seed user spesifik.

## 7. Hot reload & iterasi kode

Source code di-bind-mount ke container:

| Host | Container | Stack |
| --- | --- | --- |
| `apps_zakat/web-vue/` | `/app` (web-vue) | zakat |
| `apps_zakat/bff-api/` | `/app` (bff-api) | zakat |
| `apps_zakat/api-python/` | `/app` (api-python) | zakat |
| `apps_wakaf/web-vue/` | `/app` (web-vue) | wakaf |
| `apps_wakaf/bff-api/` | `/app` (bff-api) | wakaf |
| `apps_wakaf/api-python/` | `/app` (api-python) | wakaf |

Edit file di host → Vite (frontend) dan `uvicorn --reload` (backend) auto pick up.

`apps_*/web-vue/node_modules/` diisolasi via anonymous volume agar tidak bentrok dengan host (mis. setelah `npm install` lokal).

`CHOKIDAR_USEPOLLING=true` sudah di-set untuk web-vue → Vite file-watching reliable di bind mount Linux.

Tambah dependency:

```bash
# Frontend (zakat)
docker compose -f docker-compose.zakat.yml exec web-vue npm install <pkg>

# Frontend (wakaf)
docker compose -f docker-compose.wakaf.yml exec web-vue npm install <pkg>

# Backend (Python — zakat)
docker compose -f docker-compose.zakat.yml exec bff-api pip install <pkg>
# lalu update pyproject.toml + rebuild image:
docker compose -f docker-compose.zakat.yml build bff-api
```

## 8. Stop & teardown

```bash
# Zakat
docker compose -f docker-compose.zakat.yml down                  # stop & hapus container
docker compose -f docker-compose.zakat.yml down -v               # + hapus volume isf-zakat (auth.sqlite hilang)

# Wakaf
docker compose -f docker-compose.wakaf.yml down
docker compose -f docker-compose.wakaf.yml down -v

# Force rebuild penuh (tanpa cache)
docker compose -f docker-compose.zakat.yml build --no-cache
```

Image cache tetap. Untuk benar-benar bersih:

```bash
docker compose -f docker-compose.zakat.yml down -v --rmi local   # hapus image local-built juga
```

## 9. Logs & inspeksi container

```bash
# Logs semua service (zakat)
docker compose -f docker-compose.zakat.yml logs -f

# Logs satu service spesifik
docker compose -f docker-compose.zakat.yml logs -f bff-api
docker compose -f docker-compose.wakaf.yml logs -f web-vue

# Shell ke dalam container
docker compose -f docker-compose.zakat.yml exec bff-api sh
docker compose -f docker-compose.wakaf.yml exec api-python python
```

Status kedua stack:

```bash
docker ps --filter "name=isf-"
```

## 10. Menjalankan unit test

Test ada di `apps_<domain>/<service>/tests/` (lihat `docs/plan-mvp.md` & `docs/plan-auth.md`).

Di dalam container:

```bash
# Zakat
docker compose -f docker-compose.zakat.yml exec bff-api python -m pytest tests/ -v
docker compose -f docker-compose.zakat.yml exec api-python python -m pytest tests/ -v

# Wakaf
docker compose -f docker-compose.wakaf.yml exec bff-api python -m pytest tests/ -v
docker compose -f docker-compose.wakaf.yml exec api-python python -m pytest tests/ -v
```

Native (di host, jika ada Python 3.12+):

```bash
cd apps_zakat/bff-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest tests/ -v
```

Frontend belum punya unit test di MVP — verifikasi via browser.

## 11. Alternatif: native dev tanpa container

Berguna jika Docker/Podman tidak tersedia atau untuk debugging cepat.

**Terminal 1 — api-python (zakat):**

```bash
cd apps_zakat/api-python
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — bff-api (zakat):**

```bash
cd apps_zakat/bff-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
API_PYTHON_BASE_URL=http://localhost:8000 \
SESSION_SECRET=dev-secret-zakat \
CORS_ORIGIN=http://localhost:5173 \
AUTH_DB_PATH=/tmp/isf-zakat-auth.sqlite \
FRONTEND_BASE_URL=http://localhost:5173 \
uvicorn app.main:app --reload --port 7000
```

**Terminal 3 — web-vue (zakat):**

```bash
cd apps_zakat/web-vue
npm install
VITE_API_BASE_URL=http://localhost:7000 VITE_PORTAL_DOMAIN=zakat npm run dev
```

Buka <http://localhost:5173>.

Untuk wakaf, ganti path `apps_zakat/` → `apps_wakaf/` dan port +1 (5174 / 7001 / 8001).

## 12. Troubleshooting

### Port sudah dipakai

```
Error: bind: address already in use
```

Salah satu port (5173 / 5174 / 7000 / 7001 / 8000 / 8001) ditempati proses lain. Cari & matikan, atau ubah host port mapping di compose:

```yaml
ports:
  - "15173:5173"   # contoh remap web-vue zakat
```

### SELinux menolak bind mount (Fedora / RHEL / podman)

Gejala: container start tapi gagal baca file atau Vite/uvicorn tidak boot.

Solusi: tambah suffix `:z` (shared) atau `:Z` (private) di bind mount:

```yaml
volumes:
  - ../apps_zakat/bff-api:/app:z
```

### Web-vue tidak hot reload

`CHOKIDAR_USEPOLLING=true` sudah di-set di compose. Jika masih bermasalah (filesystem aneh), naikkan polling interval:

```yaml
environment:
  CHOKIDAR_USEPOLLING: "true"
  CHOKIDAR_INTERVAL: "300"
```

### Cookie tidak nyangkut (login terus diminta)

- Pastikan browser hit `http://localhost:5173` (bukan `127.0.0.1:5173`) — SameSite=lax menuntut origin konsisten.
- Cek CORS di BFF: `CORS_ORIGIN` harus persis sama dengan origin browser.
- Untuk wakaf, browser di `:5174` → CORS BFF wakaf `:7001` harus `http://localhost:5174`.

### `depends_on: condition: service_healthy` ditolak podman-compose lama

Upgrade ke podman-compose ≥ 1.0.3. Atau sebagai workaround:

```bash
podman-compose -f docker-compose.zakat.yml up -d api-python
sleep 5
podman-compose -f docker-compose.zakat.yml up -d bff-api web-vue
```

### Build gagal pip install / npm install (offline)

Cek koneksi internet. Build memerlukan akses ke PyPI dan npm registry.

### `web-vue` exit dengan "EACCES /app/node_modules"

Anonymous volume `node_modules` rusak. Bersihkan:

```bash
docker compose -f docker-compose.zakat.yml down -v
docker compose -f docker-compose.zakat.yml up -d --build
```

### Wakaf & zakat saling tumpang-tindih volume

Tidak mungkin terjadi karena `name:` directive di compose namespace volume per project (`isf-zakat-*`, `isf-wakaf-*`). Verifikasi:

```bash
docker volume ls | grep isf-
# Harus terlihat: isf-zakat-bff-data, isf-wakaf-bff-data (terpisah)
```

### Healthcheck gagal padahal service jalan

Lihat detail:

```bash
docker inspect isf-zakat-bff-api --format '{{json .State.Health}}' | jq
```

Penyebab umum: service masih starting (start_period 15–30s). Tunggu, atau cek logs.

---

## 13. Mengaktifkan Google SSO

Tombol "Continue with Google" di login page disabled saat `GOOGLE_OAUTH_CLIENT_ID` & `GOOGLE_OAUTH_CLIENT_SECRET` kosong. Cara aktifkan:

### 13.1 Buat OAuth client di Google Cloud Console

1. <https://console.cloud.google.com/apis/credentials> → pilih/buat project.
2. **+ CREATE CREDENTIALS → OAuth client ID**. Konfigurasi consent screen kalau pertama kali.
3. Application type: **Web application**.
4. Name: `isf-app dev`.
5. **Authorized JavaScript origins**: `http://localhost:5173` dan `http://localhost:5174` (tambahkan keduanya kalau pakai dua portal).
6. **Authorized redirect URIs** — wajib match dengan env `GOOGLE_OAUTH_REDIRECT_URL_*`:
   - `http://localhost:7000/api/auth/google/callback` (zakat)
   - `http://localhost:7001/api/auth/google/callback` (wakaf)
7. Klik **Create**. Copy Client ID & Client Secret.

### 13.2 Set env di `infra/.env`

```env
GOOGLE_OAUTH_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-yyyyy
GOOGLE_ALLOWED_DOMAINS=ihsansolusi.co.id
# atau GOOGLE_ALLOWED_EMAILS=user@gmail.com untuk per-email allowlist
```

(Optionally override redirect URL atau frontend base URL kalau berbeda dari default.)

### 13.3 Restart stack

```bash
cd infra
docker compose -f docker-compose.zakat.yml restart bff-api                          # zakat
docker compose -f docker-compose.wakaf.yml restart bff-api  # wakaf
```

### 13.4 Verifikasi

```bash
curl -s http://localhost:7000/api/auth/providers | jq
# expected: { "data": { "password": true, "google": true }, "meta": {...} }
curl -s http://localhost:7001/api/auth/providers | jq
# expected sama
```

Login di browser → tombol Google sekarang enabled.

### 13.5 Production checklist

- Update redirect URI di GCP ke domain production (`https://app.example.com/...`).
- Sesuaikan `GOOGLE_OAUTH_REDIRECT_URL_*` dan `FRONTEND_BASE_URL_*` di env production.
- Cek audit log: `SELECT * FROM audit_log WHERE event LIKE 'sso_%' ORDER BY ts DESC LIMIT 20` (lihat §15).

---

## 14. Rotate `SESSION_SECRET` (force logout)

Session pakai signed cookie (Starlette `SessionMiddleware`) — tidak ada server-side session store. Untuk **force-logout semua user** di stack tertentu:

```bash
# Generate secret baru
python -c "import secrets; print(secrets.token_urlsafe(48))"

# Edit infra/.env — pilih variabel sesuai stack
#   SESSION_SECRET_ZAKAT=<paste hasil step 1>
#   SESSION_SECRET_WAKAF=<paste hasil step 1>

# Restart bff-api stack terkait
cd infra
docker compose -f docker-compose.zakat.yml restart bff-api                              # zakat saja
# atau:
docker compose -f docker-compose.wakaf.yml restart bff-api  # wakaf saja
```

Semua cookie session lama jadi invalid (signature mismatch) → pengguna diminta login lagi.

> Untuk revocation per-user, perlu pindah ke server-side session store (mis. Redis). Lihat `docs/architecture.md` §14 / out-of-scope di `docs/plan-auth.md`.

---

## 15. Inspect audit log

Tiap stack punya `auth.sqlite` sendiri (volume `isf-zakat-bff-data` / `isf-wakaf-bff-data`).

```bash
# 20 event terakhir — zakat
docker compose -f docker-compose.zakat.yml exec bff-api sqlite3 /data/auth.sqlite \
  "SELECT ts, event, user_id, tenant_id, payload_json FROM audit_log ORDER BY ts DESC LIMIT 20"

# Login gagal seminggu terakhir — zakat
docker compose -f docker-compose.zakat.yml exec bff-api sqlite3 /data/auth.sqlite \
  "SELECT ts, payload_json FROM audit_log WHERE event='login_failed' AND ts >= datetime('now','-7 days')"

# Aktivitas SSO — wakaf
docker compose -f docker-compose.wakaf.yml exec bff-api sqlite3 /data/auth.sqlite \
  "SELECT ts, event, payload_json FROM audit_log WHERE event LIKE 'sso_%' ORDER BY ts DESC"
```

Tabel tersedia: `users`, `user_credentials`, `user_provider_links`, `tenants`, `tenant_memberships`, `audit_log` (lihat skema di `docs/plan-auth.md` §3).

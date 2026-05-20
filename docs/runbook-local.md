# Runbook — Local Deployment

> Cara membawa stack `isf-app` (MVP Fase 1) sampai jalan di laptop pengembang. Lihat [`docs/plan-mvp.md`](./plan-mvp.md) untuk konteks fitur, [`docs/architecture.md`](./architecture.md) untuk arsitektur.

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

---

## 1. Prasyarat

| Tool | Versi | Catatan |
| --- | --- | --- |
| Docker (Engine + Compose v2) | terbaru | atau Podman ≥ 4 + `podman-compose` |
| Git | apa saja | |
| Browser modern | evergreen | Chrome / Edge / Firefox / Safari |

Tidak perlu Python atau Node terinstal di host — semua dijalankan dalam container.

## 2. Topologi & port

```
Browser
  └─ http://localhost:5173      ── web-vue   (Vite dev server)
       └─ fetch                ─→ http://localhost:7000  bff-api   (FastAPI + session)
                                     └─ proxy           ─→ http://api-python:8000  api-python (FastAPI)
```

Port yang dipakai di host:

| Port | Service | Tujuan |
| --- | --- | --- |
| 5173 | web-vue | UI (Vite dev) |
| 7000 | bff-api | API publik untuk browser |
| 8000 | api-python | Backend (akses langsung opsional, untuk debugging) |

Pastikan ketiganya kosong sebelum start (`ss -ltn '( sport = :5173 or sport = :7000 or sport = :8000 )'`).

## 3. First-time setup

```bash
git clone <repo-url> isf-app
cd isf-app/infra
cp .env.example .env          # opsional; default sudah cukup untuk dev
```

Tidak ada langkah `npm install` atau `pip install` di host — container yang mengurusnya.

## 4. Menjalankan stack

```bash
cd infra
docker compose up --build -d     # build images pertama kali butuh beberapa menit
```

Jika pakai Podman:

```bash
cd infra
podman-compose up --build -d
```

Pertama kali build (tanpa cache) men-download:

- `python:3.12-slim` + `pip install fastapi uvicorn httpx itsdangerous pydantic pydantic-settings pytest`
- `node:20-alpine` + `npm install vue vue-router pinia vite @vitejs/plugin-vue typescript vue-tsc`

Estimasi 3–8 menit tergantung jaringan. Build kedua dan seterusnya pakai cache (cepat).

Periksa status:

```bash
docker compose ps
```

Ketiga service harus `running` / `healthy`.

## 5. Verifikasi cepat

### 5.1 Health checks

```bash
curl -s http://localhost:8000/health
curl -s http://localhost:7000/health
```

Keduanya harus respons `{"data":{"status":"ok"},"meta":{...}}`.

### 5.2 End-to-end via curl (membuktikan multi-tenant)

```bash
COOKIE=/tmp/isf-cookie.txt

# Login
curl -s -c "$COOKIE" -X POST http://localhost:7000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"admin123"}' | jq .

# List tenant + current
curl -s -b "$COOKIE" http://localhost:7000/api/tenants | jq .

# Dashboard untuk tenant default (perusahaan_a)
curl -s -b "$COOKIE" http://localhost:7000/api/dashboard/summary | jq .

# Switch ke perusahaan_b
curl -s -b "$COOKIE" -c "$COOKIE" -X POST http://localhost:7000/api/tenants/switch \
  -H 'Content-Type: application/json' \
  -d '{"tenant_id":"perusahaan_b"}' | jq .

# Dashboard sekarang harus berubah ke perusahaan_b
curl -s -b "$COOKIE" http://localhost:7000/api/dashboard/summary | jq .

# Logout
curl -s -b "$COOKIE" -X POST http://localhost:7000/api/auth/logout | jq .
```

### 5.3 Via browser

1. Buka `http://localhost:5173` → otomatis redirect ke `/login`.
2. Login `admin` / `admin123`.
3. Dashboard tampil dengan 2 widget (Penerimaan & Penyaluran) untuk **Lembaga ZISWAF A**.
4. Klik dropdown perusahaan di header → pilih **Lembaga ZISWAF B** → widget update.
5. Klik **Logout** → kembali ke login.

## 6. Akun demo

| Username | Password | Tenant |
| --- | --- | --- |
| `admin` | `admin123` | perusahaan_a + perusahaan_b |
| `finance.a` | `finance123` | perusahaan_a saja |
| `finance.b` | `finance123` | perusahaan_b saja |

User `finance.a` mencoba switch ke `perusahaan_b` akan ditolak (HTTP 403 `TENANT_FORBIDDEN`).

## 7. Hot reload & iterasi kode

Source code di-bind-mount ke container:

| Path host | Path container |
| --- | --- |
| `apps/web-vue/` | `/app` (web-vue) |
| `apps/bff-api/` | `/app` (bff-api) |
| `apps/api-python/` | `/app` (api-python) |

- Edit file di host → Vite (frontend) dan `uvicorn --reload` (backend & BFF) otomatis pick up perubahan.
- `apps/web-vue/node_modules/` diisolasi dengan anonymous volume agar tidak bentrok dengan host (kalau host pernah `npm install`).

Tambah dependency:

```bash
# Frontend
docker compose exec web-vue npm install <pkg>

# Python (bff-api atau api-python)
docker compose exec bff-api pip install <pkg>
# lalu tambahkan ke pyproject.toml dan rebuild image: docker compose build bff-api
```

## 8. Stop & teardown

```bash
cd infra
docker compose down                 # stop & hapus container
docker compose down -v              # + hapus volume (termasuk node_modules)
```

Image cache tetap. Untuk paksa rebuild penuh:

```bash
docker compose build --no-cache
```

## 9. Logs & inspeksi container

```bash
docker compose logs -f                 # semua service
docker compose logs -f bff-api         # satu service
docker compose exec bff-api sh         # shell ke dalam container
docker compose exec api-python python  # REPL Python
```

## 10. Menjalankan unit test

Test diletakkan di `apps/<service>/tests/` (lihat `docs/plan-mvp.md`).

Di dalam container:

```bash
docker compose exec bff-api python -m pytest tests/ -v
docker compose exec api-python python -m pytest tests/ -v
```

Atau secara native (jika punya Python 3.12+):

```bash
cd apps/bff-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest tests/ -v
```

Frontend belum punya unit test di MVP — verifikasi via browser.

## 11. Alternatif: native dev tanpa container

Berguna jika Docker tidak tersedia (atau untuk debugging cepat).

**Terminal 1 — api-python:**

```bash
cd apps/api-python
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — bff-api:**

```bash
cd apps/bff-api
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
API_PYTHON_BASE_URL=http://localhost:8000 \
SESSION_SECRET=dev-secret-change-me \
CORS_ORIGIN=http://localhost:5173 \
uvicorn app.main:app --reload --port 7000
```

**Terminal 3 — web-vue:**

```bash
cd apps/web-vue
npm install
VITE_API_BASE_URL=http://localhost:7000 npm run dev
```

Lalu buka `http://localhost:5173`.

## 12. Troubleshooting

### Port sudah dipakai

```
Error: bind: address already in use
```

Salah satu port (5173 / 7000 / 8000) ditempati proses lain. Cari & matikan, atau ubah host port mapping di `infra/docker-compose.yml`:

```yaml
ports:
  - "15173:5173"   # contoh remap
```

### SELinux menolak bind mount (Fedora / RHEL / podman)

Gejala: container start tapi gagal baca file atau Vite/uvicorn tidak boot.

Solusi: tambahkan suffix `:z` (shared) atau `:Z` (private) pada bind mount di `docker-compose.yml`:

```yaml
volumes:
  - ../apps/bff-api:/app:z
```

### Web-vue tidak hot reload di Linux

File watcher Vite kadang butuh polling pada bind mount:

```yaml
environment:
  CHOKIDAR_USEPOLLING: "true"
  VITE_API_BASE_URL: http://localhost:7000
```

### Cookie tidak nyangkut (login terus diminta)

Pastikan browser hit `http://localhost:5173` (bukan `127.0.0.1:5173`) dan request fetch ke `http://localhost:7000`. SameSite=lax memerlukan origin yang konsisten. Cek juga CORS di BFF (`CORS_ORIGIN` harus persis sama dengan origin browser).

### `depends_on: condition: service_healthy` ditolak podman-compose lama

podman-compose 1.0.x belum mendukung. Solusi cepat:

```bash
podman-compose up -d api-python
sleep 5
podman-compose up -d bff-api web-vue
```

Atau upgrade ke podman-compose ≥ 1.0.3.

### Build gagal pip install / npm install (offline)

Cek koneksi internet di host. Build memerlukan akses ke PyPI dan npm registry.

### `web-vue` segera exit dengan "EACCES /app/node_modules"

Anonymous volume untuk `node_modules` rusak. Bersihkan:

```bash
docker compose down -v
docker compose up --build -d
```

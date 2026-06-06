---
name: run-isf-app
description: Run, start, launch, screenshot, verify, or test the isf-app zakat portal. Use when asked to run the app, confirm a feature works in the browser, take a screenshot of any page, or smoke-test the stack.
---

# isf-app — Zakat Portal Run Skill

isf-app adalah sistem manajemen ZIS (Zakat, Infaq, Sedekah) dengan empat service per portal. Portal **zakat** dijalankan via **podman-compose** dan diakses di `http://localhost:5173`. Untuk interaksi browser gunakan **Playwright MCP** (`mcp__plugin_playwright_playwright__*`) — tidak perlu driver terpisah.

---

## Arsitektur (Zakat Stack)

| Service | Container | Port host | Keterangan |
|---|---|---|---|
| web-vue | `isf-zakat-web-vue` | 5173 | Frontend Vue 3 |
| bff-api | `isf-zakat-bff-api` | 7000 | Session gateway + proxy |
| api-python | `isf-zakat-api-python` | 8000 | Operasional / transaksi |
| report-api | `isf-zakat-report-api` | 8010 | Laporan read-only |

---

## Prerequisites

```bash
# Semua sudah ada di host ini:
podman          # container runtime
podman-compose  # compose wrapper
make            # orkestrasi Makefile
```

DB lokal (PostgreSQL) sudah ada; user `transaction:solusi`. Untuk isf_auth:

```bash
# Hanya perlu sekali (kalau DB belum ada):
make migrate
```

---

## Build — hanya jika pyproject.toml / package.json berubah

Source code di-bind-mount sehingga uvicorn/vite auto-reload. Rebuild hanya diperlukan bila dependency berubah:

```bash
# Rebuild semua zakat images (SELinux workaround sudah di-set)
make build-zakat
```

Perintah di atas menjalankan `podman build --security-opt label=disable` untuk api-python, report-api, bff-api, web-vue secara berurutan.

---

## Run (agent path) — Playwright MCP

### 1. Pastikan stack berjalan

```bash
make run-zakat
# atau cek status:
podman-compose -f infra/docker-compose.zakat.yml ps
```

Semua harus menunjukkan `(healthy)`:

```
isf-zakat-api-python   Up X min (healthy)   0.0.0.0:8000->8000/tcp
isf-zakat-report-api   Up X min (healthy)   0.0.0.0:8010->8000/tcp
isf-zakat-bff-api      Up X min (healthy)   0.0.0.0:7000->7000/tcp
isf-zakat-web-vue      Up X min (healthy)   0.0.0.0:5173->5173/tcp
```

Verifikasi cepat:

```bash
curl -s http://localhost:7000/health   # {"data":{"status":"ok"},...}
curl -s http://localhost:8000/health   # {"data":{"status":"ok"},...}
curl -s http://localhost:8010/health   # {"data":{"status":"ok"},...}
curl -s http://localhost:5173 -o /dev/null -w "%{http_code}"  # 200
```

### 2. Buka browser via Playwright MCP

```
mcp__plugin_playwright_playwright__browser_navigate  url=http://localhost:5173
```

### 3. Login

Halaman login di `/login`. Kredensial dev yang tersedia:

| Username | Password | Roles | Cabang |
|---|---|---|---|
| `RAIS` | `test1234` | ACC, KEU | 001 (single) |
| `HADI` | `test1234` | DIST, SPVDIST | semua |

```
mcp__plugin_playwright_playwright__browser_fill_form
  fields: [
    { target: "input[name=username]" atau snapshot ref, name: "Username", type: "textbox", value: "RAIS" },
    { target: "input[type=password]", name: "Password",  type: "textbox", value: "test1234" }
  ]

mcp__plugin_playwright_playwright__browser_click  target: button[Masuk]
```

Setelah login sukses, browser redirect ke `/`.

> ⚠️ **Menu key penting**: setelah menambah `role_menu` baru ke DB, user harus **logout + login ulang** — session menus di-snapshot saat login. Gunakan tombol profil → Logout di pojok kanan atas.

### 4. Navigasi dan screenshot

```
# Contoh — Histori Transaksi
mcp__plugin_playwright_playwright__browser_navigate  url=http://localhost:5173/keuangan/transaksi/histori

# Screenshot (fullPage=true untuk halaman panjang)
mcp__plugin_playwright_playwright__browser_take_screenshot  type=png  filename=ss-histori.png  fullPage=true
```

Route utama yang tersedia:

| Path | Keterangan |
|---|---|
| `/` | Dashboard overview |
| `/dashboard/keuangan` | Dashboard keuangan |
| `/keuangan/coa` | Chart of Accounts |
| `/keuangan/kas` | Manajemen Kas |
| `/keuangan/bank` | Manajemen Bank |
| `/keuangan/transaksi/histori` | Histori Transaksi (role KEU/SPVKEU) |
| `/keuangan/upload/penghimpunan` | Upload Penghimpunan (role KEU/SPVKEU) |
| `/keuangan/upload/penghimpunan/list` | Otorisasi Upload (role SPVKEU) |
| `/keuangan/laporan/jurnal-harian` | Jurnal Harian |
| `/keuangan/laporan/transaksi-umum` | List Transaksi Umum |

### 5. Isi form tanggal (DateField)

DateField menerima format DD-MM-YYYY. Cara paling andal via JS evaluation:

```js
// Set input pertama (begin date) ke 01-01-2025
await page.evaluate(() => {
  const inp = document.querySelectorAll('input[placeholder="DD-MM-YYYY"]')[0];
  inp.value = '01012025';
  inp.dispatchEvent(new Event('input', {bubbles: true}));
  inp.dispatchEvent(new Event('blur', {bubbles: true}));
});
```

Lalu klik tombol "Tampilkan" dan tunggu data:

```
mcp__plugin_playwright_playwright__browser_click  target: button[Tampilkan]
mcp__plugin_playwright_playwright__browser_wait_for  time=3
```

---

## Run (human path)

```bash
make run-zakat      # start stack
# buka http://localhost:5173 di browser
make stop-zakat     # stop
```

---

## Smoke test via curl (tanpa browser)

Login dan test API langsung:

```bash
# Login, simpan cookie
curl -s -c /tmp/isf.txt -X POST http://localhost:7000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"RAIS","password":"test1234"}'

# Cek session
curl -s -b /tmp/isf.txt http://localhost:7000/api/auth/me | python3 -m json.tool

# Search histori transaksi (106k+ rows di data lokal)
curl -s -b /tmp/isf.txt \
  "http://localhost:7000/api/transaksi-histori/search?begin=2025-01-01&end=2026-06-06&page=1&page_size=5" \
  | python3 -c "import sys,json;d=json.load(sys.stdin)['data'];print(f'total={d[\"total\"]} rows={len(d[\"rows\"])}')"
# → total=56882 rows=5  (angka bervariasi sesuai filter cabang RAIS=001)

# Health checks semua service
curl -s http://localhost:8000/health   # api-python
curl -s http://localhost:8010/health   # report-api
curl -s http://localhost:7000/health   # bff-api
```

Script E2E yang sudah ada:

```bash
bash testing/e2e-histori-transaksi.sh    # histori transaksi
bash testing/e2e-upload-penghimpunan.sh  # upload penghimpunan
```

> ⚠️ Script E2E menggunakan port 8001 (hardcoded lama) — api-python aktual di port **8000**. Ganti `API="http://localhost:8000"` bila perlu.

---

## Gotchas

- **`podman build` gagal `Permission denied`** di Fedora 44 + SELinux Enforcing: jangan gunakan `--build` di `podman-compose up`. Selalu pre-build manual dengan `--security-opt label=disable` via `make build-zakat`.

- **`python-multipart` tidak ada di bff-api image lama**: kalau bff-api crash dengan `RuntimeError: Form data requires "python-multipart"`, rebuild image bff-api (`make build-zakat`).

- **`asyncpg` menolak string ISO untuk parameter date**: query repository transaksi_histori mengonversi `begin`/`end` ke `datetime.date` object via `_date.fromisoformat()`. Jika error `'str' object has no attribute 'toordinal'`, pastikan versi terbaru kode sudah di-bind-mount dan uvicorn sudah reload.

- **Menu baru tidak muncul di sidebar**: session menus di-snapshot saat login. Setelah menambah `role_menu` ke DB, user wajib **logout + login ulang** di browser. Tidak cukup refresh halaman.

- **DateField tidak bisa diketik langsung via Playwright `fill()`**: gunakan `page.evaluate()` + dispatch `input` + `blur` event (lihat contoh di atas).

- **E2E script port salah**: `testing/e2e-histori-transaksi.sh` dan `e2e-upload-penghimpunan.sh` hardcode `API=http://localhost:8001` — port lama. Api-python aktual: **8000**.

---

## Troubleshooting

| Gejala | Penyebab | Fix |
|---|---|---|
| `bff-api` status `starting` loop → crash | `python-multipart` belum di-install | `make build-zakat` |
| Login redirect kembali ke `/login` | `ISF_AUTH_DATABASE_URL` tidak di-set atau DB isf_auth belum di-migrate | `make migrate` |
| Histori transaksi → `denied=keuangan.transaksi.histori` | Session lama (login sebelum menu key ditambah) | Logout + Login ulang |
| `isf-zakat-web-vue` status `Exited (1)` | npm install gagal di startup | `make build-zakat` lalu `make run-zakat` |
| COA halaman kosong / error | `DATABASE_URL` tidak terhubung ke mziss_laz | Periksa `infra/.env` dan koneksi Postgres |

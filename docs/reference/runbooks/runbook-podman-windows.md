# Runbook — Podman Desktop di Windows

> Panduan menjalankan stack `isf-app` (Portal Zakat & Portal Wakaf) menggunakan **Podman Desktop di Windows 10/11**, tanpa Docker Desktop. Untuk konsep umum lihat [`runbook-local.md`](./runbook-local.md); runbook ini fokus pada hal Windows-specific.

## Daftar isi

1. [Kenapa Podman, bukan Docker](#1-kenapa-podman-bukan-docker)
2. [Prasyarat](#2-prasyarat)
3. [Install WSL2](#3-install-wsl2)
4. [Install Podman Desktop](#4-install-podman-desktop)
5. [Atur resource WSL2 lewat `.wslconfig`](#5-atur-resource-wsl2-lewat-wslconfig)
6. [Buat Podman machine](#6-buat-podman-machine)
7. [Install `podman-compose`](#7-install-podman-compose)
8. [Setup PostgreSQL di host Windows](#8-setup-postgresql-di-host-windows)
9. [Konfigurasi `.env`](#9-konfigurasi-env)
10. [Menjalankan stack](#10-menjalankan-stack)
11. [Verifikasi](#11-verifikasi)
12. [Auto-start saat boot](#12-auto-start-saat-boot)
13. [Update kode & rebuild](#13-update-kode--rebuild)
14. [Stop & teardown](#14-stop--teardown)
15. [Troubleshooting](#15-troubleshooting)

---

## 1. Kenapa Podman, bukan Docker

| Aspek | Podman Desktop | Docker Desktop |
| --- | --- | --- |
| Lisensi | Open source, gratis tanpa batas | Berbayar untuk perusahaan > 250 employee / > $10M revenue |
| Engine | Rootless by default | Root daemon |
| Compose | `podman-compose` (Python) atau `podman compose` (Go) | `docker compose` (built-in) |
| Compatibility | API Docker-compatible | Native |
| Konvensi project | `host.containers.internal` (default di compose ini) | `host.docker.internal` |

Compose file project ini (`docker-compose.zakat.yml`, `docker-compose.wakaf.yml`) sudah pakai `host.containers.internal` — **konvensi native Podman**. README contoh perintah juga `podman-compose`. Jadi Podman = pilihan first-class untuk repo ini.

## 2. Prasyarat

| Komponen | Versi minimum | Catatan |
| --- | --- | --- |
| Windows | 10 build 19041+ / 11 | Virtualization aktif di BIOS (Intel VT-x / AMD-V) |
| RAM | 8 GB | Direkomendasikan 16 GB+ (host + WSL2 + container) |
| Disk | 20 GB free | Untuk image, build cache, dan WSL2 disk |
| WSL2 | terbaru | Install via `wsl --install` |
| Podman | ≥ 4.5 | Via `winget` atau installer |
| Podman Desktop | ≥ 1.0 | GUI opsional tapi sangat membantu |
| Python | ≥ 3.10 | Untuk `pip install podman-compose` |
| PostgreSQL | ≥ 14 | Native Windows installer (EDB) |

Cek virtualization aktif:

```powershell
systeminfo | findstr /i "Hyper-V"
```

Kalau muncul "A hypervisor has been detected" → aktif. Kalau tidak, masuk BIOS, enable Intel Virtualization Technology / AMD-V, lalu boot ulang.

## 3. Install WSL2

Buka **PowerShell sebagai Administrator**, jalankan:

```powershell
wsl --install --no-distribution
```

Flag `--no-distribution` skip install Ubuntu — Podman akan bikin distro sendiri (`podman-machine-default`).

**Restart Windows** setelah selesai.

Verifikasi:

```powershell
wsl --status
```

Pastikan "Default Version: 2".

## 4. Install Podman Desktop

Lewat winget (PowerShell user biasa):

```powershell
winget install -e --id RedHat.Podman
winget install -e --id RedHat.Podman-Desktop
```

Atau manual download:

- Engine: <https://podman.io/docs/installation>
- Desktop: <https://podman-desktop.io/downloads/windows>

Verifikasi:

```powershell
podman version
```

## 5. Atur resource WSL2 lewat `.wslconfig`

> ⚠️ Podman di Windows pakai WSL2 backend. CPU & memory tidak bisa diubah dengan `podman machine set` (akan muncul error *"changing CPUs not supported for WSL machines"*). Limit diatur **global** lewat `%UserProfile%\.wslconfig`.

Buat file `C:\Users\<username>\.wslconfig` (catat: nama file dengan titik di depan):

```ini
[wsl2]
processors=8
memory=8GB
swap=2GB
```

Atau lewat PowerShell:

```powershell
@"
[wsl2]
processors=8
memory=8GB
swap=2GB
"@ | Out-File -FilePath "$env:USERPROFILE\.wslconfig" -Encoding ASCII
```

Sesuaikan angka dengan spec mesin:

| Mesin | `processors` | `memory` | Catatan |
| --- | --- | --- | --- |
| Workstation 16C/32T, 32 GB RAM | 8 | 8GB | Cukup untuk 6 container + headroom |
| Laptop 8C/16T, 16 GB RAM | 4 | 6GB | Sisakan 10 GB untuk Windows |
| Server dedicated | 16 | 16GB | Kalau dipakai untuk staging multi-stack |

Setelah file dibuat:

```powershell
wsl --shutdown                              # apply config
```

Konfigurasi `.wslconfig` berlaku untuk **semua** WSL2 distro di akun user tersebut.

## 6. Buat Podman machine

### Lewat GUI

Buka Podman Desktop → wizard "Get started" akan muncul → tab **Podman Setup**. Form "Create a Podman machine":

| Field | Nilai |
| --- | --- |
| Name | `podman-machine-default` (biarkan) |
| Image Path | kosong |
| Image URL | kosong |
| Machine with root privileges | Enabled |
| User mode networking | Disabled |
| Start the machine now | Enabled |

Klik **Create**. Tunggu sampai status `RUNNING`.

### Lewat CLI

```powershell
podman machine init
podman machine start
```

Note: flag `--cpus` dan `--memory` saat `init` di Windows akan **diabaikan** karena tunduk pada `.wslconfig`. Set `.wslconfig` dulu (langkah 5) sebelum init machine.

Verifikasi:

```powershell
podman machine list
podman machine inspect podman-machine-default | findstr -i "state cpus memory"
podman run --rm hello-world
```

## 7. Install `podman-compose`

```powershell
pip install --upgrade podman-compose
podman-compose --version       # ≥ 1.0.3
```

> Catatan: `podman compose` (tanpa tanda hubung, subcommand bawaan Podman 4+) juga bisa, tapi `podman-compose` lebih kompatibel dengan compose file project ini (yang pakai fitur `env_file: { path:, required: }` dari Compose spec v2).

## 8. Setup PostgreSQL di host Windows

Compose pointing ke `host.containers.internal:5432` → **Postgres di host Windows**, bukan container.

### 8.1 Install

Download installer dari EDB: <https://www.postgresql.org/download/windows/>

Saat install:

- Pilih versi ≥ 14
- Password superuser: catat untuk login awal
- Port: `5432`
- Locale: default

### 8.2 Buat user & database

Buka **pgAdmin** (terinstall otomatis) atau psql:

```sql
-- login sebagai postgres superuser
CREATE USER transaction WITH PASSWORD 'solusi';

CREATE DATABASE mziss_laz OWNER transaction;
CREATE DATABASE mziss_wakaf OWNER transaction;

GRANT ALL PRIVILEGES ON DATABASE mziss_laz TO transaction;
GRANT ALL PRIVILEGES ON DATABASE mziss_wakaf TO transaction;
```

### 8.3 Allow koneksi dari WSL2

WSL2 punya subnet `172.x.x.x` yang berubah-ubah. Edit `C:\Program Files\PostgreSQL\<ver>\data\pg_hba.conf`, tambahkan:

```
# Allow WSL2 subnet
host    all    transaction    172.16.0.0/12    scram-sha-256
host    all    transaction    192.168.0.0/16   scram-sha-256
```

Edit `postgresql.conf`:

```
listen_addresses = '*'
```

Restart service PostgreSQL:

```powershell
Restart-Service postgresql-x64-16            # nama service tergantung versi
```

Atau lewat **Services.msc** → cari `postgresql-*` → Restart.

### 8.4 Buka firewall

Allow inbound TCP 5432 dari subnet WSL2:

```powershell
New-NetFirewallRule -DisplayName "PostgreSQL WSL2" `
  -Direction Inbound -Protocol TCP -LocalPort 5432 `
  -RemoteAddress 172.16.0.0/12,192.168.0.0/16 -Action Allow
```

### 8.5 Verifikasi dari container

Setelah machine running:

```powershell
podman run --rm -it postgres:16 psql `
  "postgresql://transaction:solusi@host.containers.internal:5432/mziss_laz" -c "SELECT 1"
```

Output `?column? = 1` → koneksi sukses.

## 9. Konfigurasi `.env`

```powershell
cd D:\workshop\isf-app\infra
Copy-Item .env.example .env
```

Edit `.env` (gunakan VSCode / Notepad++). Field yang relevan untuk Windows + Podman:

| Field | Nilai Windows | Catatan |
| --- | --- | --- |
| `HOST_IP` | kosong (untuk akses lokal) atau LAN-IP Windows (mis. `192.168.1.50`) | Untuk akses dari HP/device lain |
| `DATABASE_URL_ZAKAT` | `postgresql://transaction:solusi@host.containers.internal:5432/mziss_laz` | Default sudah benar |
| `DATABASE_URL_WAKAF` | `postgresql://transaction:solusi@host.containers.internal:5432/mziss_wakaf` | Default sudah benar |
| `SESSION_SECRET_ZAKAT` | string random panjang | Ganti dari default untuk production-ish |
| `SESSION_SECRET_WAKAF` | string random panjang | Ganti dari default untuk production-ish |

Generate session secret random:

```powershell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

## 10. Menjalankan stack

```powershell
cd D:\workshop\isf-app\infra

# Portal Zakat
podman-compose -f docker-compose.zakat.yml up -d --build
# → http://localhost:5173

# Portal Wakaf (terminal lain atau setelah zakat siap)
podman-compose -f docker-compose.wakaf.yml up -d --build
# → http://localhost:5174
```

Build pertama: 3–8 menit per stack (download `python:3.12-slim`, `node:20-alpine` + install deps). Build berikutnya cepat (cache).

Cek semua container:

```powershell
podman ps --filter "name=isf-"
# → 6 container running (3 zakat + 3 wakaf)
```

## 11. Verifikasi

### 11.1 Health endpoint

```powershell
# Zakat
curl http://localhost:8000/health
curl http://localhost:7000/health

# Wakaf
curl http://localhost:8001/health
curl http://localhost:7001/health
```

Semua harus respons HTTP 200.

### 11.2 Frontend

Buka browser:

- Zakat: <http://localhost:5173>
- Wakaf: <http://localhost:5174>

Login pakai akun demo (sama untuk kedua portal):

- `admin / admin123`
- `finance.a / finance123`
- `finance.b / finance123`

### 11.3 Inspect via Podman Desktop GUI

- **Containers**: lihat 6 container `isf-zakat-*` dan `isf-wakaf-*` semua hijau
- **Logs**: klik nama container → tab Logs
- **Terminal**: shell langsung ke dalam container (klik ikon terminal)

## 12. Auto-start saat boot

Podman machine **tidak** auto-start setelah Windows restart. Solusi:

### Opsi A — Enable di Podman Desktop

Settings → **Preferences** → enable **"Start machine on launch"**.

Lalu taruh shortcut Podman Desktop di startup:

```powershell
$startup = [Environment]::GetFolderPath("Startup")
Copy-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Podman Desktop.lnk" $startup
```

### Opsi B — Task Scheduler (lebih reliable)

Buat task yang auto-start machine + auto-up compose saat user login:

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-WindowStyle Hidden -Command `"podman machine start; cd D:\workshop\isf-app\infra; podman-compose -f docker-compose.zakat.yml up -d; podman-compose -f docker-compose.wakaf.yml up -d`""

$trigger = New-ScheduledTaskTrigger -AtLogOn

Register-ScheduledTask -TaskName "ISF Auto Start" -Action $action -Trigger $trigger -RunLevel Highest
```

### Opsi C — Power settings

Cegah PC sleep/hibernate (penting kalau dipakai sebagai "server" 24/7):

```powershell
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
powercfg /change monitor-timeout-ac 30
```

## 13. Update kode & rebuild

Compose mount source code dari host:

```yaml
volumes:
  - ../apps_zakat/api-python:/app
```

→ **edit kode di Windows langsung ter-reflect di container** (FastAPI `--reload` & Vite HMR aktif).

Kalau ubah dependency (`pyproject.toml` / `package.json`), wajib rebuild:

```powershell
podman-compose -f docker-compose.zakat.yml up -d --build api-python
```

## 14. Stop & teardown

```powershell
# Stop salah satu stack
podman-compose -f docker-compose.zakat.yml down

# Stop + hapus volume (reset session DB SQLite)
podman-compose -f docker-compose.zakat.yml down -v

# Stop Podman machine (free RAM untuk Windows)
podman machine stop

# Hapus machine total (nuclear option — semua image hilang)
podman machine rm podman-machine-default --force
```

## 15. Troubleshooting

### Container tidak bisa connect ke Postgres

**Gejala**: `api-python` log error `connection refused` ke `host.containers.internal:5432`.

**Cek**:

```powershell
# 1. Postgres listen di * dan port 5432
Test-NetConnection -ComputerName localhost -Port 5432

# 2. Firewall allow 5432 dari WSL subnet
Get-NetFirewallRule -DisplayName "*PostgreSQL*"

# 3. Dari dalam container
podman exec -it isf-zakat-api-python python -c "import socket; print(socket.gethostbyname('host.containers.internal'))"
```

Solusi: pastikan langkah 8.3–8.4 sudah benar.

### Port sudah dipakai

**Gejala**: `bind: address already in use`.

```powershell
# Cari proses yang pakai port
Get-NetTCPConnection -LocalPort 5173 | Select-Object OwningProcess
Get-Process -Id <PID>
```

Stop proses tersebut, atau ubah port mapping di compose.

### `podman machine` lambat / tidak respons

Penyebab umum: WSL2 belum di-restart setelah ubah `.wslconfig`.

```powershell
podman machine stop
wsl --shutdown
podman machine start
```

### Hot reload Vue tidak jalan

Compose sudah set `CHOKIDAR_USEPOLLING: "true"` untuk file watcher lintas filesystem. Kalau masih tidak reload:

- Pastikan kode diedit di host Windows (jalur `D:\workshop\isf-app\...`), bukan di dalam container
- Restart container web: `podman restart isf-zakat-web-vue`

### Build lambat / file IO terasa lag

Penyebab: project di NTFS Windows (`D:\`) di-mount ke ext4 WSL2 — penalty IO 5–10×.

Mitigasi:

- Untuk dev: sesekali clone repo ke dalam WSL filesystem (`\\wsl$\podman-machine-default\home\...`) untuk pengetikan/build paling cepat. Tradeoff: tidak bisa diedit pakai Explorer Windows langsung.
- Untuk pemakaian sebagai "server" jangka panjang: biarkan di `D:\` — sekali build, jarang rebuild.

### `podman-compose` error `KeyError: 'env_file'`

Versi `podman-compose` < 1.0.3 tidak support format `env_file: { path:, required: }` yang dipakai compose ini.

```powershell
pip install --upgrade "podman-compose>=1.0.3"
```

### Podman Desktop tidak detect machine

Lewat GUI klik tombol refresh, atau:

```powershell
podman machine list
podman system connection list
podman system connection default podman-machine-default
```

### Reset total

Kalau setup hancur dan mau ulang dari awal:

```powershell
podman-compose -f docker-compose.zakat.yml down -v
podman-compose -f docker-compose.wakaf.yml down -v
podman machine stop
podman machine rm podman-machine-default --force
podman machine init
podman machine start
```

`.wslconfig`, Postgres native, dan `.env` tidak terhapus — cuma machine + image yang fresh.

# Specs: Sistem Otorisasi Terpusat — Modul Keuangan

**Tanggal:** 2026-06-08
**Event:** Desain fitur baru — sistem otorisasi multi-level generic untuk modul keuangan

---

## ==== HASIL ANALISIS DESAIN ====

**FITUR:** Sistem Otorisasi Terpusat  
**MODUL:** `keuangan` (extensible ke modul lain ke depannya)  
**SCOPE AWAL:** Penghimpunan Dana + Penyaluran Dana + Upload Penghimpunan + Master COA + Master Kas + Master Bank

> **Catatan Upload Penghimpunan:** Upload saat ini sudah punya pola approve tersendiri (`keuangan.upload.penghimpunan.approve`). Implementasi ini menggantikan pola tersebut — upload diintegrasikan ke `otorisasi.submission` dengan `entity_type='upload_penghimpunan'`. Menu lama `keuangan.upload.penghimpunan.approve` tidak dipakai lagi.

---

## KONSEP UTAMA

Sebelum diotorisasi, **data tidak masuk ke tabel utama**. Semua input disimpan di
`otorisasi.submission` (staging generic dengan JSONB payload). Tabel utama hanya diisi
setelah submission terotorisasi penuh.

Data yang belum terotorisasi tetap bisa ditampilkan di halaman list masing-masing
melalui endpoint `GET /api/otorisasi/my-submissions/?entity_type=...`.

---

## STATUS MACHINE

```
[DRAFT]
  │  inputer klik "Submit untuk Otorisasi"
  ▼
[PENDING]  level_current = 1
  │  otorisator L1 approve
  ├─ level_required = 1 → [AUTHORIZED] → dispatch ke service → buat record di tabel utama
  └─ level_required > 1 → level_current naik → tunggu otorisator L berikutnya
  │  otorisator menolak (kapanpun level)
  ▼
[REJECTED]  + catatan wajib
  │  inputer revisi payload → submit ulang
  ├─ → kembali [DRAFT] → bisa submit ulang
  └─ inputer hapus → submission dihapus
```

Status valid: `DRAFT` | `PENDING` | `AUTHORIZED` | `REJECTED`

---

## SKEMA DB

**Schema:** `otorisasi` (di database business: `mziss_laz` / `mziss_wakaf`)

### `otorisasi.submission`

| Kolom | Tipe | Keterangan |
|---|---|---|
| `id` | SERIAL PK | |
| `entity_type` | VARCHAR(50) | `'penghimpunan'`, `'penyaluran'`, `'upload_penghimpunan'`, `'coa'`, `'kas'`, `'bank'` |
| `module` | VARCHAR(50) | `'keuangan'`, `'personalia'`, ... |
| `branch_code` | VARCHAR(10) | Cabang inputer |
| `payload` | JSONB NOT NULL | Seluruh data input apa adanya |
| `status` | VARCHAR(20) | DEFAULT `'DRAFT'` |
| `level_current` | INTEGER | DEFAULT `0` (0=draft, 1=menunggu L1, dst) |
| `submitted_by` | VARCHAR(50) | user_id inputer |
| `submitted_at` | TIMESTAMP | NULL saat DRAFT, diisi saat submit |
| `result_entity_id` | INTEGER | Diisi setelah AUTHORIZED → ID di tabel utama |
| `created_at` | TIMESTAMP | DEFAULT NOW() |
| `updated_at` | TIMESTAMP | DEFAULT NOW() |

### `otorisasi.approval_log`

| Kolom | Tipe | Keterangan |
|---|---|---|
| `id` | SERIAL PK | |
| `submission_id` | INTEGER FK | → `otorisasi.submission.id` |
| `level` | INTEGER | Level otorisasi (1, 2, ...) |
| `authorizer_id` | VARCHAR(50) | user_id otorisator |
| `status` | VARCHAR(20) | `'APPROVED'` \| `'REJECTED'` |
| `notes` | TEXT | Wajib isi jika REJECTED, opsional jika APPROVED |
| `logged_at` | TIMESTAMP | DEFAULT NOW() |

### `otorisasi.entity_config`

| Kolom | Tipe | Keterangan |
|---|---|---|
| `entity_type` | VARCHAR(50) PK | |
| `module` | VARCHAR(50) | |
| `level_required` | INTEGER | DEFAULT `1` |
| `label` | VARCHAR(100) | Label tampilan di UI |
| `menu_key` | VARCHAR(100) | Menu key otorisasi modul ini |

### Seed Data `entity_config` — Modul Keuangan

```sql
INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('penghimpunan',       'keuangan', 1, 'Penghimpunan Dana',   'keuangan.monitoring.otorisasi'),
  ('penyaluran',         'keuangan', 1, 'Penyaluran Dana',     'keuangan.monitoring.otorisasi'),
  ('upload_penghimpunan','keuangan', 1, 'Upload Penghimpunan', 'keuangan.monitoring.otorisasi'),
  ('coa',                'keuangan', 1, 'Master COA',          'keuangan.monitoring.otorisasi'),
  ('kas',                'keuangan', 1, 'Master Kas',          'keuangan.monitoring.otorisasi'),
  ('bank',               'keuangan', 1, 'Master Bank',         'keuangan.monitoring.otorisasi');
```

---

## AKSES

| Menu Key | Role (default) | Keterangan |
|---|---|---|
| `keuangan.monitoring.otorisasi` | `SPVDIST`, `KEU`, `MANAJER` | Otorisator — lihat pending + approve/reject |
| `keuangan.transaksi.penghimpunan` | `ACC` | Inputer — submit submission penghimpunan |
| `keuangan.transaksi.penyaluran` | `DIST`, `SPVDIST` | Inputer — submit submission penyaluran |

Branch access: `branch_access='T'` hanya lihat submission cabang sendiri.
`branch_access='S'` lihat semua cabang (untuk membantu otorisasi lintas cabang).

---

## API DESIGN

### api-python (internal, tanpa auth)

| Method | Path | Query Params | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/submission/` | `?user_id=&branch_code=` | Simpan DRAFT baru |
| `GET` | `/api/otorisasi/submission/{id}` | | Detail submission + approval_log |
| `PUT` | `/api/otorisasi/submission/{id}` | `?user_id=` | Update payload (DRAFT/REJECTED only) |
| `DELETE` | `/api/otorisasi/submission/{id}` | `?user_id=` | Hapus (DRAFT/REJECTED only) |
| `POST` | `/api/otorisasi/submission/{id}/submit` | `?user_id=` | DRAFT → PENDING |
| `GET` | `/api/otorisasi/submissions/` | `?module=&entity_type=&status=&submitted_by=&branch=&page=&page_size=` | List submissions |
| `POST` | `/api/otorisasi/submission/{id}/approve` | `?authorizer_id=&branch_access=` | Approve satu level |
| `POST` | `/api/otorisasi/submission/{id}/reject` | `?authorizer_id=` | Tolak + catatan |
| `POST` | `/api/otorisasi/bulk/approve` | `?authorizer_id=&branch_access=` | Bulk approve |
| `POST` | `/api/otorisasi/bulk/reject` | `?authorizer_id=` | Bulk reject |
| `GET` | `/api/otorisasi/entity-config/` | `?module=` | List entity_config |

### bff-api (public)

| Method | Path | Menu Key | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/submission/` | entity's menu_key | Simpan DRAFT — menu_key dari `entity_type` via entity_config |
| `GET` | `/api/otorisasi/submission/{id}` | entity's atau monitoring | Detail |
| `PUT` | `/api/otorisasi/submission/{id}` | entity's menu_key | Update DRAFT/REJECTED |
| `DELETE` | `/api/otorisasi/submission/{id}` | entity's menu_key | Hapus |
| `POST` | `/api/otorisasi/submission/{id}/submit` | entity's menu_key | Submit untuk otorisasi |
| `GET` | `/api/otorisasi/my-submissions/` | entity's menu_key | Submission milik inputer sendiri — `?entity_type=` |
| `GET` | `/api/otorisasi/pending/` | `keuangan.monitoring.otorisasi` | List PENDING untuk otorisator (branch otomatis) |
| `POST` | `/api/otorisasi/submission/{id}/approve` | `keuangan.monitoring.otorisasi` | Approve |
| `POST` | `/api/otorisasi/submission/{id}/reject` | `keuangan.monitoring.otorisasi` | Reject |
| `POST` | `/api/otorisasi/bulk/approve` | `keuangan.monitoring.otorisasi` | Bulk approve |
| `POST` | `/api/otorisasi/bulk/reject` | `keuangan.monitoring.otorisasi` | Bulk reject |

### Payload Shape — POST /api/otorisasi/submission/

```json
{
  "entity_type": "penghimpunan",
  "module": "keuangan",
  "payload": {
    "actual_date": "2026-06-08",
    "payment_type": "C",
    "description": "...",
    "items": [
      { "product_id": 1, "amount": 500000, "fund_entity": 2 }
    ]
  }
}
```

Payload per entity_type mengikuti schema yang sudah ada di masing-masing service.

---

## UI FLOW — INPUTER

**Halaman list (PenghimpunanDanaPage, PenyaluranDanaPage, CoaPage, KasPage, BankPage):**

- Fetch 2 sumber secara paralel:
  1. `GET /api/otorisasi/my-submissions/?entity_type=penghimpunan` → DRAFT/PENDING/REJECTED
  2. `GET /api/penghimpunan/` → data AUTHORIZED dari tabel utama
- Gabung dan tampilkan dengan kolom status badge:
  - `DRAFT` (abu-abu) → tombol [Edit] [Submit]
  - `PENDING` (kuning) → tombol [Lihat] saja, tidak bisa diedit
  - `REJECTED` (merah) → tombol [Revisi] [Hapus] + tooltip catatan penolakan
  - `AUTHORIZED` (hijau) → tampilan normal tanpa aksi otorisasi

**Halaman form (PenghimpunanDanaFormPage, dll):**

- Tombol simpan → `POST /api/otorisasi/submission/` (bukan langsung ke endpoint transaksi)
- Setelah berhasil → redirect ke list dengan status DRAFT
- Tombol "Submit untuk Otorisasi" ada di list page (bukan form)

**Edit submission REJECTED:**

- Klik [Revisi] → buka form yang sama, payload di-preload dari `submission.payload`
- Simpan → `PUT /api/otorisasi/submission/{id}` → status kembali `DRAFT`
- Inputer bisa submit ulang dari list

---

## UI FLOW — OTORISATOR

**Halaman OtorisasiPage.vue** (route: `/keuangan/monitoring/otorisasi`):

```
┌─────────────────────────────────────────────────────────────────┐
│ TOOLBAR  [Filter: Semua | Penghimpunan | Penyaluran | ...]      │
│          [Cabang: dropdown]     [Tanggal: dari–sampai]          │
├─────────────────────────────────────────────────────────────────┤
│ PAGINATION  Showing 1–25 of 48          [< 1 2 >]               │
├─────────────────────────────────────────────────────────────────┤
│ ☐  Jenis         Inputer    Cabang  Tanggal     Total    Level  │
│ ☐  Penghimpunan  RAIS       001     08-06-2026  500.000  1/1   │
│ ☑  Penyaluran    HADI       002     07-06-2026  250.000  1/2   │
│ ☑  Master COA    RAIS       001     08-06-2026  —        1/1   │
├─────────────────────────────────────────────────────────────────┤
│ [Otorisasi (2)]  [Tolak (2)]         ← muncul saat ada pilihan  │
└─────────────────────────────────────────────────────────────────┘
```

- Klik baris → `SubmissionDetailDrawer.vue` slide dari kanan
- Drawer render payload sesuai `entity_type` (read-only view)
- Drawer menampilkan riwayat approval_log di bagian bawah
- Tombol [Otorisasi] [Tolak] di dalam drawer (aksi satuan)
- Bulk: checklist multiple → [Otorisasi (N)] [Tolak (N)] muncul di toolbar bawah

**Sidebar keuangan:**

```
Keuangan
  └─ Monitoring dan Kontrol
       └─ Otorisasi     [badge: jumlah PENDING]
       └─ Historikal    ← future, tidak diimplementasi sekarang
  └─ Transaksi
       └─ Penghimpunan Dana
       └─ Penyaluran Dana
  └─ Master
       └─ COA  │  Kas  │  Bank
  └─ Laporan
```

---

## DISPATCH REGISTRY (api-python)

```python
# apps_zakat/api-python/app/modules/otorisasi/service.py

ENTITY_DISPATCHERS = {
    'penghimpunan':        penghimpunan_service.create_from_payload,
    'penyaluran':          penyaluran_service.create_from_payload,
    'upload_penghimpunan': upload_penghimpunan_service.create_from_payload,
    'coa':                 coa_service.create_from_payload,
    'kas':                 kas_service.create_from_payload,
    'bank':                bank_service.create_from_payload,
    # tambah modul baru = tambah satu baris
}

async def _dispatch_authorized(submission, db):
    dispatcher = ENTITY_DISPATCHERS.get(submission.entity_type)
    if dispatcher:
        result_id = await dispatcher(submission.payload, db)
        submission.result_entity_id = result_id
        submission.status = 'AUTHORIZED'
```

---

## MENU KEYS BARU

| Key | Label | Section |
|---|---|---|
| `keuangan.monitoring.otorisasi` | Otorisasi | Monitoring dan Kontrol |

Ditambahkan ke `apps_zakat/web-vue/src/lib/menu/registry.ts`.

---

## HANDOFF KE AGENT LAIN

```
→ isf-agent-db:
  Buat schema otorisasi + 3 tabel migration:
    infra/db/migrations/otorisasi/001_create_schema.sql
    infra/db/migrations/otorisasi/002_create_submission.sql
    infra/db/migrations/otorisasi/003_create_approval_log.sql
    infra/db/migrations/otorisasi/004_create_entity_config.sql
  Apply ke mziss_laz (dan mziss_wakaf jika multi-portal)

→ isf-agent-seed:
  MENU_KEY: keuangan.monitoring.otorisasi
  LABEL: Otorisasi
  ROLES: SPVDIST, KEU, MANAJER
  FILE: infra/db/migrations/seed/seed-menu-otorisasi.sql
  + seed entity_config 6 rows ke otorisasi.entity_config

→ isf-agent-python:
  MODULE: otorisasi (cross-module, bukan di transaction/)
  PATH: apps_zakat/api-python/app/modules/otorisasi/
  FILES: schema.py, repo.py, service.py, router.py
  DISPATCH REGISTRY: penghimpunan, penyaluran, upload_penghimpunan, coa, kas, bank
  Setiap service target perlu fungsi create_from_payload(payload, db)

→ isf-agent-bff:
  ROUTER: apps_zakat/bff-api/app/routers/otorisasi.py
  PREFIX: /api/otorisasi
  MENU KEY GATING:
    - submission CRUD: entity's menu_key (resolve dari entity_config)
    - approve/reject/pending: keuangan.monitoring.otorisasi

→ isf-agent-ui:
  PAGE BARU:
    pages/keuangan/OtorisasiPage.vue
    components/otorisasi/SubmissionDetailDrawer.vue
    components/otorisasi/StatusBadge.vue
  ROUTE: /keuangan/monitoring/otorisasi
  MENU KEY: keuangan.monitoring.otorisasi
  SIDEBAR: tambah section "Monitoring dan Kontrol" di AppSidebar.vue
  MODIFIKASI:
    - PenghimpunanDanaPage.vue → fetch my-submissions + gabung dengan list utama
    - PenghimpunanDanaFormPage.vue → save ke /api/otorisasi/submission/ bukan /api/penghimpunan/
    - PenyaluranDanaPage.vue → idem
    - PenyaluranDanaFormPage.vue → idem
    - UploadPenghimpunanPage.vue → idem
    - CoaPage.vue, KasPage.vue, BankPage.vue → idem
```

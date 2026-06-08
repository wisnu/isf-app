# Plan: Implementasi Sistem Otorisasi Terpusat — Modul Keuangan

**Tanggal:** 2026-06-08  
**Berdasarkan Specs:** `docs/todos/2026-06-08-002-otorisasi/specs.md`  
**Status:** Pending

---

## Ringkasan

Sistem otorisasi terpusat generic berbasis staging table (`otorisasi.submission` + JSONB payload).
Data input tidak masuk tabel utama sebelum terotorisasi. Mendukung multi-level (default single),
multi-entity-type, dan multi-modul. Scope awal: 6 entity type modul keuangan.

---

## Checklist Progress

### Layer 1 — Database

| # | File | Aksi | Status |
|---|------|------|--------|
| 1 | `infra/db/migrations/otorisasi/001_create_schema.sql` | CREATE | ⏳ Pending |
| 2 | `infra/db/migrations/otorisasi/002_create_submission.sql` | CREATE | ⏳ Pending |
| 3 | `infra/db/migrations/otorisasi/003_create_approval_log.sql` | CREATE | ⏳ Pending |
| 4 | `infra/db/migrations/otorisasi/004_create_entity_config.sql` | CREATE | ⏳ Pending |

### Layer 2 — Seed

| # | File | Aksi | Status |
|---|------|------|--------|
| 5 | `infra/db/migrations/seed/seed-otorisasi-entity-config.sql` | CREATE | ⏳ Pending |
| 6 | `infra/db/migrations/seed/seed-menu-otorisasi.sql` | CREATE | ⏳ Pending |

### Layer 3 — api-python

| # | File | Aksi | Status |
|---|------|------|--------|
| 7 | `apps_zakat/api-python/app/modules/otorisasi/__init__.py` | CREATE | ⏳ Pending |
| 8 | `apps_zakat/api-python/app/modules/otorisasi/schema.py` | CREATE | ⏳ Pending |
| 9 | `apps_zakat/api-python/app/modules/otorisasi/repo.py` | CREATE | ⏳ Pending |
| 10 | `apps_zakat/api-python/app/modules/otorisasi/service.py` | CREATE | ⏳ Pending |
| 11 | `apps_zakat/api-python/app/modules/otorisasi/router.py` | CREATE | ⏳ Pending |
| 12 | `apps_zakat/api-python/app/main.py` | MODIFY | ⏳ Pending — register otorisasi router |
| 13 | `apps_zakat/api-python/app/modules/transaction/penghimpunan_service.py` | MODIFY | ⏳ Pending — tambah `create_from_payload()` |
| 14 | `apps_zakat/api-python/app/modules/transaction/penyaluran_service.py` | MODIFY | ⏳ Pending — tambah `create_from_payload()` |

### Layer 4 — bff-api

| # | File | Aksi | Status |
|---|------|------|--------|
| 15 | `apps_zakat/bff-api/app/routers/otorisasi.py` | CREATE | ⏳ Pending |
| 16 | `apps_zakat/bff-api/app/main.py` | MODIFY | ⏳ Pending — register otorisasi_router |

### Layer 5 — web-vue (komponen baru)

| # | File | Aksi | Status |
|---|------|------|--------|
| 17 | `apps_zakat/web-vue/src/lib/menu/registry.ts` | MODIFY | ⏳ Pending — tambah `keuangan.monitoring.otorisasi` |
| 18 | `apps_zakat/web-vue/src/router/index.ts` | MODIFY | ⏳ Pending — route `/keuangan/monitoring/otorisasi` |
| 19 | `apps_zakat/web-vue/src/components/AppSidebar.vue` | MODIFY | ⏳ Pending — section Monitoring dan Kontrol |
| 20 | `apps_zakat/web-vue/src/pages/keuangan/OtorisasiPage.vue` | CREATE | ⏳ Pending |
| 21 | `apps_zakat/web-vue/src/components/otorisasi/SubmissionDetailDrawer.vue` | CREATE | ⏳ Pending |
| 22 | `apps_zakat/web-vue/src/components/otorisasi/StatusBadge.vue` | CREATE | ⏳ Pending |

### Layer 6 — web-vue (modifikasi halaman existing)

| # | File | Aksi | Status |
|---|------|------|--------|
| 23 | `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaPage.vue` | MODIFY | ⏳ Pending — gabung my-submissions + badge status |
| 24 | `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue` | MODIFY | ⏳ Pending — save → /api/otorisasi/submission/ |
| 25 | `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue` | MODIFY | ⏳ Pending — gabung my-submissions + badge status |
| 26 | `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue` | MODIFY | ⏳ Pending — save → /api/otorisasi/submission/ |
| 27 | `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue` | MODIFY | ⏳ Pending — submit → otorisasi |
| 28 | `apps_zakat/web-vue/src/pages/keuangan/CoaPage.vue` | MODIFY | ⏳ Pending — gabung my-submissions + badge status |
| 29 | `apps_zakat/web-vue/src/pages/keuangan/KasPage.vue` | MODIFY | ⏳ Pending — gabung my-submissions + badge status |
| 30 | `apps_zakat/web-vue/src/pages/keuangan/BankPage.vue` | MODIFY | ⏳ Pending — gabung my-submissions + badge status |

---

## Langkah Manual Yang Belum Dilakukan

| # | Langkah | Status |
|---|---------|--------|
| A | Apply migration DB ke `mziss_laz` (4 SQL files) | ⏳ Pending |
| B | Apply seed entity_config ke `mziss_laz` | ⏳ Pending |
| C | Apply seed menu otorisasi ke `isf_auth_zakat` | ⏳ Pending |
| D | User otorisator logout + login ulang agar menu muncul | ⏳ Pending |
| E | Restart container api-python + bff-api + web-vue | ⏳ Pending |
| F | Test E2E (lihat section Test E2E di bawah) | ⏳ Pending |

### Apply Migration DB

```bash
for f in 001 002 003 004; do
  PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
    -f infra/db/migrations/otorisasi/${f}_*.sql
done
```

### Apply Seed

```bash
# Entity config
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -f infra/db/migrations/seed/seed-otorisasi-entity-config.sql

# Menu otorisasi
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -f infra/db/migrations/seed/seed-menu-otorisasi.sql
```

---

## Arsitektur Alur Data

```
=== ALUR INPUTER ===

User isi PenghimpunanDanaFormPage.vue
  ↓ klik Simpan
  ↓ POST /api/otorisasi/submission/ { entity_type: 'penghimpunan', payload: {...} }
bff-api/routers/otorisasi.py
  → require_menu('keuangan.transaksi.penghimpunan')  ← menu key dari entity_config
  → _session() untuk user_id + branch_code
  → POST api-python /api/otorisasi/submission/?user_id=&branch_code=
api-python/modules/otorisasi/service.py
  → INSERT otorisasi.submission (status='DRAFT', level_current=0)
  ← { submission_id: 42 }

User klik [Submit untuk Otorisasi] di list page
  ↓ POST /api/otorisasi/submission/42/submit
api-python
  → UPDATE submission SET status='PENDING', level_current=1, submitted_at=NOW()
  ← { status: 'PENDING' }

=== ALUR OTORISATOR ===

OtorisasiPage.vue load
  ↓ GET /api/otorisasi/pending/?module=keuangan
bff-api
  → require_menu('keuangan.monitoring.otorisasi')
  → _session() → branch_code + branch_access
  → GET api-python /api/otorisasi/submissions/?module=keuangan&status=PENDING&branch=...
api-python
  → query otorisasi.submission JOIN entity_config
  → filter branch_code (jika branch_access='T' hanya cabang sendiri)
  ← { data: [...], pagination: {...} }

Otorisator klik [Otorisasi] (satuan atau bulk)
  ↓ POST /api/otorisasi/submission/42/approve { notes: '...' }
api-python/otorisasi/service.py → approve_submission()
  → INSERT approval_log (level=1, status='APPROVED')
  → Cek: level_current >= level_required?
    → YA (single level): _dispatch_authorized(submission)
      → ENTITY_DISPATCHERS['penghimpunan'](payload, db)
        → penghimpunan_service.create_from_payload()
          → (alur lama: batch, INSERT transaction, journal, dll)
          ← result_entity_id
      → UPDATE submission SET status='AUTHORIZED', result_entity_id=X
    → TIDAK (multi level): UPDATE submission SET level_current=level_current+1

Otorisator klik [Tolak]
  ↓ POST /api/otorisasi/submission/42/reject { notes: 'Jumlah tidak sesuai' }
api-python
  → INSERT approval_log (status='REJECTED', notes wajib)
  → UPDATE submission SET status='REJECTED'
  ← { status: 'REJECTED' }

=== ALUR INPUTER SETELAH DITOLAK ===

PenghimpunanDanaPage.vue list → baris REJECTED muncul [Revisi] [Hapus]
  Klik [Revisi]
  ↓ GET /api/otorisasi/submission/42 → payload + catatan penolakan
  Form dibuka dengan payload preload
  ↓ PUT /api/otorisasi/submission/42 { payload: {...updated} }
  → status kembali 'DRAFT'
  Inputer bisa submit ulang
```

---

## Endpoint Kontrak

### api-python (internal)

| Method | Path | Auth | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/submission/` | none | `?user_id=&branch_code=` |
| `GET` | `/api/otorisasi/submission/{id}` | none | detail + approval_log |
| `PUT` | `/api/otorisasi/submission/{id}` | none | `?user_id=` — DRAFT/REJECTED only |
| `DELETE` | `/api/otorisasi/submission/{id}` | none | `?user_id=` — DRAFT/REJECTED only |
| `POST` | `/api/otorisasi/submission/{id}/submit` | none | `?user_id=` |
| `GET` | `/api/otorisasi/submissions/` | none | `?module=&entity_type=&status=&submitted_by=&branch=&page=&page_size=` |
| `POST` | `/api/otorisasi/submission/{id}/approve` | none | `?authorizer_id=&branch_access=` |
| `POST` | `/api/otorisasi/submission/{id}/reject` | none | `?authorizer_id=` + body `{ notes }` |
| `POST` | `/api/otorisasi/bulk/approve` | none | `?authorizer_id=` + body `{ ids: [...] }` |
| `POST` | `/api/otorisasi/bulk/reject` | none | `?authorizer_id=` + body `{ ids: [...], notes }` |
| `GET` | `/api/otorisasi/entity-config/` | none | `?module=` |

### bff-api (public)

| Method | Path | Menu Key | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/submission/` | entity's key | Resolve dari entity_config |
| `GET` | `/api/otorisasi/submission/{id}` | entity's atau monitoring | |
| `PUT` | `/api/otorisasi/submission/{id}` | entity's key | |
| `DELETE` | `/api/otorisasi/submission/{id}` | entity's key | |
| `POST` | `/api/otorisasi/submission/{id}/submit` | entity's key | |
| `GET` | `/api/otorisasi/my-submissions/` | entity's key | `?entity_type=` |
| `GET` | `/api/otorisasi/pending/` | `keuangan.monitoring.otorisasi` | list PENDING otorisator |
| `POST` | `/api/otorisasi/submission/{id}/approve` | `keuangan.monitoring.otorisasi` | |
| `POST` | `/api/otorisasi/submission/{id}/reject` | `keuangan.monitoring.otorisasi` | |
| `POST` | `/api/otorisasi/bulk/approve` | `keuangan.monitoring.otorisasi` | |
| `POST` | `/api/otorisasi/bulk/reject` | `keuangan.monitoring.otorisasi` | |

---

## Test E2E

```bash
# Login sebagai RAIS (ACC role, inputer)
TOKEN_RAIS=$(curl -s -c cookies_rais.txt http://localhost:7000/api/auth/login \
  -d '{"username":"RAIS","password":"test1234"}' \
  -H 'Content-Type: application/json' | jq -r '.data.token')

# Login sebagai HADI (SPVDIST role, otorisator)
TOKEN_HADI=$(curl -s -c cookies_hadi.txt http://localhost:7000/api/auth/login \
  -d '{"username":"HADI","password":"test1234"}' \
  -H 'Content-Type: application/json' | jq -r '.data.token')

# 1. Inputer buat DRAFT penghimpunan
SUBMISSION_ID=$(curl -s -b cookies_rais.txt -X POST http://localhost:7000/api/otorisasi/submission/ \
  -H 'Content-Type: application/json' \
  -d '{
    "entity_type": "penghimpunan",
    "module": "keuangan",
    "payload": {
      "actual_date": "2026-06-08",
      "payment_type": "C",
      "description": "Test otorisasi",
      "rate": 1.0,
      "currency_code": "IDR",
      "product_branch_code": "001",
      "items": [{ "product_id": 1, "account_no": "1101001001", "amount": 100000, "fund_entity": 2, "percentage_of_amil": 0 }]
    }
  }' | jq -r '.data.id')

echo "Submission ID: $SUBMISSION_ID"

# 2. Cek status DRAFT
curl -s -b cookies_rais.txt "http://localhost:7000/api/otorisasi/submission/$SUBMISSION_ID" | jq '.data.status'

# 3. Submit untuk otorisasi
curl -s -b cookies_rais.txt -X POST "http://localhost:7000/api/otorisasi/submission/$SUBMISSION_ID/submit" | jq '.data.status'

# 4. Otorisator lihat pending
curl -s -b cookies_hadi.txt 'http://localhost:7000/api/otorisasi/pending/?module=keuangan' | jq '.data | length'

# 5. Otorisator approve
curl -s -b cookies_hadi.txt -X POST "http://localhost:7000/api/otorisasi/submission/$SUBMISSION_ID/approve" \
  -H 'Content-Type: application/json' \
  -d '{"notes": "OK"}' | jq '.data.status'
# Expected: "AUTHORIZED"

# 6. Cek result_entity_id terisi (record dibuat di tabel utama)
curl -s -b cookies_rais.txt "http://localhost:7000/api/otorisasi/submission/$SUBMISSION_ID" | jq '.data.result_entity_id'

# 7. Test tolak — buat submission baru, submit, lalu tolak
SUBMISSION_ID2=$(curl -s -b cookies_rais.txt -X POST http://localhost:7000/api/otorisasi/submission/ \
  -H 'Content-Type: application/json' \
  -d '{"entity_type":"penghimpunan","module":"keuangan","payload":{"actual_date":"2026-06-08","payment_type":"C","description":"Test tolak","rate":1.0,"currency_code":"IDR","product_branch_code":"001","items":[{"product_id":1,"account_no":"1101001001","amount":50000,"fund_entity":2,"percentage_of_amil":0}]}}' \
  | jq -r '.data.id')

curl -s -b cookies_rais.txt -X POST "http://localhost:7000/api/otorisasi/submission/$SUBMISSION_ID2/submit"

curl -s -b cookies_hadi.txt -X POST "http://localhost:7000/api/otorisasi/submission/$SUBMISSION_ID2/reject" \
  -H 'Content-Type: application/json' \
  -d '{"notes": "Jumlah tidak sesuai SOP"}' | jq '.data.status'
# Expected: "REJECTED"

# 8. Test bulk approve
curl -s -b cookies_hadi.txt -X POST "http://localhost:7000/api/otorisasi/bulk/approve" \
  -H 'Content-Type: application/json' \
  -d '{"ids": [1, 2, 3]}' | jq '.'
```

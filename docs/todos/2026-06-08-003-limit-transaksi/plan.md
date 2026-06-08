# Plan: Implementasi Limit Transaksi Per User

**Tanggal:** 2026-06-08  
**Berdasarkan Specs:** `docs/todos/2026-06-08-003-limit-transaksi/specs.md`  
**Status:** Pending

---

## Ringkasan

Setiap user memiliki limit transaksi dari `enterprise.limittransaksi`. Transaksi di bawah limit langsung efektif (bypass otorisasi); di atas limit masuk antrian otorisasi seperti biasa. Form input menggunakan satu tombol "Simpan & Submit" — alur DRAFT tidak terlihat user.

---

## Checklist Progress

### Layer 1 — Database

| # | File | Aksi | Status |
|---|------|------|--------|
| 1 | `infra/db/migrations/transaction/add_jenis_limit_to_transactiontype.sql` | CREATE | ⏳ Pending |

### Layer 2 — api-python

| # | File | Aksi | Status |
|---|------|------|--------|
| 2 | `apps_zakat/api-python/app/modules/otorisasi/repo.py` | MODIFY — tambah `get_user_limit()` | ⏳ Pending |
| 3 | `apps_zakat/api-python/app/modules/otorisasi/service.py` | MODIFY — tambah `ENTITY_TRANSACTION_CODE`, `save_and_submit()`, `get_user_limit_for_entity()` | ⏳ Pending |
| 4 | `apps_zakat/api-python/app/modules/otorisasi/router.py` | MODIFY — tambah `POST /save-and-submit/` + `GET /user-limit/` | ⏳ Pending |

### Layer 3 — bff-api

| # | File | Aksi | Status |
|---|------|------|--------|
| 5 | `apps_zakat/bff-api/app/routers/otorisasi.py` | MODIFY — tambah `POST /save-and-submit/` + `GET /user-limit/` | ⏳ Pending |

### Layer 4 — web-vue

| # | File | Aksi | Status |
|---|------|------|--------|
| 6 | `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue` | MODIFY — ganti tombol + fetch limit + saveAndSubmit() | ⏳ Pending |
| 7 | `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue` | MODIFY — ganti tombol + fetch limit + saveAndSubmit() | ⏳ Pending |

---

## Langkah Manual

| # | Langkah | Status |
|---|---------|--------|
| A | Apply migration ke `mziss_laz` | ⏳ Pending |
| B | Set `nilai_limit` untuk user test (RAIS): `UPDATE enterprise.limittransaksi SET nilai_limit = 500000 WHERE id_user = 'RAIS'` | ⏳ Pending |
| C | Test E2E (lihat section di bawah) | ⏳ Pending |

---

## Arsitektur Alur Data

```
=== ALUR BELOW LIMIT (langsung efektif) ===

User isi PenyaluranDanaFormPage → klik "Simpan & Submit"
  ↓ GET /api/otorisasi/user-limit/?entity_type=penyaluran
  ← { nilai_limit: 5000000, has_limit: true }
  (tampil: "Limit Anda: Rp 5.000.000 — akan langsung efektif")

  ↓ POST /api/otorisasi/save-and-submit/ { entity_type, module, payload }
bff-api:
  → require_menu('keuangan.transaksi.penyaluran')
  → POST api-python /api/otorisasi/save-and-submit/?user_id=RAIS&branch_code=001
api-python service.save_and_submit():
  → total = sum(items.amount) = 2.500.000
  → get_user_limit('RAIS', 'DD001') = 5.000.000
  → bypassed = True (2.5jt ≤ 5jt)
  → create_submission() → sub_id = 43
  → dispatcher('penyaluran')(payload) → transaction_id = 9999
  → insert_approval_log(sub_id, 0, 'SYSTEM_AUTO', 'APPROVED', 'Dalam limit')
  → authorize_submission(43, 9999)
  ← { submission_id: 43, status: 'AUTHORIZED', transaction_id: 9999, bypassed_auth: true }

Frontend: toast "Transaksi berhasil — langsung efektif" → redirect ke list

=== ALUR ABOVE LIMIT (perlu otorisasi) ===

User isi form → total = 8.000.000 > limit 5.000.000
  ↓ POST /api/otorisasi/save-and-submit/
api-python:
  → bypassed = False
  → create_submission() → sub_id = 44
  → submit_submission(44) → status = PENDING
  ← { submission_id: 44, status: 'PENDING', transaction_id: null, bypassed_auth: false }

Frontend: toast "Transaksi dikirim — menunggu otorisasi" → redirect ke list
```

---

## Endpoint Kontrak

### api-python (internal)

| Method | Path | Params | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/save-and-submit/` | `?user_id=&branch_code=` | Body: `{ entity_type, module, payload }` |
| `GET` | `/api/otorisasi/user-limit/` | `?user_id=&entity_type=` | Return `{ nilai_limit, has_limit }` |

### bff-api (public)

| Method | Path | Menu Key | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/save-and-submit/` | entity's menu_key | Proxy ke api-python |
| `GET` | `/api/otorisasi/user-limit/` | entity's menu_key | `?entity_type=` |

---

## Test E2E

```bash
# Setup: set limit untuk RAIS
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -c "UPDATE enterprise.limittransaksi SET nilai_limit = 500000 WHERE id_user = 'RAIS'"

# Login sebagai RAIS
curl -s -c /tmp/ck_rais.txt http://localhost:7000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"RAIS","password":"test1234"}' > /dev/null

# 1. Cek limit
curl -s -b /tmp/ck_rais.txt 'http://localhost:7000/api/otorisasi/user-limit/?entity_type=penyaluran' \
  | python3 -m json.tool
# Expected: { nilai_limit: 500000, has_limit: true }

# 2. Test BELOW limit (total 100.000 ≤ 500.000) → harus AUTHORIZED langsung
curl -s -b /tmp/ck_rais.txt -X POST http://localhost:7000/api/otorisasi/save-and-submit/ \
  -H 'Content-Type: application/json' \
  -d '{
    "entity_type": "penyaluran",
    "module": "keuangan",
    "payload": {
      "actual_date": "2026-06-08",
      "payment_type": "C",
      "rate": 1.0,
      "currency_code": "IDR",
      "product_branch_code": "001",
      "items": [{"product_id": 1, "account_no": "Z1BI002.001.IDR", "amount": 100000,
                 "fund_entity": 1, "ashnaf": "F", "description": "Test below limit"}]
    }
  }' | python3 -m json.tool
# Expected: status = "AUTHORIZED", bypassed_auth = true, transaction_id != null

# 3. Test ABOVE limit (total 1.000.000 > 500.000) → harus PENDING
curl -s -b /tmp/ck_rais.txt -X POST http://localhost:7000/api/otorisasi/save-and-submit/ \
  -H 'Content-Type: application/json' \
  -d '{
    "entity_type": "penyaluran",
    "module": "keuangan",
    "payload": {
      "actual_date": "2026-06-08",
      "payment_type": "C",
      "rate": 1.0,
      "currency_code": "IDR",
      "product_branch_code": "001",
      "items": [{"product_id": 1, "account_no": "Z1BI002.001.IDR", "amount": 1000000,
                 "fund_entity": 1, "ashnaf": "F", "description": "Test above limit"}]
    }
  }' | python3 -m json.tool
# Expected: status = "PENDING", bypassed_auth = false, transaction_id = null

# 4. Reset limit ke 0 (kembali default)
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -c "UPDATE enterprise.limittransaksi SET nilai_limit = 0 WHERE id_user = 'RAIS'"
```

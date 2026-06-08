# Plan: Implementasi Transaksi Penghimpunan Dana

**Tanggal:** 2026-06-08  
**Berdasarkan Specs:** `docs/todos/2026-06-08-001-penghimpunan-dana/specs.md`  
**Status:** Done — semua file sudah dibuat/dimodifikasi

---

## Ringkasan

Migrasi fitur input transaksi penghimpunan dana (kas masuk ZIS) dari legacy DAF
ke isf-app web-vue. Fitur ini setara dengan `fFundCollection` di legacy core module,
dengan transaction code `SD001`, accessible oleh role `ACC`.

---

## File Yang Dibuat / Dimodifikasi

## Checklist Progress

| # | File | Aksi | Status |
|---|------|------|--------|
| 1 | `apps_zakat/api-python/.../penghimpunan_schema.py` | CREATE | ✅ Done |
| 2 | `apps_zakat/api-python/.../penghimpunan_repo.py` | CREATE | ✅ Done |
| 3 | `apps_zakat/api-python/.../penghimpunan_service.py` | CREATE | ✅ Done |
| 4 | `apps_zakat/api-python/.../router.py` | MODIFY | ✅ Done — tambah 6 endpoint SD001 |
| 5 | `apps_zakat/bff-api/app/routers/penghimpunan.py` | CREATE | ✅ Done |
| 6 | `apps_zakat/bff-api/app/main.py` | MODIFY | ✅ Done — register penghimpunan_router |
| 7 | `apps_zakat/web-vue/src/lib/menu/registry.ts` | MODIFY | ✅ Done — tambah menu key |
| 8 | `apps_zakat/web-vue/src/router/index.ts` | MODIFY | ✅ Done — 2 route baru |
| 9 | `apps_zakat/web-vue/src/components/AppSidebar.vue` | MODIFY | ✅ Done — tambah ArrowUpCircle + entry |
| 10 | `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaPage.vue` | CREATE | ✅ Done |
| 11 | `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue` | CREATE | ✅ Done |
| 12 | `infra/db/migrations/seed/seed-menu-penghimpunan.sql` | CREATE | ✅ Done |

## Langkah Manual Yang Belum Dilakukan

| # | Langkah | Status |
|---|---------|--------|
| A | Apply seed ke `isf_auth_zakat` — run perintah di bawah | ⏳ Pending |
| B | User ACC logout + login ulang agar menu muncul | ⏳ Pending |
| C | Test E2E (lihat section Test E2E di bawah) | ⏳ Pending |
| D | Deploy/restart container bff-api + api-python + web-vue | ⏳ Pending |

### Apply Seed

```bash
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -f infra/db/migrations/seed/seed-menu-penghimpunan.sql
```

## File yang Dibuat/Dimodifikasi

---

## Arsitektur Alur Data

```
User fills PenghimpunanDanaFormPage.vue
  ↓ POST /api/penghimpunan/
bff-api/routers/penghimpunan.py
  → require_menu('keuangan.transaksi.penghimpunan')
  → _session() untuk user_id + branch_code
  → POST api-python /api/transaction/penghimpunan/
api-python/modules/transaction/router.py
  → penghimpunan_service.create_penghimpunan(req, user_id, branch_code)
    → _get_or_create_batch() [desc='Penghimpunan Dana']
    → _resolve_payment() [K/C/B/A → rekening]
    → INSERT transaction (transactioncode='SD001')
    → INSERT journal + journalblock (journal_type='SD001')
    → per item: INSERT transactionitem (mutationtype='C') + accounttransactionitem (accounttitype='D')
    → INSERT payment item (transactiontype='D')
    → UPDATE financialaccount SET balance = balance + amount (semua akun)
    → INSERT transhistoryofchanges
  ← { transaction_id, transaction_no: 'KM-2026-001-KAS-0000001' }
```

---

## Perbedaan Kunci vs Penyaluran Dana (DD001)

| Aspek | Penyaluran (DD001) | Penghimpunan (SD001) |
|---|---|---|
| Transaction code | `DD001` | `SD001` |
| Trans number prefix | `KK-` (Kas Keluar) | `KM-` (Kas Masuk) |
| Journal type | `DD001` | `SD001` |
| Batch description | `'Penyaluran Dana'` | `'Penghimpunan Dana'` |
| Product items mutation | `'D'` (debit) | `'C'` (credit) |
| Payment item mutation | `'C'` (credit) | `'D'` (debit) |
| AccounttiType | `'Z'` (penyaluran) | `'D'` (penghimpunan) |
| Balance update | `balance - amount` | `balance + amount` |
| Journal product | `amount_debit` | `amount_credit` |
| Journal payment | `amount_credit` | `amount_debit` |
| Donor field | Opsional (donorid) | Opsional (donorid + donorno + donorname) |
| Ashnaf | Required for Zakat items | Tidak ada |
| Fund account source | `fund_account_no` (wajib) | Tidak ada — product account IS fund account |

---

## Endpoint Kontrak

### api-python (internal)

| Method | Path | Auth | Keterangan |
|---|---|---|---|
| GET | `/api/transaction/penghimpunan/lookup/rekening` | none | ?type=bank\|petty\|cabang&branch= |
| GET | `/api/transaction/penghimpunan/lookup/produk` | none | ?branch_code=&currency= |
| GET | `/api/transaction/penghimpunan/lookup/donor` | none | ?q=&branch= |
| GET | `/api/transaction/penghimpunan/` | none | ?begin=&end=&page=&page_size=&search=&branch= |
| GET | `/api/transaction/penghimpunan/{id}` | none | detail transaksi |
| POST | `/api/transaction/penghimpunan/` | none | ?user_id=&branch_code= |

### bff-api (public)

| Method | Path | Menu Key | Keterangan |
|---|---|---|---|
| GET | `/api/penghimpunan/lookup/rekening` | `keuangan.transaksi.penghimpunan` | proxy + branch gate |
| GET | `/api/penghimpunan/lookup/produk` | `keuangan.transaksi.penghimpunan` | proxy + branch |
| GET | `/api/penghimpunan/lookup/donor` | `keuangan.transaksi.penghimpunan` | proxy |
| GET | `/api/penghimpunan/` | `keuangan.transaksi.penghimpunan` | list dengan pagination |
| GET | `/api/penghimpunan/{id}` | `keuangan.transaksi.penghimpunan` | detail |
| POST | `/api/penghimpunan/` | `keuangan.transaksi.penghimpunan` | create |

---

## Seed Command

```bash
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -f infra/db/migrations/seed/seed-menu-penghimpunan.sql
```

Setelah seed: user ACC harus **logout + login ulang** agar menu muncul.

---

## Test E2E

```bash
# Login sebagai RAIS (ACC role, branch 001)
TOKEN=$(curl -s -c cookies.txt http://localhost:7000/api/auth/login \
  -d '{"username":"RAIS","password":"test1234"}' \
  -H 'Content-Type: application/json' | jq -r '.data.token')

# Lookup rekening bank
curl -s -b cookies.txt 'http://localhost:7000/api/penghimpunan/lookup/rekening?type=bank'

# Lookup produk
curl -s -b cookies.txt 'http://localhost:7000/api/penghimpunan/lookup/produk?branch_code=001'

# Create penghimpunan
curl -s -b cookies.txt -X POST http://localhost:7000/api/penghimpunan/ \
  -H 'Content-Type: application/json' \
  -d '{
    "actual_date": "2026-06-08",
    "description": "Penerimaan zakat test",
    "payment_type": "C",
    "rate": 1.0,
    "currency_code": "IDR",
    "product_branch_code": "001",
    "items": [
      { "product_id": 1, "account_no": "1101001001",
        "amount": 100000, "description": "Zakat maal",
        "fund_entity": 1, "percentage_of_amil": 12.5 }
    ]
  }'
```

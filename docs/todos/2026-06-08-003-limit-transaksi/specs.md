# Specs: Limit Transaksi Per User — Bypass Otorisasi

**Tanggal:** 2026-06-08  
**Event:** Desain fitur baru — limit transaksi per user untuk penghimpunan & penyaluran

---

## ==== HASIL ANALISIS DESAIN ====

**FITUR:** Limit Transaksi dengan Bypass Otorisasi  
**MODUL:** `keuangan` — input transaksi (penghimpunan + penyaluran)  
**SCOPE:** SD001 (penghimpunan), DD001 (penyaluran), SDULBA (upload penghimpunan)

---

## KONSEP UTAMA

Setiap user memiliki limit transaksi dari `enterprise.limittransaksi`. Saat menyimpan transaksi:

- `nilai_limit = 0` (belum diset) → selalu wajib otorisasi
- `total ≤ nilai_limit` → **langsung efektif** (bypass otorisasi)
- `total > nilai_limit` → masuk antrian otorisasi seperti biasa

Alur form disederhanakan menjadi **satu tombol "Simpan & Submit"** — user tidak perlu tahu tentang status DRAFT. Semua transaksi tetap tercatat di `otorisasi.submission` sebagai audit trail.

---

## STATUS MACHINE (extended)

```
Form → POST /api/otorisasi/save-and-submit/
              ↓ (atomic: save + limit check + decide)
        nilai_limit = 0 OR total > nilai_limit
              → status = PENDING  (masuk antrian otorisasi)
        nilai_limit > 0 AND total ≤ nilai_limit
              → status = AUTHORIZED  (langsung efektif, dispatch ke tabel utama)
```

Kedua path menghasilkan record di `otorisasi.submission` (audit trail lengkap).

---

## SKEMA DB

### Perubahan `transaction.transactiontype`

```sql
ALTER TABLE transaction.transactiontype
  ADD COLUMN jenis_limit VARCHAR(1) DEFAULT NULL;

UPDATE transaction.transactiontype
  SET jenis_limit = 'O'
  WHERE transactioncode IN ('SD001', 'SDMULTI', 'SDULBA', 'DD001');
```

### Tabel referensi (sudah ada, tidak diubah)

**`enterprise.limittransaksi`:**

| Kolom | Tipe | Keterangan |
|---|---|---|
| `id_limit_transaksi` | INTEGER PK | |
| `jenis_limit` | VARCHAR(1) | 'O' = satu limit berlaku semua |
| `nilai_limit` | DOUBLE PRECISION | 0 = belum diset → wajib otorisasi |
| `nilai_limit_akumulasi` | DOUBLE PRECISION | (belum digunakan fase ini) |
| `jumlah_item_limit` | INTEGER | (belum digunakan fase ini) |
| `id_user` | VARCHAR(20) | FK ke user |

### Mapping `entity_type → transactioncode` (konstanta di kode)

```python
ENTITY_TRANSACTION_CODE: dict[str, str] = {
    'penghimpunan':        'SD001',
    'penyaluran':          'DD001',
    'upload_penghimpunan': 'SDULBA',
    # coa, kas, bank → tidak ada mapping → selalu otorisasi
}
```

### Query limit user

```sql
SELECT lt.nilai_limit
  FROM enterprise.limittransaksi lt
  JOIN transaction.transactiontype tt
    ON tt.jenis_limit = lt.jenis_limit
 WHERE lt.id_user = $1
   AND tt.transactioncode = $2
 LIMIT 1
```

---

## API DESIGN

### api-python — endpoint baru

| Method | Path | Query | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/save-and-submit/` | `?user_id=&branch_code=` | Baru: simpan + cek limit + decide |
| `PUT` | `/api/otorisasi/save-and-submit/{id}` | `?user_id=` | Edit REJECTED: update payload + cek limit + decide |
| `GET` | `/api/otorisasi/user-limit/` | `?user_id=&entity_type=` | Fetch limit user untuk display di form |

### bff-api — endpoint baru

| Method | Path | Menu Key | Keterangan |
|---|---|---|---|
| `POST` | `/api/otorisasi/save-and-submit/` | entity's menu_key | Proxy ke api-python |
| `PUT` | `/api/otorisasi/save-and-submit/{id}` | entity's menu_key | Proxy edit mode |
| `GET` | `/api/otorisasi/user-limit/` | entity's menu_key | Proxy, `?entity_type=` |

### Request/Response `save-and-submit`

**POST (baru):**
```json
{
  "entity_type": "penyaluran",
  "module": "keuangan",
  "payload": { "actual_date": "2026-06-08", "payment_type": "B", "items": [...] }
}
```

**PUT (edit REJECTED) body:** `{ "payload": { ...updated fields... } }` — tidak perlu `entity_type`/`module`, diambil dari submission existing.

**Response (sama untuk POST dan PUT):**
```json
{
  "data": {
    "submission_id": 42,
    "status": "AUTHORIZED",
    "transaction_id": 1234,
    "transaction_no": "KK-2026-001-BANK-0000042",
    "bypassed_auth": true
  }
}
```

Jika PENDING: `transaction_id = null`, `transaction_no = null`, `bypassed_auth = false`.

### Response `user-limit`

```json
{
  "data": {
    "entity_type": "penyaluran",
    "nilai_limit": 5000000.0,
    "has_limit": true
  }
}
```

`has_limit = false` jika `nilai_limit = 0` (belum diset).

---

## LOGIKA SERVICE (api-python)

### `otorisasi/repo.py` — fungsi baru

```python
async def get_user_limit(user_id: str, transaction_code: str) -> float:
    """Return nilai_limit user untuk transaction_code. 0.0 jika belum diset."""
    row = await fetch_one(
        """SELECT lt.nilai_limit
           FROM enterprise.limittransaksi lt
           JOIN transaction.transactiontype tt
             ON tt.jenis_limit = lt.jenis_limit
           WHERE lt.id_user = UPPER($1)
             AND tt.transactioncode = $2
           LIMIT 1""",
        user_id, transaction_code,
    )
    return float(row['nilai_limit']) if row and row['nilai_limit'] else 0.0
```

### `otorisasi/service.py` — fungsi baru

```python
ENTITY_TRANSACTION_CODE: dict[str, str] = {
    'penghimpunan':        'SD001',
    'penyaluran':          'DD001',
    'upload_penghimpunan': 'SDULBA',
}

async def save_and_submit(
    entity_type: str, module: str, payload: dict,
    user_id: str, branch_code: str,
) -> dict:
    config = await repo.get_entity_config(entity_type)
    if not config:
        raise HTTPException(400, f"entity_type '{entity_type}' tidak dikenal")

    # Hitung total dari payload items
    total = sum(float(i.get('amount', 0)) for i in payload.get('items', []))

    # Cek limit user
    tx_code = ENTITY_TRANSACTION_CODE.get(entity_type)
    nilai_limit = await repo.get_user_limit(user_id, tx_code) if tx_code else 0.0
    bypassed = nilai_limit > 0 and total <= nilai_limit

    # Simpan submission
    sub_id = await repo.create_submission(entity_type, module, branch_code, payload, user_id)

    if bypassed:
        # Langsung efektif — dispatch ke service transaksi
        dispatcher = _DISPATCHERS.get(entity_type)
        result_entity_id = None
        if dispatcher:
            result_entity_id = await dispatcher(
                payload=dict(payload), user_id=user_id, branch_code=branch_code,
            )
        await repo.insert_approval_log(sub_id, 0, 'SYSTEM_AUTO', 'APPROVED', 'Dalam limit')
        await repo.authorize_submission(sub_id, result_entity_id)
        return {
            'submission_id': sub_id,
            'status': 'AUTHORIZED',
            'transaction_id': result_entity_id,
            'bypassed_auth': True,
        }
    else:
        # Submit untuk otorisasi — set PENDING
        await repo.submit_submission(sub_id)
        return {
            'submission_id': sub_id,
            'status': 'PENDING',
            'transaction_id': None,
            'bypassed_auth': False,
        }
```

**Catatan:** `approval_log` diisi dengan `authorizer_id = 'SYSTEM_AUTO'` dan `level = 0` untuk transaksi yang bypass. Ini memudahkan audit — terlihat jelas mana yang auto-approved dan mana yang diotorisasi manual.

---

## UX FRONTEND

### Form — tombol

Ganti semua tombol save di PenghimpunanDanaFormPage dan PenyaluranDanaFormPage:

**Sebelum:** `[Batal] [Simpan Draft] [Update Draft]`  
**Sesudah:** `[Batal] [Simpan & Submit]`

Untuk edit mode (revisi submission REJECTED): tombol menjadi `[Batal] [Update & Submit]`

### Form — display limit

Tampilkan di bawah total amount, load on mount via `GET /api/otorisasi/user-limit/?entity_type=penyaluran`:

```
┌─────────────────────────────────────────┐
│ Total: Rp 2.500.000                     │
│ Limit Anda: Rp 5.000.000               │
│ ✓ Transaksi ini akan langsung efektif  │
└─────────────────────────────────────────┘
```

atau:

```
┌─────────────────────────────────────────┐
│ Total: Rp 8.000.000                     │
│ Limit Anda: Rp 5.000.000               │
│ ⓘ Transaksi ini memerlukan otorisasi   │
└─────────────────────────────────────────┘
```

atau jika limit belum diset:

```
┌─────────────────────────────────────────┐
│ Total: Rp 2.500.000                     │
│ ⓘ Semua transaksi memerlukan otorisasi  │
└─────────────────────────────────────────┘
```

### Toast setelah submit

| Status response | Toast |
|---|---|
| `AUTHORIZED` | ✅ "Transaksi berhasil — langsung efektif" |
| `PENDING` | ℹ️ "Transaksi dikirim — menunggu otorisasi" |
| Error | ❌ "Gagal menyimpan transaksi" |

Setelah keduanya → redirect ke list page.

---

## HANDOFF KE AGENT LAIN

```
→ isf-agent-db:
  FILE: infra/db/migrations/transaction/add_jenis_limit_to_transactiontype.sql
  ALTER TABLE transaction.transactiontype ADD COLUMN jenis_limit VARCHAR(1) DEFAULT NULL
  UPDATE SET jenis_limit='O' WHERE transactioncode IN ('SD001','SDMULTI','SDULBA','DD001')
  Apply ke mziss_laz

→ isf-agent-python:
  MODULE: otorisasi (di apps_zakat/api-python/app/modules/otorisasi/)
  TAMBAH di repo.py: get_user_limit(user_id, transaction_code) → float
  TAMBAH di service.py: ENTITY_TRANSACTION_CODE + save_and_submit() + get_user_limit_for_entity()
  TAMBAH di router.py: POST /save-and-submit/ + GET /user-limit/

→ isf-agent-bff:
  FILE: apps_zakat/bff-api/app/routers/otorisasi.py
  TAMBAH: POST /save-and-submit/ + GET /user-limit/
  Menu key: entity's menu_key (sama dengan save draft)

→ isf-agent-ui:
  MODIFIKASI: PenghimpunanDanaFormPage.vue + PenyaluranDanaFormPage.vue
  - Ganti save() → saveAndSubmit() → POST /api/otorisasi/save-and-submit/
  - Fetch user limit on mount → tampilkan limit info + indicator
  - Toast berbeda berdasarkan status response
  - Edit mode (REJECTED): tetap pakai PUT + submit, bukan save-and-submit
```

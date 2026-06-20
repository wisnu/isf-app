# Limit Transaksi Per User Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Setiap user memiliki limit transaksi; jika total ≤ limit → langsung efektif (bypass otorisasi), jika > limit atau limit = 0 → masuk antrian otorisasi seperti biasa.

**Architecture:** Endpoint atomik `POST /api/otorisasi/save-and-submit/` (baru) dan `PUT /api/otorisasi/save-and-submit/{id}` (edit REJECTED) menggantikan alur dua-langkah save-then-submit. Limit dibaca dari `enterprise.limittransaksi` via join ke `transaction.transactiontype.jenis_limit`. Form menampilkan limit user dan indikator apakah transaksi akan langsung efektif.

**Tech Stack:** PostgreSQL (asyncpg), FastAPI (api-python + bff-api), Vue 3 + Tailwind (web-vue), `api.post`/`api.put` dari `lib/api/client.ts`.

**Spec:** `docs/todos/2026-06-08-003-limit-transaksi/specs.md`

---

## File Map

| File | Aksi | Tanggung jawab |
|---|---|---|
| `infra/db/migrations/transaction/add_jenis_limit_to_transactiontype.sql` | CREATE | Tambah kolom + update data |
| `apps_zakat/api-python/app/modules/otorisasi/repo.py` | MODIFY | Tambah `get_user_limit()` |
| `apps_zakat/api-python/app/modules/otorisasi/service.py` | MODIFY | Tambah `ENTITY_TRANSACTION_CODE`, `save_and_submit()`, `update_and_submit()`, `get_user_limit_for_entity()` |
| `apps_zakat/api-python/app/modules/otorisasi/router.py` | MODIFY | Tambah 3 endpoint baru |
| `apps_zakat/bff-api/app/routers/otorisasi.py` | MODIFY | Tambah 3 endpoint proxy |
| `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue` | MODIFY | Ganti save → saveAndSubmit, tambah limit display |
| `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue` | MODIFY | Ganti save → saveAndSubmit, tambah limit display |

---

## Task 1: DB Migration — tambah jenis_limit ke transactiontype

**Files:**
- Create: `infra/db/migrations/transaction/add_jenis_limit_to_transactiontype.sql`

- [ ] **Step 1: Buat file SQL**

`infra/db/migrations/transaction/add_jenis_limit_to_transactiontype.sql`:
```sql
ALTER TABLE transaction.transactiontype
  ADD COLUMN IF NOT EXISTS jenis_limit VARCHAR(1) DEFAULT NULL;

-- Map transaksi input yang mendukung limit
UPDATE transaction.transactiontype
  SET jenis_limit = 'O'
  WHERE transactioncode IN ('SD001', 'SDMULTI', 'SDULBA', 'DD001');
```

- [ ] **Step 2: Apply ke database**

```bash
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -f infra/db/migrations/transaction/add_jenis_limit_to_transactiontype.sql
```

- [ ] **Step 3: Verifikasi**

```bash
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -c "SELECT transactioncode, jenis_limit FROM transaction.transactiontype WHERE jenis_limit IS NOT NULL ORDER BY transactioncode"
```

Expected output:
```
 transactioncode | jenis_limit
-----------------+-------------
 DD001           | O
 SD001           | O
 SDMULTI         | O
 SDULBA          | O
(4 rows)
```

- [ ] **Step 4: Commit**

```bash
git add infra/db/migrations/transaction/add_jenis_limit_to_transactiontype.sql
git commit -m "[LIMIT-TRANSAKSI] feat(db): tambah jenis_limit ke transaction.transactiontype

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: api-python repo — get_user_limit()

**Files:**
- Modify: `apps_zakat/api-python/app/modules/otorisasi/repo.py`
- Test: `apps_zakat/api-python/tests/otorisasi/test_repo.py`

- [ ] **Step 1: Tulis test (TDD)**

Tambahkan ke `apps_zakat/api-python/tests/otorisasi/test_repo.py`:
```python
@pytest.mark.asyncio
async def test_get_user_limit_no_limit():
    # RAIS punya nilai_limit=0 → kembalikan 0.0
    result = await repo.get_user_limit('RAIS', 'DD001')
    assert isinstance(result, float)
    assert result == 0.0


@pytest.mark.asyncio
async def test_get_user_limit_unknown_user():
    result = await repo.get_user_limit('NONEXISTENT_USER_XYZ', 'DD001')
    assert result == 0.0


@pytest.mark.asyncio
async def test_get_user_limit_no_jenis_limit_mapping():
    # COA tidak punya jenis_limit → kembalikan 0.0
    result = await repo.get_user_limit('RAIS', 'COA999')
    assert result == 0.0
```

- [ ] **Step 2: Jalankan test — pastikan FAIL**

```bash
cd apps_zakat/api-python
DATABASE_URL=postgresql://transaction:solusi@localhost/mziss_laz pytest tests/otorisasi/test_repo.py::test_get_user_limit_no_limit -v
```

Expected: `AttributeError: module 'app.modules.otorisasi.repo' has no attribute 'get_user_limit'`

- [ ] **Step 3: Implementasikan fungsi**

Tambahkan di akhir `apps_zakat/api-python/app/modules/otorisasi/repo.py`:
```python
async def get_user_limit(user_id: str, transaction_code: str) -> float:
    """Return nilai_limit user untuk transaction_code. 0.0 jika belum diset atau tidak ditemukan."""
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
    if not row or not row['nilai_limit']:
        return 0.0
    return float(row['nilai_limit'])
```

- [ ] **Step 4: Jalankan test — pastikan PASS**

```bash
DATABASE_URL=postgresql://transaction:solusi@localhost/mziss_laz pytest tests/otorisasi/test_repo.py -v
```

Expected: semua test pass (termasuk test lama).

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/api-python/app/modules/otorisasi/repo.py \
        apps_zakat/api-python/tests/otorisasi/test_repo.py
git commit -m "[LIMIT-TRANSAKSI] feat(api-python): repo.get_user_limit() — cek limit user dari enterprise.limittransaksi

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: api-python service — save_and_submit() + update_and_submit() + get_user_limit_for_entity()

**Files:**
- Modify: `apps_zakat/api-python/app/modules/otorisasi/service.py`
- Test: `apps_zakat/api-python/tests/otorisasi/test_service.py`

- [ ] **Step 1: Tulis tests (TDD)**

Tambahkan ke `apps_zakat/api-python/tests/otorisasi/test_service.py`:
```python
@pytest.mark.asyncio
async def test_save_and_submit_below_limit_dispatches():
    """Total ≤ limit → AUTHORIZED langsung, dispatcher dipanggil."""
    mock_sub = {
        'status': 'PENDING', 'level_current': 1, 'level_required': 1,
        'entity_type': 'penyaluran', 'submitted_by': 'RAIS', 'branch_code': '001',
        'payload': {'items': [{'amount': 100000}]},
    }
    mock_dispatcher = AsyncMock(return_value=999)
    with patch('app.modules.otorisasi.service.repo.get_entity_config',
               return_value={'entity_type': 'penyaluran'}), \
         patch('app.modules.otorisasi.service.repo.get_user_limit', return_value=500000.0), \
         patch('app.modules.otorisasi.service.repo.create_submission', return_value=42), \
         patch('app.modules.otorisasi.service.repo.insert_approval_log', return_value=1), \
         patch('app.modules.otorisasi.service.repo.authorize_submission'), \
         patch.dict('app.modules.otorisasi.service._DISPATCHERS', {'penyaluran': mock_dispatcher}):
        result = await service.save_and_submit(
            'penyaluran', 'keuangan',
            {'items': [{'amount': 100000}]},
            'RAIS', '001',
        )
    assert result['status'] == 'AUTHORIZED'
    assert result['bypassed_auth'] is True
    assert result['transaction_id'] == 999
    mock_dispatcher.assert_called_once_with(
        payload={'items': [{'amount': 100000}]}, user_id='RAIS', branch_code='001',
    )


@pytest.mark.asyncio
async def test_save_and_submit_above_limit_goes_pending():
    """Total > limit → PENDING."""
    mock_dispatcher = AsyncMock(return_value=999)
    with patch('app.modules.otorisasi.service.repo.get_entity_config',
               return_value={'entity_type': 'penyaluran'}), \
         patch('app.modules.otorisasi.service.repo.get_user_limit', return_value=50000.0), \
         patch('app.modules.otorisasi.service.repo.create_submission', return_value=43), \
         patch('app.modules.otorisasi.service.repo.submit_submission'), \
         patch.dict('app.modules.otorisasi.service._DISPATCHERS', {'penyaluran': mock_dispatcher}):
        result = await service.save_and_submit(
            'penyaluran', 'keuangan',
            {'items': [{'amount': 100000}]},
            'RAIS', '001',
        )
    assert result['status'] == 'PENDING'
    assert result['bypassed_auth'] is False
    assert result['transaction_id'] is None
    mock_dispatcher.assert_not_called()


@pytest.mark.asyncio
async def test_save_and_submit_zero_limit_goes_pending():
    """nilai_limit = 0 (belum diset) → selalu PENDING."""
    with patch('app.modules.otorisasi.service.repo.get_entity_config',
               return_value={'entity_type': 'penghimpunan'}), \
         patch('app.modules.otorisasi.service.repo.get_user_limit', return_value=0.0), \
         patch('app.modules.otorisasi.service.repo.create_submission', return_value=44), \
         patch('app.modules.otorisasi.service.repo.submit_submission'):
        result = await service.save_and_submit(
            'penghimpunan', 'keuangan',
            {'items': [{'amount': 1}]},
            'RAIS', '001',
        )
    assert result['status'] == 'PENDING'
    assert result['bypassed_auth'] is False
```

- [ ] **Step 2: Jalankan test — pastikan FAIL**

```bash
DATABASE_URL=postgresql://transaction:solusi@localhost/mziss_laz pytest tests/otorisasi/test_service.py::test_save_and_submit_below_limit_dispatches -v
```

Expected: `AttributeError: module 'app.modules.otorisasi.service' has no attribute 'save_and_submit'`

- [ ] **Step 3: Implementasikan fungsi-fungsi baru**

Tambahkan di `apps_zakat/api-python/app/modules/otorisasi/service.py`, setelah `_DISPATCHERS` dict:

```python
ENTITY_TRANSACTION_CODE: dict[str, str] = {
    'penghimpunan':        'SD001',
    'penyaluran':          'DD001',
    'upload_penghimpunan': 'SDULBA',
}


async def get_user_limit_for_entity(user_id: str, entity_type: str) -> float:
    """Return nilai_limit user untuk entity_type. 0.0 jika tidak ada mapping atau belum diset."""
    tx_code = ENTITY_TRANSACTION_CODE.get(entity_type)
    if not tx_code:
        return 0.0
    return await repo.get_user_limit(user_id, tx_code)


async def _decide_and_finalize(
    sub_id: int, entity_type: str, payload: dict,
    user_id: str, branch_code: str, nilai_limit: float,
) -> dict:
    """Shared logic: cek limit, dispatch atau pending. Dipanggil dari save_and_submit dan update_and_submit."""
    total = sum(float(i.get('amount', 0)) for i in payload.get('items', []))
    bypassed = nilai_limit > 0 and total <= nilai_limit

    if bypassed:
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
        await repo.submit_submission(sub_id)
        return {
            'submission_id': sub_id,
            'status': 'PENDING',
            'transaction_id': None,
            'bypassed_auth': False,
        }


async def save_and_submit(
    entity_type: str, module: str, payload: dict,
    user_id: str, branch_code: str,
) -> dict:
    """Buat submission baru + cek limit + dispatch atau set PENDING."""
    config = await repo.get_entity_config(entity_type)
    if not config:
        raise HTTPException(400, f"entity_type '{entity_type}' tidak dikenal")

    nilai_limit = await get_user_limit_for_entity(user_id, entity_type)
    sub_id = await repo.create_submission(entity_type, module, branch_code, payload, user_id)
    return await _decide_and_finalize(sub_id, entity_type, payload, user_id, branch_code, nilai_limit)


async def update_and_submit(
    submission_id: int, payload: dict, user_id: str,
) -> dict:
    """Update payload submission REJECTED + cek limit + dispatch atau set PENDING."""
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['submitted_by'] != user_id:
        raise HTTPException(403, 'Bukan submission Anda')
    if sub['status'] != 'REJECTED':
        raise HTTPException(400, f"Hanya submission REJECTED yang bisa di-update. Status saat ini: '{sub['status']}'")

    await repo.update_payload(submission_id, payload)

    entity_type = sub['entity_type']
    branch_code = sub['branch_code']
    nilai_limit = await get_user_limit_for_entity(user_id, entity_type)
    return await _decide_and_finalize(submission_id, entity_type, payload, user_id, branch_code, nilai_limit)
```

- [ ] **Step 4: Jalankan semua service tests — pastikan PASS**

```bash
DATABASE_URL=postgresql://transaction:solusi@localhost/mziss_laz pytest tests/otorisasi/test_service.py -v
```

Expected: semua test pass (lama + baru = 7 passed).

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/api-python/app/modules/otorisasi/service.py \
        apps_zakat/api-python/tests/otorisasi/test_service.py
git commit -m "[LIMIT-TRANSAKSI] feat(api-python): save_and_submit + update_and_submit + limit check logic

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: api-python router — 3 endpoint baru

**Files:**
- Modify: `apps_zakat/api-python/app/modules/otorisasi/router.py`

- [ ] **Step 1: Tambahkan 3 endpoint di akhir router.py**

```python
class SaveAndSubmitIn(BaseModel):
    entity_type: str
    module: str
    payload: dict[str, Any]


class UpdateAndSubmitIn(BaseModel):
    payload: dict[str, Any]
```

Tambahkan import `SaveAndSubmitIn` dan `UpdateAndSubmitIn` ke bagian atas (setelah import `SubmissionIn`). Kemudian tambahkan di akhir file:

```python
@router.post('/save-and-submit/')
async def save_and_submit_endpoint(
    body: SaveAndSubmitIn,
    user_id: str = Query(...),
    branch_code: str = Query(...),
):
    try:
        result = await service.save_and_submit(
            body.entity_type, body.module, body.payload, user_id, branch_code,
        )
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.put('/save-and-submit/{submission_id}')
async def update_and_submit_endpoint(
    submission_id: int,
    body: UpdateAndSubmitIn,
    user_id: str = Query(...),
):
    try:
        result = await service.update_and_submit(submission_id, body.payload, user_id)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.get('/user-limit/')
async def get_user_limit_endpoint(
    user_id: str = Query(...),
    entity_type: str = Query(...),
):
    nilai_limit = await service.get_user_limit_for_entity(user_id, entity_type)
    return JSONResponse(ok({
        'entity_type': entity_type,
        'nilai_limit': nilai_limit,
        'has_limit': nilai_limit > 0,
    }))
```

Perlu tambah `from typing import Any` jika belum ada, dan `from pydantic import BaseModel` (cek apakah sudah diimport dari schema).

> Catatan: `SaveAndSubmitIn` dan `UpdateAndSubmitIn` bisa juga diletakkan di `schema.py` mengikuti pola yang sudah ada. Cek `schema.py` — jika model lain ada di sana, pindahkan ke sana juga.

- [ ] **Step 2: Smoke test (setelah restart api-python)**

```bash
cd /home/wishnew/workshop/isf-app/infra
podman-compose -f docker-compose.zakat.yml restart api-python
sleep 5

# Test user-limit endpoint langsung
curl -s 'http://localhost:8000/api/otorisasi/user-limit/?user_id=RAIS&entity_type=penyaluran' | python3 -m json.tool
```

Expected:
```json
{"data": {"entity_type": "penyaluran", "nilai_limit": 0.0, "has_limit": false}, "meta": {...}}
```

- [ ] **Step 3: Commit**

```bash
git add apps_zakat/api-python/app/modules/otorisasi/router.py
git commit -m "[LIMIT-TRANSAKSI] feat(api-python): endpoint save-and-submit POST+PUT + user-limit GET

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: bff-api — 3 endpoint proxy baru

**Files:**
- Modify: `apps_zakat/bff-api/app/routers/otorisasi.py`

- [ ] **Step 1: Tambahkan 3 endpoint proxy di otorisasi.py**

Buka `apps_zakat/bff-api/app/routers/otorisasi.py`. Cari bagian fixed-menu endpoints. Tambahkan setelah `entity_configs` endpoint (paling akhir):

```python
@router.post('/save-and-submit/')
async def save_and_submit(request: Request):
    """Simpan submission baru + cek limit + dispatch atau PENDING."""
    body = await request.json()
    entity_type = body.get('entity_type', '')
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    await require_menu(menu_key)(request)
    s = _session(request)
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/otorisasi/save-and-submit/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.put('/save-and-submit/{submission_id}')
async def update_and_submit(submission_id: int, request: Request):
    """Update submission REJECTED + cek limit + dispatch atau PENDING."""
    # Fetch detail dulu untuk get entity_type (untuk menu check)
    detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if detail.status_code != 200:
        return JSONResponse(status_code=detail.status_code, content=detail.json())
    entity_type = (detail.json().get('data') or {}).get('entity_type', '')
    await _check_dynamic_menu(request, entity_type)
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/otorisasi/save-and-submit/{submission_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.put(url, json=body, params={'user_id': s['user_id']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/user-limit/')
async def get_user_limit(
    request: Request,
    entity_type: str = Query(...),
):
    """Return limit user untuk entity_type. Gating: entity's menu key."""
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    await require_menu(menu_key)(request)
    s = _session(request)
    downstream = await get_api_python(
        '/api/otorisasi/user-limit/',
        params={'user_id': s['user_id'], 'entity_type': entity_type},
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
```

- [ ] **Step 2: Restart bff-api dan smoke test**

```bash
cd /home/wishnew/workshop/isf-app/infra
podman-compose -f docker-compose.zakat.yml restart bff-api
sleep 5

# Login sebagai RAIS
curl -s -c /tmp/ck_rais.txt http://localhost:7000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"RAIS","password":"test1234"}' > /dev/null

# Test user-limit via BFF
curl -s -b /tmp/ck_rais.txt 'http://localhost:7000/api/otorisasi/user-limit/?entity_type=penyaluran' \
  | python3 -m json.tool
```

Expected: `{"data": {"entity_type": "penyaluran", "nilai_limit": 0.0, "has_limit": false}, ...}`

- [ ] **Step 3: Test save-and-submit via BFF (nilai_limit=0 → PENDING)**

```bash
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
      "items": [{"product_id": 1, "account_no": "Z1BI002.001.IDR",
                 "amount": 100000, "fund_entity": 1, "ashnaf": "F", "description": "test"}]
    }
  }' | python3 -m json.tool
```

Expected: `"status": "PENDING"`, `"bypassed_auth": false`

- [ ] **Step 4: Set limit user dan test AUTHORIZED path**

```bash
# Set limit 500000 untuk RAIS
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -c "UPDATE enterprise.limittransaksi SET nilai_limit = 500000 WHERE id_user = 'RAIS'"

# Test lagi (total 100000 ≤ limit 500000 → AUTHORIZED)
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
      "items": [{"product_id": 1, "account_no": "Z1BI002.001.IDR",
                 "amount": 100000, "fund_entity": 1, "ashnaf": "F", "description": "test below limit"}]
    }
  }' | python3 -m json.tool

# Expected: "status": "AUTHORIZED", "bypassed_auth": true, "transaction_id": <number>

# Reset limit ke 0
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -c "UPDATE enterprise.limittransaksi SET nilai_limit = 0 WHERE id_user = 'RAIS'"
```

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/bff-api/app/routers/otorisasi.py
git commit -m "[LIMIT-TRANSAKSI] feat(bff-api): proxy save-and-submit POST+PUT + user-limit GET

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: web-vue — PenyaluranDanaFormPage

**Files:**
- Modify: `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue`

Read file dulu untuk memahami struktur saat ini:
```bash
grep -n "submit\|loading\|router\|toast\|Button\|limit\|total\|items" \
  apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue | head -40
```

- [ ] **Step 1: Tambah state limit dan computed total**

Di `<script setup>`, setelah deklarasi state yang ada, tambahkan:

```typescript
// ── Limit & total ──────────────────────────────────────────────────────────────
const nilaiLimit = shallowRef<number>(0)
const hasLimit = shallowRef<boolean>(false)
const limitLoading = shallowRef<boolean>(false)

const totalAmount = computed(() =>
  items.value.reduce((sum, i) => sum + (i.amount ?? 0), 0)
)

const willBypass = computed(() =>
  hasLimit.value && totalAmount.value > 0 && totalAmount.value <= nilaiLimit.value
)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmtRp = (n: number) => 'Rp ' + idr.format(n)
```

- [ ] **Step 2: Fetch limit on mount**

Tambahkan fungsi fetch limit sebelum `onMounted`:

```typescript
async function fetchUserLimit() {
  if (isEditMode.value) return  // edit mode: limit sudah berlaku saat submit
  limitLoading.value = true
  try {
    const res = await api.get<{ nilai_limit: number; has_limit: boolean }>(
      '/api/otorisasi/user-limit/?entity_type=penyaluran',
    )
    nilaiLimit.value = res.nilai_limit
    hasLimit.value = res.has_limit
  } catch {
    // silent fail — limit info tidak kritis untuk UX
  } finally {
    limitLoading.value = false
  }
}
```

Ubah `onMounted` untuk memanggil `fetchUserLimit()`:

```typescript
onMounted(async () => {
  await Promise.all([loadLookups(), fetchUserLimit()])
  if (isEditMode.value && editId.value !== null) {
    await loadSubmission(editId.value)
  }
})
```

> Cek fungsi `onMounted` yang ada — sesuaikan supaya tidak duplikasi `loadLookups()`.

- [ ] **Step 3: Ganti fungsi submit() → saveAndSubmit()**

Ganti isi fungsi `submit()` yang ada dengan implementasi baru:

```typescript
async function submit() {
  const validErr = validate()
  if (validErr) { toast.error(validErr); return }
  loading.value = true
  errorMsg.value = null
  try {
    const innerPayload = {
      actual_date: actualDate.value,
      reference_no: referenceNo.value || null,
      description: description.value,
      paid_to: paidTo.value || null,
      payment_type: paymentType.value,
      payment_account_no: paymentAccountNo.value,
      fund_account_no: fundAccountNo.value,
      product_branch_code: productBranchCode.value,
      rate: rate.value,
      currency_code: currencyCode.value,
      items: items.value.map((i) => ({
        product_id: i.product_id,
        account_no: i.account_no,
        amount: i.amount,
        description: i.description || description.value,
        fund_entity: i.fund_entity,
        ashnaf: i.fund_entity === 1 ? i.ashnaf : 'L',
        dist_item_account: i.dist_item_account,
        distribution_category: i.distribution_category,
      })),
    }

    let res: { status: string; bypassed_auth: boolean }

    if (isEditMode.value && editId.value !== null) {
      res = await api.put<{ status: string; bypassed_auth: boolean }>(
        `/api/otorisasi/save-and-submit/${editId.value}`,
        { payload: innerPayload },
      )
    } else {
      res = await api.post<{ status: string; bypassed_auth: boolean }>(
        '/api/otorisasi/save-and-submit/',
        { entity_type: 'penyaluran', module: 'keuangan', payload: innerPayload },
      )
    }

    if (res.status === 'AUTHORIZED') {
      toast.success('Transaksi berhasil — langsung efektif')
    } else {
      toast.success('Transaksi dikirim — menunggu otorisasi')
    }
    router.push({ name: 'keuangan-transaksi-penyaluran' })
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal menyimpan transaksi')
  } finally {
    loading.value = false
  }
}
```

- [ ] **Step 4: Tambah limit info display di template**

Cari bagian total amount di template (biasanya dekat tombol submit). Tambahkan sebelum tombol submit:

```vue
<!-- Limit info & indicator -->
<div v-if="!isEditMode && items.length > 0" class="rounded border px-4 py-3 text-sm space-y-1">
  <div class="flex justify-between font-medium">
    <span class="text-zinc-500">Total transaksi</span>
    <span>{{ fmtRp(totalAmount) }}</span>
  </div>
  <template v-if="!limitLoading">
    <div v-if="hasLimit" class="flex justify-between text-xs text-zinc-400">
      <span>Limit Anda</span>
      <span>{{ fmtRp(nilaiLimit) }}</span>
    </div>
    <div :class="[
      'flex items-center gap-1.5 text-xs font-medium mt-1',
      willBypass ? 'text-green-600' : 'text-amber-600',
    ]">
      <span>{{ willBypass ? '✓' : 'ⓘ' }}</span>
      <span>{{
        willBypass
          ? 'Transaksi ini akan langsung efektif'
          : hasLimit
            ? 'Transaksi ini memerlukan otorisasi'
            : 'Semua transaksi memerlukan otorisasi'
      }}</span>
    </div>
  </template>
</div>
```

- [ ] **Step 5: Ganti label tombol**

Cari baris tombol submit di template (sekitar baris 448-454 berdasarkan grep sebelumnya):

```vue
<!-- Ganti: -->
{{ loading ? 'Menyimpan...' : isEditMode ? 'Update Draft' : 'Simpan Draft' }}

<!-- Dengan: -->
{{ loading ? 'Menyimpan...' : isEditMode ? 'Update & Submit' : 'Simpan & Submit' }}
```

- [ ] **Step 6: Verifikasi di browser**

Buka `http://localhost:5173/keuangan/transaksi/penyaluran/baru`:
1. Tambah 1 item → limit info muncul di bawah
2. Jika `nilai_limit = 0` → teks "Semua transaksi memerlukan otorisasi"
3. Set limit: `UPDATE enterprise.limittransaksi SET nilai_limit = 500000 WHERE id_user = 'RAIS'`
4. Refresh form → teks berubah sesuai total vs limit
5. Klik "Simpan & Submit" → toast sesuai status

- [ ] **Step 7: Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue
git commit -m "[LIMIT-TRANSAKSI] feat(ui): penyaluran form — Simpan & Submit + limit indicator

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: web-vue — PenghimpunanDanaFormPage

**Files:**
- Modify: `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue`

- [ ] **Step 1: Tambah state limit dan computed total**

Sama persis dengan Task 6 Step 1, tambahkan di script:

```typescript
const nilaiLimit = shallowRef<number>(0)
const hasLimit = shallowRef<boolean>(false)
const limitLoading = shallowRef<boolean>(false)

const totalAmount = computed(() =>
  items.value.reduce((sum, i) => sum + (i.amount ?? 0), 0)
)

const willBypass = computed(() =>
  hasLimit.value && totalAmount.value > 0 && totalAmount.value <= nilaiLimit.value
)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmtRp = (n: number) => 'Rp ' + idr.format(n)
```

- [ ] **Step 2: Fetch limit on mount**

Tambahkan fungsi (sama seperti Task 6 Step 2, tapi `entity_type=penghimpunan`):

```typescript
async function fetchUserLimit() {
  if (isEditMode.value) return
  limitLoading.value = true
  try {
    const res = await api.get<{ nilai_limit: number; has_limit: boolean }>(
      '/api/otorisasi/user-limit/?entity_type=penghimpunan',
    )
    nilaiLimit.value = res.nilai_limit
    hasLimit.value = res.has_limit
  } catch {
    // silent fail
  } finally {
    limitLoading.value = false
  }
}
```

Sesuaikan `onMounted` untuk memanggil `fetchUserLimit()`.

- [ ] **Step 3: Ganti submit() → saveAndSubmit()**

Ganti isi fungsi `submit()` yang ada (sekitar baris 210-278):

```typescript
async function submit() {
  const validErr = validate()
  if (validErr) { toast.error(validErr); return }
  loading.value = true
  errorMsg.value = null
  try {
    const innerPayload = {
      actual_date: actualDate.value,
      reference_no: referenceNo.value || null,
      description: description.value,
      paid_to: paidTo.value || null,
      donor_id: donorId.value || null,
      donor_no: donorNo.value || null,
      donor_name: donorName.value || null,
      payment_type: paymentType.value,
      payment_account_no: paymentAccountNo.value || null,
      rate: rate.value,
      currency_code: currencyCode.value,
      product_branch_code: productBranchCode.value,
      items: items.value.map((i) => ({
        product_id: i.product_id,
        account_no: i.account_no,
        amount: i.amount,
        description: i.description || description.value,
        fund_entity: i.fund_entity,
        percentage_of_amil: i.percentage_of_amil ?? 0,
      })),
    }

    let res: { status: string; bypassed_auth: boolean }

    if (isEditMode.value && editId.value !== null) {
      res = await api.put<{ status: string; bypassed_auth: boolean }>(
        `/api/otorisasi/save-and-submit/${editId.value}`,
        { payload: innerPayload },
      )
    } else {
      res = await api.post<{ status: string; bypassed_auth: boolean }>(
        '/api/otorisasi/save-and-submit/',
        { entity_type: 'penghimpunan', module: 'keuangan', payload: innerPayload },
      )
    }

    if (res.status === 'AUTHORIZED') {
      toast.success('Transaksi berhasil — langsung efektif')
    } else {
      toast.success('Transaksi dikirim — menunggu otorisasi')
    }
    router.push({ name: 'keuangan-transaksi-penghimpunan' })
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal menyimpan transaksi')
  } finally {
    loading.value = false
  }
}
```

> Sesuaikan field `innerPayload` dengan field aktual yang ada di form penghimpunan — baca bagian `if (isEditMode.value)` yang sudah ada sebelumnya untuk referensi field apa saja yang dikumpulkan.

- [ ] **Step 4: Tambah limit info di template**

Tambahkan blok yang sama dengan Task 6 Step 4 di dekat tombol submit penghimpunan. Ganti label tombol:

```vue
{{ loading ? 'Menyimpan...' : isEditMode ? 'Update & Submit' : 'Simpan & Submit' }}
```

- [ ] **Step 5: Verifikasi di browser**

Buka `http://localhost:5173/keuangan/transaksi/penghimpunan/baru`:
1. Tambah item → limit indicator muncul
2. Klik "Simpan & Submit" → toast sesuai (`nilai_limit=0` → "menunggu otorisasi")

- [ ] **Step 6: Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue
git commit -m "[LIMIT-TRANSAKSI] feat(ui): penghimpunan form — Simpan & Submit + limit indicator

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Checklist Akhir

- [ ] `jenis_limit = 'O'` tersimpan di 4 transaction codes di DB
- [ ] `GET /api/otorisasi/user-limit/?entity_type=penyaluran` → `{ nilai_limit, has_limit }`
- [ ] `POST /api/otorisasi/save-and-submit/` dengan `nilai_limit = 0` → `status = PENDING`
- [ ] `POST /api/otorisasi/save-and-submit/` dengan `total ≤ limit` → `status = AUTHORIZED`, `transaction_id` terisi
- [ ] `POST /api/otorisasi/save-and-submit/` dengan `total > limit` → `status = PENDING`
- [ ] `PUT /api/otorisasi/save-and-submit/{id}` pada submission REJECTED → update + decide
- [ ] Form penyaluran: tombol "Simpan & Submit", limit indicator muncul
- [ ] Form penghimpunan: tombol "Simpan & Submit", limit indicator muncul
- [ ] `approval_log` mencatat `authorizer_id = 'SYSTEM_AUTO'` untuk transaksi bypass

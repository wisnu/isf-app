# Sistem Otorisasi Terpusat Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bangun sistem otorisasi terpusat generic berbasis `otorisasi.submission` (JSONB staging) yang menampung semua input keuangan (Penghimpunan, Penyaluran, Upload, COA, Kas, Bank) sebelum diposting ke tabel utama.

**Architecture:** Data input disimpan di `otorisasi.submission` (JSONB payload) sebelum diotorisasi — tabel utama hanya diisi setelah terotorisasi via dispatch registry. Multi-level didukung via `entity_config.level_required` (default 1). BFF gateway mengontrol akses per menu key yang di-resolve dari entity_config.

**Tech Stack:** PostgreSQL (asyncpg), FastAPI (api-python + bff-api), Vue 3 + PrimeVue unstyled + Tailwind (web-vue), Lucide icons.

**Spec:** `docs/todos/2026-06-08-002-otorisasi/specs.md`  
**Checklist tingkat tinggi:** `docs/todos/2026-06-08-002-otorisasi/plan.md`

---

## File Map

| File | Aksi | Tanggung jawab |
|---|---|---|
| `infra/db/migrations/otorisasi/001_create_schema.sql` | CREATE | Schema `otorisasi` |
| `infra/db/migrations/otorisasi/002_create_submission.sql` | CREATE | Tabel staging generic + index |
| `infra/db/migrations/otorisasi/003_create_approval_log.sql` | CREATE | Histori tiap level approval |
| `infra/db/migrations/otorisasi/004_create_entity_config.sql` | CREATE | Konfigurasi level per entity_type |
| `infra/db/migrations/seed/seed-otorisasi-entity-config.sql` | CREATE | 6 rows keuangan ke entity_config |
| `infra/db/migrations/seed/seed-menu-otorisasi.sql` | CREATE | Menu + role_menu `keuangan.monitoring.otorisasi` |
| `apps_zakat/api-python/app/modules/otorisasi/__init__.py` | CREATE | Module marker |
| `apps_zakat/api-python/app/modules/otorisasi/schema.py` | CREATE | Pydantic request/response models |
| `apps_zakat/api-python/app/modules/otorisasi/repo.py` | CREATE | asyncpg queries ke otorisasi.* |
| `apps_zakat/api-python/app/modules/otorisasi/service.py` | CREATE | Business logic + dispatch registry |
| `apps_zakat/api-python/app/modules/otorisasi/router.py` | CREATE | FastAPI endpoints |
| `apps_zakat/api-python/app/main.py` | MODIFY | Register otorisasi router + call `_register_defaults()` |
| `apps_zakat/api-python/app/modules/transaction/penghimpunan_service.py` | MODIFY | Tambah `create_from_payload()` |
| `apps_zakat/api-python/app/modules/transaction/penyaluran_service.py` | MODIFY | Tambah `create_from_payload()` |
| `apps_zakat/bff-api/app/routers/otorisasi.py` | CREATE | BFF proxy + menu gate |
| `apps_zakat/bff-api/app/main.py` | MODIFY | Register otorisasi_router |
| `apps_zakat/web-vue/src/lib/menu/registry.ts` | MODIFY | Tambah `keuangan.monitoring.otorisasi` |
| `apps_zakat/web-vue/src/router/index.ts` | MODIFY | Route `/keuangan/monitoring/otorisasi` |
| `apps_zakat/web-vue/src/components/otorisasi/StatusBadge.vue` | CREATE | Badge DRAFT/PENDING/REJECTED/AUTHORIZED |
| `apps_zakat/web-vue/src/components/otorisasi/SubmissionDetailDrawer.vue` | CREATE | Detail drawer per entity_type |
| `apps_zakat/web-vue/src/pages/keuangan/OtorisasiPage.vue` | CREATE | Halaman otorisator |
| `apps_zakat/web-vue/src/components/AppSidebar.vue` | MODIFY | Section Monitoring dan Kontrol |
| `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue` | MODIFY | Save → otorisasi.submission |
| `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaPage.vue` | MODIFY | Gabung my-submissions + badge |
| `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue` | MODIFY | Save → otorisasi.submission |
| `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue` | MODIFY | Gabung my-submissions + badge |
| `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue` | MODIFY | Submit → otorisasi.submission |
| `apps_zakat/web-vue/src/pages/keuangan/CoaPage.vue` | MODIFY | Gabung my-submissions + badge |
| `apps_zakat/web-vue/src/pages/keuangan/KasPage.vue` | MODIFY | Gabung my-submissions + badge |
| `apps_zakat/web-vue/src/pages/keuangan/BankPage.vue` | MODIFY | Gabung my-submissions + badge |

---

## Task 1: DB Migrations

**Files:**
- Create: `infra/db/migrations/otorisasi/001_create_schema.sql`
- Create: `infra/db/migrations/otorisasi/002_create_submission.sql`
- Create: `infra/db/migrations/otorisasi/003_create_approval_log.sql`
- Create: `infra/db/migrations/otorisasi/004_create_entity_config.sql`

- [ ] **Step 1: Buat folder dan 4 file SQL**

```bash
mkdir -p infra/db/migrations/otorisasi
```

`infra/db/migrations/otorisasi/001_create_schema.sql`:
```sql
CREATE SCHEMA IF NOT EXISTS otorisasi;
```

`infra/db/migrations/otorisasi/002_create_submission.sql`:
```sql
CREATE TABLE otorisasi.submission (
    id              SERIAL PRIMARY KEY,
    entity_type     VARCHAR(50)  NOT NULL,
    module          VARCHAR(50)  NOT NULL,
    branch_code     VARCHAR(10)  NOT NULL,
    payload         JSONB        NOT NULL,
    status          VARCHAR(20)  NOT NULL DEFAULT 'DRAFT',
    level_current   INTEGER      NOT NULL DEFAULT 0,
    submitted_by    VARCHAR(50)  NOT NULL,
    submitted_at    TIMESTAMP,
    result_entity_id INTEGER,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_otorisasi_submission_status      ON otorisasi.submission(status);
CREATE INDEX idx_otorisasi_submission_branch      ON otorisasi.submission(branch_code);
CREATE INDEX idx_otorisasi_submission_entity_type ON otorisasi.submission(entity_type);
CREATE INDEX idx_otorisasi_submission_submitted_by ON otorisasi.submission(submitted_by);
```

`infra/db/migrations/otorisasi/003_create_approval_log.sql`:
```sql
CREATE TABLE otorisasi.approval_log (
    id            SERIAL PRIMARY KEY,
    submission_id INTEGER      NOT NULL REFERENCES otorisasi.submission(id) ON DELETE CASCADE,
    level         INTEGER      NOT NULL,
    authorizer_id VARCHAR(50)  NOT NULL,
    status        VARCHAR(20)  NOT NULL,
    notes         TEXT,
    logged_at     TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_otorisasi_approval_log_submission ON otorisasi.approval_log(submission_id);
```

`infra/db/migrations/otorisasi/004_create_entity_config.sql`:
```sql
CREATE TABLE otorisasi.entity_config (
    entity_type    VARCHAR(50)  PRIMARY KEY,
    module         VARCHAR(50)  NOT NULL,
    level_required INTEGER      NOT NULL DEFAULT 1,
    label          VARCHAR(100) NOT NULL,
    menu_key       VARCHAR(100) NOT NULL
);
```

- [ ] **Step 2: Apply ke database**

```bash
for f in 001 002 003 004; do
  PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
    -f infra/db/migrations/otorisasi/${f}_*.sql && echo "✓ $f"
done
```

Expected: 4 baris `✓`.

- [ ] **Step 3: Verifikasi**

```bash
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -c "\dt otorisasi.*"
```

Expected: `submission`, `approval_log`, `entity_config` muncul.

- [ ] **Step 4: Commit**

```bash
git add infra/db/migrations/otorisasi/
git commit -m "[OTORISASI] feat(db): buat schema otorisasi + tabel submission, approval_log, entity_config"
```

---

## Task 2: Seed Data

**Files:**
- Create: `infra/db/migrations/seed/seed-otorisasi-entity-config.sql`
- Create: `infra/db/migrations/seed/seed-menu-otorisasi.sql`

- [ ] **Step 1: Buat seed entity_config**

`infra/db/migrations/seed/seed-otorisasi-entity-config.sql`:
```sql
INSERT INTO otorisasi.entity_config (entity_type, module, level_required, label, menu_key) VALUES
  ('penghimpunan',        'keuangan', 1, 'Penghimpunan Dana',   'keuangan.monitoring.otorisasi'),
  ('penyaluran',          'keuangan', 1, 'Penyaluran Dana',     'keuangan.monitoring.otorisasi'),
  ('upload_penghimpunan', 'keuangan', 1, 'Upload Penghimpunan', 'keuangan.monitoring.otorisasi'),
  ('coa',                 'keuangan', 1, 'Master COA',          'keuangan.monitoring.otorisasi'),
  ('kas',                 'keuangan', 1, 'Master Kas',          'keuangan.monitoring.otorisasi'),
  ('bank',                'keuangan', 1, 'Master Bank',         'keuangan.monitoring.otorisasi')
ON CONFLICT (entity_type) DO NOTHING;
```

- [ ] **Step 2: Buat seed menu otorisasi**

`infra/db/migrations/seed/seed-menu-otorisasi.sql`:
```sql
-- Menu: Monitoring dan Kontrol (parent)
INSERT INTO isf_auth.menu (menu_key, label, parent_key, sort_order, icon, route_path)
VALUES ('keuangan.monitoring', 'Monitoring dan Kontrol', 'keuangan', 50, 'monitor', NULL)
ON CONFLICT (menu_key) DO NOTHING;

-- Menu: Otorisasi (child)
INSERT INTO isf_auth.menu (menu_key, label, parent_key, sort_order, icon, route_path)
VALUES ('keuangan.monitoring.otorisasi', 'Otorisasi', 'keuangan.monitoring', 10, 'shield-check', '/keuangan/monitoring/otorisasi')
ON CONFLICT (menu_key) DO NOTHING;

-- Role menu: SPVDIST
INSERT INTO isf_auth.role_menu (role_code, menu_key)
VALUES ('SPVDIST', 'keuangan.monitoring.otorisasi'),
       ('SPVDIST', 'keuangan.monitoring')
ON CONFLICT DO NOTHING;

-- Role menu: KEU
INSERT INTO isf_auth.role_menu (role_code, menu_key)
VALUES ('KEU', 'keuangan.monitoring.otorisasi'),
       ('KEU', 'keuangan.monitoring')
ON CONFLICT DO NOTHING;

-- Role menu: MANAJER (jika role ini ada)
INSERT INTO isf_auth.role_menu (role_code, menu_key)
VALUES ('MANAJER', 'keuangan.monitoring.otorisasi'),
       ('MANAJER', 'keuangan.monitoring')
ON CONFLICT DO NOTHING;
```

> **Catatan:** Sesuaikan schema `isf_auth.menu` dengan struktur aktual di `isf_auth_zakat`. Cek dulu: `\d isf_auth.menu`

- [ ] **Step 3: Apply seed**

```bash
# entity_config ke business DB
PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_laz \
  -f infra/db/migrations/seed/seed-otorisasi-entity-config.sql

# menu ke auth DB
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -f infra/db/migrations/seed/seed-menu-otorisasi.sql
```

- [ ] **Step 4: Commit**

```bash
git add infra/db/migrations/seed/seed-otorisasi-entity-config.sql \
        infra/db/migrations/seed/seed-menu-otorisasi.sql
git commit -m "[OTORISASI] feat(seed): entity_config 6 rows keuangan + menu keuangan.monitoring.otorisasi"
```

---

## Task 3: api-python — otorisasi module (schema + repo)

**Files:**
- Create: `apps_zakat/api-python/app/modules/otorisasi/__init__.py`
- Create: `apps_zakat/api-python/app/modules/otorisasi/schema.py`
- Create: `apps_zakat/api-python/app/modules/otorisasi/repo.py`

- [ ] **Step 1: Tulis test repo (TDD)**

Buat `apps_zakat/api-python/tests/otorisasi/test_repo.py`:
```python
import pytest
import json
from app.modules.otorisasi import repo


@pytest.mark.asyncio
async def test_create_and_get_submission():
    sub_id = await repo.create_submission(
        entity_type='penghimpunan', module='keuangan',
        branch_code='001',
        payload={"actual_date": "2026-06-08", "payment_type": "C", "items": []},
        submitted_by='RAIS'
    )
    assert isinstance(sub_id, int)

    sub = await repo.get_submission(sub_id)
    assert sub is not None
    assert sub['status'] == 'DRAFT'
    assert sub['entity_type'] == 'penghimpunan'
    assert isinstance(sub['payload'], dict)
    assert sub['payload']['payment_type'] == 'C'
    assert sub['entity_label'] == 'Penghimpunan Dana'  # dari join entity_config


@pytest.mark.asyncio
async def test_submit_and_reject_flow():
    sub_id = await repo.create_submission(
        entity_type='penyaluran', module='keuangan',
        branch_code='001', payload={"actual_date": "2026-06-08"},
        submitted_by='HADI'
    )
    await repo.submit_submission(sub_id)
    sub = await repo.get_submission(sub_id)
    assert sub['status'] == 'PENDING'
    assert sub['level_current'] == 1

    await repo.insert_approval_log(sub_id, 1, 'SPVDIST', 'REJECTED', 'Jumlah tidak sesuai')
    await repo.reject_submission_db(sub_id)
    sub = await repo.get_submission(sub_id)
    assert sub['status'] == 'REJECTED'

    log = await repo.get_approval_log(sub_id)
    assert len(log) == 1
    assert log[0]['status'] == 'REJECTED'
    assert log[0]['notes'] == 'Jumlah tidak sesuai'
```

- [ ] **Step 2: Jalankan test — pastikan FAIL**

```bash
cd apps_zakat/api-python
pytest tests/otorisasi/test_repo.py -v
```

Expected: `ImportError` atau `ModuleNotFoundError`.

- [ ] **Step 3: Buat module files**

`apps_zakat/api-python/app/modules/otorisasi/__init__.py`:
```python
```

`apps_zakat/api-python/app/modules/otorisasi/schema.py`:
```python
from __future__ import annotations
from typing import Any
from pydantic import BaseModel


class SubmissionIn(BaseModel):
    entity_type: str
    module: str
    payload: dict[str, Any]


class UpdatePayloadIn(BaseModel):
    payload: dict[str, Any]


class ApproveIn(BaseModel):
    notes: str | None = None


class RejectIn(BaseModel):
    notes: str


class BulkApproveIn(BaseModel):
    ids: list[int]
    notes: str | None = None


class BulkRejectIn(BaseModel):
    ids: list[int]
    notes: str
```

`apps_zakat/api-python/app/modules/otorisasi/repo.py`:
```python
from __future__ import annotations
import json
from app.shared.db import fetch_all, fetch_one, get_pool


async def create_submission(
    entity_type: str, module: str, branch_code: str,
    payload: dict, submitted_by: str,
) -> int:
    async with get_pool().acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO otorisasi.submission
               (entity_type, module, branch_code, payload, submitted_by)
               VALUES ($1, $2, $3, CAST($4 AS jsonb), $5)
               RETURNING id""",
            entity_type, module, branch_code, json.dumps(payload), submitted_by,
        )
        return int(row['id'])


async def get_submission(submission_id: int) -> dict | None:
    row = await fetch_one(
        """SELECT s.*, ec.label AS entity_label, ec.level_required, ec.menu_key
           FROM otorisasi.submission s
           LEFT JOIN otorisasi.entity_config ec ON ec.entity_type = s.entity_type
           WHERE s.id = $1""",
        submission_id,
    )
    if row is None:
        return None
    # asyncpg mengembalikan JSONB sebagai dict — pastikan bisa di-serialize
    r = dict(row)
    if isinstance(r.get('payload'), str):
        r['payload'] = json.loads(r['payload'])
    return r


async def get_approval_log(submission_id: int) -> list[dict]:
    return await fetch_all(
        """SELECT * FROM otorisasi.approval_log
           WHERE submission_id = $1 ORDER BY level, logged_at""",
        submission_id,
    )


async def submit_submission(submission_id: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET status = 'PENDING', level_current = 1,
                   submitted_at = NOW(), updated_at = NOW()
               WHERE id = $1""",
            submission_id,
        )


async def update_payload(submission_id: int, payload: dict) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET payload = CAST($1 AS jsonb), status = 'DRAFT', updated_at = NOW()
               WHERE id = $2""",
            json.dumps(payload), submission_id,
        )


async def delete_submission(submission_id: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            "DELETE FROM otorisasi.submission WHERE id = $1", submission_id,
        )


async def insert_approval_log(
    submission_id: int, level: int, authorizer_id: str,
    status: str, notes: str | None,
) -> int:
    async with get_pool().acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO otorisasi.approval_log
               (submission_id, level, authorizer_id, status, notes)
               VALUES ($1, $2, $3, $4, $5) RETURNING id""",
            submission_id, level, authorizer_id, status, notes,
        )
        return int(row['id'])


async def advance_level(submission_id: int, new_level: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET level_current = $1, updated_at = NOW() WHERE id = $2""",
            new_level, submission_id,
        )


async def authorize_submission(submission_id: int, result_entity_id: int | None) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET status = 'AUTHORIZED', result_entity_id = $1, updated_at = NOW()
               WHERE id = $2""",
            result_entity_id, submission_id,
        )


async def reject_submission_db(submission_id: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET status = 'REJECTED', updated_at = NOW() WHERE id = $1""",
            submission_id,
        )


async def list_submissions(
    module: str | None = None,
    entity_type: str | None = None,
    status: str | None = None,
    submitted_by: str | None = None,
    branch: str | None = None,
    branch_access: str = 'single',
    page: int = 1,
    page_size: int = 25,
) -> tuple[list[dict], int]:
    # branch_access='all' → tidak filter branch; 'single' → filter ke branch user
    total_row = await fetch_one(
        """SELECT COUNT(*) AS n FROM otorisasi.submission s
           WHERE ($1 IS NULL OR s.module = $1)
             AND ($2 IS NULL OR s.entity_type = $2)
             AND ($3 IS NULL OR s.status = $3)
             AND ($4 IS NULL OR s.submitted_by = $4)
             AND ($5 IS NULL OR $6 = 'all' OR s.branch_code = $5)""",
        module, entity_type, status, submitted_by, branch, branch_access,
    )
    total = int(total_row['n']) if total_row else 0
    offset = (page - 1) * page_size
    rows = await fetch_all(
        """SELECT s.*, ec.label AS entity_label, ec.level_required
           FROM otorisasi.submission s
           LEFT JOIN otorisasi.entity_config ec ON ec.entity_type = s.entity_type
           WHERE ($1 IS NULL OR s.module = $1)
             AND ($2 IS NULL OR s.entity_type = $2)
             AND ($3 IS NULL OR s.status = $3)
             AND ($4 IS NULL OR s.submitted_by = $4)
             AND ($5 IS NULL OR $6 = 'all' OR s.branch_code = $5)
           ORDER BY s.created_at DESC
           LIMIT $7 OFFSET $8""",
        module, entity_type, status, submitted_by, branch, branch_access,
        page_size, offset,
    )
    return rows, total


async def get_entity_config(entity_type: str) -> dict | None:
    return await fetch_one(
        "SELECT * FROM otorisasi.entity_config WHERE entity_type = $1", entity_type,
    )


async def list_entity_configs(module: str | None = None) -> list[dict]:
    if module:
        return await fetch_all(
            "SELECT * FROM otorisasi.entity_config WHERE module = $1 ORDER BY entity_type",
            module,
        )
    return await fetch_all(
        "SELECT * FROM otorisasi.entity_config ORDER BY module, entity_type",
    )
```

- [ ] **Step 4: Jalankan test — pastikan PASS**

```bash
pytest tests/otorisasi/test_repo.py -v
```

Expected: `2 passed`.

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/api-python/app/modules/otorisasi/ \
        apps_zakat/api-python/tests/otorisasi/
git commit -m "[OTORISASI] feat(api-python): otorisasi module — schema + repo (asyncpg)"
```

---

## Task 4: api-python — otorisasi service

**Files:**
- Create: `apps_zakat/api-python/app/modules/otorisasi/service.py`

- [ ] **Step 1: Tulis test service (TDD)**

`apps_zakat/api-python/tests/otorisasi/test_service.py`:
```python
import pytest
from unittest.mock import AsyncMock, patch
from app.modules.otorisasi import service


@pytest.mark.asyncio
async def test_save_draft_unknown_entity_type():
    with patch('app.modules.otorisasi.service.repo.get_entity_config', return_value=None):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            await service.save_draft('unknown', 'keuangan', {}, 'RAIS', '001')
        assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_submit_rejects_already_pending():
    mock_sub = {'submitted_by': 'RAIS', 'status': 'PENDING'}
    with patch('app.modules.otorisasi.service.repo.get_submission', return_value=mock_sub):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            await service.submit_for_auth(1, 'RAIS')
        assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_approve_single_level_dispatches():
    mock_sub = {
        'status': 'PENDING', 'level_current': 1, 'level_required': 1,
        'entity_type': 'penghimpunan', 'submitted_by': 'RAIS', 'branch_code': '001',
        'payload': {'actual_date': '2026-06-08'},
    }
    mock_dispatcher = AsyncMock(return_value=42)
    with patch('app.modules.otorisasi.service.repo.get_submission', return_value=mock_sub), \
         patch('app.modules.otorisasi.service.repo.insert_approval_log', return_value=1), \
         patch('app.modules.otorisasi.service.repo.authorize_submission') as mock_auth, \
         patch.dict('app.modules.otorisasi.service._DISPATCHERS', {'penghimpunan': mock_dispatcher}):
        result = await service.approve(1, 'SPVDIST', 'single', 'OK')
    assert result['status'] == 'AUTHORIZED'
    assert result['result_entity_id'] == 42
    mock_dispatcher.assert_called_once_with(
        payload={'actual_date': '2026-06-08'}, user_id='RAIS', branch_code='001'
    )


@pytest.mark.asyncio
async def test_reject_requires_pending():
    mock_sub = {'status': 'DRAFT', 'level_current': 0}
    with patch('app.modules.otorisasi.service.repo.get_submission', return_value=mock_sub):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            await service.reject(1, 'SPVDIST', 'Alasan penolakan')
        assert exc.value.status_code == 400
```

- [ ] **Step 2: Jalankan test — pastikan FAIL**

```bash
pytest tests/otorisasi/test_service.py -v
```

Expected: `ImportError` karena `service.py` belum ada.

- [ ] **Step 3: Buat service.py**

`apps_zakat/api-python/app/modules/otorisasi/service.py`:
```python
from __future__ import annotations
from fastapi import HTTPException
from . import repo

# Registry: entity_type → async fn(payload, user_id, branch_code) → int
_DISPATCHERS: dict = {}


def register_dispatcher(entity_type: str, fn) -> None:
    _DISPATCHERS[entity_type] = fn


def _register_defaults() -> None:
    """Dipanggil di app startup untuk daftarkan semua dispatcher."""
    from app.modules.transaction import penghimpunan_service, penyaluran_service
    register_dispatcher('penghimpunan', penghimpunan_service.create_from_payload)
    register_dispatcher('penyaluran', penyaluran_service.create_from_payload)
    # coa, kas, bank dispatcher ditambahkan saat modul master tersedia


async def save_draft(
    entity_type: str, module: str, payload: dict,
    user_id: str, branch_code: str,
) -> dict:
    config = await repo.get_entity_config(entity_type)
    if not config:
        raise HTTPException(400, f"entity_type '{entity_type}' tidak dikenal")
    submission_id = await repo.create_submission(
        entity_type, module, branch_code, payload, user_id,
    )
    return {'id': submission_id, 'status': 'DRAFT'}


async def submit_for_auth(submission_id: int, user_id: str) -> dict:
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['submitted_by'] != user_id:
        raise HTTPException(403, 'Bukan submission Anda')
    if sub['status'] not in ('DRAFT', 'REJECTED'):
        raise HTTPException(400, f"Status '{sub['status']}' tidak bisa disubmit")
    await repo.submit_submission(submission_id)
    return {'id': submission_id, 'status': 'PENDING'}


async def approve(
    submission_id: int, authorizer_id: str,
    branch_access: str = 'single', notes: str | None = None,
) -> dict:
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['status'] != 'PENDING':
        raise HTTPException(400, f"Status '{sub['status']}' tidak bisa diotorisasi")

    level = sub['level_current']
    level_required = sub['level_required']

    await repo.insert_approval_log(submission_id, level, authorizer_id, 'APPROVED', notes)

    if level >= level_required:
        dispatcher = _DISPATCHERS.get(sub['entity_type'])
        result_entity_id = None
        if dispatcher:
            result_entity_id = await dispatcher(
                payload=dict(sub['payload']),
                user_id=sub['submitted_by'],
                branch_code=sub['branch_code'],
            )
        await repo.authorize_submission(submission_id, result_entity_id)
        return {'id': submission_id, 'status': 'AUTHORIZED', 'result_entity_id': result_entity_id}

    await repo.advance_level(submission_id, level + 1)
    return {'id': submission_id, 'status': 'PENDING', 'level_current': level + 1}


async def reject(submission_id: int, authorizer_id: str, notes: str) -> dict:
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['status'] != 'PENDING':
        raise HTTPException(400, f"Status '{sub['status']}' tidak bisa ditolak")
    await repo.insert_approval_log(submission_id, sub['level_current'], authorizer_id, 'REJECTED', notes)
    await repo.reject_submission_db(submission_id)
    return {'id': submission_id, 'status': 'REJECTED'}


async def bulk_approve(ids: list[int], authorizer_id: str, branch_access: str) -> list[dict]:
    results = []
    for sid in ids:
        try:
            results.append(await approve(sid, authorizer_id, branch_access))
        except HTTPException as e:
            results.append({'id': sid, 'error': e.detail})
    return results


async def bulk_reject(ids: list[int], authorizer_id: str, notes: str) -> list[dict]:
    results = []
    for sid in ids:
        try:
            results.append(await reject(sid, authorizer_id, notes))
        except HTTPException as e:
            results.append({'id': sid, 'error': e.detail})
    return results
```

- [ ] **Step 4: Jalankan test — pastikan PASS**

```bash
pytest tests/otorisasi/test_service.py -v
```

Expected: `4 passed`.

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/api-python/app/modules/otorisasi/service.py
git commit -m "[OTORISASI] feat(api-python): otorisasi service + dispatch registry"
```

---

## Task 5: api-python — otorisasi router + register di main

**Files:**
- Create: `apps_zakat/api-python/app/modules/otorisasi/router.py`
- Modify: `apps_zakat/api-python/app/main.py`

- [ ] **Step 1: Buat router.py**

`apps_zakat/api-python/app/modules/otorisasi/router.py`:
```python
from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from app.shared.response import ok, err
from .schema import SubmissionIn, UpdatePayloadIn, ApproveIn, RejectIn, BulkApproveIn, BulkRejectIn
from . import repo, service

router = APIRouter(prefix='/otorisasi', tags=['otorisasi'])


@router.post('/submission/')
async def create_submission(
    body: SubmissionIn,
    user_id: str = Query(...),
    branch_code: str = Query(...),
):
    try:
        result = await service.save_draft(body.entity_type, body.module, body.payload, user_id, branch_code)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.get('/submission/{submission_id}')
async def get_submission(submission_id: int):
    sub = await repo.get_submission(submission_id)
    if not sub:
        return JSONResponse(err('NOT_FOUND', 'Submission tidak ditemukan'), status_code=404)
    log = await repo.get_approval_log(submission_id)
    data = dict(sub)
    data['approval_log'] = [dict(l) for l in log]
    return JSONResponse(ok(data))


@router.put('/submission/{submission_id}')
async def update_submission(submission_id: int, body: UpdatePayloadIn, user_id: str = Query(...)):
    sub = await repo.get_submission(submission_id)
    if not sub:
        return JSONResponse(err('NOT_FOUND', 'Submission tidak ditemukan'), status_code=404)
    if sub['submitted_by'] != user_id:
        return JSONResponse(err('FORBIDDEN', 'Bukan submission Anda'), status_code=403)
    if sub['status'] not in ('DRAFT', 'REJECTED'):
        return JSONResponse(err('INVALID_STATUS', 'Tidak bisa diedit'), status_code=400)
    await repo.update_payload(submission_id, body.payload)
    return JSONResponse(ok({'id': submission_id, 'status': 'DRAFT'}))


@router.delete('/submission/{submission_id}')
async def delete_submission(submission_id: int, user_id: str = Query(...)):
    sub = await repo.get_submission(submission_id)
    if not sub:
        return JSONResponse(err('NOT_FOUND', 'Submission tidak ditemukan'), status_code=404)
    if sub['submitted_by'] != user_id:
        return JSONResponse(err('FORBIDDEN', 'Bukan submission Anda'), status_code=403)
    if sub['status'] not in ('DRAFT', 'REJECTED'):
        return JSONResponse(err('INVALID_STATUS', 'Tidak bisa dihapus'), status_code=400)
    await repo.delete_submission(submission_id)
    return JSONResponse(ok({'deleted': True}))


@router.post('/submission/{submission_id}/submit')
async def submit_submission(submission_id: int, user_id: str = Query(...)):
    try:
        result = await service.submit_for_auth(submission_id, user_id)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.get('/submissions/')
async def list_submissions(
    module: str | None = Query(None),
    entity_type: str | None = Query(None),
    status: str | None = Query(None),
    submitted_by: str | None = Query(None),
    branch: str | None = Query(None),
    branch_access: str = Query('single'),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
):
    rows, total = await repo.list_submissions(
        module=module, entity_type=entity_type, status=status,
        submitted_by=submitted_by, branch=branch, branch_access=branch_access,
        page=page, page_size=page_size,
    )
    return JSONResponse({
        'data': [dict(r) for r in rows],
        'pagination': {'page': page, 'limit': page_size, 'total': total, 'total_pages': -(-total // page_size)},
        'meta': {'request_id': ''},
    })


@router.post('/submission/{submission_id}/approve')
async def approve_submission(
    submission_id: int, body: ApproveIn,
    authorizer_id: str = Query(...),
    branch_access: str = Query('single'),
):
    try:
        result = await service.approve(submission_id, authorizer_id, branch_access, body.notes)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.post('/submission/{submission_id}/reject')
async def reject_submission(submission_id: int, body: RejectIn, authorizer_id: str = Query(...)):
    try:
        result = await service.reject(submission_id, authorizer_id, body.notes)
        return JSONResponse(ok(result))
    except HTTPException as e:
        return JSONResponse(err('ERROR', e.detail), status_code=e.status_code)


@router.post('/bulk/approve')
async def bulk_approve(body: BulkApproveIn, authorizer_id: str = Query(...), branch_access: str = Query('single')):
    results = await service.bulk_approve(body.ids, authorizer_id, branch_access)
    return JSONResponse(ok(results))


@router.post('/bulk/reject')
async def bulk_reject(body: BulkRejectIn, authorizer_id: str = Query(...)):
    results = await service.bulk_reject(body.ids, authorizer_id, body.notes)
    return JSONResponse(ok(results))


@router.get('/entity-config/')
async def get_entity_configs(module: str | None = Query(None)):
    configs = await repo.list_entity_configs(module)
    return JSONResponse(ok([dict(c) for c in configs]))
```

- [ ] **Step 2: Register di main.py**

Edit `apps_zakat/api-python/app/main.py` — tambahkan:

```python
# Tambah import (setelah import transaksi_histori_router)
from app.modules.otorisasi.router import router as otorisasi_router
from app.modules.otorisasi.service import _register_defaults
```

Di dalam `lifespan`, setelah `init_pool()`:
```python
    pool = await init_pool()
    isf_auth_pool = await init_isf_auth_pool()
    app.state.db_pool = pool
    app.state.isf_auth_pool = isf_auth_pool
    _register_defaults()   # ← tambahkan ini
    yield
```

Di bagian `include_router`:
```python
app.include_router(otorisasi_router, prefix="/api")  # ← tambahkan ini
```

- [ ] **Step 3: Smoke test endpoint**

```bash
# Restart api-python container dulu
curl -s http://localhost:8000/api/otorisasi/entity-config/?module=keuangan | jq '.data | length'
```

Expected: `6` (6 entity types keuangan).

- [ ] **Step 4: Commit**

```bash
git add apps_zakat/api-python/app/modules/otorisasi/router.py \
        apps_zakat/api-python/app/main.py
git commit -m "[OTORISASI] feat(api-python): otorisasi router + register di main + _register_defaults"
```

---

## Task 6: api-python — create_from_payload di penghimpunan + penyaluran

**Files:**
- Modify: `apps_zakat/api-python/app/modules/transaction/penghimpunan_service.py`
- Modify: `apps_zakat/api-python/app/modules/transaction/penyaluran_service.py`

- [ ] **Step 1: Tambah create_from_payload ke penghimpunan_service.py**

Tambahkan fungsi berikut di bagian akhir `penghimpunan_service.py`:
```python
async def create_from_payload(payload: dict, user_id: str, branch_code: str) -> int:
    """Dipanggil oleh otorisasi dispatch setelah submission terotorisasi."""
    req = PenghimpunanCreate(**payload)
    result = await create_penghimpunan(req, user_id, branch_code)
    return result.transaction_id
```

- [ ] **Step 2: Tambah create_from_payload ke penyaluran_service.py**

Cek signature `create_penyaluran` di `penyaluran_service.py` terlebih dahulu:
```bash
grep -n "^async def create_penyaluran" apps_zakat/api-python/app/modules/transaction/penyaluran_service.py
```

Tambahkan di bagian akhir `penyaluran_service.py`:
```python
async def create_from_payload(payload: dict, user_id: str, branch_code: str) -> int:
    """Dipanggil oleh otorisasi dispatch setelah submission terotorisasi."""
    from app.modules.transaction.penyaluran_schema import PenyaluranCreate
    req = PenyaluranCreate(**payload)
    result = await create_penyaluran(req, user_id, branch_code)
    return result.transaction_id
```

> Sesuaikan `result.transaction_id` dengan field yang dikembalikan `create_penyaluran`.

- [ ] **Step 3: Test integrasi dispatch**

```bash
# 1. Buat submission draft penghimpunan
SUB_ID=$(curl -s -X POST 'http://localhost:8000/api/otorisasi/submission/?user_id=RAIS&branch_code=001' \
  -H 'Content-Type: application/json' \
  -d '{
    "entity_type": "penghimpunan",
    "module": "keuangan",
    "payload": {
      "actual_date": "2026-06-08",
      "payment_type": "C",
      "rate": 1.0,
      "currency_code": "IDR",
      "product_branch_code": "001",
      "items": [{"product_id": 1, "account_no": "1101001001", "amount": 100000, "fund_entity": 2, "percentage_of_amil": 0}]
    }
  }' | jq -r '.data.id')
echo "Submission ID: $SUB_ID"

# 2. Submit
curl -s -X POST "http://localhost:8000/api/otorisasi/submission/$SUB_ID/submit?user_id=RAIS" | jq '.data.status'

# 3. Approve → dispatch → cek result_entity_id
curl -s -X POST "http://localhost:8000/api/otorisasi/submission/$SUB_ID/approve?authorizer_id=HADI" \
  -H 'Content-Type: application/json' -d '{"notes": "OK"}' | jq '.'
```

Expected: `status: "AUTHORIZED"`, `result_entity_id` terisi (bukan null).

- [ ] **Step 4: Commit**

```bash
git add apps_zakat/api-python/app/modules/transaction/penghimpunan_service.py \
        apps_zakat/api-python/app/modules/transaction/penyaluran_service.py
git commit -m "[OTORISASI] feat(api-python): tambah create_from_payload di penghimpunan + penyaluran service"
```

---

## Task 7: bff-api — otorisasi router

**Files:**
- Create: `apps_zakat/bff-api/app/routers/otorisasi.py`
- Modify: `apps_zakat/bff-api/app/main.py`

- [ ] **Step 1: Buat bff-api/app/routers/otorisasi.py**

```python
from __future__ import annotations
import httpx
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from app.services.auth import require_menu
from app.services.proxy import get_api_python
from app.shared.config import settings

router = APIRouter(prefix='/otorisasi', tags=['otorisasi'])

# Menu key per entity_type — mirror dari entity_config
# BFF tidak query DB; mapping ini sesuai seed entity_config
_ENTITY_MENU: dict[str, str] = {
    'penghimpunan':        'keuangan.transaksi.penghimpunan',
    'penyaluran':          'keuangan.transaksi.penyaluran',
    'upload_penghimpunan': 'keuangan.upload.penghimpunan',
    'coa':                 'keuangan.coa',
    'kas':                 'keuangan.kas',
    'bank':                'keuangan.bank',
}
_MENU_MONITORING = 'keuangan.monitoring.otorisasi'


def _session(request: Request) -> dict:
    return {
        'user_id': request.session.get('user_id', ''),
        'branch': '' if request.session.get('branch_access') == 'all'
                  else (request.session.get('primary_branch') or ''),
        'branch_access': request.session.get('branch_access', 'single'),
    }


@router.post('/submission/')
async def create_submission(request: Request):
    body = await request.json()
    entity_type = body.get('entity_type', '')
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    _ = require_menu(menu_key)(request)
    s = _session(request)
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/submission/{submission_id}')
async def get_submission(submission_id: int, request: Request):
    # Cek menu: entity's menu ATAU monitoring
    # Untuk simplifikasi: require monitoring menu (otorisator selalu punya akses lihat)
    _ = require_menu(_MENU_MONITORING)(request)
    downstream = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.put('/submission/{submission_id}')
async def update_submission(submission_id: int, request: Request):
    downstream_detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if downstream_detail.status_code != 200:
        return JSONResponse(status_code=downstream_detail.status_code, content=downstream_detail.json())
    entity_type = downstream_detail.json().get('data', {}).get('entity_type', '')
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    _ = require_menu(menu_key)(request)
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.put(url, json=body, params={'user_id': s['user_id']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.delete('/submission/{submission_id}')
async def delete_submission(submission_id: int, request: Request):
    downstream_detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    if downstream_detail.status_code != 200:
        return JSONResponse(status_code=downstream_detail.status_code, content=downstream_detail.json())
    entity_type = downstream_detail.json().get('data', {}).get('entity_type', '')
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    _ = require_menu(menu_key)(request)
    s = _session(request)
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.delete(url, params={'user_id': s['user_id']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/submission/{submission_id}/submit')
async def submit_submission(submission_id: int, request: Request):
    downstream_detail = await get_api_python(f'/api/otorisasi/submission/{submission_id}')
    entity_type = downstream_detail.json().get('data', {}).get('entity_type', '')
    menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
    _ = require_menu(menu_key)(request)
    s = _session(request)
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}/submit"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, params={'user_id': s['user_id']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/my-submissions/')
async def my_submissions(
    request: Request,
    entity_type: str | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
):
    if entity_type:
        menu_key = _ENTITY_MENU.get(entity_type, _MENU_MONITORING)
        _ = require_menu(menu_key)(request)
    s = _session(request)
    params: dict = {'submitted_by': s['user_id'], 'page': page, 'page_size': page_size}
    if entity_type:
        params['entity_type'] = entity_type
    if status:
        params['status'] = status
    downstream = await get_api_python('/api/otorisasi/submissions/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/pending/')
async def list_pending(
    request: Request,
    module: str | None = Query(None),
    entity_type: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=200),
):
    _ = require_menu(_MENU_MONITORING)(request)
    s = _session(request)
    params: dict = {'status': 'PENDING', 'page': page, 'page_size': page_size,
                    'branch_access': s['branch_access']}
    if module:
        params['module'] = module
    if entity_type:
        params['entity_type'] = entity_type
    if s['branch']:
        params['branch'] = s['branch']
    downstream = await get_api_python('/api/otorisasi/submissions/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/submission/{submission_id}/approve')
async def approve_submission(submission_id: int, request: Request):
    _ = require_menu(_MENU_MONITORING)(request)
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}/approve"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body,
                                 params={'authorizer_id': s['user_id'], 'branch_access': s['branch_access']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/submission/{submission_id}/reject')
async def reject_submission(submission_id: int, request: Request):
    _ = require_menu(_MENU_MONITORING)(request)
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/otorisasi/submission/{submission_id}/reject"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(url, json=body, params={'authorizer_id': s['user_id']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/bulk/approve')
async def bulk_approve(request: Request):
    _ = require_menu(_MENU_MONITORING)(request)
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/otorisasi/bulk/approve"
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=body,
                                 params={'authorizer_id': s['user_id'], 'branch_access': s['branch_access']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.post('/bulk/reject')
async def bulk_reject(request: Request):
    _ = require_menu(_MENU_MONITORING)(request)
    s = _session(request)
    body = await request.json()
    url = f"{settings.api_python_base_url}/api/otorisasi/bulk/reject"
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=body, params={'authorizer_id': s['user_id']})
    return JSONResponse(status_code=resp.status_code, content=resp.json())


@router.get('/entity-config/')
async def entity_configs(request: Request, module: str | None = Query(None)):
    downstream = await get_api_python('/api/otorisasi/entity-config/', params={'module': module} if module else {})
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
```

- [ ] **Step 2: Register di bff-api/app/main.py**

Tambahkan import:
```python
from app.routers.otorisasi import router as otorisasi_router
```

Di bagian `include_router` (ikuti pola yang sudah ada):
```python
app.include_router(otorisasi_router, prefix='/api')
```

- [ ] **Step 3: Smoke test via BFF (login sebagai HADI)**

```bash
TOKEN=$(curl -s -c cookies.txt http://localhost:7000/api/auth/login \
  -d '{"username":"HADI","password":"test1234"}' \
  -H 'Content-Type: application/json' | jq -r '.data.token')

curl -s -b cookies.txt 'http://localhost:7000/api/otorisasi/pending/?module=keuangan' | jq '.pagination.total'
```

Expected: integer (boleh 0 jika belum ada submission).

- [ ] **Step 4: Commit**

```bash
git add apps_zakat/bff-api/app/routers/otorisasi.py apps_zakat/bff-api/app/main.py
git commit -m "[OTORISASI] feat(bff-api): otorisasi router — submission CRUD + approve/reject + bulk"
```

---

## Task 8: web-vue — registry + route + StatusBadge

**Files:**
- Modify: `apps_zakat/web-vue/src/lib/menu/registry.ts`
- Modify: `apps_zakat/web-vue/src/router/index.ts`
- Create: `apps_zakat/web-vue/src/components/otorisasi/StatusBadge.vue`

- [ ] **Step 1: Tambah menu key ke registry.ts**

Di `src/lib/menu/registry.ts`, tambahkan di section keuangan:
```typescript
// Monitoring dan Kontrol
'keuangan.monitoring.otorisasi': 'keuangan.monitoring.otorisasi',
```

- [ ] **Step 2: Tambah route ke router/index.ts**

```typescript
{
  path: '/keuangan/monitoring/otorisasi',
  name: 'keuangan-monitoring-otorisasi',
  component: () => import('@/pages/keuangan/OtorisasiPage.vue'),
  meta: { menu_key: 'keuangan.monitoring.otorisasi' },
},
```

- [ ] **Step 3: Buat StatusBadge.vue**

`src/components/otorisasi/StatusBadge.vue`:
```vue
<script setup lang="ts">
const props = defineProps<{ status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED' }>()

const config = {
  DRAFT:      { label: 'Draft',       class: 'bg-gray-100 text-gray-600' },
  PENDING:    { label: 'Menunggu',    class: 'bg-yellow-100 text-yellow-700' },
  AUTHORIZED: { label: 'Terotorisasi',class: 'bg-green-100 text-green-700' },
  REJECTED:   { label: 'Ditolak',     class: 'bg-red-100 text-red-700' },
} as const
</script>

<template>
  <span :class="['inline-flex items-center px-2 py-0.5 rounded text-xs font-medium', config[status].class]">
    {{ config[status].label }}
  </span>
</template>
```

- [ ] **Step 4: Commit**

```bash
git add apps_zakat/web-vue/src/lib/menu/registry.ts \
        apps_zakat/web-vue/src/router/index.ts \
        apps_zakat/web-vue/src/components/otorisasi/StatusBadge.vue
git commit -m "[OTORISASI] feat(ui): menu key + route + StatusBadge component"
```

---

## Task 9: web-vue — SubmissionDetailDrawer

**Files:**
- Create: `apps_zakat/web-vue/src/components/otorisasi/SubmissionDetailDrawer.vue`

- [ ] **Step 1: Buat SubmissionDetailDrawer.vue**

```vue
<script setup lang="ts">
import { ref, watch } from 'vue'
import { X, CheckCircle, XCircle } from 'lucide-vue-next'
import { POST } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from 'primevue/usetoast'

interface ApprovalLog {
  level: number
  authorizer_id: string
  status: 'APPROVED' | 'REJECTED'
  notes: string | null
  logged_at: string
}

interface Submission {
  id: number
  entity_type: string
  entity_label: string
  branch_code: string
  payload: Record<string, any>
  status: string
  level_current: number
  level_required: number
  submitted_by: string
  submitted_at: string | null
  approval_log: ApprovalLog[]
}

const props = defineProps<{ submission: Submission | null; open: boolean }>()
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'approved', id: number): void
  (e: 'rejected', id: number): void
}>()

const toast = useToast()
const notes = ref('')
const rejectNotes = ref('')
const showRejectForm = ref(false)
const loading = ref(false)

watch(() => props.open, (val) => {
  if (!val) { notes.value = ''; rejectNotes.value = ''; showRejectForm.value = false }
})

async function approve() {
  if (!props.submission) return
  loading.value = true
  try {
    await POST(`/api/otorisasi/submission/${props.submission.id}/approve`, { notes: notes.value || null })
    toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Submission diotorisasi', life: 3000 })
    emit('approved', props.submission.id)
    emit('close')
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Otorisasi gagal', life: 3000 })
  } finally {
    loading.value = false
  }
}

async function reject() {
  if (!props.submission || !rejectNotes.value.trim()) return
  loading.value = true
  try {
    await POST(`/api/otorisasi/submission/${props.submission.id}/reject`, { notes: rejectNotes.value })
    toast.add({ severity: 'warn', summary: 'Ditolak', detail: 'Submission ditolak', life: 3000 })
    emit('rejected', props.submission.id)
    emit('close')
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Penolakan gagal', life: 3000 })
  } finally {
    loading.value = false
  }
}

function formatPayload(payload: Record<string, any>): { label: string; value: string }[] {
  // Tampilkan field penting dari payload secara generik
  const skip = ['items']
  return Object.entries(payload)
    .filter(([k]) => !skip.includes(k))
    .map(([k, v]) => ({
      label: k.replace(/_/g, ' '),
      value: typeof v === 'object' ? JSON.stringify(v) : String(v ?? '—'),
    }))
}
</script>

<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="open && submission" class="fixed inset-0 z-50 flex justify-end">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/30" @click="emit('close')" />

        <!-- Panel -->
        <div class="relative w-full max-w-lg bg-white shadow-xl flex flex-col h-full overflow-y-auto">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b">
            <div>
              <p class="text-xs text-gray-500">{{ submission.entity_label }}</p>
              <h2 class="text-base font-semibold text-gray-800">Detail Submission #{{ submission.id }}</h2>
            </div>
            <button @click="emit('close')" class="text-gray-400 hover:text-gray-600">
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- Info -->
          <div class="px-6 py-4 space-y-3 border-b">
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <p class="text-gray-400 text-xs">Inputer</p>
                <p class="font-medium">{{ submission.submitted_by }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs">Cabang</p>
                <p class="font-medium">{{ submission.branch_code }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs">Disubmit</p>
                <p class="font-medium">{{ submission.submitted_at ? dmy(submission.submitted_at) : '—' }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs">Level</p>
                <p class="font-medium">{{ submission.level_current }}/{{ submission.level_required }}</p>
              </div>
            </div>
          </div>

          <!-- Payload -->
          <div class="px-6 py-4 border-b">
            <p class="text-xs font-medium text-gray-500 uppercase mb-3">Data Input</p>
            <dl class="space-y-2 text-sm">
              <div v-for="field in formatPayload(submission.payload)" :key="field.label"
                   class="flex justify-between gap-4">
                <dt class="text-gray-500 capitalize">{{ field.label }}</dt>
                <dd class="font-medium text-right">{{ field.value }}</dd>
              </div>
            </dl>
            <!-- Items jika ada -->
            <div v-if="submission.payload.items?.length" class="mt-3">
              <p class="text-xs font-medium text-gray-500 uppercase mb-2">Item ({{ submission.payload.items.length }})</p>
              <div v-for="(item, i) in submission.payload.items" :key="i"
                   class="text-xs bg-gray-50 rounded px-2 py-1 mb-1">
                {{ item.product_name || item.product_id }} — Rp {{ item.amount?.toLocaleString('id-ID') }}
              </div>
            </div>
          </div>

          <!-- Approval Log -->
          <div v-if="submission.approval_log.length" class="px-6 py-4 border-b">
            <p class="text-xs font-medium text-gray-500 uppercase mb-3">Riwayat Otorisasi</p>
            <div v-for="log in submission.approval_log" :key="log.level"
                 class="flex items-start gap-3 text-sm mb-2">
              <span :class="log.status === 'APPROVED' ? 'text-green-500' : 'text-red-500'">
                <CheckCircle v-if="log.status === 'APPROVED'" class="w-4 h-4" />
                <XCircle v-else class="w-4 h-4" />
              </span>
              <div>
                <p class="font-medium">Level {{ log.level }} — {{ log.authorizer_id }}</p>
                <p v-if="log.notes" class="text-gray-500 text-xs">{{ log.notes }}</p>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div v-if="submission.status === 'PENDING'" class="px-6 py-4 space-y-3 mt-auto border-t">
            <div v-if="!showRejectForm" class="flex gap-3">
              <button @click="approve" :disabled="loading"
                      class="flex-1 bg-green-600 text-white py-2 rounded font-medium hover:bg-green-700 disabled:opacity-50">
                Otorisasi
              </button>
              <button @click="showRejectForm = true"
                      class="flex-1 border border-red-500 text-red-600 py-2 rounded font-medium hover:bg-red-50">
                Tolak
              </button>
            </div>
            <div v-else class="space-y-2">
              <textarea v-model="rejectNotes" rows="3" placeholder="Alasan penolakan (wajib)"
                        class="w-full border rounded px-3 py-2 text-sm resize-none" />
              <div class="flex gap-2">
                <button @click="reject" :disabled="loading || !rejectNotes.trim()"
                        class="flex-1 bg-red-600 text-white py-2 rounded font-medium hover:bg-red-700 disabled:opacity-50">
                  Konfirmasi Tolak
                </button>
                <button @click="showRejectForm = false"
                        class="px-4 py-2 border rounded text-gray-600 hover:bg-gray-50">
                  Batal
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.drawer-enter-active, .drawer-leave-active { transition: transform 0.25s ease; }
.drawer-enter-from, .drawer-leave-to { transform: translateX(100%); }
</style>
```

- [ ] **Step 2: Commit**

```bash
git add apps_zakat/web-vue/src/components/otorisasi/SubmissionDetailDrawer.vue
git commit -m "[OTORISASI] feat(ui): SubmissionDetailDrawer — panel detail + approve/reject inline"
```

---

## Task 10: web-vue — OtorisasiPage

**Files:**
- Create: `apps_zakat/web-vue/src/pages/keuangan/OtorisasiPage.vue`

- [ ] **Step 1: Buat OtorisasiPage.vue**

```vue
<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Shield } from 'lucide-vue-next'
import { GET, POST } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from 'primevue/usetoast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Paginator from 'primevue/paginator'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import SubmissionDetailDrawer from '@/components/otorisasi/SubmissionDetailDrawer.vue'

const toast = useToast()

interface SubmissionRow {
  id: number
  entity_type: string
  entity_label: string
  branch_code: string
  submitted_by: string
  submitted_at: string | null
  status: string
  level_current: number
  level_required: number
  payload: Record<string, any>
  approval_log: any[]
}

const rows = ref<SubmissionRow[]>([])
const total = ref(0)
const page = ref(0)
const pageSize = ref(25)
const loading = ref(false)
const selectedRows = ref<SubmissionRow[]>([])
const filterEntityType = ref<string | null>(null)
const drawerOpen = ref(false)
const drawerSubmission = ref<SubmissionRow | null>(null)
const bulkLoading = ref(false)
const bulkRejectNotes = ref('')
const showBulkRejectInput = ref(false)

const entityTypes = [
  { label: 'Semua', value: null },
  { label: 'Penghimpunan', value: 'penghimpunan' },
  { label: 'Penyaluran', value: 'penyaluran' },
  { label: 'Upload Penghimpunan', value: 'upload_penghimpunan' },
  { label: 'Master COA', value: 'coa' },
  { label: 'Master Kas', value: 'kas' },
  { label: 'Master Bank', value: 'bank' },
]

async function load() {
  loading.value = true
  try {
    const params: Record<string, any> = { page: page.value + 1, page_size: pageSize.value }
    if (filterEntityType.value) params.entity_type = filterEntityType.value
    const res = await GET<{ data: SubmissionRow[]; pagination: any }>('/api/otorisasi/pending/', params)
    rows.value = res.data
    total.value = res.pagination.total
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat data', life: 3000 })
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function openDetail(row: SubmissionRow) {
  // Fetch full detail dengan approval_log
  try {
    const res = await GET<{ data: SubmissionRow }>(`/api/otorisasi/submission/${row.id}`)
    drawerSubmission.value = res.data
    drawerOpen.value = true
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat detail', life: 3000 })
  }
}

async function bulkApprove() {
  const ids = selectedRows.value.map(r => r.id)
  if (!ids.length) return
  bulkLoading.value = true
  try {
    const res = await POST<{ data: any[] }>('/api/otorisasi/bulk/approve', { ids })
    const failed = res.data.filter((r: any) => r.error)
    if (failed.length) {
      toast.add({ severity: 'warn', summary: 'Sebagian gagal', detail: `${failed.length} gagal diotorisasi`, life: 4000 })
    } else {
      toast.add({ severity: 'success', summary: 'Berhasil', detail: `${ids.length} submission diotorisasi`, life: 3000 })
    }
    selectedRows.value = []
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Bulk approve gagal', life: 3000 })
  } finally {
    bulkLoading.value = false
    showBulkRejectInput.value = false
  }
}

async function bulkReject() {
  if (!bulkRejectNotes.value.trim()) return
  const ids = selectedRows.value.map(r => r.id)
  bulkLoading.value = true
  try {
    await POST('/api/otorisasi/bulk/reject', { ids, notes: bulkRejectNotes.value })
    toast.add({ severity: 'warn', summary: 'Ditolak', detail: `${ids.length} submission ditolak`, life: 3000 })
    selectedRows.value = []
    bulkRejectNotes.value = ''
    showBulkRejectInput.value = false
    await load()
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Bulk reject gagal', life: 3000 })
  } finally {
    bulkLoading.value = false
  }
}

function onPageChange(e: { page: number; rows: number }) {
  page.value = e.page
  pageSize.value = e.rows
  load()
}

function onApproved() { load() }
function onRejected() { load() }
</script>

<template>
  <div class="p-6 space-y-4">
    <div class="flex items-center gap-2 mb-4">
      <Shield class="w-5 h-5 text-blue-600" />
      <h1 class="text-xl font-semibold text-gray-800">Otorisasi</h1>
    </div>

    <!-- Filter -->
    <div class="flex gap-2 flex-wrap">
      <button v-for="et in entityTypes" :key="String(et.value)"
              @click="filterEntityType = et.value; page = 0; load()"
              :class="['px-3 py-1.5 rounded text-sm border transition',
                       filterEntityType === et.value
                         ? 'bg-blue-600 text-white border-blue-600'
                         : 'bg-white text-gray-600 border-gray-300 hover:border-blue-400']">
        {{ et.label }}
      </button>
    </div>

    <!-- Bulk actions — muncul saat ada pilihan -->
    <div v-if="selectedRows.length" class="flex items-center gap-3 bg-blue-50 border border-blue-200 rounded px-4 py-2">
      <span class="text-sm text-blue-700 font-medium">{{ selectedRows.length }} dipilih</span>
      <button @click="bulkApprove" :disabled="bulkLoading"
              class="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50">
        Otorisasi ({{ selectedRows.length }})
      </button>
      <button @click="showBulkRejectInput = !showBulkRejectInput"
              class="px-3 py-1 border border-red-500 text-red-600 text-sm rounded hover:bg-red-50">
        Tolak ({{ selectedRows.length }})
      </button>
      <div v-if="showBulkRejectInput" class="flex gap-2 flex-1">
        <input v-model="bulkRejectNotes" placeholder="Alasan penolakan"
               class="flex-1 border rounded px-2 py-1 text-sm" />
        <button @click="bulkReject" :disabled="!bulkRejectNotes.trim() || bulkLoading"
                class="px-3 py-1 bg-red-600 text-white text-sm rounded disabled:opacity-50">
          Konfirmasi
        </button>
      </div>
    </div>

    <!-- Pagination (atas) -->
    <div class="border rounded-t bg-white px-4 py-2 flex items-center justify-between">
      <span class="text-sm text-gray-500">
        Menampilkan {{ page * pageSize + 1 }}–{{ Math.min((page + 1) * pageSize, total) }} dari {{ total }} submission
      </span>
      <Paginator :rows="pageSize" :totalRecords="total" :first="page * pageSize"
                 @page="onPageChange" :rowsPerPageOptions="[25, 50]" class="text-sm" />
    </div>

    <!-- Tabel -->
    <DataTable :value="rows" v-model:selection="selectedRows" dataKey="id"
               :loading="loading" class="border border-t-0 rounded-b"
               selectionMode="multiple">
      <Column selectionMode="multiple" headerStyle="width: 3rem" />
      <Column field="entity_label" header="Jenis" />
      <Column field="submitted_by" header="Inputer" />
      <Column field="branch_code" header="Cabang" />
      <Column header="Disubmit">
        <template #body="{ data }">{{ data.submitted_at ? dmy(data.submitted_at) : '—' }}</template>
      </Column>
      <Column header="Total">
        <template #body="{ data }">
          {{ data.payload?.items
              ? 'Rp ' + data.payload.items.reduce((s: number, i: any) => s + (i.amount || 0), 0).toLocaleString('id-ID')
              : '—' }}
        </template>
      </Column>
      <Column header="Level">
        <template #body="{ data }">{{ data.level_current }}/{{ data.level_required }}</template>
      </Column>
      <Column header="Aksi">
        <template #body="{ data }">
          <button @click="openDetail(data)"
                  class="text-blue-600 text-sm hover:underline">Lihat Detail</button>
        </template>
      </Column>
    </DataTable>

    <!-- Detail Drawer -->
    <SubmissionDetailDrawer
      :open="drawerOpen"
      :submission="drawerSubmission"
      @close="drawerOpen = false"
      @approved="onApproved"
      @rejected="onRejected"
    />
  </div>
</template>
```

- [ ] **Step 2: Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/OtorisasiPage.vue
git commit -m "[OTORISASI] feat(ui): OtorisasiPage — list pending + bulk approve/reject + detail drawer"
```

---

## Task 11: web-vue — AppSidebar (Monitoring dan Kontrol)

**Files:**
- Modify: `apps_zakat/web-vue/src/components/AppSidebar.vue`

- [ ] **Step 1: Tambah section Monitoring dan Kontrol**

Buka `AppSidebar.vue`, cari section `Transaksi` di dalam sidebar keuangan. Tambahkan section `Monitoring dan Kontrol` **sebelum** section Transaksi:

```vue
<!-- Monitoring dan Kontrol -->
<SidebarSection v-if="hasMenu('keuangan.monitoring.otorisasi')" label="Monitoring dan Kontrol">
  <SidebarItem
    :to="{ name: 'keuangan-monitoring-otorisasi' }"
    label="Otorisasi"
    menu-key="keuangan.monitoring.otorisasi"
  >
    <template #icon><ShieldCheck class="w-4 h-4" /></template>
  </SidebarItem>
</SidebarSection>
```

Tambahkan import `ShieldCheck` dari lucide-vue-next di bagian `<script setup>`.

> Sesuaikan nama komponen `SidebarSection` dan `SidebarItem` dengan yang dipakai di file AppSidebar.vue aktual.

- [ ] **Step 2: Verifikasi di browser**

```bash
# Buka http://localhost:5173
# Login sebagai HADI (SPVDIST)
# Cek sidebar keuangan: "Monitoring dan Kontrol" → "Otorisasi" muncul
```

- [ ] **Step 3: Commit**

```bash
git add apps_zakat/web-vue/src/components/AppSidebar.vue
git commit -m "[OTORISASI] feat(ui): sidebar keuangan — tambah section Monitoring dan Kontrol"
```

---

## Task 12: web-vue — PenghimpunanDana pages (form + list)

**Files:**
- Modify: `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue`
- Modify: `apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaPage.vue`

- [ ] **Step 1: Ubah PenghimpunanDanaFormPage — save ke otorisasi.submission**

Cari fungsi `save()` / `handleSubmit()` di `PenghimpunanDanaFormPage.vue`. Saat ini memanggil `POST('/api/penghimpunan/', body)`. Ubah menjadi:

```typescript
async function save() {
  loading.value = true
  try {
    await POST('/api/otorisasi/submission/', {
      entity_type: 'penghimpunan',
      module: 'keuangan',
      payload: {
        actual_date: form.actualDate,
        reference_no: form.referenceNo || null,
        description: form.description,
        paid_to: form.paidTo || null,
        donor_id: form.donorId || null,
        donor_no: form.donorNo || null,
        donor_name: form.donorName || null,
        payment_type: form.paymentType,
        payment_account_no: form.paymentAccountNo || null,
        rate: form.rate,
        currency_code: form.currencyCode,
        product_branch_code: form.productBranchCode,
        items: form.items.map(i => ({
          product_id: i.product_id,
          account_no: i.account_no,
          amount: i.amount,
          description: i.description,
          fund_entity: i.fund_entity,
          percentage_of_amil: i.percentage_of_amil,
        })),
      },
    })
    toast.add({ severity: 'success', summary: 'Tersimpan', detail: 'Draft penghimpunan dibuat. Klik Submit di halaman daftar untuk mengotorisasi.', life: 5000 })
    router.push({ name: 'keuangan-transaksi-penghimpunan' })
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal menyimpan draft', life: 3000 })
  } finally {
    loading.value = false
  }
}
```

- [ ] **Step 2: Ubah PenghimpunanDanaPage — tampilkan my-submissions + badge status**

Di `PenghimpunanDanaPage.vue`, tambahkan fetch submissions paralel:

```typescript
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'

interface SubmissionRow {
  id: number
  source: 'submission'
  actual_date: string
  description: string
  total: number
  status: 'DRAFT' | 'PENDING' | 'REJECTED'
  submission_id: number
}

interface TransactionRow {
  transaction_id: number
  source: 'transaction'
  actual_date: string
  description: string | null
  amount: number
  status: 'AUTHORIZED'
  transaction_no: string
}

type ListRow = SubmissionRow | TransactionRow

const submissions = ref<SubmissionRow[]>([])
const transactions = ref<TransactionRow[]>([])

async function loadAll() {
  loading.value = true
  try {
    const [subsRes, txRes] = await Promise.all([
      GET<{ data: any[] }>('/api/otorisasi/my-submissions/', { entity_type: 'penghimpunan' }),
      GET<{ data: any[]; pagination: any }>('/api/penghimpunan/', { begin, end, page, page_size }),
    ])
    submissions.value = subsRes.data.map(s => ({
      id: s.id,
      source: 'submission',
      actual_date: s.payload?.actual_date || '',
      description: s.payload?.description || '',
      total: (s.payload?.items || []).reduce((acc: number, i: any) => acc + (i.amount || 0), 0),
      status: s.status,
      submission_id: s.id,
    }))
    transactions.value = txRes.data.map(t => ({ ...t, source: 'transaction', status: 'AUTHORIZED' }))
    total.value = txRes.pagination.total + submissions.value.length
  } finally {
    loading.value = false
  }
}
```

Di template, tambahkan kolom status dan aksi submission:
```vue
<!-- Di DataTable, tambahkan kolom Status -->
<Column header="Status">
  <template #body="{ data }">
    <StatusBadge :status="data.status" />
  </template>
</Column>

<!-- Kolom Aksi: berbeda per source -->
<Column header="Aksi">
  <template #body="{ data }">
    <template v-if="data.source === 'submission'">
      <div class="flex gap-2">
        <button v-if="data.status === 'DRAFT'"
                @click="submitForAuth(data.submission_id)"
                class="text-blue-600 text-xs hover:underline">Submit</button>
        <button v-if="data.status === 'DRAFT' || data.status === 'REJECTED'"
                @click="editSubmission(data.submission_id)"
                class="text-gray-600 text-xs hover:underline">Edit</button>
        <span v-if="data.status === 'REJECTED'"
              class="text-red-500 text-xs cursor-help" :title="data.reject_notes">Ditolak</span>
      </div>
    </template>
    <template v-else>
      <RouterLink :to="{ name: 'keuangan-transaksi-penghimpunan-detail', params: { id: data.transaction_id } }"
                  class="text-blue-600 text-xs hover:underline">Detail</RouterLink>
    </template>
  </template>
</Column>
```

```typescript
async function submitForAuth(submissionId: number) {
  loading.value = true
  try {
    await POST(`/api/otorisasi/submission/${submissionId}/submit`, {})
    toast.add({ severity: 'success', summary: 'Submitted', detail: 'Menunggu otorisasi', life: 3000 })
    await loadAll()
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Submit gagal', life: 3000 })
  } finally {
    loading.value = false
  }
}

function editSubmission(submissionId: number) {
  router.push({ name: 'keuangan-transaksi-penghimpunan-edit', params: { id: submissionId } })
}
```

- [ ] **Step 3: Tambah route edit submission**

Di `router/index.ts`:
```typescript
{
  path: '/keuangan/transaksi/penghimpunan/edit/:id',
  name: 'keuangan-transaksi-penghimpunan-edit',
  component: () => import('@/pages/keuangan/PenghimpunanDanaFormPage.vue'),
  meta: { menu_key: 'keuangan.transaksi.penghimpunan' },
},
```

Di `PenghimpunanDanaFormPage.vue`, detect mode edit:
```typescript
const route = useRoute()
const submissionId = computed(() => route.params.id ? Number(route.params.id) : null)

onMounted(async () => {
  if (submissionId.value) {
    // Load payload dari submission untuk pre-fill form
    const res = await GET<{ data: any }>(`/api/otorisasi/submission/${submissionId.value}`)
    const payload = res.data.payload
    Object.assign(form, {
      actualDate: payload.actual_date,
      referenceNo: payload.reference_no,
      description: payload.description,
      // ... dst
      items: payload.items || [],
    })
  }
})

async function save() {
  loading.value = true
  try {
    const body = { /* ... payload ... */ }
    if (submissionId.value) {
      // Update existing submission
      await PUT(`/api/otorisasi/submission/${submissionId.value}`, { payload: body })
    } else {
      // Create new draft
      await POST('/api/otorisasi/submission/', { entity_type: 'penghimpunan', module: 'keuangan', payload: body })
    }
    toast.add({ severity: 'success', summary: 'Tersimpan', detail: 'Draft tersimpan', life: 3000 })
    router.push({ name: 'keuangan-transaksi-penghimpunan' })
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal menyimpan', life: 3000 })
  } finally {
    loading.value = false
  }
}
```

> Import `PUT` dari `@/lib/api/client` — cek apakah sudah tersedia, jika belum tambahkan ke client.ts mengikuti pola GET/POST.

- [ ] **Step 4: Verifikasi di browser**

```
1. Login sebagai RAIS (ACC role)
2. Buka Keuangan → Transaksi → Penghimpunan Dana
3. Klik Tambah → isi form → Simpan
4. Cek list: baris baru muncul dengan badge DRAFT
5. Klik Submit → badge berubah ke PENDING
6. Login sebagai HADI → Monitoring dan Kontrol → Otorisasi
7. Submission RAIS muncul → Lihat Detail → Otorisasi
8. Kembali ke Penghimpunan Dana sebagai RAIS → baris hilang dari submissions, muncul di transactions
```

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaFormPage.vue \
        apps_zakat/web-vue/src/pages/keuangan/PenghimpunanDanaPage.vue \
        apps_zakat/web-vue/src/router/index.ts
git commit -m "[OTORISASI] feat(ui): penghimpunan dana — form save ke otorisasi.submission + list gabung submissions"
```

---

## Task 13: web-vue — PenyaluranDana pages

**Files:**
- Modify: `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue`
- Modify: `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue`

- [ ] **Ikuti pola yang sama persis dengan Task 12**, dengan penyesuaian:

Form save body:
```typescript
await POST('/api/otorisasi/submission/', {
  entity_type: 'penyaluran',
  module: 'keuangan',
  payload: {
    actual_date: form.actualDate,
    reference_no: form.referenceNo || null,
    description: form.description,
    paid_to: form.paidTo || null,
    payment_type: form.paymentType,
    payment_account_no: form.paymentAccountNo || null,
    fund_account_no: form.fundAccountNo || null,
    product_branch_code: form.productBranchCode,
    rate: form.rate,
    currency_code: form.currencyCode,
    items: form.items.map(i => ({
      product_id: i.product_id,
      account_no: i.account_no,
      amount: i.amount,
      description: i.description,
      fund_entity: i.fund_entity,
      ashnaf: i.ashnaf,
      dist_item_account: i.dist_item_account,
      distribution_category: i.distribution_category,
    })),
  },
})
```

List page: ganti `entity_type: 'penyaluran'` di my-submissions query, route name `keuangan-transaksi-penyaluran`.

- [ ] **Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue \
        apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue
git commit -m "[OTORISASI] feat(ui): penyaluran dana — form save ke otorisasi.submission + list gabung submissions"
```

---

## Task 14: web-vue — UploadPenghimpunan + Master Data (COA, Kas, Bank)

**Files:**
- Modify: `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue`
- Modify: `apps_zakat/web-vue/src/pages/keuangan/CoaPage.vue`
- Modify: `apps_zakat/web-vue/src/pages/keuangan/KasPage.vue`
- Modify: `apps_zakat/web-vue/src/pages/keuangan/BankPage.vue`

- [ ] **UploadPenghimpunanPage — submit ke otorisasi**

Cari aksi "Approve" / submit di `UploadPenghimpunanPage.vue`. Saat ini menggunakan menu lama `keuangan.upload.penghimpunan.approve`. Ubah menjadi submit ke `otorisasi.submission`:

```typescript
// Saat user klik "Submit untuk Otorisasi" di upload page
await POST('/api/otorisasi/submission/', {
  entity_type: 'upload_penghimpunan',
  module: 'keuangan',
  payload: {
    upload_id: uploadId,          // ID hasil parse
    rows: parsedRows,             // data yang sudah diparsing
    branch_code: branchCode,
  },
})
```

> Sesuaikan field payload dengan struktur aktual `UploadPenghimpunanPage.vue`. Cek file untuk memahami flow yang ada.
>
> Tambahkan dispatcher `upload_penghimpunan` ke `_DISPATCHERS` di `service.py` saat implementasi service upload tersedia.

- [ ] **CoaPage, KasPage, BankPage — tambah badge + my-submissions**

Untuk setiap halaman master, pola sama:

1. Tambah fetch `GET /api/otorisasi/my-submissions/?entity_type=coa` (paralel dengan fetch master)
2. Tampilkan submissions dengan badge `DRAFT` / `PENDING` / `REJECTED` di bagian atas list
3. Form add/edit → `POST /api/otorisasi/submission/` dengan `entity_type` sesuai

Contoh untuk CoaPage submit:
```typescript
await POST('/api/otorisasi/submission/', {
  entity_type: 'coa',
  module: 'keuangan',
  payload: {
    account_no: form.accountNo,
    account_name: form.accountName,
    account_type: form.accountType,
    parent_no: form.parentNo || null,
    // field COA lainnya
  },
})
```

> Dispatcher `coa`, `kas`, `bank` di `service.py` perlu diimplementasikan saat service master tersedia. Untuk sementara, jika dispatcher tidak ada, `result_entity_id` akan `null` dan status tetap `AUTHORIZED` (data manual harus dibuat oleh admin).

- [ ] **Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue \
        apps_zakat/web-vue/src/pages/keuangan/CoaPage.vue \
        apps_zakat/web-vue/src/pages/keuangan/KasPage.vue \
        apps_zakat/web-vue/src/pages/keuangan/BankPage.vue
git commit -m "[OTORISASI] feat(ui): upload penghimpunan + master COA/Kas/Bank — submit ke otorisasi.submission"
```

---

## Checklist Akhir

- [ ] `GET /api/otorisasi/entity-config/?module=keuangan` → 6 rows
- [ ] Inputer (RAIS) bisa buat draft, submit, lihat status di list
- [ ] Otorisator (HADI) bisa lihat pending, approve satuan, bulk approve
- [ ] Setelah approve → `result_entity_id` terisi, record muncul di tabel utama
- [ ] Reject → catatan wajib, inputer lihat badge merah + bisa revisi
- [ ] Badge status konsisten di semua list page
- [ ] Sidebar Monitoring dan Kontrol muncul untuk user dengan menu `keuangan.monitoring.otorisasi`
- [ ] Bulk reject: input alasan → konfirmasi → semua ditolak

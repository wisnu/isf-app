# Upload Penghimpunan Multi-Bank — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bangun fitur upload transaksi penghimpunan ZIS dari file XLS/XLSX — alur dua-tahap (draft oleh uploader, otorisasi oleh SPVKEU) — lengkap dengan commit transaksi akuntansi ke DB.

**Architecture:** Frontend Vue → BFF (session + menu gating) → api-python (parse/store/approve) → PostgreSQL (mziss_laz). Report-api tidak disentuh (read-only). Approve endpoint melakukan full DB commit: transaction + transactionitem + accounttransactionitem + journal + balance updates dalam satu asyncpg transaction.

**Tech Stack:** Python 3.12, FastAPI, asyncpg, openpyxl (XLSX), xlrd (XLS), Vue 3 + TypeScript, Pydantic v2.

---

## File Map

**Create:**
- `infra/db/migrations/transaction/009_upload_penghimpunan.sql`
- `apps_zakat/api-python/app/modules/transaction/__init__.py`
- `apps_zakat/api-python/app/modules/transaction/schema.py`
- `apps_zakat/api-python/app/modules/transaction/parse.py`
- `apps_zakat/api-python/app/modules/transaction/repository.py`
- `apps_zakat/api-python/app/modules/transaction/service.py`
- `apps_zakat/api-python/app/modules/transaction/commit.py`
- `apps_zakat/api-python/app/modules/transaction/template.py`
- `apps_zakat/api-python/app/modules/transaction/router.py`
- `apps_zakat/api-python/tests/test_upload_penghimpunan.py`
- `apps_zakat/bff-api/app/routers/transaction.py`
- `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue`
- `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanListPage.vue`
- `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanDetailPage.vue`
- `testing/e2e-upload-penghimpunan.sh`

**Modify:**
- `apps_zakat/api-python/pyproject.toml` — tambah xlrd
- `apps_zakat/api-python/app/main.py` — include transaction_router
- `apps_zakat/bff-api/app/services/proxy.py` — tambah post_multipart_api_python
- `apps_zakat/bff-api/app/main.py` — include transaction_router
- `apps_zakat/web-vue/src/lib/menu/registry.ts` — tambah 2 menu key
- `apps_zakat/web-vue/src/components/AppSidebar.vue` — tambah Upload section
- `apps_zakat/web-vue/src/router/index.ts` — tambah 3 route
- `infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql` — tambah menu + role_menu

---

## Task 1: DB Migration

**Files:**
- Create: `infra/db/migrations/transaction/009_upload_penghimpunan.sql`

- [ ] **Cek nomor migration terakhir di `infra/db/migrations/transaction/`** — kalau direktori belum ada, buat dulu. Kalau sudah ada file lain, sesuaikan angka 009.

- [ ] **Tulis migration SQL:**

```sql
-- 009_upload_penghimpunan.sql
-- Kolom legacy yang belum ada di schema dump batchuploaditem
ALTER TABLE transaction.batchuploaditem
  ADD COLUMN IF NOT EXISTS amountzakatperusahaan numeric(30,6) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS amountinfaqterikat     numeric(30,6) DEFAULT 0,
  ADD COLUMN IF NOT EXISTS amounttitipanqurban    numeric(30,6) DEFAULT 0;

-- Status otorisasi batch: P=pending, A=approved
ALTER TABLE transaction.batchupload
  ADD COLUMN IF NOT EXISTS authstatus character varying(1) DEFAULT 'P';
```

- [ ] **Apply ke mziss_laz:**

```bash
PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz \
  -f infra/db/migrations/transaction/009_upload_penghimpunan.sql
```

Expected: `ALTER TABLE` (×4), no errors.

- [ ] **Verify:**

```bash
PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz \
  -c "\d transaction.batchuploaditem" | grep -E "amountzakat|amountinfaq|amounttitipan"
PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz \
  -c "\d transaction.batchupload" | grep authstatus
```

Expected: kolom-kolom muncul.

- [ ] **Commit:**

```bash
git add infra/db/migrations/transaction/009_upload_penghimpunan.sql
git commit -m "[UPLOAD-PENGHIMPUNAN] chore(db): migration tambah kolom batchuploaditem + authstatus"
```

---

## Task 2: Tambah Dependency xlrd

**Files:**
- Modify: `apps_zakat/api-python/pyproject.toml`

- [ ] **Edit pyproject.toml** — tambah `xlrd>=2.0` di dependencies:

```toml
dependencies = [
  "fastapi>=0.115",
  "uvicorn[standard]>=0.30",
  "pydantic>=2.7",
  "pydantic-settings>=2.4",
  "asyncpg>=0.30",
  "openpyxl>=3.1",
  "xlrd>=2.0",
]
```

- [ ] **Rebuild image** (sesuai CLAUDE.md, source di bind-mount — cukup `pip install` lokal untuk dev, atau rebuild kalau dibutuhkan):

```bash
cd apps_zakat/api-python
pip install "xlrd>=2.0"
```

- [ ] **Verify import:**

```bash
python -c "import xlrd; print(xlrd.__version__)"
```

Expected: version ≥ 2.0.

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/pyproject.toml
git commit -m "[UPLOAD-PENGHIMPUNAN] chore(api-python): tambah xlrd untuk parsing .xls"
```

---

## Task 3: api-python — schema.py + parse.py

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/__init__.py`
- Create: `apps_zakat/api-python/app/modules/transaction/schema.py`
- Create: `apps_zakat/api-python/app/modules/transaction/parse.py`
- Create: `apps_zakat/api-python/tests/test_upload_penghimpunan.py`

- [ ] **Buat `__init__.py` kosong:**

```python
# apps_zakat/api-python/app/modules/transaction/__init__.py
```

- [ ] **Buat `schema.py`:**

```python
# apps_zakat/api-python/app/modules/transaction/schema.py
from __future__ import annotations
from pydantic import BaseModel


PRODUCT_ID_MAP: dict[str, int] = {
    'ZakatProfesi':    518,
    'ZakatMaal':       5,
    'ZakatFitrah':     141,
    'ZakatPerusahaan': 575,
    'Infaq':           95,
    'InfaqTerikat':    572,
    'DPU':             145,
    'AnakYatim':       143,
    'AnakAsuh':        142,
    'TitipanWakaf':    12,
    'TitipanQurban':   574,
    'Qurban':          144,
    'NonHalal':        516,
    'Fidyah':          569,
}

FUND_ENTITY_MAP: dict[str, int] = {
    'Z': 1, 'T': 2, 'I': 2, 'W': 3, 'A': 4, 'N': 5,
}

PRODUCT_KEYS = list(PRODUCT_ID_MAP.keys())


class ParsedRow(BaseModel):
    row_no: int
    no_rekening: str
    tanggal: str          # ISO YYYY-MM-DD
    keterangan: str
    no_ref: str
    total_kredit: float
    zakat_profesi: float
    zakat_maal: float
    zakat_fitrah: float
    zakat_perusahaan: float
    infaq: float
    infaq_terikat: float
    dpu: float
    anak_yatim: float
    anak_asuh: float
    titipan_wakaf: float
    titipan_qurban: float
    qurban: float
    non_halal: float
    fidyah: float
    status: str           # 'valid', 'warning', 'invalid'
    pesan: str


class DraftRequest(BaseModel):
    filename: str
    branch_code: str
    rows: list[ParsedRow]


class DraftResponse(BaseModel):
    batch_id: int
    total_valid: int
    total_warning: int


class BatchSummary(BaseModel):
    batch_id: int
    filename: str
    upload_date: str       # ISO
    upload_user: str
    branch_code: str
    total_record: int
    total_amount: float
    authstatus: str        # P / A


class BatchItem(BaseModel):
    batch_item_id: int
    row_no: int
    no_rekening: str
    tanggal: str           # ISO
    keterangan: str
    no_ref: str
    total_kredit: float
    zakat_profesi: float
    zakat_maal: float
    zakat_fitrah: float
    zakat_perusahaan: float
    infaq: float
    infaq_terikat: float
    dpu: float
    anak_yatim: float
    anak_asuh: float
    titipan_wakaf: float
    titipan_qurban: float
    qurban: float
    non_halal: float
    fidyah: float
    status: str
    pesan: str
    transaction_no: str | None


class BatchDetail(BaseModel):
    batch_id: int
    filename: str
    upload_date: str
    upload_user: str
    branch_code: str
    total_record: int
    total_amount: float
    authstatus: str
    authorized_user: str | None
    items: list[BatchItem]


class ApproveResult(BaseModel):
    batch_id: int
    total_committed: int
```

- [ ] **Buat `parse.py`:**

```python
# apps_zakat/api-python/app/modules/transaction/parse.py
from __future__ import annotations

import re
from datetime import datetime
from io import BytesIO

from app.modules.transaction.schema import PRODUCT_KEYS, ParsedRow


def _to_float(v: object) -> float:
    if v is None or v == '':
        return 0.0
    try:
        return float(str(v).replace(',', ''))
    except (ValueError, TypeError):
        return 0.0


def _parse_date_dmy(raw: object) -> str | None:
    """DD/MM/YYYY → ISO YYYY-MM-DD. Returns None if invalid."""
    s = str(raw).strip() if raw else ''
    m = re.fullmatch(r'(\d{1,2})/(\d{1,2})/(\d{4})', s)
    if not m:
        return None
    d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    try:
        datetime(y, mo, d)
        return f'{y:04d}-{mo:02d}-{d:02d}'
    except ValueError:
        return None


def _validate_row(
    row_no: int,
    cols: list,
    known_accounts: set[str],
    seen_refs: set[tuple],
) -> ParsedRow | None:
    """Parse + validate one row. Returns None if TotalKredit <= 0 (skip)."""
    def col(i: int) -> object:
        return cols[i] if i < len(cols) else None

    total_kredit = _to_float(col(4))
    if total_kredit <= 0:
        return None

    no_rekening = str(col(0) or '').strip()
    tanggal_raw = col(1)
    keterangan = str(col(2) or '').strip()
    no_ref = str(col(3) or '').strip()

    amounts = [_to_float(col(5 + i)) for i in range(14)]
    # ZakatProfesi, ZakatMaal, ZakatFitrah, ZakatPerusahaan, Infaq,
    # InfaqTerikat, DPU, AnakYatim, AnakAsuh, TitipanWakaf,
    # TitipanQurban, Qurban, NonHalal, Fidyah
    (zp, zm, zf, zper, infaq, infaq_t, dpu,
     ay, aa, tw, tq, qurban, nh, fidyah) = amounts

    status = 'valid'
    pesan = ''
    msgs: list[str] = []

    tanggal_iso = _parse_date_dmy(tanggal_raw)
    if tanggal_iso is None:
        status = 'invalid'
        msgs.append('Format tanggal tidak valid')

    if no_rekening not in known_accounts:
        status = 'invalid'
        msgs.append('Nomor rekening tidak terdaftar')

    detail_sum = sum(amounts)
    if abs(detail_sum - total_kredit) > 0.01:
        if status == 'valid':
            status = 'warning'
        msgs.append('Total detail tidak sesuai nominal')

    ref_key = (no_ref, tanggal_iso or '', total_kredit)
    if ref_key in seen_refs:
        if status == 'valid':
            status = 'warning'
        msgs.append('Sudah pernah di-upload')
    else:
        seen_refs.add(ref_key)

    if msgs:
        pesan = '; '.join(msgs)

    return ParsedRow(
        row_no=row_no,
        no_rekening=no_rekening,
        tanggal=tanggal_iso or '',
        keterangan=keterangan,
        no_ref=no_ref,
        total_kredit=total_kredit,
        zakat_profesi=zp, zakat_maal=zm, zakat_fitrah=zf,
        zakat_perusahaan=zper, infaq=infaq, infaq_terikat=infaq_t,
        dpu=dpu, anak_yatim=ay, anak_asuh=aa,
        titipan_wakaf=tw, titipan_qurban=tq,
        qurban=qurban, non_halal=nh, fidyah=fidyah,
        status=status, pesan=pesan,
    )


def parse_xlsx(data: bytes, known_accounts: set[str],
               seen_refs: set[tuple]) -> list[ParsedRow]:
    from openpyxl import load_workbook
    wb = load_workbook(BytesIO(data), read_only=True, data_only=True)
    ws = wb.active
    rows: list[ParsedRow] = []
    consecutive_empty = 0
    for excel_row_no, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        cols = list(row)
        if not cols or (cols[0] is None and (len(cols) < 2 or cols[1] is None)):
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break
            continue
        consecutive_empty = 0
        parsed = _validate_row(excel_row_no, cols, known_accounts, seen_refs)
        if parsed is not None:
            rows.append(parsed)
    wb.close()
    return rows


def parse_xls(data: bytes, known_accounts: set[str],
              seen_refs: set[tuple]) -> list[ParsedRow]:
    import xlrd
    wb = xlrd.open_workbook(file_contents=data)
    ws = wb.sheet_by_index(0)
    rows: list[ParsedRow] = []
    consecutive_empty = 0
    for r in range(1, ws.nrows):  # skip header row 0
        raw_cols = [ws.cell_value(r, c) for c in range(ws.ncols)]
        if not raw_cols or (raw_cols[0] == '' and (len(raw_cols) < 2 or raw_cols[1] == '')):
            consecutive_empty += 1
            if consecutive_empty >= 2:
                break
            continue
        consecutive_empty = 0
        # xlrd returns float for numeric cells — handle date cells
        date_val = raw_cols[1] if len(raw_cols) > 1 else None
        if isinstance(date_val, float):
            try:
                t = xlrd.xldate_as_tuple(date_val, wb.datemode)
                raw_cols[1] = f'{t[2]:02d}/{t[1]:02d}/{t[0]:04d}'
            except Exception:
                pass
        parsed = _validate_row(r + 1, raw_cols, known_accounts, seen_refs)
        if parsed is not None:
            rows.append(parsed)
    return rows


def parse_file(filename: str, data: bytes,
               known_accounts: set[str],
               seen_refs: set[tuple]) -> list[ParsedRow]:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext == 'xlsx':
        return parse_xlsx(data, known_accounts, seen_refs)
    elif ext == 'xls':
        return parse_xls(data, known_accounts, seen_refs)
    else:
        raise ValueError(f'Format tidak didukung: {ext}. Gunakan .xls atau .xlsx')
```

- [ ] **Tulis unit tests:**

```python
# apps_zakat/api-python/tests/test_upload_penghimpunan.py
from __future__ import annotations
import io
from openpyxl import Workbook
from app.modules.transaction.parse import parse_xlsx, parse_xls, _parse_date_dmy


def _make_xlsx(rows: list[list]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.append(['NoRek','Tanggal','Ket','Ref','Total','ZP','ZM','ZF','ZPer',
               'Infaq','InfaqT','DPU','AY','AA','TW','TQ','Qurban','NH','Fidyah'])
    for r in rows:
        ws.append(r)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_parse_date_dmy_valid():
    assert _parse_date_dmy('01/06/2026') == '2026-06-01'


def test_parse_date_dmy_invalid():
    assert _parse_date_dmy('2026-06-01') is None
    assert _parse_date_dmy('32/01/2026') is None
    assert _parse_date_dmy('') is None


def test_parse_xlsx_valid_row():
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Transfer zakat', 'REF001', 500000,
         300000, 200000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert len(rows) == 1
    assert rows[0].status == 'valid'
    assert rows[0].tanggal == '2026-06-01'
    assert rows[0].total_kredit == 500000
    assert rows[0].zakat_profesi == 300000
    assert rows[0].zakat_maal == 200000


def test_parse_xlsx_invalid_date():
    data = _make_xlsx([
        ['1234567890', 'bukan-tanggal', 'Transfer', 'REF001', 500000,
         500000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert rows[0].status == 'invalid'
    assert 'tanggal' in rows[0].pesan.lower()


def test_parse_xlsx_unknown_account():
    data = _make_xlsx([
        ['9999999', '01/06/2026', 'Transfer', 'REF001', 100000,
         100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts=set(), seen_refs=set())
    assert rows[0].status == 'invalid'
    assert 'rekening' in rows[0].pesan.lower()


def test_parse_xlsx_total_mismatch_gives_warning():
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Transfer', 'REF001', 500000,
         200000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # detail=200k, total=500k
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert rows[0].status == 'warning'
    assert 'nominal' in rows[0].pesan.lower()


def test_parse_xlsx_skips_zero_kredit():
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Zero', 'REF001', 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=set())
    assert rows == []


def test_parse_xlsx_duplicate_ref_gives_warning():
    seen: set = {('REF001', '2026-06-01', 100000.0)}
    data = _make_xlsx([
        ['1234567890', '01/06/2026', 'Transfer', 'REF001', 100000,
         100000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    rows = parse_xlsx(data, known_accounts={'1234567890'}, seen_refs=seen)
    assert rows[0].status == 'warning'
    assert 'pernah' in rows[0].pesan.lower()
```

- [ ] **Run tests:**

```bash
cd apps_zakat/api-python
python -m pytest tests/test_upload_penghimpunan.py -v
```

Expected: 8 tests PASS.

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaction/ \
        apps_zakat/api-python/tests/test_upload_penghimpunan.py
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(api-python): schema + Excel parser dengan validasi"
```

---

## Task 4: api-python — repository.py

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/repository.py`

- [ ] **Buat `repository.py`:**

```python
# apps_zakat/api-python/app/modules/transaction/repository.py
from __future__ import annotations
from app.shared.db import fetch_all, fetch_one, get_pool


async def get_bank_accounts() -> set[str]:
    """Return set of known bankaccountno from transaction.cashaccount."""
    rows = await fetch_all(
        "SELECT bankaccountno FROM transaction.cashaccount WHERE bankaccountno IS NOT NULL"
    )
    return {r['bankaccountno'] for r in rows if r['bankaccountno']}


async def get_existing_refs() -> set[tuple]:
    """Return set of (referenceno, transactiondate::date::text, amount) already in batchuploaditem."""
    rows = await fetch_all(
        """SELECT referenceno, to_char(transactiondate, 'YYYY-MM-DD') AS tdate, amount
           FROM transaction.batchuploaditem
           WHERE referenceno IS NOT NULL"""
    )
    return {(r['referenceno'], r['tdate'] or '', float(r['amount'] or 0)) for r in rows}


async def insert_batch(
    *,
    filename: str,
    branch_code: str,
    upload_user: str,
    total_record: int,
    total_amount: float,
) -> int:
    """Insert into transaction.batchupload, return batchid."""
    from datetime import datetime, timezone
    pool = get_pool()
    async with pool.acquire() as conn:
        batch_id = await conn.fetchval(
            "SELECT nextval('transaction.seq_batchupload')"
        )
        await conn.execute(
            """INSERT INTO transaction.batchupload
               (batchid, filename, branchcode, uploaduser, uploaddate,
                totalrecord, totalamount, batchuploadtype, authstatus)
               VALUES ($1,$2,$3,$4,$5,$6,$7,'M','P')""",
            batch_id, filename, branch_code, upload_user,
            datetime.now(timezone.utc), total_record, total_amount,
        )
    return batch_id


async def insert_batch_items(batch_id: int, rows: list[dict]) -> None:
    """Bulk insert batchuploaditem rows."""
    pool = get_pool()
    async with pool.acquire() as conn:
        for row in rows:
            item_id = await conn.fetchval(
                "SELECT nextval('transaction.seq_batchuploaditem')"
            )
            await conn.execute(
                """INSERT INTO transaction.batchuploaditem
                   (batchitemid, batchid, transactiondate, amount, description,
                    referenceno, bankaccountno, validationstatus,
                    amountzakatprofesi, amountzakatmaal, amountzakatfitrah,
                    amountzakatperusahaan, amountinfaq, amountinfaqterikat,
                    amountdpu, amountanakyatim, amountanakasuh,
                    amounttitipanwakaf, amounttitipanqurban,
                    amountqurban, amountnonhalal, amountfidyah)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,$8,
                           $9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22)""",
                item_id, batch_id,
                row['tanggal'], row['total_kredit'], row['keterangan'],
                row['no_ref'], row['no_rekening'],
                'T' if row['status'] == 'valid' else 'F',
                row['zakat_profesi'], row['zakat_maal'], row['zakat_fitrah'],
                row['zakat_perusahaan'], row['infaq'], row['infaq_terikat'],
                row['dpu'], row['anak_yatim'], row['anak_asuh'],
                row['titipan_wakaf'], row['titipan_qurban'],
                row['qurban'], row['non_halal'], row['fidyah'],
            )


async def list_batches(
    begin: str | None,
    end: str | None,
    status: str | None,
) -> list[dict]:
    conds = ["batchuploadtype = 'M'"]
    params: list = []
    if begin:
        params.append(begin)
        conds.append(f"uploaddate::date >= ${len(params)}")
    if end:
        params.append(end)
        conds.append(f"uploaddate::date <= ${len(params)}")
    if status and status.upper() in ('P', 'A'):
        params.append(status.upper())
        conds.append(f"COALESCE(authstatus,'P') = ${len(params)}")
    where = 'WHERE ' + ' AND '.join(conds)
    rows = await fetch_all(
        f"""SELECT batchid, filename, uploaddate, uploaduser, branchcode,
                   COALESCE(totalrecord,0) AS totalrecord,
                   COALESCE(totalamount,0) AS totalamount,
                   COALESCE(authstatus,'P') AS authstatus
            FROM transaction.batchupload
            {where}
            ORDER BY uploaddate DESC
            LIMIT 500""",
        *params,
    )
    return rows


async def get_batch(batch_id: int) -> dict | None:
    return await fetch_one(
        """SELECT batchid, filename, uploaddate, uploaduser, branchcode,
                  COALESCE(totalrecord,0) AS totalrecord,
                  COALESCE(totalamount,0) AS totalamount,
                  COALESCE(authstatus,'P') AS authstatus,
                  authorizeduser
           FROM transaction.batchupload
           WHERE batchid = $1""",
        batch_id,
    )


async def get_batch_items(batch_id: int) -> list[dict]:
    return await fetch_all(
        """SELECT batchitemid, transactiondate, amount, description, referenceno,
                  bankaccountno, validationstatus,
                  amountzakatprofesi, amountzakatmaal, amountzakatfitrah,
                  amountzakatperusahaan, amountinfaq, amountinfaqterikat,
                  amountdpu, amountanakyatim, amountanakasuh,
                  amounttitipanwakaf, amounttitipanqurban,
                  amountqurban, amountnonhalal, amountfidyah,
                  transactionno
           FROM transaction.batchuploaditem
           WHERE batchid = $1
           ORDER BY batchitemid""",
        batch_id,
    )
```

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaction/repository.py
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(api-python): repository — batch CRUD + bank account lookup"
```

---

## Task 5: api-python — service.py

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/service.py`

- [ ] **Buat `service.py`:**

```python
# apps_zakat/api-python/app/modules/transaction/service.py
from __future__ import annotations
from app.modules.transaction import repository as repo
from app.modules.transaction.parse import parse_file
from app.modules.transaction.schema import (
    BatchDetail, BatchItem, BatchSummary, DraftResponse, ParsedRow,
)


async def parse_upload(filename: str, data: bytes) -> list[ParsedRow]:
    known_accounts = await repo.get_bank_accounts()
    seen_refs = await repo.get_existing_refs()
    return parse_file(filename, data, known_accounts, seen_refs)


async def save_draft(
    filename: str,
    branch_code: str,
    upload_user: str,
    rows: list[ParsedRow],
) -> DraftResponse:
    saveable = [r for r in rows if r.status != 'invalid']
    if not saveable:
        raise ValueError('Tidak ada baris yang bisa disimpan (semua invalid)')

    total_amount = sum(r.total_kredit for r in saveable)
    batch_id = await repo.insert_batch(
        filename=filename,
        branch_code=branch_code,
        upload_user=upload_user,
        total_record=len(saveable),
        total_amount=total_amount,
    )
    await repo.insert_batch_items(batch_id, [r.model_dump() for r in saveable])
    valid_count = sum(1 for r in saveable if r.status == 'valid')
    warning_count = sum(1 for r in saveable if r.status == 'warning')
    return DraftResponse(
        batch_id=batch_id,
        total_valid=valid_count,
        total_warning=warning_count,
    )


async def list_batches(
    begin: str | None = None,
    end: str | None = None,
    status: str | None = None,
) -> list[BatchSummary]:
    rows = await repo.list_batches(begin, end, status)
    return [
        BatchSummary(
            batch_id=r['batchid'],
            filename=r['filename'] or '',
            upload_date=str(r['uploaddate'])[:10] if r['uploaddate'] else '',
            upload_user=r['uploaduser'] or '',
            branch_code=r['branchcode'] or '',
            total_record=int(r['totalrecord'] or 0),
            total_amount=float(r['totalamount'] or 0),
            authstatus=r['authstatus'] or 'P',
        )
        for r in rows
    ]


async def get_batch_detail(batch_id: int) -> BatchDetail | None:
    batch = await repo.get_batch(batch_id)
    if not batch:
        return None
    items_raw = await repo.get_batch_items(batch_id)
    items = [
        BatchItem(
            batch_item_id=it['batchitemid'],
            row_no=i + 1,
            no_rekening=it['bankaccountno'] or '',
            tanggal=str(it['transactiondate'])[:10] if it['transactiondate'] else '',
            keterangan=it['description'] or '',
            no_ref=it['referenceno'] or '',
            total_kredit=float(it['amount'] or 0),
            zakat_profesi=float(it['amountzakatprofesi'] or 0),
            zakat_maal=float(it['amountzakatmaal'] or 0),
            zakat_fitrah=float(it['amountzakatfitrah'] or 0),
            zakat_perusahaan=float(it['amountzakatperusahaan'] or 0),
            infaq=float(it['amountinfaq'] or 0),
            infaq_terikat=float(it['amountinfaqterikat'] or 0),
            dpu=float(it['amountdpu'] or 0),
            anak_yatim=float(it['amountanakyatim'] or 0),
            anak_asuh=float(it['amountanakasuh'] or 0),
            titipan_wakaf=float(it['amounttitipanwakaf'] or 0),
            titipan_qurban=float(it['amounttitipanqurban'] or 0),
            qurban=float(it['amountqurban'] or 0),
            non_halal=float(it['amountnonhalal'] or 0),
            fidyah=float(it['amountfidyah'] or 0),
            status='valid' if it['validationstatus'] == 'T' else 'warning',
            pesan='',
            transaction_no=it['transactionno'],
        )
        for i, it in enumerate(items_raw)
    ]
    return BatchDetail(
        batch_id=batch['batchid'],
        filename=batch['filename'] or '',
        upload_date=str(batch['uploaddate'])[:10] if batch['uploaddate'] else '',
        upload_user=batch['uploaduser'] or '',
        branch_code=batch['branchcode'] or '',
        total_record=int(batch['totalrecord'] or 0),
        total_amount=float(batch['totalamount'] or 0),
        authstatus=batch['authstatus'] or 'P',
        authorized_user=batch['authorizeduser'],
        items=items,
    )
```

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaction/service.py
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(api-python): service layer — parse/draft/list/detail"
```

---

## Task 6: api-python — template.py

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/template.py`

- [ ] **Buat `template.py`:**

```python
# apps_zakat/api-python/app/modules/transaction/template.py
from __future__ import annotations
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


HEADERS = [
    'NoRekening', 'Tanggal (DD/MM/YYYY)', 'Keterangan', 'NoRef', 'TotalKredit',
    'ZakatProfesi', 'ZakatMaal', 'ZakatFitrah', 'ZakatPerusahaan',
    'Infaq', 'InfaqTerikat', 'DPU', 'AnakYatim', 'AnakAsuh',
    'TitipanWakaf', 'TitipanQurban', 'Qurban', 'NonHalal', 'Fidyah',
]


def build_template() -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = 'UploadPenghimpunan'
    header_fill = PatternFill('solid', fgColor='1E40AF')
    header_font = Font(bold=True, color='FFFFFF')
    for col_idx, h in enumerate(HEADERS, 1):
        cell = ws.cell(row=1, column=col_idx, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 35
    ws.column_dimensions['D'].width = 15
    for col in range(5, len(HEADERS) + 1):
        ws.column_dimensions[chr(64 + col)].width = 14
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()
```

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaction/template.py
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(api-python): template XLSX generator"
```

---

## Task 7: api-python — commit.py (Transaction Commit)

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/commit.py`

> ⚠️ **Sebelum menulis SQL di task ini**, jalankan dulu di DB lokal:
> ```bash
> PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz -c "\d transaction.productaccount"
> PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz -c "\d transaction.journal"
> PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz \
>   -c "SELECT journal_no FROM transaction.journal LIMIT 3"
> ```
> Verifikasi format journal_no yang ada (mis. `J001-2026-001-0000001`) sebelum melanjutkan.

- [ ] **Buat `commit.py`:**

```python
# apps_zakat/api-python/app/modules/transaction/commit.py
"""Full transaction commit untuk approve batch upload penghimpunan."""
from __future__ import annotations

import re
from datetime import datetime, timezone

from app.modules.transaction.schema import FUND_ENTITY_MAP, PRODUCT_ID_MAP
from app.shared.db import get_pool


_DONOR_PATTERNS = [
    re.compile(r'DARI\s+(?P<NAMA>[A-Z][A-Z\s]+)\s+TRANSFER', re.IGNORECASE),
    re.compile(r'TRANSFER\s+DARI\s+(?P<NAMA>[A-Z][A-Z\s]+)', re.IGNORECASE),
    re.compile(r'TRF\s+DARI\s+-?\s*(?P<NAMA>[A-Z][A-Z\s]+)', re.IGNORECASE),
]


def _extract_donor_name(description: str) -> str | None:
    for pat in _DONOR_PATTERNS:
        m = pat.search(description.upper())
        if m:
            return m.group('NAMA').strip()
    return None


async def _get_default_donor(conn) -> dict:
    pg = await conn.fetchrow(
        "SELECT nilai_parameter FROM transaction.parameterglobal WHERE kode_parameter='DEF_DONOR'"
    )
    if not pg:
        raise RuntimeError("Parameter DEF_DONOR tidak ditemukan di transaction.parameterglobal")
    donor_id = int(pg['nilai_parameter'])
    donor = await conn.fetchrow(
        "SELECT donorid, donorname, donorno, donortype FROM fund.donor WHERE donorid=$1",
        donor_id,
    )
    if not donor:
        raise RuntimeError(f"Default donor ID {donor_id} tidak ditemukan")
    return dict(donor)


async def _lookup_product_accounts(conn, branch_code: str) -> dict[str, dict]:
    """Return mapping produk_name → {accountno, fundentity, percentage_amil}."""
    result = {}
    for product_name, product_id in PRODUCT_ID_MAP.items():
        # productaccount maps productid → accountno (global, no branchcode)
        # financialaccount has branchcode — join to filter by branch
        row = await conn.fetchrow(
            """SELECT pa.accountno, p.fundcategory, p.percentageofamilfunds
               FROM transaction.productaccount pa
               JOIN transaction.product p ON pa.productid = p.productid
               WHERE pa.productid = $1
               LIMIT 1""",
            product_id,
        )
        if row:
            fc = (row['fundcategory'] or 'I').strip()
            result[product_name] = {
                'accountno': row['accountno'],
                'fundentity': FUND_ENTITY_MAP.get(fc, 2),
                'percentage_amil': float(row['percentageofamilfunds'] or 0),
            }
    return result


async def _lookup_bank_account(conn, bankaccountno: str) -> dict:
    row = await conn.fetchrow(
        """SELECT accountno, cashcode FROM transaction.cashaccount
           WHERE bankaccountno = $1 LIMIT 1""",
        bankaccountno,
    )
    if not row:
        raise RuntimeError(f"Nomor rekening bank {bankaccountno!r} tidak ditemukan")
    return dict(row)


async def _get_or_create_donor(conn, description: str, default_donor: dict) -> dict:
    name = _extract_donor_name(description)
    if name:
        row = await conn.fetchrow(
            "SELECT donorid, donorname, donorno, donortype FROM fund.donor "
            "WHERE UPPER(donorname) = UPPER($1) LIMIT 1",
            name,
        )
        if row:
            return dict(row)
    return default_donor


async def _generate_journal_no(conn, branch_code: str, year: int) -> str:
    seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
    return f'J{branch_code}-{year}-{seq:07d}'


async def _commit_item(conn, item: dict, product_accounts: dict,
                       branch_code: str, inputer: str, default_donor: dict) -> str:
    """Commit one batchuploaditem. Returns transactionno."""
    now = datetime.now(timezone.utc)
    trans_date = item['transactiondate']
    year = trans_date.year if hasattr(trans_date, 'year') else int(str(trans_date)[:4])

    donor = await _get_or_create_donor(conn, item['description'] or '', default_donor)
    bank = await _lookup_bank_account(conn, item['bankaccountno'])

    # 1. INSERT transaction
    trans_id = await conn.fetchval("SELECT nextval('transaction.seq_transaction')")
    await conn.execute(
        """INSERT INTO transaction.transaction
           (transactionid, transactiondate, actualdate, transactiontime,
            description, inputer, transactioncode, branchcode,
            channelcode, donorid, donorno, donorname,
            amount, currencycode, channelaccountno, authstatus, isposted)
           VALUES ($1,$2,$2,$3,$4,$5,'SDMULTI',$6,'A',$7,$8,$9,$10,'IDR',$11,'A','T')""",
        trans_id, trans_date, now,
        (item['description'] or '')[:100], inputer, branch_code,
        donor['donorid'], donor['donorno'] or '', donor['donorname'] or '',
        float(item['amount']), bank['accountno'],
    )

    # 2. Product credit items
    for product_name, pa in product_accounts.items():
        field_map = {
            'ZakatProfesi': 'amountzakatprofesi', 'ZakatMaal': 'amountzakatmaal',
            'ZakatFitrah': 'amountzakatfitrah', 'ZakatPerusahaan': 'amountzakatperusahaan',
            'Infaq': 'amountinfaq', 'InfaqTerikat': 'amountinfaqterikat',
            'DPU': 'amountdpu', 'AnakYatim': 'amountanakyatim',
            'AnakAsuh': 'amountanakasuh', 'TitipanWakaf': 'amounttitipanwakaf',
            'TitipanQurban': 'amounttitipanqurban', 'Qurban': 'amountqurban',
            'NonHalal': 'amountnonhalal', 'Fidyah': 'amountfidyah',
        }
        amount = float(item.get(field_map[product_name]) or 0)
        if amount <= 0:
            continue
        ti_id = await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')")
        await conn.execute(
            """INSERT INTO transaction.transactionitem
               (transactionitemid, transactionid, mutationtype, amount, currencycode, rate)
               VALUES ($1,$2,'C',$3,'IDR',1.0)""",
            ti_id, trans_id, amount,
        )
        await conn.execute(
            """INSERT INTO transaction.accounttransactionitem
               (transactionitemid, accounttitype, accountno, fundentity, donorid, isupdatebalance)
               VALUES ($1,'D',$2,$3,$4,'T')""",
            ti_id, pa['accountno'], pa['fundentity'], donor['donorid'],
        )
        # Update product account balance
        await conn.execute(
            "UPDATE transaction.financialaccount SET balance = COALESCE(balance,0) + $1 "
            "WHERE accountno = $2",
            amount, pa['accountno'],
        )
        # Update donor total fund
        await conn.execute(
            """INSERT INTO fund.donortotalfund (totalfundid, donorid, fundentity, totalamount)
               VALUES (nextval('fund.seq_totalfundid'), $1, $2, $3)
               ON CONFLICT (donorid, fundentity)
               DO UPDATE SET totalamount = fund.donortotalfund.totalamount + $3""",
            donor['donorid'], pa['fundentity'], amount,
        )

    # 3. Bank debit item
    total = float(item['amount'])
    ti_bank = await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')")
    await conn.execute(
        """INSERT INTO transaction.transactionitem
           (transactionitemid, transactionid, mutationtype, amount, currencycode, rate)
           VALUES ($1,$2,'D',$3,'IDR',1.0)""",
        ti_bank, trans_id, total,
    )
    await conn.execute(
        """INSERT INTO transaction.accounttransactionitem
           (transactionitemid, accounttitype, accountno, isupdatebalance)
           VALUES ($1,'A',$2,'T')""",
        ti_bank, bank['accountno'],
    )
    # Update bank balance (debit = increase bank balance for cash-in)
    await conn.execute(
        "UPDATE transaction.financialaccount SET balance = COALESCE(balance,0) + $1 "
        "WHERE accountno = $2",
        total, bank['accountno'],
    )

    # 4. Generate transaction number
    seq_no = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
    trans_no = f'SDMULTI-{year}-{branch_code}-{bank["cashcode"] or "BNK"}-{seq_no:07d}'
    await conn.execute(
        "UPDATE transaction.transaction SET transactionno=$1 WHERE transactionid=$2",
        trans_no, trans_id,
    )

    # 5. Journal
    journal_no = await _generate_journal_no(conn, branch_code, year)
    await conn.execute(
        """INSERT INTO transaction.journal
           (journal_no, journal_date, journal_date_posting, description,
            userid_create, branch_code, is_posted, status, source_app)
           VALUES ($1,$2,$2,$3,$4,$5,'T','A','isf-app')""",
        journal_no, trans_date,
        (item['description'] or '')[:200], inputer, branch_code,
    )
    # Journal items — one per product account (credit side) + bank (debit side)
    item_no = 1
    for product_name, pa in product_accounts.items():
        field_map = {
            'ZakatProfesi': 'amountzakatprofesi', 'ZakatMaal': 'amountzakatmaal',
            'ZakatFitrah': 'amountzakatfitrah', 'ZakatPerusahaan': 'amountzakatperusahaan',
            'Infaq': 'amountinfaq', 'InfaqTerikat': 'amountinfaqterikat',
            'DPU': 'amountdpu', 'AnakYatim': 'amountanakyatim',
            'AnakAsuh': 'amountanakasuh', 'TitipanWakaf': 'amounttitipanwakaf',
            'TitipanQurban': 'amounttitipanqurban', 'Qurban': 'amountqurban',
            'NonHalal': 'amountnonhalal', 'Fidyah': 'amountfidyah',
        }
        amount = float(item.get(field_map[product_name]) or 0)
        if amount <= 0:
            continue
        await conn.execute(
            """INSERT INTO transaction.journalitem
               (fl_journal, journalitem_no, fl_account, amount_credit, amount_debit,
                description, branch_code, valuta_code, userid_create)
               VALUES ($1,$2,$3,$4,0,$5,$6,'IDR',$7)""",
            journal_no, item_no, pa['accountno'], amount,
            (item['description'] or '')[:200], branch_code, inputer,
        )
        item_no += 1

    # Bank debit journal item
    await conn.execute(
        """INSERT INTO transaction.journalitem
           (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
            description, branch_code, valuta_code, userid_create)
           VALUES ($1,$2,$3,$4,0,$5,$6,'IDR',$7)""",
        journal_no, item_no, bank['accountno'], total,
        (item['description'] or '')[:200], branch_code, inputer,
    )

    # Journal block
    jblock_id = await conn.fetchval("SELECT nextval('transaction.seq_journalblock')")
    await conn.execute(
        """INSERT INTO transaction.journalblock
           (id_journalblock, journal_no, system_id, class_id, key_id)
           VALUES ($1,$2,'TRANS','BatchUploadMulti',$3)""",
        jblock_id, journal_no, trans_id,
    )
    await conn.execute(
        "UPDATE transaction.transaction SET journalno=$1 WHERE transactionid=$2",
        journal_no, trans_id,
    )

    # History
    hist_id = await conn.fetchval(
        "SELECT nextval('transaction.seq_transhistoryofchanges')"
    )
    await conn.execute(
        """INSERT INTO transaction.transhistoryofchanges
           (historyid, transactionid, transactionno, userid, processtime, changetype)
           VALUES ($1,$2,$3,$4,$5,'I')""",
        hist_id, trans_id, trans_no, inputer, now,
    )
    # Update batchuploaditem — gunakan batchitemid (primary key) agar tidak ambigu
    await conn.execute(
        "UPDATE transaction.batchuploaditem "
        "SET transactionid=$1, transactionno=$2 WHERE batchitemid=$3",
        trans_id, trans_no, item['batchitemid'],
    )
    return trans_no


async def approve_batch(batch_id: int, authorized_user: str,
                        branch_code: str, inputer: str) -> int:
    """Commit all pending items for batch_id. Returns count of committed transactions."""
    pool = get_pool()
    async with pool.acquire() as conn:
        batch = await conn.fetchrow(
            "SELECT authstatus FROM transaction.batchupload WHERE batchid=$1", batch_id
        )
        if not batch:
            raise LookupError(f'Batch {batch_id} tidak ditemukan')
        if (batch['authstatus'] or 'P') == 'A':
            raise ValueError('Batch sudah pernah diotorisasi')

        items = await conn.fetch(
            "SELECT * FROM transaction.batchuploaditem WHERE batchid=$1 ORDER BY batchitemid",
            batch_id,
        )
        if not items:
            raise ValueError('Batch tidak memiliki item')

        default_donor = await _get_default_donor(conn)
        product_accounts = await _lookup_product_accounts(conn, branch_code)

        async with conn.transaction():
            total_committed = 0
            total_amount = 0.0
            for item in items:
                item_dict = dict(item)
                item_dict['batchid'] = batch_id
                await _commit_item(
                    conn, item_dict, product_accounts,
                    branch_code, inputer, default_donor,
                )
                total_amount += float(item['amount'] or 0)
                total_committed += 1

            from datetime import datetime, timezone
            await conn.execute(
                """UPDATE transaction.batchupload
                   SET authstatus='A', authorizeduser=$1, totalrecord=$2, totalamount=$3
                   WHERE batchid=$4""",
                authorized_user, total_committed, total_amount, batch_id,
            )
    return total_committed
```

> ⚠️ `fund.seq_totalfundid` mungkin belum ada — cek dengan `\ds fund.*` di psql. Kalau tidak ada, ganti `ON CONFLICT` dengan lookup + insert/update manual.

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaction/commit.py
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(api-python): commit.py — full transaction + journal creation"
```

---

## Task 8: api-python — router.py + main.py wiring

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/router.py`
- Modify: `apps_zakat/api-python/app/main.py`

- [ ] **Buat `router.py`:**

```python
# apps_zakat/api-python/app/modules/transaction/router.py
from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter, File, Form, Query, UploadFile
from fastapi.responses import JSONResponse, Response

from app.modules.transaction import service
from app.modules.transaction.commit import approve_batch
from app.modules.transaction.template import build_template
from app.shared.response import err, ok

router = APIRouter(prefix='/transaction', tags=['transaction'])

_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


@router.post('/upload/penghimpunan/parse')
async def parse_endpoint(
    file: UploadFile = File(...),
    branch_code: str = Form(''),
):
    filename = file.filename or 'upload'
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    if ext not in ('xls', 'xlsx'):
        return JSONResponse(
            status_code=422,
            content=err('INVALID_FORMAT', 'Hanya file .xls dan .xlsx yang diterima'),
        )
    data = await file.read()
    try:
        rows = await service.parse_upload(filename, data)
    except Exception as exc:
        return JSONResponse(
            status_code=400,
            content=err('PARSE_ERROR', str(exc)),
        )
    return ok({'rows': [r.model_dump() for r in rows], 'filename': filename})


@router.post('/upload/penghimpunan/draft')
async def draft_endpoint(
    file: UploadFile = File(...),
    branch_code: str = Form(...),
    upload_user: str = Form(...),
):
    filename = file.filename or 'upload'
    data = await file.read()
    try:
        rows = await service.parse_upload(filename, data)
        result = await service.save_draft(filename, branch_code, upload_user, rows)
    except ValueError as exc:
        return JSONResponse(status_code=400, content=err('DRAFT_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())


@router.get('/upload/penghimpunan/template')
async def template_endpoint():
    xlsx = build_template()
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': 'attachment; filename="template-upload-penghimpunan.xlsx"'},
    )


@router.get('/upload/penghimpunan/batches')
async def batches_endpoint(
    begin: str | None = Query(default=None),
    end: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    batches = await service.list_batches(begin, end, status)
    return ok([b.model_dump() for b in batches])


@router.get('/upload/penghimpunan/batches/{batch_id}')
async def batch_detail_endpoint(batch_id: int):
    detail = await service.get_batch_detail(batch_id)
    if not detail:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', f'Batch {batch_id} tidak ditemukan'))
    return ok(detail.model_dump())


@router.post('/upload/penghimpunan/batches/{batch_id}/approve')
async def approve_endpoint(
    batch_id: int,
    authorized_user: str = Form(...),
    branch_code: str = Form(...),
    inputer: str = Form(...),
):
    try:
        committed = await approve_batch(batch_id, authorized_user, branch_code, inputer)
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except ValueError as exc:
        if 'sudah pernah' in str(exc):
            return JSONResponse(status_code=409, content=err('ALREADY_APPROVED', str(exc)))
        return JSONResponse(status_code=400, content=err('APPROVE_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok({'batch_id': batch_id, 'total_committed': committed})
```

- [ ] **Edit `app/main.py`** — tambah `transaction_router`:

Di `apps_zakat/api-python/app/main.py`, tambahkan:
```python
from app.modules.transaction.router import router as transaction_router
```
dan di bawah `app.include_router(identity_router, prefix="/api")`:
```python
app.include_router(transaction_router, prefix="/api")
```

- [ ] **Test parse endpoint secara manual** (pastikan server berjalan):

```bash
# Buat file test kecil dulu
python3 -c "
from openpyxl import Workbook; import io
wb = Workbook(); ws = wb.active
ws.append(['NoRek','Tanggal','Ket','Ref','Total','ZP','ZM','ZF','ZPer','Infaq','InfaqT','DPU','AY','AA','TW','TQ','Qurban','NH','Fidyah'])
ws.append(['1234567','01/06/2026','Transfer zakat','REF001',100000,100000,0,0,0,0,0,0,0,0,0,0,0,0,0])
b=io.BytesIO(); wb.save(b)
open('/tmp/test_upload.xlsx','wb').write(b.getvalue())
"
curl -s -X POST http://localhost:8001/api/transaction/upload/penghimpunan/parse \
  -F "file=@/tmp/test_upload.xlsx" -F "branch_code=001" | python3 -m json.tool
```

Expected: JSON dengan `data.rows` berisi 1 baris (mungkin `status=invalid` kalau rekening tidak dikenal — itu normal).

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaction/router.py \
        apps_zakat/api-python/app/main.py
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(api-python): router + main.py wiring"
```

---

## Task 9: BFF — proxy update + router/transaction.py

**Files:**
- Modify: `apps_zakat/bff-api/app/services/proxy.py`
- Create: `apps_zakat/bff-api/app/routers/transaction.py`

- [ ] **Tambah `post_multipart_api_python` ke `proxy.py`** — append di akhir file:

```python
async def post_multipart_api_python(
    path: str,
    *,
    data: dict,
    file_content: bytes,
    file_field: str = 'file',
    filename: str = 'upload',
    content_type: str = 'application/octet-stream',
) -> httpx.Response:
    """POST multipart/form-data ke api-python (untuk upload file)."""
    url = f"{settings.api_python_base_url}{path}"
    files = {file_field: (filename, file_content, content_type)}
    async with httpx.AsyncClient(timeout=30.0) as client:
        return await client.post(url, data=data, files=files)
```

- [ ] **Buat `apps_zakat/bff-api/app/routers/transaction.py`:**

```python
# apps_zakat/bff-api/app/routers/transaction.py
from __future__ import annotations

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from fastapi.responses import JSONResponse, Response

from app.services.auth import current_user_id_or_401, require_menu
from app.services.proxy import get_api_python, post_api_python, post_multipart_api_python
from app.shared.response import err

router = APIRouter(prefix='/transaction', tags=['transaction'])

_UPLOAD_MENU = 'keuangan.upload.penghimpunan'
_APPROVE_MENU = 'keuangan.upload.penghimpunan.approve'
_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def _branch_for_session(request: Request) -> str:
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    return '' if access == 'all' else primary


@router.post('/upload/penghimpunan/parse')
async def parse(
    request: Request,
    _: str = Depends(require_menu(_UPLOAD_MENU)),
    file: UploadFile = File(...),
):
    branch_code = _branch_for_session(request)
    data = await file.read()
    downstream = await post_multipart_api_python(
        '/api/transaction/upload/penghimpunan/parse',
        data={'branch_code': branch_code},
        file_content=data,
        filename=file.filename or 'upload',
        content_type=file.content_type or 'application/octet-stream',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/upload/penghimpunan/draft')
async def draft(
    request: Request,
    _: str = Depends(require_menu(_UPLOAD_MENU)),
    file: UploadFile = File(...),
):
    user_id = request.session.get('user_id', '')
    branch_code = _branch_for_session(request)
    data = await file.read()
    downstream = await post_multipart_api_python(
        '/api/transaction/upload/penghimpunan/draft',
        data={'branch_code': branch_code, 'upload_user': user_id},
        file_content=data,
        filename=file.filename or 'upload',
        content_type=file.content_type or 'application/octet-stream',
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/upload/penghimpunan/template')
async def template(
    request: Request,
    _: str = Depends(require_menu(_UPLOAD_MENU)),
):
    downstream = await get_api_python('/api/transaction/upload/penghimpunan/template')
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': 'attachment; filename="template-upload-penghimpunan.xlsx"'},
    )


@router.get('/upload/penghimpunan/batches')
async def batches(
    request: Request,
    _: str = Depends(require_menu(_APPROVE_MENU)),
    begin: str | None = Query(default=None),
    end: str | None = Query(default=None),
    status: str | None = Query(default=None),
):
    params: dict = {}
    if begin:
        params['begin'] = begin
    if end:
        params['end'] = end
    if status:
        params['status'] = status
    downstream = await get_api_python('/api/transaction/upload/penghimpunan/batches', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/upload/penghimpunan/batches/{batch_id}')
async def batch_detail(
    request: Request,
    batch_id: int,
    _: str = Depends(require_menu(_APPROVE_MENU)),
):
    downstream = await get_api_python(f'/api/transaction/upload/penghimpunan/batches/{batch_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/upload/penghimpunan/batches/{batch_id}/approve')
async def approve(
    request: Request,
    batch_id: int,
    _: str = Depends(require_menu(_APPROVE_MENU)),
):
    user_id = request.session.get('user_id', '')
    branch_code = _branch_for_session(request)
    downstream = await post_api_python(
        f'/api/transaction/upload/penghimpunan/batches/{batch_id}/approve',
        json_body={
            'authorized_user': user_id,
            'branch_code': branch_code,
            'inputer': user_id,
        },
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
```

> ⚠️ BFF approve endpoint menggunakan `post_api_python` (JSON), tapi api-python router approve menerima `Form(...)`. Perlu disesuaikan — ubah api-python approve endpoint untuk menerima JSON body juga, atau gunakan `post_multipart_api_python` di BFF. Pilih salah satu dan konsisten.

**Perbaiki:** ubah api-python `approve_endpoint` menjadi menerima JSON body:

```python
# Di router.py api-python, ganti approve_endpoint dengan:
from pydantic import BaseModel

class ApproveRequest(BaseModel):
    authorized_user: str
    branch_code: str
    inputer: str

@router.post('/upload/penghimpunan/batches/{batch_id}/approve')
async def approve_endpoint(batch_id: int, req: ApproveRequest):
    try:
        committed = await approve_batch(batch_id, req.authorized_user, req.branch_code, req.inputer)
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except ValueError as exc:
        if 'sudah pernah' in str(exc):
            return JSONResponse(status_code=409, content=err('ALREADY_APPROVED', str(exc)))
        return JSONResponse(status_code=400, content=err('APPROVE_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok({'batch_id': batch_id, 'total_committed': committed})
```

- [ ] **Edit BFF `main.py`** — tambah transaction_router:

```python
from app.routers.transaction import router as transaction_router
# ...
app.include_router(transaction_router, prefix="/api")
```

- [ ] **Commit:**

```bash
git add apps_zakat/bff-api/app/services/proxy.py \
        apps_zakat/bff-api/app/routers/transaction.py \
        apps_zakat/bff-api/app/main.py \
        apps_zakat/api-python/app/modules/transaction/router.py
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(bff): BFF router transaction + proxy multipart"
```

---

## Task 10: Menu & Auth Wiring

**Files:**
- Modify: `apps_zakat/web-vue/src/lib/menu/registry.ts`
- Modify: `infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql`

- [ ] **Edit `registry.ts`** — tambah 2 key sebelum `'admin.role_menu'`:

```typescript
  'keuangan.upload.penghimpunan',
  'keuangan.upload.penghimpunan.approve',
```

- [ ] **Tambah ke `seed-menu-and-rolemenu.sql`** — append di akhir file:

```sql
-- Upload Penghimpunan
INSERT INTO isf_auth.menu (key, label)
VALUES
  ('keuangan.upload.penghimpunan', 'Upload Penghimpunan'),
  ('keuangan.upload.penghimpunan.approve', 'Otorisasi Upload Penghimpunan')
ON CONFLICT (key) DO NOTHING;

INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.id_peran, m.key
FROM enterprise.peran r
CROSS JOIN (VALUES
  ('KEU',    'keuangan.upload.penghimpunan'),
  ('SPVKEU', 'keuangan.upload.penghimpunan'),
  ('SPVKEU', 'keuangan.upload.penghimpunan.approve')
) AS m(role, key)
WHERE r.id_peran = m.role
ON CONFLICT DO NOTHING;
```

- [ ] **Apply seed ke isf_auth_zakat:**

```bash
PGPASSWORD=solusi psql -h localhost -U postgres -d isf_auth_zakat \
  -f infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql
```

Expected: `INSERT 0 2` (menu) dan `INSERT 0 3` (role_menu), no errors. User harus logout+login ulang agar menu masuk session.

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/lib/menu/registry.ts \
        infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql
git commit -m "[UPLOAD-PENGHIMPUNAN] chore(auth): menu key + role_menu seed untuk upload penghimpunan"
```

---

## Task 11: Frontend — UploadPenghimpunanPage.vue

**Files:**
- Create: `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue`

- [ ] **Buat halaman upload + preview:**

```vue
<!-- apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue -->
<script setup lang="ts">
import { Upload, Download, FileCheck } from 'lucide-vue-next'
import { ref, computed } from 'vue'
import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { BASE_URL, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'

interface ParsedRow {
  row_no: number
  no_rekening: string
  tanggal: string
  keterangan: string
  no_ref: string
  total_kredit: number
  zakat_profesi: number
  zakat_maal: number
  zakat_fitrah: number
  zakat_perusahaan: number
  infaq: number
  infaq_terikat: number
  dpu: number
  anak_yatim: number
  anak_asuh: number
  titipan_wakaf: number
  titipan_qurban: number
  qurban: number
  non_halal: number
  fidyah: number
  status: 'valid' | 'warning' | 'invalid'
  pesan: string
}

const phase = ref<'idle' | 'preview' | 'submitted'>('idle')
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const rows = ref<ParsedRow[]>([])
const parsedFilename = ref('')
const batchId = ref<number | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)

const validRows = computed(() => rows.value.filter(r => r.status !== 'invalid'))
const invalidCount = computed(() => rows.value.filter(r => r.status === 'invalid').length)
const totalAmount = computed(() => validRows.value.reduce((s, r) => s + r.total_kredit, 0))
const canSave = computed(() => validRows.value.length > 0)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function statusColor(s: string) {
  if (s === 'valid') return 'bg-green-100 text-green-800'
  if (s === 'warning') return 'bg-yellow-100 text-yellow-800'
  return 'bg-red-100 text-red-800'
}

async function downloadTemplate() {
  const res = await fetch(`${BASE_URL}/api/transaction/upload/penghimpunan/template`, {
    credentials: 'include',
  })
  if (!res.ok) return
  const blob = await res.blob()
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'template-upload-penghimpunan.xlsx'
  a.click()
  setTimeout(() => URL.revokeObjectURL(a.href), 1000)
}

async function parseFile() {
  if (!selectedFile.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const form = new FormData()
    form.append('file', selectedFile.value)
    const res = await fetch(`${BASE_URL}/api/transaction/upload/penghimpunan/parse`, {
      method: 'POST',
      credentials: 'include',
      body: form,
    })
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Parse gagal')
    rows.value = payload.data.rows
    parsedFilename.value = payload.data.filename
    phase.value = 'preview'
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

async function saveDraft() {
  if (!selectedFile.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const form = new FormData()
    form.append('file', selectedFile.value)
    const res = await fetch(`${BASE_URL}/api/transaction/upload/penghimpunan/draft`, {
      method: 'POST',
      credentials: 'include',
      body: form,
    })
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Simpan draft gagal')
    batchId.value = payload.data.batch_id
    phase.value = 'submitted'
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="p-6 max-w-full">
    <div class="mb-4 flex items-center gap-3">
      <Upload class="w-5 h-5 text-primary" />
      <h1 class="text-lg font-semibold">Upload Penghimpunan Multi-Bank</h1>
    </div>

    <!-- Phase: idle / file selection -->
    <div v-if="phase === 'idle' || phase === 'preview'" class="space-y-4">
      <div class="flex items-center gap-3 flex-wrap">
        <input
          ref="fileInput"
          type="file"
          accept=".xls,.xlsx"
          class="block text-sm text-muted file:mr-3 file:py-1.5 file:px-3 file:rounded file:border-0 file:bg-primary file:text-primary-foreground file:text-xs file:cursor-pointer cursor-pointer"
          @change="(e) => { selectedFile = (e.target as HTMLInputElement).files?.[0] ?? null; phase = 'idle'; rows = [] }"
        />
        <Button variant="outline" size="sm" @click="downloadTemplate">
          <Download class="w-3.5 h-3.5 mr-1" /> Template
        </Button>
        <Button
          size="sm"
          :disabled="!selectedFile || loading"
          @click="parseFile"
        >
          {{ loading ? 'Membaca...' : 'Parse File' }}
        </Button>
      </div>

      <Alert v-if="errorMsg" variant="error" :message="errorMsg" />

      <!-- Preview table -->
      <template v-if="phase === 'preview' && rows.length">
        <!-- Summary -->
        <div class="flex items-center gap-6 text-sm text-muted bg-surface border border-border rounded-lg px-4 py-2">
          <span>{{ validRows.length }} baris akan disimpan</span>
          <span v-if="invalidCount > 0" class="text-red-600">{{ invalidCount }} baris invalid (dilewati)</span>
          <span class="ml-auto font-medium">Total: Rp {{ fmt(totalAmount) }}</span>
        </div>

        <div class="overflow-x-auto border border-border rounded-lg">
          <table class="text-xs w-full">
            <thead class="bg-surface sticky top-0">
              <tr>
                <th class="px-2 py-1.5 text-left whitespace-nowrap">No</th>
                <th class="px-2 py-1.5 text-left whitespace-nowrap">Rekening</th>
                <th class="px-2 py-1.5 text-left whitespace-nowrap">Tanggal</th>
                <th class="px-2 py-1.5 text-left whitespace-nowrap min-w-[180px]">Keterangan</th>
                <th class="px-2 py-1.5 text-left whitespace-nowrap">Ref</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Total</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Zakat P</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Zakat M</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Zakat F</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Zakat Per</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Infaq</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">InfaqT</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">DPU</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">A.Yatim</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">A.Asuh</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">T.Wakaf</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">T.Qurban</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Qurban</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">NonHalal</th>
                <th class="px-2 py-1.5 text-right whitespace-nowrap">Fidyah</th>
                <th class="px-2 py-1.5 text-left whitespace-nowrap">Status</th>
                <th class="px-2 py-1.5 text-left whitespace-nowrap">Pesan</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in rows"
                :key="row.row_no"
                :class="row.status === 'invalid' ? 'opacity-50 bg-red-50' : 'hover:bg-background'"
              >
                <td class="px-2 py-1 text-center">{{ row.row_no }}</td>
                <td class="px-2 py-1">{{ row.no_rekening }}</td>
                <td class="px-2 py-1 whitespace-nowrap">{{ dmy(row.tanggal) }}</td>
                <td class="px-2 py-1 max-w-[200px] truncate" :title="row.keterangan">{{ row.keterangan }}</td>
                <td class="px-2 py-1">{{ row.no_ref }}</td>
                <td class="px-2 py-1 text-right">{{ fmt(row.total_kredit) }}</td>
                <td class="px-2 py-1 text-right">{{ row.zakat_profesi ? fmt(row.zakat_profesi) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.zakat_maal ? fmt(row.zakat_maal) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.zakat_fitrah ? fmt(row.zakat_fitrah) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.zakat_perusahaan ? fmt(row.zakat_perusahaan) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.infaq ? fmt(row.infaq) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.infaq_terikat ? fmt(row.infaq_terikat) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.dpu ? fmt(row.dpu) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.anak_yatim ? fmt(row.anak_yatim) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.anak_asuh ? fmt(row.anak_asuh) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.titipan_wakaf ? fmt(row.titipan_wakaf) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.titipan_qurban ? fmt(row.titipan_qurban) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.qurban ? fmt(row.qurban) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.non_halal ? fmt(row.non_halal) : '' }}</td>
                <td class="px-2 py-1 text-right">{{ row.fidyah ? fmt(row.fidyah) : '' }}</td>
                <td class="px-2 py-1">
                  <span :class="['px-1.5 py-0.5 rounded text-[10px] font-medium uppercase', statusColor(row.status)]">
                    {{ row.status }}
                  </span>
                </td>
                <td class="px-2 py-1 text-muted max-w-[160px] truncate" :title="row.pesan">{{ row.pesan }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="flex justify-end">
          <Button :disabled="!canSave || loading" @click="saveDraft">
            {{ loading ? 'Menyimpan...' : 'Simpan Draft' }}
          </Button>
        </div>
      </template>
    </div>

    <!-- Phase: submitted -->
    <div v-if="phase === 'submitted'" class="flex flex-col items-center gap-4 py-12">
      <FileCheck class="w-12 h-12 text-green-600" />
      <p class="text-lg font-medium">Draft disimpan (Batch #{{ batchId }})</p>
      <p class="text-sm text-muted">Supervisor perlu mengotorisasi sebelum transaksi terbentuk.</p>
      <div class="flex gap-3">
        <Button variant="outline" @click="phase = 'idle'; selectedFile = null; rows = []">Upload Lagi</Button>
        <router-link to="/keuangan/upload/penghimpunan/list">
          <Button>Lihat Daftar Batch</Button>
        </router-link>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanPage.vue
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(web-vue): halaman upload + preview penghimpunan"
```

---

## Task 12: Frontend — List & Detail Pages

**Files:**
- Create: `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanListPage.vue`
- Create: `apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanDetailPage.vue`

- [ ] **Buat `UploadPenghimpunanListPage.vue`:**

```vue
<!-- apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanListPage.vue -->
<script setup lang="ts">
import { List } from 'lucide-vue-next'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'

interface Batch {
  batch_id: number
  filename: string
  upload_date: string
  upload_user: string
  branch_code: string
  total_record: number
  total_amount: number
  authstatus: string
}

const router = useRouter()
const today = new Date().toISOString().slice(0, 10)
const begin = ref(today.slice(0, 8) + '01')  // first of month
const end = ref(today)
const statusFilter = ref('')
const batches = ref<Batch[]>([])
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const hasLoaded = ref(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function statusChip(s: string) {
  return s === 'A'
    ? 'bg-green-100 text-green-800'
    : 'bg-yellow-100 text-yellow-800'
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const p = new URLSearchParams({ begin: begin.value, end: end.value })
    if (statusFilter.value) p.set('status', statusFilter.value)
    batches.value = await api.get<Batch[]>(`/api/transaction/upload/penghimpunan/batches?${p}`)
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof ApiError ? e.message : String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <List class="w-5 h-5 text-primary" />
      <h1 class="text-lg font-semibold">Daftar Batch Upload Penghimpunan</h1>
    </div>

    <div class="flex items-end gap-3 mb-4 flex-wrap">
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Dari</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Sampai</label>
        <DateField v-model="end" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Status</label>
        <select v-model="statusFilter" class="border border-border rounded px-2 py-1.5 text-sm bg-background">
          <option value="">Semua</option>
          <option value="P">Pending</option>
          <option value="A">Approved</option>
        </select>
      </div>
      <Button :disabled="loading" @click="load">{{ loading ? 'Memuat...' : 'Tampilkan' }}</Button>
    </div>

    <Alert v-if="errorMsg" variant="error" :message="errorMsg" class="mb-3" />

    <div v-if="hasLoaded" class="border border-border rounded-lg overflow-hidden">
      <table v-if="batches.length" class="w-full text-sm">
        <thead class="bg-surface">
          <tr>
            <th class="px-3 py-2 text-left">Batch</th>
            <th class="px-3 py-2 text-left">Filename</th>
            <th class="px-3 py-2 text-left">Tgl Upload</th>
            <th class="px-3 py-2 text-left">Uploader</th>
            <th class="px-3 py-2 text-right">Record</th>
            <th class="px-3 py-2 text-right">Total (Rp)</th>
            <th class="px-3 py-2 text-left">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="b in batches"
            :key="b.batch_id"
            class="border-t border-border hover:bg-background cursor-pointer"
            @click="router.push(`/keuangan/upload/penghimpunan/${b.batch_id}`)"
          >
            <td class="px-3 py-2 font-mono text-xs">#{{ b.batch_id }}</td>
            <td class="px-3 py-2 text-xs">{{ b.filename }}</td>
            <td class="px-3 py-2 whitespace-nowrap">{{ dmy(b.upload_date) }}</td>
            <td class="px-3 py-2">{{ b.upload_user }}</td>
            <td class="px-3 py-2 text-right">{{ b.total_record }}</td>
            <td class="px-3 py-2 text-right">{{ fmt(b.total_amount) }}</td>
            <td class="px-3 py-2">
              <span :class="['px-1.5 py-0.5 rounded text-[10px] font-medium uppercase', statusChip(b.authstatus)]">
                {{ b.authstatus === 'A' ? 'Approved' : 'Pending' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="p-6 text-center text-muted text-sm">Tidak ada batch ditemukan.</div>
    </div>
    <div v-else-if="!loading" class="text-sm text-muted">Klik "Tampilkan" untuk memuat data.</div>
  </div>
</template>
```

- [ ] **Buat `UploadPenghimpunanDetailPage.vue`:**

```vue
<!-- apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanDetailPage.vue -->
<script setup lang="ts">
import { ShieldCheck } from 'lucide-vue-next'
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { api, ApiError, BASE_URL } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'

interface BatchItem {
  batch_item_id: number
  row_no: number
  no_rekening: string
  tanggal: string
  keterangan: string
  no_ref: string
  total_kredit: number
  status: string
  pesan: string
  transaction_no: string | null
}

interface BatchDetail {
  batch_id: number
  filename: string
  upload_date: string
  upload_user: string
  branch_code: string
  total_record: number
  total_amount: number
  authstatus: string
  authorized_user: string | null
  items: BatchItem[]
}

const route = useRoute()
const auth = useAuthStore()
const batchId = Number(route.params.id)
const detail = ref<BatchDetail | null>(null)
const loading = ref(true)
const approving = ref(false)
const showConfirm = ref(false)
const errorMsg = ref<string | null>(null)
const approveError = ref<string | null>(null)

const canApprove = computed(
  () => detail.value?.authstatus === 'P' && auth.hasMenu('keuangan.upload.penghimpunan.approve')
)
const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

onMounted(async () => {
  try {
    detail.value = await api.get<BatchDetail>(
      `/api/transaction/upload/penghimpunan/batches/${batchId}`
    )
  } catch (e: unknown) {
    errorMsg.value = e instanceof ApiError ? e.message : String(e)
  } finally {
    loading.value = false
  }
})

async function confirmApprove() {
  approving.value = true
  approveError.value = null
  try {
    const res = await fetch(
      `${BASE_URL}/api/transaction/upload/penghimpunan/batches/${batchId}/approve`,
      { method: 'POST', credentials: 'include', headers: { 'Content-Type': 'application/json' }, body: '{}' }
    )
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Otorisasi gagal')
    detail.value = await api.get<BatchDetail>(
      `/api/transaction/upload/penghimpunan/batches/${batchId}`
    )
    showConfirm.value = false
  } catch (e: unknown) {
    approveError.value = e instanceof Error ? e.message : String(e)
  } finally {
    approving.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <ShieldCheck class="w-5 h-5 text-primary" />
      <h1 class="text-lg font-semibold">Detail Batch #{{ batchId }}</h1>
    </div>

    <div v-if="loading" class="text-sm text-muted">Memuat...</div>
    <Alert v-else-if="errorMsg" variant="error" :message="errorMsg" />

    <template v-else-if="detail">
      <!-- Header card -->
      <div class="border border-border rounded-lg p-4 mb-4 bg-surface grid grid-cols-2 gap-3 text-sm">
        <div><span class="text-muted">Filename:</span> {{ detail.filename }}</div>
        <div><span class="text-muted">Tgl Upload:</span> {{ dmy(detail.upload_date) }}</div>
        <div><span class="text-muted">Uploader:</span> {{ detail.upload_user }}</div>
        <div><span class="text-muted">Cabang:</span> {{ detail.branch_code }}</div>
        <div><span class="text-muted">Total Record:</span> {{ detail.total_record }}</div>
        <div><span class="text-muted">Total Amount:</span> Rp {{ fmt(detail.total_amount) }}</div>
        <div>
          <span class="text-muted">Status:</span>
          <span :class="['ml-2 px-1.5 py-0.5 rounded text-[10px] font-medium uppercase',
            detail.authstatus === 'A' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800']">
            {{ detail.authstatus === 'A' ? 'Approved' : 'Pending' }}
          </span>
        </div>
        <div v-if="detail.authorized_user">
          <span class="text-muted">Diotorisasi:</span> {{ detail.authorized_user }}
        </div>
      </div>

      <!-- Approve button -->
      <div v-if="canApprove" class="mb-4 flex gap-3 items-center">
        <Button @click="showConfirm = true">Otorisasi Batch</Button>
        <span class="text-xs text-muted">Tindakan ini tidak bisa dibatalkan — semua transaksi akan terbentuk.</span>
      </div>

      <!-- Confirm dialog -->
      <div v-if="showConfirm" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
        <div class="bg-white rounded-xl shadow-xl p-6 max-w-sm w-full mx-4">
          <h2 class="font-semibold mb-2">Konfirmasi Otorisasi</h2>
          <p class="text-sm text-muted mb-4">
            {{ detail.total_record }} transaksi akan dibuat dan dijurnal. Lanjutkan?
          </p>
          <Alert v-if="approveError" variant="error" :message="approveError" class="mb-3" />
          <div class="flex gap-3 justify-end">
            <Button variant="outline" :disabled="approving" @click="showConfirm = false">Batal</Button>
            <Button :disabled="approving" @click="confirmApprove">
              {{ approving ? 'Memproses...' : 'Ya, Otorisasi' }}
            </Button>
          </div>
        </div>
      </div>

      <!-- Items table -->
      <div class="border border-border rounded-lg overflow-x-auto">
        <table class="w-full text-xs">
          <thead class="bg-surface">
            <tr>
              <th class="px-2 py-1.5 text-left">No</th>
              <th class="px-2 py-1.5 text-left">Rekening</th>
              <th class="px-2 py-1.5 text-left">Tanggal</th>
              <th class="px-2 py-1.5 text-left min-w-[160px]">Keterangan</th>
              <th class="px-2 py-1.5 text-left">Ref</th>
              <th class="px-2 py-1.5 text-right">Total</th>
              <th class="px-2 py-1.5 text-left">Status</th>
              <th class="px-2 py-1.5 text-left">No Transaksi</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in detail.items"
              :key="item.batch_item_id"
              class="border-t border-border hover:bg-background"
            >
              <td class="px-2 py-1">{{ item.row_no }}</td>
              <td class="px-2 py-1">{{ item.no_rekening }}</td>
              <td class="px-2 py-1 whitespace-nowrap">{{ dmy(item.tanggal) }}</td>
              <td class="px-2 py-1 max-w-[200px] truncate" :title="item.keterangan">{{ item.keterangan }}</td>
              <td class="px-2 py-1">{{ item.no_ref }}</td>
              <td class="px-2 py-1 text-right">{{ fmt(item.total_kredit) }}</td>
              <td class="px-2 py-1">
                <span :class="['px-1 py-0.5 rounded text-[9px] font-medium uppercase',
                  item.status === 'valid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800']">
                  {{ item.status }}
                </span>
              </td>
              <td class="px-2 py-1 font-mono text-[10px]">{{ item.transaction_no ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
```

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanListPage.vue \
        apps_zakat/web-vue/src/pages/keuangan/UploadPenghimpunanDetailPage.vue
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(web-vue): halaman list batch + detail + otorisasi"
```

---

## Task 13: Sidebar + Router Wiring

**Files:**
- Modify: `apps_zakat/web-vue/src/components/AppSidebar.vue`
- Modify: `apps_zakat/web-vue/src/router/index.ts`

- [ ] **Edit `AppSidebar.vue`** — tambah Upload section di bawah `{ label: 'Bank', to: '/keuangan/bank', icon: Landmark }` (dalam children Keuangan):

```typescript
{ section: 'Upload' },
{ label: 'Upload Penghimpunan', to: '/keuangan/upload/penghimpunan', icon: Upload },
{ label: 'Otorisasi Upload', to: '/keuangan/upload/penghimpunan/list', icon: ClipboardCheck },
```

Tambah import di script setup:
```typescript
import { ..., Upload, ClipboardCheck } from 'lucide-vue-next'
```

- [ ] **Edit `router/index.ts`** — tambah 3 route sebelum `catchAll`:

```typescript
{
  path: '/keuangan/upload/penghimpunan',
  name: 'keuangan-upload-penghimpunan',
  component: () => import('@/pages/keuangan/UploadPenghimpunanPage.vue'),
  meta: { title: 'Upload Penghimpunan', menu_key: 'keuangan.upload.penghimpunan' as MenuKey },
},
{
  path: '/keuangan/upload/penghimpunan/list',
  name: 'keuangan-upload-penghimpunan-list',
  component: () => import('@/pages/keuangan/UploadPenghimpunanListPage.vue'),
  meta: { title: 'Daftar Batch Upload', menu_key: 'keuangan.upload.penghimpunan.approve' as MenuKey },
},
{
  path: '/keuangan/upload/penghimpunan/:id',
  name: 'keuangan-upload-penghimpunan-detail',
  component: () => import('@/pages/keuangan/UploadPenghimpunanDetailPage.vue'),
  meta: { title: 'Detail Batch', menu_key: 'keuangan.upload.penghimpunan.approve' as MenuKey },
},
```

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/components/AppSidebar.vue \
        apps_zakat/web-vue/src/router/index.ts
git commit -m "[UPLOAD-PENGHIMPUNAN] feat(web-vue): sidebar + router wiring 3 halaman upload"
```

---

## Task 14: E2E Test Script

**Files:**
- Create: `testing/e2e-upload-penghimpunan.sh`

- [ ] **Buat test fixture XLSX** dan **script E2E:**

```bash
#!/usr/bin/env bash
# testing/e2e-upload-penghimpunan.sh
set -e
BFF="http://localhost:7000"
API="http://localhost:8001"

echo "=== E2E: Upload Penghimpunan ==="

# 1. Generate test fixture
python3 - <<'PYEOF'
from openpyxl import Workbook
import io, os
wb = Workbook(); ws = wb.active
ws.append(['NoRek','Tanggal','Ket','Ref','Total','ZP','ZM','ZF','ZPer',
           'Infaq','InfaqT','DPU','AY','AA','TW','TQ','Qurban','NH','Fidyah'])
ws.append(['1234567890','01/06/2026','Transfer DARI Budi TRANSFER','REF-TEST-001',
           500000, 300000, 200000, 0,0,0,0,0,0,0,0,0,0,0,0])
ws.append(['1234567890','02/06/2026','Transfer masuk infaq','REF-TEST-002',
           100000, 0, 0, 0, 0, 100000, 0, 0, 0, 0, 0, 0, 0, 0, 0])
buf = io.BytesIO(); wb.save(buf)
open('/tmp/e2e_upload.xlsx','wb').write(buf.getvalue())
print("Fixture created: /tmp/e2e_upload.xlsx")
PYEOF

echo ""
echo "2. Parse endpoint (api-python langsung):"
curl -s -X POST "$API/api/transaction/upload/penghimpunan/parse" \
  -F "file=@/tmp/e2e_upload.xlsx" -F "branch_code=001" | python3 -m json.tool | head -40

echo ""
echo "3. Template download:"
curl -sI "$API/api/transaction/upload/penghimpunan/template" | grep -i "content-"

echo ""
echo "4. List batches (api-python):"
curl -s "$API/api/transaction/upload/penghimpunan/batches?begin=2026-06-01&end=2026-06-30" \
  | python3 -m json.tool | head -20

echo ""
echo "=== Done. Manual steps needed ==="
echo "- Login via BFF, test parse + draft + approve via browser atau curl dengan session cookie"
echo "- Verify transaction.transaction rows setelah approve:"
echo "  PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz \\"
echo "    -c \"SELECT transactionno, amount FROM transaction.transaction WHERE transactioncode='SDMULTI' ORDER BY transactionid DESC LIMIT 5\""
```

```bash
chmod +x testing/e2e-upload-penghimpunan.sh
```

- [ ] **Run script:**

```bash
bash testing/e2e-upload-penghimpunan.sh
```

Expected: fixture dibuat, parse endpoint → JSON rows (mungkin status invalid karena NoRekening test fiktif), template → `Content-Type: application/vnd...xlsx`.

- [ ] **Commit:**

```bash
git add testing/e2e-upload-penghimpunan.sh
git commit -m "[UPLOAD-PENGHIMPUNAN] test(e2e): script e2e upload penghimpunan"
```

---

## Task 15: Integration Smoke Test

Setelah semua service berjalan (`make run` atau `podman-compose up`):

- [ ] **Login** ke `http://localhost:5173` sebagai user dengan role SPVKEU (mis. `RAIS`).

- [ ] **Pastikan menu "Upload Penghimpunan" muncul** di sidebar bawah Keuangan > section Upload. Jika tidak muncul → user harus logout+login (session menus di-refresh saat login).

- [ ] **Test upload**: buka `/keuangan/upload/penghimpunan`, pilih file `/tmp/e2e_upload.xlsx`, klik "Parse File" → preview muncul.

- [ ] **Test simpan draft**: klik "Simpan Draft" → redirect ke confirmation screen dengan batch_id.

- [ ] **Test list**: buka `/keuangan/upload/penghimpunan/list` → pilih rentang tanggal, klik "Tampilkan" → batch muncul di tabel.

- [ ] **Test detail + otorisasi**: klik batch → halaman detail, klik "Otorisasi Batch" → confirm → reload → status jadi Approved.

- [ ] **Verify transaksi terbentuk di DB:**

```bash
PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz \
  -c "SELECT transactionno, amount, transactioncode, branchcode
      FROM transaction.transaction
      WHERE transactioncode = 'SDMULTI'
      ORDER BY transactionid DESC LIMIT 5"
```

Expected: baris dengan `transactioncode = SDMULTI` dan `amount` sesuai.

- [ ] **Verify journal terbentuk:**

```bash
PGPASSWORD=solusi psql -h localhost -U postgres -d mziss_laz \
  -c "SELECT j.journal_no, j.branch_code, COUNT(ji.journalitem_no) AS items
      FROM transaction.journal j
      JOIN transaction.journalitem ji ON j.journal_no = ji.fl_journal
      WHERE j.source_app = 'isf-app'
      GROUP BY j.journal_no, j.branch_code
      ORDER BY j.journal_no DESC LIMIT 5"
```

Expected: journal entries dengan `source_app='isf-app'`.

- [ ] **Final commit jika ada hotfix kecil dari smoke test.**

---

## Known Risks & Mitigations

| Risk | Mitigation |
|---|---|
| `fund.seq_totalfundid` sequence tidak ada | Cek `\ds fund.*`; ganti ON CONFLICT dengan explicit SELECT+INSERT/UPDATE |
| `productaccount` tidak ada data untuk product_id tertentu | Log warning, skip produk tersebut (tidak block approve) |
| Journal number format berbeda dari yang diharapkan | Inspect actual journal_no dari DB sebelum implement `_generate_journal_no` |
| Kolom `batchid` di `batchuploaditem` tidak di-set saat commit | Task 7 `_commit_item` menerima `item_dict['batchid']` — pastikan di-set sebelum insert |
| `Konversi asyncpg date → python date` di approve | `transactiondate` dari DB bisa `datetime.date` atau `datetime.datetime` — handle keduanya dengan `getattr(trans_date, 'year', ...)` |

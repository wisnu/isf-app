# Histori Transaksi — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bangun menu pencarian histori transaksi real-time dengan search+filter, detail+jurnal, hapus dua jalur, re-post jurnal, dan export XLSX.

**Architecture:** api-python modul baru `transaksi_histori/` query langsung ke `transaction.*` (bukan DWH). BFF inject `is_spv`/`user_id`/`branch_code` dari session. SPV mode (role SPVKEU) melihat semua transaksi; role lain hanya milik sendiri.

**Tech Stack:** Python 3.12, FastAPI, asyncpg, openpyxl, Vue 3 + TypeScript, Pydantic v2.

---

## File Map

**Create:**
- `apps_zakat/api-python/app/modules/transaksi_histori/__init__.py`
- `apps_zakat/api-python/app/modules/transaksi_histori/schema.py`
- `apps_zakat/api-python/app/modules/transaksi_histori/repository.py`
- `apps_zakat/api-python/app/modules/transaksi_histori/service.py`
- `apps_zakat/api-python/app/modules/transaksi_histori/delete.py`
- `apps_zakat/api-python/app/modules/transaksi_histori/export.py`
- `apps_zakat/api-python/app/modules/transaksi_histori/router.py`
- `apps_zakat/api-python/tests/test_histori_transaksi.py`
- `apps_zakat/bff-api/app/routers/histori_transaksi.py`
- `apps_zakat/web-vue/src/pages/keuangan/HistoriTransaksiPage.vue`
- `apps_zakat/web-vue/src/pages/keuangan/HistoriTransaksiDetailPage.vue`
- `testing/e2e-histori-transaksi.sh`

**Modify:**
- `apps_zakat/api-python/app/main.py` — include transaksi_histori router
- `apps_zakat/bff-api/app/services/proxy.py` — tambah `stream_api_python`
- `apps_zakat/bff-api/app/main.py` — include histori_transaksi router
- `apps_zakat/web-vue/src/lib/menu/registry.ts` — tambah 1 menu key
- `apps_zakat/web-vue/src/components/AppSidebar.vue` — tambah Transaksi section
- `apps_zakat/web-vue/src/router/index.ts` — tambah 2 route
- `infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql` — tambah menu + role_menu

---

## Task 1: schema.py + unit tests + repository WHERE builder

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaksi_histori/__init__.py`
- Create: `apps_zakat/api-python/app/modules/transaksi_histori/schema.py`
- Create: `apps_zakat/api-python/app/modules/transaksi_histori/repository.py`
- Create: `apps_zakat/api-python/tests/test_histori_transaksi.py`

- [ ] **Buat `__init__.py` kosong:**

```python
# apps_zakat/api-python/app/modules/transaksi_histori/__init__.py
```

- [ ] **Buat `schema.py`:**

```python
# apps_zakat/api-python/app/modules/transaksi_histori/schema.py
from __future__ import annotations
from pydantic import BaseModel


class TransaksiRow(BaseModel):
    transactionid: int
    transactionno: str | None
    transactiondate: str   # ISO YYYY-MM-DD
    actualdate: str        # ISO YYYY-MM-DD
    amount: float
    donorno: str | None
    donorname: str | None
    referenceno: str | None
    description: str | None
    inputer: str | None
    authstatus: str | None
    isposted: str | None
    authoperationmode: str | None
    branchcode: str | None
    channelaccountno: str | None
    channelname: str | None
    exttransactionid: int | None
    titlesubsystem: str | None


class JournalItem(BaseModel):
    journalitem_no: int
    fl_account: str | None
    account_name: str | None
    branch_code: str | None
    valuta_code: str | None
    amount_debit: float
    amount_credit: float
    description: str | None
    subaccountcode: str | None
    subaccountname: str | None


class TransaksiDetail(TransaksiRow):
    journal_items: list[JournalItem]


class DeleteResult(BaseModel):
    deleted: bool
    pending_approval: bool
    message: str


class RepostResult(BaseModel):
    journal_no: str
    success: bool
```

- [ ] **Buat `repository.py`** — pisahkan WHERE builder sebagai pure function agar bisa di-test:

```python
# apps_zakat/api-python/app/modules/transaksi_histori/repository.py
from __future__ import annotations
from app.shared.db import fetch_all, fetch_one

_SORT_MAP = {
    'actual_date':      't.actualdate',
    'transaction_date': 't.transactiondate',
    'transaction_no':   't.transactionno',
    'donor_no':         't.donorno',
    'donor_name':       't.donorname',
    'channel_name':     'f.accountname',
}

_SEARCH_COL = {
    'transno':     't.transactionno',
    'donorno':     't.donorno',
    'donorname':   't.donorname',
    'description': 't.description',
    'refno':       't.referenceno',
}

_TX_SELECT = """
    SELECT
      t.transactionid, t.transactionno,
      to_char(t.transactiondate, 'YYYY-MM-DD') AS transactiondate,
      to_char(t.actualdate,      'YYYY-MM-DD') AS actualdate,
      t.amount::float, t.donorno, t.donorname, t.referenceno,
      t.description, t.inputer, t.authstatus, t.isposted,
      t.branchcode, t.authoperationmode, t.channelaccountno,
      f.accountname AS channelname,
      e.exttransactionid, s.titlesubsystem
    FROM transaction.transaction t
    LEFT JOIN transaction.financialaccount    f ON f.accountno = t.channelaccountno
    LEFT JOIN transaction.externaltransaction e ON e.transactionid = t.transactionid
    LEFT JOIN transaction.accsubsystem        s ON s.subsystemcode = e.subsystemcode
"""

_TX_SELECT_WITH_JOURNAL = _TX_SELECT.replace(
    "    LEFT JOIN transaction.accsubsystem",
    "      , t.journalno\n    LEFT JOIN transaction.accsubsystem",
)


def build_search_where(
    begin: str,
    end: str,
    date_type: str,
    search_category: str,
    search_text: str | None,
    cash_account_no: str | None,
    branch: str | None,
    is_spv: bool,
    user_id: str,
) -> tuple[str, list]:
    """Return (WHERE clause string without 'WHERE', args list).
    Pure function — no DB access — fully unit-testable."""
    date_col = 't.actualdate' if date_type == 'actual' else 't.transactiondate'
    conds: list[str] = [
        f"{date_col}::date >= $1",
        f"{date_col}::date <= $2",
    ]
    args: list = [begin, end]

    if branch:
        args.append(branch)
        conds.append(f"t.branchcode = ${len(args)}")

    if not is_spv and user_id:
        args.append(user_id.upper())
        conds.append(f"UPPER(COALESCE(t.inputer,'')) = ${len(args)}")

    if search_category != 'none' and search_text and search_category in _SEARCH_COL:
        args.append(f'%{search_text.upper()}%')
        conds.append(f"UPPER(COALESCE({_SEARCH_COL[search_category]}, '')) LIKE ${len(args)}")

    if cash_account_no:
        args.append(cash_account_no)
        conds.append(f"t.channelaccountno = ${len(args)}")

    return ' AND '.join(conds), args


async def search_transactions(
    begin: str, end: str,
    date_type: str = 'actual',
    sort_by: str = 'actual_date',
    search_category: str = 'none',
    search_text: str | None = None,
    cash_account_no: str | None = None,
    limit: int = 50,
    branch: str | None = None,
    is_spv: bool = False,
    user_id: str = '',
) -> list[dict]:
    where, args = build_search_where(
        begin, end, date_type, search_category, search_text,
        cash_account_no, branch, is_spv, user_id,
    )
    order_col = _SORT_MAP.get(sort_by, 't.actualdate')
    limit = min(max(1, limit), 500)
    return await fetch_all(
        f"{_TX_SELECT} WHERE {where} ORDER BY {order_col} ASC LIMIT {limit}",
        *args,
    )


async def get_transaction(transaction_id: int) -> dict | None:
    return await fetch_one(
        f"""SELECT t.transactionid, t.transactionno, t.journalno,
              to_char(t.transactiondate,'YYYY-MM-DD') AS transactiondate,
              to_char(t.actualdate,'YYYY-MM-DD') AS actualdate,
              t.amount::float, t.donorno, t.donorname, t.referenceno,
              t.description, t.inputer, t.authstatus, t.isposted,
              t.branchcode, t.authoperationmode, t.channelaccountno,
              f.accountname AS channelname,
              e.exttransactionid, s.titlesubsystem
            FROM transaction.transaction t
            LEFT JOIN transaction.financialaccount    f ON f.accountno = t.channelaccountno
            LEFT JOIN transaction.externaltransaction e ON e.transactionid = t.transactionid
            LEFT JOIN transaction.accsubsystem        s ON s.subsystemcode = e.subsystemcode
            WHERE t.transactionid = $1""",
        transaction_id,
    )


async def get_journal_items(journal_no: str) -> list[dict]:
    return await fetch_all(
        """SELECT ji.journalitem_no, ji.fl_account,
                  a.account_name,
                  ji.branch_code, ji.valuta_code,
                  COALESCE(ji.amount_debit, 0)::float  AS amount_debit,
                  COALESCE(ji.amount_credit, 0)::float AS amount_credit,
                  ji.description, ji.subaccountcode, ji.subaccountname
           FROM transaction.journalitem ji
           LEFT JOIN transaction.account a ON a.account_code = ji.fl_account
           WHERE ji.fl_journal = $1
           ORDER BY ji.journalitem_no""",
        journal_no,
    )


async def get_transaction_items_for_ops(transaction_id: int) -> list[dict]:
    """Fetch transactionitem + accounttransactionitem — used by delete and repost."""
    return await fetch_all(
        """SELECT ti.transactionitemid, ti.mutationtype, ti.amount::float,
                  ati.accounttitype, ati.accountno, ati.fundentity, ati.donorid
           FROM transaction.transactionitem ti
           JOIN transaction.accounttransactionitem ati
             ON ati.transactionitemid = ti.transactionitemid
           WHERE ti.transactionid = $1""",
        transaction_id,
    )
```

- [ ] **Tulis unit tests (WHERE builder saja — export tests ditambah di Task 2 setelah export.py ada):**

```python
# apps_zakat/api-python/tests/test_histori_transaksi.py
from __future__ import annotations
from app.modules.transaksi_histori.repository import build_search_where


# --- WHERE builder tests ---

def test_basic_date_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, None, True, '',
    )
    assert '$1' in where and '$2' in where
    assert args[0] == '2026-06-01'
    assert args[1] == '2026-06-30'


def test_transaction_date_type():
    where, _ = build_search_where(
        '2026-06-01', '2026-06-30', 'transaction', 'none',
        None, None, None, True, '',
    )
    assert 'transactiondate' in where


def test_non_spv_adds_inputer_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, None, False, 'HADI',
    )
    assert 'inputer' in where.lower()
    assert 'HADI' in args


def test_spv_no_inputer_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, None, True, 'HADI',
    )
    assert 'inputer' not in where.lower()


def test_branch_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, None, '001', True, '',
    )
    assert 'branchcode' in where
    assert '001' in args


def test_search_text_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'donorname',
        'budi', None, None, True, '',
    )
    assert 'donorname' in where.lower()
    assert '%BUDI%' in args


def test_cash_account_filter():
    where, args = build_search_where(
        '2026-06-01', '2026-06-30', 'actual', 'none',
        None, 'ACC001', None, True, '',
    )
    assert 'channelaccountno' in where
    assert 'ACC001' in args
```

- [ ] **Run tests:**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -m pytest tests/test_histori_transaksi.py -v
```

Expected: 7 tests PASS.

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaksi_histori/ \
        apps_zakat/api-python/tests/test_histori_transaksi.py
git commit -m "[HISTORI-TRANSAKSI] feat(api-python): schema + repository WHERE builder + unit tests

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: api-python — service.py + export.py

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaksi_histori/service.py`
- Create: `apps_zakat/api-python/app/modules/transaksi_histori/export.py`

- [ ] **Buat `export.py`:**

```python
# apps_zakat/api-python/app/modules/transaksi_histori/export.py
from __future__ import annotations
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from app.modules.transaksi_histori.schema import TransaksiRow

_HEADERS = [
    'No Transaksi', 'Rekening', 'Tgl Transaksi', 'Tgl Aktual',
    'Nominal', 'No Donatur', 'Nama Donatur', 'No Ref',
    'Keterangan', 'Inputer', 'Auth Status', 'Posted', 'Cabang',
]


def _dmy(iso: str | None) -> str:
    if not iso or len(iso) < 10:
        return iso or ''
    return f'{iso[8:10]}-{iso[5:7]}-{iso[:4]}'


def build_histori_xlsx(rows: list[TransaksiRow], begin: str, end: str) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = 'HistoriTransaksi'
    hfill = PatternFill('solid', fgColor='1E40AF')
    hfont = Font(bold=True, color='FFFFFF')
    for ci, h in enumerate(_HEADERS, 1):
        cell = ws.cell(row=1, column=ci, value=h)
        cell.fill = hfill
        cell.font = hfont
        cell.alignment = Alignment(horizontal='center')
    for i, r in enumerate(rows, start=2):
        ws.cell(row=i, column=1,  value=r.transactionno or '')
        ws.cell(row=i, column=2,  value=r.channelname or r.channelaccountno or '')
        ws.cell(row=i, column=3,  value=_dmy(r.transactiondate))
        ws.cell(row=i, column=4,  value=_dmy(r.actualdate))
        ws.cell(row=i, column=5,  value=r.amount)
        ws.cell(row=i, column=6,  value=r.donorno or '')
        ws.cell(row=i, column=7,  value=r.donorname or '')
        ws.cell(row=i, column=8,  value=r.referenceno or '')
        ws.cell(row=i, column=9,  value=r.description or '')
        ws.cell(row=i, column=10, value=r.inputer or '')
        ws.cell(row=i, column=11, value=r.authstatus or '')
        ws.cell(row=i, column=12, value=r.isposted or '')
        ws.cell(row=i, column=13, value=r.branchcode or '')
    buf = BytesIO()
    wb.save(buf)
    return buf.getvalue()
```

- [ ] **Buat `service.py`:**

```python
# apps_zakat/api-python/app/modules/transaksi_histori/service.py
from __future__ import annotations
from datetime import datetime, timezone
from app.modules.transaksi_histori import repository as repo
from app.modules.transaksi_histori.schema import (
    JournalItem, RepostResult, TransaksiDetail, TransaksiRow,
)
from app.shared.db import get_pool


def _to_row(r: dict) -> TransaksiRow:
    return TransaksiRow(
        transactionid=int(r['transactionid']),
        transactionno=r.get('transactionno'),
        transactiondate=str(r.get('transactiondate') or '')[:10],
        actualdate=str(r.get('actualdate') or '')[:10],
        amount=float(r.get('amount') or 0),
        donorno=r.get('donorno'),
        donorname=r.get('donorname'),
        referenceno=r.get('referenceno'),
        description=r.get('description'),
        inputer=r.get('inputer'),
        authstatus=r.get('authstatus'),
        isposted=r.get('isposted'),
        authoperationmode=r.get('authoperationmode'),
        branchcode=r.get('branchcode'),
        channelaccountno=r.get('channelaccountno'),
        channelname=r.get('channelname'),
        exttransactionid=r.get('exttransactionid'),
        titlesubsystem=r.get('titlesubsystem'),
    )


async def search(
    begin: str, end: str,
    date_type: str = 'actual',
    sort_by: str = 'actual_date',
    search_category: str = 'none',
    search_text: str | None = None,
    cash_account_no: str | None = None,
    limit: int = 50,
    branch: str | None = None,
    is_spv: bool = False,
    user_id: str = '',
) -> list[TransaksiRow]:
    rows = await repo.search_transactions(
        begin=begin, end=end, date_type=date_type, sort_by=sort_by,
        search_category=search_category, search_text=search_text,
        cash_account_no=cash_account_no, limit=limit,
        branch=branch, is_spv=is_spv, user_id=user_id,
    )
    return [_to_row(r) for r in rows]


async def detail(transaction_id: int) -> TransaksiDetail | None:
    row = await repo.get_transaction(transaction_id)
    if not row:
        return None
    journal_no = row.get('journalno')
    ji_raw = await repo.get_journal_items(journal_no) if journal_no else []
    journal_items = [
        JournalItem(
            journalitem_no=int(ji['journalitem_no']),
            fl_account=ji.get('fl_account'),
            account_name=ji.get('account_name'),
            branch_code=ji.get('branch_code'),
            valuta_code=ji.get('valuta_code'),
            amount_debit=float(ji.get('amount_debit') or 0),
            amount_credit=float(ji.get('amount_credit') or 0),
            description=ji.get('description'),
            subaccountcode=ji.get('subaccountcode'),
            subaccountname=ji.get('subaccountname'),
        )
        for ji in ji_raw
    ]
    return TransaksiDetail(**_to_row(row).model_dump(), journal_items=journal_items)


async def repost_journal(
    transaction_id: int,
    user_id: str,
    branch_code: str,
    is_spv: bool,
) -> RepostResult:
    pool = get_pool()
    async with pool.acquire() as conn:
        tx = await conn.fetchrow(
            """SELECT transactionid, transactionno, transactiondate,
                      branchcode, isposted
               FROM transaction.transaction WHERE transactionid = $1""",
            transaction_id,
        )
        if not tx:
            raise LookupError(f'Transaksi {transaction_id} tidak ditemukan')
        if not is_spv and (tx['branchcode'] or '').strip() != (branch_code or '').strip():
            raise PermissionError('BRANCH_FORBIDDEN')
        if (tx['isposted'] or 'F') == 'T':
            raise ValueError('ALREADY_POSTED')

        items = await conn.fetch(
            """SELECT ti.transactionitemid, ti.amount::float,
                      ati.accounttitype, ati.accountno
               FROM transaction.transactionitem ti
               JOIN transaction.accounttransactionitem ati
                 ON ati.transactionitemid = ti.transactionitemid
               WHERE ti.transactionid = $1""",
            transaction_id,
        )

        trans_date = tx['transactiondate']
        branch = (tx['branchcode'] or branch_code or '001').strip()
        year = trans_date.year if hasattr(trans_date, 'year') else int(str(trans_date)[:4])

        async with conn.transaction():
            seq = await conn.fetchval(
                "SELECT nextval('transaction.seq_transactionnumber')"
            )
            journal_no = f'J{branch}-{year}-{seq:07d}'

            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_date, journal_date_posting, description,
                    userid_create, branch_code, is_posted, status, source_app)
                   VALUES ($1,$2,$2,$3,$4,$5,'T','A','isf-app')""",
                journal_no, trans_date, tx['transactionno'], user_id, branch,
            )

            item_no = 1
            for item in items:
                if item['accounttitype'] == 'D':
                    await conn.execute(
                        """INSERT INTO transaction.journalitem
                           (fl_journal, journalitem_no, fl_account,
                            amount_credit, amount_debit, branch_code, valuta_code, userid_create)
                           VALUES ($1,$2,$3,$4,0,$5,'IDR',$6)""",
                        journal_no, item_no, item['accountno'],
                        item['amount'], branch, user_id,
                    )
                elif item['accounttitype'] == 'A':
                    await conn.execute(
                        """INSERT INTO transaction.journalitem
                           (fl_journal, journalitem_no, fl_account,
                            amount_debit, amount_credit, branch_code, valuta_code, userid_create)
                           VALUES ($1,$2,$3,$4,0,$5,'IDR',$6)""",
                        journal_no, item_no, item['accountno'],
                        item['amount'], branch, user_id,
                    )
                item_no += 1

            jblock_id = await conn.fetchval(
                "SELECT nextval('transaction.seq_journalblock')"
            )
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, journal_no, system_id, class_id, key_id)
                   VALUES ($1,$2,'TRANS','Transaction',$3)""",
                jblock_id, journal_no, transaction_id,
            )
            await conn.execute(
                "UPDATE transaction.transaction SET journalno=$1, isposted='T' WHERE transactionid=$2",
                journal_no, transaction_id,
            )

    return RepostResult(journal_no=journal_no, success=True)
```

- [ ] **Tambah export + dmy tests ke `tests/test_histori_transaksi.py`** — append di akhir file:

```python
from app.modules.transaksi_histori.export import build_histori_xlsx, _dmy
from app.modules.transaksi_histori.schema import TransaksiRow


def _sample_row(**kw) -> TransaksiRow:
    base = dict(
        transactionid=1, transactionno='TX-001',
        transactiondate='2026-06-01', actualdate='2026-06-01',
        amount=100000.0, donorno='D001', donorname='Budi',
        referenceno='REF01', description='Test', inputer='HADI',
        authstatus='T', isposted='T', authoperationmode=None,
        branchcode='001', channelaccountno='ACC001', channelname='Bank A',
        exttransactionid=None, titlesubsystem=None,
    )
    base.update(kw)
    return TransaksiRow(**base)


def test_dmy_converts_iso():
    assert _dmy('2026-06-01') == '01-06-2026'


def test_dmy_handles_none():
    assert _dmy(None) == ''


def test_export_returns_bytes():
    rows = [_sample_row(), _sample_row(transactionid=2, transactionno='TX-002')]
    result = build_histori_xlsx(rows, '2026-06-01', '2026-06-30')
    assert isinstance(result, bytes)
    assert len(result) > 100
```

- [ ] **Run all tests:**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -m pytest tests/test_histori_transaksi.py -v
```

Expected: 10 tests PASS.

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaksi_histori/service.py \
        apps_zakat/api-python/app/modules/transaksi_histori/export.py
git commit -m "[HISTORI-TRANSAKSI] feat(api-python): service layer + XLSX export

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: api-python — delete.py

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaksi_histori/delete.py`

- [ ] **Buat `delete.py`:**

```python
# apps_zakat/api-python/app/modules/transaksi_histori/delete.py
"""Delete transaksi dua jalur:
  - authstatus='F': hapus langsung (reverse journal + balance jika sudah posted)
  - authstatus='T': tandai untuk dihapus (perlu approval supervisor)
"""
from __future__ import annotations
from datetime import datetime, timezone
from app.modules.transaksi_histori.schema import DeleteResult
from app.shared.db import get_pool


async def delete_transaction(
    transaction_id: int,
    user_id: str,
    branch_code: str,
    is_spv: bool,
) -> DeleteResult:
    pool = get_pool()
    async with pool.acquire() as conn:
        tx = await conn.fetchrow(
            """SELECT transactionid, transactionno, branchcode,
                      authstatus, authoperationmode, isposted, journalno
               FROM transaction.transaction WHERE transactionid = $1""",
            transaction_id,
        )
        if not tx:
            raise LookupError(f'Transaksi {transaction_id} tidak ditemukan')

        if not is_spv and (tx['branchcode'] or '').strip() != (branch_code or '').strip():
            raise PermissionError('BRANCH_FORBIDDEN')

        ext = await conn.fetchrow(
            "SELECT exttransactionid FROM transaction.externaltransaction "
            "WHERE transactionid = $1",
            transaction_id,
        )
        if ext:
            raise ValueError('EXTERNAL_TX')

        if (tx['authstatus'] or 'F') == 'F' and (tx['authoperationmode'] or '') == 'D':
            raise ValueError('ALREADY_PENDING_DELETE')

        if (tx['authstatus'] or 'F') == 'F':
            # Case A: unauth — delete immediately
            async with conn.transaction():
                if (tx['isposted'] or 'F') == 'T' and tx['journalno']:
                    jno = tx['journalno']
                    # Fetch items to reverse balances
                    items = await conn.fetch(
                        """SELECT ti.amount::float,
                                  ati.accounttitype, ati.accountno,
                                  ati.fundentity, ati.donorid
                           FROM transaction.transactionitem ti
                           JOIN transaction.accounttransactionitem ati
                             ON ati.transactionitemid = ti.transactionitemid
                           WHERE ti.transactionid = $1""",
                        transaction_id,
                    )
                    for item in items:
                        # Reverse balance on every account (both product and bank were +amount)
                        await conn.execute(
                            "UPDATE transaction.financialaccount "
                            "SET balance = COALESCE(balance,0) - $1 WHERE accountno = $2",
                            item['amount'], item['accountno'],
                        )
                        # Reverse donortotalfund only for product (type 'D') items
                        if item['accounttitype'] == 'D' and item['donorid'] and item['fundentity']:
                            existing = await conn.fetchrow(
                                """SELECT totalfundid FROM fund.donortotalfund
                                   WHERE donorid = $1 AND fundentity = $2
                                   ORDER BY totalfundid LIMIT 1""",
                                item['donorid'], item['fundentity'],
                            )
                            if existing:
                                await conn.execute(
                                    "UPDATE fund.donortotalfund "
                                    "SET totalamount = COALESCE(totalamount,0) - $1 "
                                    "WHERE totalfundid = $2",
                                    item['amount'], int(existing['totalfundid']),
                                )
                    # Delete journal
                    await conn.execute(
                        "DELETE FROM transaction.journalblock WHERE journal_no = $1", jno
                    )
                    await conn.execute(
                        "DELETE FROM transaction.journalitem WHERE fl_journal = $1", jno
                    )
                    await conn.execute(
                        "DELETE FROM transaction.journal WHERE journal_no = $1", jno
                    )

                # Delete transaction records
                await conn.execute(
                    """DELETE FROM transaction.accounttransactionitem
                       WHERE transactionitemid IN (
                           SELECT transactionitemid FROM transaction.transactionitem
                           WHERE transactionid = $1
                       )""",
                    transaction_id,
                )
                await conn.execute(
                    "DELETE FROM transaction.transactionitem WHERE transactionid = $1",
                    transaction_id,
                )
                await conn.execute(
                    "DELETE FROM transaction.transaction WHERE transactionid = $1",
                    transaction_id,
                )
                hist_id = await conn.fetchval(
                    "SELECT nextval('transaction.seq_transhistoryofchanges')"
                )
                await conn.execute(
                    """INSERT INTO transaction.transhistoryofchanges
                       (historyid, transactionid, transactionno, userid, processtime, changetype)
                       VALUES ($1,$2,$3,$4,$5,'D')""",
                    hist_id, transaction_id, tx['transactionno'],
                    user_id, datetime.now(timezone.utc),
                )
            return DeleteResult(
                deleted=True, pending_approval=False,
                message='Transaksi berhasil dihapus',
            )

        else:
            # Case B: auth — mark for supervisor approval
            await conn.execute(
                "UPDATE transaction.transaction "
                "SET authstatus='F', authoperationmode='D' WHERE transactionid=$1",
                transaction_id,
            )
            return DeleteResult(
                deleted=False, pending_approval=True,
                message='Transaksi ditandai untuk dihapus, menunggu otorisasi supervisor',
            )
```

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaksi_histori/delete.py
git commit -m "[HISTORI-TRANSAKSI] feat(api-python): delete dua jalur + reverse journal/balance

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: api-python — router.py + main.py wiring

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaksi_histori/router.py`
- Modify: `apps_zakat/api-python/app/main.py`

- [ ] **Buat `router.py`:**

```python
# apps_zakat/api-python/app/modules/transaksi_histori/router.py
from __future__ import annotations
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from app.modules.transaksi_histori import service
from app.modules.transaksi_histori.delete import delete_transaction
from app.modules.transaksi_histori.export import build_histori_xlsx
from app.shared.db import ping
from app.shared.response import err, ok

router = APIRouter(prefix='/transaksi-histori', tags=['transaksi-histori'])
_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


class DeleteRequest(BaseModel):
    user_id: str
    branch_code: str
    is_spv: bool = False


class RepostRequest(BaseModel):
    user_id: str
    branch_code: str
    is_spv: bool = False


@router.get('/search')
async def search(
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
    branch: str | None = Query(default=None),
    is_spv: bool = Query(default=False),
    user_id: str = Query(default=''),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    rows = await service.search(
        begin=begin, end=end, date_type=date_type, sort_by=sort_by,
        search_category=search_category, search_text=search_text,
        cash_account_no=cash_account_no, limit=limit,
        branch=branch, is_spv=is_spv, user_id=user_id,
    )
    return ok([r.model_dump() for r in rows])


@router.get('/search/export.xlsx')
async def search_export(
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    is_spv: bool = Query(default=False),
    user_id: str = Query(default=''),
):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    rows = await service.search(
        begin=begin, end=end, date_type=date_type, sort_by=sort_by,
        search_category=search_category, search_text=search_text,
        cash_account_no=cash_account_no, limit=500,
        branch=branch, is_spv=is_spv, user_id=user_id,
    )
    xlsx = build_histori_xlsx(rows, begin, end)
    fname = f'histori-transaksi-{begin}-{end}.xlsx'
    return Response(
        content=xlsx,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': f'attachment; filename="{fname}"'},
    )


@router.get('/transactions/{transaction_id}')
async def get_detail(transaction_id: int):
    if not await ping():
        return JSONResponse(status_code=503, content=err('DB_UNAVAILABLE', 'Database not ready'))
    result = await service.detail(transaction_id)
    if not result:
        return JSONResponse(
            status_code=404,
            content=err('NOT_FOUND', f'Transaksi {transaction_id} tidak ditemukan'),
        )
    return ok(result.model_dump())


@router.post('/transactions/{transaction_id}/delete')
async def do_delete(transaction_id: int, req: DeleteRequest):
    try:
        result = await delete_transaction(
            transaction_id, req.user_id, req.branch_code, req.is_spv
        )
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except PermissionError:
        return JSONResponse(
            status_code=403,
            content=err('BRANCH_FORBIDDEN', 'Anda tidak dapat menghapus transaksi milik cabang lain'),
        )
    except ValueError as exc:
        code = str(exc)
        if code == 'EXTERNAL_TX':
            return JSONResponse(
                status_code=400,
                content=err('EXTERNAL_TX', 'Transaksi dari sistem eksternal tidak dapat dihapus'),
            )
        if code == 'ALREADY_PENDING_DELETE':
            return JSONResponse(
                status_code=409,
                content=err('ALREADY_PENDING_DELETE', 'Transaksi sudah dalam antrean hapus'),
            )
        return JSONResponse(status_code=400, content=err('DELETE_ERROR', code))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())


@router.post('/transactions/{transaction_id}/repost')
async def do_repost(transaction_id: int, req: RepostRequest):
    try:
        result = await service.repost_journal(
            transaction_id, req.user_id, req.branch_code, req.is_spv
        )
    except LookupError as exc:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', str(exc)))
    except PermissionError:
        return JSONResponse(
            status_code=403,
            content=err('BRANCH_FORBIDDEN', 'Anda tidak dapat memproses transaksi milik cabang lain'),
        )
    except ValueError as exc:
        if 'ALREADY_POSTED' in str(exc):
            return JSONResponse(
                status_code=409,
                content=err('ALREADY_POSTED', 'Transaksi sudah di-posting'),
            )
        return JSONResponse(status_code=400, content=err('REPOST_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())
```

- [ ] **Edit `apps_zakat/api-python/app/main.py`** — tambahkan setelah baris `from app.modules.transaction.router`:

```python
from app.modules.transaksi_histori.router import router as transaksi_histori_router
```

Dan di bawah `app.include_router(transaction_router, prefix="/api")`:

```python
app.include_router(transaksi_histori_router, prefix="/api")
```

- [ ] **Verify syntax:**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python3 -c "from app.modules.transaksi_histori.router import router; print('router OK')"
python3 -c "from app.main import app; print('main OK')"
```

Expected: masing-masing cetak OK.

- [ ] **Test parse endpoint:**

```bash
curl -s "http://localhost:8001/api/transaksi-histori/search?begin=2026-06-01&end=2026-06-30&is_spv=true&user_id=TEST" 2>/dev/null \
  | python3 -m json.tool | head -10 || echo "service not running — syntax verified only"
```

- [ ] **Commit:**

```bash
git add apps_zakat/api-python/app/modules/transaksi_histori/router.py \
        apps_zakat/api-python/app/main.py
git commit -m "[HISTORI-TRANSAKSI] feat(api-python): router + main.py wiring

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: BFF — proxy + router + main.py

**Files:**
- Modify: `apps_zakat/bff-api/app/services/proxy.py`
- Create: `apps_zakat/bff-api/app/routers/histori_transaksi.py`
- Modify: `apps_zakat/bff-api/app/main.py`

- [ ] **Append `stream_api_python` ke `proxy.py`:**

```python
async def stream_api_python(path: str, params: dict | None = None) -> httpx.Response:
    """GET biner ke api-python (mis. export .xlsx). Timeout lebih longgar untuk generate file."""
    url = f"{settings.api_python_base_url}{path}"
    async with httpx.AsyncClient(timeout=60.0) as client:
        return await client.get(url, params=params)
```

- [ ] **Buat `apps_zakat/bff-api/app/routers/histori_transaksi.py`:**

```python
# apps_zakat/bff-api/app/routers/histori_transaksi.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse, Response

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python, stream_api_python

router = APIRouter(prefix='/transaksi-histori', tags=['transaksi-histori'])

_MENU = 'keuangan.transaksi.histori'
_XLSX_MIME = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'


def _inject(request: Request) -> dict:
    """Derive is_spv, user_id, branch from session."""
    roles = request.session.get('roles') or []
    is_spv = 'SPVKEU' in roles
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'is_spv': is_spv, 'user_id': user_id, 'branch': branch}


@router.get('/search')
async def search(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=500),
):
    inj = _inject(request)
    params: dict = {
        'begin': begin, 'end': end, 'date_type': date_type,
        'sort_by': sort_by, 'search_category': search_category,
        'limit': limit,
        'is_spv': str(inj['is_spv']).lower(),
        'user_id': inj['user_id'],
    }
    if inj['branch']:
        params['branch'] = inj['branch']
    if search_text:
        params['search_text'] = search_text
    if cash_account_no:
        params['cash_account_no'] = cash_account_no
    downstream = await get_api_python('/api/transaksi-histori/search', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/search/export.xlsx')
async def search_export(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    date_type: str = Query(default='actual'),
    sort_by: str = Query(default='actual_date'),
    search_category: str = Query(default='none'),
    search_text: str | None = Query(default=None),
    cash_account_no: str | None = Query(default=None),
):
    inj = _inject(request)
    params: dict = {
        'begin': begin, 'end': end, 'date_type': date_type,
        'sort_by': sort_by, 'search_category': search_category,
        'is_spv': str(inj['is_spv']).lower(), 'user_id': inj['user_id'],
    }
    if inj['branch']:
        params['branch'] = inj['branch']
    if search_text:
        params['search_text'] = search_text
    if cash_account_no:
        params['cash_account_no'] = cash_account_no
    downstream = await stream_api_python(
        '/api/transaksi-histori/search/export.xlsx', params=params
    )
    if downstream.status_code != 200:
        return JSONResponse(status_code=downstream.status_code, content=downstream.json())
    fname = f'histori-transaksi-{begin}-{end}.xlsx'
    return Response(
        content=downstream.content,
        media_type=_XLSX_MIME,
        headers={'Content-Disposition': f'attachment; filename="{fname}"'},
    )


@router.get('/transactions/{transaction_id}')
async def get_detail(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(
        f'/api/transaksi-histori/transactions/{transaction_id}'
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/transactions/{transaction_id}/delete')
async def do_delete(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    inj = _inject(request)
    downstream = await post_api_python(
        f'/api/transaksi-histori/transactions/{transaction_id}/delete',
        json_body={
            'user_id': inj['user_id'],
            'branch_code': inj['branch'],
            'is_spv': inj['is_spv'],
        },
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/transactions/{transaction_id}/repost')
async def do_repost(
    request: Request,
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    inj = _inject(request)
    downstream = await post_api_python(
        f'/api/transaksi-histori/transactions/{transaction_id}/repost',
        json_body={
            'user_id': inj['user_id'],
            'branch_code': inj['branch'],
            'is_spv': inj['is_spv'],
        },
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())
```

- [ ] **Edit `apps_zakat/bff-api/app/main.py`** — tambahkan setelah baris `from app.routers.transaction import router as transaction_router`:

```python
from app.routers.histori_transaksi import router as histori_transaksi_router
```

Dan di bawah `app.include_router(transaction_router, prefix="/api")`:

```python
app.include_router(histori_transaksi_router, prefix="/api")
```

- [ ] **Verify syntax:**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/bff-api
python3 -c "from app.routers.histori_transaksi import router; print('BFF router OK')"
```

- [ ] **Commit:**

```bash
git add apps_zakat/bff-api/app/services/proxy.py \
        apps_zakat/bff-api/app/routers/histori_transaksi.py \
        apps_zakat/bff-api/app/main.py
git commit -m "[HISTORI-TRANSAKSI] feat(bff): BFF router histori transaksi + stream_api_python

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Menu & auth wiring

**Files:**
- Modify: `apps_zakat/web-vue/src/lib/menu/registry.ts`
- Modify: `infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql`

- [ ] **Edit `registry.ts`** — tambah key sebelum `'keuangan.upload.penghimpunan'`:

```typescript
  'keuangan.transaksi.histori',
```

- [ ] **Append ke `seed-menu-and-rolemenu.sql`:**

```sql

-- Histori Transaksi (2026-06-05)
INSERT INTO isf_auth.menu (key, label)
VALUES ('keuangan.transaksi.histori', 'Histori Transaksi')
ON CONFLICT (key) DO NOTHING;

INSERT INTO isf_auth.role_menu (role_id, menu_key)
SELECT r.id_peran, 'keuangan.transaksi.histori'
FROM enterprise.peran r
WHERE r.id_peran IN ('KEU','SPVKEU','ADM','ACC')
ON CONFLICT DO NOTHING;
```

- [ ] **Apply seed:**

```bash
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -f infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql
```

- [ ] **Verify:**

```bash
PGPASSWORD=solusi psql -h localhost -U transaction -d isf_auth_zakat \
  -c "SELECT key FROM isf_auth.menu WHERE key = 'keuangan.transaksi.histori'"
```

Expected: 1 baris.

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/lib/menu/registry.ts \
        infra/db/migrations/isf_auth/seed-menu-and-rolemenu.sql
git commit -m "[HISTORI-TRANSAKSI] chore(auth): menu key + role_menu seed histori transaksi

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: Frontend — HistoriTransaksiPage.vue

**Files:**
- Create: `apps_zakat/web-vue/src/pages/keuangan/HistoriTransaksiPage.vue`

- [ ] **Buat file:**

```vue
<script setup lang="ts">
import { Download, History, Search } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { BASE_URL } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'

interface TransaksiRow {
  transactionid: number
  transactionno: string | null
  transactiondate: string
  actualdate: string
  amount: number
  donorno: string | null
  donorname: string | null
  referenceno: string | null
  description: string | null
  inputer: string | null
  authstatus: string | null
  isposted: string | null
  authoperationmode: string | null
  branchcode: string | null
  channelname: string | null
  exttransactionid: number | null
}

const router = useRouter()
const auth = useAuthStore()
const today = new Date().toISOString().slice(0, 10)
const begin = ref(today)
const end = ref(today)
const dateType = ref('actual')
const sortBy = ref('actual_date')
const searchCategory = ref('none')
const searchText = ref('')
const cashAccountNo = ref('')
const limitRows = ref(50)

const rows = ref<TransaksiRow[]>([])
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)
const hasLoaded = ref(false)

const deleteConfirmId = ref<number | null>(null)
const deleteMsg = ref<string | null>(null)
const deleting = ref(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function canDelete(row: TransaksiRow): boolean {
  if (row.exttransactionid != null) return false
  if (row.authstatus === 'F' && row.authoperationmode === 'D') return false
  return true
}

function authChip(s: string | null) {
  return s === 'T' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
}
function authLabel(s: string | null) {
  return s === 'T' ? 'Terotorisasi' : 'Pending'
}
function postedChip(s: string | null) {
  return s === 'T' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'
}

function buildParams(extra: Record<string, string> = {}): string {
  const p = new URLSearchParams({
    begin: begin.value, end: end.value,
    date_type: dateType.value, sort_by: sortBy.value,
    search_category: searchCategory.value,
    limit: String(limitRows.value),
    ...extra,
  })
  if (searchCategory.value !== 'none' && searchText.value)
    p.set('search_text', searchText.value)
  if (cashAccountNo.value)
    p.set('cash_account_no', cashAccountNo.value)
  return p.toString()
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/transaksi-histori/search?${buildParams()}`, {
      credentials: 'include',
    })
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Gagal memuat data')
    rows.value = payload.data
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  exporting.value = true
  try {
    const res = await fetch(
      `${BASE_URL}/api/transaksi-histori/search/export.xlsx?${buildParams()}`,
      { credentials: 'include' },
    )
    if (!res.ok) throw new Error('Export gagal')
    const disp = res.headers.get('Content-Disposition') ?? ''
    const match = /filename\s*=\s*"?([^";]+)"?/i.exec(disp)
    const filename = match?.[1] ?? `histori-transaksi-${begin.value}-${end.value}.xlsx`
    const blob = await res.blob()
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = filename
    a.click()
    setTimeout(() => URL.revokeObjectURL(a.href), 1000)
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    exporting.value = false
  }
}

async function confirmDelete() {
  if (!deleteConfirmId.value) return
  deleting.value = true
  deleteMsg.value = null
  try {
    const res = await fetch(
      `${BASE_URL}/api/transaksi-histori/transactions/${deleteConfirmId.value}/delete`,
      {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: '{}',
      },
    )
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Hapus gagal')
    const result = payload.data
    deleteConfirmId.value = null
    if (result.deleted) {
      rows.value = rows.value.filter((r) => r.transactionid !== deleteConfirmId.value)
      await load()
    } else {
      // pending approval — update row status
      await load()
    }
  } catch (e: unknown) {
    deleteMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <History class="h-5 w-5 text-primary" />
      <h1 class="text-lg font-semibold">Histori Transaksi</h1>
    </div>

    <!-- Filter bar -->
    <div class="mb-4 flex flex-wrap items-end gap-3">
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Dari</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Sampai</label>
        <DateField v-model="end" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Tipe Tanggal</label>
        <select v-model="dateType" class="rounded border border-border bg-background px-2 py-1.5 text-sm">
          <option value="actual">Aktual</option>
          <option value="transaction">Transaksi</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Urut</label>
        <select v-model="sortBy" class="rounded border border-border bg-background px-2 py-1.5 text-sm">
          <option value="actual_date">Tgl Aktual</option>
          <option value="transaction_date">Tgl Transaksi</option>
          <option value="transaction_no">No Transaksi</option>
          <option value="donor_no">No Donatur</option>
          <option value="donor_name">Nama Donatur</option>
          <option value="channel_name">Rekening</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Cari</label>
        <div class="flex gap-1">
          <select v-model="searchCategory" class="rounded border border-border bg-background px-2 py-1.5 text-sm">
            <option value="none">(Semua)</option>
            <option value="transno">No Transaksi</option>
            <option value="donorno">No Donatur</option>
            <option value="donorname">Nama Donatur</option>
            <option value="description">Keterangan</option>
            <option value="refno">No Referensi</option>
          </select>
          <input
            v-model="searchText"
            :disabled="searchCategory === 'none'"
            placeholder="Teks cari..."
            class="rounded border border-border bg-background px-2 py-1.5 text-sm w-36 disabled:opacity-50"
          />
        </div>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Rekening</label>
        <input
          v-model="cashAccountNo"
          placeholder="Opsional"
          class="rounded border border-border bg-background px-2 py-1.5 text-sm w-28"
        />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Max Baris</label>
        <input
          v-model.number="limitRows"
          type="number"
          min="1"
          max="500"
          class="rounded border border-border bg-background px-2 py-1.5 text-sm w-20"
        />
      </div>
      <Button :disabled="loading" @click="load">
        <Search class="mr-1 h-3.5 w-3.5" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
      <Button
        v-if="hasLoaded && rows.length"
        variant="outline"
        :disabled="exporting"
        @click="exportXlsx"
      >
        <Download class="mr-1 h-3.5 w-3.5" />
        {{ exporting ? 'Mengekspor...' : 'Export XLSX' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="error" :message="errorMsg" class="mb-3" />

    <div v-if="hasLoaded" class="overflow-x-auto rounded-lg border border-border">
      <table v-if="rows.length" class="w-full text-xs">
        <thead class="bg-surface">
          <tr>
            <th class="px-2 py-1.5 text-left">No</th>
            <th class="px-2 py-1.5 text-left">No Transaksi</th>
            <th class="px-2 py-1.5 text-left">Rekening</th>
            <th class="px-2 py-1.5 text-left whitespace-nowrap">Tgl Aktual</th>
            <th class="px-2 py-1.5 text-left whitespace-nowrap">Tgl Transaksi</th>
            <th class="px-2 py-1.5 text-right">Nominal</th>
            <th class="px-2 py-1.5 text-left">No Donatur</th>
            <th class="px-2 py-1.5 text-left min-w-[120px]">Nama Donatur</th>
            <th class="px-2 py-1.5 text-left">No Ref</th>
            <th class="px-2 py-1.5 text-left min-w-[140px]">Keterangan</th>
            <th class="px-2 py-1.5 text-left">Inputer</th>
            <th class="px-2 py-1.5 text-left">Status</th>
            <th class="px-2 py-1.5 text-left">Posted</th>
            <th class="px-2 py-1.5 text-left">Cabang</th>
            <th class="px-2 py-1.5 text-left">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, i) in rows"
            :key="row.transactionid"
            class="border-t border-border hover:bg-background cursor-pointer"
            @click="router.push(`/keuangan/transaksi/histori/${row.transactionid}`)"
          >
            <td class="px-2 py-1 text-center">{{ i + 1 }}</td>
            <td class="px-2 py-1 font-mono text-[10px]">{{ row.transactionno ?? '—' }}</td>
            <td class="px-2 py-1 max-w-[100px] truncate" :title="row.channelname ?? ''">
              {{ row.channelname ?? row.transactionno }}
            </td>
            <td class="px-2 py-1 whitespace-nowrap">{{ dmy(row.actualdate) }}</td>
            <td class="px-2 py-1 whitespace-nowrap">{{ dmy(row.transactiondate) }}</td>
            <td class="px-2 py-1 text-right">{{ fmt(row.amount) }}</td>
            <td class="px-2 py-1">{{ row.donorno ?? '' }}</td>
            <td class="px-2 py-1 max-w-[140px] truncate" :title="row.donorname ?? ''">
              {{ row.donorname ?? '' }}
            </td>
            <td class="px-2 py-1">{{ row.referenceno ?? '' }}</td>
            <td class="px-2 py-1 max-w-[160px] truncate" :title="row.description ?? ''">
              {{ row.description ?? '' }}
            </td>
            <td class="px-2 py-1">{{ row.inputer ?? '' }}</td>
            <td class="px-2 py-1">
              <span :class="['rounded px-1 py-0.5 text-[9px] font-medium uppercase', authChip(row.authstatus)]">
                {{ authLabel(row.authstatus) }}
              </span>
            </td>
            <td class="px-2 py-1">
              <span :class="['rounded px-1 py-0.5 text-[9px] font-medium', postedChip(row.isposted)]">
                {{ row.isposted === 'T' ? 'Posted' : 'Belum' }}
              </span>
            </td>
            <td class="px-2 py-1">{{ row.branchcode ?? '' }}</td>
            <td class="px-2 py-1" @click.stop>
              <Button
                v-if="canDelete(row)"
                size="sm"
                variant="outline"
                class="text-red-600 hover:bg-red-50 border-red-200 text-[10px] px-1.5 py-0.5"
                @click="deleteConfirmId = row.transactionid; deleteMsg = null"
              >Hapus</Button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="p-6 text-center text-sm text-muted">Tidak ada transaksi ditemukan.</div>
    </div>
    <div v-else-if="!loading" class="text-sm text-muted">Klik "Tampilkan" untuk memuat data.</div>

    <!-- Delete confirm dialog -->
    <div
      v-if="deleteConfirmId !== null"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
    >
      <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-2 font-semibold">Konfirmasi Hapus Transaksi</h2>
        <p class="mb-4 text-sm text-muted">
          Transaksi #{{ deleteConfirmId }} akan dihapus. Jika sudah terotorisasi, akan masuk antrean
          approval supervisor. Lanjutkan?
        </p>
        <Alert v-if="deleteMsg" variant="error" :message="deleteMsg" class="mb-3" />
        <div class="flex justify-end gap-3">
          <Button variant="outline" :disabled="deleting" @click="deleteConfirmId = null">Batal</Button>
          <Button
            class="bg-red-600 hover:bg-red-700 text-white"
            :disabled="deleting"
            @click="confirmDelete"
          >
            {{ deleting ? 'Memproses...' : 'Ya, Hapus' }}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/HistoriTransaksiPage.vue
git commit -m "[HISTORI-TRANSAKSI] feat(web-vue): halaman search histori transaksi

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: Frontend — HistoriTransaksiDetailPage.vue

**Files:**
- Create: `apps_zakat/web-vue/src/pages/keuangan/HistoriTransaksiDetailPage.vue`

- [ ] **Buat file:**

```vue
<script setup lang="ts">
import { ArrowLeft, RefreshCw, Trash2 } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { api, ApiError, BASE_URL } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'

interface JournalItem {
  journalitem_no: number
  fl_account: string | null
  account_name: string | null
  branch_code: string | null
  amount_debit: number
  amount_credit: number
  description: string | null
}

interface TransaksiDetail {
  transactionid: number
  transactionno: string | null
  transactiondate: string
  actualdate: string
  amount: number
  donorno: string | null
  donorname: string | null
  referenceno: string | null
  description: string | null
  inputer: string | null
  authstatus: string | null
  isposted: string | null
  authoperationmode: string | null
  branchcode: string | null
  channelaccountno: string | null
  channelname: string | null
  exttransactionid: number | null
  titlesubsystem: string | null
  journal_items: JournalItem[]
}

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const txId = Number(route.params.id)
const detail = ref<TransaksiDetail | null>(null)
const loading = ref(true)
const errorMsg = ref<string | null>(null)

const showDeleteConfirm = ref(false)
const deleting = ref(false)
const deleteError = ref<string | null>(null)

const showRepostConfirm = ref(false)
const reposting = ref(false)
const repostError = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const hasActions = computed(() => detail.value?.exttransactionid == null)
const canDelete = computed(() => {
  if (!detail.value) return false
  if (detail.value.authstatus === 'F' && detail.value.authoperationmode === 'D') return false
  return true
})
const canRepost = computed(() => detail.value?.isposted === 'F')

onMounted(async () => {
  try {
    detail.value = await api.get<TransaksiDetail>(
      `/api/transaksi-histori/transactions/${txId}`,
    )
  } catch (e: unknown) {
    errorMsg.value = e instanceof ApiError ? e.message : String(e)
  } finally {
    loading.value = false
  }
})

async function doDelete() {
  deleting.value = true
  deleteError.value = null
  try {
    const res = await fetch(
      `${BASE_URL}/api/transaksi-histori/transactions/${txId}/delete`,
      {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: '{}',
      },
    )
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Hapus gagal')
    showDeleteConfirm.value = false
    router.push('/keuangan/transaksi/histori')
  } catch (e: unknown) {
    deleteError.value = e instanceof Error ? e.message : String(e)
  } finally {
    deleting.value = false
  }
}

async function doRepost() {
  reposting.value = true
  repostError.value = null
  try {
    const res = await fetch(
      `${BASE_URL}/api/transaksi-histori/transactions/${txId}/repost`,
      {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: '{}',
      },
    )
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Re-post gagal')
    showRepostConfirm.value = false
    // Reload detail
    detail.value = await api.get<TransaksiDetail>(
      `/api/transaksi-histori/transactions/${txId}`,
    )
  } catch (e: unknown) {
    repostError.value = e instanceof Error ? e.message : String(e)
  } finally {
    reposting.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <button class="text-muted hover:text-foreground" @click="router.back()">
        <ArrowLeft class="h-4 w-4" />
      </button>
      <h1 class="text-lg font-semibold">Detail Transaksi #{{ txId }}</h1>
    </div>

    <div v-if="loading" class="text-sm text-muted">Memuat...</div>
    <Alert v-else-if="errorMsg" variant="error" :message="errorMsg" />

    <template v-else-if="detail">
      <!-- Header card -->
      <div class="mb-4 grid grid-cols-2 gap-3 rounded-lg border border-border bg-surface p-4 text-sm">
        <div><span class="text-muted">No Transaksi:</span> {{ detail.transactionno ?? '—' }}</div>
        <div><span class="text-muted">Rekening:</span> {{ detail.channelname ?? detail.channelaccountno ?? '—' }}</div>
        <div><span class="text-muted">Tgl Aktual:</span> {{ dmy(detail.actualdate) }}</div>
        <div><span class="text-muted">Tgl Transaksi:</span> {{ dmy(detail.transactiondate) }}</div>
        <div><span class="text-muted">Nominal:</span> Rp {{ fmt(detail.amount) }}</div>
        <div><span class="text-muted">Inputer:</span> {{ detail.inputer ?? '—' }}</div>
        <div><span class="text-muted">No Donatur:</span> {{ detail.donorno ?? '—' }}</div>
        <div><span class="text-muted">Nama Donatur:</span> {{ detail.donorname ?? '—' }}</div>
        <div><span class="text-muted">No Ref:</span> {{ detail.referenceno ?? '—' }}</div>
        <div><span class="text-muted">Keterangan:</span> {{ detail.description ?? '—' }}</div>
        <div><span class="text-muted">Cabang:</span> {{ detail.branchcode ?? '—' }}</div>
        <div>
          <span class="text-muted">Auth Status:</span>
          <span :class="['ml-1 rounded px-1 py-0.5 text-[9px] font-medium uppercase',
            detail.authstatus === 'T' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800']">
            {{ detail.authstatus === 'T' ? 'Terotorisasi' : 'Pending' }}
          </span>
        </div>
        <div>
          <span class="text-muted">Posted:</span>
          <span :class="['ml-1 rounded px-1 py-0.5 text-[9px] font-medium',
            detail.isposted === 'T' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600']">
            {{ detail.isposted === 'T' ? 'Posted' : 'Belum' }}
          </span>
        </div>
        <div v-if="detail.titlesubsystem">
          <span class="text-muted">Sub-sistem:</span> {{ detail.titlesubsystem }}
        </div>
      </div>

      <!-- Action buttons -->
      <div v-if="hasActions" class="mb-4 flex gap-3 items-center">
        <Button
          v-if="canRepost"
          variant="outline"
          @click="showRepostConfirm = true"
        >
          <RefreshCw class="mr-1 h-3.5 w-3.5" /> Re-post Jurnal
        </Button>
        <Button
          v-if="canDelete"
          variant="outline"
          class="text-red-600 hover:bg-red-50 border-red-200"
          @click="showDeleteConfirm = true"
        >
          <Trash2 class="mr-1 h-3.5 w-3.5" /> Hapus Transaksi
        </Button>
        <span v-if="!canRepost && detail.isposted === 'T'" class="text-xs text-muted">
          Jurnal sudah ada
        </span>
      </div>

      <!-- Journal items table -->
      <div class="overflow-x-auto rounded-lg border border-border">
        <div class="px-3 py-2 text-xs font-semibold text-muted bg-surface border-b border-border">
          Jurnal Items {{ detail.journal_items.length === 0 ? '— belum ada jurnal' : '' }}
        </div>
        <table v-if="detail.journal_items.length" class="w-full text-xs">
          <thead class="bg-surface">
            <tr>
              <th class="px-2 py-1.5 text-left">No</th>
              <th class="px-2 py-1.5 text-left">Kode Akun</th>
              <th class="px-2 py-1.5 text-left min-w-[160px]">Nama Akun</th>
              <th class="px-2 py-1.5 text-right">Debit</th>
              <th class="px-2 py-1.5 text-right">Kredit</th>
              <th class="px-2 py-1.5 text-left">Keterangan</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="ji in detail.journal_items"
              :key="ji.journalitem_no"
              class="border-t border-border hover:bg-background"
            >
              <td class="px-2 py-1">{{ ji.journalitem_no }}</td>
              <td class="px-2 py-1 font-mono">{{ ji.fl_account ?? '—' }}</td>
              <td class="px-2 py-1">{{ ji.account_name ?? ji.fl_account ?? '—' }}</td>
              <td class="px-2 py-1 text-right">{{ ji.amount_debit ? fmt(ji.amount_debit) : '' }}</td>
              <td class="px-2 py-1 text-right">{{ ji.amount_credit ? fmt(ji.amount_credit) : '' }}</td>
              <td class="px-2 py-1 max-w-[180px] truncate" :title="ji.description ?? ''">
                {{ ji.description ?? '' }}
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="p-4 text-sm text-muted text-center">Belum ada jurnal untuk transaksi ini.</div>
      </div>
    </template>

    <!-- Repost confirm dialog -->
    <div v-if="showRepostConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-2 font-semibold">Konfirmasi Re-post Jurnal</h2>
        <p class="mb-4 text-sm text-muted">Jurnal baru akan dibuat untuk transaksi ini. Lanjutkan?</p>
        <Alert v-if="repostError" variant="error" :message="repostError" class="mb-3" />
        <div class="flex justify-end gap-3">
          <Button variant="outline" :disabled="reposting" @click="showRepostConfirm = false">Batal</Button>
          <Button :disabled="reposting" @click="doRepost">
            {{ reposting ? 'Memproses...' : 'Ya, Re-post' }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Delete confirm dialog -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-2 font-semibold">Konfirmasi Hapus Transaksi</h2>
        <p class="mb-4 text-sm text-muted">
          Transaksi akan dihapus. Jika sudah terotorisasi, akan masuk antrean approval supervisor.
        </p>
        <Alert v-if="deleteError" variant="error" :message="deleteError" class="mb-3" />
        <div class="flex justify-end gap-3">
          <Button variant="outline" :disabled="deleting" @click="showDeleteConfirm = false">Batal</Button>
          <Button
            class="bg-red-600 hover:bg-red-700 text-white"
            :disabled="deleting"
            @click="doDelete"
          >
            {{ deleting ? 'Memproses...' : 'Ya, Hapus' }}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
```

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/HistoriTransaksiDetailPage.vue
git commit -m "[HISTORI-TRANSAKSI] feat(web-vue): halaman detail transaksi + jurnal + aksi

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: Sidebar + router/index.ts wiring

**Files:**
- Modify: `apps_zakat/web-vue/src/components/AppSidebar.vue`
- Modify: `apps_zakat/web-vue/src/router/index.ts`

- [ ] **Edit `AppSidebar.vue`** — tambah `Clock` ke lucide import dan tambah section Transaksi.

Di baris import lucide, tambah `Clock`:
```typescript
import {
  BarChart3,
  Banknote,
  BookOpen,
  ChevronDown,
  ClipboardCheck,
  Clock,       // ← tambah ini
  FileText,
  HandCoins,
  Landmark,
  LayoutDashboard,
  PieChart,
  Settings,
  TrendingUp,
  Upload,
  Users,
  Wallet,
} from 'lucide-vue-next'
```

Di dalam `children` dari item Keuangan, tambah setelah `{ label: 'Bank', ... }` dan **sebelum** `{ section: 'Upload' }`:

```typescript
          { section: 'Transaksi' },
          { label: 'Histori Transaksi', to: '/keuangan/transaksi/histori', icon: Clock },
```

Hasil akhir urutan children Keuangan:
```
COA → Kas → Bank → [section: Transaksi] → Histori Transaksi → [section: Upload] → Upload Penghimpunan → Otorisasi Upload
```

- [ ] **Edit `router/index.ts`** — tambah 2 route sebelum `{ path: '/:catchAll(.*)', redirect: '/' }`:

```typescript
    {
      path: '/keuangan/transaksi/histori',
      name: 'keuangan-transaksi-histori',
      component: () => import('@/pages/keuangan/HistoriTransaksiPage.vue'),
      meta: { title: 'Histori Transaksi', menu_key: 'keuangan.transaksi.histori' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/histori/:id',
      name: 'keuangan-transaksi-histori-detail',
      component: () => import('@/pages/keuangan/HistoriTransaksiDetailPage.vue'),
      meta: { title: 'Detail Transaksi', menu_key: 'keuangan.transaksi.histori' as MenuKey },
    },
```

- [ ] **Commit:**

```bash
git add apps_zakat/web-vue/src/components/AppSidebar.vue \
        apps_zakat/web-vue/src/router/index.ts
git commit -m "[HISTORI-TRANSAKSI] feat(web-vue): sidebar + router wiring histori transaksi

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: E2E test script + smoke test

**Files:**
- Create: `testing/e2e-histori-transaksi.sh`

- [ ] **Buat script:**

```bash
#!/usr/bin/env bash
# testing/e2e-histori-transaksi.sh
# Smoke test untuk fitur Histori Transaksi.
# Jalankan terhadap api-python langsung (port 8001).
set -e
API="http://localhost:8001"
TODAY=$(date +%Y-%m-%d)
FIRST=$(date +%Y-%m-01)

echo "=== E2E: Histori Transaksi ==="

echo ""
echo "1. Search (SPV mode, semua transaksi hari ini):"
curl -s "$API/api/transaksi-histori/search?begin=${FIRST}&end=${TODAY}&is_spv=true&user_id=TEST&limit=5" \
  | python3 -m json.tool | head -30

echo ""
echo "2. Export template (HEAD check):"
curl -sI "$API/api/transaksi-histori/search/export.xlsx?begin=${FIRST}&end=${TODAY}&is_spv=true&user_id=TEST" \
  | grep -i "content-type"

echo ""
echo "3. Detail transaksi pertama (jika ada):"
FIRST_ID=$(curl -s "$API/api/transaksi-histori/search?begin=${FIRST}&end=${TODAY}&is_spv=true&user_id=TEST&limit=1" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0]['transactionid'] if d.get('data') else 'NONE')" 2>/dev/null)
if [ "$FIRST_ID" != "NONE" ] && [ -n "$FIRST_ID" ]; then
  echo "  Transaction ID: $FIRST_ID"
  curl -s "$API/api/transaksi-histori/transactions/$FIRST_ID" | python3 -m json.tool | head -30
else
  echo "  Tidak ada transaksi — skip detail test"
fi

echo ""
echo "=== Done ==="
echo "Untuk full BFF flow (dengan session + menu gating):"
echo "  Login ke http://localhost:5173 sebagai KEU/SPVKEU user"
echo "  Buka menu Keuangan > Histori Transaksi di sidebar"
```

- [ ] **Buat executable dan run:**

```bash
chmod +x testing/e2e-histori-transaksi.sh
bash testing/e2e-histori-transaksi.sh 2>&1 | head -40 || true
```

Expected: fixture jalan, curl mungkin fail (service down), tapi tidak ada syntax error.

- [ ] **Run semua unit tests:**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -m pytest tests/test_histori_transaksi.py -v
```

Expected: 10 tests PASS.

- [ ] **Commit:**

```bash
git add testing/e2e-histori-transaksi.sh
git commit -m "[HISTORI-TRANSAKSI] test(e2e): script e2e histori transaksi

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Known Risks

| Risk | Mitigation |
|---|---|
| `transaction.account` tidak punya `account_name` (kolom mungkin berbeda) | Inspect `\d transaction.account` di DB lokal; ganti ke kolom yang benar |
| Re-post jurnal: `transactionitemid` di `accounttransactionitem` tidak ada untuk transaksi legacy | Query fetchrow sudah handle null — skip item bila tidak ada ATI |
| Delete reverse balance: `donortotalfund` menjadi negatif | Acceptable — mirror perilaku legacy; saldo akuntansi akan di-rekonsiliasi via laporan |
| BFF `_inject` mengambil `roles` dari session — pastikan identity service populate `roles` di session saat login | Cek `apps_zakat/bff-api/app/routers/auth.py` — session["roles"] harus di-set saat `AfterSuccessfulLogin` |

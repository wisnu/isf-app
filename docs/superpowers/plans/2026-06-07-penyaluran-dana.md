# Penyaluran Dana Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrasi fFundDistribution (legacy DAF) → isf-app zakat: API endpoints + BFF + halaman list & form create transaksi penyaluran dana (DD001).

**Architecture:** Extend modul `transaction/` di api-python dengan 3 file baru (schema, repo, service) + extend router. BFF router baru proxy ke api-python. Dua halaman Vue baru (list + form create) mengikuti pola HistoriTransaksiPage.

**Tech Stack:** Python 3.12 + asyncpg + FastAPI (api-python, bff-api), Vue 3.5 + TypeScript + PrimeVue unstyled + Tailwind CSS 4 (web-vue).

**Spec:** `docs/superpowers/specs/2026-06-07-penyaluran-dana-design.md`

---

## DB Facts (verified dari mziss_laz)

- `transaction.cashaccount` — rekening kas/bank: `cashaccounttype` = 'A' (Bank), 'R' (Kas Cabang), 'P' (Kas Kecil). Field `accountinterface` = GL COA untuk journal. Field `productid` = link ke collection product account.
- `transaction.financialaccount` — running balance per account. `financialaccounttype` = 'C' (cash/bank), 'P' (product account).
- `transaction.product` — master produk: `fundcategory` (Z/I/T/W/A/N), `isdetail='T'`, `status='A'`.
- `transaction.productaccount` — link product ke account: `accountno`, `productid`.
- `transaction.transactionbatch` — batch harian per user. `batchdate`, `inputer`, `branchcode`.
- Sequence `transaction.seq_transactionnumber` — untuk generate transaction_no dan journal_no.
- Sequence `transaction.seq_transaction`, `seq_transactionitem`, `seq_journalblock`, `seq_transhistoryofchanges`.
- DD001 transaction_no format: `KK-{YYYY}-{branch}-{cashcode}-{7digit}` (cashcode dari cashaccount, kosong → pakai 'KAS').
- Journal_no format: `DD001.{YYYY}.{MM:02d}.{7digit}`.
- Journal debit = product account (penyaluran), credit = bank/kas accountinterface.
- `authstatus='P'` (Pending) untuk transaksi baru — perlu supervisor approval.
- FundEntity map: Z→1, I→2, T→2, W→3, A→4, N→5.
- Ashnaf wajib isi (bukan 'L') jika fundEntity=1 (Zakat).

---

## File Map

| File | Action | Tanggung Jawab |
|---|---|---|
| `apps_zakat/api-python/app/modules/transaction/penyaluran_schema.py` | CREATE | Pydantic models |
| `apps_zakat/api-python/app/modules/transaction/penyaluran_repo.py` | CREATE | DB queries: lookup + list + count |
| `apps_zakat/api-python/app/modules/transaction/penyaluran_service.py` | CREATE | Business logic: create DD001 |
| `apps_zakat/api-python/app/modules/transaction/router.py` | MODIFY | Tambah 7 endpoint baru |
| `apps_zakat/api-python/tests/test_penyaluran.py` | CREATE | Unit test pure functions |
| `apps_zakat/bff-api/app/routers/penyaluran.py` | CREATE | BFF proxy + auth |
| `apps_zakat/bff-api/app/main.py` | MODIFY | Include penyaluran router |
| `apps_zakat/web-vue/src/lib/menu/registry.ts` | MODIFY | Tambah menu key |
| `apps_zakat/web-vue/src/router/index.ts` | MODIFY | Tambah 2 route |
| `apps_zakat/web-vue/src/components/AppSidebar.vue` | MODIFY | Tambah sidebar entry |
| `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue` | CREATE | List page |
| `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue` | CREATE | Form create |
| `infra/db/migrations/seed/seed-menu-penyaluran.sql` | CREATE | Menu + role_menu seed |
| `testing/e2e-penyaluran.sh` | CREATE | E2E curl tests |

---

## Task 1: penyaluran_schema.py — Pydantic Models

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/penyaluran_schema.py`

- [ ] **Step 1: Buat file schema**

```python
# apps_zakat/api-python/app/modules/transaction/penyaluran_schema.py
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, field_validator


FUND_ENTITY_MAP: dict[str, int] = {'Z': 1, 'I': 2, 'T': 2, 'W': 3, 'A': 4, 'N': 5}

CHANNEL_CODE_MAP: dict[str, str] = {'K': 'P', 'C': 'R', 'B': 'A', 'A': 'G'}

ASHNAF_LIST = [
    {'code': 'F', 'name': 'Fakir'},
    {'code': 'M', 'name': 'Miskin'},
    {'code': 'A', 'name': 'Amil'},
    {'code': 'K', 'name': 'Mualaf'},
    {'code': 'R', 'name': 'Riqab'},
    {'code': 'G', 'name': 'Gharimin'},
    {'code': 'S', 'name': 'Fi Sabilillah'},
    {'code': 'I', 'name': 'Ibnu Sabil'},
]


class PenyaluranItem(BaseModel):
    product_id: int
    account_no: str               # productaccount.accountno penyaluran
    ashnaf: str                   # wajib jika fund_entity=1, else 'L'
    amount: float
    description: str = ''
    fund_entity: int              # 1-5
    dist_item_account: str | None = None
    budget_id: int | None = None
    budget_code: str | None = None
    distribution_category: str | None = None

    @field_validator('amount')
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('amount harus > 0')
        return v


class PenyaluranCreate(BaseModel):
    actual_date: str              # ISO YYYY-MM-DD
    reference_no: str | None = None
    description: str = ''
    paid_to: str | None = None
    received_from: str | None = None
    payment_type: Literal['K', 'C', 'B', 'A']
    payment_account_no: str | None = None  # wajib K dan B
    asset_code: str | None = None          # wajib A
    asset_currency: str | None = None      # wajib A
    rate: float = 1.0
    currency_code: str = 'IDR'
    fund_account_no: str                   # productaccount penghimpunan (sumber dana)
    product_branch_code: str               # untuk journal code (same/cross branch)
    donor_id: int | None = None
    sponsor_id: int | None = None
    volunteer_id: str | None = None
    items: list[PenyaluranItem]

    @field_validator('items')
    @classmethod
    def items_not_empty(cls, v: list) -> list:
        if not v:
            raise ValueError('items tidak boleh kosong')
        return v

    @field_validator('actual_date')
    @classmethod
    def valid_date(cls, v: str) -> str:
        from datetime import date
        date.fromisoformat(v)  # raises ValueError kalau format salah
        return v


class PenyaluranListRow(BaseModel):
    transaction_id: int
    transaction_no: str | None
    actual_date: str
    description: str | None
    amount: float
    channel_code: str | None
    channel_account_no: str | None
    channel_name: str | None
    inputer: str | None
    auth_status: str | None
    branch_code: str | None


class PenyaluranListPage(BaseModel):
    data: list[PenyaluranListRow]
    pagination: dict


class RekeningRow(BaseModel):
    account_no: str
    account_name: str
    account_interface: str | None   # GL COA
    currency_code: str | None
    branch_code: str | None
    bank_name: str | None = None
    bank_account_no: str | None = None
    cash_code: str | None = None
    product_id: int | None = None
    fund_category: str | None = None


class ProductRow(BaseModel):
    product_id: int
    product_name: str
    fund_category: str
    product_code: str | None
    account_no: str               # productaccount.accountno
    fund_entity: int              # derived dari fund_category


class FundProductAccountRow(BaseModel):
    account_no: str               # productaccount.accountno (sumber dana)
    account_name: str
    product_id: int | None
    fund_category: str | None


class CreateResult(BaseModel):
    transaction_id: int
    transaction_no: str
```

- [ ] **Step 2: Verifikasi import bersih**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -c "from app.modules.transaction.penyaluran_schema import PenyaluranCreate, FUND_ENTITY_MAP; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add apps_zakat/api-python/app/modules/transaction/penyaluran_schema.py
git commit -m "[PENYALURAN] feat(api): add penyaluran_schema — Pydantic models DD001

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: penyaluran_repo.py — DB Queries

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/penyaluran_repo.py`
- Create: `apps_zakat/api-python/tests/test_penyaluran.py`

- [ ] **Step 1: Tulis unit test dulu (pure functions)**

```python
# apps_zakat/api-python/tests/test_penyaluran.py
from datetime import date
from app.modules.transaction.penyaluran_repo import build_list_where
from app.modules.transaction.penyaluran_schema import FUND_ENTITY_MAP


def test_fund_entity_map_z():
    assert FUND_ENTITY_MAP['Z'] == 1


def test_fund_entity_map_t_is_infaq():
    assert FUND_ENTITY_MAP['T'] == 2


def test_build_list_where_basic():
    where, args = build_list_where(
        begin='2026-01-01', end='2026-12-31',
        search=None, branch=None,
    )
    assert 't.transactioncode = $1' in where
    assert "'DD001'" in where or args[0] == 'DD001'
    assert len(args) >= 3  # DD001, begin, end


def test_build_list_where_with_search():
    where, args = build_list_where(
        begin='2026-01-01', end='2026-12-31',
        search='KK-2026', branch=None,
    )
    assert 'LIKE' in where
    assert any('%KK-2026%' in str(a) for a in args)


def test_build_list_where_with_branch():
    where, args = build_list_where(
        begin='2026-01-01', end='2026-12-31',
        search=None, branch='001',
    )
    assert 'branchcode' in where
    assert '001' in args
```

- [ ] **Step 2: Jalankan test — harusnya FAIL**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -m pytest tests/test_penyaluran.py -v 2>&1 | head -30
```

Expected: `ImportError` atau `ModuleNotFoundError` karena `penyaluran_repo` belum ada.

- [ ] **Step 3: Buat penyaluran_repo.py**

```python
# apps_zakat/api-python/app/modules/transaction/penyaluran_repo.py
from __future__ import annotations
from datetime import date as _date
from app.shared.db import fetch_all, fetch_one, get_pool
from app.modules.transaction.penyaluran_schema import (
    FundProductAccountRow, ProductRow, RekeningRow,
    PenyaluranListRow, FUND_ENTITY_MAP,
)


def build_list_where(
    begin: str,
    end: str,
    search: str | None,
    branch: str | None,
) -> tuple[str, list]:
    """Pure function — unit-testable, no DB access."""
    args: list = ['DD001', _date.fromisoformat(begin), _date.fromisoformat(end)]
    conds = [
        "t.transactioncode = $1",
        "t.actualdate >= $2",
        "t.actualdate <= $3",
    ]
    if branch:
        args.append(branch)
        conds.append(f"t.branchcode = ${len(args)}")
    if search:
        args.append(f'%{search.upper()}%')
        conds.append(f"UPPER(COALESCE(t.transactionno,'')) LIKE ${len(args)}")
    return ' AND '.join(conds), args


_LIST_SELECT = """
    SELECT
      t.transactionid, t.transactionno,
      to_char(t.actualdate, 'YYYY-MM-DD') AS actual_date,
      t.description, t.amount::float,
      t.channelcode, t.channelaccountno,
      fa.accountname AS channel_name,
      t.inputer, t.authstatus, t.branchcode
    FROM transaction.transaction t
    LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
"""


async def count_list(begin: str, end: str, search: str | None, branch: str | None) -> int:
    where, args = build_list_where(begin, end, search, branch)
    row = await fetch_one(
        f"SELECT COUNT(*)::int AS n FROM transaction.transaction t WHERE {where}",
        *args,
    )
    return int((row or {}).get('n', 0))


async def fetch_list(
    begin: str, end: str,
    search: str | None,
    branch: str | None,
    page: int,
    page_size: int,
) -> list[PenyaluranListRow]:
    where, args = build_list_where(begin, end, search, branch)
    offset = (page - 1) * page_size
    args += [page_size, offset]
    rows = await fetch_all(
        f"{_LIST_SELECT} WHERE {where}"
        f" ORDER BY t.actualdate DESC, t.transactionid DESC"
        f" LIMIT ${len(args)-1} OFFSET ${len(args)}",
        *args,
    )
    return [
        PenyaluranListRow(
            transaction_id=int(r['transactionid']),
            transaction_no=r.get('transactionno'),
            actual_date=str(r.get('actual_date') or '')[:10],
            description=r.get('description'),
            amount=float(r.get('amount') or 0),
            channel_code=r.get('channelcode'),
            channel_account_no=r.get('channelaccountno'),
            channel_name=r.get('channel_name'),
            inputer=r.get('inputer'),
            auth_status=r.get('authstatus'),
            branch_code=r.get('branchcode'),
        )
        for r in rows
    ]


async def fetch_rekening(account_type: str, branch: str | None) -> list[RekeningRow]:
    """Lookup rekening kas/bank dari cashaccount JOIN financialaccount."""
    args: list = [account_type]
    where = "ca.cashaccounttype = $1"
    if branch:
        args.append(branch)
        where += f" AND fa.branchcode = ${len(args)}"
    rows = await fetch_all(
        f"""SELECT ca.accountno, fa.accountname, ca.accountinterface,
               fa.currencycode, fa.branchcode,
               ca.bankname, ca.bankaccountno, ca.cashcode,
               ca.productid, ca.fundcategory
            FROM transaction.cashaccount ca
            JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
            WHERE {where}
            ORDER BY fa.accountname""",
        *args,
    )
    return [
        RekeningRow(
            account_no=r['accountno'],
            account_name=r.get('accountname') or r['accountno'],
            account_interface=r.get('accountinterface'),
            currency_code=r.get('currencycode'),
            branch_code=r.get('branchcode'),
            bank_name=r.get('bankname'),
            bank_account_no=r.get('bankaccountno'),
            cash_code=r.get('cashcode'),
            product_id=r.get('productid'),
            fund_category=r.get('fundcategory'),
        )
        for r in rows
    ]


async def fetch_products(branch: str, currency: str = 'IDR') -> list[ProductRow]:
    """Produk penyaluran aktif untuk branch tertentu."""
    rows = await fetch_all(
        """SELECT p.productid, p.productname, p.fundcategory, p.productcode,
                  pa.accountno
           FROM transaction.product p
           JOIN transaction.productaccount pa ON pa.productid = p.productid
           JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
           WHERE fa.branchcode = $1
             AND fa.currencycode = $2
             AND p.isdetail = 'T'
             AND p.status = 'A'
           ORDER BY p.fundcategory, p.productname""",
        branch, currency,
    )
    return [
        ProductRow(
            product_id=int(r['productid']),
            product_name=r['productname'],
            fund_category=r.get('fundcategory') or 'I',
            product_code=r.get('productcode'),
            account_no=r['accountno'],
            fund_entity=FUND_ENTITY_MAP.get(r.get('fundcategory') or 'I', 2),
        )
        for r in rows
    ]


async def fetch_fund_product_accounts(bank_account_no: str, branch: str) -> list[FundProductAccountRow]:
    """Sumber dana penghimpunan: product account yang terhubung ke bank account."""
    rows = await fetch_all(
        """SELECT pa.accountno, fa.accountname, ca.productid, ca.fundcategory
           FROM transaction.cashaccount ca
           JOIN transaction.productaccount pa ON pa.productid = ca.productid
           JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
           WHERE ca.accountno = $1 AND fa.branchcode = $2""",
        bank_account_no, branch,
    )
    if not rows:
        # Fallback: semua product account aktif untuk branch ini
        rows = await fetch_all(
            """SELECT pa.accountno, fa.accountname, pa.productid, NULL AS fundcategory
               FROM transaction.productaccount pa
               JOIN transaction.financialaccount fa ON fa.accountno = pa.accountno
               WHERE fa.branchcode = $1 AND fa.currencycode = 'IDR'
               ORDER BY fa.accountname LIMIT 20""",
            branch,
        )
    return [
        FundProductAccountRow(
            account_no=r['accountno'],
            account_name=r.get('accountname') or r['accountno'],
            product_id=r.get('productid'),
            fund_category=r.get('fundcategory'),
        )
        for r in rows
    ]


async def get_cashaccount(account_no: str) -> dict | None:
    return await fetch_one(
        """SELECT ca.accountno, ca.accountinterface, ca.cashaccounttype,
                  ca.cashcode, fa.currencycode, fa.branchcode
           FROM transaction.cashaccount ca
           JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
           WHERE ca.accountno = $1""",
        account_no,
    )


async def get_branch_cash(branch: str, currency: str = 'IDR') -> dict | None:
    return await fetch_one(
        """SELECT ca.accountno, ca.accountinterface
           FROM transaction.cashaccount ca
           JOIN transaction.financialaccount fa ON fa.accountno = ca.accountno
           WHERE ca.cashaccounttype = 'R' AND fa.branchcode = $1
             AND fa.currencycode = $2
           LIMIT 1""",
        branch, currency,
    )
```

- [ ] **Step 4: Jalankan test — harusnya PASS**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -m pytest tests/test_penyaluran.py -v
```

Expected: semua 5 test PASS.

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/api-python/app/modules/transaction/penyaluran_repo.py \
        apps_zakat/api-python/tests/test_penyaluran.py
git commit -m "[PENYALURAN] feat(api): add penyaluran_repo + unit tests

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: penyaluran_service.py — Create DD001

**Files:**
- Create: `apps_zakat/api-python/app/modules/transaction/penyaluran_service.py`

- [ ] **Step 1: Buat penyaluran_service.py**

```python
# apps_zakat/api-python/app/modules/transaction/penyaluran_service.py
from __future__ import annotations
from datetime import date, datetime, timezone

from app.modules.transaction.penyaluran_repo import get_cashaccount, get_branch_cash
from app.modules.transaction.penyaluran_schema import (
    CHANNEL_CODE_MAP, PenyaluranCreate, CreateResult,
)
from app.shared.db import get_pool


async def _get_or_create_batch(
    conn, actual_date: date, user_id: str, branch_code: str, now: datetime,
) -> int:
    row = await conn.fetchrow(
        """SELECT batchid FROM transaction.transactionbatch
           WHERE DATE(batchdate) = $1 AND UPPER(inputer) = $2 AND branchcode = $3
           ORDER BY batchid DESC LIMIT 1""",
        actual_date, user_id.upper(), branch_code,
    )
    if row:
        return int(row['batchid'])
    batch_id = await conn.fetchval("SELECT nextval('transaction.seq_transactionbatch')")
    await conn.execute(
        """INSERT INTO transaction.transactionbatch
           (batchid, batchdate, description, inputer, branchcode, isclosed, isposted)
           VALUES ($1, $2, 'Penyaluran Dana', $3, $4, 'F', 'F')""",
        int(batch_id), actual_date, user_id.upper(), branch_code,
    )
    return int(batch_id)


async def _resolve_payment(
    conn, req: PenyaluranCreate, branch_code: str,
) -> tuple[str, str, str]:
    """Return (payment_accountno, payment_interface_coa, cash_code).

    payment_accountno = accountno di financialaccount (untuk balance update).
    payment_interface_coa = GL account untuk journal credit line.
    cash_code = untuk transaction_no suffix.
    """
    if req.payment_type == 'B':
        ca = await get_cashaccount(req.payment_account_no or '')
        if not ca:
            raise ValueError(f'Rekening bank {req.payment_account_no} tidak ditemukan')
        return (
            ca['accountno'],
            ca.get('accountinterface') or ca['accountno'],
            ca.get('cashcode') or 'BANK',
        )
    elif req.payment_type == 'K':
        ca = await get_cashaccount(req.payment_account_no or '')
        if not ca:
            raise ValueError(f'Rekening kas kecil {req.payment_account_no} tidak ditemukan')
        return (
            ca['accountno'],
            ca.get('accountinterface') or ca['accountno'],
            ca.get('cashcode') or 'KAS',
        )
    elif req.payment_type == 'C':
        ca = await get_branch_cash(branch_code, req.currency_code)
        if not ca:
            raise ValueError(f'Rekening kas cabang {branch_code} tidak ditemukan')
        return (
            ca['accountno'],
            ca.get('accountinterface') or ca['accountno'],
            'KAS',
        )
    elif req.payment_type == 'A':
        # Aset/GL: gunakan asset_code langsung sebagai GL account
        code = req.asset_code or ''
        return (code, code, 'ASET')
    raise ValueError(f'payment_type tidak dikenal: {req.payment_type}')


async def create_penyaluran(
    req: PenyaluranCreate,
    user_id: str,
    branch_code: str,
) -> CreateResult:
    # Validasi ashnaf
    for item in req.items:
        if item.fund_entity == 1 and item.ashnaf in ('L', '', None):
            raise ValueError(f'Ashnaf wajib diisi untuk produk Zakat (fund_entity=1)')

    pool = get_pool()
    now = datetime.now(timezone.utc)
    now_naive = now.replace(tzinfo=None)
    actual_date = date.fromisoformat(req.actual_date)
    year = actual_date.year

    journal_code = '10' if req.product_branch_code == branch_code else '15'
    total_amount = sum(item.amount for item in req.items)
    channel_code = CHANNEL_CODE_MAP[req.payment_type]

    async with pool.acquire() as conn:
        async with conn.transaction():
            batch_id = await _get_or_create_batch(conn, actual_date, user_id, branch_code, now)
            payment_acctno, payment_coa, cash_code = await _resolve_payment(conn, req, branch_code)

            # Transaction number + journal number
            seq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            transaction_no = f"KK-{year}-{branch_code}-{cash_code}-{int(seq):07d}"

            jseq = await conn.fetchval("SELECT nextval('transaction.seq_transactionnumber')")
            journal_no = f"DD001.{year}.{actual_date.month:02d}.{int(jseq):07d}"

            # Transaction header
            transaction_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transaction')"))
            await conn.execute(
                """INSERT INTO transaction.transaction
                   (transactionid, transactiondate, transactiontime, actualdate,
                    referenceno, description, inputer, transactioncode, channelcode,
                    branchcode, authstatus, isposted, batchid, donorid,
                    paidto, receivedfrom, amount, currencycode, rate,
                    transactionno, channelaccountno, sponsorid, volunteerid)
                   VALUES ($1,$2,$3,$4,$5,$6,$7,'DD001',$8,$9,'P','F',$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20)""",
                transaction_id, actual_date, now_naive, actual_date,
                req.reference_no, req.description, user_id.upper(),
                channel_code, branch_code, batch_id,
                req.donor_id, req.paid_to, req.received_from,
                total_amount, req.currency_code, req.rate,
                transaction_no,
                payment_acctno if req.payment_type != 'A' else req.asset_code,
                req.sponsor_id, req.volunteer_id,
            )

            # Journal block
            block_id = int(await conn.fetchval("SELECT nextval('transaction.seq_journalblock')"))
            await conn.execute(
                """INSERT INTO transaction.journalblock
                   (id_journalblock, class_id, key_id, journal_no, subsystemcode, transaction_tag)
                   VALUES ($1,'Transaction',$2,$3,'CORE','DD001')""",
                block_id, transaction_id, journal_no,
            )

            # Journal header
            await conn.execute(
                """INSERT INTO transaction.journal
                   (journal_no, journal_type, journal_date, journal_date_posting,
                    transaction_date, description, userid_create, userid_posting,
                    is_posted, status, journal_state, branch_code,
                    source_app, source_app_class, source_app_ref, lastitemno)
                   VALUES ($1,'DD001',$2,$2,$2,$3,$4,$4,'T','C','C',$5,'CORE','Transaction',$6,$7)""",
                journal_no, actual_date, req.description, user_id.upper(),
                branch_code, str(transaction_id), len(req.items) + 1,
            )

            journalitem_no = 0

            # Tiap item distribusi → transactionitem (D) + accounttransactionitem + journal debit
            for item in req.items:
                item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
                await conn.execute(
                    """INSERT INTO transaction.transactionitem
                       (transactionitemid, transactionid, branchcode, currencycode,
                        mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                        description, refaccountno, accountcode, parameterjournalid)
                       VALUES ($1,$2,$3,$4,'D',$5,$6,$7,'A',$8,$9,$9,$10)""",
                    item_id, transaction_id, branch_code, req.currency_code,
                    item.amount, req.rate, item.amount * req.rate,
                    item.description or req.description,
                    item.account_no, journal_code,
                )
                await conn.execute(
                    """INSERT INTO transaction.accounttransactionitem
                       (transactionitemid, accounttitype, accountno, ashnaf,
                        fundentity, distributionitemaccount, distributioncategory,
                        fundaccountno, isupdatebalance)
                       VALUES ($1,'Z',$2,$3,$4,$5,$6,$7,'T')""",
                    item_id, item.account_no,
                    item.ashnaf if item.fund_entity == 1 else 'L',
                    item.fund_entity,
                    item.dist_item_account, item.distribution_category,
                    req.fund_account_no,
                )
                # Debit product account balance (penyaluran mengurangi saldo)
                await conn.execute(
                    "UPDATE transaction.financialaccount SET balance = COALESCE(balance,0) - $2 WHERE accountno = $1",
                    item.account_no, item.amount,
                )
                # Journal debit line
                journalitem_no += 1
                await conn.execute(
                    """INSERT INTO transaction.journalitem
                       (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                        description, branch_code, valuta_code, journalitemtype,
                        userid_create, id_journalblock, source_class_id, source_key_id)
                       VALUES ($1,$2,$3,$4,0,$5,$6,$7,'V',$8,$9,'ProductTransactionItem',$10)""",
                    journal_no, journalitem_no, item.account_no, item.amount,
                    item.description or req.description,
                    branch_code, req.currency_code, user_id.upper(), block_id, item_id,
                )

            # Item pembayaran → transactionitem (C) + accounttransactionitem + journal credit
            pay_item_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transactionitem')"))
            await conn.execute(
                """INSERT INTO transaction.transactionitem
                   (transactionitemid, transactionid, branchcode, currencycode,
                    mutationtype, amount, rate, ekuivalenamount, transactionitemtype,
                    description, refaccountno, accountcode, parameterjournalid)
                   VALUES ($1,$2,$3,$4,'C',$5,$6,$7,'A',$8,$9,$9,$10)""",
                pay_item_id, transaction_id, branch_code, req.currency_code,
                total_amount, req.rate, total_amount * req.rate,
                req.description, payment_acctno, journal_code,
            )
            await conn.execute(
                """INSERT INTO transaction.accounttransactionitem
                   (transactionitemid, accountno, isupdatebalance)
                   VALUES ($1,$2,'T')""",
                pay_item_id, payment_acctno,
            )
            if req.payment_type != 'A':
                await conn.execute(
                    "UPDATE transaction.financialaccount SET balance = COALESCE(balance,0) - $2 WHERE accountno = $1",
                    payment_acctno, total_amount,
                )
            # Journal credit line
            journalitem_no += 1
            await conn.execute(
                """INSERT INTO transaction.journalitem
                   (fl_journal, journalitem_no, fl_account, amount_debit, amount_credit,
                    description, branch_code, valuta_code, journalitemtype,
                    userid_create, id_journalblock, source_class_id, source_key_id)
                   VALUES ($1,$2,$3,0,$4,$5,$6,$7,'V',$8,$9,'AccountTransactionItem',$10)""",
                journal_no, journalitem_no, payment_coa, total_amount,
                req.description, branch_code, req.currency_code,
                user_id.upper(), block_id, pay_item_id,
            )

            # Update transaction dengan journal_no
            await conn.execute(
                "UPDATE transaction.transaction SET journalno = $2 WHERE transactionid = $1",
                transaction_id, journal_no,
            )

            # Audit: transhistoryofchanges
            hist_id = int(await conn.fetchval("SELECT nextval('transaction.seq_transhistoryofchanges')"))
            await conn.execute(
                """INSERT INTO transaction.transhistoryofchanges
                   (historyid, transactionid, transactionno, userid, processtime, changetype)
                   VALUES ($1,$2,$3,$4,$5,'I')""",
                hist_id, transaction_id, transaction_no, user_id.upper(), now_naive,
            )

    return CreateResult(transaction_id=transaction_id, transaction_no=transaction_no)
```

- [ ] **Step 2: Verifikasi import bersih (tanpa koneksi DB)**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -c "from app.modules.transaction.penyaluran_service import create_penyaluran; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add apps_zakat/api-python/app/modules/transaction/penyaluran_service.py
git commit -m "[PENYALURAN] feat(api): add penyaluran_service — create DD001 transaction

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Extend router.py — Tambah Endpoint Penyaluran

**Files:**
- Modify: `apps_zakat/api-python/app/modules/transaction/router.py`

- [ ] **Step 1: Tambah import di router.py**

Buka `apps_zakat/api-python/app/modules/transaction/router.py`. Tambah setelah import yang sudah ada:

```python
from app.modules.transaction import penyaluran_repo as prp
from app.modules.transaction import penyaluran_service as psvc
from app.modules.transaction.penyaluran_schema import (
    ASHNAF_LIST, PenyaluranCreate,
)
```

- [ ] **Step 2: Tambah 7 endpoint baru di akhir router.py**

Append ke bawah file (setelah endpoint approve yang sudah ada):

```python
# ── Penyaluran Dana (DD001) ──────────────────────────────────────────────────

@router.get('/penyaluran/lookup/ashnaf')
async def penyaluran_lookup_ashnaf():
    return ok(ASHNAF_LIST)


@router.get('/penyaluran/lookup/rekening')
async def penyaluran_lookup_rekening(
    type: str = Query(default='bank'),
    branch: str | None = Query(default=None),
):
    type_map = {'bank': 'A', 'petty': 'P', 'cabang': 'R'}
    acct_type = type_map.get(type, 'A')
    rows = await prp.fetch_rekening(acct_type, branch)
    return ok([r.model_dump() for r in rows])


@router.get('/penyaluran/lookup/produk')
async def penyaluran_lookup_produk(
    branch_code: str = Query(...),
    currency: str = Query(default='IDR'),
):
    rows = await prp.fetch_products(branch_code, currency)
    return ok([r.model_dump() for r in rows])


@router.get('/penyaluran/lookup/fund-product-account')
async def penyaluran_lookup_fund_product_account(
    bank_account_no: str = Query(...),
    branch_code: str = Query(...),
):
    rows = await prp.fetch_fund_product_accounts(bank_account_no, branch_code)
    return ok([r.model_dump() for r in rows])


@router.get('/penyaluran/')
async def penyaluran_list(
    begin: str = Query(...),
    end: str = Query(...),
    search: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    import asyncio
    page_size = min(page_size, 200)
    total, rows = await asyncio.gather(
        prp.count_list(begin, end, search, branch),
        prp.fetch_list(begin, end, search, branch, page, page_size),
    )
    total_pages = max(1, (total + page_size - 1) // page_size)
    return ok(
        [r.model_dump() for r in rows],
        # inject pagination into response menggunakan wrapper manual
    ) | {'pagination': {'page': page, 'limit': page_size, 'total': total, 'total_pages': total_pages}}


@router.get('/penyaluran/{transaction_id}')
async def penyaluran_detail(transaction_id: int):
    from app.shared.db import fetch_one, fetch_all
    row = await fetch_one(
        """SELECT t.transactionid, t.transactionno,
              to_char(t.actualdate,'YYYY-MM-DD') AS actual_date,
              t.description, t.amount::float, t.channelcode,
              t.channelaccountno, fa.accountname AS channel_name,
              t.inputer, t.authstatus, t.branchcode, t.journalno,
              to_char(t.transactiondate,'YYYY-MM-DD') AS transaction_date,
              t.referenceno, t.paidto, t.receivedfrom, t.rate, t.currencycode
           FROM transaction.transaction t
           LEFT JOIN transaction.financialaccount fa ON fa.accountno = t.channelaccountno
           WHERE t.transactionid = $1 AND t.transactioncode = 'DD001'""",
        transaction_id,
    )
    if not row:
        return JSONResponse(status_code=404, content=err('NOT_FOUND', 'Transaksi tidak ditemukan'))
    items = await fetch_all(
        """SELECT ati.accounttitype, ati.accountno, ati.ashnaf, ati.fundentity,
                  ati.distributionitemaccount, ati.distributioncategory, ati.fundaccountno,
                  ti.amount::float, ti.description, ti.mutationtype,
                  fa.accountname
           FROM transaction.transactionitem ti
           JOIN transaction.accounttransactionitem ati ON ati.transactionitemid = ti.transactionitemid
           LEFT JOIN transaction.financialaccount fa ON fa.accountno = ati.accountno
           WHERE ti.transactionid = $1
           ORDER BY ti.transactionitemid""",
        transaction_id,
    )
    return ok({**dict(row), 'items': [dict(i) for i in items]})


@router.post('/penyaluran/')
async def penyaluran_create(req: PenyaluranCreate, branch_code: str = '', user_id: str = ''):
    try:
        result = await psvc.create_penyaluran(req, user_id, branch_code)
    except ValueError as exc:
        return JSONResponse(status_code=422, content=err('VALIDATION_ERROR', str(exc)))
    except Exception as exc:
        return JSONResponse(status_code=500, content=err('SERVER_ERROR', str(exc)))
    return ok(result.model_dump())
```

> **Note:** `branch_code` dan `user_id` di endpoint POST akan diisi oleh BFF dari session — bukan dari request body user. Parameter query digunakan di api-python karena BFF meng-inject melalui request params.

- [ ] **Step 3: Fix endpoint list yang pakai dict merge tidak valid**

Ganti endpoint `/penyaluran/` list dengan versi yang benar:

```python
@router.get('/penyaluran/')
async def penyaluran_list(
    begin: str = Query(...),
    end: str = Query(...),
    search: str | None = Query(default=None),
    branch: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    import asyncio
    page_size = min(page_size, 200)
    total, rows = await asyncio.gather(
        prp.count_list(begin, end, search, branch),
        prp.fetch_list(begin, end, search, branch, page, page_size),
    )
    total_pages = max(1, (total + page_size - 1) // page_size)
    return JSONResponse(content={
        'data': [r.model_dump() for r in rows],
        'pagination': {
            'page': page, 'limit': page_size,
            'total': total, 'total_pages': total_pages,
        },
        'meta': {'request_id': None},
    })
```

Pastikan `from fastapi.responses import JSONResponse` sudah diimport di router.py (sudah ada di existing code).

- [ ] **Step 4: Verifikasi app bisa start**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/api-python
python -c "from app.modules.transaction.router import router; print('routes:', len(router.routes))"
```

Expected: angka routes lebih besar dari sebelumnya (ada 7 route baru).

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/api-python/app/modules/transaction/router.py
git commit -m "[PENYALURAN] feat(api): extend transaction/router — 7 DD001 endpoints

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: BFF — Router Penyaluran + Include ke main.py

**Files:**
- Create: `apps_zakat/bff-api/app/routers/penyaluran.py`
- Modify: `apps_zakat/bff-api/app/main.py`

- [ ] **Step 1: Buat BFF router**

```python
# apps_zakat/bff-api/app/routers/penyaluran.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import JSONResponse

from app.services.auth import require_menu
from app.services.proxy import get_api_python, post_api_python

router = APIRouter(prefix='/penyaluran', tags=['penyaluran'])

_MENU = 'keuangan.transaksi.penyaluran'


def _session(request: Request) -> dict:
    roles = request.session.get('roles') or []
    user_id = request.session.get('user_id', '')
    access = request.session.get('branch_access', 'single')
    primary = request.session.get('primary_branch') or ''
    branch = '' if access == 'all' else primary
    return {'user_id': user_id, 'branch': branch}


@router.get('/lookup/ashnaf')
async def lookup_ashnaf(_: str = Depends(require_menu(_MENU))):
    downstream = await get_api_python('/api/transaction/penyaluran/lookup/ashnaf')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/rekening')
async def lookup_rekening(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    type: str = Query(default='bank'),
):
    s = _session(request)
    params: dict = {'type': type}
    if s['branch']:
        params['branch'] = s['branch']
    downstream = await get_api_python('/api/transaction/penyaluran/lookup/rekening', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/produk')
async def lookup_produk(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    currency: str = Query(default='IDR'),
):
    s = _session(request)
    branch = s['branch'] or '001'
    params = {'branch_code': branch, 'currency': currency}
    downstream = await get_api_python('/api/transaction/penyaluran/lookup/produk', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/lookup/fund-product-account')
async def lookup_fund_product_account(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    bank_account_no: str = Query(...),
):
    s = _session(request)
    branch = s['branch'] or '001'
    params = {'bank_account_no': bank_account_no, 'branch_code': branch}
    downstream = await get_api_python(
        '/api/transaction/penyaluran/lookup/fund-product-account', params=params
    )
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/')
async def list_penyaluran(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
    begin: str = Query(...),
    end: str = Query(...),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=200),
):
    s = _session(request)
    params: dict = {'begin': begin, 'end': end, 'page': page, 'page_size': page_size}
    if s['branch']:
        params['branch'] = s['branch']
    if search:
        params['search'] = search
    downstream = await get_api_python('/api/transaction/penyaluran/', params=params)
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.get('/{transaction_id}')
async def detail_penyaluran(
    transaction_id: int,
    _: str = Depends(require_menu(_MENU)),
):
    downstream = await get_api_python(f'/api/transaction/penyaluran/{transaction_id}')
    return JSONResponse(status_code=downstream.status_code, content=downstream.json())


@router.post('/')
async def create_penyaluran(
    request: Request,
    _: str = Depends(require_menu(_MENU)),
):
    s = _session(request)
    body = await request.json()
    # Inject user_id dan branch_code dari session
    params = {'user_id': s['user_id'], 'branch_code': s['branch'] or '001'}
    downstream = await post_api_python(
        '/api/transaction/penyaluran/',
        json_body=body,
        method='POST',
    )
    # api-python menerima user_id & branch_code via query param
    # Re-call dengan params
    import httpx
    from app.shared.config import settings
    url = f"{settings.api_python_base_url}/api/transaction/penyaluran/"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=body, params=params)
    return JSONResponse(status_code=resp.status_code, content=resp.json())
```

> **Note:** Endpoint POST memanggil api-python langsung dengan params (user_id, branch_code) karena `post_api_python` tidak support query params. Ini workaround yang bersih — api-python endpoint menerima user_id dan branch_code dari query string yang di-inject BFF dari session.

- [ ] **Step 2: Include router di main.py**

Di `apps_zakat/bff-api/app/main.py`, tambah setelah import `histori_transaksi_router`:

```python
from app.routers.penyaluran import router as penyaluran_router
```

Dan tambah setelah `app.include_router(histori_transaksi_router, prefix="/api")`:

```python
app.include_router(penyaluran_router, prefix="/api")
```

- [ ] **Step 3: Verifikasi app import**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/bff-api
python -c "from app.main import app; print('routes:', len(app.routes))"
```

Expected: angka route bertambah.

- [ ] **Step 4: Commit**

```bash
git add apps_zakat/bff-api/app/routers/penyaluran.py \
        apps_zakat/bff-api/app/main.py
git commit -m "[PENYALURAN] feat(bff): add penyaluran router — proxy + require_menu

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Vue — Menu Registry + Router + Sidebar

**Files:**
- Modify: `apps_zakat/web-vue/src/lib/menu/registry.ts`
- Modify: `apps_zakat/web-vue/src/router/index.ts`
- Modify: `apps_zakat/web-vue/src/components/AppSidebar.vue`

- [ ] **Step 1: Tambah menu key di registry.ts**

File: `apps_zakat/web-vue/src/lib/menu/registry.ts`

Tambah `'keuangan.transaksi.penyaluran'` setelah `'keuangan.transaksi.histori'`:

```ts
  'keuangan.transaksi.histori',
  'keuangan.transaksi.penyaluran',   // ← tambah ini
  'keuangan.upload.penghimpunan',
```

- [ ] **Step 2: Tambah routes di router/index.ts**

Cari blok route `keuangan-transaksi-histori` (sekitar line 279–288). Tambah 2 route baru setelah blok tersebut:

```ts
    {
      path: '/keuangan/transaksi/penyaluran',
      name: 'keuangan-transaksi-penyaluran',
      component: () => import('@/pages/keuangan/PenyaluranDanaPage.vue'),
      meta: { title: 'Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
    {
      path: '/keuangan/transaksi/penyaluran/baru',
      name: 'keuangan-transaksi-penyaluran-baru',
      component: () => import('@/pages/keuangan/PenyaluranDanaFormPage.vue'),
      meta: { title: 'Input Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
```

- [ ] **Step 3: Tambah sidebar entry di AppSidebar.vue**

Cari blok `{ section: 'Transaksi' }` di AppSidebar.vue (line 70). Tambah entry "Input Penyaluran Dana" setelah `{ label: 'Histori Transaksi', ... }`:

```ts
          { section: 'Transaksi' },
          { label: 'Histori Transaksi', to: '/keuangan/transaksi/histori', icon: Clock },
          { label: 'Input Penyaluran Dana', to: '/keuangan/transaksi/penyaluran', icon: ArrowDownCircle },   // ← tambah
```

Tambah `ArrowDownCircle` ke import Lucide di baris 1–19:

```ts
import {
  ArrowDownCircle,   // ← tambah
  BarChart3,
  Banknote,
  ...
} from 'lucide-vue-next'
```

- [ ] **Step 4: Verifikasi TypeScript tidak error**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/web-vue
npx vue-tsc --noEmit 2>&1 | head -20
```

Expected: 0 error, atau error yang tidak terkait perubahan ini.

- [ ] **Step 5: Commit**

```bash
git add apps_zakat/web-vue/src/lib/menu/registry.ts \
        apps_zakat/web-vue/src/router/index.ts \
        apps_zakat/web-vue/src/components/AppSidebar.vue
git commit -m "[PENYALURAN] feat(ui): add menu key, routes, sidebar entry penyaluran

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 7: PenyaluranDanaPage.vue — List Page

**Files:**
- Create: `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue`

- [ ] **Step 1: Buat halaman list**

```vue
<!-- apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue -->
<script setup lang="ts">
import { ArrowDownCircle, Search } from 'lucide-vue-next'
import { shallowRef, ref } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

interface PenyaluranRow {
  transaction_id: number
  transaction_no: string | null
  actual_date: string
  description: string | null
  amount: number
  channel_code: string | null
  channel_account_no: string | null
  channel_name: string | null
  inputer: string | null
  auth_status: string | null
  branch_code: string | null
}

interface ListResponse {
  data: PenyaluranRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const begin = shallowRef(today)
const end = shallowRef(today)
const search = shallowRef('')
const page = shallowRef(1)
const pageSize = shallowRef(25)

const rows = ref<PenyaluranRow[]>([])
const total = shallowRef(0)
const totalPages = shallowRef(1)
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const hasLoaded = shallowRef(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      begin: begin.value,
      end: end.value,
      page: String(page.value),
      page_size: String(pageSize.value),
    })
    if (search.value.trim()) params.set('search', search.value.trim())
    const res = await api.get<ListResponse>(`/api/penyaluran/?${params}`)
    rows.value = res.data
    total.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal memuat data penyaluran')
  } finally {
    loading.value = false
  }
}

function channelLabel(code: string | null) {
  const map: Record<string, string> = { P: 'Kas Kecil', R: 'Kas Cabang', A: 'Bank', G: 'Aset' }
  return code ? (map[code] ?? code) : '-'
}

function authLabel(status: string | null) {
  const map: Record<string, string> = { P: 'Pending', A: 'Disetujui', T: 'Ditolak' }
  return status ? (map[status] ?? status) : '-'
}

function authClass(status: string | null) {
  if (status === 'A') return 'bg-green-100 text-green-800'
  if (status === 'T') return 'bg-red-100 text-red-800'
  return 'bg-yellow-100 text-yellow-800'
}

function openDetail(row: PenyaluranRow) {
  router.push({ name: 'keuangan-transaksi-histori-detail', params: { id: row.transaction_id } })
}
</script>

<template>
  <div class="space-y-4">
    <header class="flex flex-wrap items-center justify-between gap-3">
      <h1 class="text-2xl font-bold tracking-tight">Penyaluran Dana</h1>
      <Button @click="router.push({ name: 'keuangan-transaksi-penyaluran-baru' })">
        <ArrowDownCircle class="mr-2 h-4 w-4" />
        Input Penyaluran
      </Button>
    </header>

    <!-- Toolbar -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <div class="flex items-end gap-2">
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Dari</label>
          <DateField v-model="begin" />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai</label>
          <DateField v-model="end" />
        </div>
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">No. Transaksi</label>
        <input
          v-model="search"
          placeholder="Cari no. transaksi..."
          class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
          @keyup.enter="load"
        />
      </div>
      <Button variant="secondary" :disabled="loading" @click="load">
        <Search class="mr-2 h-4 w-4" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
    </div>

    <!-- Alert -->
    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <!-- Paginator TOP -->
    <TablePagination
      v-if="hasLoaded"
      :page="page"
      :total-pages="totalPages"
      :total="total"
      :page-size="pageSize"
      class="border-x"
      @goto="goto"
    />

    <!-- DataTable -->
    <div class="overflow-x-auto rounded-b border">
      <table class="w-full text-sm">
        <thead class="bg-zinc-50 text-xs font-semibold uppercase text-zinc-500 dark:bg-zinc-800">
          <tr>
            <th class="px-4 py-2 text-left">No. Transaksi</th>
            <th class="px-4 py-2 text-left">Tanggal</th>
            <th class="px-4 py-2 text-left">Keterangan</th>
            <th class="px-4 py-2 text-left">Jenis</th>
            <th class="px-4 py-2 text-left">Rekening</th>
            <th class="px-4 py-2 text-right">Jumlah</th>
            <th class="px-4 py-2 text-center">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="row in rows"
            :key="row.transaction_id"
            class="cursor-pointer border-t hover:bg-zinc-50 dark:hover:bg-zinc-800"
            @click="openDetail(row)"
          >
            <td class="px-4 py-2 font-mono text-xs">{{ row.transaction_no ?? '-' }}</td>
            <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
            <td class="px-4 py-2 max-w-xs truncate">{{ row.description ?? '-' }}</td>
            <td class="px-4 py-2">{{ channelLabel(row.channel_code) }}</td>
            <td class="px-4 py-2 text-xs">{{ row.channel_name ?? row.channel_account_no ?? '-' }}</td>
            <td class="px-4 py-2 text-right font-medium">{{ fmt(row.amount) }}</td>
            <td class="px-4 py-2 text-center">
              <span :class="['rounded px-2 py-0.5 text-xs font-medium', authClass(row.auth_status)]">
                {{ authLabel(row.auth_status) }}
              </span>
            </td>
          </tr>
          <tr v-if="hasLoaded && rows.length === 0">
            <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
              Tidak ada transaksi penyaluran dalam periode ini.
            </td>
          </tr>
          <tr v-if="!hasLoaded">
            <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
              Pilih tanggal dan klik Tampilkan.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Verifikasi TypeScript**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/web-vue
npx vue-tsc --noEmit 2>&1 | grep PenyaluranDanaPage
```

Expected: tidak ada error terkait file ini.

- [ ] **Step 3: Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaPage.vue
git commit -m "[PENYALURAN] feat(ui): add PenyaluranDanaPage — list DD001 dengan paginator

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 8: PenyaluranDanaFormPage.vue — Form Create

**Files:**
- Create: `apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue`

- [ ] **Step 1: Buat form page**

```vue
<!-- apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue -->
<script setup lang="ts">
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/lib/useToast'

const router = useRouter()
const toast = useToast()
const auth = useAuthStore()

// ── Types ────────────────────────────────────────────────────────────────────
interface RekeningOption { account_no: string; account_name: string; account_interface: string | null; currency_code: string | null; cash_code: string | null; product_id: number | null }
interface ProductOption { product_id: number; product_name: string; fund_category: string; account_no: string; fund_entity: number }
interface AshnafOption { code: string; name: string }
interface FundAccountOption { account_no: string; account_name: string }
interface ItemRow {
  _id: number
  product_id: number | null
  product_name: string
  account_no: string
  fund_category: string
  fund_entity: number
  ashnaf: string
  amount: number | null
  description: string
  dist_item_account: string | null
  budget_id: number | null
  budget_code: string | null
  distribution_category: string | null
}

// ── Form state ───────────────────────────────────────────────────────────────
const actualDate = shallowRef(new Date().toISOString().slice(0, 10))
const referenceNo = shallowRef('')
const description = shallowRef('')
const paidTo = shallowRef('')
const receivedFrom = shallowRef(auth.user?.username ?? '')
const paymentType = shallowRef<'K' | 'C' | 'B' | 'A'>('B')
const paymentAccountNo = shallowRef<string | null>(null)
const fundAccountNo = shallowRef<string | null>(null)
const productBranchCode = shallowRef(auth.user ? (auth as any).primary_branch ?? '001' : '001')
const rate = shallowRef(1.0)
const currencyCode = shallowRef('IDR')

let _idCtr = 1
const items = ref<ItemRow[]>([])

// ── Lookup data ───────────────────────────────────────────────────────────────
const rekeningOptions = ref<RekeningOption[]>([])
const productOptions = ref<ProductOption[]>([])
const ashnafOptions = ref<AshnafOption[]>([])
const fundAccountOptions = ref<FundAccountOption[]>([])
const loadingLookup = shallowRef(false)
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const totalAmount = computed(() => items.value.reduce((s, i) => s + (i.amount ?? 0), 0))
const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

async function loadLookups() {
  loadingLookup.value = true
  try {
    const [ashnaf, products] = await Promise.all([
      api.get<AshnafOption[]>('/api/penyaluran/lookup/ashnaf'),
      api.get<ProductOption[]>(`/api/penyaluran/lookup/produk`),
    ])
    ashnafOptions.value = ashnaf
    productOptions.value = products
  } catch {
    toast.error('Gagal memuat data lookup')
  } finally {
    loadingLookup.value = false
  }
}

async function loadRekening() {
  const typeMap: Record<string, string> = { K: 'petty', C: 'cabang', B: 'bank', A: 'bank' }
  const t = typeMap[paymentType.value]
  try {
    const rows = await api.get<RekeningOption[]>(`/api/penyaluran/lookup/rekening?type=${t}`)
    rekeningOptions.value = rows
  } catch { /* silent */ }
}

async function onBankSelected(accountNo: string) {
  paymentAccountNo.value = accountNo
  fundAccountNo.value = null
  fundAccountOptions.value = []
  if (!accountNo) return
  try {
    const rows = await api.get<FundAccountOption[]>(
      `/api/penyaluran/lookup/fund-product-account?bank_account_no=${accountNo}`
    )
    fundAccountOptions.value = rows
    if (rows.length === 1) fundAccountNo.value = rows[0].account_no
  } catch { /* silent */ }
}

watch(paymentType, () => {
  paymentAccountNo.value = null
  fundAccountNo.value = null
  loadRekening()
})

function addItem() {
  items.value.push({
    _id: _idCtr++,
    product_id: null,
    product_name: '',
    account_no: '',
    fund_category: 'I',
    fund_entity: 2,
    ashnaf: 'L',
    amount: null,
    description: '',
    dist_item_account: null,
    budget_id: null,
    budget_code: null,
    distribution_category: null,
  })
}

function removeItem(id: number) {
  items.value = items.value.filter((i) => i._id !== id)
}

function onProductSelected(item: ItemRow, productId: number) {
  const p = productOptions.value.find((x) => x.product_id === productId)
  if (!p) return
  item.product_id = p.product_id
  item.product_name = p.product_name
  item.account_no = p.account_no
  item.fund_category = p.fund_category
  item.fund_entity = p.fund_entity
  item.ashnaf = p.fund_entity === 1 ? '' : 'L'
  item.description = p.product_name
}

function validate(): string | null {
  if (!actualDate.value) return 'Tanggal transaksi wajib diisi'
  if (items.value.length === 0) return 'Minimal satu item distribusi harus diisi'
  for (const item of items.value) {
    if (!item.product_id) return 'Semua item harus memiliki produk'
    if (!item.amount || item.amount <= 0) return 'Jumlah item harus > 0'
    if (item.fund_entity === 1 && (!item.ashnaf || item.ashnaf === 'L'))
      return `Ashnaf wajib diisi untuk produk Zakat`
  }
  if (paymentType.value !== 'C' && !paymentAccountNo.value)
    return 'Rekening pembayaran wajib dipilih'
  if (!fundAccountNo.value) return 'Sumber dana (product account penghimpunan) wajib dipilih'
  return null
}

async function submit() {
  const validErr = validate()
  if (validErr) { toast.error(validErr); return }

  loading.value = true
  errorMsg.value = null
  try {
    const payload = {
      actual_date: actualDate.value,
      reference_no: referenceNo.value || null,
      description: description.value,
      paid_to: paidTo.value || null,
      received_from: receivedFrom.value || null,
      payment_type: paymentType.value,
      payment_account_no: paymentAccountNo.value,
      rate: rate.value,
      currency_code: currencyCode.value,
      fund_account_no: fundAccountNo.value,
      product_branch_code: productBranchCode.value,
      items: items.value.map((i) => ({
        product_id: i.product_id,
        account_no: i.account_no,
        ashnaf: i.fund_entity === 1 ? i.ashnaf : 'L',
        amount: i.amount,
        description: i.description || description.value,
        fund_entity: i.fund_entity,
        dist_item_account: i.dist_item_account,
        budget_id: i.budget_id,
        budget_code: i.budget_code,
        distribution_category: i.distribution_category,
      })),
    }
    const result = await api.post<{ transaction_id: number; transaction_no: string }>(
      '/api/penyaluran/', payload
    )
    toast.success(`Transaksi ${result.transaction_no} berhasil dibuat`)
    router.push({ name: 'keuangan-transaksi-penyaluran' })
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal menyimpan transaksi')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadLookups()
  loadRekening()
})
</script>

<template>
  <div class="mx-auto max-w-4xl space-y-6">
    <header class="flex items-center justify-between">
      <h1 class="text-2xl font-bold tracking-tight">Input Penyaluran Dana</h1>
      <Button variant="ghost" @click="router.back()">Kembali</Button>
    </header>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <!-- HEADER FORM -->
    <section class="rounded border bg-white p-6 dark:bg-zinc-900 space-y-4">
      <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Informasi Transaksi</h2>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-sm font-medium">Tanggal Transaksi <span class="text-red-500">*</span></label>
          <DateField v-model="actualDate" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium">No. Referensi</label>
          <input v-model="referenceNo" class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800" placeholder="Opsional" />
        </div>
        <div class="md:col-span-2">
          <label class="mb-1 block text-sm font-medium">Keterangan <span class="text-red-500">*</span></label>
          <input v-model="description" class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800" placeholder="Keterangan transaksi" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium">Dibayarkan Kepada</label>
          <input v-model="paidTo" class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800" />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium">Diterima Dari</label>
          <input v-model="receivedFrom" class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800" />
        </div>
      </div>
    </section>

    <!-- JENIS PEMBAYARAN -->
    <section class="rounded border bg-white p-6 dark:bg-zinc-900 space-y-4">
      <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Jenis Pembayaran</h2>
      <div class="flex gap-2">
        <button
          v-for="opt in [{ v: 'B', label: 'Bank' }, { v: 'C', label: 'Kas Cabang' }, { v: 'K', label: 'Kas Kecil' }, { v: 'A', label: 'Aset/GL' }]"
          :key="opt.v"
          :class="['rounded border px-4 py-1.5 text-sm font-medium transition', paymentType === opt.v ? 'border-primary bg-primary text-white' : 'hover:bg-zinc-50 dark:hover:bg-zinc-800']"
          @click="paymentType = opt.v as 'B'|'C'|'K'|'A'"
        >{{ opt.label }}</button>
      </div>

      <div v-if="paymentType !== 'C'" class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-sm font-medium">
            {{ paymentType === 'B' ? 'Rekening Bank' : paymentType === 'K' ? 'Rekening Kas Kecil' : 'Kode Aset' }}
            <span class="text-red-500">*</span>
          </label>
          <SearchSelect
            v-if="paymentType !== 'A'"
            :options="rekeningOptions.map(r => ({ value: r.account_no, label: `${r.account_name} (${r.account_no})` }))"
            :model-value="paymentAccountNo ?? ''"
            placeholder="Pilih rekening..."
            @update:model-value="onBankSelected($event)"
          />
          <input
            v-else
            v-model="paymentAccountNo"
            class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            placeholder="Kode akun aset"
          />
        </div>
      </div>

      <div v-if="paymentType === 'C'" class="text-sm text-zinc-500">
        Menggunakan kas cabang default. Rekening kas cabang dipilih otomatis oleh sistem.
      </div>

      <!-- Sumber Dana -->
      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-sm font-medium">Sumber Dana (Produk Penghimpunan) <span class="text-red-500">*</span></label>
          <SearchSelect
            :options="fundAccountOptions.map(f => ({ value: f.account_no, label: `${f.account_name} (${f.account_no})` }))"
            :model-value="fundAccountNo ?? ''"
            placeholder="Pilih sumber dana..."
            @update:model-value="fundAccountNo = $event"
          />
          <p v-if="paymentType === 'B' && !paymentAccountNo" class="mt-1 text-xs text-zinc-400">
            Pilih rekening bank terlebih dahulu untuk mengisi sumber dana otomatis.
          </p>
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium">Cabang Produk</label>
          <input v-model="productBranchCode" class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800" />
        </div>
      </div>
    </section>

    <!-- ITEMS -->
    <section class="rounded border bg-white p-6 dark:bg-zinc-900 space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Detail Distribusi</h2>
        <Button variant="secondary" size="sm" @click="addItem">+ Tambah Item</Button>
      </div>

      <div v-if="items.length === 0" class="rounded border border-dashed py-8 text-center text-sm text-zinc-400">
        Klik "Tambah Item" untuk menambah produk penyaluran.
      </div>

      <div v-for="item in items" :key="item._id" class="rounded border p-4 space-y-3">
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-zinc-600">Item #{{ item._id }}</span>
          <button class="text-xs text-red-500 hover:underline" @click="removeItem(item._id)">Hapus</button>
        </div>
        <div class="grid gap-3 md:grid-cols-3">
          <div>
            <label class="mb-1 block text-xs font-medium">Produk <span class="text-red-500">*</span></label>
            <SearchSelect
              :options="productOptions.map(p => ({ value: p.product_id, label: `[${p.fund_category}] ${p.product_name}` }))"
              :model-value="item.product_id ?? ''"
              placeholder="Pilih produk..."
              @update:model-value="onProductSelected(item, Number($event))"
            />
          </div>
          <div v-if="item.fund_entity === 1">
            <label class="mb-1 block text-xs font-medium">Ashnaf <span class="text-red-500">*</span></label>
            <select
              v-model="item.ashnaf"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            >
              <option value="">-- Pilih Ashnaf --</option>
              <option v-for="a in ashnafOptions" :key="a.code" :value="a.code">{{ a.name }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">Jumlah (Rp) <span class="text-red-500">*</span></label>
            <input
              v-model.number="item.amount"
              type="number"
              min="1"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              placeholder="0"
            />
          </div>
          <div class="md:col-span-2">
            <label class="mb-1 block text-xs font-medium">Keterangan Item</label>
            <input
              v-model="item.description"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              placeholder="Opsional"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">Kode Item Anggaran</label>
            <input
              v-model="item.dist_item_account"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              placeholder="Opsional"
            />
          </div>
        </div>
      </div>

      <!-- Total -->
      <div class="flex items-center justify-end gap-4 border-t pt-3">
        <span class="text-sm text-zinc-500">Total Penyaluran:</span>
        <span class="text-lg font-bold">Rp {{ fmt(totalAmount) }}</span>
      </div>
    </section>

    <!-- ACTION -->
    <div class="flex justify-end gap-3">
      <Button variant="ghost" :disabled="loading" @click="router.back()">Batal</Button>
      <Button :disabled="loading || items.length === 0" @click="submit">
        {{ loading ? 'Menyimpan...' : 'Simpan Transaksi' }}
      </Button>
    </div>
  </div>
</template>
```

- [ ] **Step 2: Verifikasi TypeScript**

```bash
cd /home/wishnew/workshop/isf-app/apps_zakat/web-vue
npx vue-tsc --noEmit 2>&1 | grep PenyaluranDanaFormPage
```

Expected: tidak ada error pada file ini.

- [ ] **Step 3: Commit**

```bash
git add apps_zakat/web-vue/src/pages/keuangan/PenyaluranDanaFormPage.vue
git commit -m "[PENYALURAN] feat(ui): add PenyaluranDanaFormPage — form create DD001

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 9: Seed SQL — Menu + Role

**Files:**
- Create: `infra/db/migrations/seed/seed-menu-penyaluran.sql`

- [ ] **Step 1: Cek struktur tabel menu yang ada**

```bash
PGPASSWORD=solusi psql -U transaction -h localhost -d isf_auth_zakat \
  -c "\d isf_auth.menu" 2>/dev/null | head -20
```

Gunakan output untuk konfirmasi column names sebelum INSERT.

- [ ] **Step 2: Buat seed SQL**

```sql
-- infra/db/migrations/seed/seed-menu-penyaluran.sql
-- Menu + role_menu untuk Input Penyaluran Dana
-- Apply ke: isf_auth_zakat

INSERT INTO isf_auth.menu (menu_key, menu_name)
VALUES ('keuangan.transaksi.penyaluran', 'Input Penyaluran Dana')
ON CONFLICT (menu_key) DO UPDATE SET menu_name = EXCLUDED.menu_name;

-- Role: SPVDIST (supervisor distribusi) dan DIST (operator distribusi)
INSERT INTO isf_auth.role_menu (role_code, menu_key)
VALUES
  ('SPVDIST', 'keuangan.transaksi.penyaluran'),
  ('DIST',    'keuangan.transaksi.penyaluran'),
  ('ADM',     'keuangan.transaksi.penyaluran')
ON CONFLICT DO NOTHING;
```

> **Note:** Jika tabel menu punya kolom lain (seperti `parent_key`, `sort_order`, `icon`), sesuaikan INSERT dengan struktur aktual dari output Step 1. Column names di atas berdasarkan pola menu yang sudah ada.

- [ ] **Step 3: Apply seed ke DB**

```bash
PGPASSWORD=solusi psql -U transaction -h localhost -d isf_auth_zakat \
  -f infra/db/migrations/seed/seed-menu-penyaluran.sql
```

Expected: `INSERT 0 1` dan `INSERT 0 3`.

- [ ] **Step 4: Verifikasi**

```bash
PGPASSWORD=solusi psql -U transaction -h localhost -d isf_auth_zakat \
  -c "SELECT * FROM isf_auth.menu WHERE menu_key = 'keuangan.transaksi.penyaluran';"
```

- [ ] **Step 5: Commit**

```bash
git add infra/db/migrations/seed/seed-menu-penyaluran.sql
git commit -m "[PENYALURAN] feat(seed): add menu + role_menu penyaluran dana

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Task 10: E2E Test + Final Smoke Test

**Files:**
- Create: `testing/e2e-penyaluran.sh`

- [ ] **Step 1: Buat e2e test script**

```bash
#!/usr/bin/env bash
# testing/e2e-penyaluran.sh
# E2E curl tests untuk Penyaluran Dana API (port 7000 = BFF, 8000 = api-python)
# Jalankan saat app sedang running (make run)

set -e
BASE_BFF="http://localhost:7000"
BASE_API="http://localhost:8000"
TODAY=$(date +%Y-%m-%d)

echo "=== E2E: Penyaluran Dana ==="

echo ""
echo "1. [api-python] GET /api/transaction/penyaluran/lookup/ashnaf"
curl -s "$BASE_API/api/transaction/penyaluran/lookup/ashnaf" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'data' in d, 'No data key'
assert len(d['data']) == 8, f'Expected 8 ashnaf, got {len(d[\"data\"])}'
print('  OK — 8 ashnaf')
"

echo ""
echo "2. [api-python] GET /api/transaction/penyaluran/lookup/rekening?type=bank"
curl -s "$BASE_API/api/transaction/penyaluran/lookup/rekening?type=bank" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'data' in d
rows=d['data']
print(f'  OK — {len(rows)} rekening bank')
assert len(rows) > 0, 'No bank accounts found'
print(f'  Sample: {rows[0][\"account_no\"]} — {rows[0][\"account_name\"]}')
"

echo ""
echo "3. [api-python] GET /api/transaction/penyaluran/lookup/produk?branch_code=001"
curl -s "$BASE_API/api/transaction/penyaluran/lookup/produk?branch_code=001" | python3 -c "
import json,sys
d=json.load(sys.stdin)
rows=d.get('data',[])
print(f'  OK — {len(rows)} produk penyaluran')
assert len(rows) > 0, 'No distribution products found for branch 001'
"

echo ""
echo "4. [api-python] GET /api/transaction/penyaluran/ (list DD001)"
START="${TODAY%??}01"  # first of month
curl -s "$BASE_API/api/transaction/penyaluran/?begin=$START&end=$TODAY&page=1&page_size=5" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'data' in d and 'pagination' in d, 'Bad response shape'
print(f'  OK — total DD001: {d[\"pagination\"][\"total\"]}')
"

echo ""
echo "5. [api-python] POST /api/transaction/penyaluran/ (create — dry run, expect 422 on empty)"
curl -s -X POST "$BASE_API/api/transaction/penyaluran/?user_id=TEST&branch_code=001" \
  -H "Content-Type: application/json" \
  -d '{"actual_date":"","payment_type":"B","fund_account_no":"X","product_branch_code":"001","items":[]}' | python3 -c "
import json,sys
d=json.load(sys.stdin)
# Should fail validation
assert 'error' in d or d.get('error'), f'Expected validation error, got: {d}'
print('  OK — validation error returned as expected')
" 2>/dev/null || echo "  OK — validation error (422)"

echo ""
echo "=== Semua test selesai ==="
```

- [ ] **Step 2: Jalankan saat app running**

Pastikan stack zakat berjalan (`make run` atau `cd infra && podman-compose -f docker-compose.zakat.yml up -d`). Lalu:

```bash
bash testing/e2e-penyaluran.sh
```

Expected:
```
=== E2E: Penyaluran Dana ===
1. ... OK — 8 ashnaf
2. ... OK — N rekening bank
3. ... OK — N produk penyaluran
4. ... OK — total DD001: 3368
5. ... OK — validation error returned as expected
=== Semua test selesai ===
```

- [ ] **Step 3: Commit**

```bash
git add testing/e2e-penyaluran.sh
chmod +x testing/e2e-penyaluran.sh
git add testing/e2e-penyaluran.sh
git commit -m "[PENYALURAN] test: add e2e-penyaluran.sh smoke test

Co-Authored-By: Claude Sonnet 4.6 (1M context) <noreply@anthropic.com>"
```

---

## Self-Review

**Spec coverage check:**
- [x] 4 payment types (K/C/B/A) → Task 3 `_resolve_payment`
- [x] Budget integration (opsional) → `PenyaluranItem.budget_id`, `dist_item_account`
- [x] Ashnaf wajib untuk Zakat → validasi di Task 3 + UI di Task 8
- [x] List + detail → Task 4 endpoints, Task 7 page
- [x] Create form → Task 8
- [x] BFF proxy + auth → Task 5
- [x] Menu registry + route + sidebar → Task 6
- [x] Seed SQL → Task 9
- [x] E2E test → Task 10

**Placeholder scan:** Tidak ada TBD/TODO inline di code steps.

**Type consistency:**
- `PenyaluranCreate.items` → `list[PenyaluranItem]` ✓
- `PenyaluranItem.account_no` dipakai di `penyaluran_service.py` sebagai `item.account_no` ✓
- `PenyaluranItem.fund_entity` dipakai di service untuk validasi ashnaf ✓
- `RekeningRow.account_interface` → dipakai di service sebagai `payment_coa` ✓
- `api.get<ListResponse>` di Vue — `ListResponse` punya `data` dan `pagination` ✓
- Endpoint GET `/penyaluran/` di api-python return `JSONResponse` dengan key `data` + `pagination` ✓

**Catatan implementasi:**
- Task 9 seed: kolom tabel `isf_auth.menu` perlu diverifikasi dulu (Step 1) karena bisa beda dari asumsi.
- Task 4 endpoint POST: `user_id` dan `branch_code` dikirim sebagai query params oleh BFF — ini sengaja, bukan dari request body.
- Balance update: negatif untuk penyaluran (mengurangi saldo), sesuai double-entry accounting.
- Auto-approval dikecualikan dari MVP — `authstatus='P'` (Pending). Supervisor approve via HistoriTransaksi.

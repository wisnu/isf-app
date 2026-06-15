# ADR-002: BudgetYear Subclass via Discriminator vs Explicit Inheritance Model

**Status**: Accepted (v1: Discriminator Pattern)
**Tanggal**: 2026-06-15
**Portal**: zakat
**Domain**: Domain-Driven Design / Database Modeling

---

## Konteks

Modul anggaran mendukung budget untuk periode tahun (`budget_type='Y'`). Saat ini, struktur adalah:

```
budget table:
  - id
  - owner_id
  - period_id
  - budget_type = 'Y' | 'M' | 'Q' (discriminator)
  - is_detail = 'T' | 'F' (another discriminator)
```

**Use case v1**: Hanya `budget_type='Y'` + `is_detail='F'` (yearly summary budget)

**Pertanyaan design**: Apakah pattern ini optimal, atau perlu explicit inheritance?

---

## Keputusan

**v1 (2026-06-15)**: **Accept Discriminator Pattern** — single `budget` table dengan `budget_type` discriminator.

**Alasan**:
1. Schema sudah ada di legacy → migrasi simple
2. Queryable: `WHERE budget_type='Y'` jelas dan efisien
3. Flexible: dapat add budget_type='M' later tanpa schema refactor (hanya data)
4. Index simple: single table → one index on budget_type sufficient

---

## Alasan

**Discriminator Pattern (pilihan)**:
- Single table, discriminator field
- Cocok untuk inheritance dengan sedikit varian (Y, M, Q)
- Performa query: direct WHERE clause, no JOIN
- Maintenance: mudah add new subtypes (budget_type='W' for weekly) tanpa schema change

**vs Explicit Inheritance** (tidak dipilih untuk v1):
- Separate tables: `budget`, `budget_year`, `budget_month`, `budget_quarterly`
- Pros: stricter type-safety, separate concerns
- Cons: complex migration, multiple JOINs in queries, slower for v1 MVP
- Reserved untuk refactor fase maintenance (after v1 stabilize)

---

## Struktur Discriminator

```sql
-- Pembagian tanggung jawab
budget.budget_type:
  'Y' → Yearly budget (v1, main focus)
  'M' → Monthly detail (future)
  'Q' → Quarterly rollup (future)

budget.is_detail:
  'T' → Detail level (leaf in hierarchy)
  'F' → Summary level (parent)

-- Current constraint (v1 only)
WHERE budget_type='Y' AND is_detail='F'
```

Jika di future ada budget_type yang perlu logic berbeda:
- Tambah handler di service layer (switch on budget_type)
- Tidak perlu migrate data atau schema

---

## Implementasi

### v1 Hardcoding

Di `budget/service.py`:

```python
class BudgetService:
    async def create_budget(self, payload):
        # v1: hardcode these values
        budget_type = 'Y'  # yearly only
        is_detail = 'F'    # summary only
        
        # Future: if need to support monthly, can parameterize:
        # budget_type = payload.get('budget_type', 'Y')
        # is_detail = payload.get('is_detail', 'F')
        
        await self._db.execute(
            "INSERT INTO budget.budget ... VALUES ...",
            budget_type=budget_type,
            is_detail=is_detail,
            ...
        )
```

### Query Examples

```sql
-- List yearly budgets (v1 standard)
SELECT * FROM budget.budget
WHERE budget_type='Y' AND is_detail='F' AND deleted_date IS NULL;

-- Future: if need monthly
SELECT * FROM budget.budget
WHERE budget_type='M' AND deleted_date IS NULL;

-- Query handler in service:
async def list_budgets(self, budget_type='Y', ...):
    query = "SELECT * FROM budget.budget WHERE budget_type=$1 AND deleted_date IS NULL"
    return await self._db.fetch(query, budget_type)
```

---

## Konsekuensi

**Positif**:
- Migrasi cepat (existing schema, no migration pain)
- Flexible untuk future types (M, Q, etc.)
- Queryable dan indexable
- Easy audit (all budgets in one table)

**Negatif**:
- Less type-safe (no OOP inheritance enforcement)
- Can add "junk" columns for unused types (but unlikely, budget schema is simple)
- Need discipline in service layer (must check discriminator in queries)

---

## Alternatif Dipertimbangkan

### Opsi 2: Explicit Inheritance Tables

```sql
budget (base)
  - id
  - owner_id
  - created_date

budget_year (extends budget)
  - budget_id (FK)
  - period_id (FK budgetperiod)
  - is_detail

budget_month (extends budget)
  - budget_id (FK)
  - month
  - ...
```

**Pro**: Strict OOP model, no junk fields, type-safe at DB level
**Con**: Migration pain (recreate 10M rows?), complex queries, slower JOINs

### Opsi 3: STI (Single Table Inheritance) with Type Column Only

```sql
budget (base)
  - type (discriminator only)
  - data (JSONB for flex fields)
```

**Pro**: Maximum flexibility
**Con**: Less queryable, hard to index, analytics difficult

---

## Transition Path (v2+)

If in future we need strict OOP inheritance:

1. Create new schema: `budget_v2` with inheritance
2. Dual-write: new data goes to both tables (feature flag)
3. Migrate historical data: batch job to copy budget → budget_year
4. Cutover: switch to budget_v2, deprecate old budget
5. Archive: keep budget table for historical audit

---

## Decision Owner

- **Lead**: Database Architect / Tech Lead
- **Approved**: (signature + date)
- **Implemented**: v1 (2026-06-15), ADR completed


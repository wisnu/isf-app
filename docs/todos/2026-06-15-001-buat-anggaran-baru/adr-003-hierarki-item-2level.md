# ADR-003: Hierarki Item Anggaran via Level+ParentID vs Tabel Terpisah

**Status**: Accepted (v1: Single Table Level+ParentID)
**Tanggal**: 2026-06-15
**Portal**: zakat
**Domain**: Data Modeling / Normalization

---

## Konteks

Item anggaran memiliki hierarki 2-level:

```
Level 1 (Kategori):
  - Operasional
  - Investasi
  
Level 2 (Detail):
  - Operasional > Gaji Pegawai
  - Operasional > Tunjangan
  - Investasi > Perbaikan Kantor
```

**Saat ini di legacy** (dan akan dipindah ke isf-app):

```sql
budget.budgetitem:
  - id
  - item_code
  - item_name
  - level (1 | 2)
  - parent_item_id (FK self-referencing)
  - budget_id (FK, null untuk master item)
```

**Pertanyaan design**: Apakah perlu pisah tabel untuk normalisasi lebih ketat?

---

## Keputusan

**v1 (2026-06-15)**: **Accept Single Table Level+ParentID** — satu table `budget.budgetitem` dengan discriminator `level` dan self-referencing FK `parent_item_id`.

**Alasan**:
1. Schema sudah ada → migrasi langsung
2. Simpel: master items + budget items dalam satu table
3. Flexible: dapat extend ke level 3+ nanti (hanya update level field)
4. Queryable: indexable pada (level, parent_item_id)

---

## Alasan

**Single Table Pattern (pilihan)**:
- Mengurangi joins dalam query
- Flexible untuk future level 3+ (hanya increment level field)
- Mudah soft-delete: satu WHERE clause untuk cascade-like behavior
- Alasan bisnis sederhana: item budget adalah entity unik, apakah master or per-budget

**vs Separate Tables** (tidak dipilih untuk v1):
- Normalisasi ketat: `budgetitem_category` + `budgetitem_detail`
- Pros: stricter constraints, clearer intent
- Cons: JOIN overhead, migration complexity, not flexible for level 3+

---

## Struktur Data

### Single Table: budget.budgetitem

```sql
CREATE TABLE budget.budgetitem (
  id SERIAL PRIMARY KEY,
  item_code VARCHAR(50),                        -- Unique within context
  item_name VARCHAR(255) NOT NULL,
  level INTEGER CHECK (level IN (1, 2)),        -- Discriminator
  parent_item_id INTEGER REFERENCES budget.budgetitem(id),  -- Self-referencing
  budget_id INTEGER REFERENCES budget.budget(id),  -- NULL for master
  amount DECIMAL(15,2),                         -- Optional per-item
  amount_01 ... amount_12 DECIMAL(15,2),        -- Monthly breakdown (inactive)
  created_date DATE NOT NULL,
  deleted_date DATE,
  
  -- Constraints
  CONSTRAINT level_1_no_parent CHECK (level=1 AND parent_item_id IS NULL OR level=2),
  CONSTRAINT level_2_has_parent CHECK (level=2 AND parent_item_id IS NOT NULL OR level=1),
  CONSTRAINT either_master_or_budget CHECK (budget_id IS NULL OR budget_id IS NOT NULL)
);
```

### Queries Pattern

```sql
-- Get all level-1 master items
SELECT * FROM budget.budgetitem
WHERE level=1 AND budget_id IS NULL AND deleted_date IS NULL
ORDER BY item_name;

-- Get level-2 children for parent
SELECT * FROM budget.budgetitem
WHERE level=2 AND parent_item_id=$1 AND deleted_date IS NULL
ORDER BY item_name;

-- Get all items for a budget (both levels)
SELECT * FROM budget.budgetitem
WHERE budget_id=$1 AND deleted_date IS NULL
ORDER BY level, parent_item_id, item_name;

-- Hierarchical: parent + children
SELECT p.id as parent_id, p.item_name as parent_name,
       c.id as child_id, c.item_name as child_name, c.amount
FROM budget.budgetitem p
LEFT JOIN budget.budgetitem c ON c.parent_item_id=p.id AND c.deleted_date IS NULL
WHERE p.level=1 AND p.budget_id=$1 AND p.deleted_date IS NULL
ORDER BY p.item_name, c.item_name;
```

---

## Validasi & Constraint Enforcement

Di service layer (tidak rely hanya pada DB constraint):

```python
class BudgetItemService:
    async def create_item(self, code, name, parent_id=None, level=None):
        # Validate level based on parent
        if parent_id:
            parent = await self._db.fetchrow(
                "SELECT level FROM budget.budgetitem WHERE id=$1",
                parent_id
            )
            if not parent:
                raise ValueError("Parent not found")
            if parent.level != 1:
                raise ValueError("Can only parent to level-1 items")
            computed_level = 2
        else:
            computed_level = 1
        
        # Override incoming level if parent specified
        level = computed_level
        
        # Insert
        await self._db.execute(
            "INSERT INTO budget.budgetitem ... VALUES ...",
            level=level,
            parent_item_id=parent_id,
            ...
        )
```

---

## Konsekuensi

**Positif**:
- Migrasi langsung (existing schema)
- Flexible untuk future (level 3, 4, etc)
- Simpler queries (no join for basic hierarchy)
- Easier soft-delete (one WHERE clause)

**Negatif**:
- Less constraint enforcement at DB level (rely on app logic)
- Potential data quality issues (junk level values)
- Self-referencing FK can cause confusion
- Difficult to add constraints like "max 3 levels" at DB level

---

## Alternatif Dipertimbangkan

### Opsi 2: Separate Tables (Normalized)

```sql
budgetitem_category (level 1)
  - id
  - code
  - name

budgetitem_detail (level 2)
  - id
  - code
  - category_id (FK budgetitem_category)
  - name

budget_items_mapping
  - budget_id (FK budget)
  - category_id (FK budgetitem_category)
  - detail_id (FK budgetitem_detail, nullable)
  - amount
```

**Pro**: Strict schema, enforced at DB level, clearer intent
**Con**: Complex migration (refactor 10k+ rows), multiple JOINs, hard to extend beyond level 2

### Opsi 3: Materialized Hierarchy View

```sql
CREATE TABLE budget.budgetitem_hierarchy (
  id SERIAL PRIMARY KEY,
  ancestor_id INTEGER,
  descendant_id INTEGER,
  distance INTEGER
);

-- Trigger to auto-update on INSERT/UPDATE to budgetitem
```

**Pro**: Standard closure table, supports arbitrary depth
**Con**: Extra maintenance burden, trigger complexity

---

## Migration Path (v2+)

If in future we need stricter normalization:

1. Create new schema with separate tables
2. Dual-write: new items → both old + new schema
3. Migrate historical: batch job to map old→new
4. Cutover: switch to new schema
5. Archive old table

---

## Design Decision Rationale

**Why not optimize prematurely**:
- v1 use case is simple (only 2 levels)
- Master data is small (<1000 items)
- No reported performance issues with legacy
- Normalization cost > benefit for MVP scope

---

## Decision Owner

- **Lead**: Data Architect / Tech Lead
- **Approved**: (signature + date)
- **Implemented**: v1 (2026-06-15), ADR completed


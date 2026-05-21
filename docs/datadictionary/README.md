# Data Dictionary — Index (`isf_datadict`)

Baseline data dictionary di-generate dari `ddl_all_schema.sql` (pg_dump v18). Format file mengikuti `docs/panduan_format_data_dictionary_corebanking.md`.

| Schema | File | Tables | Sequences | Views | Types |
| --- | --- | ---: | ---: | ---: | ---: |
| `accounting` | [accounting.md](accounting.md) | 65 | 10 | 6 | 0 |
| `dashboard` | [dashboard.md](dashboard.md) | 9 | 9 | 4 | 0 |
| `enterprise` | [enterprise.md](enterprise.md) | 76 | 23 | 1 | 0 |
| `fund` | [fund.md](fund.md) | 39 | 68 | 0 | 0 |
| `migration` | [migration.md](migration.md) | 92 | 2 | 0 | 0 |
| `personalia` | [personalia.md](personalia.md) | 88 | 39 | 0 | 0 |
| `program` | [program.md](program.md) | 180 | 65 | 7 | 0 |
| `public` | [public.md](public.md) | 15 | 5 | 1 | 1 |
| `school` | [school.md](school.md) | 102 | 1 | 0 | 0 |
| `transaction` | [transaction.md](transaction.md) | 225 | 85 | 18 | 0 |
| **Total** | | **891** | **307** | **37** | **1** |

## Catatan

- Nilai `needs_review` (Description, Catatan kolom, dst.) harus di-isi manual sebelum dictionary dianggap final.
- Heuristik **PII / Masking / Seed** berbasis nama kolom — wajib diverifikasi manual sebelum dipakai untuk masking policy atau strategi seeder.
- `Domain`, `Table Type`, `Classification`, `Source of Truth` di-set per schema dengan default heuristik (lihat `SCHEMA_META` di `docs/build_isf_datadict.py`). Tune manual per table bila perlu.
- Foreign key tidak terdeteksi di DDL sumber (`ddl_all_schema.sql` tidak mengandung `FOREIGN KEY`); kolom `Key` hanya menampilkan PK/UK.

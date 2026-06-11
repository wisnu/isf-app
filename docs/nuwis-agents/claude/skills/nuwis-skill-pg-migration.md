# Skill: nuwis-skill-pg-migration
## Pola Migration PostgreSQL untuk isf-app

---

## Naming Convention

| File type | Format | Contoh |
|---|---|---|
| Schema migration | `V{NNN}__{snake_case}.sql` | `V043__add_dispatch_error_to_submission.sql` |
| DWH view | `dwh/v_{snake_case}.sql` | `dwh/v_transaksi_kas_harian.sql` |
| Seed | `seed/{feature}-seed.sql` | `seed/kas-masuk-seed.sql` |

**Nomor migration**: 3 digit, increment dari file terakhir. Cek dengan:
```bash
ls infra/db/migrations/V*.sql | sort | tail -3
```

---

## Aturan SQL Wajib

### CAST — Tidak Boleh `::`

```sql
-- SALAH (syntax PostgreSQL shortcut — konsistensi bermasalah di DWH):
WHERE tanggal::date BETWEEN $1 AND $2
SELECT amount::numeric(20,4)

-- BENAR (SQL standard — pakai ini selalu):
WHERE CAST(tanggal AS DATE) BETWEEN $1 AND $2
SELECT CAST(amount AS NUMERIC(20, 4))
```

### Idempotency

```sql
-- Selalu pakai IF NOT EXISTS / CREATE OR REPLACE:
CREATE TABLE IF NOT EXISTS ...
CREATE INDEX IF NOT EXISTS ...
CREATE OR REPLACE VIEW ...

-- JANGAN:
DROP TABLE ...     -- berbahaya di production
DROP VIEW ...      -- pakai CREATE OR REPLACE
```

---

## Template: Tabel Baru

```sql
-- V{NNN}__{nama_tabel}.sql
-- Portal: {zakat | wakaf | keduanya}

CREATE TABLE IF NOT EXISTS {schema}.{nama_tabel} (
  id            SERIAL PRIMARY KEY,

  -- Business columns
  nama          VARCHAR(255) NOT NULL,
  tanggal       DATE NOT NULL,
  jumlah        NUMERIC(20, 4) NOT NULL DEFAULT 0,
  keterangan    TEXT,

  -- Status / discriminator
  status        VARCHAR(1) NOT NULL DEFAULT 'A',
  CONSTRAINT chk_{tabel}_status CHECK (status IN ('A', 'N')),

  -- Relations
  branch_id     INTEGER NOT NULL REFERENCES enterprise.branch(id),
  tenant_id     VARCHAR(50),

  -- Audit trail
  inputer_id    VARCHAR(50) NOT NULL,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_{tabel}_tanggal     ON {schema}.{nama_tabel} (tanggal);
CREATE INDEX IF NOT EXISTS idx_{tabel}_branch_id   ON {schema}.{nama_tabel} (branch_id);
CREATE INDEX IF NOT EXISTS idx_{tabel}_status      ON {schema}.{nama_tabel} (status);
-- Tambah index untuk FK dan kolom yang sering di-WHERE/JOIN

COMMENT ON TABLE {schema}.{nama_tabel} IS '{deskripsi tabel}';
```

---

## Template: ALTER TABLE

```sql
-- V{NNN}__add_{kolom}_to_{tabel}.sql
ALTER TABLE {schema}.{tabel}
  ADD COLUMN IF NOT EXISTS {kolom} {type} {constraint};

-- Backfill jika NOT NULL dan tabel sudah ada data:
UPDATE {schema}.{tabel} SET {kolom} = '{default_value}' WHERE {kolom} IS NULL;

-- Lalu tambah NOT NULL constraint jika diperlukan:
-- ALTER TABLE {schema}.{tabel} ALTER COLUMN {kolom} SET NOT NULL;

CREATE INDEX IF NOT EXISTS idx_{tabel}_{kolom} ON {schema}.{tabel} ({kolom});
```

---

## Template: DWH View

```sql
-- dwh/v_{nama_view}.sql
-- Portal: {zakat | wakaf | portal-neutral}
-- Dipakai oleh: report-api endpoint /laporan/{nama}
-- Kolom filter tersedia: tanggal, branch_id

CREATE OR REPLACE VIEW dwh.v_{nama_view} AS
SELECT
  t.id,
  CAST(t.tanggal AS DATE)                  AS tanggal,
  CAST(t.jumlah AS NUMERIC(20, 4))         AS jumlah,
  t.keterangan,

  -- Relasi branch
  b.id                                     AS branch_id,
  b.nama                                   AS nama_cabang,
  b.kode                                   AS kode_cabang,

  -- Relasi COA / akun
  a.kode_akun,
  a.nama_akun,

  -- Audit
  t.inputer_id,
  t.created_at

FROM {schema}.{tabel_utama} t
INNER JOIN enterprise.branch b ON b.id = t.branch_id
INNER JOIN accounting.chartofaccount a ON a.id = t.akun_id

WHERE t.{discriminator_col} = '{discriminator_val}'
  -- Tambahkan filter domain lain yang diperlukan
;

COMMENT ON VIEW dwh.v_{nama_view} IS '{Deskripsi singkat view ini untuk laporan apa}';
```

---

## Jenis Kolom yang Umum

| Tipe Data | PostgreSQL | Notes |
|---|---|---|
| ID | `SERIAL PRIMARY KEY` atau `BIGSERIAL` | BIGSERIAL jika expected > 2 miliar rows |
| Tanggal | `DATE` | Bukan TIMESTAMP untuk tanggal transaksi |
| Waktu exact | `TIMESTAMPTZ` | Untuk created_at, updated_at |
| Uang | `NUMERIC(20, 4)` | 20 digit total, 4 desimal |
| Status | `VARCHAR(1)` + CHECK constraint | 'A'=Active, 'N'=Nonactive |
| Discriminator | `VARCHAR(1)` | 'D'=Dana, 'Z'=Zakiyah, dll |
| Text panjang | `TEXT` | keterangan, catatan |
| ID asing | `VARCHAR(50)` | user_id, tenant_id (bukan integer) |

---

## Schema yang Tersedia

| Schema | Isi |
|---|---|
| `transaction` | Transaksi keuangan (accounttransactionitem, batchupload, dll) |
| `accounting` | COA, jurnal, saldo |
| `enterprise` | Cabang, konfigurasi organisasi |
| `fund` | Program penghimpunan, donatur |
| `program` | Program penyaluran |
| `personalia` | Karyawan, aset tetap |
| `otorisasi` | Submission, workflow approval |
| `dwh` | Data warehouse views (HANYA views, tidak ada tabel) |

---

## Portal Isolation

```sql
-- Migration yang sama untuk dua portal → apply dua kali:
-- psql -d mziss_laz  -f V043__...sql
-- psql -d mziss_wakaf -f V043__...sql

-- DWH view untuk zakat saja → file berbeda:
-- dwh/v_arus_kas_zakat.sql (COA zakat, 31 balancesum items)
-- dwh/v_arus_kas_wakaf.sql (COA wakaf, 6 balancesum items — BERBEDA!)
```

Jangan assume konfigurasi COA/balancesum sama antara zakat dan wakaf.

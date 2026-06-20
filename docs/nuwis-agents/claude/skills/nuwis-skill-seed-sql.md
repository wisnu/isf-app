# Skill: nuwis-skill-seed-sql
## Pola Seed SQL untuk Menu & Role di isf-app

---

## Naming Convention — Bahasa Inggris (WAJIB)

- **menu_key**: English dotted → `finance.transactions.fund_collection`. JANGAN `keuangan.penghimpunan`.
- **route_path**: English kebab-case, cocok dengan Vue Router → `/finance/transactions/fund-collection`.
- **entity_type** (di `otorisasi.entity_config`): pakai nilai yang **sudah ada/disepakati** (`penghimpunan`, `penyaluran`, `budget_owner`, …) — ini kode BEKU, harus identik dengan key dispatcher di `authorization/service.py:_register_defaults()` dan literal di frontend. Jangan terjemahkan.
- **`id_peran`**: nama kolom DB asli di `isf_auth.role_menu` (BUKAN `role_code`) — pakai apa adanya.
- **label** menu: Bahasa Indonesia (teks UI) — mis. `'Penerimaan Amil'`.

> 3-way consistency wajib: `menu_key` di registry.ts ↔ route `meta.menu_key` ↔ seed SQL ini.
> Glossary: `docs/todos/2026-06-20-002-refactor-naming-english/glossary.md`

---

## Database Target

| Portal | Database | Schema |
|---|---|---|
| Zakat | `isf_auth_zakat` | `isf_auth` |
| Wakaf | `isf_auth_wakaf` | `isf_auth` |

---

## Tabel yang Relevan

```sql
isf_auth.menu          -- menu registry: semua menu items
isf_auth.role_menu     -- permission: role → menu mapping
isf_auth.users         -- user registry
isf_auth.user_credentials -- password hash
isf_auth.tenants
isf_auth.tenant_memberships
```

---

## Template Menu Seed Lengkap

```sql
-- Seed: {feature-slug}-seed.sql
-- Portal: {zakat | wakaf | keduanya}
-- Dibuat: {tanggal}
-- Fitur: {nama fitur}

-- ── 1. Menu entries ──────────────────────────────────────────────────────────

-- Parent groups (skip jika sudah ada):
INSERT INTO isf_auth.menu (menu_key, label, parent_key, sort_order, icon, path, is_group)
VALUES
  -- Level 1 group (contoh — skip jika sudah ada):
  -- ('keuangan', 'Keuangan', NULL, 10, 'wallet', NULL, TRUE),

  -- Level 2 group (contoh — skip jika sudah ada):
  -- ('keuangan.transaksi', 'Transaksi', 'keuangan', 20, NULL, NULL, TRUE),

  -- Level 3 item (yang baru):
  ('{menu_key}', '{Label UI}', '{parent_menu_key}', {sort_order}, '{icon}', '/{route-path}', FALSE)

ON CONFLICT (menu_key) DO UPDATE SET
  label      = EXCLUDED.label,
  parent_key = EXCLUDED.parent_key,
  sort_order = EXCLUDED.sort_order,
  icon       = EXCLUDED.icon,
  path       = EXCLUDED.path;


-- ── 2. Role assignments ──────────────────────────────────────────────────────
-- Kolom di isf_auth.role_menu: id_peran (BUKAN role_code), menu_key
-- PK: (id_peran, menu_key)

INSERT INTO isf_auth.role_menu (id_peran, menu_key)
VALUES
  ('{ROLE1}', '{menu_key}'),
  ('{ROLE2}', '{menu_key}')
  -- Tambah semua role yang harus punya akses

ON CONFLICT (id_peran, menu_key) DO NOTHING;
```

---

## Parent Menu yang Sudah Ada (jangan duplikasi)

Cek dengan: `psql -d isf_auth_zakat -c "SELECT menu_key, label FROM isf_auth.menu WHERE parent_key IS NULL OR is_group = TRUE ORDER BY sort_order;"`

Yang umumnya sudah ada:

| menu_key | Label | Sort |
|---|---|---|
| `dashboard` | Dashboard | 1 |
| `keuangan` | Keuangan | 10 |
| `keuangan.master` | Master Data | 11 |
| `keuangan.transaksi` | Transaksi | 12 |
| `keuangan.monitoring` | Monitoring | 13 |
| `keuangan.laporan` | Laporan | 14 |
| `admin` | Admin | 90 |
| `admin.users` | Manajemen User | 91 |

---

## Format Menu Key

```
{domain}.{sub-domain}.{action}

Level 1: {domain}                    → keuangan, admin, dashboard
Level 2: {domain}.{sub}              → keuangan.transaksi, keuangan.laporan
Level 3: {domain}.{sub}.{fitur}      → keuangan.transaksi.penghimpunan
Level 4: {domain}.{sub}.{fitur}.{op} → keuangan.transaksi.penghimpunan.tambah

Untuk button-level permission (tambah/edit/hapus), buat menu_key level 4.
Tidak perlu path untuk level 4 — isi NULL.
```

---

## Template: Dev User

```sql
-- Dev user untuk testing (password: test1234)
-- Ganti hash dengan bcrypt dari 'test1234':
-- python3 -c "import bcrypt; print(bcrypt.hashpw(b'test1234', bcrypt.gensalt()).decode())"

INSERT INTO isf_auth.users (username, email, full_name, is_active)
VALUES ('{USERNAME}', '{email@domain.com}', '{Nama Lengkap}', TRUE)
ON CONFLICT (username) DO NOTHING;

INSERT INTO isf_auth.user_credentials (user_id, credential_hash)
SELECT id, '$2b$12$HASH_DARI_BCRYPT_DI_SINI'
FROM isf_auth.users WHERE username = '{USERNAME}'
ON CONFLICT (user_id) DO UPDATE SET
  credential_hash = EXCLUDED.credential_hash;
```

Dev users yang sudah ada (password `test1234`):
- `HADI` — role DIST/SPVDIST, branch_access=all
- `RAIS` — role ACC/KEU, single-branch 001

---

## 3-Way Consistency Check

Sebelum apply seed, verifikasi ketiganya cocok:

```
1. lib/menu/registry.ts:
   MENU_KEYS.keuangan.transaksi.penghimpunan = 'keuangan.transaksi.penghimpunan'

2. router/index.ts:
   { meta: { menu_key: 'keuangan.transaksi.penghimpunan' } }

3. seed SQL:
   INSERT INTO isf_auth.menu VALUES ('keuangan.transaksi.penghimpunan', ...)
```

Jika ada ketidakcocokan, laporkan sebelum apply.

---

## Cara Apply

**WAJIB pakai `-h localhost`** — peer auth di Unix socket akan gagal dengan "Peer authentication failed".

```bash
# Zakat — menu seed:
PGPASSWORD=solusi psql -U transaction -h localhost -d isf_auth_zakat \
  -f infra/db/migrations/seed/{feature-slug}-seed.sql

# Wakaf — menu seed:
PGPASSWORD=solusi psql -U transaction -h localhost -d isf_auth_wakaf \
  -f infra/db/migrations/seed/{feature-slug}-seed.sql

# otorisasi.entity_config ada di BUSINESS DB (mziss_laz / mziss_wakaf), BUKAN auth DB:
PGPASSWORD=solusi psql -U transaction -h localhost -d mziss_laz \
  -f infra/db/migrations/seed/seed-entity-config-{slug}.sql

# Verifikasi menu + role:
PGPASSWORD=solusi psql -U transaction -h localhost -d isf_auth_zakat -c \
  "SELECT m.menu_key, m.label, rm.id_peran
   FROM isf_auth.menu m
   LEFT JOIN isf_auth.role_menu rm ON rm.menu_key = m.menu_key
   WHERE m.menu_key LIKE '{domain}.%'
   ORDER BY m.menu_key, rm.id_peran;"
```

**Penting**: menus[] di session di-populate saat login. User harus logout + login
setelah seed diapply agar menu baru muncul.

---

## Catatan Schema Kritis

| Tabel | Kolom PK / FK | Catatan |
|---|---|---|
| `isf_auth.role_menu` | `id_peran` (BUKAN `role_code`) | PK: `(id_peran, menu_key)` |
| `isf_auth.menu` | `menu_key` (PK) | FK dari role_menu |
| `otorisasi.entity_config` | `entity_type` (PK) | Ada di **mziss_laz/mziss_wakaf**, bukan auth DB |

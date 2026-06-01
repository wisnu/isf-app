-- Seed isf_auth.menu + isf_auth.role_menu untuk dev/test environment.
--
-- Konteks: seed scripts asli (reflog lines 51, 55, 76) hilang akibat NTFS
-- corruption 2026-05-27. File ini me-rebuild minimal viable seed berdasarkan
-- MENU_KEYS di apps_*/web-vue/src/lib/menu/registry.ts dan 14 role aktif di
-- enterprise.peran (mziss_laz / mziss_wakaf).
--
-- Strategi role_menu untuk dev: permissive — semua role aktif dapat semua menu.
-- Refinement per-role bisa via admin UI (/admin/role-menu) saat sudah live.
--
-- Idempotent: pakai ON CONFLICT DO NOTHING / DO UPDATE. Aman di-rerun.
--
-- Apply:
--   psql -U postgres -d isf_auth_zakat -f seed-menu-and-rolemenu.sql
--   psql -U postgres -d isf_auth_wakaf -f seed-menu-and-rolemenu.sql

BEGIN;

-- ── 1. isf_auth.menu — 9 keys dari MENU_KEYS registry ────────────────────────

INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status) VALUES
  ('dashboard.overview',     'Overview',                'Dashboard', '/',                       10, 'A'),
  ('dashboard.keuangan',     'Dashboard Keuangan',      'Dashboard', '/dashboard/keuangan',     20, 'A'),
  ('dashboard.penyaluran',   'Dashboard Penyaluran',    'Dashboard', '/dashboard/penyaluran',   30, 'A'),
  ('dashboard.penghimpunan', 'Dashboard Penghimpunan',  'Dashboard', '/dashboard/penghimpunan', 40, 'A'),
  ('keuangan.coa',           'Chart of Accounts',       'Keuangan',  '/keuangan/coa',          110, 'A'),
  ('keuangan.kas',           'Manajemen Kas',           'Keuangan',  '/keuangan/kas',          120, 'A'),
  ('keuangan.bank',          'Manajemen Bank',          'Keuangan',  '/keuangan/bank',         130, 'A'),
  ('keuangan.report.journal_daily', 'Laporan Jurnal Harian', 'Keuangan', '/keuangan/laporan/jurnal-harian', 140, 'A'),
  ('keuangan.report.general_transaction', 'List Transaksi Umum', 'Keuangan', '/keuangan/laporan/transaksi-umum', 141, 'A'),
  ('keuangan.report.cash_daily', 'Transaksi Kas/Bank Harian', 'Keuangan', '/keuangan/laporan/kas-harian', 142, 'A'),
  ('admin.role_menu',        'Role ↔ Menu Mapping',     'Admin',     '/admin/role-menu',       910, 'A'),
  ('admin.users',            'User Management',         'Admin',     '/admin/users',           920, 'A')
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  sort_order  = EXCLUDED.sort_order,
  status      = EXCLUDED.status,
  updated_at  = NOW();


-- ── 2. isf_auth.role_menu — permissive dev seed ──────────────────────────────
-- NOTE: 14 active roles berasal dari enterprise.peran di DB legacy (mziss_*).
-- DB isf_auth_<portal> sengaja terpisah, jadi list role di hard-code di sini.
-- Refresh manual lewat admin UI saat ada perubahan peran.

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by) VALUES
  -- ADM: full access
  ('ADM',     'dashboard.overview',     'seed'),
  ('ADM',     'dashboard.keuangan',     'seed'),
  ('ADM',     'dashboard.penyaluran',   'seed'),
  ('ADM',     'dashboard.penghimpunan', 'seed'),
  ('ADM',     'keuangan.coa',           'seed'),
  ('ADM',     'keuangan.kas',           'seed'),
  ('ADM',     'keuangan.bank',          'seed'),
  ('ADM',     'admin.role_menu',        'seed'),
  ('ADM',     'admin.users',            'seed'),
  -- SPVADM: admin minus user mgmt
  ('SPVADM',  'dashboard.overview',     'seed'),
  ('SPVADM',  'dashboard.keuangan',     'seed'),
  ('SPVADM',  'dashboard.penyaluran',   'seed'),
  ('SPVADM',  'dashboard.penghimpunan', 'seed'),
  ('SPVADM',  'keuangan.coa',           'seed'),
  ('SPVADM',  'keuangan.kas',           'seed'),
  ('SPVADM',  'keuangan.bank',          'seed'),
  ('SPVADM',  'admin.role_menu',        'seed'),
  -- KEU / SPVKEU / ACC / SPVACC: keuangan
  ('KEU',     'dashboard.overview',     'seed'),
  ('KEU',     'dashboard.keuangan',     'seed'),
  ('KEU',     'keuangan.coa',           'seed'),
  ('KEU',     'keuangan.kas',           'seed'),
  ('KEU',     'keuangan.bank',          'seed'),
  ('SPVKEU',  'dashboard.overview',     'seed'),
  ('SPVKEU',  'dashboard.keuangan',     'seed'),
  ('SPVKEU',  'keuangan.coa',           'seed'),
  ('SPVKEU',  'keuangan.kas',           'seed'),
  ('SPVKEU',  'keuangan.bank',          'seed'),
  ('ACC',     'dashboard.overview',     'seed'),
  ('ACC',     'dashboard.keuangan',     'seed'),
  ('ACC',     'keuangan.coa',           'seed'),
  ('SPVACC',  'dashboard.overview',     'seed'),
  ('SPVACC',  'dashboard.keuangan',     'seed'),
  ('SPVACC',  'keuangan.coa',           'seed'),
  -- Laporan Jurnal Harian (keuangan report). Finance roles + DIST/SPVDIST
  -- (DIST/SPVDIST diikutkan untuk E2E dev — user uji HADI; seed ini permissive-dev).
  ('ADM',     'keuangan.report.journal_daily', 'seed'),
  ('SPVADM',  'keuangan.report.journal_daily', 'seed'),
  ('KEU',     'keuangan.report.journal_daily', 'seed'),
  ('SPVKEU',  'keuangan.report.journal_daily', 'seed'),
  ('ACC',     'keuangan.report.journal_daily', 'seed'),
  ('SPVACC',  'keuangan.report.journal_daily', 'seed'),
  ('DIST',    'keuangan.report.journal_daily', 'seed'),
  ('SPVDIST', 'keuangan.report.journal_daily', 'seed'),
  ('ADM',     'keuangan.report.general_transaction', 'seed'),
  ('SPVADM',  'keuangan.report.general_transaction', 'seed'),
  ('KEU',     'keuangan.report.general_transaction', 'seed'),
  ('SPVKEU',  'keuangan.report.general_transaction', 'seed'),
  ('ACC',     'keuangan.report.general_transaction', 'seed'),
  ('SPVACC',  'keuangan.report.general_transaction', 'seed'),
  ('DIST',    'keuangan.report.general_transaction', 'seed'),
  ('SPVDIST', 'keuangan.report.general_transaction', 'seed'),
  -- Transaksi Kas/Bank Harian — AllowedGroups legacy TR0027: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.cash_daily', 'seed'),
  ('KEU',     'keuangan.report.cash_daily', 'seed'),
  ('ACC',     'keuangan.report.cash_daily', 'seed'),
  ('SPVKEU',  'keuangan.report.cash_daily', 'seed'),
  ('QAC',     'keuangan.report.cash_daily', 'seed'),
  ('SPVACC',  'keuangan.report.cash_daily', 'seed'),
  -- PHP / SPVPHP: penghimpunan
  ('PHP',     'dashboard.overview',     'seed'),
  ('PHP',     'dashboard.penghimpunan', 'seed'),
  ('SPVPHP',  'dashboard.overview',     'seed'),
  ('SPVPHP',  'dashboard.penghimpunan', 'seed'),
  -- DIST / SPVDIST: penyaluran
  ('DIST',    'dashboard.overview',     'seed'),
  ('DIST',    'dashboard.penyaluran',   'seed'),
  ('SPVDIST', 'dashboard.overview',     'seed'),
  ('SPVDIST', 'dashboard.penyaluran',   'seed'),
  -- GA / SPVGA / QAC: dashboard only
  ('GA',      'dashboard.overview',     'seed'),
  ('SPVGA',   'dashboard.overview',     'seed'),
  ('QAC',     'dashboard.overview',     'seed'),
  -- MIGRASI: tooling, no UI menu
  ('MIGRASI', 'dashboard.overview',     'seed')
ON CONFLICT (id_peran, menu_key) DO NOTHING;

COMMIT;

-- Verify
SELECT 'menu' AS table_name, COUNT(*) AS rows FROM isf_auth.menu
UNION ALL
SELECT 'role_menu', COUNT(*) FROM isf_auth.role_menu
UNION ALL
SELECT 'distinct id_peran', COUNT(DISTINCT id_peran) FROM isf_auth.role_menu;

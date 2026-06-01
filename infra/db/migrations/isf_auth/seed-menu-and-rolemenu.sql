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
  ('keuangan.report.cash_daily', 'Transaksi Kas/Bank Harian', 'Keuangan', '/keuangan/laporan/kas-harian', 140, 'A'),
  ('keuangan.report.cash_summary', 'Rekapitulasi Transaksi Kas/Bank', 'Keuangan', '/keuangan/laporan/rekap-kas', 141, 'A'),
  ('keuangan.report.cash_monthly', 'Monitoring Saldo Kas/Bank Bulanan', 'Keuangan', '/keuangan/laporan/saldo-bulanan', 142, 'A'),
  ('keuangan.report.journal_daily', 'Laporan Jurnal Harian', 'Keuangan', '/keuangan/laporan/jurnal-harian', 143, 'A'),
  ('keuangan.report.general_transaction', 'List Transaksi Umum', 'Keuangan', '/keuangan/laporan/transaksi-umum', 144, 'A'),
  ('keuangan.report.trial_balance', 'Trial Balance', 'Keuangan', '/keuangan/laporan/trial-balance', 150, 'A'),
  ('keuangan.report.neraca', 'Neraca', 'Keuangan', '/keuangan/laporan/neraca', 151, 'A'),
  ('keuangan.report.cash_flow', 'Arus Kas', 'Keuangan', '/keuangan/laporan/arus-kas', 152, 'A'),
  ('keuangan.report.general_ledger', 'Buku Besar', 'Keuangan', '/keuangan/laporan/buku-besar', 153, 'A'),
  ('keuangan.report.fund_changes', 'Perubahan Dana', 'Keuangan', '/keuangan/laporan/perubahan-dana', 154, 'A'),
  ('keuangan.report.fund_changes_detail', 'Perubahan Dana Detail', 'Keuangan', '/keuangan/laporan/perubahan-dana-detail', 155, 'A'),
  ('keuangan.report.amil_in', 'Penerimaan Amil', 'Keuangan', '/keuangan/laporan/penerimaan-amil', 160, 'A'),
  ('keuangan.report.amil_out', 'Pengeluaran Amil', 'Keuangan', '/keuangan/laporan/pengeluaran-amil', 161, 'A'),
  ('keuangan.report.distribution', 'Penyaluran Dana', 'Keuangan', '/keuangan/laporan/penyaluran-dana', 131, 'A'),
  ('keuangan.report.collection', 'Penghimpunan Dana', 'Keuangan', '/keuangan/laporan/penghimpunan-dana', 130, 'A'),
  ('keuangan.report.ar_employee', 'Piutang pada Karyawan', 'Keuangan', '/keuangan/laporan/piutang-karyawan', 170, 'A'),
  ('keuangan.report.ar_external', 'Piutang pada Non-Karyawan', 'Keuangan', '/keuangan/laporan/piutang-non-karyawan', 171, 'A'),
  ('keuangan.report.ca_employee', 'Rekapitulasi Uang Muka Kegiatan', 'Keuangan', '/keuangan/laporan/uang-muka-kegiatan', 172, 'A'),
  ('keuangan.report.ca_list', 'List Transaksi Uang Muka Kegiatan', 'Keuangan', '/keuangan/laporan/list-uang-muka', 173, 'A'),
  ('keuangan.report.project_memo', 'Laporan Realisasi Project (Memo)', 'Keuangan', '/keuangan/laporan/realisasi-memo', 174, 'A'),
  ('keuangan.report.program_ar', 'Piutang Realisasi Penyaluran', 'Keuangan', '/keuangan/laporan/piutang-realisasi', 175, 'A'),
  ('keuangan.report.upz', 'List Transaksi UPZ', 'Keuangan', '/keuangan/laporan/upz', 180, 'A'),
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
  -- Rekapitulasi Transaksi Kas/Bank — AllowedGroups legacy TR0028 (sama)
  ('ADM',     'keuangan.report.cash_summary', 'seed'),
  ('KEU',     'keuangan.report.cash_summary', 'seed'),
  ('ACC',     'keuangan.report.cash_summary', 'seed'),
  ('SPVKEU',  'keuangan.report.cash_summary', 'seed'),
  ('QAC',     'keuangan.report.cash_summary', 'seed'),
  ('SPVACC',  'keuangan.report.cash_summary', 'seed'),
  -- Monitoring Saldo Kas/Bank Bulanan — AllowedGroups legacy TR0028A (sama)
  ('ADM',     'keuangan.report.cash_monthly', 'seed'),
  ('KEU',     'keuangan.report.cash_monthly', 'seed'),
  ('ACC',     'keuangan.report.cash_monthly', 'seed'),
  ('SPVKEU',  'keuangan.report.cash_monthly', 'seed'),
  ('QAC',     'keuangan.report.cash_monthly', 'seed'),
  ('SPVACC',  'keuangan.report.cash_monthly', 'seed'),
  -- Trial Balance — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.trial_balance', 'seed'),
  ('KEU',     'keuangan.report.trial_balance', 'seed'),
  ('ACC',     'keuangan.report.trial_balance', 'seed'),
  ('SPVKEU',  'keuangan.report.trial_balance', 'seed'),
  ('QAC',     'keuangan.report.trial_balance', 'seed'),
  ('SPVACC',  'keuangan.report.trial_balance', 'seed'),
  -- Neraca — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.neraca', 'seed'),
  ('KEU',     'keuangan.report.neraca', 'seed'),
  ('ACC',     'keuangan.report.neraca', 'seed'),
  ('SPVKEU',  'keuangan.report.neraca', 'seed'),
  ('QAC',     'keuangan.report.neraca', 'seed'),
  ('SPVACC',  'keuangan.report.neraca', 'seed'),
  -- Arus Kas — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.cash_flow', 'seed'),
  ('KEU',     'keuangan.report.cash_flow', 'seed'),
  ('ACC',     'keuangan.report.cash_flow', 'seed'),
  ('SPVKEU',  'keuangan.report.cash_flow', 'seed'),
  ('QAC',     'keuangan.report.cash_flow', 'seed'),
  ('SPVACC',  'keuangan.report.cash_flow', 'seed'),
  -- Buku Besar — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.general_ledger', 'seed'),
  ('KEU',     'keuangan.report.general_ledger', 'seed'),
  ('ACC',     'keuangan.report.general_ledger', 'seed'),
  ('SPVKEU',  'keuangan.report.general_ledger', 'seed'),
  ('QAC',     'keuangan.report.general_ledger', 'seed'),
  ('SPVACC',  'keuangan.report.general_ledger', 'seed'),
  -- Perubahan Dana — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.fund_changes', 'seed'),
  ('KEU',     'keuangan.report.fund_changes', 'seed'),
  ('ACC',     'keuangan.report.fund_changes', 'seed'),
  ('SPVKEU',  'keuangan.report.fund_changes', 'seed'),
  ('QAC',     'keuangan.report.fund_changes', 'seed'),
  ('SPVACC',  'keuangan.report.fund_changes', 'seed'),
  -- Perubahan Dana Detail — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.fund_changes_detail', 'seed'),
  ('KEU',     'keuangan.report.fund_changes_detail', 'seed'),
  ('ACC',     'keuangan.report.fund_changes_detail', 'seed'),
  ('SPVKEU',  'keuangan.report.fund_changes_detail', 'seed'),
  ('QAC',     'keuangan.report.fund_changes_detail', 'seed'),
  ('SPVACC',  'keuangan.report.fund_changes_detail', 'seed'),
  -- Penerimaan Amil / Pengeluaran Amil — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.amil_in', 'seed'),
  ('KEU',     'keuangan.report.amil_in', 'seed'),
  ('ACC',     'keuangan.report.amil_in', 'seed'),
  ('SPVKEU',  'keuangan.report.amil_in', 'seed'),
  ('QAC',     'keuangan.report.amil_in', 'seed'),
  ('SPVACC',  'keuangan.report.amil_in', 'seed'),
  ('ADM',     'keuangan.report.amil_out', 'seed'),
  ('KEU',     'keuangan.report.amil_out', 'seed'),
  ('ACC',     'keuangan.report.amil_out', 'seed'),
  ('SPVKEU',  'keuangan.report.amil_out', 'seed'),
  ('QAC',     'keuangan.report.amil_out', 'seed'),
  ('SPVACC',  'keuangan.report.amil_out', 'seed'),
  -- Penyaluran Dana — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.distribution', 'seed'),
  ('KEU',     'keuangan.report.distribution', 'seed'),
  ('ACC',     'keuangan.report.distribution', 'seed'),
  ('SPVKEU',  'keuangan.report.distribution', 'seed'),
  ('QAC',     'keuangan.report.distribution', 'seed'),
  ('SPVACC',  'keuangan.report.distribution', 'seed'),
  -- Penghimpunan Dana — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'keuangan.report.collection', 'seed'),
  ('KEU',     'keuangan.report.collection', 'seed'),
  ('ACC',     'keuangan.report.collection', 'seed'),
  ('SPVKEU',  'keuangan.report.collection', 'seed'),
  ('QAC',     'keuangan.report.collection', 'seed'),
  ('SPVACC',  'keuangan.report.collection', 'seed'),
  -- Piutang Karyawan / Non-Karyawan / Rekap Uang Muka — AllowedGroups: ADM;SPVKEU;ACC;KEU;QAC;SPVACC
  ('ADM',     'keuangan.report.ar_employee', 'seed'),
  ('KEU',     'keuangan.report.ar_employee', 'seed'),
  ('ACC',     'keuangan.report.ar_employee', 'seed'),
  ('SPVKEU',  'keuangan.report.ar_employee', 'seed'),
  ('QAC',     'keuangan.report.ar_employee', 'seed'),
  ('SPVACC',  'keuangan.report.ar_employee', 'seed'),
  ('ADM',     'keuangan.report.ar_external', 'seed'),
  ('KEU',     'keuangan.report.ar_external', 'seed'),
  ('ACC',     'keuangan.report.ar_external', 'seed'),
  ('SPVKEU',  'keuangan.report.ar_external', 'seed'),
  ('QAC',     'keuangan.report.ar_external', 'seed'),
  ('SPVACC',  'keuangan.report.ar_external', 'seed'),
  ('ADM',     'keuangan.report.ca_employee', 'seed'),
  ('KEU',     'keuangan.report.ca_employee', 'seed'),
  ('ACC',     'keuangan.report.ca_employee', 'seed'),
  ('SPVKEU',  'keuangan.report.ca_employee', 'seed'),
  ('QAC',     'keuangan.report.ca_employee', 'seed'),
  ('SPVACC',  'keuangan.report.ca_employee', 'seed'),
  -- Grup C: List Uang Muka / Realisasi Memo / Piutang Realisasi — ADM;SPVKEU;ACC;KEU;QAC;SPVACC
  ('ADM',     'keuangan.report.ca_list', 'seed'),
  ('KEU',     'keuangan.report.ca_list', 'seed'),
  ('ACC',     'keuangan.report.ca_list', 'seed'),
  ('SPVKEU',  'keuangan.report.ca_list', 'seed'),
  ('QAC',     'keuangan.report.ca_list', 'seed'),
  ('SPVACC',  'keuangan.report.ca_list', 'seed'),
  ('ADM',     'keuangan.report.project_memo', 'seed'),
  ('KEU',     'keuangan.report.project_memo', 'seed'),
  ('ACC',     'keuangan.report.project_memo', 'seed'),
  ('SPVKEU',  'keuangan.report.project_memo', 'seed'),
  ('QAC',     'keuangan.report.project_memo', 'seed'),
  ('SPVACC',  'keuangan.report.project_memo', 'seed'),
  ('ADM',     'keuangan.report.program_ar', 'seed'),
  ('KEU',     'keuangan.report.program_ar', 'seed'),
  ('ACC',     'keuangan.report.program_ar', 'seed'),
  ('SPVKEU',  'keuangan.report.program_ar', 'seed'),
  ('QAC',     'keuangan.report.program_ar', 'seed'),
  ('SPVACC',  'keuangan.report.program_ar', 'seed'),
  ('ADM',     'keuangan.report.upz', 'seed'),
  ('KEU',     'keuangan.report.upz', 'seed'),
  ('ACC',     'keuangan.report.upz', 'seed'),
  ('SPVKEU',  'keuangan.report.upz', 'seed'),
  ('QAC',     'keuangan.report.upz', 'seed'),
  ('SPVACC',  'keuangan.report.upz', 'seed'),
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

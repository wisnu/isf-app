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
  ('dashboard.finance',     'Dashboard Keuangan',      'Dashboard', '/dashboard/finance',     20, 'A'),
  ('dashboard.distribution',   'Dashboard Penyaluran',    'Dashboard', '/dashboard/distribution',   30, 'A'),
  ('dashboard.collection', 'Dashboard Penghimpunan',  'Dashboard', '/dashboard/collection', 40, 'A'),
  ('finance.coa',           'Chart of Accounts',       'Keuangan',  '/finance/coa',          110, 'A'),
  ('finance.cash',           'Manajemen Kas',           'Keuangan',  '/finance/cash',          120, 'A'),
  ('finance.bank',          'Manajemen Bank',          'Keuangan',  '/finance/bank',         130, 'A'),
  ('finance.reports.daily_cash', 'Transaksi Kas/Bank Harian', 'Keuangan', '/finance/reports/daily-cash', 140, 'A'),
  ('finance.reports.cash_summary', 'Rekapitulasi Transaksi Kas/Bank', 'Keuangan', '/finance/reports/cash-summary', 141, 'A'),
  ('finance.reports.monthly_balance', 'Monitoring Saldo Kas/Bank Bulanan', 'Keuangan', '/finance/reports/monthly-balance', 142, 'A'),
  ('finance.reports.daily_journal', 'Laporan Jurnal Harian', 'Keuangan', '/finance/reports/daily-journal', 143, 'A'),
  ('finance.reports.general_transaction', 'List Transaksi Umum', 'Keuangan', '/finance/reports/general-transaction', 144, 'A'),
  ('finance.reports.trial_balance', 'Trial Balance', 'Keuangan', '/finance/reports/trial-balance', 150, 'A'),
  ('finance.reports.balance_sheet', 'Neraca', 'Keuangan', '/finance/reports/balance-sheet', 151, 'A'),
  ('finance.reports.cash_flow', 'Arus Kas', 'Keuangan', '/finance/reports/cash-flow', 152, 'A'),
  ('finance.reports.general_ledger', 'Buku Besar', 'Keuangan', '/finance/reports/general-ledger', 153, 'A'),
  ('finance.reports.fund_changes', 'Perubahan Dana', 'Keuangan', '/finance/reports/fund-changes', 154, 'A'),
  ('finance.reports.fund_changes_detail', 'Perubahan Dana Detail', 'Keuangan', '/finance/reports/fund-changes-detail', 155, 'A'),
  ('finance.reports.amil_receipt', 'Penerimaan Amil', 'Keuangan', '/finance/reports/amil-receipt', 160, 'A'),
  ('finance.reports.amil_expense', 'Pengeluaran Amil', 'Keuangan', '/finance/reports/amil-expense', 161, 'A'),
  ('finance.reports.fund_distribution', 'Penyaluran Dana', 'Keuangan', '/finance/reports/fund-distribution', 131, 'A'),
  ('finance.reports.fund_collection', 'Penghimpunan Dana', 'Keuangan', '/finance/reports/fund-collection', 130, 'A'),
  ('finance.reports.employee_receivable', 'Piutang pada Karyawan', 'Keuangan', '/finance/reports/employee-receivable', 170, 'A'),
  ('finance.reports.non_employee_receivable', 'Piutang pada Non-Karyawan', 'Keuangan', '/finance/reports/non-employee-receivable', 171, 'A'),
  ('finance.reports.activity_cash_advance', 'Rekapitulasi Uang Muka Kegiatan', 'Keuangan', '/finance/reports/activity-cash-advance', 172, 'A'),
  ('finance.reports.cash_advance_list', 'List Transaksi Uang Muka Kegiatan', 'Keuangan', '/finance/reports/cash-advance-list', 173, 'A'),
  ('finance.reports.memo_realization', 'Laporan Realisasi Project (Memo)', 'Keuangan', '/finance/reports/memo-realization', 174, 'A'),
  ('finance.reports.receivable_realization', 'Piutang Realisasi Penyaluran', 'Keuangan', '/finance/reports/receivable-realization', 175, 'A'),
  ('finance.reports.upz', 'List Transaksi UPZ', 'Keuangan', '/finance/reports/upz', 180, 'A'),
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
  ('ADM',     'dashboard.finance',     'seed'),
  ('ADM',     'dashboard.distribution',   'seed'),
  ('ADM',     'dashboard.collection', 'seed'),
  ('ADM',     'finance.coa',           'seed'),
  ('ADM',     'finance.cash',           'seed'),
  ('ADM',     'finance.bank',          'seed'),
  ('ADM',     'admin.role_menu',        'seed'),
  ('ADM',     'admin.users',            'seed'),
  -- SPVADM: admin minus user mgmt
  ('SPVADM',  'dashboard.overview',     'seed'),
  ('SPVADM',  'dashboard.finance',     'seed'),
  ('SPVADM',  'dashboard.distribution',   'seed'),
  ('SPVADM',  'dashboard.collection', 'seed'),
  ('SPVADM',  'finance.coa',           'seed'),
  ('SPVADM',  'finance.cash',           'seed'),
  ('SPVADM',  'finance.bank',          'seed'),
  ('SPVADM',  'admin.role_menu',        'seed'),
  -- KEU / SPVKEU / ACC / SPVACC: keuangan
  ('KEU',     'dashboard.overview',     'seed'),
  ('KEU',     'dashboard.finance',     'seed'),
  ('KEU',     'finance.coa',           'seed'),
  ('KEU',     'finance.cash',           'seed'),
  ('KEU',     'finance.bank',          'seed'),
  ('SPVKEU',  'dashboard.overview',     'seed'),
  ('SPVKEU',  'dashboard.finance',     'seed'),
  ('SPVKEU',  'finance.coa',           'seed'),
  ('SPVKEU',  'finance.cash',           'seed'),
  ('SPVKEU',  'finance.bank',          'seed'),
  ('ACC',     'dashboard.overview',     'seed'),
  ('ACC',     'dashboard.finance',     'seed'),
  ('ACC',     'finance.coa',           'seed'),
  ('SPVACC',  'dashboard.overview',     'seed'),
  ('SPVACC',  'dashboard.finance',     'seed'),
  ('SPVACC',  'finance.coa',           'seed'),
  -- Laporan Jurnal Harian (keuangan report). Finance roles + DIST/SPVDIST
  -- (DIST/SPVDIST diikutkan untuk E2E dev — user uji HADI; seed ini permissive-dev).
  ('ADM',     'finance.reports.daily_journal', 'seed'),
  ('SPVADM',  'finance.reports.daily_journal', 'seed'),
  ('KEU',     'finance.reports.daily_journal', 'seed'),
  ('SPVKEU',  'finance.reports.daily_journal', 'seed'),
  ('ACC',     'finance.reports.daily_journal', 'seed'),
  ('SPVACC',  'finance.reports.daily_journal', 'seed'),
  ('DIST',    'finance.reports.daily_journal', 'seed'),
  ('SPVDIST', 'finance.reports.daily_journal', 'seed'),
  ('ADM',     'finance.reports.general_transaction', 'seed'),
  ('SPVADM',  'finance.reports.general_transaction', 'seed'),
  ('KEU',     'finance.reports.general_transaction', 'seed'),
  ('SPVKEU',  'finance.reports.general_transaction', 'seed'),
  ('ACC',     'finance.reports.general_transaction', 'seed'),
  ('SPVACC',  'finance.reports.general_transaction', 'seed'),
  ('DIST',    'finance.reports.general_transaction', 'seed'),
  ('SPVDIST', 'finance.reports.general_transaction', 'seed'),
  -- Transaksi Kas/Bank Harian — AllowedGroups legacy TR0027: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.daily_cash', 'seed'),
  ('KEU',     'finance.reports.daily_cash', 'seed'),
  ('ACC',     'finance.reports.daily_cash', 'seed'),
  ('SPVKEU',  'finance.reports.daily_cash', 'seed'),
  ('QAC',     'finance.reports.daily_cash', 'seed'),
  ('SPVACC',  'finance.reports.daily_cash', 'seed'),
  -- Rekapitulasi Transaksi Kas/Bank — AllowedGroups legacy TR0028 (sama)
  ('ADM',     'finance.reports.cash_summary', 'seed'),
  ('KEU',     'finance.reports.cash_summary', 'seed'),
  ('ACC',     'finance.reports.cash_summary', 'seed'),
  ('SPVKEU',  'finance.reports.cash_summary', 'seed'),
  ('QAC',     'finance.reports.cash_summary', 'seed'),
  ('SPVACC',  'finance.reports.cash_summary', 'seed'),
  -- Monitoring Saldo Kas/Bank Bulanan — AllowedGroups legacy TR0028A (sama)
  ('ADM',     'finance.reports.monthly_balance', 'seed'),
  ('KEU',     'finance.reports.monthly_balance', 'seed'),
  ('ACC',     'finance.reports.monthly_balance', 'seed'),
  ('SPVKEU',  'finance.reports.monthly_balance', 'seed'),
  ('QAC',     'finance.reports.monthly_balance', 'seed'),
  ('SPVACC',  'finance.reports.monthly_balance', 'seed'),
  -- Trial Balance — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.trial_balance', 'seed'),
  ('KEU',     'finance.reports.trial_balance', 'seed'),
  ('ACC',     'finance.reports.trial_balance', 'seed'),
  ('SPVKEU',  'finance.reports.trial_balance', 'seed'),
  ('QAC',     'finance.reports.trial_balance', 'seed'),
  ('SPVACC',  'finance.reports.trial_balance', 'seed'),
  -- Neraca — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.balance_sheet', 'seed'),
  ('KEU',     'finance.reports.balance_sheet', 'seed'),
  ('ACC',     'finance.reports.balance_sheet', 'seed'),
  ('SPVKEU',  'finance.reports.balance_sheet', 'seed'),
  ('QAC',     'finance.reports.balance_sheet', 'seed'),
  ('SPVACC',  'finance.reports.balance_sheet', 'seed'),
  -- Arus Kas — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.cash_flow', 'seed'),
  ('KEU',     'finance.reports.cash_flow', 'seed'),
  ('ACC',     'finance.reports.cash_flow', 'seed'),
  ('SPVKEU',  'finance.reports.cash_flow', 'seed'),
  ('QAC',     'finance.reports.cash_flow', 'seed'),
  ('SPVACC',  'finance.reports.cash_flow', 'seed'),
  -- Buku Besar — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.general_ledger', 'seed'),
  ('KEU',     'finance.reports.general_ledger', 'seed'),
  ('ACC',     'finance.reports.general_ledger', 'seed'),
  ('SPVKEU',  'finance.reports.general_ledger', 'seed'),
  ('QAC',     'finance.reports.general_ledger', 'seed'),
  ('SPVACC',  'finance.reports.general_ledger', 'seed'),
  -- Perubahan Dana — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.fund_changes', 'seed'),
  ('KEU',     'finance.reports.fund_changes', 'seed'),
  ('ACC',     'finance.reports.fund_changes', 'seed'),
  ('SPVKEU',  'finance.reports.fund_changes', 'seed'),
  ('QAC',     'finance.reports.fund_changes', 'seed'),
  ('SPVACC',  'finance.reports.fund_changes', 'seed'),
  -- Perubahan Dana Detail — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.fund_changes_detail', 'seed'),
  ('KEU',     'finance.reports.fund_changes_detail', 'seed'),
  ('ACC',     'finance.reports.fund_changes_detail', 'seed'),
  ('SPVKEU',  'finance.reports.fund_changes_detail', 'seed'),
  ('QAC',     'finance.reports.fund_changes_detail', 'seed'),
  ('SPVACC',  'finance.reports.fund_changes_detail', 'seed'),
  -- Penerimaan Amil / Pengeluaran Amil — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.amil_receipt', 'seed'),
  ('KEU',     'finance.reports.amil_receipt', 'seed'),
  ('ACC',     'finance.reports.amil_receipt', 'seed'),
  ('SPVKEU',  'finance.reports.amil_receipt', 'seed'),
  ('QAC',     'finance.reports.amil_receipt', 'seed'),
  ('SPVACC',  'finance.reports.amil_receipt', 'seed'),
  ('ADM',     'finance.reports.amil_expense', 'seed'),
  ('KEU',     'finance.reports.amil_expense', 'seed'),
  ('ACC',     'finance.reports.amil_expense', 'seed'),
  ('SPVKEU',  'finance.reports.amil_expense', 'seed'),
  ('QAC',     'finance.reports.amil_expense', 'seed'),
  ('SPVACC',  'finance.reports.amil_expense', 'seed'),
  -- Penyaluran Dana — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.fund_distribution', 'seed'),
  ('KEU',     'finance.reports.fund_distribution', 'seed'),
  ('ACC',     'finance.reports.fund_distribution', 'seed'),
  ('SPVKEU',  'finance.reports.fund_distribution', 'seed'),
  ('QAC',     'finance.reports.fund_distribution', 'seed'),
  ('SPVACC',  'finance.reports.fund_distribution', 'seed'),
  -- Penghimpunan Dana — AllowedGroups: ADM;KEU;ACC;SPVKEU;QAC;SPVACC
  ('ADM',     'finance.reports.fund_collection', 'seed'),
  ('KEU',     'finance.reports.fund_collection', 'seed'),
  ('ACC',     'finance.reports.fund_collection', 'seed'),
  ('SPVKEU',  'finance.reports.fund_collection', 'seed'),
  ('QAC',     'finance.reports.fund_collection', 'seed'),
  ('SPVACC',  'finance.reports.fund_collection', 'seed'),
  -- Piutang Karyawan / Non-Karyawan / Rekap Uang Muka — AllowedGroups: ADM;SPVKEU;ACC;KEU;QAC;SPVACC
  ('ADM',     'finance.reports.employee_receivable', 'seed'),
  ('KEU',     'finance.reports.employee_receivable', 'seed'),
  ('ACC',     'finance.reports.employee_receivable', 'seed'),
  ('SPVKEU',  'finance.reports.employee_receivable', 'seed'),
  ('QAC',     'finance.reports.employee_receivable', 'seed'),
  ('SPVACC',  'finance.reports.employee_receivable', 'seed'),
  ('ADM',     'finance.reports.non_employee_receivable', 'seed'),
  ('KEU',     'finance.reports.non_employee_receivable', 'seed'),
  ('ACC',     'finance.reports.non_employee_receivable', 'seed'),
  ('SPVKEU',  'finance.reports.non_employee_receivable', 'seed'),
  ('QAC',     'finance.reports.non_employee_receivable', 'seed'),
  ('SPVACC',  'finance.reports.non_employee_receivable', 'seed'),
  ('ADM',     'finance.reports.activity_cash_advance', 'seed'),
  ('KEU',     'finance.reports.activity_cash_advance', 'seed'),
  ('ACC',     'finance.reports.activity_cash_advance', 'seed'),
  ('SPVKEU',  'finance.reports.activity_cash_advance', 'seed'),
  ('QAC',     'finance.reports.activity_cash_advance', 'seed'),
  ('SPVACC',  'finance.reports.activity_cash_advance', 'seed'),
  -- Grup C: List Uang Muka / Realisasi Memo / Piutang Realisasi — ADM;SPVKEU;ACC;KEU;QAC;SPVACC
  ('ADM',     'finance.reports.cash_advance_list', 'seed'),
  ('KEU',     'finance.reports.cash_advance_list', 'seed'),
  ('ACC',     'finance.reports.cash_advance_list', 'seed'),
  ('SPVKEU',  'finance.reports.cash_advance_list', 'seed'),
  ('QAC',     'finance.reports.cash_advance_list', 'seed'),
  ('SPVACC',  'finance.reports.cash_advance_list', 'seed'),
  ('ADM',     'finance.reports.memo_realization', 'seed'),
  ('KEU',     'finance.reports.memo_realization', 'seed'),
  ('ACC',     'finance.reports.memo_realization', 'seed'),
  ('SPVKEU',  'finance.reports.memo_realization', 'seed'),
  ('QAC',     'finance.reports.memo_realization', 'seed'),
  ('SPVACC',  'finance.reports.memo_realization', 'seed'),
  ('ADM',     'finance.reports.receivable_realization', 'seed'),
  ('KEU',     'finance.reports.receivable_realization', 'seed'),
  ('ACC',     'finance.reports.receivable_realization', 'seed'),
  ('SPVKEU',  'finance.reports.receivable_realization', 'seed'),
  ('QAC',     'finance.reports.receivable_realization', 'seed'),
  ('SPVACC',  'finance.reports.receivable_realization', 'seed'),
  ('ADM',     'finance.reports.upz', 'seed'),
  ('KEU',     'finance.reports.upz', 'seed'),
  ('ACC',     'finance.reports.upz', 'seed'),
  ('SPVKEU',  'finance.reports.upz', 'seed'),
  ('QAC',     'finance.reports.upz', 'seed'),
  ('SPVACC',  'finance.reports.upz', 'seed'),
  -- PHP / SPVPHP: penghimpunan
  ('PHP',     'dashboard.overview',     'seed'),
  ('PHP',     'dashboard.collection', 'seed'),
  ('SPVPHP',  'dashboard.overview',     'seed'),
  ('SPVPHP',  'dashboard.collection', 'seed'),
  -- DIST / SPVDIST: penyaluran
  ('DIST',    'dashboard.overview',     'seed'),
  ('DIST',    'dashboard.distribution',   'seed'),
  ('SPVDIST', 'dashboard.overview',     'seed'),
  ('SPVDIST', 'dashboard.distribution',   'seed'),
  -- GA / SPVGA / QAC: dashboard only
  ('GA',      'dashboard.overview',     'seed'),
  ('SPVGA',   'dashboard.overview',     'seed'),
  ('QAC',     'dashboard.overview',     'seed'),
  -- MIGRASI: tooling, no UI menu
  ('MIGRASI', 'dashboard.overview',     'seed')
ON CONFLICT (id_peran, menu_key) DO NOTHING;

COMMIT;

-- Upload Penghimpunan (2026-06-05)
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES
  ('finance.upload.collection',         'Upload Penghimpunan',           'Keuangan', '/finance/upload/collection',         190, 'A'),
  ('finance.upload.collection.approve',  'Otorisasi Upload Penghimpunan', 'Keuangan', '/finance/upload/collection/list', 191, 'A')
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  sort_order  = EXCLUDED.sort_order,
  status      = EXCLUDED.status,
  updated_at  = NOW();

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by) VALUES
  ('KEU',    'finance.upload.collection',         'seed'),
  ('SPVKEU', 'finance.upload.collection',         'seed'),
  ('SPVKEU', 'finance.upload.collection.approve', 'seed')
ON CONFLICT (id_peran, menu_key) DO NOTHING;

-- Histori Transaksi (2026-06-05)
INSERT INTO isf_auth.menu (menu_key, label, group_label, route_path, sort_order, status)
VALUES ('finance.transactions.history', 'Histori Transaksi', 'Keuangan', '/finance/transactions/history', 145, 'A')
ON CONFLICT (menu_key) DO UPDATE SET
  label       = EXCLUDED.label,
  group_label = EXCLUDED.group_label,
  route_path  = EXCLUDED.route_path,
  sort_order  = EXCLUDED.sort_order,
  status      = EXCLUDED.status,
  updated_at  = NOW();

INSERT INTO isf_auth.role_menu (id_peran, menu_key, created_by) VALUES
  ('ADM',    'finance.transactions.history', 'seed'),
  ('SPVADM', 'finance.transactions.history', 'seed'),
  ('KEU',    'finance.transactions.history', 'seed'),
  ('SPVKEU', 'finance.transactions.history', 'seed'),
  ('ACC',    'finance.transactions.history', 'seed'),
  ('SPVACC', 'finance.transactions.history', 'seed'),
  ('QAC',    'finance.transactions.history', 'seed')
ON CONFLICT (id_peran, menu_key) DO NOTHING;

-- Verify
SELECT 'menu' AS table_name, COUNT(*) AS rows FROM isf_auth.menu
UNION ALL
SELECT 'role_menu', COUNT(*) FROM isf_auth.role_menu
UNION ALL
SELECT 'distinct id_peran', COUNT(DISTINCT id_peran) FROM isf_auth.role_menu;

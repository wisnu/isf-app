-- Migration: rename menu_key values from Indonesian to English
-- Apply to: isf_auth_zakat AND isf_auth_wakaf
--
--   psql -U transaction -d isf_auth_zakat -f migrate-menu-keys-to-english.sql
--   psql -U transaction -d isf_auth_wakaf -f migrate-menu-keys-to-english.sql
--
-- Safe to re-run (WHERE clause is idempotent for old keys).

BEGIN;

-- Defer FK constraints so we can update both tables freely
SET CONSTRAINTS ALL DEFERRED;

-- ── 1. isf_auth.menu — update menu_key + route_path ─────────────────────────

UPDATE isf_auth.menu SET menu_key = 'dashboard.finance',     route_path = '/dashboard/finance'     WHERE menu_key = 'dashboard.keuangan';
UPDATE isf_auth.menu SET menu_key = 'dashboard.distribution', route_path = '/dashboard/distribution' WHERE menu_key = 'dashboard.penyaluran';
UPDATE isf_auth.menu SET menu_key = 'dashboard.collection',  route_path = '/dashboard/collection'  WHERE menu_key = 'dashboard.penghimpunan';

UPDATE isf_auth.menu SET menu_key = 'finance.coa',       route_path = '/finance/coa'       WHERE menu_key = 'keuangan.coa';
UPDATE isf_auth.menu SET menu_key = 'finance.cash',      route_path = '/finance/cash'      WHERE menu_key = 'keuangan.kas';
UPDATE isf_auth.menu SET menu_key = 'finance.bank',      route_path = '/finance/bank'      WHERE menu_key = 'keuangan.bank';
UPDATE isf_auth.menu SET menu_key = 'finance.petty_cash', route_path = '/finance/petty-cash' WHERE menu_key = 'keuangan.kas_kecil';

UPDATE isf_auth.menu SET menu_key = 'finance.budget.import',   route_path = '/finance/budget/import'   WHERE menu_key = 'keuangan.anggaran.import';
UPDATE isf_auth.menu SET menu_key = 'finance.budget.revise',   route_path = '/finance/budget/revise'   WHERE menu_key = 'keuangan.anggaran.revisi';
UPDATE isf_auth.menu SET menu_key = 'finance.budget.inquiry',  route_path = '/finance/budget/inquiry'  WHERE menu_key = 'keuangan.anggaran.inquiry';

UPDATE isf_auth.menu SET menu_key = 'finance.parameter.budget_owner',        route_path = '/parameter/budget-owner'         WHERE menu_key = 'keuangan.parameter.pemilik-anggaran';
UPDATE isf_auth.menu SET menu_key = 'finance.parameter.budget_owner.create', route_path = '/parameter/budget-owner'         WHERE menu_key = 'keuangan.parameter.pemilik-anggaran.tambah';
UPDATE isf_auth.menu SET menu_key = 'finance.parameter.budget_owner.edit',   route_path = '/parameter/budget-owner'         WHERE menu_key = 'keuangan.parameter.pemilik-anggaran.ubah';
UPDATE isf_auth.menu SET menu_key = 'finance.parameter.budget_owner.delete', route_path = '/parameter/budget-owner'         WHERE menu_key = 'keuangan.parameter.pemilik-anggaran.hapus';
UPDATE isf_auth.menu SET menu_key = 'finance.parameter.budget.owner',        route_path = '/parameter/budget-owner'         WHERE menu_key = 'keuangan.parameter.anggaran.pemilik';
UPDATE isf_auth.menu SET menu_key = 'finance.parameter.budget.item',         route_path = '/parameter/anggaran/item'        WHERE menu_key = 'keuangan.parameter.anggaran.item';
UPDATE isf_auth.menu SET menu_key = 'finance.parameter.budget.period',       route_path = '/parameter/anggaran/periode'     WHERE menu_key = 'keuangan.parameter.anggaran.periode';

UPDATE isf_auth.menu SET menu_key = 'finance.transactions.history',          route_path = '/finance/transactions/history'         WHERE menu_key = 'keuangan.transaksi.histori';
UPDATE isf_auth.menu SET menu_key = 'finance.transactions.fund_distribution', route_path = '/finance/transactions/fund-distribution' WHERE menu_key = 'keuangan.transaksi.penyaluran';
UPDATE isf_auth.menu SET menu_key = 'finance.transactions.fund_collection',  route_path = '/finance/transactions/fund-collection'  WHERE menu_key = 'keuangan.transaksi.penghimpunan';
UPDATE isf_auth.menu SET menu_key = 'finance.transactions.general',          route_path = '/finance/transactions/general'          WHERE menu_key = 'keuangan.transaksi.umum';
UPDATE isf_auth.menu SET menu_key = 'finance.receivable'                                                                       WHERE menu_key = 'keuangan.piutang';
UPDATE isf_auth.menu SET menu_key = 'finance.transactions.receivable',       route_path = '/finance/transactions/receivable'       WHERE menu_key = 'keuangan.piutang.pinjam-bayar';
UPDATE isf_auth.menu SET menu_key = 'finance.transactions.cash_advance',     route_path = '/finance/transactions/cash-advance'     WHERE menu_key = 'keuangan.transaksi.uang-muka-penyerahan';
UPDATE isf_auth.menu SET menu_key = 'finance.transactions.cash_advance_lpj', route_path = '/finance/transactions/cash-advance-lpj' WHERE menu_key = 'keuangan.transaksi.uang-muka-pengembalian';
UPDATE isf_auth.menu SET menu_key = 'finance.transactions.fund_transfer',    route_path = '/finance/transactions/fund-transfer'    WHERE menu_key = 'keuangan.transaksi.transfer-antar-rekening';

UPDATE isf_auth.menu SET menu_key = 'finance.monitoring'                                                               WHERE menu_key = 'keuangan.monitoring';
UPDATE isf_auth.menu SET menu_key = 'finance.monitoring.authorization', route_path = '/finance/monitoring/authorization' WHERE menu_key = 'keuangan.monitoring.otorisasi';
UPDATE isf_auth.menu SET menu_key = 'finance.monitoring.history',       route_path = '/finance/monitoring/history'       WHERE menu_key = 'keuangan.monitoring.riwayat';

UPDATE isf_auth.menu SET menu_key = 'finance.upload.collection',        route_path = '/finance/upload/collection'      WHERE menu_key = 'keuangan.upload.penghimpunan';
UPDATE isf_auth.menu SET menu_key = 'finance.upload.collection.approve', route_path = '/finance/upload/collection/list' WHERE menu_key = 'keuangan.upload.penghimpunan.approve';
UPDATE isf_auth.menu SET menu_key = 'finance.upload.zis_routine',       route_path = '/finance/upload/zis-routine'     WHERE menu_key = 'keuangan.upload.zis-rutin';
UPDATE isf_auth.menu SET menu_key = 'finance.upload.zis_routine_list',  route_path = '/finance/upload/zis-routine/list' WHERE menu_key = 'keuangan.upload.zis-rutin-list';

UPDATE isf_auth.menu SET menu_key = 'finance.reports.daily_journal',        route_path = '/finance/reports/daily-journal'        WHERE menu_key = 'keuangan.report.journal_daily';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.general_transaction',   route_path = '/finance/reports/general-transaction'   WHERE menu_key = 'keuangan.report.general_transaction';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.daily_cash',            route_path = '/finance/reports/daily-cash'            WHERE menu_key = 'keuangan.report.cash_daily';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.cash_summary',          route_path = '/finance/reports/cash-summary'          WHERE menu_key = 'keuangan.report.cash_summary';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.monthly_balance',       route_path = '/finance/reports/monthly-balance'       WHERE menu_key = 'keuangan.report.cash_monthly';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.trial_balance',         route_path = '/finance/reports/trial-balance'         WHERE menu_key = 'keuangan.report.trial_balance';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.balance_sheet',         route_path = '/finance/reports/balance-sheet'         WHERE menu_key = 'keuangan.report.neraca';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.cash_flow',             route_path = '/finance/reports/cash-flow'             WHERE menu_key = 'keuangan.report.cash_flow';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.general_ledger',        route_path = '/finance/reports/general-ledger'        WHERE menu_key = 'keuangan.report.general_ledger';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.fund_changes',          route_path = '/finance/reports/fund-changes'          WHERE menu_key = 'keuangan.report.fund_changes';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.fund_changes_detail',   route_path = '/finance/reports/fund-changes-detail'   WHERE menu_key = 'keuangan.report.fund_changes_detail';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.amil_receipt',          route_path = '/finance/reports/amil-receipt'          WHERE menu_key = 'keuangan.report.amil_in';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.amil_expense',          route_path = '/finance/reports/amil-expense'          WHERE menu_key = 'keuangan.report.amil_out';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.fund_distribution',     route_path = '/finance/reports/fund-distribution'     WHERE menu_key = 'keuangan.report.distribution';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.fund_collection',       route_path = '/finance/reports/fund-collection'       WHERE menu_key = 'keuangan.report.collection';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.employee_receivable',   route_path = '/finance/reports/employee-receivable'   WHERE menu_key = 'keuangan.report.ar_employee';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.non_employee_receivable', route_path = '/finance/reports/non-employee-receivable' WHERE menu_key = 'keuangan.report.ar_external';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.activity_cash_advance', route_path = '/finance/reports/activity-cash-advance' WHERE menu_key = 'keuangan.report.ca_employee';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.cash_advance_list',     route_path = '/finance/reports/cash-advance-list'     WHERE menu_key = 'keuangan.report.ca_list';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.memo_realization',      route_path = '/finance/reports/memo-realization'      WHERE menu_key = 'keuangan.report.project_memo';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.receivable_realization', route_path = '/finance/reports/receivable-realization' WHERE menu_key = 'keuangan.report.program_ar';
UPDATE isf_auth.menu SET menu_key = 'finance.reports.upz',                  route_path = '/finance/reports/upz'                  WHERE menu_key = 'keuangan.report.upz';

-- ── 2. isf_auth.role_menu — update menu_key references ──────────────────────

UPDATE isf_auth.role_menu SET menu_key = 'dashboard.finance'       WHERE menu_key = 'dashboard.keuangan';
UPDATE isf_auth.role_menu SET menu_key = 'dashboard.distribution'  WHERE menu_key = 'dashboard.penyaluran';
UPDATE isf_auth.role_menu SET menu_key = 'dashboard.collection'    WHERE menu_key = 'dashboard.penghimpunan';

UPDATE isf_auth.role_menu SET menu_key = 'finance.coa'        WHERE menu_key = 'keuangan.coa';
UPDATE isf_auth.role_menu SET menu_key = 'finance.cash'       WHERE menu_key = 'keuangan.kas';
UPDATE isf_auth.role_menu SET menu_key = 'finance.bank'       WHERE menu_key = 'keuangan.bank';
UPDATE isf_auth.role_menu SET menu_key = 'finance.petty_cash' WHERE menu_key = 'keuangan.kas_kecil';

UPDATE isf_auth.role_menu SET menu_key = 'finance.budget.import'   WHERE menu_key = 'keuangan.anggaran.import';
UPDATE isf_auth.role_menu SET menu_key = 'finance.budget.revise'   WHERE menu_key = 'keuangan.anggaran.revisi';
UPDATE isf_auth.role_menu SET menu_key = 'finance.budget.inquiry'  WHERE menu_key = 'keuangan.anggaran.inquiry';

UPDATE isf_auth.role_menu SET menu_key = 'finance.parameter.budget_owner'        WHERE menu_key = 'keuangan.parameter.pemilik-anggaran';
UPDATE isf_auth.role_menu SET menu_key = 'finance.parameter.budget_owner.create' WHERE menu_key = 'keuangan.parameter.pemilik-anggaran.tambah';
UPDATE isf_auth.role_menu SET menu_key = 'finance.parameter.budget_owner.edit'   WHERE menu_key = 'keuangan.parameter.pemilik-anggaran.ubah';
UPDATE isf_auth.role_menu SET menu_key = 'finance.parameter.budget_owner.delete' WHERE menu_key = 'keuangan.parameter.pemilik-anggaran.hapus';
UPDATE isf_auth.role_menu SET menu_key = 'finance.parameter.budget.owner'        WHERE menu_key = 'keuangan.parameter.anggaran.pemilik';
UPDATE isf_auth.role_menu SET menu_key = 'finance.parameter.budget.item'         WHERE menu_key = 'keuangan.parameter.anggaran.item';
UPDATE isf_auth.role_menu SET menu_key = 'finance.parameter.budget.period'       WHERE menu_key = 'keuangan.parameter.anggaran.periode';

UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.history'           WHERE menu_key = 'keuangan.transaksi.histori';
UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.fund_distribution' WHERE menu_key = 'keuangan.transaksi.penyaluran';
UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.fund_collection'   WHERE menu_key = 'keuangan.transaksi.penghimpunan';
UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.general'           WHERE menu_key = 'keuangan.transaksi.umum';
UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.receivable'        WHERE menu_key = 'keuangan.piutang.pinjam-bayar';
UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.cash_advance'      WHERE menu_key = 'keuangan.transaksi.uang-muka-penyerahan';
UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.cash_advance_lpj'  WHERE menu_key = 'keuangan.transaksi.uang-muka-pengembalian';
UPDATE isf_auth.role_menu SET menu_key = 'finance.transactions.fund_transfer'     WHERE menu_key = 'keuangan.transaksi.transfer-antar-rekening';

UPDATE isf_auth.role_menu SET menu_key = 'finance.monitoring.authorization' WHERE menu_key = 'keuangan.monitoring.otorisasi';
UPDATE isf_auth.role_menu SET menu_key = 'finance.monitoring.history'       WHERE menu_key = 'keuangan.monitoring.riwayat';

UPDATE isf_auth.role_menu SET menu_key = 'finance.upload.collection'         WHERE menu_key = 'keuangan.upload.penghimpunan';
UPDATE isf_auth.role_menu SET menu_key = 'finance.upload.collection.approve' WHERE menu_key = 'keuangan.upload.penghimpunan.approve';
UPDATE isf_auth.role_menu SET menu_key = 'finance.upload.zis_routine'        WHERE menu_key = 'keuangan.upload.zis-rutin';
UPDATE isf_auth.role_menu SET menu_key = 'finance.upload.zis_routine_list'   WHERE menu_key = 'keuangan.upload.zis-rutin-list';

UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.daily_journal'         WHERE menu_key = 'keuangan.report.journal_daily';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.general_transaction'   WHERE menu_key = 'keuangan.report.general_transaction';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.daily_cash'            WHERE menu_key = 'keuangan.report.cash_daily';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.cash_summary'          WHERE menu_key = 'keuangan.report.cash_summary';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.monthly_balance'       WHERE menu_key = 'keuangan.report.cash_monthly';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.trial_balance'         WHERE menu_key = 'keuangan.report.trial_balance';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.balance_sheet'         WHERE menu_key = 'keuangan.report.neraca';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.cash_flow'             WHERE menu_key = 'keuangan.report.cash_flow';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.general_ledger'        WHERE menu_key = 'keuangan.report.general_ledger';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.fund_changes'          WHERE menu_key = 'keuangan.report.fund_changes';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.fund_changes_detail'   WHERE menu_key = 'keuangan.report.fund_changes_detail';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.amil_receipt'          WHERE menu_key = 'keuangan.report.amil_in';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.amil_expense'          WHERE menu_key = 'keuangan.report.amil_out';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.fund_distribution'     WHERE menu_key = 'keuangan.report.distribution';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.fund_collection'       WHERE menu_key = 'keuangan.report.collection';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.employee_receivable'   WHERE menu_key = 'keuangan.report.ar_employee';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.non_employee_receivable' WHERE menu_key = 'keuangan.report.ar_external';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.activity_cash_advance' WHERE menu_key = 'keuangan.report.ca_employee';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.cash_advance_list'     WHERE menu_key = 'keuangan.report.ca_list';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.memo_realization'      WHERE menu_key = 'keuangan.report.project_memo';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.receivable_realization' WHERE menu_key = 'keuangan.report.program_ar';
UPDATE isf_auth.role_menu SET menu_key = 'finance.reports.upz'                   WHERE menu_key = 'keuangan.report.upz';

COMMIT;

-- Verify
SELECT 'menu remaining old keys' AS check_name,
       COUNT(*) AS count
FROM isf_auth.menu
WHERE menu_key LIKE 'keuangan.%' OR menu_key LIKE 'dashboard.keuangan'
  OR menu_key IN ('dashboard.penyaluran', 'dashboard.penghimpunan');

import type { RouteRecordRaw } from 'vue-router'
import type { MenuKey } from '@/shared/constants/menu-keys'

export const financeRoutes: RouteRecordRaw[] = [
  // ── Dashboard ────────────────────────────────────────────────────────────
  {
    path: '/',
    name: 'dashboard',
    component: () => import('./views/dashboard/DashboardView.vue'),
    meta: { title: 'Dashboard', menu_key: 'dashboard.overview' as MenuKey, domain: 'finance' },
  },
  {
    path: '/dashboard/finance',
    name: 'dashboard-finance',
    component: () => import('./views/dashboard/DashboardFinanceView.vue'),
    meta: { title: 'Dashboard Keuangan', menu_key: 'dashboard.finance' as MenuKey, domain: 'finance' },
  },
  {
    path: '/dashboard/distribution',
    name: 'dashboard-distribution',
    component: () => import('./views/dashboard/DashboardDistributionView.vue'),
    meta: { title: 'Dashboard Penyaluran', menu_key: 'dashboard.distribution' as MenuKey, domain: 'finance' },
  },
  {
    path: '/dashboard/collection',
    name: 'dashboard-collection',
    component: () => import('./views/dashboard/DashboardCollectionView.vue'),
    meta: { title: 'Dashboard Penghimpunan', menu_key: 'dashboard.collection' as MenuKey, domain: 'finance' },
  },

  // ── Master Data ───────────────────────────────────────────────────────────
  {
    path: '/finance/coa',
    name: 'finance-coa',
    component: () => import('./views/master/coa/CoaListView.vue'),
    meta: { title: 'Chart of Accounts', menu_key: 'finance.coa' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/coa/create',
    name: 'finance-coa-create',
    component: () => import('./views/master/coa/CoaCreateView.vue'),
    meta: { title: 'Tambah Akun COA', menu_key: 'finance.coa' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/cash',
    name: 'finance-cash',
    component: () => import('./views/master/cash/CashListView.vue'),
    meta: { title: 'Manajemen Kas', menu_key: 'finance.cash' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/cash/create',
    name: 'finance-cash-create',
    component: () => import('./views/master/cash/CashCreateView.vue'),
    meta: { title: 'Tambah Kas', menu_key: 'finance.cash' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/bank',
    name: 'finance-bank',
    component: () => import('./views/master/bank/BankListView.vue'),
    meta: { title: 'Manajemen Bank', menu_key: 'finance.bank' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/bank/create',
    name: 'finance-bank-create',
    component: () => import('./views/master/bank/BankCreateView.vue'),
    meta: { title: 'Tambah Rekening Bank', menu_key: 'finance.bank' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/petty-cash',
    name: 'finance-petty-cash',
    component: () => import('./views/master/petty-cash/PettyCashListView.vue'),
    meta: { title: 'Manajemen Kas Kecil', menu_key: 'finance.petty_cash' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/petty-cash/create',
    name: 'finance-petty-cash-create',
    component: () => import('./views/master/petty-cash/PettyCashCreateView.vue'),
    meta: { title: 'Tambah Rekening Kas Kecil', menu_key: 'finance.petty_cash' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/master/budget-owner',
    name: 'finance-master-budget-owner',
    component: () => import('./views/master/budget-owner/BudgetOwnerView.vue'),
    meta: { title: 'Pemilik Anggaran', menu_key: 'finance.parameter.budget_owner' as MenuKey, domain: 'finance' },
  },

  // ── Budget ────────────────────────────────────────────────────────────────
  {
    path: '/finance/budget/import',
    name: 'finance-budget-import',
    component: () => import('./views/budget/import/BudgetImportView.vue'),
    meta: { title: 'Buat Anggaran Baru', menu_key: 'finance.budget.import' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/budget/revise',
    name: 'finance-budget-revise',
    component: () => import('./views/budget/revise/BudgetReviseListView.vue'),
    meta: { title: 'Revisi Anggaran', menu_key: 'finance.budget.revise' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/budget/revise/create',
    name: 'finance-budget-revise-create',
    component: () => import('./views/budget/revise/BudgetReviseCreateView.vue'),
    meta: { title: 'Tambah Anggaran', menu_key: 'finance.budget.revise' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/budget/item',
    name: 'finance-budget-item',
    component: () => import('./views/budget/item/BudgetItemView.vue'),
    meta: { title: 'Item Anggaran', menu_key: 'finance.parameter.budget.item' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/budget/period',
    name: 'finance-budget-period',
    component: () => import('./views/budget/period/BudgetPeriodView.vue'),
    meta: { title: 'Periode Anggaran', menu_key: 'finance.parameter.budget.period' as MenuKey, domain: 'finance' },
  },

  // ── Inquiry ───────────────────────────────────────────────────────────────
  {
    path: '/finance/budget/inquiry',
    name: 'finance-budget-inquiry',
    component: () => import('./views/inquiry/budget/BudgetInquiryView.vue'),
    meta: { title: 'Inquiry Anggaran', menu_key: 'finance.budget.inquiry' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/budget/inquiry/owner/:owner_id',
    name: 'finance-budget-inquiry-owner',
    component: () => import('./views/inquiry/budget/BudgetInquiryOwnerView.vue'),
    meta: { title: 'Detail Anggaran Pemilik', menu_key: 'finance.budget.inquiry' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/budget/inquiry/budget/:budget_id/transactions',
    name: 'finance-budget-inquiry-transactions',
    component: () => import('./views/inquiry/budget/BudgetInquiryTransaksiView.vue'),
    meta: { title: 'Riwayat Transaksi Anggaran', menu_key: 'finance.budget.inquiry' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/history',
    name: 'finance-transactions-history',
    component: () => import('./views/inquiry/transaction-history/TransactionHistoryListView.vue'),
    meta: { title: 'Histori Transaksi', menu_key: 'finance.transactions.history' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/history/:id',
    name: 'finance-transactions-history-detail',
    component: () => import('./views/inquiry/transaction-history/TransactionHistoryDetailView.vue'),
    meta: { title: 'Detail Transaksi', menu_key: 'finance.transactions.history' as MenuKey, domain: 'finance' },
  },

  {
    path: '/finance/inquiry/cash-advance',
    name: 'finance-inquiry-cash-advance',
    component: () => import('./views/inquiry/cash-advance/CashAdvanceInquiryView.vue'),
    meta: { title: 'Uang Muka Kegiatan', menu_key: 'finance.inquiry.cash_advance' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/inquiry/receivable',
    name: 'finance-inquiry-receivable',
    component: () => import('./views/inquiry/receivable/ReceivableInquiryView.vue'),
    meta: { title: 'Piutang Karyawan / Non Karyawan', menu_key: 'finance.inquiry.receivable' as MenuKey, domain: 'finance' },
  },

  // ── Transaction ───────────────────────────────────────────────────────────
  {
    path: '/finance/transactions/fund-collection',
    name: 'finance-transactions-fund-collection',
    component: () => import('./views/transaction/fund-collection/FundCollectionListView.vue'),
    meta: { title: 'Penghimpunan Dana', menu_key: 'finance.transactions.fund_collection' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/fund-collection/create',
    name: 'finance-transactions-fund-collection-create',
    component: () => import('./views/transaction/fund-collection/FundCollectionCreateView.vue'),
    meta: { title: 'Input Penghimpunan Dana', menu_key: 'finance.transactions.fund_collection' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/fund-collection/edit/:id',
    name: 'finance-transactions-fund-collection-edit',
    component: () => import('./views/transaction/fund-collection/FundCollectionCreateView.vue'),
    meta: { title: 'Edit Draft Penghimpunan', menu_key: 'finance.transactions.fund_collection' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/fund-distribution',
    name: 'finance-transactions-fund-distribution',
    component: () => import('./views/transaction/fund-distribution/FundDistributionListView.vue'),
    meta: { title: 'Penyaluran Dana', menu_key: 'finance.transactions.fund_distribution' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/fund-distribution/create',
    name: 'finance-transactions-fund-distribution-create',
    component: () => import('./views/transaction/fund-distribution/FundDistributionCreateView.vue'),
    meta: { title: 'Input Penyaluran Dana', menu_key: 'finance.transactions.fund_distribution' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/fund-distribution/edit/:id',
    name: 'finance-transactions-fund-distribution-edit',
    component: () => import('./views/transaction/fund-distribution/FundDistributionCreateView.vue'),
    meta: { title: 'Edit Draft Penyaluran', menu_key: 'finance.transactions.fund_distribution' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/cash-advance',
    name: 'finance-transactions-cash-advance',
    component: () => import('./views/transaction/cash-advance/CashAdvanceListView.vue'),
    meta: { title: 'Penyerahan Uang Muka', menu_key: 'finance.transactions.cash_advance' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/cash-advance/create',
    name: 'finance-transactions-cash-advance-create',
    component: () => import('./views/transaction/cash-advance/CashAdvanceCreateView.vue'),
    meta: { title: 'Input Penyerahan Uang Muka', menu_key: 'finance.transactions.cash_advance' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/cash-advance-lpj',
    name: 'finance-transactions-cash-advance-lpj',
    component: () => import('./views/transaction/cash-advance-lpj/CashAdvanceLPJListView.vue'),
    meta: { title: 'LPJ Uang Muka', menu_key: 'finance.transactions.cash_advance_lpj' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/cash-advance-lpj/create',
    name: 'finance-transactions-cash-advance-lpj-create',
    component: () => import('./views/transaction/cash-advance-lpj/CashAdvanceLPJCreateView.vue'),
    meta: { title: 'Input LPJ Uang Muka', menu_key: 'finance.transactions.cash_advance_lpj' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/fund-transfer',
    name: 'finance-transactions-fund-transfer',
    component: () => import('./views/transaction/fund-transfer/FundTransferListView.vue'),
    meta: { title: 'Transfer Antar Rekening', menu_key: 'finance.transactions.fund_transfer' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/fund-transfer/create',
    name: 'finance-transactions-fund-transfer-create',
    component: () => import('./views/transaction/fund-transfer/FundTransferCreateView.vue'),
    meta: { title: 'Input Transfer Antar Rekening', menu_key: 'finance.transactions.fund_transfer' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/general',
    name: 'finance-transactions-general',
    component: () => import('./views/transaction/general/GeneralTransactionListView.vue'),
    meta: { title: 'Transaksi Umum', menu_key: 'finance.transactions.general' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/general/create',
    name: 'finance-transactions-general-create',
    component: () => import('./views/transaction/general/GeneralTransactionCreateView.vue'),
    meta: { title: 'Input Transaksi Umum', menu_key: 'finance.transactions.general' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/amil-income',
    name: 'finance-transactions-amil-income',
    component: () => import('./views/transaction/amil-income/AmilIncomeListView.vue'),
    meta: { title: 'Penerimaan Amil', menu_key: 'finance.transactions.amil_income' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/amil-income/create',
    name: 'finance-transactions-amil-income-create',
    component: () => import('./views/transaction/amil-income/AmilIncomeCreateView.vue'),
    meta: { title: 'Input Penerimaan Amil', menu_key: 'finance.transactions.amil_income' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/amil-expense',
    name: 'finance-transactions-amil-expense',
    component: () => import('./views/transaction/amil-expense/AmilExpenseListView.vue'),
    meta: { title: 'Pengeluaran Amil', menu_key: 'finance.transactions.amil_expense' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/amil-expense/create',
    name: 'finance-transactions-amil-expense-create',
    component: () => import('./views/transaction/amil-expense/AmilExpenseCreateView.vue'),
    meta: { title: 'Input Pengeluaran Amil', menu_key: 'finance.transactions.amil_expense' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/receivable',
    name: 'finance-transactions-receivable',
    component: () => import('./views/transaction/receivable/ReceivableListView.vue'),
    meta: { title: 'Piutang (Pinjam/Bayar)', menu_key: 'finance.transactions.receivable' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/transactions/receivable/create',
    name: 'finance-transactions-receivable-create',
    component: () => import('./views/transaction/receivable/ReceivableCreateView.vue'),
    meta: { title: 'Input Piutang', menu_key: 'finance.transactions.receivable' as MenuKey, domain: 'finance' },
  },

  // ── Upload ────────────────────────────────────────────────────────────────
  {
    path: '/finance/upload/collection',
    name: 'finance-upload-collection',
    component: () => import('./views/upload/collection/UploadCollectionView.vue'),
    meta: { title: 'Upload Penghimpunan', menu_key: 'finance.upload.collection' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/upload/collection/list',
    name: 'finance-upload-collection-list',
    component: () => import('./views/upload/collection/UploadCollectionListView.vue'),
    meta: { title: 'Daftar Batch Upload', menu_key: 'finance.upload.collection.approve' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/upload/collection/:id',
    name: 'finance-upload-collection-detail',
    component: () => import('./views/upload/collection/UploadCollectionDetailView.vue'),
    meta: { title: 'Detail Batch', menu_key: 'finance.upload.collection.approve' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/upload/zis-routine',
    name: 'finance-upload-zis-routine',
    component: () => import('./views/upload/zis-routine/UploadZisRoutineView.vue'),
    meta: { title: 'Upload ZIS Rutin', menu_key: 'finance.upload.zis_routine' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/upload/zis-routine/list',
    name: 'finance-upload-zis-routine-list',
    component: () => import('./views/upload/zis-routine/UploadZisRoutineListView.vue'),
    meta: { title: 'Daftar Upload ZIS Rutin', menu_key: 'finance.upload.zis_routine_list' as MenuKey, domain: 'finance' },
  },

  // ── Reports ───────────────────────────────────────────────────────────────
  {
    path: '/finance/reports/daily-journal',
    name: 'finance-reports-daily-journal',
    component: () => import('./views/reports/ReportDailyJournalView.vue'),
    meta: { title: 'Laporan Jurnal Harian', menu_key: 'finance.reports.daily_journal' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/general-transaction',
    name: 'finance-reports-general-transaction',
    component: () => import('./views/reports/ReportGeneralTransactionView.vue'),
    meta: { title: 'List Transaksi Umum', menu_key: 'finance.reports.general_transaction' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/daily-cash',
    name: 'finance-reports-daily-cash',
    component: () => import('./views/reports/ReportCashDailyView.vue'),
    meta: { title: 'Transaksi Kas/Bank Harian', menu_key: 'finance.reports.daily_cash' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/cash-summary',
    name: 'finance-reports-cash-summary',
    component: () => import('./views/reports/ReportCashSummaryView.vue'),
    meta: { title: 'Rekapitulasi Transaksi Kas/Bank', menu_key: 'finance.reports.cash_summary' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/monthly-balance',
    name: 'finance-reports-monthly-balance',
    component: () => import('./views/reports/ReportCashMonthlyView.vue'),
    meta: { title: 'Monitoring Saldo Kas/Bank Bulanan', menu_key: 'finance.reports.monthly_balance' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/trial-balance',
    name: 'finance-reports-trial-balance',
    component: () => import('./views/reports/ReportTrialBalanceView.vue'),
    meta: { title: 'Trial Balance', menu_key: 'finance.reports.trial_balance' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/balance-sheet',
    name: 'finance-reports-balance-sheet',
    component: () => import('./views/reports/ReportBalanceSheetView.vue'),
    meta: { title: 'Neraca', menu_key: 'finance.reports.balance_sheet' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/cash-flow',
    name: 'finance-reports-cash-flow',
    component: () => import('./views/reports/ReportCashFlowView.vue'),
    meta: { title: 'Arus Kas', menu_key: 'finance.reports.cash_flow' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/general-ledger',
    name: 'finance-reports-general-ledger',
    component: () => import('./views/reports/ReportGeneralLedgerView.vue'),
    meta: { title: 'Buku Besar', menu_key: 'finance.reports.general_ledger' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/fund-changes',
    name: 'finance-reports-fund-changes',
    component: () => import('./views/reports/ReportFundChangeView.vue'),
    meta: { title: 'Perubahan Dana', menu_key: 'finance.reports.fund_changes' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/fund-changes-detail',
    name: 'finance-reports-fund-changes-detail',
    component: () => import('./views/reports/ReportFundChangeDetailView.vue'),
    meta: { title: 'Perubahan Dana Detail', menu_key: 'finance.reports.fund_changes_detail' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/amil-receipt',
    name: 'finance-reports-amil-receipt',
    component: () => import('./views/reports/ReportAmilView.vue'),
    meta: { title: 'Penerimaan Amil', menu_key: 'finance.reports.amil_receipt' as MenuKey, amilKind: 'in', domain: 'finance' },
  },
  {
    path: '/finance/reports/amil-expense',
    name: 'finance-reports-amil-expense',
    component: () => import('./views/reports/ReportAmilView.vue'),
    meta: { title: 'Pengeluaran Amil', menu_key: 'finance.reports.amil_expense' as MenuKey, amilKind: 'out', domain: 'finance' },
  },
  {
    path: '/finance/reports/fund-collection',
    name: 'finance-reports-fund-collection',
    component: () => import('./views/reports/ReportFundCollectionView.vue'),
    meta: { title: 'Penghimpunan Dana', menu_key: 'finance.reports.fund_collection' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/fund-distribution',
    name: 'finance-reports-fund-distribution',
    component: () => import('./views/reports/ReportFundDistributionView.vue'),
    meta: { title: 'Penyaluran Dana', menu_key: 'finance.reports.fund_distribution' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/employee-receivable',
    name: 'finance-reports-employee-receivable',
    component: () => import('./views/reports/ReportARSummaryView.vue'),
    meta: { title: 'Piutang pada Karyawan', menu_key: 'finance.reports.employee_receivable' as MenuKey, arEndpoint: 'employee-ar', arFile: 'piutangkaryawan', domain: 'finance' },
  },
  {
    path: '/finance/reports/non-employee-receivable',
    name: 'finance-reports-non-employee-receivable',
    component: () => import('./views/reports/ReportARSummaryView.vue'),
    meta: { title: 'Piutang pada Non-Karyawan', menu_key: 'finance.reports.non_employee_receivable' as MenuKey, arEndpoint: 'external-ar', arFile: 'piutangnonkaryawan', domain: 'finance' },
  },
  {
    path: '/finance/reports/activity-cash-advance',
    name: 'finance-reports-activity-cash-advance',
    component: () => import('./views/reports/ReportARSummaryView.vue'),
    meta: { title: 'Rekapitulasi Uang Muka Kegiatan', menu_key: 'finance.reports.activity_cash_advance' as MenuKey, arEndpoint: 'cash-advance', arFile: 'rekapuangmuka', domain: 'finance' },
  },
  {
    path: '/finance/reports/cash-advance-list',
    name: 'finance-reports-cash-advance-list',
    component: () => import('./views/reports/ReportCashAdvanceListView.vue'),
    meta: { title: 'List Transaksi Uang Muka Kegiatan', menu_key: 'finance.reports.cash_advance_list' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/memo-realization',
    name: 'finance-reports-memo-realization',
    component: () => import('./views/reports/ReportMemoRealizationView.vue'),
    meta: { title: 'Laporan Realisasi Project (Memo)', menu_key: 'finance.reports.memo_realization' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/receivable-realization',
    name: 'finance-reports-receivable-realization',
    component: () => import('./views/reports/ReportReceivableRealizationView.vue'),
    meta: { title: 'Piutang Realisasi Penyaluran', menu_key: 'finance.reports.receivable_realization' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/reports/upz',
    name: 'finance-reports-upz',
    component: () => import('./views/reports/ReportUpzView.vue'),
    meta: { title: 'List Transaksi UPZ', menu_key: 'finance.reports.upz' as MenuKey, domain: 'finance' },
  },

  // ── Monitoring ────────────────────────────────────────────────────────────
  {
    path: '/finance/monitoring/authorization',
    name: 'finance-monitoring-authorization',
    component: () => import('./views/monitoring/AuthorizationView.vue'),
    meta: { title: 'Otorisasi', menu_key: 'finance.monitoring.authorization' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/monitoring/history',
    name: 'finance-monitoring-history',
    component: () => import('./views/monitoring/SubmissionHistoryView.vue'),
    meta: { title: 'Riwayat Submission', menu_key: 'finance.monitoring.history' as MenuKey, domain: 'finance' },
  },
]

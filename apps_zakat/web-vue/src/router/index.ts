import { createRouter, createWebHistory } from 'vue-router'

import type { MenuKey } from '@/lib/menu/registry'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue'),
      meta: { public: true, title: 'Masuk' },
    },
    {
      path: '/no-tenant',
      name: 'no-tenant',
      component: () => import('@/pages/NoTenantPage.vue'),
      meta: { requiresNoTenant: true, title: 'Akun' },
    },
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/pages/dashboard/DashboardPage.vue'),
      meta: { title: 'Dashboard', menu_key: 'dashboard.overview' as MenuKey },
    },
    {
      path: '/finance/coa',
      name: 'finance-coa',
      component: () => import('@/pages/finance/coa/CoaListPage.vue'),
      meta: { title: 'Chart of Accounts', menu_key: 'keuangan.coa' as MenuKey },
    },
    {
      path: '/finance/coa/create',
      name: 'finance-coa-create',
      component: () => import('@/pages/finance/coa/CoaCreatePage.vue'),
      meta: { title: 'Tambah Akun COA', menu_key: 'keuangan.coa' as MenuKey },
    },
    {
      path: '/finance/cash',
      name: 'finance-cash',
      component: () => import('@/pages/finance/cash/CashListPage.vue'),
      meta: { title: 'Manajemen Kas', menu_key: 'keuangan.kas' as MenuKey },
    },
    {
      path: '/finance/cash/create',
      name: 'finance-cash-create',
      component: () => import('@/pages/finance/cash/CashCreatePage.vue'),
      meta: { title: 'Tambah Kas', menu_key: 'keuangan.kas' as MenuKey },
    },
    {
      path: '/finance/bank',
      name: 'finance-bank',
      component: () => import('@/pages/finance/bank/BankListPage.vue'),
      meta: { title: 'Manajemen Bank', menu_key: 'keuangan.bank' as MenuKey },
    },
    {
      path: '/finance/bank/create',
      name: 'finance-bank-create',
      component: () => import('@/pages/finance/bank/BankCreatePage.vue'),
      meta: { title: 'Tambah Rekening Bank', menu_key: 'keuangan.bank' as MenuKey },
    },
    {
      path: '/finance/petty-cash',
      name: 'finance-petty-cash',
      component: () => import('@/pages/finance/petty-cash/PettyCashListPage.vue'),
      meta: { title: 'Manajemen Kas Kecil', menu_key: 'keuangan.kas_kecil' as MenuKey },
    },
    {
      path: '/finance/petty-cash/create',
      name: 'finance-petty-cash-create',
      component: () => import('@/pages/finance/petty-cash/PettyCashCreatePage.vue'),
      meta: { title: 'Tambah Rekening Kas Kecil', menu_key: 'keuangan.kas_kecil' as MenuKey },
    },
    {
      path: '/finance/budget/import',
      name: 'finance-budget-import',
      component: () => import('@/pages/finance/budget-import/BudgetImportCreatePage.vue'),
      meta: { title: 'Buat Anggaran Baru', menu_key: 'keuangan.anggaran.import' as MenuKey },
    },
    {
      path: '/finance/budget/revise',
      name: 'finance-budget-revise',
      component: () => import('@/pages/finance/budget-revise/BudgetReviseListPage.vue'),
      meta: { title: 'Revisi Anggaran', menu_key: 'keuangan.anggaran.revisi' as MenuKey },
    },
    {
      path: '/finance/budget/revise/create',
      name: 'finance-budget-revise-create',
      component: () => import('@/pages/finance/budget-revise/BudgetReviseCreatePage.vue'),
      meta: { title: 'Tambah Anggaran', menu_key: 'keuangan.anggaran.revisi' as MenuKey },
    },
    {
      path: '/finance/budget/inquiry',
      name: 'finance-budget-inquiry',
      component: () => import('@/pages/finance/budget-inquiry/BudgetInquiryPage.vue'),
      meta: { title: 'Inquiry Anggaran', menu_key: 'keuangan.anggaran.inquiry' as MenuKey },
    },
    {
      path: '/finance/budget/inquiry/owner/:owner_id',
      name: 'finance-budget-inquiry-owner',
      component: () => import('@/pages/finance/budget-inquiry/BudgetInquiryOwnerPage.vue'),
      meta: { title: 'Detail Anggaran Pemilik', menu_key: 'keuangan.anggaran.inquiry' as MenuKey },
    },
    {
      path: '/finance/budget/inquiry/budget/:budget_id/transactions',
      name: 'finance-budget-inquiry-transactions',
      component: () => import('@/pages/finance/budget-inquiry/BudgetInquiryTransaksiPage.vue'),
      meta: { title: 'Riwayat Transaksi Anggaran', menu_key: 'keuangan.anggaran.inquiry' as MenuKey },
    },
    {
      path: '/finance/reports/daily-journal',
      name: 'finance-reports-daily-journal',
      component: () => import('@/pages/finance/reports/ReportDailyJournalPage.vue'),
      meta: {
        title: 'Laporan Jurnal Harian',
        menu_key: 'keuangan.report.journal_daily' as MenuKey,
      },
    },
    {
      path: '/finance/reports/general-transaction',
      name: 'finance-reports-general-transaction',
      component: () => import('@/pages/finance/reports/ReportGeneralTransactionPage.vue'),
      meta: {
        title: 'List Transaksi Umum',
        menu_key: 'keuangan.report.general_transaction' as MenuKey,
      },
    },
    {
      path: '/finance/reports/daily-cash',
      name: 'finance-reports-daily-cash',
      component: () => import('@/pages/finance/reports/ReportCashDailyPage.vue'),
      meta: {
        title: 'Transaksi Kas/Bank Harian',
        menu_key: 'keuangan.report.cash_daily' as MenuKey,
      },
    },
    {
      path: '/finance/reports/cash-summary',
      name: 'finance-reports-cash-summary',
      component: () => import('@/pages/finance/reports/ReportCashSummaryPage.vue'),
      meta: {
        title: 'Rekapitulasi Transaksi Kas/Bank',
        menu_key: 'keuangan.report.cash_summary' as MenuKey,
      },
    },
    {
      path: '/finance/reports/monthly-balance',
      name: 'finance-reports-monthly-balance',
      component: () => import('@/pages/finance/reports/ReportCashMonthlyPage.vue'),
      meta: {
        title: 'Monitoring Saldo Kas/Bank Bulanan',
        menu_key: 'keuangan.report.cash_monthly' as MenuKey,
      },
    },
    {
      path: '/finance/reports/trial-balance',
      name: 'finance-reports-trial-balance',
      component: () => import('@/pages/finance/reports/ReportTrialBalancePage.vue'),
      meta: {
        title: 'Trial Balance',
        menu_key: 'keuangan.report.trial_balance' as MenuKey,
      },
    },
    {
      path: '/finance/reports/balance-sheet',
      name: 'finance-reports-balance-sheet',
      component: () => import('@/pages/finance/reports/ReportBalanceSheetPage.vue'),
      meta: {
        title: 'Neraca',
        menu_key: 'keuangan.report.neraca' as MenuKey,
      },
    },
    {
      path: '/finance/reports/cash-flow',
      name: 'finance-reports-cash-flow',
      component: () => import('@/pages/finance/reports/ReportCashFlowPage.vue'),
      meta: {
        title: 'Arus Kas',
        menu_key: 'keuangan.report.cash_flow' as MenuKey,
      },
    },
    {
      path: '/finance/reports/general-ledger',
      name: 'finance-reports-general-ledger',
      component: () => import('@/pages/finance/reports/ReportGeneralLedgerPage.vue'),
      meta: {
        title: 'Buku Besar',
        menu_key: 'keuangan.report.general_ledger' as MenuKey,
      },
    },
    {
      path: '/finance/reports/fund-changes',
      name: 'finance-reports-fund-changes',
      component: () => import('@/pages/finance/reports/ReportFundChangePage.vue'),
      meta: {
        title: 'Perubahan Dana',
        menu_key: 'keuangan.report.fund_changes' as MenuKey,
      },
    },
    {
      path: '/finance/reports/fund-changes-detail',
      name: 'finance-reports-fund-changes-detail',
      component: () => import('@/pages/finance/reports/ReportFundChangeDetailPage.vue'),
      meta: {
        title: 'Perubahan Dana Detail',
        menu_key: 'keuangan.report.fund_changes_detail' as MenuKey,
      },
    },
    {
      path: '/finance/reports/amil-receipt',
      name: 'finance-reports-amil-receipt',
      component: () => import('@/pages/finance/reports/ReportAmilPage.vue'),
      meta: {
        title: 'Penerimaan Amil',
        menu_key: 'keuangan.report.amil_in' as MenuKey,
        amilKind: 'in',
      },
    },
    {
      path: '/finance/reports/amil-expense',
      name: 'finance-reports-amil-expense',
      component: () => import('@/pages/finance/reports/ReportAmilPage.vue'),
      meta: {
        title: 'Pengeluaran Amil',
        menu_key: 'keuangan.report.amil_out' as MenuKey,
        amilKind: 'out',
      },
    },
    {
      path: '/finance/reports/fund-distribution',
      name: 'finance-reports-fund-distribution',
      component: () => import('@/pages/finance/reports/ReportFundDistributionPage.vue'),
      meta: {
        title: 'Penyaluran Dana',
        menu_key: 'keuangan.report.distribution' as MenuKey,
      },
    },
    {
      path: '/finance/reports/fund-collection',
      name: 'finance-reports-fund-collection',
      component: () => import('@/pages/finance/reports/ReportFundCollectionPage.vue'),
      meta: {
        title: 'Penghimpunan Dana',
        menu_key: 'keuangan.report.collection' as MenuKey,
      },
    },
    {
      path: '/finance/reports/employee-receivable',
      name: 'finance-reports-employee-receivable',
      component: () => import('@/pages/finance/reports/ReportARSummaryPage.vue'),
      meta: { title: 'Piutang pada Karyawan', menu_key: 'keuangan.report.ar_employee' as MenuKey, arEndpoint: 'employee-ar', arFile: 'piutangkaryawan' },
    },
    {
      path: '/finance/reports/non-employee-receivable',
      name: 'finance-reports-non-employee-receivable',
      component: () => import('@/pages/finance/reports/ReportARSummaryPage.vue'),
      meta: { title: 'Piutang pada Non-Karyawan', menu_key: 'keuangan.report.ar_external' as MenuKey, arEndpoint: 'external-ar', arFile: 'piutangnonkaryawan' },
    },
    {
      path: '/finance/reports/activity-cash-advance',
      name: 'finance-reports-activity-cash-advance',
      component: () => import('@/pages/finance/reports/ReportARSummaryPage.vue'),
      meta: { title: 'Rekapitulasi Uang Muka Kegiatan', menu_key: 'keuangan.report.ca_employee' as MenuKey, arEndpoint: 'cash-advance', arFile: 'rekapuangmuka' },
    },
    {
      path: '/finance/reports/cash-advance-list',
      name: 'finance-reports-cash-advance-list',
      component: () => import('@/pages/finance/reports/ReportCashAdvanceListPage.vue'),
      meta: { title: 'List Transaksi Uang Muka Kegiatan', menu_key: 'keuangan.report.ca_list' as MenuKey },
    },
    {
      path: '/finance/reports/memo-realization',
      name: 'finance-reports-memo-realization',
      component: () => import('@/pages/finance/reports/ReportMemoRealizationPage.vue'),
      meta: { title: 'Laporan Realisasi Project (Memo)', menu_key: 'keuangan.report.project_memo' as MenuKey },
    },
    {
      path: '/finance/reports/receivable-realization',
      name: 'finance-reports-receivable-realization',
      component: () => import('@/pages/finance/reports/ReportReceivableRealizationPage.vue'),
      meta: { title: 'Piutang Realisasi Penyaluran', menu_key: 'keuangan.report.program_ar' as MenuKey },
    },
    {
      path: '/finance/reports/upz',
      name: 'finance-reports-upz',
      component: () => import('@/pages/finance/reports/ReportUpzPage.vue'),
      meta: { title: 'List Transaksi UPZ', menu_key: 'keuangan.report.upz' as MenuKey },
    },
    {
      path: '/dashboard/finance',
      name: 'dashboard-finance',
      component: () => import('@/pages/dashboard/DashboardFinancePage.vue'),
      meta: { title: 'Dashboard Keuangan', menu_key: 'dashboard.keuangan' as MenuKey },
    },
    {
      path: '/dashboard/distribution',
      name: 'dashboard-distribution',
      component: () => import('@/pages/dashboard/DashboardDistributionPage.vue'),
      meta: { title: 'Dashboard Penyaluran', menu_key: 'dashboard.penyaluran' as MenuKey },
    },
    {
      path: '/dashboard/collection',
      name: 'dashboard-collection',
      component: () => import('@/pages/dashboard/DashboardCollectionPage.vue'),
      meta: { title: 'Dashboard Penghimpunan', menu_key: 'dashboard.penghimpunan' as MenuKey },
    },
    {
      path: '/admin/role-menu',
      name: 'admin-role-menu',
      component: () => import('@/pages/admin/RoleMenuPage.vue'),
      meta: { title: 'Mapping Role-Menu', menu_key: 'admin.role_menu' as MenuKey },
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: () => import('@/pages/admin/UsersPage.vue'),
      meta: { title: 'List User', menu_key: 'admin.users' as MenuKey },
    },
    {
      path: '/profile/password',
      name: 'profile-password',
      component: () => import('@/pages/profile/PasswordPage.vue'),
      meta: { title: 'Ganti Password' },
    },
    {
      path: '/finance/upload/collection',
      name: 'finance-upload-collection',
      component: () => import('@/pages/finance/upload-collection-multi/UploadCollectionMultiPage.vue'),
      meta: { title: 'Upload Penghimpunan', menu_key: 'keuangan.upload.penghimpunan' as MenuKey },
    },
    {
      path: '/finance/upload/collection/list',
      name: 'finance-upload-collection-list',
      component: () => import('@/pages/finance/upload-collection-multi/UploadCollectionMultiListPage.vue'),
      meta: { title: 'Daftar Batch Upload', menu_key: 'keuangan.upload.penghimpunan.approve' as MenuKey },
    },
    {
      path: '/finance/upload/collection/:id',
      name: 'finance-upload-collection-detail',
      component: () => import('@/pages/finance/upload-collection-multi/UploadCollectionMultiDetailPage.vue'),
      meta: { title: 'Detail Batch', menu_key: 'keuangan.upload.penghimpunan.approve' as MenuKey },
    },
    {
      path: '/finance/upload/zis-routine',
      name: 'finance-upload-zis-routine',
      component: () => import('@/pages/finance/upload-collection-hc/UploadCollectionHCZisPage.vue'),
      meta: { title: 'Upload ZIS Rutin', menu_key: 'keuangan.upload.zis-rutin' as MenuKey },
    },
    {
      path: '/finance/upload/zis-routine/list',
      name: 'finance-upload-zis-routine-list',
      component: () => import('@/pages/finance/upload-collection-hc/UploadCollectionHCZisListPage.vue'),
      meta: { title: 'Daftar Upload ZIS Rutin', menu_key: 'keuangan.upload.zis-rutin-list' as MenuKey },
    },
    {
      path: '/finance/transactions/history',
      name: 'finance-transactions-history',
      component: () => import('@/pages/finance/transaction-history/TransactionHistoryListPage.vue'),
      meta: { title: 'Histori Transaksi', menu_key: 'keuangan.transaksi.histori' as MenuKey },
    },
    {
      path: '/finance/transactions/history/:id',
      name: 'finance-transactions-history-detail',
      component: () => import('@/pages/finance/transaction-history/TransactionHistoryDetailPage.vue'),
      meta: { title: 'Detail Transaksi', menu_key: 'keuangan.transaksi.histori' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-distribution',
      name: 'finance-transactions-fund-distribution',
      component: () => import('@/pages/finance/fund-distribution/FundDistributionListPage.vue'),
      meta: { title: 'Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-distribution/create',
      name: 'finance-transactions-fund-distribution-create',
      component: () => import('@/pages/finance/fund-distribution/FundDistributionCreatePage.vue'),
      meta: { title: 'Input Penyaluran Dana', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-distribution/edit/:id',
      name: 'finance-transactions-fund-distribution-edit',
      component: () => import('@/pages/finance/fund-distribution/FundDistributionCreatePage.vue'),
      meta: { title: 'Edit Draft Penyaluran', menu_key: 'keuangan.transaksi.penyaluran' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-collection',
      name: 'finance-transactions-fund-collection',
      component: () => import('@/pages/finance/fund-collection/FundCollectionListPage.vue'),
      meta: { title: 'Penghimpunan Dana', menu_key: 'keuangan.transaksi.penghimpunan' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-collection/create',
      name: 'finance-transactions-fund-collection-create',
      component: () => import('@/pages/finance/fund-collection/FundCollectionCreatePage.vue'),
      meta: { title: 'Input Penghimpunan Dana', menu_key: 'keuangan.transaksi.penghimpunan' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-collection/edit/:id',
      name: 'finance-transactions-fund-collection-edit',
      component: () => import('@/pages/finance/fund-collection/FundCollectionCreatePage.vue'),
      meta: { title: 'Edit Draft Penghimpunan', menu_key: 'keuangan.transaksi.penghimpunan' as MenuKey },
    },
    {
      path: '/finance/transactions/cash-advance',
      name: 'finance-transactions-cash-advance',
      component: () => import('@/pages/finance/cash-advance/CashAdvanceListPage.vue'),
      meta: { title: 'Penyerahan Uang Muka', menu_key: 'keuangan.transaksi.uang-muka-penyerahan' as MenuKey },
    },
    {
      path: '/finance/transactions/cash-advance/create',
      name: 'finance-transactions-cash-advance-create',
      component: () => import('@/pages/finance/cash-advance/CashAdvanceCreatePage.vue'),
      meta: { title: 'Input Penyerahan Uang Muka', menu_key: 'keuangan.transaksi.uang-muka-penyerahan' as MenuKey },
    },
    {
      path: '/finance/transactions/cash-advance-lpj',
      name: 'finance-transactions-cash-advance-lpj',
      component: () => import('@/pages/finance/cash-advance-lpj/CashAdvanceLPJListPage.vue'),
      meta: { title: 'LPJ Uang Muka', menu_key: 'keuangan.transaksi.uang-muka-pengembalian' as MenuKey },
    },
    {
      path: '/finance/transactions/cash-advance-lpj/create',
      name: 'finance-transactions-cash-advance-lpj-create',
      component: () => import('@/pages/finance/cash-advance-lpj/CashAdvanceLPJCreatePage.vue'),
      meta: { title: 'Input LPJ Uang Muka', menu_key: 'keuangan.transaksi.uang-muka-pengembalian' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-transfer',
      name: 'finance-transactions-fund-transfer',
      component: () => import('@/pages/finance/fund-transfer/FundTransferListPage.vue'),
      meta: { title: 'Transfer Antar Rekening', menu_key: 'keuangan.transaksi.transfer-antar-rekening' as MenuKey },
    },
    {
      path: '/finance/transactions/fund-transfer/create',
      name: 'finance-transactions-fund-transfer-create',
      component: () => import('@/pages/finance/fund-transfer/FundTransferCreatePage.vue'),
      meta: { title: 'Input Transfer Antar Rekening', menu_key: 'keuangan.transaksi.transfer-antar-rekening' as MenuKey },
    },
    {
      path: '/finance/transactions/general',
      name: 'finance-transactions-general',
      component: () => import('@/pages/finance/general-transaction/GeneralTransactionListPage.vue'),
      meta: { title: 'Transaksi Umum', menu_key: 'keuangan.transaksi.umum' as MenuKey },
    },
    {
      path: '/finance/transactions/general/create',
      name: 'finance-transactions-general-create',
      component: () => import('@/pages/finance/general-transaction/GeneralTransactionCreatePage.vue'),
      meta: { title: 'Input Transaksi Umum', menu_key: 'keuangan.transaksi.umum' as MenuKey },
    },
    {
      path: '/finance/transactions/receivable',
      name: 'finance-transactions-receivable',
      component: () => import('@/pages/finance/receivable/ReceivableListPage.vue'),
      meta: { title: 'Piutang (Pinjam/Bayar)', menu_key: 'keuangan.piutang.pinjam-bayar' as MenuKey },
    },
    {
      path: '/finance/transactions/receivable/create',
      name: 'finance-transactions-receivable-create',
      component: () => import('@/pages/finance/receivable/ReceivableCreatePage.vue'),
      meta: { title: 'Input Piutang', menu_key: 'keuangan.piutang.pinjam-bayar' as MenuKey },
    },
    {
      path: '/finance/monitoring/authorization',
      name: 'finance-monitoring-authorization',
      component: () => import('@/pages/finance/AuthorizationPage.vue'),
      meta: { title: 'Otorisasi', menu_key: 'keuangan.monitoring.otorisasi' as MenuKey },
    },
    {
      path: '/finance/monitoring/history',
      name: 'finance-monitoring-history',
      component: () => import('@/pages/finance/SubmissionHistoryPage.vue'),
      meta: { title: 'Riwayat Submission', menu_key: 'keuangan.monitoring.riwayat' as MenuKey },
    },
    {
      path: '/parameter/budget-owner',
      name: 'parameter-budget-owner',
      component: () => import('@/pages/parameter/BudgetOwnerPage.vue'),
      meta: { title: 'Pemilik Anggaran', menu_key: 'keuangan.parameter.pemilik-anggaran' as MenuKey },
    },
    {
      path: '/parameter/anggaran/item',
      name: 'parameter-anggaran-item',
      component: () => import('@/pages/parameter/BudgetItemPage.vue'),
      meta: { title: 'Item Anggaran', menu_key: 'keuangan.parameter.anggaran.item' as MenuKey },
    },
    {
      path: '/parameter/anggaran/periode',
      name: 'parameter-anggaran-periode',
      component: () => import('@/pages/parameter/BudgetPeriodPage.vue'),
      meta: { title: 'Periode Anggaran', menu_key: 'keuangan.parameter.anggaran.periode' as MenuKey },
    },
    { path: '/:catchAll(.*)', redirect: '/' },
  ],
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.initialized) await auth.bootstrap()

  if (!to.meta.public && !auth.user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (to.name === 'login' && auth.user) {
    return auth.activeTenantId ? { name: 'dashboard' } : { name: 'no-tenant' }
  }

  if (auth.user && !auth.activeTenantId && to.name !== 'no-tenant' && to.name !== 'login') {
    return { name: 'no-tenant' }
  }

  if (auth.user && auth.activeTenantId && to.name === 'no-tenant') {
    return { name: 'dashboard' }
  }

  // Menu authorization check
  const requiredMenu = to.meta.menu_key as MenuKey | undefined
  if (requiredMenu && auth.user && !auth.hasMenu(requiredMenu)) {
    return { name: 'dashboard', query: { denied: requiredMenu } }
  }
})

export default router

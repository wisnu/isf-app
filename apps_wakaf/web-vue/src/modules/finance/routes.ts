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
    component: () => import('./views/master/coa/CoaView.vue'),
    meta: { title: 'Chart of Accounts', menu_key: 'finance.coa' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/cash',
    name: 'finance-cash',
    component: () => import('./views/master/cash/CashView.vue'),
    meta: { title: 'Manajemen Kas', menu_key: 'finance.cash' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/bank',
    name: 'finance-bank',
    component: () => import('./views/master/bank/BankView.vue'),
    meta: { title: 'Manajemen Bank', menu_key: 'finance.bank' as MenuKey, domain: 'finance' },
  },
  {
    path: '/finance/master/budget-owner',
    name: 'finance-master-budget-owner',
    component: () => import('./views/master/budget-owner/BudgetOwnerView.vue'),
    meta: { title: 'Pemilik Anggaran', menu_key: 'finance.parameter.budget_owner' as MenuKey, domain: 'finance' },
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
]

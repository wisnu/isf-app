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
      component: () => import('@/pages/DashboardPage.vue'),
      meta: { title: 'Dashboard', menu_key: 'dashboard.overview' as MenuKey },
    },
    {
      path: '/finance/coa',
      name: 'finance-coa',
      component: () => import('@/pages/finance/CoaPage.vue'),
      meta: { title: 'Chart of Accounts', menu_key: 'finance.coa' as MenuKey },
    },
    {
      path: '/finance/cash',
      name: 'finance-cash',
      component: () => import('@/pages/finance/KasPage.vue'),
      meta: { title: 'Manajemen Kas', menu_key: 'finance.cash' as MenuKey },
    },
    {
      path: '/finance/bank',
      name: 'finance-bank',
      component: () => import('@/pages/finance/BankPage.vue'),
      meta: { title: 'Manajemen Bank', menu_key: 'finance.bank' as MenuKey },
    },
    {
      path: '/finance/reports/daily-journal',
      name: 'finance-reports-daily-journal',
      component: () => import('@/pages/finance/reports/ReportDailyJournalPage.vue'),
      meta: {
        title: 'Laporan Jurnal Harian',
        menu_key: 'finance.reports.daily_journal' as MenuKey,
      },
    },
    {
      path: '/finance/reports/general-transaction',
      name: 'finance-reports-general-transaction',
      component: () => import('@/pages/finance/reports/ReportGeneralTransactionPage.vue'),
      meta: {
        title: 'List Transaksi Umum',
        menu_key: 'finance.reports.general_transaction' as MenuKey,
      },
    },
    {
      path: '/finance/reports/daily-cash',
      name: 'finance-reports-daily-cash',
      component: () => import('@/pages/finance/reports/ReportCashDailyPage.vue'),
      meta: {
        title: 'Transaksi Kas/Bank Harian',
        menu_key: 'finance.reports.daily_cash' as MenuKey,
      },
    },
    {
      path: '/finance/reports/cash-summary',
      name: 'finance-reports-cash-summary',
      component: () => import('@/pages/finance/reports/ReportCashSummaryPage.vue'),
      meta: {
        title: 'Rekapitulasi Transaksi Kas/Bank',
        menu_key: 'finance.reports.cash_summary' as MenuKey,
      },
    },
    {
      path: '/finance/reports/monthly-balance',
      name: 'finance-reports-monthly-balance',
      component: () => import('@/pages/finance/reports/ReportCashMonthlyPage.vue'),
      meta: {
        title: 'Monitoring Saldo Kas/Bank Bulanan',
        menu_key: 'finance.reports.monthly_balance' as MenuKey,
      },
    },
    {
      path: '/dashboard/finance',
      name: 'dashboard-finance',
      component: () => import('@/pages/DashboardFinancePage.vue'),
      meta: { title: 'Dashboard Keuangan', menu_key: 'dashboard.finance' as MenuKey },
    },
    {
      path: '/dashboard/distribution',
      name: 'dashboard-distribution',
      component: () => import('@/pages/DashboardDistributionPage.vue'),
      meta: { title: 'Dashboard Penyaluran', menu_key: 'dashboard.distribution' as MenuKey },
    },
    {
      path: '/dashboard/collection',
      name: 'dashboard-collection',
      component: () => import('@/pages/DashboardCollectionPage.vue'),
      meta: { title: 'Dashboard Penghimpunan', menu_key: 'dashboard.collection' as MenuKey },
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
      path: '/parameter/budget-owner',
      name: 'parameter-budget-owner',
      component: () => import('@/pages/parameter/BudgetOwnerPage.vue'),
      meta: { title: 'Pemilik Anggaran', menu_key: 'finance.parameter.budget_owner' as MenuKey },
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

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
      path: '/keuangan/coa',
      name: 'keuangan-coa',
      component: () => import('@/pages/keuangan/CoaPage.vue'),
      meta: { title: 'Chart of Accounts', menu_key: 'keuangan.coa' as MenuKey },
    },
    {
      path: '/keuangan/kas',
      name: 'keuangan-kas',
      component: () => import('@/pages/keuangan/KasPage.vue'),
      meta: { title: 'Manajemen Kas', menu_key: 'keuangan.kas' as MenuKey },
    },
    {
      path: '/keuangan/bank',
      name: 'keuangan-bank',
      component: () => import('@/pages/keuangan/BankPage.vue'),
      meta: { title: 'Manajemen Bank', menu_key: 'keuangan.bank' as MenuKey },
    },
    {
      path: '/keuangan/laporan/jurnal-harian',
      name: 'keuangan-laporan-jurnal-harian',
      component: () => import('@/pages/keuangan/LaporanJurnalHarianPage.vue'),
      meta: {
        title: 'Laporan Jurnal Harian',
        menu_key: 'keuangan.report.journal_daily' as MenuKey,
      },
    },
    {
      path: '/dashboard/keuangan',
      name: 'dashboard-keuangan',
      component: () => import('@/pages/DashboardKeuanganPage.vue'),
      meta: { title: 'Dashboard Keuangan', menu_key: 'dashboard.keuangan' as MenuKey },
    },
    {
      path: '/dashboard/penyaluran',
      name: 'dashboard-penyaluran',
      component: () => import('@/pages/DashboardPenyaluranPage.vue'),
      meta: { title: 'Dashboard Penyaluran', menu_key: 'dashboard.penyaluran' as MenuKey },
    },
    {
      path: '/dashboard/penghimpunan',
      name: 'dashboard-penghimpunan',
      component: () => import('@/pages/DashboardPenghimpunanPage.vue'),
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

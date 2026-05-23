import { createRouter, createWebHistory } from 'vue-router'

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
      meta: { title: 'Dashboard' },
    },
    {
      path: '/keuangan/coa',
      name: 'keuangan-coa',
      component: () => import('@/pages/keuangan/CoaPage.vue'),
      meta: { title: 'Chart of Accounts' },
    },
    {
      path: '/keuangan/kas',
      name: 'keuangan-kas',
      component: () => import('@/pages/keuangan/KasPage.vue'),
      meta: { title: 'Manajemen Kas' },
    },
    {
      path: '/keuangan/bank',
      name: 'keuangan-bank',
      component: () => import('@/pages/keuangan/BankPage.vue'),
      meta: { title: 'Manajemen Bank' },
    },
    {
      path: '/dashboard/keuangan',
      name: 'dashboard-keuangan',
      component: () => import('@/pages/DashboardKeuanganPage.vue'),
      meta: { title: 'Dashboard Keuangan' },
    },
    {
      path: '/dashboard/penyaluran',
      name: 'dashboard-penyaluran',
      component: () => import('@/pages/DashboardPenyaluranPage.vue'),
      meta: { title: 'Dashboard Penyaluran' },
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

  if (
    auth.user &&
    !auth.activeTenantId &&
    to.name !== 'no-tenant' &&
    to.name !== 'login'
  ) {
    return { name: 'no-tenant' }
  }

  if (auth.user && auth.activeTenantId && to.name === 'no-tenant') {
    return { name: 'dashboard' }
  }
})

export default router

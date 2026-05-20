import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/pages/LoginPage.vue'),
      meta: { public: true },
    },
    {
      path: '/no-tenant',
      name: 'no-tenant',
      component: () => import('@/pages/NoTenantPage.vue'),
      meta: { requiresNoTenant: true },
    },
    { path: '/', name: 'dashboard', component: () => import('@/pages/DashboardPage.vue') },
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
})

export default router

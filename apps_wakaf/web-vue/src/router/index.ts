import { createRouter, createWebHistory } from 'vue-router'

import { financeRoutes }        from '@/modules/finance/routes'
import { administrationRoutes } from '@/modules/administration/routes'
import { fundraisingRoutes }    from '@/modules/fundraising/routes'
import { distributionRoutes }   from '@/modules/distribution/routes'
import { enterpriseRoutes }     from '@/modules/enterprise/routes'
import { registerGuards }       from '@/app/router/guards'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // ── App-level routes ──────────────────────────────────────────────────
    {
      path: '/login',
      name: 'login',
      component: () => import('@/app/views/LoginView.vue'),
      meta: { public: true, title: 'Masuk' },
    },
    {
      path: '/no-tenant',
      name: 'no-tenant',
      component: () => import('@/app/views/NoTenantView.vue'),
      meta: { requiresNoTenant: true, title: 'Akun' },
    },
    {
      path: '/profile/password',
      name: 'profile-password',
      component: () => import('@/app/views/profile/PasswordView.vue'),
      meta: { title: 'Ganti Password' },
    },

    // ── Domain module routes ──────────────────────────────────────────────
    ...financeRoutes,
    ...administrationRoutes,
    ...fundraisingRoutes,
    ...distributionRoutes,
    ...enterpriseRoutes,

    { path: '/:catchAll(.*)', redirect: '/' },
  ],
})

registerGuards(router)

export default router

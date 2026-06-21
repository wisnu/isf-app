import type { Router } from 'vue-router'
import type { MenuKey } from '@/shared/constants/menu-keys'
import { useAuthStore } from '@/app/stores/auth.store'

export function registerGuards(router: Router) {
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

    const requiredMenu = to.meta.menu_key as MenuKey | undefined
    if (requiredMenu && auth.user && !auth.hasMenu(requiredMenu)) {
      return { name: 'dashboard', query: { denied: requiredMenu } }
    }
  })
}

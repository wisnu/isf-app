import { computed, shallowRef } from 'vue'
import { defineStore } from 'pinia'

import { api, ApiError } from '@/lib/api/client'
import type { MenuKey } from '@/lib/menu/registry'

export interface Tenant { id: string; name: string }
export interface User {
  username: string
  name: string
  tenants: Tenant[]
  default_tenant: string | null
  roles: string[]
  branches: string[]
  primary_branch: string | null
  menus: string[]
  branch_access?: 'all' | 'single'
}

export interface AuthProviders {
  password: boolean
  google: boolean
}

export const useAuthStore = defineStore('auth', () => {
  const initialized = shallowRef(false)
  const user = shallowRef<User | null>(null)
  const activeTenantId = shallowRef<string | null>(null)
  const providers = shallowRef<AuthProviders>({ password: true, google: false })
  const providersLoaded = shallowRef(false)

  const activeTenant = computed<Tenant | null>(() => {
    if (!user.value || !activeTenantId.value) return null
    return user.value.tenants.find((t) => t.id === activeTenantId.value) ?? null
  })
  const hasTenant = computed(() => Boolean(activeTenantId.value))
  const menus = computed(() => user.value?.menus ?? [])

  function hasMenu(key: MenuKey | string): boolean {
    return Boolean(user.value && user.value.menus.includes(key))
  }

  async function loadProviders() {
    if (providersLoaded.value) return
    try {
      const result = await api.get<AuthProviders>('/api/auth/providers')
      providers.value = result
    } catch {
      // fallback to defaults
    } finally {
      providersLoaded.value = true
    }
  }

  async function bootstrap() {
    try {
      const me = await api.get<{ user: User; active_tenant_id: string | null }>('/api/auth/me')
      user.value = me.user
      activeTenantId.value = me.active_tenant_id
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        user.value = null
        activeTenantId.value = null
      } else {
        throw e
      }
    } finally {
      initialized.value = true
    }
  }

  async function login(username: string, password: string) {
    const result = await api.post<{ user: User; active_tenant_id: string }>(
      '/api/auth/login', { username, password },
    )
    user.value = result.user
    activeTenantId.value = result.active_tenant_id
  }

  async function logout() {
    try {
      await api.post('/api/auth/logout')
    } finally {
      user.value = null
      activeTenantId.value = null
    }
  }

  async function switchTenant(tenantId: string) {
    const result = await api.post<{ active_tenant_id: string }>(
      '/api/tenants/switch', { tenant_id: tenantId },
    )
    activeTenantId.value = result.active_tenant_id
  }

  async function refreshProfile() {
    await api.post('/api/auth/refresh-profile')
    const me = await api.get<{ user: User; active_tenant_id: string | null }>('/api/auth/me')
    user.value = me.user
    activeTenantId.value = me.active_tenant_id
  }

  return {
    initialized,
    user,
    activeTenantId,
    providers,
    providersLoaded,
    activeTenant,
    hasTenant,
    menus,
    hasMenu,
    loadProviders,
    bootstrap,
    login,
    logout,
    switchTenant,
    refreshProfile,
  }
})

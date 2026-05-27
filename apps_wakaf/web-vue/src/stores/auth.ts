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
}

export interface AuthProviders {
  password: boolean
  google: boolean
}

interface State {
  initialized: boolean
  user: User | null
  activeTenantId: string | null
  providers: AuthProviders
  providersLoaded: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): State => ({
    initialized: false,
    user: null,
    activeTenantId: null,
    providers: { password: true, google: false },
    providersLoaded: false,
  }),
  getters: {
    activeTenant(state): Tenant | null {
      if (!state.user || !state.activeTenantId) return null
      return state.user.tenants.find((t) => t.id === state.activeTenantId) ?? null
    },
    hasTenant(state): boolean {
      return Boolean(state.activeTenantId)
    },
    menus(state): string[] {
      return state.user?.menus ?? []
    },
    hasMenu(state) {
      return (key: MenuKey | string): boolean =>
        Boolean(state.user && state.user.menus.includes(key))
    },
  },
  actions: {
    async loadProviders() {
      if (this.providersLoaded) return
      try {
        const result = await api.get<AuthProviders>('/api/auth/providers')
        this.providers = result
      } catch {
        // fallback to defaults
      } finally {
        this.providersLoaded = true
      }
    },

    async bootstrap() {
      try {
        const me = await api.get<{ user: User; active_tenant_id: string | null }>('/api/auth/me')
        this.user = me.user
        this.activeTenantId = me.active_tenant_id
      } catch (e) {
        if (e instanceof ApiError && e.status === 401) {
          this.user = null
          this.activeTenantId = null
        } else {
          throw e
        }
      } finally {
        this.initialized = true
      }
    },

    async login(username: string, password: string) {
      const result = await api.post<{ user: User; active_tenant_id: string }>(
        '/api/auth/login', { username, password },
      )
      this.user = result.user
      this.activeTenantId = result.active_tenant_id
    },

    async logout() {
      try {
        await api.post('/api/auth/logout')
      } finally {
        this.user = null
        this.activeTenantId = null
      }
    },

    async switchTenant(tenantId: string) {
      const result = await api.post<{ active_tenant_id: string }>(
        '/api/tenants/switch', { tenant_id: tenantId },
      )
      this.activeTenantId = result.active_tenant_id
      console.log('[audit] tenant switched', {
        tenant_id: tenantId,
        at: new Date().toISOString(),
      })
    },

    async refreshProfile() {
      await api.post('/api/auth/refresh-profile')
      // Re-bootstrap untuk dapat user shape baru dari /me
      const me = await api.get<{ user: User; active_tenant_id: string | null }>('/api/auth/me')
      this.user = me.user
      this.activeTenantId = me.active_tenant_id
    },
  },
})

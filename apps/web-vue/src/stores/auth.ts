import { defineStore } from 'pinia'

import { api, ApiError } from '@/lib/api/client'

export interface Tenant { id: string; name: string }
export interface User {
  username: string
  name: string
  tenants: Tenant[]
  default_tenant: string
}

interface State {
  initialized: boolean
  user: User | null
  activeTenantId: string | null
}

export const useAuthStore = defineStore('auth', {
  state: (): State => ({ initialized: false, user: null, activeTenantId: null }),
  getters: {
    activeTenant(state): Tenant | null {
      if (!state.user || !state.activeTenantId) return null
      return state.user.tenants.find((t) => t.id === state.activeTenantId) ?? null
    },
  },
  actions: {
    async bootstrap() {
      try {
        const me = await api.get<{ user: User; active_tenant_id: string }>('/api/auth/me')
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
        '/api/auth/login',
        { username, password },
      )
      this.user = result.user
      this.activeTenantId = result.active_tenant_id
    },
    async logout() {
      await api.post('/api/auth/logout')
      this.user = null
      this.activeTenantId = null
    },
    async switchTenant(tenantId: string) {
      const result = await api.post<{ active_tenant_id: string }>(
        '/api/tenants/switch',
        { tenant_id: tenantId },
      )
      this.activeTenantId = result.active_tenant_id
      console.log('[audit] tenant switched', { tenant_id: tenantId, at: new Date().toISOString() })
    },
  },
})

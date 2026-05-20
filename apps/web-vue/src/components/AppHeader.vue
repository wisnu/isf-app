<script setup lang="ts">
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function onSwitch(event: Event) {
  const tenantId = (event.target as HTMLSelectElement).value
  if (tenantId && tenantId !== auth.activeTenantId) {
    await auth.switchTenant(tenantId)
  }
}

async function logout() {
  await auth.logout()
  router.replace({ name: 'login' })
}
</script>

<template>
  <header class="header">
    <div class="brand">
      <strong>isf-app</strong>
      <span class="muted">· Portal ZISWAF</span>
    </div>
    <div class="actions" v-if="auth.user">
      <label class="tenant-switcher">
        <span class="muted">Perusahaan</span>
        <select :value="auth.activeTenantId ?? ''" @change="onSwitch">
          <option v-for="t in auth.user.tenants" :key="t.id" :value="t.id">{{ t.name }}</option>
        </select>
      </label>
      <span class="user muted">{{ auth.user.name }}</span>
      <button @click="logout">Logout</button>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.brand { display: flex; gap: 0.4rem; align-items: baseline; }
.muted { color: var(--color-text-muted); font-size: 0.85rem; }
.actions { display: flex; align-items: center; gap: 1rem; }
.tenant-switcher { display: flex; flex-direction: column; gap: 0.2rem; font-size: 0.75rem; }
.tenant-switcher select { width: auto; min-width: 200px; }
.user { white-space: nowrap; }
</style>

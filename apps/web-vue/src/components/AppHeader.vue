<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const auth = useAuthStore()
const theme = useThemeStore()
const router = useRouter()

const activeTenantName = computed(
  () => auth.user?.tenants.find((t) => t.id === auth.activeTenantId)?.name ?? '—'
)

async function onSwitch(tenantId: string) {
  if (tenantId !== auth.activeTenantId) {
    await auth.switchTenant(tenantId)
  }
}

async function logout() {
  await auth.logout()
  router.replace({ name: 'login' })
}
</script>

<template>
  <q-header elevated>
    <q-toolbar>
      <q-toolbar-title>
        <span class="text-weight-bold">isf-app</span>
        <span class="text-caption q-ml-xs">· Portal ZISWAF</span>
      </q-toolbar-title>

      <q-btn-dropdown
        v-if="auth.user"
        flat
        no-caps
        icon="apartment"
        :label="activeTenantName"
      >
        <q-list>
          <q-item
            v-for="t in auth.user.tenants"
            :key="t.id"
            v-close-popup
            clickable
            @click="onSwitch(t.id)"
          >
            <q-item-section avatar style="min-width: 32px">
              <q-icon
                v-if="t.id === auth.activeTenantId"
                name="check"
                color="positive"
              />
            </q-item-section>
            <q-item-section>{{ t.name }}</q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>

      <q-space />

      <span v-if="auth.user" class="text-caption q-mr-sm">{{ auth.user.name }}</span>

      <q-btn
        flat
        round
        dense
        :icon="theme.isDark ? 'light_mode' : 'dark_mode'"
        :title="theme.isDark ? 'Light mode' : 'Dark mode'"
        @click="theme.toggle"
      />

      <q-btn flat dense label="Logout" icon-right="logout" @click="logout" />
    </q-toolbar>
  </q-header>
</template>

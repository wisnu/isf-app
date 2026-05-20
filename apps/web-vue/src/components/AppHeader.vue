<script setup lang="ts">
import { Building2, Check, LogOut, Moon, Sun } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import NotificationBell from '@/components/NotificationBell.vue'
import SystemDate from '@/components/SystemDate.vue'
import Button from '@/components/ui/Button.vue'
import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import DropdownMenuItem from '@/components/ui/DropdownMenuItem.vue'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const auth = useAuthStore()
const theme = useThemeStore()
const router = useRouter()

const activeTenantName = computed(
  () => auth.user?.tenants.find((t) => t.id === auth.activeTenantId)?.name ?? '—',
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
  <header
    class="bg-primary text-primary-foreground border-b border-border px-4 sm:px-6 py-3 flex items-center justify-between gap-3 sm:gap-4 shrink-0"
  >
    <div class="flex items-baseline gap-1.5 min-w-0">
      <span class="font-bold text-base sm:text-lg">isf-app</span>
      <span class="text-xs opacity-80 max-sm:hidden">· Portal ZISWAF</span>
    </div>

    <div class="flex items-center gap-2 sm:gap-3">
      <SystemDate />

      <DropdownMenu v-if="auth.user">
        <template #trigger>
          <Button
            variant="ghost-on-primary"
            size="sm"
            class="gap-2 max-w-[180px] sm:max-w-none"
          >
            <Building2 class="w-4 h-4 shrink-0" />
            <span class="truncate">{{ activeTenantName }}</span>
          </Button>
        </template>
        <DropdownMenuItem
          v-for="t in auth.user.tenants"
          :key="t.id"
          @click="onSwitch(t.id)"
        >
          <Check
            v-if="t.id === auth.activeTenantId"
            class="w-4 h-4 text-positive shrink-0"
          />
          <span v-else class="w-4 h-4 shrink-0" aria-hidden="true" />
          <span>{{ t.name }}</span>
        </DropdownMenuItem>
      </DropdownMenu>

      <span v-if="auth.user" class="text-xs opacity-90 max-sm:hidden">
        {{ auth.user.name }}
      </span>

      <NotificationBell v-if="auth.user" />

      <Button
        variant="ghost-on-primary"
        size="icon"
        :title="theme.isDark ? 'Light mode' : 'Dark mode'"
        @click="theme.toggle"
      >
        <Sun v-if="theme.isDark" class="w-4 h-4" />
        <Moon v-else class="w-4 h-4" />
      </Button>

      <Button
        variant="ghost-on-primary"
        size="sm"
        title="Logout"
        @click="logout"
      >
        <LogOut class="w-4 h-4" />
        <span class="max-sm:sr-only">Logout</span>
      </Button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { Building2, Check, ChevronDown, Menu } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import AppLogo from '@/layouts/AppLogo.vue'
import NotificationBell from '@/layouts/NotificationBell.vue'
import SystemDate from '@/layouts/SystemDate.vue'
import UserMenu from '@/layouts/UserMenu.vue'
import DropdownMenu from '@/shared/components/DropdownMenu.vue'
import DropdownMenuItem from '@/shared/components/DropdownMenuItem.vue'
import { cn } from '@/shared/utils/utils'
import { useAuthStore } from '@/app/stores/auth.store'
import { useSidebarStore } from '@/app/stores/sidebar.store'

const auth = useAuthStore()
const sidebar = useSidebarStore()
const route = useRoute()

const pageTitle = computed(() => (route.meta.title as string | undefined) ?? '')

const activeTenantName = computed(
  () => auth.user?.tenants.find((t) => t.id === auth.activeTenantId)?.name ?? '—',
)

async function onSwitch(tenantId: string) {
  if (tenantId !== auth.activeTenantId) {
    await auth.switchTenant(tenantId)
  }
}
</script>

<template>
  <header
    class="bg-primary text-primary-foreground border-b border-border h-12 px-3 sm:px-4 flex items-center justify-between gap-2 sm:gap-3 shrink-0"
  >
    <div class="flex items-center gap-2 sm:gap-3 min-w-0">
      <button
        v-if="auth.user"
        type="button"
        :class="
          cn(
            'hidden lg:inline-flex h-8 w-8 items-center justify-center rounded-md',
            'hover:bg-white/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40',
          )
        "
        :title="sidebar.collapsed ? 'Buka sidebar' : 'Tutup sidebar'"
        @click="sidebar.toggle"
      >
        <Menu class="w-4 h-4" />
      </button>

      <div class="lg:hidden flex items-center gap-1.5">
        <AppLogo class="w-5 h-5" />
        <span class="font-semibold text-sm">isf-app</span>
      </div>

      <span class="text-sm font-medium opacity-95 truncate max-sm:hidden">
        {{ pageTitle }}
      </span>
    </div>

    <div class="flex items-center gap-1.5 sm:gap-2">
      <DropdownMenu v-if="auth.user">
        <template #trigger>
          <button
            type="button"
            :class="
              cn(
                'h-8 px-2.5 inline-flex items-center gap-1.5 rounded-md bg-white/10',
                'hover:bg-white/20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40',
              )
            "
            :title="'Perusahaan aktif: ' + activeTenantName"
          >
            <Building2 class="w-3.5 h-3.5 shrink-0" />
            <span class="text-xs sm:text-sm truncate max-w-[120px] sm:max-w-[200px]">
              {{ activeTenantName }}
            </span>
            <ChevronDown class="w-3 h-3 opacity-70 shrink-0" />
          </button>
        </template>
        <div class="px-3 py-1.5 text-[10px] uppercase tracking-wider text-muted font-semibold">
          Pilih Perusahaan
        </div>
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

      <SystemDate />
      <!-- TODO(fase-akhir): aktifkan kembali ikon notifikasi (ganti v-if="false" → "auth.user") -->
      <NotificationBell v-if="false" />
      <UserMenu v-if="auth.user" />
    </div>
  </header>
</template>

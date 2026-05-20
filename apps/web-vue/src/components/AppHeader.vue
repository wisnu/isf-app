<script setup lang="ts">
import { Menu } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import AppLogo from '@/components/AppLogo.vue'
import NotificationBell from '@/components/NotificationBell.vue'
import SystemDate from '@/components/SystemDate.vue'
import UserMenu from '@/components/UserMenu.vue'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/stores/auth'
import { useSidebarStore } from '@/stores/sidebar'

const auth = useAuthStore()
const sidebar = useSidebarStore()
const route = useRoute()

const pageTitle = computed(() => (route.meta.title as string | undefined) ?? '')
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

      <span class="text-sm font-medium opacity-95 truncate">{{ pageTitle }}</span>
    </div>

    <div class="flex items-center gap-1.5 sm:gap-2">
      <SystemDate />
      <NotificationBell v-if="auth.user" />
      <UserMenu v-if="auth.user" />
    </div>
  </header>
</template>

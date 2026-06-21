<script setup lang="ts">
import { LogOut, Moon, Sun, UserCircle2 } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import UserAvatar from '@/layouts/UserAvatar.vue'
import DropdownMenu from '@/shared/components/DropdownMenu.vue'
import { cn } from '@/shared/utils/utils'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const auth = useAuthStore()
const theme = useThemeStore()
const router = useRouter()

const username = computed(() => auth.user?.username ?? '')
const displayName = computed(() => auth.user?.name ?? '')
const email = computed(() =>
  username.value.includes('@') ? username.value : `${username.value}@isf.local`,
)

const roles = computed<string[]>(() => {
  const u = username.value
  if (u === 'admin') return ['Administrator', 'Multi-tenant']
  if (u.startsWith('finance.')) return ['Finance']
  return ['Member']
})

async function logout() {
  await auth.logout()
  router.replace({ name: 'login' })
}
</script>

<template>
  <DropdownMenu content-class="w-72 p-0">
    <template #trigger>
      <button
        type="button"
        :class="
          cn(
            'h-8 px-1 inline-flex items-center gap-2 rounded-md',
            'hover:bg-white/10 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40',
          )
        "
        :title="displayName"
      >
        <UserAvatar :name="displayName" size="sm" />
      </button>
    </template>

    <!-- Header: avatar + name + handle + email -->
    <div class="px-4 py-3 border-b border-border flex items-start gap-3">
      <UserAvatar :name="displayName" size="lg" class="bg-primary text-primary-foreground" />
      <div class="min-w-0 flex-1">
        <p class="text-sm font-semibold text-foreground truncate">{{ displayName }}</p>
        <p class="text-xs text-muted truncate">@{{ username }}</p>
        <p class="text-xs text-muted truncate">{{ email }}</p>
      </div>
    </div>

    <!-- Roles -->
    <div class="px-4 py-2.5 border-b border-border">
      <p class="text-[10px] uppercase tracking-wider text-muted font-semibold mb-1.5">Roles</p>
      <div class="flex flex-wrap gap-1.5">
        <span
          v-for="r in roles"
          :key="r"
          class="text-xs bg-background border border-border text-foreground px-2 py-0.5 rounded-full"
        >{{ r }}</span>
      </div>
    </div>

    <!-- Actions -->
    <div class="py-1">
      <button
        type="button"
        class="w-full flex items-center gap-2 px-4 py-2 text-sm text-muted cursor-not-allowed"
        disabled
        title="Tersedia di Fase 4"
      >
        <UserCircle2 class="w-4 h-4" />
        <span>Profil Saya</span>
        <span class="ml-auto text-[10px] uppercase tracking-wide">Fase 4</span>
      </button>

      <button
        type="button"
        class="w-full flex items-center gap-2 px-4 py-2 text-sm text-foreground hover:bg-background"
        @click="theme.toggle()"
      >
        <Sun v-if="theme.isDark" class="w-4 h-4" />
        <Moon v-else class="w-4 h-4" />
        <span>{{ theme.isDark ? 'Mode terang' : 'Mode gelap' }}</span>
      </button>

      <div class="border-t border-border my-1" />

      <button
        type="button"
        class="w-full flex items-center gap-2 px-4 py-2 text-sm text-destructive hover:bg-destructive/10"
        @click="logout()"
      >
        <LogOut class="w-4 h-4" />
        <span>Logout</span>
      </button>
    </div>
  </DropdownMenu>
</template>

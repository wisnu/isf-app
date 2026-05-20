<script setup lang="ts">
import {
  ChevronsLeft,
  ChevronsRight,
  FileText,
  HandCoins,
  LayoutDashboard,
  Settings,
  TrendingUp,
  Users,
  Wallet,
} from 'lucide-vue-next'
import type { FunctionalComponent } from 'vue'
import { useRoute } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import { cn } from '@/lib/utils'
import { useSidebarStore } from '@/stores/sidebar'

interface MenuItem {
  label: string
  to?: string
  icon: FunctionalComponent
  disabled?: boolean
  badge?: string
}

interface MenuGroup {
  label: string
  items: MenuItem[]
}

const groups: MenuGroup[] = [
  {
    label: 'Utama',
    items: [{ label: 'Dashboard', to: '/', icon: LayoutDashboard }],
  },
  {
    label: 'Domain ZISWAF',
    items: [
      { label: 'Keuangan', icon: Wallet, disabled: true, badge: 'Fase 2' },
      { label: 'Program', icon: HandCoins, disabled: true, badge: 'Fase 3' },
      { label: 'Penghimpunan', icon: TrendingUp, disabled: true, badge: 'Fase 3' },
    ],
  },
  {
    label: 'Administrasi',
    items: [
      { label: 'Manajemen User', icon: Users, disabled: true, badge: 'Fase 4' },
      { label: 'Back Office', icon: Settings, disabled: true, badge: 'Fase 4' },
      { label: 'Audit Log', icon: FileText, disabled: true, badge: 'Fase 4' },
    ],
  },
]

const sidebar = useSidebarStore()
const route = useRoute()
const isActive = (item: MenuItem) => Boolean(item.to && route.path === item.to)
</script>

<template>
  <aside
    :class="
      cn(
        'hidden lg:flex shrink-0 border-r border-border bg-surface flex-col py-4 transition-[width] duration-200',
        sidebar.collapsed ? 'w-16' : 'w-60',
      )
    "
  >
    <div
      class="px-3 mb-3 flex"
      :class="sidebar.collapsed ? 'justify-center' : 'justify-end'"
    >
      <Button
        variant="ghost"
        size="icon"
        :title="sidebar.collapsed ? 'Perluas sidebar' : 'Kecilkan sidebar'"
        @click="sidebar.toggle"
      >
        <ChevronsRight v-if="sidebar.collapsed" class="w-4 h-4" />
        <ChevronsLeft v-else class="w-4 h-4" />
      </Button>
    </div>

    <nav class="flex flex-col gap-4 px-3 flex-1">
      <div v-for="group in groups" :key="group.label" class="flex flex-col gap-1">
        <div
          v-if="!sidebar.collapsed"
          class="px-3 text-[10px] uppercase tracking-wider text-muted font-semibold"
        >
          {{ group.label }}
        </div>
        <component
          :is="item.disabled || !item.to ? 'div' : 'router-link'"
          v-for="item in group.items"
          :key="item.label"
          :to="item.to"
          :title="sidebar.collapsed ? item.label + (item.badge ? ' · ' + item.badge : '') : undefined"
          :class="
            cn(
              'flex items-center gap-3 rounded-md text-sm transition-colors',
              sidebar.collapsed ? 'justify-center px-2 py-2' : 'px-3 py-2',
              item.disabled
                ? 'text-muted cursor-not-allowed'
                : isActive(item)
                  ? 'bg-primary/10 text-primary font-medium'
                  : 'text-foreground hover:bg-background',
            )
          "
        >
          <component :is="item.icon" class="w-4 h-4 shrink-0" />
          <span v-if="!sidebar.collapsed" class="flex-1 truncate">{{ item.label }}</span>
          <span
            v-if="!sidebar.collapsed && item.badge"
            class="text-[10px] uppercase tracking-wide bg-background text-muted px-1.5 py-0.5 rounded"
          >{{ item.badge }}</span>
        </component>
      </div>
    </nav>

    <div
      v-if="!sidebar.collapsed"
      class="px-6 pt-3 mt-auto text-xs text-muted border-t border-border"
    >
      v0.2.0 · Fase 1 MVP
    </div>
    <div
      v-else
      class="px-3 pt-3 mt-auto text-[10px] text-muted text-center border-t border-border"
      :title="'v0.2.0 · Fase 1 MVP'"
    >
      v0.2
    </div>
  </aside>
</template>

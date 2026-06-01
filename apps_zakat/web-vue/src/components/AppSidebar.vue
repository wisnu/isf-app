<script setup lang="ts">
import {
  BarChart3,
  Banknote,
  BookOpen,
  ChevronDown,
  FileText,
  HandCoins,
  Landmark,
  LayoutDashboard,
  PieChart,
  Settings,
  TrendingUp,
  Users,
  Wallet,
} from 'lucide-vue-next'
import type { FunctionalComponent } from 'vue'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import AppLogo from '@/components/AppLogo.vue'
import { cn } from '@/lib/utils'
import { portalLabel } from '@/lib/portal'
import { useSidebarStore } from '@/stores/sidebar'

interface MenuItem {
  label?: string
  to?: string
  icon?: FunctionalComponent
  disabled?: boolean
  badge?: string
  children?: MenuItem[]
  section?: string // sub-heading di dalam daftar children (bukan item klik)
}

interface MenuGroup {
  label: string
  items: MenuItem[]
}

const groups: MenuGroup[] = [
  {
    label: 'Utama',
    items: [
      {
        label: 'Dashboard',
        icon: LayoutDashboard,
        children: [
          { label: 'Overview', to: '/', icon: LayoutDashboard },
          { label: 'Keuangan', to: '/dashboard/keuangan', icon: BarChart3 },
          { label: 'Penyaluran', to: '/dashboard/penyaluran', icon: PieChart },
          { label: 'Penghimpunan', to: '/dashboard/penghimpunan', icon: HandCoins },
        ],
      },
    ],
  },
  {
    label: 'Domain ZISWAF',
    items: [
      {
        label: 'Keuangan',
        icon: Wallet,
        children: [
          { label: 'Chart of Accounts', to: '/keuangan/coa', icon: BookOpen },
          { label: 'Kas', to: '/keuangan/kas', icon: Banknote },
          { label: 'Bank', to: '/keuangan/bank', icon: Landmark },
        ],
      },
      {
        label: 'Laporan',
        icon: FileText,
        children: [
          { section: 'Kas & Transaksi' },
          { label: 'Transaksi Kas/Bank Harian', to: '/keuangan/laporan/kas-harian', icon: Banknote },
          { label: 'Rekapitulasi Kas/Bank', to: '/keuangan/laporan/rekap-kas', icon: Banknote },
          { label: 'Monitoring Saldo Kas Bulanan', to: '/keuangan/laporan/saldo-bulanan', icon: Banknote },
          { label: 'Jurnal Harian', to: '/keuangan/laporan/jurnal-harian', icon: BookOpen },
          { label: 'List Transaksi Umum', to: '/keuangan/laporan/transaksi-umum', icon: BookOpen },
          { section: 'Akuntansi' },
          { label: 'Trial Balance', to: '/keuangan/laporan/trial-balance', icon: FileText },
          { label: 'Neraca', to: '/keuangan/laporan/neraca', icon: FileText },
          { label: 'Arus Kas', to: '/keuangan/laporan/arus-kas', icon: FileText },
          { label: 'Buku Besar', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'Perubahan Dana', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'Perubahan Dana Detail', icon: FileText, disabled: true, badge: 'Segera' },
          { section: 'Penghimpunan & Penyaluran' },
          { label: 'Penghimpunan Dana', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'Penyaluran Dana', icon: FileText, disabled: true, badge: 'Segera' },
          { section: 'Amil' },
          { label: 'Penerimaan Amil', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'Pengeluaran Amil', icon: FileText, disabled: true, badge: 'Segera' },
          { section: 'Piutang' },
          { label: 'Piutang pada Karyawan', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'Piutang pada Non-Karyawan', icon: FileText, disabled: true, badge: 'Segera' },
          { section: 'Uang Muka Kegiatan' },
          { label: 'Rekapitulasi Uang Muka Kegiatan', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'List Transaksi Uang Muka Kegiatan', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'Laporan Realisasi Project (Memo)', icon: FileText, disabled: true, badge: 'Segera' },
          { label: 'Piutang Realisasi Penyaluran', icon: FileText, disabled: true, badge: 'Segera' },
          { section: 'UPZ' },
          { label: 'List Transaksi UPZ', icon: FileText, disabled: true, badge: 'Segera' },
        ],
      },
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

const EXPANDED_KEY = 'isf-sidebar-expanded-groups'
const expandedParents = ref<Set<string>>(new Set())

function persistExpanded() {
  localStorage.setItem(EXPANDED_KEY, JSON.stringify([...expandedParents.value]))
}

function setExpanded(next: Set<string>) {
  expandedParents.value = next
  persistExpanded()
}

function toggleParent(label: string) {
  const copy = new Set(expandedParents.value)
  if (copy.has(label)) copy.delete(label)
  else copy.add(label)
  setExpanded(copy)
}

function autoExpandForRoute(path: string) {
  for (const g of groups) {
    for (const item of g.items) {
      if (item.children?.some((c) => c.to && path.startsWith(c.to))) {
        if (!expandedParents.value.has(item.label)) {
          const copy = new Set(expandedParents.value)
          copy.add(item.label)
          setExpanded(copy)
        }
      }
    }
  }
}

onMounted(() => {
  try {
    const raw = localStorage.getItem(EXPANDED_KEY)
    if (raw) expandedParents.value = new Set(JSON.parse(raw))
  } catch {
    // ignore
  }
  autoExpandForRoute(route.path)
})
watch(() => route.path, (p) => autoExpandForRoute(p))

function handleParentClick(item: MenuItem) {
  if (sidebar.collapsed) {
    sidebar.toggle()
    const copy = new Set(expandedParents.value)
    copy.add(item.label)
    setExpanded(copy)
  } else {
    toggleParent(item.label)
  }
}

const isExpanded = (label: string) => expandedParents.value.has(label)
const isActiveItem = (item: MenuItem) => Boolean(item.to && route.path === item.to)
const isActiveParent = (item: MenuItem) =>
  Boolean(item.children?.some((c) => c.to && route.path.startsWith(c.to)))

const parentBaseClass = computed(() =>
  sidebar.collapsed ? 'justify-center px-2 py-2' : 'px-3 py-2',
)
</script>

<template>
  <aside
    :class="
      cn(
        'hidden lg:flex shrink-0 border-r border-border bg-surface flex-col transition-[width] duration-200',
        sidebar.collapsed ? 'w-16' : 'w-72',
      )
    "
  >
    <!-- Brand header -->
    <div
      :class="
        cn(
          'h-12 flex items-center gap-2 border-b border-border bg-primary text-primary-foreground shrink-0',
          sidebar.collapsed ? 'justify-center px-2' : 'px-4',
        )
      "
    >
      <AppLogo class="w-7 h-7 shrink-0 rounded object-contain" />
      <div v-if="!sidebar.collapsed" class="flex flex-col leading-tight min-w-0">
        <span class="font-bold text-sm">isf-app</span>
        <span class="text-[10px] opacity-80 truncate">{{ portalLabel }}</span>
      </div>
    </div>

    <!-- Menu -->
    <nav class="flex flex-col gap-4 px-3 py-4 flex-1 overflow-y-auto">
      <div v-for="group in groups" :key="group.label" class="flex flex-col gap-1">
        <div
          v-if="!sidebar.collapsed"
          class="px-3 text-[10px] uppercase tracking-wider text-muted font-semibold"
        >
          {{ group.label }}
        </div>

        <template v-for="item in group.items" :key="item.label">
          <div class="flex flex-col">
            <!-- Parent with children -->
            <template v-if="item.children">
            <button
              type="button"
              :title="
                sidebar.collapsed
                  ? item.label + ': ' + item.children.filter((c) => c.label).map((c) => c.label).join(', ')
                  : undefined
              "
              :class="
                cn(
                  'flex items-center gap-3 rounded-md text-sm transition-colors w-full text-left',
                  parentBaseClass,
                  isActiveParent(item)
                    ? 'bg-primary/10 text-primary font-medium'
                    : 'text-foreground hover:bg-background',
                )
              "
              @click="handleParentClick(item)"
            >
              <component :is="item.icon" class="w-4 h-4 shrink-0" />
              <span v-if="!sidebar.collapsed" class="flex-1 truncate">{{ item.label }}</span>
              <ChevronDown
                v-if="!sidebar.collapsed"
                :class="[
                  'w-3.5 h-3.5 shrink-0 transition-transform duration-150',
                  isExpanded(item.label) ? '' : '-rotate-90',
                ]"
              />
            </button>

            <!-- Children list -->
            <div
              v-if="!sidebar.collapsed && isExpanded(item.label)"
              class="ml-4 mt-0.5 pl-3 border-l border-border flex flex-col gap-0.5"
            >
              <template v-for="(child, ci) in item.children" :key="child.section ?? child.label ?? ci">
                <!-- Sub-heading section -->
                <div
                  v-if="child.section"
                  class="px-2 pt-2 pb-0.5 text-[9px] uppercase tracking-wider text-muted/60 font-semibold first:pt-0.5"
                >{{ child.section }}</div>
                <!-- Active link -->
                <router-link
                  v-else-if="child.to && !child.disabled"
                  :to="child.to"
                  :class="
                    cn(
                      'flex items-center gap-2 px-2 py-1.5 rounded-md text-xs transition-colors',
                      isActiveItem(child)
                        ? 'bg-primary/10 text-primary font-medium'
                        : 'text-muted hover:text-foreground hover:bg-background',
                    )
                  "
                >
                  <component :is="child.icon" class="w-3.5 h-3.5 shrink-0" />
                  <span class="flex-1 truncate">{{ child.label }}</span>
                </router-link>
                <!-- Disabled placeholder -->
                <div
                  v-else
                  :title="child.label"
                  class="flex items-center gap-2 px-2 py-1.5 rounded-md text-xs text-muted/50 cursor-not-allowed"
                >
                  <component :is="child.icon" class="w-3.5 h-3.5 shrink-0" />
                  <span class="flex-1 truncate">{{ child.label }}</span>
                  <span
                    v-if="child.badge"
                    class="text-[9px] uppercase tracking-wide bg-background text-muted px-1 py-px rounded shrink-0"
                  >{{ child.badge }}</span>
                </div>
              </template>
            </div>
            </template>

            <!-- Standalone link (no children) -->
            <component
              v-else-if="!item.disabled && item.to"
              :is="'router-link'"
              :to="item.to"
              :title="sidebar.collapsed ? item.label : undefined"
              :class="
                cn(
                  'flex items-center gap-3 rounded-md text-sm transition-colors',
                  parentBaseClass,
                  isActiveItem(item)
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

            <!-- Disabled placeholder -->
            <div
              v-else
              :title="
                sidebar.collapsed
                  ? item.label + (item.badge ? ' · ' + item.badge : '')
                  : undefined
              "
              :class="
                cn(
                  'flex items-center gap-3 rounded-md text-sm text-muted cursor-not-allowed',
                  parentBaseClass,
                )
              "
            >
              <component :is="item.icon" class="w-4 h-4 shrink-0" />
              <span v-if="!sidebar.collapsed" class="flex-1 truncate">{{ item.label }}</span>
              <span
                v-if="!sidebar.collapsed && item.badge"
                class="text-[10px] uppercase tracking-wide bg-background text-muted px-1.5 py-0.5 rounded"
              >{{ item.badge }}</span>
            </div>
          </div>
        </template>
      </div>
    </nav>

    <div
      v-if="!sidebar.collapsed"
      class="px-4 py-3 text-xs text-muted border-t border-border"
    >
      v0.2.0 · Fase 1 MVP
    </div>
    <div
      v-else
      class="px-2 py-3 text-[10px] text-muted text-center border-t border-border"
      title="v0.2.0 · Fase 1 MVP"
    >
      v0.2
    </div>
  </aside>
</template>

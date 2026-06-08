<script setup lang="ts">
import {
  ArrowDownCircle,
  ArrowUpCircle,
  BarChart3,
  Banknote,
  BookOpen,
  ChevronDown,
  ClipboardCheck,
  ClipboardList,
  Clock,
  FileText,
  HandCoins,
  Landmark,
  LayoutDashboard,
  PieChart,
  Settings,
  ShieldCheck,
  TrendingUp,
  Upload,
  Users,
  Wallet,
} from 'lucide-vue-next'
import type { FunctionalComponent } from 'vue'
import { computed, onMounted, shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'

import AppLogo from '@/components/AppLogo.vue'
import { cn } from '@/lib/utils'
import { portalLabel } from '@/lib/portal'
import { useSidebarStore } from '@/stores/sidebar'
import { useAuthStore } from '@/stores/auth'
import type { MenuKey } from '@/lib/menu/registry'

interface MenuItem {
  label?: string
  to?: string
  icon?: FunctionalComponent
  disabled?: boolean
  badge?: string
  menu_key?: MenuKey | string
  children?: MenuItem[]
  section?: string
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
          { label: 'Overview',     to: '/',                       icon: LayoutDashboard, menu_key: 'dashboard.overview' },
          { label: 'Keuangan',    to: '/dashboard/keuangan',     icon: BarChart3,       menu_key: 'dashboard.keuangan' },
          { label: 'Penyaluran',  to: '/dashboard/penyaluran',   icon: PieChart,        menu_key: 'dashboard.penyaluran' },
          { label: 'Penghimpunan',to: '/dashboard/penghimpunan', icon: HandCoins,       menu_key: 'dashboard.penghimpunan' },
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
          { label: 'Chart of Accounts', to: '/keuangan/coa',  icon: BookOpen,  menu_key: 'keuangan.coa' },
          { label: 'Kas',               to: '/keuangan/kas',  icon: Banknote,  menu_key: 'keuangan.kas' },
          { label: 'Bank',              to: '/keuangan/bank',      icon: Landmark,  menu_key: 'keuangan.bank' },
          { label: 'Kas Kecil',        to: '/keuangan/kas-kecil', icon: Wallet,    menu_key: 'keuangan.kas_kecil' },
          { section: 'Monitoring dan Kontrol' },
          { label: 'Otorisasi',         to: '/keuangan/monitoring/otorisasi', icon: ShieldCheck, menu_key: 'keuangan.monitoring.otorisasi' },
          { label: 'Riwayat Submission', to: '/keuangan/monitoring/riwayat',   icon: ClipboardList, menu_key: 'keuangan.monitoring.riwayat' },
          { section: 'Transaksi' },
          { label: 'Histori Transaksi',     to: '/keuangan/transaksi/histori',     icon: Clock,           menu_key: 'keuangan.transaksi.histori' },
          { label: 'Input Penghimpunan Dana', to: '/keuangan/transaksi/penghimpunan', icon: ArrowUpCircle, menu_key: 'keuangan.transaksi.penghimpunan' },
          { label: 'Input Penyaluran Dana',   to: '/keuangan/transaksi/penyaluran',  icon: ArrowDownCircle, menu_key: 'keuangan.transaksi.penyaluran' },
          { section: 'Upload' },
          { label: 'Upload Penghimpunan', to: '/keuangan/upload/penghimpunan',      icon: Upload,          menu_key: 'keuangan.upload.penghimpunan' },
          { label: 'Otorisasi Upload',    to: '/keuangan/upload/penghimpunan/list', icon: ClipboardCheck,  menu_key: 'keuangan.upload.penghimpunan.approve' },
        ],
      },
      {
        label: 'Laporan',
        icon: FileText,
        children: [
          { section: 'Kas & Transaksi' },
          { label: 'Transaksi Kas/Bank Harian',       to: '/keuangan/laporan/kas-harian',       icon: Banknote,  menu_key: 'keuangan.report.cash_daily' },
          { label: 'Rekapitulasi Kas/Bank',           to: '/keuangan/laporan/rekap-kas',         icon: Banknote,  menu_key: 'keuangan.report.cash_summary' },
          { label: 'Monitoring Saldo Kas Bulanan',    to: '/keuangan/laporan/saldo-bulanan',     icon: Banknote,  menu_key: 'keuangan.report.cash_monthly' },
          { label: 'Jurnal Harian',                   to: '/keuangan/laporan/jurnal-harian',     icon: BookOpen,  menu_key: 'keuangan.report.journal_daily' },
          { label: 'List Transaksi Umum',             to: '/keuangan/laporan/transaksi-umum',    icon: BookOpen,  menu_key: 'keuangan.report.general_transaction' },
          { section: 'Akuntansi' },
          { label: 'Trial Balance',                   to: '/keuangan/laporan/trial-balance',     icon: FileText,  menu_key: 'keuangan.report.trial_balance' },
          { label: 'Neraca',                          to: '/keuangan/laporan/neraca',            icon: FileText,  menu_key: 'keuangan.report.neraca' },
          { label: 'Arus Kas',                        to: '/keuangan/laporan/arus-kas',          icon: FileText,  menu_key: 'keuangan.report.cash_flow' },
          { label: 'Buku Besar',                      to: '/keuangan/laporan/buku-besar',        icon: FileText,  menu_key: 'keuangan.report.general_ledger' },
          { label: 'Perubahan Dana',                  to: '/keuangan/laporan/perubahan-dana',    icon: FileText,  menu_key: 'keuangan.report.fund_changes' },
          { label: 'Perubahan Dana Detail',           to: '/keuangan/laporan/perubahan-dana-detail', icon: FileText, menu_key: 'keuangan.report.fund_changes_detail' },
          { section: 'Penghimpunan & Penyaluran' },
          { label: 'Penghimpunan Dana',               to: '/keuangan/laporan/penghimpunan-dana', icon: FileText,  menu_key: 'keuangan.report.collection' },
          { label: 'Penyaluran Dana',                 to: '/keuangan/laporan/penyaluran-dana',   icon: FileText,  menu_key: 'keuangan.report.distribution' },
          { section: 'Amil' },
          { label: 'Penerimaan Amil',                 to: '/keuangan/laporan/penerimaan-amil',   icon: FileText,  menu_key: 'keuangan.report.amil_in' },
          { label: 'Pengeluaran Amil',                to: '/keuangan/laporan/pengeluaran-amil',  icon: FileText,  menu_key: 'keuangan.report.amil_out' },
          { section: 'Piutang' },
          { label: 'Piutang pada Karyawan',           to: '/keuangan/laporan/piutang-karyawan',  icon: FileText,  menu_key: 'keuangan.report.ar_employee' },
          { label: 'Piutang pada Non-Karyawan',       to: '/keuangan/laporan/piutang-non-karyawan', icon: FileText, menu_key: 'keuangan.report.ar_external' },
          { section: 'Uang Muka Kegiatan' },
          { label: 'Rekapitulasi Uang Muka Kegiatan', to: '/keuangan/laporan/uang-muka-kegiatan', icon: FileText, menu_key: 'keuangan.report.ca_employee' },
          { label: 'List Transaksi Uang Muka Kegiatan', to: '/keuangan/laporan/list-uang-muka', icon: FileText, menu_key: 'keuangan.report.ca_list' },
          { label: 'Laporan Realisasi Project (Memo)', to: '/keuangan/laporan/realisasi-memo',  icon: FileText,  menu_key: 'keuangan.report.project_memo' },
          { label: 'Piutang Realisasi Penyaluran',   to: '/keuangan/laporan/piutang-realisasi', icon: FileText,  menu_key: 'keuangan.report.program_ar' },
          { section: 'UPZ' },
          { label: 'List Transaksi UPZ',              to: '/keuangan/laporan/upz',               icon: FileText,  menu_key: 'keuangan.report.upz' },
        ],
      },
      { label: 'Program',      icon: HandCoins,  disabled: true, badge: 'Fase 3' },
      { label: 'Penghimpunan', icon: TrendingUp, disabled: true, badge: 'Fase 3' },
    ],
  },
  {
    label: 'Administrasi',
    items: [
      { label: 'Manajemen User', icon: Users,    disabled: true, badge: 'Fase 4' },
      { label: 'Back Office',    icon: Settings, disabled: true, badge: 'Fase 4' },
      { label: 'Audit Log',      icon: FileText, disabled: true, badge: 'Fase 4' },
    ],
  },
]

const auth = useAuthStore()
const sidebar = useSidebarStore()
const route = useRoute()

// ── Menu visibility ────────────────────────────────────────────────────────────

function hasMenu(key: string | undefined): boolean {
  if (!key) return true
  return auth.hasMenu(key as MenuKey)
}

/**
 * Filter children: remove hidden items and section headings that have no
 * visible items below them (so empty sections don't appear).
 */
function visibleChildren(children: MenuItem[]): MenuItem[] {
  const out: MenuItem[] = []
  let pendingSection: MenuItem | null = null

  for (const child of children) {
    if (child.section) {
      pendingSection = child
    } else if (!child.menu_key || hasMenu(child.menu_key)) {
      if (pendingSection) { out.push(pendingSection); pendingSection = null }
      out.push(child)
    }
  }
  return out
}

/** A parent item is visible if it has at least one visible child. */
function hasVisibleChildren(item: MenuItem): boolean {
  if (!item.children) return !item.disabled
  return visibleChildren(item.children).some(c => !c.section)
}

// ── Expand / collapse ─────────────────────────────────────────────────────────

const EXPANDED_KEY = 'isf-sidebar-expanded-groups'
const expandedParents = shallowRef<Set<string>>(new Set())

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
  } catch { /* ignore */ }
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

const isExpanded    = (label: string) => expandedParents.value.has(label)
const isActiveItem  = (item: MenuItem) => Boolean(item.to && route.path === item.to)
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
          <!-- Only render item if user has access (or item is standalone disabled) -->
          <div v-if="hasVisibleChildren(item)" class="flex flex-col">

            <!-- Parent with children -->
            <template v-if="item.children">
              <button
                type="button"
                :title="
                  sidebar.collapsed
                    ? item.label + ': ' + visibleChildren(item.children).filter((c) => c.label).map((c) => c.label).join(', ')
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

              <!-- Children list — filtered by menu access -->
              <div
                v-if="!sidebar.collapsed && isExpanded(item.label)"
                class="ml-4 mt-0.5 pl-3 border-l border-border flex flex-col gap-0.5"
              >
                <template v-for="(child, ci) in visibleChildren(item.children)" :key="child.section ?? child.label ?? ci">
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

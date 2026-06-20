<script setup lang="ts">
import {
  ArrowLeftRight,
  ArrowDownCircle,
  ArrowUpCircle,
  BarChart3,
  Banknote,
  BookOpen,
  Calendar,
  ChevronDown,
  ChevronRight,
  ClipboardCheck,
  ClipboardList,
  DollarSign,
  FileText,
  HandCoins,
  Landmark,
  RotateCcw,
  LayoutDashboard,
  Pencil,
  PieChart,
  Search,
  Settings,
  ShieldCheck,
  Tag,
  TrendingUp,
  Upload,
  Users,
  Wallet,
} from 'lucide-vue-next'
import type { FunctionalComponent } from 'vue'
import { onMounted, shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'

import { cn } from '@/lib/utils'
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
  icon?: FunctionalComponent
  items: MenuItem[]
}

const groups: MenuGroup[] = [
  {
    label: 'Menu',
    items: [
      {
        label: 'Dashboard',
        icon: LayoutDashboard,
        children: [
          { label: 'Overview',      to: '/',                          icon: LayoutDashboard, menu_key: 'dashboard.overview' },
          { label: 'Keuangan',      to: '/dashboard/finance',         icon: BarChart3,       menu_key: 'dashboard.finance' },
          { label: 'Penyaluran',    to: '/dashboard/distribution',    icon: PieChart,        menu_key: 'dashboard.distribution' },
          { label: 'Penghimpunan',  to: '/dashboard/collection',      icon: HandCoins,       menu_key: 'dashboard.collection' },
        ],
      },
      {
        label: 'Master Data',
        icon: BookOpen,
        children: [
          { label: 'Chart of Accounts', to: '/finance/coa',               icon: BookOpen,  menu_key: 'finance.coa' },
          { label: 'Kas',               to: '/finance/cash',              icon: Banknote,  menu_key: 'finance.cash' },
          { label: 'Bank',              to: '/finance/bank',              icon: Landmark,  menu_key: 'finance.bank' },
          { label: 'Kas Kecil',         to: '/finance/petty-cash',        icon: Wallet,    menu_key: 'finance.petty_cash' },
          { label: 'Pemilik Anggaran',  to: '/parameter/budget-owner',    icon: Users,     menu_key: 'finance.parameter.budget_owner' },
        ],
      },
      {
        label: 'Anggaran',
        icon: Wallet,
        children: [
          { label: 'Buat Anggaran Baru', to: '/finance/budget/import',           icon: Upload,    menu_key: 'finance.budget.import' },
          { label: 'Revisi Anggaran',    to: '/finance/budget/revise',           icon: Pencil,    menu_key: 'finance.budget.revise' },
          { label: 'Inquiry Anggaran',   to: '/finance/budget/inquiry',          icon: Search,    menu_key: 'finance.budget.inquiry' },
          { label: 'Item Anggaran',      to: '/parameter/anggaran/item',         icon: Tag,       menu_key: 'finance.parameter.budget.item' },
          { label: 'Periode Anggaran',   to: '/parameter/anggaran/periode',      icon: Calendar,  menu_key: 'finance.parameter.budget.period' },
        ],
      },
      {
        label: 'Transaksi',
        icon: ArrowLeftRight,
        children: [
          { label: 'Histori Transaksi',       to: '/finance/transactions/history',             icon: ClipboardList,   menu_key: 'finance.transactions.history' },
          { label: 'Input Penghimpunan',      to: '/finance/transactions/fund-collection',     icon: ArrowUpCircle,   menu_key: 'finance.transactions.fund_collection' },
          { label: 'Input Penyaluran',        to: '/finance/transactions/fund-distribution',   icon: ArrowDownCircle, menu_key: 'finance.transactions.fund_distribution' },
          { label: 'Uang Muka',               to: '/finance/transactions/cash-advance',        icon: HandCoins,       menu_key: 'finance.transactions.cash_advance' },
          { label: 'LPJ Uang Muka',           to: '/finance/transactions/cash-advance-lpj',    icon: RotateCcw,       menu_key: 'finance.transactions.cash_advance_lpj' },
          { label: 'Transfer Antar Rekening', to: '/finance/transactions/fund-transfer',       icon: ArrowLeftRight,  menu_key: 'finance.transactions.fund_transfer' },
          { label: 'Transaksi Umum',          to: '/finance/transactions/general',             icon: BookOpen,        menu_key: 'finance.transactions.general' as MenuKey },
          { label: 'Piutang',                 to: '/finance/transactions/receivable',          icon: DollarSign,      menu_key: 'finance.transactions.receivable' },
        ],
      },
      {
        label: 'Upload',
        icon: Upload,
        children: [
          { label: 'Upload Penghimpunan', to: '/finance/upload/collection',      icon: Upload,         menu_key: 'finance.upload.collection' },
          { label: 'Otorisasi Upload',    to: '/finance/upload/collection/list', icon: ClipboardCheck, menu_key: 'finance.upload.collection.approve' },
          { label: 'Upload ZIS Rutin',    to: '/finance/upload/zis-routine',     icon: Upload,         menu_key: 'finance.upload.zis_routine' },
          { label: 'Daftar Upload ZIS',   to: '/finance/upload/zis-routine/list',icon: ClipboardCheck, menu_key: 'finance.upload.zis_routine_list' },
        ],
      },
      {
        label: 'Laporan',
        icon: FileText,
        children: [
          { section: 'Kas & Transaksi' },
          { label: 'Transaksi Kas/Bank Harian',    to: '/finance/reports/daily-cash',           icon: Banknote,  menu_key: 'finance.reports.daily_cash' },
          { label: 'Rekapitulasi Kas/Bank',         to: '/finance/reports/cash-summary',         icon: Banknote,  menu_key: 'finance.reports.cash_summary' },
          { label: 'Monitoring Saldo Bulanan',      to: '/finance/reports/monthly-balance',      icon: Banknote,  menu_key: 'finance.reports.monthly_balance' },
          { label: 'Jurnal Harian',                 to: '/finance/reports/daily-journal',        icon: BookOpen,  menu_key: 'finance.reports.daily_journal' },
          { label: 'List Transaksi Umum',           to: '/finance/reports/general-transaction',  icon: BookOpen,  menu_key: 'finance.reports.general_transaction' },
          { section: 'Akuntansi' },
          { label: 'Trial Balance',                 to: '/finance/reports/trial-balance',        icon: FileText,  menu_key: 'finance.reports.trial_balance' },
          { label: 'Neraca',                        to: '/finance/reports/balance-sheet',        icon: FileText,  menu_key: 'finance.reports.balance_sheet' },
          { label: 'Arus Kas',                      to: '/finance/reports/cash-flow',            icon: FileText,  menu_key: 'finance.reports.cash_flow' },
          { label: 'Buku Besar',                    to: '/finance/reports/general-ledger',       icon: FileText,  menu_key: 'finance.reports.general_ledger' },
          { label: 'Perubahan Dana',                to: '/finance/reports/fund-changes',         icon: FileText,  menu_key: 'finance.reports.fund_changes' },
          { label: 'Perubahan Dana Detail',         to: '/finance/reports/fund-changes-detail',  icon: FileText,  menu_key: 'finance.reports.fund_changes_detail' },
          { section: 'Penghimpunan & Penyaluran' },
          { label: 'Penghimpunan Dana',             to: '/finance/reports/fund-collection',      icon: FileText,  menu_key: 'finance.reports.fund_collection' },
          { label: 'Penyaluran Dana',               to: '/finance/reports/fund-distribution',    icon: FileText,  menu_key: 'finance.reports.fund_distribution' },
          { section: 'Amil' },
          { label: 'Penerimaan Amil',               to: '/finance/reports/amil-receipt',         icon: FileText,  menu_key: 'finance.reports.amil_receipt' },
          { label: 'Pengeluaran Amil',              to: '/finance/reports/amil-expense',         icon: FileText,  menu_key: 'finance.reports.amil_expense' },
          { section: 'Piutang' },
          { label: 'Piutang pada Karyawan',         to: '/finance/reports/employee-receivable',      icon: FileText,  menu_key: 'finance.reports.employee_receivable' },
          { label: 'Piutang pada Non-Karyawan',     to: '/finance/reports/non-employee-receivable',  icon: FileText,  menu_key: 'finance.reports.non_employee_receivable' },
          { section: 'Uang Muka Kegiatan' },
          { label: 'Rekapitulasi Uang Muka',        to: '/finance/reports/activity-cash-advance',    icon: FileText,  menu_key: 'finance.reports.activity_cash_advance' },
          { label: 'List Transaksi Uang Muka',      to: '/finance/reports/cash-advance-list',        icon: FileText,  menu_key: 'finance.reports.cash_advance_list' },
          { label: 'Realisasi Project (Memo)',       to: '/finance/reports/memo-realization',         icon: FileText,  menu_key: 'finance.reports.memo_realization' },
          { label: 'Piutang Realisasi Penyaluran',  to: '/finance/reports/receivable-realization',   icon: FileText,  menu_key: 'finance.reports.receivable_realization' },
          { section: 'UPZ' },
          { label: 'List Transaksi UPZ',            to: '/finance/reports/upz',                      icon: FileText,  menu_key: 'finance.reports.upz' },
        ],
      },
      {
        label: 'Monitoring',
        icon: ShieldCheck,
        children: [
          { label: 'Otorisasi',          to: '/finance/monitoring/authorization', icon: ShieldCheck,   menu_key: 'finance.monitoring.authorization' },
          { label: 'Riwayat Submission', to: '/finance/monitoring/history',       icon: ClipboardList, menu_key: 'finance.monitoring.history' },
        ],
      },
      { label: 'Program',        icon: HandCoins,  disabled: true, badge: 'Fase 3' },
      { label: 'Penghimpunan',   icon: TrendingUp, disabled: true, badge: 'Fase 3' },
      { label: 'Manajemen User', icon: Users,      disabled: true, badge: 'Fase 4' },
      { label: 'Back Office',    icon: Settings,   disabled: true, badge: 'Fase 4' },
      { label: 'Audit Log',      icon: FileText,   disabled: true, badge: 'Fase 4' },
    ],
  },
]

const auth = useAuthStore()
const sidebar = useSidebarStore()
const route = useRoute()

// ── App version ───────────────────────────────────────────────────────────────

const appVersion = 'v0.2.0'

// ── Menu visibility ────────────────────────────────────────────────────────────

function hasMenu(key: string | undefined): boolean {
  if (!key) return true
  return auth.hasMenu(key as MenuKey)
}

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
        if (!expandedParents.value.has(item.label!)) {
          const copy = new Set(expandedParents.value)
          copy.add(item.label!)
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
    copy.add(item.label!)
    setExpanded(copy)
  } else {
    toggleParent(item.label!)
  }
}

const isExpanded     = (label: string) => expandedParents.value.has(label)
const isActiveItem   = (item: MenuItem) => Boolean(item.to && route.path === item.to)
const isActiveParent = (item: MenuItem) =>
  Boolean(item.children?.some((c) => c.to && route.path.startsWith(c.to)))
</script>

<template>
  <aside
    :class="
      cn(
        'hidden lg:flex shrink-0 flex-col bg-slate-900 transition-[width] duration-200 overflow-hidden',
        sidebar.collapsed ? 'w-14' : 'w-52',
      )
    "
  >
    <!-- ── Sidebar header ──────────────────────────────────────────────────── -->
    <div
      :class="
        cn(
          'flex items-center gap-2.5 px-3 py-3 border-b border-slate-700/60 shrink-0',
          sidebar.collapsed && 'justify-center px-2',
        )
      "
    >
      <!-- Logo icon -->
      <div class="flex-shrink-0 w-8 h-8 rounded-lg bg-indigo-600 grid place-items-center overflow-hidden">
        <img src="@/assets/logo.svg" alt="Logo" class="w-6 h-6 object-contain" />
      </div>

      <template v-if="!sidebar.collapsed">
        <div class="min-w-0 flex-1">
          <p class="text-sm font-bold text-white leading-tight truncate">MZISS</p>
          <p class="text-[10px] text-slate-500 italic leading-tight truncate">Modul Akuntansi</p>
        </div>
      </template>
    </div>

    <!-- ── Navigation ─────────────────────────────────────────────────────── -->
    <nav class="flex flex-col flex-1 overflow-y-auto py-2 gap-0.5">
      <template v-for="group in groups" :key="group.label">
        <template v-for="item in group.items" :key="item.label">

          <div v-if="hasVisibleChildren(item)" class="flex flex-col">

            <!-- Parent with children -->
            <template v-if="item.children">
              <button
                type="button"
                :title="
                  sidebar.collapsed
                    ? item.label
                    : undefined
                "
                :class="
                  cn(
                    'flex items-center gap-2.5 text-xs font-semibold uppercase tracking-widest transition-colors w-full text-left',
                    sidebar.collapsed ? 'justify-center px-0 py-2.5 mx-auto' : 'px-3 py-2',
                    isActiveParent(item)
                      ? 'text-white'
                      : 'text-slate-500 hover:text-slate-300',
                  )
                "
                @click="handleParentClick(item)"
              >
                <component
                  :is="item.icon"
                  :class="cn('shrink-0', sidebar.collapsed ? 'w-5 h-5' : 'w-3.5 h-3.5')"
                />
                <template v-if="!sidebar.collapsed">
                  <span class="flex-1 truncate">{{ item.label }}</span>
                  <ChevronDown
                    :class="[
                      'w-3 h-3 shrink-0 transition-transform duration-150',
                      isExpanded(item.label!) ? '' : '-rotate-90',
                    ]"
                  />
                </template>
              </button>

              <!-- Children list -->
              <div
                v-if="!sidebar.collapsed && isExpanded(item.label!)"
                class="flex flex-col gap-px pb-1"
              >
                <template
                  v-for="(child, ci) in visibleChildren(item.children)"
                  :key="child.section ?? child.label ?? ci"
                >
                  <!-- Sub-section heading -->
                  <div
                    v-if="child.section"
                    class="px-3 pt-2 pb-0.5 text-[9px] uppercase tracking-widest text-slate-600 font-semibold first:pt-1"
                  >
                    {{ child.section }}
                  </div>

                  <!-- Active child link -->
                  <router-link
                    v-else-if="child.to && !child.disabled"
                    :to="child.to"
                    :class="
                      cn(
                        'flex items-center gap-2 pl-4 pr-3 py-1.5 text-xs transition-colors rounded-r-full mr-1',
                        isActiveItem(child)
                          ? 'bg-indigo-600 text-white font-medium'
                          : 'text-slate-200 hover:text-white hover:bg-slate-800',
                      )
                    "
                  >
                    <span
                      v-if="!isActiveItem(child)"
                      class="text-slate-500 text-[10px] leading-none shrink-0"
                      aria-hidden="true"
                    >•</span>
                    <component
                      v-else
                      :is="child.icon"
                      class="w-3 h-3 shrink-0"
                    />
                    <span class="flex-1 truncate">{{ child.label }}</span>
                  </router-link>

                  <!-- Disabled child -->
                  <div
                    v-else
                    class="flex items-center gap-2 pl-4 pr-3 py-1.5 text-xs text-slate-700 cursor-not-allowed"
                  >
                    <span class="text-slate-700 text-[10px] leading-none shrink-0" aria-hidden="true">•</span>
                    <span class="flex-1 truncate">{{ child.label }}</span>
                    <span
                      v-if="child.badge"
                      class="text-[9px] uppercase tracking-wide bg-slate-800 text-slate-500 px-1 py-px rounded shrink-0"
                    >{{ child.badge }}</span>
                  </div>
                </template>
              </div>
            </template>

            <!-- Standalone item (no children) — disabled only since all real items have children -->
            <div
              v-else
              :title="
                sidebar.collapsed
                  ? item.label + (item.badge ? ' · ' + item.badge : '')
                  : undefined
              "
              :class="
                cn(
                  'flex items-center gap-2.5 text-xs font-semibold uppercase tracking-widest text-slate-700 cursor-not-allowed',
                  sidebar.collapsed ? 'justify-center px-0 py-2.5' : 'px-3 py-2',
                )
              "
            >
              <component
                :is="item.icon"
                :class="cn('shrink-0', sidebar.collapsed ? 'w-5 h-5' : 'w-3.5 h-3.5')"
              />
              <template v-if="!sidebar.collapsed">
                <span class="flex-1 truncate">{{ item.label }}</span>
                <span
                  v-if="item.badge"
                  class="text-[9px] uppercase tracking-wide bg-slate-800 text-slate-500 px-1.5 py-0.5 rounded"
                >{{ item.badge }}</span>
              </template>
            </div>

          </div>
        </template>
      </template>
    </nav>

    <!-- ── Bottom: App Version ───────────────────────────────────────────────── -->
    <div
      :class="
        cn(
          'border-t border-slate-700/60 shrink-0',
          sidebar.collapsed ? 'px-2 py-2.5 flex justify-center' : 'px-3 py-2.5',
        )
      "
    >
      <template v-if="!sidebar.collapsed">
        <p class="text-[10px] text-slate-500 leading-none">{{ appVersion }}</p>
      </template>
      <template v-else>
        <p class="text-[9px] text-slate-600 leading-none" :title="appVersion">{{ appVersion }}</p>
      </template>
    </div>
  </aside>
</template>

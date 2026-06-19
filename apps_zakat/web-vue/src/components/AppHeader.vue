<script setup lang="ts">
import { ChevronRight, Menu } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'
import { useSidebarStore } from '@/stores/sidebar'

const auth = useAuthStore()
const sidebar = useSidebarStore()
const route = useRoute()
const router = useRouter()

// ── Breadcrumb ────────────────────────────────────────────────────────────────
// Routes carry meta.breadcrumb?: string[] for explicit crumbs.
// Fallback: derive from meta.title split by parent inference.

const breadcrumbs = computed<string[]>(() => {
  const explicit = route.meta.breadcrumb as string[] | undefined
  if (explicit?.length) return explicit

  const title = (route.meta.title as string | undefined) ?? ''
  if (!title) return []

  // Infer parent from route name pattern:
  // e.g. "finance-transactions-general-create" → parent "Transaksi Umum", child "Input Transaksi Umum"
  const name = String(route.name ?? '')

  // Group mappings: route-name prefix → human label
  const parentMap: Record<string, string> = {
    'dashboard':                     'Dashboard',
    'finance-coa':                   'Master Data',
    'finance-cash':                  'Master Data',
    'finance-bank':                  'Master Data',
    'finance-petty-cash':            'Master Data',
    'parameter-budget-owner':        'Master Data',
    'finance-budget':                'Anggaran',
    'parameter-anggaran':            'Anggaran',
    'finance-transactions':          'Transaksi',
    'finance-upload':                'Upload',
    'finance-reports':               'Laporan',
    'finance-monitoring':            'Monitoring',
    'admin':                         'Admin',
    'profile':                       'Profil',
  }

  let parent: string | null = null
  for (const [prefix, label] of Object.entries(parentMap)) {
    if (name === prefix || name.startsWith(prefix + '-')) {
      parent = label
      break
    }
  }

  if (!parent || parent === title) return [title]
  return [parent, title]
})

// ── Active period ─────────────────────────────────────────────────────────────

const activePeriod = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('id-ID', { month: 'long', year: 'numeric' }).toUpperCase()
})

// ── User info ─────────────────────────────────────────────────────────────────

const displayName = computed(() => auth.user?.name ?? '')
const username = computed(() => auth.user?.username ?? '')

const userInitials = computed(() => {
  const parts = displayName.value.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return '?'
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
})

// Role label: pick the first role or show generic
const roleLabel = computed(() => {
  const roles = auth.user?.roles ?? []
  if (!roles.length) return 'Pengguna'
  // map common role codes to display labels
  const roleLabels: Record<string, string> = {
    ACC: 'Admin Akuntansi',
    KEU: 'Staf Keuangan',
    ADM: 'Administrator',
    DIST: 'Distribusi',
    SPVDIST: 'Supervisor Distribusi',
  }
  return roleLabels[roles[0]] ?? roles[0]
})

function goProfile() {
  router.push({ name: 'profile-password' })
}
</script>

<template>
  <header class="bg-slate-900 h-12 px-3 sm:px-4 flex items-center justify-between gap-2 shrink-0 border-b border-slate-700/60">

    <!-- LEFT: hamburger + breadcrumb -->
    <div class="flex items-center gap-2 min-w-0">
      <!-- Sidebar toggle -->
      <button
        v-if="auth.user"
        type="button"
        class="hidden lg:inline-flex h-8 w-8 items-center justify-center rounded-md text-slate-400 hover:text-white hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/30 transition-colors shrink-0"
        :title="sidebar.collapsed ? 'Buka sidebar' : 'Tutup sidebar'"
        @click="sidebar.toggle"
      >
        <Menu class="w-4 h-4" />
      </button>

      <!-- Breadcrumb -->
      <nav v-if="breadcrumbs.length" class="flex items-center gap-1 min-w-0" aria-label="Breadcrumb">
        <template v-for="(crumb, idx) in breadcrumbs" :key="crumb">
          <ChevronRight
            v-if="idx > 0"
            class="w-3 h-3 text-slate-600 shrink-0"
            aria-hidden="true"
          />
          <span
            :class="[
              'text-xs truncate',
              idx === breadcrumbs.length - 1
                ? 'text-white font-medium'
                : 'text-slate-400',
            ]"
          >
            {{ crumb }}
          </span>
        </template>
      </nav>
    </div>

    <!-- RIGHT: period label + user avatar + user info -->
    <div v-if="auth.user" class="flex items-center gap-3 shrink-0">

      <!-- Periode aktif -->
      <div class="hidden sm:flex flex-col items-end leading-none">
        <span class="text-[9px] text-slate-500 uppercase tracking-widest font-semibold">Periode</span>
        <span class="text-xs text-slate-300 font-semibold tabular-nums mt-0.5">{{ activePeriod }}</span>
      </div>

      <!-- Divider -->
      <div class="hidden sm:block w-px h-5 bg-slate-700" aria-hidden="true" />

      <!-- Avatar + name + username -->
      <button
        type="button"
        class="flex items-center gap-2 rounded-md px-1.5 py-1 hover:bg-slate-800 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/30"
        :title="displayName"
        @click="goProfile"
      >
        <!-- Avatar circle -->
        <div class="w-7 h-7 rounded-full bg-indigo-600 grid place-items-center shrink-0">
          <span class="text-[10px] font-bold text-white leading-none">{{ userInitials }}</span>
        </div>

        <div class="hidden sm:flex flex-col items-start leading-none">
          <span class="text-xs font-semibold text-white truncate max-w-[120px]">{{ displayName }}</span>
          <span class="text-[10px] text-slate-400 truncate max-w-[120px] mt-0.5">{{ roleLabel }}</span>
        </div>
      </button>
    </div>
  </header>
</template>

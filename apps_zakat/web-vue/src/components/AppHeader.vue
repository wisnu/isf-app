<script setup lang="ts">
import { ChevronRight, KeyRound, LogOut, Menu } from 'lucide-vue-next'
import { computed, onBeforeUnmount, onMounted, shallowRef } from 'vue'
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

// ── Today's date ──────────────────────────────────────────────────────────────

const todayLabel = computed(() => {
  const now = new Date()
  return now.toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' })
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

// ── User dropdown ─────────────────────────────────────────────────────────────

const dropdownOpen = shallowRef(false)

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
}

function closeDropdown() {
  dropdownOpen.value = false
}

function goChangePassword() {
  closeDropdown()
  router.push({ name: 'profile-password' })
}

async function doLogout() {
  closeDropdown()
  await auth.logout()
  router.push({ name: 'login' })
}

function onDocumentClick(e: MouseEvent) {
  const target = e.target as HTMLElement
  if (!target.closest('[data-user-menu]')) {
    closeDropdown()
  }
}

onMounted(() => document.addEventListener('click', onDocumentClick, true))
onBeforeUnmount(() => document.removeEventListener('click', onDocumentClick, true))
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

    <!-- RIGHT: today's date + user avatar + dropdown -->
    <div v-if="auth.user" class="flex items-center gap-3 shrink-0">

      <!-- Tanggal hari ini -->
      <div class="hidden sm:flex items-center leading-none">
        <span class="text-xs text-slate-300 font-semibold tabular-nums">{{ todayLabel }}</span>
      </div>

      <!-- Divider -->
      <div class="hidden sm:block w-px h-5 bg-slate-700" aria-hidden="true" />

      <!-- Avatar + name + dropdown -->
      <div class="relative" data-user-menu>
        <button
          type="button"
          class="flex items-center gap-2 rounded-md px-1.5 py-1 hover:bg-slate-800 transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/30"
          :title="displayName"
          @click="toggleDropdown"
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

        <!-- Dropdown menu -->
        <div
          v-if="dropdownOpen"
          class="absolute right-0 top-full mt-1.5 w-44 bg-slate-800 border border-slate-700 rounded shadow-lg z-50 py-1 overflow-hidden"
          role="menu"
        >
          <button
            type="button"
            class="flex items-center gap-2.5 w-full text-left px-4 py-2 text-xs text-slate-200 hover:bg-slate-700 transition-colors"
            role="menuitem"
            @click="goChangePassword"
          >
            <KeyRound class="w-3.5 h-3.5 shrink-0" />
            <span>Ubah Password</span>
          </button>
          <div class="my-1 border-t border-slate-700" aria-hidden="true" />
          <button
            type="button"
            class="flex items-center gap-2.5 w-full text-left px-4 py-2 text-xs text-slate-200 hover:bg-slate-700 transition-colors"
            role="menuitem"
            @click="doLogout"
          >
            <LogOut class="w-3.5 h-3.5 shrink-0" />
            <span>Keluar</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

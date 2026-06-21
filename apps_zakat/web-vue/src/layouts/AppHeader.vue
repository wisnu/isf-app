<script setup lang="ts">
import { ChevronRight, KeyRound, LogOut, Menu } from 'lucide-vue-next'
import { computed, onBeforeUnmount, onMounted, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/app/stores/auth.store'
import { useSidebarStore } from '@/app/stores/sidebar.store'

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
    'dashboard':                       'Dashboard',
    'finance-coa':                     'Master Data',
    'finance-cash':                    'Master Data',
    'finance-bank':                    'Master Data',
    'finance-petty-cash':              'Master Data',
    'finance-master':                  'Master Data',
    'finance-budget':                  'Anggaran',
    'finance-transactions':            'Transaksi',
    'finance-upload':                  'Upload',
    'finance-reports':                 'Laporan',
    'finance-monitoring':              'Monitoring',
    'administration':                  'Administrasi',
    'profile':                         'Profil',
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
  <header
    class="flex items-center shrink-0 border-b border-[#e4e8f0] px-4 gap-3"
    style="height:64px; background:rgba(238,240,245,.96); backdrop-filter:blur(14px);"
  >
    <!-- LEFT: hamburger + breadcrumb (static, not flex-1) -->
    <div class="flex items-center gap-3 shrink-0">
      <!-- Sidebar toggle -->
      <button
        v-if="auth.user"
        type="button"
        class="w-8 h-8 grid place-items-center rounded-[9px] border border-[#e8ecf4] bg-white text-slate-500
               hover:bg-slate-50 hover:border-slate-300 transition-all shrink-0"
        :title="sidebar.collapsed ? 'Buka sidebar' : 'Tutup sidebar'"
        @click="sidebar.toggle"
      >
        <Menu class="w-4 h-4" />
      </button>

      <!-- Breadcrumb -->
      <div v-if="breadcrumbs.length" class="flex flex-col leading-tight">
        <div class="flex items-center gap-1">
          <template v-for="(crumb, idx) in breadcrumbs" :key="crumb">
            <ChevronRight v-if="idx > 0" class="w-3 h-3 text-slate-300 shrink-0" aria-hidden="true" />
            <span :class="['text-[11px] truncate', idx === breadcrumbs.length - 1 ? 'text-slate-400' : 'text-slate-400']">
              {{ crumb }}
            </span>
          </template>
        </div>
        <span class="text-[17px] font-extrabold text-slate-900 leading-tight mt-px">
          {{ breadcrumbs[breadcrumbs.length - 1] ?? '' }}
        </span>
      </div>
    </div>

    <!-- RIGHT: date + user -->
    <div v-if="auth.user" class="ml-auto flex items-center gap-2 shrink-0">
      <span class="hidden sm:block text-[11px] text-slate-500 font-semibold tabular-nums">{{ todayLabel }}</span>
      <div class="hidden sm:block w-px h-5 bg-slate-200" aria-hidden="true" />

      <!-- User chip -->
      <div class="relative" data-user-menu>
        <button
          type="button"
          class="flex items-center gap-2 px-2 py-1.5 rounded-[10px] border border-[#e4e8f0] bg-white hover:bg-slate-50 transition-all"
          :title="displayName"
          @click="toggleDropdown"
        >
          <div class="w-7 h-7 rounded-full bg-blue-600 grid place-items-center shrink-0">
            <span class="text-[10px] font-extrabold text-white leading-none">{{ userInitials }}</span>
          </div>
          <div class="hidden sm:flex flex-col items-start leading-none">
            <span class="text-[12px] font-bold text-slate-900 truncate max-w-[110px]">{{ displayName }}</span>
            <span class="text-[10px] text-slate-400 truncate max-w-[110px] mt-0.5">{{ roleLabel }}</span>
          </div>
        </button>

        <!-- Dropdown -->
        <div
          v-if="dropdownOpen"
          class="absolute right-0 top-full mt-2 w-44 bg-white border border-slate-200 rounded-xl shadow-lg z-50 py-1 overflow-hidden"
          role="menu"
        >
          <button
            type="button"
            class="flex items-center gap-2.5 w-full text-left px-4 py-2.5 text-[12px] text-slate-700 hover:bg-slate-50 transition-colors"
            role="menuitem"
            @click="goChangePassword"
          >
            <KeyRound class="w-3.5 h-3.5 shrink-0 text-slate-400" />
            <span>Ubah Password</span>
          </button>
          <div class="my-1 border-t border-slate-100" aria-hidden="true" />
          <button
            type="button"
            class="flex items-center gap-2.5 w-full text-left px-4 py-2.5 text-[12px] text-slate-700 hover:bg-slate-50 transition-colors"
            role="menuitem"
            @click="doLogout"
          >
            <LogOut class="w-3.5 h-3.5 shrink-0 text-slate-400" />
            <span>Keluar</span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

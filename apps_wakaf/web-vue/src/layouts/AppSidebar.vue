<script setup lang="ts">
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search } from 'lucide-vue-next'

import { cn } from '@/shared/utils/utils'
import { useSidebarStore } from '@/app/stores/sidebar.store'
import { useAuthStore } from '@/app/stores/auth.store'
import { DOMAIN_MAP } from '@/shared/constants/domains'
import type { DomainId, NavGroup, NavItem, NavSection } from '@/shared/constants/domains'
import type { MenuKey } from '@/shared/constants/menu-keys'

const route  = useRoute()
const router = useRouter()
const sidebar = useSidebarStore()
const auth   = useAuthStore()

// ── Active domain config ──────────────────────────────────────────────────────
const activeDomain = computed(() => route.meta.domain as DomainId | undefined)
const domainConfig = computed(() => activeDomain.value ? DOMAIN_MAP[activeDomain.value] : null)

// ── RBAC ──────────────────────────────────────────────────────────────────────
function hasMenu(key: string | undefined): boolean {
  if (!key) return true
  return auth.hasMenu(key as MenuKey)
}

function visibleItems(items: (NavItem | NavSection)[]): (NavItem | NavSection)[] {
  const out: (NavItem | NavSection)[] = []
  let pendingSection: NavSection | null = null
  for (const item of items) {
    if ('section' in item) {
      pendingSection = item
    } else {
      if (hasMenu(item.menu_key)) {
        if (pendingSection) { out.push(pendingSection); pendingSection = null }
        out.push(item)
      }
    }
  }
  return out
}

function visibleGroups(groups: NavGroup[]): NavGroup[] {
  return groups
    .map(g => ({ ...g, items: visibleItems(g.items) }))
    .filter(g => g.items.some(i => !('section' in i)))
}

// ── Tab ───────────────────────────────────────────────────────────────────────
type Tab = 'all' | 'fav'
const activeTab = ref<Tab>('all')

// ── Favorites ─────────────────────────────────────────────────────────────────
const FAV_KEY = 'isf-sidebar-favorites'
const favorites = shallowRef<Set<string>>(new Set())

function loadFavorites() {
  try {
    const raw = localStorage.getItem(FAV_KEY)
    if (raw) favorites.value = new Set(JSON.parse(raw))
  } catch { /* ignore */ }
}

function toggleFavorite(to: string, e: Event) {
  e.stopPropagation()
  const next = new Set(favorites.value)
  if (next.has(to)) next.delete(to)
  else next.add(to)
  favorites.value = next
  localStorage.setItem(FAV_KEY, JSON.stringify([...next]))
}

onMounted(loadFavorites)

// ── Search ────────────────────────────────────────────────────────────────────
const searchQuery = ref('')

interface FlatItem extends NavItem { groupLabel: string }

const searchResults = computed<FlatItem[]>(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q || !domainConfig.value) return []
  const results: FlatItem[] = []
  for (const g of visibleGroups(domainConfig.value.groups)) {
    for (const item of g.items) {
      if (!('section' in item) && item.label.toLowerCase().includes(q)) {
        results.push({ ...item, groupLabel: g.label })
      }
    }
  }
  return results
})

const favItems = computed<FlatItem[]>(() => {
  if (!domainConfig.value) return []
  const results: FlatItem[] = []
  for (const g of visibleGroups(domainConfig.value.groups)) {
    for (const item of g.items) {
      if (!('section' in item) && favorites.value.has(item.to)) {
        results.push({ ...item, groupLabel: g.label })
      }
    }
  }
  return results
})

// ── Expand / collapse ─────────────────────────────────────────────────────────
const EXPANDED_KEY = 'isf-sidebar-expanded-groups'
const expandedGroups = shallowRef<Set<string>>(new Set())

function persistExpanded() {
  localStorage.setItem(EXPANDED_KEY, JSON.stringify([...expandedGroups.value]))
}

function toggleGroup(id: string) {
  const next = new Set(expandedGroups.value)
  if (next.has(id)) next.delete(id)
  else next.add(id)
  expandedGroups.value = next
  persistExpanded()
}

function isExpanded(id: string) { return expandedGroups.value.has(id) }

function autoExpand(path: string) {
  if (!domainConfig.value) return
  for (const g of domainConfig.value.groups) {
    if (g.items.some(i => !('section' in i) && path.startsWith(i.to) && i.to !== '/')) {
      if (!expandedGroups.value.has(g.id)) {
        const next = new Set(expandedGroups.value)
        next.add(g.id)
        expandedGroups.value = next
        persistExpanded()
      }
    }
  }
  // Always expand dashboard group if at root
  if (path === '/') {
    const next = new Set(expandedGroups.value)
    next.add('dashboard')
    expandedGroups.value = next
    persistExpanded()
  }
}

onMounted(() => {
  try {
    const raw = localStorage.getItem(EXPANDED_KEY)
    if (raw) expandedGroups.value = new Set(JSON.parse(raw))
  } catch { /* ignore */ }
  autoExpand(route.path)
})

watch(() => route.path, autoExpand)
watch(activeDomain, (newDomain) => {
  if (newDomain && domainConfig.value?.groups.length) {
    const firstGroup = domainConfig.value.groups[0].id
    if (!expandedGroups.value.has(firstGroup)) {
      const next = new Set(expandedGroups.value)
      next.add(firstGroup)
      expandedGroups.value = next
      persistExpanded()
    }
  }
})

// ── Active state ──────────────────────────────────────────────────────────────
const isActiveItem = (to: string) => route.path === to
</script>

<template>
  <aside
    :class="cn(
      'flex flex-col bg-white border-r border-slate-100 transition-[width] duration-200 overflow-hidden shrink-0',
      sidebar.collapsed ? 'w-0' : 'w-[278px]',
    )"
  >
    <!-- Domain header -->
    <div class="px-3.5 pt-4 pb-3 border-b border-slate-100 shrink-0" v-if="domainConfig">
      <p class="text-base font-extrabold text-slate-900 leading-tight">{{ domainConfig.label }}</p>
      <p class="text-[10.5px] text-slate-400 mt-0.5">{{ domainConfig.sub }}</p>
    </div>

    <!-- Search -->
    <div class="px-2.5 py-2 border-b border-slate-100 shrink-0">
      <div class="relative">
        <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-slate-400 pointer-events-none" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari menu, fitur..."
          class="w-full pl-8 pr-3 py-2 text-[12.5px] bg-slate-50 border border-slate-200 rounded-[10px]
                 text-slate-900 placeholder-slate-400 outline-none
                 focus:border-blue-300 focus:ring-2 focus:ring-blue-100 transition-all"
        />
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-1.5 px-2.5 py-2 border-b border-slate-100 shrink-0">
      <button
        type="button"
        :class="cn(
          'flex-1 rounded-full py-1.5 text-[11.5px] font-semibold border transition-all',
          activeTab === 'all'
            ? 'bg-blue-600 border-blue-600 text-white font-bold'
            : 'bg-white border-slate-200 text-slate-500 hover:bg-slate-50 hover:border-slate-300',
        )"
        @click="activeTab = 'all'; searchQuery = ''"
      >
        Semua
      </button>
      <button
        type="button"
        :class="cn(
          'flex-1 rounded-full py-1.5 text-[11.5px] font-semibold border transition-all',
          activeTab === 'fav'
            ? 'bg-blue-600 border-blue-600 text-white font-bold'
            : 'bg-white border-slate-200 text-slate-500 hover:bg-slate-50 hover:border-slate-300',
        )"
        @click="activeTab = 'fav'; searchQuery = ''"
      >
        ⭐ Favorit
      </button>
    </div>

    <!-- Nav area -->
    <nav class="flex-1 overflow-y-auto py-1.5 px-2.5 scrollbar-thin scrollbar-thumb-slate-200">

      <!-- Search results -->
      <template v-if="searchQuery.trim()">
        <div v-if="searchResults.length === 0" class="py-5 text-center text-sm text-slate-400">
          Tidak ada menu yang cocok.
        </div>
        <router-link
          v-for="item in searchResults"
          :key="item.to"
          :to="item.to"
          :class="cn(
            'group flex items-center gap-2 w-full text-left px-2 py-2 rounded-[9px] text-[12.5px] transition-all',
            isActiveItem(item.to)
              ? 'bg-blue-50 text-blue-700 font-bold'
              : 'text-slate-600 hover:bg-slate-50',
          )"
        >
          <span class="flex-1 truncate">{{ item.label }}</span>
          <span class="text-[10px] bg-slate-100 text-slate-400 rounded-full px-2 py-px font-bold shrink-0">
            {{ item.groupLabel }}
          </span>
          <span
            :class="cn(
              'text-sm transition-colors cursor-pointer shrink-0',
              favorites.has(item.to) ? 'text-amber-400' : 'text-transparent group-hover:text-slate-300 hover:!text-amber-400',
            )"
            @click="toggleFavorite(item.to, $event)"
          >★</span>
        </router-link>
      </template>

      <!-- Favorites tab -->
      <template v-else-if="activeTab === 'fav'">
        <div v-if="favItems.length === 0" class="py-5 text-center text-sm text-slate-400">
          Belum ada favorit.<br>
          <span class="text-xs">Klik ★ pada menu item untuk menyimpan.</span>
        </div>
        <router-link
          v-for="item in favItems"
          :key="item.to"
          :to="item.to"
          :class="cn(
            'group flex items-center gap-2 w-full text-left px-2 py-2 rounded-[9px] text-[12.5px] transition-all',
            isActiveItem(item.to)
              ? 'bg-blue-50 text-blue-700 font-bold'
              : 'text-slate-600 hover:bg-slate-50',
          )"
        >
          <span class="flex-1 truncate">{{ item.label }}</span>
          <span class="text-[10px] bg-slate-100 text-slate-400 rounded-full px-2 py-px font-bold shrink-0">
            {{ item.groupLabel }}
          </span>
          <span
            class="text-sm text-amber-400 transition-colors cursor-pointer shrink-0 hover:text-amber-500"
            @click="toggleFavorite(item.to, $event)"
          >★</span>
        </router-link>
      </template>

      <!-- Normal grouped view -->
      <template v-else-if="domainConfig">
        <div
          v-for="group in visibleGroups(domainConfig.groups)"
          :key="group.id"
          class="border border-slate-100 rounded-[13px] bg-white mb-1.5 overflow-hidden"
        >
          <!-- Group header -->
          <button
            type="button"
            class="flex items-center gap-2 w-full text-left px-3 py-2.5 text-[12.5px] font-bold text-slate-700 select-none"
            @click="toggleGroup(group.id)"
          >
            <component :is="group.icon" class="w-3.5 h-3.5 text-slate-400 shrink-0" :stroke-width="2" />
            <span class="flex-1">{{ group.label }}</span>
            <span class="text-[10px] bg-slate-100 text-slate-400 rounded-full px-1.5 py-px font-bold">
              {{ group.items.filter(i => !('section' in i)).length }}
            </span>
            <svg
              :class="cn('w-3 h-3 text-slate-300 transition-transform duration-150 shrink-0', isExpanded(group.id) ? 'rotate-90' : '')"
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"
            ><polyline points="9 18 15 12 9 6"/></svg>
          </button>

          <!-- Items -->
          <div v-if="isExpanded(group.id)" class="pb-1.5 px-1.5">
            <template v-for="(item, idx) in group.items" :key="'section' in item ? `sect-${idx}` : item.to">
              <!-- Section divider -->
              <div
                v-if="'section' in item"
                class="px-2 pt-2 pb-0.5 text-[9.5px] uppercase tracking-wider text-slate-300 font-bold first:pt-1"
              >
                {{ item.section }}
              </div>

              <!-- Nav item -->
              <router-link
                v-else
                :to="item.to"
                :class="cn(
                  'group flex items-center gap-2 px-2 py-2 rounded-[9px] text-[12.5px] transition-all',
                  isActiveItem(item.to)
                    ? 'bg-blue-50 text-blue-700 font-bold'
                    : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700',
                )"
              >
                <span class="flex-1 truncate">{{ item.label }}</span>
                <span
                  :class="cn(
                    'text-sm transition-colors cursor-pointer shrink-0',
                    favorites.has(item.to)
                      ? 'text-amber-400'
                      : 'text-transparent group-hover:text-slate-300 hover:!text-amber-400',
                  )"
                  @click="toggleFavorite(item.to, $event)"
                >★</span>
              </router-link>
            </template>
          </div>
        </div>
      </template>
    </nav>

    <!-- Footer -->
    <div class="px-3 py-2 border-t border-slate-100 shrink-0">
      <p class="text-[10px] text-slate-300">v0.2.0</p>
    </div>
  </aside>
</template>

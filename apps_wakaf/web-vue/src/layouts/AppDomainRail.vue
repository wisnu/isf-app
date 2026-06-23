<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSidebarStore } from '@/app/stores/sidebar.store'
import { DOMAIN_MAP, DOMAIN_ORDER } from '@/shared/constants/domains'
import type { DomainId, NavItem } from '@/shared/constants/domains'
import { useAuthStore } from '@/app/stores/auth.store'

const route  = useRoute()
const router = useRouter()
const sidebar = useSidebarStore()
const auth   = useAuthStore()

const activeDomain = computed(() => route.meta.domain as DomainId | undefined)

function isNavItem(item: unknown): item is NavItem {
  return typeof item === 'object' && item !== null && 'to' in item
}

const visibleDomains = computed(() => {
  return DOMAIN_ORDER.filter(id => {
    const domain = DOMAIN_MAP[id]
    if (domain.locked) return true
    const keys = domain.groups
      .flatMap(g => (g.items ?? []).filter(isNavItem))
      .map(item => item.menu_key)
      .filter(Boolean) as string[]
    if (keys.length === 0) return true
    return keys.some(k => auth.hasMenu(k))
  })
})

function handleDomainClick(id: DomainId) {
  const domain = DOMAIN_MAP[id]
  if (domain.locked) return

  if (sidebar.collapsed) sidebar.toggle()

  if (activeDomain.value !== id) {
    router.push(domain.defaultRoute)
  }
}
</script>

<template>
  <nav
    class="flex flex-col items-center bg-slate-900 border-r border-white/[0.04] py-3.5 gap-1 overflow-visible z-20"
    style="width: 66px;"
    aria-label="Modul aplikasi"
  >
    <!-- App brand mark -->
    <div class="w-10 h-10 rounded-xl grid place-items-center font-black text-white text-sm mb-1 shrink-0"
         style="background: linear-gradient(135deg, #3b82f6, #22c55e); box-shadow: 0 6px 16px rgba(0,0,0,.28)">
      IS
    </div>

    <!-- Divider between brand and domains -->
    <div class="w-8 h-px bg-white/10 mb-1 shrink-0" />

    <!-- Domain buttons -->
    <template v-for="id in visibleDomains" :key="id">
      <div class="relative group">
        <button
          type="button"
          :class="[
            'w-11 h-11 rounded-[13px] grid place-items-center text-xl transition-all duration-150 shrink-0',
            DOMAIN_MAP[id].locked
              ? 'opacity-25 cursor-not-allowed'
              : 'cursor-pointer',
            activeDomain === id
              ? 'bg-blue-600 shadow-[0_4px_14px_rgba(37,99,235,.45)] opacity-100'
              : 'bg-transparent opacity-45 hover:bg-white/8 hover:opacity-85',
          ]"
          :title="DOMAIN_MAP[id].locked ? `${DOMAIN_MAP[id].label} — ${DOMAIN_MAP[id].lockedBadge}` : ''"
          @click="handleDomainClick(id)"
        >
          <component :is="DOMAIN_MAP[id].icon" class="w-5 h-5 text-white" :stroke-width="1.8" />
        </button>

        <!-- Tooltip -->
        <div
          v-if="!DOMAIN_MAP[id].locked"
          class="pointer-events-none absolute left-[calc(100%+10px)] top-1/2 -translate-y-1/2 whitespace-nowrap
                 bg-slate-800 text-slate-200 text-[11.5px] font-semibold px-3 py-1.5 rounded-lg
                 shadow-[0_4px_14px_rgba(0,0,0,.35)] border border-white/5
                 opacity-0 group-hover:opacity-100 transition-opacity duration-150 z-50"
        >
          {{ DOMAIN_MAP[id].label }}
        </div>
        <div
          v-else
          class="pointer-events-none absolute left-[calc(100%+10px)] top-1/2 -translate-y-1/2 whitespace-nowrap
                 bg-slate-800 text-slate-400 text-[11px] font-semibold px-3 py-1.5 rounded-lg
                 shadow-[0_4px_14px_rgba(0,0,0,.35)] border border-white/5
                 opacity-0 group-hover:opacity-100 transition-opacity duration-150 z-50"
        >
          {{ DOMAIN_MAP[id].label }} — {{ DOMAIN_MAP[id].lockedBadge }}
        </div>
      </div>
    </template>

    <!-- Spacer -->
    <div class="flex-1" />

    <!-- Version info -->
    <div class="flex flex-col items-center gap-0.5 pb-1">
      <div class="flex flex-col items-center">
        <span class="text-[8px] font-bold uppercase tracking-wider text-slate-600 leading-none">FE</span>
        <span class="text-[9px] font-semibold text-slate-700 leading-relaxed">v0.2.0</span>
      </div>
      <div class="w-5 h-px bg-white/5" />
      <div class="flex flex-col items-center">
        <span class="text-[8px] font-bold uppercase tracking-wider text-slate-600 leading-none">BE</span>
        <span class="text-[9px] font-semibold text-slate-700 leading-relaxed">v1.4.2</span>
      </div>
    </div>
  </nav>
</template>

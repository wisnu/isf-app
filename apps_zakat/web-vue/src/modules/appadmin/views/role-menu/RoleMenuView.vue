<script setup lang="ts">
import { AlertCircle, Check, Loader2, RefreshCw, Save, Search, X } from 'lucide-vue-next'
import { computed, onBeforeUnmount, onMounted, ref, shallowRef } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import Input from '@/shared/components/Input.vue'
import CrudLayout from '@/shared/components/CrudLayout.vue'
import DataPanel from '@/shared/components/DataPanel.vue'
import FilterGroup from '@/shared/components/FilterGroup.vue'
import FilterPanel from '@/shared/components/FilterPanel.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import { api, ApiError } from '@/shared/api/client'

interface RoleInfo {
  role_id: string
  role_name: string
  user_count: number
}

interface MenuInfo {
  menu_key: string
  label: string
  group_label: string
  sort_order: number
}

interface MappingPair {
  role_id: string
  menu_key: string
}

interface Snapshot {
  roles: RoleInfo[]
  menus: MenuInfo[]
  mapping: MappingPair[]
}

interface UpdateResponse {
  updated: boolean
  total_rows: number
  diff: { added: MappingPair[]; removed: MappingPair[] }
}

const loading = shallowRef(true)
const saving = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const successMsg = shallowRef<string | null>(null)

const roles = ref<RoleInfo[]>([])
const menus = ref<MenuInfo[]>([])

const original = shallowRef<Set<string>>(new Set())
const current = shallowRef<Set<string>>(new Set())

const searchRole = shallowRef('')
const visibleGroups = shallowRef<Set<string>>(new Set())

const pairKey = (role_id: string, menu_key: string) => `${role_id}|${menu_key}`

const dirty = computed(() => {
  const added: MappingPair[] = []
  const removed: MappingPair[] = []
  for (const k of current.value) {
    if (!original.value.has(k)) {
      const [rp, mk] = k.split('|')
      added.push({ role_id: rp, menu_key: mk })
    }
  }
  for (const k of original.value) {
    if (!current.value.has(k)) {
      const [rp, mk] = k.split('|')
      removed.push({ role_id: rp, menu_key: mk })
    }
  }
  return { added, removed, count: added.length + removed.length }
})

const isDirty = computed(() => dirty.value.count > 0)

const menuGroups = computed(() => {
  const groups = new Map<string, MenuInfo[]>()
  for (const m of menus.value) {
    if (!groups.has(m.group_label)) groups.set(m.group_label, [])
    groups.get(m.group_label)!.push(m)
  }
  return Array.from(groups.entries())
})

const filteredMenus = computed(() =>
  menus.value.filter((m) => visibleGroups.value.has(m.group_label))
)

const filteredRoles = computed(() => {
  const q = searchRole.value.trim().toLowerCase()
  if (!q) return roles.value
  return roles.value.filter(
    (r) =>
      r.role_id.toLowerCase().includes(q) ||
      r.role_name.toLowerCase().includes(q)
  )
})

function isChecked(role_id: string, menu_key: string): boolean {
  return current.value.has(pairKey(role_id, menu_key))
}

function isCellDirty(role_id: string, menu_key: string): boolean {
  const k = pairKey(role_id, menu_key)
  return original.value.has(k) !== current.value.has(k)
}

function toggleCell(role_id: string, menu_key: string) {
  const k = pairKey(role_id, menu_key)
  const next = new Set(current.value)
  if (next.has(k)) next.delete(k)
  else next.add(k)
  current.value = next
}

function toggleRowAll(role_id: string) {
  const visibleKeys = filteredMenus.value.map((m) => pairKey(role_id, m.menu_key))
  const allOn = visibleKeys.every((k) => current.value.has(k))
  const next = new Set(current.value)
  if (allOn) {
    visibleKeys.forEach((k) => next.delete(k))
  } else {
    visibleKeys.forEach((k) => next.add(k))
  }
  current.value = next
}

function toggleColumnAll(menu_key: string) {
  const visibleKeys = filteredRoles.value.map((r) => pairKey(r.role_id, menu_key))
  const allOn = visibleKeys.every((k) => current.value.has(k))
  const next = new Set(current.value)
  if (allOn) {
    visibleKeys.forEach((k) => next.delete(k))
  } else {
    visibleKeys.forEach((k) => next.add(k))
  }
  current.value = next
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const snap = await api.get<Snapshot>('/api/appadmin/role-menu')
    roles.value = snap.roles
    menus.value = snap.menus
    const keys = new Set(snap.mapping.map((p) => pairKey(p.role_id, p.menu_key)))
    original.value = keys
    current.value = new Set(keys)
    // Default semua group menu visible
    visibleGroups.value = new Set(snap.menus.map((m) => m.group_label))
  } catch (e) {
    errorMsg.value =
      e instanceof ApiError ? e.message : 'Gagal memuat data. Coba refresh.'
  } finally {
    loading.value = false
  }
}

function discard() {
  current.value = new Set(original.value)
  successMsg.value = null
  errorMsg.value = null
}

async function save() {
  if (!isDirty.value || saving.value) return
  saving.value = true
  errorMsg.value = null
  successMsg.value = null
  const mapping: MappingPair[] = [...current.value].map((k) => {
    const [rp, mk] = k.split('|')
    return { role_id: rp, menu_key: mk }
  })
  try {
    const result = await api.put<UpdateResponse>('/api/appadmin/role-menu', { mapping })
    successMsg.value = `Tersimpan: +${result.diff.added.length} added, −${result.diff.removed.length} removed`
    original.value = new Set(current.value)
  } catch (e) {
    if (e instanceof ApiError) {
      errorMsg.value = `${e.code}: ${e.message}`
    } else {
      errorMsg.value = 'Gagal menyimpan. Coba lagi.'
    }
  } finally {
    saving.value = false
  }
}

function toggleGroup(label: string) {
  const next = new Set(visibleGroups.value)
  if (next.has(label)) next.delete(label)
  else next.add(label)
  visibleGroups.value = next
}

function onBeforeUnloadHandler(e: BeforeUnloadEvent) {
  if (isDirty.value) {
    e.preventDefault()
    e.returnValue = ''
  }
}

onMounted(() => {
  load()
  window.addEventListener('beforeunload', onBeforeUnloadHandler)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', onBeforeUnloadHandler)
})

onBeforeRouteLeave(() => {
  if (isDirty.value) {
    return window.confirm(
      `Anda punya ${dirty.value.count} perubahan belum disimpan. Tinggalkan halaman?`
    )
  }
})
</script>

<template>
  <CrudLayout>
    <template #header>
      <PageHeader title="Mapping Role-Menu">
        <template #actions>
          <Button :disabled="loading || saving" variant="ghost" size="sm" @click="load">
            <RefreshCw class="w-4 h-4" /> Refresh
          </Button>
          <Button :disabled="!isDirty || saving" variant="outline" size="sm" @click="discard">
            <X class="w-4 h-4" /> Discard
          </Button>
          <Button :disabled="!isDirty || saving" size="sm" @click="save">
            <Loader2 v-if="saving" class="w-4 h-4 animate-spin" />
            <Save v-else class="w-4 h-4" />
            Save Changes
            <span v-if="isDirty" class="ml-1 text-xs opacity-75">({{ dirty.count }})</span>
          </Button>
        </template>
      </PageHeader>
    </template>

    <template #alert>
      <Alert v-if="errorMsg" variant="destructive">
        <AlertCircle class="w-4 h-4 shrink-0" />
        {{ errorMsg }}
      </Alert>
      <Alert v-else-if="successMsg" class="bg-positive/10 text-positive border-positive/30">
        <Check class="w-4 h-4 shrink-0" />
        {{ successMsg }}
      </Alert>
      <Alert v-else-if="isDirty" class="bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-900/20 dark:text-amber-300 dark:border-amber-700/40">
        Anda punya {{ dirty.count }} perubahan belum disimpan
      </Alert>
    </template>

    <template #filter>
      <FilterPanel>
        <FilterGroup label="Cari role">
          <div class="relative">
            <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted pointer-events-none" />
            <Input v-model="searchRole" placeholder="role_id atau nama..." class="pl-8 text-xs h-8" />
          </div>
        </FilterGroup>
        <FilterGroup label="Group menu">
          <div class="space-y-0.5">
            <label
              v-for="[groupLabel, items] in menuGroups"
              :key="groupLabel"
              class="flex items-center gap-2 text-xs cursor-pointer py-1 hover:text-foreground text-muted"
            >
              <input
                type="checkbox"
                :checked="visibleGroups.has(groupLabel)"
                class="rounded"
                @change="toggleGroup(groupLabel)"
              />
              <span>{{ groupLabel }} <span class="opacity-50">({{ items.length }})</span></span>
            </label>
          </div>
        </FilterGroup>
      </FilterPanel>
    </template>

    <template #data>
      <DataPanel title="Matrix Role-Menu" :loading="loading && roles.length === 0" :is-empty="!loading && filteredRoles.length === 0">
        <template #empty>Tidak ada role yang cocok dengan '{{ searchRole }}'</template>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="sticky top-0 z-10 text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
              <tr>
                <th class="text-left p-2 sticky left-0 bg-surface z-20 min-w-[180px] font-semibold">
                  Role
                </th>
                <th
                  v-for="m in filteredMenus"
                  :key="m.menu_key"
                  class="p-2 text-center min-w-[90px] cursor-pointer hover:bg-background transition-colors"
                  :title="`Klik untuk toggle semua: ${m.menu_key}`"
                  @click="toggleColumnAll(m.menu_key)"
                >
                  <div class="font-medium leading-tight">{{ m.label }}</div>
                  <div class="text-[9px] text-muted mt-0.5">{{ m.group_label }}</div>
                </th>
                <th class="p-2 text-center min-w-[60px] font-semibold">Bulk</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="role in filteredRoles"
                :key="role.role_id"
                class="border-b border-border hover:bg-background/50 transition-colors"
              >
                <td
                  class="p-2 sticky left-0 bg-surface"
                  :title="`${role.user_count} user`"
                >
                  <div class="font-mono font-semibold text-[11px]">{{ role.role_id }}</div>
                  <div class="text-[10px] text-muted">{{ role.role_name }}</div>
                </td>
                <td
                  v-for="m in filteredMenus"
                  :key="m.menu_key"
                  class="p-2 text-center transition-colors"
                  :class="isCellDirty(role.role_id, m.menu_key)
                    ? 'bg-amber-100 dark:bg-amber-900/30'
                    : ''"
                >
                  <input
                    type="checkbox"
                    :checked="isChecked(role.role_id, m.menu_key)"
                    :disabled="saving"
                    class="cursor-pointer disabled:cursor-not-allowed"
                    @change="toggleCell(role.role_id, m.menu_key)"
                  />
                </td>
                <td class="p-2 text-center">
                  <button
                    type="button"
                    class="text-[10px] underline text-muted hover:text-foreground transition-colors"
                    @click="toggleRowAll(role.role_id)"
                  >
                    Toggle
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </DataPanel>
    </template>
  </CrudLayout>
</template>

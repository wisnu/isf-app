<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { ChevronDown, ChevronRight, Download, RefreshCw, Save, X } from 'lucide-vue-next'

import { api, ApiError } from '@/shared/api/client'
import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'

// ── Types ─────────────────────────────────────────────────────────────────────

interface RoleInfo       { role_id: string; role_name: string; user_count: number }
interface MenuInfo       { menu_key: string; label: string; group_label: string; sort_order: number }
interface MenuPermission { menu_key: string; actions: string[] }

interface PermissionSnapshot {
  roles: RoleInfo[]
  menus: MenuInfo[]
  permissions: MenuPermission[]
}

interface UpdateResult {
  updated: boolean
  role_id: string
  added_count: number
  removed_count: number
}

const ACTIONS = [
  { key: 'view',   label: 'V', title: 'View' },
  { key: 'tambah', label: 'T', title: 'Tambah' },
  { key: 'edit',   label: 'E', title: 'Edit' },
  { key: 'hapus',  label: 'H', title: 'Hapus' },
  { key: 'detail', label: 'D', title: 'Detail' },
] as const

type ActionKey = typeof ACTIONS[number]['key']

// ── State ─────────────────────────────────────────────────────────────────────

const loading   = ref(false)
const saving    = ref(false)
const exporting = ref(false)
const error     = ref('')
const success   = ref('')

const allRoles = ref<RoleInfo[]>([])
const allMenus = ref<MenuInfo[]>([])

// selectedRoleId uses '' as "no selection" to match SearchSelect's string modelValue
const selectedRoleId = ref('')

// current: menu_key → Set of actions (editable copy)
// original: menu_key → Set of actions (snapshot for dirty tracking)
const current  = ref(new Map<string, Set<string>>())
const original = ref(new Map<string, Set<string>>())

const expandedGroups = ref(new Set<string>())

// ── Confirm modal (replaces window.confirm) ───────────────────────────────────

const showConfirmModal = ref(false)
const confirmMessage = ref('')
let confirmResolve: ((v: boolean) => void) | null = null

function confirmUnsaved(message: string): Promise<boolean> {
  confirmMessage.value = message
  showConfirmModal.value = true
  return new Promise(resolve => { confirmResolve = resolve })
}
function onConfirmOk() { showConfirmModal.value = false; confirmResolve?.(true) }
function onConfirmCancel() { showConfirmModal.value = false; confirmResolve?.(false) }

// ── Derived ───────────────────────────────────────────────────────────────────

const roleOptions = computed(() =>
  allRoles.value.map(r => ({
    value: r.role_id,
    label: `${r.role_id} — ${r.role_name}`,
  }))
)

const groupedMenus = computed(() => {
  const groups = new Map<string, MenuInfo[]>()
  for (const menu of allMenus.value) {
    if (!groups.has(menu.group_label)) groups.set(menu.group_label, [])
    groups.get(menu.group_label)!.push(menu)
  }
  return Array.from(groups.entries()).map(([label, menus]) => ({ label, menus }))
})

const isDirty = computed(() => {
  if (current.value.size !== original.value.size) return true
  for (const [mk, acts] of current.value) {
    const orig = original.value.get(mk) ?? new Set<string>()
    if (acts.size !== orig.size) return true
    for (const a of acts) if (!orig.has(a)) return true
  }
  return false
})

const dirtyCount = computed(() => {
  let count = 0
  const allKeys = new Set([...current.value.keys(), ...original.value.keys()])
  for (const mk of allKeys) {
    const curr = current.value.get(mk) ?? new Set<string>()
    const orig = original.value.get(mk) ?? new Set<string>()
    for (const a of ACTIONS.map(a => a.key)) {
      if (curr.has(a) !== orig.has(a)) count++
    }
  }
  return count
})

// ── Helpers ───────────────────────────────────────────────────────────────────

function hasAction(menuKey: string, action: string): boolean {
  return current.value.get(menuKey)?.has(action) ?? false
}

function isDirtyCell(menuKey: string, action: string): boolean {
  const curr = current.value.get(menuKey)?.has(action) ?? false
  const orig = original.value.get(menuKey)?.has(action) ?? false
  return curr !== orig
}

function activeMenuCount(group: { menus: MenuInfo[] }): number {
  return group.menus.filter(m => (current.value.get(m.menu_key)?.size ?? 0) > 0).length
}

function cloneMap(src: Map<string, Set<string>>): Map<string, Set<string>> {
  return new Map(Array.from(src.entries()).map(([k, v]) => [k, new Set(v)]))
}

function applySnapshot(permissions: MenuPermission[]) {
  const map = new Map<string, Set<string>>()
  for (const p of permissions) {
    map.set(p.menu_key, new Set(p.actions))
  }
  // Ensure all menus have an entry (even empty) so dirty checks work
  for (const m of allMenus.value) {
    if (!map.has(m.menu_key)) map.set(m.menu_key, new Set())
  }
  current.value  = map
  original.value = cloneMap(map)
}

// ── Data loading ──────────────────────────────────────────────────────────────

async function loadRoles() {
  if (allRoles.value.length > 0) return
  loading.value = true
  error.value   = ''
  try {
    // Load roles list from dedicated endpoint
    const response = await api.get<{ rows: RoleInfo[]; pagination: { page: number; limit: number; total: number; total_pages: number } }>(
      '/api/appadmin/roles?limit=200&status=active'
    )
    allRoles.value = response.rows
    // Menus will be loaded when a role is selected via loadPermissions()
  } catch (e: unknown) {
    error.value = e instanceof ApiError ? e.message : 'Gagal memuat daftar role'
  } finally {
    loading.value = false
  }
}

async function loadPermissions(roleId: string) {
  loading.value = true
  error.value   = ''
  success.value = ''
  try {
    const snap = await api.get<PermissionSnapshot>(
      `/api/appadmin/role-menu-permission?role_id=${encodeURIComponent(roleId)}`
    )
    // Update catalogs if not yet populated
    if (allRoles.value.length === 0) allRoles.value = snap.roles
    if (allMenus.value.length === 0)  allMenus.value  = snap.menus
    applySnapshot(snap.permissions)
    // Expand all groups on first load
    if (expandedGroups.value.size === 0) {
      expandedGroups.value = new Set(allMenus.value.map(m => m.group_label))
    }
  } catch (e: unknown) {
    error.value = e instanceof ApiError ? e.message : 'Gagal memuat permission'
  } finally {
    loading.value = false
  }
}

// ── Actions ───────────────────────────────────────────────────────────────────

function toggleAction(menuKey: string, action: ActionKey, event: Event) {
  const checked = (event.target as HTMLInputElement).checked
  const map = cloneMap(current.value)
  const actions = map.get(menuKey) ?? new Set<string>()
  const next = new Set(actions)

  if (action === 'view' && !checked) {
    // Unchecking view clears all actions
    next.clear()
  } else if (action !== 'view' && checked) {
    // Checking any non-view action also enables view
    next.add('view')
    next.add(action)
  } else {
    if (checked) next.add(action)
    else next.delete(action)
  }

  map.set(menuKey, next)
  current.value = map
}

function toggleGroup(groupLabel: string) {
  const next = new Set(expandedGroups.value)
  if (next.has(groupLabel)) next.delete(groupLabel)
  else next.add(groupLabel)
  expandedGroups.value = next
}

function activateAll(groupLabel: string) {
  const group = groupedMenus.value.find(g => g.label === groupLabel)
  if (!group) return
  const map = cloneMap(current.value)
  for (const m of group.menus) {
    map.set(m.menu_key, new Set(ACTIONS.map(a => a.key)))
  }
  current.value = map
}

function onDiscard() {
  current.value = cloneMap(original.value)
  success.value = ''
  error.value   = ''
}

async function onSave() {
  if (!selectedRoleId.value || !isDirty.value) return
  saving.value  = true
  error.value   = ''
  success.value = ''
  try {
    const permissions: MenuPermission[] = Array.from(current.value.entries())
      .filter(([, actSet]) => actSet.size > 0)
      .map(([menu_key, actSet]) => ({
        menu_key,
        actions: Array.from(actSet),
      }))
    const result = await api.put<UpdateResult>(
      '/api/appadmin/role-menu-permission',
      { role_id: selectedRoleId.value, permissions }
    )
    original.value = cloneMap(current.value)
    success.value  = `Tersimpan: +${result.added_count} ditambah, −${result.removed_count} dihapus`
  } catch (e: unknown) {
    error.value = e instanceof ApiError ? e.message : 'Gagal menyimpan permission'
  } finally {
    saving.value = false
  }
}

async function exportExcel() {
  exporting.value = true
  error.value     = ''
  try {
    await api.downloadBlob('/api/appadmin/role-menu-permission/export', 'role-menu-permission.xlsx')
  } catch (e: unknown) {
    error.value = e instanceof ApiError ? e.message : 'Gagal export Excel'
  } finally {
    exporting.value = false
  }
}

// ── Watchers ──────────────────────────────────────────────────────────────────

let reverting = false
watch(selectedRoleId, async (newId: string, oldId: string) => {
  if (reverting || !newId) return
  if (oldId && isDirty.value) {
    const ok = await confirmUnsaved('Ada perubahan yang belum disimpan. Lanjutkan pindah role?')
    if (!ok) {
      reverting = true
      selectedRoleId.value = oldId
      reverting = false
      return
    }
  }
  await loadPermissions(newId)
})

const beforeUnloadHandler = (e: BeforeUnloadEvent) => {
  if (isDirty.value) {
    e.preventDefault()
    e.returnValue = ''
  }
}
window.addEventListener('beforeunload', beforeUnloadHandler)
onBeforeUnmount(() => window.removeEventListener('beforeunload', beforeUnloadHandler))

onBeforeRouteLeave(async (_to: unknown, _from: unknown, next: (ok?: boolean) => void) => {
  if (!isDirty.value) return next()
  const ok = await confirmUnsaved('Ada perubahan yang belum disimpan. Keluar halaman?')
  next(ok)
})

// ── Init ──────────────────────────────────────────────────────────────────────

loadRoles()
</script>

<template>
  <!-- Confirm modal for unsaved-changes guard -->
  <Modal v-if="showConfirmModal" max-width="max-w-sm" @close="onConfirmCancel">
    <template #header>
      <span class="text-base font-semibold text-gray-900 dark:text-gray-100">Ada perubahan belum disimpan</span>
    </template>
    <p class="text-sm text-gray-600 dark:text-gray-300">{{ confirmMessage }}</p>
    <template #footer>
      <div class="flex justify-end gap-2">
        <Button variant="outline" size="sm" @click="onConfirmCancel">Batal</Button>
        <Button variant="destructive" size="sm" @click="onConfirmOk">Lanjutkan</Button>
      </div>
    </template>
  </Modal>

  <div class="flex flex-col gap-4 p-4 max-w-screen-xl mx-auto">

    <!-- Header -->
    <div class="flex items-center justify-between flex-wrap gap-2">
      <h1 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Pengaturan Menu</h1>
      <div class="flex items-center gap-2 flex-wrap">
        <Button variant="outline" size="sm" :disabled="exporting" @click="exportExcel">
          <Download class="w-3.5 h-3.5" />
          Export Excel
        </Button>
        <Button
          variant="outline"
          size="sm"
          :disabled="!selectedRoleId || loading"
          @click="selectedRoleId && loadPermissions(selectedRoleId)"
        >
          <RefreshCw class="w-3.5 h-3.5" :class="loading ? 'animate-spin' : ''" />
          Refresh
        </Button>
        <Button variant="outline" size="sm" :disabled="!isDirty" @click="onDiscard">
          <X class="w-3.5 h-3.5" />
          Discard
        </Button>
        <Button size="sm" :disabled="!isDirty || saving" @click="onSave">
          <Save class="w-3.5 h-3.5" />
          {{ saving ? 'Menyimpan...' : 'Simpan' }}
        </Button>
      </div>
    </div>

    <!-- Alerts -->
    <Alert v-if="error" variant="destructive">{{ error }}</Alert>
    <Alert
      v-if="success"
      class="bg-positive/10 text-positive border-positive/30"
    >{{ success }}</Alert>
    <Alert
      v-if="isDirty && !error && !success"
      class="bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-900/20 dark:text-amber-300 dark:border-amber-700/40"
    >
      {{ dirtyCount }} perubahan belum disimpan
    </Alert>

    <!-- Role picker -->
    <div class="flex items-center gap-3">
      <label class="text-sm font-medium text-gray-700 dark:text-gray-300 shrink-0">Role</label>
      <div class="w-72">
        <SearchSelect
          v-model="selectedRoleId"
          :options="roleOptions"
          placeholder="Pilih role..."
        />
      </div>
    </div>

    <!-- Prompt state: no role selected -->
    <div v-if="!selectedRoleId" class="flex items-center justify-center py-16 text-sm text-gray-400 italic">
      Pilih role untuk melihat dan mengatur permission menu.
    </div>

    <!-- Loading state -->
    <div v-else-if="loading" class="flex items-center justify-center py-16 text-sm text-gray-500">
      <RefreshCw class="w-4 h-4 animate-spin mr-2" />
      Memuat...
    </div>

    <!-- Accordion per group -->
    <div v-else class="space-y-2">
      <div
        v-for="group in groupedMenus"
        :key="group.label"
        class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
      >
        <!-- Group header -->
        <div class="w-full flex items-center justify-between px-4 py-2.5 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
          <button
            type="button"
            class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-200 cursor-pointer"
            @click="toggleGroup(group.label)"
          >
            <component
              :is="expandedGroups.has(group.label) ? ChevronDown : ChevronRight"
              class="w-4 h-4 shrink-0"
            />
            {{ group.label }}
            <span class="text-xs text-gray-400 font-normal">
              ({{ activeMenuCount(group) }} dari {{ group.menus.length }} menu aktif)
            </span>
          </button>
          <button
            type="button"
            class="text-xs text-emerald-600 hover:text-emerald-700 dark:text-emerald-400 px-2 py-0.5 border border-emerald-300 rounded hover:bg-emerald-50 dark:hover:bg-emerald-900/20 transition-colors shrink-0"
            @click="activateAll(group.label)"
          >
            Aktifkan Semua
          </button>
        </div>

        <!-- Menu table -->
        <div v-show="expandedGroups.has(group.label)" class="overflow-x-auto">
          <table class="w-full text-sm border-t border-gray-100 dark:border-gray-700">
            <thead>
              <tr class="bg-white dark:bg-gray-900">
                <th class="text-left px-4 py-2 text-xs font-medium text-gray-500 dark:text-gray-400">Menu</th>
                <th
                  v-for="action in ACTIONS"
                  :key="action.key"
                  class="px-3 py-2 text-xs font-medium text-gray-500 dark:text-gray-400 text-center w-12"
                  :title="action.title"
                >
                  {{ action.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="menu in group.menus"
                :key="menu.menu_key"
                class="border-t border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50"
              >
                <td class="px-4 py-2 text-gray-700 dark:text-gray-300">
                  <span>{{ menu.label }}</span>
                  <span class="ml-2 text-xs text-gray-400 font-mono">{{ menu.menu_key }}</span>
                </td>
                <td
                  v-for="action in ACTIONS"
                  :key="action.key"
                  class="px-3 py-2 text-center transition-colors"
                  :class="isDirtyCell(menu.menu_key, action.key)
                    ? 'bg-amber-50 dark:bg-amber-900/20'
                    : ''"
                >
                  <input
                    type="checkbox"
                    :checked="hasAction(menu.menu_key, action.key)"
                    :disabled="saving"
                    class="h-4 w-4 rounded border-gray-300 text-emerald-600 cursor-pointer disabled:cursor-not-allowed"
                    @change="toggleAction(menu.menu_key, action.key as ActionKey, $event)"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>

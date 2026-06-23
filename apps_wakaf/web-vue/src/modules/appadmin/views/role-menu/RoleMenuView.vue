<script setup lang="ts">
import { computed, onBeforeUnmount, ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { Download, RefreshCw, Save } from 'lucide-vue-next'

import { api, ApiError } from '@/shared/api/client'
import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'

// ── Types ─────────────────────────────────────────────────────────────────────

interface RoleInfo       { role_id: string; role_name: string; user_count: number }
interface MenuInfo       { menu_key: string; label: string; group_label: string; sort_order: number }
interface MenuPermission { menu_key: string; actions: string[] }

interface PermissionSnapshot {
  roles: RoleInfo[]
  menus: MenuInfo[]
  permissions: MenuPermission[]
}

// Domain mapping — sesuai domain rail
const DOMAIN_LABELS: Record<string, string> = {
  finance:       'Keuangan',
  distribution:  'Program / Penyaluran',
  fundraising:   'Penghimpunan',
  generalaffair: 'Administrasi & Umum',
  appadmin:      'Pengaturan Akses',
  dashboard:     'Dashboard',
}
const DOMAIN_ORDER = ['finance', 'distribution', 'fundraising', 'generalaffair', 'appadmin', 'dashboard']

function getDomain(menuKey: string): string { return menuKey.split('.')[0] ?? 'other' }
function getDomainLabel(menuKey: string): string {
  return DOMAIN_LABELS[getDomain(menuKey)] ?? getDomain(menuKey)
}

const ACTION_ROWS = [
  { key: 'view',   label: 'List (Lihat Daftar)' },
  { key: 'tambah', label: 'Create (Tambah Data)' },
  { key: 'detail', label: 'Read (Detail Data)' },
  { key: 'edit',   label: 'Edit (Ubah Data)' },
  { key: 'hapus',  label: 'Delete (Hapus Data)' },
] as const

type ActionKey = typeof ACTION_ROWS[number]['key']

// ── State ─────────────────────────────────────────────────────────────────────

const loading   = ref(false)
const saving    = ref(false)
const exporting = ref(false)
const error     = ref('')
const success   = ref('')

const allRoles = ref<RoleInfo[]>([])
const allMenus = ref<MenuInfo[]>([])

// current[role_id][menu_key] = Set<action>
const current  = ref(new Map<string, Map<string, Set<string>>>())
const original = ref(new Map<string, Map<string, Set<string>>>())

// Filters
const domainFilter  = ref('')   // '' = semua domain
const roleFilter    = ref('')   // '' = semua role (as column filter)
const pendingDomain = ref('')
const pendingRole   = ref('')

// Confirm modal
const showConfirmModal = ref(false)
const confirmMessage   = ref('')
let   confirmResolve: ((v: boolean) => void) | null = null

// ── Derived ───────────────────────────────────────────────────────────────────

// Ordered list of domains present in menu catalog
const domains = computed(() => {
  const present = new Set(allMenus.value.map((m: MenuInfo) => getDomain(m.menu_key)))
  return DOMAIN_ORDER.filter(d => present.has(d)).map(d => ({ id: d, label: DOMAIN_LABELS[d] ?? d }))
})

const visibleRoles = computed(() =>
  roleFilter.value ? allRoles.value.filter((r: RoleInfo) => r.role_id === roleFilter.value) : allRoles.value
)

const groupedMenus = computed(() => {
  const menus = domainFilter.value
    ? allMenus.value.filter((m: MenuInfo) => getDomain(m.menu_key) === domainFilter.value)
    : allMenus.value
  // Group by domain, ordered
  const groups = new Map<string, MenuInfo[]>()
  for (const m of menus) {
    const d = getDomain(m.menu_key)
    if (!groups.has(d)) groups.set(d, [])
    groups.get(d)!.push(m)
  }
  return DOMAIN_ORDER
    .filter(d => groups.has(d))
    .map(d => ({ id: d, label: DOMAIN_LABELS[d] ?? d, items: groups.get(d)! }))
})

const isDirty = computed(() => {
  for (const [rid, mmap] of current.value) {
    const orig = original.value.get(rid) ?? new Map()
    for (const [mk, acts] of mmap) {
      const o = orig.get(mk) ?? new Set()
      if (acts.size !== o.size) return true
      for (const a of acts) if (!o.has(a)) return true
    }
  }
  return false
})

const dirtyRoleIds = computed((): string[] => {
  const ids: string[] = []
  for (const [rid, mmap] of current.value) {
    const orig = original.value.get(rid) ?? new Map<string, Set<string>>()
    let dirty = false
    outer: for (const [mk, acts] of mmap) {
      const o = orig.get(mk) ?? new Set<string>()
      if (acts.size !== o.size) { dirty = true; break }
      for (const a of acts) { if (!o.has(a)) { dirty = true; break outer } }
    }
    if (dirty) ids.push(rid)
  }
  return ids
})

// ── Helpers ───────────────────────────────────────────────────────────────────

function hasAction(roleId: string, menuKey: string, action: string): boolean {
  return current.value.get(roleId)?.get(menuKey)?.has(action) ?? false
}

function isDirtyCell(roleId: string, menuKey: string, action: string): boolean {
  const c = current.value.get(roleId)?.get(menuKey)?.has(action) ?? false
  const o = original.value.get(roleId)?.get(menuKey)?.has(action) ?? false
  return c !== o
}

function cloneAll(src: Map<string, Map<string, Set<string>>>): Map<string, Map<string, Set<string>>> {
  return new Map(Array.from(src.entries()).map(([rid, mm]) =>
    [rid, new Map(Array.from(mm.entries()).map(([mk, acts]) => [mk, new Set(acts)]))]
  ))
}

function confirmUnsaved(msg: string): Promise<boolean> {
  confirmMessage.value = msg
  showConfirmModal.value = true
  return new Promise(resolve => { confirmResolve = resolve })
}
function onConfirmOk()     { showConfirmModal.value = false; confirmResolve?.(true) }
function onConfirmCancel() { showConfirmModal.value = false; confirmResolve?.(false) }

// ── Data loading ──────────────────────────────────────────────────────────────

async function loadAll() {
  loading.value = true
  error.value   = ''
  success.value = ''
  try {
    const rolesResp = await api.get<{ rows: RoleInfo[] }>('/api/appadmin/roles?limit=100')
    allRoles.value = rolesResp.rows

    // Fetch all roles' permissions in parallel
    const results = await Promise.all(
      rolesResp.rows.map(r =>
        api.get<PermissionSnapshot>(`/api/appadmin/role-menu-permission?role_id=${encodeURIComponent(r.role_id)}`)
          .then(snap => ({ role_id: r.role_id, snap }))
          .catch(() => null)
      )
    )

    const first = results.find(r => r !== null)
    if (first) allMenus.value = first.snap.menus

    const curr = new Map<string, Map<string, Set<string>>>()
    const orig = new Map<string, Map<string, Set<string>>>()
    for (const result of results) {
      if (!result) continue
      const mm = new Map<string, Set<string>>()
      for (const p of result.snap.permissions) mm.set(p.menu_key, new Set(p.actions))
      for (const m of allMenus.value) { if (!mm.has(m.menu_key)) mm.set(m.menu_key, new Set()) }
      curr.set(result.role_id, mm)
      orig.set(result.role_id, new Map(Array.from(mm.entries()).map(([k, v]) => [k, new Set(v)])))
    }
    current.value  = curr
    original.value = orig
  } catch (e: unknown) {
    error.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
}

// ── Actions ───────────────────────────────────────────────────────────────────

function toggleCell(roleId: string, menuKey: string, action: ActionKey, checked: boolean) {
  const map = cloneAll(current.value)
  if (!map.has(roleId)) map.set(roleId, new Map())
  const mm = new Map(map.get(roleId)!)
  const acts = new Set(mm.get(menuKey) ?? [])

  if (action === 'view' && !checked) {
    acts.clear()
  } else if (action !== 'view' && checked) {
    acts.add('view')
    acts.add(action)
  } else {
    if (checked) acts.add(action)
    else acts.delete(action)
  }

  mm.set(menuKey, acts)
  map.set(roleId, mm)
  current.value = map
}

function applyFilter() {
  domainFilter.value = pendingDomain.value
  roleFilter.value   = pendingRole.value
}

function onDiscard() {
  current.value = cloneAll(original.value)
  success.value = ''
  error.value   = ''
}

async function onSave() {
  if (!isDirty.value) return
  saving.value  = true
  error.value   = ''
  success.value = ''
  try {
    await Promise.all(
      dirtyRoleIds.value.map((roleId: string) => {
        const entries = Array.from(current.value.get(roleId)!.entries()) as [string, Set<string>][]
        const permissions = entries
          .filter(([, acts]) => acts.size > 0)
          .map(([menu_key, acts]) => ({ menu_key, actions: Array.from(acts) }))
        return api.put('/api/appadmin/role-menu-permission', { role_id: roleId, permissions })
      })
    )
    original.value = cloneAll(current.value)
    success.value  = `Tersimpan: ${dirtyRoleIds.value.length} role diperbarui`
  } catch (e: unknown) {
    error.value = e instanceof ApiError ? e.message : 'Gagal menyimpan'
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

// ── Guards ────────────────────────────────────────────────────────────────────

const beforeUnload = (e: BeforeUnloadEvent) => {
  if (isDirty.value) { e.preventDefault(); e.returnValue = '' }
}
window.addEventListener('beforeunload', beforeUnload)
onBeforeUnmount(() => window.removeEventListener('beforeunload', beforeUnload))

onBeforeRouteLeave(async (_to: unknown, _from: unknown, next: (ok?: boolean) => void) => {
  if (!isDirty.value) return next()
  const ok = await confirmUnsaved('Ada perubahan yang belum disimpan. Keluar halaman?')
  next(ok)
})

// ── Init ──────────────────────────────────────────────────────────────────────
loadAll()
</script>

<template>
  <div class="flex flex-col gap-4 p-4 max-w-screen-2xl">

    <!-- Confirm modal -->
    <Modal v-if="showConfirmModal" @close="onConfirmCancel">
      <template #header>Ada perubahan belum disimpan</template>
      <p class="text-sm text-gray-600 dark:text-gray-300">{{ confirmMessage }}</p>
      <template #footer>
        <Button variant="outline" size="sm" @click="onConfirmCancel">Batal</Button>
        <Button size="sm" @click="onConfirmOk">Lanjutkan</Button>
      </template>
    </Modal>

    <!-- Header -->
    <div class="flex items-start justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900 dark:text-gray-100">Manajemen Akses & Role</h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
          Atur matriks izin List, CRUD, dan fungsi khusus untuk setiap peran.
        </p>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <Button variant="outline" size="sm" :disabled="exporting" @click="exportExcel">
          <Download class="w-3.5 h-3.5 mr-1.5" />Export Excel
        </Button>
        <Button variant="outline" size="sm" :disabled="loading" @click="loadAll">
          <RefreshCw class="w-3.5 h-3.5 mr-1.5" :class="loading && 'animate-spin'" />Refresh
        </Button>
        <Button variant="outline" size="sm" :disabled="!isDirty" @click="onDiscard">
          Discard
        </Button>
        <Button size="sm" :disabled="!isDirty || saving" @click="onSave">
          <Save class="w-3.5 h-3.5 mr-1.5" />
          {{ saving ? 'Menyimpan...' : 'Simpan Perubahan' }}
        </Button>
      </div>
    </div>

    <!-- Alerts -->
    <Alert v-if="error"   type="error">{{ error }}</Alert>
    <Alert v-if="success" type="success">{{ success }}</Alert>
    <Alert v-if="isDirty && !error && !success" type="warning">
      {{ dirtyRoleIds.length }} role memiliki perubahan belum disimpan
    </Alert>

    <!-- Filters -->
    <div class="flex items-end gap-4">
      <div class="flex-1 max-w-sm">
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
          Domain / Modul Aplikasi
        </label>
        <select
          v-model="pendingDomain"
          class="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800
                 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-emerald-500"
        >
          <option value="">Semua Domain</option>
          <option v-for="d in domains" :key="d.id" :value="d.id">{{ d.label }}</option>
        </select>
      </div>
      <div class="flex-1 max-w-sm">
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">
          Filter Role (Tampilan Kolom)
        </label>
        <select
          v-model="pendingRole"
          class="w-full rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800
                 px-3 py-2 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-1 focus:ring-emerald-500"
        >
          <option value="">Semua Role</option>
          <option v-for="r in allRoles" :key="r.role_id" :value="r.role_id">
            {{ r.role_name }} ({{ r.role_id }})
          </option>
        </select>
      </div>
      <Button variant="outline" @click="applyFilter">Terapkan Filter</Button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-sm text-gray-400 italic text-center py-8">Memuat data...</div>

    <!-- Matrix table -->
    <div v-else-if="allRoles.length && allMenus.length" class="overflow-x-auto border border-gray-200 dark:border-gray-700 rounded-lg">
      <table class="w-full text-sm border-collapse">
        <thead>
          <tr class="bg-gray-800 dark:bg-gray-900 text-white">
            <th class="px-4 py-3 text-left font-semibold sticky left-0 bg-gray-800 dark:bg-gray-900 min-w-64 w-72">
              Menu & Hak Akses
            </th>
            <th
              v-for="role in visibleRoles"
              :key="role.role_id"
              class="px-4 py-3 text-center font-semibold min-w-28 whitespace-nowrap"
            >
              {{ role.role_name }}
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-for="group in groupedMenus" :key="group.id">
            <!-- Domain section header -->
            <tr class="bg-gray-800 dark:bg-gray-950 border-t-4 border-gray-600">
              <td
                :colspan="visibleRoles.length + 1"
                class="px-4 py-2 sticky left-0 bg-gray-800 dark:bg-gray-950"
              >
                <span class="text-sm font-bold text-white tracking-wide uppercase">
                  {{ group.label }}
                </span>
              </td>
            </tr>
            <template v-for="menu in group.items" :key="menu.menu_key">
              <!-- Menu header row -->
              <tr class="bg-gray-100 dark:bg-gray-800/60 border-t border-gray-300 dark:border-gray-600">
                <td
                  :colspan="visibleRoles.length + 1"
                  class="px-4 py-2 pl-6 sticky left-0 bg-gray-100 dark:bg-gray-800/60"
                >
                  <span class="text-sm font-semibold text-gray-700 dark:text-gray-200">
                    📁 {{ menu.label }}
                  </span>
                </td>
              </tr>
              <!-- Action sub-rows -->
              <tr
                v-for="actionRow in ACTION_ROWS"
                :key="`${menu.menu_key}:${actionRow.key}`"
                class="border-t border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-800/20"
              >
                <td class="px-4 py-1.5 pl-12 text-gray-600 dark:text-gray-300 sticky left-0 bg-white dark:bg-gray-900 hover:bg-gray-50 dark:hover:bg-gray-800/20">
                  <span class="text-gray-400 mr-1.5 text-xs">↳</span>{{ actionRow.label }}
                </td>
                <td
                  v-for="role in visibleRoles"
                  :key="role.role_id"
                  class="py-1.5 text-center border-l border-gray-100 dark:border-gray-700/30"
                  :class="isDirtyCell(role.role_id, menu.menu_key, actionRow.key)
                    ? 'bg-amber-50 dark:bg-amber-900/20'
                    : ''"
                >
                  <input
                    type="checkbox"
                    :checked="hasAction(role.role_id, menu.menu_key, actionRow.key)"
                    class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                    @change="toggleCell(role.role_id, menu.menu_key, actionRow.key as ActionKey, ($event.target as HTMLInputElement).checked)"
                  />
                </td>
              </tr>
            </template>
          </template>
        </tbody>
      </table>
    </div>

  </div>
</template>

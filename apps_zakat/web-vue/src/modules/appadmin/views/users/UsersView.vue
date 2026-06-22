<script setup lang="ts">
import { KeyRound, Pencil, Plus, Search, ShieldCheck, UserCheck, UserX } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'

interface RoleOption { role_id: string; role_name: string }
interface BranchOption { branch_code: string; branch_name: string }

interface UserListItem {
  user_id: string
  display_name: string
  status: string
  is_locked: boolean
  primary_branch: string | null
  branch_access: string
  role_ids: string[]
}

interface UserDetail extends UserListItem {
  roles: { role_id: string; role_name: string }[]
  allowed_branches: string[]
}

interface ListResp { rows: UserListItem[]; pagination: { page: number; limit: number; total: number; total_pages: number } }

const toast = useToast()
const auth = useAuthStore()

const rows = ref<UserListItem[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const pageSize = shallowRef(25)
const searchInput = ref('')
const statusFilter = ref('')

const allRoles = ref<RoleOption[]>([])
const allBranches = ref<BranchOption[]>([])

// ----- create/edit modal -----
const showModal = shallowRef(false)
const isEdit = shallowRef(false)
const saving = shallowRef(false)
const form = reactive({
  user_id: '',
  display_name: '',
  password: '',
  confirm_password: '',
  primary_branch: '',
  branch_access: 'single',
  selected_roles: [] as string[],
  selected_branches: [] as string[],
})
const formErrors = reactive<Record<string, string>>({})

// ----- reset password modal -----
const showPasswordModal = shallowRef(false)
const passwordTarget = ref<UserListItem | null>(null)
const newPassword = ref('')
const confirmNewPassword = ref('')
const savingPassword = shallowRef(false)

// ----- deactivate/activate confirm modal -----
const showStatusModal = shallowRef(false)
const statusTarget = ref<UserListItem | null>(null)
const savingStatus = shallowRef(false)

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})
watch(statusFilter, () => { page.value = 1; loadData() })

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), limit: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('keyword', searchInput.value.trim())
    if (statusFilter.value) params.set('status', statusFilter.value)
    const res = await api.get<ListResp>(`/api/appadmin/users?${params}`)
    rows.value = res.rows
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data user'
  } finally {
    loading.value = false
  }
}

async function loadRolesAndBranches() {
  const [roleRes, branchRes] = await Promise.allSettled([
    api.get<{ rows: RoleOption[] }>('/api/appadmin/roles?limit=100&status=active'),
    api.get<{ rows: BranchOption[] }>('/api/appadmin/branches/parents'),
  ])
  if (roleRes.status === 'fulfilled') allRoles.value = roleRes.value.rows
  if (branchRes.status === 'fulfilled') allBranches.value = branchRes.value.rows
}

function openCreate() {
  isEdit.value = false
  Object.assign(form, { user_id: '', display_name: '', password: '', confirm_password: '', primary_branch: '', branch_access: 'single', selected_roles: [], selected_branches: [] })
  Object.keys(formErrors).forEach(k => delete formErrors[k])
  showModal.value = true
}

async function openEdit(row: UserListItem) {
  isEdit.value = true
  const detail = await api.get<UserDetail>(`/api/appadmin/users/${row.user_id}`)
  Object.assign(form, {
    user_id: detail.user_id,
    display_name: detail.display_name,
    password: '',
    confirm_password: '',
    primary_branch: detail.primary_branch ?? '',
    branch_access: detail.branch_access,
    selected_roles: detail.roles.map(r => r.role_id),
    selected_branches: detail.allowed_branches,
  })
  Object.keys(formErrors).forEach(k => delete formErrors[k])
  showModal.value = true
}

function validateForm(): boolean {
  Object.keys(formErrors).forEach(k => delete formErrors[k])
  if (!form.user_id.trim() && !isEdit.value) formErrors.user_id = 'ID User wajib diisi'
  if (!form.display_name.trim()) formErrors.display_name = 'Nama wajib diisi'
  if (!isEdit.value) {
    if (!form.password) formErrors.password = 'Password wajib diisi'
    else if (form.password.length < 8) formErrors.password = 'Password minimal 8 karakter'
    else if (form.password !== form.confirm_password) formErrors.confirm_password = 'Konfirmasi password tidak cocok'
  }
  if (!form.primary_branch) formErrors.primary_branch = 'Cabang utama wajib dipilih'
  return Object.keys(formErrors).length === 0
}

async function saveUser() {
  if (!validateForm()) return
  saving.value = true
  try {
    if (isEdit.value) {
      await api.put(`/api/appadmin/users/${form.user_id}`, {
        display_name: form.display_name,
        primary_branch: form.primary_branch,
        branch_access: form.branch_access,
      })
      await api.put(`/api/appadmin/users/${form.user_id}/roles`, { roles: form.selected_roles })
      await api.put(`/api/appadmin/users/${form.user_id}/branches`, { branches: Array.from(new Set([form.primary_branch, ...form.selected_branches])) })
      toast.success('Data user berhasil diperbarui')
    } else {
      await api.post('/api/appadmin/users', {
        user_id: form.user_id.trim().toUpperCase(),
        display_name: form.display_name,
        password: form.password,
        primary_branch: form.primary_branch,
        branch_access: form.branch_access,
        roles: form.selected_roles,
        branches: Array.from(new Set([form.primary_branch, ...form.selected_branches])),
      })
      toast.success('User berhasil dibuat')
    }
    showModal.value = false
    await loadData()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan user')
  } finally {
    saving.value = false
  }
}

function openPasswordReset(row: UserListItem) {
  passwordTarget.value = row
  newPassword.value = ''
  confirmNewPassword.value = ''
  showPasswordModal.value = true
}

async function savePassword() {
  if (!newPassword.value || newPassword.value.length < 8) {
    toast.error('Password minimal 8 karakter')
    return
  }
  if (newPassword.value !== confirmNewPassword.value) {
    toast.error('Konfirmasi password tidak cocok')
    return
  }
  savingPassword.value = true
  try {
    await api.put(`/api/appadmin/users/${passwordTarget.value!.user_id}/password`, {
      new_password: newPassword.value,
    })
    toast.success('Password berhasil direset')
    showPasswordModal.value = false
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal reset password')
  } finally {
    savingPassword.value = false
  }
}

function openStatusToggle(row: UserListItem) {
  statusTarget.value = row
  showStatusModal.value = true
}

async function confirmStatusToggle() {
  if (!statusTarget.value) return
  savingStatus.value = true
  const newStatus = statusTarget.value.status === 'active' ? 'inactive' : 'active'
  try {
    await api.patch(`/api/appadmin/users/${statusTarget.value.user_id}/status`, { status: newStatus })
    toast.success(newStatus === 'active' ? 'User berhasil diaktifkan' : 'User berhasil dinonaktifkan')
    showStatusModal.value = false
    await loadData()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal mengubah status user')
  } finally {
    savingStatus.value = false
  }
}

function toggleRole(roleId: string) {
  const idx = form.selected_roles.indexOf(roleId)
  if (idx === -1) form.selected_roles.push(roleId)
  else form.selected_roles.splice(idx, 1)
}

function toggleBranch(code: string) {
  const idx = form.selected_branches.indexOf(code)
  if (idx === -1) form.selected_branches.push(code)
  else form.selected_branches.splice(idx, 1)
}

onMounted(async () => {
  await Promise.all([loadData(), loadRolesAndBranches()])
})
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <PageHeader
      title="Manajemen User"
      subtitle="Kelola akun pengguna, role, dan akses cabang"
    />

    <div v-if="errorMsg" class="rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Table container -->
    <div class="rounded border border-border overflow-hidden bg-white">
      <!-- Toolbar -->
      <div class="flex flex-wrap items-center gap-2 rounded-t border-b border-border bg-white px-4 py-3">
        <div class="relative flex-1 min-w-[180px]">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted" />
          <input
            v-model="searchInput"
            placeholder="Cari ID / nama user..."
            class="h-9 w-full rounded border border-border pl-8 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        <select
          v-model="statusFilter"
          class="h-9 rounded border border-border px-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="">Semua Status</option>
          <option value="active">Aktif</option>
          <option value="inactive">Tidak Aktif</option>
        </select>

        <Button
          v-if="auth.hasMenu('appadmin.users.create')"
          size="sm"
          class="gap-1.5 h-9 ml-auto"
          @click="openCreate"
        >
          <Plus class="w-3.5 h-3.5" />
          Input User Baru
        </Button>
      </div>

      <!-- Pagination bar -->
      <div class="flex items-center justify-between border-b border-border bg-white px-4 py-2">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} user
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          :page-size-options="[25, 50, 100]"
          @prev="() => { if (page > 1) { page.value--; loadData() } }"
          @next="() => { if (page < totalPages) { page.value++; loadData() } }"
          @update:page-size="(s) => { pageSize.value = s; page.value = 1; loadData() }"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-surface-50">
            <tr>
              <th class="px-4 py-2 text-left font-medium">ID User</th>
              <th class="px-4 py-2 text-left font-medium">Nama</th>
              <th class="px-4 py-2 text-left font-medium">Role</th>
              <th class="px-4 py-2 text-left font-medium">Cabang Utama</th>
              <th class="px-4 py-2 text-left font-medium">Akses Cabang</th>
              <th class="px-4 py-2 text-left font-medium">Status</th>
              <th class="px-4 py-2 text-left font-medium">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="7" class="px-4 py-8 text-center text-muted text-sm">Memuat data...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="7" class="px-4 py-8 text-center text-muted text-sm">Tidak ada user ditemukan</td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.user_id"
              class="border-t border-border hover:bg-surface-50 transition-colors"
            >
              <td class="px-4 py-2 font-mono text-xs font-medium">{{ row.user_id }}</td>
              <td class="px-4 py-2">{{ row.display_name }}</td>
              <td class="px-4 py-2">
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="rid in row.role_ids.slice(0, 3)"
                    :key="rid"
                    class="inline-flex items-center rounded-full bg-blue-50 px-2 py-0.5 text-[10px] font-medium text-blue-700"
                  >{{ rid }}</span>
                  <span
                    v-if="row.role_ids.length > 3"
                    class="inline-flex items-center rounded-full bg-surface-100 px-2 py-0.5 text-[10px] text-muted"
                  >+{{ row.role_ids.length - 3 }}</span>
                  <span v-if="row.role_ids.length === 0" class="text-[11px] text-muted">—</span>
                </div>
              </td>
              <td class="px-4 py-2 font-mono text-xs">{{ row.primary_branch ?? '—' }}</td>
              <td class="px-4 py-2">
                <span
                  :class="row.branch_access === 'all'
                    ? 'bg-teal-50 text-teal-700'
                    : 'bg-surface-100 text-muted'"
                  class="inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-medium"
                >
                  {{ row.branch_access === 'all' ? 'Seluruh' : 'Tunggal' }}
                </span>
              </td>
              <td class="px-4 py-2">
                <span
                  :class="row.status === 'active'
                    ? 'bg-green-50 text-green-700'
                    : 'bg-red-50 text-red-600'"
                  class="inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-medium"
                >
                  {{ row.status === 'active' ? 'Aktif' : 'Tidak Aktif' }}
                  <span v-if="row.is_locked" class="ml-1 text-[9px]">(Terkunci)</span>
                </span>
              </td>
              <td class="px-4 py-2">
                <div class="flex items-center gap-1">
                  <button
                    v-if="auth.hasMenu('appadmin.users.edit')"
                    class="rounded border border-border p-1 text-muted hover:border-primary hover:text-primary transition"
                    title="Edit"
                    @click="openEdit(row)"
                  >
                    <Pencil class="w-3.5 h-3.5" />
                  </button>
                  <button
                    v-if="auth.hasMenu('appadmin.users.edit')"
                    class="rounded border border-border p-1 text-muted hover:border-amber-500 hover:text-amber-500 transition"
                    title="Reset Password"
                    @click="openPasswordReset(row)"
                  >
                    <KeyRound class="w-3.5 h-3.5" />
                  </button>
                  <button
                    v-if="auth.hasMenu('appadmin.users.edit')"
                    :class="row.status === 'active'
                      ? 'hover:border-red-400 hover:text-red-500'
                      : 'hover:border-green-500 hover:text-green-600'"
                    class="rounded border border-border p-1 text-muted transition"
                    :title="row.status === 'active' ? 'Nonaktifkan' : 'Aktifkan'"
                    @click="openStatusToggle(row)"
                  >
                    <UserX v-if="row.status === 'active'" class="w-3.5 h-3.5" />
                    <UserCheck v-else class="w-3.5 h-3.5" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Modal v-if="showModal" max-width="max-w-2xl" @close="showModal = false">
      <template #header>
        <h2 class="text-base font-semibold">
          {{ isEdit ? 'Koreksi Data User' : 'Input User Baru' }}
        </h2>
      </template>

      <div class="space-y-4">
        <!-- ID User (create only) -->
        <div v-if="!isEdit">
          <label class="mb-1 block text-xs font-medium text-muted">ID User Login <span class="text-red-500">*</span></label>
          <input
            v-model="form.user_id"
            placeholder="Contoh: HUSAIN"
            :class="formErrors.user_id ? 'border-red-400' : 'border-border'"
            class="h-9 w-full rounded border px-3 text-sm uppercase focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <p v-if="formErrors.user_id" class="mt-0.5 text-[11px] text-red-500">{{ formErrors.user_id }}</p>
        </div>
        <div v-else class="flex items-center gap-2 rounded bg-surface-50 px-3 py-2 text-sm">
          <span class="text-muted text-xs">ID User:</span>
          <span class="font-mono font-medium">{{ form.user_id }}</span>
        </div>

        <!-- Nama -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted">Nama Lengkap <span class="text-red-500">*</span></label>
          <input
            v-model="form.display_name"
            placeholder="Nama lengkap user"
            :class="formErrors.display_name ? 'border-red-400' : 'border-border'"
            class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <p v-if="formErrors.display_name" class="mt-0.5 text-[11px] text-red-500">{{ formErrors.display_name }}</p>
        </div>

        <!-- Password (create only) -->
        <template v-if="!isEdit">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-medium text-muted">Password <span class="text-red-500">*</span></label>
              <input
                v-model="form.password"
                type="password"
                placeholder="Min. 8 karakter"
                :class="formErrors.password ? 'border-red-400' : 'border-border'"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <p v-if="formErrors.password" class="mt-0.5 text-[11px] text-red-500">{{ formErrors.password }}</p>
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium text-muted">Konfirmasi Password <span class="text-red-500">*</span></label>
              <input
                v-model="form.confirm_password"
                type="password"
                placeholder="Ulangi password"
                :class="formErrors.confirm_password ? 'border-red-400' : 'border-border'"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              />
              <p v-if="formErrors.confirm_password" class="mt-0.5 text-[11px] text-red-500">{{ formErrors.confirm_password }}</p>
            </div>
          </div>
        </template>

        <!-- Cabang Utama + Tipe Akses -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted">Cabang Utama <span class="text-red-500">*</span></label>
            <SearchSelect
              v-model="form.primary_branch"
              :options="allBranches.map(b => ({ value: b.branch_code, label: `${b.branch_code} — ${b.branch_name}` }))"
              placeholder="Pilih cabang..."
            />
            <p v-if="formErrors.primary_branch" class="mt-0.5 text-[11px] text-red-500">{{ formErrors.primary_branch }}</p>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted">Tipe Akses Cabang</label>
            <select
              v-model="form.branch_access"
              class="h-9 w-full rounded border border-border px-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="single">Tunggal (Cabang Utama saja)</option>
              <option value="all">Seluruh Cabang</option>
            </select>
          </div>
        </div>

        <!-- Role Selection -->
        <div>
          <label class="mb-1.5 block text-xs font-medium text-muted">
            <ShieldCheck class="inline w-3.5 h-3.5 mr-1" />
            Role Pengguna
          </label>
          <div class="flex flex-wrap gap-2 rounded border border-border p-3">
            <label
              v-for="role in allRoles"
              :key="role.role_id"
              class="flex items-center gap-1.5 cursor-pointer"
            >
              <input
                type="checkbox"
                :checked="form.selected_roles.includes(role.role_id)"
                class="rounded border-border"
                @change="toggleRole(role.role_id)"
              />
              <span class="text-xs">{{ role.role_id }} — {{ role.role_name }}</span>
            </label>
            <span v-if="allRoles.length === 0" class="text-xs text-muted">Tidak ada role tersedia</span>
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" @click="showModal = false">Batal</Button>
          <Button variant="success" :disabled="saving" @click="saveUser">
            {{ saving ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Reset Password Modal -->
    <Modal v-if="showPasswordModal" max-width="max-w-sm" @close="showPasswordModal = false">
      <template #header>
        <h2 class="text-base font-semibold">Reset Password</h2>
      </template>

      <div class="space-y-3">
        <div class="rounded bg-surface-50 px-3 py-2 text-sm">
          <span class="text-muted text-xs">User:</span>
          <span class="ml-2 font-mono font-medium">{{ passwordTarget?.user_id }}</span>
          <span class="ml-2 text-xs text-muted">{{ passwordTarget?.display_name }}</span>
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-muted">Password Baru</label>
          <input v-model="newPassword" type="password" placeholder="Min. 8 karakter"
                 class="h-9 w-full rounded border border-border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-muted">Konfirmasi Password</label>
          <input v-model="confirmNewPassword" type="password" placeholder="Ulangi password"
                 class="h-9 w-full rounded border border-border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" @click="showPasswordModal = false">Batal</Button>
          <Button variant="success" :disabled="savingPassword" @click="savePassword">
            {{ savingPassword ? 'Menyimpan...' : 'Reset Password' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Status Toggle Confirm Modal -->
    <Modal v-if="showStatusModal" max-width="max-w-sm" @close="showStatusModal = false">
      <template #header>
        <h2 class="text-base font-semibold">
          {{ statusTarget?.status === 'active' ? 'Nonaktifkan User' : 'Aktifkan User' }}
        </h2>
      </template>

      <div class="space-y-3">
        <div class="rounded border border-border p-3 text-sm space-y-1.5">
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">ID User</span>
            <span class="font-mono text-xs font-medium">{{ statusTarget?.user_id }}</span>
          </div>
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">Nama</span>
            <span class="text-xs">{{ statusTarget?.display_name }}</span>
          </div>
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">Status saat ini</span>
            <span class="text-xs">{{ statusTarget?.status === 'active' ? 'Aktif' : 'Tidak Aktif' }}</span>
          </div>
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">Cabang Utama</span>
            <span class="font-mono text-xs">{{ statusTarget?.primary_branch ?? '—' }}</span>
          </div>
        </div>
        <p class="text-sm text-muted">
          {{ statusTarget?.status === 'active'
            ? 'User tidak akan dapat login setelah dinonaktifkan.'
            : 'User akan dapat login kembali setelah diaktifkan.' }}
        </p>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" @click="showStatusModal = false">Batal</Button>
          <Button
            :variant="statusTarget?.status === 'active' ? 'destructive' : 'success'"
            :disabled="savingStatus"
            @click="confirmStatusToggle"
          >
            {{ savingStatus ? 'Memproses...' : (statusTarget?.status === 'active' ? 'Nonaktifkan' : 'Aktifkan') }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

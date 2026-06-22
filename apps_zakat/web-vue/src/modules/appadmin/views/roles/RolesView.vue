<script setup lang="ts">
import { Pencil, Plus, Search, ShieldCheck, ShieldOff } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'

interface RoleListItem {
  role_id: string
  role_name: string
  description: string | null
  status: string
  user_count: number
}

interface ListResp { rows: RoleListItem[]; pagination: { page: number; limit: number; total: number; total_pages: number } }

const toast = useToast()
const auth = useAuthStore()

const rows = ref<RoleListItem[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const pageSize = shallowRef(25)
const searchInput = ref('')
const statusFilter = ref('')

// ----- create/edit modal -----
const showModal = shallowRef(false)
const isEdit = shallowRef(false)
const saving = shallowRef(false)
const form = reactive({ role_id: '', role_name: '', description: '' })
const formErrors = reactive<Record<string, string>>({})

// ----- status toggle modal -----
const showStatusModal = shallowRef(false)
const statusTarget = ref<RoleListItem | null>(null)
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
    const res = await api.get<ListResp>(`/api/appadmin/roles?${params}`)
    rows.value = res.rows
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data role'
  } finally {
    loading.value = false
  }
}

function openCreate() {
  isEdit.value = false
  Object.assign(form, { role_id: '', role_name: '', description: '' })
  Object.keys(formErrors).forEach(k => delete formErrors[k])
  showModal.value = true
}

function openEdit(row: RoleListItem) {
  isEdit.value = true
  Object.assign(form, { role_id: row.role_id, role_name: row.role_name, description: row.description ?? '' })
  Object.keys(formErrors).forEach(k => delete formErrors[k])
  showModal.value = true
}

function validate(): boolean {
  Object.keys(formErrors).forEach(k => delete formErrors[k])
  if (!form.role_id.trim() && !isEdit.value) formErrors.role_id = 'ID Role wajib diisi'
  if (!form.role_name.trim()) formErrors.role_name = 'Nama Role wajib diisi'
  return Object.keys(formErrors).length === 0
}

async function saveRole() {
  if (!validate()) return
  saving.value = true
  try {
    if (isEdit.value) {
      await api.put(`/api/appadmin/roles/${form.role_id}`, {
        role_name: form.role_name,
        description: form.description || null,
      })
      toast.success('Role berhasil diperbarui')
    } else {
      await api.post('/api/appadmin/roles', {
        role_id: form.role_id.trim().toUpperCase(),
        role_name: form.role_name,
        description: form.description || null,
      })
      toast.success('Role berhasil dibuat')
    }
    showModal.value = false
    await loadData()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan role')
  } finally {
    saving.value = false
  }
}

function openStatusToggle(row: RoleListItem) {
  statusTarget.value = row
  showStatusModal.value = true
}

async function confirmStatusToggle() {
  if (!statusTarget.value) return
  savingStatus.value = true
  const newStatus = statusTarget.value.status === 'active' ? 'inactive' : 'active'
  try {
    await api.patch(`/api/appadmin/roles/${statusTarget.value.role_id}/status`, { status: newStatus })
    toast.success(newStatus === 'active' ? 'Role berhasil diaktifkan' : 'Role berhasil dinonaktifkan')
    showStatusModal.value = false
    await loadData()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal mengubah status role')
  } finally {
    savingStatus.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <PageHeader
      title="Manajemen Role"
      subtitle="Kelola role / peran pengguna sistem"
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
            placeholder="Cari ID / nama role..."
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
          v-if="auth.hasMenu('appadmin.roles.create')"
          size="sm"
          class="gap-1.5 h-9 ml-auto"
          @click="openCreate"
        >
          <Plus class="w-3.5 h-3.5" />
          Input Role Baru
        </Button>
      </div>

      <!-- Pagination bar -->
      <div class="flex items-center justify-between border-b border-border bg-white px-4 py-2">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} role
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
              <th class="px-4 py-2 text-left font-medium">ID Role</th>
              <th class="px-4 py-2 text-left font-medium">Nama Role</th>
              <th class="px-4 py-2 text-left font-medium">Deskripsi</th>
              <th class="px-4 py-2 text-center font-medium">Jumlah User</th>
              <th class="px-4 py-2 text-left font-medium">Status</th>
              <th class="px-4 py-2 text-left font-medium">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6" class="px-4 py-8 text-center text-muted text-sm">Memuat data...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="6" class="px-4 py-8 text-center text-muted text-sm">Tidak ada role ditemukan</td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.role_id"
              class="border-t border-border hover:bg-surface-50 transition-colors"
            >
              <td class="px-4 py-2 font-mono text-xs font-medium">{{ row.role_id }}</td>
              <td class="px-4 py-2">{{ row.role_name }}</td>
              <td class="px-4 py-2 text-sm text-muted">{{ row.description ?? '—' }}</td>
              <td class="px-4 py-2 text-center">
                <span class="inline-flex items-center rounded-full bg-surface-100 px-2 py-0.5 text-[11px] font-medium">
                  {{ row.user_count }}
                </span>
              </td>
              <td class="px-4 py-2">
                <span
                  :class="row.status === 'active' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-600'"
                  class="inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-medium"
                >
                  {{ row.status === 'active' ? 'Aktif' : 'Tidak Aktif' }}
                </span>
              </td>
              <td class="px-4 py-2">
                <div class="flex items-center gap-1">
                  <button
                    v-if="auth.hasMenu('appadmin.roles.edit')"
                    class="rounded border border-border p-1 text-muted hover:border-primary hover:text-primary transition"
                    title="Edit"
                    @click="openEdit(row)"
                  >
                    <Pencil class="w-3.5 h-3.5" />
                  </button>
                  <button
                    v-if="auth.hasMenu('appadmin.roles.edit')"
                    :class="row.status === 'active' ? 'hover:border-red-400 hover:text-red-500' : 'hover:border-green-500 hover:text-green-600'"
                    class="rounded border border-border p-1 text-muted transition"
                    :title="row.status === 'active' ? 'Nonaktifkan' : 'Aktifkan'"
                    @click="openStatusToggle(row)"
                  >
                    <ShieldOff v-if="row.status === 'active'" class="w-3.5 h-3.5" />
                    <ShieldCheck v-else class="w-3.5 h-3.5" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Modal v-if="showModal" max-width="max-w-md" @close="showModal = false">
      <template #header>
        <h2 class="text-base font-semibold">
          {{ isEdit ? 'Koreksi Data Role' : 'Input Role Baru' }}
        </h2>
      </template>

      <div class="space-y-4">
        <!-- ID Role (create only) -->
        <div v-if="!isEdit">
          <label class="mb-1 block text-xs font-medium text-muted">ID Role <span class="text-red-500">*</span></label>
          <input
            v-model="form.role_id"
            placeholder="Contoh: SPVDIST"
            :class="formErrors.role_id ? 'border-red-400' : 'border-border'"
            class="h-9 w-full rounded border px-3 text-sm uppercase focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <p v-if="formErrors.role_id" class="mt-0.5 text-[11px] text-red-500">{{ formErrors.role_id }}</p>
        </div>
        <div v-else class="flex items-center gap-2 rounded bg-surface-50 px-3 py-2 text-sm">
          <span class="text-muted text-xs">ID Role:</span>
          <span class="font-mono font-medium">{{ form.role_id }}</span>
        </div>

        <div>
          <label class="mb-1 block text-xs font-medium text-muted">Nama Role <span class="text-red-500">*</span></label>
          <input
            v-model="form.role_name"
            placeholder="Nama role / peran"
            :class="formErrors.role_name ? 'border-red-400' : 'border-border'"
            class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <p v-if="formErrors.role_name" class="mt-0.5 text-[11px] text-red-500">{{ formErrors.role_name }}</p>
        </div>

        <div>
          <label class="mb-1 block text-xs font-medium text-muted">Deskripsi</label>
          <input
            v-model="form.description"
            placeholder="Deskripsi singkat (opsional)"
            class="h-9 w-full rounded border border-border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" @click="showModal = false">Batal</Button>
          <Button variant="success" :disabled="saving" @click="saveRole">
            {{ saving ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Status Toggle Confirm Modal -->
    <Modal v-if="showStatusModal" max-width="max-w-sm" @close="showStatusModal = false">
      <template #header>
        <h2 class="text-base font-semibold">
          {{ statusTarget?.status === 'active' ? 'Nonaktifkan Role' : 'Aktifkan Role' }}
        </h2>
      </template>

      <div class="space-y-3">
        <div class="rounded border border-border p-3 text-sm space-y-1.5">
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">ID Role</span>
            <span class="font-mono text-xs font-medium">{{ statusTarget?.role_id }}</span>
          </div>
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">Nama Role</span>
            <span class="text-xs">{{ statusTarget?.role_name }}</span>
          </div>
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">Jumlah User</span>
            <span class="text-xs">{{ statusTarget?.user_count }} user terdaftar</span>
          </div>
          <div class="flex gap-3">
            <span class="text-muted text-xs w-24 shrink-0">Status saat ini</span>
            <span class="text-xs">{{ statusTarget?.status === 'active' ? 'Aktif' : 'Tidak Aktif' }}</span>
          </div>
        </div>
        <p class="text-sm text-muted">
          {{ statusTarget?.status === 'active'
            ? 'Role ini tidak akan muncul di daftar aktif setelah dinonaktifkan.'
            : 'Role ini akan aktif kembali dan bisa digunakan setelah diaktifkan.' }}
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

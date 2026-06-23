<script setup lang="ts">
import { Building2, Pencil, Plus, Power, PowerOff, Search, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'
import type { MenuKey } from '@/shared/constants/menu-keys'

interface BranchListItem {
  branch_code: string
  branch_name: string
  branch_type: string
  branch_status: string
  parent_branch_code: string | null
  parent_branch_name: string | null
  is_active: boolean
}

interface BranchDetail extends BranchListItem {
  office_name: string | null
  office_npwp: string | null
  office_address: string | null
  office_postal_code: string | null
  office_phone1: string | null
  office_phone2: string | null
  office_phone3: string | null
  access_status: string | null
  created_by: string | null
  created_at: string | null
}

interface ParentBranchItem {
  branch_code: string
  branch_name: string
}

interface ListResponse {
  rows: BranchListItem[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const toast = useToast()
const auth = useAuthStore()

// List state
const rows = ref<BranchListItem[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const pageSize = shallowRef(25)
const searchInput = ref('')
const statusFilter = ref<'all' | 'active' | 'inactive'>('active')

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

watch(statusFilter, () => {
  page.value = 1
  loadData()
})

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), limit: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('keyword', searchInput.value.trim())

    const statusActive = statusFilter.value === 'active' ? 'T' : statusFilter.value === 'inactive' ? 'F' : null
    if (statusActive) params.set('status_active', statusActive)

    const res = await api.get<ListResponse>(`/api/appadmin/branches?${params}`)
    rows.value = res.rows
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Gagal memuat data cabang'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

// Modal state
const showForm = shallowRef(false)
const formMode = shallowRef<'create' | 'edit'>('create')
const showConfirmDeactivate = shallowRef(false)
const showConfirmActivate = shallowRef(false)
const selectedRow = ref<BranchListItem | null>(null)
const formData = reactive<Partial<BranchDetail>>({})
const parentBranches = ref<ParentBranchItem[]>([])
const formLoading = shallowRef(false)
const loadingParents = shallowRef(false)

const branchTypeOptions = [
  { value: 'CP', label: 'Cabang Pembantu' },
  { value: 'CU', label: 'Cabang Umum' },
  { value: 'GM', label: 'Gerai' },
  { value: 'KS', label: 'Kantor Kas' },
  { value: 'NO', label: 'Pusat Non Operasional' },
  { value: 'PO', label: 'Pusat Operasional' },
]

const requiresParentBranch = () => {
  return ['CP', 'GM', 'KS'].includes(formData.branch_type || '')
}

async function loadParentBranches() {
  loadingParents.value = true
  try {
    const res = await api.get<{ rows: ParentBranchItem[] }>('/api/appadmin/branches/parents')
    parentBranches.value = res.rows
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Gagal memuat daftar cabang induk',
      life: 3000,
    })
  } finally {
    loadingParents.value = false
  }
}

function openAdd() {
  formMode.value = 'create'
  selectedRow.value = null
  formData.branch_code = ''
  formData.branch_name = ''
  formData.branch_type = 'CU'
  formData.parent_branch_code = null
  formData.office_name = ''
  formData.office_npwp = ''
  formData.office_address = ''
  formData.office_postal_code = ''
  formData.office_phone1 = ''
  formData.office_phone2 = ''
  formData.office_phone3 = ''
  showForm.value = true
  loadParentBranches()
}

async function openEdit(row: BranchListItem) {
  formMode.value = 'edit'
  selectedRow.value = row
  formLoading.value = true
  try {
    const detail = await api.get<BranchDetail>(`/api/appadmin/branches/${row.branch_code}`)
    formData.branch_code = detail.branch_code
    formData.branch_name = detail.branch_name
    formData.branch_type = detail.branch_type
    formData.parent_branch_code = detail.parent_branch_code
    formData.office_name = detail.office_name
    formData.office_npwp = detail.office_npwp
    formData.office_address = detail.office_address
    formData.office_postal_code = detail.office_postal_code
    formData.office_phone1 = detail.office_phone1
    formData.office_phone2 = detail.office_phone2
    formData.office_phone3 = detail.office_phone3
    showForm.value = true
    loadParentBranches()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Gagal memuat detail cabang',
      life: 3000,
    })
  } finally {
    formLoading.value = false
  }
}

function openDeactivateConfirm(row: BranchListItem) {
  selectedRow.value = row
  showConfirmDeactivate.value = true
}

function openActivateConfirm(row: BranchListItem) {
  selectedRow.value = row
  showConfirmActivate.value = true
}

async function submitForm() {
  if (!formData.branch_code || !formData.branch_name || !formData.branch_type) {
    toast.add({
      severity: 'warning',
      summary: 'Validasi',
      detail: 'Kode cabang, nama cabang, dan tipe cabang harus diisi',
      life: 3000,
    })
    return
  }

  if (requiresParentBranch() && !formData.parent_branch_code) {
    toast.add({
      severity: 'warning',
      summary: 'Validasi',
      detail: 'Cabang induk harus diisi untuk tipe cabang ini',
      life: 3000,
    })
    return
  }

  formLoading.value = true
  try {
    if (formMode.value === 'create') {
      await api.post('/api/appadmin/branches', {
        branch_code: formData.branch_code,
        branch_name: formData.branch_name,
        branch_type: formData.branch_type,
        parent_branch_code: requiresParentBranch() ? formData.parent_branch_code : null,
        office_name: formData.office_name,
        office_npwp: formData.office_npwp,
        office_address: formData.office_address,
        office_postal_code: formData.office_postal_code,
        office_phone1: formData.office_phone1,
        office_phone2: formData.office_phone2,
        office_phone3: formData.office_phone3,
      })
      toast.add({
        severity: 'success',
        summary: 'Berhasil',
        detail: 'Cabang baru berhasil ditambahkan',
        life: 3000,
      })
    } else {
      await api.put(`/api/appadmin/branches/${formData.branch_code}`, {
        branch_name: formData.branch_name,
        branch_type: formData.branch_type,
        parent_branch_code: requiresParentBranch() ? formData.parent_branch_code : null,
        office_name: formData.office_name,
        office_npwp: formData.office_npwp,
        office_address: formData.office_address,
        office_postal_code: formData.office_postal_code,
        office_phone1: formData.office_phone1,
        office_phone2: formData.office_phone2,
        office_phone3: formData.office_phone3,
      })
      toast.add({
        severity: 'success',
        summary: 'Berhasil',
        detail: 'Cabang berhasil diubah',
        life: 3000,
      })
    }
    showForm.value = false
    loadData()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: e instanceof Error ? e.message : 'Gagal menyimpan cabang',
      life: 3000,
    })
  } finally {
    formLoading.value = false
  }
}

async function confirmDeactivate() {
  if (!selectedRow.value) return
  formLoading.value = true
  try {
    await api.patch(`/api/appadmin/branches/${selectedRow.value.branch_code}/deactivate`, {})
    toast.add({
      severity: 'success',
      summary: 'Berhasil',
      detail: 'Cabang berhasil dinonaktifkan',
      life: 3000,
    })
    showConfirmDeactivate.value = false
    loadData()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: e instanceof Error ? e.message : 'Gagal menonaktifkan cabang',
      life: 3000,
    })
  } finally {
    formLoading.value = false
  }
}

async function confirmActivate() {
  if (!selectedRow.value) return
  formLoading.value = true
  try {
    await api.patch(`/api/appadmin/branches/${selectedRow.value.branch_code}/activate`, {})
    toast.add({
      severity: 'success',
      summary: 'Berhasil',
      detail: 'Cabang berhasil diaktifkan',
      life: 3000,
    })
    showConfirmActivate.value = false
    loadData()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: e instanceof Error ? e.message : 'Gagal mengaktifkan cabang',
      life: 3000,
    })
  } finally {
    formLoading.value = false
  }
}

function getBranchTypeLabel(type: string): string {
  return branchTypeOptions.find(o => o.value === type)?.label || type
}
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="List Cabang" subtitle="Lihat dan kelola data cabang organisasi" />

    <!-- Error message -->
    <div v-if="errorMsg" class="flex items-center gap-2 rounded-lg border border-red-200
                                bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table (satu card bersambung) -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3 flex-wrap">
        <div class="flex items-center gap-3 flex-1 min-w-0">
          <div class="relative flex-1 max-w-xs">
            <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
            <input
              v-model="searchInput"
              placeholder="Cari kode/nama cabang..."
              class="h-8 w-full rounded pl-8 pr-3 text-xs border border-border bg-background
                     focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </div>
          <select
            v-model="statusFilter"
            class="h-8 rounded px-3 text-xs border border-border bg-background
                   focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="all">Semua</option>
            <option value="active">Aktif</option>
            <option value="inactive">Tidak Aktif</option>
          </select>
        </div>
        <Button
          v-if="auth.menus.includes('appadmin.branch.create' as MenuKey)"
          size="sm"
          @click="openAdd"
        >
          <Plus class="w-3.5 h-3.5 mr-1" /> Tambah Cabang
        </Button>
      </div>

      <!-- Pagination (SELALU di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} data
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @prev="() => { if (page > 1) { page.value--; loadData() } }"
          @next="() => { if (page < totalPages) { page.value++; loadData() } }"
          @update:page-size="(s) => { pageSize.value = s; page.value = 1; loadData() }"
        />
      </div>

      <!-- Tabel -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">Kode Cabang</th>
              <th class="px-4 py-2 text-left font-medium">Nama Cabang</th>
              <th class="px-4 py-2 text-left font-medium">Tipe Cabang</th>
              <th class="px-4 py-2 text-left font-medium">Cabang Induk</th>
              <th class="px-4 py-2 text-left font-medium">Status</th>
              <th class="px-4 py-2 text-right font-medium w-32">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada data yang ditemukan.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.branch_code"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-1 text-xs font-mono">{{ row.branch_code }}</td>
              <td class="px-4 py-1 text-xs">{{ row.branch_name }}</td>
              <td class="px-4 py-1 text-xs">{{ getBranchTypeLabel(row.branch_type) }}</td>
              <td class="px-4 py-1 text-xs">
                <template v-if="row.parent_branch_name">
                  {{ row.parent_branch_name }}
                </template>
                <template v-else>
                  <span class="text-muted-foreground italic">-</span>
                </template>
              </td>
              <td class="px-4 py-1 text-xs">
                <span
                  :class="[
                    'inline-block px-1.5 py-px text-[10px] font-semibold rounded',
                    row.is_active
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-zinc-100 text-zinc-500'
                  ]"
                >
                  {{ row.is_active ? 'Aktif' : 'Tidak Aktif' }}
                </span>
              </td>
              <td class="px-4 py-1 text-right">
                <div class="flex items-center justify-end gap-1">
                  <button
                    v-if="auth.menus.includes('appadmin.branch.edit' as MenuKey)"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Edit"
                    @click="openEdit(row)"
                  >
                    <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                  </button>
                  <button
                    v-if="auth.menus.includes('appadmin.branch.edit' as MenuKey)"
                    :class="[
                      'p-1 rounded transition-colors',
                      row.is_active
                        ? 'hover:bg-red-100'
                        : 'hover:bg-emerald-100'
                    ]"
                    :title="row.is_active ? 'Nonaktifkan' : 'Aktifkan'"
                    @click="row.is_active ? openDeactivateConfirm(row) : openActivateConfirm(row)"
                  >
                    <PowerOff v-if="row.is_active" class="w-3.5 h-3.5 text-red-500" />
                    <Power v-else class="w-3.5 h-3.5 text-emerald-600" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Form Modal (Tambah/Edit) -->
    <Modal
      v-if="showForm"
      class="max-w-2xl"
      @close="showForm = false"
    >
      <template #header>
        <div class="flex items-center gap-2">
          <Building2 class="w-5 h-5" />
          <span>{{ formMode === 'create' ? 'Tambah Cabang Baru' : 'Edit Cabang' }}</span>
        </div>
      </template>

      <template #content>
        <div class="space-y-5">
          <!-- Section: Data Cabang -->
          <div class="space-y-3">
            <h4 class="text-sm font-semibold text-foreground">Data Cabang</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Kode Cabang *</label>
                <input
                  v-model="formData.branch_code"
                  :disabled="formMode === 'edit'"
                  type="text"
                  placeholder="Contoh: 001"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50 disabled:cursor-not-allowed"
                />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Nama Cabang *</label>
                <input
                  v-model="formData.branch_name"
                  type="text"
                  placeholder="Contoh: Cabang Jakarta Pusat"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Tipe Cabang *</label>
                <select
                  v-model="formData.branch_type"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring"
                >
                  <option value="">-- Pilih Tipe Cabang --</option>
                  <option v-for="opt in branchTypeOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>
              <div v-if="requiresParentBranch()" class="flex flex-col gap-1">
                <label class="text-xs font-medium">Cabang Induk *</label>
                <select
                  v-model="formData.parent_branch_code"
                  :disabled="loadingParents"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                >
                  <option value="">-- Pilih Cabang Induk --</option>
                  <option v-for="pb in parentBranches" :key="pb.branch_code" :value="pb.branch_code">
                    {{ pb.branch_name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <!-- Section: Data Kantor -->
          <div class="space-y-3">
            <h4 class="text-sm font-semibold text-foreground">Data Kantor</h4>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Nama Kantor</label>
                <input
                  v-model="formData.office_name"
                  type="text"
                  placeholder="Nama kantor"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">NPWP</label>
                <input
                  v-model="formData.office_npwp"
                  type="text"
                  placeholder="Nomor NPWP"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
            </div>

            <div class="flex flex-col gap-1">
              <label class="text-xs font-medium">Alamat</label>
              <input
                v-model="formData.office_address"
                type="text"
                placeholder="Alamat lengkap"
                class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                       focus:outline-none focus:ring-1 focus:ring-ring"
              />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Kode Pos</label>
                <input
                  v-model="formData.office_postal_code"
                  type="text"
                  placeholder="Kode pos"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Telepon 1</label>
                <input
                  v-model="formData.office_phone1"
                  type="text"
                  placeholder="Nomor telepon"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Telepon 2</label>
                <input
                  v-model="formData.office_phone2"
                  type="text"
                  placeholder="Nomor telepon"
                  class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                         focus:outline-none focus:ring-1 focus:ring-ring"
                />
              </div>
            </div>

            <div class="flex flex-col gap-1">
              <label class="text-xs font-medium">Telepon 3</label>
              <input
                v-model="formData.office_phone3"
                type="text"
                placeholder="Nomor telepon"
                class="h-9 rounded-lg px-2.5 text-xs border border-border bg-background
                       focus:outline-none focus:ring-1 focus:ring-ring"
              />
            </div>
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" @click="showForm = false">Batal</Button>
          <Button
            :loading="formLoading"
            @click="submitForm"
          >
            {{ formMode === 'create' ? 'Tambah' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Deactivate Confirmation Modal -->
    <Modal
      v-if="showConfirmDeactivate && selectedRow"
      class="max-w-sm"
      @close="showConfirmDeactivate = false"
    >
      <template #header>
        <span>Konfirmasi Nonaktifkan Cabang</span>
      </template>

      <template #content>
        <div class="space-y-3">
          <p class="text-sm">
            Apakah Anda yakin ingin menonaktifkan cabang <span class="font-semibold">{{ selectedRow.branch_name }}</span> ({{ selectedRow.branch_code }})?
          </p>
          <p class="text-xs text-muted-foreground">
            Cabang yang tidak aktif tidak akan muncul di menu pilihan cabang.
          </p>
        </div>
      </template>

      <template #footer>
        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" @click="showConfirmDeactivate = false">Batal</Button>
          <Button
            variant="destructive"
            :loading="formLoading"
            @click="confirmDeactivate"
          >
            Nonaktifkan
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Activate Confirmation Modal -->
    <Modal
      v-if="showConfirmActivate && selectedRow"
      class="max-w-sm"
      @close="showConfirmActivate = false"
    >
      <template #header>
        <span>Konfirmasi Aktifkan Cabang</span>
      </template>

      <template #content>
        <div class="space-y-3">
          <p class="text-sm">
            Apakah Anda yakin ingin mengaktifkan cabang <span class="font-semibold">{{ selectedRow.branch_name }}</span> ({{ selectedRow.branch_code }})?
          </p>
          <p class="text-xs text-muted-foreground">
            Cabang yang aktif akan tersedia di menu pilihan cabang.
          </p>
        </div>
      </template>

      <template #footer>
        <div class="flex items-center justify-end gap-2">
          <Button variant="outline" @click="showConfirmActivate = false">Batal</Button>
          <Button
            :loading="formLoading"
            @click="confirmActivate"
          >
            Aktifkan
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

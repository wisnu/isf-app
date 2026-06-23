<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch } from 'vue'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'

import Button from '@/shared/components/Button.vue'
import Input from '@/shared/components/Input.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'

// ── Types ─────────────────────────────────────────────────────────────────────

interface JenisDokumenRow {
  id_jenis_dokumen: number
  kode_jenis_dokumen: string
  nama_jenis_dokumen: string
}

interface Pagination {
  page: number
  limit: number
  total: number
  total_pages: number
}

interface ListResponse {
  rows: JenisDokumenRow[]
  pagination: Pagination
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const auth = useAuthStore()

const rows = ref<JenisDokumenRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const pageSize = shallowRef(25)
const searchInput = ref('')

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

// ── API Calls ─────────────────────────────────────────────────────────────────

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    const res = await api.get<ListResponse>(`/api/generalaffair/document-types?${params}`)
    rows.value = res.rows
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
}

async function saveData() {
  if (formMode.value === 'create') {
    await createData()
  } else {
    await updateData()
  }
}

async function createData() {
  if (!formData.kode_jenis_dokumen.trim() || !formData.nama_jenis_dokumen.trim()) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Semua field wajib diisi', life: 3000 })
    return
  }

  formLoading.value = true
  try {
    await api.post('/api/generalaffair/document-types', {
      kode_jenis_dokumen: formData.kode_jenis_dokumen.trim(),
      nama_jenis_dokumen: formData.nama_jenis_dokumen.trim(),
    })
    toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Jenis dokumen berhasil dibuat', life: 3000 })
    showForm.value = false
    loadData()
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof ApiError ? e.message : 'Gagal menyimpan', life: 3000 })
  } finally {
    formLoading.value = false
  }
}

async function updateData() {
  if (!formData.kode_jenis_dokumen.trim() || !formData.nama_jenis_dokumen.trim()) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Semua field wajib diisi', life: 3000 })
    return
  }

  if (!selected.value) return
  formLoading.value = true
  try {
    await api.put(`/api/generalaffair/document-types/${selected.value.id_jenis_dokumen}`, {
      kode_jenis_dokumen: formData.kode_jenis_dokumen.trim(),
      nama_jenis_dokumen: formData.nama_jenis_dokumen.trim(),
    })
    toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Jenis dokumen berhasil diperbarui', life: 3000 })
    showForm.value = false
    loadData()
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof ApiError ? e.message : 'Gagal menyimpan', life: 3000 })
  } finally {
    formLoading.value = false
  }
}

async function deleteData() {
  if (!selected.value) return
  deleteLoading.value = true
  try {
    await api.delete(`/api/generalaffair/document-types/${selected.value.id_jenis_dokumen}`)
    toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Jenis dokumen berhasil dihapus', life: 3000 })
    showDelete.value = false
    loadData()
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof ApiError ? e.message : 'Gagal menghapus', life: 3000 })
  } finally {
    deleteLoading.value = false
  }
}

onMounted(loadData)

// ── Modal State ───────────────────────────────────────────────────────────────

const showForm = shallowRef(false)
const showDelete = shallowRef(false)
const formMode = shallowRef<'create' | 'edit'>('create')
const selected = ref<JenisDokumenRow | null>(null)
const formLoading = shallowRef(false)
const deleteLoading = shallowRef(false)

const formData = ref({
  kode_jenis_dokumen: '',
  nama_jenis_dokumen: '',
})

function openAdd() {
  formMode.value = 'create'
  selected.value = null
  formData.value = { kode_jenis_dokumen: '', nama_jenis_dokumen: '' }
  showForm.value = true
}

function openEdit(row: JenisDokumenRow) {
  formMode.value = 'edit'
  selected.value = row
  formData.value = {
    kode_jenis_dokumen: row.kode_jenis_dokumen,
    nama_jenis_dokumen: row.nama_jenis_dokumen,
  }
  showForm.value = true
}

function openDeleteConfirm(row: JenisDokumenRow) {
  selected.value = row
  showDelete.value = true
}

function resetForm() {
  formData.value = { kode_jenis_dokumen: '', nama_jenis_dokumen: '' }
  selected.value = null
}
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Jenis Dokumen" subtitle="Kelola tipe dan klasifikasi dokumen" />

    <!-- Error message -->
    <div v-if="errorMsg" class="flex items-center gap-2 rounded-lg border border-red-200
                                bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3">
        <div class="relative flex-1 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input
            v-model="searchInput"
            placeholder="Cari..."
            class="h-8 w-full rounded pl-8 pr-3 text-xs border border-border bg-background
                   focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <Button
          v-if="auth.menus.includes('generalaffair.parameter.document-type')"
          size="sm"
          @click="openAdd"
        >
          <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
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
          @prev="page > 1 && (page--, loadData())"
          @next="page < totalPages && (page++, loadData())"
          @update:page-size="(s) => { pageSize.value = s; page.value = 1; loadData() }"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">Kode</th>
              <th class="px-4 py-2 text-left font-medium">Nama Jenis Dokumen</th>
              <th class="px-4 py-2 text-right font-medium w-24">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="3" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="3" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada data yang ditemukan.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.id_jenis_dokumen"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-1 text-xs">{{ row.kode_jenis_dokumen }}</td>
              <td class="px-4 py-1 text-xs">{{ row.nama_jenis_dokumen }}</td>
              <td class="px-4 py-1 text-right">
                <div class="flex items-center justify-end gap-1">
                  <button
                    v-if="auth.menus.includes('generalaffair.parameter.document-type')"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Edit"
                    @click="openEdit(row)"
                  >
                    <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                  </button>
                  <button
                    v-if="auth.menus.includes('generalaffair.parameter.document-type')"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Hapus"
                    @click="openDeleteConfirm(row)"
                  >
                    <Trash2 class="w-3.5 h-3.5 text-red-500" />
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
      :open="showForm"
      :title="`${formMode === 'create' ? 'Tambah' : 'Edit'} Jenis Dokumen`"
      :loading="formLoading"
      @close="() => { showForm = false; resetForm() }"
      @submit="saveData"
    >
      <div class="space-y-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">Kode Jenis Dokumen</label>
          <Input
            v-model="formData.kode_jenis_dokumen"
            placeholder="Contoh: DM001"
            class="text-sm"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">Nama Jenis Dokumen</label>
          <Input
            v-model="formData.nama_jenis_dokumen"
            placeholder="Contoh: Surat Masuk"
            class="text-sm"
          />
        </div>
      </div>
    </Modal>

    <!-- Delete Modal -->
    <Modal
      v-if="showDelete && selected"
      :open="showDelete"
      title="Hapus Jenis Dokumen"
      :loading="deleteLoading"
      danger
      @close="() => { showDelete = false; selected = null }"
      @submit="deleteData"
    >
      <div class="space-y-4 text-sm">
        <p><strong>Kode:</strong> {{ selected.kode_jenis_dokumen }}</p>
        <p><strong>Nama:</strong> {{ selected.nama_jenis_dokumen }}</p>
        <p class="text-red-600 font-medium">Apakah Anda yakin ingin menghapus data ini?</p>
      </div>
    </Modal>
  </div>
</template>

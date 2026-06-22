<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

interface ProgramTypeRow {
  program_type_id: number
  code: string | null
  name: string | null
  description: string | null
  status: string | null
}

interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

interface ListResponse {
  rows: ProgramTypeRow[]
  pagination: Pagination
}

const toast = useToast()

const rows        = ref<ProgramTypeRow[]>([])
const loading     = shallowRef(false)
const errorMsg    = shallowRef<string | null>(null)
const page        = shallowRef(1)
const totalPages  = shallowRef(1)
const totalRec    = shallowRef(0)
const pageSize    = shallowRef(25)
const searchInput = ref('')

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    const res = await api.get<ListResponse>(`/api/distribution/parameter/program-type?${params}`)
    rows.value       = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRec.value   = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function prevPage() { if (page.value > 1) { page.value--; loadData() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadData() } }
function changePageSize(s: number) { pageSize.value = s; page.value = 1; loadData() }

type ModalMode = 'create' | 'edit' | 'delete'

const modalMode    = shallowRef<ModalMode>('create')
const modalOpen    = shallowRef(false)
const modalLoading = shallowRef(false)
const modalError   = shallowRef<string | null>(null)
const selectedRow  = ref<ProgramTypeRow | null>(null)

const form = reactive({ code: '', name: '', description: '', status: 'A' })

function resetForm() {
  form.code = ''
  form.name = ''
  form.description = ''
  form.status = 'A'
}

function fillForm(d: ProgramTypeRow) {
  form.code        = d.code ?? ''
  form.name        = d.name ?? ''
  form.description = d.description ?? ''
  form.status      = d.status ?? 'A'
}

function openCreate() {
  resetForm()
  modalMode.value  = 'create'
  modalError.value = null
  modalOpen.value  = true
}

function openEdit(row: ProgramTypeRow) {
  selectedRow.value = row
  fillForm(row)
  modalMode.value  = 'edit'
  modalError.value = null
  modalOpen.value  = true
}

function openDelete(row: ProgramTypeRow) {
  selectedRow.value = row
  modalMode.value   = 'delete'
  modalError.value  = null
  modalOpen.value   = true
}

function closeModal() { modalOpen.value = false }

async function saveForm() {
  if (!form.code.trim()) { modalError.value = 'Kode jenis program wajib diisi.'; return }
  if (!form.name.trim()) { modalError.value = 'Nama jenis program wajib diisi.'; return }
  modalLoading.value = true
  modalError.value   = null
  try {
    const payload = {
      code:        form.code.trim(),
      name:        form.name.trim(),
      description: form.description.trim() || null,
      status:      form.status,
    }
    if (modalMode.value === 'create') {
      await api.post('/api/distribution/parameter/program-type', payload)
      toast.success('Jenis program berhasil ditambahkan.')
    } else {
      await api.put(`/api/distribution/parameter/program-type/${selectedRow.value!.program_type_id}`, payload)
      toast.success('Jenis program berhasil diperbarui.')
    }
    closeModal()
    loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menyimpan data.'
  } finally {
    modalLoading.value = false
  }
}

async function confirmDelete() {
  if (!selectedRow.value) return
  modalLoading.value = true
  modalError.value   = null
  try {
    await api.delete(`/api/distribution/parameter/program-type/${selectedRow.value.program_type_id}`)
    toast.success('Jenis program berhasil dihapus.')
    closeModal()
    loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menghapus data.'
  } finally {
    modalLoading.value = false
  }
}

onMounted(() => { loadData() })
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Jenis Program" subtitle="Master data jenis / kelompok program penyaluran">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="openCreate">
          <Plus class="w-3.5 h-3.5" />
          Tambah
        </Button>
      </template>
    </PageHeader>

    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400">
      {{ errorMsg }}
    </div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center gap-3">
        <div class="relative flex-1 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input
            v-model="searchInput"
            type="text"
            placeholder="Cari kode / nama..."
            class="w-full h-8 pl-8 pr-8 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring"
          />
          <button v-if="searchInput" class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground" @click="searchInput = ''">
            <X class="w-3 h-3" />
          </button>
        </div>
      </div>

      <!-- Pagination (atas) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} data
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @prev="prevPage" @next="nextPage" @update:page-size="changePageSize"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium w-32">Kode</th>
              <th class="px-4 py-2 text-left font-medium">Nama Jenis Program</th>
              <th class="px-4 py-2 text-left font-medium max-w-xs">Deskripsi</th>
              <th class="px-4 py-2 text-left font-medium w-24">Status</th>
              <th class="px-4 py-2 text-right font-medium w-24">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="5" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="5" class="px-4 py-8 text-center text-muted-foreground text-xs italic">Belum ada data jenis program.</td>
            </tr>
            <tr v-for="row in rows" :key="row.program_type_id" class="hover:bg-background/60">
              <td class="px-4 py-1.5 font-mono text-xs font-medium">{{ row.code || '—' }}</td>
              <td class="px-4 py-1.5 font-medium">{{ row.name || '—' }}</td>
              <td class="px-4 py-1.5 text-xs text-muted-foreground max-w-xs truncate">{{ row.description || '—' }}</td>
              <td class="px-4 py-1.5">
                <span
                  :class="[
                    'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium',
                    row.status === 'A'
                      ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                      : 'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400'
                  ]"
                >{{ row.status === 'A' ? 'Aktif' : 'Non Aktif' }}</span>
              </td>
              <td class="px-4 py-1.5">
                <div class="flex items-center justify-end gap-0.5">
                  <button
                    class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-blue-600 transition-colors"
                    title="Ubah"
                    @click="openEdit(row)"
                  ><Pencil class="w-3.5 h-3.5" /></button>
                  <button
                    class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600 transition-colors"
                    title="Hapus"
                    @click="openDelete(row)"
                  ><Trash2 class="w-3.5 h-3.5" /></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create / Edit Modal -->
    <Modal v-if="modalOpen && (modalMode === 'create' || modalMode === 'edit')" max-width="max-w-md" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">{{ modalMode === 'create' ? 'Tambah Jenis Program' : 'Ubah Jenis Program' }}</h2>
      </template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <div>
          <label class="block text-xs font-medium mb-1">Kode <span class="text-red-500">*</span></label>
          <input v-model="form.code" type="text" maxlength="10" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" placeholder="Maks 10 karakter" />
        </div>
        <div>
          <label class="block text-xs font-medium mb-1">Nama Jenis Program <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" maxlength="50" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" placeholder="Nama jenis program" />
        </div>
        <div>
          <label class="block text-xs font-medium mb-1">Deskripsi</label>
          <textarea v-model="form.description" rows="2" maxlength="200" class="w-full px-3 py-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring resize-none" placeholder="Deskripsi (opsional)" />
        </div>
        <div>
          <label class="block text-xs font-medium mb-1">Status</label>
          <select v-model="form.status" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
            <option value="A">Aktif</option>
            <option value="N">Non Aktif</option>
          </select>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button size="sm" :disabled="modalLoading" @click="saveForm">
            {{ modalLoading ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Delete Modal -->
    <Modal v-if="modalOpen && modalMode === 'delete'" max-width="max-w-sm" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold text-red-600">Hapus Jenis Program</h2>
      </template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <p class="text-sm text-muted-foreground">Data berikut akan dihapus permanen:</p>
        <div class="rounded border border-border bg-muted/30 px-4 py-3 text-sm space-y-1">
          <div class="font-semibold">{{ selectedRow?.name }}</div>
          <div class="text-xs text-muted-foreground font-mono">{{ selectedRow?.code }}</div>
        </div>
        <p class="text-xs text-red-600 font-medium">Tindakan ini tidak dapat dibatalkan.</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button variant="destructive" size="sm" :disabled="modalLoading" @click="confirmDelete">
            {{ modalLoading ? 'Menghapus...' : 'Hapus' }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

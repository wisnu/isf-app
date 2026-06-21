<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import Tooltip from '@/shared/components/Tooltip.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BudgetItemRow {
  item_id: string
  item_code: string
  item_name: string
  item_level: number
  parent_id: string | null
  parent_name: string | null
}

interface BudgetItemList {
  rows: BudgetItemRow[]
  pagination: { page: number; page_size: number; total: number; total_pages: number }
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()

const rows = ref<BudgetItemRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRecords = shallowRef(0)

const searchInput = ref('')
let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadItems() }, 300)
})

// ── Load data ─────────────────────────────────────────────────────────────────

async function loadItems() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), limit: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('q', searchInput.value.trim())
    const res = await api.get<BudgetItemList>(`/api/budget/parameter/items?${params}`)
    rows.value = res.rows
    totalRecords.value = res.pagination.total
    totalPages.value = res.pagination.total_pages || 1
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat item anggaran'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function prevPage() { if (page.value > 1) { page.value--; loadItems() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadItems() } }
function changePageSize(size: number) { pageSize.value = size; page.value = 1; loadItems() }

// ── Modal state ───────────────────────────────────────────────────────────────

const modalOpen = shallowRef(false)
const modalMode = shallowRef<'create' | 'edit' | 'delete'>('create')
const selectedItem = ref<BudgetItemRow | null>(null)
const submitting = shallowRef(false)

const form = reactive({
  item_code: '',
  item_name: '',
})

function resetForm() {
  form.item_code = ''
  form.item_name = ''
}

function openCreate() {
  modalMode.value = 'create'
  selectedItem.value = null
  resetForm()
  modalOpen.value = true
}

function openEdit(item: BudgetItemRow) {
  modalMode.value = 'edit'
  selectedItem.value = item
  form.item_code = item.item_code
  form.item_name = item.item_name
  modalOpen.value = true
}

function openDelete(item: BudgetItemRow) {
  modalMode.value = 'delete'
  selectedItem.value = item
  form.item_code = item.item_code
  form.item_name = item.item_name
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
  selectedItem.value = null
  resetForm()
}

// ── Submit ────────────────────────────────────────────────────────────────────

async function submitForm() {
  if (!form.item_code.trim()) {
    toast.error('Kode Item wajib diisi')
    return
  }
  if (!form.item_name.trim()) {
    toast.error('Nama Item wajib diisi')
    return
  }

  submitting.value = true
  try {
    const isCreate = modalMode.value === 'create'
    const payload = {
      item_code: form.item_code.trim(),
      item_name: form.item_name.trim(),
    }

    if (isCreate) {
      await api.post('/api/budget/parameter/items', payload)
      toast.success('Item anggaran berhasil ditambahkan')
    } else {
      await api.put(`/api/budget/parameter/items/${selectedItem.value?.item_id}`, payload)
      toast.success('Item anggaran berhasil diubah')
    }

    closeModal()
    loadItems()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan item anggaran')
  } finally {
    submitting.value = false
  }
}

async function submitDelete() {
  submitting.value = true
  try {
    await api.delete(`/api/budget/parameter/items/${selectedItem.value?.item_id}`)
    toast.success('Item anggaran berhasil dihapus')
    closeModal()
    loadItems()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menghapus item anggaran')
  } finally {
    submitting.value = false
  }
}

onMounted(loadItems)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Item Anggaran" subtitle="Master data item dan kelompok kegiatan anggaran" />

    <!-- Error -->
    <div
      v-if="errorMsg"
      class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400"
    >
      <strong>Error:</strong> {{ errorMsg }}
    </div>

    <!-- 3-part table layout -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3">
        <div class="relative flex-1 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground pointer-events-none" />
          <input
            v-model="searchInput"
            placeholder="Cari kode atau nama..."
            class="h-8 w-full rounded pl-8 pr-3 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
        <Button size="sm" @click="openCreate">
          <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
        </Button>
      </div>

      <!-- Pagination -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRecords > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRecords) }}
            dari {{ totalRecords }} item
          </template>
          <template v-else>Tidak ada item</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRecords"
          :page-size="pageSize"
          :loading="loading"
          unit="item"
          @prev="prevPage"
          @next="nextPage"
          @update:page-size="changePageSize"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">Kode Item</th>
              <th class="px-4 py-2 text-left font-medium">Nama Item</th>
              <th class="px-4 py-2 text-center font-medium">Level</th>
              <th class="px-4 py-2 text-left font-medium">Induk</th>
              <th class="px-4 py-2 text-right font-medium w-20">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="px-4 py-8 text-center text-muted">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="5" class="px-4 py-8 text-center text-muted italic">
                Tidak ada item yang ditemukan.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.item_id"
              class="border-b border-border last:border-0 hover:bg-background/60"
            >
              <td class="px-4 py-1 font-mono text-xs">{{ row.item_code }}</td>
              <td class="px-4 py-1 text-xs">{{ row.item_name }}</td>
              <td class="px-4 py-1 text-center text-xs">
                <span
                  class="inline-block text-[10px] font-semibold px-1.5 py-px rounded"
                  :class="row.item_level === 1 ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' : 'bg-gray-100 text-gray-700 dark:bg-gray-900/30 dark:text-gray-300'"
                >
                  {{ row.item_level === 1 ? 'Kelompok' : 'Detail' }}
                </span>
              </td>
              <td class="px-4 py-1 text-xs">{{ row.parent_name ?? '—' }}</td>
              <td class="px-4 py-1">
                <div class="flex items-center justify-end gap-1">
                  <Tooltip side="top">
                    <template #trigger>
                      <button
                        class="p-1 rounded hover:bg-muted transition-colors"
                        @click="openEdit(row)"
                      >
                        <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                      </button>
                    </template>
                    Ubah
                  </Tooltip>
                  <Tooltip side="top">
                    <template #trigger>
                      <button
                        class="p-1 rounded hover:bg-red-50 transition-colors"
                        @click="openDelete(row)"
                      >
                        <Trash2 class="w-3.5 h-3.5 text-red-500" />
                      </button>
                    </template>
                    Hapus
                  </Tooltip>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Form Modal -->
    <Teleport to="body">
      <div
        v-if="modalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
        @click.self="closeModal"
      >
        <div class="w-full max-w-sm rounded-xl border border-border bg-surface shadow-xl flex flex-col">
          <!-- Header -->
          <div class="flex items-center justify-between border-b border-border px-6 py-4">
            <div>
              <h2 class="text-base font-semibold" :class="modalMode === 'delete' ? 'text-red-700' : ''">
                {{
                  modalMode === 'create'
                    ? 'Tambah Item Anggaran'
                    : modalMode === 'edit'
                      ? 'Ubah Item Anggaran'
                      : 'Konfirmasi Hapus'
                }}
              </h2>
              <p class="text-[11px] mt-0.5" :class="modalMode === 'delete' ? 'text-red-500' : 'text-muted'">
                {{ modalMode === 'delete' ? 'Periksa data berikut sebelum menghapus' : '' }}
              </p>
            </div>
            <button
              type="button"
              class="rounded-lg p-1.5 text-muted hover:bg-background transition-colors"
              @click="closeModal"
            >
              <X class="w-4 h-4" />
            </button>
          </div>

          <!-- Body -->
          <div class="px-6 py-5 space-y-4" :class="{ 'pointer-events-none select-none': modalMode === 'delete' }">
            <div>
              <label class="mb-1 block text-xs font-medium">
                Kode Item <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.item_code"
                placeholder="mis. KEL-001"
                class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>

            <div>
              <label class="mb-1 block text-xs font-medium">
                Nama Item <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.item_name"
                placeholder="mis. Kelompok Program Zakat"
                class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>

            <div v-if="modalMode === 'delete'" class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-3 py-2 text-xs text-red-700 dark:text-red-400">
              ⚠ Item anggaran ini akan dihapus secara permanen. Tindakan tidak dapat dibatalkan.
            </div>
          </div>

          <!-- Footer -->
          <div class="border-t border-border px-6 py-3 flex justify-end gap-2">
            <Button variant="outline" size="sm" :disabled="submitting" @click="closeModal">
              Batal
            </Button>
            <button
              v-if="modalMode === 'delete'"
              type="button"
              class="inline-flex items-center gap-1.5 rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50 transition-colors"
              :disabled="submitting"
              @click="submitDelete"
            >
              {{ submitting ? 'Menghapus...' : 'Hapus Item' }}
            </button>
            <Button v-else size="sm" :disabled="submitting" @click="submitForm">
              {{ submitting ? 'Menyimpan...' : (modalMode === 'create' ? 'Tambah Item' : 'Ubah Item') }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

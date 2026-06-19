<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'
import BudgetOwnerFormModal from '@/components/parameter/BudgetOwnerFormModal.vue'
import BudgetOwnerDeleteModal from '@/components/parameter/BudgetOwnerDeleteModal.vue'

interface OwnerRow {
  ownerid: number
  ownercode: string
  ownername: string
  level: number
  is_detail: string
  parentownerid: number | null
  status: string
}

interface ListResponse {
  rows: OwnerRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const toast  = useToast()
const auth   = useAuthStore()

const rows       = ref<OwnerRow[]>([])
const loading    = shallowRef(false)
const errorMsg   = shallowRef<string | null>(null)
const page       = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec   = shallowRef(0)
const pageSize   = shallowRef(25)
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
    const params = new URLSearchParams({ page: String(page.value), limit: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('q', searchInput.value.trim())
    const res = await api.get<ListResponse>(`/api/parameter/pemilik-anggaran?${params}`)
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

// ── Modal state ───────────────────────────────────────────────────────────────

const formOpen    = shallowRef(false)
const deleteOpen  = shallowRef(false)
const modalMode   = shallowRef<'create' | 'edit'>('create')
const selectedRow = ref<OwnerRow | null>(null)

function openCreate() {
  modalMode.value = 'create'
  selectedRow.value = null
  formOpen.value = true
}

function openEdit(row: OwnerRow) {
  modalMode.value = 'edit'
  selectedRow.value = row
  formOpen.value = true
}

function openDelete(row: OwnerRow) {
  selectedRow.value = row
  deleteOpen.value = true
}

function onSaved() {
  formOpen.value = false
  loadData()
}

function onDeleted() {
  deleteOpen.value = false
  loadData()
}

onMounted(loadData)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Pemilik Anggaran" subtitle="Master data pemilik / penanggung jawab anggaran">
      <template #actions>
        <Button
          v-if="auth.hasMenu('keuangan.parameter.pemilik-anggaran.tambah')"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="openCreate"
        >
          <Plus class="w-3.5 h-3.5" />
          Tambah
        </Button>
      </template>
    </PageHeader>

    <!-- Error -->
    <div
      v-if="errorMsg"
      class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400"
    >
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table -->
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
          <button
            v-if="searchInput"
            class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            @click="searchInput = ''"
          >
            <X class="w-3 h-3" />
          </button>
        </div>
      </div>

      <!-- Pagination (SELALU di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} pemilik
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
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
              <th class="px-4 py-2 text-left font-medium">Kode</th>
              <th class="px-4 py-2 text-left font-medium">Nama Pemilik</th>
              <th class="px-4 py-2 text-center font-medium">Level</th>
              <th class="px-4 py-2 text-center font-medium">Tipe</th>
              <th class="px-4 py-2 text-center font-medium">Status</th>
              <th class="px-4 py-2 text-right font-medium w-20">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">Tidak ada pemilik anggaran yang ditemukan.</td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.ownerid"
              class="border-b border-border last:border-0 hover:bg-background/60"
            >
              <td class="px-4 py-1 font-mono">{{ row.ownercode }}</td>
              <td class="px-4 py-1">
                <span
                  v-if="row.level > 1"
                  class="inline-block mr-1 text-muted-foreground"
                  :style="{ marginLeft: `${(row.level - 1) * 12}px` }"
                >↳</span>
                {{ row.ownername }}
              </td>
              <td class="px-4 py-1 text-center tabular-nums text-muted-foreground">{{ row.level }}</td>
              <td class="px-4 py-1 text-center">
                <span
                  class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="row.is_detail === 'T'
                    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
                    : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'"
                >
                  {{ row.is_detail === 'T' ? 'Detail' : 'Induk' }}
                </span>
              </td>
              <td class="px-4 py-1 text-center">
                <span
                  class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="row.status === 'A'
                    ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300'
                    : 'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400'"
                >
                  {{ row.status === 'A' ? 'Aktif' : 'Tidak Aktif' }}
                </span>
              </td>
              <td class="px-4 py-1">
                <div class="flex items-center justify-end gap-1">
                  <Tooltip v-if="auth.hasMenu('keuangan.parameter.pemilik-anggaran.ubah')" side="top">
                    <template #trigger>
                      <button
                        class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                        @click="openEdit(row)"
                      >
                        <Pencil class="w-3.5 h-3.5" />
                      </button>
                    </template>
                    Ubah
                  </Tooltip>
                  <Tooltip v-if="auth.hasMenu('keuangan.parameter.pemilik-anggaran.hapus')" side="top">
                    <template #trigger>
                      <button
                        class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600 transition-colors"
                        @click="openDelete(row)"
                      >
                        <Trash2 class="w-3.5 h-3.5" />
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

    <!-- Modals -->
    <BudgetOwnerFormModal
      v-if="formOpen"
      :mode="modalMode"
      :initial-data="selectedRow"
      @close="formOpen = false"
      @saved="onSaved"
    />
    <BudgetOwnerDeleteModal
      v-if="deleteOpen"
      :row="selectedRow!"
      @close="deleteOpen = false"
      @deleted="onDeleted"
    />
  </div>
</template>

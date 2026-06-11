<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api, ApiError } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'
import PemilikAnggaranFormModal from '@/components/parameter/PemilikAnggaranFormModal.vue'
import PemilikAnggaranDeleteModal from '@/components/parameter/PemilikAnggaranDeleteModal.vue'

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

const formOpen    = shallowRef(false)
const deleteOpen  = shallowRef(false)
const modalMode   = shallowRef<'create' | 'edit'>('create')
const selectedRow = ref<OwnerRow | null>(null)

function openCreate() { modalMode.value = 'create'; selectedRow.value = null; formOpen.value = true }
function openEdit(row: OwnerRow) { modalMode.value = 'edit'; selectedRow.value = row; formOpen.value = true }
function openDelete(row: OwnerRow) { selectedRow.value = row; deleteOpen.value = true }
function onSaved() { formOpen.value = false; loadData() }
function onDeleted() { deleteOpen.value = false; loadData() }

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

    <div class="flex items-center gap-2">
      <div class="relative flex-1 max-w-xs">
        <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
        <input
          v-model="searchInput"
          type="text"
          placeholder="Cari kode / nama..."
          class="w-full h-8 pl-8 pr-8 text-xs border border-border rounded-md bg-background focus:outline-none focus:ring-1 focus:ring-ring"
        />
        <button v-if="searchInput" class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground" @click="searchInput = ''">
          <X class="w-3 h-3" />
        </button>
      </div>
    </div>

    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{{ errorMsg }}</div>

    <TablePagination
      :page="page" :total-pages="totalPages" :total-records="totalRec" :page-size="pageSize"
      @prev="prevPage" @next="nextPage" @change-size="changePageSize"
    />

    <div class="rounded-b-lg border border-border overflow-x-auto">
      <table class="w-full text-sm">
        <thead class="bg-muted/50 text-xs uppercase tracking-wide text-muted-foreground">
          <tr>
            <th class="px-4 py-2.5 text-left font-medium">Kode</th>
            <th class="px-4 py-2.5 text-left font-medium">Nama Pemilik</th>
            <th class="px-4 py-2.5 text-center font-medium">Level</th>
            <th class="px-4 py-2.5 text-center font-medium">Tipe</th>
            <th class="px-4 py-2.5 text-center font-medium">Status</th>
            <th class="px-4 py-2.5 text-right font-medium">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-border">
          <tr v-if="loading"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat data…</td></tr>
          <tr v-else-if="rows.length === 0"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Tidak ada data</td></tr>
          <tr v-for="row in rows" :key="row.ownerid" class="hover:bg-muted/30 transition-colors">
            <td class="px-4 py-2.5 font-mono text-xs">{{ row.ownercode }}</td>
            <td class="px-4 py-2.5">
              <span v-if="row.level > 1" class="inline-block mr-1" :style="{ marginLeft: `${(row.level - 1) * 12}px` }">↳</span>
              {{ row.ownername }}
            </td>
            <td class="px-4 py-2.5 text-center tabular-nums text-xs text-muted-foreground">{{ row.level }}</td>
            <td class="px-4 py-2.5 text-center">
              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                :class="row.is_detail === 'T' ? 'bg-blue-100 text-blue-700' : 'bg-amber-100 text-amber-700'">
                {{ row.is_detail === 'T' ? 'Detail' : 'Induk' }}
              </span>
            </td>
            <td class="px-4 py-2.5 text-center">
              <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                :class="row.status === 'A' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'">
                {{ row.status === 'A' ? 'Aktif' : 'Tidak Aktif' }}
              </span>
            </td>
            <td class="px-4 py-2.5">
              <div class="flex items-center justify-end gap-1">
                <button v-if="auth.hasMenu('keuangan.parameter.pemilik-anggaran.ubah')"
                  class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-foreground" @click="openEdit(row)">
                  <Pencil class="w-3.5 h-3.5" />
                </button>
                <button v-if="auth.hasMenu('keuangan.parameter.pemilik-anggaran.hapus')"
                  class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600" @click="openDelete(row)">
                  <Trash2 class="w-3.5 h-3.5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <PemilikAnggaranFormModal v-if="formOpen" :mode="modalMode" :initial-data="selectedRow"
      @close="formOpen = false" @saved="onSaved" />
    <PemilikAnggaranDeleteModal v-if="deleteOpen" :row="selectedRow!"
      @close="deleteOpen = false" @deleted="onDeleted" />
  </div>
</template>

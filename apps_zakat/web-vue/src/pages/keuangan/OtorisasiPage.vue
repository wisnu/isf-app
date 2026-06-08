<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ShieldCheck } from 'lucide-vue-next'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Paginator from 'primevue/paginator'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import SubmissionDetailDrawer from '@/components/otorisasi/SubmissionDetailDrawer.vue'

const toast = useToast()

interface SubmissionRow {
  id: number
  entity_type: string
  entity_label: string
  branch_code: string
  submitted_by: string
  submitted_at: string | null
  status: string
  level_current: number
  level_required: number
  payload: Record<string, any>
  approval_log: any[]
}

interface ListResponse {
  rows: SubmissionRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const rows = ref<SubmissionRow[]>([])
const total = ref(0)
const page = ref(0)
const pageSize = ref(25)
const loading = ref(false)
const selectedRows = ref<SubmissionRow[]>([])
const filterEntityType = ref<string | null>(null)
const drawerOpen = ref(false)
const drawerSubmission = ref<SubmissionRow | null>(null)
const bulkLoading = ref(false)
const bulkRejectNotes = ref('')
const showBulkRejectInput = ref(false)

const entityTypes = [
  { label: 'Semua', value: null },
  { label: 'Penghimpunan', value: 'penghimpunan' },
  { label: 'Penyaluran', value: 'penyaluran' },
  { label: 'Upload Penghimpunan', value: 'upload_penghimpunan' },
  { label: 'Master COA', value: 'coa' },
  { label: 'Master Kas', value: 'kas' },
  { label: 'Master Bank', value: 'bank' },
]

async function load() {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: String(page.value + 1),
      page_size: String(pageSize.value),
    })
    if (filterEntityType.value) params.set('entity_type', filterEntityType.value)
    const res = await api.get<ListResponse>(`/api/otorisasi/pending/?${params}`)
    rows.value = res.rows
    total.value = res.pagination.total
  } catch {
    toast.error('Gagal memuat data')
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function openDetail(row: SubmissionRow) {
  try {
    const res = await api.get<SubmissionRow>(`/api/otorisasi/submission/${row.id}`)
    drawerSubmission.value = res
    drawerOpen.value = true
  } catch {
    toast.error('Gagal memuat detail')
  }
}

async function bulkApprove() {
  const ids = selectedRows.value.map(r => r.id)
  if (!ids.length) return
  bulkLoading.value = true
  try {
    const res = await api.post<any[]>('/api/otorisasi/bulk/approve', { ids })
    const failed = res.filter((r: any) => r.error)
    if (failed.length) {
      toast.warning(`${failed.length} submission gagal diotorisasi`)
    } else {
      toast.success(`${ids.length} submission diotorisasi`)
    }
    selectedRows.value = []
    await load()
  } catch {
    toast.error('Bulk approve gagal')
  } finally {
    bulkLoading.value = false
    showBulkRejectInput.value = false
  }
}

async function bulkReject() {
  if (!bulkRejectNotes.value.trim()) return
  const ids = selectedRows.value.map(r => r.id)
  bulkLoading.value = true
  try {
    await api.post('/api/otorisasi/bulk/reject', { ids, notes: bulkRejectNotes.value })
    toast.warning(`${ids.length} submission ditolak`)
    selectedRows.value = []
    bulkRejectNotes.value = ''
    showBulkRejectInput.value = false
    await load()
  } catch {
    toast.error('Bulk reject gagal')
  } finally {
    bulkLoading.value = false
  }
}

function onPageChange(e: { page: number; rows: number }) {
  page.value = e.page
  pageSize.value = e.rows
  load()
}

function onApproved() { load() }
function onRejected() { load() }
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <div class="flex items-center gap-2">
      <ShieldCheck class="w-5 h-5 text-blue-600" />
      <h1 class="text-xl font-semibold text-gray-800">Otorisasi</h1>
    </div>

    <!-- Filter entity type -->
    <div class="flex gap-2 flex-wrap">
      <button v-for="et in entityTypes" :key="String(et.value)"
              @click="filterEntityType = et.value; page = 0; load()"
              :class="['px-3 py-1.5 rounded text-sm border transition',
                       filterEntityType === et.value
                         ? 'bg-blue-600 text-white border-blue-600'
                         : 'bg-white text-gray-600 border-gray-300 hover:border-blue-400']">
        {{ et.label }}
      </button>
    </div>

    <!-- Bulk actions bar -->
    <div v-if="selectedRows.length"
         class="flex items-center gap-3 bg-blue-50 border border-blue-200 rounded px-4 py-2 flex-wrap">
      <span class="text-sm text-blue-700 font-medium">{{ selectedRows.length }} dipilih</span>
      <button @click="bulkApprove" :disabled="bulkLoading"
              class="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50">
        Otorisasi ({{ selectedRows.length }})
      </button>
      <button @click="showBulkRejectInput = !showBulkRejectInput"
              class="px-3 py-1 border border-red-500 text-red-600 text-sm rounded hover:bg-red-50">
        Tolak ({{ selectedRows.length }})
      </button>
      <div v-if="showBulkRejectInput" class="flex gap-2 flex-1 min-w-0">
        <input v-model="bulkRejectNotes" placeholder="Alasan penolakan"
               class="flex-1 border rounded px-2 py-1 text-sm min-w-0" />
        <button @click="bulkReject" :disabled="!bulkRejectNotes.trim() || bulkLoading"
                class="px-3 py-1 bg-red-600 text-white text-sm rounded disabled:opacity-50 shrink-0">
          Konfirmasi
        </button>
      </div>
    </div>

    <!-- Pagination (top) -->
    <div class="border rounded-t bg-white px-4 py-2 flex items-center justify-between">
      <span class="text-sm text-gray-500">
        Menampilkan {{ total === 0 ? 0 : page * pageSize + 1 }}–{{ Math.min((page + 1) * pageSize, total) }} dari {{ total }} submission
      </span>
      <Paginator :rows="pageSize" :totalRecords="total" :first="page * pageSize"
                 @page="onPageChange" :rowsPerPageOptions="[25, 50]" class="text-sm" />
    </div>

    <!-- Table -->
    <div class="overflow-x-auto border border-t-0 rounded-b">
      <DataTable :value="rows" v-model:selection="selectedRows" dataKey="id"
                 :loading="loading" class="w-full" selectionMode="multiple">
        <Column selectionMode="multiple" headerStyle="width: 3rem" />
        <Column field="entity_label" header="Jenis" />
        <Column field="submitted_by" header="Inputer" />
        <Column field="branch_code" header="Cabang" />
        <Column header="Disubmit">
          <template #body="{ data }">{{ data.submitted_at ? dmy(data.submitted_at) : '—' }}</template>
        </Column>
        <Column header="Total">
          <template #body="{ data }">
            <span v-if="data.payload?.items?.length">
              Rp {{ data.payload.items.reduce((s: number, i: any) => s + (i.amount || 0), 0).toLocaleString('id-ID') }}
            </span>
            <span v-else>—</span>
          </template>
        </Column>
        <Column header="Level">
          <template #body="{ data }">{{ data.level_current }}/{{ data.level_required }}</template>
        </Column>
        <Column header="Aksi">
          <template #body="{ data }">
            <button @click="openDetail(data)"
                    class="text-blue-600 text-sm hover:underline">Lihat Detail</button>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- Detail Drawer -->
    <SubmissionDetailDrawer
      :open="drawerOpen"
      :submission="drawerSubmission"
      @close="drawerOpen = false"
      @approved="onApproved"
      @rejected="onRejected"
    />
  </div>
</template>

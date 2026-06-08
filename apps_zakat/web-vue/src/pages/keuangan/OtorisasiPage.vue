<script setup lang="ts">
import { ShieldCheck } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'

import TablePagination from '@/components/ui/TablePagination.vue'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import SubmissionDetailDrawer from '@/components/otorisasi/SubmissionDetailDrawer.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

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
const total = shallowRef(0)
const totalPages = shallowRef(1)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const loading = shallowRef(false)
const hasLoaded = shallowRef(false)
const selectedIds = ref(new Set<number>())
const filterEntityType = shallowRef<string | null>(null)
const drawerOpen = ref(false)
const drawerSubmission = ref<SubmissionRow | null>(null)
const bulkLoading = shallowRef(false)
const bulkRejectNotes = ref('')
const showBulkRejectInput = ref(false)

const entityTypes = [
  { label: 'Semua', value: null },
  { label: 'Penghimpunan', value: 'penghimpunan' },
  { label: 'Penyaluran', value: 'penyaluran' },
  { label: 'Upload', value: 'upload_penghimpunan' },
  { label: 'COA', value: 'coa' },
  { label: 'Kas', value: 'kas' },
  { label: 'Bank', value: 'bank' },
]

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const selectedRows = computed(() => rows.value.filter(r => selectedIds.value.has(r.id)))
const allSelected = computed(() => rows.value.length > 0 && rows.value.every(r => selectedIds.value.has(r.id)))
const someSelected = computed(() => selectedIds.value.size > 0 && !allSelected.value)

const showCount = computed(() => {
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, total.value)
  return total.value > 0 ? `Showing ${from}–${to} of ${total.value} submission` : 'Tidak ada submission pending'
})

function toggleAll() {
  if (allSelected.value) {
    selectedIds.value = new Set()
  } else {
    selectedIds.value = new Set(rows.value.map(r => r.id))
  }
}

function toggleRow(id: number) {
  const next = new Set(selectedIds.value)
  next.has(id) ? next.delete(id) : next.add(id)
  selectedIds.value = next
}

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

async function load() {
  loading.value = true
  selectedIds.value = new Set()
  showBulkRejectInput.value = false
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      page_size: String(pageSize.value),
    })
    if (filterEntityType.value) params.set('entity_type', filterEntityType.value)
    const res = await api.get<ListResponse>(`/api/otorisasi/pending/?${params}`)
    rows.value = res.rows
    total.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
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
    await load()
  } catch {
    toast.error('Bulk approve gagal')
  } finally {
    bulkLoading.value = false
  }
}

async function bulkReject() {
  if (!bulkRejectNotes.value.trim()) return
  const ids = selectedRows.value.map(r => r.id)
  bulkLoading.value = true
  try {
    await api.post('/api/otorisasi/bulk/reject', { ids, notes: bulkRejectNotes.value })
    toast.warning(`${ids.length} submission ditolak`)
    bulkRejectNotes.value = ''
    await load()
  } catch {
    toast.error('Bulk reject gagal')
  } finally {
    bulkLoading.value = false
  }
}

function onApproved() { drawerOpen.value = false; load() }
function onRejected() { drawerOpen.value = false; load() }
</script>

<template>
  <div class="space-y-0">
    <header class="mb-4 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-2">
        <ShieldCheck class="h-6 w-6 text-primary" />
        <h1 class="text-2xl font-bold tracking-tight">Otorisasi</h1>
      </div>
    </header>

    <!-- Toolbar: entity filter + contextual bulk actions -->
    <div class="flex flex-wrap items-center gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <!-- Entity type filter chips -->
      <div class="flex flex-wrap gap-1.5">
        <button
          v-for="et in entityTypes"
          :key="String(et.value)"
          :class="[
            'rounded border px-3 py-1 text-xs font-medium transition',
            filterEntityType === et.value
              ? 'border-primary bg-primary text-white'
              : 'border-zinc-300 bg-white text-zinc-600 hover:border-primary hover:text-primary dark:bg-zinc-800',
          ]"
          @click="filterEntityType = et.value; page = 1; load()"
        >{{ et.label }}</button>
      </div>

      <!-- Bulk actions (contextual — only when rows selected) -->
      <template v-if="selectedRows.length">
        <div class="ml-auto flex flex-wrap items-center gap-2">
          <span class="text-xs font-medium text-zinc-500">{{ selectedRows.length }} dipilih</span>
          <button
            class="rounded border border-green-600 px-3 py-1 text-xs font-medium text-green-700 hover:bg-green-50 transition disabled:opacity-50"
            :disabled="bulkLoading"
            @click="bulkApprove"
          >Otorisasi ({{ selectedRows.length }})</button>
          <button
            class="rounded border border-red-400 px-3 py-1 text-xs font-medium text-red-600 hover:bg-red-50 transition"
            @click="showBulkRejectInput = !showBulkRejectInput"
          >Tolak ({{ selectedRows.length }})</button>
          <template v-if="showBulkRejectInput">
            <input
              v-model="bulkRejectNotes"
              placeholder="Alasan penolakan"
              class="h-7 rounded border px-2 text-xs focus:outline-none focus:ring-1 focus:ring-primary dark:bg-zinc-800"
            />
            <button
              class="rounded border border-red-600 bg-red-600 px-3 py-1 text-xs font-medium text-white hover:bg-red-700 transition disabled:opacity-50"
              :disabled="!bulkRejectNotes.trim() || bulkLoading"
              @click="bulkReject"
            >Konfirmasi</button>
          </template>
        </div>
      </template>
    </div>

    <!-- Pagination TOP -->
    <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
      <span class="text-xs text-zinc-500">
        {{ hasLoaded ? showCount : 'Memuat...' }}
      </span>
      <TablePagination
        v-if="hasLoaded && totalPages > 1"
        :page="page"
        :total-pages="totalPages"
        :total="total"
        :page-size="pageSize"
        @goto="goto"
      />
    </div>

    <!-- Table -->
    <div class="overflow-x-auto rounded-b border">
      <table class="w-full text-sm">
        <thead class="bg-zinc-50 text-xs font-semibold uppercase text-zinc-500 dark:bg-zinc-800">
          <tr>
            <th class="w-10 px-4 py-2 text-left">
              <input
                type="checkbox"
                :checked="allSelected"
                :indeterminate="someSelected"
                class="cursor-pointer rounded border-zinc-300"
                @change="toggleAll"
              />
            </th>
            <th class="px-4 py-2 text-left">Jenis</th>
            <th class="px-4 py-2 text-left">Inputer</th>
            <th class="px-4 py-2 text-left">Cabang</th>
            <th class="px-4 py-2 text-left">Disubmit</th>
            <th class="px-4 py-2 text-right">Total</th>
            <th class="px-4 py-2 text-center">Level</th>
            <th class="px-4 py-2 text-center">Status</th>
            <th class="px-4 py-2 text-left">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading && !rows.length">
            <td colspan="9" class="px-4 py-8 text-center text-zinc-400">Memuat...</td>
          </tr>
          <tr v-else-if="hasLoaded && rows.length === 0">
            <td colspan="9" class="px-4 py-8 text-center text-zinc-400">
              Tidak ada submission pending.
            </td>
          </tr>
          <tr
            v-for="row in rows"
            :key="row.id"
            class="border-t hover:bg-zinc-50 dark:hover:bg-zinc-800"
          >
            <td class="px-4 py-2">
              <input
                type="checkbox"
                :checked="selectedIds.has(row.id)"
                class="cursor-pointer rounded border-zinc-300"
                @change="toggleRow(row.id)"
              />
            </td>
            <td class="px-4 py-2 font-medium">{{ row.entity_label }}</td>
            <td class="px-4 py-2 text-zinc-600">{{ row.submitted_by }}</td>
            <td class="px-4 py-2 text-zinc-600">{{ row.branch_code }}</td>
            <td class="px-4 py-2">{{ row.submitted_at ? dmy(row.submitted_at) : '—' }}</td>
            <td class="px-4 py-2 text-right font-medium">
              <template v-if="row.payload?.items?.length">
                {{ fmt(row.payload.items.reduce((s: number, i: any) => s + (i.amount ?? 0), 0)) }}
              </template>
              <template v-else>—</template>
            </td>
            <td class="px-4 py-2 text-center text-xs text-zinc-500">
              {{ row.level_current }}/{{ row.level_required }}
            </td>
            <td class="px-4 py-2 text-center">
              <StatusBadge :status="(row.status as any)" />
            </td>
            <td class="px-4 py-2">
              <button
                class="text-xs font-medium text-primary hover:underline"
                @click="openDetail(row)"
              >Lihat Detail</button>
            </td>
          </tr>
        </tbody>
      </table>
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

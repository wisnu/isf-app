<script setup lang="ts">
import { RefreshCw, ShieldCheck } from 'lucide-vue-next'
import { computed, onMounted, onUnmounted, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import StatusBadge from '@/components/authorization/StatusBadge.vue'
import SubmissionDetailDrawer from '@/components/authorization/SubmissionDetailDrawer.vue'
import DateField from '@/shared/components/DateField.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import { api } from '@/shared/api/client'
import { dmyt } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'
import type { SubmissionRow } from '@/types/authorization'

const toast = useToast()

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

function defaultDateFrom(): string {
  const d = new Date()
  d.setMonth(d.getMonth() - 1)
  return d.toISOString().slice(0, 10)
}
const filterDateFrom = shallowRef(defaultDateFrom())
const filterDateTo = shallowRef(new Date().toISOString().slice(0, 10))
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

const PAYMENT_LABEL: Record<string, string> = {
  K: 'Kas Kecil', C: 'Kas Cabang', B: 'Bank', A: 'Aset/GL',
}

type SummaryItem = { label: string; value: string; isAction?: boolean }

function parsePayload(payload: unknown): Record<string, any> {
  if (typeof payload === 'string') {
    try { return JSON.parse(payload) } catch { return {} }
  }
  return (payload as Record<string, any>) ?? {}
}

function rowTotal(row: SubmissionRow & { _parsed?: Record<string, any> }): string {
  const items: any[] = (row._parsed ?? parsePayload(row.payload)).items ?? []
  const total = items.reduce((s, i) => s + (i.amount ?? 0), 0)
  return total > 0 ? fmt(total) : '—'
}

function summaryFor(row: SubmissionRow & { _parsed?: Record<string, any> }): SummaryItem[] {
  const p = row._parsed ?? parsePayload(row.payload)
  const items: (SummaryItem | null)[] = []

  switch (row.entity_type) {
    case 'penghimpunan':
      items.push(
        p.donor_name ? { label: 'Donatur', value: p.donor_name } : null,
        p.payment_type ? { label: 'Bayar', value: PAYMENT_LABEL[p.payment_type] ?? p.payment_type } : null,
        p.items?.length ? { label: 'Item', value: `${p.items.length} produk` } : null,
      )
      break
    case 'penyaluran':
      items.push(
        p.description ? { label: 'Ket', value: p.description } : null,
        p.payment_type ? { label: 'Bayar', value: PAYMENT_LABEL[p.payment_type] ?? p.payment_type } : null,
        p.items?.length ? { label: 'Item', value: `${p.items.length} produk` } : null,
      )
      break
    case 'upload_penghimpunan':
      items.push(
        p.filename ? { label: 'File', value: p.filename } : null,
        (p.total_rows ?? p.rows?.length) != null
          ? { label: 'Baris', value: String(p.total_rows ?? p.rows?.length) }
          : null,
        p.total_amount != null ? { label: 'Total', value: fmt(p.total_amount) } : null,
      )
      break
    case 'coa':
      items.push(
        p.action ? { label: 'Aksi', value: String(p.action).toUpperCase(), isAction: true } : null,
        p.account_no ? { label: 'Kode', value: p.account_no } : null,
        p.account_name ? { label: 'Nama', value: p.account_name } : null,
        p.account_type ? { label: 'Tipe', value: p.account_type } : null,
      )
      break
    case 'kas':
      items.push(
        p.action ? { label: 'Aksi', value: String(p.action).toUpperCase(), isAction: true } : null,
        (p.account_name ?? p.name ?? p.code) ? { label: 'Nama', value: p.account_name ?? p.name ?? p.code } : null,
      )
      break
    case 'bank':
      items.push(
        p.action ? { label: 'Aksi', value: String(p.action).toUpperCase(), isAction: true } : null,
        p.account_name ? { label: 'Nama', value: p.account_name } : null,
        p.bank_account_no ? { label: 'No. Rek', value: p.bank_account_no } : null,
        (p.bank_name ?? p.bank_code) ? { label: 'Bank', value: p.bank_name ?? p.bank_code } : null,
      )
      break
  }

  return items.filter((x): x is SummaryItem => x !== null)
}

const selectedRows = computed(() => rows.value.filter(r => selectedIds.value.has(r.id)))
const allSelected = computed(() => rows.value.length > 0 && rows.value.every(r => selectedIds.value.has(r.id)))
const someSelected = computed(() => selectedIds.value.size > 0 && !allSelected.value)

const parsedRows = computed(() =>
  rows.value.map(r => ({ ...r, _parsed: parsePayload(r.payload) }))
)

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
    if (filterDateFrom.value) params.set('date_from', filterDateFrom.value)
    if (filterDateTo.value) params.set('date_to', filterDateTo.value)
    const res = await api.get<ListResponse>(`/api/authorization/pending/?${params}`)
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

// Auto-refresh setiap 5s saat ada submission PROCESSING
const hasProcessing = computed(() => rows.value.some(r => r.status === 'PROCESSING'))
let refreshTimer: ReturnType<typeof setInterval> | null = null

watch(hasProcessing, (val) => {
  if (val && !refreshTimer) {
    refreshTimer = setInterval(() => load(), 5000)
  } else if (!val && refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}, { immediate: true })

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
})

async function openDetail(row: SubmissionRow) {
  try {
    const res = await api.get<SubmissionRow>(`/api/authorization/submission/${row.id}`)
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
    const res = await api.post<any[]>('/api/authorization/bulk/approve', { ids })
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
    await api.post('/api/authorization/bulk/reject', { ids, notes: bulkRejectNotes.value })
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
    <PageHeader title="Otorisasi" subtitle="Daftar submission menunggu persetujuan">
      <template #actions>
        <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" :disabled="loading" @click="load()">
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
          Refresh
        </Button>
      </template>
    </PageHeader>

    <!-- Toolbar: filter + bulk actions -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <!-- Tanggal dari -->
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Dari Tanggal</label>
        <DateField v-model="filterDateFrom" />
      </div>
      <!-- Tanggal sampai -->
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai Tanggal</label>
        <DateField v-model="filterDateTo" />
      </div>
      <!-- Entity type filter dropdown -->
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Jenis Input</label>
        <select
          v-model="filterEntityType"
          class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
          @change="page = 1; load()"
        >
          <option v-for="et in entityTypes" :key="String(et.value)" :value="et.value">
            {{ et.label }}
          </option>
        </select>
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
        @prev="goto(page - 1)"
        @next="goto(page + 1)"
        @update:page-size="pageSize = $event; goto(1)"
      />
    </div>

    <!-- Table -->
    <div class="overflow-x-auto rounded-b border">
      <table class="w-full text-sm">
        <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
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
            <th class="px-4 py-2 font-medium text-left">Jenis</th>
            <th class="px-4 py-2 font-medium text-left">Inputer</th>
            <th class="px-4 py-2 font-medium text-left">Cabang</th>
            <th class="px-4 py-2 font-medium text-left">Disubmit</th>
            <th class="px-4 py-2 font-medium text-left">Operasi</th>
            <th class="px-4 py-2 font-medium text-left">Ringkasan</th>
            <th class="px-4 py-2 text-right">Total</th>
            <th class="px-4 py-2 text-center">Level</th>
            <th class="px-4 py-2 text-center">Status</th>
            <th class="px-4 py-2 font-medium text-left">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading && !rows.length">
            <td colspan="11" class="px-4 py-8 text-center text-zinc-400">Memuat...</td>
          </tr>
          <tr v-else-if="hasLoaded && rows.length === 0">
            <td colspan="11" class="px-4 py-8 text-center text-zinc-400">
              Tidak ada submission pending.
            </td>
          </tr>
          <tr
            v-for="row in parsedRows"
            :key="row.id"
            class="border-b border-border last:border-0 hover:bg-background/60"
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
            <td class="px-4 py-2 text-xs">{{ row.submitted_at ? dmyt(row.submitted_at) : '—' }}</td>
            <!-- Kolom Operasi: CREATE / EDIT / DELETE -->
            <td class="px-4 py-2">
              <template v-if="row._parsed.action">
                <span
                  :class="[
                    'inline-block rounded px-1.5 py-px text-[10px] font-bold uppercase tracking-wide',
                    row._parsed.action === 'create' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300' :
                    row._parsed.action === 'delete' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300' :
                    row._parsed.action === 'edit'   ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300' :
                                                      'bg-zinc-100 text-zinc-600'
                  ]"
                >{{ String(row._parsed.action).toUpperCase() }}</span>
              </template>
              <span v-else class="text-xs text-zinc-300">—</span>
            </td>
            <!-- Kolom Ringkasan: detail tanpa action -->
            <td class="px-4 py-2">
              <div class="space-y-0.5">
                <div
                  v-for="item in summaryFor(row).filter(i => !i.isAction)"
                  :key="item.label"
                  class="flex items-baseline gap-1 text-xs"
                >
                  <span class="shrink-0 text-zinc-400">{{ item.label }}:</span>
                  <span class="truncate max-w-[180px] text-zinc-700 dark:text-zinc-300">{{ item.value }}</span>
                </div>
                <span v-if="!summaryFor(row).filter(i => !i.isAction).length" class="text-xs text-zinc-300">—</span>
              </div>
            </td>
            <td class="px-4 py-2 text-right font-medium">{{ rowTotal(row) }}</td>
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

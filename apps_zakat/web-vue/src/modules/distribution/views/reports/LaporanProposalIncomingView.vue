<script setup lang="ts">
import { Download, FileText } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'

interface ProposalRow {
  id: number
  proposal_date: string
  proposal_number: string
  mustahiq_name: string
  program_type: string
  description: string
  amount: number
  received_by: string | null
  received_date: string | null
  reference: string | null
  realization_date: string | null
  realization_amount: number
  memo_number: string | null
  fund_source: string | null
}

interface ListResponse {
  rows: ProposalRow[]
  total: number
  page: number
  page_size: number
}

interface MustahiqOption {
  id: number
  name: string
}

const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const today = new Date()
const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1)
const dateFrom = shallowRef(firstDayOfMonth.toISOString().split('T')[0])
const dateTo = shallowRef(today.toISOString().split('T')[0])
const mustahiqId = ref<number | null>(null)
const mustahiqOptions = ref<MustahiqOption[]>([])

const rows = ref<ProposalRow[]>([])
const total = ref(0)
const page = shallowRef(1)
const pageSize = 25

const hasData = computed(() => rows.value.length > 0)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

async function loadMustahiq() {
  try {
    mustahiqOptions.value = await api.get<MustahiqOption[]>('/api/distribution/mustahiq/lookup')
  } catch {
    mustahiqOptions.value = []
  }
}

async function fetchData() {
  if (loading.value) return
  loading.value = true
  errorMsg.value = null
  page.value = 1
  try {
    const params = new URLSearchParams({
      date_from: dateFrom.value,
      date_to: dateTo.value,
      page: String(page.value),
      page_size: String(pageSize),
    })
    if (mustahiqId.value) params.set('mustahiq_id', String(mustahiqId.value))

    const res = await api.get<ListResponse>(`/api/distribution/report/proposal-incoming?${params}`)
    rows.value = res.rows
    total.value = res.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    rows.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

async function exportExcel() {
  if (exporting.value) return
  exporting.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      date_from: dateFrom.value,
      date_to: dateTo.value,
    })
    if (mustahiqId.value) params.set('mustahiq_id', String(mustahiqId.value))

    const now = new Date()
    const ts = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
    await api.downloadBlob(
      `/api/distribution/report/proposal-incoming/export.xlsx?${params}`,
      `laporan-proposal-masuk-${ts}.xlsx`
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

function onPageChange(event: { page: number; rows: number }) {
  page.value = event.page + 1
  fetchData()
}

onMounted(() => {
  loadMustahiq()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Laporan Proposal Masuk</h1>
      <p class="text-sm text-muted">Daftar proposal yang diterima untuk program penyaluran</p>
    </div>

    <!-- Filter Card -->
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Proposal Dari</label>
        <DateField v-model="dateFrom" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Proposal S/D</label>
        <DateField v-model="dateTo" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Mustahiq</label>
        <SearchSelect
          :options="mustahiqOptions"
          :model-value="mustahiqId"
          placeholder="Pilih mustahiq..."
          option-label="name"
          option-value="id"
          @update:model-value="mustahiqId = $event"
        />
      </div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="fetchData">
        <FileText class="w-4 h-4" :class="{ 'animate-pulse': loading }" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !hasData" @click="exportExcel">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <!-- Error Alert -->
    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <!-- Empty State -->
    <div v-if="!hasData && !loading" class="flex flex-col items-center justify-center py-16 text-neutral-400">
      <FileText class="w-12 h-12 mb-3 opacity-40" />
      <p class="text-sm">Isi filter dan klik <strong>Tampilkan</strong> untuk melihat data</p>
    </div>

    <!-- Data Section -->
    <template v-else>
      <!-- Pagination Info and Controls (ABOVE table) -->
      <div v-if="hasData || loading" class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="total > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, total) }} dari {{ total }} data
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="total"
          :page-size="pageSize"
          @prev="page > 1 && (page--, fetchData())"
          @next="page < totalPages && (page++, fetchData())"
        />
      </div>

      <!-- Table -->
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-muted/30">
              <tr>
                <th class="px-4 py-2 text-left font-medium">No</th>
                <th class="px-4 py-2 text-left font-medium">Nama Mustahiq</th>
                <th class="px-4 py-2 text-left font-medium">Jenis Program</th>
                <th class="px-4 py-2 text-left font-medium">No Proposal</th>
                <th class="px-4 py-2 text-left font-medium">Tgl Proposal</th>
                <th class="px-4 py-2 text-left font-medium">Deskripsi</th>
                <th class="px-4 py-2 text-right font-medium">Nominal</th>
                <th class="px-4 py-2 text-left font-medium">Diterima Oleh</th>
                <th class="px-4 py-2 text-left font-medium">Tgl Diterima</th>
                <th class="px-4 py-2 text-left font-medium">Referensi</th>
                <th class="px-4 py-2 text-left font-medium">Tgl Realisasi</th>
                <th class="px-4 py-2 text-right font-medium">Nominal Realisasi</th>
                <th class="px-4 py-2 text-left font-medium">No Memo</th>
                <th class="px-4 py-2 text-left font-medium">Sumber Dana</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-if="loading">
                <td colspan="14" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
              </tr>
              <tr v-else-if="!rows.length">
                <td colspan="14" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                  Tidak ada data yang ditemukan.
                </td>
              </tr>
              <tr v-for="(row, idx) in rows" :key="row.id" class="hover:bg-muted/30 transition-colors">
                <td class="px-4 py-1 text-xs">{{ (page - 1) * pageSize + idx + 1 }}</td>
                <td class="px-4 py-1 text-xs">{{ row.mustahiq_name }}</td>
                <td class="px-4 py-1 text-xs">{{ row.program_type }}</td>
                <td class="px-4 py-1 text-xs">{{ row.proposal_number }}</td>
                <td class="px-4 py-1 text-xs whitespace-nowrap">{{ dmy(row.proposal_date) }}</td>
                <td class="px-4 py-1 text-xs">{{ row.description }}</td>
                <td class="px-4 py-1 text-xs text-right tabular-nums whitespace-nowrap">{{ fmt(row.amount) }}</td>
                <td class="px-4 py-1 text-xs">{{ row.received_by }}</td>
                <td class="px-4 py-1 text-xs whitespace-nowrap">{{ row.received_date ? dmy(row.received_date) : '-' }}</td>
                <td class="px-4 py-1 text-xs">{{ row.reference || '-' }}</td>
                <td class="px-4 py-1 text-xs whitespace-nowrap">{{ row.realization_date ? dmy(row.realization_date) : '-' }}</td>
                <td class="px-4 py-1 text-xs text-right tabular-nums whitespace-nowrap">{{ fmt(row.realization_amount) }}</td>
                <td class="px-4 py-1 text-xs">{{ row.memo_number || '-' }}</td>
                <td class="px-4 py-1 text-xs">{{ row.fund_source || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

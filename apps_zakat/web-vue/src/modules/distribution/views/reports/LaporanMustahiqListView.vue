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

interface MustahiqRow {
  id: number
  mustahiq_id: string
  name: string
  mustahiq_type: string
  ashnaf: string
  address: string
  phone: string | null
  supervisor_name: string | null
  program_name: string
  program_date: string
  planned_distribution: number
}

interface ListResponse {
  rows: MustahiqRow[]
  total: number
  page: number
  page_size: number
}

interface ProgramOption {
  id: number
  name: string
}

const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const mustahiqType = ref<string>('')
const programId = ref<number | null>(null)
const programOptions = ref<ProgramOption[]>([])
const dateStartFrom = ref<string>('')
const dateStartTo = ref<string>('')

const rows = ref<MustahiqRow[]>([])
const total = ref(0)
const page = shallowRef(1)
const pageSize = 25

const hasData = computed(() => rows.value.length > 0)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

const mustahiqTypeOptions = [
  { value: '', label: 'Semua' },
  { value: 'MP', label: 'Individu' },
  { value: 'MC', label: 'Lembaga' },
]

async function loadPrograms() {
  try {
    programOptions.value = await api.get<ProgramOption[]>('/api/distribution/program/lookup')
  } catch {
    programOptions.value = []
  }
}

async function fetchData() {
  if (loading.value) return
  loading.value = true
  errorMsg.value = null
  page.value = 1
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      page_size: String(pageSize),
    })
    if (mustahiqType.value) params.set('mustahiq_type', mustahiqType.value)
    if (programId.value) params.set('product_id', String(programId.value))
    if (dateStartFrom.value) params.set('date_start_from', dateStartFrom.value)
    if (dateStartTo.value) params.set('date_start_to', dateStartTo.value)

    const res = await api.get<ListResponse>(`/api/distribution/report/mustahiq-list?${params}`)
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
    const params = new URLSearchParams()
    if (mustahiqType.value) params.set('mustahiq_type', mustahiqType.value)
    if (programId.value) params.set('product_id', String(programId.value))
    if (dateStartFrom.value) params.set('date_start_from', dateStartFrom.value)
    if (dateStartTo.value) params.set('date_start_to', dateStartTo.value)

    const now = new Date()
    const ts = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
    await api.downloadBlob(
      `/api/distribution/report/mustahiq-list/export.xlsx?${params}`,
      `laporan-daftar-mustahiq-${ts}.xlsx`
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
  loadPrograms()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Laporan Daftar Mustahiq</h1>
      <p class="text-sm text-muted">Daftar lengkap penerima manfaat program penyaluran</p>
    </div>

    <!-- Filter Card -->
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Golongan</label>
        <select v-model="mustahiqType" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="o in mustahiqTypeOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Program</label>
        <SearchSelect
          :options="programOptions"
          :model-value="programId"
          placeholder="Pilih program..."
          option-label="name"
          option-value="id"
          @update:model-value="programId = $event"
        />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tgl Program Dari</label>
        <DateField v-model="dateStartFrom" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tgl Program S/D</label>
        <DateField v-model="dateStartTo" />
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
                <th class="px-4 py-2 text-left font-medium">ID Mustahiq</th>
                <th class="px-4 py-2 text-left font-medium">Nama</th>
                <th class="px-4 py-2 text-left font-medium">Golongan</th>
                <th class="px-4 py-2 text-left font-medium">Ashnaf</th>
                <th class="px-4 py-2 text-left font-medium">Alamat</th>
                <th class="px-4 py-2 text-left font-medium">Telepon</th>
                <th class="px-4 py-2 text-left font-medium">Supervisor</th>
                <th class="px-4 py-2 text-left font-medium">Nama Program</th>
                <th class="px-4 py-2 text-left font-medium">Tgl Program</th>
                <th class="px-4 py-2 text-right font-medium">Rencana Distribusi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-if="loading">
                <td colspan="11" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
              </tr>
              <tr v-else-if="!rows.length">
                <td colspan="11" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                  Tidak ada data yang ditemukan.
                </td>
              </tr>
              <tr v-for="(row, idx) in rows" :key="row.id" class="hover:bg-muted/30 transition-colors">
                <td class="px-4 py-1 text-xs">{{ (page - 1) * pageSize + idx + 1 }}</td>
                <td class="px-4 py-1 text-xs">{{ row.mustahiq_id }}</td>
                <td class="px-4 py-1 text-xs">{{ row.name }}</td>
                <td class="px-4 py-1 text-xs">{{ row.mustahiq_type === 'MP' ? 'Individu' : row.mustahiq_type === 'MC' ? 'Lembaga' : row.mustahiq_type }}</td>
                <td class="px-4 py-1 text-xs">{{ row.ashnaf }}</td>
                <td class="px-4 py-1 text-xs">{{ row.address }}</td>
                <td class="px-4 py-1 text-xs">{{ row.phone || '-' }}</td>
                <td class="px-4 py-1 text-xs">{{ row.supervisor_name || '-' }}</td>
                <td class="px-4 py-1 text-xs">{{ row.program_name }}</td>
                <td class="px-4 py-1 text-xs whitespace-nowrap">{{ dmy(row.program_date) }}</td>
                <td class="px-4 py-1 text-xs text-right tabular-nums whitespace-nowrap">{{ fmt(row.planned_distribution) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

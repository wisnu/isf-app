<script setup lang="ts">
import {
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  Download,
  Search,
} from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import AppDataTable from '@/components/ui/AppDataTable.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'

interface JournalRow {
  journal_date: string | null
  journal_no: string | null
  transactionno: string | null
  account_branch_code: string | null
  account_code: string | null
  account_name: string | null
  subaccountcode: string | null
  subaccountname: string | null
  description: string | null
  debit_ekuiv: number
  credit_ekuiv: number
  inputer: string | null
}
interface JournalPage {
  rows: JournalRow[]
  total: number
  capped: boolean
  page: number
  page_size: number
}
interface BranchOption {
  code: string
  name: string
}

const auth = useAuthStore()
const canAll = computed(() => auth.user?.branch_access === 'all')

const today = new Date().toISOString().slice(0, 10)
const begin = shallowRef(today)
const end = shallowRef(today)
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const page = shallowRef(1)
const pageSize = shallowRef(50)
const data = ref<JournalPage | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const fmt = (n: number) => (n ? idr.format(n) : '')

const totalPages = computed(() =>
  data.value ? Math.max(1, Math.ceil(data.value.total / data.value.page_size)) : 1,
)

function queryParams(withPaging: boolean): string {
  const p = new URLSearchParams()
  p.set('begin', begin.value)
  p.set('end', end.value)
  if (branch.value) p.set('branch', branch.value)
  if (withPaging) {
    p.set('page', String(page.value))
    p.set('page_size', String(pageSize.value))
  }
  return p.toString()
}

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/journal-daily/branches')
    // 'single' user: kunci ke primary_branch (atau satu-satunya cabang yang ada)
    if (!canAll.value && !branch.value && branches.value.length) {
      branch.value = branches.value[0].code
    }
  } catch {
    branches.value = []
  }
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<JournalPage>(`/api/report/journal-daily?${queryParams(true)}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'
    data.value = null
  } finally {
    loading.value = false
  }
}

function search() {
  page.value = 1
  load()
}

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value)
  load()
}

async function exportXlsx() {
  exporting.value = true
  errorMsg.value = null
  try {
    const d = new Date()
    const p = (n: number) => String(n).padStart(2, '0')
    const ts = `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`
    await api.downloadBlob(
      `/api/report/journal-daily/export.xlsx?${queryParams(false)}`,
      `journaldaily-${ts}.xlsx`,
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

// Standar laporan: jangan auto-load data saat buka halaman — hanya siapkan
// filter (cabang). Data di-load saat klik "Tampilkan".
onMounted(async () => {
  await loadBranches()
})
</script>

<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Laporan Jurnal Harian</h1>
        <p class="text-sm text-muted">Daftar jurnal transaksi per cabang &amp; periode (sumber: dwh.v_journal_daily)</p>
      </div>
    </div>

    <!-- Filter bar -->
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select
          v-model="branch"
          :disabled="!canAll"
          class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 disabled:cursor-not-allowed focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option v-if="canAll" value="ALL">Semua cabang</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">
            {{ b.code }} — {{ b.name }}
          </option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Dari Tanggal</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Sampai Tanggal</label>
        <DateField v-model="end" />
      </div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="search">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" />
        Tampilkan
      </Button>
      <Button
        variant="outline" size="sm" class="gap-1.5 h-9"
        :disabled="exporting || loading || !data || data.total === 0"
        @click="exportXlsx"
      >
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="data?.capped" class="flex items-center gap-2 text-sm rounded-lg border border-amber-300 bg-amber-50 text-amber-800 px-3 py-2 dark:bg-amber-900/20 dark:text-amber-300">
      <AlertTriangle class="w-4 h-4 shrink-0" />
      Hasil {{ data.total.toLocaleString('id-ID') }} baris melebihi batas export (50.000). Persempit rentang tanggal atau pilih satu cabang sebelum export.
    </div>

    <!-- Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
        Atur filter lalu klik "Tampilkan"
      </div>

      <AppDataTable v-else :value="data?.rows ?? []" :loading="loading">
        <Column field="journal_date" header="Tanggal">
          <template #body="{ data: r }">
            <span class="whitespace-nowrap tabular-nums">{{ dmy(r.journal_date) }}</span>
          </template>
        </Column>
        <Column header="No. Transaksi">
          <template #body="{ data: r }">
            <span class="font-mono whitespace-nowrap">{{ r.transactionno || '—' }}</span>
          </template>
        </Column>
        <Column header="Akun">
          <template #body="{ data: r }">
            <span class="font-mono text-muted">{{ r.account_code }}</span>
            <span class="ml-1">{{ r.account_name }}</span>
          </template>
        </Column>
        <Column header="Sub-akun">
          <template #body="{ data: r }">
            <span class="text-muted">{{ [r.subaccountcode, r.subaccountname].filter(Boolean).join(' - ') || '—' }}</span>
          </template>
        </Column>
        <Column header="Keterangan">
          <template #body="{ data: r }">
            <span class="max-w-[24rem] truncate block" :title="r.description ?? ''">{{ r.description }}</span>
          </template>
        </Column>
        <Column header="Debet" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }">
            <span class="block text-right tabular-nums">{{ fmt(r.debit_ekuiv) }}</span>
          </template>
        </Column>
        <Column header="Kredit" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }">
            <span class="block text-right tabular-nums">{{ fmt(r.credit_ekuiv) }}</span>
          </template>
        </Column>
        <Column header="Inputer">
          <template #body="{ data: r }">{{ r.inputer || '—' }}</template>
        </Column>
        <template #empty>Tidak ada data untuk filter ini.</template>
      </AppDataTable>

      <!-- Pagination server-side — tetap manual -->
      <div v-if="data && data.total > 0" class="px-4 py-2 border-t border-border flex items-center justify-between gap-2 flex-wrap">
        <p class="text-[11px] text-muted tabular-nums">
          Hal {{ data.page }} / {{ totalPages }} · total {{ data.total.toLocaleString('id-ID') }} baris
        </p>
        <div class="flex items-center gap-1">
          <button :disabled="page <= 1 || loading" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background" @click="goto(page - 1)"><ChevronLeft class="w-3.5 h-3.5" /></button>
          <span class="text-[11px] px-2.5 py-0.5 rounded-md bg-background border border-border tabular-nums">{{ page }}</span>
          <button :disabled="page >= totalPages || loading" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background" @click="goto(page + 1)"><ChevronRight class="w-3.5 h-3.5" /></button>
        </div>
      </div>
    </div>
  </div>
</template>

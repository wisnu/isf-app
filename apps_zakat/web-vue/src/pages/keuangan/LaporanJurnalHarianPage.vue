<script setup lang="ts">
import {
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  Download,
  Loader2,
  Search,
} from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'

import Alert from '@/components/ui/Alert.vue'
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
const begin = ref(today)
const end = ref(today)
const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const page = ref(1)
const pageSize = ref(50)
const data = ref<JournalPage | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

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
      <div v-if="loading && !data" class="flex justify-center p-12">
        <Loader2 class="w-7 h-7 animate-spin text-primary" />
      </div>
      <div v-else-if="data && data.rows.length === 0" class="p-10 text-center text-sm text-muted italic">
        Tidak ada data untuk filter ini.
      </div>
      <div v-else-if="data" class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
            <tr>
              <th class="text-left px-3 py-2 font-semibold">Tanggal</th>
              <th class="text-left px-3 py-2 font-semibold">No. Transaksi</th>
              <th class="text-left px-3 py-2 font-semibold">Akun</th>
              <th class="text-left px-3 py-2 font-semibold">Sub-akun</th>
              <th class="text-left px-3 py-2 font-semibold">Keterangan</th>
              <th class="text-right px-3 py-2 font-semibold">Debet</th>
              <th class="text-right px-3 py-2 font-semibold">Kredit</th>
              <th class="text-left px-3 py-2 font-semibold">Inputer</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in data.rows" :key="i" class="border-b border-border/40 hover:bg-muted/5">
              <td class="px-3 py-1.5 whitespace-nowrap tabular-nums">{{ dmy(r.journal_date) }}</td>
              <td class="px-3 py-1.5 font-mono text-[11px] whitespace-nowrap">{{ r.transactionno || '—' }}</td>
              <td class="px-3 py-1.5">
                <span class="font-mono text-[11px] text-muted">{{ r.account_code }}</span>
                <span class="ml-1">{{ r.account_name }}</span>
              </td>
              <td class="px-3 py-1.5 text-[11px] text-muted">
                {{ [r.subaccountcode, r.subaccountname].filter(Boolean).join(' - ') || '—' }}
              </td>
              <td class="px-3 py-1.5 max-w-[24rem] truncate" :title="r.description ?? ''">{{ r.description }}</td>
              <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(r.debit_ekuiv) }}</td>
              <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(r.credit_ekuiv) }}</td>
              <td class="px-3 py-1.5 text-[11px]">{{ r.inputer || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
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

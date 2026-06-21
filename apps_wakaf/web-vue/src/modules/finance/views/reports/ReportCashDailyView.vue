<script setup lang="ts">
import { AlertTriangle, ChevronLeft, ChevronRight, Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import { api, ApiError } from '@/shared/api/client'
import { useAuthStore } from '@/app/stores/auth.store'

interface CashRow {
  actualdate: string | null
  transactionno: string | null
  mutationtype: string | null
  amount: number
  balance: number
  description: string | null
  reference_no: string | null
  inputer: string | null
  auth_status: string | null
}
interface CashPage {
  account_no: string
  begin_balance: number
  total_debit: number
  total_credit: number
  end_balance: number
  rows: CashRow[]
  total: number
  capped: boolean
  page: number
  page_size: number
}
interface BranchOption { code: string; name: string }
interface AccountOption { account_no: string; account_name: string; account_type: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const now = new Date()
const firstOfMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`
const today = now.toISOString().slice(0, 10)
const begin = ref(firstOfMonth)
const end = ref(today)

const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])
const account = ref<string>('')
const accounts = ref<AccountOption[]>([])

const page = ref(1)
const pageSize = ref(50)
const data = ref<CashPage | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const fmt = (n: number) => idr.format(n ?? 0)
const AUTH_LABEL: Record<string, string> = { T: 'Sudah Otorisasi', F: 'Belum Otorisasi' }

const totalPages = computed(() =>
  data.value ? Math.max(1, Math.ceil(data.value.total / data.value.page_size)) : 1,
)

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/cash-mutation/branches')
    if (!branch.value && branches.value.length) branch.value = branches.value[0].code
  } catch {
    branches.value = []
  }
}

async function loadAccounts() {
  account.value = ''
  accounts.value = []
  if (!branch.value) return
  try {
    accounts.value = await api.get<AccountOption[]>(
      `/api/report/cash-accounts?branch=${encodeURIComponent(branch.value)}`,
    )
    if (accounts.value.length) account.value = accounts.value[0].account_no
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat daftar rekening'
  }
}

function qs(): string {
  const p = new URLSearchParams()
  p.set('account', account.value)
  p.set('begin', begin.value)
  p.set('end', end.value)
  return p.toString()
}

async function load() {
  if (!account.value) {
    errorMsg.value = 'Pilih rekening dulu'
    return
  }
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<CashPage>(`/api/report/cash-mutation?${qs()}&page=${page.value}&page_size=${pageSize.value}`)
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
    await api.downloadBlob(`/api/report/cash-mutation/export.xlsx?${qs()}`, `cashdaily-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

watch(branch, () => { loadAccounts() })

onMounted(async () => {
  await loadBranches()
  await loadAccounts()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Transaksi Kas/Bank Harian</h1>
      <p class="text-sm text-muted">Mutasi satu rekening kas/bank + saldo berjalan (sumber: dwh.v_cash_mutation)</p>
    </div>

    <!-- Filter bar -->
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[12rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Rekening</label>
        <select v-model="account" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[18rem] focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-if="!accounts.length" value="">(tidak ada rekening)</option>
          <option v-for="a in accounts" :key="a.account_no" :value="a.account_no">{{ a.account_no }} — {{ a.account_name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Dari Tanggal</label>
        <input v-model="begin" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Sampai Tanggal</label>
        <input v-model="end" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
      </div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading || !account" @click="search">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" />
        Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || data.total === 0" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <!-- Summary cards -->
    <div v-if="data" class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Saldo Awal</div>
        <div class="text-lg font-bold tabular-nums">{{ fmt(data.begin_balance) }}</div>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Total Debet</div>
        <div class="text-lg font-bold tabular-nums text-blue-600 dark:text-blue-400">{{ fmt(data.total_debit) }}</div>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Total Kredit</div>
        <div class="text-lg font-bold tabular-nums text-emerald-600 dark:text-emerald-400">{{ fmt(data.total_credit) }}</div>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Saldo Akhir</div>
        <div class="text-lg font-bold tabular-nums">{{ fmt(data.end_balance) }}</div>
      </div>
    </div>

    <div v-if="data?.capped" class="flex items-center gap-2 text-sm rounded-lg border border-amber-300 bg-amber-50 text-amber-800 px-3 py-2 dark:bg-amber-900/20 dark:text-amber-300">
      <AlertTriangle class="w-4 h-4 shrink-0" />
      Hasil {{ data.total.toLocaleString('id-ID') }} baris melebihi batas export (50.000). Persempit rentang tanggal.
    </div>

    <!-- Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>
      <div v-else-if="data && data.rows.length === 0" class="p-10 text-center text-sm text-muted italic">Tidak ada mutasi untuk filter ini.</div>
      <div v-else-if="data" class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
            <tr>
              <th class="text-left px-3 py-2 font-semibold">Tanggal</th>
              <th class="text-left px-3 py-2 font-semibold">No Transaksi</th>
              <th class="text-center px-2 py-2 font-semibold w-12">D/K</th>
              <th class="text-right px-3 py-2 font-semibold">Nominal</th>
              <th class="text-right px-3 py-2 font-semibold">Saldo</th>
              <th class="text-left px-3 py-2 font-semibold">Keterangan</th>
              <th class="text-left px-3 py-2 font-semibold">Referensi</th>
              <th class="text-left px-3 py-2 font-semibold">Inputer</th>
              <th class="text-left px-3 py-2 font-semibold">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in data.rows" :key="i" class="border-b border-border/40 hover:bg-muted/5">
              <td class="px-3 py-1.5 whitespace-nowrap tabular-nums">{{ r.actualdate }}</td>
              <td class="px-3 py-1.5 font-mono text-[11px] whitespace-nowrap">{{ r.transactionno }}</td>
              <td class="px-2 py-1.5 text-center">
                <span :class="['text-[10px] font-semibold px-1.5 py-px rounded', r.mutationtype === 'D' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300']">{{ r.mutationtype }}</span>
              </td>
              <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(r.amount) }}</td>
              <td class="px-3 py-1.5 text-right tabular-nums font-medium">{{ fmt(r.balance) }}</td>
              <td class="px-3 py-1.5 max-w-[20rem] truncate" :title="r.description ?? ''">{{ r.description }}</td>
              <td class="px-3 py-1.5 text-[11px]">{{ r.reference_no || '—' }}</td>
              <td class="px-3 py-1.5 text-[11px]">{{ r.inputer || '—' }}</td>
              <td class="px-3 py-1.5 text-[11px]">{{ AUTH_LABEL[r.auth_status ?? ''] ?? (r.auth_status || '—') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="data && data.total > 0" class="px-4 py-2 border-t border-border flex items-center justify-between gap-2 flex-wrap">
        <p class="text-[11px] text-muted tabular-nums">Hal {{ data.page }} / {{ totalPages }} · {{ data.total.toLocaleString('id-ID') }} mutasi</p>
        <div class="flex items-center gap-1">
          <button :disabled="page <= 1 || loading" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background" @click="goto(page - 1)"><ChevronLeft class="w-3.5 h-3.5" /></button>
          <span class="text-[11px] px-2.5 py-0.5 rounded-md bg-background border border-border tabular-nums">{{ page }}</span>
          <button :disabled="page >= totalPages || loading" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background" @click="goto(page + 1)"><ChevronRight class="w-3.5 h-3.5" /></button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AlertTriangle, Download, Search } from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import AppDataTable from '@/shared/components/AppDataTable.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
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
const begin = shallowRef(firstOfMonth)
const end = shallowRef(today)

const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])
const account = shallowRef<string>('')
const accounts = ref<AccountOption[]>([])
const accountOptions = computed(() =>
  accounts.value.map((a) => ({ value: a.account_no, label: `${a.account_no} — ${a.account_name}` })),
)

const page = shallowRef(1)
const pageSize = shallowRef(50)
const data = ref<CashPage | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const fmt = (n: number) => idr.format(n ?? 0)
const AUTH_LABEL: Record<string, string> = { T: 'Sudah Otorisasi', F: 'Belum Otorisasi' }

const totalPages = computed(() =>
  data.value ? Math.max(1, Math.ceil(data.value.total / data.value.page_size)) : 1,
)

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/finance/report/cash-mutation/branches')
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
      `/api/finance/report/cash-accounts?branch=${encodeURIComponent(branch.value)}`,
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
    data.value = await api.get<CashPage>(`/api/finance/report/cash-mutation?${qs()}&page=${page.value}&page_size=${pageSize.value}`)
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
    await api.downloadBlob(`/api/finance/report/cash-mutation/export.xlsx?${qs()}`, `cashdaily-${ts}.xlsx`)
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
        <div class="min-w-[20rem]">
          <SearchSelect v-model="account" :options="accountOptions" :placeholder="accounts.length ? 'Cari no. / nama rekening…' : '(tidak ada rekening)'" />
        </div>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Dari Tanggal</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Sampai Tanggal</label>
        <DateField v-model="end" />
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
      <!-- Pagination — atas tabel -->
      <div v-if="data && data.total > 0" class="px-4 py-2 border-b border-border flex items-center justify-end">
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="data.total"
          :loading="loading"
          unit="mutasi"
          @prev="goto(page - 1)"
          @next="goto(page + 1)"
        />
      </div>

      <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
        Atur filter lalu klik "Tampilkan"
      </div>
      <AppDataTable v-else :value="data?.rows ?? []" :loading="loading">
        <Column header="Tanggal" style="width:90px;min-width:90px">
          <template #body="{ data: r }">
            <span class="whitespace-nowrap tabular-nums">{{ dmy(r.actualdate) }}</span>
          </template>
        </Column>
        <Column header="No Transaksi" style="width:170px;min-width:150px">
          <template #body="{ data: r }">
            <span class="font-mono whitespace-nowrap">{{ r.transactionno }}</span>
          </template>
        </Column>
        <Column
          header="D/K"
          style="width:44px;min-width:44px"
          :pt="{ headerCell: { class: 'text-center px-2 py-1 font-semibold' } }"
        >
          <template #body="{ data: r }">
            <span class="flex justify-center">
              <span :class="['text-[10px] font-semibold px-1.5 py-px rounded', r.mutationtype === 'D' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300']">{{ r.mutationtype }}</span>
            </span>
          </template>
        </Column>
        <Column
          header="Nominal"
          style="width:115px;min-width:100px"
          :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold' } }"
        >
          <template #body="{ data: r }">
            <span class="block text-right tabular-nums">{{ fmt(r.amount) }}</span>
          </template>
        </Column>
        <Column
          header="Saldo"
          style="width:130px;min-width:115px"
          :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold' } }"
        >
          <template #body="{ data: r }">
            <span class="block text-right tabular-nums font-medium">{{ fmt(r.balance) }}</span>
          </template>
        </Column>
        <Column header="Keterangan" :pt="{ bodyCell: { class: 'px-3 py-1 overflow-hidden max-w-xs' } }">
          <template #body="{ data: r }">
            <span class="truncate block" :title="r.description ?? ''">{{ r.description }}</span>
          </template>
        </Column>
        <Column header="Referensi" style="width:80px;min-width:60px">
          <template #body="{ data: r }">
            <span class="text-muted">{{ r.reference_no || '—' }}</span>
          </template>
        </Column>
        <Column header="Inputer" style="width:70px;min-width:60px">
          <template #body="{ data: r }">
            <span>{{ r.inputer || '—' }}</span>
          </template>
        </Column>
        <Column header="Status" style="width:120px;min-width:100px">
          <template #body="{ data: r }">
            <span>{{ AUTH_LABEL[r.auth_status ?? ''] ?? (r.auth_status || '—') }}</span>
          </template>
        </Column>
        <template #empty>Tidak ada mutasi untuk filter ini.</template>
      </AppDataTable>
    </div>
  </div>
</template>

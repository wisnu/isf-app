<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/app/stores/auth.store'

interface AccountOption {
  account_no: string
  account_name: string
  branch_code: string
}

interface HistoryRow {
  transaction_item_id: number
  actual_date: string
  transaction_code: string | null
  mutation_type: string
  amount: number
  debet: number
  kredit: number
  running_balance: number
  reference_no: string | null
  description: string | null
  transaction_no: string | null
  inputer: string | null
  auth_status: string
}

interface HistoryResult {
  account_no: string
  account_name: string
  branch_code: string
  beginning_balance: number
  total_debet: number
  total_kredit: number
  ending_balance: number
  rows: HistoryRow[]
}

const auth = useAuthStore()
const today = new Date().toISOString().slice(0, 10)
const p = (n: number) => String(n).padStart(2, '0')
const thisYearStart = `${new Date().getFullYear()}-01-01`

const accounts = ref<AccountOption[]>([])
const selectedAccount = shallowRef('')
const begin = shallowRef(thisYearStart)
const end = shallowRef(today)

const result = ref<HistoryResult | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const hasLoaded = shallowRef(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number | null | undefined) => idr.format(Math.round(n ?? 0))

const canExport = computed(() => hasLoaded.value && result.value !== null)

async function loadAccounts() {
  try {
    const data = await api.get<{ rows: AccountOption[] }>('/api/finance/inquiry/cash-advance/accounts')
    accounts.value = data.rows
  } catch {
    accounts.value = []
  }
}

async function load() {
  if (!selectedAccount.value) {
    errorMsg.value = 'Pilih rekening terlebih dahulu.'
    return
  }
  loading.value = true
  errorMsg.value = null
  result.value = null
  try {
    result.value = await api.get<HistoryResult>(
      `/api/finance/inquiry/cash-advance/history?account_no=${encodeURIComponent(selectedAccount.value)}&begin=${begin.value}&end=${end.value}`,
    )
    hasLoaded.value = true
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data.'
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  if (!selectedAccount.value) return
  exporting.value = true
  errorMsg.value = null
  try {
    const n = new Date()
    const ts = `${n.getFullYear()}${p(n.getMonth() + 1)}${p(n.getDate())}-${p(n.getHours())}${p(n.getMinutes())}`
    await api.downloadBlob(
      `/api/finance/inquiry/cash-advance/history/export.xlsx?account_no=${encodeURIComponent(selectedAccount.value)}&begin=${begin.value}&end=${end.value}`,
      `uangmuka-${selectedAccount.value}-${ts}.xlsx`,
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal.'
  } finally {
    exporting.value = false
  }
}

onMounted(() => loadAccounts())
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Uang Muka Kegiatan</h1>
      <p class="text-sm text-muted">Histori mutasi rekening uang muka karyawan.</p>
    </div>

    <!-- Filter -->
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1 min-w-[16rem] flex-1">
        <label class="text-xs font-medium text-muted">Rekening Uang Muka</label>
        <select
          v-model="selectedAccount"
          class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="">— Pilih rekening —</option>
          <option v-for="a in accounts" :key="a.account_no" :value="a.account_no">
            {{ a.account_no }} — {{ a.account_name }}
          </option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Awal</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Akhir</label>
        <DateField v-model="end" />
      </div>
      <div class="flex gap-2">
        <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="load">
          <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" />
          Tampilkan
        </Button>
        <Button
          size="sm"
          variant="outline"
          class="gap-1.5 h-9"
          :disabled="!canExport || exporting"
          @click="exportXlsx"
        >
          <Download class="w-4 h-4" />
          Export
        </Button>
      </div>
    </div>

    <Alert v-if="errorMsg" variant="error" :message="errorMsg" />

    <!-- Empty / prompt state -->
    <div
      v-if="!hasLoaded && !loading"
      class="rounded-xl border border-border bg-surface p-12 text-center text-muted"
    >
      Pilih rekening dan rentang tanggal lalu klik <strong>Tampilkan</strong>.
    </div>

    <!-- Summary + Table -->
    <template v-if="result">
      <!-- Balance summary cards -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="rounded-xl border border-border bg-surface p-4">
          <div class="text-xs text-muted mb-1">Saldo Awal</div>
          <div class="text-lg font-semibold tabular-nums">{{ fmt(result.beginning_balance) }}</div>
        </div>
        <div class="rounded-xl border border-border bg-surface p-4">
          <div class="text-xs text-muted mb-1">Total Debet</div>
          <div class="text-lg font-semibold tabular-nums text-blue-600">{{ fmt(result.total_debet) }}</div>
        </div>
        <div class="rounded-xl border border-border bg-surface p-4">
          <div class="text-xs text-muted mb-1">Total Kredit</div>
          <div class="text-lg font-semibold tabular-nums text-orange-600">{{ fmt(result.total_kredit) }}</div>
        </div>
        <div class="rounded-xl border border-border bg-surface p-4">
          <div class="text-xs text-muted mb-1">Saldo Akhir</div>
          <div class="text-lg font-bold tabular-nums">{{ fmt(result.ending_balance) }}</div>
        </div>
      </div>

      <!-- Account info -->
      <div class="text-sm text-muted">
        Rekening: <strong>{{ result.account_no }}</strong> — {{ result.account_name }}
        <span class="ml-2 text-xs">({{ result.rows.length }} transaksi)</span>
      </div>

      <!-- Transaction table -->
      <div class="rounded-xl border border-border overflow-hidden">
        <DataTable
          :value="result.rows"
          size="small"
          striped-rows
          class="w-full"
        >
          <Column field="actual_date" header="Tanggal" style="min-width:9rem">
            <template #body="{ data }">{{ dmy(data.actual_date) }}</template>
          </Column>
          <Column field="transaction_code" header="Kode" style="min-width:7rem" />
          <Column field="transaction_no" header="No. Transaksi" style="min-width:11rem" />
          <Column field="debet" header="Debet" style="min-width:10rem;text-align:right">
            <template #body="{ data }">
              <span v-if="data.debet" class="text-blue-600 tabular-nums">{{ fmt(data.debet) }}</span>
            </template>
          </Column>
          <Column field="kredit" header="Kredit" style="min-width:10rem;text-align:right">
            <template #body="{ data }">
              <span v-if="data.kredit" class="text-orange-600 tabular-nums">{{ fmt(data.kredit) }}</span>
            </template>
          </Column>
          <Column field="running_balance" header="Saldo" style="min-width:10rem;text-align:right">
            <template #body="{ data }">
              <span class="font-medium tabular-nums">{{ fmt(data.running_balance) }}</span>
            </template>
          </Column>
          <Column field="description" header="Keterangan" style="min-width:14rem" />
          <Column field="reference_no" header="Ref" style="min-width:9rem" />
          <Column field="inputer" header="Inputer" style="min-width:8rem" />
          <Column field="auth_status" header="Status" style="min-width:10rem" />
        </DataTable>

        <div v-if="result.rows.length === 0" class="p-8 text-center text-muted">
          Tidak ada transaksi dalam periode ini.
        </div>
      </div>
    </template>
  </div>
</template>

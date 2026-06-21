<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import AppDataTable from '@/shared/components/AppDataTable.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import { api, ApiError } from '@/shared/api/client'
import { useAuthStore } from '@/app/stores/auth.store'

interface SumRow {
  account_no: string
  account_name: string | null
  begin_balance: number
  debit: number
  credit: number
  total: number
  end_balance: number
}
interface SumGroup {
  currency: string
  rows: SumRow[]
  subtotal: { begin_balance: number; debit: number; credit: number; total: number; end_balance: number }
}
interface SumPayload {
  groups: SumGroup[]
  grand: { begin_balance: number; total_debit: number; total_credit: number; total_end: number }
  period: string
}
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const now = new Date()
const firstOfMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`
const today = now.toISOString().slice(0, 10)
const begin = shallowRef(firstOfMonth)
const end = shallowRef(today)
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<SumPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const fmt = (n: number) => idr.format(n ?? 0)

// Gabungkan rows + subtotal row per group untuk AppDataTable
function groupRows(grp: SumGroup) {
  return [
    ...grp.rows.map((r) => ({ ...r, _isSubtotal: false, _label: null as string | null })),
    {
      _isSubtotal: true,
      _label: `Subtotal ${grp.currency}`,
      account_no: '',
      account_name: null,
      begin_balance: grp.subtotal.begin_balance,
      debit: grp.subtotal.debit,
      credit: grp.subtotal.credit,
      total: grp.subtotal.total,
      end_balance: grp.subtotal.end_balance,
    },
  ]
}

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/cash-summary/branches')
    if (!branch.value && branches.value.length) branch.value = branches.value[0].code
  } catch {
    branches.value = []
  }
}

function qs(): string {
  const p = new URLSearchParams()
  p.set('begin', begin.value)
  p.set('end', end.value)
  if (branch.value) p.set('branch', branch.value)
  return p.toString()
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<SumPayload>(`/api/report/cash-summary?${qs()}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'
    data.value = null
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  exporting.value = true
  errorMsg.value = null
  try {
    const d = new Date()
    const p = (n: number) => String(n).padStart(2, '0')
    const ts = `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`
    await api.downloadBlob(`/api/report/cash-summary/export.xlsx?${qs()}`, `cashsummary-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

watch(branch, () => { data.value = null })

// Standar laporan: data di-load saat klik "Tampilkan", bukan saat buka halaman.
onMounted(async () => {
  await loadBranches()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Rekapitulasi Transaksi Kas/Bank</h1>
      <p class="text-sm text-muted">Ringkasan saldo &amp; mutasi per rekening kas/bank (sumber: dwh.v_cash_summary_src)</p>
    </div>

    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
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
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading || !branch" @click="load">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.groups.length" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <!-- Grand total cards -->
    <div v-if="data" class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Total Saldo Awal</div>
        <div class="text-lg font-bold tabular-nums">{{ fmt(data.grand.begin_balance) }}</div>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Total Debet</div>
        <div class="text-lg font-bold tabular-nums text-blue-600 dark:text-blue-400">{{ fmt(data.grand.total_debit) }}</div>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Total Kredit</div>
        <div class="text-lg font-bold tabular-nums text-emerald-600 dark:text-emerald-400">{{ fmt(data.grand.total_credit) }}</div>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <div class="text-xs text-muted uppercase tracking-wide">Total Saldo Akhir</div>
        <div class="text-lg font-bold tabular-nums">{{ fmt(data.grand.total_end) }}</div>
      </div>
    </div>

    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>

    <!-- Per-currency tables -->
    <div v-else class="space-y-4">
      <div v-for="grp in data?.groups ?? []" :key="grp.currency" class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 bg-background/60 border-b border-border text-sm font-semibold">Valuta: {{ grp.currency }}</div>
        <AppDataTable :value="groupRows(grp)" :loading="loading">
          <Column header="Rekening">
            <template #body="{ data: r }">
              <span v-if="r._isSubtotal" class="font-semibold">{{ r._label }}</span>
              <span v-else>
                <span class="font-mono text-[11px] text-muted">{{ r.account_no }}</span>
                <span class="ml-1">{{ r.account_name }}</span>
              </span>
            </template>
          </Column>
          <Column header="Saldo Awal" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }">
              <span :class="['block text-right tabular-nums', r._isSubtotal ? 'font-semibold' : '']">{{ fmt(r.begin_balance) }}</span>
            </template>
          </Column>
          <Column header="Debet" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }">
              <span :class="['block text-right tabular-nums', r._isSubtotal ? 'font-semibold' : '']">{{ fmt(r.debit) }}</span>
            </template>
          </Column>
          <Column header="Kredit" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }">
              <span :class="['block text-right tabular-nums', r._isSubtotal ? 'font-semibold' : '']">{{ fmt(r.credit) }}</span>
            </template>
          </Column>
          <Column header="Total" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }">
              <span :class="['block text-right tabular-nums', r._isSubtotal ? 'font-semibold' : '']">{{ fmt(r.total) }}</span>
            </template>
          </Column>
          <Column header="Saldo Akhir" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }">
              <span :class="['block text-right tabular-nums font-medium', r._isSubtotal ? 'font-semibold' : '']">{{ fmt(r.end_balance) }}</span>
            </template>
          </Column>
          <template #empty>Tidak ada data kas untuk filter ini.</template>
        </AppDataTable>
      </div>
    </div>
  </div>
</template>

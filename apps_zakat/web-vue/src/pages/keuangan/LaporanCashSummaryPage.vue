<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

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
const begin = ref(firstOfMonth)
const end = ref(today)
const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<SumPayload | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const fmt = (n: number) => idr.format(n ?? 0)

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
        <input v-model="begin" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Sampai Tanggal</label>
        <input v-model="end" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
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

    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>
    <div v-else-if="data && data.groups.length === 0" class="rounded-xl border border-border bg-surface p-10 text-center text-sm text-muted italic">Tidak ada data kas untuk filter ini.</div>

    <!-- Per-currency tables -->
    <div v-else-if="data" class="space-y-4">
      <div v-for="grp in data.groups" :key="grp.currency" class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 bg-background/60 border-b border-border text-sm font-semibold">Valuta: {{ grp.currency }}</div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
              <tr>
                <th class="text-left px-3 py-2 font-semibold">Rekening</th>
                <th class="text-right px-3 py-2 font-semibold">Saldo Awal</th>
                <th class="text-right px-3 py-2 font-semibold">Debet</th>
                <th class="text-right px-3 py-2 font-semibold">Kredit</th>
                <th class="text-right px-3 py-2 font-semibold">Total</th>
                <th class="text-right px-3 py-2 font-semibold">Saldo Akhir</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in grp.rows" :key="r.account_no" class="border-b border-border/40 hover:bg-muted/5">
                <td class="px-3 py-1.5">
                  <span class="font-mono text-[11px] text-muted">{{ r.account_no }}</span>
                  <span class="ml-1">{{ r.account_name }}</span>
                </td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(r.begin_balance) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(r.debit) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(r.credit) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(r.total) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums font-medium">{{ fmt(r.end_balance) }}</td>
              </tr>
              <tr class="border-t-2 border-border bg-background/40 font-semibold">
                <td class="px-3 py-1.5">Subtotal {{ grp.currency }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(grp.subtotal.begin_balance) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(grp.subtotal.debit) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(grp.subtotal.credit) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(grp.subtotal.total) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums">{{ fmt(grp.subtotal.end_balance) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

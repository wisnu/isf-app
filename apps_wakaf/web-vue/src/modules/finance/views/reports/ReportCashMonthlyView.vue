<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import { api, ApiError } from '@/shared/api/client'
import { useAuthStore } from '@/app/stores/auth.store'

interface MonthlyRow { account_no: string; account_name: string | null; balances: number[] }
interface MonthlyGroup { type: string; type_label: string; rows: MonthlyRow[]; totals: number[] }
interface MonthlyPayload { groups: MonthlyGroup[]; year: number; months: string[] }
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const currentYear = new Date().getFullYear()
const yearOptions = Array.from({ length: 5 }, (_, i) => currentYear - i)
const year = ref<number>(currentYear)
const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<MonthlyPayload | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/finance/report/cash-monthly/branches')
    if (!branch.value && branches.value.length) branch.value = branches.value[0].code
  } catch {
    branches.value = []
  }
}

async function load() {
  if (!branch.value) return
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<MonthlyPayload>(`/api/report/cash-monthly?branch=${encodeURIComponent(branch.value)}&year=${year.value}`)
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
    await api.downloadBlob(
      `/api/report/cash-monthly/export.xlsx?branch=${encodeURIComponent(branch.value)}&year=${year.value}`,
      `cashmonthly-${ts}.xlsx`,
    )
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
      <h1 class="text-2xl font-bold tracking-tight">Monitoring Saldo Kas/Bank Bulanan</h1>
      <p class="text-sm text-muted">Saldo kumulatif akhir tiap bulan per rekening (sumber: dwh.v_cash_summary_src)</p>
    </div>

    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tahun</label>
        <select v-model.number="year" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
        </select>
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

    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>
    <div v-else-if="data && data.groups.length === 0" class="rounded-xl border border-border bg-surface p-10 text-center text-sm text-muted italic">Tidak ada data kas untuk filter ini.</div>

    <div v-else-if="data" class="rounded-xl border border-border bg-surface overflow-x-auto">
      <table class="w-full text-xs">
        <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
          <tr>
            <th class="text-left px-3 py-2 font-semibold sticky left-0 bg-background/50 min-w-[16rem]">Rekening</th>
            <th v-for="m in data.months" :key="m" class="text-right px-3 py-2 font-semibold whitespace-nowrap">{{ m }}</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="grp in data.groups" :key="grp.type">
            <tr class="bg-background/40">
              <td class="px-3 py-1.5 font-semibold sticky left-0 bg-background/40" :colspan="13">{{ grp.type_label }}</td>
            </tr>
            <tr v-for="r in grp.rows" :key="r.account_no" class="border-b border-border/30 hover:bg-muted/5">
              <td class="px-3 py-1 sticky left-0 bg-surface">
                <span class="font-mono text-[10px] text-muted">{{ r.account_no }}</span>
                <span class="ml-1">{{ r.account_name }}</span>
              </td>
              <td v-for="(b, mi) in r.balances" :key="mi" class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(b) }}</td>
            </tr>
            <tr class="border-y-2 border-border bg-background/30 font-semibold">
              <td class="px-3 py-1.5 sticky left-0 bg-background/30">Total {{ grp.type_label }}</td>
              <td v-for="(b, mi) in grp.totals" :key="mi" class="px-3 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(b) }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

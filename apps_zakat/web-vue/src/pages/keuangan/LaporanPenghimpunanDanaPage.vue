<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'

interface CollRow {
  actualdate: string; branch_name: string | null; account_name: string | null
  description: string | null; fund_label: string; channel: string | null; amount: number
  donorname: string | null; transactionno: string | null; inputer: string | null
}
interface CollPayload { rows: CollRow[]; total: number; total_amount: number; page: number; page_size: number }
interface RekapFund { fund_label: string; saldo_awal: number; mutasi: number; saldo_akhir: number; donors: number }
interface RekapPayload { funds: RekapFund[]; grand_total: { saldo_awal: number; mutasi: number; saldo_akhir: number; donors: number } }
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef<string>(`${today.getFullYear()}-01-01`)
const end = shallowRef<string>(iso(today))
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const fund = shallowRef<string>('')
const branches = ref<BranchOption[]>([])
const page = shallowRef(1)
const pageSize = 50

const fundOptions = [
  { v: '', label: 'Semua Dana' }, { v: '1', label: 'Zakat' }, { v: '2', label: 'Infaq' },
  { v: '3', label: 'Wakaf' }, { v: '4', label: 'Amil' }, { v: '5', label: 'Non Halal' },
]

const data = ref<CollPayload | null>(null)
const rekap = ref<RekapPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))
const totalPages = computed(() => (data.value ? Math.max(1, Math.ceil(data.value.total / pageSize)) : 1))

const qs = () => {
  let s = `begin=${begin.value}&end=${end.value}`
  if (branch.value) s += `&branch=${encodeURIComponent(branch.value)}`
  if (fund.value) s += `&fund=${fund.value}`
  return s
}

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/collection/branches')
    if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code
  } catch { branches.value = [] }
}

async function load() {
  loading.value = true; errorMsg.value = null
  try {
    const [d, rk] = await Promise.all([
      api.get<CollPayload>(`/api/report/collection?${qs()}&page=${page.value}&page_size=${pageSize}`),
      api.get<RekapPayload>(`/api/report/collection/rekap?begin=${begin.value}&end=${end.value}${branch.value ? `&branch=${encodeURIComponent(branch.value)}` : ''}`),
    ])
    data.value = d; rekap.value = rk
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'; data.value = null; rekap.value = null
  } finally { loading.value = false }
}

async function loadPage(pp: number) {
  page.value = pp; loading.value = true
  try { data.value = await api.get<CollPayload>(`/api/report/collection?${qs()}&page=${page.value}&page_size=${pageSize}`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? e.message : 'Gagal' }
  finally { loading.value = false }
}

async function exportXlsx() {
  exporting.value = true; errorMsg.value = null
  try {
    const now = new Date()
    const ts = `${now.getFullYear()}${p(now.getMonth() + 1)}${p(now.getDate())}-${p(now.getHours())}${p(now.getMinutes())}${p(now.getSeconds())}`
    await api.downloadBlob(`/api/report/collection/export.xlsx?${qs()}`, `penghimpunandana-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally { exporting.value = false }
}

watch([begin, end, branch, fund], () => { data.value = null; rekap.value = null; page.value = 1 })
onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Laporan Penghimpunan Dana</h1>
      <p class="text-sm text-muted">Rekap per dana (saldo awal/mutasi/akhir + donatur) &amp; daftar transaksi penerimaan.</p>
    </div>

    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-if="canPickBranch" value="">Konsolidasi (Semua Cabang)</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Jenis Dana</label>
        <select v-model="fund" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="o in fundOptions" :key="o.v" :value="o.v">{{ o.label }}</option>
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
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="page = 1; load()">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.total" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>

    <template v-else-if="data">
      <div v-if="rekap" class="rounded-xl border border-border bg-surface overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
            <tr>
              <th class="text-left px-3 py-1 font-semibold">Dana</th>
              <th class="text-right px-3 py-1 font-semibold">Saldo Awal</th>
              <th class="text-right px-3 py-1 font-semibold">Mutasi (Penerimaan)</th>
              <th class="text-right px-3 py-1 font-semibold">Saldo Akhir</th>
              <th class="text-right px-3 py-1 font-semibold">Jml Donatur</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="f in rekap.funds" :key="f.fund_label" class="border-b border-border/20">
              <td class="px-3 py-1 font-medium">{{ f.fund_label }}</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ fmt(f.saldo_awal) }}</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ fmt(f.mutasi) }}</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ fmt(f.saldo_akhir) }}</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ f.donors }}</td>
            </tr>
            <tr class="border-t-2 border-primary/40 bg-primary/5 font-bold">
              <td class="px-3 py-1">TOTAL</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ fmt(rekap.grand_total.saldo_awal) }}</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ fmt(rekap.grand_total.mutasi) }}</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ fmt(rekap.grand_total.saldo_akhir) }}</td>
              <td class="px-3 py-1 text-right tabular-nums">{{ rekap.grand_total.donors }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="text-sm text-muted">Detail transaksi — total <span class="font-medium text-foreground">{{ data.total }}</span>, nominal <span class="font-medium text-foreground tabular-nums">{{ fmt(data.total_amount) }}</span></div>
      <div class="rounded-xl border border-border bg-surface overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
            <tr>
              <th class="text-left px-3 py-1 font-semibold whitespace-nowrap">Tanggal</th>
              <th class="text-left px-3 py-1 font-semibold">Dana</th>
              <th class="text-left px-3 py-1 font-semibold">Akun</th>
              <th class="text-left px-3 py-1 font-semibold">Donatur</th>
              <th class="text-left px-3 py-1 font-semibold min-w-[12rem]">Keterangan</th>
              <th class="text-left px-3 py-1 font-semibold">Channel</th>
              <th class="text-left px-3 py-1 font-semibold whitespace-nowrap">No. Transaksi</th>
              <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Nominal</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in data.rows" :key="i" class="border-b border-border/20 hover:bg-muted/5">
              <td class="px-3 py-1 whitespace-nowrap">{{ dmy(r.actualdate) }}</td>
              <td class="px-3 py-1">{{ r.fund_label }}</td>
              <td class="px-3 py-1">{{ r.account_name }}</td>
              <td class="px-3 py-1">{{ r.donorname }}</td>
              <td class="px-3 py-1 whitespace-pre-line">{{ r.description }}</td>
              <td class="px-3 py-1">{{ r.channel }}</td>
              <td class="px-3 py-1 font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.amount) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="totalPages > 1" class="flex items-center justify-center gap-3 text-sm">
        <Button variant="outline" size="sm" :disabled="page <= 1 || loading" @click="loadPage(page - 1)">‹ Sebelumnya</Button>
        <span class="text-muted">Halaman {{ page }} / {{ totalPages }}</span>
        <Button variant="outline" size="sm" :disabled="page >= totalPages || loading" @click="loadPage(page + 1)">Berikutnya ›</Button>
      </div>
    </template>
  </div>
</template>

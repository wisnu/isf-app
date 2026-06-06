<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'

interface Row {
  actualdate: string; accountname: string | null; transactionno: string | null
  description: string | null; amount: number; ekuiv: number; currencycode: string | null
  lpj_label: string; return_transactionno: string | null; inputer: string | null
}
interface Payload { rows: Row[]; total: number; total_amount: number; page: number; page_size: number }
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')
const p = (n: number) => String(n).padStart(2, '0')
const today = new Date()
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = ref(`${today.getFullYear()}-01-01`)
const end = ref(iso(today))
const branch = ref(auth.user?.primary_branch ?? '')
const lpj = ref('')
const branches = ref<BranchOption[]>([])
const page = ref(1)
const pageSize = 50

const lpjOptions = [{ v: '', label: 'Semua Status' }, { v: 'B', label: 'Belum ada LPJ' }, { v: 'S', label: 'Sudah ada LPJ' }]

const data = ref<Payload | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)
const idr = new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))
const totalPages = computed(() => (data.value ? Math.max(1, Math.ceil(data.value.total / pageSize)) : 1))

const qs = () => {
  let s = `begin=${begin.value}&end=${end.value}`
  if (branch.value) s += `&branch=${encodeURIComponent(branch.value)}`
  if (lpj.value) s += `&lpj=${lpj.value}`
  return s
}
async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/cashadvance-list/branches')
    if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code
  } catch { branches.value = [] }
}
async function load() {
  loading.value = true; errorMsg.value = null
  try { data.value = await api.get<Payload>(`/api/report/cashadvance-list?${qs()}&page=${page.value}&page_size=${pageSize}`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'; data.value = null }
  finally { loading.value = false }
}
function goPage(pp: number) { page.value = pp; load() }
async function exportXlsx() {
  exporting.value = true; errorMsg.value = null
  try {
    const n = new Date(); const ts = `${n.getFullYear()}${p(n.getMonth() + 1)}${p(n.getDate())}-${p(n.getHours())}${p(n.getMinutes())}${p(n.getSeconds())}`
    await api.downloadBlob(`/api/report/cashadvance-list/export.xlsx?${qs()}`, `listuangmuka-${ts}.xlsx`)
  } catch (e) { errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal' }
  finally { exporting.value = false }
}
watch([begin, end, branch, lpj], () => { data.value = null; page.value = 1 })
onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">List Transaksi Uang Muka Kegiatan</h1>
      <p class="text-sm text-muted">Daftar pencairan uang muka karyawan + status LPJ.</p>
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
        <label class="text-xs font-medium text-muted">Status LPJ</label>
        <select v-model="lpj" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="o in lpjOptions" :key="o.v" :value="o.v">{{ o.label }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1"><label class="text-xs font-medium text-muted">Tanggal Awal</label><DateField v-model="begin" /></div>
      <div class="flex flex-col gap-1"><label class="text-xs font-medium text-muted">Tanggal Akhir</label><DateField v-model="end" /></div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="goPage(1)"><Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan</Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.total" @click="exportXlsx"><Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />{{ exporting ? 'Mengekspor…' : 'Export Excel' }}</Button>
    </div>
    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>
    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>
    <div v-else-if="data && data.total === 0" class="rounded-xl border border-border bg-surface p-10 text-center text-sm text-muted italic">Tidak ada transaksi untuk filter ini.</div>
    <div v-else-if="data" class="space-y-3">
      <div class="text-sm text-muted">Total transaksi <span class="font-medium text-foreground">{{ data.total }}</span>, nominal <span class="font-medium text-foreground tabular-nums">{{ fmt(data.total_amount) }}</span></div>
      <div class="rounded-xl border border-border bg-surface overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
            <tr>
              <th class="text-left px-3 py-1 font-semibold whitespace-nowrap">Tanggal</th>
              <th class="text-left px-3 py-1 font-semibold">Akun (Karyawan)</th>
              <th class="text-left px-3 py-1 font-semibold whitespace-nowrap">No. Transaksi</th>
              <th class="text-left px-3 py-1 font-semibold min-w-[14rem]">Keterangan</th>
              <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Nominal</th>
              <th class="text-left px-3 py-1 font-semibold">Status LPJ</th>
              <th class="text-left px-3 py-1 font-semibold">Inputer</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in data.rows" :key="i" class="border-b border-border/20 hover:bg-muted/5">
              <td class="px-3 py-1 whitespace-nowrap">{{ dmy(r.actualdate) }}</td>
              <td class="px-3 py-1">{{ r.accountname }}</td>
              <td class="px-3 py-1 font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</td>
              <td class="px-3 py-1 whitespace-pre-line">{{ r.description }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.amount) }}</td>
              <td class="px-3 py-1"><span :class="r.lpj_label === 'Sudah Ada LPJ' ? 'text-emerald-600' : 'text-amber-600'">{{ r.lpj_label }}</span></td>
              <td class="px-3 py-1">{{ r.inputer }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="totalPages > 1" class="flex items-center justify-center gap-3 text-sm">
        <Button variant="outline" size="sm" :disabled="page <= 1 || loading" @click="goPage(page - 1)">‹ Sebelumnya</Button>
        <span class="text-muted">Halaman {{ page }} / {{ totalPages }}</span>
        <Button variant="outline" size="sm" :disabled="page >= totalPages || loading" @click="goPage(page + 1)">Berikutnya ›</Button>
      </div>
    </div>
  </div>
</template>

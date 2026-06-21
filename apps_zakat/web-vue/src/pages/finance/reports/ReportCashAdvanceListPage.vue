<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import Column from 'primevue/column'

import Alert from '@/shared/components/Alert.vue'
import AppDataTable from '@/shared/components/AppDataTable.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
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

const begin = shallowRef(`${today.getFullYear()}-01-01`)
const end = shallowRef(iso(today))
const branch = shallowRef(auth.user?.primary_branch ?? '')
const lpj = shallowRef('')
const branches = ref<BranchOption[]>([])
const page = shallowRef(1)
const pageSize = 50

const lpjOptions = [{ v: '', label: 'Semua Status' }, { v: 'B', label: 'Belum ada LPJ' }, { v: 'S', label: 'Sudah ada LPJ' }]

const data = ref<Payload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
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
    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>
    <div v-else class="space-y-3">
      <div v-if="data" class="text-sm text-muted">Total transaksi <span class="font-medium text-foreground">{{ data.total }}</span>, nominal <span class="font-medium text-foreground tabular-nums">{{ fmt(data.total_amount) }}</span></div>
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div v-if="data && data.total > 0" class="px-4 py-2 border-b border-border flex items-center justify-end">
          <TablePagination
            :page="page"
            :total-pages="totalPages"
            :total="data.total"
            :loading="loading"
            unit="transaksi"
            @prev="goPage(page - 1)"
            @next="goPage(page + 1)"
          />
        </div>
        <AppDataTable :value="data?.rows ?? []" :loading="loading">
          <Column header="Tanggal">
            <template #body="{ data: r }"><span class="whitespace-nowrap tabular-nums">{{ dmy(r.actualdate) }}</span></template>
          </Column>
          <Column field="accountname" header="Akun (Karyawan)" />
          <Column header="No. Transaksi">
            <template #body="{ data: r }"><span class="font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</span></template>
          </Column>
          <Column header="Keterangan" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold min-w-[14rem]' } }">
            <template #body="{ data: r }">
              <span class="max-w-[24rem] truncate block" :title="r.description ?? ''">{{ r.description }}</span>
            </template>
          </Column>
          <Column header="Nominal" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.amount) }}</span></template>
          </Column>
          <Column header="Status LPJ">
            <template #body="{ data: r }">
              <span :class="r.lpj_label === 'Sudah Ada LPJ' ? 'text-emerald-600' : 'text-amber-600'">{{ r.lpj_label }}</span>
            </template>
          </Column>
          <Column field="inputer" header="Inputer" />
          <template #empty>Tidak ada transaksi untuk filter ini.</template>
        </AppDataTable>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import AppDataTable from '@/shared/components/AppDataTable.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/app/stores/auth.store'

interface DistRow {
  actualdate: string; branch_name: string | null; product_name: string | null
  account_name: string | null; description: string | null; ashnaf_label: string
  category_label: string; fund_label: string; channel: string | null; amount: number
  donorname: string | null; transactionno: string | null; inputer: string | null; budget: string
}
interface DistPayload { rows: DistRow[]; total: number; total_amount: number; page: number; page_size: number }
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

const data = ref<DistPayload | null>(null)
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
    branches.value = await api.get<BranchOption[]>('/api/finance/report/distribution/branches')
    if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code
  } catch { branches.value = [] }
}

async function load() {
  loading.value = true; errorMsg.value = null
  try {
    data.value = await api.get<DistPayload>(`/api/report/distribution?${qs()}&page=${page.value}&page_size=${pageSize}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'; data.value = null
  } finally { loading.value = false }
}

function goPage(pp: number) { page.value = pp; load() }

async function exportXlsx() {
  exporting.value = true; errorMsg.value = null
  try {
    const now = new Date()
    const ts = `${now.getFullYear()}${p(now.getMonth() + 1)}${p(now.getDate())}-${p(now.getHours())}${p(now.getMinutes())}${p(now.getSeconds())}`
    await api.downloadBlob(`/api/report/distribution/export.xlsx?${qs()}`, `penyalurandana-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally { exporting.value = false }
}

watch([begin, end, branch, fund], () => { data.value = null; page.value = 1 })
onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Laporan Penyaluran Dana</h1>
      <p class="text-sm text-muted">Daftar transaksi penyaluran per ashnaf/program/dana.</p>
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
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="goPage(1)">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.total" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>

    <template v-else>
      <div v-if="data" class="flex flex-wrap items-center gap-x-6 text-sm">
        <span class="text-muted">Total transaksi: <span class="font-medium text-foreground">{{ data.total }}</span></span>
        <span class="text-muted">Total nominal: <span class="font-medium text-foreground tabular-nums">{{ fmt(data.total_amount) }}</span></span>
      </div>
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
          <template #body="{ data: r }"><span class="whitespace-nowrap">{{ dmy(r.actualdate) }}</span></template>
        </Column>
        <Column field="fund_label" header="Dana" />
        <Column field="ashnaf_label" header="Ashnaf" />
        <Column header="Produk / Akun">
          <template #body="{ data: r }">
            {{ r.product_name }}<span v-if="r.account_name" class="text-muted"> · {{ r.account_name }}</span>
          </template>
        </Column>
        <Column header="Keterangan" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold min-w-[14rem]' } }">
          <template #body="{ data: r }"><span class="whitespace-pre-line">{{ r.description }}</span></template>
        </Column>
        <Column field="donorname" header="Penerima" />
        <Column header="No. Transaksi">
          <template #body="{ data: r }"><span class="font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</span></template>
        </Column>
        <Column header="Nominal" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block text-right tabular-nums whitespace-nowrap">{{ fmt(r.amount) }}</span></template>
        </Column>
        <template #empty>Tidak ada transaksi untuk filter ini.</template>
      </AppDataTable>
    </template>
  </div>
</template>

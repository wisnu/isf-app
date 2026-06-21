<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import Column from 'primevue/column'

import Alert from '@/shared/components/Alert.vue'
import AppDataTable from '@/shared/components/AppDataTable.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/app/stores/auth.store'

interface Row {
  realizationdate: string; memo_number: string | null; type_label: string; description: string | null
  amount: number; report_amount: number; outstanding: number; employee_name: string | null; input_user: string | null
  _isTotal?: true
}
interface Payload { rows: Row[]; grand_total: { amount: number; report_amount: number; outstanding: number }; begin: string; end: string }
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')
const p = (n: number) => String(n).padStart(2, '0')
const today = new Date()
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef(`${today.getFullYear()}-01-01`)
const end = shallowRef(iso(today))
const branch = shallowRef(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])
const data = ref<Payload | null>(null)
const loading = shallowRef(false); const exporting = shallowRef(false); const errorMsg = shallowRef<string | null>(null)
const idr = new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))
const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

const tableRows = computed<Row[]>(() => {
  if (!data.value) return []
  return [
    ...data.value.rows,
    { realizationdate: '', memo_number: null, type_label: 'TOTAL', description: null, _isTotal: true, ...data.value.grand_total, employee_name: null, input_user: null },
  ]
})

async function loadBranches() {
  try { branches.value = await api.get<BranchOption[]>('/api/finance/report/program-realization/branches'); if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code } catch { branches.value = [] }
}
async function load() {
  loading.value = true; errorMsg.value = null
  try { data.value = await api.get<Payload>(`/api/report/program-realization?begin=${begin.value}&end=${end.value}${branchQS()}`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'; data.value = null }
  finally { loading.value = false }
}
async function exportXlsx() {
  exporting.value = true; errorMsg.value = null
  try { const n = new Date(); const ts = `${n.getFullYear()}${p(n.getMonth() + 1)}${p(n.getDate())}-${p(n.getHours())}${p(n.getMinutes())}${p(n.getSeconds())}`
    await api.downloadBlob(`/api/report/program-realization/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`, `piutangrealisasi-${ts}.xlsx`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal' } finally { exporting.value = false }
}
watch([begin, end, branch], () => { data.value = null })
onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Piutang Realisasi Penyaluran</h1>
      <p class="text-sm text-muted">Outstanding = nilai realisasi − yang sudah dilaporkan (LPJ).</p>
    </div>
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-if="canPickBranch" value="">Konsolidasi (Semua Cabang)</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1"><label class="text-xs font-medium text-muted">Tanggal Awal</label><DateField v-model="begin" /></div>
      <div class="flex flex-col gap-1"><label class="text-xs font-medium text-muted">Tanggal Akhir</label><DateField v-model="end" /></div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="load"><Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan</Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.rows.length" @click="exportXlsx"><Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />{{ exporting ? 'Mengekspor…' : 'Export Excel' }}</Button>
    </div>
    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>
    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>
    <AppDataTable v-else :value="tableRows" :loading="loading"
      :row-class="(r: Row) => r._isTotal ? 'border-t-2 border-primary/40 bg-primary/5 font-bold' : ''">
      <Column header="Tanggal">
        <template #body="{ data: r }"><span class="whitespace-nowrap tabular-nums">{{ r._isTotal ? '' : dmy(r.realizationdate) }}</span></template>
      </Column>
      <Column header="No. Memo">
        <template #body="{ data: r }"><span class="font-mono text-[10px] whitespace-nowrap">{{ r.memo_number }}</span></template>
      </Column>
      <Column header="Jenis">
        <template #body="{ data: r }"><span :class="r._isTotal ? 'font-bold' : ''">{{ r.type_label }}</span></template>
      </Column>
      <Column header="Keterangan" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold whitespace-nowrap min-w-[14rem]' } }">
        <template #body="{ data: r }"><span class="whitespace-pre-line">{{ r.description }}</span></template>
      </Column>
      <Column header="Realisasi" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.amount) }}</span></template>
      </Column>
      <Column header="Dilaporkan" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.report_amount) }}</span></template>
      </Column>
      <Column header="Outstanding" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #body="{ data: r }"><span class="block text-right tabular-nums font-medium" :class="r.outstanding > 0 && !r._isTotal ? 'text-amber-600' : ''">{{ fmt(r.outstanding) }}</span></template>
      </Column>
      <Column field="employee_name" header="Karyawan" />
      <template #empty>Tidak ada data untuk filter ini.</template>
    </AppDataTable>
  </div>
</template>

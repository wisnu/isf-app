<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import Column from 'primevue/column'

import Alert from '@/components/ui/Alert.vue'
import AppDataTable from '@/components/ui/AppDataTable.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import Input from '@/components/ui/Input.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/stores/auth'

interface Row {
  memo_date: string; memo_number: string | null; memo_subject: string | null
  memo_amount: number; total_realisasi: number; total_return: number; outstanding: number; realisasi_count: number
}
interface Payload { rows: Row[]; grand_total: { memo_amount: number; total_realisasi: number; total_return: number; outstanding: number }; begin: string; end: string }
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')
const p = (n: number) => String(n).padStart(2, '0')
const today = new Date()
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef(`${today.getFullYear()}-01-01`)
const end = shallowRef(iso(today))
const branch = shallowRef(auth.user?.primary_branch ?? '')
const q = shallowRef('')
const branches = ref<BranchOption[]>([])
const data = ref<Payload | null>(null)
const loading = shallowRef(false); const exporting = shallowRef(false); const errorMsg = shallowRef<string | null>(null)
const idr = new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))
const qs = () => {
  let s = `begin=${begin.value}&end=${end.value}`
  if (branch.value) s += `&branch=${encodeURIComponent(branch.value)}`
  if (q.value) s += `&q=${encodeURIComponent(q.value)}`
  return s
}
async function loadBranches() {
  try { branches.value = await api.get<BranchOption[]>('/api/report/realization-memo/branches'); if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code } catch { branches.value = [] }
}
async function load() {
  loading.value = true; errorMsg.value = null
  try { data.value = await api.get<Payload>(`/api/report/realization-memo?${qs()}`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'; data.value = null }
  finally { loading.value = false }
}
async function exportXlsx() {
  exporting.value = true; errorMsg.value = null
  try { const n = new Date(); const ts = `${n.getFullYear()}${p(n.getMonth() + 1)}${p(n.getDate())}-${p(n.getHours())}${p(n.getMinutes())}${p(n.getSeconds())}`
    await api.downloadBlob(`/api/report/realization-memo/export.xlsx?${qs()}`, `realisasimemo-${ts}.xlsx`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal' } finally { exporting.value = false }
}
watch([begin, end, branch, q], () => { data.value = null })
onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Laporan Realisasi Project (Memo)</h1>
      <p class="text-sm text-muted">Ringkasan realisasi per memo distribusi + outstanding (nilai memo − realisasi).</p>
    </div>
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-if="canPickBranch" value="">Konsolidasi (Semua Cabang)</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1"><label class="text-xs font-medium text-muted">Cari No/Subjek Memo</label><Input v-model="q" placeholder="mis. DPNY / kegiatan" class="h-9 w-56" /></div>
      <div class="flex flex-col gap-1"><label class="text-xs font-medium text-muted">Tanggal Awal</label><DateField v-model="begin" /></div>
      <div class="flex flex-col gap-1"><label class="text-xs font-medium text-muted">Tanggal Akhir</label><DateField v-model="end" /></div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="load"><Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan</Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.rows.length" @click="exportXlsx"><Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />{{ exporting ? 'Mengekspor…' : 'Export Excel' }}</Button>
    </div>
    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>
    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>
    <div v-else class="rounded-xl border border-border bg-surface overflow-hidden">
      <AppDataTable :value="data?.rows ?? []" :loading="loading">
        <Column header="Tanggal">
          <template #body="{ data: r }"><span class="whitespace-nowrap tabular-nums">{{ dmy(r.memo_date) }}</span></template>
        </Column>
        <Column header="No. Memo">
          <template #body="{ data: r }"><span class="font-mono text-[10px] whitespace-nowrap">{{ r.memo_number }}</span></template>
        </Column>
        <Column header="Subjek" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold min-w-[16rem]' } }">
          <template #body="{ data: r }"><span class="max-w-[24rem] truncate block" :title="r.memo_subject ?? ''">{{ r.memo_subject }}</span></template>
        </Column>
        <Column header="Nilai Memo" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.memo_amount) }}</span></template>
        </Column>
        <Column header="Realisasi" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.total_realisasi) }}</span></template>
        </Column>
        <Column header="Pengembalian" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.total_return) }}</span></template>
        </Column>
        <Column header="Outstanding" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block text-right tabular-nums font-medium" :class="r.outstanding > 0 ? 'text-amber-600' : ''">{{ fmt(r.outstanding) }}</span></template>
        </Column>
        <template #empty>Tidak ada memo untuk filter ini.</template>
        <template v-if="data && data.rows.length" #footer>
          <tr class="border-t-2 border-primary/40 bg-primary/5 font-bold text-[11px]">
            <td class="px-3 py-1" colspan="3">TOTAL</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.memo_amount) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.total_realisasi) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.total_return) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.outstanding) }}</td>
          </tr>
        </template>
      </AppDataTable>
    </div>
  </div>
</template>

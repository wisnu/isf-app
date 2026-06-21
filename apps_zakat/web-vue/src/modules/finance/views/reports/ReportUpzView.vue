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

interface Row { journal_date: string; transactionno: string | null; trxtype: string | null; description: string; subaccount: string; debit: number; credit: number }
interface Acc { account_code: string; account_name: string | null; total_debit: number; total_credit: number; net: number; rows: Row[] }
interface Payload { accounts: Acc[]; grand_total: { debit: number; credit: number }; begin: string; end: string; capped: boolean }
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

async function loadBranches() {
  try { branches.value = await api.get<BranchOption[]>('/api/report/upz/branches'); if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code } catch { branches.value = [] }
}
async function load() {
  loading.value = true; errorMsg.value = null
  try { data.value = await api.get<Payload>(`/api/report/upz?begin=${begin.value}&end=${end.value}${branchQS()}`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'; data.value = null }
  finally { loading.value = false }
}
async function exportXlsx() {
  exporting.value = true; errorMsg.value = null
  try { const n = new Date(); const ts = `${n.getFullYear()}${p(n.getMonth() + 1)}${p(n.getDate())}-${p(n.getHours())}${p(n.getMinutes())}${p(n.getSeconds())}`
    await api.downloadBlob(`/api/report/upz/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`, `listupz-${ts}.xlsx`) }
  catch (e) { errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal' } finally { exporting.value = false }
}
watch([begin, end, branch], () => { data.value = null })
onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">List Transaksi UPZ</h1>
      <p class="text-sm text-muted">Transaksi pada akun titipan/penampungan UPZ (210302 / 110109), per akun.</p>
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
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.accounts.length" @click="exportXlsx"><Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />{{ exporting ? 'Mengekspor…' : 'Export Excel' }}</Button>
    </div>
    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>
    <Alert v-if="data && data.capped" variant="default" class="text-xs">Hasil dibatasi 50.000 baris — persempit periode/cabang.</Alert>
    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>
    <div v-else class="space-y-5">
      <div v-for="acc in (data?.accounts ?? [])" :key="acc.account_code" class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="flex flex-wrap items-center gap-x-6 gap-y-1 px-4 py-2 bg-background/40 border-b border-border">
          <span class="font-semibold text-sm">{{ acc.account_code }} — {{ acc.account_name }}</span>
          <span class="text-xs text-muted ml-auto">Debet: <span class="tabular-nums text-foreground">{{ fmt(acc.total_debit) }}</span> · Kredit: <span class="tabular-nums text-foreground">{{ fmt(acc.total_credit) }}</span></span>
        </div>
        <AppDataTable :value="acc.rows" :loading="loading && !data">
          <Column header="Tanggal">
            <template #body="{ data: r }"><span class="whitespace-nowrap tabular-nums">{{ dmy(r.journal_date) }}</span></template>
          </Column>
          <Column header="No. Transaksi">
            <template #body="{ data: r }"><span class="font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</span></template>
          </Column>
          <Column field="trxtype" header="Jenis" />
          <Column header="Keterangan" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold min-w-[16rem]' } }">
            <template #body="{ data: r }">
              <span class="max-w-[24rem] truncate block" :title="(r.description + (r.subaccount ? ' · ' + r.subaccount : ''))">{{ r.description }}<span v-if="r.subaccount" class="text-muted"> · {{ r.subaccount }}</span></span>
            </template>
          </Column>
          <Column header="Debet" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.debit) }}</span></template>
          </Column>
          <Column header="Kredit" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }"><span class="block text-right tabular-nums">{{ fmt(r.credit) }}</span></template>
          </Column>
          <template #empty>Tidak ada transaksi UPZ untuk filter ini.</template>
          <template #footer>
            <tr class="border-t-2 border-border bg-background/30 font-semibold text-[11px]">
              <td class="px-3 py-1" colspan="4">Total</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(acc.total_debit) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(acc.total_credit) }}</td>
            </tr>
          </template>
        </AppDataTable>
      </div>
      <div v-if="loading && !data" class="p-10 text-center">
        <span class="text-sm text-muted italic">Memuat data…</span>
      </div>
    </div>
  </div>
</template>

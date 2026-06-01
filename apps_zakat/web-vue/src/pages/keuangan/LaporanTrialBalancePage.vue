<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface TBRow {
  account_code: string
  account_name: string | null
  branch_code: string | null
  saldo_awal: number
  debit: number
  credit: number
  saldo_akhir: number
}
interface TBSubtotal { saldo_awal: number; debit: number; credit: number; saldo_akhir: number }
interface TBGroup { type: string; type_label: string; rows: TBRow[]; subtotal: TBSubtotal }
interface TBPayload {
  groups: TBGroup[]
  grand_total: TBSubtotal
  begin: string
  end: string
  konsolidasi: boolean
  with_journal: boolean
}
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = ref<string>(`${today.getFullYear()}-01-01`)
const end = ref<string>(iso(today))
// '' = Konsolidasi (hanya untuk user branch_access='all')
const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<TBPayload | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/trial-balance/branches')
    if (!branch.value && branches.value.length && !canPickBranch.value)
      branch.value = branches.value[0].code
  } catch {
    branches.value = []
  }
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<TBPayload>(
      `/api/report/trial-balance?begin=${begin.value}&end=${end.value}${branchQS()}`,
    )
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
    const ts = `${today.getFullYear()}${p(today.getMonth() + 1)}${p(today.getDate())}-${p(new Date().getHours())}${p(new Date().getMinutes())}${p(new Date().getSeconds())}`
    await api.downloadBlob(
      `/api/report/trial-balance/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`,
      `trialbalance-${ts}.xlsx`,
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

watch([begin, end, branch], () => { data.value = null })

// Standar laporan: data di-load saat klik "Tampilkan", bukan saat buka halaman.
onMounted(async () => {
  await loadBranches()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Trial Balance</h1>
      <p class="text-sm text-muted">Neraca saldo per akun detail: saldo awal, mutasi debet/kredit, saldo akhir.</p>
    </div>

    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[16rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-if="canPickBranch" value="">Konsolidasi (Semua Cabang)</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
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
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="load">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.groups.length" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>
    <Alert v-if="data && data.with_journal" variant="default" class="text-xs">
      Periode mencakup tanggal ≥ hari ini — mutasi memakai jurnal harian (dailybalance belum dihitung untuk tanggal tsb).
    </Alert>

    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>
    <div v-else-if="data && data.groups.length === 0" class="rounded-xl border border-border bg-surface p-10 text-center text-sm text-muted italic">Tidak ada data untuk filter ini.</div>

    <div v-else-if="data" class="rounded-xl border border-border bg-surface overflow-x-auto">
      <table class="w-full text-xs">
        <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
          <tr>
            <th class="text-left px-3 py-2 font-semibold">Kode</th>
            <th class="text-left px-3 py-2 font-semibold min-w-[18rem]">Nama Account</th>
            <th v-if="data.konsolidasi" class="text-left px-3 py-2 font-semibold">Cabang</th>
            <th class="text-right px-3 py-2 font-semibold whitespace-nowrap">Saldo Awal</th>
            <th class="text-right px-3 py-2 font-semibold whitespace-nowrap">Debet</th>
            <th class="text-right px-3 py-2 font-semibold whitespace-nowrap">Kredit</th>
            <th class="text-right px-3 py-2 font-semibold whitespace-nowrap">Saldo Akhir</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="grp in data.groups" :key="grp.type">
            <tr class="bg-background/40">
              <td class="px-3 py-1.5 font-semibold" :colspan="data.konsolidasi ? 7 : 6">{{ grp.type_label }}</td>
            </tr>
            <tr v-for="r in grp.rows" :key="grp.type + r.account_code + (r.branch_code ?? '')" class="border-b border-border/30 hover:bg-muted/5">
              <td class="px-3 py-1 font-mono text-[10px] text-muted whitespace-nowrap">{{ r.account_code }}</td>
              <td class="px-3 py-1">{{ r.account_name }}</td>
              <td v-if="data.konsolidasi" class="px-3 py-1 font-mono text-[10px] text-muted">{{ r.branch_code }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.saldo_awal) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.debit) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.credit) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.saldo_akhir) }}</td>
            </tr>
            <tr class="border-y-2 border-border bg-background/30 font-semibold">
              <td class="px-3 py-1.5" :colspan="data.konsolidasi ? 3 : 2">Total {{ grp.type_label }}</td>
              <td class="px-3 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(grp.subtotal.saldo_awal) }}</td>
              <td class="px-3 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(grp.subtotal.debit) }}</td>
              <td class="px-3 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(grp.subtotal.credit) }}</td>
              <td class="px-3 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(grp.subtotal.saldo_akhir) }}</td>
            </tr>
          </template>
          <tr class="border-y-2 border-primary/40 bg-primary/5 font-bold">
            <td class="px-3 py-2" :colspan="data.konsolidasi ? 3 : 2">GRAND TOTAL</td>
            <td class="px-3 py-2 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.saldo_awal) }}</td>
            <td class="px-3 py-2 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.debit) }}</td>
            <td class="px-3 py-2 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.credit) }}</td>
            <td class="px-3 py-2 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.saldo_akhir) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

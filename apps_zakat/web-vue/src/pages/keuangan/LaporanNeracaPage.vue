<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface NeracaRow {
  account_code: string
  account_name: string | null
  account_level: number
  account_type: string
  balance: number
  balance_prev: number
}
interface NeracaPayload {
  aktiva: NeracaRow[]
  pasiva: NeracaRow[]
  total_aktiva: number
  total_aktiva_prev: number
  total_pasiva: number
  total_pasiva_prev: number
  selisih: number
  status_balance: string
  tanggal: string
  tanggal_prev: string
  jenisperiode: string
  konsolidasi: boolean
}
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const tanggal = shallowRef<string>(iso(today))
const jenisperiode = shallowRef<'T' | 'B'>('T')
const level = shallowRef<number>(0) // 0 = semua
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<NeracaPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const levelOptions = [
  { v: 0, label: 'Semua level' },
  { v: 1, label: 'Level 0' },
  { v: 2, label: 's/d Level 1' },
  { v: 3, label: 's/d Level 2' },
  { v: 4, label: 's/d Level 3' },
]

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')
const baseQS = () => `tanggal=${tanggal.value}&jenisperiode=${jenisperiode.value}&level=${level.value}${branchQS()}`

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/neraca/branches')
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
    data.value = await api.get<NeracaPayload>(`/api/report/neraca?${baseQS()}`)
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
    const now = new Date()
    const ts = `${now.getFullYear()}${p(now.getMonth() + 1)}${p(now.getDate())}-${p(now.getHours())}${p(now.getMinutes())}${p(now.getSeconds())}`
    await api.downloadBlob(`/api/report/neraca/export.xlsx?${baseQS()}`, `neraca-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

watch([tanggal, jenisperiode, level, branch], () => { data.value = null })

// Standar laporan: data di-load saat klik "Tampilkan", bukan saat buka halaman.
onMounted(async () => {
  await loadBranches()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Neraca</h1>
      <p class="text-sm text-muted">Posisi aktiva &amp; pasiva (hierarkis) dengan pembanding periode sebelumnya.</p>
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
        <label class="text-xs font-medium text-muted">Per Tanggal</label>
        <DateField v-model="tanggal" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Periode Pembanding</label>
        <select v-model="jenisperiode" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary">
          <option value="T">Tahunan (akhir thn lalu)</option>
          <option value="B">Bulanan (akhir bln lalu)</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Level</label>
        <select v-model.number="level" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-for="o in levelOptions" :key="o.v" :value="o.v">{{ o.label }}</option>
        </select>
      </div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="load">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>

    <div v-else-if="data" class="space-y-3">
      <div class="rounded-xl border bg-surface p-3 flex flex-wrap items-center gap-x-6 gap-y-1 text-sm"
           :class="data.status_balance === 'BALANCE' ? 'border-emerald-500/40' : 'border-red-500/40'">
        <span class="font-semibold" :class="data.status_balance === 'BALANCE' ? 'text-emerald-600' : 'text-red-600'">
          {{ data.status_balance }}
        </span>
        <span class="text-muted">Selisih Aktiva − Pasiva: <span class="tabular-nums font-medium text-foreground">{{ fmt(data.selisih) }}</span></span>
        <span class="text-muted ml-auto text-xs">Per {{ data.tanggal }} · Pembanding {{ data.tanggal_prev }} ({{ data.jenisperiode }})</span>
      </div>

      <div class="rounded-xl border border-border bg-surface overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
            <tr>
              <th class="text-left px-3 py-1 font-semibold min-w-[26rem]">Akun</th>
              <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Nilai per {{ data.tanggal }}</th>
              <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Nilai per {{ data.tanggal_prev }}</th>
            </tr>
          </thead>
          <tbody>
            <tr class="bg-background/40"><td class="px-3 py-1 font-bold" colspan="3">AKTIVA</td></tr>
            <tr v-for="r in data.aktiva" :key="'a' + r.account_code" class="border-b border-border/30 hover:bg-muted/5">
              <td class="px-3 py-1" :style="{ paddingLeft: `${0.75 + r.account_level * 1.25}rem` }">
                <span :class="r.account_level === 0 ? 'font-semibold' : ''">
                  <span class="font-mono text-[10px] text-muted">{{ r.account_code }}</span>
                  <span class="ml-1">{{ r.account_name }}</span>
                </span>
              </td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap" :class="r.account_level === 0 ? 'font-semibold' : ''">{{ fmt(r.balance) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap text-muted">{{ fmt(r.balance_prev) }}</td>
            </tr>
            <tr class="border-y-2 border-border bg-background/30 font-semibold">
              <td class="px-3 py-1">Total Aktiva</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.total_aktiva) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.total_aktiva_prev) }}</td>
            </tr>

            <tr class="bg-background/40"><td class="px-3 py-1 font-bold" colspan="3">PASIVA</td></tr>
            <tr v-for="r in data.pasiva" :key="'p' + r.account_code" class="border-b border-border/30 hover:bg-muted/5">
              <td class="px-3 py-1" :style="{ paddingLeft: `${0.75 + r.account_level * 1.25}rem` }">
                <span :class="r.account_level === 0 ? 'font-semibold' : ''">
                  <span class="font-mono text-[10px] text-muted">{{ r.account_code }}</span>
                  <span class="ml-1">{{ r.account_name }}</span>
                </span>
              </td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap" :class="r.account_level === 0 ? 'font-semibold' : ''">{{ fmt(r.balance) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap text-muted">{{ fmt(r.balance_prev) }}</td>
            </tr>
            <tr class="border-y-2 border-primary/40 bg-primary/5 font-bold">
              <td class="px-3 py-1">Total Pasiva</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.total_pasiva) }}</td>
              <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.total_pasiva_prev) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

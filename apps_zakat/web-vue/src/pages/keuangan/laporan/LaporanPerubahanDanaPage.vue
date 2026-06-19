<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface PDLine { label: string; value: number }
interface PDFund {
  fund: string
  penerimaan: PDLine[]
  penyaluran: PDLine[]
  total_penerimaan: number
  total_penyaluran: number
  surplus: number
  saldo_awal: number
  saldo_akhir: number
}
interface PDPayload { funds: PDFund[]; total_saldo_akhir: number; begin: string; end: string; konsolidasi: boolean }
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef<string>(`${today.getFullYear()}-01-01`)
const end = shallowRef<string>(iso(today))
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<PDPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/perubahan-dana/branches')
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
    data.value = await api.get<PDPayload>(`/api/report/perubahan-dana?begin=${begin.value}&end=${end.value}${branchQS()}`)
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
    await api.downloadBlob(`/api/report/perubahan-dana/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`, `perubahandana-${ts}.xlsx`)
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
      <h1 class="text-2xl font-bold tracking-tight">Laporan Perubahan Dana</h1>
      <p class="text-sm text-muted">Penerimaan, penyaluran, surplus/defisit &amp; saldo per jenis dana (Zakat, Infaq, Non-Halal, Amil).</p>
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
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>

    <div v-else-if="data" class="grid gap-4 md:grid-cols-2">
      <div v-for="f in data.funds" :key="f.fund" class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 bg-background/40 border-b border-border font-semibold text-sm">{{ f.fund }}</div>
        <table class="w-full text-sm">
          <tbody>
            <tr><td class="px-4 py-1 font-semibold text-muted" colspan="2">Penerimaan</td></tr>
            <tr v-for="(ln, i) in f.penerimaan" :key="'r' + i" class="border-b border-border/20">
              <td class="px-4 py-1 pl-7">{{ ln.label }}</td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(ln.value) }}</td>
            </tr>
            <tr class="border-y border-border/40 font-medium bg-background/20">
              <td class="px-4 py-1">Jumlah Penerimaan</td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(f.total_penerimaan) }}</td>
            </tr>
            <tr><td class="px-4 py-1 pt-2 font-semibold text-muted" colspan="2">Penyaluran / Penggunaan</td></tr>
            <tr v-for="(ln, i) in f.penyaluran" :key="'d' + i" class="border-b border-border/20">
              <td class="px-4 py-1 pl-7">{{ ln.label }}</td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(ln.value) }}</td>
            </tr>
            <tr class="border-y border-border/40 font-medium bg-background/20">
              <td class="px-4 py-1">Jumlah Penyaluran/Penggunaan</td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(f.total_penyaluran) }}</td>
            </tr>
            <tr class="font-semibold">
              <td class="px-4 py-1">Surplus (Defisit)</td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap" :class="f.surplus < 0 ? 'text-red-600' : ''">{{ fmt(f.surplus) }}</td>
            </tr>
            <tr class="border-t border-border/30">
              <td class="px-4 py-1">Saldo Awal Dana</td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(f.saldo_awal) }}</td>
            </tr>
            <tr class="border-t-2 border-primary/40 bg-primary/5 font-bold">
              <td class="px-4 py-1.5">Saldo Akhir Dana</td>
              <td class="px-4 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(f.saldo_akhir) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="rounded-xl border border-primary/40 bg-primary/5 p-4 flex items-center justify-between md:col-span-2">
        <span class="font-bold">Total Saldo Akhir Seluruh Dana</span>
        <span class="font-bold tabular-nums text-lg">{{ fmt(data.total_saldo_akhir) }}</span>
      </div>
    </div>
  </div>
</template>

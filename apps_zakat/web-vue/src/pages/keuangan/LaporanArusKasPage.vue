<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface AKLine { label: string; value: number }
interface AKSection { title: string; lines: AKLine[]; subtotal: number }
interface AKPayload {
  sections: AKSection[]
  kenaikan_bersih: number
  saldo_awal: number
  saldo_akhir: number
  begin: string
  end: string
  konsolidasi: boolean
}
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = ref<string>(`${today.getFullYear()}-01-01`)
const end = ref<string>(iso(today))
const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<AKPayload | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/aruskas/branches')
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
    data.value = await api.get<AKPayload>(`/api/report/aruskas?begin=${begin.value}&end=${end.value}${branchQS()}`)
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
    await api.downloadBlob(
      `/api/report/aruskas/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`,
      `aruskas-${ts}.xlsx`,
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
      <h1 class="text-2xl font-bold tracking-tight">Laporan Arus Kas</h1>
      <p class="text-sm text-muted">Aktivitas Operasi, Investasi &amp; Pendanaan + rekonsiliasi saldo kas.</p>
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
        <input v-model="begin" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Akhir</label>
        <input v-model="end" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
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

    <div v-else-if="data" class="rounded-xl border border-border bg-surface overflow-x-auto max-w-3xl">
      <table class="w-full text-sm">
        <tbody>
          <template v-for="sec in data.sections" :key="sec.title">
            <tr class="bg-background/40 border-b border-border">
              <td class="px-4 py-2 font-semibold">{{ sec.title }}</td>
              <td class="px-4 py-2"></td>
            </tr>
            <tr v-for="(ln, i) in sec.lines" :key="sec.title + i" class="border-b border-border/30 hover:bg-muted/5">
              <td class="px-4 py-1 pl-8">{{ ln.label }}</td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap" :class="ln.value < 0 ? 'text-red-600' : ''">{{ fmt(ln.value) }}</td>
            </tr>
            <tr class="border-y border-border bg-background/30 font-semibold">
              <td class="px-4 py-1.5">Jumlah {{ sec.title }}</td>
              <td class="px-4 py-1.5 text-right tabular-nums whitespace-nowrap" :class="sec.subtotal < 0 ? 'text-red-600' : ''">{{ fmt(sec.subtotal) }}</td>
            </tr>
            <tr><td colspan="2" class="py-1"></td></tr>
          </template>

          <tr class="border-t-2 border-border font-semibold">
            <td class="px-4 py-2">Kenaikan (Penurunan) Kas Bersih</td>
            <td class="px-4 py-2 text-right tabular-nums whitespace-nowrap" :class="data.kenaikan_bersih < 0 ? 'text-red-600' : ''">{{ fmt(data.kenaikan_bersih) }}</td>
          </tr>
          <tr class="border-b border-border/30">
            <td class="px-4 py-1">Saldo Kas &amp; Setara Kas Awal Periode</td>
            <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.saldo_awal) }}</td>
          </tr>
          <tr class="border-y-2 border-primary/40 bg-primary/5 font-bold">
            <td class="px-4 py-2">Saldo Kas &amp; Setara Kas Akhir Periode</td>
            <td class="px-4 py-2 text-right tabular-nums whitespace-nowrap">{{ fmt(data.saldo_akhir) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

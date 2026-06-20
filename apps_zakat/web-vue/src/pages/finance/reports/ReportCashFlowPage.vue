<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import AppDataTable from '@/components/ui/AppDataTable.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface AKLine { label: string; value: number }
interface AKSection { title: string; lines: AKLine[]; subtotal: number }
interface AKPayload {
  sections: AKSection[]
  kenaikan_bersih: number
  opening_balance: number
  closing_balance: number
  begin: string
  end: string
  konsolidasi: boolean
}
interface BranchOption { code: string; name: string }

// Sentinel row types untuk flatten
type AKTableRow =
  | { __kind: 'section-header'; title: string }
  | { __kind: 'line'; label: string; value: number }
  | { __kind: 'subtotal'; title: string; subtotal: number }
  | { __kind: 'spacer' }
  | { __kind: 'summary-kenaikan'; value: number }
  | { __kind: 'summary-saldo-awal'; value: number }
  | { __kind: 'summary-saldo-akhir'; value: number }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef<string>(`${today.getFullYear()}-01-01`)
const end = shallowRef<string>(iso(today))
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<AKPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

// Flatten semua baris ke satu array untuk AppDataTable
const tableRows = computed<AKTableRow[]>(() => {
  if (!data.value) return []
  const rows: AKTableRow[] = []
  for (const sec of data.value.sections) {
    rows.push({ __kind: 'section-header', title: sec.title })
    for (const ln of sec.lines)
      rows.push({ __kind: 'line', label: ln.label, value: ln.value })
    rows.push({ __kind: 'subtotal', title: sec.title, subtotal: sec.subtotal })
    rows.push({ __kind: 'spacer' })
  }
  rows.push({ __kind: 'summary-kenaikan', value: data.value.kenaikan_bersih })
  rows.push({ __kind: 'summary-saldo-awal', value: data.value.opening_balance })
  rows.push({ __kind: 'summary-saldo-akhir', value: data.value.closing_balance })
  return rows
})

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/cash-flow/branches')
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
    data.value = await api.get<AKPayload>(`/api/report/cash-flow?begin=${begin.value}&end=${end.value}${branchQS()}`)
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
      `/api/report/cash-flow/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`,
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

    <AppDataTable v-else :value="tableRows" :loading="loading" class="max-w-3xl">
      <template #empty>Tidak ada data untuk filter ini.</template>

      <!-- Kolom label -->
      <Column :pt="{ headerCell: { class: 'px-4 py-1 font-semibold' } }">
        <template #header>&nbsp;</template>
        <template #body="{ data: r }">
          <span v-if="r.__kind === 'section-header'"
                class="block px-4 py-1 font-semibold bg-background/40">{{ r.title }}</span>
          <span v-else-if="r.__kind === 'line'"
                class="block px-4 py-1 pl-8">{{ r.label }}</span>
          <span v-else-if="r.__kind === 'subtotal'"
                class="block px-4 py-1.5 font-semibold bg-background/30">Jumlah {{ r.title }}</span>
          <span v-else-if="r.__kind === 'spacer'" class="block py-1" />
          <span v-else-if="r.__kind === 'summary-kenaikan'"
                class="block px-4 py-1 font-semibold">Kenaikan (Penurunan) Kas Bersih</span>
          <span v-else-if="r.__kind === 'summary-saldo-awal'"
                class="block px-4 py-1">Saldo Kas &amp; Setara Kas Awal Periode</span>
          <span v-else-if="r.__kind === 'summary-saldo-akhir'"
                class="block px-4 py-1 font-bold text-primary">Saldo Kas &amp; Setara Kas Akhir Periode</span>
        </template>
      </Column>

      <!-- Kolom nilai -->
      <Column :pt="{ headerCell: { class: 'text-right px-4 py-1 font-semibold whitespace-nowrap' } }">
        <template #header>Nominal</template>
        <template #body="{ data: r }">
          <span v-if="r.__kind === 'section-header' || r.__kind === 'spacer'" />
          <span v-else-if="r.__kind === 'line'"
                class="block text-right tabular-nums whitespace-nowrap px-4 py-1"
                :class="r.value < 0 ? 'text-red-600' : ''">{{ fmt(r.value) }}</span>
          <span v-else-if="r.__kind === 'subtotal'"
                class="block text-right tabular-nums whitespace-nowrap px-4 py-1.5 font-semibold bg-background/30"
                :class="r.subtotal < 0 ? 'text-red-600' : ''">{{ fmt(r.subtotal) }}</span>
          <span v-else-if="r.__kind === 'summary-kenaikan'"
                class="block text-right tabular-nums whitespace-nowrap px-4 py-1 font-semibold"
                :class="r.value < 0 ? 'text-red-600' : ''">{{ fmt(r.value) }}</span>
          <span v-else-if="r.__kind === 'summary-saldo-awal'"
                class="block text-right tabular-nums whitespace-nowrap px-4 py-1">{{ fmt(r.value) }}</span>
          <span v-else-if="r.__kind === 'summary-saldo-akhir'"
                class="block text-right tabular-nums whitespace-nowrap px-4 py-1 font-bold text-primary">{{ fmt(r.value) }}</span>
        </template>
      </Column>
    </AppDataTable>
  </div>
</template>

<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'

import Alert from '@/shared/components/Alert.vue'
import AppDataTable from '@/shared/components/AppDataTable.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import { api, ApiError } from '@/shared/api/client'
import { useAuthStore } from '@/stores/auth'

interface ARRow {
  accountno: string; accountname: string | null; debtor_description: string | null
  opening_balance: number; debet: number; kredit: number; closing_balance: number
  _isTotal?: boolean
}
interface ARPayload {
  rows: ARRow[]
  grand_total: { opening_balance: number; debet: number; kredit: number; closing_balance: number }
  title: string; with_debtor: boolean; begin: string; end: string
}
interface BranchOption { code: string; name: string }

const route = useRoute()
const endpoint = computed(() => (route.meta.arEndpoint as string) || 'employee-ar')
const fileBase = computed(() => (route.meta.arFile as string) || 'piutang')
const title = computed(() => (route.meta.title as string) || 'Ringkasan Piutang')

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef<string>(`${today.getFullYear()}-01-01`)
const end = shallowRef<string>(iso(today))
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<ARPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const tableRows = computed<ARRow[]>(() => {
  if (!data.value) return []
  return [
    ...data.value.rows,
    { accountno: '', accountname: null, debtor_description: null, _isTotal: true, ...data.value.grand_total },
  ]
})

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))
const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>(`/api/report/${endpoint.value}/branches`)
    if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code
  } catch { branches.value = [] }
}

async function load() {
  loading.value = true; errorMsg.value = null
  try {
    data.value = await api.get<ARPayload>(`/api/report/${endpoint.value}?begin=${begin.value}&end=${end.value}${branchQS()}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'; data.value = null
  } finally { loading.value = false }
}

async function exportXlsx() {
  exporting.value = true; errorMsg.value = null
  try {
    const now = new Date()
    const ts = `${now.getFullYear()}${p(now.getMonth() + 1)}${p(now.getDate())}-${p(now.getHours())}${p(now.getMinutes())}${p(now.getSeconds())}`
    await api.downloadBlob(`/api/report/${endpoint.value}/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`, `${fileBase.value}-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally { exporting.value = false }
}

watch([begin, end, branch, endpoint], () => { data.value = null })
onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">{{ title }}</h1>
      <p class="text-sm text-muted">Saldo awal, movement debet/kredit &amp; saldo akhir per akun.</p>
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
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.rows.length" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>
    <AppDataTable v-else :value="tableRows" :loading="loading"
      :row-class="(r: ARRow) => r._isTotal ? 'border-t-2 border-primary/40 bg-primary/5 font-bold' : ''">
      <Column :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #header>No. Akun</template>
        <template #body="{ data: r }">
          <span v-if="r._isTotal" class="font-bold">TOTAL</span>
          <span v-else class="font-mono text-[10px] whitespace-nowrap">{{ r.accountno }}</span>
        </template>
      </Column>
      <Column header="Nama" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold min-w-[16rem]' } }">
        <template #body="{ data: r }">
          <span v-if="!r._isTotal">{{ r.accountname }}</span>
        </template>
      </Column>
      <Column v-if="data?.with_debtor" header="Keterangan">
        <template #body="{ data: r }">
          <span v-if="!r._isTotal" class="text-muted">{{ r.debtor_description }}</span>
        </template>
      </Column>
      <Column header="Saldo Awal" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #body="{ data: r }"><span class="block text-right tabular-nums whitespace-nowrap">{{ fmt(r.opening_balance) }}</span></template>
      </Column>
      <Column header="Debet" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #body="{ data: r }"><span class="block text-right tabular-nums whitespace-nowrap">{{ fmt(r.debet) }}</span></template>
      </Column>
      <Column header="Kredit" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #body="{ data: r }"><span class="block text-right tabular-nums whitespace-nowrap">{{ fmt(r.kredit) }}</span></template>
      </Column>
      <Column header="Saldo Akhir" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
        <template #body="{ data: r }"><span class="block text-right tabular-nums whitespace-nowrap font-medium">{{ fmt(r.closing_balance) }}</span></template>
      </Column>
      <template #empty>Tidak ada data untuk filter ini.</template>
    </AppDataTable>
  </div>
</template>

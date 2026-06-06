<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface ARRow {
  accountno: string; accountname: string | null; debtor_description: string | null
  saldo_awal: number; debet: number; kredit: number; saldo_akhir: number
}
interface ARPayload {
  rows: ARRow[]
  grand_total: { saldo_awal: number; debet: number; kredit: number; saldo_akhir: number }
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

const begin = ref<string>(`${today.getFullYear()}-01-01`)
const end = ref<string>(iso(today))
const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<ARPayload | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

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
      <p class="text-sm text-muted">Saldo awal, mutasi debet/kredit &amp; saldo akhir per akun.</p>
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

    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>
    <div v-else-if="data && data.rows.length === 0" class="rounded-xl border border-border bg-surface p-10 text-center text-sm text-muted italic">Tidak ada akun untuk filter ini.</div>

    <div v-else-if="data" class="rounded-xl border border-border bg-surface overflow-x-auto">
      <table class="w-full text-[11px]">
        <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50">
          <tr>
            <th class="text-left px-3 py-1 font-semibold">No. Akun</th>
            <th class="text-left px-3 py-1 font-semibold min-w-[16rem]">Nama</th>
            <th v-if="data.with_debtor" class="text-left px-3 py-1 font-semibold">Keterangan</th>
            <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Saldo Awal</th>
            <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Debet</th>
            <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Kredit</th>
            <th class="text-right px-3 py-1 font-semibold whitespace-nowrap">Saldo Akhir</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(r, i) in data.rows" :key="i" class="border-b border-border/20 hover:bg-muted/5">
            <td class="px-3 py-1 font-mono text-[10px] whitespace-nowrap">{{ r.accountno }}</td>
            <td class="px-3 py-1">{{ r.accountname }}</td>
            <td v-if="data.with_debtor" class="px-3 py-1 text-muted">{{ r.debtor_description }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.saldo_awal) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.debet) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.kredit) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap font-medium">{{ fmt(r.saldo_akhir) }}</td>
          </tr>
          <tr class="border-t-2 border-primary/40 bg-primary/5 font-bold">
            <td class="px-3 py-1" :colspan="data.with_debtor ? 3 : 2">TOTAL</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.saldo_awal) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.debet) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.kredit) }}</td>
            <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(data.grand_total.saldo_akhir) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

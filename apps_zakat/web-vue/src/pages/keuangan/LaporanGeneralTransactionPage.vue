<script setup lang="ts">
import {
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  Download,
  Loader2,
  Search,
} from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface GtItem {
  refaccountno: string | null
  refaccountname: string | null
  mutationtype: string | null
  amount: number
  item_description: string | null
  budget_code: string | null
  budget_item_description: string | null
}
interface GtTransaction {
  transactionno: string | null
  transactiondate: string | null
  actualdate: string | null
  description: string | null
  inputer: string | null
  items: GtItem[]
}
interface GtPage {
  transactions: GtTransaction[]
  total: number
  item_total: number
  capped: boolean
  page: number
  page_size: number
}
interface BranchOption {
  code: string
  name: string
}

const auth = useAuthStore()
const canAll = computed(() => auth.user?.branch_access === 'all')

const now = new Date()
const firstOfMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`
const today = now.toISOString().slice(0, 10)
const begin = ref(firstOfMonth)
const end = ref(today)
const branch = ref<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const page = ref(1)
const pageSize = ref(25)
const data = ref<GtPage | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const fmt = (n: number) => (n ? idr.format(n) : '0,00')

const totalPages = computed(() =>
  data.value ? Math.max(1, Math.ceil(data.value.total / data.value.page_size)) : 1,
)

function queryParams(withPaging: boolean): string {
  const p = new URLSearchParams()
  p.set('begin', begin.value)
  p.set('end', end.value)
  if (branch.value) p.set('branch', branch.value)
  if (withPaging) {
    p.set('page', String(page.value))
    p.set('page_size', String(pageSize.value))
  }
  return p.toString()
}

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/general-transaction/branches')
    if (!canAll.value && !branch.value && branches.value.length) {
      branch.value = branches.value[0].code
    }
  } catch {
    branches.value = []
  }
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<GtPage>(`/api/report/general-transaction?${queryParams(true)}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'
    data.value = null
  } finally {
    loading.value = false
  }
}

function search() {
  page.value = 1
  load()
}

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value)
  load()
}

async function exportXlsx() {
  exporting.value = true
  errorMsg.value = null
  try {
    const d = new Date()
    const p = (n: number) => String(n).padStart(2, '0')
    const ts = `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`
    await api.downloadBlob(
      `/api/report/general-transaction/export.xlsx?${queryParams(false)}`,
      `generaltransaction-${ts}.xlsx`,
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

onMounted(async () => {
  await loadBranches()
  await load()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">List Transaksi Umum</h1>
      <p class="text-sm text-muted">Transaksi umum (GT) per cabang &amp; periode (sumber: dwh.v_general_transaction)</p>
    </div>

    <!-- Filter bar -->
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select
          v-model="branch"
          :disabled="!canAll"
          class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 disabled:cursor-not-allowed focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option v-if="canAll" value="ALL">Semua cabang</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Dari Tanggal</label>
        <input v-model="begin" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Sampai Tanggal</label>
        <input v-model="end" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
      </div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="search">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" />
        Tampilkan
      </Button>
      <Button
        variant="outline" size="sm" class="gap-1.5 h-9"
        :disabled="exporting || loading || !data || data.total === 0"
        @click="exportXlsx"
      >
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="data?.capped" class="flex items-center gap-2 text-sm rounded-lg border border-amber-300 bg-amber-50 text-amber-800 px-3 py-2 dark:bg-amber-900/20 dark:text-amber-300">
      <AlertTriangle class="w-4 h-4 shrink-0" />
      Hasil {{ data.item_total.toLocaleString('id-ID') }} baris melebihi batas export (50.000). Persempit rentang tanggal atau pilih satu cabang sebelum export.
    </div>

    <!-- Grouped list -->
    <div v-if="loading && !data" class="flex justify-center p-12">
      <Loader2 class="w-7 h-7 animate-spin text-primary" />
    </div>
    <div v-else-if="data && data.transactions.length === 0" class="rounded-xl border border-border bg-surface p-10 text-center text-sm text-muted italic">
      Tidak ada transaksi untuk filter ini.
    </div>
    <div v-else-if="data" class="space-y-3">
      <div
        v-for="(tx, ti) in data.transactions"
        :key="ti"
        class="rounded-xl border border-border bg-surface overflow-hidden"
      >
        <!-- Transaction header -->
        <div class="flex flex-wrap items-center gap-x-6 gap-y-1 px-4 py-2 bg-background/60 border-b border-border">
          <span class="font-mono text-sm font-semibold">{{ tx.transactionno }}</span>
          <span class="text-xs text-muted">Tgl: <span class="tabular-nums text-foreground">{{ tx.actualdate }}</span></span>
          <span class="text-xs text-muted">Inputer: <span class="text-foreground">{{ tx.inputer || '—' }}</span></span>
          <span class="text-xs text-muted truncate flex-1 min-w-[12rem]" :title="tx.description ?? ''">{{ tx.description }}</span>
        </div>
        <!-- Items -->
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border/60">
            <tr>
              <th class="text-left px-4 py-1.5 font-semibold">Ref Account</th>
              <th class="text-center px-2 py-1.5 font-semibold w-12">D/K</th>
              <th class="text-right px-4 py-1.5 font-semibold w-40">Nominal</th>
              <th class="text-left px-4 py-1.5 font-semibold">Keterangan</th>
              <th class="text-left px-4 py-1.5 font-semibold">Budget</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(it, ii) in tx.items" :key="ii" class="border-b border-border/30 last:border-0">
              <td class="px-4 py-1.5">
                <span class="font-mono text-[11px] text-muted">{{ it.refaccountno }}</span>
                <span class="ml-1">{{ it.refaccountname }}</span>
              </td>
              <td class="px-2 py-1.5 text-center">
                <span :class="['text-[10px] font-semibold px-1.5 py-px rounded', it.mutationtype === 'D' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300']">
                  {{ it.mutationtype }}
                </span>
              </td>
              <td class="px-4 py-1.5 text-right tabular-nums">{{ fmt(it.amount) }}</td>
              <td class="px-4 py-1.5 max-w-[20rem] truncate" :title="it.item_description ?? ''">{{ it.item_description }}</td>
              <td class="px-4 py-1.5 text-[11px] text-muted">
                {{ [it.budget_code, it.budget_item_description].filter(Boolean).join(' - ') || '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="data.total > 0" class="flex items-center justify-between gap-2 flex-wrap px-1">
        <p class="text-[11px] text-muted tabular-nums">
          Hal {{ data.page }} / {{ totalPages }} · {{ data.total.toLocaleString('id-ID') }} transaksi
        </p>
        <div class="flex items-center gap-1">
          <button :disabled="page <= 1 || loading" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background" @click="goto(page - 1)"><ChevronLeft class="w-3.5 h-3.5" /></button>
          <span class="text-[11px] px-2.5 py-0.5 rounded-md bg-background border border-border tabular-nums">{{ page }}</span>
          <button :disabled="page >= totalPages || loading" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background" @click="goto(page + 1)"><ChevronRight class="w-3.5 h-3.5" /></button>
        </div>
      </div>
    </div>
  </div>
</template>

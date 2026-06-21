<script setup lang="ts">
import {
  AlertTriangle,
  Download,
  Search,
} from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import AppDataTable from '@/shared/components/AppDataTable.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/app/stores/auth.store'

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
const begin = shallowRef(firstOfMonth)
const end = shallowRef(today)
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const page = shallowRef(1)
const pageSize = shallowRef(25)
const data = ref<GtPage | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

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

// Standar laporan: data di-load saat klik "Tampilkan", bukan saat buka halaman.
onMounted(async () => {
  await loadBranches()
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
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Sampai Tanggal</label>
        <DateField v-model="end" />
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
    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>
    <div v-else class="space-y-3">
      <div v-if="data && data.total > 0" class="px-1 py-2 border-b border-border flex items-center justify-end">
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="data.total"
          :loading="loading"
          unit="transaksi"
          @prev="goto(page - 1)"
          @next="goto(page + 1)"
        />
      </div>

      <div
        v-for="(tx, ti) in data?.transactions ?? []"
        :key="ti"
        class="rounded-xl border border-border bg-surface overflow-hidden"
      >
        <!-- Transaction header -->
        <div class="flex flex-wrap items-center gap-x-6 gap-y-1 px-4 py-2 bg-background/60 border-b border-border">
          <span class="font-mono text-sm font-semibold">{{ tx.transactionno }}</span>
          <span class="text-xs text-muted">Tgl: <span class="tabular-nums text-foreground">{{ dmy(tx.actualdate) }}</span></span>
          <span class="text-xs text-muted">Inputer: <span class="text-foreground">{{ tx.inputer || '—' }}</span></span>
          <span class="text-xs text-muted truncate flex-1 min-w-[12rem]" :title="tx.description ?? ''">{{ tx.description }}</span>
        </div>
        <!-- Items -->
        <AppDataTable :value="tx.items" :loading="false">
          <Column header="Ref Account">
            <template #body="{ data: it }">
              <span class="font-mono text-[11px] text-muted">{{ it.refaccountno }}</span>
              <span class="ml-1">{{ it.refaccountname }}</span>
            </template>
          </Column>
          <Column header="D/K" :pt="{ headerCell: { class: 'text-center px-2 py-1 font-semibold whitespace-nowrap w-12' } }">
            <template #body="{ data: it }">
              <span class="flex justify-center">
                <span :class="['text-[10px] font-semibold px-1.5 py-px rounded', it.mutationtype === 'D' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300']">
                  {{ it.mutationtype }}
                </span>
              </span>
            </template>
          </Column>
          <Column header="Nominal" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: it }">
              <span class="block text-right tabular-nums">{{ fmt(it.amount) }}</span>
            </template>
          </Column>
          <Column header="Keterangan">
            <template #body="{ data: it }">
              <span class="max-w-[20rem] truncate block" :title="it.item_description ?? ''">{{ it.item_description }}</span>
            </template>
          </Column>
          <Column header="Budget">
            <template #body="{ data: it }">
              <span class="text-muted">{{ [it.budget_code, it.budget_item_description].filter(Boolean).join(' - ') || '—' }}</span>
            </template>
          </Column>
          <template #empty>—</template>
        </AppDataTable>
      </div>

    </div>
  </div>
</template>

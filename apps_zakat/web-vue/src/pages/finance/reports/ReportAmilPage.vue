<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import { useRoute } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import AppDataTable from '@/components/ui/AppDataTable.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/stores/auth'

interface AmilRow {
  actualdate: string
  account_code: string
  account_name: string | null
  description: string | null
  channel: string | null
  amount: number
  referenceno: string | null
  transactionno: string | null
  inputer: string | null
  budgetcode?: string | null
  budgetitemdescription?: string | null
}
interface AmilPayload { rows: AmilRow[]; total: number; total_amount: number; page: number; page_size: number }
interface BranchOption { code: string; name: string }

const route = useRoute()
const kind = computed(() => (route.meta.amilKind as string) || 'in')
const isOut = computed(() => kind.value === 'out')
const endpoint = computed(() => (isOut.value ? 'amil-cashout' : 'amil-cashin'))
const title = computed(() => (isOut.value ? 'Laporan Pengeluaran Amil' : 'Laporan Penerimaan Amil'))
const fileBase = computed(() => (isOut.value ? 'pengeluaranamil' : 'penerimaanamil'))

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef<string>(`${today.getFullYear()}-01-01`)
const end = shallowRef<string>(iso(today))
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])
const page = shallowRef(1)
const pageSize = 50

const data = ref<AmilPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))
const totalPages = computed(() => (data.value ? Math.max(1, Math.ceil(data.value.total / pageSize)) : 1))

const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>(`/api/report/${endpoint.value}/branches`)
    if (!branch.value && branches.value.length && !canPickBranch.value) branch.value = branches.value[0].code
  } catch { branches.value = [] }
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<AmilPayload>(`/api/report/${endpoint.value}?begin=${begin.value}&end=${end.value}${branchQS()}&page=${page.value}&page_size=${pageSize}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'
    data.value = null
  } finally { loading.value = false }
}

function goPage(pp: number) { page.value = pp; load() }

async function exportXlsx() {
  exporting.value = true
  errorMsg.value = null
  try {
    const now = new Date()
    const ts = `${now.getFullYear()}${p(now.getMonth() + 1)}${p(now.getDate())}-${p(now.getHours())}${p(now.getMinutes())}${p(now.getSeconds())}`
    await api.downloadBlob(`/api/report/${endpoint.value}/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`, `${fileBase.value}-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally { exporting.value = false }
}

watch([begin, end, branch], () => { data.value = null; page.value = 1 })

onMounted(async () => { await loadBranches() })
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">{{ title }}</h1>
      <p class="text-sm text-muted">Daftar transaksi {{ isOut ? 'beban/pengeluaran' : 'penerimaan' }} dana amil.</p>
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
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="goPage(1)">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.total" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>

    <div v-else class="space-y-3">
      <div v-if="data" class="flex flex-wrap items-center gap-x-6 text-sm">
        <span class="text-muted">Total transaksi: <span class="font-medium text-foreground">{{ data.total }}</span></span>
        <span class="text-muted">Total nominal: <span class="font-medium text-foreground tabular-nums">{{ fmt(data.total_amount) }}</span></span>
      </div>

      <div v-if="data && data.total > 0" class="px-1 py-2 border-b border-border flex items-center justify-end">
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="data.total"
          :loading="loading"
          unit="transaksi"
          @prev="goPage(page - 1)"
          @next="goPage(page + 1)"
        />
      </div>

      <AppDataTable :value="data?.rows ?? []" :loading="loading">
        <template #empty>Tidak ada transaksi untuk filter ini.</template>

        <Column header="Tanggal" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block px-3 py-1 whitespace-nowrap">{{ dmy(r.actualdate) }}</span></template>
        </Column>

        <Column header="Akun" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold' } }">
          <template #body="{ data: r }">
            <span class="block px-3 py-1">
              <span class="font-mono text-[10px] text-muted">{{ r.account_code }}</span> {{ r.account_name }}
            </span>
          </template>
        </Column>

        <Column header="Keterangan" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold min-w-[16rem]' } }">
          <template #body="{ data: r }"><span class="block px-3 py-1 whitespace-pre-line">{{ r.description }}</span></template>
        </Column>

        <Column header="Channel" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold' } }">
          <template #body="{ data: r }"><span class="block px-3 py-1">{{ r.channel }}</span></template>
        </Column>

        <Column v-if="isOut" header="Anggaran" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold' } }">
          <template #body="{ data: r }">
            <span class="block px-3 py-1 text-muted">{{ [r.budgetcode, r.budgetitemdescription].filter(Boolean).join(' - ') }}</span>
          </template>
        </Column>

        <Column header="No. Transaksi" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block px-3 py-1 font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</span></template>
        </Column>

        <Column header="Nominal" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
          <template #body="{ data: r }"><span class="block text-right tabular-nums px-3 py-1 whitespace-nowrap">{{ fmt(r.amount) }}</span></template>
        </Column>
      </AppDataTable>

    </div>
  </div>
</template>

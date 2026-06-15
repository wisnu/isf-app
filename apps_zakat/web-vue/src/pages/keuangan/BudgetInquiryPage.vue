<script setup lang="ts">
import { ArrowLeft, ChevronRight, Download, Eye, X } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface Period { period_id: number; period_value: number }

interface OwnerSummaryRow {
  owner_id: number
  owner_name: string
  total_budget: number
  total_realization: number
  remaining: number
}

interface SummaryResponse {
  period_id: number
  period_value: number
  rows: OwnerSummaryRow[]
}

interface BudgetDetailRow {
  budget_id: number
  budget_code: string
  item_group: string
  item_name: string
  amount: number
  realization: number
}

interface BudgetListResponse {
  rows: BudgetDetailRow[]
  pagination: { total: number }
}

interface TxRow {
  transaction_item_id: number
  actual_date: string
  transaction_code: string
  transaction_no: string | null
  realization_amount: number
  return_amount: number
  budget_trans_type: string | null
  reference_no: string | null
  inputer: string | null
}

interface TxResponse {
  rows: TxRow[]
  pagination: { total: number }
}

interface SelectOption { value: string; label: string }

// ── State: summary ────────────────────────────────────────────────────────────

const toast = useToast()

const periods = ref<SelectOption[]>([])
const selectedPeriod = ref('')
const selectedPeriodId = shallowRef(0)
const periodsLoading = shallowRef(false)

const summaryRows = ref<OwnerSummaryRow[]>([])
const loading = shallowRef(false)
const hasData = shallowRef(false)
const periodLabel = shallowRef('')

const summary = ref({ total_budget: 0, total_realization: 0, total_remaining: 0 })

function computeSummary(items: OwnerSummaryRow[]) {
  const total_budget = items.reduce((s, r) => s + (r.total_budget || 0), 0)
  const total_realization = items.reduce((s, r) => s + (r.total_realization || 0), 0)
  summary.value = { total_budget, total_realization, total_remaining: total_budget - total_realization }
}

// ── State: drawer ─────────────────────────────────────────────────────────────

type DrawerMode = 'owner' | 'transactions'

const drawerOpen = shallowRef(false)
const drawerMode = shallowRef<DrawerMode>('owner')

// owner detail
const ownerDetailName = shallowRef('')
const ownerDetailRows = ref<BudgetDetailRow[]>([])
const ownerDetailLoading = shallowRef(false)
const ownerDetailOwnerId = shallowRef(0)

// transaction detail
const txBudgetId = shallowRef(0)
const txBudgetCode = shallowRef('')
const txOwnerName = shallowRef('')
const txRows = ref<TxRow[]>([])
const txLoading = shallowRef(false)

// ── Load lookups ──────────────────────────────────────────────────────────────

async function loadPeriods() {
  periodsLoading.value = true
  try {
    const res = await api.get<{ data: Period[] }>('/api/budget/periods')
    periods.value = (res.data ?? []).map((p) => ({
      value: String(p.period_id),
      label: String(p.period_value),
    }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat daftar tahun')
  } finally {
    periodsLoading.value = false
  }
}

// ── Load summary ──────────────────────────────────────────────────────────────

async function tampilkan() {
  if (!selectedPeriod.value) {
    toast.error('Pilih tahun anggaran terlebih dahulu')
    return
  }
  loading.value = true
  hasData.value = false
  try {
    const res = await api.get<SummaryResponse>(`/api/budget/summary?period_id=${selectedPeriod.value}`)
    summaryRows.value = res.rows ?? []
    periodLabel.value = String(res.period_value)
    selectedPeriodId.value = res.period_id
    computeSummary(summaryRows.value)
    hasData.value = true
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat inquiry anggaran')
    summaryRows.value = []
  } finally {
    loading.value = false
  }
}

// ── Drawer: owner detail ──────────────────────────────────────────────────────

async function openOwnerDetail(row: OwnerSummaryRow) {
  ownerDetailName.value = row.owner_name
  ownerDetailOwnerId.value = row.owner_id
  ownerDetailRows.value = []
  drawerMode.value = 'owner'
  drawerOpen.value = true
  ownerDetailLoading.value = true
  try {
    const params = new URLSearchParams({
      owner_id: String(row.owner_id),
      period_id: String(selectedPeriodId.value),
      limit: '200',
    })
    const res = await api.get<BudgetListResponse>(`/api/budget?${params}`)
    ownerDetailRows.value = res.rows ?? []
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat detail anggaran')
  } finally {
    ownerDetailLoading.value = false
  }
}

// ── Drawer: transactions ──────────────────────────────────────────────────────

async function openTransactions(row: BudgetDetailRow) {
  txBudgetId.value = row.budget_id
  txBudgetCode.value = row.budget_code
  txOwnerName.value = ownerDetailName.value
  txRows.value = []
  drawerMode.value = 'transactions'
  txLoading.value = true
  try {
    const res = await api.get<TxResponse>(`/api/budget/${row.budget_id}/transactions?limit=100`)
    txRows.value = res.rows ?? []
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat transaksi')
  } finally {
    txLoading.value = false
  }
}

function backToOwnerDetail() {
  drawerMode.value = 'owner'
}

function closeDrawer() {
  drawerOpen.value = false
}

onMounted(loadPeriods)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Inquiry Anggaran" subtitle="Ringkasan anggaran per pemilik berdasarkan tahun" />

    <!-- Filter card -->
    <Card>
      <CardContent class="p-5">
        <div class="flex flex-wrap items-end gap-4">
          <div class="w-48">
            <label class="mb-1.5 block text-sm font-medium">
              Tahun <span class="text-red-500">*</span>
            </label>
            <SearchSelect
              v-model="selectedPeriod"
              :options="periods"
              :loading="periodsLoading"
              placeholder="Pilih tahun..."
            />
          </div>
          <div class="flex gap-2">
            <Button :loading="loading" @click="tampilkan">Tampilkan</Button>
            <Button variant="outline" :disabled="!hasData">
              <Download class="w-3.5 h-3.5 mr-1" />
              Export Excel
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Empty state -->
    <div v-if="!hasData && !loading" class="flex items-center justify-center h-48 text-muted-foreground text-sm">
      Pilih tahun anggaran, lalu klik "Tampilkan" untuk melihat laporan
    </div>

    <!-- Results -->
    <template v-if="hasData">
      <!-- Summary totals -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Card>
          <CardContent class="p-4">
            <p class="text-xs uppercase tracking-wide text-muted">Total Anggaran {{ periodLabel }}</p>
            <p class="text-2xl font-bold tabular-nums text-primary mt-1">{{ formatIdr(summary.total_budget) }}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="p-4">
            <p class="text-xs uppercase tracking-wide text-muted">Total Realisasi</p>
            <p class="text-2xl font-bold tabular-nums text-accent mt-1">{{ formatIdr(summary.total_realization) }}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="p-4">
            <p class="text-xs uppercase tracking-wide text-muted">Sisa Anggaran</p>
            <p
              class="text-2xl font-bold tabular-nums mt-1"
              :class="summary.total_remaining >= 0 ? 'text-positive' : 'text-red-600'"
            >
              {{ formatIdr(summary.total_remaining) }}
            </p>
          </CardContent>
        </Card>
      </div>

      <!-- Summary table -->
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 border-b border-border">
          <span class="text-[11px] text-muted tabular-nums">{{ summaryRows.length }} pemilik anggaran</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-[11px]">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
              <tr>
                <th class="px-4 py-2 text-center font-medium w-10">No</th>
                <th class="px-4 py-2 text-left font-medium">Pemilik Anggaran</th>
                <th class="px-4 py-2 text-right font-medium">Anggaran</th>
                <th class="px-4 py-2 text-right font-medium">Realisasi</th>
                <th class="px-4 py-2 text-right font-medium">Sisa</th>
                <th class="px-4 py-2 text-right font-medium w-24">% Realisasi</th>
                <th class="px-4 py-2 text-center font-medium w-16">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-if="loading">
                <td colspan="7" class="px-4 py-8 text-center text-muted">Memuat...</td>
              </tr>
              <tr v-else-if="summaryRows.length === 0">
                <td colspan="7" class="px-4 py-8 text-center text-muted italic">Tidak ada data untuk tahun ini.</td>
              </tr>
              <tr v-for="(row, idx) in summaryRows" :key="row.owner_id" class="hover:bg-muted/30">
                <td class="px-4 py-1.5 text-center text-xs text-muted">{{ idx + 1 }}</td>
                <td class="px-4 py-1.5 text-xs font-medium">{{ row.owner_name }}</td>
                <td class="px-4 py-1.5 text-right text-xs tabular-nums">{{ formatIdr(row.total_budget) }}</td>
                <td class="px-4 py-1.5 text-right text-xs tabular-nums">{{ formatIdr(row.total_realization) }}</td>
                <td
                  class="px-4 py-1.5 text-right text-xs tabular-nums font-medium"
                  :class="row.remaining >= 0 ? '' : 'text-red-600'"
                >
                  {{ formatIdr(row.remaining) }}
                </td>
                <td class="px-4 py-1.5 text-right text-xs tabular-nums text-muted">
                  {{ row.total_budget > 0 ? ((row.total_realization / row.total_budget) * 100).toFixed(1) + '%' : '—' }}
                </td>
                <td class="px-4 py-1.5 text-center">
                  <Tooltip side="top">
                    <template #trigger>
                      <button
                        class="p-1 rounded hover:bg-muted/50 text-muted hover:text-foreground transition-colors"
                        @click="openOwnerDetail(row)"
                      >
                        <Eye class="w-3.5 h-3.5" />
                      </button>
                    </template>
                    Lihat Detail
                  </Tooltip>
                </td>
              </tr>
            </tbody>
            <tfoot v-if="summaryRows.length > 0" class="border-t-2 border-border bg-muted/20">
              <tr class="font-semibold">
                <td colspan="2" class="px-4 py-2 text-xs">Total</td>
                <td class="px-4 py-2 text-right text-xs tabular-nums">{{ formatIdr(summary.total_budget) }}</td>
                <td class="px-4 py-2 text-right text-xs tabular-nums">{{ formatIdr(summary.total_realization) }}</td>
                <td
                  class="px-4 py-2 text-right text-xs tabular-nums"
                  :class="summary.total_remaining >= 0 ? '' : 'text-red-600'"
                >
                  {{ formatIdr(summary.total_remaining) }}
                </td>
                <td class="px-4 py-2 text-right text-xs tabular-nums text-muted">
                  {{ summary.total_budget > 0 ? ((summary.total_realization / summary.total_budget) * 100).toFixed(1) + '%' : '—' }}
                </td>
                <td />
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </template>

    <!-- ── Drawer ─────────────────────────────────────────────────────────── -->
    <Teleport to="body">
      <Transition name="drawer">
        <div v-if="drawerOpen" class="fixed inset-0 z-50 flex justify-end">
          <!-- Backdrop -->
          <div class="absolute inset-0 bg-black/40" @click="closeDrawer" />

          <!-- Panel -->
          <div class="relative z-10 flex flex-col w-full max-w-2xl bg-surface shadow-2xl h-full overflow-hidden">

            <!-- ── Owner detail view ──────────────────────────────────── -->
            <template v-if="drawerMode === 'owner'">
              <div class="flex items-center justify-between px-5 py-4 border-b border-border">
                <div>
                  <p class="text-xs text-muted uppercase tracking-wide">Detail Anggaran</p>
                  <h3 class="font-semibold text-sm leading-tight mt-0.5">{{ ownerDetailName }}</h3>
                  <p class="text-xs text-muted mt-0.5">Tahun {{ periodLabel }}</p>
                </div>
                <button class="p-1.5 rounded hover:bg-muted/50 text-muted" @click="closeDrawer">
                  <X class="w-4 h-4" />
                </button>
              </div>

              <div class="flex-1 overflow-auto">
                <div v-if="ownerDetailLoading" class="flex items-center justify-center h-48 text-muted text-sm">
                  Memuat...
                </div>
                <table v-else class="w-full text-[11px]">
                  <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border sticky top-0 bg-surface">
                    <tr>
                      <th class="px-4 py-2 text-left font-medium">Kode</th>
                      <th class="px-4 py-2 text-left font-medium">Kelompok</th>
                      <th class="px-4 py-2 text-left font-medium">Rincian</th>
                      <th class="px-4 py-2 text-right font-medium">Anggaran</th>
                      <th class="px-4 py-2 text-right font-medium">Realisasi</th>
                      <th class="px-4 py-2 text-right font-medium">Sisa</th>
                      <th class="px-4 py-2 text-center font-medium w-14">Transaksi</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-border">
                    <tr v-if="ownerDetailRows.length === 0">
                      <td colspan="7" class="px-4 py-8 text-center text-muted italic">Tidak ada data.</td>
                    </tr>
                    <tr
                      v-for="row in ownerDetailRows"
                      :key="row.budget_id"
                      class="hover:bg-muted/30"
                    >
                      <td class="px-4 py-1.5 font-mono text-xs">{{ row.budget_code }}</td>
                      <td class="px-4 py-1.5 text-xs">{{ row.item_group }}</td>
                      <td class="px-4 py-1.5 text-xs">{{ row.item_name }}</td>
                      <td class="px-4 py-1.5 text-right text-xs tabular-nums">{{ formatIdr(row.amount) }}</td>
                      <td class="px-4 py-1.5 text-right text-xs tabular-nums">
                        {{ row.realization ? formatIdr(row.realization) : '—' }}
                      </td>
                      <td
                        class="px-4 py-1.5 text-right text-xs tabular-nums"
                        :class="(row.amount - row.realization) < 0 ? 'text-red-600' : ''"
                      >
                        {{ formatIdr(row.amount - row.realization) }}
                      </td>
                      <td class="px-4 py-1.5 text-center">
                        <Tooltip side="top">
                          <template #trigger>
                            <button
                              class="p-1 rounded hover:bg-muted/50 text-muted hover:text-foreground transition-colors"
                              @click="openTransactions(row)"
                            >
                              <ChevronRight class="w-3.5 h-3.5" />
                            </button>
                          </template>
                          Lihat Transaksi
                        </Tooltip>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </template>

            <!-- ── Transaction detail view ────────────────────────────── -->
            <template v-else-if="drawerMode === 'transactions'">
              <div class="flex items-center justify-between px-5 py-4 border-b border-border">
                <div class="flex items-center gap-3">
                  <button
                    class="p-1.5 rounded hover:bg-muted/50 text-muted"
                    @click="backToOwnerDetail"
                  >
                    <ArrowLeft class="w-4 h-4" />
                  </button>
                  <div>
                    <p class="text-xs text-muted uppercase tracking-wide">Riwayat Transaksi</p>
                    <h3 class="font-semibold text-sm leading-tight mt-0.5">
                      {{ txOwnerName }} — <span class="font-mono">{{ txBudgetCode }}</span>
                    </h3>
                    <p class="text-xs text-muted mt-0.5">Tahun {{ periodLabel }}</p>
                  </div>
                </div>
                <button class="p-1.5 rounded hover:bg-muted/50 text-muted" @click="closeDrawer">
                  <X class="w-4 h-4" />
                </button>
              </div>

              <div class="flex-1 overflow-auto">
                <div v-if="txLoading" class="flex items-center justify-center h-48 text-muted text-sm">
                  Memuat...
                </div>
                <table v-else class="w-full text-[11px]">
                  <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border sticky top-0 bg-surface">
                    <tr>
                      <th class="px-4 py-2 text-left font-medium">Tanggal</th>
                      <th class="px-4 py-2 text-left font-medium">Kode Transaksi</th>
                      <th class="px-4 py-2 text-left font-medium">No Transaksi</th>
                      <th class="px-4 py-2 text-right font-medium">Realisasi</th>
                      <th class="px-4 py-2 text-right font-medium">Pengembalian</th>
                      <th class="px-4 py-2 text-left font-medium">Inputer</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-border">
                    <tr v-if="txRows.length === 0">
                      <td colspan="6" class="px-4 py-8 text-center text-muted italic">
                        Belum ada transaksi untuk kode anggaran ini.
                      </td>
                    </tr>
                    <tr
                      v-for="row in txRows"
                      :key="row.transaction_item_id"
                      class="hover:bg-muted/30"
                    >
                      <td class="px-4 py-1.5 text-xs tabular-nums">{{ dmy(row.actual_date) }}</td>
                      <td class="px-4 py-1.5 font-mono text-xs">{{ row.transaction_code }}</td>
                      <td class="px-4 py-1.5 text-xs">{{ row.transaction_no ?? '—' }}</td>
                      <td class="px-4 py-1.5 text-right text-xs tabular-nums">
                        {{ row.realization_amount ? formatIdr(row.realization_amount) : '—' }}
                      </td>
                      <td class="px-4 py-1.5 text-right text-xs tabular-nums text-muted">
                        {{ row.return_amount ? formatIdr(row.return_amount) : '—' }}
                      </td>
                      <td class="px-4 py-1.5 text-xs text-muted">{{ row.inputer ?? '—' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </template>

          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.2s ease;
}
.drawer-enter-active .relative,
.drawer-leave-active .relative {
  transition: transform 0.25s ease;
}
.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}
</style>

<script setup lang="ts">
import { Download, Eye } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

const CACHE_KEY = 'budget-inquiry-state'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'
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

interface SelectOption { value: string; label: string }

// ── State ─────────────────────────────────────────────────────────────────────

const router = useRouter()
const toast = useToast()

const periods = ref<SelectOption[]>([])
const selectedPeriod = ref('')
const selectedPeriodId = shallowRef(0)
const selectedPeriodValue = shallowRef(0)
const periodsLoading = shallowRef(false)

const rows = ref<OwnerSummaryRow[]>([])
const loading = shallowRef(false)
const hasData = shallowRef(false)

const summary = ref({ total_budget: 0, total_realization: 0, total_remaining: 0 })

function computeSummary(items: OwnerSummaryRow[]) {
  const total_budget = items.reduce((s, r) => s + (r.total_budget || 0), 0)
  const total_realization = items.reduce((s, r) => s + (r.total_realization || 0), 0)
  summary.value = { total_budget, total_realization, total_remaining: total_budget - total_realization }
}

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
    rows.value = res.rows ?? []
    selectedPeriodId.value = res.period_id
    selectedPeriodValue.value = res.period_value
    computeSummary(rows.value)
    hasData.value = true
    sessionStorage.setItem(CACHE_KEY, JSON.stringify({
      selectedPeriod: selectedPeriod.value,
      periodId: res.period_id,
      periodValue: res.period_value,
      rows: res.rows,
    }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat inquiry anggaran')
    rows.value = []
  } finally {
    loading.value = false
  }
}

// ── Navigation ────────────────────────────────────────────────────────────────

function goToDetail(row: OwnerSummaryRow) {
  router.push({
    name: 'keuangan-anggaran-inquiry-owner',
    params: { owner_id: row.owner_id },
    query: {
      period_id: selectedPeriodId.value,
      owner_name: row.owner_name,
      period_value: selectedPeriodValue.value,
    },
  })
}

onMounted(async () => {
  await loadPeriods()
  const cached = sessionStorage.getItem(CACHE_KEY)
  if (cached) {
    try {
      const s = JSON.parse(cached)
      selectedPeriod.value = s.selectedPeriod
      selectedPeriodId.value = s.periodId
      selectedPeriodValue.value = s.periodValue
      rows.value = s.rows ?? []
      computeSummary(rows.value)
      hasData.value = true
    } catch {
      sessionStorage.removeItem(CACHE_KEY)
    }
  }
})
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
      <!-- Summary cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Card>
          <CardContent class="p-4">
            <p class="text-xs uppercase tracking-wide text-muted">Total Anggaran {{ selectedPeriodValue }}</p>
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

      <!-- Table -->
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 border-b border-border">
          <span class="text-[11px] text-muted tabular-nums">{{ rows.length }} pemilik anggaran</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
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
              <tr v-else-if="rows.length === 0">
                <td colspan="7" class="px-4 py-8 text-center text-muted italic">Tidak ada data untuk tahun ini.</td>
              </tr>
              <tr v-for="(row, idx) in rows" :key="row.owner_id" class="hover:bg-muted/30">
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
                        @click="goToDetail(row)"
                      >
                        <Eye class="w-3.5 h-3.5" />
                      </button>
                    </template>
                    Lihat Detail
                  </Tooltip>
                </td>
              </tr>
            </tbody>
            <tfoot v-if="rows.length > 0" class="border-t-2 border-border bg-muted/20">
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
  </div>
</template>

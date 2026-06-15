<script setup lang="ts">
import { ChevronRight } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'
import { formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BudgetDetailRow {
  budget_id: number
  budget_code: string
  item_group: string
  item_name: string
  amount: number
  realization: number
  owner_name: string
  period_value: number
}

interface BudgetListResponse {
  rows: BudgetDetailRow[]
  pagination: { total: number }
}

// ── Route params ──────────────────────────────────────────────────────────────

const route = useRoute()
const router = useRouter()
const toast = useToast()

const ownerId = Number(route.params.owner_id)
const periodId = Number(route.query.period_id)
const ownerName = String(route.query.owner_name ?? '')
const periodLabel = String(route.query.period_value ?? '')

// ── State ─────────────────────────────────────────────────────────────────────

const rows = ref<BudgetDetailRow[]>([])
const loading = shallowRef(false)

const summary = ref({ total_budget: 0, total_realization: 0, total_remaining: 0 })

function computeSummary(items: BudgetDetailRow[]) {
  const total_budget = items.reduce((s, r) => s + (r.amount || 0), 0)
  const total_realization = items.reduce((s, r) => s + (r.realization || 0), 0)
  summary.value = { total_budget, total_realization, total_remaining: total_budget - total_realization }
}

// ── Load data ─────────────────────────────────────────────────────────────────

async function loadData() {
  loading.value = true
  try {
    const params = new URLSearchParams({
      owner_id: String(ownerId),
      period_id: String(periodId),
      limit: '200',
    })
    const res = await api.get<BudgetListResponse>(`/api/budget?${params}`)
    rows.value = res.rows ?? []
    computeSummary(rows.value)
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat detail anggaran')
  } finally {
    loading.value = false
  }
}

function goToTransaksi(row: BudgetDetailRow) {
  router.push({
    name: 'keuangan-anggaran-inquiry-transaksi',
    params: { budget_id: row.budget_id },
    query: {
      budget_code: row.budget_code,
      owner_name: ownerName,
      period_value: periodLabel,
    },
  })
}

onMounted(loadData)
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center gap-3">
      <Button variant="outline" size="sm" @click="router.back()">← Kembali</Button>
      <PageHeader
        :title="ownerName || 'Detail Anggaran'"
        :subtitle="`Rincian anggaran tahun ${periodLabel}`"
      />
    </div>

    <!-- Summary totals -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <div class="rounded-xl border border-border bg-surface p-4">
        <p class="text-xs uppercase tracking-wide text-muted">Total Anggaran</p>
        <p class="text-2xl font-bold tabular-nums text-primary mt-1">{{ formatIdr(summary.total_budget) }}</p>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <p class="text-xs uppercase tracking-wide text-muted">Total Realisasi</p>
        <p class="text-2xl font-bold tabular-nums text-accent mt-1">{{ formatIdr(summary.total_realization) }}</p>
      </div>
      <div class="rounded-xl border border-border bg-surface p-4">
        <p class="text-xs uppercase tracking-wide text-muted">Sisa Anggaran</p>
        <p
          class="text-2xl font-bold tabular-nums mt-1"
          :class="summary.total_remaining >= 0 ? 'text-positive' : 'text-red-600'"
        >
          {{ formatIdr(summary.total_remaining) }}
        </p>
      </div>
    </div>

    <!-- Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <div class="px-4 py-2 border-b border-border">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else>{{ rows.length }} item anggaran</template>
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 text-center font-medium w-10">No</th>
              <th class="px-4 py-2 text-left font-medium">Kode</th>
              <th class="px-4 py-2 text-left font-medium">Kelompok Kegiatan</th>
              <th class="px-4 py-2 text-left font-medium">Rincian Kebutuhan</th>
              <th class="px-4 py-2 text-right font-medium">Anggaran</th>
              <th class="px-4 py-2 text-right font-medium">Realisasi</th>
              <th class="px-4 py-2 text-right font-medium">Sisa</th>
              <th class="px-4 py-2 text-center font-medium w-16">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="8" class="px-4 py-8 text-center text-muted">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="8" class="px-4 py-8 text-center text-muted italic">Tidak ada data anggaran.</td>
            </tr>
            <tr v-for="(row, idx) in rows" :key="row.budget_id" class="hover:bg-muted/30">
              <td class="px-4 py-1.5 text-center text-xs text-muted">{{ idx + 1 }}</td>
              <td class="px-4 py-1.5 font-mono text-xs">{{ row.budget_code }}</td>
              <td class="px-4 py-1.5 text-xs">{{ row.item_group }}</td>
              <td class="px-4 py-1.5 text-xs">{{ row.item_name }}</td>
              <td class="px-4 py-1.5 text-right text-xs tabular-nums">{{ formatIdr(row.amount) }}</td>
              <td class="px-4 py-1.5 text-right text-xs tabular-nums">
                {{ row.realization ? formatIdr(row.realization) : '—' }}
              </td>
              <td
                class="px-4 py-1.5 text-right text-xs tabular-nums font-medium"
                :class="(row.amount - row.realization) < 0 ? 'text-red-600' : ''"
              >
                {{ formatIdr(row.amount - row.realization) }}
              </td>
              <td class="px-4 py-1.5 text-center">
                <Tooltip side="top">
                  <template #trigger>
                    <button
                      class="p-1 rounded hover:bg-muted/50 text-muted hover:text-foreground transition-colors"
                      @click="goToTransaksi(row)"
                    >
                      <ChevronRight class="w-3.5 h-3.5" />
                    </button>
                  </template>
                  Lihat Transaksi
                </Tooltip>
              </td>
            </tr>
          </tbody>
          <tfoot v-if="rows.length > 0" class="border-t-2 border-border bg-muted/20">
            <tr class="font-semibold">
              <td colspan="4" class="px-4 py-2 text-xs">Total</td>
              <td class="px-4 py-2 text-right text-xs tabular-nums">{{ formatIdr(summary.total_budget) }}</td>
              <td class="px-4 py-2 text-right text-xs tabular-nums">{{ formatIdr(summary.total_realization) }}</td>
              <td
                class="px-4 py-2 text-right text-xs tabular-nums"
                :class="summary.total_remaining >= 0 ? '' : 'text-red-600'"
              >
                {{ formatIdr(summary.total_remaining) }}
              </td>
              <td />
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  </div>
</template>

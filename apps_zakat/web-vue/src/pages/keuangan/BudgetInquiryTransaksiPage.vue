<script setup lang="ts">
import { onMounted, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

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

// ── Route params ──────────────────────────────────────────────────────────────

const route = useRoute()
const router = useRouter()
const toast = useToast()

const budgetId = Number(route.params.budget_id)
const budgetCode = String(route.query.budget_code ?? '')
const ownerName = String(route.query.owner_name ?? '')
const periodLabel = String(route.query.period_value ?? '')

// ── State ─────────────────────────────────────────────────────────────────────

const rows = ref<TxRow[]>([])
const loading = shallowRef(false)

// ── Load ──────────────────────────────────────────────────────────────────────

async function loadData() {
  loading.value = true
  try {
    const res = await api.get<TxResponse>(`/api/budget/${budgetId}/transactions?limit=100`)
    rows.value = res.rows ?? []
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat transaksi')
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center gap-3">
      <Button variant="outline" size="sm" @click="router.back()">← Kembali</Button>
      <PageHeader
        :title="`Transaksi — ${budgetCode}`"
        :subtitle="`${ownerName} · Tahun ${periodLabel}`"
      />
    </div>

    <!-- Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <div class="px-4 py-2 border-b border-border">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else>{{ rows.length }} transaksi</template>
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 text-center font-medium w-10">No</th>
              <th class="px-4 py-2 text-left font-medium">Tanggal</th>
              <th class="px-4 py-2 text-left font-medium">Kode Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">No Transaksi</th>
              <th class="px-4 py-2 text-right font-medium">Realisasi</th>
              <th class="px-4 py-2 text-right font-medium">Pengembalian</th>
              <th class="px-4 py-2 text-left font-medium">Referensi</th>
              <th class="px-4 py-2 text-left font-medium">Inputer</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="8" class="px-4 py-8 text-center text-muted">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="8" class="px-4 py-8 text-center text-muted italic">
                Belum ada transaksi untuk kode anggaran ini.
              </td>
            </tr>
            <tr v-for="(row, idx) in rows" :key="row.transaction_item_id" class="hover:bg-muted/30">
              <td class="px-4 py-1.5 text-center text-xs text-muted">{{ idx + 1 }}</td>
              <td class="px-4 py-1.5 text-xs tabular-nums">{{ dmy(row.actual_date) }}</td>
              <td class="px-4 py-1.5 font-mono text-xs">{{ row.transaction_code }}</td>
              <td class="px-4 py-1.5 text-xs">{{ row.transaction_no ?? '—' }}</td>
              <td class="px-4 py-1.5 text-right text-xs tabular-nums font-medium">
                {{ row.realization_amount ? formatIdr(row.realization_amount) : '—' }}
              </td>
              <td class="px-4 py-1.5 text-right text-xs tabular-nums text-muted">
                {{ row.return_amount ? formatIdr(row.return_amount) : '—' }}
              </td>
              <td class="px-4 py-1.5 text-xs text-muted">{{ row.reference_no ?? '—' }}</td>
              <td class="px-4 py-1.5 text-xs text-muted">{{ row.inputer ?? '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import DateField from '@/shared/components/DateField.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { formatIdr } from '@/shared/utils/format'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface TxRow {
  transaction_item_id: number
  actual_date: string
  transaction_code: string
  transaction_type_name: string | null
  transaction_no: string | null
  realization_amount: number
  return_amount: number
  budget_trans_type: string | null
  reference_no: string | null
  description: string | null
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
const periodValue = String(route.query.period_value ?? '')
const itemGroup = String(route.query.item_group ?? '')
const itemName = String(route.query.item_name ?? '')

// Default filter: 1 Jan tahun anggaran → hari ini
const year = periodValue || String(new Date().getFullYear())
const defaultBegin = `${year}-01-01`
const defaultEnd = new Date().toISOString().slice(0, 10)

// ── State ─────────────────────────────────────────────────────────────────────

const beginDate = ref(defaultBegin)
const endDate = ref(defaultEnd)
const rows = ref<TxRow[]>([])
const loading = shallowRef(false)
const hasData = shallowRef(false)

const totals = ref({ realization: 0, return: 0, saldo: 0 })

function computeTotals(items: TxRow[]) {
  const r = items.reduce((s, r) => s + (r.realization_amount || 0), 0)
  const p = items.reduce((s, r) => s + (r.return_amount || 0), 0)
  totals.value = { realization: r, return: p, saldo: r - p }
}

// ── Load ──────────────────────────────────────────────────────────────────────

async function tampilkan() {
  loading.value = true
  hasData.value = false
  try {
    const params = new URLSearchParams({ limit: '500' })
    if (beginDate.value) params.set('begin_date', beginDate.value)
    if (endDate.value) params.set('end_date', endDate.value)
    const res = await api.get<TxResponse>(`/api/finance/budget/${budgetId}/transactions?${params}`)
    rows.value = res.rows ?? []
    computeTotals(rows.value)
    hasData.value = true
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat transaksi')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header nav -->
    <div class="flex items-center gap-3">
      <Button variant="outline" size="sm" @click="router.back()">← Kembali</Button>
      <PageHeader title="Informasi Detail Transaksi Anggaran" />
    </div>

    <!-- Info header (read-only) -->
    <div class="rounded-xl border border-border bg-surface p-5">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2 text-sm">
        <div class="flex gap-2">
          <span class="w-40 text-muted shrink-0">Nama Pemilik Budget</span>
          <span class="font-medium">{{ ownerName }}</span>
        </div>
        <div class="flex gap-2">
          <span class="w-40 text-muted shrink-0">Tahun Anggaran</span>
          <span class="font-medium">{{ periodValue }}</span>
        </div>
        <div class="flex gap-2">
          <span class="w-40 text-muted shrink-0">Kode Anggaran</span>
          <span class="font-mono font-medium">{{ budgetCode }}</span>
        </div>
        <div class="flex gap-2">
          <span class="w-40 text-muted shrink-0">Kegiatan</span>
          <span class="font-medium">{{ itemGroup || '—' }}</span>
        </div>
        <div class="flex gap-2 sm:col-span-2">
          <span class="w-40 text-muted shrink-0">Rincian Kebutuhan</span>
          <span class="font-medium">{{ itemName || '—' }}</span>
        </div>
      </div>

      <!-- Filter periode -->
      <div class="mt-4 pt-4 border-t border-border flex flex-wrap items-end gap-3">
        <div>
          <label class="mb-1 block text-xs text-muted">Periode Tgl</label>
          <DateField v-model="beginDate" />
        </div>
        <span class="text-muted text-sm pb-1">s/d</span>
        <div>
          <label class="mb-1 block text-xs text-muted">&nbsp;</label>
          <DateField v-model="endDate" />
        </div>
        <Button :loading="loading" @click="tampilkan">Tampilkan Transaksi</Button>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="!hasData && !loading" class="flex items-center justify-center h-32 text-muted-foreground text-sm">
      Pilih periode dan klik "Tampilkan Transaksi"
    </div>

    <!-- Table -->
    <template v-if="hasData">
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 border-b border-border">
          <span class="text-[11px] text-muted tabular-nums">{{ rows.length }} transaksi</span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
              <tr>
                <th class="px-3 py-2 text-center font-medium w-8">No</th>
                <th class="px-3 py-2 text-left font-medium">Tanggal</th>
                <th class="px-3 py-2 text-right font-medium">Nilai Realisasi</th>
                <th class="px-3 py-2 text-right font-medium">Nilai Pengembalian</th>
                <th class="px-3 py-2 text-left font-medium">No Referensi</th>
                <th class="px-3 py-2 text-left font-medium">Keterangan</th>
                <th class="px-3 py-2 text-left font-medium">Jenis Transaksi</th>
                <th class="px-3 py-2 text-left font-medium">Inputer</th>
                <th class="px-3 py-2 text-left font-medium">Nomor Transaksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-if="loading">
                <td colspan="9" class="px-4 py-8 text-center text-muted">Memuat...</td>
              </tr>
              <tr v-else-if="rows.length === 0">
                <td colspan="9" class="px-4 py-8 text-center text-muted italic">
                  Tidak ada transaksi pada periode ini.
                </td>
              </tr>
              <tr v-for="(row, idx) in rows" :key="row.transaction_item_id" class="hover:bg-muted/30">
                <td class="px-3 py-1.5 text-center text-muted">{{ idx + 1 }}</td>
                <td class="px-3 py-1.5 tabular-nums whitespace-nowrap">{{ dmy(row.actual_date) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums font-medium">
                  {{ row.realization_amount ? formatIdr(row.realization_amount) : '—' }}
                </td>
                <td class="px-3 py-1.5 text-right tabular-nums text-muted">
                  {{ row.return_amount ? formatIdr(row.return_amount) : '—' }}
                </td>
                <td class="px-3 py-1.5 text-muted">{{ row.reference_no ?? '—' }}</td>
                <td class="px-3 py-1.5 max-w-xs truncate" :title="row.description ?? ''">
                  {{ row.description ?? '—' }}
                </td>
                <td class="px-3 py-1.5 whitespace-nowrap">{{ row.transaction_type_name ?? row.transaction_code }}</td>
                <td class="px-3 py-1.5">{{ row.inputer ?? '—' }}</td>
                <td class="px-3 py-1.5 font-mono">{{ row.transaction_no ?? '—' }}</td>
              </tr>
            </tbody>
            <tfoot v-if="rows.length > 0" class="border-t-2 border-border bg-muted/20 font-semibold">
              <tr>
                <td colspan="2" class="px-3 py-2 text-xs">Total Realisasi</td>
                <td class="px-3 py-2 text-right text-xs tabular-nums">{{ formatIdr(totals.realization) }}</td>
                <td colspan="6" />
              </tr>
              <tr class="border-t border-border/50">
                <td colspan="2" class="px-3 py-2 text-xs">Total Pengembalian</td>
                <td />
                <td class="px-3 py-2 text-right text-xs tabular-nums text-muted">{{ formatIdr(totals.return) }}</td>
                <td colspan="5" />
              </tr>
              <tr class="border-t border-border/50">
                <td colspan="2" class="px-3 py-2 text-xs">Saldo</td>
                <td
                  class="px-3 py-2 text-right text-xs tabular-nums"
                  :class="totals.saldo >= 0 ? 'text-positive' : 'text-red-600'"
                >
                  {{ formatIdr(totals.saldo) }}
                </td>
                <td colspan="6" />
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

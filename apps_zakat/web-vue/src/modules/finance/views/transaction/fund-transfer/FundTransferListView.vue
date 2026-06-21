<script setup lang="ts">
import { Plus, Search } from 'lucide-vue-next'
import { computed, shallowRef, ref } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'
import type { MenuKey } from '@/shared/constants/menu-keys'

// ── Types ─────────────────────────────────────────────────────────────────────
interface TransferRow {
  transactionid: number
  transaction_no: string | null
  actual_date: string
  amount: number
  auth_status: string
  branch_code: string
  inputer: string
  description: string | null
  reference_no: string | null
  source_account_name: string | null
  source_cash_account_no: string | null
  dest_account_name: string | null
  dest_cash_account_no: string | null
}

interface ListResponse {
  rows: TransferRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

// ── State ─────────────────────────────────────────────────────────────────────
const auth = useAuthStore()
const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const rows = ref<TransferRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)

const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const showCount = computed(() => {
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, totalRec.value)
  if (!hasLoaded.value) return 'Pilih periode dan klik Tampilkan'
  return totalRec.value > 0 ? `Showing ${from}–${to} of ${totalRec.value} records` : 'Tidak ada data'
})

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

// ── Load ──────────────────────────────────────────────────────────────────────
async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      date_from: dateFrom.value,
      date_to: dateTo.value,
      page: String(page.value),
      limit: String(pageSize.value),
    })
    const res = await api.get<ListResponse>(`/api/transaction/inter-account-transfer/?${params}`)
    rows.value = res.rows ?? []
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : 'Gagal memuat data'
    toast.error('Gagal memuat data transfer')
  } finally {
    loading.value = false
  }
}

// ── Status badge ──────────────────────────────────────────────────────────────
function authLabel(status: string) {
  return status === 'T' ? 'Disetujui' : 'Menunggu'
}
function authClass(status: string) {
  if (status === 'T') return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200'
  return 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-200'
}
</script>

<template>
  <div class="space-y-0">
    <PageHeader title="Transfer Antar Rekening" subtitle="Transfer dana antara rekening kas dan bank">
      <template #actions>
        <Button
          v-if="auth.hasMenu('finance.transactions.fund_transfer' as MenuKey)"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="router.push({ name: 'finance-transactions-fund-transfer-create' })"
        >
          <Plus class="w-3.5 h-3.5" />
          Input Baru
        </Button>
      </template>
    </PageHeader>

    <!-- Error -->
    <div v-if="errorMsg" class="mx-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar -->
      <div class="px-4 py-3 border-b border-border">
        <div class="flex flex-wrap items-end gap-3">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Dari Tanggal</label>
            <DateField v-model="dateFrom" />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Sampai Tanggal</label>
            <DateField v-model="dateTo" />
          </div>
          <Button variant="secondary" :disabled="loading" @click="() => { page = 1; load() }">
            <Search class="mr-2 h-4 w-4" />
            {{ loading ? 'Memuat...' : 'Tampilkan' }}
          </Button>
        </div>
      </div>

      <!-- Pagination (selalu di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-xs text-muted-foreground tabular-nums">{{ showCount }}</span>
        <TablePagination
          v-if="hasLoaded && totalPages > 1"
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @goto="goto"
        />
      </div>

      <!-- Tabel -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">No. Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">Tanggal</th>
              <th class="px-4 py-2 text-left font-medium">Rekening Sumber</th>
              <th class="px-4 py-2 text-left font-medium">Rekening Tujuan</th>
              <th class="px-4 py-2 text-right font-medium">Nominal</th>
              <th class="px-4 py-2 text-center font-medium">Status</th>
              <th class="px-4 py-2 text-left font-medium">Input Oleh</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length && !hasLoaded">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Pilih periode dan klik Tampilkan untuk melihat data.
              </td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada transaksi dalam periode ini.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.transactionid"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-2 text-xs font-mono">{{ row.transaction_no ?? '-' }}</td>
              <td class="px-4 py-2 text-xs">{{ dmy(row.actual_date) }}</td>
              <td class="px-4 py-2 text-xs">
                <span class="font-mono text-[10px] text-muted-foreground">{{ row.source_cash_account_no }}</span>
                <span v-if="row.source_account_name" class="ml-1">{{ row.source_account_name }}</span>
              </td>
              <td class="px-4 py-2 text-xs">
                <span class="font-mono text-[10px] text-muted-foreground">{{ row.dest_cash_account_no }}</span>
                <span v-if="row.dest_account_name" class="ml-1">{{ row.dest_account_name }}</span>
              </td>
              <td class="px-4 py-2 text-xs text-right font-tabular">{{ fmt(row.amount) }}</td>
              <td class="px-4 py-2 text-xs text-center">
                <span :class="['inline-block px-2 py-1 rounded text-[10px] font-semibold', authClass(row.auth_status)]">
                  {{ authLabel(row.auth_status) }}
                </span>
              </td>
              <td class="px-4 py-2 text-xs">{{ row.inputer }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

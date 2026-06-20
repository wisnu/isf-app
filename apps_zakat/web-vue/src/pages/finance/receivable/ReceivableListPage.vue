<script setup lang="ts">
import { Plus, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import StatusBadge from '@/components/authorization/StatusBadge.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────
interface ReceivableRow {
  _rowKind: 'transaction'
  id: number
  transaction_no: string | null
  transaction_code: string
  actual_date: string
  debtor_name: string
  debtor_type: string
  amount: number
  status: string
  description: string | null
  inputer: string
}

interface SubmissionRow {
  _rowKind: 'submission'
  id: number
  actual_date: string
  transaction_type: string
  debtor_name: string
  debtor_type: string
  amount: number
  status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED'
  rejection_notes: string | null
  payload: Record<string, any>
}

type MergedRow = ReceivableRow | SubmissionRow

interface ListResponse {
  rows: Omit<ReceivableRow, '_rowKind'>[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

// ── State ─────────────────────────────────────────────────────────────────────
const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const txRows = ref<ReceivableRow[]>([])
const subRows = ref<SubmissionRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)
const actionLoading = shallowRef<number | null>(null)

const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const mergedRows = computed<MergedRow[]>(() => [
  ...subRows.value,
  ...txRows.value,
])

const showCount = computed(() => {
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, totalRec.value)
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

    const [txRes, subRes] = await Promise.all([
      api.get<ListResponse>(`/api/receivable/?${params}`).catch(() => ({
        rows: [],
        pagination: { page: 1, limit: 25, total: 0, total_pages: 1 },
      })),
      api.get<{ rows: any[] }>('/api/authorization/my-submissions/?entity_type=piutang').catch(
        () => ({ rows: [] }),
      ),
    ])

    txRows.value = txRes.rows.map((r) => ({ ...r, _rowKind: 'transaction' as const }))
    totalRec.value = txRes.pagination.total
    totalPages.value = txRes.pagination.total_pages
    hasLoaded.value = true

    subRows.value = subRes.rows.map((r: any) => ({
      _rowKind: 'submission' as const,
      id: r.id,
      actual_date: r.payload?.actual_date ?? r.submitted_at ?? today,
      transaction_type: r.payload?.transaction_type ?? '',
      debtor_name: r.payload?.debtor_name ?? '-',
      debtor_type: r.payload?.debtor_type ?? '',
      amount: r.payload?.amount ?? 0,
      status: r.status,
      rejection_notes: r.rejection_notes ?? null,
      payload: r.payload ?? {},
    }))
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal memuat data piutang')
  } finally {
    loading.value = false
  }
}

// ── Submission actions ────────────────────────────────────────────────────────
async function submitDraft(id: number) {
  actionLoading.value = id
  try {
    await api.post(`/api/authorization/submission/${id}/submit`, {})
    toast.success('Submission berhasil dikirim untuk otorisasi')
    await load()
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal mengirim submission')
  } finally {
    actionLoading.value = null
  }
}

async function deleteDraft(id: number) {
  actionLoading.value = id
  try {
    await api.delete(`/api/authorization/submission/${id}`)
    toast.success('Draft dihapus')
    subRows.value = subRows.value.filter((r) => r.id !== id)
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal menghapus draft')
  } finally {
    actionLoading.value = null
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function typeLabel(code: string) {
  if (code === 'EAR' || code === 'P') return 'Pinjam'
  if (code === 'PEAR' || code === 'B') return 'Bayar'
  return code
}

function debtorTypeLabel(type: string) {
  return type === 'E' ? 'Karyawan' : type === 'X' ? 'Non-Karyawan' : type
}

onMounted(load)
</script>

<template>
  <div class="space-y-0">
    <PageHeader title="Piutang (Pinjam/Bayar)" subtitle="Kelola transaksi pinjam dan bayar piutang kepada karyawan dan pihak eksternal">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="router.push({ name: 'finance-transactions-receivable-create' })">
          <Plus class="w-3.5 h-3.5" />
          Input Piutang
        </Button>
      </template>
    </PageHeader>

    <Alert v-if="errorMsg" variant="destructive" class="mb-3">{{ errorMsg }}</Alert>

    <!-- Toolbar -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <div class="flex items-end gap-2">
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Dari</label>
          <DateField v-model="dateFrom" />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai</label>
          <DateField v-model="dateTo" />
        </div>
      </div>
      <Button size="sm" class="gap-1.5 h-8 text-xs" :disabled="loading" @click="() => { page = 1; load() }">
        <Search class="w-3.5 h-3.5" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
    </div>

    <!-- Paginator TOP -->
    <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
      <span class="text-xs text-zinc-500">
        {{ hasLoaded ? showCount : 'Pilih tanggal dan klik Tampilkan' }}
        <span v-if="subRows.length" class="ml-2 text-yellow-600">(+ {{ subRows.length }} draft/pending)</span>
      </span>
      <TablePagination
        v-if="hasLoaded && totalPages > 1"
        :page="page"
        :total-pages="totalPages"
        :total="totalRec"
        :page-size="pageSize"
        @prev="goto(page - 1)"
        @next="goto(page + 1)"
        @update:page-size="pageSize = $event; goto(1)"
      />
    </div>

    <!-- DataTable -->
    <div class="overflow-x-auto rounded-b border">
      <table class="w-full text-sm">
        <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
          <tr>
            <th class="px-4 py-2 font-medium text-left">No. Transaksi / Draft</th>
            <th class="px-4 py-2 font-medium text-left">Tanggal</th>
            <th class="px-4 py-2 font-medium text-left">Jenis</th>
            <th class="px-4 py-2 font-medium text-left">Debitur</th>
            <th class="px-4 py-2 font-medium text-left">Tipe Debitur</th>
            <th class="px-4 py-2 font-medium text-right">Nominal</th>
            <th class="px-4 py-2 font-medium text-center">Status</th>
            <th class="px-4 py-2 font-medium text-left">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!hasLoaded">
            <td colspan="8" class="px-4 py-8 text-center text-zinc-400">
              Pilih tanggal dan klik Tampilkan untuk melihat data.
            </td>
          </tr>
          <tr v-else-if="mergedRows.length === 0">
            <td colspan="8" class="px-4 py-8 text-center text-zinc-400">
              Tidak ada transaksi piutang dalam periode ini.
            </td>
          </tr>

          <!-- Submission rows (DRAFT/PENDING/REJECTED) -->
          <tr
            v-for="row in subRows"
            :key="`sub-${row.id}`"
            class="border-b border-border bg-amber-50/40 dark:bg-amber-900/10"
          >
            <td class="px-4 py-2 font-mono text-xs text-zinc-400">Draft #{{ row.id }}</td>
            <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
            <td class="px-4 py-2">{{ typeLabel(row.transaction_type) }}</td>
            <td class="px-4 py-2 text-zinc-700 dark:text-zinc-300">{{ row.debtor_name }}</td>
            <td class="px-4 py-2">{{ debtorTypeLabel(row.debtor_type) }}</td>
            <td class="px-4 py-2 text-right font-medium">{{ fmt(row.amount) }}</td>
            <td class="px-4 py-2 text-center">
              <StatusBadge :status="row.status" />
            </td>
            <td class="px-4 py-2">
              <div class="flex items-center gap-1.5 flex-wrap">
                <template v-if="row.status === 'DRAFT'">
                  <button
                    class="rounded border border-primary px-2 py-0.5 text-xs font-medium text-primary hover:bg-primary hover:text-white transition disabled:opacity-50"
                    :disabled="actionLoading === row.id"
                    @click="submitDraft(row.id)"
                  >Submit</button>
                </template>
                <template v-else-if="row.status === 'PENDING'">
                  <span class="text-xs text-zinc-500">Menunggu otorisasi</span>
                </template>
                <template v-else-if="row.status === 'REJECTED'">
                  <button
                    class="rounded border border-amber-500 px-2 py-0.5 text-xs font-medium text-amber-600 hover:bg-amber-50 transition disabled:opacity-50"
                    :disabled="actionLoading === row.id"
                    @click="router.push({ name: 'finance-transactions-receivable-create' })"
                  >Revisi</button>
                  <button
                    class="rounded border border-red-400 px-2 py-0.5 text-xs font-medium text-red-500 hover:bg-red-50 transition disabled:opacity-50"
                    :disabled="actionLoading === row.id"
                    @click="deleteDraft(row.id)"
                  >Hapus</button>
                  <span
                    v-if="row.rejection_notes"
                    :title="row.rejection_notes"
                    class="cursor-help text-xs text-red-400 underline decoration-dotted"
                  >Alasan</span>
                </template>
              </div>
            </td>
          </tr>

          <!-- Transaction rows (authorized) -->
          <tr
            v-for="row in txRows"
            :key="`tx-${row.id}`"
            class="cursor-pointer border-b border-border last:border-0 hover:bg-background/60"
          >
            <td class="px-4 py-2 font-mono text-xs">{{ row.transaction_no ?? '-' }}</td>
            <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
            <td class="px-4 py-2">{{ typeLabel(row.transaction_code) }}</td>
            <td class="px-4 py-2 text-zinc-700 dark:text-zinc-300">{{ row.debtor_name }}</td>
            <td class="px-4 py-2">{{ debtorTypeLabel(row.debtor_type) }}</td>
            <td class="px-4 py-2 text-right font-medium">{{ fmt(row.amount) }}</td>
            <td class="px-4 py-2 text-center">
              <span class="rounded px-2 py-0.5 text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                Terotorisasi
              </span>
            </td>
            <td class="px-4 py-2 text-xs text-zinc-400">{{ row.inputer ?? '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

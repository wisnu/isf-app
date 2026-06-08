<script setup lang="ts">
import { onMounted, ref, shallowRef, computed } from 'vue'
import { useRouter } from 'vue-router'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Paginator from 'primevue/paginator'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────
interface PenghimpunanRow {
  _rowKind: 'transaction'
  transaction_id: number
  transaction_no: string | null
  actual_date: string
  description: string | null
  amount: number
  channel_code: string | null
  channel_account_no: string | null
  channel_name: string | null
  inputer: string | null
  auth_status: string | null
  branch_code: string | null
  donor_name: string | null
}

interface SubmissionRow {
  _rowKind: 'submission'
  id: number
  actual_date: string
  description: string | null
  amount: number
  status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED'
  submitted_by: string | null
  rejection_notes: string | null
  payload: Record<string, any>
}

type MergedRow = PenghimpunanRow | SubmissionRow

// ── State ─────────────────────────────────────────────────────────────────────
const router = useRouter()
const toast = useToast()

const today = new Date().toISOString().slice(0, 10)
const firstOfMonth = today.slice(0, 8) + '01'

const begin = shallowRef(firstOfMonth)
const end = shallowRef(today)
const search = shallowRef('')

const txRows = ref<PenghimpunanRow[]>([])
const subRows = ref<SubmissionRow[]>([])
const total = shallowRef(0)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const actionLoading = shallowRef<number | null>(null)

const first = computed({
  get: () => (page.value - 1) * pageSize.value,
  set: (val: number) => { page.value = Math.floor(val / pageSize.value) + 1 },
})
const from = computed(() => total.value === 0 ? 0 : (page.value - 1) * pageSize.value + 1)
const to = computed(() => Math.min(page.value * pageSize.value, total.value))
const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => 'Rp ' + idr.format(n)

const CHANNEL_LABEL: Record<string, string> = {
  P: 'Kas Kecil', R: 'Kas Cabang', A: 'Bank', G: 'Aset/GL',
}

// ── Merged rows: submissions first, then authorized transactions ───────────────
const mergedRows = computed<MergedRow[]>(() => [
  ...subRows.value,
  ...txRows.value,
])

// ── Load ──────────────────────────────────────────────────────────────────────
async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      begin: begin.value,
      end: end.value,
      page: String(page.value),
      page_size: String(pageSize.value),
    })
    if (search.value) params.set('search', search.value)

    const [txRes, subRes] = await Promise.all([
      api.get<{ rows: Omit<PenghimpunanRow, '_rowKind'>[]; pagination: { total: number } }>(
        `/api/penghimpunan/?${params}`,
      ).catch(() => ({ rows: [], pagination: { total: 0 } })),
      api.get<{ rows: Omit<SubmissionRow, '_rowKind'>[] }>(
        '/api/otorisasi/my-submissions/?entity_type=penghimpunan',
      ).catch(() => ({ rows: [] })),
    ])

    txRows.value = txRes.rows.map((r) => ({ ...r, _rowKind: 'transaction' as const }))
    total.value = txRes.pagination.total

    subRows.value = subRes.rows.map((r: any) => ({
      _rowKind: 'submission' as const,
      id: r.id,
      actual_date: r.payload?.actual_date ?? r.submitted_at ?? today,
      description: r.payload?.description ?? null,
      amount: (r.payload?.items ?? []).reduce((s: number, i: any) => s + (i.amount ?? 0), 0),
      status: r.status,
      submitted_by: r.submitted_by ?? null,
      rejection_notes: r.rejection_notes ?? null,
      payload: r.payload ?? {},
    }))
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

function onPage(ev: { page: number; rows: number }) {
  page.value = ev.page + 1
  pageSize.value = ev.rows
  load()
}

function onSearch() {
  page.value = 1
  load()
}

// ── Submission actions ────────────────────────────────────────────────────────
async function submitDraft(id: number) {
  actionLoading.value = id
  try {
    await api.post(`/api/otorisasi/submission/${id}/submit`, {})
    toast.success('Submission berhasil dikirim untuk otorisasi')
    await load()
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal mengirim submission')
  } finally {
    actionLoading.value = null
  }
}

function editDraft(id: number) {
  router.push({ name: 'keuangan-transaksi-penghimpunan-edit', params: { id: String(id) } })
}

async function deleteDraft(id: number) {
  actionLoading.value = id
  try {
    await api.delete(`/api/otorisasi/submission/${id}`)
    toast.success('Draft dihapus')
    subRows.value = subRows.value.filter((r) => r.id !== id)
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal menghapus draft')
  } finally {
    actionLoading.value = null
  }
}

onMounted(load)
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <!-- Page header -->
    <header class="flex items-center justify-between">
      <h1 class="text-2xl font-bold tracking-tight">Penghimpunan Dana</h1>
      <Button @click="router.push({ name: 'keuangan-transaksi-penghimpunan-baru' })">
        + Input Penghimpunan
      </Button>
    </header>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <!-- Toolbar -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border border-b-0 bg-white px-4 py-3 dark:bg-zinc-900">
      <div class="flex items-end gap-2">
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Dari</label>
          <DateField v-model="begin" class="w-36" />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai</label>
          <DateField v-model="end" class="w-36" />
        </div>
      </div>
      <div class="flex-1 min-w-[200px]">
        <label class="mb-1 block text-xs font-medium text-zinc-500">Cari No. Transaksi</label>
        <div class="flex gap-2">
          <input
            v-model="search"
            placeholder="KM-2026-..."
            class="h-9 flex-1 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            @keyup.enter="onSearch"
          />
          <Button variant="secondary" @click="onSearch">Tampilkan</Button>
        </div>
      </div>
    </div>

    <!-- Pagination bar (top) -->
    <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
      <span class="text-sm text-zinc-400">
        Showing {{ from }}–{{ to }} of <strong>{{ total }}</strong> records
        <span v-if="subRows.length" class="ml-2 text-yellow-600">(+ {{ subRows.length }} draft/pending)</span>
      </span>
      <Paginator
        v-model:first="first"
        :rows="pageSize"
        :total-records="total"
        :rows-per-page-options="[25, 50, 100]"
        template="RowsPerPageDropdown FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
        class="!p-0 !bg-transparent"
        @page="onPage"
      />
    </div>

    <!-- Table -->
    <div class="overflow-x-auto rounded-b border dark:border-zinc-700">
      <DataTable
        :value="mergedRows"
        :loading="loading"
        class="w-full"
        row-hover
        data-key="_rowKind === 'transaction' ? transaction_id : id"
      >
        <!-- No. Transaksi / ID Draft -->
        <Column header="No. Transaksi / Draft" class="min-w-[160px]">
          <template #body="{ data }">
            <template v-if="data._rowKind === 'transaction'">
              <span class="font-mono text-xs">{{ (data as any).transaction_no ?? '-' }}</span>
            </template>
            <template v-else>
              <span class="font-mono text-xs text-zinc-400">Draft #{{ (data as any).id }}</span>
            </template>
          </template>
        </Column>

        <!-- Tanggal -->
        <Column field="actual_date" header="Tanggal" class="min-w-[110px]">
          <template #body="{ data }">{{ dmy(data.actual_date) }}</template>
        </Column>

        <!-- Donatur (only for transactions) -->
        <Column header="Donatur" class="min-w-[140px]">
          <template #body="{ data }">
            <span v-if="data._rowKind === 'transaction'">{{ (data as any).donor_name ?? '-' }}</span>
            <span v-else class="text-xs text-zinc-400">—</span>
          </template>
        </Column>

        <!-- Keterangan -->
        <Column header="Keterangan" class="min-w-[180px]">
          <template #body="{ data }">
            <span class="line-clamp-1 text-sm">{{ data.description ?? '-' }}</span>
          </template>
        </Column>

        <!-- Jenis Bayar (only for transactions) -->
        <Column header="Jenis Bayar" class="min-w-[110px]">
          <template #body="{ data }">
            <span v-if="data._rowKind === 'transaction'">
              {{ CHANNEL_LABEL[(data as any).channel_code ?? ''] ?? (data as any).channel_code ?? '-' }}
            </span>
            <span v-else class="text-xs text-zinc-400">—</span>
          </template>
        </Column>

        <!-- Total -->
        <Column header="Total" class="min-w-[130px] text-right">
          <template #body="{ data }">
            <span class="font-semibold">{{ fmt(data.amount) }}</span>
          </template>
        </Column>

        <!-- Status -->
        <Column header="Status" class="min-w-[110px]">
          <template #body="{ data }">
            <template v-if="data._rowKind === 'transaction'">
              <span :class="[
                'rounded px-2 py-0.5 text-xs font-medium',
                (data as any).auth_status === 'A' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700',
              ]">
                {{ (data as any).auth_status === 'A' ? 'Approved' : 'Pending' }}
              </span>
            </template>
            <template v-else>
              <StatusBadge :status="(data as any).status" />
            </template>
          </template>
        </Column>

        <!-- Aksi -->
        <Column header="Aksi" class="min-w-[160px]">
          <template #body="{ data }">
            <!-- Transaction rows: no actions -->
            <span v-if="data._rowKind === 'transaction'" class="text-xs text-zinc-400">
              {{ (data as any).inputer ?? '-' }}
            </span>

            <!-- Submission rows: actions by status -->
            <div v-else class="flex items-center gap-1.5 flex-wrap">
              <!-- DRAFT: Submit + Edit -->
              <template v-if="(data as any).status === 'DRAFT'">
                <button
                  class="rounded border border-primary px-2 py-0.5 text-xs font-medium text-primary hover:bg-primary hover:text-white transition disabled:opacity-50"
                  :disabled="actionLoading === (data as any).id"
                  @click="submitDraft((data as any).id)"
                >Submit</button>
                <button
                  class="rounded border border-zinc-300 px-2 py-0.5 text-xs font-medium text-zinc-600 hover:bg-zinc-100 transition disabled:opacity-50"
                  :disabled="actionLoading === (data as any).id"
                  @click="editDraft((data as any).id)"
                >Edit</button>
              </template>

              <!-- PENDING: read-only -->
              <template v-else-if="(data as any).status === 'PENDING'">
                <span class="text-xs text-zinc-500">Menunggu otorisasi</span>
              </template>

              <!-- REJECTED: Revisi + Hapus + tooltip notes -->
              <template v-else-if="(data as any).status === 'REJECTED'">
                <button
                  class="rounded border border-amber-500 px-2 py-0.5 text-xs font-medium text-amber-600 hover:bg-amber-50 transition disabled:opacity-50"
                  :disabled="actionLoading === (data as any).id"
                  @click="editDraft((data as any).id)"
                >Revisi</button>
                <button
                  class="rounded border border-red-400 px-2 py-0.5 text-xs font-medium text-red-500 hover:bg-red-50 transition disabled:opacity-50"
                  :disabled="actionLoading === (data as any).id"
                  @click="deleteDraft((data as any).id)"
                >Hapus</button>
                <span
                  v-if="(data as any).rejection_notes"
                  :title="(data as any).rejection_notes"
                  class="cursor-help text-xs text-red-400 underline decoration-dotted"
                >Alasan</span>
              </template>
            </div>
          </template>
        </Column>

        <template #empty>
          <div class="py-12 text-center text-sm text-zinc-400">Tidak ada data untuk periode ini.</div>
        </template>
      </DataTable>
    </div>
  </div>
</template>

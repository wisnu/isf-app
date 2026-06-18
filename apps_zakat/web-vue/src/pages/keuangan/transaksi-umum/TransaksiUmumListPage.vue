<script setup lang="ts">
import { BookOpen, Pencil, Plus, Search, Trash2 } from 'lucide-vue-next'
import { computed, ref, shallowRef, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import AppTable from '@/components/ui/AppTable.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import Modal from '@/components/ui/Modal.vue'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

interface TxRow {
  _kind: 'tx'
  transactionid: number
  transactionno: string
  actual_date: string
  description: string
  reference_no: string | null
  amount: number
  authstatus: string
  inputer: string
  branch_code: string
}

interface SubRow {
  _kind: 'sub'
  id: number
  actual_date: string
  status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED' | 'PROCESSING'
  rejection_notes: string | null
  payload: Record<string, unknown>
}

type MergedRow = TxRow | SubRow

const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const txRows = ref<TxRow[]>([])
const subRows = ref<SubRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)
const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)
const search = shallowRef('')
const statusFilter = shallowRef<'all' | 'posted' | 'draft'>('all')

// Detail modal
const showDetail = shallowRef(false)
const detailRow = ref<TxRow & { items?: unknown[] } | null>(null)
const detailLoading = shallowRef(false)

// Delete modal
const showDeleteModal = shallowRef(false)
const deleteRow = ref<MergedRow | null>(null)
const deleteLoading = shallowRef(false)

const mergedRows = computed<MergedRow[]>(() => {
  const subs = subRows.value.map(r => ({ ...r, _kind: 'sub' as const }))
  const txs = txRows.value.map(r => ({ ...r, _kind: 'tx' as const }))
  if (statusFilter.value === 'posted') return txs
  if (statusFilter.value === 'draft') return subs
  return [...subs, ...txs]
})

const showCount = computed(() => {
  if (!totalRec.value && !subRows.value.length) return 'Tidak ada data'
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, totalRec.value)
  return `Showing ${from}–${to} of ${totalRec.value} records`
})

const detailItems = computed<Record<string, unknown>[]>(() => {
  const row = detailRow.value as (TxRow & { items?: Record<string, unknown>[] }) | null
  return row?.items ?? []
})

const deleteRowLabel = computed(() => {
  if (!deleteRow.value) return null
  if (deleteRow.value._kind === 'tx') return deleteRow.value.transactionno
  return `Draft #${deleteRow.value.id}`
})

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      limit: String(pageSize.value),
      date_from: dateFrom.value,
      date_to: dateTo.value,
    })
    if (search.value) params.set('search', search.value)

    const [txRes, subRes] = await Promise.all([
      api.get<{ rows: Omit<TxRow, '_kind'>[]; pagination: { total: number; total_pages: number } }>(
        `/api/transaksi-umum/?${params}`
      ),
      api.get<{ rows: Omit<SubRow, '_kind'>[] }>(
        '/api/otorisasi/my-submissions/?entity_type=transaksi_umum'
      ).catch(() => ({ rows: [] })),
    ])

    txRows.value = (txRes?.rows ?? []).map(r => ({ ...r, _kind: 'tx' as const }))
    subRows.value = (subRes?.rows ?? []).map(r => ({ ...r, _kind: 'sub' as const }))
    totalRec.value = txRes?.pagination?.total ?? 0
    totalPages.value = txRes?.pagination?.total_pages ?? 1
    hasLoaded.value = true
  } catch {
    errorMsg.value = 'Gagal memuat data transaksi'
  } finally {
    loading.value = false
  }
}

async function openDetail(row: TxRow) {
  detailLoading.value = true
  showDetail.value = true
  detailRow.value = { ...row }
  try {
    const res = await api.get<{ id: number; items: unknown[] }>(`/api/transaksi-umum/${row.transactionid}`)
    detailRow.value = { ...row, items: res?.items ?? [] } as TxRow & { items: unknown[] }
  } catch {
    // keep header
  } finally {
    detailLoading.value = false
  }
}

function openDeleteModal(row: MergedRow) {
  deleteRow.value = row
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!deleteRow.value) return
  deleteLoading.value = true
  try {
    if (deleteRow.value._kind === 'tx') {
      await api.delete(`/api/transaksi-umum/${deleteRow.value.transactionid}`)
    } else {
      await api.delete(`/api/otorisasi/submission/${deleteRow.value.id}`)
    }
    toast.success('Transaksi berhasil dihapus')
    showDeleteModal.value = false
    deleteRow.value = null
    load()
  } catch (e: unknown) {
    toast.error((e as { message?: string })?.message ?? 'Gagal menghapus transaksi')
  } finally {
    deleteLoading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <BookOpen class="h-5 w-5 text-primary" />
        <h1 class="text-xl font-bold text-foreground">Transaksi Umum</h1>
      </div>
      <Button size="sm" class="gap-1.5" @click="router.push({ name: 'keuangan-transaksi-umum-create' })">
        <Plus class="h-3.5 w-3.5" />
        Input Transaksi
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <div class="space-y-0">
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
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Status</label>
          <select
            v-model="statusFilter"
            class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
          >
            <option value="all">Semua</option>
            <option value="posted">Posted</option>
            <option value="draft">Draft / Pending</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Cari</label>
          <input
            v-model="search"
            placeholder="No. transaksi / deskripsi..."
            class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            @keyup.enter="() => { page.value = 1; load() }"
          />
        </div>
        <Button size="sm" class="h-8 gap-1.5 text-xs" :disabled="loading" @click="() => { page.value = 1; load() }">
          <Search class="h-3.5 w-3.5" />
          {{ loading ? 'Memuat...' : 'Tampilkan' }}
        </Button>
      </div>

      <!-- Count + pagination -->
      <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
        <span class="text-xs text-zinc-500">
          {{ hasLoaded ? showCount : 'Pilih tanggal dan klik Tampilkan' }}
          <span v-if="subRows.length && statusFilter !== 'posted'" class="ml-2 text-yellow-600">
            (+ {{ subRows.length }} draft/pending)
          </span>
        </span>
        <TablePagination
          v-if="hasLoaded && totalPages > 1"
          :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @goto="goto"
        />
      </div>

      <!-- Table -->
      <AppTable class="rounded-b border">
        <template #head>
          <tr>
            <th class="px-4 py-3 text-left">No. Transaksi</th>
            <th class="px-4 py-3 text-left">Tanggal</th>
            <th class="px-4 py-3 text-left">Deskripsi</th>
            <th class="px-4 py-3 text-right">Nilai</th>
            <th class="px-4 py-3 text-center">Status</th>
            <th class="px-4 py-3 text-left">Inputer</th>
            <th class="px-4 py-3 text-center w-20">Aksi</th>
          </tr>
        </template>

        <tr v-if="!hasLoaded">
          <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
            Pilih tanggal dan klik Tampilkan untuk melihat data.
          </td>
        </tr>
        <tr v-else-if="mergedRows.length === 0">
          <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
            Tidak ada transaksi dalam periode ini.
          </td>
        </tr>

        <template v-for="row in mergedRows" :key="row._kind === 'tx' ? `tx-${row.transactionid}` : `sub-${row.id}`">
          <tr v-if="row._kind === 'sub'" class="border-t bg-amber-50/40 dark:bg-amber-900/10">
            <td class="px-4 py-3 font-mono text-xs text-zinc-400">Draft #{{ row.id }}</td>
            <td class="px-4 py-3">{{ dmy(row.actual_date) }}</td>
            <td class="px-4 py-3 text-zinc-500">{{ (row.payload as Record<string,unknown>).description as string || '—' }}</td>
            <td class="px-4 py-3 text-right text-zinc-400">—</td>
            <td class="px-4 py-3 text-center"><StatusBadge :status="row.status" /></td>
            <td class="px-4 py-3">
              <span v-if="row.status === 'REJECTED' && row.rejection_notes" :title="row.rejection_notes" class="cursor-help text-xs text-red-400 underline decoration-dotted">Alasan</span>
              <span v-else-if="row.status === 'PENDING'" class="text-xs text-zinc-400">Menunggu otorisasi</span>
            </td>
            <td class="px-4 py-3 text-center">
              <button
                v-if="row.status === 'DRAFT'"
                class="rounded p-1.5 text-red-400 hover:bg-red-50 hover:text-red-600"
                title="Hapus draft"
                @click.stop="openDeleteModal(row)"
              >
                <Trash2 class="h-3.5 w-3.5" />
              </button>
            </td>
          </tr>

          <tr v-else class="cursor-pointer border-t hover:bg-zinc-50 dark:hover:bg-zinc-800" @click="openDetail(row as TxRow)">
            <td class="px-4 py-3 font-mono">{{ row.transactionno }}</td>
            <td class="px-4 py-3">{{ dmy(row.actual_date) }}</td>
            <td class="px-4 py-3 max-w-xs truncate" :title="row.description">{{ row.description }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ row.amount.toLocaleString('id-ID') }}</td>
            <td class="px-4 py-3 text-center">
              <span class="rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-medium text-green-700">Posted</span>
            </td>
            <td class="px-4 py-3 text-zinc-500">{{ row.inputer }}</td>
            <td class="px-4 py-3 text-center" @click.stop>
              <div class="flex items-center justify-center gap-1">
                <button
                  class="rounded p-1.5 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-600"
                  title="Lihat detail"
                  @click="openDetail(row as TxRow)"
                >
                  <Pencil class="h-3.5 w-3.5" />
                </button>
                <button
                  class="rounded p-1.5 text-red-400 hover:bg-red-50 hover:text-red-600"
                  title="Hapus transaksi"
                  @click="openDeleteModal(row as TxRow)"
                >
                  <Trash2 class="h-3.5 w-3.5" />
                </button>
              </div>
            </td>
          </tr>
        </template>
      </AppTable>
    </div>

    <!-- Detail Modal -->
    <Modal v-if="showDetail" max-width="max-w-3xl" @close="showDetail = false">
      <template #header><span class="font-semibold">Detail Transaksi Umum</span></template>

      <div v-if="detailRow" class="space-y-4">
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <div class="text-xs text-zinc-500">No. Transaksi</div>
            <div class="font-mono font-medium">{{ detailRow.transactionno }}</div>
          </div>
          <div>
            <div class="text-xs text-zinc-500">Tanggal</div>
            <div>{{ dmy(detailRow.actual_date) }}</div>
          </div>
          <div class="col-span-2">
            <div class="text-xs text-zinc-500">Deskripsi</div>
            <div>{{ detailRow.description }}</div>
          </div>
          <div v-if="detailRow.reference_no">
            <div class="text-xs text-zinc-500">No. Referensi</div>
            <div>{{ detailRow.reference_no }}</div>
          </div>
          <div>
            <div class="text-xs text-zinc-500">Inputer</div>
            <div>{{ detailRow.inputer }}</div>
          </div>
        </div>

        <div v-if="detailItems.length">
          <div class="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">Baris Jurnal</div>
          <div class="overflow-x-auto rounded border">
            <table class="w-full text-xs">
              <thead class="border-b bg-zinc-50 text-xs font-semibold text-zinc-600 dark:bg-zinc-800/50 dark:text-zinc-400">
                <tr>
                  <th class="px-3 py-2 text-left">Kode / Referensi</th>
                  <th class="px-3 py-2 text-left">Nama</th>
                  <th class="px-3 py-2 text-center">D/K</th>
                  <th class="px-3 py-2 text-right">Jumlah</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in detailItems" :key="idx" class="border-t">
                  <td class="px-3 py-1.5 font-mono text-zinc-500">{{ String(item.account_code ?? '') || '—' }}</td>
                  <td class="px-3 py-1.5">{{ String(item.account_name ?? '') }}</td>
                  <td
                    class="px-3 py-1.5 text-center font-bold"
                    :class="item.mutation_type === 'D' ? 'text-emerald-700' : 'text-red-600'"
                  >
                    {{ item.mutation_type === 'D' ? 'Debet' : 'Kredit' }}
                  </td>
                  <td class="px-3 py-1.5 text-right font-mono">{{ Number(item.amount ?? 0).toLocaleString('id-ID') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else-if="detailLoading" class="py-4 text-center text-xs text-zinc-400">Memuat detail...</div>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <Button variant="outline" @click="showDetail = false">Tutup</Button>
        </div>
      </template>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal v-if="showDeleteModal" max-width="max-w-md" @close="showDeleteModal = false">
      <template #header>
        <span class="font-semibold text-red-600">Hapus Transaksi</span>
      </template>

      <div v-if="deleteRow" class="space-y-4">
        <p class="text-sm text-zinc-600">
          Yakin ingin menghapus transaksi berikut? Tindakan ini tidak dapat dibatalkan.
        </p>

        <div class="rounded-lg border bg-zinc-50 p-4 text-sm space-y-2 dark:bg-zinc-800">
          <div class="flex justify-between">
            <span class="text-zinc-500">No. Transaksi</span>
            <span class="font-mono font-medium">{{ deleteRowLabel }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-zinc-500">Tanggal</span>
            <span>{{ dmy(deleteRow.actual_date) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-zinc-500">Deskripsi</span>
            <span class="max-w-[200px] truncate text-right">
              {{ deleteRow._kind === 'tx' ? deleteRow.description : ((deleteRow.payload as Record<string,unknown>).description as string || '—') }}
            </span>
          </div>
          <div v-if="deleteRow._kind === 'tx'" class="flex justify-between">
            <span class="text-zinc-500">Nilai</span>
            <span class="font-mono">{{ deleteRow.amount.toLocaleString('id-ID') }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-zinc-500">Status</span>
            <span v-if="deleteRow._kind === 'tx'" class="rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-medium text-green-700">Posted</span>
            <StatusBadge v-else :status="deleteRow.status" />
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" :disabled="deleteLoading" @click="showDeleteModal = false">Batal</Button>
          <Button variant="destructive" :disabled="deleteLoading" @click="confirmDelete">
            {{ deleteLoading ? 'Menghapus...' : 'Hapus Transaksi' }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

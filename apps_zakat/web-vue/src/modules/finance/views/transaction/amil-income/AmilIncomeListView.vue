<script setup lang="ts">
import { Eye, Plus, Search } from 'lucide-vue-next'
import { computed, ref, shallowRef, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/shared/components/Alert.vue'
import AppTable from '@/shared/components/AppTable.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import StatusBadge from '@/modules/finance/components/authorization/StatusBadge.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'

interface AmilIncomeRow {
  id: number
  transactionno: string
  actual_date: string
  bank_account_no: string
  bank_account_name: string
  total_amount: number
  status: 'AUTHORIZED' | 'PENDING' | 'REJECTED' | 'DRAFT'
  inputer: string
}

interface ListResponse {
  rows: AmilIncomeRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const router = useRouter()
const today = new Date().toISOString().slice(0, 10)

const rows = ref<AmilIncomeRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)
const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)

// Detail modal
const showDetail = shallowRef(false)
const detailRow = ref<AmilIncomeRow & { items?: unknown[] } | null>(null)
const detailLoading = shallowRef(false)

const showCount = computed(() => {
  if (!hasLoaded.value) return 'Pilih tanggal dan klik Tampilkan'
  if (!totalRec.value) return 'Tidak ada data'
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, totalRec.value)
  return `Showing ${from}–${to} of ${totalRec.value} records`
})

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

function searchAndReset() {
  page.value = 1
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

    const res = await api.get<ListResponse>(
      `/api/finance/transaction/amil-income/?${params}`
    )

    rows.value = res?.rows ?? []
    totalRec.value = res?.pagination?.total ?? 0
    totalPages.value = res?.pagination?.total_pages ?? 1
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = 'Gagal memuat data penerimaan amil'
  } finally {
    loading.value = false
  }
}

async function openDetail(row: AmilIncomeRow) {
  detailLoading.value = true
  showDetail.value = true
  detailRow.value = { ...row }
  try {
    const res = await api.get<{ items: unknown[] }>(`/api/finance/transaction/amil-income/${row.id}`)
    detailRow.value = { ...row, items: res?.items ?? [] } as AmilIncomeRow & { items: unknown[] }
  } catch {
    // keep header
  } finally {
    detailLoading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <div class="space-y-0">
      <!-- Toolbar -->
      <div class="flex flex-wrap items-end gap-2 rounded-t border border-slate-200 bg-white px-3 py-2.5 dark:bg-zinc-900">
        <div class="flex items-end gap-2">
          <div>
            <label class="mb-1 block text-[10px] font-medium uppercase tracking-wide text-slate-500">Dari</label>
            <DateField v-model="dateFrom" />
          </div>
          <div>
            <label class="mb-1 block text-[10px] font-medium uppercase tracking-wide text-slate-500">Sampai</label>
            <DateField v-model="dateTo" />
          </div>
        </div>
        <Button size="sm" class="gap-1.5" :disabled="loading" @click="searchAndReset">
          <Search class="h-3.5 w-3.5" />
          {{ loading ? 'Memuat...' : 'Tampilkan' }}
        </Button>
        <div class="ml-auto">
          <Button size="sm" class="gap-1.5" @click="router.push({ name: 'finance-transactions-amil-income-create' })">
            <Plus class="h-3.5 w-3.5" />
            Tambah Penerimaan Amil
          </Button>
        </div>
      </div>

      <!-- Count + pagination -->
      <div class="flex items-center justify-between border-x border-slate-200 bg-white px-3 py-1.5 dark:bg-zinc-900">
        <span class="text-xs text-slate-500">
          {{ showCount }}
        </span>
        <TablePagination
          v-if="hasLoaded && totalPages > 1"
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @goto="goto"
        />
      </div>

      <!-- Table -->
      <AppTable class="rounded-b border border-slate-200">
        <template #head>
          <tr>
            <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-slate-600">No. Transaksi</th>
            <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-slate-600">Tanggal</th>
            <th class="px-3 py-2 text-left text-xs font-semibold uppercase tracking-wide text-slate-600">Rekening</th>
            <th class="px-3 py-2 text-right text-xs font-semibold uppercase tracking-wide text-slate-600">Total</th>
            <th class="px-3 py-2 text-center text-xs font-semibold uppercase tracking-wide text-slate-600">Status</th>
            <th class="px-3 py-2 text-center w-20 text-xs font-semibold uppercase tracking-wide text-slate-600">Aksi</th>
          </tr>
        </template>

        <tr v-if="!hasLoaded">
          <td colspan="6" class="px-3 py-5 text-center text-xs text-slate-400">
            Pilih tanggal dan klik Tampilkan untuk melihat data.
          </td>
        </tr>
        <tr v-else-if="rows.length === 0">
          <td colspan="6" class="px-3 py-5 text-center text-xs text-slate-400">
            Tidak ada penerimaan amil dalam periode ini.
          </td>
        </tr>

        <tr
          v-for="row in rows"
          :key="row.id"
          class="cursor-pointer border-t border-slate-100 hover:bg-indigo-50/40 dark:hover:bg-zinc-800"
          :class="{ 'bg-slate-50/50': rows.indexOf(row) % 2 === 1 }"
          @click="openDetail(row)"
        >
          <td class="px-3 py-1.5 font-mono text-sm">{{ row.transactionno }}</td>
          <td class="px-3 py-1.5 text-sm">{{ dmy(row.actual_date) }}</td>
          <td class="px-3 py-1.5 text-sm max-w-xs truncate" :title="row.bank_account_name">{{ row.bank_account_name }}</td>
          <td class="px-3 py-1.5 text-right font-mono text-sm">{{ row.total_amount.toLocaleString('id-ID') }}</td>
          <td class="px-3 py-1.5 text-center">
            <StatusBadge :status="row.status" />
          </td>
          <td class="px-3 py-1.5 text-center" @click.stop>
            <button
              class="rounded p-1 text-indigo-500 hover:bg-indigo-50 hover:text-indigo-700"
              title="Lihat detail"
              @click="openDetail(row)"
            >
              <Eye class="h-3.5 w-3.5" />
            </button>
          </td>
        </tr>
      </AppTable>
    </div>

    <!-- Detail Modal -->
    <Modal v-if="showDetail" max-width="max-w-3xl" @close="showDetail = false">
      <template #header><span class="font-semibold text-slate-800">Detail Penerimaan Amil</span></template>

      <div v-if="detailRow" class="space-y-3">
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <div class="text-xs text-slate-500">No. Transaksi</div>
            <div class="font-mono font-medium text-slate-800">{{ detailRow.transactionno }}</div>
          </div>
          <div>
            <div class="text-xs text-slate-500">Tanggal</div>
            <div class="text-slate-700">{{ dmy(detailRow.actual_date) }}</div>
          </div>
          <div>
            <div class="text-xs text-slate-500">Rekening Tujuan</div>
            <div class="text-slate-700">{{ detailRow.bank_account_name }}</div>
          </div>
          <div>
            <div class="text-xs text-slate-500">Total</div>
            <div class="font-mono font-medium text-slate-800">{{ detailRow.total_amount.toLocaleString('id-ID') }}</div>
          </div>
          <div>
            <div class="text-xs text-slate-500">Status</div>
            <StatusBadge :status="detailRow.status" />
          </div>
          <div>
            <div class="text-xs text-slate-500">Input Oleh</div>
            <div class="text-slate-700">{{ detailRow.inputer }}</div>
          </div>
        </div>

        <div v-if="detailRow.items && detailRow.items.length">
          <div class="mb-1.5 text-[10px] font-semibold uppercase tracking-wide text-slate-500">Detail Penerimaan</div>
          <div class="overflow-x-auto rounded border border-slate-200">
            <table class="w-full text-xs">
              <thead class="border-b border-slate-200 bg-slate-50 text-[10px] font-semibold uppercase tracking-wide text-slate-600 dark:bg-zinc-800/50 dark:text-zinc-400">
                <tr>
                  <th class="px-3 py-1.5 text-left">Akun Pendapatan</th>
                  <th class="px-3 py-1.5 text-left">Deskripsi</th>
                  <th class="px-3 py-1.5 text-right">Jumlah</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, idx) in detailRow.items" :key="idx" class="border-t border-slate-100">
                  <td class="px-3 py-1.5 font-mono text-slate-500">{{ String(item.account_code ?? '') || '—' }}</td>
                  <td class="px-3 py-1.5 text-slate-700">{{ String(item.description ?? '') || '—' }}</td>
                  <td class="px-3 py-1.5 text-right font-mono text-slate-800">{{ Number(item.amount ?? 0).toLocaleString('id-ID') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else-if="detailLoading" class="py-3 text-center text-xs text-slate-400">Memuat detail...</div>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <Button variant="outline" @click="showDetail = false">Tutup</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

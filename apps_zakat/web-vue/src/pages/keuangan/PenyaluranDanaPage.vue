<script setup lang="ts">
import { ArrowDownCircle, Search } from 'lucide-vue-next'
import { computed, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

interface PenyaluranRow {
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
}

interface ListResponse {
  data: PenyaluranRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const begin = shallowRef(today)
const end = shallowRef(today)
const search = shallowRef('')
const page = shallowRef(1)
const pageSize = shallowRef(25)

const rows = ref<PenyaluranRow[]>([])
const total = shallowRef(0)
const totalPages = shallowRef(1)
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const hasLoaded = shallowRef(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const showCount = computed(() => {
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, total.value)
  return total.value > 0 ? `Showing ${from}–${to} of ${total.value} records` : 'Tidak ada data'
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
      begin: begin.value,
      end: end.value,
      page: String(page.value),
      page_size: String(pageSize.value),
    })
    if (search.value.trim()) params.set('search', search.value.trim())
    const res = await api.get<ListResponse>(`/api/penyaluran/?${params}`)
    rows.value = res.data
    total.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal memuat data penyaluran')
  } finally {
    loading.value = false
  }
}

function channelLabel(code: string | null) {
  const map: Record<string, string> = { P: 'Kas Kecil', R: 'Kas Cabang', A: 'Bank', G: 'Aset' }
  return code ? (map[code] ?? code) : '-'
}

function authLabel(status: string | null) {
  const map: Record<string, string> = { P: 'Pending', A: 'Disetujui', T: 'Ditolak' }
  return status ? (map[status] ?? status) : '-'
}

function authClass(status: string | null) {
  if (status === 'A') return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  if (status === 'T') return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
}

function openDetail(row: PenyaluranRow) {
  router.push({ name: 'keuangan-transaksi-histori-detail', params: { id: String(row.transaction_id) } })
}
</script>

<template>
  <div class="space-y-0">
    <header class="mb-4 flex flex-wrap items-center justify-between gap-3">
      <h1 class="text-2xl font-bold tracking-tight">Penyaluran Dana</h1>
      <Button @click="router.push({ name: 'keuangan-transaksi-penyaluran-baru' })">
        <ArrowDownCircle class="mr-2 h-4 w-4" />
        Input Penyaluran
      </Button>
    </header>

    <Alert v-if="errorMsg" variant="destructive" class="mb-3">{{ errorMsg }}</Alert>

    <!-- Toolbar -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <div class="flex items-end gap-2">
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Dari</label>
          <DateField v-model="begin" />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai</label>
          <DateField v-model="end" />
        </div>
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">No. Transaksi</label>
        <input
          v-model="search"
          placeholder="Cari no. transaksi..."
          class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
          @keyup.enter="() => { page = 1; load() }"
        />
      </div>
      <Button variant="secondary" :disabled="loading" @click="() => { page = 1; load() }">
        <Search class="mr-2 h-4 w-4" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
    </div>

    <!-- Paginator TOP -->
    <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
      <span class="text-xs text-zinc-500">{{ hasLoaded ? showCount : 'Pilih tanggal dan klik Tampilkan' }}</span>
      <TablePagination
        v-if="hasLoaded && totalPages > 1"
        :page="page"
        :total-pages="totalPages"
        :total="total"
        :page-size="pageSize"
        @goto="goto"
      />
    </div>

    <!-- DataTable -->
    <div class="overflow-x-auto rounded-b border">
      <table class="w-full text-sm">
        <thead class="bg-zinc-50 text-xs font-semibold uppercase text-zinc-500 dark:bg-zinc-800">
          <tr>
            <th class="px-4 py-2 text-left">No. Transaksi</th>
            <th class="px-4 py-2 text-left">Tanggal</th>
            <th class="px-4 py-2 text-left">Keterangan</th>
            <th class="px-4 py-2 text-left">Jenis</th>
            <th class="px-4 py-2 text-left">Rekening</th>
            <th class="px-4 py-2 text-right">Jumlah</th>
            <th class="px-4 py-2 text-center">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!hasLoaded">
            <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
              Pilih tanggal dan klik Tampilkan untuk melihat data.
            </td>
          </tr>
          <tr v-else-if="rows.length === 0">
            <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
              Tidak ada transaksi penyaluran dalam periode ini.
            </td>
          </tr>
          <tr
            v-for="row in rows"
            :key="row.transaction_id"
            class="cursor-pointer border-t hover:bg-zinc-50 dark:hover:bg-zinc-800"
            @click="openDetail(row)"
          >
            <td class="px-4 py-2 font-mono text-xs">{{ row.transaction_no ?? '-' }}</td>
            <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
            <td class="max-w-xs truncate px-4 py-2 text-zinc-700 dark:text-zinc-300">
              {{ row.description ?? '-' }}
            </td>
            <td class="px-4 py-2">{{ channelLabel(row.channel_code) }}</td>
            <td class="px-4 py-2 text-xs text-zinc-500">
              {{ row.channel_name ?? row.channel_account_no ?? '-' }}
            </td>
            <td class="px-4 py-2 text-right font-medium">{{ fmt(row.amount) }}</td>
            <td class="px-4 py-2 text-center">
              <span :class="['rounded px-2 py-0.5 text-xs font-medium', authClass(row.auth_status)]">
                {{ authLabel(row.auth_status) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

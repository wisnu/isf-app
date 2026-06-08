<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import TransaksiDeleteDialog from '@/components/keuangan/TransaksiDeleteDialog.vue'
import DateField from '@/components/ui/DateField.vue'
import CrudLayout from '@/components/layout/CrudLayout.vue'
import DataPanel from '@/components/layout/DataPanel.vue'
import FilterGroup from '@/components/layout/FilterGroup.vue'
import FilterPanel from '@/components/layout/FilterPanel.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

interface SearchResult {
  rows: TransaksiRow[]
  total: number
  total_pages: number
  page: number
}

interface TransaksiRow {
  transactionid: number
  transactionno: string | null
  transactiondate: string
  actualdate: string
  amount: number
  donorno: string | null
  donorname: string | null
  referenceno: string | null
  description: string | null
  inputer: string | null
  authstatus: string | null
  isposted: string | null
  authoperationmode: string | null
  branchcode: string | null
  channelname: string | null
  exttransactionid: number | null
}

const STORAGE_KEY = 'histori-transaksi-state'

const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const begin = shallowRef(today)
const end = shallowRef(today)
const dateType = shallowRef('actual')
const sortBy = shallowRef('actual_date')
const searchCategory = shallowRef('none')
const searchText = shallowRef('')
const cashAccountNo = shallowRef('')
const page = shallowRef(1)
const pageSize = shallowRef(20)

const rows = ref<TransaksiRow[]>([])
const total = shallowRef(0)
const totalPages = shallowRef(1)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const hasLoaded = shallowRef(false)

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

const deleteConfirmId = shallowRef<number | null>(null)
const deleteMsg = shallowRef<string | null>(null)
const deleting = shallowRef(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const hasFilters = computed(
  () =>
    searchCategory.value !== 'none' ||
    searchText.value.trim() !== '' ||
    cashAccountNo.value.trim() !== '' ||
    dateType.value !== 'actual' ||
    sortBy.value !== 'actual_date',
)

function resetFilters() {
  dateType.value = 'actual'
  sortBy.value = 'actual_date'
  searchCategory.value = 'none'
  searchText.value = ''
  cashAccountNo.value = ''
  page.value = 1
}

function saveState() {
  sessionStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      begin: begin.value,
      end: end.value,
      dateType: dateType.value,
      sortBy: sortBy.value,
      searchCategory: searchCategory.value,
      searchText: searchText.value,
      cashAccountNo: cashAccountNo.value,
      page: page.value,
      pageSize: pageSize.value,
      rows: rows.value,
      total: total.value,
      totalPages: totalPages.value,
      hasLoaded: hasLoaded.value,
    }),
  )
}

function restoreState() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return
    const s = JSON.parse(raw)
    begin.value = s.begin ?? today
    end.value = s.end ?? today
    dateType.value = s.dateType ?? 'actual'
    sortBy.value = s.sortBy ?? 'actual_date'
    searchCategory.value = s.searchCategory ?? 'none'
    searchText.value = s.searchText ?? ''
    cashAccountNo.value = s.cashAccountNo ?? ''
    page.value = s.page ?? 1
    pageSize.value = s.pageSize ?? 50
    rows.value = s.rows ?? []
    total.value = s.total ?? 0
    totalPages.value = s.totalPages ?? 1
    hasLoaded.value = s.hasLoaded ?? false
  } catch {
    // ignore corrupt state
  }
}

onMounted(restoreState)

function canDelete(row: TransaksiRow): boolean {
  if (row.exttransactionid != null) return false
  if (row.authstatus === 'F' && row.authoperationmode === 'D') return false
  return true
}

function authChip(s: string | null) {
  return s === 'T' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
}
function authLabel(s: string | null) {
  return s === 'T' ? 'Terotorisasi' : 'Pending'
}
function postedChip(s: string | null) {
  return s === 'T' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'
}

function buildParams(forExport = false): URLSearchParams {
  const p = new URLSearchParams({
    begin: begin.value,
    end: end.value,
    date_type: dateType.value,
    sort_by: sortBy.value,
    search_category: searchCategory.value,
  })
  if (!forExport) {
    p.set('page', String(page.value))
    p.set('page_size', String(pageSize.value))
  }
  if (searchCategory.value !== 'none' && searchText.value)
    p.set('search_text', searchText.value)
  if (cashAccountNo.value)
    p.set('cash_account_no', cashAccountNo.value)
  return p
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const d = await api.get<SearchResult>(`/api/transaksi-histori/search?${buildParams()}`)
    rows.value = d.rows
    total.value = d.total
    totalPages.value = d.total_pages
    page.value = d.page
    hasLoaded.value = true
    saveState()
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  exporting.value = true
  try {
    await api.downloadBlob(
      '/api/transaksi-histori/search/export.xlsx',
      `histori-transaksi-${begin.value}-${end.value}.xlsx`,
      buildParams(true),
    )
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    exporting.value = false
  }
}

function search() {
  page.value = 1
  load()
}

function goToDetail(id: number) {
  saveState()
  router.push(`/keuangan/transaksi/histori/${id}`)
}

async function confirmDelete() {
  if (!deleteConfirmId.value) return
  deleting.value = true
  deleteMsg.value = null
  const targetId = deleteConfirmId.value
  try {
    await api.post(`/api/transaksi-histori/transactions/${targetId}/delete`, {})
    toast.success('Transaksi berhasil dihapus')
    deleteConfirmId.value = null
    await load()
  } catch (e: unknown) {
    deleteMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <div class="p-6 space-y-3">
    <PageHeader title="Histori Transaksi">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" :disabled="loading" @click="search">
          <Search class="w-3.5 h-3.5" />
          {{ loading ? 'Memuat...' : 'Tampilkan' }}
        </Button>
        <Button
          v-if="hasLoaded && rows.length"
          variant="outline"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          :disabled="exporting"
          @click="exportXlsx"
        >
          <Download class="w-3.5 h-3.5" />
          {{ exporting ? 'Mengekspor...' : 'Export XLSX' }}
        </Button>
      </template>
    </PageHeader>

    <Alert v-if="errorMsg" variant="error" :message="errorMsg" />

    <CrudLayout>
      <template #filter>
        <FilterPanel :has-filters="hasFilters" @reset="resetFilters">
          <FilterGroup label="Periode">
            <div class="flex flex-col gap-2">
              <div class="flex flex-col gap-0.5">
                <span class="text-[10px] text-muted">Dari</span>
                <DateField v-model="begin" />
              </div>
              <div class="flex flex-col gap-0.5">
                <span class="text-[10px] text-muted">Sampai</span>
                <DateField v-model="end" />
              </div>
            </div>
          </FilterGroup>

          <FilterGroup label="Tipe Tanggal">
            <div class="flex gap-1">
              <button
                v-for="opt in [{ v: 'actual', l: 'Aktual' }, { v: 'transaction', l: 'Transaksi' }]"
                :key="opt.v"
                type="button"
                :class="[
                  'text-[11px] px-2.5 py-0.5 rounded-full border transition-colors',
                  dateType === opt.v
                    ? 'bg-primary text-primary-foreground border-primary font-medium'
                    : 'border-border text-muted hover:bg-background hover:text-foreground',
                ]"
                @click="dateType = opt.v"
              >{{ opt.l }}</button>
            </div>
          </FilterGroup>

          <FilterGroup label="Urut Berdasar">
            <select
              v-model="sortBy"
              class="w-full rounded-lg border border-border bg-surface px-2 py-1.5 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="actual_date">Tgl Aktual</option>
              <option value="transaction_date">Tgl Transaksi</option>
              <option value="transaction_no">No Transaksi</option>
              <option value="donor_no">No Donatur</option>
              <option value="donor_name">Nama Donatur</option>
              <option value="channel_name">Rekening</option>
            </select>
          </FilterGroup>

          <FilterGroup label="Cari">
            <div class="flex flex-col gap-1.5">
              <select
                v-model="searchCategory"
                class="w-full rounded-lg border border-border bg-surface px-2 py-1.5 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              >
                <option value="none">(Semua kolom)</option>
                <option value="transno">No Transaksi</option>
                <option value="donorno">No Donatur</option>
                <option value="donorname">Nama Donatur</option>
                <option value="description">Keterangan</option>
                <option value="refno">No Referensi</option>
              </select>
              <input
                v-model="searchText"
                :disabled="searchCategory === 'none'"
                placeholder="Ketik kata kunci..."
                class="w-full rounded-lg border border-border bg-surface px-2 py-1.5 text-[11px] disabled:opacity-40 focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </FilterGroup>

          <FilterGroup label="Rekening Kas/Bank">
            <input
              v-model="cashAccountNo"
              placeholder="Opsional"
              class="w-full rounded-lg border border-border bg-surface px-2 py-1.5 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </FilterGroup>

        </FilterPanel>
      </template>

      <template #data>
        <DataPanel
          title="Daftar Transaksi"
          :row-count="rows.length"
          :total="hasLoaded ? total : undefined"
          :loading="loading"
          :is-empty="hasLoaded && !loading && rows.length === 0"
        >
          <template #empty>Tidak ada transaksi dalam rentang tanggal ini</template>

          <div v-if="!hasLoaded && !loading" class="py-10 text-center text-xs text-muted">
            Atur filter lalu klik "Tampilkan"
          </div>

          <template v-else-if="rows.length">
            <!-- Pagination di atas tabel (standard) -->
            <div v-if="hasLoaded && totalPages > 1" class="px-4 py-2 border-b border-border flex items-center justify-end">
              <TablePagination
                :page="page"
                :total-pages="totalPages"
                :total="total"
                :page-size="pageSize"
                :loading="loading"
                unit="transaksi"
                @prev="goto(page - 1)"
                @next="goto(page + 1)"
                @update:page-size="pageSize = $event; goto(1)"
              />
            </div>

          <div class="overflow-x-auto">
            <table class="w-full text-[11px]">
              <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
                <tr>
                  <th class="px-3 py-1.5 text-left font-semibold">No Transaksi</th>
                  <th class="px-3 py-1.5 text-left font-semibold">Rekening</th>
                  <th class="px-3 py-1.5 text-left font-semibold whitespace-nowrap">Tgl Aktual</th>
                  <th class="px-3 py-1.5 text-left font-semibold whitespace-nowrap">Tgl Trans</th>
                  <th class="px-3 py-1.5 text-right font-semibold">Nominal</th>
                  <th class="px-3 py-1.5 text-left font-semibold min-w-[120px]">Nama Donatur</th>
                  <th class="px-3 py-1.5 text-left font-semibold min-w-[140px]">Keterangan</th>
                  <th class="px-3 py-1.5 text-left font-semibold">Inputer</th>
                  <th class="px-3 py-1.5 text-left font-semibold">Status</th>
                  <th class="px-3 py-1.5 text-left font-semibold">Posted</th>
                  <th class="px-3 py-1.5 text-center font-semibold w-12">Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="row in rows"
                  :key="row.transactionid"
                  class="border-b border-border/40 transition-colors hover:bg-muted/5 cursor-pointer"
                  @click="goToDetail(row.transactionid)"
                >
                  <td class="px-3 py-1 font-mono text-[10px] text-muted">{{ row.transactionno ?? '—' }}</td>
                  <td class="px-3 py-1 max-w-[110px] truncate" :title="row.channelname ?? ''">{{ row.channelname ?? '—' }}</td>
                  <td class="px-3 py-1 whitespace-nowrap">{{ dmy(row.actualdate) }}</td>
                  <td class="px-3 py-1 whitespace-nowrap">{{ dmy(row.transactiondate) }}</td>
                  <td class="px-3 py-1 text-right tabular-nums">{{ fmt(row.amount) }}</td>
                  <td class="px-3 py-1 max-w-[130px] truncate" :title="row.donorname ?? ''">{{ row.donorname ?? '' }}</td>
                  <td class="px-3 py-1 max-w-[180px] truncate" :title="row.description ?? ''">{{ row.description ?? '' }}</td>
                  <td class="px-3 py-1">{{ row.inputer ?? '' }}</td>
                  <td class="px-3 py-1">
                    <span :class="['rounded px-1 py-0.5 text-[9px] font-medium uppercase', authChip(row.authstatus)]">{{ authLabel(row.authstatus) }}</span>
                  </td>
                  <td class="px-3 py-1">
                    <span :class="['rounded px-1 py-0.5 text-[9px] font-medium', postedChip(row.isposted)]">{{ row.isposted === 'T' ? 'Posted' : 'Belum' }}</span>
                  </td>
                  <td class="px-3 py-1 text-center" @click.stop>
                    <Button
                      v-if="canDelete(row)"
                      size="sm"
                      variant="outline"
                      class="border-red-200 text-red-600 hover:bg-red-50 px-1.5 py-0.5 text-[10px]"
                      @click="deleteConfirmId = row.transactionid; deleteMsg = null"
                    >Hapus</Button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          </template>
        </DataPanel>
      </template>
    </CrudLayout>

    <TransaksiDeleteDialog
      v-if="deleteConfirmId !== null"
      :transaction-id="deleteConfirmId"
      :message="deleteMsg"
      :deleting="deleting"
      @cancel="deleteConfirmId = null; deleteMsg = null"
      @confirm="confirmDelete"
    />
  </div>
</template>

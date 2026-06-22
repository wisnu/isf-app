<script setup lang="ts">
import { Eye, Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref, shallowRef, watch } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { dmy } from '@/shared/utils/date'
import { formatIdr } from '@/shared/utils/format'

// ── Types ─────────────────────────────────────────────────────────────────────

interface RealizationDetailRow {
  realization_detail_id: number
  mustahiq_product_id: number
  product_name: string | null
  mustahiq_name: string | null
  program_detail_name: string | null
  account_no: string | null
  account_name: string | null
  memo_amount: number
  realization_amount: number
  ashnaf: string | null
  fund_product_id: number | null
}

interface RealizationRow {
  realization_id: number
  realization_date: string | null
  realization_description: string | null
  realization_location: string | null
  memo_number: string | null
  memo_id: number | null
  status_receivables: string | null
  status_reclpj: string | null
  branch_code: string | null
  realization_amount: number | null
}

interface RealizationDetail extends RealizationRow {
  details: RealizationDetailRow[]
  budgets: number[]
  partners: number[]
}

interface PaginationState {
  page: number
  page_size: number
  total: number
  total_pages: number
}

interface MemoLookupItem {
  realization_memo_id: number
  realization_memo_number: string | null
  realization_memo_date: string | null
  realization_memo_amount: number | null
  realization_memo_subject: string | null
}

interface MemoDetailItem {
  mustahiq_product_id: number
  product_name: string | null
  mustahiq_name: string | null
  program_detail_name: string | null
  account_no: string | null
  account_name: string | null
  memo_amount: number
  ashnaf: string | null
  fund_product_id: number | null
  proposal_date: string | null
  proposal_nominal: number | null
  proposal_reference_by: string | null
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_PREFIX = '/api/distribution/realization/non-regular'
const PAGE_TITLE = 'Realisasi Program Non Rutin'
const REALIZATION_TYPE = 'N'

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()

const rows       = ref<RealizationRow[]>([])
const loading    = shallowRef(false)
const errorMsg   = shallowRef<string | null>(null)
const hasLoaded  = shallowRef(false)
const page       = shallowRef(1)
const pageSize   = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec   = shallowRef(0)

// filters
const filterDateFrom = ref('')
const filterDateTo   = ref('')

// show count
const from = computed(() => rows.value.length === 0 ? 0 : (page.value - 1) * pageSize.value + 1)
const to   = computed(() => (page.value - 1) * pageSize.value + rows.value.length)

// ── Load Data ─────────────────────────────────────────────────────────────────

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params: Record<string, string | number> = { page: page.value, page_size: pageSize.value }
    if (filterDateFrom.value)        params.date_from = filterDateFrom.value
    if (filterDateTo.value)          params.date_to   = filterDateTo.value

    const res = await api.get<{ rows: RealizationRow[]; pagination: PaginationState }>(API_PREFIX, params)
    rows.value       = res.rows
    totalPages.value = res.pagination.total_pages
    totalRec.value   = res.pagination.total
    pageSize.value   = res.pagination.page_size
    hasLoaded.value  = true
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    toast.error(errorMsg.value ?? 'Gagal memuat data')
  } finally {
    loading.value = false
  }
}

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

// ── Memo Lookup ────────────────────────────────────────────────────────────────

const memoLookup    = ref<MemoLookupItem[]>([])
const memoSearch    = ref('')
const memoLoading   = shallowRef(false)

async function loadMemos(q: string) {
  memoLoading.value = true
  try {
    const params: Record<string, string> = {}
    if (q.trim()) params.search = q.trim()
    const res = await api.get<{ data: MemoLookupItem[] }>(`${API_PREFIX}/lookup/memos`, params)
    memoLookup.value = res.data
  } catch { /* non-critical */ } finally {
    memoLoading.value = false
  }
}

watch(memoSearch, (q) => {
  clearTimeout(memoSearchTimer)
  memoSearchTimer = window.setTimeout(() => loadMemos(q), 300)
})
let memoSearchTimer = 0

// ── Form Modal State ──────────────────────────────────────────────────────────

const showForm  = shallowRef(false)
const formMode  = shallowRef<'create' | 'edit' | 'view'>('create')
const formLoading = shallowRef(false)

interface FormState {
  realization_id: number | null
  realization_date: string
  realization_description: string
  realization_location: string
  memo_id: number | null
  memo_number: string
  memo_date: string
  status_receivables: string
  employee_id: string
  details: FormDetail[]
}

interface FormDetail {
  _key: number
  realization_detail_id: number | null
  mustahiq_product_id: number
  product_name: string
  mustahiq_name: string
  program_detail_name: string
  account_no: string
  account_name: string
  memo_amount: number
  realization_amount: number
}

let detailKeySeq = 0

const form = reactive<FormState>({
  realization_id: null,
  realization_date: '',
  realization_description: '',
  realization_location: '',
  memo_id: null,
  memo_number: '',
  memo_date: '',
  status_receivables: 'T',
  employee_id: '',
  details: [],
})

const selectedMemo = ref<MemoLookupItem | null>(null)
const totalMemoAmount = computed(() => form.details.reduce((s, d) => s + (d.memo_amount || 0), 0))
const totalRealizationAmount = computed(() => form.details.reduce((s, d) => s + (d.realization_amount || 0), 0))

function openCreate() {
  formMode.value = 'create'
  Object.assign(form, {
    realization_id: null,
    realization_date: '',
    realization_description: '',
    realization_location: '',
    memo_id: null,
    memo_number: '',
    memo_date: '',
    status_receivables: 'T',
    employee_id: '',
    details: [],
  })
  selectedMemo.value = null
  memoSearch.value = ''
  memoLookup.value = []
  showForm.value = true
}

async function openEdit(row: RealizationRow) {
  formMode.value = 'edit'
  formLoading.value = true
  showForm.value = true
  try {
    const detail = await api.get<RealizationDetail>(`${API_PREFIX}/${row.realization_id}`)
    Object.assign(form, {
      realization_id: detail.realization_id,
      realization_date: detail.realization_date ?? '',
      realization_description: detail.realization_description ?? '',
      realization_location: detail.realization_location ?? '',
      memo_id: detail.memo_id,
      memo_number: detail.memo_number ?? '',
      memo_date: detail.realization_date ?? '',  // Use realization date as reference
      status_receivables: detail.status_receivables ?? 'T',
      employee_id: '',  // API doesn't return this yet
      details: detail.details.map(d => ({
        _key: ++detailKeySeq,
        realization_detail_id: d.realization_detail_id,
        mustahiq_product_id: d.mustahiq_product_id,
        product_name: d.product_name ?? '',
        mustahiq_name: d.mustahiq_name ?? '',
        program_detail_name: d.program_detail_name ?? '',
        account_no: d.account_no ?? '',
        account_name: d.account_name ?? '',
        memo_amount: d.memo_amount,
        realization_amount: d.realization_amount,
      })),
    })
    if (detail.memo_id) {
      selectedMemo.value = {
        realization_memo_id: detail.memo_id,
        realization_memo_number: detail.memo_number,
        realization_memo_date: '',
        realization_memo_amount: null,
        realization_memo_subject: null,
      }
    }
    memoSearch.value = ''
    memoLookup.value = []
  } catch (e) {
    toast.error('Gagal memuat detail realisasi')
    showForm.value = false
  } finally {
    formLoading.value = false
  }
}

async function openView(row: RealizationRow) {
  formMode.value = 'view'
  formLoading.value = true
  showForm.value = true
  try {
    const detail = await api.get<RealizationDetail>(`${API_PREFIX}/${row.realization_id}`)
    Object.assign(form, {
      realization_id: detail.realization_id,
      realization_date: detail.realization_date ?? '',
      realization_description: detail.realization_description ?? '',
      realization_location: detail.realization_location ?? '',
      memo_id: detail.memo_id,
      memo_number: detail.memo_number ?? '',
      memo_date: detail.realization_date ?? '',
      status_receivables: detail.status_receivables ?? 'T',
      employee_id: '',
      details: detail.details.map(d => ({
        _key: ++detailKeySeq,
        realization_detail_id: d.realization_detail_id,
        mustahiq_product_id: d.mustahiq_product_id,
        product_name: d.product_name ?? '',
        mustahiq_name: d.mustahiq_name ?? '',
        program_detail_name: d.program_detail_name ?? '',
        account_no: d.account_no ?? '',
        account_name: d.account_name ?? '',
        memo_amount: d.memo_amount,
        realization_amount: d.realization_amount,
      })),
    })
    memoSearch.value = ''
    memoLookup.value = []
  } catch (e) {
    toast.error('Gagal memuat detail realisasi')
    showForm.value = false
  } finally {
    formLoading.value = false
  }
}

// ── Memo Picker ───────────────────────────────────────────────────────────────

async function selectMemo(m: MemoLookupItem) {
  selectedMemo.value = m
  form.memo_id = m.realization_memo_id
  form.memo_number = m.realization_memo_number ?? ''
  form.memo_date = m.realization_memo_date ?? ''
  memoSearch.value = ''
  memoLookup.value = []

  // Fetch memo detail and populate grid
  try {
    formLoading.value = true
    const memoDetails = await api.get<{ data: MemoDetailItem[] }>(
      `${API_PREFIX}/lookup/memo-detail/${m.realization_memo_id}`
    )
    form.details = memoDetails.data.map(md => ({
      _key: ++detailKeySeq,
      realization_detail_id: null,
      mustahiq_product_id: md.mustahiq_product_id,
      product_name: md.product_name ?? '',
      mustahiq_name: md.mustahiq_name ?? '',
      program_detail_name: md.program_detail_name ?? '',
      account_no: md.account_no ?? '',
      account_name: md.account_name ?? '',
      memo_amount: md.memo_amount,
      realization_amount: md.memo_amount,  // Default to memo amount
    }))
  } catch (e) {
    toast.error('Gagal memuat detail memo')
  } finally {
    formLoading.value = false
  }
}

// ── Save ──────────────────────────────────────────────────────────────────────

async function save() {
  if (!form.realization_date) { toast.error('Tanggal realisasi harus diisi'); return }
  if (!form.memo_id) { toast.error('Memo harus dipilih'); return }
  if (!form.realization_description.trim()) { toast.error('Deskripsi realisasi harus diisi'); return }
  if (!form.realization_location.trim()) { toast.error('Lokasi realisasi harus diisi'); return }
  if (form.status_receivables === 'Y' && !form.employee_id?.trim()) {
    toast.error('Karyawan PJ Piutang harus diisi jika status piutang = Ya')
    return
  }
  if (form.details.length === 0) { toast.error('Pilih memo terlebih dahulu untuk mengisi detail realisasi'); return }

  formLoading.value = true
  try {
    const body = {
      realization_date:    form.realization_date,
      description:         form.realization_description.trim(),
      location:            form.realization_location.trim(),
      memo_id:             form.memo_id,
      status_receivables:  form.status_receivables,
      employee_id:         form.employee_id?.trim() || null,
      details: form.details.map(d => ({
        mustahiq_product_id: d.mustahiq_product_id,
        realization_amount:  d.realization_amount,
        detail_description:  null,
      })),
      budgets:  null,
      partners: null,
    }

    if (formMode.value === 'create') {
      await api.post(API_PREFIX, body)
      toast.success('Realisasi berhasil dibuat')
    } else {
      await api.put(`${API_PREFIX}/${form.realization_id}`, body)
      toast.success('Realisasi berhasil diperbarui')
    }
    showForm.value = false
    page.value = 1
    load()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan realisasi')
  } finally {
    formLoading.value = false
  }
}

// ── Delete ────────────────────────────────────────────────────────────────────

const showDeleteModal = shallowRef(false)
const deleteTarget    = ref<RealizationRow | null>(null)
const deleteLoading   = shallowRef(false)

function openDelete(row: RealizationRow) {
  deleteTarget.value = row
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleteLoading.value = true
  try {
    await api.delete(`${API_PREFIX}/${deleteTarget.value.realization_id}`)
    toast.success('Realisasi berhasil dihapus')
    showDeleteModal.value = false
    deleteTarget.value = null
    load()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menghapus realisasi')
  } finally {
    deleteLoading.value = false
  }
}

// ── Detail row remove ─────────────────────────────────────────────────────────

function removeDetail(key: number) {
  const idx = form.details.findIndex(d => d._key === key)
  if (idx >= 0) form.details.splice(idx, 1)
}

// ── Status badges ─────────────────────────────────────────────────────────────

function getStatusBadgeClass(status: string | null) {
  if (status === 'Y') return 'bg-amber-100 text-amber-700'
  return 'bg-zinc-100 text-zinc-500'
}

function getStatusBadgeText(status: string | null) {
  if (status === 'Y') return 'Piutang'
  return 'Non Piutang'
}

function getLpjBadgeClass(status: string | null) {
  if (status === 'Y') return 'bg-emerald-100 text-emerald-700'
  return 'bg-zinc-100 text-zinc-500'
}

function getLpjBadgeText(status: string | null) {
  if (status === 'Y') return 'Ada LPJ'
  return '-'
}
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <h1 class="text-lg font-semibold text-zinc-800">{{ PAGE_TITLE }}</h1>
      </div>
      <Button size="sm" class="gap-1.5" @click="openCreate">
        <Plus class="w-4 h-4" />
        Tambah
      </Button>
    </div>

    <!-- Error -->
    <div v-if="errorMsg" class="rounded border border-red-200 bg-red-50 px-4 py-2 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Table Container -->
    <div class="space-y-0">

      <!-- Toolbar -->
      <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3">
        <div class="flex items-end gap-2">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-500">Dari</label>
            <DateField v-model="filterDateFrom" />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai</label>
            <DateField v-model="filterDateTo" />
          </div>
        </div>
        <Button size="sm" class="gap-1.5 h-9 text-xs" :disabled="loading" @click="() => { page = 1; load() }">
          <Search class="w-3.5 h-3.5" />
          {{ loading ? 'Memuat...' : 'Tampilkan' }}
        </Button>
      </div>

      <!-- Count + Pagination -->
      <div class="flex items-center justify-between border-x bg-white px-4 py-2">
        <span class="text-xs text-zinc-500">
          <template v-if="!hasLoaded">Klik Tampilkan untuk memuat data</template>
          <template v-else-if="totalRec === 0">Tidak ada data</template>
          <template v-else>Showing {{ from }}–{{ to }} of <strong>{{ totalRec }}</strong> records</template>
        </span>
        <TablePagination
          v-if="hasLoaded && totalPages > 1"
          :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @goto="goto"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto rounded-b border border-surface-200">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] uppercase tracking-widest border-b border-surface-200 bg-zinc-50 text-zinc-500">
            <tr>
              <th class="px-4 py-2 text-left">Tanggal</th>
              <th class="px-4 py-2 text-left">Deskripsi</th>
              <th class="px-4 py-2 text-left">Nomor Memo</th>
              <th class="px-4 py-2 text-right">Total Realisasi</th>
              <th class="px-4 py-2 text-center">Status Piutang</th>
              <th class="px-4 py-2 text-center">Status LPJ</th>
              <th class="px-4 py-2 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="!hasLoaded">
              <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
                Pilih filter lalu klik Tampilkan untuk melihat data.
              </td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="7" class="px-4 py-8 text-center text-zinc-400">
                Tidak ada realisasi dalam periode ini.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.realization_id"
              class="border-b border-surface-200 last:border-0 hover:bg-zinc-50"
            >
              <td class="px-4 py-2">{{ dmy(row.realization_date) }}</td>
              <td class="px-4 py-2 max-w-[200px] truncate" :title="row.realization_description ?? ''">
                {{ row.realization_description ?? '-' }}
              </td>
              <td class="px-4 py-2 font-mono">{{ row.memo_number ?? '-' }}</td>
              <td class="px-4 py-2 text-right font-mono">
                {{ formatIdr(row.realization_amount ?? 0) }}
              </td>
              <td class="px-4 py-2 text-center">
                <span :class="['px-1.5 py-px rounded text-[10px] font-semibold', getStatusBadgeClass(row.status_receivables)]">
                  {{ getStatusBadgeText(row.status_receivables) }}
                </span>
              </td>
              <td class="px-4 py-2 text-center">
                <span :class="['px-1.5 py-px rounded text-[10px] font-semibold', getLpjBadgeClass(row.status_reclpj)]">
                  {{ getLpjBadgeText(row.status_reclpj) }}
                </span>
              </td>
              <td class="px-4 py-2 text-center">
                <div class="flex items-center justify-center gap-1">
                  <button
                    class="rounded border border-zinc-300 p-1 hover:bg-zinc-100 transition"
                    title="Lihat"
                    @click="openView(row)"
                  >
                    <Eye class="w-3 h-3 text-zinc-600" />
                  </button>
                  <button
                    class="rounded border border-zinc-300 p-1 hover:bg-zinc-100 transition"
                    title="Edit"
                    @click="openEdit(row)"
                  >
                    <Pencil class="w-3 h-3 text-zinc-600" />
                  </button>
                  <button
                    class="rounded border border-red-300 p-1 hover:bg-red-50 transition"
                    title="Hapus"
                    @click="openDelete(row)"
                  >
                    <Trash2 class="w-3 h-3 text-red-500" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Form Modal ──────────────────────────────────────────────────────── -->
    <Modal
      v-model:open="showForm"
      :title="formMode === 'create' ? 'Tambah Realisasi Program Non Rutin' : formMode === 'edit' ? 'Edit Realisasi Program Non Rutin' : 'Lihat Realisasi Program Non Rutin'"
      size="2xl"
    >
      <div v-if="formLoading && formMode !== 'create'" class="flex items-center justify-center py-12 text-zinc-400">
        Memuat data...
      </div>
      <div v-else class="space-y-6">
        <!-- Header fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Tanggal Realisasi <span class="text-red-500">*</span></label>
            <DateField v-model="form.realization_date" :disabled="formMode === 'view'" />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Status Piutang <span class="text-red-500">*</span></label>
            <select
              v-model="form.status_receivables"
              :disabled="formMode === 'view'"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary disabled:bg-zinc-100 disabled:text-zinc-500"
            >
              <option value="T">Tidak</option>
              <option value="Y">Ya</option>
            </select>
          </div>
        </div>

        <!-- Description & Location -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Deskripsi <span class="text-red-500">*</span></label>
            <input
              v-model="form.realization_description"
              :disabled="formMode === 'view'"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary disabled:bg-zinc-100 disabled:text-zinc-500"
              placeholder="Deskripsi realisasi..."
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Lokasi <span class="text-red-500">*</span></label>
            <input
              v-model="form.realization_location"
              :disabled="formMode === 'view'"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary disabled:bg-zinc-100 disabled:text-zinc-500"
              placeholder="Lokasi realisasi..."
            />
          </div>
        </div>

        <!-- Memo Picker -->
        <div v-if="formMode !== 'view'" class="rounded border border-dashed border-zinc-300 p-4 space-y-3">
          <p class="text-xs font-semibold text-zinc-600 uppercase tracking-wide">Pilih Memo <span class="text-red-500">*</span></p>
          <div>
            <label class="mb-1 block text-xs text-zinc-500">Cari Memo</label>
            <input
              v-model="memoSearch"
              :disabled="formMode === 'view'"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary disabled:bg-zinc-100 disabled:text-zinc-500"
              placeholder="Nomor / perihal memo..."
            />
          </div>

          <!-- Memo Search Results -->
          <div v-if="memoLookup.length > 0 || memoLoading" class="max-h-40 overflow-y-auto rounded border bg-white text-xs">
            <div v-if="memoLoading" class="px-3 py-2 text-zinc-400">Mencari...</div>
            <button
              v-for="m in memoLookup.slice(0, 50)"
              :key="m.realization_memo_id"
              class="flex w-full items-center gap-2 px-3 py-2 text-left hover:bg-primary/10 transition"
              :class="selectedMemo?.realization_memo_id === m.realization_memo_id ? 'bg-primary/10 font-semibold' : ''"
              @click="selectMemo(m)"
            >
              <span class="flex-1 truncate">{{ m.realization_memo_number }} — {{ dmy(m.realization_memo_date) }}</span>
              <span class="font-mono text-zinc-400">{{ formatIdr(m.realization_memo_amount ?? 0) }}</span>
            </button>
          </div>

          <p v-if="selectedMemo" class="text-xs text-primary">
            Dipilih: <strong>{{ selectedMemo.realization_memo_number }}</strong>
          </p>
        </div>

        <!-- Memo Info (view mode) -->
        <div v-if="formMode === 'view'" class="rounded border bg-zinc-50 px-4 py-3 space-y-1 text-xs">
          <div><span class="text-zinc-500">Nomor Memo:</span> <strong>{{ form.memo_number }}</strong></div>
          <div><span class="text-zinc-500">Tanggal Memo:</span> {{ dmy(form.memo_date) }}</div>
        </div>

        <!-- Employee PJ (only if status_receivables === 'Y') -->
        <div v-if="form.status_receivables === 'Y'" class="grid grid-cols-1 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Karyawan PJ Piutang <span class="text-red-500">*</span></label>
            <input
              v-model="form.employee_id"
              :disabled="formMode === 'view'"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary disabled:bg-zinc-100 disabled:text-zinc-500"
              placeholder="Nama / ID karyawan..."
            />
          </div>
        </div>

        <!-- Detail Realisasi (grid) -->
        <div v-if="form.details.length > 0">
          <p class="mb-2 text-xs font-semibold text-zinc-600 uppercase tracking-wide">Detail Realisasi ({{ form.details.length }})</p>
          <div class="overflow-x-auto rounded border">
            <table class="w-full text-xs">
              <thead class="bg-zinc-50 border-b text-[10px] uppercase tracking-widest text-zinc-500">
                <tr>
                  <th class="px-3 py-2 text-left">Program</th>
                  <th class="px-3 py-2 text-left">Mustahiq</th>
                  <th class="px-3 py-2 text-left">Sumber Dana</th>
                  <th class="px-3 py-2 text-right">Nominal Memo</th>
                  <th class="px-3 py-2 text-right">Nominal Realisasi</th>
                  <th v-if="formMode !== 'view'" class="px-3 py-2 text-center"></th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="d in form.details"
                  :key="d._key"
                  class="border-b last:border-0"
                >
                  <td class="px-3 py-2">{{ d.program_detail_name || d.product_name }}</td>
                  <td class="px-3 py-2 text-zinc-500">{{ d.mustahiq_name }}</td>
                  <td class="px-3 py-2 text-zinc-500">{{ d.account_name || d.account_no || '-' }}</td>
                  <td class="px-3 py-2 text-right font-mono">{{ formatIdr(d.memo_amount) }}</td>
                  <td class="px-3 py-2 text-right font-mono">
                    <template v-if="formMode === 'view'">
                      {{ formatIdr(d.realization_amount) }}
                    </template>
                    <template v-else>
                      <input
                        v-model.number="d.realization_amount"
                        type="number"
                        min="0"
                        class="w-24 rounded border px-2 py-1 text-right text-xs focus:outline-none focus:ring-1 focus:ring-primary"
                      />
                    </template>
                  </td>
                  <td v-if="formMode !== 'view'" class="px-3 py-2 text-center">
                    <button class="text-red-400 hover:text-red-600 transition" @click="removeDetail(d._key)">
                      <X class="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Totals -->
          <div class="mt-2 space-y-1 text-xs">
            <div class="flex justify-between px-2">
              <span class="text-zinc-600">Total Memo:</span>
              <span class="font-mono font-semibold">{{ formatIdr(totalMemoAmount) }}</span>
            </div>
            <div class="flex justify-between px-2 border-t pt-1">
              <span class="text-zinc-600">Total Realisasi:</span>
              <span class="font-mono font-semibold text-primary">{{ formatIdr(totalRealizationAmount) }}</span>
            </div>
          </div>
        </div>
        <p v-else class="text-xs text-zinc-400 italic">Belum ada detail. Pilih memo terlebih dahulu.</p>
      </div>

      <template #footer>
        <Button variant="outline" @click="showForm = false">{{ formMode === 'view' ? 'Tutup' : 'Batal' }}</Button>
        <Button v-if="formMode !== 'view'" variant="success" :disabled="formLoading" @click="save">
          {{ formLoading ? 'Menyimpan...' : 'Simpan' }}
        </Button>
      </template>
    </Modal>

    <!-- ── Delete Confirmation Modal ──────────────────────────────────────── -->
    <Modal v-model:open="showDeleteModal" title="Hapus Realisasi Program Non Rutin" size="sm">
      <div class="space-y-3 text-sm">
        <p>Anda akan menghapus realisasi berikut:</p>
        <div class="rounded border bg-zinc-50 px-4 py-3 space-y-1 text-xs">
          <div><span class="text-zinc-500">Tanggal:</span> <strong>{{ dmy(deleteTarget?.realization_date) }}</strong></div>
          <div><span class="text-zinc-500">Nomor Memo:</span> <strong>{{ deleteTarget?.memo_number }}</strong></div>
          <div><span class="text-zinc-500">Deskripsi:</span> {{ deleteTarget?.realization_description }}</div>
          <div><span class="text-zinc-500">Lokasi:</span> {{ deleteTarget?.realization_location }}</div>
          <div><span class="text-zinc-500">Total Realisasi:</span> <strong class="font-mono">{{ formatIdr(deleteTarget?.realization_amount ?? 0) }}</strong></div>
          <div><span class="text-zinc-500">Status Piutang:</span> {{ deleteTarget?.status_receivables === 'Y' ? 'Piutang' : 'Non Piutang' }}</div>
        </div>
        <p class="text-red-600 text-xs">Tindakan ini tidak dapat dibatalkan. Semua detail realisasi akan ikut terhapus.</p>
      </div>
      <template #footer>
        <Button variant="outline" @click="showDeleteModal = false">Batal</Button>
        <Button variant="destructive" :disabled="deleteLoading" @click="confirmDelete">
          {{ deleteLoading ? 'Menghapus...' : 'Hapus' }}
        </Button>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { Eye, Pencil, Plus, Search, Trash2, X, ChevronDown, ChevronUp } from 'lucide-vue-next'
import { computed, reactive, ref, shallowRef, watch } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { dmy } from '@/shared/utils/date'

// ── Types ─────────────────────────────────────────────────────────────────────

interface RealizationReturnRow {
  return_id: number
  return_date: string | null
  return_description: string | null
  return_amount: number | null
  realization_amount: number | null
  memo_number: string | null
  branch_code: string | null
}

interface DetailRow {
  return_detail_id: number
  realization_detail_id: number
  mustahiq_product_id: number | null
  mustahiq_product_name: string | null
  account_no: string | null
  account_name: string | null
  realization_amount: number | null
  return_amount: number | null
  detail_description: string | null
}

interface CostRow {
  cost_id: number
  cost_item_id: number | null
  cost_item_code: string | null
  cost_item_description: string | null
  cost_amount: number | null
}

interface RealizationReturnDetail {
  return_id: number
  return_date: string | null
  return_description: string | null
  return_amount: number | null
  cost_amount: number | null
  realization_id: number | null
  realization_date: string | null
  realization_description: string | null
  realization_amount: number | null
  memo_number: string | null
  branch_code: string | null
  details: DetailRow[]
  costs: CostRow[]
}

interface CostItem {
  cost_item_id: number
  cost_item_code: string
  cost_item_description: string
}

interface RealizationLookup {
  realization_id: number
  realization_date: string | null
  realization_description: string | null
  realization_amount: number | null
  realization_type: string | null
  memo_number: string | null
}

interface RealizationDetailLookup {
  realization_detail_id: number
  realization_amount: number | null
  account_no: string | null
  account_name: string | null
  mustahiq_product_id: number | null
  mustahiq_product_name: string | null
}

interface FormDetailRow {
  realization_detail_id: number
  mustahiq_product_id: number | null
  mustahiq_product_name: string | null
  account_no: string | null
  account_name: string | null
  realization_amount: number
  return_amount: number | null
  detail_description: string
}

interface FormCostRow {
  _key: number
  cost_item_id: number | null
  cost_item_description: string | null
  cost_amount: number | null
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_PREFIX = '/api/distribution/realization-return'

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()

const rows = ref<RealizationReturnRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const hasLoaded = shallowRef(false)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)

const beginDate = ref(getTodayISO())
const endDate = ref(getTodayISO())

// Modal state
const showForm = shallowRef(false)
const formMode = shallowRef<'create' | 'edit' | 'view'>('create')
const showDelete = shallowRef(false)
const selected = ref<RealizationReturnDetail | null>(null)
const formSaving = shallowRef(false)

// Cost items lookup
const costItems = ref<CostItem[]>([])
const costItemOptions = computed(() =>
  costItems.value.map((ci) => ({
    value: String(ci.cost_item_id),
    label: `${ci.cost_item_code} - ${ci.cost_item_description}`,
  })),
)

// Search realization dialog
const showSearchRealization = shallowRef(false)
const realizationSearchQuery = ref('')
const realizationTypeFilter = ref('')
const realizationRows = ref<RealizationLookup[]>([])
const realizationSearchPage = shallowRef(1)
const realizationSearchTotal = shallowRef(0)
const realizationSearchLoading = shallowRef(false)

// Form state
const form = reactive({
  return_date: '',
  return_description: '',
  realization_id: null as number | null,
  // read-only auto-fills
  realization_date: '',
  realization_description: '',
  memo_number: '',
  total_realization: 0,
  // detail grid (filled from realization)
  details: [] as FormDetailRow[],
  // cost grid (user-managed)
  costs: [] as FormCostRow[],
})

let _costKey = 0

function getTodayISO(): string {
  return new Date().toISOString().split('T')[0]
}

// ── Computed totals ───────────────────────────────────────────────────────────

const totalReturn = computed(() =>
  form.details.reduce((s, d) => s + (d.return_amount ?? 0), 0),
)

const totalCost = computed(() =>
  form.costs.reduce((s, c) => s + (c.cost_amount ?? 0), 0),
)

const totalBalance = computed(() => totalReturn.value + totalCost.value)

const balanceOk = computed(() =>
  form.details.length === 0 || Math.abs(totalBalance.value - form.total_realization) < 0.01,
)

const isReadOnly = computed(() => formMode.value === 'view')

// ── API Calls ─────────────────────────────────────────────────────────────────

async function loadData() {
  if (!hasLoaded.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      begin_date: beginDate.value,
      end_date: endDate.value,
      page: String(page.value),
      page_size: String(pageSize.value),
    })
    const res = await api.get<{
      rows: RealizationReturnRow[]
      pagination: { page: number; page_size: number; total: number; total_pages: number }
    }>(`${API_PREFIX}?${params}`)
    rows.value = res.rows
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
}

async function tampilkan() {
  page.value = 1
  hasLoaded.value = true
  await loadData()
}

watch(page, loadData)

async function loadCostItems() {
  if (costItems.value.length > 0) return
  try {
    const res = await api.get<{ items: CostItem[] }>(`${API_PREFIX}/lookup/cost-items`)
    costItems.value = res.items
  } catch {
    // ignore — show empty
  }
}

async function searchRealizations() {
  realizationSearchLoading.value = true
  try {
    const params = new URLSearchParams({
      page: String(realizationSearchPage.value),
      page_size: '20',
    })
    if (realizationSearchQuery.value.trim())
      params.set('search', realizationSearchQuery.value.trim())
    if (realizationTypeFilter.value)
      params.set('realization_type', realizationTypeFilter.value)

    const res = await api.get<{
      rows: RealizationLookup[]
      pagination: { total: number }
    }>(`${API_PREFIX}/lookup/realizations?${params}`)
    realizationRows.value = res.rows
    realizationSearchTotal.value = res.pagination.total
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat data realisasi', life: 3000 })
  } finally {
    realizationSearchLoading.value = false
  }
}

async function loadRealizationDetails(realizationId: number) {
  try {
    const res = await api.get<{ rows: RealizationDetailLookup[] }>(
      `${API_PREFIX}/realization/${realizationId}/details`,
    )
    form.details = res.rows.map((r) => ({
      realization_detail_id: r.realization_detail_id,
      mustahiq_product_id: r.mustahiq_product_id,
      mustahiq_product_name: r.mustahiq_product_name,
      account_no: r.account_no,
      account_name: r.account_name,
      realization_amount: r.realization_amount ?? 0,
      return_amount: null,
      detail_description: '',
    }))
    form.total_realization = res.rows.reduce((s, r) => s + (r.realization_amount ?? 0), 0)
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat detail realisasi', life: 3000 })
  }
}

async function getDetail(returnId: number): Promise<RealizationReturnDetail | null> {
  try {
    const res = await api.get<RealizationReturnDetail>(`${API_PREFIX}/${returnId}`)
    return res
  } catch {
    toast.add({ severity: 'error', summary: 'Gagal', detail: 'Gagal memuat detail data', life: 3000 })
    return null
  }
}

// ── Form Actions ──────────────────────────────────────────────────────────────

function resetForm() {
  form.return_date = getTodayISO()
  form.return_description = ''
  form.realization_id = null
  form.realization_date = ''
  form.realization_description = ''
  form.memo_number = ''
  form.total_realization = 0
  form.details = []
  form.costs = []
}

function openCreate() {
  formMode.value = 'create'
  resetForm()
  loadCostItems()
  showForm.value = true
}

async function openEdit(row: RealizationReturnRow) {
  const detail = await getDetail(row.return_id)
  if (!detail) return
  selected.value = detail
  formMode.value = 'edit'
  loadCostItems()
  populateFormFromDetail(detail)
  showForm.value = true
}

async function openView(row: RealizationReturnRow) {
  const detail = await getDetail(row.return_id)
  if (!detail) return
  selected.value = detail
  formMode.value = 'view'
  showForm.value = true
}

async function openDelete(row: RealizationReturnRow) {
  const detail = await getDetail(row.return_id)
  if (!detail) return
  selected.value = detail
  showDelete.value = true
}

function populateFormFromDetail(detail: RealizationReturnDetail) {
  form.return_date = detail.return_date ?? getTodayISO()
  form.return_description = detail.return_description ?? ''
  form.realization_id = detail.realization_id
  form.realization_date = detail.realization_date ?? ''
  form.realization_description = detail.realization_description ?? ''
  form.memo_number = detail.memo_number ?? ''
  form.total_realization = detail.realization_amount ?? 0
  form.details = detail.details.map((d) => ({
    realization_detail_id: d.realization_detail_id,
    mustahiq_product_id: d.mustahiq_product_id,
    mustahiq_product_name: d.mustahiq_product_name,
    account_no: d.account_no,
    account_name: d.account_name,
    realization_amount: d.realization_amount ?? 0,
    return_amount: d.return_amount,
    detail_description: d.detail_description ?? '',
  }))
  form.costs = detail.costs.map((c) => ({
    _key: _costKey++,
    cost_item_id: c.cost_item_id,
    cost_item_description: c.cost_item_description,
    cost_amount: c.cost_amount,
  }))
}

// ── Realization Search Dialog ─────────────────────────────────────────────────

function openRealizationSearch() {
  realizationRows.value = []
  realizationSearchQuery.value = ''
  realizationTypeFilter.value = ''
  realizationSearchPage.value = 1
  realizationSearchTotal.value = 0
  showSearchRealization.value = true
  searchRealizations()
}

async function selectRealization(r: RealizationLookup) {
  form.realization_id = r.realization_id
  form.realization_date = r.realization_date ?? ''
  form.realization_description = r.realization_description ?? ''
  form.memo_number = r.memo_number ?? ''
  form.details = []
  form.total_realization = r.realization_amount ?? 0
  showSearchRealization.value = false
  await loadRealizationDetails(r.realization_id)
}

// ── Cost Grid ─────────────────────────────────────────────────────────────────

function addCostRow() {
  form.costs.push({ _key: _costKey++, cost_item_id: null, cost_item_description: null, cost_amount: null })
}

function removeCostRow(key: number) {
  const idx = form.costs.findIndex((c) => c._key === key)
  if (idx >= 0) form.costs.splice(idx, 1)
}

function onCostItemSelect(row: FormCostRow, costItemId: string) {
  const ci = costItems.value.find((c) => String(c.cost_item_id) === costItemId)
  row.cost_item_id = ci ? ci.cost_item_id : null
  row.cost_item_description = ci ? ci.cost_item_description : null
}

// ── Save ──────────────────────────────────────────────────────────────────────

function validateForm(): string[] {
  const errors: string[] = []
  if (!form.return_date) errors.push('Tanggal pengembalian harus diisi')
  if (!form.return_description.trim()) errors.push('Keterangan pengembalian harus diisi')
  if (!form.realization_id) errors.push('Realisasi harus dipilih')
  if (form.realization_date && form.return_date < form.realization_date)
    errors.push('Tanggal pengembalian tidak boleh lebih kecil dari tanggal realisasi')
  if (form.details.length === 0) errors.push('Detail realisasi belum dimuat')
  const totalRet = totalReturn.value
  if (totalRet <= 0) errors.push('Total pengembalian harus lebih dari 0')
  for (const d of form.details) {
    if ((d.return_amount ?? 0) < 0)
      errors.push(`Nominal pengembalian tidak boleh negatif (${d.mustahiq_product_name})`)
    if ((d.return_amount ?? 0) > d.realization_amount)
      errors.push(`Nominal pengembalian melebihi nominal realisasi (${d.mustahiq_product_name})`)
  }
  for (const c of form.costs) {
    if (!c.cost_item_id) errors.push('Semua baris rincian biaya harus memilih jenis biaya')
    if ((c.cost_amount ?? 0) < 0) errors.push('Nominal biaya tidak boleh negatif')
  }
  if (form.details.length > 0 && !balanceOk.value)
    errors.push('Total pengembalian + total biaya harus sama dengan total pencairan realisasi')
  return errors
}

async function saveForm() {
  const errors = validateForm()
  if (errors.length > 0) {
    toast.add({ severity: 'error', summary: 'Validasi Gagal', detail: errors.join('; '), life: 6000 })
    return
  }

  formSaving.value = true
  try {
    const payload = {
      return_date: form.return_date,
      return_description: form.return_description,
      realization_id: form.realization_id,
      details: form.details.map((d) => ({
        realization_detail_id: d.realization_detail_id,
        return_amount: d.return_amount ?? 0,
        detail_description: d.detail_description,
        mustahiq_product_id: d.mustahiq_product_id,
        account_no: d.account_no,
      })),
      costs: form.costs.map((c) => ({
        cost_item_id: c.cost_item_id,
        cost_amount: c.cost_amount ?? 0,
      })),
    }

    if (formMode.value === 'create') {
      await api.post(API_PREFIX, payload)
      toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Pengembalian realisasi berhasil ditambahkan', life: 3000 })
    } else if (formMode.value === 'edit' && selected.value) {
      await api.put(`${API_PREFIX}/${selected.value.return_id}`, payload)
      toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Pengembalian realisasi berhasil diperbarui', life: 3000 })
    }

    showForm.value = false
    await loadData()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal Menyimpan',
      detail: e instanceof ApiError ? e.message : 'Terjadi kesalahan',
      life: 5000,
    })
  } finally {
    formSaving.value = false
  }
}

async function confirmDelete() {
  if (!selected.value) return
  loading.value = true
  try {
    await api.delete(`${API_PREFIX}/${selected.value.return_id}`)
    toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Pengembalian realisasi berhasil dihapus', life: 3000 })
    showDelete.value = false
    selected.value = null
    await loadData()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal Hapus',
      detail: e instanceof ApiError ? e.message : 'Terjadi kesalahan',
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────

function formatAmount(n: number | null | undefined): string {
  if (n === null || n === undefined) return '-'
  return new Intl.NumberFormat('id-ID', { maximumFractionDigits: 2 }).format(n)
}

const realizationTypeOptions = [
  { value: '', label: 'Semua' },
  { value: 'R', label: 'Rutin' },
  { value: 'N', label: 'Non Rutin' },
]
</script>

<template>
  <div class="space-y-4">
    <!-- ── Toolbar ── -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <div class="flex flex-wrap items-end gap-2 flex-1">
        <div class="flex flex-col gap-1">
          <span class="text-xs text-zinc-500">Tanggal Dari</span>
          <DateField v-model="beginDate" class="w-36" />
        </div>
        <div class="flex flex-col gap-1">
          <span class="text-xs text-zinc-500">s/d</span>
          <DateField v-model="endDate" class="w-36" />
        </div>
        <Button variant="secondary" :icon="Search" @click="tampilkan" :loading="loading">
          Tampilkan
        </Button>
      </div>
      <Button :icon="Plus" @click="openCreate">Tambah</Button>
    </div>

    <!-- ── Pagination ── -->
    <div class="border-x border-zinc-200 bg-white px-4 py-2 dark:border-zinc-700 dark:bg-zinc-900">
      <TablePagination
        :page="page"
        :page-size="pageSize"
        :total="totalRec"
        :total-pages="totalPages"
        @update:page="page = $event"
      />
    </div>

    <!-- ── Table ── -->
    <div class="rounded-b border bg-white dark:border-zinc-700 dark:bg-zinc-900 overflow-x-auto">
      <div v-if="errorMsg" class="p-4 text-sm text-red-600">{{ errorMsg }}</div>
      <div v-else-if="!hasLoaded" class="p-8 text-center text-sm text-zinc-400">
        Pilih periode lalu klik Tampilkan
      </div>
      <div v-else-if="loading" class="p-8 text-center text-sm text-zinc-400">Memuat...</div>
      <div v-else-if="rows.length === 0" class="p-8 text-center text-sm text-zinc-400">
        Tidak ada data
      </div>
      <DataTable v-else :value="rows" striped-rows class="text-sm">
        <Column field="return_date" header="Tgl Pengembalian" style="width: 130px">
          <template #body="{ data }">{{ dmy(data.return_date) }}</template>
        </Column>
        <Column field="memo_number" header="No Memo" style="width: 160px" />
        <Column field="return_description" header="Keterangan" />
        <Column field="realization_amount" header="Nilai Realisasi" style="width: 140px; text-align: right">
          <template #body="{ data }">
            <span class="font-mono">{{ formatAmount(data.realization_amount) }}</span>
          </template>
        </Column>
        <Column field="return_amount" header="Nilai Pengembalian" style="width: 150px; text-align: right">
          <template #body="{ data }">
            <span class="font-mono text-emerald-700 dark:text-emerald-400">{{ formatAmount(data.return_amount) }}</span>
          </template>
        </Column>
        <Column header="Aksi" style="width: 130px; text-align: center">
          <template #body="{ data }">
            <div class="flex justify-center gap-1">
              <button
                class="rounded p-1 text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800 dark:hover:bg-zinc-700"
                title="Tampilkan"
                @click="openView(data)"
              >
                <Eye :size="15" />
              </button>
              <button
                class="rounded p-1 text-blue-500 hover:bg-blue-50 hover:text-blue-700 dark:hover:bg-blue-900"
                title="Ubah"
                @click="openEdit(data)"
              >
                <Pencil :size="15" />
              </button>
              <button
                class="rounded p-1 text-red-500 hover:bg-red-50 hover:text-red-700 dark:hover:bg-red-900"
                title="Hapus"
                @click="openDelete(data)"
              >
                <Trash2 :size="15" />
              </button>
            </div>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- ── Form Dialog (Add / Edit / View) ── -->
    <Dialog
      v-model:visible="showForm"
      :header="formMode === 'create' ? 'Tambah Pengembalian Realisasi' : formMode === 'edit' ? 'Ubah Pengembalian Realisasi' : 'Detail Pengembalian Realisasi'"
      modal
      :style="{ width: '900px', maxWidth: '98vw' }"
      :closable="!formSaving"
    >
      <!-- Header fields -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-zinc-600">Tgl Transaksi Pengembalian <span class="text-red-500">*</span></label>
          <DateField v-model="form.return_date" :disabled="isReadOnly" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-zinc-600">Keterangan Pengembalian <span class="text-red-500">*</span></label>
          <input
            v-model="form.return_description"
            :disabled="isReadOnly"
            class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary disabled:bg-zinc-50 dark:bg-zinc-800 dark:disabled:bg-zinc-900"
            placeholder="Keterangan..."
          />
        </div>

        <!-- Realization selector -->
        <div class="col-span-2 rounded-md border border-dashed border-zinc-300 bg-zinc-50 p-3 dark:border-zinc-600 dark:bg-zinc-800/50">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold text-zinc-600 dark:text-zinc-300">Data Realisasi</span>
            <Button
              v-if="!isReadOnly"
              variant="secondary"
              :icon="Search"
              size="sm"
              @click="openRealizationSearch"
            >
              Pilih Realisasi
            </Button>
          </div>
          <div v-if="!form.realization_id" class="text-xs text-zinc-400 italic">
            Belum dipilih — klik Pilih Realisasi
          </div>
          <div v-else class="grid grid-cols-3 gap-3 text-sm">
            <div class="flex flex-col gap-1">
              <span class="text-xs text-zinc-500">No Memo</span>
              <span class="font-medium">{{ form.memo_number || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-xs text-zinc-500">Tgl Realisasi</span>
              <span>{{ dmy(form.realization_date) || '-' }}</span>
            </div>
            <div class="flex flex-col gap-1">
              <span class="text-xs text-zinc-500">Total Pencairan</span>
              <span class="font-mono font-semibold">{{ formatAmount(form.total_realization) }}</span>
            </div>
            <div class="col-span-3 flex flex-col gap-1">
              <span class="text-xs text-zinc-500">Keterangan Realisasi</span>
              <span class="text-zinc-700 dark:text-zinc-300">{{ form.realization_description || '-' }}</span>
            </div>
          </div>
        </div>

        <!-- Summary totals -->
        <div
          v-if="form.realization_id"
          class="col-span-2 grid grid-cols-3 gap-3 rounded-md border px-4 py-3 text-sm"
          :class="balanceOk ? 'border-emerald-200 bg-emerald-50 dark:border-emerald-700 dark:bg-emerald-900/20' : 'border-amber-300 bg-amber-50 dark:border-amber-600 dark:bg-amber-900/20'"
        >
          <div class="flex flex-col gap-1">
            <span class="text-xs text-zinc-500">Total Pencairan</span>
            <span class="font-mono font-semibold">{{ formatAmount(form.total_realization) }}</span>
          </div>
          <div class="flex flex-col gap-1">
            <span class="text-xs text-zinc-500">Total Pengembalian</span>
            <span class="font-mono font-semibold text-emerald-700 dark:text-emerald-400">{{ formatAmount(totalReturn) }}</span>
          </div>
          <div class="flex flex-col gap-1">
            <span class="text-xs text-zinc-500">Total Biaya</span>
            <span class="font-mono font-semibold text-blue-700 dark:text-blue-400">{{ formatAmount(totalCost) }}</span>
          </div>
          <div v-if="!balanceOk" class="col-span-3 text-xs text-amber-700 dark:text-amber-400">
            ⚠ Total pengembalian + total biaya ({{ formatAmount(totalBalance) }}) belum sama dengan total pencairan ({{ formatAmount(form.total_realization) }})
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <TabView v-if="form.realization_id">
        <!-- Tab 1: Detail Realisasi -->
        <TabPanel header="Detail Realisasi">
          <div class="overflow-x-auto">
            <table class="w-full text-sm border-collapse">
              <thead>
                <tr class="bg-zinc-50 dark:bg-zinc-800 text-left">
                  <th class="border px-3 py-2 text-xs font-semibold text-zinc-600">Program</th>
                  <th class="border px-3 py-2 text-xs font-semibold text-zinc-600">Sumber Dana</th>
                  <th class="border px-3 py-2 text-xs font-semibold text-zinc-600 text-right">Nominal Realisasi</th>
                  <th class="border px-3 py-2 text-xs font-semibold text-zinc-600 text-right" style="width: 160px">
                    Nominal Pengembalian <span v-if="!isReadOnly" class="text-red-500">*</span>
                  </th>
                  <th class="border px-3 py-2 text-xs font-semibold text-zinc-600">Keterangan</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="form.details.length === 0">
                  <td colspan="5" class="border px-3 py-4 text-center text-zinc-400 italic text-xs">
                    Memuat detail...
                  </td>
                </tr>
                <tr
                  v-for="d in form.details"
                  :key="d.realization_detail_id"
                  class="hover:bg-zinc-50 dark:hover:bg-zinc-800/50"
                >
                  <td class="border px-3 py-2">{{ d.mustahiq_product_name || '-' }}</td>
                  <td class="border px-3 py-2">{{ d.account_name || d.account_no || '-' }}</td>
                  <td class="border px-3 py-2 text-right font-mono">{{ formatAmount(d.realization_amount) }}</td>
                  <td class="border px-1 py-1">
                    <input
                      v-if="!isReadOnly"
                      v-model.number="d.return_amount"
                      type="number"
                      min="0"
                      :max="d.realization_amount"
                      step="0.01"
                      class="h-8 w-full rounded border px-2 text-sm text-right font-mono focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                      placeholder="0"
                    />
                    <span v-else class="block px-3 font-mono text-right">{{ formatAmount(d.return_amount) }}</span>
                  </td>
                  <td class="border px-1 py-1">
                    <input
                      v-if="!isReadOnly"
                      v-model="d.detail_description"
                      type="text"
                      class="h-8 w-full rounded border px-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                      placeholder="Keterangan..."
                    />
                    <span v-else class="block px-3">{{ d.detail_description || '-' }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </TabPanel>

        <!-- Tab 2: Rincian Biaya -->
        <TabPanel header="Rincian Biaya">
          <div class="mb-2 flex justify-end" v-if="!isReadOnly">
            <Button variant="secondary" :icon="Plus" size="sm" @click="addCostRow">Tambah Baris</Button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-sm border-collapse">
              <thead>
                <tr class="bg-zinc-50 dark:bg-zinc-800 text-left">
                  <th class="border px-3 py-2 text-xs font-semibold text-zinc-600">Jenis Biaya</th>
                  <th class="border px-3 py-2 text-xs font-semibold text-zinc-600 text-right" style="width: 160px">Nominal</th>
                  <th v-if="!isReadOnly" class="border px-3 py-2 text-xs font-semibold text-zinc-600 text-center" style="width: 50px"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="form.costs.length === 0">
                  <td :colspan="isReadOnly ? 2 : 3" class="border px-3 py-4 text-center text-zinc-400 italic text-xs">
                    {{ isReadOnly ? 'Tidak ada rincian biaya' : 'Klik Tambah Baris untuk menambah rincian biaya' }}
                  </td>
                </tr>
                <tr
                  v-for="c in form.costs"
                  :key="c._key"
                  class="hover:bg-zinc-50 dark:hover:bg-zinc-800/50"
                >
                  <td class="border px-1 py-1">
                    <SearchSelect
                      v-if="!isReadOnly"
                      :model-value="c.cost_item_id ? String(c.cost_item_id) : ''"
                      :options="costItemOptions"
                      placeholder="Pilih jenis biaya..."
                      @update:model-value="(v) => onCostItemSelect(c, v)"
                    />
                    <span v-else class="block px-3">{{ c.cost_item_description || '-' }}</span>
                  </td>
                  <td class="border px-1 py-1">
                    <input
                      v-if="!isReadOnly"
                      v-model.number="c.cost_amount"
                      type="number"
                      min="0"
                      step="0.01"
                      class="h-8 w-full rounded border px-2 text-sm text-right font-mono focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                      placeholder="0"
                    />
                    <span v-else class="block px-3 font-mono text-right">{{ formatAmount(c.cost_amount) }}</span>
                  </td>
                  <td v-if="!isReadOnly" class="border px-2 py-1 text-center">
                    <button
                      class="rounded p-1 text-red-500 hover:bg-red-50 hover:text-red-700"
                      @click="removeCostRow(c._key)"
                    >
                      <X :size="14" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </TabPanel>
      </TabView>

      <div v-else class="py-6 text-center text-sm text-zinc-400 italic">
        Pilih data realisasi terlebih dahulu untuk mengisi detail pengembalian
      </div>

      <!-- Dialog footer -->
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="secondary" @click="showForm = false" :disabled="formSaving">Tutup</Button>
          <Button
            v-if="!isReadOnly"
            :loading="formSaving"
            @click="saveForm"
          >
            Simpan
          </Button>
        </div>
      </template>
    </Dialog>

    <!-- ── Search Realization Dialog ── -->
    <Dialog
      v-model:visible="showSearchRealization"
      header="Pilih Data Realisasi"
      modal
      :style="{ width: '700px', maxWidth: '98vw' }"
    >
      <div class="flex flex-wrap gap-2 mb-3">
        <input
          v-model="realizationSearchQuery"
          type="text"
          class="h-9 flex-1 min-w-[200px] rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
          placeholder="Cari nomor memo atau keterangan..."
          @keyup.enter="() => { realizationSearchPage = 1; searchRealizations() }"
        />
        <select
          v-model="realizationTypeFilter"
          class="h-9 rounded border px-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
          @change="() => { realizationSearchPage = 1; searchRealizations() }"
        >
          <option value="">Semua Tipe</option>
          <option value="R">Rutin</option>
          <option value="N">Non Rutin</option>
        </select>
        <Button variant="secondary" :icon="Search" size="sm" @click="() => { realizationSearchPage = 1; searchRealizations() }">
          Cari
        </Button>
      </div>

      <div v-if="realizationSearchLoading" class="py-6 text-center text-sm text-zinc-400">Memuat...</div>
      <div v-else-if="realizationRows.length === 0" class="py-6 text-center text-sm text-zinc-400">Tidak ada data</div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="bg-zinc-50 dark:bg-zinc-800">
              <th class="border px-3 py-2 text-xs text-left">No Memo</th>
              <th class="border px-3 py-2 text-xs text-left">Tgl Realisasi</th>
              <th class="border px-3 py-2 text-xs text-left">Keterangan</th>
              <th class="border px-3 py-2 text-xs text-right">Nilai</th>
              <th class="border px-3 py-2 text-xs text-center">Tipe</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="r in realizationRows"
              :key="r.realization_id"
              class="cursor-pointer hover:bg-blue-50 dark:hover:bg-blue-900/30"
              @click="selectRealization(r)"
            >
              <td class="border px-3 py-2 font-medium text-blue-700 dark:text-blue-400">{{ r.memo_number || '-' }}</td>
              <td class="border px-3 py-2">{{ dmy(r.realization_date) }}</td>
              <td class="border px-3 py-2 max-w-[200px] truncate">{{ r.realization_description || '-' }}</td>
              <td class="border px-3 py-2 text-right font-mono">{{ formatAmount(r.realization_amount) }}</td>
              <td class="border px-3 py-2 text-center">
                <span
                  class="rounded-full px-2 py-0.5 text-xs font-semibold"
                  :class="r.realization_type === 'R' ? 'bg-blue-100 text-blue-700' : 'bg-orange-100 text-orange-700'"
                >
                  {{ r.realization_type === 'R' ? 'Rutin' : 'Non Rutin' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-2 flex items-center justify-between text-xs text-zinc-500">
        <span>Total: {{ realizationSearchTotal }} data</span>
        <div class="flex gap-1">
          <button
            :disabled="realizationSearchPage <= 1"
            class="rounded border px-2 py-1 disabled:opacity-40 hover:bg-zinc-100"
            @click="() => { realizationSearchPage--; searchRealizations() }"
          >
            ←
          </button>
          <span class="px-2 py-1">Hal {{ realizationSearchPage }}</span>
          <button
            :disabled="realizationRows.length < 20"
            class="rounded border px-2 py-1 disabled:opacity-40 hover:bg-zinc-100"
            @click="() => { realizationSearchPage++; searchRealizations() }"
          >
            →
          </button>
        </div>
      </div>

      <template #footer>
        <Button variant="secondary" @click="showSearchRealization = false">Tutup</Button>
      </template>
    </Dialog>

    <!-- ── Delete Confirmation Modal ── -->
    <Modal v-if="showDelete" v-model:open="showDelete" title="Hapus Pengembalian Realisasi">
      <div v-if="selected" class="space-y-3 text-sm">
        <p class="text-zinc-600 dark:text-zinc-400">
          Konfirmasi hapus data pengembalian realisasi berikut:
        </p>
        <div class="rounded-md border bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 p-4 space-y-2">
          <div class="grid grid-cols-2 gap-2">
            <div>
              <div class="text-xs text-zinc-500">No Memo</div>
              <div class="font-medium">{{ selected.memo_number || '-' }}</div>
            </div>
            <div>
              <div class="text-xs text-zinc-500">Tgl Pengembalian</div>
              <div>{{ dmy(selected.return_date) }}</div>
            </div>
            <div class="col-span-2">
              <div class="text-xs text-zinc-500">Keterangan</div>
              <div>{{ selected.return_description || '-' }}</div>
            </div>
            <div>
              <div class="text-xs text-zinc-500">Nilai Realisasi</div>
              <div class="font-mono">{{ formatAmount(selected.realization_amount) }}</div>
            </div>
            <div>
              <div class="text-xs text-zinc-500">Nilai Pengembalian</div>
              <div class="font-mono font-semibold text-emerald-700">{{ formatAmount(selected.return_amount) }}</div>
            </div>
          </div>
        </div>
        <p class="text-red-600 text-xs">Tindakan ini tidak dapat dibatalkan.</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="secondary" @click="showDelete = false">Batal</Button>
          <Button variant="danger" :loading="loading" @click="confirmDelete">Hapus</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

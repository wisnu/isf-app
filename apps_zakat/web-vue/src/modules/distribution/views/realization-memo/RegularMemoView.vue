<script setup lang="ts">
import { FileText, Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
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

interface MemoRow {
  memo_id: number
  memo_number: string | null
  memo_subject: string | null
  memo_from: string | null
  memo_to: string | null
  memo_amount: number | null
  memo_date: string | null
  branch_code: string | null
  user_input: string | null
}

interface MemoDetail extends MemoRow {
  details: DetailRow[]
}

interface DetailRow {
  memo_detail_id: number
  mustahiq_product_id: number
  product_name: string | null
  mustahiq_name: string | null
  program_detail_name: string | null
  amount: number
}

interface ProgramLookupItem {
  mustahiq_product_id: number
  mustahiq_product_name: string | null
  product_name: string | null
  mustahiq_name: string | null
  distribution_amount: number | null
}

interface PaginationState {
  page: number
  page_size: number
  total: number
  total_pages: number
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_PREFIX = '/api/distribution/realization-memo/regular'
const PAGE_TITLE = 'Memo Penyaluran Rutin'

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()

const rows       = ref<MemoRow[]>([])
const loading    = shallowRef(false)
const errorMsg   = shallowRef<string | null>(null)
const hasLoaded  = shallowRef(false)
const page       = shallowRef(1)
const pageSize   = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec   = shallowRef(0)

// filters
const filterSearch   = ref('')
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
    if (filterSearch.value.trim())   params.search    = filterSearch.value.trim()
    if (filterDateFrom.value)        params.date_from = filterDateFrom.value
    if (filterDateTo.value)          params.date_to   = filterDateTo.value

    const res = await api.get<{ rows: MemoRow[]; pagination: PaginationState }>(API_PREFIX, params)
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

onMounted(load)

// ── Program Lookup ────────────────────────────────────────────────────────────

const programLookup   = ref<ProgramLookupItem[]>([])
const programSearch   = ref('')
const programLoading  = shallowRef(false)

async function loadPrograms(q: string) {
  programLoading.value = true
  try {
    const params: Record<string, string> = {}
    if (q.trim()) params.search = q.trim()
    const res = await api.get<{ data: ProgramLookupItem[] }>(`${API_PREFIX}/lookup/programs`, params)
    programLookup.value = res.data
  } catch { /* non-critical */ } finally {
    programLoading.value = false
  }
}

watch(programSearch, (q) => {
  clearTimeout(programSearchTimer)
  programSearchTimer = window.setTimeout(() => loadPrograms(q), 300)
})
let programSearchTimer = 0

// ── Form Modal State ──────────────────────────────────────────────────────────

const showForm  = shallowRef(false)
const formMode  = shallowRef<'create' | 'edit'>('create')
const formLoading = shallowRef(false)

interface FormState {
  memo_id: number | null
  memo_number: string
  memo_subject: string
  memo_from: string
  memo_to: string
  memo_date: string
  details: FormDetail[]
}

interface FormDetail {
  _key: number
  mustahiq_product_id: number
  product_name: string
  mustahiq_name: string
  program_detail_name: string
  amount: number
}

let detailKeySeq = 0

const form = reactive<FormState>({
  memo_id: null,
  memo_number: '',
  memo_subject: '',
  memo_from: '',
  memo_to: '',
  memo_date: '',
  details: [],
})

const totalAmount = computed(() => form.details.reduce((s, d) => s + (d.amount || 0), 0))

// selected program to add
const selectedProgram = ref<ProgramLookupItem | null>(null)
const addAmount = ref<number>(0)

function openCreate() {
  formMode.value = 'create'
  Object.assign(form, { memo_id: null, memo_number: '', memo_subject: '', memo_from: '', memo_to: '', memo_date: '', details: [] })
  selectedProgram.value = null
  addAmount.value = 0
  programSearch.value = ''
  programLookup.value = []
  loadPrograms('')
  showForm.value = true
}

async function openEdit(row: MemoRow) {
  formMode.value = 'edit'
  formLoading.value = true
  showForm.value = true
  try {
    const detail = await api.get<MemoDetail>(`${API_PREFIX}/${row.memo_id}`)
    Object.assign(form, {
      memo_id:      detail.memo_id,
      memo_number:  detail.memo_number ?? '',
      memo_subject: detail.memo_subject ?? '',
      memo_from:    detail.memo_from ?? '',
      memo_to:      detail.memo_to ?? '',
      memo_date:    detail.memo_date ?? '',
      details: detail.details.map(d => ({
        _key: ++detailKeySeq,
        mustahiq_product_id: d.mustahiq_product_id,
        product_name:        d.product_name ?? '',
        mustahiq_name:       d.mustahiq_name ?? '',
        program_detail_name: d.program_detail_name ?? '',
        amount:              d.amount,
      })),
    })
    selectedProgram.value = null
    addAmount.value = 0
    programSearch.value = ''
    loadPrograms('')
  } catch {
    toast.error('Gagal memuat detail memo')
    showForm.value = false
  } finally {
    formLoading.value = false
  }
}

// ── Program Picker ────────────────────────────────────────────────────────────

function selectProgram(p: ProgramLookupItem) {
  selectedProgram.value = p
  addAmount.value = p.distribution_amount ?? 0
}

function addProgramToDetail() {
  const p = selectedProgram.value
  if (!p) { toast.error('Pilih program terlebih dahulu'); return }
  if (addAmount.value <= 0) { toast.error('Nominal harus lebih dari 0'); return }

  const alreadyExists = form.details.find(d => d.mustahiq_product_id === p.mustahiq_product_id)
  if (alreadyExists) { toast.error('Program sudah ada dalam daftar'); return }

  form.details.push({
    _key:                ++detailKeySeq,
    mustahiq_product_id: p.mustahiq_product_id,
    product_name:        p.product_name ?? '',
    mustahiq_name:       p.mustahiq_name ?? '',
    program_detail_name: p.mustahiq_product_name ?? '',
    amount:              addAmount.value,
  })

  selectedProgram.value = null
  addAmount.value = 0
}

function removeDetail(key: number) {
  const idx = form.details.findIndex(d => d._key === key)
  if (idx >= 0) form.details.splice(idx, 1)
}

// ── Save ──────────────────────────────────────────────────────────────────────

async function save() {
  if (!form.memo_number.trim()) { toast.error('Nomor memo harus diisi'); return }
  if (!form.memo_subject.trim()) { toast.error('Perihal harus diisi'); return }
  if (!form.memo_from.trim()) { toast.error('Dari harus diisi'); return }
  if (!form.memo_to.trim()) { toast.error('Kepada harus diisi'); return }
  if (!form.memo_date) { toast.error('Tanggal memo harus diisi'); return }
  if (form.details.length === 0) { toast.error('Tambahkan minimal satu program penyaluran'); return }

  formLoading.value = true
  try {
    const body = {
      memo_number:  form.memo_number.trim(),
      memo_subject: form.memo_subject.trim(),
      memo_from:    form.memo_from.trim(),
      memo_to:      form.memo_to.trim(),
      memo_date:    form.memo_date,
      details: form.details.map(d => ({
        mustahiq_product_id: d.mustahiq_product_id,
        amount:              d.amount,
      })),
    }

    if (formMode.value === 'create') {
      await api.post(API_PREFIX, body)
      toast.success('Memo berhasil dibuat')
    } else {
      await api.put(`${API_PREFIX}/${form.memo_id}`, body)
      toast.success('Memo berhasil diperbarui')
    }
    showForm.value = false
    load()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan memo')
  } finally {
    formLoading.value = false
  }
}

// ── Delete ────────────────────────────────────────────────────────────────────

const showDeleteModal = shallowRef(false)
const deleteTarget    = ref<MemoRow | null>(null)
const deleteLoading   = shallowRef(false)

function openDelete(row: MemoRow) {
  deleteTarget.value = row
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleteLoading.value = true
  try {
    await api.delete(`${API_PREFIX}/${deleteTarget.value.memo_id}`)
    toast.success('Memo berhasil dihapus')
    showDeleteModal.value = false
    deleteTarget.value = null
    load()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menghapus memo')
  } finally {
    deleteLoading.value = false
  }
}

// ── Filtered lookup (exclude already added) ───────────────────────────────────

const filteredLookup = computed(() => {
  const added = new Set(form.details.map(d => d.mustahiq_product_id))
  return programLookup.value.filter(p => !added.has(p.mustahiq_product_id))
})
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <FileText class="w-5 h-5 text-primary" />
        <h1 class="text-lg font-semibold text-zinc-800">{{ PAGE_TITLE }}</h1>
      </div>
      <Button size="sm" class="gap-1.5" @click="openCreate">
        <Plus class="w-4 h-4" />
        Tambah Memo
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
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Cari</label>
          <input
            v-model="filterSearch"
            placeholder="Nomor / perihal / dari..."
            class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            @keyup.enter="() => { page = 1; load() }"
          />
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
              <th class="px-4 py-2 text-left">Nomor Memo</th>
              <th class="px-4 py-2 text-left">Tanggal</th>
              <th class="px-4 py-2 text-left">Perihal</th>
              <th class="px-4 py-2 text-left">Dari</th>
              <th class="px-4 py-2 text-left">Kepada</th>
              <th class="px-4 py-2 text-right">Total Pencairan</th>
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
                Tidak ada memo dalam periode ini.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.memo_id"
              class="border-b border-surface-200 last:border-0 hover:bg-zinc-50"
            >
              <td class="px-4 py-2 font-mono">{{ row.memo_number ?? '-' }}</td>
              <td class="px-4 py-2">{{ dmy(row.memo_date) }}</td>
              <td class="px-4 py-2 max-w-[200px] truncate" :title="row.memo_subject ?? ''">
                {{ row.memo_subject ?? '-' }}
              </td>
              <td class="px-4 py-2 max-w-[140px] truncate" :title="row.memo_from ?? ''">
                {{ row.memo_from ?? '-' }}
              </td>
              <td class="px-4 py-2 max-w-[140px] truncate" :title="row.memo_to ?? ''">
                {{ row.memo_to ?? '-' }}
              </td>
              <td class="px-4 py-2 text-right font-mono">
                {{ formatIdr(row.memo_amount ?? 0) }}
              </td>
              <td class="px-4 py-2 text-center">
                <div class="flex items-center justify-center gap-1">
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
    <Modal v-model:open="showForm" :title="formMode === 'create' ? 'Tambah Memo Penyaluran Rutin' : 'Edit Memo Penyaluran Rutin'" size="xl">
      <div v-if="formLoading && formMode === 'edit'" class="flex items-center justify-center py-12 text-zinc-400">
        Memuat data...
      </div>
      <div v-else class="space-y-6">
        <!-- Header fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Nomor Memo <span class="text-red-500">*</span></label>
            <input
              v-model="form.memo_number"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="contoh: MAI.DPNY/00001/2026"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Tanggal Memo <span class="text-red-500">*</span></label>
            <DateField v-model="form.memo_date" class="w-full" />
          </div>
          <div class="md:col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Perihal <span class="text-red-500">*</span></label>
            <input
              v-model="form.memo_subject"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Perihal memo..."
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Dari <span class="text-red-500">*</span></label>
            <input
              v-model="form.memo_from"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Pengirim memo"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Kepada <span class="text-red-500">*</span></label>
            <input
              v-model="form.memo_to"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Penerima memo"
            />
          </div>
        </div>

        <!-- Total -->
        <div class="flex items-center gap-2 rounded bg-zinc-50 border px-4 py-2">
          <span class="text-xs text-zinc-500">Total Pencairan:</span>
          <span class="font-mono font-semibold text-sm text-primary">{{ formatIdr(totalAmount) }}</span>
        </div>

        <!-- Program Picker -->
        <div class="rounded border border-dashed border-zinc-300 p-4 space-y-3">
          <p class="text-xs font-semibold text-zinc-600 uppercase tracking-wide">Tambah Program</p>
          <div class="flex flex-wrap gap-2 items-end">
            <div class="flex-1 min-w-[200px]">
              <label class="mb-1 block text-xs text-zinc-500">Cari Program Rutin</label>
              <input
                v-model="programSearch"
                class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Nama program / mustahiq..."
              />
            </div>
            <div class="w-32">
              <label class="mb-1 block text-xs text-zinc-500">Nominal</label>
              <input
                v-model.number="addAmount"
                type="number"
                min="0"
                class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
            <Button
              size="sm"
              variant="outline"
              class="gap-1 h-9 text-xs"
              :disabled="!selectedProgram"
              @click="addProgramToDetail"
            >
              <Plus class="w-3 h-3" />
              Tambah
            </Button>
          </div>

          <!-- Program Search Results -->
          <div v-if="filteredLookup.length > 0 || programLoading" class="max-h-40 overflow-y-auto rounded border bg-white text-xs">
            <div v-if="programLoading" class="px-3 py-2 text-zinc-400">Mencari...</div>
            <button
              v-for="p in filteredLookup.slice(0, 50)"
              :key="p.mustahiq_product_id"
              class="flex w-full items-center gap-2 px-3 py-2 text-left hover:bg-primary/10 transition"
              :class="selectedProgram?.mustahiq_product_id === p.mustahiq_product_id ? 'bg-primary/10 font-semibold' : ''"
              @click="selectProgram(p)"
            >
              <span class="flex-1 truncate">{{ p.product_name }} — {{ p.mustahiq_name }}</span>
              <span class="font-mono text-zinc-400">{{ formatIdr(p.distribution_amount ?? 0) }}</span>
            </button>
          </div>
          <p v-if="selectedProgram" class="text-xs text-primary">
            Dipilih: <strong>{{ selectedProgram.product_name }}</strong> ({{ selectedProgram.mustahiq_name }})
          </p>
        </div>

        <!-- Detail Table -->
        <div v-if="form.details.length > 0">
          <p class="mb-2 text-xs font-semibold text-zinc-600 uppercase tracking-wide">Daftar Program ({{ form.details.length }})</p>
          <div class="overflow-x-auto rounded border">
            <table class="w-full text-xs">
              <thead class="bg-zinc-50 border-b text-[10px] uppercase tracking-widest text-zinc-500">
                <tr>
                  <th class="px-3 py-2 text-left">Program</th>
                  <th class="px-3 py-2 text-left">Mustahiq</th>
                  <th class="px-3 py-2 text-right">Nominal</th>
                  <th class="px-3 py-2 text-center"></th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="d in form.details"
                  :key="d._key"
                  class="border-b last:border-0"
                >
                  <td class="px-3 py-2">{{ d.product_name }}</td>
                  <td class="px-3 py-2 text-zinc-500">{{ d.mustahiq_name }}</td>
                  <td class="px-3 py-2 text-right">
                    <input
                      v-model.number="d.amount"
                      type="number"
                      min="0"
                      class="w-28 rounded border px-2 py-1 text-right text-xs focus:outline-none focus:ring-1 focus:ring-primary"
                    />
                  </td>
                  <td class="px-3 py-2 text-center">
                    <button class="text-red-400 hover:text-red-600 transition" @click="removeDetail(d._key)">
                      <X class="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <p v-else class="text-xs text-zinc-400 italic">Belum ada program yang ditambahkan.</p>
      </div>

      <template #footer>
        <Button variant="outline" @click="showForm = false">Batal</Button>
        <Button variant="success" :disabled="formLoading" @click="save">
          {{ formLoading ? 'Menyimpan...' : 'Simpan' }}
        </Button>
      </template>
    </Modal>

    <!-- ── Delete Confirmation Modal ──────────────────────────────────────── -->
    <Modal v-model:open="showDeleteModal" title="Hapus Memo Penyaluran" size="sm">
      <div class="space-y-3 text-sm">
        <p>Anda akan menghapus memo berikut:</p>
        <div class="rounded border bg-zinc-50 px-4 py-3 space-y-1 text-xs">
          <div><span class="text-zinc-500">Nomor:</span> <strong>{{ deleteTarget?.memo_number }}</strong></div>
          <div><span class="text-zinc-500">Perihal:</span> {{ deleteTarget?.memo_subject }}</div>
          <div><span class="text-zinc-500">Tanggal:</span> {{ dmy(deleteTarget?.memo_date) }}</div>
          <div><span class="text-zinc-500">Total:</span> <strong class="font-mono">{{ formatIdr(deleteTarget?.memo_amount ?? 0) }}</strong></div>
        </div>
        <p class="text-red-600 text-xs">Tindakan ini tidak dapat dibatalkan. Semua detail program akan ikut terhapus.</p>
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

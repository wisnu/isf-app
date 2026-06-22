<script setup lang="ts">
import { CalendarDays, Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'
import { dmy } from '@/shared/utils/date'
import { formatIdr } from '@/shared/utils/format'

// ── Types ─────────────────────────────────────────────────────────────────────

interface ProgramRow {
  program_id: number
  mustahiq_id: number
  mustahiq_name: string | null
  product_id: number
  product_name: string | null
  program_detail_name: string | null
  distribution_amount: number | null
  date_start: string | null
  date_end: string | null
  proposal_id: number | null
  branch_code: string | null
  ashnaf: string | null
}

interface ProgramDetail extends ProgramRow {
  proposal_no: string | null
}

interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

interface LookupItem { value: string; label: string }

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const auth  = useAuthStore()

const rows        = ref<ProgramRow[]>([])
const loading     = shallowRef(false)
const errorMsg    = shallowRef<string | null>(null)
const page        = shallowRef(1)
const totalPages  = shallowRef(1)
const totalRec    = shallowRef(0)
const pageSize    = shallowRef(25)

// filter
const filterDateFrom  = ref('')
const filterDateTo    = ref('')
const filterProductId = ref('')
const filterSearch    = ref('')

// Lookups
const productOptions  = ref<LookupItem[]>([])
const mustahiqOptions = ref<LookupItem[]>([])

// ── Lookups load ──────────────────────────────────────────────────────────────

async function loadProductLookup() {
  try {
    const res = await api.get<{ data: { product_id: number; product_name: string | null }[] }>(
      '/api/distribution/non-regular-program/lookup/products'
    )
    productOptions.value = res.data.map(p => ({ value: String(p.product_id), label: p.product_name ?? '' }))
  } catch { /* non-critical */ }
}

async function loadMustahiqLookup(search?: string) {
  try {
    const q = search?.trim() ? `?search=${encodeURIComponent(search.trim())}` : ''
    const res = await api.get<{ data: { mustahiq_id: number; mustahiq_name: string | null }[] }>(
      `/api/distribution/non-regular-program/lookup/mustahiq${q}`
    )
    mustahiqOptions.value = res.data.map(m => ({ value: String(m.mustahiq_id), label: m.mustahiq_name ?? '' }))
  } catch { /* non-critical */ }
}

// ── List ──────────────────────────────────────────────────────────────────────

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (filterDateFrom.value) params.set('date_from', filterDateFrom.value)
    if (filterDateTo.value)   params.set('date_to',   filterDateTo.value)
    if (filterProductId.value) params.set('product_id', filterProductId.value)
    if (filterSearch.value.trim()) params.set('search', filterSearch.value.trim())

    const res = await api.get<{ rows: ProgramRow[]; pagination: Pagination }>(
      `/api/distribution/non-regular-program?${params}`
    )
    rows.value       = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRec.value   = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    rows.value = []
  } finally {
    loading.value = false
  }
}

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(filterSearch, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})
watch([filterDateFrom, filterDateTo, filterProductId], () => { page.value = 1; loadData() })

function prevPage() { if (page.value > 1) { page.value--; loadData() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadData() } }
function changePageSize(s: number) { pageSize.value = s; page.value = 1; loadData() }

function clearFilters() {
  filterDateFrom.value  = ''
  filterDateTo.value    = ''
  filterProductId.value = ''
  filterSearch.value    = ''
  page.value = 1
  loadData()
}

// ── Modal state ───────────────────────────────────────────────────────────────

type ModalMode = 'create' | 'edit' | 'detail' | 'delete'

const modalMode    = shallowRef<ModalMode>('create')
const modalOpen    = shallowRef(false)
const modalLoading = shallowRef(false)
const modalError   = shallowRef<string | null>(null)
const selectedRow  = ref<ProgramRow | null>(null)
const detailData   = ref<ProgramDetail | null>(null)

const form = reactive({
  mustahiq_id:         '',
  product_id:          '',
  program_detail_name: '',
  distribution_amount: '',
  date_start:          '',
  date_end:            '' as string,
  proposal_id:         '' as string,
})

function resetForm() {
  form.mustahiq_id         = ''
  form.product_id          = ''
  form.program_detail_name = ''
  form.distribution_amount = ''
  form.date_start          = ''
  form.date_end            = ''
  form.proposal_id         = ''
}

function fillForm(d: ProgramDetail) {
  form.mustahiq_id         = String(d.mustahiq_id)
  form.product_id          = String(d.product_id)
  form.program_detail_name = d.program_detail_name ?? ''
  form.distribution_amount = String(d.distribution_amount ?? '')
  form.date_start          = d.date_start ?? ''
  form.date_end            = d.date_end ?? ''
  form.proposal_id         = d.proposal_id ? String(d.proposal_id) : ''
  if (d.mustahiq_id && d.mustahiq_name) {
    const key = String(d.mustahiq_id)
    if (!mustahiqOptions.value.find(o => o.value === key)) {
      mustahiqOptions.value = [{ value: key, label: d.mustahiq_name }, ...mustahiqOptions.value]
    }
  }
}

function openCreate() {
  resetForm()
  modalMode.value  = 'create'
  modalError.value = null
  modalOpen.value  = true
}

async function openEdit(row: ProgramRow) {
  selectedRow.value  = row
  modalMode.value    = 'edit'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  try {
    const d = await api.get<ProgramDetail>(`/api/distribution/non-regular-program/${row.program_id}`)
    detailData.value = d
    fillForm(d)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

async function openDetail(row: ProgramRow) {
  selectedRow.value  = row
  modalMode.value    = 'detail'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  try {
    detailData.value = await api.get<ProgramDetail>(`/api/distribution/non-regular-program/${row.program_id}`)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

function openDelete(row: ProgramRow) {
  selectedRow.value  = row
  detailData.value   = null
  modalMode.value    = 'delete'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  api.get<ProgramDetail>(`/api/distribution/non-regular-program/${row.program_id}`)
    .then(d => { detailData.value = d })
    .catch(() => {})
    .finally(() => { modalLoading.value = false })
}

function closeModal() { modalOpen.value = false }

// ── Save / Delete ─────────────────────────────────────────────────────────────

function validateForm(): string | null {
  if (!form.mustahiq_id)         return 'Mustahiq wajib dipilih.'
  if (!form.product_id)          return 'Program wajib dipilih.'
  if (!form.program_detail_name.trim()) return 'Nama program detail wajib diisi.'
  const amt = Number(form.distribution_amount)
  if (!form.distribution_amount || isNaN(amt) || amt <= 0) return 'Nominal harus diisi dan > 0.'
  if (!form.date_start)          return 'Tanggal program wajib diisi.'
  return null
}

async function saveForm() {
  const err = validateForm()
  if (err) { modalError.value = err; return }

  modalLoading.value = true
  modalError.value   = null
  try {
    const payload: Record<string, unknown> = {
      mustahiq_id:         Number(form.mustahiq_id),
      product_id:          Number(form.product_id),
      program_detail_name: form.program_detail_name.trim(),
      distribution_amount: Number(form.distribution_amount),
      date_start:          form.date_start,
      date_end:            form.date_end || null,
      proposal_id:         form.proposal_id ? Number(form.proposal_id) : null,
    }
    if (modalMode.value === 'create') {
      await api.post('/api/distribution/non-regular-program', payload)
      toast.success('Program Non Rutin berhasil ditambahkan.')
    } else {
      await api.put(`/api/distribution/non-regular-program/${selectedRow.value!.program_id}`, payload)
      toast.success('Program Non Rutin berhasil diperbarui.')
    }
    closeModal()
    loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menyimpan data.'
  } finally {
    modalLoading.value = false
  }
}

async function confirmDelete() {
  if (!selectedRow.value) return
  modalLoading.value = true
  modalError.value   = null
  try {
    await api.delete(`/api/distribution/non-regular-program/${selectedRow.value.program_id}`)
    toast.success('Program Non Rutin berhasil dihapus.')
    closeModal()
    loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menghapus data.'
  } finally {
    modalLoading.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadProductLookup(), loadMustahiqLookup()])
  loadData()
})
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Program Non Rutin" subtitle="Data program penyaluran non rutin per mustahiq">
      <template #actions>
        <Button
          v-if="auth.hasMenu('distribution.program.non-regular')"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="openCreate"
        >
          <Plus class="w-3.5 h-3.5" />
          Tambah
        </Button>
      </template>
    </PageHeader>

    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400">
      {{ errorMsg }}
    </div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex flex-wrap items-center gap-2">
        <!-- Search -->
        <div class="relative flex-1 min-w-48 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input
            v-model="filterSearch"
            type="text"
            placeholder="Cari mustahiq / nama program..."
            class="w-full h-8 pl-8 pr-8 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring"
          />
          <button v-if="filterSearch" class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground" @click="filterSearch = ''">
            <X class="w-3 h-3" />
          </button>
        </div>

        <!-- Filter Program -->
        <div class="w-56">
          <SearchSelect
            v-model="filterProductId"
            :options="productOptions"
            all-label="Semua Program"
            placeholder="Filter program..."
          />
        </div>

        <!-- Filter tanggal -->
        <div class="flex items-center gap-1.5">
          <CalendarDays class="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />
          <DateField v-model="filterDateFrom" class="w-32" />
          <span class="text-xs text-muted-foreground">s/d</span>
          <DateField v-model="filterDateTo" class="w-32" />
        </div>

        <!-- Clear -->
        <button
          v-if="filterSearch || filterProductId || filterDateFrom || filterDateTo"
          class="h-8 px-2 text-[11px] text-muted-foreground hover:text-foreground border border-border rounded bg-background"
          @click="clearFilters"
        >
          Reset
        </button>
      </div>

      <!-- Pagination (atas) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} program
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @prev="prevPage" @next="nextPage" @update:page-size="changePageSize"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium w-24">Tgl Program</th>
              <th class="px-4 py-2 text-left font-medium">Nama Program</th>
              <th class="px-4 py-2 text-left font-medium max-w-xs">Detail Program</th>
              <th class="px-4 py-2 text-left font-medium">Mustahiq</th>
              <th class="px-4 py-2 text-right font-medium w-36">Nominal</th>
              <th class="px-4 py-2 text-right font-medium w-28">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">Belum ada data program non rutin.</td>
            </tr>
            <tr v-for="row in rows" :key="row.program_id" class="hover:bg-background/60">
              <td class="px-4 py-1.5 text-xs tabular-nums">{{ row.date_start ? dmy(row.date_start) : '—' }}</td>
              <td class="px-4 py-1.5 text-xs">{{ row.product_name || '—' }}</td>
              <td class="px-4 py-1.5 text-xs max-w-xs truncate" :title="row.program_detail_name ?? ''">{{ row.program_detail_name || '—' }}</td>
              <td class="px-4 py-1.5 font-medium text-xs">{{ row.mustahiq_name || '—' }}</td>
              <td class="px-4 py-1.5 text-xs text-right tabular-nums font-medium">
                {{ row.distribution_amount != null ? formatIdr(row.distribution_amount) : '—' }}
              </td>
              <td class="px-4 py-1.5">
                <div class="flex items-center justify-end gap-0.5">
                  <button
                    class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors text-[10px]"
                    title="Detail"
                    @click="openDetail(row)"
                  >Detail</button>
                  <button
                    class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-blue-600 transition-colors"
                    title="Ubah"
                    @click="openEdit(row)"
                  ><Pencil class="w-3.5 h-3.5" /></button>
                  <button
                    class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600 transition-colors"
                    title="Hapus"
                    @click="openDelete(row)"
                  ><Trash2 class="w-3.5 h-3.5" /></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Create / Edit Modal ──────────────────────────────────────────────── -->
    <Modal v-if="modalOpen && (modalMode === 'create' || modalMode === 'edit')" max-width="max-w-2xl" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">{{ modalMode === 'create' ? 'Tambah Program Non Rutin' : 'Ubah Program Non Rutin' }}</h2>
      </template>

      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat data...</div>
      <div v-else class="space-y-4">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>

        <div class="grid grid-cols-2 gap-4">
          <!-- Mustahiq -->
          <div class="col-span-2">
            <label class="block text-xs font-medium mb-1">Mustahiq <span class="text-red-500">*</span></label>
            <SearchSelect
              v-model="form.mustahiq_id"
              :options="mustahiqOptions"
              placeholder="Pilih mustahiq..."
              @search="loadMustahiqLookup"
            />
          </div>

          <!-- Program -->
          <div class="col-span-2">
            <label class="block text-xs font-medium mb-1">Nama Program <span class="text-red-500">*</span></label>
            <SearchSelect
              v-model="form.product_id"
              :options="productOptions"
              placeholder="Pilih jenis program..."
            />
          </div>

          <!-- Nama Detail -->
          <div class="col-span-2">
            <label class="block text-xs font-medium mb-1">Nama Program Detail / Keterangan <span class="text-red-500">*</span></label>
            <input
              v-model="form.program_detail_name"
              type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="Contoh: Bantuan Sembako Ramadhan RT 03"
            />
          </div>

          <!-- Nominal -->
          <div>
            <label class="block text-xs font-medium mb-1">Nominal (Rp) <span class="text-red-500">*</span></label>
            <input
              v-model="form.distribution_amount"
              type="number"
              min="0"
              step="1000"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="0"
            />
          </div>

          <!-- Proposal ID (optional) -->
          <div>
            <label class="block text-xs font-medium mb-1">ID Proposal (opsional)</label>
            <input
              v-model="form.proposal_id"
              type="number"
              min="1"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="Nomor proposal"
            />
          </div>

          <!-- Tanggal Program -->
          <div>
            <label class="block text-xs font-medium mb-1">Tanggal Program <span class="text-red-500">*</span></label>
            <DateField v-model="form.date_start" class="w-full" />
          </div>

          <!-- Tanggal Selesai (opsional) -->
          <div>
            <label class="block text-xs font-medium mb-1">Tanggal Selesai (opsional)</label>
            <DateField v-model="form.date_end" class="w-full" :min="form.date_start || undefined" />
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button size="sm" :disabled="modalLoading" @click="saveForm">
            {{ modalLoading ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Detail Modal -->
    <Modal v-if="modalOpen && modalMode === 'detail'" max-width="max-w-xl" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">Detail Program Non Rutin</h2>
      </template>
      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat...</div>
      <div v-else-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
      <div v-else-if="detailData" class="space-y-3 text-sm">
        <div class="grid grid-cols-2 gap-x-6 gap-y-2">
          <div class="col-span-2">
            <span class="text-xs text-muted-foreground">Mustahiq</span>
            <p class="font-medium">{{ detailData.mustahiq_name || '—' }}</p>
          </div>
          <div class="col-span-2">
            <span class="text-xs text-muted-foreground">Nama Program</span>
            <p>{{ detailData.product_name || '—' }}</p>
          </div>
          <div class="col-span-2">
            <span class="text-xs text-muted-foreground">Detail / Keterangan</span>
            <p>{{ detailData.program_detail_name || '—' }}</p>
          </div>
          <div>
            <span class="text-xs text-muted-foreground">Nominal</span>
            <p class="font-semibold tabular-nums">
              {{ detailData.distribution_amount != null ? formatIdr(detailData.distribution_amount) : '—' }}
            </p>
          </div>
          <div>
            <span class="text-xs text-muted-foreground">Ashnaf</span>
            <p>{{ detailData.ashnaf || '—' }}</p>
          </div>
          <div>
            <span class="text-xs text-muted-foreground">Tanggal Program</span>
            <p>{{ detailData.date_start ? dmy(detailData.date_start) : '—' }}</p>
          </div>
          <div>
            <span class="text-xs text-muted-foreground">Tanggal Selesai</span>
            <p>{{ detailData.date_end ? dmy(detailData.date_end) : '—' }}</p>
          </div>
          <div>
            <span class="text-xs text-muted-foreground">Cabang</span>
            <p>{{ detailData.branch_code || '—' }}</p>
          </div>
          <div>
            <span class="text-xs text-muted-foreground">Proposal</span>
            <p>{{ detailData.proposal_no || (detailData.proposal_id ? String(detailData.proposal_id) : '—') }}</p>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end"><Button variant="outline" size="sm" @click="closeModal">Tutup</Button></div>
      </template>
    </Modal>

    <!-- Delete Modal -->
    <Modal v-if="modalOpen && modalMode === 'delete'" max-width="max-w-md" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold text-red-600">Hapus Program Non Rutin</h2>
      </template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <p class="text-sm text-muted-foreground">Data program non rutin berikut akan dihapus permanen:</p>
        <div v-if="modalLoading" class="py-4 text-center text-muted-foreground text-xs">Memuat...</div>
        <div v-else class="rounded border border-border bg-muted/30 px-4 py-3 text-sm space-y-1">
          <div class="font-semibold">{{ detailData?.mustahiq_name || selectedRow?.mustahiq_name || '—' }}</div>
          <div class="text-xs text-muted-foreground">Program: {{ detailData?.product_name || selectedRow?.product_name || '—' }}</div>
          <div class="text-xs text-muted-foreground">Detail: {{ detailData?.program_detail_name || selectedRow?.program_detail_name || '—' }}</div>
          <div v-if="detailData?.distribution_amount != null" class="text-xs font-medium tabular-nums">
            Nominal: {{ formatIdr(detailData.distribution_amount) }}
          </div>
          <div class="text-xs text-muted-foreground">
            Tanggal: {{ detailData?.date_start ? dmy(detailData.date_start) : '—' }}
            <template v-if="detailData?.date_end"> s/d {{ dmy(detailData.date_end) }}</template>
          </div>
        </div>
        <p class="text-xs text-red-600 font-medium">Tindakan ini tidak dapat dibatalkan.</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button variant="destructive" size="sm" :disabled="modalLoading" @click="confirmDelete">
            {{ modalLoading ? 'Menghapus...' : 'Hapus' }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

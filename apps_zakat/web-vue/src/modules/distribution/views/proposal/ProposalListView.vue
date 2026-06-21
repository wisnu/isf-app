<script setup lang="ts">
import { ChevronDown, Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/app/stores/auth.store'

// ── Types ─────────────────────────────────────────────────────────────────────

interface ProposalRow {
  proposal_id: number
  proposal_no: string
  proposal_date: string
  received_date: string
  description: string
  nominal: number
  received_by: string | null
  reference_by: string | null
  reference_position: number | null
  status: string
  mustahiq_id: number
  mustahiq_name: string
  product_group_id: number
  product_group_name: string
  branch_code: string
}

interface ProposalDetail extends ProposalRow {
  address_street: string | null
  address_kelurahan: string | null
  address_kecamatan: string | null
}

interface ProductGroupItem {
  product_group_id: number
  product_group_name: string
  product_group_code: string
}

interface MustahiqItem {
  mustahiq_id: number
  mustahiq_name: string
  address: string | null
}

interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

interface ListResponse {
  rows: ProposalRow[]
  pagination: Pagination
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const auth = useAuthStore()

const rows = ref<ProposalRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const pageSize = shallowRef(25)

// Filter state
const dateFrom = ref('')
const dateTo = ref('')
const searchMustahiq = ref('')
const statusFilter = ref('')

let filterTimer: ReturnType<typeof setTimeout> | null = null

// Debounce filter changes
watch([dateFrom, dateTo, searchMustahiq, statusFilter], () => {
  if (filterTimer) clearTimeout(filterTimer)
  filterTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

// ── List ──────────────────────────────────────────────────────────────────────

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (dateFrom.value) params.set('date_from', dateFrom.value)
    if (dateTo.value) params.set('date_to', dateTo.value)
    if (searchMustahiq.value.trim()) params.set('mustahiq_name', searchMustahiq.value.trim())
    if (statusFilter.value) params.set('status', statusFilter.value)
    const res = await api.get<ListResponse>(`/api/distribution/proposal?${params}`)
    rows.value = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRec.value = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function prevPage() { if (page.value > 1) { page.value--; loadData() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadData() } }
function changePageSize(s: number) { pageSize.value = s; page.value = 1; loadData() }

// ── Lookups ───────────────────────────────────────────────────────────────────

const productGroups = ref<ProductGroupItem[]>([])
const mustahiqOptions = ref<MustahiqItem[]>([])
const totalProposalByMustahiq = ref(0)

async function loadProductGroups() {
  try {
    const res = await api.get<{ data: ProductGroupItem[] }>('/api/distribution/proposal/lookup/product-groups')
    productGroups.value = (res as any).data ?? res as any
  } catch { /* non-critical */ }
}

async function loadMustahiqOptions(search?: string) {
  try {
    const params = new URLSearchParams()
    if (search) params.set('search', search)
    const res = await api.get<{ data: MustahiqItem[] }>(`/api/distribution/proposal/lookup/mustahiq?${params}`)
    mustahiqOptions.value = (res as any).data ?? res as any
  } catch { /* non-critical */ }
}

async function loadTotalByMustahiq(mustahiqId: number) {
  try {
    const res = await api.get<{ total: number }>(`/api/distribution/proposal/total-by-mustahiq?mustahiq_id=${mustahiqId}`)
    totalProposalByMustahiq.value = res.total ?? 0
  } catch { /* non-critical */ }
}

const productGroupOptions = () => productGroups.value.map(p => ({ value: String(p.product_group_id), label: p.product_group_name }))
const mustahiqLookupOptions = () => mustahiqOptions.value.map(m => ({ value: String(m.mustahiq_id), label: m.mustahiq_name }))

// ── Modal state ───────────────────────────────────────────────────────────────

type ModalMode = 'create' | 'edit' | 'detail' | 'delete'

const modalMode = shallowRef<ModalMode>('create')
const modalOpen = shallowRef(false)
const modalLoading = shallowRef(false)
const modalError = shallowRef<string | null>(null)
const selectedRow = ref<ProposalRow | null>(null)
const detailData = ref<ProposalDetail | null>(null)

const form = reactive<Omit<ProposalDetail, 'proposal_id' | 'proposal_no' | 'branch_code'> & { proposal_date: string; received_date: string }>({
  proposal_date: '',
  received_date: '',
  description: '',
  nominal: 0,
  received_by: null,
  reference_by: null,
  reference_position: null,
  status: 'B',
  mustahiq_id: 0,
  mustahiq_name: '',
  product_group_id: 0,
  product_group_name: '',
  address_street: null,
  address_kelurahan: null,
  address_kecamatan: null,
})

function resetForm() {
  const today = new Date().toISOString().slice(0, 10)
  form.proposal_date = today
  form.received_date = today
  form.description = ''
  form.nominal = 0
  form.received_by = null
  form.reference_by = null
  form.reference_position = null
  form.status = 'B'
  form.mustahiq_id = 0
  form.mustahiq_name = ''
  form.product_group_id = 0
  form.product_group_name = ''
  form.address_street = null
  form.address_kelurahan = null
  form.address_kecamatan = null
}

function fillForm(d: ProposalDetail) {
  form.proposal_date = d.proposal_date
  form.received_date = d.received_date
  form.description = d.description
  form.nominal = d.nominal
  form.received_by = d.received_by
  form.reference_by = d.reference_by
  form.reference_position = d.reference_position
  form.status = d.status
  form.mustahiq_id = d.mustahiq_id
  form.mustahiq_name = d.mustahiq_name
  form.product_group_id = d.product_group_id
  form.product_group_name = d.product_group_name
  form.address_street = d.address_street
  form.address_kelurahan = d.address_kelurahan
  form.address_kecamatan = d.address_kecamatan
}

async function openCreate() {
  resetForm()
  await loadProductGroups()
  await loadMustahiqOptions()
  modalMode.value = 'create'
  modalError.value = null
  modalOpen.value = true
}

async function openEdit(row: ProposalRow) {
  selectedRow.value = row
  modalMode.value = 'edit'
  modalError.value = null
  modalLoading.value = true
  modalOpen.value = true
  try {
    await Promise.all([loadProductGroups(), loadMustahiqOptions()])
    const d = await api.get<ProposalDetail>(`/api/distribution/proposal/${row.proposal_id}`)
    detailData.value = d
    fillForm(d)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

async function openDetail(row: ProposalRow) {
  selectedRow.value = row
  modalMode.value = 'detail'
  modalError.value = null
  modalLoading.value = true
  modalOpen.value = true
  try {
    detailData.value = await api.get<ProposalDetail>(`/api/distribution/proposal/${row.proposal_id}`)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

function openDelete(row: ProposalRow) {
  selectedRow.value = row
  modalMode.value = 'delete'
  modalError.value = null
  modalOpen.value = true
}

function closeModal() { modalOpen.value = false }

// ── Save / Delete ────────────────────────────────────────────────────────────

async function saveForm() {
  // Validation
  if (!form.product_group_id) { modalError.value = 'Jenis program wajib dipilih.'; return }
  if (!form.mustahiq_id) { modalError.value = 'Mustahiq wajib dipilih.'; return }
  if (!form.proposal_date) { modalError.value = 'Tanggal proposal wajib diisi.'; return }
  if (!form.received_date) { modalError.value = 'Tanggal terima wajib diisi.'; return }
  if (!form.description.trim()) { modalError.value = 'Deskripsi wajib diisi.'; return }
  if (form.nominal <= 0) { modalError.value = 'Nominal harus lebih dari 0.'; return }

  modalLoading.value = true
  modalError.value = null
  try {
    const payload = {
      product_group_id: form.product_group_id,
      mustahiq_id: form.mustahiq_id,
      proposal_date: form.proposal_date,
      received_date: form.received_date,
      description: form.description.trim(),
      nominal: form.nominal,
      received_by: form.received_by || null,
      reference_by: form.reference_by || null,
      reference_position: form.reference_position || null,
    }
    if (modalMode.value === 'create') {
      await api.post('/api/distribution/proposal', payload)
      toast.success('Proposal bantuan dana berhasil ditambahkan.')
    } else {
      await api.put(`/api/distribution/proposal/${selectedRow.value!.proposal_id}`, payload)
      toast.success('Proposal bantuan dana berhasil diperbarui.')
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
  modalError.value = null
  try {
    await api.delete(`/api/distribution/proposal/${selectedRow.value.proposal_id}`)
    toast.success('Proposal bantuan dana berhasil dihapus.')
    closeModal()
    loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menghapus data.'
  } finally {
    modalLoading.value = false
  }
}

// ── Init default filter dates ─────────────────────────────────────────────────

function initDefaultDates() {
  const today = new Date()
  const firstDay = new Date(today.getFullYear(), today.getMonth(), 1)
  dateTo.value = today.toISOString().slice(0, 10)
  dateFrom.value = firstDay.toISOString().slice(0, 10)
}

onMounted(() => {
  initDefaultDates()
  loadProductGroups()
  loadMustahiqOptions()
  loadData()
})
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Proposal Bantuan Dana" subtitle="Manajemen proposal bantuan dana kepada mustahiq">
      <template #actions>
        <Button
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="openCreate"
        >
          <Plus class="w-3.5 h-3.5" />
          Tambah
        </Button>
      </template>
    </PageHeader>

    <!-- Error message -->
    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table (satu card bersambung) -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center gap-3 flex-wrap">
        <div class="flex items-end gap-2 flex-wrap">
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-muted-foreground">Tgl Terima Dari</label>
            <DateField v-model="dateFrom" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-muted-foreground">Sampai</label>
            <DateField v-model="dateTo" />
          </div>
        </div>

        <div class="relative flex-1 min-w-48 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input
            v-model="searchMustahiq"
            type="text"
            placeholder="Cari mustahiq..."
            class="w-full h-8 pl-8 pr-3 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>

        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-muted-foreground">Status</label>
          <select
            v-model="statusFilter"
            class="h-8 rounded px-2 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="">Semua</option>
            <option value="B">Baru</option>
            <option value="S">Disetujui</option>
          </select>
        </div>
      </div>

      <!-- Pagination (SELALU di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} proposal
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @prev="prevPage"
          @next="nextPage"
          @update:page-size="changePageSize"
        />
      </div>

      <!-- Tabel (TIDAK pakai DataTable PrimeVue dengan paginator) -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">No Proposal</th>
              <th class="px-4 py-2 text-left font-medium">Tgl Proposal</th>
              <th class="px-4 py-2 text-left font-medium">Tgl Terima</th>
              <th class="px-4 py-2 text-left font-medium">Mustahiq</th>
              <th class="px-4 py-2 text-left font-medium">Deskripsi</th>
              <th class="px-4 py-2 text-right font-medium">Nominal</th>
              <th class="px-4 py-2 text-center font-medium">Status</th>
              <th class="px-4 py-2 text-right font-medium w-24">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="8" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="8" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada data proposal yang ditemukan.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.proposal_id"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-1 text-xs font-mono">{{ row.proposal_no }}</td>
              <td class="px-4 py-1 text-xs">{{ dmy(row.proposal_date) }}</td>
              <td class="px-4 py-1 text-xs">{{ dmy(row.received_date) }}</td>
              <td class="px-4 py-1 text-xs">{{ row.mustahiq_name }}</td>
              <td class="px-4 py-1 text-xs text-muted-foreground truncate max-w-xs" :title="row.description">
                {{ row.description.length > 60 ? row.description.slice(0, 60) + '…' : row.description }}
              </td>
              <td class="px-4 py-1 text-xs text-right font-mono">
                {{ new Intl.NumberFormat('id-ID').format(row.nominal) }}
              </td>
              <td class="px-4 py-1 text-center">
                <span
                  class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="row.status === 'B'
                    ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
                    : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300'"
                >
                  {{ row.status === 'B' ? 'Baru' : 'Disetujui' }}
                </span>
              </td>
              <td class="px-4 py-1 text-right">
                <div class="flex items-center justify-end gap-1">
                  <button
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Lihat"
                    @click="openDetail(row)"
                  >
                    <Search class="w-3.5 h-3.5 text-muted-foreground" />
                  </button>
                  <button
                    v-if="row.status === 'B'"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Ubah"
                    @click="openEdit(row)"
                  >
                    <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                  </button>
                  <button
                    v-if="row.status === 'B'"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Hapus"
                    @click="openDelete(row)"
                  >
                    <Trash2 class="w-3.5 h-3.5 text-red-500" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Modals ──────────────────────────────────────────────────────────── -->

    <!-- Create / Edit -->
    <Modal v-if="modalOpen && (modalMode === 'create' || modalMode === 'edit')" max-width="max-w-2xl" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">{{ modalMode === 'create' ? 'Tambah Proposal Bantuan Dana' : 'Ubah Proposal Bantuan Dana' }}</h2>
      </template>

      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat data...</div>
      <div v-else class="space-y-4">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>

        <!-- Form fields -->
        <fieldset class="space-y-3">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium mb-1">Jenis Program <span class="text-red-500">*</span></label>
              <SearchSelect
                :model-value="form.product_group_id ? String(form.product_group_id) : ''"
                :options="productGroupOptions()"
                all-label="— Pilih jenis program —"
                @update:model-value="form.product_group_id = $event ? Number($event) : 0"
              />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Mustahiq <span class="text-red-500">*</span></label>
              <SearchSelect
                :model-value="form.mustahiq_id ? String(form.mustahiq_id) : ''"
                :options="mustahiqLookupOptions()"
                all-label="— Pilih mustahiq —"
                @update:model-value="async (v) => { form.mustahiq_id = v ? Number(v) : 0; if (form.mustahiq_id) await loadTotalByMustahiq(form.mustahiq_id) }"
              />
            </div>
          </div>

          <div v-if="form.mustahiq_id && totalProposalByMustahiq > 0" class="rounded border border-border bg-muted/20 px-3 py-2 text-xs text-muted-foreground">
            Jumlah Proposal Sebelumnya: <span class="font-semibold">{{ totalProposalByMustahiq }} proposal</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium mb-1">Tanggal Proposal <span class="text-red-500">*</span></label>
              <DateField v-model="form.proposal_date" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Tanggal Terima <span class="text-red-500">*</span></label>
              <DateField v-model="form.received_date" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium mb-1">Deskripsi <span class="text-red-500">*</span></label>
            <textarea
              v-model="form.description"
              class="w-full h-16 rounded-lg px-3 py-2 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="Deskripsi proposal bantuan dana"
            />
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium mb-1">Nominal <span class="text-red-500">*</span></label>
              <input
                v-model.number="form.nominal"
                type="number"
                min="0"
                class="w-full h-9 rounded-lg px-2.5 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
                placeholder="0"
              />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Diterima Oleh</label>
              <input
                v-model="form.received_by"
                type="text"
                class="w-full h-9 rounded-lg px-2.5 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
                placeholder="Nama penerima"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium mb-1">Referensi Oleh</label>
              <input
                v-model="form.reference_by"
                type="text"
                class="w-full h-9 rounded-lg px-2.5 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
                placeholder="Nama referensi"
              />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Posisi Referensi</label>
              <select
                v-model.number="form.reference_position"
                class="w-full h-9 rounded-lg px-2.5 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
              >
                <option :value="null">— Pilih posisi —</option>
                <option :value="1">Muzakki</option>
                <option :value="2">Non Muzakki</option>
                <option :value="3">Pengurus</option>
                <option :value="4">Pelaksana</option>
                <option :value="5">Dewan Syariah</option>
              </select>
            </div>
          </div>
        </fieldset>
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

    <!-- Detail -->
    <Modal v-if="modalOpen && modalMode === 'detail'" max-width="max-w-2xl" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">Detail Proposal Bantuan Dana</h2>
      </template>
      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat...</div>
      <div v-else-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
      <div v-else-if="detailData" class="space-y-4 text-sm">
        <div class="grid grid-cols-2 gap-x-6 gap-y-2">
          <div><span class="text-xs text-muted-foreground">No Proposal</span><p class="font-mono">{{ detailData.proposal_no }}</p></div>
          <div><span class="text-xs text-muted-foreground">Status</span>
            <p>
              <span class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                :class="detailData.status === 'B' ? 'bg-yellow-100 text-yellow-800' : 'bg-emerald-100 text-emerald-700'">
                {{ detailData.status === 'B' ? 'Baru' : 'Disetujui' }}
              </span>
            </p>
          </div>
          <div><span class="text-xs text-muted-foreground">Jenis Program</span><p class="font-medium">{{ detailData.product_group_name }}</p></div>
          <div><span class="text-xs text-muted-foreground">Mustahiq</span><p class="font-medium">{{ detailData.mustahiq_name }}</p></div>
          <div><span class="text-xs text-muted-foreground">Tgl Proposal</span><p>{{ dmy(detailData.proposal_date) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Tgl Terima</span><p>{{ dmy(detailData.received_date) }}</p></div>
          <div class="col-span-2"><span class="text-xs text-muted-foreground">Deskripsi</span><p>{{ detailData.description }}</p></div>
          <div><span class="text-xs text-muted-foreground">Nominal</span><p class="font-mono">{{ new Intl.NumberFormat('id-ID').format(detailData.nominal) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Diterima Oleh</span><p>{{ detailData.received_by || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Referensi Oleh</span><p>{{ detailData.reference_by || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Posisi Referensi</span><p>
            {{ detailData.reference_position ? (['Muzakki', 'Non Muzakki', 'Pengurus', 'Pelaksana', 'Dewan Syariah'][detailData.reference_position - 1] || '—') : '—' }}
          </p></div>
          <div class="col-span-2"><span class="text-xs text-muted-foreground">Alamat</span><p>{{ detailData.address_street || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Kelurahan</span><p>{{ detailData.address_kelurahan || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Kecamatan</span><p>{{ detailData.address_kecamatan || '—' }}</p></div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end"><Button variant="outline" size="sm" @click="closeModal">Tutup</Button></div>
      </template>
    </Modal>

    <!-- Delete -->
    <Modal v-if="modalOpen && modalMode === 'delete'" max-width="max-w-md" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold text-red-600">Hapus Proposal Bantuan Dana</h2>
      </template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <p class="text-sm text-muted-foreground">Data proposal berikut akan dihapus permanen:</p>
        <div class="rounded border border-border bg-muted/30 px-4 py-3 text-sm space-y-1">
          <div class="font-semibold">{{ selectedRow?.proposal_no }}</div>
          <div class="text-xs text-muted-foreground">Mustahiq: {{ selectedRow?.mustahiq_name }}</div>
          <div class="text-xs text-muted-foreground">Nominal: {{ selectedRow ? new Intl.NumberFormat('id-ID').format(selectedRow.nominal) : '—' }}</div>
          <div class="text-xs text-muted-foreground">Tanggal Terima: {{ selectedRow ? dmy(selectedRow.received_date) : '—' }}</div>
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

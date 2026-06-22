<script setup lang="ts">
import { Eye, Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'
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
import { useAuthStore } from '@/app/stores/auth.store'

// ── Types ─────────────────────────────────────────────────────────────────────

interface PersonItem {
  id?: number
  name: string
  unit_field: string
}

interface MonitoringVisitRow {
  visit_id: number
  visit_date: string
  mustahiq_name: string
  program_name: string | null
  mustahiq_product_name: string | null
  visit_location: string
}

interface MonitoringVisitDetail extends MonitoringVisitRow {
  mustahiq_id: number
  mustahiq_product_id: number | null
  visit_address: string
  persons_amil: PersonItem[]
  persons_mustahiq: PersonItem[]
  purposes: string[]
  results: string[]
  followups: string[]
}

interface PaginationState {
  page: number
  page_size: number
  total: number
  total_pages: number
}

interface MustahiqLookupItem {
  mustahiq_id: number
  mustahiq_name: string
  address: string | null
}

interface ProgramLookupItem {
  mustahiq_product_id: number
  program_name: string | null
  mustahiq_product_name: string | null
  mustahiq_name: string | null
}

// ── Constants ─────────────────────────────────────────────────────────────────

const API_PREFIX = '/api/distribution/monitoring-visits'
const PAGE_TITLE = 'Monitoring Program Penyaluran'

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const auth = useAuthStore()

const rows = ref<MonitoringVisitRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const hasLoaded = shallowRef(false)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)

// Filters
const beginDate = ref('')
const endDate = ref('')

// Lookups
const mustahiqOptions = ref<MustahiqLookupItem[]>([])
const programOptions = ref<ProgramLookupItem[]>([])
const loadingMustahiq = shallowRef(false)
const loadingPrograms = shallowRef(false)

// Modal state
const showForm = shallowRef(false)
const formMode = shallowRef<'create' | 'edit' | 'view'>('create')
const showDelete = shallowRef(false)
const selected = ref<MonitoringVisitDetail | null>(null)

// Form state
const form = reactive({
  mustahiq_id: null as number | null,
  mustahiq_product_id: null as number | null,
  visit_address: '',
  visit_location: '',
  visit_date: '',
  persons_amil: [] as PersonItem[],
  persons_mustahiq: [] as PersonItem[],
  purposes: [] as string[],
  results: [] as string[],
  followups: [] as string[],
})

// ── Initialization ────────────────────────────────────────────────────────────

function getTodayISO(): string {
  const today = new Date()
  return today.toISOString().split('T')[0]
}

onMounted(() => {
  beginDate.value = getTodayISO()
  endDate.value = getTodayISO()
})

// ── API Calls ─────────────────────────────────────────────────────────────────

async function loadData() {
  if (!hasLoaded.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      page_size: String(pageSize.value),
      begin_date: beginDate.value,
      end_date: endDate.value,
    })
    const res = await api.get<{
      rows: MonitoringVisitRow[]
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

async function loadMustahiq(search: string) {
  loadingMustahiq.value = true
  try {
    const params = new URLSearchParams({ search })
    const res = await api.get<{ items: MustahiqLookupItem[] }>(
      `/api/distribution/monitoring-visits/lookup/mustahiq?${params}`,
    )
    mustahiqOptions.value = res.items
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal',
      detail: 'Gagal memuat daftar mustahiq',
      life: 3000,
    })
  } finally {
    loadingMustahiq.value = false
  }
}

async function loadPrograms(search: string) {
  if (!form.mustahiq_id) {
    programOptions.value = []
    return
  }
  loadingPrograms.value = true
  try {
    const params = new URLSearchParams({
      mustahiq_id: String(form.mustahiq_id),
      search,
    })
    const res = await api.get<{ items: ProgramLookupItem[] }>(
      `/api/distribution/monitoring-visits/lookup/programs?${params}`,
    )
    programOptions.value = res.items
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal',
      detail: 'Gagal memuat daftar program',
      life: 3000,
    })
  } finally {
    loadingPrograms.value = false
  }
}

async function getDetail(visitId: number) {
  try {
    const res = await api.get<MonitoringVisitDetail>(`${API_PREFIX}/${visitId}`)
    return res
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal',
      detail: 'Gagal memuat detail data',
      life: 3000,
    })
    return null
  }
}

async function saveVisit() {
  // ── Validasi ────────────────────────────────────────────────────────────
  const errors: string[] = []

  if (form.mustahiq_id === null || form.mustahiq_id === 0) {
    errors.push('Mustahiq harus dipilih')
  }
  if (form.visit_address.trim() === '') {
    errors.push('Alamat harus diisi')
  }
  if (form.visit_location.trim() === '') {
    errors.push('Tempat pertemuan harus diisi')
  }
  if (form.visit_date === '') {
    errors.push('Tanggal pelaksanaan harus diisi')
  }
  if (form.persons_amil.length === 0) {
    errors.push('Minimal 1 pihak BPZIS harus ditambahkan')
  }
  if (form.persons_mustahiq.length === 0) {
    errors.push('Minimal 1 pihak mustahiq harus ditambahkan')
  }
  if (form.purposes.length === 0) {
    errors.push('Minimal 1 tujuan kunjungan harus ditambahkan')
  }
  if (form.results.length === 0) {
    errors.push('Minimal 1 hasil kunjungan harus ditambahkan')
  }
  if (form.followups.length === 0) {
    errors.push('Minimal 1 tindak lanjut harus ditambahkan')
  }

  if (errors.length > 0) {
    toast.add({
      severity: 'error',
      summary: 'Validasi Gagal',
      detail: errors.join('; '),
      life: 5000,
    })
    return
  }

  loading.value = true
  try {
    const payload = {
      mustahiq_id: form.mustahiq_id,
      mustahiq_product_id: form.mustahiq_product_id,
      visit_address: form.visit_address,
      visit_location: form.visit_location,
      visit_date: form.visit_date,
      persons_amil: form.persons_amil,
      persons_mustahiq: form.persons_mustahiq,
      purposes: form.purposes,
      results: form.results,
      followups: form.followups,
    }

    if (formMode.value === 'create') {
      await api.post(API_PREFIX, payload)
      toast.add({
        severity: 'success',
        summary: 'Berhasil',
        detail: 'Monitoring kunjungan berhasil ditambahkan',
        life: 3000,
      })
    } else if (formMode.value === 'edit' && selected.value) {
      await api.put(`${API_PREFIX}/${selected.value.visit_id}`, payload)
      toast.add({
        severity: 'success',
        summary: 'Berhasil',
        detail: 'Monitoring kunjungan berhasil disimpan',
        life: 3000,
      })
    }

    showForm.value = false
    await loadData()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal',
      detail: e instanceof ApiError ? e.message : 'Gagal menyimpan data',
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

async function deleteVisit() {
  if (!selected.value) return
  loading.value = true
  try {
    await api.delete(`${API_PREFIX}/${selected.value.visit_id}`)
    toast.add({
      severity: 'success',
      summary: 'Berhasil',
      detail: 'Monitoring kunjungan berhasil dihapus',
      life: 3000,
    })
    showDelete.value = false
    await loadData()
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal',
      detail: e instanceof ApiError ? e.message : 'Gagal menghapus data',
      life: 5000,
    })
  } finally {
    loading.value = false
  }
}

// ── Modal Actions ────────────────────────────────────────────────────────────

function openAdd() {
  formMode.value = 'create'
  selected.value = null
  resetForm()
  showForm.value = true
}

async function openEdit(row: MonitoringVisitRow) {
  const detail = await getDetail(row.visit_id)
  if (!detail) return
  formMode.value = 'edit'
  selected.value = detail
  populateForm(detail)
  showForm.value = true
}

async function openView(row: MonitoringVisitRow) {
  const detail = await getDetail(row.visit_id)
  if (!detail) return
  formMode.value = 'view'
  selected.value = detail
  populateForm(detail)
  showForm.value = true
}

async function openDelete(row: MonitoringVisitRow) {
  const detail = await getDetail(row.visit_id)
  if (!detail) return
  selected.value = detail
  showDelete.value = true
}

function resetForm() {
  form.mustahiq_id = null
  form.mustahiq_product_id = null
  form.visit_address = ''
  form.visit_location = ''
  form.visit_date = ''
  form.persons_amil = []
  form.persons_mustahiq = []
  form.purposes = []
  form.results = []
  form.followups = []
  mustahiqOptions.value = []
  programOptions.value = []
}

function populateForm(detail: MonitoringVisitDetail) {
  form.mustahiq_id = detail.mustahiq_id
  form.mustahiq_product_id = detail.mustahiq_product_id
  form.visit_address = detail.visit_address
  form.visit_location = detail.visit_location
  form.visit_date = detail.visit_date
  form.persons_amil = JSON.parse(JSON.stringify(detail.persons_amil || []))
  form.persons_mustahiq = JSON.parse(JSON.stringify(detail.persons_mustahiq || []))
  form.purposes = JSON.parse(JSON.stringify(detail.purposes || []))
  form.results = JSON.parse(JSON.stringify(detail.results || []))
  form.followups = JSON.parse(JSON.stringify(detail.followups || []))
}

function closeModal() {
  showForm.value = false
  resetForm()
}

// ── Form Item Actions ────────────────────────────────────────────────────────

function addPersonAmil() {
  form.persons_amil.push({ name: '', unit_field: '' })
}

function removePersonAmil(idx: number) {
  form.persons_amil.splice(idx, 1)
}

function addPersonMustahiq() {
  form.persons_mustahiq.push({ name: '', unit_field: '' })
}

function removePersonMustahiq(idx: number) {
  form.persons_mustahiq.splice(idx, 1)
}

function addPurpose() {
  form.purposes.push('')
}

function removePurpose(idx: number) {
  form.purposes.splice(idx, 1)
}

function addResult() {
  form.results.push('')
}

function removeResult(idx: number) {
  form.results.splice(idx, 1)
}

function addFollowup() {
  form.followups.push('')
}

function removeFollowup(idx: number) {
  form.followups.splice(idx, 1)
}

// ── Mustahiq Selection Handler ────────────────────────────────────────────────

function onMustahiqChange(mustahiqId: number | null) {
  form.mustahiq_id = mustahiqId
  form.mustahiq_product_id = null
  if (mustahiqId) {
    const selected = mustahiqOptions.value.find((m) => m.mustahiq_id === mustahiqId)
    if (selected) {
      form.visit_address = selected.address || ''
    }
  }
}
</script>

<template>
  <div class="space-y-4">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-foreground">{{ PAGE_TITLE }}</h1>
        <p class="text-sm text-muted-foreground mt-1">Pantau kegiatan kunjungan dan interaksi dengan penerima manfaat</p>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="errorMsg" class="flex items-center gap-2 rounded-lg border border-red-200
                                 bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Filter Card -->
    <div class="rounded-xl border border-border bg-surface p-4">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-foreground">Tanggal Awal</label>
          <DateField v-model="beginDate" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium text-foreground">Tanggal Akhir</label>
          <DateField v-model="endDate" />
        </div>
        <Button :loading="loading" @click="tampilkan">Tampilkan Data</Button>
      </div>
    </div>

    <!-- Empty State (before data is loaded) -->
    <div v-if="!hasLoaded" class="flex flex-col items-center justify-center h-48 rounded-xl border border-dashed border-border bg-muted/50">
      <p class="text-muted-foreground text-sm">Pilih periode lalu klik "Tampilkan Data" untuk melihat monitoring kunjungan</p>
    </div>

    <!-- Table Card (after data is loaded) -->
    <template v-else>
      <div class="rounded-xl border border-border bg-surface overflow-hidden">

        <!-- Toolbar -->
        <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3">
          <div class="relative flex-1 max-w-xs">
            <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
            <input
              placeholder="Cari..."
              disabled
              class="h-8 w-full rounded pl-8 pr-3 text-xs border border-border bg-background
                     focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
            />
          </div>
          <Button
            v-if="auth.roles?.includes('DIST')"
            size="sm"
            @click="openAdd"
          >
            <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
          </Button>
        </div>

        <!-- Pagination (above table) -->
        <div class="px-4 py-2 border-b border-border flex items-center justify-between">
          <span class="text-[11px] text-muted tabular-nums">
            <template v-if="loading">Memuat...</template>
            <template v-else-if="totalRec > 0">
              {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} data
            </template>
            <template v-else>Tidak ada data</template>
          </span>
          <TablePagination
            :page="page"
            :total-pages="totalPages"
            :total="totalRec"
            :page-size="pageSize"
            @prev="page > 1 && (page--, loadData())"
            @next="page < totalPages && (page++, loadData())"
            @update:page-size="(s) => { pageSize = s; page = 1; loadData() }"
          />
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
              <tr>
                <th class="px-4 py-2 text-left font-medium">Tanggal</th>
                <th class="px-4 py-2 text-left font-medium">Mustahiq</th>
                <th class="px-4 py-2 text-left font-medium">Program</th>
                <th class="px-4 py-2 text-left font-medium">Detail Program</th>
                <th class="px-4 py-2 text-left font-medium">Lokasi</th>
                <th class="px-4 py-2 text-right font-medium w-32">Aksi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-if="loading">
                <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
              </tr>
              <tr v-else-if="!rows.length">
                <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                  Tidak ada data yang ditemukan.
                </td>
              </tr>
              <tr
                v-for="row in rows"
                :key="row.visit_id"
                class="hover:bg-muted/30 transition-colors"
              >
                <td class="px-4 py-1 text-xs">{{ dmy(row.visit_date) }}</td>
                <td class="px-4 py-1 text-xs">{{ row.mustahiq_name }}</td>
                <td class="px-4 py-1 text-xs">{{ row.program_name || '–' }}</td>
                <td class="px-4 py-1 text-xs">{{ row.mustahiq_product_name || '–' }}</td>
                <td class="px-4 py-1 text-xs">{{ row.visit_location }}</td>
                <td class="px-4 py-1 text-right">
                  <div class="flex items-center justify-end gap-1">
                    <button
                      class="p-1 rounded hover:bg-muted transition-colors"
                      title="Lihat"
                      @click="openView(row)"
                    >
                      <Eye class="w-3.5 h-3.5 text-muted-foreground" />
                    </button>
                    <button
                      v-if="auth.roles?.includes('DIST')"
                      class="p-1 rounded hover:bg-muted transition-colors"
                      title="Ubah"
                      @click="openEdit(row)"
                    >
                      <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                    </button>
                    <button
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
    </template>
  </div>

  <!-- Form Modal -->
  <Dialog
    v-model:visible="showForm"
    :header="formMode === 'create' ? 'Tambah Monitoring Kunjungan' : (formMode === 'edit' ? 'Ubah Monitoring Kunjungan' : 'Detail Monitoring Kunjungan')"
    :modal="true"
    class="w-full max-w-2xl"
    @hide="closeModal"
  >
    <template #default>
      <div class="space-y-4">
        <!-- Tab View -->
        <TabView>
          <!-- Tab 1: Data Utama -->
          <TabPanel header="Data Utama" headerClass="text-xs sm:text-sm">
            <div class="space-y-4 pr-4">
              <!-- Mustahiq -->
              <div class="flex flex-col gap-1">
                <label class="text-sm font-medium text-foreground">Nama Mustahiq <span class="text-red-500">*</span></label>
                <SearchSelect
                  v-model="form.mustahiq_id"
                  :options="mustahiqOptions.map((m) => ({
                    value: String(m.mustahiq_id),
                    label: m.mustahiq_name,
                  }))"
                  :disabled="formMode === 'view' || loadingMustahiq"
                  placeholder="Pilih atau ketik nama mustahiq..."
                  @search="loadMustahiq"
                  @update:model-value="onMustahiqChange"
                />
              </div>

              <!-- Program Penyaluran -->
              <div class="flex flex-col gap-1">
                <label class="text-sm font-medium text-foreground">Program Penyaluran</label>
                <SearchSelect
                  v-model="form.mustahiq_product_id"
                  :options="programOptions.map((p) => ({
                    value: String(p.mustahiq_product_id),
                    label: `${p.mustahiq_product_name || '–'} - ${p.program_name || '–'}`,
                  }))"
                  :disabled="formMode === 'view' || !form.mustahiq_id || loadingPrograms"
                  placeholder="Pilih atau ketik nama program..."
                  @search="loadPrograms"
                />
              </div>

              <!-- Alamat -->
              <div class="flex flex-col gap-1">
                <label class="text-sm font-medium text-foreground">Alamat <span class="text-red-500">*</span></label>
                <textarea
                  v-model="form.visit_address"
                  :disabled="formMode === 'view'"
                  maxlength="200"
                  rows="2"
                  class="rounded-lg border border-border bg-background px-2.5 py-1.5 text-xs
                         focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                  placeholder="Masukkan alamat..."
                />
                <span class="text-[10px] text-muted-foreground">{{ form.visit_address.length }}/200</span>
              </div>

              <!-- Tempat Pertemuan -->
              <div class="flex flex-col gap-1">
                <label class="text-sm font-medium text-foreground">Tempat Pertemuan <span class="text-red-500">*</span></label>
                <textarea
                  v-model="form.visit_location"
                  :disabled="formMode === 'view'"
                  maxlength="200"
                  rows="2"
                  class="rounded-lg border border-border bg-background px-2.5 py-1.5 text-xs
                         focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                  placeholder="Masukkan tempat pertemuan..."
                />
                <span class="text-[10px] text-muted-foreground">{{ form.visit_location.length }}/200</span>
              </div>

              <!-- Tanggal Pelaksanaan -->
              <div class="flex flex-col gap-1">
                <label class="text-sm font-medium text-foreground">Tanggal Pelaksanaan <span class="text-red-500">*</span></label>
                <DateField v-model="form.visit_date" :disabled="formMode === 'view'" />
              </div>
            </div>
          </TabPanel>

          <!-- Tab 2: Pihak Yang Bertemu -->
          <TabPanel header="Pihak Yang Bertemu" headerClass="text-xs sm:text-sm">
            <div class="space-y-6 pr-4">
              <!-- Pihak BPZIS -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-sm font-semibold text-foreground">Pihak BPZIS <span class="text-red-500">*</span></h3>
                  <Button
                    v-if="formMode !== 'view'"
                    size="sm"
                    variant="outline"
                    @click="addPersonAmil"
                  >
                    <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
                  </Button>
                </div>
                <div class="overflow-x-auto border border-border rounded-lg">
                  <table class="w-full text-xs">
                    <thead class="bg-muted border-b border-border">
                      <tr>
                        <th class="px-3 py-2 text-left font-medium">Nama</th>
                        <th class="px-3 py-2 text-left font-medium">Unit Kerja/Bidang</th>
                        <th v-if="formMode !== 'view'" class="px-3 py-2 text-right font-medium w-12">Aksi</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-border">
                      <tr v-if="form.persons_amil.length === 0">
                        <td :colspan="formMode === 'view' ? 2 : 3" class="px-3 py-2 text-center text-muted-foreground italic">
                          Belum ada pihak
                        </td>
                      </tr>
                      <tr v-for="(person, idx) in form.persons_amil" :key="idx">
                        <td class="px-3 py-2">
                          <input
                            v-model="person.name"
                            :disabled="formMode === 'view'"
                            type="text"
                            maxlength="100"
                            class="w-full border border-border rounded px-2 py-1 text-xs
                                   focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                            placeholder="Nama..."
                          />
                        </td>
                        <td class="px-3 py-2">
                          <input
                            v-model="person.unit_field"
                            :disabled="formMode === 'view'"
                            type="text"
                            maxlength="100"
                            class="w-full border border-border rounded px-2 py-1 text-xs
                                   focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                            placeholder="Unit..."
                          />
                        </td>
                        <td v-if="formMode !== 'view'" class="px-3 py-2 text-right">
                          <button
                            class="p-1 rounded hover:bg-muted transition-colors"
                            @click="removePersonAmil(idx)"
                          >
                            <Trash2 class="w-3.5 h-3.5 text-red-500" />
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <!-- Pihak Mustahiq -->
              <div>
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-sm font-semibold text-foreground">Pihak Mustahiq/Yayasan <span class="text-red-500">*</span></h3>
                  <Button
                    v-if="formMode !== 'view'"
                    size="sm"
                    variant="outline"
                    @click="addPersonMustahiq"
                  >
                    <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
                  </Button>
                </div>
                <div class="overflow-x-auto border border-border rounded-lg">
                  <table class="w-full text-xs">
                    <thead class="bg-muted border-b border-border">
                      <tr>
                        <th class="px-3 py-2 text-left font-medium">Nama</th>
                        <th class="px-3 py-2 text-left font-medium">Unit Kerja/Bidang</th>
                        <th v-if="formMode !== 'view'" class="px-3 py-2 text-right font-medium w-12">Aksi</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-border">
                      <tr v-if="form.persons_mustahiq.length === 0">
                        <td :colspan="formMode === 'view' ? 2 : 3" class="px-3 py-2 text-center text-muted-foreground italic">
                          Belum ada pihak
                        </td>
                      </tr>
                      <tr v-for="(person, idx) in form.persons_mustahiq" :key="idx">
                        <td class="px-3 py-2">
                          <input
                            v-model="person.name"
                            :disabled="formMode === 'view'"
                            type="text"
                            maxlength="100"
                            class="w-full border border-border rounded px-2 py-1 text-xs
                                   focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                            placeholder="Nama..."
                          />
                        </td>
                        <td class="px-3 py-2">
                          <input
                            v-model="person.unit_field"
                            :disabled="formMode === 'view'"
                            type="text"
                            maxlength="100"
                            class="w-full border border-border rounded px-2 py-1 text-xs
                                   focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                            placeholder="Unit..."
                          />
                        </td>
                        <td v-if="formMode !== 'view'" class="px-3 py-2 text-right">
                          <button
                            class="p-1 rounded hover:bg-muted transition-colors"
                            @click="removePersonMustahiq(idx)"
                          >
                            <Trash2 class="w-3.5 h-3.5 text-red-500" />
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </TabPanel>

          <!-- Tab 3: Tujuan Kunjungan -->
          <TabPanel header="Tujuan Kunjungan" headerClass="text-xs sm:text-sm">
            <div class="space-y-3 pr-4">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-semibold text-foreground">Tujuan Kunjungan <span class="text-red-500">*</span></h3>
                <Button
                  v-if="formMode !== 'view'"
                  size="sm"
                  variant="outline"
                  @click="addPurpose"
                >
                  <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
                </Button>
              </div>
              <div v-if="form.purposes.length === 0" class="text-center text-muted-foreground text-xs italic py-4">
                Belum ada tujuan
              </div>
              <div v-for="(purpose, idx) in form.purposes" :key="idx" class="flex gap-2">
                <textarea
                  v-model="form.purposes[idx]"
                  :disabled="formMode === 'view'"
                  maxlength="200"
                  rows="2"
                  class="flex-1 rounded-lg border border-border bg-background px-2.5 py-1.5 text-xs
                         focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                  placeholder="Masukkan tujuan kunjungan..."
                />
                <button
                  v-if="formMode !== 'view'"
                  class="p-1 rounded hover:bg-muted transition-colors mt-1"
                  @click="removePurpose(idx)"
                >
                  <Trash2 class="w-3.5 h-3.5 text-red-500" />
                </button>
              </div>
            </div>
          </TabPanel>

          <!-- Tab 4: Hasil Kunjungan -->
          <TabPanel header="Hasil Kunjungan" headerClass="text-xs sm:text-sm">
            <div class="space-y-3 pr-4">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-semibold text-foreground">Hasil Kunjungan <span class="text-red-500">*</span></h3>
                <Button
                  v-if="formMode !== 'view'"
                  size="sm"
                  variant="outline"
                  @click="addResult"
                >
                  <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
                </Button>
              </div>
              <div v-if="form.results.length === 0" class="text-center text-muted-foreground text-xs italic py-4">
                Belum ada hasil
              </div>
              <div v-for="(result, idx) in form.results" :key="idx" class="flex gap-2">
                <textarea
                  v-model="form.results[idx]"
                  :disabled="formMode === 'view'"
                  maxlength="200"
                  rows="2"
                  class="flex-1 rounded-lg border border-border bg-background px-2.5 py-1.5 text-xs
                         focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                  placeholder="Masukkan hasil kunjungan..."
                />
                <button
                  v-if="formMode !== 'view'"
                  class="p-1 rounded hover:bg-muted transition-colors mt-1"
                  @click="removeResult(idx)"
                >
                  <Trash2 class="w-3.5 h-3.5 text-red-500" />
                </button>
              </div>
            </div>
          </TabPanel>

          <!-- Tab 5: Tindak Lanjut -->
          <TabPanel header="Tindak Lanjut" headerClass="text-xs sm:text-sm">
            <div class="space-y-3 pr-4">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-semibold text-foreground">Tindak Lanjut <span class="text-red-500">*</span></h3>
                <Button
                  v-if="formMode !== 'view'"
                  size="sm"
                  variant="outline"
                  @click="addFollowup"
                >
                  <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
                </Button>
              </div>
              <div v-if="form.followups.length === 0" class="text-center text-muted-foreground text-xs italic py-4">
                Belum ada tindak lanjut
              </div>
              <div v-for="(followup, idx) in form.followups" :key="idx" class="flex gap-2">
                <textarea
                  v-model="form.followups[idx]"
                  :disabled="formMode === 'view'"
                  maxlength="200"
                  rows="2"
                  class="flex-1 rounded-lg border border-border bg-background px-2.5 py-1.5 text-xs
                         focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50"
                  placeholder="Masukkan tindak lanjut..."
                />
                <button
                  v-if="formMode !== 'view'"
                  class="p-1 rounded hover:bg-muted transition-colors mt-1"
                  @click="removeFollowup(idx)"
                >
                  <Trash2 class="w-3.5 h-3.5 text-red-500" />
                </button>
              </div>
            </div>
          </TabPanel>
        </TabView>
      </div>
    </template>

    <template #footer>
      <div class="flex items-center justify-end gap-2">
        <Button
          variant="outline"
          @click="closeModal"
        >
          Batal
        </Button>
        <Button
          v-if="formMode !== 'view'"
          :loading="loading"
          @click="saveVisit"
        >
          Simpan
        </Button>
      </div>
    </template>
  </Dialog>

  <!-- Delete Confirmation Modal -->
  <Dialog
    v-model:visible="showDelete"
    header="Hapus Monitoring Kunjungan"
    :modal="true"
    class="w-full max-w-sm"
  >
    <template #default>
      <div v-if="selected" class="space-y-3">
        <p class="text-sm text-foreground">Apakah Anda yakin ingin menghapus monitoring kunjungan berikut?</p>
        <div class="bg-muted rounded-lg p-3 space-y-2">
          <div class="flex justify-between">
            <span class="text-xs text-muted-foreground">Tanggal:</span>
            <span class="text-xs font-medium text-foreground">{{ dmy(selected.visit_date) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-xs text-muted-foreground">Mustahiq:</span>
            <span class="text-xs font-medium text-foreground">{{ selected.mustahiq_name }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-xs text-muted-foreground">Lokasi:</span>
            <span class="text-xs font-medium text-foreground">{{ selected.visit_location }}</span>
          </div>
        </div>
        <p class="text-xs text-red-600">Data yang dihapus tidak dapat dipulihkan.</p>
      </div>
    </template>

    <template #footer>
      <div class="flex items-center justify-end gap-2">
        <Button
          variant="outline"
          @click="showDelete = false"
        >
          Batal
        </Button>
        <Button
          variant="destructive"
          :loading="loading"
          @click="deleteVisit"
        >
          Hapus
        </Button>
      </div>
    </template>
  </Dialog>
</template>

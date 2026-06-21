<script setup lang="ts">
import {
  CheckCircle2, Pencil, Plus, Search, Trash2, X, XCircle,
} from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'

// ── Types ─────────────────────────────────────────────────────────────────────

interface MustahiqRow {
  mustahiq_id: number
  no_mustahiq: string | null
  name: string | null
  address: string | null
  phone_number: string | null
  status: string | null
}

interface BankAccountItem {
  bank_account_id: number | null
  account_no: string
  account_name: string
  bank_code: string
  is_default: string
}

interface PersonalDetail {
  mustahiq_id: number
  no_mustahiq: string | null
  name: string
  address: string | null
  address_kelurahan: string | null
  address_kecamatan: string | null
  province_id: number | null
  postal_code: string | null
  reference_by: string | null
  phone_number: string | null
  gender: string | null
  ashnaf: string | null
  birth_place: string | null
  birth_date: string | null
  identity_number: string | null
  identity_type: string | null
  religion: number | null
  total_family: number | null
  formal_education: string | null
  income: number | null
  marital: string | null
  work_sector: string | null
  status: string | null
  bank_accounts: BankAccountItem[]
}

interface Pagination { page: number; page_size: number; total: number; total_pages: number }
interface ListResponse { rows: MustahiqRow[]; pagination: Pagination }
interface ProvinceLookup { province_id: number; province_name: string }
interface BankLookup { bank_code: string; bank_short_name: string | null; bank_name: string | null }

// ── Enum options ──────────────────────────────────────────────────────────────

const GENDER_OPTIONS     = [{ value: 'L', label: 'Laki-Laki' }, { value: 'P', label: 'Perempuan' }]
const IDENTITY_OPTIONS   = [{ value: 'K', label: 'KTP' }, { value: 'S', label: 'SIM' }, { value: 'F', label: 'Kartu Keluarga' }, { value: 'P', label: 'Passport' }]
const RELIGION_OPTIONS   = [1,2,3,4,5,6].map((v, i) => ({ value: String(v), label: ['Islam','Katolik','Protestan','Hindu','Budha','Aliran Kepercayaan'][i] }))
const MARITAL_OPTIONS    = [{ value: 'K', label: 'Menikah' }, { value: 'B', label: 'Belum Menikah' }, { value: 'S', label: 'Duda/Janda' }]
const EDUCATION_OPTIONS  = ['0','1','2','3','4','5','6'].map((v, i) => ({ value: v, label: ['Tdk Sekolah Formal','SD','SMP','SMU/Sederajat','S1','S2','S3'][i] }))
const ASHNAF_OPTIONS     = [
  { value: 'F', label: 'Fakir' }, { value: 'M', label: 'Miskin' }, { value: 'U', label: 'Mualaf' },
  { value: 'H', label: 'Hamba Sahaya' }, { value: 'G', label: 'Gharimin' }, { value: 'S', label: 'Fisabilillah' },
  { value: 'I', label: 'Ibnu Sabil' }, { value: 'A', label: 'Amil' },
]
const SECTOR_OPTIONS     = [1,2,3,4,5,6,7,8,9].map((v, i) => ({ value: String(v), label: [
  'Pertanian/Perkebunan/Perikanan','Pertambangan','Industri/Pabrik','Listrik/Gas/Air',
  'Konstruksi','Perdagangan','Pengangkutan/Pergudangan/Komunikasi','Jasa Keuangan','Jasa Sosial',
][i] }))

function labelOf(opts: {value: string; label: string}[], val: string | null | undefined) {
  if (!val) return '—'
  return opts.find(o => o.value === String(val))?.label ?? val
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const auth  = useAuthStore()

const rows       = ref<MustahiqRow[]>([])
const loading    = shallowRef(false)
const errorMsg   = shallowRef<string | null>(null)
const page       = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec   = shallowRef(0)
const pageSize   = shallowRef(25)
const searchInput = ref('')

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

// ── Lookups ───────────────────────────────────────────────────────────────────

const provinces = ref<ProvinceLookup[]>([])
const banks     = ref<BankLookup[]>([])

async function loadLookups() {
  try {
    const [prov, bank] = await Promise.all([
      api.get<any>('/api/distribution/mustahiq/lookup/provinces'),
      api.get<any>('/api/distribution/mustahiq/lookup/banks'),
    ])
    provinces.value = prov?.data ?? prov
    banks.value     = bank?.data ?? bank
  } catch { /* non-critical */ }
}

const provinceOptions = () => provinces.value.map(p => ({ value: String(p.province_id), label: p.province_name }))
const bankOptions     = () => banks.value.map(b => ({ value: b.bank_code, label: `${b.bank_short_name ?? b.bank_code} — ${b.bank_name ?? ''}` }))

// ── List ──────────────────────────────────────────────────────────────────────

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    const res = await api.get<ListResponse>(`/api/distribution/mustahiq/personal?${params}`)
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

function prevPage() { if (page.value > 1) { page.value--; loadData() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadData() } }
function changePageSize(s: number) { pageSize.value = s; page.value = 1; loadData() }

// ── Modal state ───────────────────────────────────────────────────────────────

type ModalMode = 'create' | 'edit' | 'detail' | 'delete' | 'status'

const modalMode    = shallowRef<ModalMode>('create')
const modalOpen    = shallowRef(false)
const modalLoading = shallowRef(false)
const modalError   = shallowRef<string | null>(null)
const selectedRow  = ref<MustahiqRow | null>(null)
const detailData   = ref<PersonalDetail | null>(null)
const pendingStatus = shallowRef<'A' | 'N'>('A')

const form = reactive({
  name: '' as string,
  address: null as string | null,
  address_kelurahan: null as string | null,
  address_kecamatan: null as string | null,
  province_id: null as number | null,
  postal_code: null as string | null,
  reference_by: null as string | null,
  phone_number: null as string | null,
  gender: null as string | null,
  ashnaf: null as string | null,
  birth_place: null as string | null,
  birth_date: null as string | null,
  identity_number: null as string | null,
  identity_type: null as string | null,
  religion: null as number | null,
  total_family: null as number | null,
  formal_education: null as string | null,
  income: null as number | null,
  marital: null as string | null,
  work_sector: null as string | null,
  bank_accounts: [] as BankAccountItem[],
})

function resetForm() {
  Object.assign(form, {
    name: '', address: null, address_kelurahan: null, address_kecamatan: null,
    province_id: null, postal_code: null, reference_by: null, phone_number: null,
    gender: null, ashnaf: null, birth_place: null, birth_date: null,
    identity_number: null, identity_type: null, religion: null, total_family: null,
    formal_education: null, income: null, marital: null, work_sector: null,
    bank_accounts: [],
  })
}

function fillForm(d: PersonalDetail) {
  Object.assign(form, {
    name: d.name, address: d.address, address_kelurahan: d.address_kelurahan,
    address_kecamatan: d.address_kecamatan, province_id: d.province_id,
    postal_code: d.postal_code, reference_by: d.reference_by, phone_number: d.phone_number,
    gender: d.gender, ashnaf: d.ashnaf, birth_place: d.birth_place, birth_date: d.birth_date,
    identity_number: d.identity_number, identity_type: d.identity_type, religion: d.religion,
    total_family: d.total_family, formal_education: d.formal_education, income: d.income,
    marital: d.marital, work_sector: d.work_sector,
    bank_accounts: d.bank_accounts.map(ba => ({ ...ba })),
  })
}

async function openCreate() {
  resetForm()
  modalMode.value  = 'create'
  modalError.value = null
  modalOpen.value  = true
}

async function openEdit(row: MustahiqRow) {
  selectedRow.value  = row
  modalMode.value    = 'edit'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  try {
    const d = await api.get<PersonalDetail>(`/api/distribution/mustahiq/personal/${row.mustahiq_id}`)
    fillForm(d)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

async function openDetail(row: MustahiqRow) {
  selectedRow.value  = row
  modalMode.value    = 'detail'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  try {
    detailData.value = await api.get<PersonalDetail>(`/api/distribution/mustahiq/personal/${row.mustahiq_id}`)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

function openDelete(row: MustahiqRow) {
  selectedRow.value = row; modalMode.value = 'delete'; modalError.value = null; modalOpen.value = true
}

function openStatus(row: MustahiqRow, newStatus: 'A' | 'N') {
  selectedRow.value = row; pendingStatus.value = newStatus; modalMode.value = 'status'; modalError.value = null; modalOpen.value = true
}

function closeModal() { modalOpen.value = false }

// ── Bank account rows ─────────────────────────────────────────────────────────

function addBankRow() { form.bank_accounts.push({ bank_account_id: null, account_no: '', account_name: '', bank_code: '', is_default: 'F' }) }
function removeBankRow(i: number) { form.bank_accounts.splice(i, 1) }
function setDefaultBank(i: number) { form.bank_accounts.forEach((ba, idx) => { ba.is_default = idx === i ? 'T' : 'F' }) }

// ── Save / Delete / Status ────────────────────────────────────────────────────

async function saveForm() {
  if (!form.name.trim()) { modalError.value = 'Nama mustahiq wajib diisi.'; return }
  modalLoading.value = true; modalError.value = null
  try {
    const payload = {
      name: form.name.trim(), address: form.address || null,
      address_kelurahan: form.address_kelurahan || null, address_kecamatan: form.address_kecamatan || null,
      province_id: form.province_id, postal_code: form.postal_code || null,
      reference_by: form.reference_by || null, phone_number: form.phone_number || null,
      gender: form.gender || null, ashnaf: form.ashnaf || null,
      birth_place: form.birth_place || null, birth_date: form.birth_date || null,
      identity_number: form.identity_number || null, identity_type: form.identity_type || null,
      religion: form.religion, total_family: form.total_family,
      formal_education: form.formal_education || null, income: form.income,
      marital: form.marital || null, work_sector: form.work_sector || null,
      bank_accounts: form.bank_accounts.map(ba => ({
        bank_account_id: ba.bank_account_id || null,
        account_no: ba.account_no || null, account_name: ba.account_name || null,
        bank_code: ba.bank_code || null, is_default: ba.is_default,
      })),
    }
    if (modalMode.value === 'create') {
      await api.post('/api/distribution/mustahiq/personal', payload)
      toast.success('Mustahiq individu berhasil ditambahkan.')
    } else {
      await api.put(`/api/distribution/mustahiq/personal/${selectedRow.value!.mustahiq_id}`, payload)
      toast.success('Mustahiq individu berhasil diperbarui.')
    }
    closeModal(); loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menyimpan data.'
  } finally {
    modalLoading.value = false
  }
}

async function confirmDelete() {
  if (!selectedRow.value) return
  modalLoading.value = true; modalError.value = null
  try {
    await api.delete(`/api/distribution/mustahiq/personal/${selectedRow.value.mustahiq_id}`)
    toast.success('Mustahiq individu berhasil dihapus.')
    closeModal(); loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menghapus data.'
  } finally { modalLoading.value = false }
}

async function confirmStatus() {
  if (!selectedRow.value) return
  modalLoading.value = true; modalError.value = null
  try {
    await api.put(`/api/distribution/mustahiq/personal/${selectedRow.value.mustahiq_id}/status`, { status: pendingStatus.value })
    const label = pendingStatus.value === 'A' ? 'diaktifkan' : 'dinonaktifkan'
    toast.success(`Mustahiq individu berhasil ${label}.`)
    closeModal(); loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal mengubah status.'
  } finally { modalLoading.value = false }
}

onMounted(() => { loadLookups(); loadData() })
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Mustahiq Individu" subtitle="Data penerima manfaat — perorangan">
      <template #actions>
        <Button
          v-if="auth.hasMenu('distribution.mustahiq.personal')"
          size="sm" class="gap-1.5 h-8 text-xs" @click="openCreate"
        >
          <Plus class="w-3.5 h-3.5" /> Tambah
        </Button>
      </template>
    </PageHeader>

    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400">
      {{ errorMsg }}
    </div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center gap-3">
        <div class="relative flex-1 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input v-model="searchInput" type="text" placeholder="Cari nama / nomor / alamat..."
            class="w-full h-8 pl-8 pr-8 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <button v-if="searchInput" class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground" @click="searchInput = ''">
            <X class="w-3 h-3" />
          </button>
        </div>
      </div>

      <!-- Pagination (atas) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">{{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} mustahiq individu</template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @prev="prevPage" @next="nextPage" @update:page-size="changePageSize" />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium w-28">No. Mustahiq</th>
              <th class="px-4 py-2 text-left font-medium">Nama</th>
              <th class="px-4 py-2 text-left font-medium max-w-xs">Alamat</th>
              <th class="px-4 py-2 text-left font-medium w-36">Telepon</th>
              <th class="px-4 py-2 text-center font-medium w-24">Status</th>
              <th class="px-4 py-2 text-right font-medium w-32">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td></tr>
            <tr v-else-if="rows.length === 0"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">Belum ada data mustahiq individu.</td></tr>
            <tr v-for="row in rows" :key="row.mustahiq_id" class="hover:bg-background/60">
              <td class="px-4 py-1.5 font-mono text-xs text-muted-foreground">{{ row.no_mustahiq || '—' }}</td>
              <td class="px-4 py-1.5 font-medium">{{ row.name || '—' }}</td>
              <td class="px-4 py-1.5 text-xs text-muted-foreground max-w-xs truncate">{{ row.address || '—' }}</td>
              <td class="px-4 py-1.5 text-xs">{{ row.phone_number || '—' }}</td>
              <td class="px-4 py-1.5 text-center">
                <span class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="row.status === 'A' ? 'bg-emerald-100 text-emerald-700' : 'bg-zinc-100 text-zinc-500'">
                  {{ row.status === 'A' ? 'Aktif' : 'NonAktif' }}
                </span>
              </td>
              <td class="px-4 py-1.5">
                <div class="flex items-center justify-end gap-0.5">
                  <button class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors text-[10px]" title="Detail" @click="openDetail(row)">Detail</button>
                  <button class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-blue-600 transition-colors" title="Ubah" @click="openEdit(row)"><Pencil class="w-3.5 h-3.5" /></button>
                  <button v-if="row.status === 'A'" class="p-1.5 rounded hover:bg-amber-50 text-muted-foreground hover:text-amber-600 transition-colors" title="NonAktifkan" @click="openStatus(row, 'N')"><XCircle class="w-3.5 h-3.5" /></button>
                  <button v-else class="p-1.5 rounded hover:bg-emerald-50 text-muted-foreground hover:text-emerald-600 transition-colors" title="Aktifkan" @click="openStatus(row, 'A')"><CheckCircle2 class="w-3.5 h-3.5" /></button>
                  <button class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600 transition-colors" title="Hapus" @click="openDelete(row)"><Trash2 class="w-3.5 h-3.5" /></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Create / Edit Modal ─────────────────────────────────────────────── -->
    <Modal v-if="modalOpen && (modalMode === 'create' || modalMode === 'edit')" max-width="max-w-4xl" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">{{ modalMode === 'create' ? 'Tambah Mustahiq Individu' : 'Ubah Mustahiq Individu' }}</h2>
      </template>

      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat data...</div>
      <div v-else class="space-y-5 max-h-[70vh] overflow-y-auto pr-1">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>

        <!-- Data Dasar -->
        <fieldset class="space-y-3">
          <legend class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Data Identitas</legend>
          <div>
            <label class="block text-xs font-medium mb-1">Nama <span class="text-red-500">*</span></label>
            <input v-model="form.name" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" placeholder="Nama lengkap" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium mb-1">Jenis Kelamin</label>
              <SearchSelect :model-value="form.gender ?? ''" :options="GENDER_OPTIONS" all-label="— Pilih —" @update:model-value="form.gender = $event || null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Ashnaf</label>
              <SearchSelect :model-value="form.ashnaf ?? ''" :options="ASHNAF_OPTIONS" all-label="— Pilih —" @update:model-value="form.ashnaf = $event || null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Tempat Lahir</label>
              <input v-model="form.birth_place" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Tanggal Lahir</label>
              <DateField v-model="form.birth_date" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Jenis Identitas</label>
              <SearchSelect :model-value="form.identity_type ?? ''" :options="IDENTITY_OPTIONS" all-label="— Pilih —" @update:model-value="form.identity_type = $event || null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">No. Identitas</label>
              <input v-model="form.identity_number" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Agama</label>
              <SearchSelect :model-value="form.religion ? String(form.religion) : ''" :options="RELIGION_OPTIONS" all-label="— Pilih —" @update:model-value="form.religion = $event ? Number($event) : null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Status Pernikahan</label>
              <SearchSelect :model-value="form.marital ?? ''" :options="MARITAL_OPTIONS" all-label="— Pilih —" @update:model-value="form.marital = $event || null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Pendidikan</label>
              <SearchSelect :model-value="form.formal_education ?? ''" :options="EDUCATION_OPTIONS" all-label="— Pilih —" @update:model-value="form.formal_education = $event || null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Bidang Pekerjaan</label>
              <SearchSelect :model-value="form.work_sector ?? ''" :options="SECTOR_OPTIONS" all-label="— Pilih —" @update:model-value="form.work_sector = $event || null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Jumlah Keluarga</label>
              <input v-model.number="form.total_family" type="number" min="0" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Pendapatan / Bulan (Rp)</label>
              <input v-model.number="form.income" type="number" min="0" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
          </div>
        </fieldset>

        <!-- Alamat -->
        <fieldset class="space-y-3">
          <legend class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Alamat & Kontak</legend>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium mb-1">Alamat</label>
              <input v-model="form.address" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Kelurahan</label>
              <input v-model="form.address_kelurahan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Kecamatan</label>
              <input v-model="form.address_kecamatan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Provinsi</label>
              <SearchSelect :model-value="form.province_id ? String(form.province_id) : ''" :options="provinceOptions()" all-label="— Pilih provinsi —" @update:model-value="form.province_id = $event ? Number($event) : null" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Kode Pos</label>
              <input v-model="form.postal_code" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Telepon</label>
              <input v-model="form.phone_number" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium mb-1">Referensi</label>
              <input v-model="form.reference_by" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
          </div>
        </fieldset>

        <!-- Rekening Bank -->
        <fieldset>
          <div class="flex items-center justify-between mb-2">
            <legend class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Rekening Bank</legend>
            <button type="button" class="text-xs text-primary hover:underline flex items-center gap-1" @click="addBankRow">
              <Plus class="w-3 h-3" /> Tambah Rekening
            </button>
          </div>
          <div class="rounded border border-border overflow-hidden">
            <table class="w-full text-xs">
              <thead class="bg-muted/30"><tr>
                <th class="px-2 py-1 text-left font-medium">No. Rekening</th>
                <th class="px-2 py-1 text-left font-medium">Nama Rekening</th>
                <th class="px-2 py-1 text-left font-medium">Bank</th>
                <th class="px-2 py-1 text-center font-medium w-16">Default</th>
                <th class="px-2 py-1 w-8"></th>
              </tr></thead>
              <tbody>
                <tr v-if="form.bank_accounts.length === 0"><td colspan="5" class="px-2 py-3 text-center text-muted-foreground italic">Belum ada rekening</td></tr>
                <tr v-for="(ba, i) in form.bank_accounts" :key="i" class="border-t border-border">
                  <td class="px-1 py-1"><input v-model="ba.account_no" type="text" class="w-full h-6 px-2 text-xs border border-border rounded bg-background focus:outline-none" /></td>
                  <td class="px-1 py-1"><input v-model="ba.account_name" type="text" class="w-full h-6 px-2 text-xs border border-border rounded bg-background focus:outline-none" /></td>
                  <td class="px-1 py-1"><SearchSelect :model-value="ba.bank_code" :options="bankOptions()" all-label="— Pilih —" @update:model-value="ba.bank_code = $event" /></td>
                  <td class="px-1 py-1 text-center"><input type="checkbox" :checked="ba.is_default === 'T'" @change="setDefaultBank(i)" class="accent-primary" /></td>
                  <td class="px-1 py-1"><button type="button" @click="removeBankRow(i)" class="text-red-500 hover:text-red-700"><X class="w-3.5 h-3.5" /></button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </fieldset>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button size="sm" :disabled="modalLoading" @click="saveForm">{{ modalLoading ? 'Menyimpan...' : 'Simpan' }}</Button>
        </div>
      </template>
    </Modal>

    <!-- ── Detail Modal ────────────────────────────────────────────────────── -->
    <Modal v-if="modalOpen && modalMode === 'detail'" max-width="max-w-2xl" @close="closeModal">
      <template #header><h2 class="text-base font-semibold">Detail Mustahiq Individu</h2></template>
      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat...</div>
      <div v-else-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
      <div v-else-if="detailData" class="space-y-4 text-sm max-h-[65vh] overflow-y-auto pr-1">
        <div class="grid grid-cols-2 gap-x-6 gap-y-2">
          <div><span class="text-xs text-muted-foreground">No. Mustahiq</span><p class="font-mono">{{ detailData.no_mustahiq || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Status</span>
            <p><span class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold" :class="detailData.status === 'A' ? 'bg-emerald-100 text-emerald-700' : 'bg-zinc-100 text-zinc-500'">{{ detailData.status === 'A' ? 'Aktif' : 'NonAktif' }}</span></p>
          </div>
          <div class="col-span-2"><span class="text-xs text-muted-foreground">Nama</span><p class="font-medium">{{ detailData.name }}</p></div>
          <div><span class="text-xs text-muted-foreground">Jenis Kelamin</span><p>{{ labelOf(GENDER_OPTIONS, detailData.gender) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Ashnaf</span><p>{{ labelOf(ASHNAF_OPTIONS, detailData.ashnaf) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Tempat Lahir</span><p>{{ detailData.birth_place || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Tanggal Lahir</span><p>{{ detailData.birth_date ? dmy(detailData.birth_date) : '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Identitas</span><p>{{ labelOf(IDENTITY_OPTIONS, detailData.identity_type) }} — {{ detailData.identity_number || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Agama</span><p>{{ labelOf(RELIGION_OPTIONS, detailData.religion ? String(detailData.religion) : null) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Pernikahan</span><p>{{ labelOf(MARITAL_OPTIONS, detailData.marital) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Pendidikan</span><p>{{ labelOf(EDUCATION_OPTIONS, detailData.formal_education) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Pekerjaan</span><p>{{ labelOf(SECTOR_OPTIONS, detailData.work_sector) }}</p></div>
          <div><span class="text-xs text-muted-foreground">Jml Keluarga</span><p>{{ detailData.total_family ?? '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Pendapatan/Bln</span><p>{{ detailData.income != null ? new Intl.NumberFormat('id-ID').format(detailData.income) : '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Alamat</span><p>{{ detailData.address || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Telepon</span><p>{{ detailData.phone_number || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Referensi</span><p>{{ detailData.reference_by || '—' }}</p></div>
        </div>
        <div v-if="detailData.bank_accounts.length > 0">
          <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">Rekening Bank</p>
          <table class="w-full text-xs border border-border rounded overflow-hidden">
            <thead class="bg-muted/30"><tr>
              <th class="px-3 py-1 text-left font-medium">No. Rek</th>
              <th class="px-3 py-1 text-left font-medium">Nama Rek</th>
              <th class="px-3 py-1 text-left font-medium">Bank</th>
              <th class="px-3 py-1 text-center font-medium">Default</th>
            </tr></thead>
            <tbody>
              <tr v-for="ba in detailData.bank_accounts" :key="ba.bank_account_id" class="border-t border-border">
                <td class="px-3 py-1">{{ ba.account_no || '—' }}</td>
                <td class="px-3 py-1">{{ ba.account_name || '—' }}</td>
                <td class="px-3 py-1">{{ ba.bank_code || '—' }}</td>
                <td class="px-3 py-1 text-center">{{ ba.is_default === 'T' ? '✓' : '' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end"><Button variant="outline" size="sm" @click="closeModal">Tutup</Button></div>
      </template>
    </Modal>

    <!-- ── Delete Modal ────────────────────────────────────────────────────── -->
    <Modal v-if="modalOpen && modalMode === 'delete'" max-width="max-w-md" @close="closeModal">
      <template #header><h2 class="text-base font-semibold text-red-600">Hapus Mustahiq Individu</h2></template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <p class="text-sm text-muted-foreground">Data berikut akan dihapus permanen:</p>
        <div class="rounded border border-border bg-muted/30 px-4 py-3 text-sm space-y-1">
          <div class="font-semibold">{{ selectedRow?.name }}</div>
          <div class="text-xs text-muted-foreground">No: {{ selectedRow?.no_mustahiq || '—' }}</div>
          <div class="text-xs text-muted-foreground">Alamat: {{ selectedRow?.address || '—' }}</div>
        </div>
        <p class="text-xs text-red-600 font-medium">Tindakan ini tidak dapat dibatalkan.</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button variant="destructive" size="sm" :disabled="modalLoading" @click="confirmDelete">{{ modalLoading ? 'Menghapus...' : 'Hapus' }}</Button>
        </div>
      </template>
    </Modal>

    <!-- ── Status Modal ────────────────────────────────────────────────────── -->
    <Modal v-if="modalOpen && modalMode === 'status'" max-width="max-w-md" @close="closeModal">
      <template #header><h2 class="text-base font-semibold">{{ pendingStatus === 'N' ? 'NonAktifkan' : 'Aktifkan' }} Mustahiq</h2></template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <div class="rounded border border-border bg-muted/30 px-4 py-3 text-sm">
          <div class="font-semibold">{{ selectedRow?.name }}</div>
          <div class="text-xs text-muted-foreground">No: {{ selectedRow?.no_mustahiq || '—' }}</div>
        </div>
        <p class="text-sm">Apakah Anda yakin ingin <strong>{{ pendingStatus === 'N' ? 'menonaktifkan' : 'mengaktifkan kembali' }}</strong> mustahiq ini?</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button size="sm" :disabled="modalLoading" @click="confirmStatus">{{ modalLoading ? 'Memproses...' : (pendingStatus === 'N' ? 'NonAktifkan' : 'Aktifkan') }}</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

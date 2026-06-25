<script setup lang="ts">
import { ArrowLeft, Plus, X } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref, shallowRef, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BankAccountItem { bank_account_id: number | null; bank_account_no: string; bank_account_name: string; bank_code: string }
interface CommitmentItem  { commitment_id: number | null; account_no: string; commitment_amount: number | null }
interface ProvinceLookup  { id_propinsi: number; province_name: string }
interface CountryLookup   { id_negara: number; country_name: string }
interface MarketerLookup  { marketer_id: number; marketer_code: string | null; marketer_name: string | null }
interface FieldOfWorkLookup { fwork_id: number; fwork_code: string | null; fwork_name: string | null }
interface WorkAreaLookup  { work_area_id: number; work_area_code: string | null; work_area_name: string | null }

// ── Route ─────────────────────────────────────────────────────────────────────

const route  = useRoute()
const router = useRouter()
const toast  = useToast()

const donorId   = computed(() => route.params.id ? Number(route.params.id) : null)
const isEdit    = computed(() => donorId.value !== null)
const pageTitle = computed(() => isEdit.value ? 'Ubah Donatur Individu' : 'Tambah Donatur Individu')

// ── Lookups ───────────────────────────────────────────────────────────────────

const provinces   = ref<ProvinceLookup[]>([])
const countries   = ref<CountryLookup[]>([])
const marketers   = ref<MarketerLookup[]>([])
const fieldOfWork = ref<FieldOfWorkLookup[]>([])
const workAreas   = ref<WorkAreaLookup[]>([])

const provinceOptions   = computed(() => provinces.value.map(p => ({ value: String(p.id_propinsi), label: p.province_name })))
const countryOptions    = computed(() => countries.value.map(c => ({ value: String(c.id_negara), label: c.country_name })))
const marketerOptions   = computed(() => marketers.value.map(m => ({ value: String(m.marketer_id), label: `${m.marketer_code ?? ''} — ${m.marketer_name ?? ''}` })))
const fieldOfWorkOptions = computed(() => fieldOfWork.value.map(f => ({ value: String(f.fwork_id), label: `${f.fwork_code ?? ''} — ${f.fwork_name ?? ''}` })))
const workAreaOptions   = computed(() => workAreas.value.map(w => ({ value: String(w.work_area_id), label: `${w.work_area_code ?? ''} — ${w.work_area_name ?? ''}` })))

async function loadLookups() {
  try {
    const [prov, ctry, mkt, fow, wa] = await Promise.all([
      api.get<any>('/api/fundraising/donors/lookup/provinces'),
      api.get<any>('/api/fundraising/donors/lookup/countries'),
      api.get<any>('/api/fundraising/donors/lookup/marketers'),
      api.get<any>('/api/fundraising/donors/lookup/field-of-work'),
      api.get<any>('/api/fundraising/donors/lookup/work-areas'),
    ])
    provinces.value   = prov?.data ?? []
    countries.value   = ctry?.data ?? []
    marketers.value   = mkt?.data ?? []
    fieldOfWork.value = fow?.data ?? []
    workAreas.value   = wa?.data ?? []
  } catch { /* non-critical */ }
}

// ── Enums ─────────────────────────────────────────────────────────────────────

const GENDER_OPTIONS = [{ value: '', label: '—' }, { value: 'L', label: 'Laki-Laki' }, { value: 'P', label: 'Perempuan' }]
const RELIGION_OPTIONS = [
  { value: '', label: '—' }, { value: '1', label: 'Islam' }, { value: '2', label: 'Katolik' },
  { value: '3', label: 'Protestan' }, { value: '4', label: 'Hindu' }, { value: '5', label: 'Budha' },
  { value: '6', label: 'Aliran Kepercayaan' },
]
const MARITAL_OPTIONS = [{ value: '', label: '—' }, { value: 'K', label: 'Menikah' }, { value: 'B', label: 'Belum Menikah' }, { value: 'S', label: 'Duda/Janda' }]
const STATUS_RUMAH_OPTIONS = [{ value: '', label: '—' }, { value: '1', label: 'Sendiri' }, { value: '2', label: 'Kontrak' }, { value: '3', label: 'Keluarga' }, { value: '4', label: 'Dinas' }]
const SECTOR_OPTIONS = [
  { value: '', label: '— Pilih Sektor —' },
  { value: '1', label: '1 — Pertanian' }, { value: '2', label: '2 — Pertambangan' },
  { value: '3', label: '3 — Industri' }, { value: '4', label: '4 — Listrik, Gas' },
  { value: '5', label: '5 — Konstruksi' }, { value: '6', label: '6 — Perdagangan' },
  { value: '7', label: '7 — Pengangkutan' }, { value: '8', label: '8 — Jasa Bisnis' },
  { value: '9', label: '9 — Jasa Sosial' },
]

// ── Form ──────────────────────────────────────────────────────────────────────

const form = reactive({
  donor_name: '',
  identity_number: '',
  gender: '',
  join_date: '' as string,
  birth_place: '',
  birth_date: '' as string,
  religion: '' as string,
  marital_state: '',
  mobile_phone: '',
  phone_number: '',
  fax: '',
  email: '',
  npwp: '',
  npwz: '',
  status: 'A',
  status_rumah: '',
  is_internal_employee: 'F',
  work_identity_number: '',
  work_area_id: '' as string,
  work_area_id_initial: '' as string,
  work_unit: '',
  work_position: '',
  work_business_area: '',
  economic_sector: '',
  fwork_id: '' as string,
  id_negara: '' as string,
  id_propinsi: '' as string,
  address_city: '',
  address_postal_code: '',
  address_kecamatan: '',
  address_kelurahan: '',
  address_street: '',
  id_propinsi_office: '' as string,
  office_address: '',
  office_kelurahan: '',
  office_kecamatan: '',
  office_city: '',
  office_phone_number: '',
  office_postal_code: '',
  corporate_name: '',
  job_position: '',
  couple_name: '',
  child: null as number | null,
  marketer_id: '' as string,
  bank_accounts: [] as BankAccountItem[],
  commitments: [] as CommitmentItem[],
})

const submitting  = shallowRef(false)
const dataLoading = shallowRef(false)
const formError   = shallowRef<string | null>(null)

// Field enable/disable based on is_internal_employee
const isEmployee = computed(() => form.is_internal_employee === 'T')
const isMarried  = computed(() => form.marital_state === 'K')

watch(() => form.is_internal_employee, (val) => {
  if (val !== 'T') {
    form.work_identity_number = ''; form.work_area_id = ''; form.work_area_id_initial = ''
    form.work_unit = ''; form.work_position = ''; form.work_business_area = ''
  }
})

// ── Bank accounts ─────────────────────────────────────────────────────────────

function addBankAccount() {
  form.bank_accounts.push({ bank_account_id: null, bank_account_no: '', bank_account_name: '', bank_code: '' })
}
function removeBankAccount(i: number) { form.bank_accounts.splice(i, 1) }

function addCommitment() {
  form.commitments.push({ commitment_id: null, account_no: '', commitment_amount: null })
}
function removeCommitment(i: number) { form.commitments.splice(i, 1) }

// ── Load existing data ────────────────────────────────────────────────────────

async function loadData() {
  if (!donorId.value) return
  dataLoading.value = true
  try {
    const res = await api.get<any>(`/api/fundraising/donors/individual/${donorId.value}`)
    const d = res.data
    form.donor_name        = d.donor_name ?? ''
    form.identity_number   = d.identity_number ?? ''
    form.gender            = d.gender ?? ''
    form.join_date         = d.join_date ?? ''
    form.birth_place       = d.birth_place ?? ''
    form.birth_date        = d.birth_date ?? ''
    form.religion          = d.religion ? String(d.religion) : ''
    form.marital_state     = d.marital_state ?? ''
    form.mobile_phone      = d.mobile_phone ?? ''
    form.phone_number      = d.phone_number ?? ''
    form.fax               = d.fax ?? ''
    form.email             = d.email ?? ''
    form.npwp              = d.npwp ?? ''
    form.npwz              = d.npwz ?? ''
    form.status            = d.status ?? 'A'
    form.status_rumah      = d.status_rumah ?? ''
    form.is_internal_employee = d.is_internal_employee ?? 'F'
    form.work_identity_number = d.work_identity_number ?? ''
    form.work_area_id      = d.work_area_id ? String(d.work_area_id) : ''
    form.work_area_id_initial = d.work_area_id_initial ? String(d.work_area_id_initial) : ''
    form.work_unit         = d.work_unit ?? ''
    form.work_position     = d.work_position ?? ''
    form.work_business_area = d.work_business_area ?? ''
    form.economic_sector   = d.economic_sector ?? ''
    form.fwork_id          = d.fwork_id ? String(d.fwork_id) : ''
    form.id_negara         = d.id_negara ? String(d.id_negara) : ''
    form.id_propinsi       = d.id_propinsi ? String(d.id_propinsi) : ''
    form.address_city      = d.address_city ?? ''
    form.address_postal_code = d.address_postal_code ?? ''
    form.address_kecamatan = d.address_kecamatan ?? ''
    form.address_kelurahan = d.address_kelurahan ?? ''
    form.address_street    = d.address_street ?? ''
    form.id_propinsi_office = d.id_propinsi_office ? String(d.id_propinsi_office) : ''
    form.office_address    = d.office_address ?? ''
    form.office_kelurahan  = d.office_kelurahan ?? ''
    form.office_kecamatan  = d.office_kecamatan ?? ''
    form.office_city       = d.office_city ?? ''
    form.office_phone_number = d.office_phone_number ?? ''
    form.office_postal_code  = d.office_postal_code ?? ''
    form.corporate_name    = d.corporate_name ?? ''
    form.job_position      = d.job_position ?? ''
    form.couple_name       = d.couple_name ?? ''
    form.child             = d.child ?? null
    form.marketer_id       = d.marketer_id ? String(d.marketer_id) : ''
    form.bank_accounts     = (d.bank_accounts ?? []).map((b: any) => ({
      bank_account_id: b.bank_account_id, bank_account_no: b.bank_account_no ?? '',
      bank_account_name: b.bank_account_name ?? '', bank_code: b.bank_code ?? '',
    }))
    form.commitments = (d.commitments ?? []).map((c: any) => ({
      commitment_id: c.commitment_id, account_no: c.account_no ?? '', commitment_amount: c.commitment_amount ?? null,
    }))
  } catch (e) {
    formError.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    dataLoading.value = false
  }
}

// ── Submit ────────────────────────────────────────────────────────────────────

async function submit() {
  if (!form.donor_name.trim()) { formError.value = 'Nama wajib diisi'; return }
  if (form.is_internal_employee === 'T' && !form.work_identity_number.trim()) {
    formError.value = 'NIP wajib diisi untuk karyawan internal'; return
  }
  submitting.value = true; formError.value = null
  try {
    const payload = {
      ...form,
      religion:         form.religion         ? Number(form.religion)         : null,
      work_area_id:     form.work_area_id     ? Number(form.work_area_id)     : null,
      work_area_id_initial: form.work_area_id_initial ? Number(form.work_area_id_initial) : null,
      fwork_id:         form.fwork_id         ? Number(form.fwork_id)         : null,
      id_negara:        form.id_negara        ? Number(form.id_negara)        : null,
      id_propinsi:      form.id_propinsi      ? Number(form.id_propinsi)      : null,
      id_propinsi_office: form.id_propinsi_office ? Number(form.id_propinsi_office) : null,
      marketer_id:      form.marketer_id      ? Number(form.marketer_id)      : null,
    }
    if (isEdit.value) {
      await api.put(`/api/fundraising/donors/individual/${donorId.value}`, payload)
      toast.success('Donatur individu berhasil diperbarui.')
    } else {
      await api.post('/api/fundraising/donors/individual', payload)
      toast.success('Donatur individu berhasil ditambahkan.')
    }
    router.push({ name: 'fundraising-donor-individual-list' })
  } catch (e) {
    formError.value = e instanceof ApiError ? e.message : 'Gagal menyimpan data.'
  } finally {
    submitting.value = false
  }
}

onMounted(() => { loadLookups(); loadData() })
</script>

<template>
  <div class="space-y-4 max-w-4xl">
    <PageHeader :title="pageTitle" subtitle="Penghimpunan / Kegiatan">
      <template #actions>
        <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" @click="router.back()">
          <ArrowLeft class="w-3.5 h-3.5" /> Kembali
        </Button>
      </template>
    </PageHeader>

    <div v-if="dataLoading" class="text-center py-10 text-muted-foreground text-sm">Memuat data...</div>

    <div v-else class="space-y-4">
      <div v-if="formError" class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{{ formError }}</div>

      <!-- Personal Data -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Data Personal</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="md:col-span-2">
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Nama <span class="text-red-500">*</span></label>
            <input v-model="form.donor_name" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Nomor KTP</label>
            <input v-model="form.identity_number" type="text" maxlength="20" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Jenis Kelamin</label>
            <select v-model="form.gender" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option v-for="opt in GENDER_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Tanggal Bergabung</label>
            <DateField v-model="form.join_date" class="w-full" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Tempat Lahir</label>
            <input v-model="form.birth_place" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Tanggal Lahir</label>
            <DateField v-model="form.birth_date" class="w-full" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Agama</label>
            <select v-model="form.religion" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option v-for="opt in RELIGION_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">NPWP</label>
            <input v-model="form.npwp" type="text" maxlength="20" placeholder="15 digit" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">NPWZ</label>
            <input v-model="form.npwz" type="text" maxlength="30" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Status</label>
            <select v-model="form.status" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option value="A">Aktif</option>
              <option value="N">NonAktif</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Jenis Donatur</label>
            <select v-model="form.is_internal_employee" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option value="F">Non-Karyawan</option>
              <option value="T">Karyawan Internal</option>
            </select>
          </div>
          <div v-if="isEmployee">
            <label class="text-xs font-medium text-muted-foreground mb-1 block">NIP <span class="text-red-500">*</span></label>
            <input v-model="form.work_identity_number" type="text" maxlength="30" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">ZIS Account Manager</label>
            <SearchSelect v-model="form.marketer_id" :options="marketerOptions" placeholder="Pilih marketer..." />
          </div>
        </div>
      </div>

      <!-- Karyawan detail (conditional) -->
      <div v-if="isEmployee" class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Data Kepegawaian</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kantor Wilayah</label>
            <SearchSelect v-model="form.work_area_id" :options="workAreaOptions" placeholder="Pilih wilayah..." />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kantor Wilayah Asal</label>
            <SearchSelect v-model="form.work_area_id_initial" :options="workAreaOptions" placeholder="Pilih wilayah asal..." />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Unit Kerja</label>
            <input v-model="form.work_unit" type="text" maxlength="100" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Posisi</label>
            <input v-model="form.work_position" type="text" maxlength="100" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Bidang Bisnis</label>
            <input v-model="form.work_business_area" type="text" maxlength="100" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
        </div>
      </div>

      <!-- Pekerjaan (non-karyawan) -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Data Pekerjaan</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Bidang Pekerjaan</label>
            <SearchSelect v-model="form.fwork_id" :options="fieldOfWorkOptions" placeholder="Pilih bidang pekerjaan..." />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Jenis Bidang Usaha</label>
            <select v-model="form.economic_sector" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option v-for="opt in SECTOR_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Nama Perusahaan</label>
            <input v-model="form.corporate_name" type="text" maxlength="50" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Jabatan</label>
            <input v-model="form.job_position" type="text" maxlength="50" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
        </div>
      </div>

      <!-- Alamat Tinggal -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Alamat Tinggal & Kontak</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Negara</label>
            <SearchSelect v-model="form.id_negara" :options="countryOptions" placeholder="Pilih negara..." />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Provinsi</label>
            <SearchSelect v-model="form.id_propinsi" :options="provinceOptions" placeholder="Pilih provinsi..." />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kota</label>
            <input v-model="form.address_city" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kode Pos</label>
            <input v-model="form.address_postal_code" type="text" maxlength="10" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kecamatan</label>
            <input v-model="form.address_kecamatan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kelurahan</label>
            <input v-model="form.address_kelurahan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div class="md:col-span-2">
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Alamat Jalan</label>
            <input v-model="form.address_street" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">No. Telepon</label>
            <input v-model="form.phone_number" type="text" maxlength="20" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">No. HP</label>
            <input v-model="form.mobile_phone" type="text" maxlength="20" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Email</label>
            <input v-model="form.email" type="email" maxlength="200" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Fax</label>
            <input v-model="form.fax" type="text" maxlength="20" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kepemilikan Rumah</label>
            <select v-model="form.status_rumah" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option v-for="opt in STATUS_RUMAH_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Data Keluarga -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Data Keluarga</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Status Pernikahan</label>
            <select v-model="form.marital_state" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option v-for="opt in MARITAL_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Nama Pasangan</label>
            <input v-model="form.couple_name" type="text" maxlength="50" :disabled="!isMarried"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Jumlah Anak</label>
            <input v-model.number="form.child" type="number" min="0" :disabled="!isMarried"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50" />
          </div>
        </div>
      </div>

      <!-- Alamat Kantor -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Alamat Kantor</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Provinsi Kantor</label>
            <SearchSelect v-model="form.id_propinsi_office" :options="provinceOptions" placeholder="Pilih provinsi..." />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kota Kantor</label>
            <input v-model="form.office_city" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kecamatan Kantor</label>
            <input v-model="form.office_kecamatan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kelurahan Kantor</label>
            <input v-model="form.office_kelurahan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div class="md:col-span-2">
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Alamat Kantor</label>
            <input v-model="form.office_address" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Telepon Kantor</label>
            <input v-model="form.office_phone_number" type="text" maxlength="50" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Kode Pos Kantor</label>
            <input v-model="form.office_postal_code" type="text" maxlength="50" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
        </div>
      </div>

      <!-- Rekening Bank -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <div class="flex items-center justify-between border-b border-border pb-2">
          <h3 class="text-sm font-semibold text-foreground">Rekening Bank</h3>
          <Button variant="outline" size="sm" class="gap-1 h-7 text-xs" @click="addBankAccount">
            <Plus class="w-3 h-3" /> Tambah Rekening
          </Button>
        </div>
        <div v-if="form.bank_accounts.length === 0" class="text-xs text-muted-foreground italic py-2">Belum ada rekening bank.</div>
        <div v-for="(acc, i) in form.bank_accounts" :key="i" class="grid grid-cols-12 gap-2 items-center">
          <input v-model="acc.bank_account_no" type="text" placeholder="No Rekening"
            class="col-span-3 h-8 px-3 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <input v-model="acc.bank_account_name" type="text" placeholder="Atas Nama"
            class="col-span-4 h-8 px-3 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <input v-model="acc.bank_code" type="text" placeholder="Kode Bank"
            class="col-span-4 h-8 px-3 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <button class="col-span-1 p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600" @click="removeBankAccount(i)">
            <X class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      <!-- Komitmen Donasi -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <div class="flex items-center justify-between border-b border-border pb-2">
          <h3 class="text-sm font-semibold text-foreground">Komitmen Donasi</h3>
          <Button variant="outline" size="sm" class="gap-1 h-7 text-xs" @click="addCommitment">
            <Plus class="w-3 h-3" /> Tambah Komitmen
          </Button>
        </div>
        <div v-if="form.commitments.length === 0" class="text-xs text-muted-foreground italic py-2">Belum ada komitmen donasi.</div>
        <div v-for="(c, i) in form.commitments" :key="i" class="grid grid-cols-12 gap-2 items-center">
          <input v-model="c.account_no" type="text" placeholder="No Rekening Kas/Bank"
            class="col-span-5 h-8 px-3 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <input v-model.number="c.commitment_amount" type="number" placeholder="Nominal"
            class="col-span-6 h-8 px-3 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <button class="col-span-1 p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600" @click="removeCommitment(i)">
            <X class="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex justify-end gap-2 pt-2">
        <Button variant="outline" size="sm" @click="router.back()">Batal</Button>
        <Button size="sm" :disabled="submitting" @click="submit">
          {{ submitting ? 'Menyimpan...' : (isEdit ? 'Perbarui' : 'Simpan') }}
        </Button>
      </div>
    </div>
  </div>
</template>

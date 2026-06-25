<script setup lang="ts">
import { ArrowLeft, Plus, X } from 'lucide-vue-next'
import { onMounted, reactive, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BankAccountRow {
  bank_account_id: number | null
  account_no: string
  account_name: string
  bank_code: string
  is_default: string
}

interface Option { value: string; label: string }

// ── Router ────────────────────────────────────────────────────────────────────

const route  = useRoute()
const router = useRouter()
const toast  = useToast()

const mustahiqId = route.params.id ? Number(route.params.id) : null
const isEdit     = mustahiqId !== null

// ── Enum options ──────────────────────────────────────────────────────────────

const GENDER_OPT: Option[]    = [{ value: 'L', label: 'Laki-Laki' }, { value: 'P', label: 'Perempuan' }]
const IDENTITY_OPT: Option[]  = [{ value: 'K', label: 'KTP' }, { value: 'S', label: 'SIM' }, { value: 'F', label: 'Kartu Keluarga' }, { value: 'P', label: 'Passport' }]
const RELIGION_OPT: Option[]  = [1, 2, 3, 4, 5, 6].map((v, i) => ({ value: String(v), label: ['Islam', 'Katolik', 'Protestan', 'Hindu', 'Budha', 'Aliran Kepercayaan'][i] }))
const MARITAL_OPT: Option[]   = [{ value: 'K', label: 'Menikah' }, { value: 'B', label: 'Belum Menikah' }, { value: 'S', label: 'Duda/Janda' }]
const EDUCATION_OPT: Option[] = ['0', '1', '2', '3', '4', '5', '6'].map((v, i) => ({ value: v, label: ['Tdk Sekolah Formal', 'SD', 'SMP', 'SMU/Sederajat', 'S1', 'S2', 'S3'][i] }))
const ASHNAF_OPT: Option[]    = [
  { value: 'F', label: 'Fakir' }, { value: 'M', label: 'Miskin' }, { value: 'U', label: 'Mualaf' },
  { value: 'H', label: 'Hamba Sahaya' }, { value: 'G', label: 'Gharimin' }, { value: 'S', label: 'Fisabilillah' },
  { value: 'I', label: 'Ibnu Sabil' }, { value: 'A', label: 'Amil' },
]
const SECTOR_OPT: Option[] = [1, 2, 3, 4, 5, 6, 7, 8, 9].map((v, i) => ({ value: String(v), label: [
  'Pertanian/Perkebunan/Perikanan', 'Pertambangan', 'Industri/Pabrik', 'Listrik/Gas/Air',
  'Konstruksi', 'Perdagangan', 'Pengangkutan/Pergudangan', 'Jasa Keuangan', 'Jasa Sosial',
][i] }))

// ── Lookups ───────────────────────────────────────────────────────────────────

const provinceOptions = shallowRef<Option[]>([])
const bankOptions     = shallowRef<Option[]>([])

async function loadLookups() {
  try {
    const [prov, bank] = await Promise.all([
      api.get<any>('/api/distribution/mustahiq/lookup/provinces'),
      api.get<any>('/api/distribution/mustahiq/lookup/banks'),
    ])
    const provinces = (prov as any).data ?? prov ?? []
    const banks     = (bank as any).data ?? bank ?? []
    provinceOptions.value = provinces.map((p: any) => ({ value: String(p.province_id), label: p.province_name }))
    bankOptions.value     = banks.map((b: any) => ({ value: b.bank_code, label: `${b.bank_short_name ?? b.bank_code} — ${b.bank_name ?? ''}` }))
  } catch { /* non-critical */ }
}

// ── Form ──────────────────────────────────────────────────────────────────────

const form = reactive({
  name:              '',
  address:           null as string | null,
  address_kelurahan: null as string | null,
  address_kecamatan: null as string | null,
  province_id:       null as number | null,
  postal_code:       null as string | null,
  reference_by:      null as string | null,
  phone_number:      null as string | null,
  gender:            null as string | null,
  ashnaf:            null as string | null,
  birth_place:       null as string | null,
  birth_date:        null as string | null,
  identity_number:   null as string | null,
  identity_type:     null as string | null,
  religion:          null as number | null,
  total_family:      null as number | null,
  formal_education:  null as string | null,
  income:            null as number | null,
  marital:           null as string | null,
  work_sector:       null as string | null,
  bank_accounts:     [] as BankAccountRow[],
})

const pageLoading = shallowRef(false)
const submitting  = shallowRef(false)
const formError   = shallowRef<string | null>(null)

// ── Load for edit ─────────────────────────────────────────────────────────────

async function loadDetail() {
  if (!mustahiqId) return
  pageLoading.value = true
  try {
    const d = await api.get<any>(`/api/distribution/mustahiq/personal/${mustahiqId}`)
    form.name              = d.name ?? ''
    form.address           = d.address
    form.address_kelurahan = d.address_kelurahan
    form.address_kecamatan = d.address_kecamatan
    form.province_id       = d.province_id
    form.postal_code       = d.postal_code
    form.reference_by      = d.reference_by
    form.phone_number      = d.phone_number
    form.gender            = d.gender
    form.ashnaf            = d.ashnaf
    form.birth_place       = d.birth_place
    form.birth_date        = d.birth_date
    form.identity_number   = d.identity_number
    form.identity_type     = d.identity_type
    form.religion          = d.religion
    form.total_family      = d.total_family
    form.formal_education  = d.formal_education
    form.income            = d.income
    form.marital           = d.marital
    form.work_sector       = d.work_sector
    form.bank_accounts     = (d.bank_accounts ?? []).map((ba: any) => ({ ...ba }))
  } catch (e) {
    formError.value = e instanceof ApiError ? e.message : 'Gagal memuat data.'
  } finally {
    pageLoading.value = false
  }
}

// ── Bank accounts ─────────────────────────────────────────────────────────────

function addBank() {
  form.bank_accounts.push({ bank_account_id: null, account_no: '', account_name: '', bank_code: '', is_default: 'F' })
}
function removeBank(i: number) { form.bank_accounts.splice(i, 1) }
function setDefault(i: number) { form.bank_accounts.forEach((b, idx) => { b.is_default = idx === i ? 'T' : 'F' }) }

// ── Save ──────────────────────────────────────────────────────────────────────

async function save() {
  if (!form.name.trim()) { formError.value = 'Nama mustahiq wajib diisi.'; return }
  submitting.value = true
  formError.value  = null
  try {
    const payload = {
      name:              form.name.trim(),
      address:           form.address || null,
      address_kelurahan: form.address_kelurahan || null,
      address_kecamatan: form.address_kecamatan || null,
      province_id:       form.province_id,
      postal_code:       form.postal_code || null,
      reference_by:      form.reference_by || null,
      phone_number:      form.phone_number || null,
      gender:            form.gender || null,
      ashnaf:            form.ashnaf || null,
      birth_place:       form.birth_place || null,
      birth_date:        form.birth_date || null,
      identity_number:   form.identity_number || null,
      identity_type:     form.identity_type || null,
      religion:          form.religion,
      total_family:      form.total_family,
      formal_education:  form.formal_education || null,
      income:            form.income,
      marital:           form.marital || null,
      work_sector:       form.work_sector || null,
      bank_accounts:     form.bank_accounts.map(b => ({
        bank_account_id: b.bank_account_id || null,
        account_no:      b.account_no || null,
        account_name:    b.account_name || null,
        bank_code:       b.bank_code || null,
        is_default:      b.is_default,
      })),
    }
    if (isEdit) {
      await api.put(`/api/distribution/mustahiq/personal/${mustahiqId}`, payload)
      toast.success('Data mustahiq individu berhasil diperbarui.')
    } else {
      await api.post('/api/distribution/mustahiq/personal', payload)
      toast.success('Mustahiq individu berhasil ditambahkan.')
    }
    router.push({ name: 'distribution-mustahiq-personal' })
  } catch (e) {
    formError.value = e instanceof ApiError ? e.message : 'Gagal menyimpan data.'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  await loadLookups()
  if (isEdit) await loadDetail()
})
</script>

<template>
  <div class="space-y-6 max-w-4xl mx-auto">
    <PageHeader
      :title="isEdit ? 'Ubah Mustahiq Individu' : 'Tambah Mustahiq Individu'"
      subtitle="Data penerima manfaat — perorangan"
    >
      <template #actions>
        <div class="flex items-center gap-2">
          <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" @click="router.back()">
            <ArrowLeft class="w-3.5 h-3.5" /> Kembali
          </Button>
          <Button size="sm" class="h-8 text-xs" :disabled="submitting || pageLoading" @click="save">
            {{ submitting ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </PageHeader>

    <div v-if="pageLoading" class="py-12 text-center text-muted-foreground text-sm">Memuat data...</div>

    <template v-else>
      <div v-if="formError" class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400">
        {{ formError }}
      </div>

      <!-- Data Identitas -->
      <div class="rounded-xl border border-border bg-surface p-6 space-y-4">
        <h3 class="text-sm font-semibold text-muted-foreground uppercase tracking-wide">Data Identitas</h3>
        <div>
          <label class="block text-xs font-medium mb-1">Nama <span class="text-red-500">*</span></label>
          <input v-model="form.name" type="text" placeholder="Nama lengkap"
            class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium mb-1">Jenis Kelamin</label>
            <SearchSelect :model-value="form.gender ?? ''" :options="GENDER_OPT" all-label="— Pilih —"
              @update:model-value="form.gender = $event || null" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Ashnaf</label>
            <SearchSelect :model-value="form.ashnaf ?? ''" :options="ASHNAF_OPT" all-label="— Pilih —"
              @update:model-value="form.ashnaf = $event || null" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Tempat Lahir</label>
            <input v-model="form.birth_place" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Tanggal Lahir</label>
            <DateField v-model="form.birth_date" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Jenis Identitas</label>
            <SearchSelect :model-value="form.identity_type ?? ''" :options="IDENTITY_OPT" all-label="— Pilih —"
              @update:model-value="form.identity_type = $event || null" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">No. Identitas</label>
            <input v-model="form.identity_number" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Agama</label>
            <SearchSelect
              :model-value="form.religion ? String(form.religion) : ''"
              :options="RELIGION_OPT" all-label="— Pilih —"
              @update:model-value="form.religion = $event ? Number($event) : null"
            />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Status Pernikahan</label>
            <SearchSelect :model-value="form.marital ?? ''" :options="MARITAL_OPT" all-label="— Pilih —"
              @update:model-value="form.marital = $event || null" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Pendidikan</label>
            <SearchSelect :model-value="form.formal_education ?? ''" :options="EDUCATION_OPT" all-label="— Pilih —"
              @update:model-value="form.formal_education = $event || null" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Bidang Pekerjaan</label>
            <SearchSelect :model-value="form.work_sector ?? ''" :options="SECTOR_OPT" all-label="— Pilih —"
              @update:model-value="form.work_sector = $event || null" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Jumlah Keluarga</label>
            <input v-model.number="form.total_family" type="number" min="0"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Pendapatan / Bulan (Rp)</label>
            <input v-model.number="form.income" type="number" min="0"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
        </div>
      </div>

      <!-- Alamat & Kontak -->
      <div class="rounded-xl border border-border bg-surface p-6 space-y-4">
        <h3 class="text-sm font-semibold text-muted-foreground uppercase tracking-wide">Alamat &amp; Kontak</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-medium mb-1">Alamat</label>
            <input v-model="form.address" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Kelurahan</label>
            <input v-model="form.address_kelurahan" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Kecamatan</label>
            <input v-model="form.address_kecamatan" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Provinsi</label>
            <SearchSelect
              :model-value="form.province_id ? String(form.province_id) : ''"
              :options="provinceOptions" all-label="— Pilih provinsi —"
              @update:model-value="form.province_id = $event ? Number($event) : null"
            />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Kode Pos</label>
            <input v-model="form.postal_code" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="block text-xs font-medium mb-1">Telepon</label>
            <input v-model="form.phone_number" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div class="col-span-2">
            <label class="block text-xs font-medium mb-1">Referensi</label>
            <input v-model="form.reference_by" type="text"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
        </div>
      </div>

      <!-- Rekening Bank -->
      <div class="rounded-xl border border-border bg-surface p-6 space-y-3">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-muted-foreground uppercase tracking-wide">Rekening Bank</h3>
          <button type="button" class="text-xs text-primary hover:underline flex items-center gap-1" @click="addBank">
            <Plus class="w-3 h-3" /> Tambah Rekening
          </button>
        </div>
        <div class="rounded border border-border overflow-hidden">
          <table class="w-full text-xs">
            <thead class="bg-muted/30">
              <tr>
                <th class="px-2 py-1.5 text-left font-medium">No. Rekening</th>
                <th class="px-2 py-1.5 text-left font-medium">Nama Rekening</th>
                <th class="px-2 py-1.5 text-left font-medium">Bank</th>
                <th class="px-2 py-1.5 text-center font-medium w-16">Default</th>
                <th class="px-2 py-1.5 w-8"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="form.bank_accounts.length === 0">
                <td colspan="5" class="px-3 py-4 text-center text-muted-foreground italic">Belum ada rekening</td>
              </tr>
              <tr v-for="(ba, i) in form.bank_accounts" :key="i" class="border-t border-border">
                <td class="px-1 py-1">
                  <input v-model="ba.account_no" type="text"
                    class="w-full h-6 px-2 text-xs border border-border rounded bg-background focus:outline-none" />
                </td>
                <td class="px-1 py-1">
                  <input v-model="ba.account_name" type="text"
                    class="w-full h-6 px-2 text-xs border border-border rounded bg-background focus:outline-none" />
                </td>
                <td class="px-1 py-1">
                  <SearchSelect :model-value="ba.bank_code" :options="bankOptions" all-label="— Pilih —"
                    @update:model-value="ba.bank_code = $event" />
                </td>
                <td class="px-1 py-1 text-center">
                  <input type="checkbox" :checked="ba.is_default === 'T'" @change="setDefault(i)" class="accent-primary" />
                </td>
                <td class="px-1 py-1">
                  <button type="button" @click="removeBank(i)" class="text-red-500 hover:text-red-700">
                    <X class="w-3.5 h-3.5" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Bottom Save -->
      <div class="flex justify-end gap-2 pb-6">
        <Button variant="outline" size="sm" @click="router.back()">Batal</Button>
        <Button size="sm" :disabled="submitting" @click="save">
          {{ submitting ? 'Menyimpan...' : 'Simpan' }}
        </Button>
      </div>
    </template>
  </div>
</template>

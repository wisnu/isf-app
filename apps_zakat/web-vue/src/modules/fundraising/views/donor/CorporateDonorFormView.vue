<script setup lang="ts">
import { ArrowLeft, Plus, X } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref, shallowRef } from 'vue'
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

// ── Route ─────────────────────────────────────────────────────────────────────

const route  = useRoute()
const router = useRouter()
const toast  = useToast()

const donorId   = computed(() => route.params.id ? Number(route.params.id) : null)
const isEdit    = computed(() => donorId.value !== null)
const pageTitle = computed(() => isEdit.value ? 'Ubah Donatur Korporat' : 'Tambah Donatur Korporat')

// ── Lookups ───────────────────────────────────────────────────────────────────

const provinces = ref<ProvinceLookup[]>([])
const countries = ref<CountryLookup[]>([])
const marketers = ref<MarketerLookup[]>([])

const provinceOptions = computed(() =>
  provinces.value.map((p: ProvinceLookup) => ({ value: String(p.id_propinsi), label: p.province_name }))
)
const countryOptions = computed(() =>
  countries.value.map((c: CountryLookup) => ({ value: String(c.id_negara), label: c.country_name }))
)
const marketerOptions = computed(() =>
  marketers.value.map((m: MarketerLookup) => ({ value: String(m.marketer_id), label: `${m.marketer_code ?? ''} — ${m.marketer_name ?? ''}` }))
)

async function loadLookups() {
  try {
    const [prov, ctry, mkt] = await Promise.all([
      api.get<any>('/api/fundraising/donors/lookup/provinces'),
      api.get<any>('/api/fundraising/donors/lookup/countries'),
      api.get<any>('/api/fundraising/donors/lookup/marketers'),
    ])
    provinces.value = prov?.data ?? []
    countries.value = ctry?.data ?? []
    marketers.value = mkt?.data ?? []
  } catch { /* non-critical */ }
}

// ── Enums ─────────────────────────────────────────────────────────────────────

const CORPORATION_OPTIONS = [
  { value: '', label: '— Pilih Tipe —' },
  { value: 'B', label: 'Bank' },
  { value: 'C', label: 'CV' },
  { value: 'D', label: 'PD' },
  { value: 'F', label: 'Firma' },
  { value: 'K', label: 'Koperasi' },
  { value: 'L', label: 'Lainnya' },
  { value: 'P', label: 'PT' },
  { value: 'Y', label: 'Yayasan' },
]
const SECTOR_OPTIONS = [
  { value: '', label: '— Pilih Sektor —' },
  { value: '1', label: '1 — Pertanian, Perkebunan, Perikanan' },
  { value: '2', label: '2 — Pertambangan' },
  { value: '3', label: '3 — Industri, Pabrik, Konsumer Goods' },
  { value: '4', label: '4 — Listrik, Gas dan Air' },
  { value: '5', label: '5 — Konstruksi' },
  { value: '6', label: '6 — Perdagangan' },
  { value: '7', label: '7 — Pengangkutan, Pergudangan dan Komunikasi' },
  { value: '8', label: '8 — Jasa-jasa Bisnis, Keuangan' },
  { value: '9', label: '9 — Jasa-jasa Sosial' },
]

// ── Form ──────────────────────────────────────────────────────────────────────

const form = reactive({
  donor_name: '',
  corporation: '',
  economic_sector: '',
  siupp: '',
  join_date: '' as string,
  npwp: '',
  npwz: '',
  status: 'A',
  marketer_id: '' as string,
  id_negara: '' as string,
  id_propinsi: '' as string,
  address_city: '',
  address_postal_code: '',
  address_kecamatan: '',
  address_kelurahan: '',
  address_street: '',
  phone_number: '',
  fax: '',
  cp_name: '',
  cp_phone: '',
  cp_mobile: '',
  cp_email: '',
  bank_accounts: [] as BankAccountItem[],
  commitments: [] as CommitmentItem[],
})

const submitting  = shallowRef(false)
const dataLoading = shallowRef(false)
const formError   = shallowRef<string | null>(null)

// ── Bank accounts ─────────────────────────────────────────────────────────────

function addBankAccount() {
  form.bank_accounts.push({ bank_account_id: null, bank_account_no: '', bank_account_name: '', bank_code: '' })
}
function removeBankAccount(i: number) { form.bank_accounts.splice(i, 1) }

// ── Commitments ───────────────────────────────────────────────────────────────

function addCommitment() {
  form.commitments.push({ commitment_id: null, account_no: '', commitment_amount: null })
}
function removeCommitment(i: number) { form.commitments.splice(i, 1) }

// ── Load existing data ────────────────────────────────────────────────────────

async function loadData() {
  if (!donorId.value) return
  dataLoading.value = true
  try {
    const res = await api.get<any>(`/api/fundraising/donors/corporate/${donorId.value}`)
    const d = res.data
    form.donor_name       = d.donor_name ?? ''
    form.corporation      = d.corporation ?? ''
    form.economic_sector  = d.economic_sector ?? ''
    form.siupp            = d.siupp ?? ''
    form.join_date        = d.join_date ?? ''
    form.npwp             = d.npwp ?? ''
    form.npwz             = d.npwz ?? ''
    form.status           = d.status ?? 'A'
    form.marketer_id      = d.marketer_id ? String(d.marketer_id) : ''
    form.id_negara        = d.id_negara ? String(d.id_negara) : ''
    form.id_propinsi      = d.id_propinsi ? String(d.id_propinsi) : ''
    form.address_city     = d.address_city ?? ''
    form.address_postal_code = d.address_postal_code ?? ''
    form.address_kecamatan   = d.address_kecamatan ?? ''
    form.address_kelurahan   = d.address_kelurahan ?? ''
    form.address_street      = d.address_street ?? ''
    form.phone_number     = d.phone_number ?? ''
    form.fax              = d.fax ?? ''
    form.cp_name          = d.cp_name ?? ''
    form.cp_phone         = d.cp_phone ?? ''
    form.cp_mobile        = d.cp_mobile ?? ''
    form.cp_email         = d.cp_email ?? ''
    form.bank_accounts    = (d.bank_accounts ?? []).map((b: any) => ({
      bank_account_id: b.bank_account_id,
      bank_account_no: b.bank_account_no ?? '',
      bank_account_name: b.bank_account_name ?? '',
      bank_code: b.bank_code ?? '',
    }))
    form.commitments = (d.commitments ?? []).map((c: any) => ({
      commitment_id: c.commitment_id,
      account_no: c.account_no ?? '',
      commitment_amount: c.commitment_amount ?? null,
    }))
  } catch (e) {
    formError.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    dataLoading.value = false
  }
}

// ── Submit ────────────────────────────────────────────────────────────────────

async function submit() {
  if (!form.donor_name.trim()) { formError.value = 'Nama perusahaan wajib diisi'; return }
  submitting.value = true; formError.value = null
  try {
    const payload = {
      ...form,
      marketer_id: form.marketer_id ? Number(form.marketer_id) : null,
      id_negara:   form.id_negara   ? Number(form.id_negara)   : null,
      id_propinsi: form.id_propinsi ? Number(form.id_propinsi) : null,
    }
    if (isEdit.value) {
      await api.put(`/api/fundraising/donors/corporate/${donorId.value}`, payload)
      toast.success('Donatur korporat berhasil diperbarui.')
    } else {
      await api.post('/api/fundraising/donors/corporate', payload)
      toast.success('Donatur korporat berhasil ditambahkan.')
    }
    router.push({ name: 'fundraising-donor-corporate-list' })
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

      <!-- Profil Perusahaan -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Profil Perusahaan</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="md:col-span-2">
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Nama Perusahaan <span class="text-red-500">*</span></label>
            <input v-model="form.donor_name" type="text" placeholder="Nama perusahaan (uppercase)"
              class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Tipe Korporat</label>
            <select v-model="form.corporation" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option v-for="opt in CORPORATION_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Jenis Bidang Usaha</label>
            <select v-model="form.economic_sector" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option v-for="opt in SECTOR_OPTIONS" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">SIUPP</label>
            <input v-model="form.siupp" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Tanggal Bergabung</label>
            <DateField v-model="form.join_date" class="w-full" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">NPWP</label>
            <input v-model="form.npwp" type="text" maxlength="20" placeholder="15 digit" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">NPWZ</label>
            <input v-model="form.npwz" type="text" maxlength="30" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Status</label>
            <select v-model="form.status" class="w-full h-8 px-2 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
              <option value="A">Aktif</option>
              <option value="N">NonAktif</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">ZIS Account Manager</label>
            <SearchSelect v-model="form.marketer_id" :options="marketerOptions" placeholder="Pilih marketer..." />
          </div>
        </div>
      </div>

      <!-- Alamat -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Alamat Perusahaan</h3>
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
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Telepon</label>
            <input v-model="form.phone_number" type="text" maxlength="20" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Fax</label>
            <input v-model="form.fax" type="text" maxlength="20" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
        </div>
      </div>

      <!-- Contact Person -->
      <div class="rounded-xl border border-border bg-surface p-4 space-y-3">
        <h3 class="text-sm font-semibold text-foreground border-b border-border pb-2">Contact Person</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="md:col-span-2">
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Nama CP</label>
            <input v-model="form.cp_name" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Telepon CP</label>
            <input v-model="form.cp_phone" type="text" maxlength="30" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">HP CP</label>
            <input v-model="form.cp_mobile" type="text" maxlength="30" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          </div>
          <div>
            <label class="text-xs font-medium text-muted-foreground mb-1 block">Email CP</label>
            <input v-model="form.cp_email" type="email" maxlength="200" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
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

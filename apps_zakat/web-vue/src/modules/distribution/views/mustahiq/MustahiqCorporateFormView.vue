<script setup lang="ts">
import { ArrowLeft, Plus, X } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BankAccountItem {
  bank_account_id: number | null
  account_no: string
  account_name: string
  bank_code: string
  is_default: string
}

interface ProvinceLookup { province_id: number; province_name: string }
interface BankLookup { bank_code: string; bank_short_name: string | null; bank_name: string | null }

// ── Route ─────────────────────────────────────────────────────────────────────

const route  = useRoute()
const router = useRouter()
const toast  = useToast()

const mustahiqId = computed(() => route.params.id ? Number(route.params.id) : null)
const isEdit     = computed(() => mustahiqId.value !== null)
const pageTitle  = computed(() => isEdit.value ? 'Ubah Mustahiq Lembaga' : 'Tambah Mustahiq Lembaga')

// ── Lookups ───────────────────────────────────────────────────────────────────

const provinces = ref<ProvinceLookup[]>([])
const banks     = ref<BankLookup[]>([])

const provinceOptions = computed(() =>
  provinces.value.map(p => ({ value: String(p.province_id), label: p.province_name }))
)
const bankOptions = computed(() =>
  banks.value.map(b => ({ value: b.bank_code, label: `${b.bank_short_name ?? b.bank_code} — ${b.bank_name ?? ''}` }))
)

async function loadLookups() {
  try {
    const [prov, bank] = await Promise.all([
      api.get<any>('/api/distribution/mustahiq/lookup/provinces'),
      api.get<any>('/api/distribution/mustahiq/lookup/banks'),
    ])
    provinces.value = (prov as any)?.data ?? prov ?? []
    banks.value     = (bank as any)?.data ?? bank ?? []
  } catch {
    // non-critical
  }
}

// ── Form ──────────────────────────────────────────────────────────────────────

const form = reactive({
  name: '',
  address: '',
  address_kelurahan: '',
  address_kecamatan: '',
  province_id: null as number | null,
  postal_code: '',
  phone_number: '',
  reference_by: '',
  cp_name: '',
  cp_phone_number: '',
  cp_mobile_number: '',
  bank_accounts: [] as BankAccountItem[],
})

const submitting  = shallowRef(false)
const dataLoading = shallowRef(false)
const formError   = shallowRef<string | null>(null)

async function loadDetail() {
  if (!mustahiqId.value) return
  dataLoading.value = true
  try {
    const d = await api.get<any>(`/api/distribution/mustahiq/corporate/${mustahiqId.value}`)
    form.name              = d.name ?? ''
    form.address           = d.address ?? ''
    form.address_kelurahan = d.address_kelurahan ?? ''
    form.address_kecamatan = d.address_kecamatan ?? ''
    form.province_id       = d.province_id ?? null
    form.postal_code       = d.postal_code ?? ''
    form.phone_number      = d.phone_number ?? ''
    form.reference_by      = d.reference_by ?? ''
    form.cp_name           = d.cp_name ?? ''
    form.cp_phone_number   = d.cp_phone_number ?? ''
    form.cp_mobile_number  = d.cp_mobile_number ?? ''
    form.bank_accounts     = (d.bank_accounts ?? []).map((ba: any) => ({
      bank_account_id: ba.bank_account_id ?? null,
      account_no:   ba.account_no ?? '',
      account_name: ba.account_name ?? '',
      bank_code:    ba.bank_code ?? '',
      is_default:   ba.is_default ?? 'F',
    }))
  } catch (e) {
    formError.value = e instanceof ApiError ? e.message : 'Gagal memuat data.'
  } finally {
    dataLoading.value = false
  }
}

// ── Bank accounts ─────────────────────────────────────────────────────────────

function addBankRow() {
  form.bank_accounts.push({ bank_account_id: null, account_no: '', account_name: '', bank_code: '', is_default: 'F' })
}

function removeBankRow(i: number) {
  form.bank_accounts.splice(i, 1)
}

function setDefaultBank(i: number) {
  form.bank_accounts.forEach((ba, idx) => { ba.is_default = idx === i ? 'T' : 'F' })
}

// ── Submit ────────────────────────────────────────────────────────────────────

async function submit() {
  if (!form.name.trim()) { formError.value = 'Nama lembaga wajib diisi.'; return }
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
      phone_number:      form.phone_number || null,
      reference_by:      form.reference_by || null,
      cp_name:           form.cp_name || null,
      cp_phone_number:   form.cp_phone_number || null,
      cp_mobile_number:  form.cp_mobile_number || null,
      bank_accounts:     form.bank_accounts.map(ba => ({
        bank_account_id: ba.bank_account_id,
        account_no:   ba.account_no || null,
        account_name: ba.account_name || null,
        bank_code:    ba.bank_code || null,
        is_default:   ba.is_default,
      })),
    }
    if (isEdit.value) {
      await api.put(`/api/distribution/mustahiq/corporate/${mustahiqId.value}`, payload)
      toast.success('Mustahiq lembaga berhasil diperbarui.')
    } else {
      await api.post('/api/distribution/mustahiq/corporate', payload)
      toast.success('Mustahiq lembaga berhasil ditambahkan.')
    }
    router.push({ name: 'distribution-mustahiq-corporate' })
  } catch (e) {
    formError.value = e instanceof ApiError ? e.message : 'Gagal menyimpan data.'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  await loadLookups()
  if (isEdit.value) await loadDetail()
})
</script>

<template>
  <div class="space-y-4">
    <PageHeader :title="pageTitle" :subtitle="isEdit ? 'Edit data mustahiq lembaga' : 'Tambah mustahiq lembaga baru'">
      <template #actions>
        <div class="flex items-center gap-2">
          <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" @click="router.back()">
            <ArrowLeft class="w-3.5 h-3.5" /> Kembali
          </Button>
          <Button size="sm" class="h-8 text-xs" :disabled="submitting || dataLoading" @click="submit">
            {{ submitting ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </PageHeader>

    <div v-if="dataLoading" class="text-center py-12 text-muted-foreground text-sm">Memuat data...</div>

    <template v-else>
      <div v-if="formError" class="max-w-3xl mx-auto rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {{ formError }}
      </div>

      <div class="max-w-3xl mx-auto space-y-4">

        <!-- Data Lembaga -->
        <div class="rounded-xl border border-border bg-surface">
          <div class="px-5 py-3 border-b border-border">
            <h3 class="text-sm font-semibold">Data Lembaga</h3>
          </div>
          <div class="px-5 py-4 space-y-4">
            <div>
              <label class="block text-xs font-medium mb-1">Nama Lembaga <span class="text-red-500">*</span></label>
              <input v-model="form.name" type="text"
                class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring"
                placeholder="Nama lembaga / organisasi" />
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-medium mb-1">Alamat</label>
                <input v-model="form.address" type="text"
                  class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1">Kelurahan</label>
                <input v-model="form.address_kelurahan" type="text"
                  class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1">Kecamatan</label>
                <input v-model="form.address_kecamatan" type="text"
                  class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1">Provinsi</label>
                <SearchSelect
                  :model-value="form.province_id ? String(form.province_id) : ''"
                  :options="provinceOptions"
                  all-label="— Pilih provinsi —"
                  @update:model-value="form.province_id = $event ? Number($event) : null"
                />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1">Kode Pos</label>
                <input v-model="form.postal_code" type="text"
                  class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div>
                <label class="block text-xs font-medium mb-1">Telepon</label>
                <input v-model="form.phone_number" type="text"
                  class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
              <div class="col-span-2">
                <label class="block text-xs font-medium mb-1">Referensi</label>
                <input v-model="form.reference_by" type="text"
                  class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
              </div>
            </div>
          </div>
        </div>

        <!-- Kontak Person -->
        <div class="rounded-xl border border-border bg-surface">
          <div class="px-5 py-3 border-b border-border">
            <h3 class="text-sm font-semibold">Kontak Person</h3>
          </div>
          <div class="px-5 py-4 grid grid-cols-3 gap-4">
            <div>
              <label class="block text-xs font-medium mb-1">Nama Kontak</label>
              <input v-model="form.cp_name" type="text"
                class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Telepon Kontak</label>
              <input v-model="form.cp_phone_number" type="text"
                class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">HP Kontak</label>
              <input v-model="form.cp_mobile_number" type="text"
                class="w-full h-9 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
          </div>
        </div>

        <!-- Rekening Bank -->
        <div class="rounded-xl border border-border bg-surface">
          <div class="px-5 py-3 border-b border-border flex items-center justify-between">
            <h3 class="text-sm font-semibold">Rekening Bank</h3>
            <button type="button" class="text-xs text-primary hover:underline flex items-center gap-1" @click="addBankRow">
              <Plus class="w-3 h-3" /> Tambah Rekening
            </button>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-xs">
              <thead class="bg-muted/30 border-b border-border">
                <tr>
                  <th class="px-4 py-2 text-left font-medium">No. Rekening</th>
                  <th class="px-4 py-2 text-left font-medium">Nama Rekening</th>
                  <th class="px-4 py-2 text-left font-medium">Bank</th>
                  <th class="px-4 py-2 text-center font-medium w-20">Default</th>
                  <th class="px-4 py-2 w-10"></th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="form.bank_accounts.length === 0">
                  <td colspan="5" class="px-4 py-4 text-center text-muted-foreground italic">Belum ada rekening. Klik "Tambah Rekening" untuk menambah.</td>
                </tr>
                <tr v-for="(ba, i) in form.bank_accounts" :key="i" class="border-t border-border">
                  <td class="px-3 py-2">
                    <input v-model="ba.account_no" type="text"
                      class="w-full h-7 px-2 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
                  </td>
                  <td class="px-3 py-2">
                    <input v-model="ba.account_name" type="text"
                      class="w-full h-7 px-2 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
                  </td>
                  <td class="px-3 py-2">
                    <SearchSelect :model-value="ba.bank_code" :options="bankOptions" all-label="— Pilih bank —"
                      @update:model-value="ba.bank_code = $event" />
                  </td>
                  <td class="px-3 py-2 text-center">
                    <input type="checkbox" :checked="ba.is_default === 'T'" @change="setDefaultBank(i)" class="accent-primary" />
                  </td>
                  <td class="px-3 py-2">
                    <button type="button" @click="removeBankRow(i)" class="text-muted-foreground hover:text-red-600 transition-colors">
                      <X class="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Footer actions -->
        <div class="flex justify-end gap-2 pb-6">
          <Button variant="outline" size="sm" @click="router.back()">Batal</Button>
          <Button size="sm" :disabled="submitting" @click="submit">
            {{ submitting ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </div>
    </template>
  </div>
</template>

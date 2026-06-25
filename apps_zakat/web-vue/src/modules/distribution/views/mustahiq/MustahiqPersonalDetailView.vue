<script setup lang="ts">
import { ArrowLeft, Pencil } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'

interface BankAccountDetail {
  bank_account_id: number
  account_no: string | null
  account_name: string | null
  bank_code: string | null
  is_default: string | null
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
  bank_accounts: BankAccountDetail[]
}

const GENDER_MAP: Record<string, string>    = { L: 'Laki-Laki', P: 'Perempuan' }
const IDENTITY_MAP: Record<string, string>  = { K: 'KTP', S: 'SIM', F: 'Kartu Keluarga', P: 'Passport' }
const RELIGION_MAP: Record<number, string>  = { 1: 'Islam', 2: 'Katolik', 3: 'Protestan', 4: 'Hindu', 5: 'Budha', 6: 'Aliran Kepercayaan' }
const MARITAL_MAP: Record<string, string>   = { K: 'Menikah', B: 'Belum Menikah', S: 'Duda/Janda' }
const EDUCATION_MAP: Record<string, string> = { '0': 'Tdk Sekolah Formal', '1': 'SD', '2': 'SMP', '3': 'SMU/Sederajat', '4': 'S1', '5': 'S2', '6': 'S3' }
const ASHNAF_MAP: Record<string, string>    = { F: 'Fakir', M: 'Miskin', U: 'Mualaf', H: 'Hamba Sahaya', G: 'Gharimin', S: 'Fisabilillah', I: 'Ibnu Sabil', A: 'Amil' }
const SECTOR_MAP: Record<string, string>    = {
  '1': 'Pertanian/Perkebunan/Perikanan', '2': 'Pertambangan', '3': 'Industri/Pabrik',
  '4': 'Listrik/Gas/Air', '5': 'Konstruksi', '6': 'Perdagangan',
  '7': 'Pengangkutan/Pergudangan', '8': 'Jasa Keuangan', '9': 'Jasa Sosial',
}

function label(map: Record<string, string>, val: string | null | undefined): string {
  if (!val) return '—'
  return map[val] ?? val
}
function labelN(map: Record<number, string>, val: number | null | undefined): string {
  if (val == null) return '—'
  return map[val] ?? String(val)
}

const route  = useRoute()
const router = useRouter()

const detail    = ref<PersonalDetail | null>(null)
const loading   = shallowRef(false)
const errorMsg  = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID')

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    detail.value = await api.get<PersonalDetail>(`/api/distribution/mustahiq/personal/${route.params.id}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Detail Mustahiq Individu" subtitle="Data penerima manfaat — perorangan">
      <template #actions>
        <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" @click="router.back()">
          <ArrowLeft class="w-3.5 h-3.5" /> Kembali
        </Button>
        <Button
          v-if="detail"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="router.push({ name: 'distribution-mustahiq-personal-edit', params: { id: route.params.id } })"
        >
          <Pencil class="w-3.5 h-3.5" /> Ubah
        </Button>
      </template>
    </PageHeader>

    <div class="max-w-4xl mx-auto space-y-4">
      <!-- Loading -->
      <div v-if="loading" class="rounded-xl border border-border bg-surface px-6 py-12 text-center text-sm text-muted-foreground">
        Memuat data...
      </div>

      <!-- Error -->
      <div v-else-if="errorMsg" class="rounded-xl border border-red-200 bg-red-50 px-6 py-4 text-sm text-red-700">
        {{ errorMsg }}
      </div>

      <template v-else-if="detail">
        <!-- Data Identitas -->
        <div class="rounded-xl border border-border bg-surface overflow-hidden">
          <div class="px-5 py-3 border-b border-border bg-muted/30">
            <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Data Identitas</h3>
          </div>
          <div class="px-5 py-4 grid grid-cols-2 gap-x-8 gap-y-3">
            <div>
              <p class="text-xs text-muted-foreground">No. Mustahiq</p>
              <p class="text-sm font-mono font-medium mt-0.5">{{ detail.no_mustahiq || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Status</p>
              <span
                class="inline-flex items-center mt-0.5 px-2 py-0.5 rounded text-[11px] font-semibold"
                :class="detail.status === 'A'
                  ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300'
                  : 'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400'"
              >{{ detail.status === 'A' ? 'Aktif' : 'NonAktif' }}</span>
            </div>
            <div class="col-span-2">
              <p class="text-xs text-muted-foreground">Nama</p>
              <p class="text-sm font-medium mt-0.5">{{ detail.name }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Jenis Kelamin</p>
              <p class="text-sm mt-0.5">{{ label(GENDER_MAP, detail.gender) }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Ashnaf</p>
              <p class="text-sm mt-0.5">{{ label(ASHNAF_MAP, detail.ashnaf) }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Tempat Lahir</p>
              <p class="text-sm mt-0.5">{{ detail.birth_place || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Tanggal Lahir</p>
              <p class="text-sm mt-0.5">{{ detail.birth_date ? dmy(detail.birth_date) : '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Jenis Identitas</p>
              <p class="text-sm mt-0.5">{{ label(IDENTITY_MAP, detail.identity_type) }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">No. Identitas</p>
              <p class="text-sm mt-0.5">{{ detail.identity_number || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Agama</p>
              <p class="text-sm mt-0.5">{{ labelN(RELIGION_MAP, detail.religion) }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Status Pernikahan</p>
              <p class="text-sm mt-0.5">{{ label(MARITAL_MAP, detail.marital) }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Pendidikan</p>
              <p class="text-sm mt-0.5">{{ label(EDUCATION_MAP, detail.formal_education ?? '') }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Bidang Pekerjaan</p>
              <p class="text-sm mt-0.5">{{ label(SECTOR_MAP, detail.work_sector ?? '') }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Jumlah Keluarga</p>
              <p class="text-sm mt-0.5">{{ detail.total_family ?? '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Pendapatan / Bulan</p>
              <p class="text-sm mt-0.5">{{ detail.income != null ? 'Rp ' + idr.format(detail.income) : '—' }}</p>
            </div>
          </div>
        </div>

        <!-- Alamat & Kontak -->
        <div class="rounded-xl border border-border bg-surface overflow-hidden">
          <div class="px-5 py-3 border-b border-border bg-muted/30">
            <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Alamat & Kontak</h3>
          </div>
          <div class="px-5 py-4 grid grid-cols-2 gap-x-8 gap-y-3">
            <div class="col-span-2">
              <p class="text-xs text-muted-foreground">Alamat</p>
              <p class="text-sm mt-0.5">{{ detail.address || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Kelurahan</p>
              <p class="text-sm mt-0.5">{{ detail.address_kelurahan || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Kecamatan</p>
              <p class="text-sm mt-0.5">{{ detail.address_kecamatan || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Kode Pos</p>
              <p class="text-sm mt-0.5">{{ detail.postal_code || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground">Telepon</p>
              <p class="text-sm mt-0.5">{{ detail.phone_number || '—' }}</p>
            </div>
            <div class="col-span-2">
              <p class="text-xs text-muted-foreground">Referensi</p>
              <p class="text-sm mt-0.5">{{ detail.reference_by || '—' }}</p>
            </div>
          </div>
        </div>

        <!-- Rekening Bank -->
        <div class="rounded-xl border border-border bg-surface overflow-hidden">
          <div class="px-5 py-3 border-b border-border bg-muted/30">
            <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Rekening Bank</h3>
          </div>
          <div v-if="detail.bank_accounts.length === 0" class="px-5 py-6 text-sm text-muted-foreground italic">
            Tidak ada rekening bank.
          </div>
          <div v-else class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
                <tr>
                  <th class="px-5 py-2 text-left font-medium">No. Rekening</th>
                  <th class="px-5 py-2 text-left font-medium">Nama Rekening</th>
                  <th class="px-5 py-2 text-left font-medium">Bank</th>
                  <th class="px-5 py-2 text-center font-medium w-20">Default</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-border">
                <tr v-for="ba in detail.bank_accounts" :key="ba.bank_account_id">
                  <td class="px-5 py-2">{{ ba.account_no || '—' }}</td>
                  <td class="px-5 py-2">{{ ba.account_name || '—' }}</td>
                  <td class="px-5 py-2">{{ ba.bank_code || '—' }}</td>
                  <td class="px-5 py-2 text-center text-emerald-600">{{ ba.is_default === 'T' ? '✓' : '' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

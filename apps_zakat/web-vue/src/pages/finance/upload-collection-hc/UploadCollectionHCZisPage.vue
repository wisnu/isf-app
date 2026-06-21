<script setup lang="ts">
import { Download, FileCheck, Upload } from 'lucide-vue-next'
import { computed, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'

interface HCZisItem {
  data_no: number
  employee_number: string
  employee_name: string
  business_area_code: string
  gender: string
  zakat_amount: number
  infaq_amount: number
  anak_asuh_amount: number
  anak_yatim_amount: number
  taqurma_amount: number
  total_amount: number
}

interface HCZisParseResult {
  batch_period_desc: string
  tanggal_transaksi: string
  namafile: string
  is_duplicate: boolean
  totals: {
    zakat_count: number
    zakat_amount: number
    infaq_count: number
    infaq_amount: number
    anak_asuh_count: number
    anak_asuh_amount: number
    anak_yatim_count: number
    anak_yatim_amount: number
    taqurma_count: number
    taqurma_amount: number
    grand_total: number
  }
  items: HCZisItem[]
}

const router = useRouter()
const toast = useToast()

const phase = shallowRef<'idle' | 'preview' | 'submitted'>('idle')
const selectedFile = ref<File | null>(null)
const tanggalTransaksi = ref('')
const parseResult = ref<HCZisParseResult | null>(null)
const submissionId = shallowRef<number | null>(null)
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function resetUpload() {
  phase.value = 'idle'
  selectedFile.value = null
  tanggalTransaksi.value = ''
  parseResult.value = null
  submissionId.value = null
  errorMsg.value = null
}

async function downloadTemplate() {
  try {
    const blob = await api.blob('/api/transaction/upload/hc-zis/template')
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'template-upload-zis-rutin.xlsx'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    setTimeout(() => URL.revokeObjectURL(url), 100)
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  }
}

async function parseFile() {
  if (!selectedFile.value || !tanggalTransaksi.value) {
    errorMsg.value = 'Pilih file dan tanggal terlebih dahulu'
    return
  }
  loading.value = true
  errorMsg.value = null
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    const result = await api.upload<HCZisParseResult>(
      `/api/transaction/upload/hc-zis/parse?tanggal_transaksi=${tanggalTransaksi.value}`,
      formData,
    )
    parseResult.value = result
    phase.value = 'preview'
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal membaca file')
  } finally {
    loading.value = false
  }
}

async function submitUntukOtorisasi() {
  if (!parseResult.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const payload = {
      batch_period_desc: parseResult.value.batch_period_desc,
      tanggal_transaksi: parseResult.value.tanggal_transaksi,
      namafile: parseResult.value.namafile,
      totals: parseResult.value.totals,
      items: parseResult.value.items,
    }
    const result = await api.post<{ id: number }>(
      '/api/transaction/upload/hc-zis/submit',
      payload,
    )
    submissionId.value = result.id
    phase.value = 'submitted'
    toast.success('Upload ZIS Rutin disimpan dan dikirim ke otorisasi')
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal menyimpan submission')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="p-6 max-w-full">
    <div class="mb-4 flex items-center gap-3">
      <Upload class="h-5 w-5 text-primary" />
      <h1 class="text-lg font-semibold">Upload Data Penerimaan ZIS Rutin (HC)</h1>
    </div>

    <div v-if="phase === 'idle' || phase === 'preview'" class="space-y-4">
      <!-- File selection and date picker -->
      <div class="space-y-3">
        <div class="flex flex-wrap items-center gap-3">
          <input
            type="file"
            accept=".xls,.xlsx"
            class="block cursor-pointer text-sm text-muted file:mr-3 file:cursor-pointer file:rounded file:border-0 file:bg-primary file:px-3 file:py-1.5 file:text-xs file:text-primary-foreground"
            @change="
              (e) => {
                selectedFile = (e.target as HTMLInputElement).files?.[0] ?? null
                phase = 'idle'
                parseResult = null
              }
            "
          />
          <Button size="sm" variant="outline" @click="downloadTemplate">
            <Download class="mr-1 h-3.5 w-3.5" /> Template
          </Button>
        </div>

        <div class="flex flex-wrap items-end gap-3">
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-muted">Tanggal Transaksi</label>
            <DateField v-model="tanggalTransaksi" />
          </div>
          <Button
            size="sm"
            :disabled="!selectedFile || !tanggalTransaksi || loading"
            @click="parseFile"
          >
            {{ loading ? 'Membaca...' : 'Proses Baca File' }}
          </Button>
        </div>
      </div>

      <Alert v-if="errorMsg" variant="error" :message="errorMsg" />

      <!-- Preview section -->
      <template v-if="phase === 'preview' && parseResult">
        <!-- Duplicate warning -->
        <Alert
          v-if="parseResult.is_duplicate"
          variant="warning"
          message="File ini sudah pernah di-upload sebelumnya. Anda masih dapat melanjutkan jika diperlukan."
        />

        <!-- Summary cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3">
          <div class="rounded-lg border border-border bg-surface px-3 py-2">
            <div class="text-[10px] uppercase tracking-wide text-muted">Zakat</div>
            <div class="text-xs font-semibold">{{ parseResult.totals.zakat_count }} org</div>
            <div class="text-xs font-medium">Rp {{ fmt(parseResult.totals.zakat_amount) }}</div>
          </div>
          <div class="rounded-lg border border-border bg-surface px-3 py-2">
            <div class="text-[10px] uppercase tracking-wide text-muted">Infaq</div>
            <div class="text-xs font-semibold">{{ parseResult.totals.infaq_count }} org</div>
            <div class="text-xs font-medium">Rp {{ fmt(parseResult.totals.infaq_amount) }}</div>
          </div>
          <div class="rounded-lg border border-border bg-surface px-3 py-2">
            <div class="text-[10px] uppercase tracking-wide text-muted">Anak Asuh</div>
            <div class="text-xs font-semibold">{{ parseResult.totals.anak_asuh_count }} org</div>
            <div class="text-xs font-medium">Rp {{ fmt(parseResult.totals.anak_asuh_amount) }}</div>
          </div>
          <div class="rounded-lg border border-border bg-surface px-3 py-2">
            <div class="text-[10px] uppercase tracking-wide text-muted">Anak Yatim</div>
            <div class="text-xs font-semibold">{{ parseResult.totals.anak_yatim_count }} org</div>
            <div class="text-xs font-medium">Rp {{ fmt(parseResult.totals.anak_yatim_amount) }}</div>
          </div>
          <div class="rounded-lg border border-border bg-surface px-3 py-2">
            <div class="text-[10px] uppercase tracking-wide text-muted">Taqurma</div>
            <div class="text-xs font-semibold">{{ parseResult.totals.taqurma_count }} org</div>
            <div class="text-xs font-medium">Rp {{ fmt(parseResult.totals.taqurma_amount) }}</div>
          </div>
          <div class="rounded-lg border border-primary bg-primary/5 px-3 py-2">
            <div class="text-[10px] uppercase tracking-wide text-primary font-semibold">Grand Total</div>
            <div class="text-sm font-bold text-primary">Rp {{ fmt(parseResult.totals.grand_total) }}</div>
          </div>
        </div>

        <!-- Items table -->
        <div class="overflow-x-auto rounded-lg border border-border">
          <table class="w-full text-sm">
            <thead class="sticky top-0 z-10 text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
              <tr>
                <th class="whitespace-nowrap px-3 py-1.5 text-left font-semibold">No</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-left font-semibold">NIP</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-left font-semibold">Nama</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-left font-semibold">Divisi</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-center font-semibold">L/P</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-right font-semibold">Zakat</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-right font-semibold">Infaq</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-right font-semibold">A. Asuh</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-right font-semibold">A. Yatim</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-right font-semibold">Taqurma</th>
                <th class="whitespace-nowrap px-3 py-1.5 text-right font-semibold">Total</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in parseResult.items" :key="item.data_no" class="hover:bg-background border-t border-border">
                <td class="px-3 py-1 text-center">{{ item.data_no }}</td>
                <td class="px-3 py-1 font-mono text-xs">{{ item.employee_number }}</td>
                <td class="px-3 py-1">{{ item.employee_name }}</td>
                <td class="px-3 py-1">{{ item.business_area_code }}</td>
                <td class="px-3 py-1 text-center">{{ item.gender }}</td>
                <td class="px-3 py-1 text-right">{{ fmt(item.zakat_amount) }}</td>
                <td class="px-3 py-1 text-right">{{ fmt(item.infaq_amount) }}</td>
                <td class="px-3 py-1 text-right">{{ fmt(item.anak_asuh_amount) }}</td>
                <td class="px-3 py-1 text-right">{{ fmt(item.anak_yatim_amount) }}</td>
                <td class="px-3 py-1 text-right">{{ fmt(item.taqurma_amount) }}</td>
                <td class="px-3 py-1 text-right font-medium">{{ fmt(item.total_amount) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="flex justify-end">
          <Button :disabled="loading" @click="submitUntukOtorisasi">
            {{ loading ? 'Menyimpan...' : 'Simpan & Kirim ke Otorisasi' }}
          </Button>
        </div>
      </template>
    </div>

    <!-- Success state -->
    <div v-if="phase === 'submitted'" class="flex flex-col items-center gap-4 py-12">
      <FileCheck class="h-12 w-12 text-green-600" />
      <p class="text-lg font-medium">Data ZIS Rutin berhasil disimpan</p>
      <div v-if="submissionId" class="text-sm text-muted">
        Submission #{{ submissionId }} menunggu otorisasi supervisor
      </div>
      <p class="text-sm text-muted text-center">
        Data akan diproses setelah supervisor memberikan persetujuan.
      </p>
      <div class="flex gap-3">
        <Button variant="outline" @click="resetUpload">Upload Lagi</Button>
        <Button @click="router.push({ name: 'finance-upload-zis-routine-list' })">
          Lihat Daftar Upload
        </Button>
      </div>
    </div>
  </div>
</template>

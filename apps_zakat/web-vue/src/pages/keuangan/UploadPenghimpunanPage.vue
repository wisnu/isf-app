<script setup lang="ts">
import { Download, FileCheck, Upload } from 'lucide-vue-next'
import { computed, ref } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { BASE_URL } from '@/lib/api/client'
import { dmy } from '@/lib/date'

interface ParsedRow {
  row_no: number
  no_rekening: string
  tanggal: string
  keterangan: string
  no_ref: string
  total_kredit: number
  zakat_profesi: number
  zakat_maal: number
  zakat_fitrah: number
  zakat_perusahaan: number
  infaq: number
  infaq_terikat: number
  dpu: number
  anak_yatim: number
  anak_asuh: number
  titipan_wakaf: number
  titipan_qurban: number
  qurban: number
  non_halal: number
  fidyah: number
  status: 'valid' | 'warning' | 'invalid'
  pesan: string
}

const phase = ref<'idle' | 'preview' | 'submitted'>('idle')
const selectedFile = ref<File | null>(null)
const rows = ref<ParsedRow[]>([])
const batchId = ref<number | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)

const validRows = computed(() => rows.value.filter((r) => r.status !== 'invalid'))
const invalidCount = computed(() => rows.value.filter((r) => r.status === 'invalid').length)
const totalAmount = computed(() => validRows.value.reduce((s, r) => s + r.total_kredit, 0))
const canSave = computed(() => validRows.value.length > 0)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function statusColor(s: string) {
  if (s === 'valid') return 'bg-green-100 text-green-800'
  if (s === 'warning') return 'bg-yellow-100 text-yellow-800'
  return 'bg-red-100 text-red-800'
}

async function downloadTemplate() {
  const res = await fetch(`${BASE_URL}/api/transaction/upload/penghimpunan/template`, {
    credentials: 'include',
  })
  if (!res.ok) return
  const blob = await res.blob()
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'template-upload-penghimpunan.xlsx'
  a.click()
  setTimeout(() => URL.revokeObjectURL(a.href), 1000)
}

async function parseFile() {
  if (!selectedFile.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const form = new FormData()
    form.append('file', selectedFile.value)
    const res = await fetch(`${BASE_URL}/api/transaction/upload/penghimpunan/parse`, {
      method: 'POST',
      credentials: 'include',
      body: form,
    })
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Parse gagal')
    rows.value = payload.data.rows
    phase.value = 'preview'
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

async function saveDraft() {
  if (!selectedFile.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const form = new FormData()
    form.append('file', selectedFile.value)
    const res = await fetch(`${BASE_URL}/api/transaction/upload/penghimpunan/draft`, {
      method: 'POST',
      credentials: 'include',
      body: form,
    })
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Simpan draft gagal')
    batchId.value = payload.data.batch_id
    phase.value = 'submitted'
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="p-6 max-w-full">
    <div class="mb-4 flex items-center gap-3">
      <Upload class="h-5 w-5 text-primary" />
      <h1 class="text-lg font-semibold">Upload Penghimpunan Multi-Bank</h1>
    </div>

    <div v-if="phase === 'idle' || phase === 'preview'" class="space-y-4">
      <div class="flex flex-wrap items-center gap-3">
        <input
          type="file"
          accept=".xls,.xlsx"
          class="block cursor-pointer text-sm text-muted file:mr-3 file:cursor-pointer file:rounded file:border-0 file:bg-primary file:px-3 file:py-1.5 file:text-xs file:text-primary-foreground"
          @change="
            (e) => {
              selectedFile = (e.target as HTMLInputElement).files?.[0] ?? null
              phase = 'idle'
              rows = []
            }
          "
        />
        <Button size="sm" variant="outline" @click="downloadTemplate">
          <Download class="mr-1 h-3.5 w-3.5" /> Template
        </Button>
        <Button size="sm" :disabled="!selectedFile || loading" @click="parseFile">
          {{ loading ? 'Membaca...' : 'Parse File' }}
        </Button>
      </div>

      <Alert v-if="errorMsg" variant="error" :message="errorMsg" />

      <template v-if="phase === 'preview' && rows.length">
        <div
          class="flex items-center gap-6 rounded-lg border border-border bg-surface px-4 py-2 text-sm text-muted"
        >
          <span>{{ validRows.length }} baris akan disimpan</span>
          <span v-if="invalidCount > 0" class="text-red-600"
            >{{ invalidCount }} baris invalid (dilewati)</span
          >
          <span class="ml-auto font-medium">Total: Rp {{ fmt(totalAmount) }}</span>
        </div>

        <div class="overflow-x-auto rounded-lg border border-border">
          <table class="w-full text-xs">
            <thead class="sticky top-0 bg-surface">
              <tr>
                <th class="whitespace-nowrap px-2 py-1.5 text-left">No</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-left">Rekening</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-left">Tanggal</th>
                <th class="min-w-[180px] whitespace-nowrap px-2 py-1.5 text-left">Keterangan</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-left">Ref</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Total</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Zakat P</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Zakat M</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Zakat F</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Zakat Per</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Infaq</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">InfaqT</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">DPU</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">A.Yatim</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">A.Asuh</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">T.Wakaf</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">T.Qurban</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Qurban</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">NonHalal</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-right">Fidyah</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-left">Status</th>
                <th class="whitespace-nowrap px-2 py-1.5 text-left">Pesan</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in rows"
                :key="row.row_no"
                :class="row.status === 'invalid' ? 'bg-red-50 opacity-50' : 'hover:bg-background'"
              >
                <td class="px-2 py-1 text-center">{{ row.row_no }}</td>
                <td class="px-2 py-1">{{ row.no_rekening }}</td>
                <td class="whitespace-nowrap px-2 py-1">{{ dmy(row.tanggal) }}</td>
                <td class="max-w-[200px] truncate px-2 py-1" :title="row.keterangan">
                  {{ row.keterangan }}
                </td>
                <td class="px-2 py-1">{{ row.no_ref }}</td>
                <td class="px-2 py-1 text-right">{{ fmt(row.total_kredit) }}</td>
                <td class="px-2 py-1 text-right">
                  {{ row.zakat_profesi ? fmt(row.zakat_profesi) : '' }}
                </td>
                <td class="px-2 py-1 text-right">
                  {{ row.zakat_maal ? fmt(row.zakat_maal) : '' }}
                </td>
                <td class="px-2 py-1 text-right">
                  {{ row.zakat_fitrah ? fmt(row.zakat_fitrah) : '' }}
                </td>
                <td class="px-2 py-1 text-right">
                  {{ row.zakat_perusahaan ? fmt(row.zakat_perusahaan) : '' }}
                </td>
                <td class="px-2 py-1 text-right">{{ row.infaq ? fmt(row.infaq) : '' }}</td>
                <td class="px-2 py-1 text-right">
                  {{ row.infaq_terikat ? fmt(row.infaq_terikat) : '' }}
                </td>
                <td class="px-2 py-1 text-right">{{ row.dpu ? fmt(row.dpu) : '' }}</td>
                <td class="px-2 py-1 text-right">
                  {{ row.anak_yatim ? fmt(row.anak_yatim) : '' }}
                </td>
                <td class="px-2 py-1 text-right">
                  {{ row.anak_asuh ? fmt(row.anak_asuh) : '' }}
                </td>
                <td class="px-2 py-1 text-right">
                  {{ row.titipan_wakaf ? fmt(row.titipan_wakaf) : '' }}
                </td>
                <td class="px-2 py-1 text-right">
                  {{ row.titipan_qurban ? fmt(row.titipan_qurban) : '' }}
                </td>
                <td class="px-2 py-1 text-right">{{ row.qurban ? fmt(row.qurban) : '' }}</td>
                <td class="px-2 py-1 text-right">
                  {{ row.non_halal ? fmt(row.non_halal) : '' }}
                </td>
                <td class="px-2 py-1 text-right">{{ row.fidyah ? fmt(row.fidyah) : '' }}</td>
                <td class="px-2 py-1">
                  <span
                    :class="[
                      'rounded px-1.5 py-0.5 text-[10px] font-medium uppercase',
                      statusColor(row.status),
                    ]"
                    >{{ row.status }}</span
                  >
                </td>
                <td class="max-w-[160px] truncate px-2 py-1 text-muted" :title="row.pesan">
                  {{ row.pesan }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="flex justify-end">
          <Button :disabled="!canSave || loading" @click="saveDraft">
            {{ loading ? 'Menyimpan...' : 'Simpan Draft' }}
          </Button>
        </div>
      </template>
    </div>

    <div v-if="phase === 'submitted'" class="flex flex-col items-center gap-4 py-12">
      <FileCheck class="h-12 w-12 text-green-600" />
      <p class="text-lg font-medium">Draft disimpan (Batch #{{ batchId }})</p>
      <p class="text-sm text-muted">
        Supervisor perlu mengotorisasi sebelum transaksi terbentuk.
      </p>
      <div class="flex gap-3">
        <Button
          variant="outline"
          @click="
            phase = 'idle'
            selectedFile = null
            rows = []
          "
          >Upload Lagi</Button
        >
        <router-link to="/keuangan/upload/penghimpunan/list">
          <Button>Lihat Daftar Batch</Button>
        </router-link>
      </div>
    </div>
  </div>
</template>

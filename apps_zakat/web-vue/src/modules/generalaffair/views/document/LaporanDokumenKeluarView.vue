<script setup lang="ts">
import { Download, FileText } from 'lucide-vue-next'
import { computed, ref, shallowRef } from 'vue'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'

// ── Types ─────────────────────────────────────────────────────────────────────

interface DokumenKeluarReportRow {
  nomor: string
  nama_jenis_dokumen: string
  tujuan: string
  perihal: string
  tanggal_dokumen: string
  tanggal_kirim: string | null
  keterangan: string | null
}

interface ReportResponse {
  rows: DokumenKeluarReportRow[]
  total: number
}

interface JenisDokumenOption {
  id_jenis_dokumen: number
  kode_jenis_dokumen: string
  nama_jenis_dokumen: string
}

// ── State ─────────────────────────────────────────────────────────────────────

const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const dateFrom = ref('')
const dateTo = ref('')
const jenisDokumenId = ref<number | null>(null)

const rows = ref<DokumenKeluarReportRow[]>([])
const total = ref(0)
const hasData = computed(() => rows.value.length > 0)

const jenisDokumenOptions = ref<JenisDokumenOption[]>([])

// ── API Calls ─────────────────────────────────────────────────────────────────

async function loadJenisDokumen() {
  try {
    const res = await api.get<{ rows: JenisDokumenOption[] }>('/api/generalaffair/document-types?page=1&page_size=100')
    jenisDokumenOptions.value = res.rows
  } catch {
    jenisDokumenOptions.value = []
  }
}

async function tampilkan() {
  if (!dateFrom.value) {
    errorMsg.value = 'Tanggal dari wajib diisi'
    return
  }
  if (!dateTo.value) {
    errorMsg.value = 'Tanggal sampai wajib diisi'
    return
  }

  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      date_from: dateFrom.value,
      date_to: dateTo.value,
    })
    if (jenisDokumenId.value) params.set('id_jenis_dokumen', String(jenisDokumenId.value))

    const res = await api.get<ReportResponse>(`/api/generalaffair/report/outgoing-document?${params}`)
    rows.value = res.rows
    total.value = res.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'
    rows.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

async function exportExcel() {
  if (exporting.value) return
  if (!dateFrom.value || !dateTo.value) return

  exporting.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      date_from: dateFrom.value,
      date_to: dateTo.value,
    })
    if (jenisDokumenId.value) params.set('id_jenis_dokumen', String(jenisDokumenId.value))

    const now = new Date()
    const ts = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
    await api.downloadBlob(
      `/api/generalaffair/report/outgoing-document/export.xlsx?${params}`,
      `laporan-dokumen-keluar-${ts}.xlsx`
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

loadJenisDokumen()
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Laporan Dokumen Keluar" subtitle="Laporan dokumen yang dikirim keluar dari organisasi" />

    <!-- Filter Card -->
    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Dari</label>
        <DateField v-model="dateFrom" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Sampai</label>
        <DateField v-model="dateTo" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Jenis Dokumen</label>
        <SearchSelect
          :model-value="jenisDokumenId"
          :options="jenisDokumenOptions.map(x => ({ value: x.id_jenis_dokumen, label: x.nama_jenis_dokumen }))"
          placeholder="Semua jenis..."
          @update:model-value="jenisDokumenId = $event"
        />
      </div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="tampilkan">
        <FileText class="w-4 h-4" :class="{ 'animate-pulse': loading }" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !hasData" @click="exportExcel">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <!-- Error Alert -->
    <div v-if="errorMsg" class="flex items-center gap-2 rounded-lg border border-red-200
                                bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Empty State (before Tampilkan) -->
    <div v-if="!hasData && !loading" class="flex flex-col items-center justify-center py-16 text-neutral-400">
      <FileText class="w-12 h-12 mb-3 opacity-40" />
      <p class="text-sm">Isi filter dan klik <strong>Tampilkan</strong> untuk melihat laporan</p>
    </div>

    <!-- Data Section (after Tampilkan) -->
    <template v-else-if="hasData || loading">
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 border-b border-border flex items-center justify-between">
          <span class="text-[11px] text-muted tabular-nums">
            <template v-if="loading">Memuat...</template>
            <template v-else-if="total > 0">
              Total {{ total }} dokumen
            </template>
            <template v-else>Tidak ada data</template>
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
              <tr>
                <th class="px-4 py-2 text-center font-medium w-12">NO</th>
                <th class="px-4 py-2 text-left font-medium">Jenis Dokumen</th>
                <th class="px-4 py-2 text-left font-medium">No Dokumen</th>
                <th class="px-4 py-2 text-left font-medium">Tujuan</th>
                <th class="px-4 py-2 text-left font-medium">Perihal</th>
                <th class="px-4 py-2 text-left font-medium">Tgl Dokumen</th>
                <th class="px-4 py-2 text-left font-medium">Tgl Kirim</th>
                <th class="px-4 py-2 text-left font-medium">Keterangan</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-if="loading">
                <td colspan="8" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
              </tr>
              <tr v-else-if="!rows.length">
                <td colspan="8" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                  Tidak ada data yang ditemukan.
                </td>
              </tr>
              <tr v-for="(row, idx) in rows" :key="idx" class="hover:bg-muted/30 transition-colors">
                <td class="px-4 py-1 text-xs text-center">{{ idx + 1 }}</td>
                <td class="px-4 py-1 text-xs">{{ row.nama_jenis_dokumen }}</td>
                <td class="px-4 py-1 text-xs">{{ row.nomor }}</td>
                <td class="px-4 py-1 text-xs">{{ row.tujuan }}</td>
                <td class="px-4 py-1 text-xs">{{ row.perihal }}</td>
                <td class="px-4 py-1 text-xs whitespace-nowrap">{{ dmy(row.tanggal_dokumen) }}</td>
                <td class="px-4 py-1 text-xs whitespace-nowrap">{{ row.tanggal_kirim ? dmy(row.tanggal_kirim) : '-' }}</td>
                <td class="px-4 py-1 text-xs">{{ row.keterangan || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

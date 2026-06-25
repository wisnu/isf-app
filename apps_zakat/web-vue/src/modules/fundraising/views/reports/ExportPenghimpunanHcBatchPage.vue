<script setup lang="ts">
import { Download } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'

interface BatchOption {
  id: number
  name: string
  batch_date: string
}

const batches = ref<BatchOption[]>([])
const selectedBatchId = shallowRef<number | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

async function loadBatches() {
  loading.value = true
  errorMsg.value = null
  try {
    batches.value = await api.get<BatchOption[]>(
      '/api/fundraising/export-penghimpunan-website/hc-batches'
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat daftar batch'
    batches.value = []
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  if (selectedBatchId.value === null) {
    errorMsg.value = 'Pilih periode batch terlebih dahulu'
    return
  }

  exporting.value = true
  errorMsg.value = null
  try {
    await api.downloadBlob(
      `/api/fundraising/export-penghimpunan-website/hc-batch?batch_id=${selectedBatchId.value}`,
      `DonationList_BATCH_${String(selectedBatchId.value).padStart(3, '0')}.xlsx`
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

onMounted(loadBatches)
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Export Donasi HC Batch</h1>
      <p class="text-sm text-muted">Ekspor data donasi berdasarkan periode HC Batch upload</p>
    </div>

    <!-- Error message -->
    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <!-- Filter card -->
    <div class="rounded-xl border border-border bg-surface p-4 space-y-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Periode Upload</label>
        <div class="min-w-full sm:min-w-[24rem]">
          <SearchSelect
            v-model="selectedBatchId"
            :options="batches.map(b => ({ value: b.id, label: `${b.name} - ${dmy(b.batch_date)}` }))"
            placeholder="Pilih periode batch…"
            :disabled="loading || batches.length === 0"
          />
        </div>
      </div>

      <div class="flex items-center gap-3">
        <Button
          :loading="exporting"
          :disabled="exporting || loading || selectedBatchId === null"
          @click="exportXlsx"
        >
          <Download class="w-3.5 h-3.5 mr-1" />
          {{ exporting ? 'Mengekspor…' : 'Download Excel' }}
        </Button>
        <span v-if="loading" class="text-xs text-muted italic">Memuat daftar batch...</span>
      </div>
    </div>

    <!-- Empty state (sebelum ada batch) -->
    <div v-if="!loading && batches.length === 0" class="rounded-xl border border-border bg-surface/30 p-10 text-center text-sm text-muted italic">
      Tidak ada batch upload yang tersedia
    </div>
  </div>
</template>

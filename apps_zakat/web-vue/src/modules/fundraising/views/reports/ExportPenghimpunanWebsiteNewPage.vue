<script setup lang="ts">
import { Download } from 'lucide-vue-next'
import { shallowRef } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import { api, ApiError } from '@/shared/api/client'

// Get today's date in ISO format
const today = new Date().toISOString().slice(0, 10)

const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

async function exportXlsx() {
  if (!dateFrom.value || !dateTo.value) {
    errorMsg.value = 'Isi tanggal awal dan akhir terlebih dahulu'
    return
  }

  exporting.value = true
  errorMsg.value = null
  try {
    const filename = `DonorTransactionList_${dateFrom.value}_${dateTo.value}.xlsx`
    const params = new URLSearchParams({
      date_from: dateFrom.value,
      date_to: dateTo.value,
    })
    await api.downloadBlob(
      `/api/fundraising/export-penghimpunan-website/date-range?${params}`,
      filename
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Export Donasi Website (Range Tanggal)</h1>
      <p class="text-sm text-muted">Ekspor data donasi berdasarkan range tanggal transaksi dengan detail donor dan breakdown produk</p>
    </div>

    <!-- Error message -->
    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <!-- Filter card -->
    <div class="rounded-xl border border-border bg-surface p-4 space-y-4">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-muted">Periode Tanggal</label>
          <DateField v-model="dateFrom" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium text-muted">s/d</label>
          <DateField v-model="dateTo" />
        </div>
      </div>

      <div class="flex items-center gap-3">
        <Button
          :loading="exporting"
          :disabled="exporting || !dateFrom || !dateTo"
          @click="exportXlsx"
        >
          <Download class="w-3.5 h-3.5 mr-1" />
          {{ exporting ? 'Mengekspor…' : 'Download Excel' }}
        </Button>
      </div>
    </div>

    <!-- Info state (sampai user klik Download) -->
    <div class="rounded-xl border border-border bg-surface/30 p-10 text-center text-sm text-muted italic">
      Atur rentang tanggal lalu klik "Download Excel" untuk mengekspor data
    </div>
  </div>
</template>

<script setup lang="ts">
import { List } from 'lucide-vue-next'
import { computed, onUnmounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'

interface Batch {
  batch_id: number
  filename: string
  upload_date: string
  upload_user: string
  branch_code: string
  total_record: number
  total_amount: number
  authstatus: string
}

const router = useRouter()
const today = new Date().toISOString().slice(0, 10)
const begin = shallowRef(today.slice(0, 8) + '01')
const end = shallowRef(today)
const statusFilter = shallowRef('')
const batches = ref<Batch[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const hasLoaded = shallowRef(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function statusChip(s: string) {
  if (s === 'A') return 'bg-green-100 text-green-800'
  if (s === 'Q') return 'bg-amber-100 text-amber-700'
  if (s === 'F') return 'bg-red-100 text-red-700'
  return 'bg-yellow-100 text-yellow-800'
}

function statusLabel(s: string) {
  if (s === 'A') return 'Approved'
  if (s === 'Q') return 'Diproses'
  if (s === 'F') return 'Gagal'
  return 'Pending'
}

// Auto-refresh setiap 5s saat ada batch dengan authstatus 'Q'
const hasProcessingBatch = computed(() => batches.value.some(b => b.authstatus === 'Q'))
let refreshTimer: ReturnType<typeof setInterval> | null = null

watch(hasProcessingBatch, (val) => {
  if (val && !refreshTimer) {
    refreshTimer = setInterval(() => load(), 5000)
  } else if (!val && refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
}, { immediate: true })

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
})

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const p = new URLSearchParams({ begin: begin.value, end: end.value })
    if (statusFilter.value) p.set('status', statusFilter.value)
    batches.value = await api.get<Batch[]>(
      `/api/transaction/upload/penghimpunan/batches?${p}`,
    )
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof ApiError ? e.message : String(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <List class="h-5 w-5 text-primary" />
      <h1 class="text-lg font-semibold">Daftar Batch Upload Penghimpunan</h1>
    </div>

    <div class="mb-4 flex flex-wrap items-end gap-3">
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Dari</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Sampai</label>
        <DateField v-model="end" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Status</label>
        <select
          v-model="statusFilter"
          class="rounded border border-border bg-background px-2 py-1.5 text-sm"
        >
          <option value="">Semua</option>
          <option value="P">Pending</option>
          <option value="A">Approved</option>
        </select>
      </div>
      <Button :disabled="loading" @click="load">
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="error" :message="errorMsg" class="mb-3" />

    <div v-if="hasLoaded" class="overflow-hidden rounded-lg border border-border">
      <table v-if="batches.length" class="w-full text-sm">
        <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
          <tr>
            <th class="px-3 py-1.5 text-left font-semibold">Batch</th>
            <th class="px-3 py-1.5 text-left font-semibold">Filename</th>
            <th class="px-3 py-1.5 text-left font-semibold">Tgl Upload</th>
            <th class="px-3 py-1.5 text-left font-semibold">Uploader</th>
            <th class="px-3 py-1.5 text-right font-semibold">Record</th>
            <th class="px-3 py-1.5 text-right font-semibold">Total (Rp)</th>
            <th class="px-3 py-1.5 text-left font-semibold">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="b in batches"
            :key="b.batch_id"
            class="cursor-pointer border-t border-border hover:bg-background"
            @click="router.push(`/keuangan/upload/penghimpunan/${b.batch_id}`)"
          >
            <td class="px-3 py-1 font-mono text-xs">#{{ b.batch_id }}</td>
            <td class="px-3 py-1 text-xs">{{ b.filename }}</td>
            <td class="whitespace-nowrap px-3 py-1">{{ dmy(b.upload_date) }}</td>
            <td class="px-3 py-1">{{ b.upload_user }}</td>
            <td class="px-3 py-1.5 text-right font-semibold">{{ b.total_record }}</td>
            <td class="px-3 py-1.5 text-right font-semibold">{{ fmt(b.total_amount) }}</td>
            <td class="px-3 py-1">
              <span
                :class="[
                  'inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[10px] font-medium uppercase',
                  statusChip(b.authstatus),
                ]"
              >
                <span
                  v-if="b.authstatus === 'Q'"
                  class="inline-block w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"
                />
                {{ statusLabel(b.authstatus) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="p-6 text-center text-sm text-muted">Tidak ada batch ditemukan.</div>
    </div>
    <div v-else-if="!loading" class="text-sm text-muted">
      Klik "Tampilkan" untuk memuat data.
    </div>
  </div>
</template>

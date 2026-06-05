<script setup lang="ts">
import { List } from 'lucide-vue-next'
import { ref } from 'vue'
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
const begin = ref(today.slice(0, 8) + '01')
const end = ref(today)
const statusFilter = ref('')
const batches = ref<Batch[]>([])
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const hasLoaded = ref(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function statusChip(s: string) {
  return s === 'A' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
}

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
        <thead class="bg-surface">
          <tr>
            <th class="px-3 py-2 text-left">Batch</th>
            <th class="px-3 py-2 text-left">Filename</th>
            <th class="px-3 py-2 text-left">Tgl Upload</th>
            <th class="px-3 py-2 text-left">Uploader</th>
            <th class="px-3 py-2 text-right">Record</th>
            <th class="px-3 py-2 text-right">Total (Rp)</th>
            <th class="px-3 py-2 text-left">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="b in batches"
            :key="b.batch_id"
            class="cursor-pointer border-t border-border hover:bg-background"
            @click="router.push(`/keuangan/upload/penghimpunan/${b.batch_id}`)"
          >
            <td class="px-3 py-2 font-mono text-xs">#{{ b.batch_id }}</td>
            <td class="px-3 py-2 text-xs">{{ b.filename }}</td>
            <td class="whitespace-nowrap px-3 py-2">{{ dmy(b.upload_date) }}</td>
            <td class="px-3 py-2">{{ b.upload_user }}</td>
            <td class="px-3 py-2 text-right">{{ b.total_record }}</td>
            <td class="px-3 py-2 text-right">{{ fmt(b.total_amount) }}</td>
            <td class="px-3 py-2">
              <span
                :class="[
                  'rounded px-1.5 py-0.5 text-[10px] font-medium uppercase',
                  statusChip(b.authstatus),
                ]"
                >{{ b.authstatus === 'A' ? 'Approved' : 'Pending' }}</span
              >
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

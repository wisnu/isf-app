<script setup lang="ts">
import { ShieldCheck } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRoute } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/stores/auth'

interface BatchItem {
  batch_item_id: number
  row_no: number
  no_rekening: string
  tanggal: string
  keterangan: string
  no_ref: string
  total_kredit: number
  status: string
  pesan: string
  transaction_no: string | null
}

interface BatchDetail {
  batch_id: number
  filename: string
  upload_date: string
  upload_user: string
  branch_code: string
  total_record: number
  total_amount: number
  authstatus: string
  authorized_user: string | null
  items: BatchItem[]
}

const route = useRoute()
const auth = useAuthStore()
const toast = useToast()
const batchId = Number(route.params.id)
const detail = ref<BatchDetail | null>(null)
const loading = shallowRef(true)
const approving = shallowRef(false)
const showConfirm = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const approveError = shallowRef<string | null>(null)

const canApprove = computed(
  () =>
    detail.value?.authstatus === 'P' &&
    auth.hasMenu('finance.upload.collection.approve'),
)
const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

onMounted(async () => {
  try {
    detail.value = await api.get<BatchDetail>(
      `/api/transaction/upload/fund-collection/batches/${batchId}`,
    )
  } catch (e: unknown) {
    errorMsg.value = e instanceof ApiError ? e.message : String(e)
  } finally {
    loading.value = false
  }
})

async function confirmApprove() {
  approving.value = true
  approveError.value = null
  try {
    await api.post(`/api/transaction/upload/fund-collection/batches/${batchId}/approve`, {})
    toast.success('Batch berhasil diotorisasi')
    detail.value = await api.get<BatchDetail>(
      `/api/transaction/upload/fund-collection/batches/${batchId}`,
    )
    showConfirm.value = false
  } catch (e: unknown) {
    approveError.value = e instanceof Error ? e.message : String(e)
  } finally {
    approving.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <ShieldCheck class="h-5 w-5 text-primary" />
      <h1 class="text-lg font-semibold">Detail Batch #{{ batchId }}</h1>
    </div>

    <div v-if="loading" class="text-sm text-muted">Memuat...</div>
    <Alert v-else-if="errorMsg" variant="error" :message="errorMsg" />

    <template v-else-if="detail">
      <div
        class="mb-4 grid grid-cols-2 gap-3 rounded-lg border border-border bg-surface p-4 text-sm"
      >
        <div><span class="text-muted">Filename:</span> {{ detail.filename }}</div>
        <div>
          <span class="text-muted">Tgl Upload:</span> {{ dmy(detail.upload_date) }}
        </div>
        <div><span class="text-muted">Uploader:</span> {{ detail.upload_user }}</div>
        <div><span class="text-muted">Cabang:</span> {{ detail.branch_code }}</div>
        <div><span class="text-muted">Total Record:</span> {{ detail.total_record }}</div>
        <div>
          <span class="text-muted">Total Amount:</span> Rp {{ fmt(detail.total_amount) }}
        </div>
        <div>
          <span class="text-muted">Status:</span>
          <span
            :class="[
              'ml-2 rounded px-1.5 py-0.5 text-[10px] font-medium uppercase',
              detail.authstatus === 'A'
                ? 'bg-green-100 text-green-800'
                : 'bg-yellow-100 text-yellow-800',
            ]"
            >{{ detail.authstatus === 'A' ? 'Approved' : 'Pending' }}</span
          >
        </div>
        <div v-if="detail.authorized_user">
          <span class="text-muted">Diotorisasi:</span> {{ detail.authorized_user }}
        </div>
      </div>

      <div v-if="canApprove" class="mb-4 flex items-center gap-3">
        <Button @click="showConfirm = true">Otorisasi Batch</Button>
        <span class="text-xs text-muted"
          >Tindakan ini tidak bisa dibatalkan — semua transaksi akan terbentuk.</span
        >
      </div>

      <div
        v-if="showConfirm"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
      >
        <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
          <h2 class="mb-2 font-semibold">Konfirmasi Otorisasi</h2>
          <p class="mb-4 text-sm text-muted">
            {{ detail.total_record }} transaksi akan dibuat dan dijurnal. Lanjutkan?
          </p>
          <Alert v-if="approveError" variant="error" :message="approveError" class="mb-3" />
          <div class="flex justify-end gap-3">
            <Button variant="outline" :disabled="approving" @click="showConfirm = false"
              >Batal</Button
            >
            <Button :disabled="approving" @click="confirmApprove">
              {{ approving ? 'Memproses...' : 'Ya, Otorisasi' }}
            </Button>
          </div>
        </div>
      </div>

      <div class="overflow-x-auto rounded-lg border border-border">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-2 py-1.5 text-left font-semibold">No</th>
              <th class="px-2 py-1.5 text-left font-semibold">Rekening</th>
              <th class="px-2 py-1.5 text-left font-semibold">Tanggal</th>
              <th class="min-w-[160px] px-2 py-1.5 text-left font-semibold">Keterangan</th>
              <th class="px-2 py-1.5 text-left font-semibold">Ref</th>
              <th class="px-2 py-1.5 text-right font-semibold">Total</th>
              <th class="px-2 py-1.5 text-left font-semibold">Status</th>
              <th class="px-2 py-1.5 text-left font-semibold">No Transaksi</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in detail.items"
              :key="item.batch_item_id"
              class="border-t border-border hover:bg-background"
            >
              <td class="px-2 py-1">{{ item.row_no }}</td>
              <td class="px-2 py-1">{{ item.no_rekening }}</td>
              <td class="whitespace-nowrap px-2 py-1">{{ dmy(item.tanggal) }}</td>
              <td
                class="max-w-[200px] truncate px-2 py-1"
                :title="item.keterangan"
              >
                {{ item.keterangan }}
              </td>
              <td class="px-2 py-1">{{ item.no_ref }}</td>
              <td class="px-2 py-1 text-right">{{ fmt(item.total_kredit) }}</td>
              <td class="px-2 py-1">
                <span
                  :class="[
                    'rounded px-1 py-0.5 text-[9px] font-medium uppercase',
                    item.status === 'valid'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800',
                  ]"
                  >{{ item.status }}</span
                >
              </td>
              <td class="px-2 py-1 font-mono text-[10px]">
                {{ item.transaction_no ?? '—' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft, RefreshCw, Trash2 } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'

interface JournalItem {
  journalitem_no: number
  fl_account: string | null
  account_name: string | null
  branch_code: string | null
  amount_debit: number
  amount_credit: number
  description: string | null
}

interface TransaksiDetail {
  transaction_id: number
  transaction_no: string | null
  transaction_date: string
  actual_date: string
  amount: number
  donor_no: string | null
  donor_name: string | null
  reference_no: string | null
  description: string | null
  inputer: string | null
  auth_status: string | null
  is_posted: string | null
  auth_operation_mode: string | null
  branch_code: string | null
  channel_account_no: string | null
  channel_name: string | null
  external_transaction_id: number | null
  title_subsystem: string | null
  journal_items: JournalItem[]
}

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()
const txId = Number(route.params.id)
const detail = ref<TransaksiDetail | null>(null)
const loading = shallowRef(true)
const errorMsg = shallowRef<string | null>(null)

const showDeleteConfirm = shallowRef(false)
const deleting = shallowRef(false)
const deleteError = shallowRef<string | null>(null)

const showRepostConfirm = shallowRef(false)
const reposting = shallowRef(false)
const repostError = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const hasActions = computed(() => detail.value?.external_transaction_id == null)
const canDelete = computed(() => {
  if (!detail.value) return false
  if (detail.value.auth_status === 'F' && detail.value.auth_operation_mode === 'D') return false
  return true
})
const canRepost = computed(() => detail.value?.is_posted === 'F')

onMounted(async () => {
  try {
    detail.value = await api.get<TransaksiDetail>(
      `/api/finance/inquiry/transaction-history/transactions/${txId}`,
    )
  } catch (e: unknown) {
    errorMsg.value = e instanceof ApiError ? e.message : String(e)
  } finally {
    loading.value = false
  }
})

async function doDelete() {
  deleting.value = true
  deleteError.value = null
  try {
    await api.post(`/api/finance/inquiry/transaction-history/transactions/${txId}/delete`, {})
    toast.success('Transaksi berhasil dihapus')
    showDeleteConfirm.value = false
    router.push({ name: 'finance-transactions-history' })
  } catch (e: unknown) {
    deleteError.value = e instanceof Error ? e.message : String(e)
  } finally {
    deleting.value = false
  }
}

async function doRepost() {
  reposting.value = true
  repostError.value = null
  try {
    await api.post(`/api/finance/inquiry/transaction-history/transactions/${txId}/repost`, {})
    toast.success('Jurnal berhasil di-repost')
    showRepostConfirm.value = false
    detail.value = await api.get<TransaksiDetail>(
      `/api/finance/inquiry/transaction-history/transactions/${txId}`,
    )
  } catch (e: unknown) {
    repostError.value = e instanceof Error ? e.message : String(e)
  } finally {
    reposting.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <button class="text-muted hover:text-foreground" @click="router.back()">
        <ArrowLeft class="h-4 w-4" />
      </button>
      <h1 class="text-lg font-semibold">Detail Transaksi #{{ txId }}</h1>
    </div>

    <div v-if="loading" class="text-sm text-muted">Memuat...</div>
    <Alert v-else-if="errorMsg" variant="error" :message="errorMsg" />

    <template v-else-if="detail">
      <!-- Header card -->
      <div class="mb-4 grid grid-cols-2 gap-3 rounded-lg border border-border bg-surface p-4 text-sm">
        <div><span class="text-muted">No Transaksi:</span> {{ detail.transaction_no ?? '—' }}</div>
        <div><span class="text-muted">Rekening:</span> {{ detail.channel_name ?? detail.channel_account_no ?? '—' }}</div>
        <div><span class="text-muted">Tgl Aktual:</span> {{ dmy(detail.actual_date) }}</div>
        <div><span class="text-muted">Tgl Transaksi:</span> {{ dmy(detail.transaction_date) }}</div>
        <div><span class="text-muted">Nominal:</span> Rp {{ fmt(detail.amount) }}</div>
        <div><span class="text-muted">Inputer:</span> {{ detail.inputer ?? '—' }}</div>
        <div><span class="text-muted">No Donatur:</span> {{ detail.donor_no ?? '—' }}</div>
        <div><span class="text-muted">Nama Donatur:</span> {{ detail.donor_name ?? '—' }}</div>
        <div><span class="text-muted">No Ref:</span> {{ detail.reference_no ?? '—' }}</div>
        <div><span class="text-muted">Keterangan:</span> {{ detail.description ?? '—' }}</div>
        <div><span class="text-muted">Cabang:</span> {{ detail.branch_code ?? '—' }}</div>
        <div>
          <span class="text-muted">Auth Status:</span>
          <span :class="['ml-1 rounded px-1 py-0.5 text-[9px] font-medium uppercase',
            detail.auth_status === 'T' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800']">
            {{ detail.auth_status === 'T' ? 'Terotorisasi' : 'Pending' }}
          </span>
        </div>
        <div>
          <span class="text-muted">Posted:</span>
          <span :class="['ml-1 rounded px-1 py-0.5 text-[9px] font-medium',
            detail.is_posted === 'T' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600']">
            {{ detail.is_posted === 'T' ? 'Posted' : 'Belum' }}
          </span>
        </div>
        <div v-if="detail.title_subsystem">
          <span class="text-muted">Sub-sistem:</span> {{ detail.title_subsystem }}
        </div>
      </div>

      <!-- Action buttons -->
      <div v-if="hasActions" class="mb-4 flex gap-3 items-center">
        <Button
          v-if="canRepost"
          variant="outline"
          @click="showRepostConfirm = true"
        >
          <RefreshCw class="mr-1 h-3.5 w-3.5" /> Re-post Jurnal
        </Button>
        <Button
          v-if="canDelete"
          variant="outline"
          class="text-red-600 hover:bg-red-50 border-red-200"
          @click="showDeleteConfirm = true"
        >
          <Trash2 class="mr-1 h-3.5 w-3.5" /> Hapus Transaksi
        </Button>
        <span v-if="!canRepost && detail.is_posted === 'T'" class="text-xs text-muted">
          Jurnal sudah ada
        </span>
      </div>

      <!-- Journal items table -->
      <div class="overflow-x-auto rounded-lg border border-border">
        <div class="px-3 py-2 text-xs font-semibold text-muted bg-surface border-b border-border">
          Jurnal Items {{ detail.journal_items.length === 0 ? '— belum ada jurnal' : '' }}
        </div>
        <table v-if="detail.journal_items.length" class="w-full text-xs">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-2 py-1.5 text-left font-semibold">No</th>
              <th class="px-2 py-1.5 text-left font-semibold">Kode Akun</th>
              <th class="px-2 py-1.5 text-left font-semibold min-w-[160px]">Nama Akun</th>
              <th class="px-2 py-1.5 text-right font-semibold">Debit</th>
              <th class="px-2 py-1.5 text-right font-semibold">Kredit</th>
              <th class="px-2 py-1.5 text-left font-semibold">Keterangan</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="ji in detail.journal_items"
              :key="ji.journalitem_no"
              class="border-t border-border hover:bg-background"
            >
              <td class="px-2 py-1">{{ ji.journalitem_no }}</td>
              <td class="px-2 py-1 font-mono">{{ ji.fl_account ?? '—' }}</td>
              <td class="px-2 py-1">{{ ji.account_name ?? ji.fl_account ?? '—' }}</td>
              <td class="px-2 py-1 text-right">{{ ji.amount_debit ? fmt(ji.amount_debit) : '' }}</td>
              <td class="px-2 py-1 text-right">{{ ji.amount_credit ? fmt(ji.amount_credit) : '' }}</td>
              <td class="px-2 py-1 max-w-[180px] truncate" :title="ji.description ?? ''">
                {{ ji.description ?? '' }}
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="p-4 text-sm text-muted text-center">Belum ada jurnal untuk transaksi ini.</div>
      </div>
    </template>

    <!-- Repost confirm dialog -->
    <div v-if="showRepostConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-2 font-semibold">Konfirmasi Re-post Jurnal</h2>
        <p class="mb-4 text-sm text-muted">Jurnal baru akan dibuat untuk transaksi ini. Lanjutkan?</p>
        <Alert v-if="repostError" variant="error" :message="repostError" class="mb-3" />
        <div class="flex justify-end gap-3">
          <Button variant="outline" :disabled="reposting" @click="showRepostConfirm = false">Batal</Button>
          <Button :disabled="reposting" @click="doRepost">
            {{ reposting ? 'Memproses...' : 'Ya, Re-post' }}
          </Button>
        </div>
      </div>
    </div>

    <!-- Delete confirm dialog -->
    <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-2 font-semibold">Konfirmasi Hapus Transaksi</h2>
        <p class="mb-4 text-sm text-muted">
          Transaksi akan dihapus. Jika sudah terotorisasi, akan masuk antrean approval supervisor.
        </p>
        <Alert v-if="deleteError" variant="error" :message="deleteError" class="mb-3" />
        <div class="flex justify-end gap-3">
          <Button variant="outline" :disabled="deleting" @click="showDeleteConfirm = false">Batal</Button>
          <Button
            class="bg-red-600 hover:bg-red-700 text-white"
            :disabled="deleting"
            @click="doDelete"
          >
            {{ deleting ? 'Memproses...' : 'Ya, Hapus' }}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

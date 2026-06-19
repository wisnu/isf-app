<script setup lang="ts">
import { ArrowLeftRight, Plus, Search, X } from 'lucide-vue-next'
import { computed, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import Modal from '@/components/ui/Modal.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'
import type { MenuKey } from '@/lib/menu/registry'

// ── Types ─────────────────────────────────────────────────────────────────────
interface TransferRow {
  transactionid: number
  transactionno: string | null
  actualdate: string
  amount: number
  authstatus: string
  branchcode: string
  inputer: string
  description: string | null
  reference_no: string | null
  source_account_name: string | null
  source_cashaccountno: string | null
  dest_account_name: string | null
  dest_cashaccountno: string | null
}

interface CashAccountOption {
  cashaccountno: string
  accountno: string
  accountname: string
  branchcode: string
  balance: number | null
  cashaccounttype: string
}

interface ListResponse {
  rows: TransferRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

// ── State ─────────────────────────────────────────────────────────────────────
const auth = useAuthStore()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const rows = ref<TransferRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)

const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)

// Modal state
const showForm = shallowRef(false)
const formSaving = shallowRef(false)
const formError = shallowRef<string | null>(null)

// Form fields
const formDate = shallowRef(today)
const formAmount = shallowRef<number | null>(null)
const formDescription = shallowRef('')
const formRefNo = shallowRef('')

// Rekening lookups
const sourceAccount = ref<CashAccountOption | null>(null)
const sourceOptions = ref<CashAccountOption[]>([])
const destAccount = ref<CashAccountOption | null>(null)
const destOptions = ref<CashAccountOption[]>([])

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const showCount = computed(() => {
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, totalRec.value)
  if (!hasLoaded.value) return 'Pilih periode dan klik Tampilkan'
  return totalRec.value > 0 ? `Showing ${from}–${to} of ${totalRec.value} records` : 'Tidak ada data'
})

function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

// ── Rekening lookup ───────────────────────────────────────────────────────────
async function searchAccounts(query: string, target: 'source' | 'dest') {
  if (!query.trim()) {
    if (target === 'source') sourceOptions.value = []
    else destOptions.value = []
    return
  }
  try {
    const res = await api.get<{ rows: CashAccountOption[] }>(
      `/api/transaksi/transfer-antar-rekening/lookup/cash-accounts?search=${encodeURIComponent(query.trim())}`
    )
    if (target === 'source') sourceOptions.value = res.rows ?? []
    else destOptions.value = res.rows ?? []
  } catch {
    if (target === 'source') sourceOptions.value = []
    else destOptions.value = []
  }
}

// ── Load data ─────────────────────────────────────────────────────────────────
async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      date_from: dateFrom.value,
      date_to: dateTo.value,
      page: String(page.value),
      limit: String(pageSize.value),
    })
    const res = await api.get<ListResponse>(`/api/transaksi/transfer-antar-rekening/?${params}`)
    rows.value = res.rows ?? []
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : 'Gagal memuat data'
    toast.error('Gagal memuat data transfer')
  } finally {
    loading.value = false
  }
}

// ── Status badge ──────────────────────────────────────────────────────────────
function authLabel(status: string) {
  return status === 'T' ? 'Disetujui' : 'Menunggu'
}
function authClass(status: string) {
  if (status === 'T') return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200'
  return 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-200'
}

// ── Form modal ────────────────────────────────────────────────────────────────
function openAdd() {
  formDate.value = today
  formAmount.value = null
  formDescription.value = ''
  formRefNo.value = ''
  sourceAccount.value = null
  destAccount.value = null
  sourceOptions.value = []
  destOptions.value = []
  formError.value = null
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  formError.value = null
}

async function submitForm() {
  if (!sourceAccount.value) {
    formError.value = 'Rekening Sumber wajib dipilih'
    return
  }
  if (!destAccount.value) {
    formError.value = 'Rekening Tujuan wajib dipilih'
    return
  }
  if (sourceAccount.value.cashaccountno === destAccount.value.cashaccountno) {
    formError.value = 'Rekening Sumber dan Tujuan tidak boleh sama'
    return
  }
  if (!formAmount.value || formAmount.value <= 0) {
    formError.value = 'Nominal transfer harus lebih dari 0'
    return
  }

  formSaving.value = true
  formError.value = null
  try {
    const result = await api.post<{ submission_id: number; status: string; transaction_id: number | null }>('/api/transaksi/transfer-antar-rekening/', {
      actual_date: formDate.value,
      source_account_no: sourceAccount.value.cashaccountno,
      dest_account_no: destAccount.value.cashaccountno,
      amount: formAmount.value,
      description: formDescription.value,
      reference_no: formRefNo.value,
    })

    if (result.status === 'AUTHORIZED') {
      toast.success(`Transfer berhasil. No. Transaksi tersimpan.`)
    } else {
      toast.info(`Transfer dikirim untuk otorisasi. Status: ${result.status}`)
    }
    closeForm()
    load()
  } catch (e: unknown) {
    formError.value = e instanceof Error ? e.message : 'Gagal menyimpan transfer'
  } finally {
    formSaving.value = false
  }
}
</script>

<template>
  <div class="space-y-0">
    <PageHeader title="Transfer Antar Rekening" subtitle="Transfer dana antara rekening kas dan bank">
      <template #actions>
        <Button
          v-if="auth.hasMenu('keuangan.transaksi.transfer-antar-rekening' as MenuKey)"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="openAdd"
        >
          <Plus class="w-3.5 h-3.5" />
          Input Baru
        </Button>
      </template>
    </PageHeader>

    <!-- Error -->
    <div v-if="errorMsg" class="mx-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar -->
      <div class="px-4 py-3 border-b border-border">
        <div class="flex flex-wrap items-end gap-3">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Dari Tanggal</label>
            <DateField v-model="dateFrom" />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Sampai Tanggal</label>
            <DateField v-model="dateTo" />
          </div>
          <Button variant="secondary" :disabled="loading" @click="() => { page = 1; load() }">
            <Search class="mr-2 h-4 w-4" />
            {{ loading ? 'Memuat...' : 'Tampilkan' }}
          </Button>
        </div>
      </div>

      <!-- Pagination (selalu di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-xs text-muted-foreground tabular-nums">{{ showCount }}</span>
        <TablePagination
          v-if="hasLoaded && totalPages > 1"
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @goto="goto"
        />
      </div>

      <!-- Tabel -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">No. Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">Tanggal</th>
              <th class="px-4 py-2 text-left font-medium">Rekening Sumber</th>
              <th class="px-4 py-2 text-left font-medium">Rekening Tujuan</th>
              <th class="px-4 py-2 text-right font-medium">Nominal</th>
              <th class="px-4 py-2 text-center font-medium">Status</th>
              <th class="px-4 py-2 text-left font-medium">Input Oleh</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length && !hasLoaded">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Pilih periode dan klik Tampilkan untuk melihat data.
              </td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada transaksi dalam periode ini.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.transactionid"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-2 text-xs font-mono">{{ row.transactionno ?? '-' }}</td>
              <td class="px-4 py-2 text-xs">{{ dmy(row.actualdate) }}</td>
              <td class="px-4 py-2 text-xs">
                <span class="font-mono text-[10px] text-muted-foreground">{{ row.source_cashaccountno }}</span>
                <span v-if="row.source_account_name" class="ml-1">{{ row.source_account_name }}</span>
              </td>
              <td class="px-4 py-2 text-xs">
                <span class="font-mono text-[10px] text-muted-foreground">{{ row.dest_cashaccountno }}</span>
                <span v-if="row.dest_account_name" class="ml-1">{{ row.dest_account_name }}</span>
              </td>
              <td class="px-4 py-2 text-xs text-right font-tabular">{{ fmt(row.amount) }}</td>
              <td class="px-4 py-2 text-xs text-center">
                <span :class="['inline-block px-2 py-1 rounded text-[10px] font-semibold', authClass(row.authstatus)]">
                  {{ authLabel(row.authstatus) }}
                </span>
              </td>
              <td class="px-4 py-2 text-xs">{{ row.inputer }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Form Modal: Input Transfer Antar Rekening -->
    <Modal v-if="showForm" @close="closeForm">
      <template #header>
        <div class="flex items-center gap-2">
          <ArrowLeftRight class="w-4 h-4 text-primary" />
          <span class="font-semibold">Input Transfer Antar Rekening</span>
        </div>
      </template>

      <div class="space-y-4 py-1">
        <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

        <!-- Tanggal -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Tanggal Transaksi <span class="text-red-500">*</span></label>
          <DateField v-model="formDate" />
        </div>

        <!-- Rekening Sumber -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Rekening Sumber <span class="text-red-500">*</span></label>
          <SearchSelect
            :model-value="sourceAccount"
            :options="sourceOptions"
            :loading="false"
            placeholder="Cari nama rekening atau nomor..."
            option-label="accountname"
            option-value="cashaccountno"
            @update:model-value="(v) => (sourceAccount = v)"
            @search="(q) => searchAccounts(q, 'source')"
          />
          <p v-if="sourceAccount" class="mt-1 text-[10px] text-muted-foreground font-mono">
            {{ sourceAccount.cashaccountno }}
            <span v-if="sourceAccount.balance !== null"> · Saldo: {{ fmt(sourceAccount.balance) }}</span>
          </p>
        </div>

        <!-- Rekening Tujuan -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Rekening Tujuan <span class="text-red-500">*</span></label>
          <SearchSelect
            :model-value="destAccount"
            :options="destOptions"
            :loading="false"
            placeholder="Cari nama rekening atau nomor..."
            option-label="accountname"
            option-value="cashaccountno"
            @update:model-value="(v) => (destAccount = v)"
            @search="(q) => searchAccounts(q, 'dest')"
          />
          <p v-if="destAccount" class="mt-1 text-[10px] text-muted-foreground font-mono">
            {{ destAccount.cashaccountno }}
            <span v-if="destAccount.balance !== null"> · Saldo: {{ fmt(destAccount.balance) }}</span>
          </p>
        </div>

        <!-- Nominal -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Nominal (Rp) <span class="text-red-500">*</span></label>
          <input
            v-model.number="formAmount"
            type="number"
            min="1"
            step="1"
            placeholder="Masukkan jumlah transfer"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        <!-- Keterangan -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Keterangan</label>
          <input
            v-model="formDescription"
            type="text"
            maxlength="100"
            placeholder="Deskripsi transfer (opsional)"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>

        <!-- No. Referensi -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">No. Referensi</label>
          <input
            v-model="formRefNo"
            type="text"
            maxlength="30"
            placeholder="Nomor referensi (opsional)"
            class="w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="ghost" :disabled="formSaving" @click="closeForm">
            <X class="mr-1.5 h-4 w-4" />
            Batal
          </Button>
          <Button :disabled="formSaving" @click="submitForm">
            <ArrowLeftRight class="mr-1.5 h-4 w-4" />
            {{ formSaving ? 'Menyimpan...' : 'Simpan Transfer' }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

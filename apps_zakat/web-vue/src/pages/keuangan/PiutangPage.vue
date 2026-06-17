<script setup lang="ts">
import { DollarSign, Plus, Search, X } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch, computed } from 'vue'

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
interface PiutangRow {
  id: number
  transactionno: string | null
  transactioncode: string  // 'EAR' (Pinjam) | 'PEAR' (Bayar)
  actualdate: string       // ISO YYYY-MM-DD
  debtorname: string
  debtortype: string       // 'E' (Karyawan) | 'X' (Non-Karyawan)
  amount: number
  status: string           // 'AUTHORIZED' | 'PENDING'
  description: string | null
  inputer: string
}

interface DebtorOption {
  debtorid: string
  debtorcode: string
  debtorname: string
  debtortype: string       // 'E' | 'X'
  branchcode: string
}

interface CashAccountOption {
  cashaccountno: string
  accountname: string
  accountno: string
  branchcode: string
  balance: number | null
  cashaccounttype: string
}

interface GLAccountOption {
  account_code: string
  account_name: string
  account_type: string
  balance: number | null
}

interface ListResponse {
  rows: PiutangRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

// ── State ─────────────────────────────────────────────────────────────────────
const auth = useAuthStore()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const rows = ref<PiutangRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)

// Filter state
const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)

// Modal state
const showForm = shallowRef(false)
const formSaving = shallowRef(false)
const formError = shallowRef<string | null>(null)

// Form fields
const formTransactionType = shallowRef<'P' | 'B'>('P')
const formChannelType = shallowRef<'C' | 'G'>('C')
const formDate = shallowRef(today)
const formAmount = shallowRef<number | null>(null)
const formRefNo = shallowRef('')
const formDescription = shallowRef('')
const formCasher = shallowRef('')

// Debitur lookup
const formDebtor = ref<DebtorOption | null>(null)
const debtorOptions = ref<DebtorOption[]>([])
const debtorDebtorType = shallowRef('')  // Read-only, auto-filled from lookup

// Kas/Bank account lookup
const formCashAccount = ref<CashAccountOption | null>(null)
const cashAccountOptions = ref<CashAccountOption[]>([])

// GL Account lookup
const formGLAccount = ref<GLAccountOption | null>(null)
const glAccountOptions = ref<GLAccountOption[]>([])

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

// ── Debitur lookup ────────────────────────────────────────────────────────────
async function searchDebtors(query: string) {
  if (!query.trim()) {
    debtorOptions.value = []
    return
  }
  try {
    const res = await api.get<{ rows: DebtorOption[] }>(
      `/api/piutang/debitur/?q=${encodeURIComponent(query.trim())}`
    )
    debtorOptions.value = res.rows ?? []
  } catch {
    debtorOptions.value = []
  }
}

function onDebtorSelected(debtor: DebtorOption | null) {
  formDebtor.value = debtor
  if (debtor) {
    debtorDebtorType.value = debtor.debtortype === 'E' ? 'Karyawan' : 'Non-Karyawan'
  } else {
    debtorDebtorType.value = ''
  }
}

// ── Cash account lookup ───────────────────────────────────────────────────────
async function searchCashAccounts(query: string) {
  if (!query.trim()) {
    cashAccountOptions.value = []
    return
  }
  try {
    const res = await api.get<{ rows: CashAccountOption[] }>(
      `/api/piutang/cash-accounts/?q=${encodeURIComponent(query.trim())}`
    )
    cashAccountOptions.value = res.rows ?? []
  } catch {
    cashAccountOptions.value = []
  }
}

// ── GL Account lookup ─────────────────────────────────────────────────────────
async function searchGLAccounts(query: string) {
  if (!query.trim()) {
    glAccountOptions.value = []
    return
  }
  try {
    const res = await api.get<{ rows: GLAccountOption[] }>(
      `/api/piutang/gl-accounts/?q=${encodeURIComponent(query.trim())}`
    )
    glAccountOptions.value = res.rows ?? []
  } catch {
    glAccountOptions.value = []
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
    const res = await api.get<ListResponse>(`/api/piutang/?${params}`)
    rows.value = res.rows ?? []
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : 'Gagal memuat data'
    toast.error('Gagal memuat data piutang')
  } finally {
    loading.value = false
  }
}

// ── Status badge ──────────────────────────────────────────────────────────────
function statusLabel(status: string) {
  if (status === 'AUTHORIZED') return 'Disetujui'
  if (status === 'PENDING') return 'Menunggu'
  return status
}

function statusClass(status: string) {
  if (status === 'AUTHORIZED') return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200'
  if (status === 'PENDING') return 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-200'
  return 'bg-zinc-100 text-zinc-700 dark:bg-zinc-800 dark:text-zinc-200'
}

// ── Transaction type label ────────────────────────────────────────────────────
function typeLabel(code: string) {
  return code === 'EAR' ? 'Pinjam' : code === 'PEAR' ? 'Bayar' : code
}

function debtorTypeLabel(type: string) {
  return type === 'E' ? 'Karyawan' : type === 'X' ? 'Non-Karyawan' : type
}

// ── Form modal ────────────────────────────────────────────────────────────────
function openAdd() {
  formTransactionType.value = 'P'
  formChannelType.value = 'C'
  formDate.value = today
  formAmount.value = null
  formRefNo.value = ''
  formDescription.value = ''
  formCasher.value = ''
  formDebtor.value = null
  debtorDebtorType.value = ''
  formCashAccount.value = null
  formGLAccount.value = null
  debtorOptions.value = []
  cashAccountOptions.value = []
  glAccountOptions.value = []
  formError.value = null
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  formError.value = null
}

async function submitForm() {
  // Validation
  if (!formDate.value) {
    formError.value = 'Tanggal transaksi wajib dipilih'
    return
  }
  if (!formDebtor.value) {
    formError.value = 'Debitur wajib dipilih'
    return
  }
  if (!formAmount.value || formAmount.value <= 0) {
    formError.value = 'Nominal harus lebih dari 0'
    return
  }
  if (formChannelType.value === 'C' && !formCashAccount.value) {
    formError.value = 'Rekening Kas/Bank wajib dipilih'
    return
  }
  if (formChannelType.value === 'G' && !formGLAccount.value) {
    formError.value = 'Kode GL Account wajib dipilih'
    return
  }

  formSaving.value = true
  formError.value = null
  try {
    const payload: Record<string, unknown> = {
      actual_date: formDate.value,
      transaction_type: formTransactionType.value,
      channel_type: formChannelType.value,
      debtor_id: formDebtor.value.debtorid,
      amount: formAmount.value,
      reference_no: formRefNo.value,
      description: formDescription.value,
      casher: formCasher.value,
    }

    if (formChannelType.value === 'C' && formCashAccount.value) {
      payload.cash_account_no = formCashAccount.value.cashaccountno
    } else if (formChannelType.value === 'G' && formGLAccount.value) {
      payload.gl_account_code = formGLAccount.value.account_code
    }

    const result = await api.post<{ submission_id: number; status: string; transaction_id: number | null }>(
      '/api/piutang/',
      payload
    )

    if (result.status === 'AUTHORIZED') {
      toast.success(`Piutang berhasil disimpan dan disetujui.`)
    } else if (result.status === 'PENDING') {
      toast.info(`Piutang dikirim untuk otorisasi. Status: ${result.status}`)
    } else {
      toast.success(`Piutang berhasil disimpan.`)
    }
    closeForm()
    load()
  } catch (e: unknown) {
    formError.value = e instanceof Error ? e.message : 'Gagal menyimpan piutang'
  } finally {
    formSaving.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="space-y-0">
    <PageHeader title="Piutang (Pinjam/Bayar)" subtitle="Kelola transaksi pinjam dan bayar piutang kepada karyawan dan pihak eksternal">
      <template #actions>
        <Button
          v-if="auth.hasMenu('keuangan.piutang.pinjam-bayar' as MenuKey)"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="openAdd"
        >
          <Plus class="w-3.5 h-3.5" />
          Input Baru
        </Button>
      </template>
    </PageHeader>

    <!-- Error message -->
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

      <!-- Pagination (SELALU di atas tabel) -->
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
          <thead class="text-[10px] text-muted-foreground uppercase tracking-widest border-b border-border bg-muted/50">
            <tr>
              <th class="px-4 py-2 text-left font-medium">No. Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">Tanggal</th>
              <th class="px-4 py-2 text-left font-medium">Jenis</th>
              <th class="px-4 py-2 text-left font-medium">Debitur</th>
              <th class="px-4 py-2 text-left font-medium">Tipe Debitur</th>
              <th class="px-4 py-2 text-right font-medium">Nominal</th>
              <th class="px-4 py-2 text-center font-medium">Status</th>
              <th class="px-4 py-2 text-left font-medium">Input Oleh</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="8" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length && !hasLoaded">
              <td colspan="8" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Pilih periode dan klik Tampilkan untuk melihat data.
              </td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="8" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada transaksi dalam periode ini.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.id"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-2 text-xs font-mono">{{ row.transactionno ?? '-' }}</td>
              <td class="px-4 py-2 text-xs">{{ dmy(row.actualdate) }}</td>
              <td class="px-4 py-2 text-xs">{{ typeLabel(row.transactioncode) }}</td>
              <td class="px-4 py-2 text-xs">{{ row.debtorname }}</td>
              <td class="px-4 py-2 text-xs">{{ debtorTypeLabel(row.debtortype) }}</td>
              <td class="px-4 py-2 text-xs text-right font-tabular">{{ fmt(row.amount) }}</td>
              <td class="px-4 py-2 text-xs text-center">
                <span :class="['inline-block px-2 py-1 rounded text-[10px] font-semibold', statusClass(row.status)]">
                  {{ statusLabel(row.status) }}
                </span>
              </td>
              <td class="px-4 py-2 text-xs">{{ row.inputer }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Form Modal: Input Piutang -->
    <Modal v-if="showForm" @close="closeForm">
      <template #header>
        <div class="flex items-center gap-2">
          <DollarSign class="w-4 h-4 text-primary" />
          <span class="font-semibold">Input Piutang (Pinjam/Bayar)</span>
        </div>
      </template>

      <div class="space-y-4 py-1">
        <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

        <!-- Row 1: Jenis Transaksi + Tanggal -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Jenis Transaksi <span class="text-red-500">*</span></label>
            <select
              v-model="formTransactionType"
              class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
            >
              <option value="P">Pinjam (EAR)</option>
              <option value="B">Bayar (PEAR)</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Tanggal Transaksi <span class="text-red-500">*</span></label>
            <DateField v-model="formDate" />
          </div>
        </div>

        <!-- Row 2: Channel Type + Account (conditional) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Channel <span class="text-red-500">*</span></label>
            <select
              v-model="formChannelType"
              class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
            >
              <option value="C">Kas/Bank</option>
              <option value="G">Rekening Ledger</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">
              <template v-if="formChannelType === 'C'">Rekening Kas/Bank <span class="text-red-500">*</span></template>
              <template v-else>GL Account Code <span class="text-red-500">*</span></template>
            </label>
            <!-- Cash Account (visible saat channel=C) -->
            <div v-show="formChannelType === 'C'">
              <SearchSelect
                :model-value="formCashAccount"
                :options="cashAccountOptions"
                :loading="false"
                placeholder="Cari rekening kas/bank..."
                option-label="accountname"
                option-value="cashaccountno"
                @update:model-value="(v) => (formCashAccount = v)"
                @search="searchCashAccounts"
              />
              <p v-if="formCashAccount" class="mt-1 text-[10px] text-muted-foreground font-mono">
                {{ formCashAccount.cashaccountno }}
                <span v-if="formCashAccount.balance !== null"> · Saldo: {{ fmt(formCashAccount.balance) }}</span>
              </p>
            </div>
            <!-- GL Account (visible saat channel=G) -->
            <div v-show="formChannelType === 'G'">
              <SearchSelect
                :model-value="formGLAccount"
                :options="glAccountOptions"
                :loading="false"
                placeholder="Cari kode GL account..."
                option-label="account_name"
                option-value="account_code"
                @update:model-value="(v) => (formGLAccount = v)"
                @search="searchGLAccounts"
              />
              <p v-if="formGLAccount" class="mt-1 text-[10px] text-muted-foreground font-mono">
                {{ formGLAccount.account_code }}
                <span v-if="formGLAccount.balance !== null"> · Saldo: {{ fmt(formGLAccount.balance) }}</span>
              </p>
            </div>
          </div>
        </div>

        <!-- Row 3: Debitur (full width) -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Nama Debitur <span class="text-red-500">*</span></label>
          <SearchSelect
            :model-value="formDebtor"
            :options="debtorOptions"
            :loading="false"
            placeholder="Cari nama debitur atau nomor..."
            option-label="debtorname"
            option-value="debtorid"
            @update:model-value="onDebtorSelected"
            @search="searchDebtors"
          />
          <p v-if="formDebtor" class="mt-1 text-[10px] text-muted-foreground font-mono">
            {{ formDebtor.debtorcode }}
          </p>
        </div>

        <!-- Tipe Debitur (read-only) -->
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Tipe Debitur</label>
          <input
            :value="debtorDebtorType"
            type="text"
            readonly
            class="w-full rounded-lg border border-input bg-muted px-2.5 py-2 text-xs text-muted-foreground cursor-not-allowed"
          />
        </div>

        <!-- Row 4: Nominal + No Referensi -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Nominal (Rp) <span class="text-red-500">*</span></label>
            <input
              v-model.number="formAmount"
              type="number"
              min="1"
              step="1"
              placeholder="Masukkan jumlah"
              class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">No. Referensi (Cek/Kwitansi)</label>
            <input
              v-model="formRefNo"
              type="text"
              maxlength="30"
              placeholder="Nomor referensi (opsional)"
              class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </div>
        </div>

        <!-- Row 5: Kasir + Keterangan -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Kasir</label>
            <input
              v-model="formCasher"
              type="text"
              maxlength="50"
              placeholder="Nama kasir (opsional)"
              class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Keterangan</label>
            <input
              v-model="formDescription"
              type="text"
              maxlength="100"
              placeholder="Deskripsi (opsional)"
              class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
            />
          </div>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="ghost" :disabled="formSaving" @click="closeForm">
            <X class="mr-1.5 h-4 w-4" />
            Batal
          </Button>
          <Button :disabled="formSaving" @click="submitForm">
            <DollarSign class="mr-1.5 h-4 w-4" />
            {{ formSaving ? 'Menyimpan...' : 'Simpan Piutang' }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

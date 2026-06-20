<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { shallowRef, ref } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────
interface DebtorOption {
  debtorid: string
  debtorcode: string
  debtorname: string
  debtortype: string
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

// ── State ─────────────────────────────────────────────────────────────────────
const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const saving = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const transactionType = shallowRef<'P' | 'B'>('P')
const channelType = shallowRef<'C' | 'G'>('C')
const txDate = shallowRef(today)
const amount = shallowRef<number | null>(null)
const refNo = shallowRef('')
const description = shallowRef('')
const casher = shallowRef('')

const debtor = ref<DebtorOption | null>(null)
const debtorOptions = ref<DebtorOption[]>([])
const debtorTypeLabel = shallowRef('')
const cashAccount = ref<CashAccountOption | null>(null)
const cashAccountOptions = ref<CashAccountOption[]>([])
const glAccount = ref<GLAccountOption | null>(null)
const glAccountOptions = ref<GLAccountOption[]>([])

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

// ── Lookups ───────────────────────────────────────────────────────────────────
async function searchDebtors(query: string) {
  if (!query.trim()) { debtorOptions.value = []; return }
  try {
    const res = await api.get<{ rows: DebtorOption[] }>(
      `/api/piutang/debitur/?q=${encodeURIComponent(query.trim())}`,
    )
    debtorOptions.value = res.rows ?? []
  } catch { debtorOptions.value = [] }
}

function onDebtorSelected(d: DebtorOption | null) {
  debtor.value = d
  debtorTypeLabel.value = d ? (d.debtortype === 'E' ? 'Karyawan' : 'Non-Karyawan') : ''
}

async function searchCashAccounts(query: string) {
  if (!query.trim()) { cashAccountOptions.value = []; return }
  try {
    const res = await api.get<{ rows: CashAccountOption[] }>(
      `/api/piutang/cash-accounts/?q=${encodeURIComponent(query.trim())}`,
    )
    cashAccountOptions.value = res.rows ?? []
  } catch { cashAccountOptions.value = [] }
}

async function searchGLAccounts(query: string) {
  if (!query.trim()) { glAccountOptions.value = []; return }
  try {
    const res = await api.get<{ rows: GLAccountOption[] }>(
      `/api/piutang/gl-accounts/?q=${encodeURIComponent(query.trim())}`,
    )
    glAccountOptions.value = res.rows ?? []
  } catch { glAccountOptions.value = [] }
}

// ── Submit ────────────────────────────────────────────────────────────────────
async function submit() {
  if (!txDate.value) { errorMsg.value = 'Tanggal transaksi wajib dipilih'; return }
  if (!debtor.value) { errorMsg.value = 'Debitur wajib dipilih'; return }
  if (!amount.value || amount.value <= 0) { errorMsg.value = 'Nominal harus lebih dari 0'; return }
  if (channelType.value === 'C' && !cashAccount.value) { errorMsg.value = 'Rekening Kas/Bank wajib dipilih'; return }
  if (channelType.value === 'G' && !glAccount.value) { errorMsg.value = 'GL Account wajib dipilih'; return }

  saving.value = true
  errorMsg.value = null
  try {
    const payload: Record<string, unknown> = {
      actual_date: txDate.value,
      transaction_type: transactionType.value,
      channel_type: channelType.value,
      debtor_id: debtor.value.debtorid,
      amount: amount.value,
      reference_no: refNo.value,
      description: description.value,
      casher: casher.value,
    }
    if (channelType.value === 'C' && cashAccount.value)
      payload.cash_account_no = cashAccount.value.cashaccountno
    else if (channelType.value === 'G' && glAccount.value)
      payload.gl_account_code = glAccount.value.account_code

    const result = await api.post<{ submission_id: number; status: string; transaction_id: number | null }>(
      '/api/piutang/', payload,
    )
    if (result.status === 'AUTHORIZED') toast.success('Piutang berhasil disimpan dan disetujui.')
    else toast.info(`Piutang dikirim untuk otorisasi. Status: ${result.status}`)

    void router.push({ name: 'finance-transactions-receivable' })
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : 'Gagal menyimpan piutang'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Back button -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-transactions-receivable' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
      <span class="text-xs text-slate-400">Buat transaksi pinjam atau bayar piutang</span>
    </div>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <!-- Form card -->
    <div class="max-w-2xl rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Input Piutang (Pinjam / Bayar)</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Jenis Transaksi <span class="text-red-500">*</span></label>
            <select v-model="transactionType" class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="P">Pinjam (EAR)</option>
              <option value="B">Bayar (PEAR)</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tanggal Transaksi <span class="text-red-500">*</span></label>
            <DateField v-model="txDate" />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Channel <span class="text-red-500">*</span></label>
            <select v-model="channelType" class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="C">Kas/Bank</option>
              <option value="G">Rekening Ledger</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              <template v-if="channelType === 'C'">Rekening Kas/Bank <span class="text-red-500">*</span></template>
              <template v-else>GL Account Code <span class="text-red-500">*</span></template>
            </label>
            <div v-show="channelType === 'C'">
              <SearchSelect
                :model-value="cashAccount"
                :options="cashAccountOptions"
                :loading="false"
                placeholder="Cari rekening kas/bank..."
                option-label="accountname"
                option-value="cashaccountno"
                @update:model-value="(v) => (cashAccount = v)"
                @search="searchCashAccounts"
              />
              <p v-if="cashAccount" class="mt-1 text-[10px] text-slate-400 font-mono">
                {{ cashAccount.cashaccountno }}
                <span v-if="cashAccount.balance !== null"> · Saldo: {{ fmt(cashAccount.balance) }}</span>
              </p>
            </div>
            <div v-show="channelType === 'G'">
              <SearchSelect
                :model-value="glAccount"
                :options="glAccountOptions"
                :loading="false"
                placeholder="Cari kode GL account..."
                option-label="account_name"
                option-value="account_code"
                @update:model-value="(v) => (glAccount = v)"
                @search="searchGLAccounts"
              />
              <p v-if="glAccount" class="mt-1 text-[10px] text-slate-400 font-mono">
                {{ glAccount.account_code }}
                <span v-if="glAccount.balance !== null"> · Saldo: {{ fmt(glAccount.balance) }}</span>
              </p>
            </div>
          </div>
        </div>

        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Nama Debitur <span class="text-red-500">*</span></label>
          <SearchSelect
            :model-value="debtor"
            :options="debtorOptions"
            :loading="false"
            placeholder="Cari nama debitur atau nomor..."
            option-label="debtorname"
            option-value="debtorid"
            @update:model-value="onDebtorSelected"
            @search="searchDebtors"
          />
          <p v-if="debtor" class="mt-1 text-[10px] text-slate-400 font-mono">
            {{ debtor.debtorcode }}
          </p>
        </div>

        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tipe Debitur</label>
          <input
            :value="debtorTypeLabel"
            type="text"
            readonly
            class="w-full cursor-not-allowed rounded border border-slate-200 bg-slate-100 px-3 py-1.5 text-sm text-slate-500 dark:bg-zinc-800"
          />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Nominal (Rp) <span class="text-red-500">*</span></label>
            <input
              v-model.number="amount"
              type="number"
              min="1"
              step="1"
              placeholder="Masukkan jumlah"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Referensi</label>
            <input
              v-model="refNo"
              type="text"
              maxlength="30"
              placeholder="Nomor referensi (opsional)"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Kasir</label>
            <input
              v-model="casher"
              type="text"
              maxlength="50"
              placeholder="Nama kasir (opsional)"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Keterangan</label>
            <input
              v-model="description"
              type="text"
              maxlength="100"
              placeholder="Deskripsi (opsional)"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <div class="flex gap-2 pt-1">
          <button
            class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
            @click="router.push({ name: 'finance-transactions-receivable' })"
          >
            Batal
          </button>
          <button
            class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="saving"
            @click="submit"
          >
            {{ saving ? 'Menyimpan...' : 'Simpan Piutang' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

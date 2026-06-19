<script setup lang="ts">
import { CreditCard } from 'lucide-vue-next'
import { shallowRef, ref } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
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
  <div class="space-y-4">
    <PageHeader title="Input Piutang (Pinjam/Bayar)" subtitle="Buat transaksi pinjam atau bayar piutang" />

    <div class="rounded-lg border bg-white dark:bg-zinc-900 p-6 space-y-4 max-w-2xl">
      <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Jenis Transaksi <span class="text-red-500">*</span></label>
          <select v-model="transactionType" class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring">
            <option value="P">Pinjam (EAR)</option>
            <option value="B">Bayar (PEAR)</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Tanggal Transaksi <span class="text-red-500">*</span></label>
          <DateField v-model="txDate" />
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Channel <span class="text-red-500">*</span></label>
          <select v-model="channelType" class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring">
            <option value="C">Kas/Bank</option>
            <option value="G">Rekening Ledger</option>
          </select>
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">
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
            <p v-if="cashAccount" class="mt-1 text-[10px] text-muted-foreground font-mono">
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
            <p v-if="glAccount" class="mt-1 text-[10px] text-muted-foreground font-mono">
              {{ glAccount.account_code }}
              <span v-if="glAccount.balance !== null"> · Saldo: {{ fmt(glAccount.balance) }}</span>
            </p>
          </div>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-xs font-medium text-muted-foreground">Nama Debitur <span class="text-red-500">*</span></label>
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
        <p v-if="debtor" class="mt-1 text-[10px] text-muted-foreground font-mono">
          {{ debtor.debtorcode }}
        </p>
      </div>

      <div>
        <label class="mb-1 block text-xs font-medium text-muted-foreground">Tipe Debitur</label>
        <input
          :value="debtorTypeLabel"
          type="text"
          readonly
          class="w-full rounded-lg border border-input bg-muted px-2.5 py-2 text-xs text-muted-foreground cursor-not-allowed"
        />
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Nominal (Rp) <span class="text-red-500">*</span></label>
          <input
            v-model.number="amount"
            type="number"
            min="1"
            step="1"
            placeholder="Masukkan jumlah"
            class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">No. Referensi</label>
          <input
            v-model="refNo"
            type="text"
            maxlength="30"
            placeholder="Nomor referensi (opsional)"
            class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Kasir</label>
          <input
            v-model="casher"
            type="text"
            maxlength="50"
            placeholder="Nama kasir (opsional)"
            class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-muted-foreground">Keterangan</label>
          <input
            v-model="description"
            type="text"
            maxlength="100"
            placeholder="Deskripsi (opsional)"
            class="w-full rounded-lg border border-input bg-background px-2.5 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
      </div>

      <div class="flex justify-end gap-2 pt-2">
        <Button variant="ghost" :disabled="saving" @click="router.push({ name: 'finance-transactions-receivable' })">
          Batal
        </Button>
        <Button :disabled="saving" @click="submit">
          <CreditCard class="mr-1.5 h-4 w-4" />
          {{ saving ? 'Menyimpan...' : 'Simpan Piutang' }}
        </Button>
      </div>
    </div>
  </div>
</template>

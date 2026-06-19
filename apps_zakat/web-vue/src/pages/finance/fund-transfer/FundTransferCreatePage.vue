<script setup lang="ts">
import { ArrowLeftRight } from 'lucide-vue-next'
import { ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────
interface CashAccountOption {
  cashaccountno: string
  accountno: string
  accountname: string
  branchcode: string
  balance: number | null
  cashaccounttype: string
}

// ── State ─────────────────────────────────────────────────────────────────────
const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const saving = shallowRef(false)
const formError = shallowRef<string | null>(null)

const formDate = shallowRef(today)
const formAmount = shallowRef<number | null>(null)
const formDescription = shallowRef('')
const formRefNo = shallowRef('')

const sourceAccount = ref<CashAccountOption | null>(null)
const sourceOptions = ref<CashAccountOption[]>([])
const destAccount = ref<CashAccountOption | null>(null)
const destOptions = ref<CashAccountOption[]>([])

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

// ── Lookup ────────────────────────────────────────────────────────────────────
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

// ── Submit ────────────────────────────────────────────────────────────────────
async function submit() {
  if (!sourceAccount.value) { formError.value = 'Rekening Sumber wajib dipilih'; return }
  if (!destAccount.value) { formError.value = 'Rekening Tujuan wajib dipilih'; return }
  if (sourceAccount.value.cashaccountno === destAccount.value.cashaccountno) {
    formError.value = 'Rekening Sumber dan Tujuan tidak boleh sama'
    return
  }
  if (!formAmount.value || formAmount.value <= 0) {
    formError.value = 'Nominal transfer harus lebih dari 0'
    return
  }

  saving.value = true
  formError.value = null
  try {
    const result = await api.post<{ submission_id: number; status: string; transaction_id: number | null }>(
      '/api/transaksi/transfer-antar-rekening/',
      {
        actual_date: formDate.value,
        source_account_no: sourceAccount.value.cashaccountno,
        dest_account_no: destAccount.value.cashaccountno,
        amount: formAmount.value,
        description: formDescription.value,
        reference_no: formRefNo.value,
      }
    )
    if (result.status === 'AUTHORIZED') toast.success('Transfer berhasil. No. Transaksi tersimpan.')
    else toast.info(`Transfer dikirim untuk otorisasi. Status: ${result.status}`)
    void router.push({ name: 'finance-transactions-fund-transfer' })
  } catch (e: unknown) {
    formError.value = e instanceof Error ? e.message : 'Gagal menyimpan transfer'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Input Transfer Antar Rekening" subtitle="Transfer dana antara rekening kas dan bank" />

    <div class="rounded-xl border border-border bg-surface p-6 space-y-4 max-w-xl">
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

      <div class="flex justify-end gap-2 pt-2">
        <Button variant="ghost" :disabled="saving" @click="router.push({ name: 'finance-transactions-fund-transfer' })">
          Batal
        </Button>
        <Button :disabled="saving" @click="submit">
          <ArrowLeftRight class="mr-1.5 h-4 w-4" />
          {{ saving ? 'Menyimpan...' : 'Simpan Transfer' }}
        </Button>
      </div>
    </div>
  </div>
</template>

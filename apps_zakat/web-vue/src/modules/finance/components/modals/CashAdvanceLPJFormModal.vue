<script setup lang="ts">
import { X } from 'lucide-vue-next'
import { ref, shallowRef, watch, onMounted } from 'vue'

import Modal from '@/shared/components/Modal.vue'
import DateField from '@/shared/components/DateField.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import AmountInput from '@/shared/components/AmountInput.vue'
import { api } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'

interface EmployeeLookup {
  employee_id: number
  employee_name: string
  employee_number: string
}

interface OpenUangMuka {
  transactionid: number
  transaction_no: string
  actual_date: string
  description: string | null
  amount: number
  transactionitemid: number
}

interface CashAccountLookup {
  cash_account_no: string
  cash_account_name: string
}

const emit = defineEmits<{ close: []; saved: [] }>()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

// Form state
const actualDate = shallowRef(today)
const selectedEmployee = ref<EmployeeLookup | null>(null)
const selectedOpenCA = ref<OpenUangMuka | null>(null)
const selectedCashAccount = ref<CashAccountLookup | null>(null)
const amount = shallowRef<number | null>(null)
const referenceNo = shallowRef('')
const description = shallowRef('')

// Lookup options
const employeeOptions = ref<EmployeeLookup[]>([])
const openCAOptions = ref<OpenUangMuka[]>([])
const cashAccountOptions = ref<CashAccountLookup[]>([])

// Loading states
const loading = shallowRef(false)
const loadingCA = shallowRef(false)

// ── Lookups ────────────────────────────────────────────────────────────────────

async function searchEmployees(query: string) {
  if (!query.trim()) { employeeOptions.value = []; return }
  try {
    const res = await api.get<{ rows: EmployeeLookup[] }>(
      `/api/finance/transaction/cash-advance/lookup/employee?search=${encodeURIComponent(query.trim())}`
    )
    employeeOptions.value = res.rows ?? []
  } catch { employeeOptions.value = [] }
}

async function loadOpenCA(emp: EmployeeLookup) {
  loadingCA.value = true
  openCAOptions.value = []
  selectedOpenCA.value = null
  try {
    const res = await api.get<{ rows: OpenUangMuka[] }>(
      `/api/finance/transaction/cash-advance-settlement/lookup/open-cash-advance?employee_id=${emp.employee_id}`
    )
    openCAOptions.value = res.rows ?? []
    if (!openCAOptions.value.length) {
      toast.error('Tidak ada uang muka yang belum di-LPJ untuk karyawan ini')
    }
  } catch (e) {
    toast.error('Gagal memuat daftar uang muka')
  } finally {
    loadingCA.value = false
  }
}

async function loadCashAccounts() {
  try {
    const res = await api.get<{ rows: { cash_account_no: string; cash_account_name: string }[] }>(
      '/api/finance/transaction/cash-advance/lookup/cash-account'
    )
    cashAccountOptions.value = (res.rows ?? []).map(r => ({
      cash_account_no: r.cash_account_no,
      cash_account_name: r.cash_account_name,
    }))
  } catch { /* silently fail */ }
}

// ── Watchers ───────────────────────────────────────────────────────────────────

watch(selectedEmployee, (emp) => {
  if (emp) loadOpenCA(emp)
  else {
    openCAOptions.value = []
    selectedOpenCA.value = null
  }
})

watch(selectedOpenCA, (ca) => {
  if (ca) {
    amount.value = ca.amount
    description.value = ca.description ?? ''
  }
})

// ── Submit ─────────────────────────────────────────────────────────────────────

function validate(): boolean {
  if (!actualDate.value) { toast.error('Tanggal harus diisi'); return false }
  if (!selectedEmployee.value) { toast.error('Karyawan harus dipilih'); return false }
  if (!selectedOpenCA.value) { toast.error('Pilih transaksi uang muka yang akan di-LPJ'); return false }
  if (!selectedCashAccount.value) { toast.error('Rekening kas harus dipilih'); return false }
  if (!amount.value || amount.value <= 0) { toast.error('Nominal harus lebih dari 0'); return false }
  return true
}

async function submitForm() {
  if (!validate()) return

  loading.value = true
  try {
    const ca = selectedOpenCA.value!
    const emp = selectedEmployee.value!
    const payload = {
      actual_date: actualDate.value,
      ref_transaction_no: ca.transaction_no,
      ref_transaction_item_id: ca.transactionitemid,
      ref_amount: ca.amount,
      employee_id: emp.employee_id,
      employee_name: emp.employee_name,
      cash_account_no: selectedCashAccount.value!.cash_account_no,
      amount: amount.value,
      reference_no: referenceNo.value,
      description: description.value,
    }
    await api.post('/api/finance/transaction/cash-advance-settlement', payload)
    toast.success('Pengembalian uang muka berhasil disimpan')
    emit('saved')
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal menyimpan pengembalian')
  } finally {
    loading.value = false
  }
}

onMounted(loadCashAccounts)
</script>

<template>
  <Modal :open="true" class="max-w-2xl" @close="emit('close')">
    <div class="flex items-center justify-between border-b border-border px-6 py-4">
      <h2 class="text-sm font-semibold text-slate-800 dark:text-slate-100">Input Pengembalian / LPJ Uang Muka</h2>
      <button class="rounded p-1 hover:bg-muted transition-colors" @click="emit('close')">
        <X class="w-4 h-4" />
      </button>
    </div>

    <div class="space-y-4 px-6 py-5">
      <!-- Tanggal -->
      <div>
        <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tanggal <span class="text-red-500">*</span></label>
        <DateField v-model="actualDate" />
      </div>

      <!-- Karyawan -->
      <div>
        <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Karyawan <span class="text-red-500">*</span></label>
        <SearchSelect
          :model-value="selectedEmployee"
          :options="employeeOptions"
          :loading="false"
          placeholder="Ketik nama atau nomor karyawan..."
          option-label="employee_name"
          @update:model-value="(v) => (selectedEmployee = v)"
          @search="searchEmployees"
        />
      </div>

      <!-- Pilih Uang Muka -->
      <div>
        <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Uang Muka Yang Di-LPJ <span class="text-red-500">*</span></label>
        <SearchSelect
          :model-value="selectedOpenCA"
          :options="openCAOptions"
          :loading="loadingCA"
          :disabled="!selectedEmployee"
          placeholder="Pilih transaksi uang muka..."
          option-label="transaction_no"
          @update:model-value="(v) => (selectedOpenCA = v)"
        />
        <!-- Ref detail (readonly) -->
        <div v-if="selectedOpenCA" class="mt-2 rounded bg-muted/50 border border-border px-3 py-2 text-xs space-y-1">
          <div class="flex gap-4">
            <span class="text-muted-foreground">Tanggal CA:</span>
            <span>{{ dmy(selectedOpenCA.actual_date) }}</span>
          </div>
          <div class="flex gap-4">
            <span class="text-muted-foreground">Nominal CA:</span>
            <span class="font-semibold">{{ new Intl.NumberFormat('id-ID').format(selectedOpenCA.amount) }}</span>
          </div>
          <div v-if="selectedOpenCA.description" class="flex gap-4">
            <span class="text-muted-foreground">Keterangan:</span>
            <span>{{ selectedOpenCA.description }}</span>
          </div>
        </div>
      </div>

      <!-- Nominal & Rekening Kas -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Nominal Pengembalian <span class="text-red-500">*</span></label>
          <AmountInput
            v-model="amount"
            placeholder="Masukkan nominal..."
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-zinc-800"
          />
          <p v-if="selectedOpenCA && amount !== selectedOpenCA.amount" class="mt-1 text-[10px] text-amber-600">
            Partial LPJ — berbeda dari nominal CA
          </p>
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Rekening Kas <span class="text-red-500">*</span></label>
          <SearchSelect
            :model-value="selectedCashAccount"
            :options="cashAccountOptions"
            :loading="false"
            placeholder="Pilih rekening kas..."
            option-label="cash_account_name"
            @update:model-value="(v) => (selectedCashAccount = v)"
          />
        </div>
      </div>

      <!-- No. Referensi & Keterangan -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Referensi</label>
          <input
            v-model="referenceNo"
            type="text"
            placeholder="No. kwitansi / bukti setor..."
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Keterangan</label>
          <input
            v-model="description"
            type="text"
            placeholder="Deskripsi singkat..."
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="flex items-center justify-end gap-3 border-t border-border px-6 py-3">
      <button
        class="border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
        @click="emit('close')"
      >Batal</button>
      <button
        class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="loading"
        @click="submitForm"
      >{{ loading ? 'Menyimpan...' : 'Simpan' }}</button>
    </div>
  </Modal>
</template>

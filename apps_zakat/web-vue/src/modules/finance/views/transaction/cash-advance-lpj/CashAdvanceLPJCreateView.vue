<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

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

const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const actualDate = shallowRef(today)
const selectedEmployee = ref<EmployeeLookup | null>(null)
const selectedOpenCA = ref<OpenUangMuka | null>(null)
const selectedCashAccount = ref<CashAccountLookup | null>(null)
const amount = shallowRef<number | null>(null)
const referenceNo = shallowRef('')
const description = shallowRef('')

const employeeOptions = ref<EmployeeLookup[]>([])
const openCAOptions = ref<OpenUangMuka[]>([])
const cashAccountOptions = ref<CashAccountLookup[]>([])

const loading = shallowRef(false)
const loadingCA = shallowRef(false)

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
    if (!openCAOptions.value.length) toast.error('Tidak ada uang muka yang belum di-LPJ untuk karyawan ini')
  } catch { toast.error('Gagal memuat daftar uang muka') }
  finally { loadingCA.value = false }
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
  } catch { /* silent */ }
}

watch(selectedEmployee, (emp) => {
  if (emp) void loadOpenCA(emp)
  else { openCAOptions.value = []; selectedOpenCA.value = null }
})

watch(selectedOpenCA, (ca) => {
  if (ca) { amount.value = ca.amount; description.value = ca.description ?? '' }
})

function validate(): boolean {
  if (!actualDate.value) { toast.error('Tanggal harus diisi'); return false }
  if (!selectedEmployee.value) { toast.error('Karyawan harus dipilih'); return false }
  if (!selectedOpenCA.value) { toast.error('Pilih transaksi uang muka yang akan di-LPJ'); return false }
  if (!selectedCashAccount.value) { toast.error('Rekening kas harus dipilih'); return false }
  if (!amount.value || amount.value <= 0) { toast.error('Nominal harus lebih dari 0'); return false }
  return true
}

async function submit() {
  if (!validate()) return
  loading.value = true
  try {
    const ca = selectedOpenCA.value!
    const emp = selectedEmployee.value!
    await api.post('/api/finance/transaction/cash-advance-settlement', {
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
    })
    toast.success('Pengembalian uang muka berhasil disimpan')
    void router.push({ name: 'finance-transactions-cash-advance-lpj' })
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal menyimpan pengembalian')
  } finally {
    loading.value = false
  }
}

onMounted(loadCashAccounts)
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Back button -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-transactions-cash-advance-lpj' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
      <span class="text-xs text-slate-400">Catat pengembalian atau LPJ uang muka karyawan</span>
    </div>

    <!-- Form card -->
    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-2xl">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Pengembalian / LPJ Uang Muka</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <!-- Tanggal -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Tanggal <span class="text-red-500">*</span>
          </label>
          <DateField v-model="actualDate" />
        </div>

        <!-- Karyawan -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Karyawan <span class="text-red-500">*</span>
          </label>
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

        <!-- Uang Muka Yang Di-LPJ -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Uang Muka Yang Di-LPJ <span class="text-red-500">*</span>
          </label>
          <SearchSelect
            :model-value="selectedOpenCA"
            :options="openCAOptions"
            :loading="loadingCA"
            :disabled="!selectedEmployee"
            placeholder="Pilih transaksi uang muka..."
            option-label="transaction_no"
            @update:model-value="(v) => (selectedOpenCA = v)"
          />
          <div v-if="selectedOpenCA" class="mt-2 rounded border border-slate-200 bg-slate-50 px-3 py-2 text-xs space-y-1 dark:bg-zinc-800">
            <div class="flex gap-4">
              <span class="text-slate-500">Tanggal CA:</span>
              <span>{{ dmy(selectedOpenCA.actual_date) }}</span>
            </div>
            <div class="flex gap-4">
              <span class="text-slate-500">Nominal CA:</span>
              <span class="font-semibold">{{ new Intl.NumberFormat('id-ID').format(selectedOpenCA.amount) }}</span>
            </div>
            <div v-if="selectedOpenCA.description" class="flex gap-4">
              <span class="text-slate-500">Keterangan:</span>
              <span>{{ selectedOpenCA.description }}</span>
            </div>
          </div>
        </div>

        <!-- Nominal Pengembalian & Rekening Kas -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Nominal Pengembalian <span class="text-red-500">*</span>
            </label>
            <AmountInput v-model="amount" placeholder="Masukkan nominal..." />
            <p v-if="selectedOpenCA && amount !== selectedOpenCA.amount" class="mt-1 text-[10px] text-amber-600">
              Partial LPJ — berbeda dari nominal CA
            </p>
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Rekening Kas <span class="text-red-500">*</span>
            </label>
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
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Referensi</label>
            <input
              v-model="referenceNo"
              placeholder="No. kwitansi / bukti setor..."
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Keterangan</label>
            <input
              v-model="description"
              placeholder="Deskripsi singkat..."
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2 pt-1">
          <button
            class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
            :disabled="loading"
            @click="router.push({ name: 'finance-transactions-cash-advance-lpj' })"
          >
            Batal
          </button>
          <button
            class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="loading"
            @click="submit"
          >
            {{ loading ? 'Menyimpan...' : 'Simpan' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

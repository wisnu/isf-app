<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
import { api } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

interface EmployeeLookup {
  employee_id: number
  employee_name: string
  employee_number: string
}

interface CashAccountLookup {
  cash_account_no: string
  cash_account_name: string
}

const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const form = ref({
  actual_date: today,
  employee_id: null as number | null,
  employee_name: '',
  cash_account_no: '',
  amount: null as number | null,
  reference_no: '',
  description: '',
  received_from: '',
})

const loading = shallowRef(false)
const selectedEmployee = ref<EmployeeLookup | null>(null)
const selectedCashAccount = ref<CashAccountLookup | null>(null)
const employeeOptions = ref<EmployeeLookup[]>([])
const cashAccountOptions = ref<CashAccountLookup[]>([])

async function searchEmployees(query: string) {
  if (!query.trim()) { employeeOptions.value = []; return }
  try {
    const res = await api.get<{ rows: EmployeeLookup[] }>(
      `/api/transaction/cash-advance/lookup/employee?search=${encodeURIComponent(query.trim())}`
    )
    employeeOptions.value = res.rows ?? []
  } catch { employeeOptions.value = [] }
}

async function loadCashAccounts() {
  try {
    const res = await api.get<{ rows: CashAccountLookup[] }>('/api/transaction/cash-advance/lookup/cash-account')
    cashAccountOptions.value = res.rows ?? []
  } catch { /* silent */ }
}

function handleEmployeeSelect(emp: EmployeeLookup | null) {
  selectedEmployee.value = emp
  if (emp) {
    form.value.employee_id = emp.employee_id
    form.value.employee_name = emp.employee_name
  } else {
    form.value.employee_id = null
    form.value.employee_name = ''
  }
}

function handleCashAccountSelect(acc: CashAccountLookup | null) {
  selectedCashAccount.value = acc
  form.value.cash_account_no = acc ? acc.cash_account_no : ''
}

function validate(): boolean {
  if (!form.value.actual_date) { toast.error('Tanggal harus diisi'); return false }
  if (!form.value.employee_id) { toast.error('Karyawan harus dipilih'); return false }
  if (!form.value.cash_account_no) { toast.error('Rekening kas harus dipilih'); return false }
  if (!form.value.amount || form.value.amount <= 0) { toast.error('Nominal harus lebih dari 0'); return false }
  return true
}

async function submit() {
  if (!validate()) return
  loading.value = true
  try {
    await api.post('/api/transaction/cash-advance', {
      ...form.value,
      budget_id: 0,
      real_memo_id: 0,
      fund_entity: 4,
    })
    toast.success('Transaksi uang muka berhasil disimpan')
    void router.push({ name: 'finance-transactions-cash-advance' })
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal menyimpan transaksi')
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
        @click="router.push({ name: 'finance-transactions-cash-advance' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
      <span class="text-xs text-slate-400">Penyerahan uang muka kepada karyawan</span>
    </div>

    <!-- Form card -->
    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-2xl">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Penyerahan Uang Muka</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <!-- Tanggal -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Tanggal <span class="text-red-500">*</span>
          </label>
          <DateField v-model="form.actual_date" />
        </div>

        <!-- Karyawan & Rekening Kas -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Karyawan <span class="text-red-500">*</span>
            </label>
            <SearchSelect
              :model-value="selectedEmployee"
              :options="employeeOptions"
              :loading="false"
              placeholder="Ketik nama atau nomor..."
              option-label="employee_name"
              @update:model-value="handleEmployeeSelect"
              @search="searchEmployees"
            />
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
              @update:model-value="handleCashAccountSelect"
            />
          </div>
        </div>

        <!-- Nominal & No. Referensi -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Nominal <span class="text-red-500">*</span>
            </label>
            <AmountInput v-model="form.amount" placeholder="Masukkan nominal..." />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Referensi</label>
            <input
              v-model="form.reference_no"
              placeholder="Contoh: CHK-2026-001"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <!-- Keterangan & Penerima Dari -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Keterangan</label>
            <input
              v-model="form.description"
              placeholder="Deskripsi singkat..."
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Penerima Dari</label>
            <input
              v-model="form.received_from"
              placeholder="Nama atau unit..."
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-2 pt-1">
          <button
            class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
            :disabled="loading"
            @click="router.push({ name: 'finance-transactions-cash-advance' })"
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

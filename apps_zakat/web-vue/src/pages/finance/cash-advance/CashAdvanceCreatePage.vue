<script setup lang="ts">
import { onMounted, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import DateField from '@/components/ui/DateField.vue'
import Input from '@/components/ui/Input.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

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
      `/api/transaksi/uang-muka/lookup/employee?search=${encodeURIComponent(query.trim())}`
    )
    employeeOptions.value = res.rows ?? []
  } catch { employeeOptions.value = [] }
}

async function loadCashAccounts() {
  try {
    const res = await api.get<{ rows: CashAccountLookup[] }>('/api/transaksi/uang-muka/lookup/cash-account')
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
    await api.post('/api/transaksi/uang-muka', {
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
  <div class="space-y-4">
    <PageHeader title="Input Penyerahan Uang Muka" subtitle="Penyerahan uang muka kepada karyawan" />

    <div class="rounded-xl border border-border bg-surface p-6 space-y-4 max-w-2xl">
      <!-- Tanggal -->
      <div>
        <label class="block text-sm font-medium mb-1.5">Tanggal <span class="text-red-500">*</span></label>
        <DateField v-model="form.actual_date" />
      </div>

      <!-- Karyawan & Rekening Kas -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1.5">Karyawan <span class="text-red-500">*</span></label>
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
          <label class="block text-sm font-medium mb-1.5">Rekening Kas <span class="text-red-500">*</span></label>
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
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1.5">Nominal <span class="text-red-500">*</span></label>
          <AmountInput v-model="form.amount" placeholder="Masukkan nominal..." />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1.5">No. Referensi</label>
          <Input v-model="form.reference_no" placeholder="Contoh: CHK-2026-001" />
        </div>
      </div>

      <!-- Keterangan & Penerima Dari -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-1.5">Keterangan</label>
          <Input v-model="form.description" placeholder="Deskripsi singkat..." />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1.5">Penerima Dari</label>
          <Input v-model="form.received_from" placeholder="Nama atau unit..." />
        </div>
      </div>

      <div class="flex justify-end gap-2 pt-2">
        <Button variant="outline" :disabled="loading" @click="router.push({ name: 'finance-transactions-cash-advance' })">
          Batal
        </Button>
        <Button :loading="loading" @click="submit">Simpan</Button>
      </div>
    </div>
  </div>
</template>

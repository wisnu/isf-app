<script setup lang="ts">
import { X } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'

import Modal from '@/components/ui/Modal.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import DateField from '@/components/ui/DateField.vue'
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

interface FormData {
  actual_date: string
  employee_id: number | null
  employee_name: string
  cash_account_no: string
  amount: number | null
  reference_no: string
  description: string
  received_from: string
}

const emit = defineEmits<{
  close: []
  saved: []
}>()

const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const form = ref<FormData>({
  actual_date: today,
  employee_id: null,
  employee_name: '',
  cash_account_no: '',
  amount: null,
  reference_no: '',
  description: '',
  received_from: '',
})

const loading = shallowRef(false)
const selectedEmployee = ref<EmployeeLookup | null>(null)
const selectedCashAccount = ref<CashAccountLookup | null>(null)

const employeeOptions = ref<EmployeeLookup[]>([])
const cashAccountOptions = ref<CashAccountLookup[]>([])

// ── Employee lookup ───────────────────────────────────────────────────────────
async function searchEmployees(query: string) {
  if (!query.trim()) {
    employeeOptions.value = []
    return
  }
  try {
    const res = await api.get<{ rows: EmployeeLookup[] }>(
      `/api/transaksi/uang-muka/lookup/employee?search=${encodeURIComponent(query.trim())}`
    )
    employeeOptions.value = res.rows ?? []
  } catch (e) {
    employeeOptions.value = []
  }
}

// ── Cash account lookup ───────────────────────────────────────────────────────
async function loadCashAccounts() {
  try {
    const res = await api.get<{ rows: CashAccountLookup[] }>(
      '/api/transaksi/uang-muka/lookup/cash-account'
    )
    cashAccountOptions.value = res.rows ?? []
  } catch (e) {
    // silently fail
  }
}

// ── Form handlers ─────────────────────────────────────────────────────────────
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
  if (acc) {
    form.value.cash_account_no = acc.cash_account_no
  } else {
    form.value.cash_account_no = ''
  }
}

function validateForm(): boolean {
  if (!form.value.actual_date) {
    toast.error('Tanggal harus diisi')
    return false
  }
  if (!form.value.employee_id) {
    toast.error('Karyawan harus dipilih')
    return false
  }
  if (!form.value.cash_account_no) {
    toast.error('Rekening kas harus dipilih')
    return false
  }
  if (!form.value.amount || form.value.amount <= 0) {
    toast.error('Nominal harus lebih dari 0')
    return false
  }
  return true
}

async function submitForm() {
  if (!validateForm()) return

  loading.value = true
  try {
    const payload = {
      actual_date: form.value.actual_date,
      employee_id: form.value.employee_id,
      employee_name: form.value.employee_name,
      cash_account_no: form.value.cash_account_no,
      amount: form.value.amount,
      reference_no: form.value.reference_no,
      description: form.value.description,
      received_from: form.value.received_from,
      budget_id: 0,
      real_memo_id: 0,
      fund_entity: 4,
    }

    await api.post('/api/transaksi/uang-muka', payload)
    toast.success('Transaksi uang muka berhasil disimpan')
    emit('saved')
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal menyimpan transaksi')
  } finally {
    loading.value = false
  }
}

// Load cash accounts on mount
onMounted(loadCashAccounts)
</script>

<template>
  <Modal :open="true" class="max-w-2xl" @close="emit('close')">
    <div class="flex items-center justify-between border-b border-border px-6 py-4">
      <h2 class="text-lg font-semibold">Input Penyerahan Uang Muka</h2>
      <button class="rounded p-1 hover:bg-muted transition-colors" @click="emit('close')">
        <X class="w-4 h-4" />
      </button>
    </div>

    <div class="space-y-4 px-6 py-5">
      <!-- Tanggal -->
      <div>
        <label class="block text-sm font-medium mb-1.5">Tanggal <span class="text-red-500">*</span></label>
        <DateField v-model="form.actual_date" />
      </div>

      <!-- Karyawan & Rekening (2 kolom) -->
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

      <!-- Nominal & Reference (2 kolom) -->
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

      <!-- Keterangan & Received From (2 kolom) -->
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
    </div>

    <!-- Footer -->
    <div class="flex items-center justify-end gap-3 border-t border-border px-6 py-3">
      <Button variant="outline" @click="emit('close')">Batal</Button>
      <Button :loading="loading" @click="submitForm">Simpan</Button>
    </div>
  </Modal>
</template>

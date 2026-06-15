<script setup lang="ts">
import { X } from 'lucide-vue-next'
import { ref, shallowRef, watch, onMounted } from 'vue'

import Modal from '@/components/ui/Modal.vue'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

interface EmployeeLookup {
  employee_id: number
  employee_name: string
  employee_number: string
}

interface OpenUangMuka {
  transactionid: number
  transactionno: string
  actualdate: string
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
      `/api/transaksi/uang-muka/lookup/employee?search=${encodeURIComponent(query.trim())}`
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
      `/api/transaksi/uang-muka-pengembalian/lookup/open-uang-muka?employee_id=${emp.employee_id}`
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
    const res = await api.get<{ rows: { cashaccountno: string; cashaccountname: string }[] }>(
      '/api/transaksi/uang-muka/lookup/cash-account'
    )
    cashAccountOptions.value = (res.rows ?? []).map(r => ({
      cash_account_no: r.cashaccountno,
      cash_account_name: r.cashaccountname,
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
      ref_transaction_no: ca.transactionno,
      ref_transaction_item_id: ca.transactionitemid,
      ref_amount: ca.amount,
      employee_id: emp.employee_id,
      employee_name: emp.employee_name,
      cash_account_no: selectedCashAccount.value!.cash_account_no,
      amount: amount.value,
      reference_no: referenceNo.value,
      description: description.value,
    }
    await api.post('/api/transaksi/uang-muka-pengembalian', payload)
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
      <h2 class="text-lg font-semibold">Input Pengembalian / LPJ Uang Muka</h2>
      <button class="rounded p-1 hover:bg-muted transition-colors" @click="emit('close')">
        <X class="w-4 h-4" />
      </button>
    </div>

    <div class="space-y-4 px-6 py-5">
      <!-- Tanggal -->
      <div>
        <label class="block text-sm font-medium mb-1.5">Tanggal <span class="text-red-500">*</span></label>
        <DateField v-model="actualDate" />
      </div>

      <!-- Karyawan -->
      <div>
        <label class="block text-sm font-medium mb-1.5">Karyawan <span class="text-red-500">*</span></label>
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
        <label class="block text-sm font-medium mb-1.5">Uang Muka Yang Di-LPJ <span class="text-red-500">*</span></label>
        <SearchSelect
          :model-value="selectedOpenCA"
          :options="openCAOptions"
          :loading="loadingCA"
          :disabled="!selectedEmployee"
          placeholder="Pilih transaksi uang muka..."
          option-label="transactionno"
          @update:model-value="(v) => (selectedOpenCA = v)"
        />
        <!-- Ref detail (readonly) -->
        <div v-if="selectedOpenCA" class="mt-2 rounded bg-muted/50 border border-border px-3 py-2 text-xs space-y-1">
          <div class="flex gap-4">
            <span class="text-muted-foreground">Tanggal CA:</span>
            <span>{{ dmy(selectedOpenCA.actualdate) }}</span>
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
          <label class="block text-sm font-medium mb-1.5">Nominal Pengembalian <span class="text-red-500">*</span></label>
          <AmountInput v-model="amount" placeholder="Masukkan nominal..." />
          <p v-if="selectedOpenCA && amount !== selectedOpenCA.amount" class="mt-1 text-[10px] text-amber-600">
            Partial LPJ — berbeda dari nominal CA
          </p>
        </div>
        <div>
          <label class="block text-sm font-medium mb-1.5">Rekening Kas <span class="text-red-500">*</span></label>
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
          <label class="block text-sm font-medium mb-1.5">No. Referensi</label>
          <Input v-model="referenceNo" placeholder="No. kwitansi / bukti setor..." />
        </div>
        <div>
          <label class="block text-sm font-medium mb-1.5">Keterangan</label>
          <Input v-model="description" placeholder="Deskripsi singkat..." />
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

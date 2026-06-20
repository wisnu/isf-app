<script setup lang="ts">
import { Plus, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import DateField from '@/components/ui/DateField.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import StatusBadge from '@/components/authorization/StatusBadge.vue'
import AppTable from '@/components/ui/AppTable.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'
import type { MenuKey } from '@/lib/menu/registry'

// ── Types ─────────────────────────────────────────────────────────────────────
interface UangMukaRow {
  transaction_id: number
  transaction_no: string | null
  actual_date: string       // ISO YYYY-MM-DD
  employee_name: string
  employee_id: number
  amount: number
  auth_status: string        // 'T'=Authorized, 'F'=Pending
  branch_code: string
  inputer: string
  description: string | null
}

interface EmployeeLookup {
  employee_id: number
  employee_name: string
  employee_number: string
}

interface ListResponse {
  rows: UangMukaRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

// ── State ─────────────────────────────────────────────────────────────────────
const auth = useAuthStore()
const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const rows = ref<UangMukaRow[]>([])
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
const selectedEmployee = ref<EmployeeLookup | null>(null)
const employeeSearchInput = ref('')
const employeeOptions = ref<EmployeeLookup[]>([])

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

// ── Employee lookup ───────────────────────────────────────────────────────────
async function searchEmployees(query: string) {
  if (!query.trim()) {
    employeeOptions.value = []
    return
  }
  try {
    const res = await api.get<{ rows: EmployeeLookup[] }>(
      `/api/transaction/cash-advance/lookup/employee?search=${encodeURIComponent(query.trim())}`
    )
    employeeOptions.value = res.rows ?? []
  } catch (e) {
    employeeOptions.value = []
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
    if (selectedEmployee.value) params.set('employee_id', String(selectedEmployee.value.employee_id))

    const res = await api.get<ListResponse>(`/api/transaction/cash-advance?${params}`)
    rows.value = res.rows ?? []
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : 'Gagal memuat data'
    toast.error('Gagal memuat data uang muka')
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="space-y-0">
    <PageHeader title="Penyerahan Uang Muka" subtitle="Daftar transaksi penyerahan uang muka kepada karyawan">
      <template #actions>
        <Button v-if="auth.hasMenu('finance.transactions.cash_advance' as MenuKey)" size="sm" class="gap-1.5 h-8 text-xs" @click="router.push({ name: 'finance-transactions-cash-advance-create' })">
          <Plus class="w-3.5 h-3.5" />
          Input Baru
        </Button>
      </template>
    </PageHeader>

    <Alert v-if="errorMsg" variant="destructive" class="mb-3">{{ errorMsg }}</Alert>

    <!-- Toolbar -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Dari</label>
        <DateField v-model="dateFrom" />
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai</label>
        <DateField v-model="dateTo" />
      </div>
      <div class="flex-1 min-w-[200px]">
        <label class="mb-1 block text-xs font-medium text-zinc-500">Karyawan</label>
        <SearchSelect
          :model-value="selectedEmployee"
          :options="employeeOptions"
          :loading="false"
          placeholder="Ketik nama atau nomor karyawan..."
          option-label="employee_name"
          option-value="employee_id"
          @update:model-value="(v) => (selectedEmployee = v)"
          @search="searchEmployees"
        />
      </div>
      <Button size="sm" class="gap-1.5 h-8 text-xs" :disabled="loading" @click="() => { page = 1; load() }">
        <Search class="w-3.5 h-3.5" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
    </div>

    <!-- Paginator TOP -->
    <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
      <span class="text-xs text-zinc-500">
        {{ hasLoaded ? showCount : 'Pilih tanggal dan klik Tampilkan' }}
      </span>
      <TablePagination
        v-if="hasLoaded && totalPages > 1"
        :page="page"
        :total-pages="totalPages"
        :total="totalRec"
        :page-size="pageSize"
        @goto="goto"
      />
    </div>

    <!-- DataTable -->
    <AppTable class="rounded-b border">
      <template #head>
        <tr>
          <th class="px-4 py-3 text-left">No. Transaksi</th>
          <th class="px-4 py-3 text-left">Tanggal</th>
          <th class="px-4 py-3 text-left">Karyawan</th>
          <th class="px-4 py-3 text-right">Nominal</th>
          <th class="px-4 py-3 text-center">Status</th>
          <th class="px-4 py-3 text-left">Input Oleh</th>
        </tr>
      </template>
      <tr v-if="!hasLoaded">
        <td colspan="6" class="px-4 py-8 text-center text-zinc-400">
          Pilih tanggal dan klik Tampilkan untuk melihat data.
        </td>
      </tr>
      <tr v-else-if="loading">
        <td colspan="6" class="px-4 py-8 text-center text-zinc-400">Memuat...</td>
      </tr>
      <tr v-else-if="!rows.length">
        <td colspan="6" class="px-4 py-8 text-center text-zinc-400">
          Tidak ada transaksi dalam periode ini.
        </td>
      </tr>
      <tr
        v-for="row in rows"
        :key="row.transaction_id"
        class="border-b border-border hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
      >
        <td class="px-4 py-3 font-mono">{{ row.transaction_no ?? '-' }}</td>
        <td class="px-4 py-3">{{ dmy(row.actual_date) }}</td>
        <td class="px-4 py-3">{{ row.employee_name }}</td>
        <td class="px-4 py-3 text-right">{{ fmt(row.amount) }}</td>
        <td class="px-4 py-3 text-center">
          <StatusBadge :status="row.auth_status === 'T' ? 'AUTHORIZED' : 'PENDING'" />
        </td>
        <td class="px-4 py-3">{{ row.inputer }}</td>
      </tr>
    </AppTable>

  </div>
</template>

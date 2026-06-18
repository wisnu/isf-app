<script setup lang="ts">
import { Plus, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import DateField from '@/components/ui/DateField.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'
import type { MenuKey } from '@/lib/menu/registry'
import UangMukaPengembalianFormModal from '@/components/modals/UangMukaPengembalianFormModal.vue'

interface PengembalianRow {
  transaction_id: number
  transaction_no: string | null
  actualdate: string
  employee_name: string
  employee_id: number
  amount: number
  authstatus: string
  branch_code: string
  inputer: string
  description: string | null
  reference_no: string | null
}

interface EmployeeLookup {
  employee_id: number
  employee_name: string
  employee_number: string
}

interface ListResponse {
  rows: PengembalianRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const auth = useAuthStore()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const rows = ref<PengembalianRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)

const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)
const selectedEmployee = ref<EmployeeLookup | null>(null)
const employeeOptions = ref<EmployeeLookup[]>([])

const showForm = shallowRef(false)

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

async function searchEmployees(query: string) {
  if (!query.trim()) { employeeOptions.value = []; return }
  try {
    const res = await api.get<{ rows: EmployeeLookup[] }>(
      `/api/transaksi/uang-muka/lookup/employee?search=${encodeURIComponent(query.trim())}`
    )
    employeeOptions.value = res.rows ?? []
  } catch { employeeOptions.value = [] }
}

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
    const res = await api.get<ListResponse>(`/api/transaksi/uang-muka-pengembalian?${params}`)
    rows.value = res.rows ?? []
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : 'Gagal memuat data'
    toast.error('Gagal memuat data pengembalian uang muka')
  } finally {
    loading.value = false
  }
}

function onSaved() {
  showForm.value = false
  load()
}

onMounted(load)
</script>

<template>
  <div class="space-y-0">
    <PageHeader
      title="Pengembalian Uang Muka"
      subtitle="Daftar transaksi pengembalian (LPJ) uang muka karyawan"
    >
      <template #actions>
        <Button
          v-if="auth.hasMenu('keuangan.transaksi.uang-muka-pengembalian' as MenuKey)"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="showForm = true"
        >
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
    <div class="overflow-x-auto rounded-b border">
      <table class="w-full text-[11px]">
        <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
          <tr>
            <th class="px-4 py-2 text-left font-medium">No. Transaksi</th>
            <th class="px-4 py-2 text-left font-medium">Tanggal</th>
            <th class="px-4 py-2 text-left font-medium">Karyawan</th>
            <th class="px-4 py-2 text-right font-medium">Nominal</th>
            <th class="px-4 py-2 text-center font-medium">Status</th>
            <th class="px-4 py-2 text-left font-medium">Input Oleh</th>
          </tr>
        </thead>
        <tbody>
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
              Tidak ada transaksi pengembalian dalam periode ini.
            </td>
          </tr>
          <tr
            v-for="row in rows"
            :key="row.transaction_id"
            class="border-b border-border hover:bg-zinc-50 dark:hover:bg-zinc-800/50 transition-colors"
          >
            <td class="px-4 py-2 font-mono">{{ row.transaction_no ?? '-' }}</td>
            <td class="px-4 py-2">{{ dmy(row.actualdate) }}</td>
            <td class="px-4 py-2">{{ row.employee_name }}</td>
            <td class="px-4 py-2 text-right">{{ fmt(row.amount) }}</td>
            <td class="px-4 py-2 text-center">
              <StatusBadge :status="row.authstatus === 'T' ? 'AUTHORIZED' : 'PENDING'" />
            </td>
            <td class="px-4 py-2">{{ row.inputer }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <UangMukaPengembalianFormModal
      v-if="showForm"
      @close="showForm = false"
      @saved="onSaved"
    />
  </div>
</template>

<script setup lang="ts">
import { HandCoins, Plus, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import DateField from '@/components/ui/DateField.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'
import type { MenuKey } from '@/lib/menu/registry'
import UangMukaFormModal from '@/components/modals/UangMukaFormModal.vue'

// ── Types ─────────────────────────────────────────────────────────────────────
interface UangMukaRow {
  transaction_id: number
  transaction_no: string | null
  actual_date: string       // ISO YYYY-MM-DD
  employee_name: string
  employee_id: number
  amount: number
  authstatus: string        // 'T'=Authorized, 'F'=Pending
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

// Modal state
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

    const res = await api.get<ListResponse>(`/api/transaksi/uang-muka?${params}`)
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

// ── Auth status badge ─────────────────────────────────────────────────────────
function authLabel(status: string) {
  return status === 'T' ? 'Disetujui' : 'Menunggu'
}

function authClass(status: string) {
  if (status === 'T') return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-200'
  return 'bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-200'
}

// ── Modal handlers ────────────────────────────────────────────────────────────
function openAdd() {
  showForm.value = true
}

function onSaved() {
  showForm.value = false
  load()
}

onMounted(load)
</script>

<template>
  <div class="space-y-0">
    <PageHeader title="Penyerahan Uang Muka" subtitle="Daftar transaksi penyerahan uang muka kepada karyawan">
      <template #actions>
        <Button v-if="auth.hasMenu('keuangan.transaksi.uang-muka-penyerahan' as MenuKey)" size="sm" class="gap-1.5 h-8 text-xs" @click="openAdd">
          <Plus class="w-3.5 h-3.5" />
          Input Baru
        </Button>
      </template>
    </PageHeader>

    <!-- Error message -->
    <div v-if="errorMsg" class="mx-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar -->
      <div class="px-4 py-3 border-b border-border space-y-3">
        <div class="flex flex-wrap items-end gap-3">
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Dari Tanggal</label>
            <DateField v-model="dateFrom" />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Sampai Tanggal</label>
            <DateField v-model="dateTo" />
          </div>
          <div class="flex-1 min-w-[200px]">
            <label class="mb-1 block text-xs font-medium text-muted-foreground">Cari Karyawan</label>
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
          <Button variant="secondary" :disabled="loading" @click="() => { page = 1; load() }">
            <Search class="mr-2 h-4 w-4" />
            {{ loading ? 'Memuat...' : 'Tampilkan' }}
          </Button>
        </div>
      </div>

      <!-- Pagination (SELALU di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-xs text-muted-foreground tabular-nums">
          {{ showCount }}
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

      <!-- Tabel -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted-foreground uppercase tracking-widest border-b border-border bg-muted/50">
            <tr>
              <th class="px-4 py-2 text-left font-medium">No. Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">Tanggal</th>
              <th class="px-4 py-2 text-left font-medium">Karyawan</th>
              <th class="px-4 py-2 text-right font-medium">Nominal</th>
              <th class="px-4 py-2 text-center font-medium">Status</th>
              <th class="px-4 py-2 text-left font-medium">Input Oleh</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length && !hasLoaded">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Pilih periode dan klik Tampilkan untuk melihat data.
              </td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada transaksi dalam periode ini.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.transaction_id"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-2 text-xs font-mono">{{ row.transaction_no ?? '-' }}</td>
              <td class="px-4 py-2 text-xs">{{ dmy(row.actual_date) }}</td>
              <td class="px-4 py-2 text-xs">{{ row.employee_name }}</td>
              <td class="px-4 py-2 text-xs text-right font-tabular">{{ fmt(row.amount) }}</td>
              <td class="px-4 py-2 text-xs text-center">
                <span :class="['inline-block px-2 py-1 rounded text-[10px] font-semibold', authClass(row.authstatus)]">
                  {{ authLabel(row.authstatus) }}
                </span>
              </td>
              <td class="px-4 py-2 text-xs">{{ row.inputer }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Form Modal -->
    <UangMukaFormModal
      v-if="showForm"
      @close="showForm = false"
      @saved="onSaved"
    />
  </div>
</template>

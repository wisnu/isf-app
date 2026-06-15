<script setup lang="ts">
import { Download } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api, ApiError, blob } from '@/lib/api/client'
import { formatIdr } from '@/lib/format'
import { downloadBlob } from '@/lib/download'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BudgetOwner { owner_id: string; owner_name: string }
interface Period { period_id: number; period_name: string }
interface BudgetItem {
  budget_id: string
  budget_code: string
  budget_group: string
  budget_detail: string
  budget_amount: number
  realization_amount: number | null
}

interface BudgetInquiryResponse {
  rows: BudgetItem[]
  pagination: { page: number; page_size: number; total: number; total_pages: number }
  summary: {
    total_budget: number
    total_realization: number
    total_remaining: number
  }
}

interface SelectOption { value: string; label: string }

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()

const owners = ref<SelectOption[]>([])
const periods = ref<SelectOption[]>([])
const selectedOwner = ref('')
const selectedPeriod = ref('')
const ownersLoading = shallowRef(false)
const periodsLoading = shallowRef(false)

const rows = ref<BudgetItem[]>([])
const loading = shallowRef(false)
const exportLoading = shallowRef(false)
const hasData = shallowRef(false)

const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRecords = shallowRef(0)

const summary = ref({
  total_budget: 0,
  total_realization: 0,
  total_remaining: 0,
})

// ── Load lookups ──────────────────────────────────────────────────────────────

async function loadOwners() {
  ownersLoading.value = true
  try {
    const res = await api.get<{ data: BudgetOwner[] }>('/api/budget/owners')
    owners.value = (res.data ?? []).map((o) => ({
      value: o.owner_id,
      label: o.owner_name,
    }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat daftar pemilik')
  } finally {
    ownersLoading.value = false
  }
}

async function loadPeriods() {
  if (!selectedOwner.value) return
  periodsLoading.value = true
  try {
    const res = await api.get<{ data: Period[] }>(`/api/budget/periods/${selectedOwner.value}`)
    periods.value = (res.data ?? []).map((p) => ({
      value: String(p.period_id),
      label: p.period_name,
    }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat periode')
  } finally {
    periodsLoading.value = false
  }
}

// ── Load data ─────────────────────────────────────────────────────────────────

async function tampilkan() {
  if (!selectedOwner.value || !selectedPeriod.value) {
    toast.error('Pilih pemilik anggaran dan periode terlebih dahulu')
    return
  }

  loading.value = true
  try {
    const params = new URLSearchParams({
      owner_id: selectedOwner.value,
      period_id: selectedPeriod.value,
      page: String(page.value),
      limit: String(pageSize.value),
    })
    const res = await api.get<BudgetInquiryResponse>(`/api/budget/inquiry?${params}`)
    rows.value = res.rows
    totalRecords.value = res.pagination.total
    totalPages.value = res.pagination.total_pages || 1
    summary.value = res.summary
    hasData.value = true
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat inquiry anggaran')
    rows.value = []
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  if (!selectedOwner.value || !selectedPeriod.value) return

  exportLoading.value = true
  try {
    const params = new URLSearchParams({
      owner_id: selectedOwner.value,
      period_id: selectedPeriod.value,
    })
    const b = await blob(`/api/budget/inquiry/export?${params}`)
    downloadBlob(b, `inquiry-anggaran-${new Date().toISOString().split('T')[0]}.xlsx`)
    toast.success('File berhasil diunduh')
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal mengunduh file')
  } finally {
    exportLoading.value = false
  }
}

onMounted(loadOwners)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Inquiry Anggaran" subtitle="Laporan pertanyaan anggaran per pemilik dan periode" />

    <!-- Filter card -->
    <Card>
      <CardContent class="p-5">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 items-end">
          <div>
            <label class="mb-1.5 block text-sm font-medium">
              Pemilik Anggaran <span class="text-red-500">*</span>
            </label>
            <SearchSelect
              v-model="selectedOwner"
              :options="owners"
              :loading="ownersLoading"
              placeholder="Pilih pemilik..."
            />
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium">
              Periode <span class="text-red-500">*</span>
            </label>
            <SearchSelect
              v-model="selectedPeriod"
              :options="periods"
              :loading="periodsLoading"
              :disabled="!selectedOwner"
              placeholder="Pilih periode..."
            />
          </div>
        </div>

        <div class="flex justify-end gap-2 mt-4">
          <Button :loading="loading" @click="tampilkan">Tampilkan</Button>
          <Button
            variant="outline"
            :disabled="!hasData"
            :loading="exportLoading"
            @click="exportXlsx"
          >
            <Download class="w-3.5 h-3.5 mr-1" />
            Export Excel
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Empty state (sebelum klik Tampilkan) -->
    <div v-if="!hasData" class="flex items-center justify-center h-48 text-muted-foreground text-sm">
      Pilih pemilik anggaran dan periode, lalu klik "Tampilkan" untuk melihat laporan
    </div>

    <!-- Report section (setelah klik Tampilkan) -->
    <template v-else>
      <!-- Summary cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <Card>
          <CardContent class="p-4">
            <p class="text-xs uppercase tracking-wide text-muted">Total Anggaran</p>
            <p class="text-2xl font-bold tabular-nums text-primary mt-1">{{ formatIdr(summary.total_budget) }}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="p-4">
            <p class="text-xs uppercase tracking-wide text-muted">Total Realisasi</p>
            <p class="text-2xl font-bold tabular-nums text-accent mt-1">{{ formatIdr(summary.total_realization) }}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent class="p-4">
            <p class="text-xs uppercase tracking-wide text-muted">Sisa Anggaran</p>
            <p class="text-2xl font-bold tabular-nums" :class="summary.total_remaining >= 0 ? 'text-positive' : 'text-red-600'">
              {{ formatIdr(summary.total_remaining) }}
            </p>
          </CardContent>
        </Card>
      </div>

      <!-- Table card -->
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <!-- Pagination -->
        <div class="px-4 py-2 border-b border-border flex items-center justify-between">
          <span class="text-[11px] text-muted tabular-nums">
            <template v-if="loading">Memuat...</template>
            <template v-else-if="totalRecords > 0">
              {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRecords) }}
              dari {{ totalRecords }} anggaran
            </template>
            <template v-else>Tidak ada anggaran</template>
          </span>
          <TablePagination
            :page="page"
            :total-pages="totalPages"
            :total="totalRecords"
            :page-size="pageSize"
            :loading="loading"
            unit="anggaran"
            @prev="page > 1 && (page--, tampilkan())"
            @next="page < totalPages && (page++, tampilkan())"
            @update:page-size="(s) => { pageSize = s; page = 1; tampilkan() }"
          />
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-[11px]">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
              <tr>
                <th class="px-4 py-2 text-center font-medium w-12">No</th>
                <th class="px-4 py-2 text-left font-medium">Kode Budget</th>
                <th class="px-4 py-2 text-left font-medium">Kelompok Kegiatan</th>
                <th class="px-4 py-2 text-left font-medium">Rincian Kebutuhan</th>
                <th class="px-4 py-2 text-right font-medium">Anggaran</th>
                <th class="px-4 py-2 text-right font-medium">Realisasi</th>
                <th class="px-4 py-2 text-right font-medium">Sisa</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-if="loading">
                <td colspan="7" class="px-4 py-8 text-center text-muted">Memuat...</td>
              </tr>
              <tr v-else-if="rows.length === 0">
                <td colspan="7" class="px-4 py-8 text-center text-muted italic">
                  Tidak ada anggaran yang ditemukan.
                </td>
              </tr>
              <tr v-for="(row, idx) in rows" :key="row.budget_id" class="hover:bg-muted/30">
                <td class="px-4 py-1 text-center text-xs">
                  {{ (page - 1) * pageSize + idx + 1 }}
                </td>
                <td class="px-4 py-1 text-xs font-mono">{{ row.budget_code }}</td>
                <td class="px-4 py-1 text-xs">{{ row.budget_group }}</td>
                <td class="px-4 py-1 text-xs">{{ row.budget_detail }}</td>
                <td class="px-4 py-1 text-right text-xs font-medium">
                  {{ formatIdr(row.budget_amount) }}
                </td>
                <td class="px-4 py-1 text-right text-xs">
                  {{ row.realization_amount ? formatIdr(row.realization_amount) : '—' }}
                </td>
                <td class="px-4 py-1 text-right text-xs font-medium">
                  {{
                    formatIdr(row.budget_amount - (row.realization_amount ?? 0))
                  }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

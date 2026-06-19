<script setup lang="ts">
import { List, Pencil, Trash2, X } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import Modal from '@/components/ui/Modal.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'
import type { MenuKey } from '@/lib/menu/registry'

interface Batch {
  id: number
  batch_period_desc: string
  tanggal_transaksi: string
  namafile: string
  total_record: number
  grand_total: number
  status: 'DRAFT' | 'PENDING' | 'PROCESSING' | 'AUTHORIZED' | 'REJECTED'
  created_at: string
  created_by: string
}

interface ListResponse {
  rows: Batch[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

interface BatchDetail {
  id: number
  batch_period_desc: string
  tanggal_transaksi: string
  namafile: string
  total_record: number
  grand_total: number
  status: string
  created_at: string
  created_by: string
  items: Array<{
    data_no: number
    employee_number: string
    employee_name: string
    business_area_code: string
    gender: string
    zakat_amount: number
    infaq_amount: number
    anak_asuh_amount: number
    anak_yatim_amount: number
    taqurma_amount: number
    total_amount: number
  }>
}

const router = useRouter()
const toast = useToast()
const auth = useAuthStore()

const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const rows = ref<Batch[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const dateFrom = ref('')
const dateTo = ref('')
const batchPeriodSearch = ref('')

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function statusBadge(status: string) {
  const classes: Record<string, string> = {
    DRAFT: 'bg-zinc-100 text-zinc-700',
    PENDING: 'bg-yellow-100 text-yellow-800',
    PROCESSING: 'bg-blue-100 text-blue-800',
    AUTHORIZED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800',
  }
  const labels: Record<string, string> = {
    DRAFT: 'Draft',
    PENDING: 'Menunggu',
    PROCESSING: 'Diproses',
    AUTHORIZED: 'Terotorisasi',
    REJECTED: 'Ditolak',
  }
  return { className: classes[status] || 'bg-gray-100 text-gray-700', label: labels[status] || status }
}

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      limit: String(pageSize.value),
    })
    if (dateFrom.value) params.set('date_from', dateFrom.value)
    if (dateTo.value) params.set('date_to', dateTo.value)
    if (batchPeriodSearch.value.trim()) params.set('batch_period_desc', batchPeriodSearch.value.trim())

    const res = await api.get<ListResponse>(`/api/transaksi/upload/hc-zis/batches?${params}`)
    rows.value = res.rows
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
}

onMounted(loadData)

// Detail drawer
const showDetail = shallowRef(false)
const detailLoading = shallowRef(false)
const selectedBatch = ref<BatchDetail | null>(null)

async function openDetail(batch: Batch) {
  detailLoading.value = true
  try {
    const detail = await api.get<BatchDetail>(`/api/transaksi/upload/hc-zis/batches/${batch.id}`)
    selectedBatch.value = detail
    showDetail.value = true
  } catch (e) {
    toast.error('Gagal memuat detail batch')
  } finally {
    detailLoading.value = false
  }
}

// Update tanggal modal
const showUpdateDate = shallowRef(false)
const updateDateBatch = ref<Batch | null>(null)
const newDate = ref('')
const updateLoading = shallowRef(false)

function openUpdateDate(batch: Batch) {
  updateDateBatch.value = batch
  newDate.value = batch.tanggal_transaksi
  showUpdateDate.value = true
}

async function submitUpdateDate() {
  if (!updateDateBatch.value || !newDate.value) return
  updateLoading.value = true
  try {
    await api.put(
      `/api/transaksi/upload/hc-zis/batches/${updateDateBatch.value.id}/date`,
      { tanggal_transaksi: newDate.value },
    )
    toast.success('Tanggal berhasil diperbarui')
    showUpdateDate.value = false
    loadData()
  } catch (e) {
    toast.error('Gagal memperbarui tanggal')
  } finally {
    updateLoading.value = false
  }
}

// Delete modal
const showDelete = shallowRef(false)
const deleteBatch = ref<Batch | null>(null)
const deleteLoading = shallowRef(false)

function openDelete(batch: Batch) {
  deleteBatch.value = batch
  showDelete.value = true
}

async function submitDelete() {
  if (!deleteBatch.value) return
  deleteLoading.value = true
  try {
    await api.delete(`/api/transaksi/upload/hc-zis/batches/${deleteBatch.value.id}`)
    toast.success('Data berhasil dihapus')
    showDelete.value = false
    loadData()
  } catch (e) {
    toast.error('Gagal menghapus data')
  } finally {
    deleteLoading.value = false
  }
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex items-center gap-3">
      <List class="h-5 w-5 text-primary" />
      <h1 class="text-lg font-semibold">Daftar Upload ZIS Rutin</h1>
    </div>

    <!-- Error message -->
    <div v-if="errorMsg" class="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar / Filter -->
      <div class="px-4 py-3 border-b border-border flex flex-wrap items-end gap-3">
        <div class="flex items-end gap-2">
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-muted">Dari</label>
            <DateField v-model="dateFrom" />
          </div>
          <div class="flex flex-col gap-1">
            <label class="text-xs font-medium text-muted">Sampai</label>
            <DateField v-model="dateTo" />
          </div>
        </div>
        <div class="flex flex-col gap-1 flex-1 max-w-xs">
          <label class="text-xs font-medium text-muted">Periode</label>
          <input
            v-model="batchPeriodSearch"
            placeholder="Cari periode..."
            class="h-9 rounded-lg px-3 text-xs border border-border bg-background focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <Button size="sm" :disabled="loading" @click="() => { page = 1; loadData() }">
          Tampilkan
        </Button>
      </div>

      <!-- Pagination info (SELALU di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} data
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          v-if="totalPages > 1"
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @prev="page > 1 && (page--, loadData())"
          @next="page < totalPages && (page++, loadData())"
          @update:page-size="(s) => { pageSize = s; page = 1; loadData() }"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">Periode</th>
              <th class="px-4 py-2 text-left font-medium">Tgl Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">File</th>
              <th class="px-4 py-2 text-right font-medium">Record</th>
              <th class="px-4 py-2 text-right font-medium">Total (Rp)</th>
              <th class="px-4 py-2 text-center font-medium">Status</th>
              <th class="px-4 py-2 text-left font-medium w-32">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="7" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada data yang ditemukan.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.id"
              class="hover:bg-muted/30 transition-colors cursor-pointer"
              @click="openDetail(row)"
            >
              <td class="px-4 py-2 text-xs font-medium">{{ row.batch_period_desc }}</td>
              <td class="px-4 py-2 text-xs">{{ dmy(row.tanggal_transaksi) }}</td>
              <td class="px-4 py-2 text-xs text-muted-foreground max-w-xs truncate" :title="row.namafile">{{ row.namafile }}</td>
              <td class="px-4 py-2 text-xs text-right">{{ row.total_record }}</td>
              <td class="px-4 py-2 text-xs text-right font-medium">Rp {{ fmt(row.grand_total) }}</td>
              <td class="px-4 py-2 text-center">
                <span :class="['inline-block px-2 py-0.5 rounded-full text-[10px] font-semibold', statusBadge(row.status).className]">
                  {{ statusBadge(row.status).label }}
                </span>
              </td>
              <td class="px-4 py-2 text-right" @click.stop>
                <div class="flex items-center justify-end gap-1">
                  <button
                    v-if="auth.hasMenu('finance.upload.zis_routine' as MenuKey)"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Update Tanggal"
                    @click="openUpdateDate(row)"
                  >
                    <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                  </button>
                  <button
                    v-if="auth.hasMenu('finance.upload.zis_routine' as MenuKey)"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Hapus"
                    @click="openDelete(row)"
                  >
                    <Trash2 class="w-3.5 h-3.5 text-red-500" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Detail Drawer Modal -->
    <Modal
      v-if="showDetail && selectedBatch"
      :open="showDetail"
      title="Detail Batch Upload ZIS Rutin"
      class="max-w-4xl"
      @close="showDetail = false"
    >
      <div class="space-y-4">
        <!-- Info header -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <div class="text-xs text-muted">Periode</div>
            <div class="text-sm font-medium">{{ selectedBatch.batch_period_desc }}</div>
          </div>
          <div>
            <div class="text-xs text-muted">Tanggal Transaksi</div>
            <div class="text-sm font-medium">{{ dmy(selectedBatch.tanggal_transaksi) }}</div>
          </div>
          <div>
            <div class="text-xs text-muted">File</div>
            <div class="text-sm font-medium">{{ selectedBatch.namafile }}</div>
          </div>
          <div>
            <div class="text-xs text-muted">Status</div>
            <div class="text-sm font-medium">
              <span :class="['inline-block px-2 py-0.5 rounded-full text-[10px] font-semibold', statusBadge(selectedBatch.status).className]">
                {{ statusBadge(selectedBatch.status).label }}
              </span>
            </div>
          </div>
          <div>
            <div class="text-xs text-muted">Total Record</div>
            <div class="text-sm font-medium">{{ selectedBatch.total_record }}</div>
          </div>
          <div>
            <div class="text-xs text-muted">Grand Total</div>
            <div class="text-sm font-medium">Rp {{ fmt(selectedBatch.grand_total) }}</div>
          </div>
        </div>

        <!-- Items table -->
        <div class="space-y-2">
          <h3 class="text-sm font-semibold">Detail Item</h3>
          <div class="overflow-x-auto rounded border border-border">
            <table class="w-full text-[10px]">
              <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
                <tr>
                  <th class="px-2 py-1.5 text-left font-semibold">No</th>
                  <th class="px-2 py-1.5 text-left font-semibold">NIP</th>
                  <th class="px-2 py-1.5 text-left font-semibold">Nama</th>
                  <th class="px-2 py-1.5 text-left font-semibold">Divisi</th>
                  <th class="px-2 py-1.5 text-right font-semibold">Zakat</th>
                  <th class="px-2 py-1.5 text-right font-semibold">Infaq</th>
                  <th class="px-2 py-1.5 text-right font-semibold">A. Asuh</th>
                  <th class="px-2 py-1.5 text-right font-semibold">A. Yatim</th>
                  <th class="px-2 py-1.5 text-right font-semibold">Taqurma</th>
                  <th class="px-2 py-1.5 text-right font-semibold">Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in selectedBatch.items" :key="item.data_no" class="border-t border-border hover:bg-muted/20">
                  <td class="px-2 py-1 text-center">{{ item.data_no }}</td>
                  <td class="px-2 py-1 font-mono">{{ item.employee_number }}</td>
                  <td class="px-2 py-1">{{ item.employee_name }}</td>
                  <td class="px-2 py-1">{{ item.business_area_code }}</td>
                  <td class="px-2 py-1 text-right">{{ fmt(item.zakat_amount) }}</td>
                  <td class="px-2 py-1 text-right">{{ fmt(item.infaq_amount) }}</td>
                  <td class="px-2 py-1 text-right">{{ fmt(item.anak_asuh_amount) }}</td>
                  <td class="px-2 py-1 text-right">{{ fmt(item.anak_yatim_amount) }}</td>
                  <td class="px-2 py-1 text-right">{{ fmt(item.taqurma_amount) }}</td>
                  <td class="px-2 py-1 text-right font-medium">{{ fmt(item.total_amount) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </Modal>

    <!-- Update Tanggal Modal -->
    <Modal
      v-if="showUpdateDate && updateDateBatch"
      :open="showUpdateDate"
      title="Update Tanggal Transaksi"
      class="max-w-sm"
      @close="showUpdateDate = false"
    >
      <div class="space-y-4">
        <div>
          <div class="text-xs text-muted mb-1">Batch: {{ updateDateBatch.batch_period_desc }}</div>
          <div class="text-xs text-muted mb-2">File: {{ updateDateBatch.namafile }}</div>
          <label class="text-sm font-medium">Tanggal Transaksi Baru</label>
          <DateField v-model="newDate" class="mt-1" />
        </div>
        <div class="flex gap-2 justify-end">
          <Button variant="outline" size="sm" @click="showUpdateDate = false">
            Batal
          </Button>
          <Button size="sm" :loading="updateLoading" @click="submitUpdateDate">
            Simpan
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Delete Confirmation Modal -->
    <Modal
      v-if="showDelete && deleteBatch"
      :open="showDelete"
      title="Konfirmasi Hapus"
      class="max-w-sm"
      @close="showDelete = false"
    >
      <div class="space-y-4">
        <div class="text-sm text-muted">
          <p class="mb-2">Anda akan menghapus batch upload ZIS Rutin berikut:</p>
          <div class="space-y-1 text-xs">
            <div><span class="text-muted">Periode:</span> <span class="font-medium">{{ deleteBatch.batch_period_desc }}</span></div>
            <div><span class="text-muted">File:</span> <span class="font-medium">{{ deleteBatch.namafile }}</span></div>
            <div><span class="text-muted">Tanggal:</span> <span class="font-medium">{{ dmy(deleteBatch.tanggal_transaksi) }}</span></div>
            <div><span class="text-muted">Total:</span> <span class="font-medium">Rp {{ fmt(deleteBatch.grand_total) }}</span></div>
          </div>
        </div>
        <p class="text-sm font-medium text-red-600">Tindakan ini tidak dapat dibatalkan.</p>
        <div class="flex gap-2 justify-end">
          <Button variant="outline" size="sm" @click="showDelete = false">
            Batal
          </Button>
          <Button variant="destructive" size="sm" :loading="deleteLoading" @click="submitDelete">
            Hapus
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { Printer, Plus, Trash2, Search } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'
import { usePermission } from '@/shared/composables/usePermission'

interface BszRow {
  bsz_id: number
  bsz_number: string
  donor_id: number
  donor_name: string
  donor_no: string
  bsz_date: string
  period_begin: string
  period_end: string
  total: number
}

interface ListResponse {
  rows: BszRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

interface DonorOption {
  donor_id: number
  donor_no: string
  donor_name: string
}

const router = useRouter()
const toast = useToast()
const perm = usePermission('fundraising.donation.bsz')

const filters = reactive({
  donor_id: null as number | null,
  donor_text: '',
  begin_date: '',
  end_date: '',
})

const rows = ref<BszRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)

const donorOptions = ref<DonorOption[]>([])
const donorSearch = shallowRef('')

const deleteTarget = ref<BszRow | null>(null)
const deleteLoading = shallowRef(false)

const idr = new Intl.NumberFormat('id-ID')
const fmtRp = (n: number) => 'Rp ' + idr.format(n)

async function searchDonors() {
  if (donorSearch.value.length < 2) return
  donorOptions.value = await api.get<DonorOption[]>(`/api/fundraising/bsz/lookup/donor?q=${encodeURIComponent(donorSearch.value)}`).catch(() => [])
}

function selectDonor(d: DonorOption) {
  filters.donor_id = d.donor_id
  filters.donor_text = `${d.donor_no} — ${d.donor_name}`
  donorOptions.value = []
  donorSearch.value = ''
  page.value = 1
  loadData()
}

function clearDonor() {
  filters.donor_id = null
  filters.donor_text = ''
  page.value = 1
  loadData()
}

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), limit: '25' })
    if (filters.donor_id) params.set('donor_id', String(filters.donor_id))
    if (filters.begin_date) params.set('begin_date', filters.begin_date)
    if (filters.end_date) params.set('end_date', filters.end_date)

    const res = await api.get<ListResponse>(`/api/fundraising/bsz?${params}`)
    rows.value = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRec.value = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function prevPage() {
  if (page.value > 1) { page.value--; loadData() }
}
function nextPage() {
  if (page.value < totalPages.value) { page.value++; loadData() }
}
function goToPage(n: number) {
  page.value = n; loadData()
}

function goCreate() {
  router.push({ name: 'fundraising-bsz-create' })
}

function openPrint(row: BszRow) {
  router.push({ name: 'fundraising-bsz-print', params: { id: row.bsz_id } })
}

function openDelete(row: BszRow) {
  deleteTarget.value = row
}

async function confirmDelete() {
  if (!deleteTarget.value) return
  deleteLoading.value = true
  try {
    await api.delete(`/api/fundraising/bsz/${deleteTarget.value.bsz_id}`)
    toast.success('BSZ berhasil dihapus')
    deleteTarget.value = null
    loadData()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menghapus BSZ')
  } finally {
    deleteLoading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <div class="flex flex-col gap-4">
    <PageHeader title="Cetak Bukti Setor Zakat" subtitle="Daftar Bukti Setor Zakat (BSZ) per donatur">
      <template #actions>
        <Button v-if="perm.canAdd" variant="primary" @click="goCreate">
          <Plus class="w-4 h-4 mr-1" />
          Buat BSZ Baru
        </Button>
      </template>
    </PageHeader>

    <!-- Filter Bar -->
    <div class="flex flex-wrap gap-3 items-end rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <!-- Donor search -->
      <div class="flex-1 min-w-[240px]">
        <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Cari Donatur</label>
        <div class="relative">
          <div v-if="filters.donor_id" class="flex items-center gap-2 rounded border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm">
            <span class="flex-1 truncate">{{ filters.donor_text }}</span>
            <button class="text-slate-400 hover:text-red-500" @click="clearDonor">×</button>
          </div>
          <div v-else class="relative">
            <input
              v-model="donorSearch"
              placeholder="Ketik nama atau no. donatur..."
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-8"
              @input="searchDonors"
            />
            <Search class="absolute right-2 top-1.5 w-4 h-4 text-slate-400" />
            <!-- Dropdown -->
            <div v-if="donorOptions.length" class="absolute z-20 mt-1 w-full rounded border border-slate-200 bg-white shadow-lg max-h-48 overflow-y-auto">
              <button
                v-for="d in donorOptions"
                :key="d.donor_id"
                class="w-full text-left px-3 py-2 text-sm hover:bg-indigo-50"
                @click="selectDonor(d)"
              >
                <span class="font-medium">{{ d.donor_name }}</span>
                <span class="ml-2 text-xs text-slate-500">{{ d.donor_no }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Date range -->
      <div class="flex items-end gap-2">
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Dari</label>
          <DateField v-model="filters.begin_date" @update:modelValue="() => { page = 1; loadData() }" />
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Sampai</label>
          <DateField v-model="filters.end_date" @update:modelValue="() => { page = 1; loadData() }" />
        </div>
        <Button variant="secondary" @click="() => { page = 1; loadData() }">
          <Search class="w-4 h-4 mr-1" /> Cari
        </Button>
      </div>
    </div>

    <!-- Table container -->
    <div class="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
      <!-- Pagination top -->
      <div class="border-b border-slate-200 px-4 py-2">
        <TablePagination
          :current-page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :limit="25"
          @prev="prevPage"
          @next="nextPage"
          @go="goToPage"
        />
      </div>

      <!-- Error -->
      <div v-if="errorMsg" class="p-4 text-sm text-red-600 bg-red-50">{{ errorMsg }}</div>

      <!-- Loading -->
      <div v-else-if="loading" class="p-8 text-center text-sm text-slate-500">Memuat data...</div>

      <!-- Empty -->
      <div v-else-if="!rows.length" class="p-10 text-center text-slate-400">
        <Printer class="w-10 h-10 mx-auto mb-3 opacity-30" />
        <p class="text-sm">Belum ada data BSZ</p>
        <p class="text-xs mt-1">Gunakan filter donatur atau buat BSZ baru</p>
      </div>

      <!-- Table -->
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-50 text-xs font-semibold text-slate-500 uppercase tracking-wide">
            <tr>
              <th class="px-4 py-3 text-left">No. BSZ</th>
              <th class="px-4 py-3 text-left">Donatur</th>
              <th class="px-4 py-3 text-left">Tgl. BSZ</th>
              <th class="px-4 py-3 text-left">Periode</th>
              <th class="px-4 py-3 text-right">Total</th>
              <th class="px-4 py-3 text-center">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            <tr v-for="row in rows" :key="row.bsz_id" class="hover:bg-slate-50">
              <td class="px-4 py-3 font-mono text-xs font-medium text-indigo-700">
                {{ row.bsz_number }}
              </td>
              <td class="px-4 py-3">
                <p class="font-semibold">{{ row.donor_name }}</p>
                <p v-if="row.donor_no" class="text-xs text-slate-500">{{ row.donor_no }}</p>
              </td>
              <td class="px-4 py-3 text-slate-700">{{ dmy(row.bsz_date) }}</td>
              <td class="px-4 py-3 text-slate-600 text-xs">
                {{ dmy(row.period_begin) }} s/d {{ dmy(row.period_end) }}
              </td>
              <td class="px-4 py-3 text-right font-semibold tabular-nums">{{ fmtRp(row.total) }}</td>
              <td class="px-4 py-3">
                <div class="flex items-center justify-center gap-2">
                  <button
                    class="rounded p-1.5 text-indigo-600 hover:bg-indigo-50"
                    title="Cetak BSZ"
                    @click="openPrint(row)"
                  >
                    <Printer class="w-4 h-4" />
                  </button>
                  <button
                    v-if="perm.canDelete"
                    class="rounded p-1.5 text-red-500 hover:bg-red-50"
                    title="Hapus BSZ"
                    @click="openDelete(row)"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Delete confirmation modal -->
    <Modal v-if="deleteTarget" title="Hapus BSZ" @close="deleteTarget = null">
      <div class="space-y-3">
        <p class="text-sm text-slate-700">Anda yakin akan menghapus BSZ berikut?</p>
        <div class="rounded-lg bg-slate-50 p-3 space-y-1 text-sm">
          <div class="flex justify-between">
            <span class="text-slate-500">No. BSZ</span>
            <span class="font-mono font-semibold text-indigo-700">{{ deleteTarget.bsz_number }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">Donatur</span>
            <span class="font-semibold">{{ deleteTarget.donor_name }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">Tanggal</span>
            <span>{{ dmy(deleteTarget.bsz_date) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-slate-500">Total</span>
            <span class="font-semibold">{{ fmtRp(deleteTarget.total) }}</span>
          </div>
        </div>
        <p class="text-xs text-amber-600">Transaksi yang terhubung akan dilepas dan bisa digunakan kembali.</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="secondary" @click="deleteTarget = null">Batal</Button>
          <Button variant="danger" :loading="deleteLoading" @click="confirmDelete">Hapus</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

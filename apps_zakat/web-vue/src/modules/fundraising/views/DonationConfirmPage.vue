<script setup lang="ts">
import { Pencil, Search, Trash2, FileText, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'
import { usePermission } from '@/shared/composables/usePermission'
import { useAuthStore } from '@/app/stores/auth.store'

interface DonationTransaction {
  transaction_id: number
  transaction_no: string
  actual_date: string
  donor_no: string | null
  donor_name: string | null
  amount: number
  description: string | null
  branch_code: string
  branch_name: string | null
  channel_name: string | null
  channel_code: string | null
  product_name: string | null
  auth_status: string
  is_posted: string
  transaction_item_id: number
}

interface ListResponse {
  rows: DonationTransaction[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

const toast = useToast()
const auth = useAuthStore()
const perm = usePermission('fundraising.donation.confirm')

// ── Filter state ──────────────────────────────────────────────────────────
const filters = reactive({
  begin_date: '',
  end_date: '',
  branch_code: auth.user?.primary_branch || '',
  is_all_branch: false,
  search_category: '0',
  search_text: '',
  amount_from: '',
  amount_to: '',
  description: '',
  limit: 25,
})

// ── Data & pagination ────────────────────────────────────────────────────
const rows = ref<DonationTransaction[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoadedOnce = shallowRef(false)

// Watch filter changes — reset to page 1
watch(
  () => ({ ...filters }),
  () => {
    page.value = 1
    loadData()
  },
  { deep: true },
)

async function loadData() {
  if (!hasLoadedOnce.value && !isBranchAccessAllowed()) {
    return
  }

  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      limit: String(filters.limit),
    })

    if (filters.begin_date) params.set('begin_date', filters.begin_date)
    if (filters.end_date) params.set('end_date', filters.end_date)
    if (filters.branch_code) params.set('branch_code', filters.branch_code)
    if (filters.is_all_branch) params.set('is_all_branch', '1')
    if (filters.search_category) params.set('search_category', filters.search_category)
    if (filters.search_text) params.set('search_text', filters.search_text.trim())
    if (filters.amount_from) params.set('amount_from', filters.amount_from)
    if (filters.amount_to) params.set('amount_to', filters.amount_to)
    if (filters.description) params.set('description', filters.description.trim())

    const res = await api.get<ListResponse>(`/api/fundraising/donation-confirm?${params}`)
    rows.value = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRec.value = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    rows.value = []
  } finally {
    loading.value = false
    hasLoadedOnce.value = true
  }
}

function isBranchAccessAllowed(): boolean {
  return !!(filters.begin_date || filters.end_date || filters.search_text)
}

function prevPage() {
  if (page.value > 1) {
    page.value--
    loadData()
  }
}

function nextPage() {
  if (page.value < totalPages.value) {
    page.value++
    loadData()
  }
}

function changePageSize(s: number) {
  filters.limit = s
  page.value = 1
  loadData()
}

function formatAmount(amount: number): string {
  return new Intl.NumberFormat('id-ID').format(amount)
}

// ── Delete Modal ──────────────────────────────────────────────────────────
const showDeleteModal = shallowRef(false)
const deleteLoading = shallowRef(false)
const deleteError = shallowRef<string | null>(null)
const selectedRow = ref<DonationTransaction | null>(null)

function openDelete(row: DonationTransaction) {
  selectedRow.value = row
  deleteError.value = null
  showDeleteModal.value = true
}

function closeDelete() {
  showDeleteModal.value = false
  selectedRow.value = null
}

async function confirmDelete() {
  if (!selectedRow.value) return
  deleteLoading.value = true
  deleteError.value = null
  try {
    await api.delete(`/api/fundraising/donation-confirm/${selectedRow.value.transaction_id}`)
    toast.success('Transaksi berhasil dihapus.')
    closeDelete()
    loadData()
  } catch (e) {
    deleteError.value = e instanceof ApiError ? e.message : 'Gagal menghapus transaksi.'
  } finally {
    deleteLoading.value = false
  }
}

// ── Post Journal Modal ────────────────────────────────────────────────────
const showPostModal = shallowRef(false)
const postLoading = shallowRef(false)
const postError = shallowRef<string | null>(null)
const selectedPostRow = ref<DonationTransaction | null>(null)

function openPostJournal(row: DonationTransaction) {
  selectedPostRow.value = row
  postError.value = null
  showPostModal.value = true
}

function closePostModal() {
  showPostModal.value = false
  selectedPostRow.value = null
}

async function confirmPostJournal() {
  if (!selectedPostRow.value) return
  postLoading.value = true
  postError.value = null
  try {
    await api.post(`/api/fundraising/donation-confirm/${selectedPostRow.value.transaction_id}/post-journal`, {})
    toast.success('Jurnal berhasil diposting.')
    closePostModal()
    loadData()
  } catch (e) {
    postError.value = e instanceof ApiError ? e.message : 'Gagal memposting jurnal.'
  } finally {
    postLoading.value = false
  }
}

// ── Receipt Download ─────────────────────────────────────────────────────
async function downloadReceipt(row: DonationTransaction) {
  try {
    const blob = await api.blob(`/api/fundraising/donation-confirm/${row.transaction_id}/receipt`)
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `Kwitansi_${row.transaction_no}.pdf`
    a.click()
    window.URL.revokeObjectURL(url)
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal mengunduh kwitansi.')
  }
}

// ── Edit Donor Modal ──────────────────────────────────────────────────────
const showEditDonorModal = shallowRef(false)
const editDonorLoading = shallowRef(false)
const editDonorError = shallowRef<string | null>(null)
const selectedEditRow = ref<DonationTransaction | null>(null)
const editDonorForm = reactive({ donor_id: '', donor_name: '' })

function openEditDonor(row: DonationTransaction) {
  selectedEditRow.value = row
  editDonorForm.donor_id = row.donor_no || ''
  editDonorForm.donor_name = row.donor_name || ''
  editDonorError.value = null
  showEditDonorModal.value = true
}

function closeEditDonorModal() {
  showEditDonorModal.value = false
  selectedEditRow.value = null
}

async function confirmEditDonor() {
  if (!selectedEditRow.value) return
  editDonorLoading.value = true
  editDonorError.value = null
  try {
    await api.put(
      `/api/fundraising/donation-confirm/${selectedEditRow.value.transaction_id}/donor`,
      {
        donor_id: editDonorForm.donor_id || null,
        donor_name: editDonorForm.donor_name || null,
      },
    )
    toast.success('Donatur berhasil diubah.')
    closeEditDonorModal()
    loadData()
  } catch (e) {
    editDonorError.value = e instanceof ApiError ? e.message : 'Gagal mengubah donatur.'
  } finally {
    editDonorLoading.value = false
  }
}

onMounted(() => {
  // Set branch code if single-access
  if (auth.user?.branch_access === 'single' && auth.user?.primary_branch) {
    filters.branch_code = auth.user.primary_branch
  }
})
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Konfirmasi Transaksi Donasi" subtitle="Verifikasi dan posting transaksi donasi" />

    <!-- Error Alert -->
    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Filter Panel -->
    <div class="rounded-xl border border-border bg-surface p-4 space-y-4">
      <!-- Row 1: Date Range + Branch -->
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Tanggal Mulai</label>
          <DateField v-model="filters.begin_date" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Tanggal Akhir</label>
          <DateField v-model="filters.end_date" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Cabang</label>
          <select
            v-model="filters.branch_code"
            :disabled="auth.user?.branch_access === 'single'"
            class="h-9 rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <option value="">Pilih Cabang</option>
            <option v-for="b in auth.user?.branches" :key="b" :value="b">
              {{ b }}
            </option>
          </select>
        </div>
        <div v-if="auth.user?.branch_access === 'all'" class="flex items-end">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              v-model="filters.is_all_branch"
              type="checkbox"
              class="w-4 h-4 border border-border rounded focus:ring-1 focus:ring-ring"
            />
            <span class="text-xs font-medium">Seluruh Cabang</span>
          </label>
        </div>
      </div>

      <!-- Row 2: Search + Category -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Kategori Pencarian</label>
          <select
            v-model="filters.search_category"
            class="h-9 rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option value="0">Semua</option>
            <option value="1">Donatur ID</option>
            <option value="2">Donatur Nama</option>
          </select>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Pencarian Teks</label>
          <div class="relative">
            <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
            <input
              v-model="filters.search_text"
              type="text"
              placeholder="Cari..."
              class="h-9 w-full rounded-lg border border-border bg-background pl-8 pr-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
            />
            <button
              v-if="filters.search_text"
              class="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              @click="filters.search_text = ''"
            >
              <X class="w-3 h-3" />
            </button>
          </div>
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Keterangan</label>
          <input
            v-model="filters.description"
            type="text"
            placeholder="Cari keterangan..."
            class="h-9 rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
      </div>

      <!-- Row 3: Amount Range + Limit + Show Button -->
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-3 items-end">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Nominal Dari</label>
          <input
            v-model="filters.amount_from"
            type="number"
            placeholder="0"
            class="h-9 rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Nominal Sampai</label>
          <input
            v-model="filters.amount_to"
            type="number"
            placeholder="0"
            class="h-9 rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Limit</label>
          <select
            v-model.number="filters.limit"
            class="h-9 rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          >
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
        </div>
        <div colspan="2" class="col-span-2">
          <Button :loading="loading" @click="loadData" class="w-full">
            Tampilkan
          </Button>
        </div>
      </div>
    </div>

    <!-- Empty State (before load) -->
    <div v-if="!hasLoadedOnce" class="rounded-xl border border-border bg-surface px-4 py-12 text-center">
      <p class="text-muted-foreground text-sm">
        Pilih periode tanggal dan klik "Tampilkan" untuk melihat data transaksi donasi
      </p>
    </div>

    <!-- Table (after load) -->
    <div v-else class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Pagination Top -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * filters.limit + 1 }}–{{ Math.min(page * filters.limit, totalRec) }} dari
            {{ totalRec }} transaksi
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="filters.limit"
          @prev="prevPage"
          @next="nextPage"
          @update:page-size="changePageSize"
        />
      </div>

      <!-- Table Content -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-muted/30">
            <tr>
              <th class="px-4 py-2 text-left font-medium">No Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">Tgl Transaksi</th>
              <th class="px-4 py-2 text-left font-medium">Donatur</th>
              <th class="px-4 py-2 text-left font-medium">Kas/Bank</th>
              <th class="px-4 py-2 text-left font-medium">Produk</th>
              <th class="px-4 py-2 text-right font-medium">Nominal</th>
              <th class="px-4 py-2 text-center font-medium">Otorisasi</th>
              <th class="px-4 py-2 text-center font-medium">Posting</th>
              <th class="px-4 py-2 text-right font-medium w-32">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="9" class="px-4 py-8 text-center text-muted-foreground text-xs">
                Memuat...
              </td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="9" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada transaksi donasi.
              </td>
            </tr>
            <tr v-for="row in rows" :key="row.transaction_id" class="hover:bg-muted/30 transition-colors">
              <td class="px-4 py-1 text-xs font-mono text-muted-foreground">{{ row.transaction_no }}</td>
              <td class="px-4 py-1 text-xs">{{ dmy(row.actual_date) }}</td>
              <td class="px-4 py-1 text-xs">
                <div class="flex flex-col">
                  <span class="font-semibold">{{ row.donor_name || '—' }}</span>
                  <span v-if="row.donor_no" class="text-[10px] text-muted-foreground">{{ row.donor_no }}</span>
                </div>
              </td>
              <td class="px-4 py-1 text-xs">{{ row.channel_name || '—' }}</td>
              <td class="px-4 py-1 text-xs">{{ row.product_name || '—' }}</td>
              <td class="px-4 py-1 text-right text-xs font-mono">{{ formatAmount(row.amount) }}</td>
              <td class="px-4 py-1 text-center">
                <span
                  class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="
                    row.auth_status === 'T'
                      ? 'bg-emerald-100 text-emerald-700'
                      : 'bg-amber-100 text-amber-700'
                  "
                >
                  {{ row.auth_status === 'T' ? 'Terotorisasi' : 'Belum Otorisasi' }}
                </span>
              </td>
              <td class="px-4 py-1 text-center">
                <span
                  class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="row.is_posted === 'T' ? 'bg-emerald-100 text-emerald-700' : 'bg-blue-100 text-blue-700'"
                >
                  {{ row.is_posted === 'T' ? 'Terposting' : 'Belum Posting' }}
                </span>
              </td>
              <td class="px-4 py-1 text-right">
                <div class="flex items-center justify-end gap-0.5">
                  <button
                    v-if="perm.canDelete.value && (row.auth_status === 'F' || auth.user?.branch_access === 'all')"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Hapus"
                    @click="openDelete(row)"
                  >
                    <Trash2 class="w-3.5 h-3.5 text-red-500" />
                  </button>
                  <button
                    v-if="perm.canAdd.value && row.auth_status === 'T' && row.is_posted === 'F'"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Post Jurnal"
                    @click="openPostJournal(row)"
                  >
                    <FileText class="w-3.5 h-3.5 text-blue-500" />
                  </button>
                  <button
                    v-if="perm.canDetail.value && row.auth_status === 'T'"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Unduh Kwitansi"
                    @click="downloadReceipt(row)"
                  >
                    <FileText class="w-3.5 h-3.5 text-green-500" />
                  </button>
                  <button
                    v-if="perm.canEdit.value"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Edit Donatur"
                    @click="openEditDonor(row)"
                  >
                    <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Delete Modal -->
    <Modal v-if="showDeleteModal" max-width="max-w-sm" @close="closeDelete">
      <template #header>
        <h2 class="text-base font-semibold">Hapus Transaksi</h2>
      </template>
      <div class="space-y-3">
        <div v-if="deleteError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
          {{ deleteError }}
        </div>
        <div class="space-y-2 text-sm">
          <div class="border border-border rounded-lg bg-muted/30 px-4 py-3">
            <p class="text-xs font-semibold text-muted-foreground mb-1">No. Transaksi</p>
            <p class="font-mono">{{ selectedRow?.transaction_no }}</p>
          </div>
          <div class="border border-border rounded-lg bg-muted/30 px-4 py-3">
            <p class="text-xs font-semibold text-muted-foreground mb-1">Tanggal</p>
            <p>{{ dmy(selectedRow?.actual_date) }}</p>
          </div>
          <div class="border border-border rounded-lg bg-muted/30 px-4 py-3">
            <p class="text-xs font-semibold text-muted-foreground mb-1">Donatur</p>
            <p>{{ selectedRow?.donor_name || '—' }}</p>
          </div>
          <div class="border border-border rounded-lg bg-muted/30 px-4 py-3">
            <p class="text-xs font-semibold text-muted-foreground mb-1">Nominal</p>
            <p class="font-mono">{{ formatAmount(selectedRow?.amount || 0) }}</p>
          </div>
          <div class="border border-border rounded-lg bg-muted/30 px-4 py-3">
            <p class="text-xs font-semibold text-muted-foreground mb-1">Status</p>
            <span
              class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
              :class="
                selectedRow?.auth_status === 'T'
                  ? 'bg-emerald-100 text-emerald-700'
                  : 'bg-amber-100 text-amber-700'
              "
            >
              {{ selectedRow?.auth_status === 'T' ? 'Terotorisasi' : 'Belum Otorisasi' }}
            </span>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeDelete">Batal</Button>
          <Button variant="destructive" size="sm" :disabled="deleteLoading" @click="confirmDelete">
            {{ deleteLoading ? 'Menghapus...' : 'Hapus' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Post Journal Modal -->
    <Modal v-if="showPostModal" max-width="max-w-sm" @close="closePostModal">
      <template #header>
        <h2 class="text-base font-semibold">Post Jurnal Transaksi</h2>
      </template>
      <div class="space-y-3">
        <div v-if="postError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
          {{ postError }}
        </div>
        <div class="border border-border rounded-lg bg-muted/30 px-4 py-3 text-sm">
          <p class="font-semibold">{{ selectedPostRow?.donor_name || 'Donatur' }}</p>
          <p class="text-xs text-muted-foreground">No: {{ selectedPostRow?.transaction_no }}</p>
        </div>
        <p class="text-sm">
          Apakah Anda yakin ingin <strong>memposting jurnal</strong> transaksi ini ke buku besar?
        </p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closePostModal">Batal</Button>
          <Button size="sm" :disabled="postLoading" @click="confirmPostJournal">
            {{ postLoading ? 'Memproses...' : 'Post Jurnal' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Edit Donor Modal -->
    <Modal v-if="showEditDonorModal" max-width="max-w-sm" @close="closeEditDonorModal">
      <template #header>
        <h2 class="text-base font-semibold">Edit Donatur Transaksi</h2>
      </template>
      <div class="space-y-4">
        <div v-if="editDonorError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
          {{ editDonorError }}
        </div>
        <div class="space-y-2">
          <label class="text-xs font-medium">ID Donatur</label>
          <input
            v-model="editDonorForm.donor_id"
            type="text"
            class="h-9 w-full rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <div class="space-y-2">
          <label class="text-xs font-medium">Nama Donatur</label>
          <input
            v-model="editDonorForm.donor_name"
            type="text"
            class="h-9 w-full rounded-lg border border-border bg-background px-2.5 text-xs focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeEditDonorModal">Batal</Button>
          <Button size="sm" :disabled="editDonorLoading" @click="confirmEditDonor">
            {{ editDonorLoading ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

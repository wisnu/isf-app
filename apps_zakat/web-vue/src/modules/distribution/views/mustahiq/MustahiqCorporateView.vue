<script setup lang="ts">
import { CheckCircle2, Pencil, Plus, Search, Trash2, X, XCircle } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface MustahiqRow {
  mustahiq_id: number
  no_mustahiq: string | null
  name: string | null
  address: string | null
  phone_number: string | null
  status: string | null
}

interface BankAccountDetail {
  bank_account_id: number
  account_no: string | null
  account_name: string | null
  bank_code: string | null
  is_default: string | null
}

interface CorporateDetail {
  mustahiq_id: number
  no_mustahiq: string | null
  name: string
  address: string | null
  address_kelurahan: string | null
  address_kecamatan: string | null
  province_id: number | null
  postal_code: string | null
  reference_by: string | null
  phone_number: string | null
  cp_name: string | null
  cp_phone_number: string | null
  cp_mobile_number: string | null
  status: string | null
  bank_accounts: BankAccountDetail[]
}

interface Pagination { page: number; page_size: number; total: number; total_pages: number }
interface ListResponse { rows: MustahiqRow[]; pagination: Pagination }

// ── State ─────────────────────────────────────────────────────────────────────

const router = useRouter()
const toast  = useToast()

const rows       = ref<MustahiqRow[]>([])
const loading    = shallowRef(false)
const errorMsg   = shallowRef<string | null>(null)
const page       = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec   = shallowRef(0)
const pageSize   = shallowRef(25)
const searchInput = ref('')

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    const res = await api.get<ListResponse>(`/api/distribution/mustahiq/corporate?${params}`)
    rows.value       = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRec.value   = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function prevPage() { if (page.value > 1) { page.value--; loadData() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadData() } }
function changePageSize(s: number) { pageSize.value = s; page.value = 1; loadData() }

// ── Navigation ────────────────────────────────────────────────────────────────

function goCreate() { router.push({ name: 'distribution-mustahiq-corporate-create' }) }
function goEdit(row: MustahiqRow) {
  router.push({ name: 'distribution-mustahiq-corporate-edit', params: { id: row.mustahiq_id } })
}

// ── Modals ────────────────────────────────────────────────────────────────────

type ModalMode = 'detail' | 'delete' | 'status'

const modalMode    = shallowRef<ModalMode>('detail')
const modalOpen    = shallowRef(false)
const modalLoading = shallowRef(false)
const modalError   = shallowRef<string | null>(null)
const selectedRow  = ref<MustahiqRow | null>(null)
const detailData   = ref<CorporateDetail | null>(null)
const pendingStatus = shallowRef<'A' | 'N'>('A')

function closeModal() { modalOpen.value = false }

async function openDetail(row: MustahiqRow) {
  selectedRow.value  = row
  modalMode.value    = 'detail'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  try {
    detailData.value = await api.get<CorporateDetail>(`/api/distribution/mustahiq/corporate/${row.mustahiq_id}`)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

function openDelete(row: MustahiqRow) {
  selectedRow.value = row; modalMode.value = 'delete'; modalError.value = null; modalOpen.value = true
}

function openStatus(row: MustahiqRow, s: 'A' | 'N') {
  selectedRow.value = row; pendingStatus.value = s; modalMode.value = 'status'; modalError.value = null; modalOpen.value = true
}

async function confirmDelete() {
  if (!selectedRow.value) return
  modalLoading.value = true; modalError.value = null
  try {
    await api.delete(`/api/distribution/mustahiq/corporate/${selectedRow.value.mustahiq_id}`)
    toast.success('Mustahiq lembaga berhasil dihapus.')
    closeModal(); loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menghapus data.'
  } finally { modalLoading.value = false }
}

async function confirmStatus() {
  if (!selectedRow.value) return
  modalLoading.value = true; modalError.value = null
  try {
    await api.put(`/api/distribution/mustahiq/corporate/${selectedRow.value.mustahiq_id}/status`, { status: pendingStatus.value })
    toast.success(`Mustahiq berhasil ${pendingStatus.value === 'A' ? 'diaktifkan' : 'dinonaktifkan'}.`)
    closeModal(); loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal mengubah status.'
  } finally { modalLoading.value = false }
}

onMounted(loadData)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Mustahiq Lembaga" subtitle="Data penerima manfaat — organisasi / institusi">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="goCreate">
          <Plus class="w-3.5 h-3.5" /> Tambah
        </Button>
      </template>
    </PageHeader>

    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{{ errorMsg }}</div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <div class="px-4 py-2.5 border-b border-border flex items-center gap-3">
        <div class="relative flex-1 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input v-model="searchInput" type="text" placeholder="Cari nama / nomor / alamat..."
            class="w-full h-8 pl-8 pr-8 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <button v-if="searchInput" class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground" @click="searchInput = ''">
            <X class="w-3 h-3" />
          </button>
        </div>
      </div>

      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">{{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} mustahiq lembaga</template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @prev="prevPage" @next="nextPage" @update:page-size="changePageSize" />
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium w-32">No. Mustahiq</th>
              <th class="px-4 py-2 text-left font-medium">Nama Lembaga</th>
              <th class="px-4 py-2 text-left font-medium">Alamat</th>
              <th class="px-4 py-2 text-left font-medium w-36">Telepon</th>
              <th class="px-4 py-2 text-center font-medium w-24">Status</th>
              <th class="px-4 py-2 text-right font-medium w-40">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td></tr>
            <tr v-else-if="rows.length === 0"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">Belum ada data mustahiq lembaga.</td></tr>
            <tr v-for="row in rows" :key="row.mustahiq_id" class="hover:bg-background/60">
              <td class="px-4 py-2 font-mono text-xs text-muted-foreground">{{ row.no_mustahiq || '—' }}</td>
              <td class="px-4 py-2 font-medium">{{ row.name || '—' }}</td>
              <td class="px-4 py-2 text-xs text-muted-foreground truncate max-w-xs">{{ row.address || '—' }}</td>
              <td class="px-4 py-2 text-xs">{{ row.phone_number || '—' }}</td>
              <td class="px-4 py-2 text-center">
                <span class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="row.status === 'A' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400'">
                  {{ row.status === 'A' ? 'Aktif' : 'NonAktif' }}
                </span>
              </td>
              <td class="px-4 py-2">
                <div class="flex items-center justify-end gap-0.5">
                  <button class="px-1.5 py-1 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors text-[10px] font-medium" @click="openDetail(row)">Detail</button>
                  <button class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-blue-600 transition-colors" title="Ubah" @click="goEdit(row)"><Pencil class="w-3.5 h-3.5" /></button>
                  <button v-if="row.status === 'A'" class="p-1.5 rounded hover:bg-amber-50 text-muted-foreground hover:text-amber-600 transition-colors" title="NonAktifkan" @click="openStatus(row, 'N')"><XCircle class="w-3.5 h-3.5" /></button>
                  <button v-else class="p-1.5 rounded hover:bg-emerald-50 text-muted-foreground hover:text-emerald-600 transition-colors" title="Aktifkan" @click="openStatus(row, 'A')"><CheckCircle2 class="w-3.5 h-3.5" /></button>
                  <button class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600 transition-colors" title="Hapus" @click="openDelete(row)"><Trash2 class="w-3.5 h-3.5" /></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Detail Modal -->
    <Modal v-if="modalOpen && modalMode === 'detail'" max-width="max-w-2xl" @close="closeModal">
      <template #header><h2 class="text-base font-semibold">Detail Mustahiq Lembaga</h2></template>
      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat...</div>
      <div v-else-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
      <div v-else-if="detailData" class="space-y-4 text-sm">
        <div class="grid grid-cols-2 gap-x-6 gap-y-2.5">
          <div><p class="text-xs text-muted-foreground mb-0.5">No. Mustahiq</p><p class="font-mono">{{ detailData.no_mustahiq || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Status</p>
            <span class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold" :class="detailData.status === 'A' ? 'bg-emerald-100 text-emerald-700' : 'bg-zinc-100 text-zinc-500'">{{ detailData.status === 'A' ? 'Aktif' : 'NonAktif' }}</span>
          </div>
          <div class="col-span-2"><p class="text-xs text-muted-foreground mb-0.5">Nama Lembaga</p><p class="font-medium">{{ detailData.name }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Alamat</p><p>{{ detailData.address || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Kelurahan</p><p>{{ detailData.address_kelurahan || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Kecamatan</p><p>{{ detailData.address_kecamatan || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Kode Pos</p><p>{{ detailData.postal_code || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Telepon</p><p>{{ detailData.phone_number || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Referensi</p><p>{{ detailData.reference_by || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Kontak Person</p><p>{{ detailData.cp_name || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">Telp Kontak</p><p>{{ detailData.cp_phone_number || '—' }}</p></div>
          <div><p class="text-xs text-muted-foreground mb-0.5">HP Kontak</p><p>{{ detailData.cp_mobile_number || '—' }}</p></div>
        </div>
        <div>
          <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">Rekening Bank</p>
          <p v-if="detailData.bank_accounts.length === 0" class="text-xs text-muted-foreground italic">Tidak ada rekening terdaftar.</p>
          <table v-else class="w-full text-xs border border-border rounded overflow-hidden">
            <thead class="bg-muted/30"><tr>
              <th class="px-3 py-1.5 text-left font-medium">No. Rekening</th>
              <th class="px-3 py-1.5 text-left font-medium">Nama Rekening</th>
              <th class="px-3 py-1.5 text-left font-medium">Bank</th>
              <th class="px-3 py-1.5 text-center font-medium w-16">Default</th>
            </tr></thead>
            <tbody>
              <tr v-for="ba in detailData.bank_accounts" :key="ba.bank_account_id" class="border-t border-border">
                <td class="px-3 py-1.5">{{ ba.account_no || '—' }}</td>
                <td class="px-3 py-1.5">{{ ba.account_name || '—' }}</td>
                <td class="px-3 py-1.5">{{ ba.bank_code || '—' }}</td>
                <td class="px-3 py-1.5 text-center">{{ ba.is_default === 'T' ? '✓' : '' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="goEdit(selectedRow!); closeModal()">Ubah</Button>
          <Button variant="outline" size="sm" @click="closeModal">Tutup</Button>
        </div>
      </template>
    </Modal>

    <!-- Delete Modal -->
    <Modal v-if="modalOpen && modalMode === 'delete'" max-width="max-w-md" @close="closeModal">
      <template #header><h2 class="text-base font-semibold text-red-600">Hapus Mustahiq Lembaga</h2></template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <p class="text-sm text-muted-foreground">Data berikut akan dihapus permanen, termasuk rekening banknya:</p>
        <div class="rounded border border-border bg-muted/30 px-4 py-3 text-sm space-y-1">
          <p class="font-semibold">{{ selectedRow?.name }}</p>
          <p class="text-xs text-muted-foreground">No: {{ selectedRow?.no_mustahiq || '—' }}</p>
          <p class="text-xs text-muted-foreground">Alamat: {{ selectedRow?.address || '—' }}</p>
          <p class="text-xs text-muted-foreground">Telepon: {{ selectedRow?.phone_number || '—' }}</p>
        </div>
        <p class="text-xs text-red-600 font-medium">Tindakan ini tidak dapat dibatalkan.</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button variant="destructive" size="sm" :disabled="modalLoading" @click="confirmDelete">{{ modalLoading ? 'Menghapus...' : 'Hapus' }}</Button>
        </div>
      </template>
    </Modal>

    <!-- Status Modal -->
    <Modal v-if="modalOpen && modalMode === 'status'" max-width="max-w-sm" @close="closeModal">
      <template #header><h2 class="text-base font-semibold">{{ pendingStatus === 'N' ? 'NonAktifkan' : 'Aktifkan' }} Mustahiq</h2></template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <div class="rounded border border-border bg-muted/30 px-4 py-3 text-sm">
          <p class="font-semibold">{{ selectedRow?.name }}</p>
          <p class="text-xs text-muted-foreground">No: {{ selectedRow?.no_mustahiq || '—' }}</p>
        </div>
        <p class="text-sm">Apakah Anda yakin ingin <strong>{{ pendingStatus === 'N' ? 'menonaktifkan' : 'mengaktifkan kembali' }}</strong> mustahiq ini?</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button size="sm" :disabled="modalLoading" @click="confirmStatus">{{ modalLoading ? 'Memproses...' : (pendingStatus === 'N' ? 'NonAktifkan' : 'Aktifkan') }}</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { CheckCircle2, Pencil, Plus, Search, X, XCircle } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

interface DonorRow {
  donor_id: number
  donor_no: string | null
  donor_name: string | null
  join_date: string | null
  phone_number: string | null
  status: string | null
}
interface Pagination { page: number; page_size: number; total: number; total_pages: number }
interface ListResponse { rows: DonorRow[]; pagination: Pagination }

const router = useRouter()
const toast  = useToast()

const rows        = ref<DonorRow[]>([])
const loading     = shallowRef(false)
const errorMsg    = shallowRef<string | null>(null)
const page        = shallowRef(1)
const totalPages  = shallowRef(1)
const totalRec    = shallowRef(0)
const pageSize    = shallowRef(25)
const searchInput = ref('')
const filterStatus = shallowRef('')

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})
watch(filterStatus, () => { page.value = 1; loadData() })

async function loadData() {
  loading.value = true; errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    if (filterStatus.value) params.set('status', filterStatus.value)
    const res = await api.get<ListResponse>(`/api/fundraising/donors/individual?${params}`)
    rows.value = res.rows
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

function goCreate() { router.push({ name: 'fundraising-donor-individual-create' }) }
function goEdit(row: DonorRow) {
  router.push({ name: 'fundraising-donor-individual-edit', params: { id: row.donor_id } })
}

// ── Status toggle modal ───────────────────────────────────────────────────────
const modalOpen    = shallowRef(false)
const modalLoading = shallowRef(false)
const modalError   = shallowRef<string | null>(null)
const selectedRow  = ref<DonorRow | null>(null)
const pendingStatus = shallowRef<'A' | 'N'>('N')

function closeModal() { modalOpen.value = false }
function openStatus(row: DonorRow, s: 'A' | 'N') {
  selectedRow.value = row; pendingStatus.value = s; modalError.value = null; modalOpen.value = true
}

async function confirmStatus() {
  if (!selectedRow.value) return
  modalLoading.value = true; modalError.value = null
  try {
    await api.patch(`/api/fundraising/donors/individual/${selectedRow.value.donor_id}/status`, { status: pendingStatus.value })
    toast.success(`Donatur berhasil ${pendingStatus.value === 'A' ? 'diaktifkan' : 'dinonaktifkan'}.`)
    closeModal(); loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal mengubah status.'
  } finally { modalLoading.value = false }
}

onMounted(loadData)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Data Donatur Individu" subtitle="Daftar donatur perorangan">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="goCreate">
          <Plus class="w-3.5 h-3.5" /> Tambah
        </Button>
      </template>
    </PageHeader>

    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{{ errorMsg }}</div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center gap-3 flex-wrap">
        <div class="relative flex-1 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input v-model="searchInput" type="text" placeholder="Cari nama / no donatur / HP..."
            class="w-full h-8 pl-8 pr-8 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
          <button v-if="searchInput" class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground" @click="searchInput = ''">
            <X class="w-3 h-3" />
          </button>
        </div>
        <select v-model="filterStatus"
          class="h-8 px-2 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring">
          <option value="">Semua Status</option>
          <option value="A">Aktif</option>
          <option value="N">NonAktif</option>
        </select>
      </div>

      <!-- Pagination top -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} donatur individu
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @prev="prevPage" @next="nextPage" @update:page-size="changePageSize" />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium w-32">No. Donatur</th>
              <th class="px-4 py-2 text-left font-medium">Nama</th>
              <th class="px-4 py-2 text-left font-medium w-32">Tgl Bergabung</th>
              <th class="px-4 py-2 text-left font-medium w-36">Telepon</th>
              <th class="px-4 py-2 text-center font-medium w-24">Status</th>
              <th class="px-4 py-2 text-right font-medium w-24">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td></tr>
            <tr v-else-if="rows.length === 0"><td colspan="6" class="px-4 py-8 text-center text-muted-foreground text-xs italic">Belum ada data donatur individu.</td></tr>
            <tr v-for="row in rows" :key="row.donor_id" class="hover:bg-background/60">
              <td class="px-4 py-2 font-mono text-xs text-muted-foreground">{{ row.donor_no || '—' }}</td>
              <td class="px-4 py-2 font-medium">{{ row.donor_name || '—' }}</td>
              <td class="px-4 py-2 text-xs">{{ row.join_date || '—' }}</td>
              <td class="px-4 py-2 text-xs">{{ row.phone_number || '—' }}</td>
              <td class="px-4 py-2 text-center">
                <span class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
                  :class="row.status === 'A' ? 'bg-emerald-100 text-emerald-700' : 'bg-zinc-100 text-zinc-500'">
                  {{ row.status === 'A' ? 'Aktif' : 'NonAktif' }}
                </span>
              </td>
              <td class="px-4 py-2">
                <div class="flex items-center justify-end gap-0.5">
                  <button class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-blue-600 transition-colors" title="Ubah" @click="goEdit(row)">
                    <Pencil class="w-3.5 h-3.5" />
                  </button>
                  <button v-if="row.status === 'A'" class="p-1.5 rounded hover:bg-amber-50 text-muted-foreground hover:text-amber-600 transition-colors" title="NonAktifkan" @click="openStatus(row, 'N')">
                    <XCircle class="w-3.5 h-3.5" />
                  </button>
                  <button v-else class="p-1.5 rounded hover:bg-emerald-50 text-muted-foreground hover:text-emerald-600 transition-colors" title="Aktifkan" @click="openStatus(row, 'A')">
                    <CheckCircle2 class="w-3.5 h-3.5" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Status Modal -->
    <Modal v-if="modalOpen" max-width="max-w-sm" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">{{ pendingStatus === 'N' ? 'NonAktifkan' : 'Aktifkan' }} Donatur</h2>
      </template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <div class="rounded border border-border bg-muted/30 px-4 py-3 text-sm">
          <p class="font-semibold">{{ selectedRow?.donor_name }}</p>
          <p class="text-xs text-muted-foreground">No: {{ selectedRow?.donor_no || '—' }}</p>
        </div>
        <p class="text-sm">Apakah Anda yakin ingin <strong>{{ pendingStatus === 'N' ? 'menonaktifkan' : 'mengaktifkan kembali' }}</strong> donatur ini?</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button size="sm" :disabled="modalLoading" @click="confirmStatus">
            {{ modalLoading ? 'Memproses...' : (pendingStatus === 'N' ? 'NonAktifkan' : 'Aktifkan') }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

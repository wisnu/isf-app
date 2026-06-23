<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/app/stores/auth.store'
import { useRouter } from 'vue-router'

// ── Types ─────────────────────────────────────────────────────────────────────

interface DokumenKeluarRow {
  dokumen_id: number
  nomor: string
  pic: string
  tujuan: string
  perihal: string
  tanggal_dokumen: string
  tanggal_kirim: string | null
  work_unit_id: number
  work_unit_desc: string
  nama_jenis_dokumen: string
  status_kirim: string | null
  branch_code: string
}

interface Pagination {
  page: number
  limit: number
  total: number
  total_pages: number
}

interface ListResponse {
  rows: DokumenKeluarRow[]
  pagination: Pagination
}

interface JenisDokumenOption {
  id_jenis_dokumen: number
  kode_jenis_dokumen: string
  nama_jenis_dokumen: string
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const auth = useAuthStore()
const router = useRouter()

const rows = ref<DokumenKeluarRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const pageSize = shallowRef(25)
const searchInput = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const jenisDokumenId = ref<number | null>(null)

const jenisDokumenOptions = ref<JenisDokumenOption[]>([])

let filterTimer: ReturnType<typeof setTimeout> | null = null
watch([searchInput, dateFrom, dateTo, jenisDokumenId], () => {
  if (filterTimer) clearTimeout(filterTimer)
  filterTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

// ── API Calls ─────────────────────────────────────────────────────────────────

async function loadJenisDokumen() {
  try {
    const res = await api.get<{ rows: JenisDokumenOption[] }>('/api/generalaffair/document-types?page=1&page_size=100')
    jenisDokumenOptions.value = res.rows
  } catch {
    jenisDokumenOptions.value = []
  }
}

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    if (dateFrom.value) params.set('date_from', dateFrom.value)
    if (dateTo.value) params.set('date_to', dateTo.value)
    if (jenisDokumenId.value) params.set('id_jenis_dokumen', String(jenisDokumenId.value))
    const res = await api.get<ListResponse>(`/api/generalaffair/document/outgoing?${params}`)
    rows.value = res.rows
    totalRec.value = res.pagination.total
    totalPages.value = res.pagination.total_pages
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
}

async function deleteData() {
  if (!selected.value) return
  deleteLoading.value = true
  try {
    await api.delete(`/api/generalaffair/document/outgoing/${selected.value.dokumen_id}`)
    toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Dokumen berhasil dihapus', life: 3000 })
    showDelete.value = false
    loadData()
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof ApiError ? e.message : 'Gagal menghapus', life: 3000 })
  } finally {
    deleteLoading.value = false
  }
}

onMounted(() => {
  loadJenisDokumen()
  loadData()
})

// ── Modal State ───────────────────────────────────────────────────────────────

const showDelete = shallowRef(false)
const selected = ref<DokumenKeluarRow | null>(null)
const deleteLoading = shallowRef(false)

function openEdit(row: DokumenKeluarRow) {
  router.push({ name: 'generalaffair-dokumen-keluar-edit', params: { id: row.dokumen_id } })
}

function openDeleteConfirm(row: DokumenKeluarRow) {
  selected.value = row
  showDelete.value = true
}
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Dokumen Keluar" subtitle="Kelola dokumen yang dikirim keluar dari organisasi" />

    <!-- Error message -->
    <div v-if="errorMsg" class="flex items-center gap-2 rounded-lg border border-red-200
                                bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Card: Toolbar + Pagination + Table -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3 flex-wrap">
        <div class="relative flex-1 min-w-xs max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input
            v-model="searchInput"
            placeholder="Cari..."
            class="h-8 w-full rounded pl-8 pr-3 text-xs border border-border bg-background
                   focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>
        <div class="flex items-center gap-2">
          <DateField v-model="dateFrom" placeholder="Dari" />
          <DateField v-model="dateTo" placeholder="Sampai" />
          <SearchSelect
            :model-value="jenisDokumenId"
            :options="jenisDokumenOptions.map(x => ({ value: x.id_jenis_dokumen, label: x.nama_jenis_dokumen }))"
            placeholder="Jenis dokumen..."
            @update:model-value="jenisDokumenId = $event"
          />
          <Button
            v-if="auth.menus.includes('generalaffair.document.outgoing')"
            size="sm"
            @click="() => router.push({ name: 'generalaffair-dokumen-keluar-create' })"
          >
            <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
          </Button>
        </div>
      </div>

      <!-- Pagination (SELALU di atas tabel) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} data
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @prev="page > 1 && (page--, loadData())"
          @next="page < totalPages && (page++, loadData())"
          @update:page-size="(s) => { pageSize.value = s; page.value = 1; loadData() }"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">Nomor</th>
              <th class="px-4 py-2 text-left font-medium">PIC</th>
              <th class="px-4 py-2 text-left font-medium">Tujuan</th>
              <th class="px-4 py-2 text-left font-medium">Perihal</th>
              <th class="px-4 py-2 text-left font-medium">Tgl Dokumen</th>
              <th class="px-4 py-2 text-left font-medium">Tgl Kirim</th>
              <th class="px-4 py-2 text-left font-medium">Unit Kerja</th>
              <th class="px-4 py-2 text-left font-medium">Jenis</th>
              <th class="px-4 py-2 text-left font-medium">Status</th>
              <th class="px-4 py-2 text-right font-medium w-24">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="10" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="!rows.length">
              <td colspan="10" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
                Tidak ada data yang ditemukan.
              </td>
            </tr>
            <tr
              v-for="row in rows"
              :key="row.dokumen_id"
              class="hover:bg-muted/30 transition-colors"
            >
              <td class="px-4 py-1 text-xs">{{ row.nomor }}</td>
              <td class="px-4 py-1 text-xs">{{ row.pic }}</td>
              <td class="px-4 py-1 text-xs">{{ row.tujuan }}</td>
              <td class="px-4 py-1 text-xs">{{ row.perihal }}</td>
              <td class="px-4 py-1 text-xs">{{ dmy(row.tanggal_dokumen) }}</td>
              <td class="px-4 py-1 text-xs">{{ row.tanggal_kirim ? dmy(row.tanggal_kirim) : '-' }}</td>
              <td class="px-4 py-1 text-xs">{{ row.work_unit_desc }}</td>
              <td class="px-4 py-1 text-xs">{{ row.nama_jenis_dokumen }}</td>
              <td class="px-4 py-1 text-xs">{{ row.status_kirim || '-' }}</td>
              <td class="px-4 py-1 text-right">
                <div class="flex items-center justify-end gap-1">
                  <button
                    v-if="auth.menus.includes('generalaffair.document.outgoing')"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Edit"
                    @click="openEdit(row)"
                  >
                    <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                  </button>
                  <button
                    v-if="auth.menus.includes('generalaffair.document.outgoing')"
                    class="p-1 rounded hover:bg-muted transition-colors"
                    title="Hapus"
                    @click="openDeleteConfirm(row)"
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

    <!-- Delete Modal -->
    <Modal
      v-if="showDelete && selected"
      :open="showDelete"
      title="Hapus Dokumen Keluar"
      :loading="deleteLoading"
      danger
      @close="() => { showDelete = false; selected = null }"
      @submit="deleteData"
    >
      <div class="space-y-3 text-sm">
        <p><strong>Nomor:</strong> {{ selected.nomor }}</p>
        <p><strong>PIC:</strong> {{ selected.pic }}</p>
        <p><strong>Tujuan:</strong> {{ selected.tujuan }}</p>
        <p><strong>Perihal:</strong> {{ selected.perihal }}</p>
        <p><strong>Tgl Dokumen:</strong> {{ dmy(selected.tanggal_dokumen) }}</p>
        <p class="text-red-600 font-medium">Apakah Anda yakin ingin menghapus data ini?</p>
      </div>
    </Modal>
  </div>
</template>

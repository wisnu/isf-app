<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/shared/components/Button.vue'
import Modal from '@/shared/components/Modal.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import TablePagination from '@/shared/components/TablePagination.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'
import { useAuthStore } from '@/app/stores/auth.store'

// ── Types ─────────────────────────────────────────────────────────────────────

interface PartnerRow {
  partner_id: number
  name: string | null
  address: string | null
  phone_number: string | null
  status: string | null
}

interface PartnerDetail {
  partner_id: number
  name: string | null
  address: string | null
  address_kelurahan: string | null
  address_kecamatan: string | null
  address_city: string | null
  phone_number: string | null
  email: string | null
  cp_name: string | null
  cp_address: string | null
  cp_mobile_phone: string | null
  cp_email: string | null
  status: string | null
}

interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

interface ListResponse {
  rows: PartnerRow[]
  pagination: Pagination
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const auth  = useAuthStore()

const rows        = ref<PartnerRow[]>([])
const loading     = shallowRef(false)
const errorMsg    = shallowRef<string | null>(null)
const page        = shallowRef(1)
const totalPages  = shallowRef(1)
const totalRec    = shallowRef(0)
const pageSize    = shallowRef(25)
const searchInput = ref('')

let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadData() }, 300)
})

// ── List ──────────────────────────────────────────────────────────────────────

async function loadData() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    const res = await api.get<ListResponse>(`/api/distribution/partner?${params}`)
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

// ── Modal state ───────────────────────────────────────────────────────────────

type ModalMode = 'create' | 'edit' | 'detail' | 'delete'

const modalMode    = shallowRef<ModalMode>('create')
const modalOpen    = shallowRef(false)
const modalLoading = shallowRef(false)
const modalError   = shallowRef<string | null>(null)
const selectedRow  = ref<PartnerRow | null>(null)
const detailData   = ref<PartnerDetail | null>(null)

const form = reactive<Omit<PartnerDetail, 'partner_id' | 'status'>>({
  name: '',
  address: null,
  address_kelurahan: null,
  address_kecamatan: null,
  address_city: null,
  phone_number: null,
  email: null,
  cp_name: null,
  cp_address: null,
  cp_mobile_phone: null,
  cp_email: null,
})

function resetForm() {
  form.name = ''
  form.address = null
  form.address_kelurahan = null
  form.address_kecamatan = null
  form.address_city = null
  form.phone_number = null
  form.email = null
  form.cp_name = null
  form.cp_address = null
  form.cp_mobile_phone = null
  form.cp_email = null
}

function fillForm(d: PartnerDetail) {
  form.name             = d.name ?? ''
  form.address          = d.address
  form.address_kelurahan = d.address_kelurahan
  form.address_kecamatan = d.address_kecamatan
  form.address_city     = d.address_city
  form.phone_number     = d.phone_number
  form.email            = d.email
  form.cp_name          = d.cp_name
  form.cp_address       = d.cp_address
  form.cp_mobile_phone  = d.cp_mobile_phone
  form.cp_email         = d.cp_email
}

function openCreate() {
  resetForm()
  modalMode.value  = 'create'
  modalError.value = null
  modalOpen.value  = true
}

async function openEdit(row: PartnerRow) {
  selectedRow.value  = row
  modalMode.value    = 'edit'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  try {
    const d = await api.get<PartnerDetail>(`/api/distribution/partner/${row.partner_id}`)
    detailData.value = d
    fillForm(d)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

async function openDetail(row: PartnerRow) {
  selectedRow.value  = row
  modalMode.value    = 'detail'
  modalError.value   = null
  modalLoading.value = true
  modalOpen.value    = true
  try {
    detailData.value = await api.get<PartnerDetail>(`/api/distribution/partner/${row.partner_id}`)
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal memuat detail'
  } finally {
    modalLoading.value = false
  }
}

function openDelete(row: PartnerRow) {
  selectedRow.value = row
  detailData.value  = null
  modalMode.value   = 'delete'
  modalError.value  = null
  modalLoading.value = true
  modalOpen.value   = true
  // Load full detail for delete confirmation modal
  api.get<PartnerDetail>(`/api/distribution/partner/${row.partner_id}`)
    .then(d => { detailData.value = d })
    .catch(() => {})
    .finally(() => { modalLoading.value = false })
}

function closeModal() { modalOpen.value = false }

// ── Save / Delete ─────────────────────────────────────────────────────────────

async function saveForm() {
  if (!form.name?.trim()) { modalError.value = 'Nama mitra wajib diisi.'; return }
  modalLoading.value = true
  modalError.value   = null
  try {
    const payload = {
      name:             form.name.trim(),
      address:          form.address || null,
      address_kelurahan: form.address_kelurahan || null,
      address_kecamatan: form.address_kecamatan || null,
      address_city:     form.address_city || null,
      phone_number:     form.phone_number || null,
      email:            form.email || null,
      cp_name:          form.cp_name || null,
      cp_address:       form.cp_address || null,
      cp_mobile_phone:  form.cp_mobile_phone || null,
      cp_email:         form.cp_email || null,
    }
    if (modalMode.value === 'create') {
      await api.post('/api/distribution/partner', payload)
      toast.success('Mitra berhasil ditambahkan.')
    } else {
      await api.put(`/api/distribution/partner/${selectedRow.value!.partner_id}`, payload)
      toast.success('Mitra berhasil diperbarui.')
    }
    closeModal()
    loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menyimpan data.'
  } finally {
    modalLoading.value = false
  }
}

async function confirmDelete() {
  if (!selectedRow.value) return
  modalLoading.value = true
  modalError.value   = null
  try {
    await api.delete(`/api/distribution/partner/${selectedRow.value.partner_id}`)
    toast.success('Mitra berhasil dihapus.')
    closeModal()
    loadData()
  } catch (e) {
    modalError.value = e instanceof ApiError ? e.message : 'Gagal menghapus data.'
  } finally {
    modalLoading.value = false
  }
}

onMounted(() => { loadData() })
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Mitra" subtitle="Data mitra program penyaluran">
      <template #actions>
        <Button
          v-if="auth.hasMenu('distribution.partner.list')"
          size="sm"
          class="gap-1.5 h-8 text-xs"
          @click="openCreate"
        >
          <Plus class="w-3.5 h-3.5" />
          Tambah
        </Button>
      </template>
    </PageHeader>

    <div v-if="errorMsg" class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400">
      {{ errorMsg }}
    </div>

    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center gap-3">
        <div class="relative flex-1 max-w-xs">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
          <input
            v-model="searchInput"
            type="text"
            placeholder="Cari nama / alamat / telepon..."
            class="w-full h-8 pl-8 pr-8 text-xs border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring"
          />
          <button v-if="searchInput" class="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground" @click="searchInput = ''">
            <X class="w-3 h-3" />
          </button>
        </div>
      </div>

      <!-- Pagination (atas) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRec > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} mitra
          </template>
          <template v-else>Tidak ada data</template>
        </span>
        <TablePagination
          :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
          @prev="prevPage" @next="nextPage" @update:page-size="changePageSize"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 text-left font-medium">Nama Mitra</th>
              <th class="px-4 py-2 text-left font-medium max-w-xs">Alamat</th>
              <th class="px-4 py-2 text-left font-medium w-40">Telepon</th>
              <th class="px-4 py-2 text-right font-medium w-28">Aksi</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border">
            <tr v-if="loading">
              <td colspan="4" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="4" class="px-4 py-8 text-center text-muted-foreground text-xs italic">Belum ada data mitra.</td>
            </tr>
            <tr v-for="row in rows" :key="row.partner_id" class="hover:bg-background/60">
              <td class="px-4 py-1.5 font-medium">{{ row.name || '—' }}</td>
              <td class="px-4 py-1.5 text-xs text-muted-foreground max-w-xs truncate">{{ row.address || '—' }}</td>
              <td class="px-4 py-1.5 text-xs">{{ row.phone_number || '—' }}</td>
              <td class="px-4 py-1.5">
                <div class="flex items-center justify-end gap-0.5">
                  <button
                    class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors text-[10px]"
                    title="Detail"
                    @click="openDetail(row)"
                  >Detail</button>
                  <button
                    class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-blue-600 transition-colors"
                    title="Ubah"
                    @click="openEdit(row)"
                  ><Pencil class="w-3.5 h-3.5" /></button>
                  <button
                    class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600 transition-colors"
                    title="Hapus"
                    @click="openDelete(row)"
                  ><Trash2 class="w-3.5 h-3.5" /></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ── Create / Edit Modal ──────────────────────────────────────────────── -->
    <Modal v-if="modalOpen && (modalMode === 'create' || modalMode === 'edit')" max-width="max-w-2xl" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">{{ modalMode === 'create' ? 'Tambah Mitra' : 'Ubah Mitra' }}</h2>
      </template>

      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat data...</div>
      <div v-else class="space-y-4">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>

        <!-- Data Mitra -->
        <fieldset class="space-y-3">
          <legend class="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">Data Mitra</legend>
          <div>
            <label class="block text-xs font-medium mb-1">Nama Mitra <span class="text-red-500">*</span></label>
            <input v-model="form.name" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" placeholder="Nama mitra / lembaga" />
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div class="col-span-2">
              <label class="block text-xs font-medium mb-1">Alamat Jalan</label>
              <input v-model="form.address" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Kelurahan</label>
              <input v-model="form.address_kelurahan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Kecamatan</label>
              <input v-model="form.address_kecamatan" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Kota / Kab</label>
              <input v-model="form.address_city" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">No Telepon</label>
              <input v-model="form.phone_number" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium mb-1">E-Mail</label>
              <input v-model="form.email" type="email" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
          </div>
        </fieldset>

        <!-- Contact Person -->
        <fieldset class="space-y-3">
          <legend class="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">Info Contact Person</legend>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium mb-1">Nama CP</label>
              <input v-model="form.cp_name" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div>
              <label class="block text-xs font-medium mb-1">Nomor HP CP</label>
              <input v-model="form.cp_mobile_phone" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium mb-1">Alamat CP</label>
              <input v-model="form.cp_address" type="text" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
            <div class="col-span-2">
              <label class="block text-xs font-medium mb-1">Email CP</label>
              <input v-model="form.cp_email" type="email" class="w-full h-8 px-3 text-sm border border-border rounded bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
            </div>
          </div>
        </fieldset>
      </div>

      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button size="sm" :disabled="modalLoading" @click="saveForm">
            {{ modalLoading ? 'Menyimpan...' : 'Simpan' }}
          </Button>
        </div>
      </template>
    </Modal>

    <!-- Detail Modal -->
    <Modal v-if="modalOpen && modalMode === 'detail'" max-width="max-w-xl" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold">Detail Mitra</h2>
      </template>
      <div v-if="modalLoading" class="py-8 text-center text-muted-foreground text-sm">Memuat...</div>
      <div v-else-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
      <div v-else-if="detailData" class="space-y-4 text-sm">
        <div class="grid grid-cols-2 gap-x-6 gap-y-2">
          <div class="col-span-2"><span class="text-xs text-muted-foreground">Nama Mitra</span><p class="font-medium">{{ detailData.name || '—' }}</p></div>
          <div class="col-span-2"><span class="text-xs text-muted-foreground">Alamat Jalan</span><p>{{ detailData.address || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Kelurahan</span><p>{{ detailData.address_kelurahan || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Kecamatan</span><p>{{ detailData.address_kecamatan || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Kota / Kab</span><p>{{ detailData.address_city || '—' }}</p></div>
          <div><span class="text-xs text-muted-foreground">Telepon</span><p>{{ detailData.phone_number || '—' }}</p></div>
          <div class="col-span-2"><span class="text-xs text-muted-foreground">E-Mail</span><p>{{ detailData.email || '—' }}</p></div>
        </div>
        <div class="border-t border-border pt-3">
          <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">Contact Person</p>
          <div class="grid grid-cols-2 gap-x-6 gap-y-2">
            <div><span class="text-xs text-muted-foreground">Nama CP</span><p>{{ detailData.cp_name || '—' }}</p></div>
            <div><span class="text-xs text-muted-foreground">HP CP</span><p>{{ detailData.cp_mobile_phone || '—' }}</p></div>
            <div class="col-span-2"><span class="text-xs text-muted-foreground">Alamat CP</span><p>{{ detailData.cp_address || '—' }}</p></div>
            <div class="col-span-2"><span class="text-xs text-muted-foreground">Email CP</span><p>{{ detailData.cp_email || '—' }}</p></div>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="flex justify-end"><Button variant="outline" size="sm" @click="closeModal">Tutup</Button></div>
      </template>
    </Modal>

    <!-- Delete Modal -->
    <Modal v-if="modalOpen && modalMode === 'delete'" max-width="max-w-md" @close="closeModal">
      <template #header>
        <h2 class="text-base font-semibold text-red-600">Hapus Mitra</h2>
      </template>
      <div class="space-y-3">
        <div v-if="modalError" class="rounded border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">{{ modalError }}</div>
        <p class="text-sm text-muted-foreground">Data mitra berikut akan dihapus permanen:</p>
        <div v-if="modalLoading" class="py-4 text-center text-muted-foreground text-xs">Memuat...</div>
        <div v-else class="rounded border border-border bg-muted/30 px-4 py-3 text-sm space-y-1">
          <div class="font-semibold">{{ detailData?.name || selectedRow?.name }}</div>
          <div class="text-xs text-muted-foreground">Alamat: {{ detailData?.address || selectedRow?.address || '—' }}</div>
          <div v-if="detailData?.cp_name" class="text-xs text-muted-foreground">Contact Person: {{ detailData.cp_name }}</div>
        </div>
        <p class="text-xs text-red-600 font-medium">Tindakan ini tidak dapat dibatalkan.</p>
      </div>
      <template #footer>
        <div class="flex justify-end gap-2">
          <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
          <Button variant="destructive" size="sm" :disabled="modalLoading" @click="confirmDelete">
            {{ modalLoading ? 'Menghapus...' : 'Hapus' }}
          </Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

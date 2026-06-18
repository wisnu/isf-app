<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'
import { formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BudgetOwner { owner_id: string; owner_name: string }
interface Period { period_id: number; period_value: number }
interface BudgetItem {
  budget_id: number
  budget_code: string
  item_group: string
  item_name: string
  amount: number
  realization: number | null
}

interface BudgetList {
  rows: BudgetItem[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
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
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRecords = shallowRef(0)

const changedItems = ref<Set<string>>(new Set())

const modalOpen = shallowRef(false)
const modalMode = shallowRef<'create' | 'edit' | 'delete'>('create')
const selectedItem = ref<BudgetItem | null>(null)

const form = reactive({
  budget_code: '',
  item_group: '',
  item_name: '',
  amount: 0,
})

// ── Lookup data ───────────────────────────────────────────────────────────────

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
      label: String(p.period_value),
    }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat periode')
  } finally {
    periodsLoading.value = false
  }
}

// ── Load budget data ──────────────────────────────────────────────────────────

async function loadBudgets() {
  if (!selectedOwner.value || !selectedPeriod.value) return

  loading.value = true
  changedItems.value.clear()
  try {
    const params = new URLSearchParams({
      owner_id: selectedOwner.value,
      period_id: selectedPeriod.value,
      page: String(page.value),
      limit: String(pageSize.value),
    })
    const res = await api.get<BudgetList>(`/api/budget/?${params}`)
    rows.value = res.rows
    totalRecords.value = res.pagination.total
    totalPages.value = res.pagination.total_pages || 1
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat anggaran')
    rows.value = []
  } finally {
    loading.value = false
  }
}

watch(selectedOwner, () => {
  selectedPeriod.value = ''
  periods.value = []
  rows.value = []
  if (selectedOwner.value) loadPeriods()
})

watch(selectedPeriod, () => {
  page.value = 1
  if (selectedPeriod.value) loadBudgets()
})

// ── Modal handlers ────────────────────────────────────────────────────────────

function resetForm() {
  form.budget_code = ''
  form.item_group = ''
  form.item_name = ''
  form.amount = 0
}

function openCreate() {
  modalMode.value = 'create'
  selectedItem.value = null
  resetForm()
  modalOpen.value = true
}

function openEdit(item: BudgetItem) {
  modalMode.value = 'edit'
  selectedItem.value = item
  form.budget_code = item.budget_code
  form.item_group = item.item_group
  form.item_name = item.item_name
  form.amount = item.amount
  modalOpen.value = true
}

function openDelete(item: BudgetItem) {
  modalMode.value = 'delete'
  selectedItem.value = item
  form.budget_code = item.budget_code
  form.item_group = item.item_group
  form.item_name = item.item_name
  form.amount = item.amount
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
  selectedItem.value = null
  resetForm()
}

// ── Submit handlers ───────────────────────────────────────────────────────────

async function submitForm() {
  if (!form.budget_code.trim()) {
    toast.error('Kode Budget wajib diisi')
    return
  }
  if (!form.item_group.trim()) {
    toast.error('Kelompok Kegiatan wajib diisi')
    return
  }
  if (!form.item_name.trim()) {
    toast.error('Rincian Kebutuhan wajib diisi')
    return
  }
  if (form.amount <= 0) {
    toast.error('Nilai Anggaran harus lebih dari 0')
    return
  }

  const isCreate = modalMode.value === 'create'
  loading.value = true

  try {
    const payload = {
      owner_id: Number(selectedOwner.value),
      period_id: Number(selectedPeriod.value),
      budget_code: form.budget_code.trim(),
      item_group: form.item_group.trim(),
      item_name: form.item_name.trim(),
      amount: form.amount,
    }

    if (isCreate) {
      await api.post('/api/budget/', payload)
    } else {
      await api.put(`/api/budget/${selectedItem.value?.budget_id}`, payload)
    }

    toast.success(
      isCreate
        ? 'Anggaran baru berhasil disimpan. Silahkan diotorisasi.'
        : 'Perubahan anggaran berhasil disimpan. Silahkan diotorisasi.',
    )
    closeModal()
    loadBudgets()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan anggaran')
  } finally {
    loading.value = false
  }
}

async function submitDelete() {
  loading.value = true

  try {
    await api.delete(`/api/budget/${selectedItem.value?.budget_id}`)
    toast.success('Anggaran berhasil dihapus.')
    closeModal()
    loadBudgets()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menghapus anggaran')
  } finally {
    loading.value = false
  }
}

// ── Inline edit ───────────────────────────────────────────────────────────────

function onAmountChange(budgetId: string) {
  changedItems.value.add(budgetId)
}

async function submitRevision() {
  if (changedItems.value.size === 0) {
    toast.error('Tidak ada perubahan yang disimpan')
    return
  }

  const items = rows.value
    .filter((r) => changedItems.value.has(r.budget_id))
    .map((r) => ({ budget_id: r.budget_id, amount: r.amount }))

  loading.value = true
  try {
    await api.post('/api/budget/revise', { items })
    toast.success('Revisi anggaran berhasil disimpan')
    changedItems.value.clear()
    loadBudgets()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan revisi')
  } finally {
    loading.value = false
  }
}

onMounted(loadOwners)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Revisi Anggaran" subtitle="Ubah dan revisi data anggaran yang sudah ada" />

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
          <Button
            variant="outline"
            size="sm"
            :disabled="!selectedOwner || !selectedPeriod"
            @click="loadBudgets"
          >
            Muat Data
          </Button>
        </div>
      </CardContent>
    </Card>

    <!-- Toolbar + Table card (hanya muncul setelah muat data) -->
    <template v-if="rows.length > 0 || loading">
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <!-- Toolbar -->
        <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3">
          <div></div>
          <div class="flex items-center gap-2">
            <Button size="sm" @click="openCreate">
              <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
            </Button>
          </div>
        </div>

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
            @prev="page > 1 && (page--, loadBudgets())"
            @next="page < totalPages && (page++, loadBudgets())"
            @update:page-size="(s) => { pageSize = s; page = 1; loadBudgets() }"
          />
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
              <tr>
                <th class="px-4 py-2 text-left font-medium">Kode Budget</th>
                <th class="px-4 py-2 text-left font-medium">Kelompok Kegiatan</th>
                <th class="px-4 py-2 text-left font-medium">Rincian Kebutuhan</th>
                <th class="px-4 py-2 text-right font-medium">Anggaran</th>
                <th class="px-4 py-2 text-right font-medium">Realisasi</th>
                <th class="px-4 py-2 text-right font-medium">Sisa</th>
                <th class="px-4 py-2 text-right font-medium w-20">Aksi</th>
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
              <tr v-for="row in rows" :key="row.budget_id" class="hover:bg-muted/30">
                <td class="px-4 py-1 text-xs font-mono">{{ row.budget_code }}</td>
                <td class="px-4 py-1 text-xs">{{ row.item_group }}</td>
                <td class="px-4 py-1 text-xs">{{ row.item_name }}</td>
                <td class="px-4 py-1 text-right text-xs">
                  {{ formatIdr(row.amount) }}
                </td>
                <td class="px-4 py-1 text-right text-xs">
                  {{ row.realization ? formatIdr(row.realization) : '—' }}
                </td>
                <td class="px-4 py-1 text-right text-xs font-medium">
                  {{
                    formatIdr(row.amount - (row.realization ?? 0))
                  }}
                </td>
                <td class="px-4 py-1 text-right">
                  <div class="flex items-center justify-end gap-1">
                    <Tooltip side="top">
                      <template #trigger>
                        <button
                          class="p-1 rounded hover:bg-muted transition-colors"
                          @click="openEdit(row)"
                        >
                          <Pencil class="w-3.5 h-3.5 text-muted-foreground" />
                        </button>
                      </template>
                      Ubah
                    </Tooltip>
                    <Tooltip side="top">
                      <template #trigger>
                        <button
                          class="p-1 rounded hover:bg-red-50 transition-colors"
                          @click="openDelete(row)"
                        >
                          <Trash2 class="w-3.5 h-3.5 text-red-500" />
                        </button>
                      </template>
                      Hapus
                    </Tooltip>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tombol simpan revisi (di bawah tabel jika ada perubahan) -->
      <div v-if="changedItems.size > 0" class="flex justify-end gap-2">
        <Button variant="outline" @click="changedItems.clear()">Batalkan Perubahan</Button>
        <Button @click="submitRevision">Simpan Revisi ({{ changedItems.size }} item)</Button>
      </div>
    </template>

    <!-- Form Modal -->
    <Teleport to="body">
      <div
        v-if="modalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
        @click.self="closeModal"
      >
        <div class="w-full max-w-2xl rounded-xl border border-border bg-surface shadow-xl flex flex-col max-h-[90vh]">
          <!-- Header -->
          <div class="flex items-center justify-between border-b border-border px-6 py-4 shrink-0">
            <div>
              <h2 class="text-base font-semibold" :class="modalMode === 'delete' ? 'text-red-700' : ''">
                {{
                  modalMode === 'create'
                    ? 'Tambah Anggaran'
                    : modalMode === 'edit'
                      ? 'Ubah Anggaran'
                      : 'Konfirmasi Hapus Anggaran'
                }}
              </h2>
              <p class="text-[11px] mt-0.5" :class="modalMode === 'delete' ? 'text-red-500' : 'text-muted'">
                {{ modalMode === 'delete' ? 'Periksa data berikut sebelum menghapus' : '' }}
              </p>
            </div>
            <button
              type="button"
              class="rounded-lg p-1.5 text-muted hover:bg-background transition-colors"
              @click="closeModal"
            >
              <X class="w-4 h-4" />
            </button>
          </div>

          <!-- Body -->
          <div v-if="modalMode !== 'delete'" class="overflow-y-auto px-6 py-5 space-y-4">
            <div>
              <label class="mb-1 block text-xs font-medium">
                Kode Budget <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.budget_code"
                placeholder="mis. BUD-001"
                class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="mb-1 block text-xs font-medium">
                  Kelompok Kegiatan <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.item_group"
                  placeholder="mis. Program Zakat"
                  class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium">
                  Rincian Kebutuhan <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.item_name"
                  placeholder="mis. Operasional Kantor"
                  class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <div>
              <label class="mb-1 block text-xs font-medium">
                Nilai Anggaran <span class="text-red-500">*</span>
              </label>
              <input
                v-model.number="form.amount"
                type="number"
                placeholder="0"
                class="h-9 w-full rounded-lg border border-border px-2.5 text-sm tabular-nums focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>

          <div v-else class="overflow-y-auto px-6 py-5 space-y-3 pointer-events-none select-none">
            <div>
              <p class="text-xs text-muted">Kode Budget</p>
              <p class="text-sm font-medium">{{ form.budget_code }}</p>
            </div>
            <div>
              <p class="text-xs text-muted">Kelompok Kegiatan</p>
              <p class="text-sm font-medium">{{ form.item_group }}</p>
            </div>
            <div>
              <p class="text-xs text-muted">Rincian Kebutuhan</p>
              <p class="text-sm font-medium">{{ form.item_name }}</p>
            </div>
            <div>
              <p class="text-xs text-muted">Nilai Anggaran</p>
              <p class="text-sm font-medium">{{ formatIdr(form.amount) }}</p>
            </div>
            <div class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-3 py-2 text-xs text-red-700 dark:text-red-400">
              ⚠ Data anggaran ini akan dihapus setelah disetujui supervisor. Tindakan tidak dapat dibatalkan.
            </div>
          </div>

          <!-- Footer -->
          <div class="border-t border-border px-6 py-3 shrink-0 flex justify-end gap-2">
            <Button variant="outline" size="sm" @click="closeModal">Batal</Button>
            <button
              v-if="modalMode === 'delete'"
              type="button"
              class="inline-flex items-center gap-1.5 rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 transition-colors"
              @click="submitDelete"
            >
              Hapus & Submit Otorisasi
            </button>
            <Button v-else size="sm" @click="submitForm">
              {{ modalMode === 'create' ? 'Simpan Anggaran' : 'Ubah Anggaran' }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

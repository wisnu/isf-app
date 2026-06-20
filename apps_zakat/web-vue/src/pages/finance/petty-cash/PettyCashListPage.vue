<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, Wallet, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import PageHeader from '@/components/layout/PageHeader.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface PettyCashRow {
  account_no: string
  account_name: string | null
  cash_code: string | null
  branch_code: string | null
  currency_code: string | null
  balance: number | null
  status: string | null
}

interface PettyCashList {
  rows: PettyCashRow[]
  pagination: { page: number; page_size: number; total: number; total_pages: number }
}

interface PettyCashDetail {
  account_no: string
  account_name: string | null
  cash_code: string | null
  account_interface: string | null
  currency_code: string | null
  branch_code: string | null
  balance: number | null
  status: string | null
  opening_date: string | null
}

interface SelectOption { value: string; label: string }

const router = useRouter()
const toast = useToast()
const pageSize = shallowRef(20)

// ── List data ─────────────────────────────────────────────────────────────────

const rows = ref<PettyCashRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRecords = shallowRef(0)

const searchInput = ref('')
let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadAccounts() }, 400)
})

async function loadAccounts() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    const res = await api.get<PettyCashList>(`/api/petty-cash/accounts?${params}`)
    rows.value = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRecords.value = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data rekening kas kecil'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function prevPage() { if (page.value > 1) { page.value--; loadAccounts() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadAccounts() } }
function changePageSize(size: number) { pageSize.value = size; page.value = 1; loadAccounts() }

// ── Lookups ───────────────────────────────────────────────────────────────────

const lookupBranches = ref<SelectOption[]>([])
const lookupCurrencies = ref<SelectOption[]>([])
const lookupGlAccounts = ref<SelectOption[]>([])
const lookupLoaded = shallowRef(false)

async function loadLookups() {
  if (lookupLoaded.value) return
  try {
    const [branches, currencies, gl] = await Promise.all([
      api.get<{ data: { branch_code: string; branch_name: string | null }[] }>('/api/petty-cash/lookup/branches'),
      api.get<{ data: { currency_code: string; short_name: string | null }[] }>('/api/petty-cash/lookup/currencies'),
      api.get<{ data: { account_code: string; account_name: string | null }[] }>('/api/petty-cash/lookup/gl_accounts'),
    ])
    lookupBranches.value = (branches.data ?? []).map((b) => ({
      value: b.branch_code,
      label: `${b.branch_code} — ${b.branch_name ?? ''}`,
    }))
    lookupCurrencies.value = (currencies.data ?? []).map((c) => ({
      value: c.currency_code,
      label: `${c.currency_code}${c.short_name && c.short_name !== c.currency_code ? ' — ' + c.short_name : ''}`,
    }))
    lookupGlAccounts.value = (gl.data ?? []).map((a) => ({
      value: a.account_code,
      label: `${a.account_code} — ${a.account_name ?? ''}`,
    }))
    lookupLoaded.value = true
  } catch {
    toast.error('Gagal memuat data referensi')
  }
}

// ── Modal state ───────────────────────────────────────────────────────────────

const modalOpen = shallowRef(false)
const modalMode = shallowRef<'edit' | 'delete'>('edit')
const modalLoading = shallowRef(false)
const editingAccountNo = shallowRef<string | null>(null)
const submitting = shallowRef(false)
const formError = shallowRef<string | null>(null)

const form = reactive({
  account_name: '',
  branch_code: '',
  currency_code: '',
  account_interface: '',
  cash_code: '',
  opening_date: '',
})

// For delete view — loaded detail
const deleteDetail = ref<PettyCashDetail | null>(null)

function resetForm() {
  form.account_name = ''
  form.branch_code = ''
  form.currency_code = ''
  form.account_interface = ''
  form.cash_code = ''
  form.opening_date = ''
}

async function openEdit(accountNo: string) {
  modalMode.value = 'edit'
  editingAccountNo.value = accountNo
  resetForm()
  formError.value = null
  modalOpen.value = true
  modalLoading.value = true
  await loadLookups()
  try {
    const res = await api.get<PettyCashDetail>(`/api/petty-cash/accounts/${accountNo}`)
    form.account_name = res.account_name ?? ''
    form.branch_code = res.branch_code ?? ''
    form.currency_code = res.currency_code ?? ''
    form.account_interface = res.account_interface ?? ''
    form.cash_code = res.cash_code ?? ''
    form.opening_date = res.opening_date ?? ''
  } catch {
    toast.error('Gagal memuat detail rekening')
    modalOpen.value = false
  } finally {
    modalLoading.value = false
  }
}

async function openDelete(accountNo: string) {
  modalMode.value = 'delete'
  editingAccountNo.value = accountNo
  deleteDetail.value = null
  formError.value = null
  modalOpen.value = true
  modalLoading.value = true
  try {
    const res = await api.get<PettyCashDetail>(`/api/petty-cash/accounts/${accountNo}`)
    deleteDetail.value = res
  } catch {
    toast.error('Gagal memuat detail rekening')
    modalOpen.value = false
  } finally {
    modalLoading.value = false
  }
}

function closeModal() {
  modalOpen.value = false
  editingAccountNo.value = null
  deleteDetail.value = null
  formError.value = null
}

// ── Validation ────────────────────────────────────────────────────────────────

function validateForm(): string | null {
  if (!form.account_name.trim()) return 'Nama Rekening wajib diisi'
  if (!form.account_interface) return 'GL Interface wajib dipilih'
  return null
}

// ── Submit create / edit ──────────────────────────────────────────────────────

async function submitForm() {
  formError.value = null
  const err = validateForm()
  if (err) { formError.value = err; toast.error(err); return }

  submitting.value = true
  try {
    await api.put<unknown>(`/api/petty-cash/accounts/${editingAccountNo.value}`, {
      account_name: form.account_name.trim(),
      account_interface: form.account_interface,
      currency_code: form.currency_code,
      cash_code: form.cash_code.trim() || null,
      opening_date: form.opening_date || null,
    })
    toast.success('Rekening kas kecil berhasil diperbarui')
    closeModal()
    await loadAccounts()
  } catch (e: unknown) {
    const msg = e instanceof ApiError ? e.message : 'Gagal menyimpan data'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}

// ── Submit delete ─────────────────────────────────────────────────────────────

async function submitDelete() {
  submitting.value = true
  formError.value = null
  try {
    await api.delete<unknown>(`/api/petty-cash/accounts/${editingAccountNo.value}`)
    toast.success('Rekening kas kecil berhasil dihapus')
    closeModal()
    await loadAccounts()
  } catch (e: unknown) {
    const msg = e instanceof ApiError ? e.message : 'Gagal menghapus rekening'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}

onMounted(loadAccounts)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Rekening Kas Kecil" subtitle="Daftar rekening petty cash milik LAZ">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="router.push({ name: 'finance-petty-cash-create' })">
          <Plus class="w-3.5 h-3.5" />
          Tambah Rekening
        </Button>
      </template>
    </PageHeader>

    <!-- Stats cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Jumlah Rekening</p>
          <p class="text-2xl font-bold tabular-nums">{{ totalRecords }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Total Saldo IDR</p>
          <p class="text-2xl font-bold tabular-nums text-positive">
            {{ formatIdr(rows.filter(r => r.currency_code === 'IDR').reduce((s, r) => s + (r.balance ?? 0), 0)) }}
          </p>
        </CardContent>
      </Card>
    </div>

    <!-- Error -->
    <div
      v-if="errorMsg"
      class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-4 py-3 text-sm text-red-700 dark:text-red-400"
    >
      <strong>Error:</strong> {{ errorMsg }}
    </div>

    <!-- 3-part table layout -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center gap-3">
        <div class="relative">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted pointer-events-none" />
          <input
            v-model="searchInput"
            placeholder="Cari kode, nama rekening..."
            class="h-8 pl-8 pr-3 rounded border border-border bg-background text-[11px] w-64 focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
      </div>

      <!-- Pagination (top) -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="loading">Memuat...</template>
          <template v-else-if="totalRecords > 0">
            {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRecords) }}
            dari {{ totalRecords }} rekening
          </template>
          <template v-else>Tidak ada rekening</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRecords"
          :page-size="pageSize"
          :loading="loading"
          unit="rekening"
          @prev="prevPage"
          @next="nextPage"
          @update:page-size="changePageSize"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
            <tr>
              <th class="px-4 py-2 font-medium text-left">No. Rekening</th>
              <th class="px-4 py-2 font-medium text-left">Nama Rekening</th>
              <th class="px-4 py-2 font-medium text-left">Kode Kas</th>
              <th class="px-4 py-2 font-medium text-left">Cabang</th>
              <th class="px-4 py-2 font-medium text-left">Valuta</th>
              <th class="px-4 py-2 font-medium text-right">Saldo</th>
              <th class="px-4 py-2 font-medium text-center">Status</th>
              <th class="px-4 py-2 font-medium text-left">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="8" class="px-4 py-8 text-center text-muted">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="8" class="px-4 py-8 text-center text-muted italic">Tidak ada rekening kas kecil yang ditemukan.</td>
            </tr>
            <tr
              v-for="r in rows"
              :key="r.account_no"
              class="border-b border-border last:border-0 hover:bg-background/60"
            >
              <td class="px-4 py-1 font-mono tabular-nums whitespace-nowrap text-muted">{{ r.account_no }}</td>
              <td class="px-4 py-1">{{ r.account_name ?? '—' }}</td>
              <td class="px-4 py-1 font-mono text-muted">{{ r.cash_code ?? '—' }}</td>
              <td class="px-4 py-1 text-muted">{{ r.branch_code ?? '—' }}</td>
              <td class="px-4 py-1">
                <span class="inline-block text-[10px] font-semibold px-1.5 py-px rounded bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
                  {{ r.currency_code ?? '—' }}
                </span>
              </td>
              <td class="px-4 py-1 text-right tabular-nums whitespace-nowrap font-medium">
                <template v-if="r.currency_code === 'IDR'">
                  {{ r.balance != null ? formatIdr(r.balance) : '—' }}
                </template>
                <template v-else>
                  {{ r.balance != null ? r.balance.toLocaleString('id-ID', { minimumFractionDigits: 2 }) : '—' }}
                </template>
              </td>
              <td class="px-4 py-1 text-center">
                <span
                  v-if="r.status === 'A'"
                  class="inline-block text-[10px] font-semibold px-1.5 py-px rounded bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"
                >Aktif</span>
                <span
                  v-else
                  class="inline-block text-[10px] font-semibold px-1.5 py-px rounded bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400"
                >Non-aktif</span>
              </td>
              <td class="px-4 py-1">
                <div class="flex items-center gap-1">
                  <Tooltip side="top">
                    <template #trigger>
                      <button
                        class="p-1.5 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                        @click="openEdit(r.account_no)"
                      >
                        <Pencil class="w-3.5 h-3.5" />
                      </button>
                    </template>
                    Ubah
                  </Tooltip>
                  <Tooltip side="top">
                    <template #trigger>
                      <button
                        class="p-1.5 rounded hover:bg-red-50 text-muted-foreground hover:text-red-600 transition-colors"
                        @click="openDelete(r.account_no)"
                      >
                        <Trash2 class="w-3.5 h-3.5" />
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

    <!-- Modal -->
    <Teleport to="body">
      <div
        v-if="modalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
        @click.self="closeModal"
      >
        <div class="w-full max-w-xl rounded-xl border border-border bg-surface shadow-xl flex flex-col max-h-[90vh]">

          <!-- Header -->
          <div class="flex items-center justify-between border-b border-border px-6 py-4 shrink-0">
            <div>
              <h2 class="text-base font-semibold" :class="modalMode === 'delete' ? 'text-red-700' : ''">
                <template v-if="modalMode === 'edit'">
                  <Wallet class="inline w-4 h-4 mr-1.5 align-text-bottom text-primary" />
                  Edit Rekening — {{ editingAccountNo }}
                </template>
                <template v-else>
                  ⚠ Konfirmasi Hapus — {{ editingAccountNo }}
                </template>
              </h2>
              <p class="text-[11px] mt-0.5" :class="modalMode === 'delete' ? 'text-red-500' : 'text-muted'">
                <template v-if="modalMode === 'delete'">Periksa data berikut sebelum menghapus</template>
                <template v-else>Ubah data rekening kas kecil</template>
              </p>
            </div>
            <button
              type="button"
              class="rounded-lg p-1.5 text-muted hover:bg-background hover:text-foreground transition-colors"
              @click="closeModal"
            >
              <X class="w-4 h-4" />
            </button>
          </div>

          <!-- Loading skeleton -->
          <div v-if="modalLoading" class="overflow-y-auto px-6 py-5 space-y-4">
            <div v-for="i in 4" :key="i" class="space-y-1.5">
              <div class="h-3 w-24 rounded bg-muted/20 animate-pulse" />
              <div class="h-9 w-full rounded-lg bg-muted/10 animate-pulse" />
            </div>
          </div>

          <!-- Delete: read-only view -->
          <div v-else-if="modalMode === 'delete' && deleteDetail" class="overflow-y-auto px-6 py-5 space-y-3">
            <dl class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">No. Rekening</dt>
                <dd class="font-mono text-[12px]">{{ deleteDetail.account_no }}</dd>
              </div>
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">Nama Rekening</dt>
                <dd class="text-[12px]">{{ deleteDetail.account_name ?? '—' }}</dd>
              </div>
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">Cabang</dt>
                <dd class="text-[12px]">{{ deleteDetail.branch_code ?? '—' }}</dd>
              </div>
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">Valuta</dt>
                <dd class="text-[12px]">{{ deleteDetail.currency_code ?? '—' }}</dd>
              </div>
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">GL Interface</dt>
                <dd class="font-mono text-[12px]">{{ deleteDetail.account_interface ?? '—' }}</dd>
              </div>
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">Kode Kas</dt>
                <dd class="font-mono text-[12px]">{{ deleteDetail.cash_code ?? '—' }}</dd>
              </div>
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">Saldo</dt>
                <dd class="tabular-nums font-medium text-[12px]">
                  {{ deleteDetail.balance != null ? formatIdr(deleteDetail.balance) : '—' }}
                </dd>
              </div>
              <div>
                <dt class="text-[10px] font-medium uppercase tracking-wide text-muted">Tgl Buka</dt>
                <dd class="text-[12px]">{{ dmy(deleteDetail.opening_date) || '—' }}</dd>
              </div>
            </dl>

            <div class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-3 py-2 text-xs text-red-700 dark:text-red-400">
              ⚠ Apakah Anda yakin ingin menghapus rekening ini? Tindakan ini tidak dapat dibatalkan.
            </div>
          </div>

          <!-- Edit: form -->
          <div v-else-if="modalMode === 'edit'" class="overflow-y-auto px-6 py-5 space-y-4">
            <!-- No. Rekening (read-only) -->
            <div>
              <label class="mb-1 block text-xs font-medium text-muted">No. Rekening</label>
              <input
                :value="editingAccountNo ?? ''"
                disabled
                class="h-9 w-full rounded-lg border border-border bg-muted/10 px-2.5 text-sm font-mono text-muted cursor-not-allowed"
              />
            </div>

            <!-- Nama Rekening -->
            <div>
              <label class="mb-1 block text-xs font-medium">
                Nama Rekening <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.account_name"
                placeholder="mis. Petty Cash Operasional"
                class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>

            <!-- Cabang + Valuta -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="mb-1 block text-xs font-medium text-muted">
                  Cabang <span class="ml-1 text-[10px] text-muted">(tidak bisa diubah)</span>
                </label>
                <SearchSelect
                  v-model="form.branch_code"
                  :options="lookupBranches"
                  placeholder="Pilih cabang..."
                  :disabled="true"
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium text-muted">
                  Valuta <span class="ml-1 text-[10px] text-muted">(tidak bisa diubah)</span>
                </label>
                <SearchSelect
                  v-model="form.currency_code"
                  :options="lookupCurrencies"
                  placeholder="Pilih valuta..."
                  :disabled="true"
                />
              </div>
            </div>

            <!-- GL Interface + Kode Kas -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="mb-1 block text-xs font-medium">
                  GL Interface <span class="text-red-500">*</span>
                </label>
                <SearchSelect
                  v-model="form.account_interface"
                  :options="lookupGlAccounts"
                  placeholder="Cari akun GL..."
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium text-muted">
                  Kode Kas <span class="text-muted">(opsional)</span>
                </label>
                <input
                  v-model="form.cash_code"
                  placeholder="Kode kas unik (opsional)"
                  class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <!-- Tgl Buka -->
            <div>
              <label class="mb-1 block text-xs font-medium">Tgl Buka</label>
              <DateField v-model="form.opening_date" />
            </div>
          </div>

          <!-- Footer -->
          <div class="border-t border-border px-6 py-3 shrink-0 space-y-2">
            <div
              v-if="formError"
              class="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700 dark:bg-red-900/10 dark:border-red-800 dark:text-red-400"
            >
              {{ formError }}
            </div>
            <div class="flex justify-end gap-2">
              <Button variant="outline" size="sm" :disabled="submitting" @click="closeModal">
                Batal
              </Button>
              <!-- Delete: tombol merah -->
              <button
                v-if="modalMode === 'delete'"
                type="button"
                class="inline-flex items-center gap-1.5 rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50 transition-colors"
                :disabled="submitting || modalLoading"
                @click="submitDelete"
              >
                {{ submitting ? 'Menghapus...' : 'Hapus Rekening' }}
              </button>
              <Button v-else size="sm" :disabled="submitting || modalLoading" @click="submitForm">
                {{ submitting ? 'Menyimpan...' : 'Simpan Perubahan' }}
              </Button>
            </div>
          </div>

        </div>
      </div>
    </Teleport>
  </div>
</template>

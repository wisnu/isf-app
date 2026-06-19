<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { computed, onMounted, onUnmounted, reactive, ref, shallowRef, watch } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'
import { formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BankAccountRow {
  account_no: string
  account_name: string | null
  bank_name: string | null
  bank_account_no: string | null
  branch_code: string | null
  currency_code: string | null
  balance: number | null
  status: string | null
}

interface BankAccountList {
  rows: BankAccountRow[]
  pagination: { page: number; page_size: number; total: number; total_pages: number }
}

interface BankAccountDetail {
  account_no: string
  account_name: string | null
  bank_name: string | null
  bank_code: string | null
  bank_account_no: string | null
  branch_code: string | null
  currency_code: string | null
  balance: number | null
  account_interface: string | null
  opening_date: string | null
  is_amil_account: boolean
  product_id: number | null
  cash_code: string | null
  status: string | null
}

interface SelectOption { value: string; label: string }

const toast = useToast()
const pageSize = shallowRef(25)

// ── List data ─────────────────────────────────────────────────────────────────

const rows = ref<BankAccountRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const totalPages = shallowRef(1)
const totalRecords = shallowRef(0)

const totalSaldoIdr = computed(() =>
  rows.value
    .filter((r) => r.currency_code === 'IDR')
    .reduce((s, r) => s + (r.balance ?? 0), 0),
)

const searchInput = ref('')
let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(searchInput, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; loadBankAccounts() }, 300)
})

async function loadBankAccounts() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({ page: String(page.value), page_size: String(pageSize.value) })
    if (searchInput.value.trim()) params.set('search', searchInput.value.trim())
    const res = await api.get<BankAccountList>(`/api/bank/accounts?${params}`)
    rows.value = res.rows
    totalPages.value = res.pagination.total_pages || 1
    totalRecords.value = res.pagination.total
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data rekening bank'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function prevPage() { if (page.value > 1) { page.value--; loadBankAccounts() } }
function nextPage() { if (page.value < totalPages.value) { page.value++; loadBankAccounts() } }
function changePageSize(size: number) { pageSize.value = size; page.value = 1; loadBankAccounts() }

// ── Submissions ───────────────────────────────────────────────────────────────


// ── Lookup data ───────────────────────────────────────────────────────────────

const lookupBanks = ref<SelectOption[]>([])
const lookupBranches = ref<SelectOption[]>([])
const lookupCurrencies = ref<SelectOption[]>([])
const lookupGlAccounts = ref<SelectOption[]>([])
const lookupProducts = ref<SelectOption[]>([])
const lookupLoaded = shallowRef(false)

async function loadLookups() {
  if (lookupLoaded.value) return
  try {
    const [banks, branches, currencies, gl, products] = await Promise.all([
      api.get<{ data: { bank_code: string; bank_short_name: string | null; bank_name: string | null }[] }>('/api/bank/lookup/banks'),
      api.get<{ data: { branch_code: string; branch_name: string | null }[] }>('/api/bank/lookup/branches'),
      api.get<{ data: { currency_code: string; short_name: string | null }[] }>('/api/bank/lookup/currencies'),
      api.get<{ data: { account_code: string; account_name: string | null }[] }>('/api/bank/lookup/gl_accounts'),
      api.get<{ data: { product_id: number; product_code: string | null; product_name: string | null }[] }>('/api/bank/lookup/products'),
    ])
    lookupBanks.value = (banks.data ?? []).map((b) => ({
      value: b.bank_code,
      label: b.bank_short_name ? `${b.bank_code} — ${b.bank_short_name}` : b.bank_code,
    }))
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
    lookupProducts.value = (products.data ?? []).map((p) => ({
      value: String(p.product_id),
      label: p.product_code ? `${p.product_code} — ${p.product_name ?? ''}` : String(p.product_id),
    }))
    lookupLoaded.value = true
  } catch {
    toast.error('Gagal memuat data referensi')
  }
}

// ── Drawer state ──────────────────────────────────────────────────────────────

const modalOpen = shallowRef(false)
const drawerMode = shallowRef<'create' | 'edit' | 'delete'>('create')
const drawerLoading = shallowRef(false)
const editingAccountNo = shallowRef<string | null>(null)
const submitting = shallowRef(false)
const formError = shallowRef<string | null>(null)

const form = reactive({
  account_name: '',
  bank_account_no: '',
  bank_code: '',
  branch_code: '',
  currency_code: '',
  account_interface: '',
  opening_date: '',
  is_amil_account: false,
  product_id: '',
  cash_code: '',
})

function resetForm() {
  form.account_name = ''
  form.bank_account_no = ''
  form.bank_code = ''
  form.branch_code = ''
  form.currency_code = ''
  form.account_interface = ''
  form.opening_date = ''
  form.is_amil_account = false
  form.product_id = ''
  form.cash_code = ''
}

async function openCreate() {
  drawerMode.value = 'create'
  editingAccountNo.value = null
  resetForm()
  modalOpen.value = true
  await loadLookups()
}

async function openEdit(accountNo: string) {
  drawerMode.value = 'edit'
  editingAccountNo.value = accountNo
  resetForm()
  modalOpen.value = true
  drawerLoading.value = true
  try {
    const [res] = await Promise.all([
      api.get<BankAccountDetail>(`/api/bank/accounts/${accountNo}`),
      loadLookups(),
    ])
    form.account_name = res.account_name ?? ''
    form.bank_account_no = res.bank_account_no ?? ''
    form.bank_code = res.bank_code ?? ''
    form.branch_code = res.branch_code ?? ''
    form.currency_code = res.currency_code ?? ''
    form.account_interface = res.account_interface ?? ''
    form.opening_date = res.opening_date ?? ''
    form.is_amil_account = res.is_amil_account ?? false
    form.product_id = res.product_id != null ? String(res.product_id) : ''
    form.cash_code = res.cash_code ?? ''
  } catch {
    toast.error('Gagal memuat detail rekening')
    modalOpen.value = false
  } finally {
    drawerLoading.value = false
  }
}

function closeDrawer() {
  modalOpen.value = false
  editingAccountNo.value = null
  formError.value = null
}

watch(() => form.is_amil_account, (val) => {
  if (val) form.product_id = ''
})

function validateForm(): string | null {
  if (!form.account_name.trim()) return 'Nama Rekening wajib diisi'
  if (!form.bank_account_no.trim()) return 'No Rekening Bank wajib diisi'
  if (form.bank_account_no.trim().length < 8) return 'No Rekening Bank minimal 8 karakter'
  if (!form.bank_code) return 'Nama Bank wajib dipilih'
  if (!form.branch_code) return 'Cabang BPZIS wajib dipilih'
  if (!form.currency_code) return 'Valuta wajib dipilih'
  if (!form.account_interface) return 'GL Interface wajib dipilih'
  return null
}

async function submitForm() {
  formError.value = null
  const validationErr = validateForm()
  if (validationErr) {
    formError.value = validationErr
    toast.error(validationErr)
    return
  }

  submitting.value = true
  try {
    const payload = {
      action: drawerMode.value === 'create' ? 'create' : 'edit',
      ...(drawerMode.value === 'edit' ? { account_no: editingAccountNo.value } : {}),
      account_name: form.account_name.trim(),
      bank_account_no: form.bank_account_no.trim(),
      bank_code: form.bank_code,
      bank_name: lookupBanks.value.find(b => b.value === form.bank_code)?.label ?? form.bank_code,
      branch_code: form.branch_code,
      branch_name: lookupBranches.value.find(b => b.value === form.branch_code)?.label ?? form.branch_code,
      currency_code: form.currency_code,
      account_interface: form.account_interface,
      opening_date: form.opening_date || null,
      is_amil_account: form.is_amil_account,
      product_id: form.is_amil_account || !form.product_id ? null : Number(form.product_id),
      cash_code: form.cash_code.trim() || null,
    }
    await api.post('/api/otorisasi/save-and-submit/', {
      entity_type: 'bank',
      module: 'keuangan',
      payload,
    })
    toast.success(
      drawerMode.value === 'create'
        ? 'Permintaan tambah rekening dikirim untuk otorisasi'
        : 'Permintaan ubah rekening dikirim untuk otorisasi',
    )
    closeDrawer()
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Gagal mengirim submission'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}

// ── Delete — buka modal read-only berisi data lengkap ────────────────────────

async function openDelete(accountNo: string) {
  drawerMode.value = 'delete'
  editingAccountNo.value = accountNo
  resetForm()
  modalOpen.value = true
  drawerLoading.value = true
  try {
    const [res] = await Promise.all([
      api.get<BankAccountDetail>(`/api/bank/accounts/${accountNo}`),
      loadLookups(),
    ])
    form.account_name = res.account_name ?? ''
    form.bank_account_no = res.bank_account_no ?? ''
    form.bank_code = res.bank_code ?? ''
    form.branch_code = res.branch_code ?? ''
    form.currency_code = res.currency_code ?? ''
    form.account_interface = res.account_interface ?? ''
    form.opening_date = res.opening_date ?? ''
    form.is_amil_account = res.is_amil_account ?? false
    form.product_id = res.product_id != null ? String(res.product_id) : ''
    form.cash_code = res.cash_code ?? ''
  } catch {
    toast.error('Gagal memuat detail rekening')
    modalOpen.value = false
  } finally {
    drawerLoading.value = false
  }
}

async function submitDelete() {
  submitting.value = true
  try {
    await api.post('/api/otorisasi/save-and-submit/', {
      entity_type: 'bank',
      module: 'keuangan',
      payload: { action: 'delete', account_no: editingAccountNo.value },
    })
    toast.success('Permintaan hapus rekening dikirim untuk otorisasi')
    closeDrawer()
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Gagal mengirim permintaan hapus'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}

onMounted(loadBankAccounts)
onUnmounted(() => { if (searchTimer) clearTimeout(searchTimer) })
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Rekening Bank" subtitle="Daftar rekening bank milik LAZ">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="openCreate">
          <Plus class="w-3.5 h-3.5" />
          Tambah Rekening
        </Button>
      </template>
    </PageHeader>

    <!-- Stats cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Total Saldo IDR</p>
          <p class="text-2xl font-bold tabular-nums text-positive">{{ formatIdr(totalSaldoIdr) }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Jumlah Rekening</p>
          <p class="text-2xl font-bold tabular-nums">{{ totalRecords }}</p>
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
            placeholder="Cari kode, nama rekening, bank..."
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
              <th class="px-4 py-2 font-medium text-left">Kode Rekening</th>
              <th class="px-4 py-2 font-medium text-left">Nama Rekening</th>
              <th class="px-4 py-2 font-medium text-left">Nama Bank</th>
              <th class="px-4 py-2 font-medium text-left">No Rekening Bank</th>
              <th class="px-4 py-2 font-medium text-left">Cabang</th>
              <th class="px-4 py-2 font-medium text-left">Valuta</th>
              <th class="px-4 py-2 font-medium text-right">Saldo</th>
              <th class="px-4 py-2 font-medium text-center">Status</th>
              <th class="px-4 py-2 font-medium text-left">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="9" class="px-4 py-8 text-center text-muted">Memuat...</td>
            </tr>
            <tr v-else-if="rows.length === 0">
              <td colspan="9" class="px-4 py-8 text-center text-muted italic">Tidak ada rekening bank yang ditemukan.</td>
            </tr>
            <tr
              v-for="r in rows"
              :key="r.account_no"
              class="border-b border-border last:border-0 hover:bg-background/60"
            >
              <td class="px-4 py-1 font-mono tabular-nums whitespace-nowrap text-muted">{{ r.account_no }}</td>
              <td class="px-4 py-1">{{ r.account_name ?? '—' }}</td>
              <td class="px-4 py-1">{{ r.bank_name ?? '—' }}</td>
              <td class="px-4 py-1 font-mono tabular-nums whitespace-nowrap text-muted">{{ r.bank_account_no ?? '—' }}</td>
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

    <!-- Form Drawer -->
    <Teleport to="body">
      <div
        v-if="modalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
        @click.self="closeDrawer"
      >
        <div class="w-full max-w-2xl rounded-xl border border-border bg-surface shadow-xl flex flex-col max-h-[90vh]">
          <!-- Modal header -->
          <div class="flex items-center justify-between border-b border-border px-6 py-4 shrink-0">
            <div>
              <h2 class="text-base font-semibold" :class="drawerMode === 'delete' ? 'text-red-700' : ''">
                {{ drawerMode === 'create' ? 'Tambah Rekening Bank'
                 : drawerMode === 'edit'   ? `Edit Rekening — ${editingAccountNo}`
                 :                           `Konfirmasi Hapus — ${editingAccountNo}` }}
              </h2>
              <p class="text-[11px] mt-0.5" :class="drawerMode === 'delete' ? 'text-red-500' : 'text-muted'">
                {{ drawerMode === 'delete' ? 'Periksa data berikut sebelum menghapus' : 'Permintaan akan diproses melalui otorisasi' }}
              </p>
            </div>
            <button
              type="button"
              class="rounded-lg p-1.5 text-muted hover:bg-background hover:text-foreground transition-colors"
              @click="closeDrawer"
            >
              <X class="w-4 h-4" />
            </button>
          </div>

          <!-- Loading skeleton (edit mode) -->
          <div v-if="drawerLoading" class="overflow-y-auto px-6 py-5 space-y-4">
            <div v-for="i in 4" :key="i" class="space-y-1.5">
              <div class="h-3 w-24 rounded bg-muted/20 animate-pulse" />
              <div class="h-9 w-full rounded-lg bg-muted/10 animate-pulse" />
            </div>
          </div>

          <!-- Form body -->
          <div v-else class="overflow-y-auto px-6 py-5 space-y-4" :class="{ 'pointer-events-none select-none': drawerMode === 'delete' }">
            <!-- Baris 1: Nama Rekening + No Rekening Bank -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="mb-1 block text-xs font-medium">
                  Nama Rekening <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.account_name"
                  placeholder="mis. ZAKAT FITRAH"
                  class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium">
                  No Rekening Bank <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="form.bank_account_no"
                  placeholder="min. 8 karakter"
                  class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
            </div>

            <!-- Baris 2: Nama Bank + Cabang BPZIS -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="mb-1 block text-xs font-medium">
                  Nama Bank <span class="text-red-500">*</span>
                </label>
                <SearchSelect
                  v-model="form.bank_code"
                  :options="lookupBanks"
                  placeholder="Pilih bank..."
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium">
                  Cabang BPZIS <span class="text-red-500">*</span>
                </label>
                <SearchSelect
                  v-model="form.branch_code"
                  :options="lookupBranches"
                  placeholder="Pilih cabang..."
                />
              </div>
            </div>

            <!-- Baris 3: Valuta + GL Interface -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="mb-1 block text-xs font-medium">
                  Valuta <span class="text-red-500">*</span>
                </label>
                <SearchSelect
                  v-model="form.currency_code"
                  :options="lookupCurrencies"
                  placeholder="Pilih valuta..."
                />
              </div>
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
            </div>

            <!-- Baris 4: Tgl Buka + Rekening Amil -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 items-end">
              <div>
                <label class="mb-1 block text-xs font-medium">Tgl Buka</label>
                <DateField v-model="form.opening_date" />
              </div>
              <div class="flex items-center gap-2 pb-1">
                <input
                  id="is-amil"
                  v-model="form.is_amil_account"
                  type="checkbox"
                  class="rounded"
                />
                <label for="is-amil" class="text-sm cursor-pointer select-none">
                  Rekening Amil?
                </label>
              </div>
            </div>

            <!-- Baris 5: Default Produk + Kode Kas -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label
                  class="mb-1 block text-xs font-medium"
                  :class="{ 'opacity-40': form.is_amil_account }"
                >
                  Default Produk / Program
                </label>
                <SearchSelect
                  v-model="form.product_id"
                  :options="lookupProducts"
                  :all-label="'— Tidak ada —'"
                  placeholder="Pilih produk..."
                  :class="{ 'opacity-40 pointer-events-none': form.is_amil_account }"
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

            <!-- Warning delete mode -->
            <div
              v-if="drawerMode === 'delete'"
              class="rounded-lg border border-red-200 bg-red-50 dark:bg-red-900/10 dark:border-red-800 px-3 py-2 text-xs text-red-700 dark:text-red-400"
            >
              ⚠ Data rekening ini akan dihapus setelah disetujui supervisor. Tindakan tidak dapat dibatalkan.
            </div>
            <p v-else class="text-[10px] text-muted">
              Permintaan ini akan masuk sistem otorisasi. Rekening aktif setelah disetujui supervisor.
            </p>
          </div>

          <!-- Modal footer -->
          <div class="border-t border-border px-6 py-3 shrink-0 space-y-2">
            <div
              v-if="formError"
              class="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700 dark:bg-red-900/10 dark:border-red-800 dark:text-red-400"
            >
              {{ formError }}
            </div>
            <div class="flex justify-end gap-2">
              <Button variant="outline" size="sm" :disabled="submitting" @click="closeDrawer">
                Batal
              </Button>
              <!-- Delete mode: tombol merah + fungsi berbeda -->
              <button
                v-if="drawerMode === 'delete'"
                type="button"
                class="inline-flex items-center gap-1.5 rounded-md bg-red-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-red-700 disabled:opacity-50 transition-colors"
                :disabled="submitting || drawerLoading"
                @click="submitDelete"
              >
                {{ submitting ? 'Mengirim...' : 'Hapus & Submit Otorisasi' }}
              </button>
              <Button v-else size="sm" :disabled="submitting || drawerLoading" @click="submitForm">
                {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
              </Button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>


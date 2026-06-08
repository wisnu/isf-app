<script setup lang="ts">
import { Pencil, Plus, Search, Trash2, X } from 'lucide-vue-next'
import Column from 'primevue/column'
import { computed, onMounted, reactive, ref, shallowRef, watch } from 'vue'

import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import AppDataTable from '@/components/ui/AppDataTable.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
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

interface BankSubmission {
  id: number
  status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED'
  payload: Record<string, unknown>
}

interface SelectOption { value: string; label: string }

const toast = useToast()
const PAGE_SIZE = 25

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
    const params = new URLSearchParams({ page: String(page.value), page_size: String(PAGE_SIZE) })
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

// ── Submissions ───────────────────────────────────────────────────────────────

const submissions = ref<BankSubmission[]>([])

async function loadSubmissions() {
  try {
    const res = await api.get<{ rows: BankSubmission[] }>('/api/otorisasi/my-submissions/?entity_type=bank')
    submissions.value = res.rows ?? []
  } catch { /* silent */ }
}

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

const drawerOpen = shallowRef(false)
const drawerMode = shallowRef<'create' | 'edit'>('create')
const drawerLoading = shallowRef(false)
const editingAccountNo = shallowRef<string | null>(null)
const submitting = shallowRef(false)

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
  drawerOpen.value = true
  await loadLookups()
}

async function openEdit(accountNo: string) {
  drawerMode.value = 'edit'
  editingAccountNo.value = accountNo
  resetForm()
  drawerOpen.value = true
  drawerLoading.value = true
  await loadLookups()
  try {
    const res = await api.get<BankAccountDetail>(`/api/bank/accounts/${accountNo}`)
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
    drawerOpen.value = false
  } finally {
    drawerLoading.value = false
  }
}

function closeDrawer() {
  drawerOpen.value = false
  editingAccountNo.value = null
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
  const err = validateForm()
  if (err) { toast.error(err); return }

  submitting.value = true
  try {
    const payload = {
      action: drawerMode.value === 'create' ? 'create' : 'edit',
      ...(drawerMode.value === 'edit' ? { account_no: editingAccountNo.value } : {}),
      account_name: form.account_name.trim(),
      bank_account_no: form.bank_account_no.trim(),
      bank_code: form.bank_code,
      branch_code: form.branch_code,
      currency_code: form.currency_code,
      account_interface: form.account_interface,
      opening_date: form.opening_date || null,
      is_amil_account: form.is_amil_account,
      product_id: form.is_amil_account || !form.product_id ? null : Number(form.product_id),
      cash_code: form.cash_code.trim() || null,
    }
    await api.post('/api/otorisasi/submission/', {
      entity_type: 'bank',
      module: 'keuangan',
      payload,
    })
    toast.success(
      drawerMode.value === 'create'
        ? 'Permintaan tambah rekening disubmit untuk otorisasi'
        : 'Permintaan ubah rekening disubmit untuk otorisasi',
    )
    closeDrawer()
    await loadSubmissions()
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal mengirim submission')
  } finally {
    submitting.value = false
  }
}

// ── Delete ────────────────────────────────────────────────────────────────────

const deletingAccountNo = shallowRef<string | null>(null)
const deleteSubmitting = shallowRef(false)

async function confirmDelete(accountNo: string) {
  deleteSubmitting.value = true
  try {
    await api.post('/api/otorisasi/submission/', {
      entity_type: 'bank',
      module: 'keuangan',
      payload: { action: 'delete', account_no: accountNo },
    })
    toast.success('Permintaan hapus rekening disubmit untuk otorisasi')
    deletingAccountNo.value = null
    await loadSubmissions()
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal mengirim permintaan hapus')
  } finally {
    deleteSubmitting.value = false
  }
}

onMounted(() => {
  loadBankAccounts()
  loadSubmissions()
})
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Rekening Bank</h1>
        <p class="text-sm text-muted">Daftar rekening bank milik LAZ</p>
      </div>
      <Button size="sm" class="gap-1.5 h-8 text-xs" @click="openCreate">
        <Plus class="w-3.5 h-3.5" />
        Tambah Rekening
      </Button>
    </div>

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

    <!-- Pending submissions -->
    <div
      v-if="submissions.length > 0"
      class="rounded-lg border border-amber-200 bg-amber-50 dark:bg-amber-900/10 dark:border-amber-800 p-3"
    >
      <p class="mb-2 text-xs font-semibold uppercase tracking-wide text-amber-700 dark:text-amber-400">
        Permintaan Rekening Bank ({{ submissions.length }})
      </p>
      <div class="space-y-1">
        <div
          v-for="sub in submissions"
          :key="sub.id"
          class="flex items-center gap-3 rounded bg-white dark:bg-zinc-900 px-3 py-1.5 text-[11px] border border-border"
        >
          <span class="font-mono text-muted">#{{ sub.id }}</span>
          <span class="text-[10px] uppercase tracking-wide px-1 py-px rounded bg-zinc-100 text-zinc-500 dark:bg-zinc-800">
            {{ (sub.payload as any).action ?? 'create' }}
          </span>
          <span class="font-semibold truncate flex-1">{{ (sub.payload as any).account_name ?? '—' }}</span>
          <span v-if="(sub.payload as any).account_no" class="font-mono text-muted">{{ (sub.payload as any).account_no }}</span>
          <StatusBadge :status="sub.status" />
        </div>
      </div>
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
            {{ (page - 1) * PAGE_SIZE + 1 }}–{{ Math.min(page * PAGE_SIZE, totalRecords) }}
            dari {{ totalRecords }} rekening
          </template>
          <template v-else>Tidak ada rekening</template>
        </span>
        <TablePagination
          :page="page"
          :total-pages="totalPages"
          :total="totalRecords"
          :loading="loading"
          unit="rekening"
          @prev="prevPage"
          @next="nextPage"
        />
      </div>

      <!-- DataTable -->
      <AppDataTable :value="rows" :loading="loading" :compact="true">
        <Column field="account_no" header="Kode Rekening" style="width:120px;min-width:100px">
          <template #body="{ data: r }">
            <span class="font-mono text-xs text-muted tabular-nums">{{ r.account_no }}</span>
          </template>
        </Column>

        <Column field="account_name" header="Nama Rekening">
          <template #body="{ data: r }">
            <span class="text-[11px]">{{ r.account_name ?? '—' }}</span>
          </template>
        </Column>

        <Column field="bank_name" header="Nama Bank" style="width:130px;min-width:100px">
          <template #body="{ data: r }">
            <span class="text-[11px]">{{ r.bank_name ?? '—' }}</span>
          </template>
        </Column>

        <Column field="bank_account_no" header="No Rekening Bank" style="width:150px;min-width:120px">
          <template #body="{ data: r }">
            <span class="font-mono text-xs text-muted tabular-nums">{{ r.bank_account_no ?? '—' }}</span>
          </template>
        </Column>

        <Column field="branch_code" header="Cabang" style="width:80px;min-width:60px">
          <template #body="{ data: r }">
            <span class="text-[11px] text-muted">{{ r.branch_code ?? '—' }}</span>
          </template>
        </Column>

        <Column field="currency_code" header="Valuta" style="width:70px;min-width:60px">
          <template #body="{ data: r }">
            <span class="inline-block text-[10px] font-semibold px-1.5 py-px rounded bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300">
              {{ r.currency_code ?? '—' }}
            </span>
          </template>
        </Column>

        <Column
          field="balance"
          header="Saldo"
          style="width:150px;min-width:120px"
          :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }"
        >
          <template #body="{ data: r }">
            <div class="text-right tabular-nums text-[11px]">
              <template v-if="r.currency_code === 'IDR'">
                {{ r.balance != null ? formatIdr(r.balance) : '—' }}
              </template>
              <template v-else>
                {{ r.balance != null ? r.balance.toLocaleString('id-ID', { minimumFractionDigits: 2 }) : '—' }}
              </template>
            </div>
          </template>
        </Column>

        <Column field="status" header="Status" style="width:80px;min-width:70px">
          <template #body="{ data: r }">
            <span
              v-if="r.status === 'A'"
              class="inline-block text-[10px] font-semibold px-1.5 py-px rounded bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300"
            >
              Aktif
            </span>
            <span
              v-else
              class="inline-block text-[10px] font-semibold px-1.5 py-px rounded bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400"
            >
              Non-aktif
            </span>
          </template>
        </Column>

        <!-- Aksi -->
        <Column header="Aksi" style="width:110px;min-width:100px">
          <template #body="{ data: r }">
            <div class="flex items-center gap-1">
              <template v-if="deletingAccountNo === r.account_no">
                <span class="text-[10px] text-red-600 font-medium mr-1">Hapus?</span>
                <button
                  class="rounded border border-red-400 px-1.5 py-0.5 text-[10px] font-medium text-red-600 hover:bg-red-50 transition disabled:opacity-50"
                  :disabled="deleteSubmitting"
                  @click="confirmDelete(r.account_no)"
                >Ya</button>
                <button
                  class="rounded border border-zinc-300 px-1.5 py-0.5 text-[10px] font-medium text-zinc-600 hover:bg-zinc-100 transition"
                  @click="deletingAccountNo = null"
                >Batal</button>
              </template>
              <template v-else>
                <button
                  class="rounded border border-zinc-300 px-1.5 py-0.5 text-[10px] font-medium text-zinc-600 hover:bg-zinc-100 transition inline-flex items-center gap-0.5"
                  @click="openEdit(r.account_no)"
                >
                  <Pencil class="w-2.5 h-2.5" />
                  Edit
                </button>
                <button
                  class="rounded border border-red-300 px-1.5 py-0.5 text-[10px] font-medium text-red-500 hover:bg-red-50 transition inline-flex items-center gap-0.5"
                  @click="deletingAccountNo = r.account_no"
                >
                  <Trash2 class="w-2.5 h-2.5" />
                  Hapus
                </button>
              </template>
            </div>
          </template>
        </Column>

        <template #empty>Tidak ada rekening bank yang ditemukan.</template>
      </AppDataTable>
    </div>

    <!-- Form Drawer -->
    <Teleport to="body">
      <Transition name="drawer-fade">
        <div
          v-if="drawerOpen"
          class="fixed inset-0 z-50 flex justify-end bg-black/40"
          @click.self="closeDrawer"
        >
          <Transition name="drawer-slide">
            <div
              v-if="drawerOpen"
              class="relative flex h-full w-full max-w-xl flex-col bg-surface shadow-2xl"
            >
              <!-- Drawer header -->
              <div class="flex items-center justify-between border-b border-border px-5 py-4">
                <div>
                  <h2 class="text-base font-semibold">
                    {{ drawerMode === 'create' ? 'Tambah Rekening Bank' : `Edit Rekening — ${editingAccountNo}` }}
                  </h2>
                  <p class="text-[11px] text-muted mt-0.5">Permintaan akan diproses melalui otorisasi</p>
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
              <div v-if="drawerLoading" class="flex-1 overflow-y-auto px-5 py-4 space-y-4">
                <div v-for="i in 6" :key="i" class="space-y-1.5">
                  <div class="h-3 w-24 rounded bg-muted/20 animate-pulse" />
                  <div class="h-9 w-full rounded-lg bg-muted/10 animate-pulse" />
                </div>
              </div>

              <!-- Form body -->
              <div v-else class="flex-1 overflow-y-auto px-5 py-4 space-y-4">
                <!-- Nama Rekening -->
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

                <!-- No Rekening Bank -->
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

                <!-- 2 kolom: Nama Bank + Cabang -->
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

                <!-- 2 kolom: Valuta + GL Interface -->
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

                <!-- Tgl Buka -->
                <div>
                  <label class="mb-1 block text-xs font-medium">Tgl Buka</label>
                  <DateField v-model="form.opening_date" />
                </div>

                <!-- Rekening Amil -->
                <div class="flex items-center gap-2">
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

                <!-- Default Produk -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-muted" :class="{ 'opacity-40': form.is_amil_account }">
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

                <!-- Kode Kas -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-muted">Kode Kas <span class="text-muted">(opsional)</span></label>
                  <input
                    v-model="form.cash_code"
                    placeholder="Kode kas unik (opsional)"
                    class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
                  />
                </div>

                <p class="text-[10px] text-muted pt-1">
                  Permintaan ini akan masuk sistem otorisasi. Rekening aktif setelah disetujui supervisor.
                </p>
              </div>

              <!-- Drawer footer -->
              <div class="border-t border-border px-5 py-3 flex justify-end gap-2">
                <Button variant="outline" size="sm" :disabled="submitting" @click="closeDrawer">
                  Batal
                </Button>
                <Button size="sm" :disabled="submitting || drawerLoading" @click="submitForm">
                  {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
                </Button>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.drawer-fade-enter-active,
.drawer-fade-leave-active {
  transition: opacity 0.2s ease;
}
.drawer-fade-enter-from,
.drawer-fade-leave-to {
  opacity: 0;
}
.drawer-slide-enter-active,
.drawer-slide-leave-active {
  transition: transform 0.25s ease;
}
.drawer-slide-enter-from,
.drawer-slide-leave-to {
  transform: translateX(100%);
}
</style>

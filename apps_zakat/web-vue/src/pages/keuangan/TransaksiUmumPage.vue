<script setup lang="ts">
import { BookOpen, Plus, Search, Trash2 } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import Modal from '@/components/ui/Modal.vue'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────
interface TxRow {
  _kind: 'tx'
  transactionid: number
  transactionno: string
  actual_date: string
  description: string
  reference_no: string | null
  amount: number
  authstatus: string
  inputer: string
  branch_code: string
}

interface SubRow {
  _kind: 'sub'
  id: number
  actual_date: string
  status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED' | 'PROCESSING'
  rejection_notes: string | null
  payload: Record<string, unknown>
}

type MergedRow = TxRow | SubRow

interface CoaOption {
  code: string
  name: string
  type_code: string | null
}

interface FormItem {
  account_code: string
  account_name: string
  mutation_type: 'D' | 'C'
  amount: number | null
  description: string
}

// ── State ─────────────────────────────────────────────────────────────────────
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const txRows = ref<TxRow[]>([])
const subRows = ref<SubRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)
const actionLoading = shallowRef<number | null>(null)

const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)
const search = shallowRef('')

// Form state
const showForm = shallowRef(false)
const formSaving = shallowRef(false)
const formError = shallowRef<string | null>(null)
const coaOptions = ref<CoaOption[]>([])
const coaLoading = shallowRef(false)

const formDate = shallowRef(today)
const formDescription = shallowRef('')
const formReferenceNo = shallowRef('')
const formItems = ref<FormItem[]>([
  { account_code: '', account_name: '', mutation_type: 'D', amount: null, description: '' },
  { account_code: '', account_name: '', mutation_type: 'C', amount: null, description: '' },
])

// Detail modal state
const showDetail = shallowRef(false)
const detailRow = ref<TxRow & { items?: unknown[] } | null>(null)
const detailLoading = shallowRef(false)

// ── Computed ──────────────────────────────────────────────────────────────────
const mergedRows = computed<MergedRow[]>(() => [
  ...subRows.value.map(r => ({ ...r, _kind: 'sub' as const })),
  ...txRows.value.map(r => ({ ...r, _kind: 'tx' as const })),
])

const showCount = computed(() => {
  if (!hasLoaded.value) return ''
  if (!totalRec.value && !subRows.value.length) return 'Tidak ada data'
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, totalRec.value)
  return `Showing ${from}–${to} of ${totalRec.value} records`
})

const coaSelectOptions = computed(() =>
  coaOptions.value.map(o => ({
    value: o.code,
    label: `${o.code} — ${o.name}`,
  }))
)

const totalDebet = computed(() =>
  formItems.value
    .filter(i => i.mutation_type === 'D')
    .reduce((s, i) => s + (i.amount ?? 0), 0)
)
const totalKredit = computed(() =>
  formItems.value
    .filter(i => i.mutation_type === 'C')
    .reduce((s, i) => s + (i.amount ?? 0), 0)
)
const isBalanced = computed(() => Math.abs(totalDebet.value - totalKredit.value) < 0.01)

// ── Methods ───────────────────────────────────────────────────────────────────
function goto(target: number) {
  page.value = Math.min(Math.max(1, target), totalPages.value || 1)
  load()
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      limit: String(pageSize.value),
      date_from: dateFrom.value,
      date_to: dateTo.value,
    })
    if (search.value) params.set('search', search.value)

    const [txRes, subRes] = await Promise.all([
      api.get<{ rows: Omit<TxRow, '_kind'>[]; pagination: { total: number; total_pages: number } }>(
        `/api/transaksi-umum/?${params}`
      ),
      api.get<{ rows: Omit<SubRow, '_kind'>[] }>(
        '/api/otorisasi/my-submissions/?entity_type=transaksi_umum'
      ).catch(() => ({ rows: [] })),
    ])

    txRows.value = (txRes?.rows ?? []).map(r => ({ ...r, _kind: 'tx' as const }))
    subRows.value = (subRes?.rows ?? []).map(r => ({ ...r, _kind: 'sub' as const }))
    totalRec.value = txRes?.pagination?.total ?? 0
    totalPages.value = txRes?.pagination?.total_pages ?? 1
    hasLoaded.value = true
  } catch (e) {
    errorMsg.value = 'Gagal memuat data transaksi'
  } finally {
    loading.value = false
  }
}

async function loadCoaOptions() {
  if (coaOptions.value.length) return
  coaLoading.value = true
  try {
    const res = await api.get<{ rows: CoaOption[] }>('/api/coa/accounts?is_detail=T&page_size=500')
    coaOptions.value = res?.rows ?? []
  } finally {
    coaLoading.value = false
  }
}

function openForm() {
  formDate.value = today
  formDescription.value = ''
  formReferenceNo.value = ''
  formItems.value = [
    { account_code: '', account_name: '', mutation_type: 'D', amount: null, description: '' },
    { account_code: '', account_name: '', mutation_type: 'C', amount: null, description: '' },
  ]
  formError.value = null
  showForm.value = true
  loadCoaOptions()
}

function addItem() {
  formItems.value.push({
    account_code: '',
    account_name: '',
    mutation_type: 'D',
    amount: null,
    description: '',
  })
}

function removeItem(idx: number) {
  if (formItems.value.length <= 2) return
  formItems.value.splice(idx, 1)
}

function onAccountSelect(idx: number, code: string) {
  const opt = coaOptions.value.find(o => o.code === code)
  formItems.value[idx].account_code = code
  formItems.value[idx].account_name = opt?.name ?? ''
}

async function submitForm() {
  formError.value = null

  if (!formDescription.value.trim()) {
    formError.value = 'Deskripsi transaksi wajib diisi'
    return
  }
  if (formItems.value.some(i => !i.account_code || !i.amount)) {
    formError.value = 'Semua baris item wajib diisi (akun + jumlah)'
    return
  }
  if (!isBalanced.value) {
    formError.value = `Jurnal tidak balance: Debet ${totalDebet.value.toLocaleString('id')} ≠ Kredit ${totalKredit.value.toLocaleString('id')}`
    return
  }

  formSaving.value = true
  try {
    await api.post('/api/transaksi-umum/', {
      actual_date: formDate.value,
      description: formDescription.value.trim(),
      reference_no: formReferenceNo.value.trim(),
      items: formItems.value.map(i => ({
        account_code: i.account_code,
        account_name: i.account_name,
        mutation_type: i.mutation_type,
        amount: i.amount ?? 0,
        description: i.description.trim(),
      })),
    })
    toast.success('Transaksi umum berhasil disubmit untuk otorisasi')
    showForm.value = false
    load()
  } catch (e: unknown) {
    const msg = (e as { message?: string })?.message ?? 'Gagal menyimpan transaksi'
    formError.value = msg
    toast.error(msg)
  } finally {
    formSaving.value = false
  }
}

async function openDetail(row: TxRow) {
  detailLoading.value = true
  showDetail.value = true
  detailRow.value = { ...row }
  try {
    const res = await api.get<{ id: number; items: unknown[] }>(
      `/api/transaksi-umum/${row.transactionid}`
    )
    detailRow.value = { ...row, items: res?.items ?? [] } as TxRow & { items: unknown[] }
  } catch {
    // keep header data visible
  } finally {
    detailLoading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-2">
        <BookOpen class="h-5 w-5 text-primary" />
        <h1 class="text-xl font-bold text-foreground">Transaksi Umum</h1>
      </div>
      <Button size="sm" class="gap-1.5" @click="openForm">
        <Plus class="h-3.5 w-3.5" />
        Input Transaksi
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <!-- Toolbar -->
    <div class="space-y-0">
      <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
        <div class="flex items-end gap-2">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-500">Dari</label>
            <DateField v-model="dateFrom" />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai</label>
            <DateField v-model="dateTo" />
          </div>
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-500">Cari</label>
          <input
            v-model="search"
            placeholder="No. transaksi / deskripsi..."
            class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            @keyup.enter="() => { page.value = 1; load() }"
          />
        </div>
        <Button
          size="sm"
          class="h-8 gap-1.5 text-xs"
          :disabled="loading"
          @click="() => { page.value = 1; load() }"
        >
          <Search class="h-3.5 w-3.5" />
          {{ loading ? 'Memuat...' : 'Tampilkan' }}
        </Button>
      </div>

      <!-- Count + pagination bar -->
      <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
        <span class="text-xs text-zinc-500">
          {{ hasLoaded ? showCount : 'Pilih tanggal dan klik Tampilkan' }}
          <span v-if="subRows.length" class="ml-2 text-yellow-600">
            (+ {{ subRows.length }} draft/pending)
          </span>
        </span>
        <TablePagination
          v-if="hasLoaded && totalPages > 1"
          :page="page"
          :total-pages="totalPages"
          :total="totalRec"
          :page-size="pageSize"
          @goto="goto"
        />
      </div>

      <!-- Table -->
      <div class="overflow-x-auto rounded-b border border-surface-200">
        <table class="w-full text-[11px]">
          <thead class="border-b border-border text-[10px] uppercase tracking-widest text-muted">
            <tr>
              <th class="px-4 py-2 text-left">No. Transaksi / Draft</th>
              <th class="px-4 py-2 text-left">Tanggal</th>
              <th class="px-4 py-2 text-left">Deskripsi</th>
              <th class="px-4 py-2 text-right">Total Debet</th>
              <th class="px-4 py-2 text-center">Status</th>
              <th class="px-4 py-2 text-left">Inputer</th>
            </tr>
          </thead>
          <tbody>
            <!-- empty states -->
            <tr v-if="!hasLoaded">
              <td colspan="6" class="px-4 py-8 text-center text-zinc-400">
                Pilih tanggal dan klik Tampilkan untuk melihat data.
              </td>
            </tr>
            <tr v-else-if="mergedRows.length === 0">
              <td colspan="6" class="px-4 py-8 text-center text-zinc-400">
                Tidak ada transaksi dalam periode ini.
              </td>
            </tr>

            <template v-for="row in mergedRows" :key="row._kind === 'tx' ? `tx-${row.transactionid}` : `sub-${row.id}`">
              <!-- Submission row (draft/pending) -->
              <tr v-if="row._kind === 'sub'" class="border-t bg-amber-50/40 dark:bg-amber-900/10">
                <td class="px-4 py-2 font-mono text-xs text-zinc-400">Draft #{{ row.id }}</td>
                <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
                <td class="px-4 py-2 text-zinc-500">
                  {{ (row.payload as Record<string, unknown>).description as string || '—' }}
                </td>
                <td class="px-4 py-2 text-right text-zinc-400">—</td>
                <td class="px-4 py-2 text-center">
                  <StatusBadge :status="row.status" />
                </td>
                <td class="px-4 py-2 text-zinc-400">
                  <template v-if="row.status === 'REJECTED' && row.rejection_notes">
                    <span :title="row.rejection_notes" class="cursor-help text-red-400 underline decoration-dotted">
                      Alasan
                    </span>
                  </template>
                  <template v-else-if="row.status === 'PENDING'">
                    <span class="text-zinc-400">Menunggu otorisasi</span>
                  </template>
                </td>
              </tr>

              <!-- Transaction row (authorized) -->
              <tr
                v-else
                class="cursor-pointer border-t hover:bg-zinc-50 dark:hover:bg-zinc-800"
                @click="openDetail(row as TxRow)"
              >
                <td class="px-4 py-2 font-mono">{{ row.transactionno }}</td>
                <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
                <td class="px-4 py-2 max-w-xs truncate" :title="row.description">{{ row.description }}</td>
                <td class="px-4 py-2 text-right font-mono">
                  {{ row.amount.toLocaleString('id-ID') }}
                </td>
                <td class="px-4 py-2 text-center">
                  <span class="rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-medium text-green-700">
                    Authorized
                  </span>
                </td>
                <td class="px-4 py-2 text-zinc-500">{{ row.inputer }}</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create Form Modal -->
    <Modal :open="showForm" title="Input Transaksi Umum" @close="showForm = false">
      <div class="space-y-4 p-4">
        <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

        <!-- Header fields -->
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Tanggal Transaksi</label>
            <DateField v-model="formDate" />
          </div>
          <div class="sm:col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Deskripsi <span class="text-red-500">*</span></label>
            <input
              v-model="formDescription"
              placeholder="Keterangan transaksi..."
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div class="sm:col-span-3">
            <label class="mb-1 block text-xs font-medium text-zinc-600">No. Referensi</label>
            <input
              v-model="formReferenceNo"
              placeholder="Opsional"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>

        <!-- Items table -->
        <div>
          <div class="mb-2 flex items-center justify-between">
            <span class="text-xs font-semibold text-zinc-600 uppercase tracking-wide">Baris Jurnal</span>
            <Button size="sm" variant="outline" class="h-7 gap-1 text-xs" @click="addItem">
              <Plus class="h-3 w-3" />
              Tambah Baris
            </Button>
          </div>

          <div class="overflow-x-auto rounded border">
            <table class="w-full text-xs">
              <thead class="border-b bg-zinc-50 text-[10px] uppercase tracking-widest text-zinc-500">
                <tr>
                  <th class="px-3 py-2 text-left w-1/3">Akun COA</th>
                  <th class="px-3 py-2 text-center w-16">D/K</th>
                  <th class="px-3 py-2 text-right w-32">Jumlah</th>
                  <th class="px-3 py-2 text-left">Keterangan</th>
                  <th class="px-3 py-2 w-8"></th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, idx) in formItems"
                  :key="idx"
                  class="border-t"
                >
                  <td class="px-3 py-1.5">
                    <select
                      :value="item.account_code"
                      :disabled="coaLoading"
                      class="w-full rounded border px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-primary"
                      @change="onAccountSelect(idx, ($event.target as HTMLSelectElement).value)"
                    >
                      <option value="">— Pilih akun —</option>
                      <option
                        v-for="opt in coaSelectOptions"
                        :key="opt.value"
                        :value="opt.value"
                      >{{ opt.label }}</option>
                    </select>
                  </td>
                  <td class="px-3 py-1.5 text-center">
                    <select
                      v-model="item.mutation_type"
                      class="rounded border px-1.5 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-primary"
                    >
                      <option value="D">D</option>
                      <option value="C">K</option>
                    </select>
                  </td>
                  <td class="px-3 py-1.5">
                    <AmountInput v-model="item.amount" class="text-right text-xs" />
                  </td>
                  <td class="px-3 py-1.5">
                    <input
                      v-model="item.description"
                      placeholder="Opsional"
                      class="w-full rounded border px-2 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-primary"
                    />
                  </td>
                  <td class="px-3 py-1.5 text-center">
                    <button
                      :disabled="formItems.length <= 2"
                      class="rounded p-1 text-red-400 hover:bg-red-50 disabled:opacity-30"
                      @click="removeItem(idx)"
                    >
                      <Trash2 class="h-3.5 w-3.5" />
                    </button>
                  </td>
                </tr>
              </tbody>
              <tfoot class="border-t bg-zinc-50">
                <tr>
                  <td class="px-3 py-2 text-right text-xs font-semibold text-zinc-600" colspan="2">
                    Total
                  </td>
                  <td class="px-3 py-2 text-right font-mono text-xs font-bold">
                    <div class="text-blue-700">D: {{ totalDebet.toLocaleString('id-ID') }}</div>
                    <div class="text-orange-700">K: {{ totalKredit.toLocaleString('id-ID') }}</div>
                  </td>
                  <td colspan="2" class="px-3 py-2">
                    <span v-if="isBalanced && totalDebet > 0" class="text-xs font-medium text-green-600">✓ Balance</span>
                    <span v-else-if="totalDebet > 0 || totalKredit > 0" class="text-xs font-medium text-red-500">
                      ✗ Selisih {{ Math.abs(totalDebet - totalKredit).toLocaleString('id-ID') }}
                    </span>
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>

        <!-- Footer buttons -->
        <div class="flex justify-end gap-2 pt-2">
          <Button variant="outline" @click="showForm = false">Batal</Button>
          <Button
            :disabled="formSaving || !isBalanced || totalDebet === 0"
            @click="submitForm"
          >
            {{ formSaving ? 'Menyimpan...' : 'Submit untuk Otorisasi' }}
          </Button>
        </div>
      </div>
    </Modal>

    <!-- Detail Modal -->
    <Modal :open="showDetail" title="Detail Transaksi Umum" @close="showDetail = false">
      <div v-if="detailRow" class="space-y-4 p-4">
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <div class="text-xs text-zinc-500">No. Transaksi</div>
            <div class="font-mono font-medium">{{ detailRow.transactionno }}</div>
          </div>
          <div>
            <div class="text-xs text-zinc-500">Tanggal</div>
            <div>{{ dmy(detailRow.actual_date) }}</div>
          </div>
          <div class="col-span-2">
            <div class="text-xs text-zinc-500">Deskripsi</div>
            <div>{{ detailRow.description }}</div>
          </div>
          <div v-if="detailRow.reference_no">
            <div class="text-xs text-zinc-500">No. Referensi</div>
            <div>{{ detailRow.reference_no }}</div>
          </div>
          <div>
            <div class="text-xs text-zinc-500">Inputer</div>
            <div>{{ detailRow.inputer }}</div>
          </div>
        </div>

        <!-- Items -->
        <div v-if="(detailRow as TxRow & { items?: unknown[] }).items">
          <div class="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">Baris Jurnal</div>
          <div class="overflow-x-auto rounded border">
            <table class="w-full text-xs">
              <thead class="border-b bg-zinc-50 text-[10px] uppercase tracking-widest text-zinc-500">
                <tr>
                  <th class="px-3 py-2 text-left">Kode Akun</th>
                  <th class="px-3 py-2 text-left">Nama Akun</th>
                  <th class="px-3 py-2 text-center">D/K</th>
                  <th class="px-3 py-2 text-right">Jumlah</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, idx) in (detailRow as TxRow & { items?: Record<string, unknown>[] }).items"
                  :key="idx"
                  class="border-t"
                >
                  <td class="px-3 py-1.5 font-mono">{{ item.account_code }}</td>
                  <td class="px-3 py-1.5">{{ item.account_name }}</td>
                  <td class="px-3 py-1.5 text-center">
                    <span
                      :class="item.mutation_type === 'D' ? 'text-blue-700' : 'text-orange-700'"
                      class="font-bold"
                    >{{ item.mutation_type === 'D' ? 'Debet' : 'Kredit' }}</span>
                  </td>
                  <td class="px-3 py-1.5 text-right font-mono">
                    {{ (item.amount as number).toLocaleString('id-ID') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else-if="detailLoading" class="py-4 text-center text-xs text-zinc-400">
          Memuat detail...
        </div>

        <div class="flex justify-end">
          <Button variant="outline" @click="showDetail = false">Tutup</Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

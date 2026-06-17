<script setup lang="ts">
import { ArrowLeft, BookOpen, Plus, Search, Trash2, X } from 'lucide-vue-next'
import { computed, ref, shallowRef, onMounted } from 'vue'

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

// Sub-item types (4 jenis mutasi)
interface ItemGL {
  item_type: 'G'
  account_code: string
  account_name: string
  mutation_type: 'D' | 'C'
  amount: number | null
  description: string
}

interface ItemKasBank {
  item_type: 'B'
  account_no: string
  account_name: string
  mutation_type: 'D' | 'C'
  amount: number | null
  description: string
}

interface ItemPenghimpunan {
  item_type: 'C'
  product_account_no: string
  product_name: string
  donor_id: number
  donor_name: string
  fund_entity: number
  mutation_type: 'C' | 'D'
  amount: number | null
  description: string
  is_reversal: boolean
}

interface ItemPenyaluran {
  item_type: 'D'
  dist_account_no: string
  dist_account_name: string
  fund_account_no: string
  fund_account_name: string
  ashnaf: string
  fund_entity: number
  mutation_type: 'D' | 'C'
  amount: number | null
  description: string
  is_correction: boolean
}

type AnyItem = ItemGL | ItemKasBank | ItemPenghimpunan | ItemPenyaluran

interface CoaOption { code: string; name: string }
interface LookupRow { account_no: string; account_name: string }
interface DonorRow { donor_id: number; donor_name: string; donor_no?: string }

// ── Constants ─────────────────────────────────────────────────────────────────
const FUND_ENTITY_OPTIONS = [
  { value: 1, label: 'Zakat' },
  { value: 2, label: 'Infaq' },
  { value: 3, label: 'Wakaf' },
  { value: 4, label: 'Amil' },
  { value: 5, label: 'Non-halal' },
]

const ASHNAF_OPTIONS = [
  { value: 'F', label: 'Fakir' },
  { value: 'M', label: 'Miskin' },
  { value: 'U', label: 'Mualaf' },
  { value: 'H', label: 'Hamba Sahaya' },
  { value: 'G', label: 'Gharimin' },
  { value: 'S', label: 'Fisabilillah' },
  { value: 'I', label: 'Ibnu Sabil' },
  { value: 'A', label: 'Amil' },
]

const ITEM_LABELS: Record<string, string> = { G: 'GL Accounting', B: 'Kas/Bank', C: 'Penghimpunan', D: 'Penyaluran' }
const ITEM_BADGES: Record<string, string> = {
  G: 'bg-blue-100 text-blue-700',
  B: 'bg-emerald-100 text-emerald-700',
  C: 'bg-violet-100 text-violet-700',
  D: 'bg-amber-100 text-amber-700',
}

// ── State ─────────────────────────────────────────────────────────────────────
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

// List state
const txRows = ref<TxRow[]>([])
const subRows = ref<SubRow[]>([])
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const totalPages = shallowRef(1)
const totalRec = shallowRef(0)
const hasLoaded = shallowRef(false)
const dateFrom = shallowRef(today)
const dateTo = shallowRef(today)
const search = shallowRef('')

// Main form
const showForm = shallowRef(false)
const formView = shallowRef<'main' | 'G' | 'B' | 'C' | 'D'>('main')
const editItemIdx = shallowRef<number | null>(null)
const formSaving = shallowRef(false)
const formError = shallowRef<string | null>(null)
const formDate = shallowRef(today)
const formDescription = shallowRef('')
const formReferenceNo = shallowRef('')
const formItems = ref<AnyItem[]>([])

// COA (for GL)
const coaOptions = ref<CoaOption[]>([])
const coaLoading = shallowRef(false)

// GL sub-form
const glAccountCode = shallowRef('')
const glAccountName = shallowRef('')
const glMutationType = shallowRef<'D' | 'C'>('D')
const glAmount = shallowRef<number | null>(null)
const glDescription = shallowRef('')

// KasBank sub-form
const kbSearch = shallowRef('')
const kbResults = ref<LookupRow[]>([])
const kbLoading = shallowRef(false)
const kbSelectedNo = shallowRef('')
const kbSelectedName = shallowRef('')
const kbMutationType = shallowRef<'D' | 'C'>('D')
const kbAmount = shallowRef<number | null>(null)
const kbDescription = shallowRef('')
const kbShowResults = shallowRef(false)

// Penghimpunan sub-form
const phDonorSearch = shallowRef('')
const phDonorResults = ref<DonorRow[]>([])
const phDonorLoading = shallowRef(false)
const phDonorId = shallowRef(0)
const phDonorName = shallowRef('HAMBA ALLAH')
const phProdukSearch = shallowRef('')
const phProdukResults = ref<LookupRow[]>([])
const phProdukLoading = shallowRef(false)
const phProdukNo = shallowRef('')
const phProdukName = shallowRef('')
const phFundEntity = shallowRef(1)
const phAmount = shallowRef<number | null>(null)
const phDescription = shallowRef('')
const phIsReversal = shallowRef(false)
const phShowDonorResults = shallowRef(false)
const phShowProdukResults = shallowRef(false)

// Penyaluran sub-form
const pyProgramSearch = shallowRef('')
const pyProgramResults = ref<LookupRow[]>([])
const pyProgramLoading = shallowRef(false)
const pyProgramNo = shallowRef('')
const pyProgramName = shallowRef('')
const pySumberSearch = shallowRef('')
const pySumberResults = ref<LookupRow[]>([])
const pySumberLoading = shallowRef(false)
const pySumberNo = shallowRef('')
const pySumberName = shallowRef('')
const pyAshnaf = shallowRef('F')
const pyFundEntity = shallowRef(1)
const pyMutationType = shallowRef<'D' | 'C'>('D')
const pyAmount = shallowRef<number | null>(null)
const pyDescription = shallowRef('')
const pyIsCorrection = shallowRef(false)
const pyShowProgramResults = shallowRef(false)
const pyShowSumberResults = shallowRef(false)

// Detail modal
const showDetail = shallowRef(false)
const detailRow = ref<TxRow & { items?: unknown[] } | null>(null)
const detailLoading = shallowRef(false)

// ── Computed ──────────────────────────────────────────────────────────────────
const mergedRows = computed<MergedRow[]>(() => [
  ...subRows.value.map(r => ({ ...r, _kind: 'sub' as const })),
  ...txRows.value.map(r => ({ ...r, _kind: 'tx' as const })),
])

const showCount = computed(() => {
  if (!totalRec.value && !subRows.value.length) return 'Tidak ada data'
  const from = (page.value - 1) * pageSize.value + 1
  const to = Math.min(page.value * pageSize.value, totalRec.value)
  return `Showing ${from}–${to} of ${totalRec.value} records`
})

const totalDebet = computed(() =>
  formItems.value.filter(i => i.mutation_type === 'D').reduce((s, i) => s + (i.amount ?? 0), 0)
)
const totalKredit = computed(() =>
  formItems.value.filter(i => i.mutation_type === 'C').reduce((s, i) => s + (i.amount ?? 0), 0)
)
const isBalanced = computed(() =>
  formItems.value.length >= 2 && Math.abs(totalDebet.value - totalKredit.value) < 0.01
)

const coaSelectOptions = computed(() =>
  coaOptions.value.map(o => ({ value: o.code, label: `${o.code} — ${o.name}` }))
)

const formTitle = computed(() => {
  if (formView.value === 'main') return editItemIdx.value !== null ? 'Edit Detail' : 'Input Transaksi Umum'
  const labels: Record<string, string> = {
    G: 'Detail GL Accounting',
    B: 'Detail Kas / Bank',
    C: 'Detail Penghimpunan Dana',
    D: 'Detail Penyaluran Dana',
  }
  return labels[formView.value] ?? 'Tambah Detail'
})

// ── List Methods ──────────────────────────────────────────────────────────────
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
  } catch {
    errorMsg.value = 'Gagal memuat data transaksi'
  } finally {
    loading.value = false
  }
}

// ── COA / Lookup ──────────────────────────────────────────────────────────────
async function loadCoa() {
  if (coaOptions.value.length) return
  coaLoading.value = true
  try {
    const res = await api.get<{ rows: CoaOption[] }>('/api/coa/accounts?is_detail=T&page_size=500')
    coaOptions.value = res?.rows ?? []
  } finally {
    coaLoading.value = false
  }
}

async function searchKasBank() {
  if (!kbSearch.value.trim()) return
  kbLoading.value = true
  kbShowResults.value = false
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/kasbank?search=${encodeURIComponent(kbSearch.value)}`
    )
    kbResults.value = res?.rows ?? []
    kbShowResults.value = true
  } finally {
    kbLoading.value = false
  }
}

function selectKasBank(r: LookupRow) {
  kbSelectedNo.value = r.account_no
  kbSelectedName.value = r.account_name
  kbShowResults.value = false
}

function clearKasBank() {
  kbSelectedNo.value = ''
  kbSelectedName.value = ''
  kbResults.value = []
  kbSearch.value = ''
}

async function searchDonor() {
  if (!phDonorSearch.value.trim()) return
  phDonorLoading.value = true
  phShowDonorResults.value = false
  try {
    const res = await api.get<{ rows: DonorRow[] }>(
      `/api/transaksi-umum/lookup/donor?search=${encodeURIComponent(phDonorSearch.value)}`
    )
    phDonorResults.value = res?.rows ?? []
    phShowDonorResults.value = true
  } finally {
    phDonorLoading.value = false
  }
}

function selectDonor(r: DonorRow) {
  phDonorId.value = r.donor_id
  phDonorName.value = r.donor_name
  phShowDonorResults.value = false
}

function clearDonor() {
  phDonorId.value = 0
  phDonorName.value = 'HAMBA ALLAH'
  phDonorResults.value = []
  phDonorSearch.value = ''
}

async function searchProduk() {
  if (!phProdukSearch.value.trim()) return
  phProdukLoading.value = true
  phShowProdukResults.value = false
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/produk?search=${encodeURIComponent(phProdukSearch.value)}&fund_entity=${phFundEntity.value}`
    )
    phProdukResults.value = res?.rows ?? []
    phShowProdukResults.value = true
  } finally {
    phProdukLoading.value = false
  }
}

function selectProduk(r: LookupRow) {
  phProdukNo.value = r.account_no
  phProdukName.value = r.account_name
  phShowProdukResults.value = false
}

function clearProduk() {
  phProdukNo.value = ''
  phProdukName.value = ''
  phProdukResults.value = []
  phProdukSearch.value = ''
}

async function searchProgram() {
  if (!pyProgramSearch.value.trim()) return
  pyProgramLoading.value = true
  pyShowProgramResults.value = false
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/penyaluran?search=${encodeURIComponent(pyProgramSearch.value)}`
    )
    pyProgramResults.value = res?.rows ?? []
    pyShowProgramResults.value = true
  } finally {
    pyProgramLoading.value = false
  }
}

function selectProgram(r: LookupRow) {
  pyProgramNo.value = r.account_no
  pyProgramName.value = r.account_name
  pyShowProgramResults.value = false
}

function clearProgram() {
  pyProgramNo.value = ''
  pyProgramName.value = ''
  pyProgramResults.value = []
  pyProgramSearch.value = ''
}

async function searchSumber() {
  if (!pySumberSearch.value.trim()) return
  pySumberLoading.value = true
  pyShowSumberResults.value = false
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/produk?search=${encodeURIComponent(pySumberSearch.value)}`
    )
    pySumberResults.value = res?.rows ?? []
    pyShowSumberResults.value = true
  } finally {
    pySumberLoading.value = false
  }
}

function selectSumber(r: LookupRow) {
  pySumberNo.value = r.account_no
  pySumberName.value = r.account_name
  pyShowSumberResults.value = false
}

function clearSumber() {
  pySumberNo.value = ''
  pySumberName.value = ''
  pySumberResults.value = []
  pySumberSearch.value = ''
}

// ── COA select handler (GL) ───────────────────────────────────────────────────
function onCoaSelect(code: string) {
  glAccountCode.value = code
  const opt = coaOptions.value.find(o => o.code === code)
  glAccountName.value = opt?.name ?? ''
}

// ── Form Control ──────────────────────────────────────────────────────────────
function openForm() {
  formDate.value = today
  formDescription.value = ''
  formReferenceNo.value = ''
  formItems.value = []
  formError.value = null
  formView.value = 'main'
  editItemIdx.value = null
  showForm.value = true
  loadCoa()
}

function openSubForm(type: 'G' | 'B' | 'C' | 'D', editIdx: number | null = null) {
  editItemIdx.value = editIdx
  formView.value = type

  if (editIdx !== null) {
    const item = formItems.value[editIdx]
    if (item.item_type === 'G') {
      glAccountCode.value = item.account_code
      glAccountName.value = item.account_name
      glMutationType.value = item.mutation_type
      glAmount.value = item.amount
      glDescription.value = item.description
    } else if (item.item_type === 'B') {
      kbSelectedNo.value = item.account_no
      kbSelectedName.value = item.account_name
      kbMutationType.value = item.mutation_type
      kbAmount.value = item.amount
      kbDescription.value = item.description
    } else if (item.item_type === 'C') {
      phDonorId.value = item.donor_id
      phDonorName.value = item.donor_name
      phProdukNo.value = item.product_account_no
      phProdukName.value = item.product_name
      phFundEntity.value = item.fund_entity
      phAmount.value = item.amount
      phDescription.value = item.description
      phIsReversal.value = item.is_reversal
    } else if (item.item_type === 'D') {
      pyProgramNo.value = item.dist_account_no
      pyProgramName.value = item.dist_account_name
      pySumberNo.value = item.fund_account_no
      pySumberName.value = item.fund_account_name
      pyAshnaf.value = item.ashnaf
      pyFundEntity.value = item.fund_entity
      pyMutationType.value = item.mutation_type
      pyAmount.value = item.amount
      pyDescription.value = item.description
      pyIsCorrection.value = item.is_correction
    }
    return
  }

  // Reset sub-form state
  if (type === 'G') {
    glAccountCode.value = ''
    glAccountName.value = ''
    glMutationType.value = 'D'
    glAmount.value = null
    glDescription.value = ''
  } else if (type === 'B') {
    clearKasBank()
    kbMutationType.value = 'D'
    kbAmount.value = null
    kbDescription.value = ''
  } else if (type === 'C') {
    phDonorId.value = 0
    phDonorName.value = 'HAMBA ALLAH'
    phDonorSearch.value = ''
    phDonorResults.value = []
    clearProduk()
    phFundEntity.value = 1
    phAmount.value = null
    phDescription.value = ''
    phIsReversal.value = false
  } else if (type === 'D') {
    clearProgram()
    clearSumber()
    pyAshnaf.value = 'F'
    pyFundEntity.value = 1
    pyMutationType.value = 'D'
    pyAmount.value = null
    pyDescription.value = ''
    pyIsCorrection.value = false
  }
}

function backToMain() {
  formView.value = 'main'
  editItemIdx.value = null
}

function saveCurrentItem() {
  if (formView.value === 'G') saveGLItem()
  else if (formView.value === 'B') saveKasBankItem()
  else if (formView.value === 'C') savePenghimpunanItem()
  else if (formView.value === 'D') savePenyaluranItem()
}

function saveGLItem() {
  if (!glAccountCode.value) { toast.error('Pilih akun COA'); return }
  if (!glAmount.value || glAmount.value <= 0) { toast.error('Nilai harus lebih dari 0'); return }
  const item: ItemGL = {
    item_type: 'G',
    account_code: glAccountCode.value,
    account_name: glAccountName.value,
    mutation_type: glMutationType.value,
    amount: glAmount.value,
    description: glDescription.value,
  }
  if (editItemIdx.value !== null) formItems.value[editItemIdx.value] = item
  else formItems.value.push(item)
  backToMain()
}

function saveKasBankItem() {
  if (!kbSelectedNo.value) { toast.error('Pilih rekening kas/bank'); return }
  if (!kbAmount.value || kbAmount.value <= 0) { toast.error('Nilai harus lebih dari 0'); return }
  const item: ItemKasBank = {
    item_type: 'B',
    account_no: kbSelectedNo.value,
    account_name: kbSelectedName.value,
    mutation_type: kbMutationType.value,
    amount: kbAmount.value,
    description: kbDescription.value,
  }
  if (editItemIdx.value !== null) formItems.value[editItemIdx.value] = item
  else formItems.value.push(item)
  backToMain()
}

function savePenghimpunanItem() {
  if (!phProdukNo.value) { toast.error('Pilih produk penghimpunan'); return }
  if (!phAmount.value || phAmount.value <= 0) { toast.error('Nilai harus lebih dari 0'); return }
  const item: ItemPenghimpunan = {
    item_type: 'C',
    product_account_no: phProdukNo.value,
    product_name: phProdukName.value,
    donor_id: phDonorId.value,
    donor_name: phDonorName.value,
    fund_entity: phFundEntity.value,
    mutation_type: phIsReversal.value ? 'D' : 'C',
    amount: phAmount.value,
    description: phDescription.value,
    is_reversal: phIsReversal.value,
  }
  if (editItemIdx.value !== null) formItems.value[editItemIdx.value] = item
  else formItems.value.push(item)
  backToMain()
}

function savePenyaluranItem() {
  if (!pyProgramNo.value) { toast.error('Pilih program penyaluran'); return }
  if (!pyAmount.value || pyAmount.value <= 0) { toast.error('Nilai harus lebih dari 0'); return }
  const item: ItemPenyaluran = {
    item_type: 'D',
    dist_account_no: pyProgramNo.value,
    dist_account_name: pyProgramName.value,
    fund_account_no: pySumberNo.value,
    fund_account_name: pySumberName.value,
    ashnaf: pyAshnaf.value,
    fund_entity: pyFundEntity.value,
    mutation_type: pyMutationType.value,
    amount: pyAmount.value,
    description: pyDescription.value,
    is_correction: pyIsCorrection.value,
  }
  if (editItemIdx.value !== null) formItems.value[editItemIdx.value] = item
  else formItems.value.push(item)
  backToMain()
}

function removeItem(idx: number) {
  formItems.value.splice(idx, 1)
}

function itemRef(item: AnyItem): string {
  if (item.item_type === 'G') return `${item.account_code} — ${item.account_name}`
  if (item.item_type === 'B') return `${item.account_no} — ${item.account_name}`
  if (item.item_type === 'C') return `${item.product_account_no} — ${item.product_name}`
  if (item.item_type === 'D') return `${item.dist_account_no} — ${item.dist_account_name}`
  return '—'
}

// ── Submit ────────────────────────────────────────────────────────────────────
async function submitForm() {
  formError.value = null
  if (!formDescription.value.trim()) { formError.value = 'Deskripsi transaksi wajib diisi'; return }
  if (formItems.value.length < 2) { formError.value = 'Minimal 2 item mutasi'; return }
  if (!isBalanced.value) {
    formError.value = `Jurnal belum balance: Debet ${totalDebet.value.toLocaleString('id')} ≠ Kredit ${totalKredit.value.toLocaleString('id')}`
    return
  }

  formSaving.value = true
  try {
    await api.post('/api/transaksi-umum/', {
      actual_date: formDate.value,
      description: formDescription.value.trim(),
      reference_no: formReferenceNo.value.trim(),
      items: formItems.value,
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

// ── Detail ────────────────────────────────────────────────────────────────────
async function openDetail(row: TxRow) {
  detailLoading.value = true
  showDetail.value = true
  detailRow.value = { ...row }
  try {
    const res = await api.get<{ id: number; items: unknown[] }>(`/api/transaksi-umum/${row.transactionid}`)
    detailRow.value = { ...row, items: res?.items ?? [] } as TxRow & { items: unknown[] }
  } catch {
    // keep header
  } finally {
    detailLoading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="p-4 sm:p-6 space-y-4">
    <!-- Page header -->
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

    <!-- List section -->
    <div class="space-y-0">
      <!-- Toolbar -->
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
        <Button size="sm" class="h-8 gap-1.5 text-xs" :disabled="loading" @click="() => { page.value = 1; load() }">
          <Search class="h-3.5 w-3.5" />
          {{ loading ? 'Memuat...' : 'Tampilkan' }}
        </Button>
      </div>

      <!-- Count + pagination -->
      <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
        <span class="text-xs text-zinc-500">
          {{ hasLoaded ? showCount : 'Pilih tanggal dan klik Tampilkan' }}
          <span v-if="subRows.length" class="ml-2 text-yellow-600">(+ {{ subRows.length }} draft/pending)</span>
        </span>
        <TablePagination
          v-if="hasLoaded && totalPages > 1"
          :page="page" :total-pages="totalPages" :total="totalRec" :page-size="pageSize"
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
              <tr v-if="row._kind === 'sub'" class="border-t bg-amber-50/40 dark:bg-amber-900/10">
                <td class="px-4 py-2 font-mono text-xs text-zinc-400">Draft #{{ row.id }}</td>
                <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
                <td class="px-4 py-2 text-zinc-500">{{ (row.payload as Record<string,unknown>).description as string || '—' }}</td>
                <td class="px-4 py-2 text-right text-zinc-400">—</td>
                <td class="px-4 py-2 text-center"><StatusBadge :status="row.status" /></td>
                <td class="px-4 py-2">
                  <template v-if="row.status === 'REJECTED' && row.rejection_notes">
                    <span :title="row.rejection_notes" class="cursor-help text-xs text-red-400 underline decoration-dotted">Alasan</span>
                  </template>
                  <template v-else-if="row.status === 'PENDING'">
                    <span class="text-xs text-zinc-400">Menunggu otorisasi</span>
                  </template>
                </td>
              </tr>

              <tr v-else class="cursor-pointer border-t hover:bg-zinc-50 dark:hover:bg-zinc-800" @click="openDetail(row as TxRow)">
                <td class="px-4 py-2 font-mono">{{ row.transactionno }}</td>
                <td class="px-4 py-2">{{ dmy(row.actual_date) }}</td>
                <td class="px-4 py-2 max-w-xs truncate" :title="row.description">{{ row.description }}</td>
                <td class="px-4 py-2 text-right font-mono">{{ row.amount.toLocaleString('id-ID') }}</td>
                <td class="px-4 py-2 text-center">
                  <span class="rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-medium text-green-700">Authorized</span>
                </td>
                <td class="px-4 py-2 text-zinc-500">{{ row.inputer }}</td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════════════════════════
         MAIN FORM MODAL — view switching: main | G | B | C | D
    ════════════════════════════════════════════════════════════════════════ -->
    <Modal v-if="showForm" max-width="max-w-5xl" @close="showForm = false">
      <template #header>
        <div class="flex items-center gap-2">
          <button
            v-if="formView !== 'main'"
            class="flex items-center gap-1 rounded px-2 py-1 text-sm text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800"
            @click="backToMain"
          >
            <ArrowLeft class="h-3.5 w-3.5" />
            Kembali
          </button>
          <span class="font-semibold text-foreground">{{ formTitle }}</span>
        </div>
      </template>

      <!-- ── MAIN VIEW ──────────────────────────────────────────────────── -->
      <div v-if="formView === 'main'" class="space-y-4">
        <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

        <!-- Header fields -->
        <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Tanggal Transaksi</label>
            <DateField v-model="formDate" />
          </div>
          <div class="sm:col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Deskripsi <span class="text-red-500">*</span></label>
            <input v-model="formDescription" placeholder="Keterangan transaksi..." class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          </div>
          <div class="sm:col-span-3">
            <label class="mb-1 block text-xs font-medium text-zinc-600">No. Referensi / Cek / Kwitansi</label>
            <input v-model="formReferenceNo" placeholder="Opsional" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          </div>
        </div>

        <!-- Summary boxes -->
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div class="rounded-xl border bg-zinc-50 p-3">
            <div class="text-xs text-zinc-500">Total Debet</div>
            <div class="mt-1 font-mono text-lg font-bold text-emerald-700">{{ totalDebet.toLocaleString('id-ID') }}</div>
          </div>
          <div class="rounded-xl border bg-zinc-50 p-3">
            <div class="text-xs text-zinc-500">Total Kredit</div>
            <div class="mt-1 font-mono text-lg font-bold text-red-600">{{ totalKredit.toLocaleString('id-ID') }}</div>
          </div>
          <div class="rounded-xl border bg-zinc-50 p-3">
            <div class="text-xs text-zinc-500">Selisih</div>
            <div class="mt-1 font-mono text-lg font-bold text-zinc-700">{{ Math.abs(totalDebet - totalKredit).toLocaleString('id-ID') }}</div>
          </div>
          <div class="rounded-xl border p-3" :class="isBalanced && formItems.length ? 'bg-green-50 border-green-200' : 'bg-zinc-50'">
            <div class="text-xs text-zinc-500">Status</div>
            <div class="mt-1 text-sm font-bold" :class="isBalanced && formItems.length ? 'text-green-700' : 'text-zinc-400'">
              {{ isBalanced && formItems.length ? '✓ Balance' : formItems.length ? '✗ Belum Balance' : '—' }}
            </div>
          </div>
        </div>

        <!-- Item toolbar -->
        <div class="rounded-t border-x border-t bg-zinc-50 px-4 py-2.5 flex flex-wrap gap-2">
          <span class="self-center text-xs font-semibold uppercase tracking-wide text-zinc-500 mr-1">Tambah:</span>
          <button class="rounded border border-blue-200 bg-blue-50 px-3 py-1.5 text-xs font-semibold text-blue-700 hover:bg-blue-100 transition" @click="openSubForm('G')">
            + GL Accounting
          </button>
          <button class="rounded border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-700 hover:bg-emerald-100 transition" @click="openSubForm('B')">
            + Kas / Bank
          </button>
          <button class="rounded border border-violet-200 bg-violet-50 px-3 py-1.5 text-xs font-semibold text-violet-700 hover:bg-violet-100 transition" @click="openSubForm('C')">
            + Penghimpunan
          </button>
          <button class="rounded border border-amber-200 bg-amber-50 px-3 py-1.5 text-xs font-semibold text-amber-700 hover:bg-amber-100 transition" @click="openSubForm('D')">
            + Penyaluran
          </button>
        </div>

        <!-- Items table -->
        <div class="overflow-x-auto rounded-b border">
          <table class="w-full text-xs">
            <thead class="border-b bg-zinc-50 text-[10px] uppercase tracking-widest text-zinc-500">
              <tr>
                <th class="px-3 py-2 text-left">Jenis</th>
                <th class="px-3 py-2 text-left">Referensi</th>
                <th class="px-3 py-2 text-center w-12">D/K</th>
                <th class="px-3 py-2 text-right w-36">Jumlah</th>
                <th class="px-3 py-2 text-left">Keterangan</th>
                <th class="px-3 py-2 w-16"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="formItems.length === 0">
                <td colspan="6" class="px-3 py-6 text-center text-zinc-400">Belum ada item — klik tombol tambah di atas</td>
              </tr>
              <tr v-for="(item, idx) in formItems" :key="idx" class="border-t">
                <td class="px-3 py-1.5">
                  <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold', ITEM_BADGES[item.item_type]]">
                    {{ ITEM_LABELS[item.item_type] }}
                  </span>
                </td>
                <td class="px-3 py-1.5 max-w-[200px] truncate text-zinc-600" :title="itemRef(item)">{{ itemRef(item) }}</td>
                <td class="px-3 py-1.5 text-center">
                  <span :class="item.mutation_type === 'D' ? 'text-emerald-700' : 'text-red-600'" class="font-bold">
                    {{ item.mutation_type === 'D' ? 'D' : 'K' }}
                  </span>
                </td>
                <td class="px-3 py-1.5 text-right font-mono font-semibold">{{ (item.amount ?? 0).toLocaleString('id-ID') }}</td>
                <td class="px-3 py-1.5 text-zinc-500 truncate max-w-[120px]">{{ item.description || '—' }}</td>
                <td class="px-3 py-1.5 text-center">
                  <div class="flex justify-center gap-1">
                    <button class="rounded p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700" @click="openSubForm(item.item_type as 'G'|'B'|'C'|'D', idx)">
                      ✎
                    </button>
                    <button class="rounded p-1 text-red-400 hover:bg-red-50" @click="removeItem(idx)">
                      <Trash2 class="h-3 w-3" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ── GL SUB-FORM ────────────────────────────────────────────────── -->
      <div v-else-if="formView === 'G'" class="space-y-4">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div class="sm:col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Rekening Ledger (COA) <span class="text-red-500">*</span></label>
            <select
              :value="glAccountCode"
              :disabled="coaLoading"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
              @change="onCoaSelect(($event.target as HTMLSelectElement).value)"
            >
              <option value="">— Pilih akun —</option>
              <option v-for="opt in coaSelectOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>

          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Mutasi</label>
            <select v-model="glMutationType" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
              <option value="D">Debet</option>
              <option value="C">Kredit</option>
            </select>
          </div>

          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Nilai <span class="text-red-500">*</span></label>
            <AmountInput v-model="glAmount" />
          </div>

          <div class="sm:col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Keterangan</label>
            <input v-model="glDescription" placeholder="Opsional" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          </div>
        </div>
      </div>

      <!-- ── KAS/BANK SUB-FORM ──────────────────────────────────────────── -->
      <div v-else-if="formView === 'B'" class="space-y-4">
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-600">Rekening Kas / Bank <span class="text-red-500">*</span></label>
          <div class="flex gap-2">
            <input v-model="kbSearch" placeholder="Cari kode / nama rekening..." class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" @keyup.enter="searchKasBank" />
            <Button size="sm" variant="outline" :disabled="kbLoading" @click="searchKasBank">
              <Search class="h-3.5 w-3.5" />
              {{ kbLoading ? '...' : 'Cari' }}
            </Button>
          </div>
          <!-- Results -->
          <div v-if="kbShowResults && kbResults.length" class="mt-1 max-h-48 overflow-y-auto rounded border bg-white shadow-sm">
            <button
              v-for="r in kbResults" :key="r.account_no"
              class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50"
              @click="selectKasBank(r)"
            >
              <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
              <span>{{ r.account_name }}</span>
            </button>
          </div>
          <div v-if="kbShowResults && !kbResults.length" class="mt-1 rounded border bg-zinc-50 px-3 py-2 text-xs text-zinc-400">Tidak ada hasil</div>
          <!-- Selected -->
          <div v-if="kbSelectedNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
            <span class="font-mono text-xs text-zinc-400">{{ kbSelectedNo }}</span>
            <span class="text-sm font-medium text-zinc-700">{{ kbSelectedName }}</span>
            <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearKasBank"><X class="h-3.5 w-3.5" /></button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Mutasi</label>
            <select v-model="kbMutationType" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
              <option value="D">Debet</option>
              <option value="C">Kredit</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Nilai <span class="text-red-500">*</span></label>
            <AmountInput v-model="kbAmount" />
          </div>
          <div class="col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Keterangan</label>
            <input v-model="kbDescription" placeholder="Opsional" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          </div>
        </div>
      </div>

      <!-- ── PENGHIMPUNAN SUB-FORM ──────────────────────────────────────── -->
      <div v-else-if="formView === 'C'" class="space-y-4">
        <!-- Donatur lookup -->
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-600">Donatur</label>
          <div class="flex gap-2">
            <input v-model="phDonorSearch" placeholder="Cari nama / kode donatur..." class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" @keyup.enter="searchDonor" />
            <Button size="sm" variant="outline" :disabled="phDonorLoading" @click="searchDonor">
              <Search class="h-3.5 w-3.5" />
              {{ phDonorLoading ? '...' : 'Cari' }}
            </Button>
          </div>
          <div v-if="phShowDonorResults && phDonorResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm">
            <button
              v-for="r in phDonorResults" :key="r.donor_id"
              class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50"
              @click="selectDonor(r)"
            >
              <span class="text-sm">{{ r.donor_name }}</span>
              <span v-if="r.donor_no" class="ml-auto font-mono text-xs text-zinc-400">{{ r.donor_no }}</span>
            </button>
          </div>
          <div class="mt-1.5 flex items-center gap-3 rounded-lg bg-violet-50 px-3 py-2">
            <span class="text-sm font-medium text-violet-800">{{ phDonorName }}</span>
            <button v-if="phDonorId" class="ml-auto text-zinc-400 hover:text-red-500" @click="clearDonor"><X class="h-3.5 w-3.5" /></button>
          </div>
        </div>

        <!-- Produk lookup -->
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-600">Produk Penghimpunan <span class="text-red-500">*</span></label>
          <div class="flex gap-2">
            <input v-model="phProdukSearch" placeholder="Cari kode / nama produk..." class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" @keyup.enter="searchProduk" />
            <Button size="sm" variant="outline" :disabled="phProdukLoading" @click="searchProduk">
              <Search class="h-3.5 w-3.5" />
              {{ phProdukLoading ? '...' : 'Cari' }}
            </Button>
          </div>
          <div v-if="phShowProdukResults && phProdukResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm">
            <button
              v-for="r in phProdukResults" :key="r.account_no"
              class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50"
              @click="selectProduk(r)"
            >
              <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
              <span>{{ r.account_name }}</span>
            </button>
          </div>
          <div v-if="phProdukNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
            <span class="font-mono text-xs text-zinc-400">{{ phProdukNo }}</span>
            <span class="text-sm font-medium">{{ phProdukName }}</span>
            <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearProduk"><X class="h-3.5 w-3.5" /></button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Dana</label>
            <select v-model="phFundEntity" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
              <option v-for="o in FUND_ENTITY_OPTIONS" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Nilai <span class="text-red-500">*</span></label>
            <AmountInput v-model="phAmount" />
          </div>
          <div class="col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Keterangan</label>
            <input v-model="phDescription" placeholder="Opsional" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          </div>
          <div class="col-span-2">
            <label class="flex items-center gap-2 cursor-pointer rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-800 font-medium">
              <input type="checkbox" v-model="phIsReversal" class="rounded" />
              Transaksi koreksi / reversal
            </label>
          </div>
        </div>
      </div>

      <!-- ── PENYALURAN SUB-FORM ────────────────────────────────────────── -->
      <div v-else-if="formView === 'D'" class="space-y-4">
        <!-- Program Penyaluran -->
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-600">Nama Program <span class="text-red-500">*</span></label>
          <div class="flex gap-2">
            <input v-model="pyProgramSearch" placeholder="Cari kode / nama program..." class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" @keyup.enter="searchProgram" />
            <Button size="sm" variant="outline" :disabled="pyProgramLoading" @click="searchProgram">
              <Search class="h-3.5 w-3.5" />
              {{ pyProgramLoading ? '...' : 'Cari' }}
            </Button>
          </div>
          <div v-if="pyShowProgramResults && pyProgramResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm">
            <button
              v-for="r in pyProgramResults" :key="r.account_no"
              class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50"
              @click="selectProgram(r)"
            >
              <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
              <span>{{ r.account_name }}</span>
            </button>
          </div>
          <div v-if="pyProgramNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
            <span class="font-mono text-xs text-zinc-400">{{ pyProgramNo }}</span>
            <span class="text-sm font-medium">{{ pyProgramName }}</span>
            <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearProgram"><X class="h-3.5 w-3.5" /></button>
          </div>
        </div>

        <!-- Sumber Dana -->
        <div>
          <label class="mb-1 block text-xs font-medium text-zinc-600">Sumber Dana</label>
          <div class="flex gap-2">
            <input v-model="pySumberSearch" placeholder="Cari rekening sumber dana..." class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" @keyup.enter="searchSumber" />
            <Button size="sm" variant="outline" :disabled="pySumberLoading" @click="searchSumber">
              <Search class="h-3.5 w-3.5" />
              {{ pySumberLoading ? '...' : 'Cari' }}
            </Button>
          </div>
          <div v-if="pyShowSumberResults && pySumberResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm">
            <button
              v-for="r in pySumberResults" :key="r.account_no"
              class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50"
              @click="selectSumber(r)"
            >
              <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
              <span>{{ r.account_name }}</span>
            </button>
          </div>
          <div v-if="pySumberNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
            <span class="font-mono text-xs text-zinc-400">{{ pySumberNo }}</span>
            <span class="text-sm font-medium">{{ pySumberName }}</span>
            <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearSumber"><X class="h-3.5 w-3.5" /></button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Dana</label>
            <select v-model="pyFundEntity" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
              <option v-for="o in FUND_ENTITY_OPTIONS" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Ashnaf</label>
            <select v-model="pyAshnaf" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
              <option v-for="o in ASHNAF_OPTIONS" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Mutasi</label>
            <select v-model="pyMutationType" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
              <option value="D">Debet</option>
              <option value="C">Kredit</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Nilai <span class="text-red-500">*</span></label>
            <AmountInput v-model="pyAmount" />
          </div>
          <div class="col-span-2">
            <label class="mb-1 block text-xs font-medium text-zinc-600">Keterangan</label>
            <input v-model="pyDescription" placeholder="Opsional" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          </div>
          <div class="col-span-2">
            <label class="flex cursor-pointer items-center gap-2 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm font-medium text-amber-800">
              <input type="checkbox" v-model="pyIsCorrection" class="rounded" />
              Transaksi koreksi
            </label>
          </div>
        </div>
      </div>

      <!-- ── FOOTER ─────────────────────────────────────────────────────── -->
      <template #footer>
        <div v-if="formView === 'main'" class="flex items-center justify-between">
          <Button variant="outline" @click="showForm = false">Batal</Button>
          <Button
            :disabled="formSaving || !isBalanced || formItems.length < 2"
            @click="submitForm"
          >
            {{ formSaving ? 'Menyimpan...' : 'Submit untuk Otorisasi' }}
          </Button>
        </div>
        <div v-else class="flex justify-end gap-2">
          <Button variant="outline" @click="backToMain">Batal</Button>
          <Button @click="saveCurrentItem">Simpan Detail</Button>
        </div>
      </template>
    </Modal>

    <!-- ═══════════════════════════════════════════════════════════════════════
         DETAIL MODAL
    ════════════════════════════════════════════════════════════════════════ -->
    <Modal v-if="showDetail" max-width="max-w-3xl" @close="showDetail = false">
      <template #header><span class="font-semibold">Detail Transaksi Umum</span></template>

      <div v-if="detailRow" class="space-y-4">
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

        <div v-if="(detailRow as TxRow & { items?: unknown[] }).items">
          <div class="mb-2 text-xs font-semibold uppercase tracking-wide text-zinc-500">Baris Jurnal</div>
          <div class="overflow-x-auto rounded border">
            <table class="w-full text-xs">
              <thead class="border-b bg-zinc-50 text-[10px] uppercase tracking-widest text-zinc-500">
                <tr>
                  <th class="px-3 py-2 text-left">Kode / Referensi</th>
                  <th class="px-3 py-2 text-left">Nama</th>
                  <th class="px-3 py-2 text-center">D/K</th>
                  <th class="px-3 py-2 text-right">Jumlah</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, idx) in (detailRow as TxRow & { items?: Record<string,unknown>[] }).items"
                  :key="idx"
                  class="border-t"
                >
                  <td class="px-3 py-1.5 font-mono text-zinc-500">{{ (item.account_code as string) || '—' }}</td>
                  <td class="px-3 py-1.5">{{ item.account_name as string }}</td>
                  <td class="px-3 py-1.5 text-center font-bold" :class="item.mutation_type === 'D' ? 'text-emerald-700' : 'text-red-600'">
                    {{ item.mutation_type === 'D' ? 'Debet' : 'Kredit' }}
                  </td>
                  <td class="px-3 py-1.5 text-right font-mono">{{ (item.amount as number).toLocaleString('id-ID') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div v-else-if="detailLoading" class="py-4 text-center text-xs text-zinc-400">Memuat detail...</div>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <Button variant="outline" @click="showDetail = false">Tutup</Button>
        </div>
      </template>
    </Modal>
  </div>
</template>

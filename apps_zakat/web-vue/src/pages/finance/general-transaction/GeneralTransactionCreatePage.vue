<script setup lang="ts">
import { ArrowLeft, BookOpen, Pencil, RefreshCw, Search, Trash2, X } from 'lucide-vue-next'
import { computed, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────
interface ItemBase {
  valuta: string
  kurs: number
  nominal: number      // original currency amount (= amount when IDR)
  amount: number | null // IDR equivalent (nominal × kurs)
  mutation_type: 'D' | 'C'
  description: string
}

interface ItemGL extends ItemBase {
  item_type: 'G'
  account_code: string
  account_name: string
  kode_anggaran: string
  ket_anggaran: string
}

interface ItemKasBank extends ItemBase {
  item_type: 'B'
  account_no: string
  account_name: string
}

interface ItemPenghimpunan extends ItemBase {
  item_type: 'C'
  product_account_no: string
  product_name: string
  donor_id: number
  donor_name: string
  donor_no: string
  fund_entity: number
  is_reversal: boolean
}

interface ItemPenyaluran extends ItemBase {
  item_type: 'D'
  dist_account_no: string
  dist_account_name: string
  fund_account_no: string
  fund_account_name: string
  ashnaf: string
  fund_entity: number
  is_correction: boolean
}

type AnyItem = ItemGL | ItemKasBank | ItemPenghimpunan | ItemPenyaluran

interface CoaOption { code: string; name: string }
interface LookupRow { account_no: string; account_name: string }
interface DonorRow { donor_id: number; donor_name: string; donor_no?: string }

// ── Constants ─────────────────────────────────────────────────────────────────
const FUND_ENTITY_ALL = [
  { value: 1, label: 'Zakat' },
  { value: 2, label: 'Infaq' },
  { value: 3, label: 'Wakaf' },
  { value: 4, label: 'Amil' },
  { value: 5, label: 'Non-halal' },
]
const FUND_ENTITY_PENGHIMPUNAN = FUND_ENTITY_ALL.filter(o => o.value <= 3)

const ASHNAF_OPTIONS = [
  { value: 'F', label: 'Fakir' },
  { value: 'M', label: 'Miskin' },
  { value: 'U', label: 'Mualaf' },
  { value: 'H', label: 'Riqab' },
  { value: 'G', label: 'Gharimin' },
  { value: 'S', label: 'Fisabilillah' },
  { value: 'I', label: 'Ibnu Sabil' },
  { value: 'A', label: 'Amil' },
]

const VALUTA_OPTIONS = [
  { value: 'IDR', label: 'IDR — Rupiah' },
  { value: 'USD', label: 'USD — Dolar Amerika' },
  { value: 'EUR', label: 'EUR — Euro' },
  { value: 'MYR', label: 'MYR — Ringgit Malaysia' },
  { value: 'SGD', label: 'SGD — Dolar Singapura' },
  { value: 'SAR', label: 'SAR — Riyal Arab Saudi' },
]

const ITEM_LABELS: Record<string, string> = {
  G: 'GL Accounting',
  B: 'Kas/Bank',
  C: 'Penghimpunan',
  D: 'Penyaluran',
}
const ITEM_BADGES: Record<string, string> = {
  G: 'bg-blue-100 text-blue-700',
  B: 'bg-emerald-100 text-emerald-700',
  C: 'bg-violet-100 text-violet-700',
  D: 'bg-amber-100 text-amber-700',
}

// ── State: Header form ─────────────────────────────────────────────────────────
const router = useRouter()
const toast = useToast()
const today = new Date().toISOString().slice(0, 10)

const saving = shallowRef(false)
const formError = shallowRef<string | null>(null)
const formDate = shallowRef(today)
const formDescription = shallowRef('')
const formReferenceNo = shallowRef('')
const formItems = ref<AnyItem[]>([])

// ── State: Drawer ──────────────────────────────────────────────────────────────
const drawerOpen = shallowRef(false)
const drawerType = shallowRef<'G' | 'B' | 'C' | 'D' | null>(null)
const drawerEditIdx = shallowRef<number | null>(null)

// Nominal panel (shared)
const drawerValuta = shallowRef('IDR')
const drawerKurs = shallowRef(1)
const drawerNilai = shallowRef<number | null>(null)
const drawerMutationType = shallowRef<'D' | 'C'>('D')
const drawerDescription = shallowRef('')
const drawerEkuivalen = computed(() =>
  Math.round((drawerNilai.value ?? 0) * (drawerKurs.value || 1))
)

// GL-specific
const coaOptions = ref<CoaOption[]>([])
const coaLoading = shallowRef(false)
const glAccountCode = shallowRef('')
const glAccountName = shallowRef('')
const glKodeAnggaran = shallowRef('')
const glKetAnggaran = shallowRef('')

// KasBank-specific
const kbResults = ref<LookupRow[]>([])
const kbLoading = shallowRef(false)
const kbSelectedNo = shallowRef('')
const kbSelectedName = shallowRef('')
// v-model for SearchSelect — holds account_no of the selected rekening
const kbSelectedValue = shallowRef('')

// Penghimpunan-specific
const phDonorNo = shallowRef('')
const phDonorSearch = shallowRef('')
const phDonorResults = ref<DonorRow[]>([])
const phDonorLoading = shallowRef(false)
const phDonorId = shallowRef(0)
const phDonorName = shallowRef('HAMBA ALLAH')
const phShowDonorResults = shallowRef(false)
const phProdukResults = ref<LookupRow[]>([])
const phProdukLoading = shallowRef(false)
const phProdukNo = shallowRef('')
const phProdukName = shallowRef('')
const phFundEntity = shallowRef(1)
// v-model for SearchSelect — holds account_no of the selected produk
const phProdukSelectedValue = shallowRef('')

// Penyaluran-specific
const pyProgramResults = ref<LookupRow[]>([])
const pyProgramLoading = shallowRef(false)
const pyProgramNo = shallowRef('')
const pyProgramName = shallowRef('')
const pySumberResults = ref<LookupRow[]>([])
const pySumberLoading = shallowRef(false)
const pySumberNo = shallowRef('')
const pySumberName = shallowRef('')
const pyAshnaf = shallowRef('F')
const pyFundEntity = shallowRef(1)
// v-model for SearchSelect — holds account_no of the selected program / sumber
const pyProgramSelectedValue = shallowRef('')
const pySumberSelectedValue = shallowRef('')

// ── Computed ──────────────────────────────────────────────────────────────────
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
const kbOptions = computed(() =>
  kbResults.value.map(r => ({ value: r.account_no, label: `${r.account_no}  ${r.account_name}` }))
)
const phProdukOptions = computed(() =>
  phProdukResults.value.map(r => ({ value: r.account_no, label: `${r.account_no}  ${r.account_name}` }))
)
const pyProgramOptions = computed(() =>
  pyProgramResults.value.map(r => ({ value: r.account_no, label: `${r.account_no}  ${r.account_name}` }))
)
const pySumberOptions = computed(() =>
  pySumberResults.value.map(r => ({ value: r.account_no, label: `${r.account_no}  ${r.account_name}` }))
)
const drawerTitle = computed(() => {
  const titles: Record<string, string> = {
    G: 'Detail GL Accounting',
    B: 'Detail Kas / Bank',
    C: 'Detail Penghimpunan Dana',
    D: 'Detail Penyaluran Dana',
  }
  return titles[drawerType.value ?? ''] ?? 'Tambah Detail'
})
const mutationOptions = computed(() => {
  if (drawerType.value === 'C') {
    return [
      { value: 'C', label: 'Kredit (Penerimaan)' },
      { value: 'D', label: 'Debit (Reversal Penerimaan)' },
    ]
  }
  if (drawerType.value === 'D') {
    return [
      { value: 'D', label: 'Debit (Penyaluran)' },
      { value: 'C', label: 'Kredit (Reversal Penyaluran)' },
    ]
  }
  return [
    { value: 'D', label: 'Debet' },
    { value: 'C', label: 'Kredit' },
  ]
})

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

function onCoaSelect(code: string) {
  glAccountCode.value = code
  glAccountName.value = coaOptions.value.find(o => o.code === code)?.name ?? ''
}

async function loadKasBankOptions() {
  kbLoading.value = true
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/kasbank?search=`
    )
    kbResults.value = res?.rows ?? []
  } finally {
    kbLoading.value = false
  }
}

function clearKasBank() {
  kbSelectedNo.value = ''
  kbSelectedName.value = ''
  kbSelectedValue.value = ''
  kbResults.value = []
}

// Sync SearchSelect selection → downstream state (account_no + account_name)
watch(kbSelectedValue, (val) => {
  const found = kbResults.value.find(r => r.account_no === val)
  kbSelectedNo.value = found?.account_no ?? ''
  kbSelectedName.value = found?.account_name ?? ''
})

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
  phDonorNo.value = r.donor_no ?? ''
  phShowDonorResults.value = false
  phDonorSearch.value = ''
}

function clearDonor() {
  phDonorId.value = 0; phDonorName.value = 'HAMBA ALLAH'
  phDonorNo.value = ''; phDonorResults.value = []; phDonorSearch.value = ''
}

async function loadProdukOptions() {
  phProdukLoading.value = true
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/produk?search=&fund_entity=${phFundEntity.value}`
    )
    phProdukResults.value = res?.rows ?? []
  } finally {
    phProdukLoading.value = false
  }
}

function clearProduk() {
  phProdukNo.value = ''; phProdukName.value = ''
  phProdukSelectedValue.value = ''
}

// Sync SearchSelect selection → downstream state
watch(phProdukSelectedValue, (val) => {
  const found = phProdukResults.value.find(r => r.account_no === val)
  phProdukNo.value = found?.account_no ?? ''
  phProdukName.value = found?.account_name ?? ''
})

// Reload produk list when fund entity changes (and drawer is open for type C)
watch(phFundEntity, () => {
  phProdukSelectedValue.value = ''
  phProdukNo.value = ''
  phProdukName.value = ''
  loadProdukOptions()
})

async function loadProgramOptions() {
  pyProgramLoading.value = true
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/penyaluran?search=`
    )
    pyProgramResults.value = res?.rows ?? []
  } finally {
    pyProgramLoading.value = false
  }
}

function clearProgram() {
  pyProgramNo.value = ''; pyProgramName.value = ''
  pyProgramSelectedValue.value = ''
}

// Sync SearchSelect selection → downstream state
watch(pyProgramSelectedValue, (val) => {
  const found = pyProgramResults.value.find(r => r.account_no === val)
  pyProgramNo.value = found?.account_no ?? ''
  pyProgramName.value = found?.account_name ?? ''
})

async function loadSumberOptions() {
  pySumberLoading.value = true
  try {
    const res = await api.get<{ rows: LookupRow[] }>(
      `/api/transaksi-umum/lookup/produk?search=`
    )
    pySumberResults.value = res?.rows ?? []
  } finally {
    pySumberLoading.value = false
  }
}

function clearSumber() {
  pySumberNo.value = ''; pySumberName.value = ''
  pySumberSelectedValue.value = ''
}

// Sync SearchSelect selection → downstream state
watch(pySumberSelectedValue, (val) => {
  const found = pySumberResults.value.find(r => r.account_no === val)
  pySumberNo.value = found?.account_no ?? ''
  pySumberName.value = found?.account_name ?? ''
})

// ── Drawer control ────────────────────────────────────────────────────────────
function resetNominalPanel(defaultMutation: 'D' | 'C') {
  drawerValuta.value = 'IDR'
  drawerKurs.value = 1
  drawerNilai.value = null
  drawerMutationType.value = defaultMutation
  drawerDescription.value = ''
}

function openDrawer(type: 'G' | 'B' | 'C' | 'D', editIdx: number | null = null) {
  drawerType.value = type
  drawerEditIdx.value = editIdx

  if (editIdx !== null) {
    const item = formItems.value[editIdx]
    drawerValuta.value = item.valuta
    drawerKurs.value = item.kurs
    drawerNilai.value = item.nominal
    drawerMutationType.value = item.mutation_type
    drawerDescription.value = item.description

    if (item.item_type === 'G') {
      glAccountCode.value = item.account_code
      glAccountName.value = item.account_name
      glKodeAnggaran.value = item.kode_anggaran
      glKetAnggaran.value = item.ket_anggaran
    } else if (item.item_type === 'B') {
      kbSelectedNo.value = item.account_no
      kbSelectedName.value = item.account_name
      kbSelectedValue.value = item.account_no
      loadKasBankOptions()
    } else if (item.item_type === 'C') {
      phDonorId.value = item.donor_id
      phDonorName.value = item.donor_name
      phDonorNo.value = item.donor_no
      phProdukNo.value = item.product_account_no
      phProdukName.value = item.product_name
      phFundEntity.value = item.fund_entity
      // load produk options then restore selection
      loadProdukOptions().then(() => {
        phProdukSelectedValue.value = item.product_account_no
      })
    } else if (item.item_type === 'D') {
      pyProgramNo.value = item.dist_account_no
      pyProgramName.value = item.dist_account_name
      pySumberNo.value = item.fund_account_no
      pySumberName.value = item.fund_account_name
      pyAshnaf.value = item.ashnaf
      pyFundEntity.value = item.fund_entity
      // load options then restore selections
      loadProgramOptions().then(() => {
        pyProgramSelectedValue.value = item.dist_account_no
      })
      loadSumberOptions().then(() => {
        pySumberSelectedValue.value = item.fund_account_no
      })
    }
  } else {
    if (type === 'G') {
      resetNominalPanel('D')
      glAccountCode.value = ''; glAccountName.value = ''
      glKodeAnggaran.value = ''; glKetAnggaran.value = ''
      loadCoa()
    } else if (type === 'B') {
      resetNominalPanel('D')
      clearKasBank()
      loadKasBankOptions()
    } else if (type === 'C') {
      resetNominalPanel('C')
      clearDonor(); clearProduk()
      phFundEntity.value = 1
      loadProdukOptions()
    } else if (type === 'D') {
      resetNominalPanel('D')
      clearProgram(); clearSumber()
      pyAshnaf.value = 'F'; pyFundEntity.value = 1
      loadProgramOptions()
      loadSumberOptions()
    }
  }

  drawerOpen.value = true
}

function closeDrawer() {
  drawerOpen.value = false
  drawerType.value = null
  drawerEditIdx.value = null
}

function saveDrawerItem() {
  if (!drawerNilai.value || drawerNilai.value <= 0) {
    toast.error('Nilai harus lebih dari 0')
    return
  }
  const base: ItemBase = {
    valuta: drawerValuta.value,
    kurs: drawerKurs.value || 1,
    nominal: drawerNilai.value,
    amount: drawerEkuivalen.value,
    mutation_type: drawerMutationType.value,
    description: drawerDescription.value,
  }

  let item: AnyItem | null = null

  if (drawerType.value === 'G') {
    if (!glAccountCode.value) { toast.error('Pilih akun COA'); return }
    item = {
      ...base,
      item_type: 'G',
      account_code: glAccountCode.value,
      account_name: glAccountName.value,
      kode_anggaran: glKodeAnggaran.value,
      ket_anggaran: glKetAnggaran.value,
    }
  } else if (drawerType.value === 'B') {
    if (!kbSelectedNo.value) { toast.error('Pilih rekening kas/bank'); return }
    item = {
      ...base,
      item_type: 'B',
      account_no: kbSelectedNo.value,
      account_name: kbSelectedName.value,
    }
  } else if (drawerType.value === 'C') {
    if (!phProdukNo.value) { toast.error('Pilih produk penghimpunan'); return }
    item = {
      ...base,
      item_type: 'C',
      product_account_no: phProdukNo.value,
      product_name: phProdukName.value,
      donor_id: phDonorId.value,
      donor_name: phDonorName.value,
      donor_no: phDonorNo.value,
      fund_entity: phFundEntity.value,
      is_reversal: drawerMutationType.value === 'D',
    }
  } else if (drawerType.value === 'D') {
    if (!pyProgramNo.value) { toast.error('Pilih program penyaluran'); return }
    item = {
      ...base,
      item_type: 'D',
      dist_account_no: pyProgramNo.value,
      dist_account_name: pyProgramName.value,
      fund_account_no: pySumberNo.value,
      fund_account_name: pySumberName.value,
      ashnaf: pyAshnaf.value,
      fund_entity: pyFundEntity.value,
      is_correction: drawerMutationType.value === 'C',
    }
  }

  if (!item) return
  if (drawerEditIdx.value !== null) formItems.value[drawerEditIdx.value] = item
  else formItems.value.push(item)
  closeDrawer()
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

// Reset kurs to 1 when switching back to IDR
watch(drawerValuta, (v) => {
  if (v === 'IDR') drawerKurs.value = 1
})

// ── Reset Detail ──────────────────────────────────────────────────────────────
function resetDetail() {
  formItems.value = []
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

  saving.value = true
  try {
    await api.post('/api/transaksi-umum/', {
      actual_date: formDate.value,
      description: formDescription.value.trim(),
      reference_no: formReferenceNo.value.trim(),
      items: formItems.value,
    })
    toast.success('Transaksi umum berhasil disubmit untuk otorisasi')
    router.push({ name: 'finance-transactions-general' })
  } catch (e: unknown) {
    const msg = (e as { message?: string })?.message ?? 'Gagal menyimpan transaksi'
    formError.value = msg
    toast.error(msg)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Back + title -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-transactions-general' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
      <BookOpen class="h-4 w-4 text-indigo-600" />
      <h1 class="text-base font-semibold text-slate-800">Input Transaksi Umum</h1>
    </div>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <!-- Split layout -->
    <div class="flex flex-col gap-3 lg:flex-row lg:items-start">

      <!-- LEFT: sticky header + summary -->
      <div class="w-full space-y-3 lg:w-[340px] lg:flex-shrink-0 lg:sticky lg:top-[64px]">

        <!-- Header form card -->
        <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden">
          <!-- Card header bar -->
          <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
            <h2 class="font-bold text-xs tracking-widest text-white uppercase">Header Transaksi</h2>
            <span class="bg-slate-600 text-white text-xs px-2 py-0.5 rounded">DRAFT</span>
          </div>
          <!-- Card body -->
          <div class="p-4 space-y-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tanggal Transaksi</label>
              <DateField v-model="formDate" />
            </div>
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Keterangan Transaksi <span class="text-red-500">*</span>
              </label>
              <textarea
                v-model="formDescription"
                placeholder="Keterangan transaksi..."
                rows="3"
                class="w-full border border-slate-200 rounded px-3 py-1.5 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-y min-h-[72px]"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Referensi / Cek / Kwitansi</label>
              <input
                v-model="formReferenceNo"
                placeholder="Opsional"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
        </div>

        <!-- Summary card + save -->
        <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden">
          <!-- Card header bar -->
          <div class="flex items-center justify-between bg-slate-700 px-4 py-2">
            <h2 class="font-bold text-xs tracking-widest text-white uppercase">Ringkasan</h2>
            <span
              class="text-xs px-2 py-0.5 rounded font-semibold"
              :class="isBalanced && formItems.length ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white'"
            >
              {{ isBalanced && formItems.length ? '• Balance' : '• Belum Balance' }}
            </span>
          </div>
          <!-- Card body -->
          <div class="p-4 space-y-3">
            <div class="grid grid-cols-2 gap-2">
              <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:bg-zinc-800">
                <div class="text-xs text-slate-500">Total Debet</div>
                <div class="mt-0.5 font-mono text-sm font-bold text-emerald-700">
                  {{ totalDebet.toLocaleString('id-ID') }}
                </div>
              </div>
              <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:bg-zinc-800">
                <div class="text-xs text-slate-500">Total Kredit</div>
                <div class="mt-0.5 font-mono text-sm font-bold text-red-600">
                  {{ totalKredit.toLocaleString('id-ID') }}
                </div>
              </div>
              <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:bg-zinc-800">
                <div class="text-xs text-slate-500">Selisih</div>
                <div class="mt-0.5 font-mono text-sm font-bold text-slate-700">
                  {{ Math.abs(totalDebet - totalKredit).toLocaleString('id-ID') }}
                </div>
              </div>
              <div
                class="rounded-lg border p-3"
                :class="isBalanced && formItems.length ? 'bg-green-50 border-green-200 dark:bg-green-900/20' : 'bg-slate-50 border-slate-200 dark:bg-zinc-800'"
              >
                <div class="text-xs text-slate-500">Status</div>
                <div
                  class="mt-0.5 text-sm font-bold"
                  :class="isBalanced && formItems.length ? 'text-green-700' : 'text-slate-400'"
                >
                  {{ isBalanced && formItems.length ? '✓ Balance' : formItems.length ? '✗ Belum Balance' : '—' }}
                </div>
              </div>
            </div>

            <div class="flex gap-2 pt-1">
              <button
                class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
                @click="router.push({ name: 'finance-transactions-general' })"
              >
                Batal
              </button>
              <button
                class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="saving || !isBalanced || formItems.length < 2"
                @click="submitForm"
              >
                {{ saving ? 'Menyimpan...' : 'Simpan Transaksi' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: detail table -->
      <div class="min-w-0 flex-1 space-y-0 rounded-lg border border-slate-200 overflow-hidden">
        <!-- Detail Transaksi header bar -->
        <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
          <h2 class="font-bold text-xs tracking-widest text-white uppercase">Detail Transaksi</h2>
          <span class="bg-slate-600 text-white text-xs px-2 py-0.5 rounded">
            {{ formItems.length }} item
          </span>
        </div>
        <!-- Toolbar: add buttons -->
        <div class="flex flex-wrap items-center gap-2 border-b border-slate-200 bg-slate-50 px-3 py-2 dark:bg-zinc-800/50">
          <Button size="sm" variant="outline" @click="openDrawer('B')">+ Kas / Bank</Button>
          <Button size="sm" variant="outline" @click="openDrawer('D')">+ Penyaluran Dana</Button>
          <Button size="sm" variant="outline" @click="openDrawer('C')">+ Penghimpunan Dana</Button>
          <Button size="sm" variant="outline" @click="openDrawer('G')">+ GL Accounting</Button>
          <div class="ml-auto">
            <button
              v-if="formItems.length > 0"
              class="flex items-center gap-1.5 border border-red-300 text-red-600 hover:bg-red-50 text-xs px-3 py-1.5 rounded"
              @click="resetDetail"
            >
              <RefreshCw class="h-3 w-3" />
              Reset Detail
            </button>
          </div>
        </div>

        <!-- Items table -->
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead class="border-b border-slate-200 bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:bg-zinc-800/50 dark:text-zinc-400">
              <tr>
                <th class="px-3 py-1.5 text-left">Jenis</th>
                <th class="px-3 py-1.5 text-left">Referensi</th>
                <th class="px-3 py-1.5 text-center w-28">Mutasi</th>
                <th class="px-3 py-1.5 text-right w-36">Jumlah (IDR)</th>
                <th class="px-3 py-1.5 text-left">Keterangan</th>
                <th class="px-3 py-1.5 w-16"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="formItems.length === 0">
                <td colspan="6" class="px-3 py-6 text-center text-xs text-slate-400">
                  Belum ada item — klik tombol tambah di atas
                </td>
              </tr>
              <tr v-for="(item, idx) in formItems" :key="idx" class="border-t border-slate-100 hover:bg-indigo-50/40 even:bg-slate-50/50">
                <td class="px-3 py-1.5">
                  <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold', ITEM_BADGES[item.item_type]]">
                    {{ ITEM_LABELS[item.item_type] }}
                  </span>
                </td>
                <td class="px-3 py-1.5 max-w-[200px] truncate text-slate-600" :title="itemRef(item)">
                  {{ itemRef(item) }}
                </td>
                <td class="px-3 py-1.5 text-center">
                  <span
                    class="font-semibold text-[10px]"
                    :class="item.mutation_type === 'D' ? 'text-emerald-700' : 'text-red-600'"
                  >
                    {{ item.mutation_type === 'D' ? 'Debet' : 'Kredit' }}
                  </span>
                  <span v-if="item.valuta !== 'IDR'" class="ml-1 rounded bg-slate-100 px-1 text-[10px] text-slate-500">
                    {{ item.valuta }}
                  </span>
                </td>
                <td class="px-3 py-1.5 text-right font-mono font-semibold text-slate-800">
                  {{ (item.amount ?? 0).toLocaleString('id-ID') }}
                </td>
                <td class="px-3 py-1.5 max-w-[120px] truncate text-slate-500">{{ item.description || '—' }}</td>
                <td class="px-3 py-1.5 text-center">
                  <div class="flex justify-center gap-1">
                    <button
                      class="rounded p-1.5 text-indigo-500 hover:bg-indigo-50 hover:text-indigo-700"
                      title="Edit"
                      @click="openDrawer(item.item_type as 'G'|'B'|'C'|'D', idx)"
                    >
                      <Pencil class="h-4 w-4" />
                    </button>
                    <button
                      class="rounded p-1.5 text-red-500 hover:bg-red-50 hover:text-red-700"
                      title="Hapus"
                      @click="removeItem(idx)"
                    >
                      <Trash2 class="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- ── DRAWER (slide from right) ────────────────────────────────────────── -->
    <Transition
      enter-active-class="transition-opacity duration-200"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-150"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="drawerOpen"
        class="fixed inset-0 z-50 flex justify-end bg-black/40"
        @click.self="closeDrawer"
      >
        <aside class="relative flex h-full w-full max-w-[960px] flex-col bg-white shadow-2xl dark:bg-zinc-900">
          <!-- Drawer header -->
          <div class="flex items-center justify-between border-b border-slate-200 px-4 py-3">
            <h2 class="text-sm font-semibold text-slate-800 dark:text-zinc-200">{{ drawerTitle }}</h2>
            <button
              class="rounded-lg p-1 text-slate-400 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
              @click="closeDrawer"
            >
              <X class="h-4 w-4" />
            </button>
          </div>

          <!-- Drawer body: form (left) + nominal panel (right) -->
          <div class="flex min-h-0 flex-1">

            <!-- LEFT: type-specific form fields -->
            <div class="flex-1 overflow-y-auto p-4 space-y-4">

              <!-- ── GL fields ─────────────────────────────────────────── -->
              <template v-if="drawerType === 'G'">
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">
                    Rekening Ledger (COA) <span class="text-red-500">*</span>
                  </label>
                  <select
                    :value="glAccountCode"
                    :disabled="coaLoading"
                    class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    @change="onCoaSelect(($event.target as HTMLSelectElement).value)"
                  >
                    <option value="">{{ coaLoading ? 'Memuat...' : '— Pilih akun —' }}</option>
                    <option v-for="opt in coaSelectOptions" :key="opt.value" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Kode Anggaran</label>
                    <input
                      v-model="glKodeAnggaran"
                      placeholder="Opsional"
                      class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                  <div>
                    <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Ket. Anggaran</label>
                    <input
                      v-model="glKetAnggaran"
                      placeholder="Opsional"
                      class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>
              </template>

              <!-- ── KasBank fields ─────────────────────────────────────── -->
              <template v-else-if="drawerType === 'B'">
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">
                    Rekening Kas / Bank <span class="text-red-500">*</span>
                  </label>
                  <div v-if="kbLoading" class="flex items-center gap-2 text-xs text-slate-400 py-1.5">
                    <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-slate-300 border-t-indigo-500 rounded-full"></span>
                    Memuat daftar rekening...
                  </div>
                  <SearchSelect
                    v-else
                    v-model="kbSelectedValue"
                    :options="kbOptions"
                    placeholder="Cari kode / nama rekening..."
                  />
                </div>
              </template>

              <!-- ── Penghimpunan fields ─────────────────────────────────── -->
              <template v-else-if="drawerType === 'C'">
                <!-- Donatur -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Donatur</label>
                  <div class="flex gap-2">
                    <input
                      v-model="phDonorSearch"
                      placeholder="Cari nama donatur..."
                      class="flex-1 rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      @keyup.enter="searchDonor"
                    />
                    <Button size="sm" variant="outline" :disabled="phDonorLoading" @click="searchDonor">
                      <Search class="h-3.5 w-3.5" />
                      {{ phDonorLoading ? '...' : 'Cari' }}
                    </Button>
                  </div>
                  <div v-if="phShowDonorResults && phDonorResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border border-slate-200 bg-white shadow-sm dark:bg-zinc-900">
                    <button
                      v-for="r in phDonorResults" :key="r.donor_id"
                      class="flex w-full items-center gap-3 border-b border-slate-100 px-3 py-1.5 text-left text-sm last:border-0 hover:bg-indigo-50/40 dark:hover:bg-zinc-800"
                      @click="selectDonor(r)"
                    >
                      <span class="font-mono text-xs text-slate-400">{{ r.donor_no || '—' }}</span>
                      <span>{{ r.donor_name }}</span>
                    </button>
                  </div>
                  <div class="mt-1.5 grid grid-cols-[100px_1fr] gap-2">
                    <div>
                      <label class="mb-0.5 block text-[10px] text-slate-400 uppercase tracking-wide">Kode Donatur</label>
                      <input
                        v-model="phDonorNo"
                        placeholder="—"
                        class="w-full rounded border border-slate-200 px-3 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                      />
                    </div>
                    <div>
                      <label class="mb-0.5 block text-[10px] text-slate-400 uppercase tracking-wide">Nama Donatur</label>
                      <div class="flex items-center gap-2 rounded-lg bg-violet-50 border border-violet-100 px-3 py-1.5 dark:bg-violet-900/20">
                        <span class="flex-1 text-sm font-medium text-violet-800 dark:text-violet-300">{{ phDonorName }}</span>
                        <button v-if="phDonorId" class="text-slate-400 hover:text-red-500" @click="clearDonor">
                          <X class="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Produk Penghimpunan -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">
                    Produk Penghimpunan <span class="text-red-500">*</span>
                  </label>
                  <div v-if="phProdukLoading" class="flex items-center gap-2 text-xs text-slate-400 py-1.5">
                    <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-slate-300 border-t-indigo-500 rounded-full"></span>
                    Memuat daftar produk...
                  </div>
                  <SearchSelect
                    v-else
                    v-model="phProdukSelectedValue"
                    :options="phProdukOptions"
                    placeholder="Cari kode / nama produk..."
                  />
                </div>

                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Jenis Dana</label>
                  <select v-model="phFundEntity" class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                    <option v-for="o in FUND_ENTITY_PENGHIMPUNAN" :key="o.value" :value="o.value">{{ o.label }}</option>
                  </select>
                </div>
              </template>

              <!-- ── Penyaluran fields ──────────────────────────────────── -->
              <template v-else-if="drawerType === 'D'">
                <!-- Program Penyaluran -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">
                    Nama Program <span class="text-red-500">*</span>
                  </label>
                  <div v-if="pyProgramLoading" class="flex items-center gap-2 text-xs text-slate-400 py-1.5">
                    <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-slate-300 border-t-indigo-500 rounded-full"></span>
                    Memuat daftar program...
                  </div>
                  <SearchSelect
                    v-else
                    v-model="pyProgramSelectedValue"
                    :options="pyProgramOptions"
                    placeholder="Cari kode / nama program..."
                  />
                </div>

                <!-- Sumber Dana -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Sumber Dana</label>
                  <div v-if="pySumberLoading" class="flex items-center gap-2 text-xs text-slate-400 py-1.5">
                    <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-slate-300 border-t-indigo-500 rounded-full"></span>
                    Memuat daftar sumber dana...
                  </div>
                  <SearchSelect
                    v-else
                    v-model="pySumberSelectedValue"
                    :options="pySumberOptions"
                    placeholder="Cari rekening sumber dana..."
                  />
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Jenis Dana</label>
                    <select v-model="pyFundEntity" class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                      <option v-for="o in FUND_ENTITY_ALL" :key="o.value" :value="o.value">{{ o.label }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Ashnaf</label>
                    <select v-model="pyAshnaf" class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
                      <option v-for="o in ASHNAF_OPTIONS" :key="o.value" :value="o.value">{{ o.label }}</option>
                    </select>
                  </div>
                </div>
              </template>

            </div><!-- end left form -->

            <!-- RIGHT: nominal panel -->
            <div class="w-60 flex-shrink-0 overflow-y-auto border-l border-slate-200 bg-slate-50/80 p-4 space-y-3 dark:bg-zinc-800/50 dark:border-zinc-700">
              <h3 class="text-xs font-semibold uppercase tracking-wide text-slate-500">Nominal Transaksi</h3>

              <div>
                <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Jenis Mutasi</label>
                <select
                  v-model="drawerMutationType"
                  class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option v-for="opt in mutationOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>

              <div>
                <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Valuta</label>
                <select
                  v-model="drawerValuta"
                  class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option v-for="v in VALUTA_OPTIONS" :key="v.value" :value="v.value">{{ v.label }}</option>
                </select>
              </div>

              <div>
                <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">
                  Nilai <span v-if="drawerValuta !== 'IDR'" class="text-slate-400">({{ drawerValuta }})</span>
                  <span class="text-red-500">*</span>
                </label>
                <AmountInput v-model="drawerNilai" />
              </div>

              <template v-if="drawerValuta !== 'IDR'">
                <div>
                  <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Kurs (ke IDR)</label>
                  <input
                    v-model.number="drawerKurs"
                    type="number"
                    min="1"
                    step="1"
                    placeholder="Contoh: 15000"
                    class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div class="rounded-lg border border-blue-200 bg-blue-50 p-2.5 dark:bg-blue-900/20">
                  <div class="text-[10px] text-slate-500 mb-1">Ekuivalen IDR</div>
                  <div class="font-mono text-sm font-bold text-blue-700 dark:text-blue-400">
                    {{ drawerEkuivalen.toLocaleString('id-ID') }}
                  </div>
                  <div class="mt-1 text-[10px] text-slate-400">
                    {{ (drawerNilai ?? 0).toLocaleString('id-ID') }} × {{ drawerKurs.toLocaleString('id-ID') }}
                  </div>
                </div>
              </template>

              <div>
                <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Keterangan</label>
                <input
                  v-model="drawerDescription"
                  placeholder="Opsional"
                  class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <!-- Summary preview -->
              <div v-if="drawerNilai" class="rounded-lg border border-slate-200 bg-white p-2.5 text-xs dark:bg-zinc-900">
                <div class="flex justify-between text-slate-500">
                  <span>Mutasi</span>
                  <span :class="drawerMutationType === 'D' ? 'font-semibold text-emerald-700' : 'font-semibold text-red-600'">
                    {{ drawerMutationType === 'D' ? 'Debet' : 'Kredit' }}
                  </span>
                </div>
                <div class="mt-1 flex justify-between">
                  <span class="text-slate-500">IDR</span>
                  <span class="font-mono font-bold text-slate-800 dark:text-zinc-200">
                    {{ drawerEkuivalen.toLocaleString('id-ID') }}
                  </span>
                </div>
              </div>
            </div><!-- end nominal panel -->

          </div><!-- end drawer body -->

          <!-- Drawer footer -->
          <div class="flex justify-end gap-2 border-t border-slate-200 px-4 py-2.5 dark:border-zinc-700">
            <Button variant="outline" size="sm" @click="closeDrawer">Batal</Button>
            <Button variant="success" size="sm" @click="saveDrawerItem">Simpan Detail</Button>
          </div>
        </aside>
      </div>
    </Transition>
  </div>
</template>

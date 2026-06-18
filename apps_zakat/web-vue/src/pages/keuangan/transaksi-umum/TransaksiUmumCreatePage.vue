<script setup lang="ts">
import { ArrowLeft, BookOpen, Search, Trash2, X } from 'lucide-vue-next'
import { computed, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
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
const kbSearch = shallowRef('')
const kbResults = ref<LookupRow[]>([])
const kbLoading = shallowRef(false)
const kbSelectedNo = shallowRef('')
const kbSelectedName = shallowRef('')
const kbShowResults = shallowRef(false)

// Penghimpunan-specific
const phDonorNo = shallowRef('')
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
const phShowDonorResults = shallowRef(false)
const phShowProdukResults = shallowRef(false)

// Penyaluran-specific
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
const pyShowProgramResults = shallowRef(false)
const pyShowSumberResults = shallowRef(false)

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
  kbSearch.value = ''
}

function clearKasBank() {
  kbSelectedNo.value = ''; kbSelectedName.value = ''
  kbResults.value = []; kbSearch.value = ''
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
  phDonorNo.value = r.donor_no ?? ''
  phShowDonorResults.value = false
  phDonorSearch.value = ''
}

function clearDonor() {
  phDonorId.value = 0; phDonorName.value = 'HAMBA ALLAH'
  phDonorNo.value = ''; phDonorResults.value = []; phDonorSearch.value = ''
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
  phProdukSearch.value = ''
}

function clearProduk() {
  phProdukNo.value = ''; phProdukName.value = ''
  phProdukResults.value = []; phProdukSearch.value = ''
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
  pyProgramSearch.value = ''
}

function clearProgram() {
  pyProgramNo.value = ''; pyProgramName.value = ''
  pyProgramResults.value = []; pyProgramSearch.value = ''
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
  pySumberSearch.value = ''
}

function clearSumber() {
  pySumberNo.value = ''; pySumberName.value = ''
  pySumberResults.value = []; pySumberSearch.value = ''
}

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
    } else if (item.item_type === 'C') {
      phDonorId.value = item.donor_id
      phDonorName.value = item.donor_name
      phDonorNo.value = item.donor_no
      phProdukNo.value = item.product_account_no
      phProdukName.value = item.product_name
      phFundEntity.value = item.fund_entity
    } else if (item.item_type === 'D') {
      pyProgramNo.value = item.dist_account_no
      pyProgramName.value = item.dist_account_name
      pySumberNo.value = item.fund_account_no
      pySumberName.value = item.fund_account_name
      pyAshnaf.value = item.ashnaf
      pyFundEntity.value = item.fund_entity
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
    } else if (type === 'C') {
      resetNominalPanel('C')
      clearDonor(); clearProduk()
      phFundEntity.value = 1
    } else if (type === 'D') {
      resetNominalPanel('D')
      clearProgram(); clearSumber()
      pyAshnaf.value = 'F'; pyFundEntity.value = 1
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
    router.push({ name: 'keuangan-transaksi-umum' })
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
  <div class="p-4 sm:p-6 space-y-4">
    <!-- Back + title -->
    <div class="flex items-center gap-3">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-sm text-zinc-500 hover:bg-zinc-100 hover:text-zinc-800 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'keuangan-transaksi-umum' })"
      >
        <ArrowLeft class="h-4 w-4" />
        Kembali
      </button>
      <BookOpen class="h-5 w-5 text-primary" />
      <h1 class="text-xl font-bold text-foreground">Input Transaksi Umum</h1>
    </div>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <!-- Split layout -->
    <div class="flex flex-col gap-6 lg:flex-row lg:items-start">

      <!-- LEFT: sticky header + summary -->
      <div class="w-full space-y-4 lg:w-[380px] lg:flex-shrink-0 lg:sticky lg:top-[64px]">

        <!-- Header form card -->
        <div class="rounded-xl border bg-white p-4 dark:bg-zinc-900 space-y-3">
          <h2 class="text-sm font-semibold text-zinc-700 dark:text-zinc-300">Header Transaksi</h2>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">Tanggal Transaksi</label>
            <DateField v-model="formDate" />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">
              Deskripsi <span class="text-red-500">*</span>
            </label>
            <input
              v-model="formDescription"
              placeholder="Keterangan transaksi..."
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium text-zinc-600">No. Referensi / Cek / Kwitansi</label>
            <input
              v-model="formReferenceNo"
              placeholder="Opsional"
              class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>

        <!-- Summary card + save -->
        <div class="rounded-xl border bg-white p-4 dark:bg-zinc-900 space-y-3">
          <h2 class="text-sm font-semibold text-zinc-700 dark:text-zinc-300">Ringkasan</h2>
          <div class="grid grid-cols-2 gap-2">
            <div class="rounded-lg border bg-zinc-50 p-3 dark:bg-zinc-800">
              <div class="text-xs text-zinc-500">Total Debet</div>
              <div class="mt-0.5 font-mono text-base font-bold text-emerald-700">
                {{ totalDebet.toLocaleString('id-ID') }}
              </div>
            </div>
            <div class="rounded-lg border bg-zinc-50 p-3 dark:bg-zinc-800">
              <div class="text-xs text-zinc-500">Total Kredit</div>
              <div class="mt-0.5 font-mono text-base font-bold text-red-600">
                {{ totalKredit.toLocaleString('id-ID') }}
              </div>
            </div>
            <div class="rounded-lg border bg-zinc-50 p-3 dark:bg-zinc-800">
              <div class="text-xs text-zinc-500">Selisih</div>
              <div class="mt-0.5 font-mono text-base font-bold text-zinc-700">
                {{ Math.abs(totalDebet - totalKredit).toLocaleString('id-ID') }}
              </div>
            </div>
            <div
              class="rounded-lg border p-3"
              :class="isBalanced && formItems.length ? 'bg-green-50 border-green-200 dark:bg-green-900/20' : 'bg-zinc-50 dark:bg-zinc-800'"
            >
              <div class="text-xs text-zinc-500">Status</div>
              <div
                class="mt-0.5 text-sm font-bold"
                :class="isBalanced && formItems.length ? 'text-green-700' : 'text-zinc-400'"
              >
                {{ isBalanced && formItems.length ? '✓ Balance' : formItems.length ? '✗ Belum Balance' : '—' }}
              </div>
            </div>
          </div>

          <div class="flex gap-2 pt-1">
            <Button variant="outline" class="flex-1" @click="router.push({ name: 'keuangan-transaksi-umum' })">
              Batal
            </Button>
            <Button
              variant="success"
              class="flex-1"
              :disabled="saving || !isBalanced || formItems.length < 2"
              @click="submitForm"
            >
              {{ saving ? 'Menyimpan...' : 'Simpan' }}
            </Button>
          </div>
        </div>
      </div>

      <!-- RIGHT: detail table -->
      <div class="min-w-0 flex-1 space-y-0">
        <!-- Toolbar: add buttons -->
        <div class="flex flex-wrap gap-2 rounded-t border bg-zinc-50 px-4 py-2.5 dark:bg-zinc-800/50">
          <Button size="sm" variant="outline" @click="openDrawer('B')">+ Kas / Bank</Button>
          <Button size="sm" variant="outline" @click="openDrawer('D')">+ Penyaluran Dana</Button>
          <Button size="sm" variant="outline" @click="openDrawer('C')">+ Penghimpunan Dana</Button>
          <Button size="sm" variant="outline" @click="openDrawer('G')">+ GL Accounting</Button>
        </div>

        <!-- Items table -->
        <div class="overflow-x-auto rounded-b border">
          <table class="w-full text-xs">
            <thead class="border-b bg-zinc-50 text-xs font-semibold text-zinc-600 dark:bg-zinc-800/50 dark:text-zinc-400">
              <tr>
                <th class="px-3 py-2 text-left">Jenis</th>
                <th class="px-3 py-2 text-left">Referensi</th>
                <th class="px-3 py-2 text-center w-28">Mutasi</th>
                <th class="px-3 py-2 text-right w-36">Jumlah (IDR)</th>
                <th class="px-3 py-2 text-left">Keterangan</th>
                <th class="px-3 py-2 w-16"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="formItems.length === 0">
                <td colspan="6" class="px-3 py-8 text-center text-zinc-400">
                  Belum ada item — klik tombol tambah di atas
                </td>
              </tr>
              <tr v-for="(item, idx) in formItems" :key="idx" class="border-t">
                <td class="px-3 py-2">
                  <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold', ITEM_BADGES[item.item_type]]">
                    {{ ITEM_LABELS[item.item_type] }}
                  </span>
                </td>
                <td class="px-3 py-2 max-w-[200px] truncate text-zinc-600" :title="itemRef(item)">
                  {{ itemRef(item) }}
                </td>
                <td class="px-3 py-2 text-center">
                  <span
                    class="font-semibold text-[10px]"
                    :class="item.mutation_type === 'D' ? 'text-emerald-700' : 'text-red-600'"
                  >
                    {{ item.mutation_type === 'D' ? 'Debet' : 'Kredit' }}
                  </span>
                  <span v-if="item.valuta !== 'IDR'" class="ml-1 rounded bg-zinc-100 px-1 text-[10px] text-zinc-500">
                    {{ item.valuta }}
                  </span>
                </td>
                <td class="px-3 py-2 text-right font-mono font-semibold">
                  {{ (item.amount ?? 0).toLocaleString('id-ID') }}
                </td>
                <td class="px-3 py-2 max-w-[120px] truncate text-zinc-500">{{ item.description || '—' }}</td>
                <td class="px-3 py-2 text-center">
                  <div class="flex justify-center gap-1">
                    <button
                      class="rounded p-1 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 text-sm"
                      title="Edit"
                      @click="openDrawer(item.item_type as 'G'|'B'|'C'|'D', idx)"
                    >✎</button>
                    <button
                      class="rounded p-1 text-red-400 hover:bg-red-50"
                      title="Hapus"
                      @click="removeItem(idx)"
                    >
                      <Trash2 class="h-3 w-3" />
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
          <div class="flex items-center justify-between border-b px-5 py-4">
            <h2 class="text-base font-semibold text-zinc-800 dark:text-zinc-200">{{ drawerTitle }}</h2>
            <button
              class="rounded-lg p-1.5 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-700 dark:hover:bg-zinc-800"
              @click="closeDrawer"
            >
              <X class="h-5 w-5" />
            </button>
          </div>

          <!-- Drawer body: form (left) + nominal panel (right) -->
          <div class="flex min-h-0 flex-1">

            <!-- LEFT: type-specific form fields -->
            <div class="flex-1 overflow-y-auto p-5 space-y-5">

              <!-- ── GL fields ─────────────────────────────────────────── -->
              <template v-if="drawerType === 'G'">
                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">
                    Rekening Ledger (COA) <span class="text-red-500">*</span>
                  </label>
                  <select
                    :value="glAccountCode"
                    :disabled="coaLoading"
                    class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                    @change="onCoaSelect(($event.target as HTMLSelectElement).value)"
                  >
                    <option value="">{{ coaLoading ? 'Memuat...' : '— Pilih akun —' }}</option>
                    <option v-for="opt in coaSelectOptions" :key="opt.value" :value="opt.value">
                      {{ opt.label }}
                    </option>
                  </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="mb-1 block text-xs font-medium text-zinc-600">Kode Anggaran</label>
                    <input
                      v-model="glKodeAnggaran"
                      placeholder="Opsional"
                      class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                  </div>
                  <div>
                    <label class="mb-1 block text-xs font-medium text-zinc-600">Ket. Anggaran</label>
                    <input
                      v-model="glKetAnggaran"
                      placeholder="Opsional"
                      class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                    />
                  </div>
                </div>
              </template>

              <!-- ── KasBank fields ─────────────────────────────────────── -->
              <template v-else-if="drawerType === 'B'">
                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">
                    Rekening Kas / Bank <span class="text-red-500">*</span>
                  </label>
                  <div class="flex gap-2">
                    <input
                      v-model="kbSearch"
                      placeholder="Cari kode / nama rekening..."
                      class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                      @keyup.enter="searchKasBank"
                    />
                    <Button size="sm" variant="outline" :disabled="kbLoading" @click="searchKasBank">
                      <Search class="h-3.5 w-3.5" />
                      {{ kbLoading ? '...' : 'Cari' }}
                    </Button>
                  </div>
                  <div v-if="kbShowResults && kbResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm dark:bg-zinc-900">
                    <button
                      v-for="r in kbResults" :key="r.account_no"
                      class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50 dark:hover:bg-zinc-800"
                      @click="selectKasBank(r)"
                    >
                      <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
                      <span>{{ r.account_name }}</span>
                    </button>
                  </div>
                  <div v-if="kbShowResults && !kbResults.length" class="mt-1 rounded border bg-zinc-50 px-3 py-2 text-xs text-zinc-400">
                    Tidak ada hasil
                  </div>
                  <div v-if="kbSelectedNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
                    <span class="font-mono text-xs text-zinc-400">{{ kbSelectedNo }}</span>
                    <span class="text-sm font-medium text-zinc-700 dark:text-zinc-300">{{ kbSelectedName }}</span>
                    <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearKasBank">
                      <X class="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>
              </template>

              <!-- ── Penghimpunan fields ─────────────────────────────────── -->
              <template v-else-if="drawerType === 'C'">
                <!-- Donatur -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">Donatur</label>
                  <div class="flex gap-2">
                    <input
                      v-model="phDonorSearch"
                      placeholder="Cari nama donatur..."
                      class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                      @keyup.enter="searchDonor"
                    />
                    <Button size="sm" variant="outline" :disabled="phDonorLoading" @click="searchDonor">
                      <Search class="h-3.5 w-3.5" />
                      {{ phDonorLoading ? '...' : 'Cari' }}
                    </Button>
                  </div>
                  <div v-if="phShowDonorResults && phDonorResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm dark:bg-zinc-900">
                    <button
                      v-for="r in phDonorResults" :key="r.donor_id"
                      class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50 dark:hover:bg-zinc-800"
                      @click="selectDonor(r)"
                    >
                      <span class="font-mono text-xs text-zinc-400">{{ r.donor_no || '—' }}</span>
                      <span>{{ r.donor_name }}</span>
                    </button>
                  </div>
                  <div class="mt-1.5 grid grid-cols-[100px_1fr] gap-2">
                    <div>
                      <label class="mb-0.5 block text-[10px] text-zinc-400">Kode Donatur</label>
                      <input
                        v-model="phDonorNo"
                        placeholder="—"
                        class="w-full rounded border px-3 py-1.5 text-xs focus:outline-none focus:ring-1 focus:ring-primary"
                      />
                    </div>
                    <div>
                      <label class="mb-0.5 block text-[10px] text-zinc-400">Nama Donatur</label>
                      <div class="flex items-center gap-2 rounded-lg bg-violet-50 px-3 py-1.5 dark:bg-violet-900/20">
                        <span class="flex-1 text-sm font-medium text-violet-800 dark:text-violet-300">{{ phDonorName }}</span>
                        <button v-if="phDonorId" class="text-zinc-400 hover:text-red-500" @click="clearDonor">
                          <X class="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Produk Penghimpunan -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">
                    Produk Penghimpunan <span class="text-red-500">*</span>
                  </label>
                  <div class="flex gap-2">
                    <input
                      v-model="phProdukSearch"
                      placeholder="Cari kode / nama produk..."
                      class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                      @keyup.enter="searchProduk"
                    />
                    <Button size="sm" variant="outline" :disabled="phProdukLoading" @click="searchProduk">
                      <Search class="h-3.5 w-3.5" />
                      {{ phProdukLoading ? '...' : 'Cari' }}
                    </Button>
                  </div>
                  <div v-if="phShowProdukResults && phProdukResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm dark:bg-zinc-900">
                    <button
                      v-for="r in phProdukResults" :key="r.account_no"
                      class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50 dark:hover:bg-zinc-800"
                      @click="selectProduk(r)"
                    >
                      <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
                      <span>{{ r.account_name }}</span>
                    </button>
                  </div>
                  <div v-if="phProdukNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
                    <span class="font-mono text-xs text-zinc-400">{{ phProdukNo }}</span>
                    <span class="text-sm font-medium text-zinc-700 dark:text-zinc-300">{{ phProdukName }}</span>
                    <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearProduk">
                      <X class="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>

                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Dana</label>
                  <select v-model="phFundEntity" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                    <option v-for="o in FUND_ENTITY_PENGHIMPUNAN" :key="o.value" :value="o.value">{{ o.label }}</option>
                  </select>
                </div>
              </template>

              <!-- ── Penyaluran fields ──────────────────────────────────── -->
              <template v-else-if="drawerType === 'D'">
                <!-- Program Penyaluran -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">
                    Nama Program <span class="text-red-500">*</span>
                  </label>
                  <div class="flex gap-2">
                    <input
                      v-model="pyProgramSearch"
                      placeholder="Cari kode / nama program..."
                      class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                      @keyup.enter="searchProgram"
                    />
                    <Button size="sm" variant="outline" :disabled="pyProgramLoading" @click="searchProgram">
                      <Search class="h-3.5 w-3.5" />
                      {{ pyProgramLoading ? '...' : 'Cari' }}
                    </Button>
                  </div>
                  <div v-if="pyShowProgramResults && pyProgramResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm dark:bg-zinc-900">
                    <button
                      v-for="r in pyProgramResults" :key="r.account_no"
                      class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50 dark:hover:bg-zinc-800"
                      @click="selectProgram(r)"
                    >
                      <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
                      <span>{{ r.account_name }}</span>
                    </button>
                  </div>
                  <div v-if="pyProgramNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
                    <span class="font-mono text-xs text-zinc-400">{{ pyProgramNo }}</span>
                    <span class="text-sm font-medium text-zinc-700 dark:text-zinc-300">{{ pyProgramName }}</span>
                    <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearProgram">
                      <X class="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>

                <!-- Sumber Dana -->
                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">Sumber Dana</label>
                  <div class="flex gap-2">
                    <input
                      v-model="pySumberSearch"
                      placeholder="Cari rekening sumber dana..."
                      class="flex-1 rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                      @keyup.enter="searchSumber"
                    />
                    <Button size="sm" variant="outline" :disabled="pySumberLoading" @click="searchSumber">
                      <Search class="h-3.5 w-3.5" />
                      {{ pySumberLoading ? '...' : 'Cari' }}
                    </Button>
                  </div>
                  <div v-if="pyShowSumberResults && pySumberResults.length" class="mt-1 max-h-40 overflow-y-auto rounded border bg-white shadow-sm dark:bg-zinc-900">
                    <button
                      v-for="r in pySumberResults" :key="r.account_no"
                      class="flex w-full items-center gap-3 border-b px-3 py-2 text-left text-sm last:border-0 hover:bg-zinc-50 dark:hover:bg-zinc-800"
                      @click="selectSumber(r)"
                    >
                      <span class="font-mono text-xs text-zinc-400">{{ r.account_no }}</span>
                      <span>{{ r.account_name }}</span>
                    </button>
                  </div>
                  <div v-if="pySumberNo" class="mt-1.5 flex items-center gap-3 rounded-lg bg-primary/5 px-3 py-2">
                    <span class="font-mono text-xs text-zinc-400">{{ pySumberNo }}</span>
                    <span class="text-sm font-medium text-zinc-700 dark:text-zinc-300">{{ pySumberName }}</span>
                    <button class="ml-auto text-zinc-400 hover:text-red-500" @click="clearSumber">
                      <X class="h-3.5 w-3.5" />
                    </button>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Dana</label>
                    <select v-model="pyFundEntity" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                      <option v-for="o in FUND_ENTITY_ALL" :key="o.value" :value="o.value">{{ o.label }}</option>
                    </select>
                  </div>
                  <div>
                    <label class="mb-1 block text-xs font-medium text-zinc-600">Ashnaf</label>
                    <select v-model="pyAshnaf" class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
                      <option v-for="o in ASHNAF_OPTIONS" :key="o.value" :value="o.value">{{ o.label }}</option>
                    </select>
                  </div>
                </div>
              </template>

            </div><!-- end left form -->

            <!-- RIGHT: nominal panel -->
            <div class="w-64 flex-shrink-0 overflow-y-auto border-l bg-zinc-50/80 p-4 space-y-4 dark:bg-zinc-800/50 dark:border-zinc-700">
              <h3 class="text-xs font-semibold uppercase tracking-wide text-zinc-500">Nominal Transaksi</h3>

              <div>
                <label class="mb-1 block text-xs font-medium text-zinc-600">Jenis Mutasi</label>
                <select
                  v-model="drawerMutationType"
                  class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option v-for="opt in mutationOptions" :key="opt.value" :value="opt.value">
                    {{ opt.label }}
                  </option>
                </select>
              </div>

              <div>
                <label class="mb-1 block text-xs font-medium text-zinc-600">Valuta</label>
                <select
                  v-model="drawerValuta"
                  class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option v-for="v in VALUTA_OPTIONS" :key="v.value" :value="v.value">{{ v.label }}</option>
                </select>
              </div>

              <div>
                <label class="mb-1 block text-xs font-medium text-zinc-600">
                  Nilai <span v-if="drawerValuta !== 'IDR'" class="text-zinc-400">({{ drawerValuta }})</span>
                  <span class="text-red-500">*</span>
                </label>
                <AmountInput v-model="drawerNilai" />
              </div>

              <template v-if="drawerValuta !== 'IDR'">
                <div>
                  <label class="mb-1 block text-xs font-medium text-zinc-600">Kurs (ke IDR)</label>
                  <input
                    v-model.number="drawerKurs"
                    type="number"
                    min="1"
                    step="1"
                    placeholder="Contoh: 15000"
                    class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                  />
                </div>

                <div class="rounded-lg border border-blue-200 bg-blue-50 p-3 dark:bg-blue-900/20">
                  <div class="text-[10px] text-zinc-500 mb-1">Ekuivalen IDR</div>
                  <div class="font-mono text-base font-bold text-blue-700 dark:text-blue-400">
                    {{ drawerEkuivalen.toLocaleString('id-ID') }}
                  </div>
                  <div class="mt-1 text-[10px] text-zinc-400">
                    {{ (drawerNilai ?? 0).toLocaleString('id-ID') }} × {{ drawerKurs.toLocaleString('id-ID') }}
                  </div>
                </div>
              </template>

              <div>
                <label class="mb-1 block text-xs font-medium text-zinc-600">Keterangan</label>
                <input
                  v-model="drawerDescription"
                  placeholder="Opsional"
                  class="w-full rounded border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>

              <!-- Summary preview -->
              <div v-if="drawerNilai" class="rounded-lg border bg-white p-3 text-xs dark:bg-zinc-900">
                <div class="flex justify-between text-zinc-500">
                  <span>Mutasi</span>
                  <span :class="drawerMutationType === 'D' ? 'font-semibold text-emerald-700' : 'font-semibold text-red-600'">
                    {{ drawerMutationType === 'D' ? 'Debet' : 'Kredit' }}
                  </span>
                </div>
                <div class="mt-1 flex justify-between">
                  <span class="text-zinc-500">IDR</span>
                  <span class="font-mono font-bold text-zinc-800 dark:text-zinc-200">
                    {{ drawerEkuivalen.toLocaleString('id-ID') }}
                  </span>
                </div>
              </div>
            </div><!-- end nominal panel -->

          </div><!-- end drawer body -->

          <!-- Drawer footer -->
          <div class="flex justify-end gap-2 border-t px-5 py-3 dark:border-zinc-700">
            <Button variant="outline" @click="closeDrawer">Batal</Button>
            <Button variant="success" @click="saveDrawerItem">Simpan Detail</Button>
          </div>
        </aside>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ArrowLeft, Plus, Trash2 } from 'lucide-vue-next'
import { computed, ref, shallowRef, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'
import { useAuthStore } from '@/stores/auth'

// ── Types ─────────────────────────────────────────────────────────────────
interface LookupBankAccount {
  account_no: string
  account_name: string
  cash_code: string
  currency_code: string
}

interface LookupPettyCashAccount {
  account_no: string
  account_name: string
  cash_code: string
  currency_code: string
}

interface LookupGlAccount {
  account_code: string
  account_name: string
  parent_account_name: string
}

interface LookupBudget {
  budget_code: string
  budget_owner: string
}

interface FormItem {
  account_code: string
  account_name: string
  amount: number | null
  description: string
  budget_code: string
  budget_owner: string
}

// ── State: Header ──────────────────────────────────────────────────────────
const router = useRouter()
const toast = useToast()
const auth = useAuthStore()
const today = new Date().toISOString().slice(0, 10)

const saving = shallowRef(false)
const formError = shallowRef<string | null>(null)

const formDate = shallowRef(today)
const formPaymentType = shallowRef<'K' | 'C' | 'B'>('K') // Delta: default = Kas, NOT Bank
const formBankAccountNo = shallowRef('')
const formBankAccountName = shallowRef('')
const formCashType = shallowRef<'K' | 'C'>('K') // Kas Kecil or Kas Cabang
const formPettyCashAccountNo = shallowRef('')
const formPettyCashAccountName = shallowRef('')
const formReferenceNo = shallowRef('')
const formPaidTo = shallowRef('')
const formReceivedFrom = shallowRef(auth.user?.username ?? '')
const formDescription = shallowRef('')
const formRate = shallowRef(1.0)

// Delta: Simplified grid items - no cash_account_no, fund_product
const formItems = ref<FormItem[]>([{ account_code: '', account_name: '', amount: null, description: '', budget_code: '', budget_owner: '' }])

// SearchSelect v-model
const bankAccountSelectedValue = shallowRef('')
const pettyCashAccountSelectedValue = shallowRef('')

// ── Lookups ────────────────────────────────────────────────────────────────
const bankAccountResults = ref<LookupBankAccount[]>([])
const bankAccountLoading = shallowRef(false)

const pettyCashAccountResults = ref<LookupPettyCashAccount[]>([])
const pettyCashAccountLoading = shallowRef(false)

const glAccountResults = ref<LookupGlAccount[]>([])
const glAccountLoading = shallowRef(false)
const glAccountSearchInput = shallowRef('')

const budgetResults = ref<LookupBudget[]>([])
const budgetLoading = shallowRef(false)
const budgetSearchInput = shallowRef('')

// ── Computed ───────────────────────────────────────────────────────────────
const bankAccountOptions = computed(() =>
  bankAccountResults.value.map(r => ({ value: r.account_no, label: `${r.account_no}  ${r.account_name}` }))
)

const pettyCashAccountOptions = computed(() =>
  pettyCashAccountResults.value.map(r => ({ value: r.account_no, label: `${r.account_no}  ${r.account_name}` }))
)

const glAccountOptions = computed(() =>
  glAccountResults.value.map(r => ({ value: r.account_code, label: `${r.account_code}  ${r.account_name}` }))
)

const budgetOptions = computed(() =>
  budgetResults.value.map(r => ({ value: r.budget_code, label: `${r.budget_code}  ${r.budget_owner}` }))
)

const totalAmount = computed(() =>
  formItems.value.reduce((sum, item) => sum + (item.amount ?? 0), 0)
)

const paymentTypeLabel = computed(() => {
  const types: Record<string, string> = { C: 'Kas Cabang', K: 'Kas Kecil', B: 'Bank' }
  return types[formPaymentType.value] ?? ''
})

// ── Sync bank account selection ────────────────────────────────────────────
watch(bankAccountSelectedValue, (val) => {
  const found = bankAccountResults.value.find(r => r.account_no === val)
  formBankAccountNo.value = found?.account_no ?? ''
  formBankAccountName.value = found?.account_name ?? ''
})

watch(pettyCashAccountSelectedValue, (val) => {
  const found = pettyCashAccountResults.value.find(r => r.account_no === val)
  formPettyCashAccountNo.value = found?.account_no ?? ''
  formPettyCashAccountName.value = found?.account_name ?? ''
})

// ── Load data ──────────────────────────────────────────────────────────────
async function loadBankAccounts() {
  bankAccountLoading.value = true
  try {
    const res = await api.get<{ rows: LookupBankAccount[] }>(
      `/api/amil-expense/lookup/bank-account?search=`
    )
    bankAccountResults.value = res?.rows ?? []
  } catch (e: unknown) {
    toast.error('Gagal memuat daftar rekening bank')
  } finally {
    bankAccountLoading.value = false
  }
}

async function loadPettyCashAccounts() {
  pettyCashAccountLoading.value = true
  try {
    const res = await api.get<{ rows: LookupPettyCashAccount[] }>(
      `/api/amil-expense/lookup/petty-cash-account?search=`
    )
    pettyCashAccountResults.value = res?.rows ?? []
  } catch (e: unknown) {
    toast.error('Gagal memuat daftar kas kecil')
  } finally {
    pettyCashAccountLoading.value = false
  }
}

async function searchGlAccounts(searchText: string) {
  if (!searchText.trim()) {
    glAccountResults.value = []
    return
  }
  glAccountLoading.value = true
  try {
    const res = await api.get<{ rows: LookupGlAccount[] }>(
      `/api/amil-expense/lookup/gl-account?search=${encodeURIComponent(searchText)}`
    )
    glAccountResults.value = res?.rows ?? []
  } catch (e: unknown) {
    toast.error('Gagal mencari akun beban')
  } finally {
    glAccountLoading.value = false
  }
}

async function searchBudgets(searchText: string) {
  if (!searchText.trim()) {
    budgetResults.value = []
    return
  }
  budgetLoading.value = true
  try {
    const res = await api.get<{ rows: LookupBudget[] }>(
      `/api/amil-expense/lookup/budget?search=${encodeURIComponent(searchText)}`
    )
    budgetResults.value = res?.rows ?? []
  } catch (e: unknown) {
    // Silent fail for budget lookup (optional field)
  } finally {
    budgetLoading.value = false
  }
}

watch(glAccountSearchInput, (val) => {
  searchGlAccounts(val)
})

watch(budgetSearchInput, (val) => {
  searchBudgets(val)
})

// ── Item management ────────────────────────────────────────────────────────
function selectGlAccount(idx: number, code: string) {
  const found = glAccountResults.value.find(r => r.account_code === code)
  if (found) {
    formItems.value[idx].account_code = found.account_code
    formItems.value[idx].account_name = found.account_name
  }
  glAccountSearchInput.value = ''
  glAccountResults.value = []
}

function selectBudget(idx: number, code: string) {
  const found = budgetResults.value.find(r => r.budget_code === code)
  if (found) {
    formItems.value[idx].budget_code = found.budget_code
    formItems.value[idx].budget_owner = found.budget_owner
  }
  budgetSearchInput.value = ''
  budgetResults.value = []
}

function addItem() {
  formItems.value.push({ account_code: '', account_name: '', amount: null, description: '', budget_code: '', budget_owner: '' })
}

function removeItem(idx: number) {
  if (formItems.value.length > 1) {
    formItems.value.splice(idx, 1)
  }
}

// ── Submit ─────────────────────────────────────────────────────────────────
async function submitForm() {
  formError.value = null

  if (!formDate.value) {
    formError.value = 'Tanggal transaksi wajib diisi'
    return
  }

  // Validate payment type specific fields
  if (formPaymentType.value === 'K' && !formPettyCashAccountNo.value) {
    formError.value = 'Kas kecil wajib dipilih'
    return
  }
  if (formPaymentType.value === 'C' && !formPettyCashAccountNo.value) {
    formError.value = 'Kas cabang wajib dipilih'
    return
  }
  if (formPaymentType.value === 'B' && !formBankAccountNo.value) {
    formError.value = 'Rekening bank wajib dipilih'
    return
  }

  if (formItems.value.length === 0) {
    formError.value = 'Minimal 1 detail pengeluaran'
    return
  }

  // Validate items
  for (let i = 0; i < formItems.value.length; i++) {
    const item = formItems.value[i]
    if (!item.account_code) {
      formError.value = `Baris ${i + 1}: Akun beban wajib dipilih`
      return
    }
    if (!item.amount || item.amount <= 0) {
      formError.value = `Baris ${i + 1}: Jumlah harus lebih dari 0`
      return
    }
  }

  saving.value = true
  try {
    const payload = {
      actual_date: formDate.value,
      payment_type: formPaymentType.value,
      bank_account_no: formPaymentType.value === 'B' ? formBankAccountNo.value : null,
      cash_type: formPaymentType.value !== 'B' ? formCashType.value : null,
      petty_cash_account_no: formPaymentType.value !== 'B' ? formPettyCashAccountNo.value : null,
      reference_no: formReferenceNo.value.trim(),
      description: formDescription.value.trim(),
      paid_to: formPaidTo.value.trim(),
      received_from: formReceivedFrom.value.trim(),
      rate: formRate.value,
      items: formItems.value.map(item => ({
        account_code: item.account_code,
        account_name: item.account_name,
        amount: item.amount,
        description: item.description,
        budget_code: item.budget_code || null,
        budget_owner: item.budget_owner || null,
      })),
    }

    const res = await api.post<{ transaction_no: string; status: string }>(
      '/api/amil-expense/save-and-submit',
      payload
    )

    toast.success(`Pengeluaran Amil ${res.transaction_no} berhasil disubmit untuk otorisasi`)
    router.push({ name: 'finance-transactions-amil-expense' })
  } catch (e: unknown) {
    const msg = (e as { message?: string })?.message ?? 'Gagal menyimpan pengeluaran amil'
    formError.value = msg
    toast.error(msg)
  } finally {
    saving.value = false
  }
}

// Load accounts on mount
onMounted(() => {
  loadBankAccounts()
  loadPettyCashAccounts()
})
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Back button -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-transactions-amil-expense' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
    </div>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <!-- Split layout -->
    <div class="flex flex-col gap-3 lg:flex-row lg:items-start">

      <!-- LEFT: Header card -->
      <div class="w-full space-y-3 lg:w-[380px] lg:flex-shrink-0 lg:sticky lg:top-[64px]">

        <!-- Header form card -->
        <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden">
          <!-- Card header bar -->
          <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
            <h2 class="font-bold text-xs tracking-widest text-white uppercase">Header Pengeluaran Amil</h2>
            <span class="bg-slate-600 text-white text-xs px-2 py-0.5 rounded">DRAFT</span>
          </div>
          <!-- Card body -->
          <div class="p-4 space-y-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tanggal Transaksi <span class="text-red-500">*</span></label>
              <DateField v-model="formDate" />
            </div>

            <!-- Payment Type Tabs -->
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Jenis Pembayaran</label>
              <div class="flex gap-1 mb-3">
                <button
                  :class="[
                    'flex-1 px-3 py-1.5 rounded text-xs font-semibold transition-colors',
                    formPaymentType === 'K'
                      ? 'bg-indigo-600 text-white'
                      : 'border border-slate-200 text-slate-600 hover:bg-slate-50'
                  ]"
                  @click="formPaymentType = 'K'; formCashType = 'K'"
                >
                  Kas Kecil
                </button>
                <button
                  :class="[
                    'flex-1 px-3 py-1.5 rounded text-xs font-semibold transition-colors',
                    formPaymentType === 'C'
                      ? 'bg-indigo-600 text-white'
                      : 'border border-slate-200 text-slate-600 hover:bg-slate-50'
                  ]"
                  @click="formPaymentType = 'C'; formCashType = 'C'"
                >
                  Kas Cabang
                </button>
                <button
                  :class="[
                    'flex-1 px-3 py-1.5 rounded text-xs font-semibold transition-colors',
                    formPaymentType === 'B'
                      ? 'bg-indigo-600 text-white'
                      : 'border border-slate-200 text-slate-600 hover:bg-slate-50'
                  ]"
                  @click="formPaymentType = 'B'"
                >
                  Bank
                </button>
              </div>
            </div>

            <!-- Kas (Kecil/Cabang) Section -->
            <template v-if="formPaymentType !== 'B'">
              <div>
                <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                  {{ formPaymentType === 'K' ? 'Kas Kecil' : 'Kas Cabang' }} <span class="text-red-500">*</span>
                </label>
                <div v-if="pettyCashAccountLoading" class="flex items-center gap-2 text-xs text-slate-400 py-1.5">
                  <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-slate-300 border-t-indigo-500 rounded-full"></span>
                  Memuat rekening...
                </div>
                <SearchSelect
                  v-else
                  v-model="pettyCashAccountSelectedValue"
                  :options="pettyCashAccountOptions"
                  placeholder="Pilih kas..."
                />
              </div>

              <div>
                <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Kwitansi</label>
                <input
                  v-model="formReferenceNo"
                  placeholder="Opsional"
                  class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </template>

            <!-- Bank Section -->
            <template v-else>
              <div>
                <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Rekening Bank <span class="text-red-500">*</span></label>
                <div v-if="bankAccountLoading" class="flex items-center gap-2 text-xs text-slate-400 py-1.5">
                  <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-slate-300 border-t-indigo-500 rounded-full"></span>
                  Memuat rekening...
                </div>
                <SearchSelect
                  v-else
                  v-model="bankAccountSelectedValue"
                  :options="bankAccountOptions"
                  placeholder="Pilih rekening bank..."
                />
              </div>

              <div>
                <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Cek / Referensi</label>
                <input
                  v-model="formReferenceNo"
                  placeholder="Opsional"
                  class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div>
                <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Nilai Kurs</label>
                <input
                  v-model.number="formRate"
                  type="number"
                  step="0.0001"
                  placeholder="1.0"
                  class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </template>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Keterangan Umum</label>
              <textarea
                v-model="formDescription"
                placeholder="Opsional"
                rows="2"
                class="w-full border border-slate-200 rounded px-3 py-1.5 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-y min-h-[56px]"
              />
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Dibayarkan Kepada</label>
              <input
                v-model="formPaidTo"
                placeholder="Opsional"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Diterima Dari</label>
              <input
                v-model="formReceivedFrom"
                placeholder="Default: Username Anda"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>
        </div>

        <!-- Summary card -->
        <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden">
          <!-- Card header bar -->
          <div class="flex items-center justify-between bg-slate-700 px-4 py-2">
            <h2 class="font-bold text-xs tracking-widest text-white uppercase">Ringkasan</h2>
          </div>
          <!-- Card body -->
          <div class="p-4 space-y-3">
            <div class="rounded-lg border border-slate-200 bg-slate-50 p-3 dark:bg-zinc-800">
              <div class="text-xs text-slate-500">Total Pengeluaran</div>
              <div class="mt-0.5 font-mono text-sm font-bold text-emerald-700">
                {{ totalAmount.toLocaleString('id-ID') }}
              </div>
            </div>

            <div class="flex gap-2">
              <button
                class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
                @click="router.push({ name: 'finance-transactions-amil-expense' })"
              >
                Batal
              </button>
              <button
                class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="saving || formItems.length === 0"
                @click="submitForm"
              >
                {{ saving ? 'Menyimpan...' : 'Simpan & Kirim Persetujuan' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Detail items table -->
      <div class="min-w-0 flex-1 space-y-0 rounded-lg border border-slate-200 overflow-hidden">
        <!-- Detail header bar -->
        <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
          <h2 class="font-bold text-xs tracking-widest text-white uppercase">Detail Pengeluaran</h2>
          <span class="bg-slate-600 text-white text-xs px-2 py-0.5 rounded">
            {{ formItems.length }} item
          </span>
        </div>

        <!-- Toolbar: add button -->
        <div class="border-b border-slate-200 bg-slate-50 px-3 py-2 dark:bg-zinc-800/50">
          <Button size="sm" variant="outline" @click="addItem">
            <Plus class="h-3.5 w-3.5" />
            Tambah Baris
          </Button>
        </div>

        <!-- Items table -->
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead class="border-b border-slate-200 bg-slate-50 text-xs font-semibold uppercase tracking-wide text-slate-500 dark:bg-zinc-800/50 dark:text-zinc-400">
              <tr>
                <th class="px-3 py-1.5 text-left">Akun Beban (31xxxx)</th>
                <th class="px-3 py-1.5 text-left">Deskripsi</th>
                <th class="px-3 py-1.5 text-left">Budget</th>
                <th class="px-3 py-1.5 text-right w-36">Jumlah</th>
                <th class="px-3 py-1.5 w-16"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="formItems.length === 0">
                <td colspan="5" class="px-3 py-6 text-center text-xs text-slate-400">
                  Belum ada item — klik tombol tambah di atas
                </td>
              </tr>
              <tr v-for="(item, idx) in formItems" :key="idx" class="border-t border-slate-100 hover:bg-indigo-50/40 even:bg-slate-50/50">
                <td class="px-3 py-1.5">
                  <div class="flex flex-col gap-1">
                    <input
                      :value="glAccountSearchInput"
                      placeholder="Cari akun..."
                      class="w-full rounded border border-slate-200 px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      @input="(e) => { glAccountSearchInput = (e.target as HTMLInputElement).value }"
                      @focus="searchGlAccounts(glAccountSearchInput)"
                    />
                    <div v-if="glAccountResults.length > 0" class="absolute z-10 w-80 rounded border border-slate-200 bg-white shadow-lg max-h-48 overflow-y-auto">
                      <div
                        v-for="result in glAccountResults"
                        :key="result.account_code"
                        class="px-2 py-1.5 hover:bg-indigo-50 cursor-pointer text-xs"
                        @click="selectGlAccount(idx, result.account_code)"
                      >
                        <div class="font-mono font-semibold">{{ result.account_code }}</div>
                        <div class="text-slate-500">{{ result.account_name }}</div>
                      </div>
                    </div>
                    <div v-if="item.account_code" class="text-xs text-emerald-600">✓ {{ item.account_code }}</div>
                  </div>
                </td>
                <td class="px-3 py-1.5">
                  <input
                    v-model="item.description"
                    placeholder="Deskripsi item"
                    class="w-full rounded border border-slate-200 px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </td>
                <td class="px-3 py-1.5">
                  <div class="flex flex-col gap-1">
                    <input
                      :value="budgetSearchInput"
                      placeholder="Cari budget..."
                      class="w-full rounded border border-slate-200 px-2 py-1 text-xs focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      @input="(e) => { budgetSearchInput = (e.target as HTMLInputElement).value }"
                      @focus="searchBudgets(budgetSearchInput)"
                    />
                    <div v-if="budgetResults.length > 0" class="absolute z-10 w-80 rounded border border-slate-200 bg-white shadow-lg max-h-48 overflow-y-auto">
                      <div
                        v-for="result in budgetResults"
                        :key="result.budget_code"
                        class="px-2 py-1.5 hover:bg-indigo-50 cursor-pointer text-xs"
                        @click="selectBudget(idx, result.budget_code)"
                      >
                        <div class="font-mono font-semibold">{{ result.budget_code }}</div>
                        <div class="text-slate-500">{{ result.budget_owner }}</div>
                      </div>
                    </div>
                    <div v-if="item.budget_code" class="text-xs text-emerald-600">✓ {{ item.budget_code }}</div>
                  </div>
                </td>
                <td class="px-3 py-1.5 text-right">
                  <AmountInput
                    v-model="item.amount"
                    placeholder="0"
                    class="text-right"
                  />
                </td>
                <td class="px-3 py-1.5 text-center">
                  <button
                    v-if="formItems.length > 1"
                    class="rounded p-1 text-red-500 hover:bg-red-50"
                    title="Hapus baris"
                    @click="removeItem(idx)"
                  >
                    <Trash2 class="h-3.5 w-3.5" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

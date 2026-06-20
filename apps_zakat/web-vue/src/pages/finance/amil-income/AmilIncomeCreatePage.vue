<script setup lang="ts">
import { ArrowLeft, Plus, Trash2, X } from 'lucide-vue-next'
import { computed, ref, shallowRef, watch } from 'vue'
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
interface LookupKasAccount {
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

interface FormItem {
  account_code: string
  account_name: string
  amount: number | null
  description: string
  cash_account_no: string
  fund_account_no: string
}

// ── State: Header ──────────────────────────────────────────────────────────
const router = useRouter()
const toast = useToast()
const auth = useAuthStore()
const today = new Date().toISOString().slice(0, 10)

const saving = shallowRef(false)
const formError = shallowRef<string | null>(null)

const formDate = shallowRef(today)
const formPaymentType = shallowRef<'C' | 'K' | 'B'>('B')
const formBankAccountNo = shallowRef('')
const formBankAccountName = shallowRef('')
const formReferenceNo = shallowRef('')
const formPaidTo = shallowRef(auth.user?.username ?? '')
const formReceivedFrom = shallowRef('')
const formDescription = shallowRef('')
const formItems = ref<FormItem[]>([{ account_code: '', account_name: '', amount: null, description: '', cash_account_no: '', fund_account_no: '' }])

// SearchSelect v-model
const bankAccountSelectedValue = shallowRef('')

// ── Lookups ────────────────────────────────────────────────────────────────
const kasAccountResults = ref<LookupKasAccount[]>([])
const kasAccountLoading = shallowRef(false)

const glAccountResults = ref<LookupGlAccount[]>([])
const glAccountLoading = shallowRef(false)
const glAccountSearchInput = shallowRef('')

// ── Computed ───────────────────────────────────────────────────────────────
const kasAccountOptions = computed(() =>
  kasAccountResults.value.map(r => ({ value: r.account_no, label: `${r.account_no}  ${r.account_name}` }))
)

const glAccountOptions = computed(() =>
  glAccountResults.value.map(r => ({ value: r.account_code, label: `${r.account_code}  ${r.account_name}` }))
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
  const found = kasAccountResults.value.find(r => r.account_no === val)
  formBankAccountNo.value = found?.account_no ?? ''
  formBankAccountName.value = found?.account_name ?? ''
})

// ── Load data ──────────────────────────────────────────────────────────────
async function loadKasAccounts() {
  kasAccountLoading.value = true
  try {
    const res = await api.get<{ rows: LookupKasAccount[] }>(
      `/api/amil-income/lookup/kas-account?search=`
    )
    kasAccountResults.value = res?.rows ?? []
  } catch (e: unknown) {
    toast.error('Gagal memuat daftar rekening kas')
  } finally {
    kasAccountLoading.value = false
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
      `/api/amil-income/lookup/gl-account?search=${encodeURIComponent(searchText)}`
    )
    glAccountResults.value = res?.rows ?? []
  } catch (e: unknown) {
    toast.error('Gagal mencari akun pendapatan')
  } finally {
    glAccountLoading.value = false
  }
}

watch(glAccountSearchInput, (val) => {
  searchGlAccounts(val)
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

function addItem() {
  formItems.value.push({ account_code: '', account_name: '', amount: null, description: '', cash_account_no: '', fund_account_no: '' })
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
  if (!formBankAccountNo.value) {
    formError.value = 'Rekening tujuan wajib dipilih'
    return
  }
  if (formItems.value.length === 0) {
    formError.value = 'Minimal 1 detail penerimaan'
    return
  }

  // Validate items
  for (let i = 0; i < formItems.value.length; i++) {
    const item = formItems.value[i]
    if (!item.account_code) {
      formError.value = `Baris ${i + 1}: Akun pendapatan wajib dipilih`
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
      bank_account_no: formBankAccountNo.value,
      reference_no: formReferenceNo.value.trim(),
      paid_to: formPaidTo.value.trim(),
      received_from: formReceivedFrom.value.trim(),
      description: formDescription.value.trim(),
      rate: 1.0,
      items: formItems.value.map(item => ({
        account_code: item.account_code,
        account_name: item.account_name,
        amount: item.amount,
        description: item.description,
        cash_account_no: item.cash_account_no,
        fund_account_no: item.fund_account_no,
      })),
    }

    const res = await api.post<{ transaction_no: string; status: string }>(
      '/api/amil-income/save-and-submit',
      payload
    )

    toast.success(`Penerimaan Amil ${res.transaction_no} berhasil disubmit untuk otorisasi`)
    router.push({ name: 'finance-transactions-amil-income' })
  } catch (e: unknown) {
    const msg = (e as { message?: string })?.message ?? 'Gagal menyimpan penerimaan amil'
    formError.value = msg
    toast.error(msg)
  } finally {
    saving.value = false
  }
}

// Load kas accounts on mount
import { onMounted } from 'vue'
onMounted(() => {
  loadKasAccounts()
})
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Back button -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-transactions-amil-income' })"
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
            <h2 class="font-bold text-xs tracking-widest text-white uppercase">Header Penerimaan Amil</h2>
            <span class="bg-slate-600 text-white text-xs px-2 py-0.5 rounded">DRAFT</span>
          </div>
          <!-- Card body -->
          <div class="p-4 space-y-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tanggal Transaksi <span class="text-red-500">*</span></label>
              <DateField v-model="formDate" />
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Jenis Pembayaran</label>
              <select
                v-model="formPaymentType"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="B">Bank</option>
                <option value="C">Kas Cabang</option>
                <option value="K">Kas Kecil</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Rekening Tujuan <span class="text-red-500">*</span></label>
              <div v-if="kasAccountLoading" class="flex items-center gap-2 text-xs text-slate-400 py-1.5">
                <span class="animate-spin inline-block w-3.5 h-3.5 border-2 border-slate-300 border-t-indigo-500 rounded-full"></span>
                Memuat rekening...
              </div>
              <SearchSelect
                v-else
                v-model="bankAccountSelectedValue"
                :options="kasAccountOptions"
                placeholder="Pilih rekening tujuan..."
              />
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Referensi</label>
              <input
                v-model="formReferenceNo"
                placeholder="Opsional"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Penerima</label>
              <input
                v-model="formPaidTo"
                placeholder="Default: Username Anda"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Dari Pihak</label>
              <input
                v-model="formReceivedFrom"
                placeholder="Opsional"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Keterangan</label>
              <textarea
                v-model="formDescription"
                placeholder="Opsional"
                rows="2"
                class="w-full border border-slate-200 rounded px-3 py-1.5 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-y min-h-[56px]"
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
              <div class="text-xs text-slate-500">Total Penerimaan</div>
              <div class="mt-0.5 font-mono text-sm font-bold text-emerald-700">
                {{ totalAmount.toLocaleString('id-ID') }}
              </div>
            </div>

            <div class="flex gap-2">
              <button
                class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
                @click="router.push({ name: 'finance-transactions-amil-income' })"
              >
                Batal
              </button>
              <button
                class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="saving || formItems.length === 0"
                @click="submitForm"
              >
                {{ saving ? 'Menyimpan...' : 'Simpan & Submit' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- RIGHT: Detail items table -->
      <div class="min-w-0 flex-1 space-y-0 rounded-lg border border-slate-200 overflow-hidden">
        <!-- Detail header bar -->
        <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
          <h2 class="font-bold text-xs tracking-widest text-white uppercase">Detail Penerimaan</h2>
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
                <th class="px-3 py-1.5 text-left">Akun Pendapatan (430xxx)</th>
                <th class="px-3 py-1.5 text-left">Deskripsi</th>
                <th class="px-3 py-1.5 text-right w-36">Jumlah</th>
                <th class="px-3 py-1.5 w-16"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="formItems.length === 0">
                <td colspan="4" class="px-3 py-6 text-center text-xs text-slate-400">
                  Belum ada item — klik tombol tambah di atas
                </td>
              </tr>
              <tr v-for="(item, idx) in formItems" :key="idx" class="border-t border-slate-100 hover:bg-indigo-50/40 even:bg-slate-50/50">
                <td class="px-3 py-1.5">
                  <div class="flex flex-col gap-1">
                    <input
                      :value="item.account_code"
                      placeholder="Cari akun..."
                      class="w-full rounded border border-slate-200 px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                      @focus="glAccountSearchInput = item.account_code"
                      @input="glAccountSearchInput = ($event.target as HTMLInputElement).value"
                    />
                    <div v-if="glAccountSearchInput && glAccountResults.length" class="absolute z-10 mt-1 max-h-32 overflow-y-auto rounded border border-slate-200 bg-white shadow-sm dark:bg-zinc-900 w-64">
                      <button
                        v-for="result in glAccountResults"
                        :key="result.account_code"
                        class="block w-full px-2 py-1 text-left text-xs hover:bg-indigo-50 dark:hover:bg-zinc-800 border-b border-slate-100 last:border-0"
                        @click="selectGlAccount(idx, result.account_code)"
                      >
                        <span class="font-mono text-slate-500">{{ result.account_code }}</span>
                        <span class="text-slate-700">{{ result.account_name }}</span>
                      </button>
                    </div>
                  </div>
                </td>
                <td class="px-3 py-1.5">
                  <input
                    v-model="item.description"
                    placeholder="Opsional"
                    class="w-full rounded border border-slate-200 px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </td>
                <td class="px-3 py-1.5">
                  <AmountInput v-model="item.amount" />
                </td>
                <td class="px-3 py-1.5 text-center">
                  <button
                    v-if="formItems.length > 1"
                    class="rounded p-1.5 text-red-500 hover:bg-red-50 hover:text-red-700"
                    title="Hapus baris"
                    @click="removeItem(idx)"
                  >
                    <Trash2 class="h-4 w-4" />
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

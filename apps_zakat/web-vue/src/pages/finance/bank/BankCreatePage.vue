<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { reactive, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

interface SelectOption { value: string; label: string }

const router = useRouter()
const toast = useToast()

// ── Lookups ───────────────────────────────────────────────────────────────────
const lookupBanks = ref<SelectOption[]>([])
const lookupBranches = ref<SelectOption[]>([])
const lookupCurrencies = ref<SelectOption[]>([])
const lookupGlAccounts = ref<SelectOption[]>([])
const lookupProducts = ref<SelectOption[]>([])
const lookupLoaded = shallowRef(false)
const lookupLoading = shallowRef(false)

async function loadLookups() {
  if (lookupLoaded.value) return
  lookupLoading.value = true
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
  } finally {
    lookupLoading.value = false
  }
}

// ── Form state ────────────────────────────────────────────────────────────────
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

const submitting = shallowRef(false)
const formError = shallowRef<string | null>(null)

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

async function submit() {
  formError.value = null
  const err = validateForm()
  if (err) { formError.value = err; toast.error(err); return }

  submitting.value = true
  try {
    const payload = {
      action: 'create',
      account_name: form.account_name.trim(),
      bank_account_no: form.bank_account_no.trim(),
      bank_code: form.bank_code,
      bank_name: lookupBanks.value.find((b) => b.value === form.bank_code)?.label ?? form.bank_code,
      branch_code: form.branch_code,
      branch_name: lookupBranches.value.find((b) => b.value === form.branch_code)?.label ?? form.branch_code,
      currency_code: form.currency_code,
      account_interface: form.account_interface,
      opening_date: form.opening_date || null,
      is_amil_account: form.is_amil_account,
      product_id: form.is_amil_account || !form.product_id ? null : Number(form.product_id),
      cash_code: form.cash_code.trim() || null,
    }
    await api.post('/api/authorization/save-and-submit/', {
      entity_type: 'bank',
      module: 'keuangan',
      payload,
    })
    toast.success('Permintaan tambah rekening dikirim untuk otorisasi')
    void router.push({ name: 'finance-bank' })
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Gagal mengirim submission'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}

// Load lookups on mount
loadLookups()
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Tombol kembali (judul halaman ada di breadcrumb header) -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-bank' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
    </div>
    <p class="text-xs text-slate-400">Permintaan akan diproses melalui otorisasi supervisor</p>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-2xl">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Tambah Rekening Bank</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <!-- Loading skeleton -->
        <div v-if="lookupLoading" class="space-y-4">
          <div v-for="i in 5" :key="i" class="space-y-1.5">
            <div class="h-3 w-24 rounded bg-slate-200/60 animate-pulse" />
            <div class="h-9 w-full rounded bg-slate-100 animate-pulse" />
          </div>
        </div>

        <template v-else>
          <!-- Nama Rekening + No Rekening Bank -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Nama Rekening <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.account_name"
                placeholder="mis. ZAKAT FITRAH"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                No Rekening Bank <span class="text-red-500">*</span>
              </label>
              <input
                v-model="form.bank_account_no"
                placeholder="min. 8 karakter"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <!-- Nama Bank + Cabang BPZIS -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Nama Bank <span class="text-red-500">*</span>
              </label>
              <SearchSelect v-model="form.bank_code" :options="lookupBanks" placeholder="Pilih bank..." />
            </div>
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Cabang BPZIS <span class="text-red-500">*</span>
              </label>
              <SearchSelect v-model="form.branch_code" :options="lookupBranches" placeholder="Pilih cabang..." />
            </div>
          </div>

          <!-- Valuta + GL Interface -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Valuta <span class="text-red-500">*</span>
              </label>
              <SearchSelect v-model="form.currency_code" :options="lookupCurrencies" placeholder="Pilih valuta..." />
            </div>
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                GL Interface <span class="text-red-500">*</span>
              </label>
              <SearchSelect v-model="form.account_interface" :options="lookupGlAccounts" placeholder="Cari akun GL..." />
            </div>
          </div>

          <!-- Tgl Buka + Rekening Amil -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 items-end">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tgl Buka</label>
              <DateField v-model="form.opening_date" />
            </div>
            <div class="flex items-center gap-2 pb-1.5">
              <input id="is-amil" v-model="form.is_amil_account" type="checkbox" class="rounded" />
              <label for="is-amil" class="text-sm cursor-pointer select-none text-slate-600">Rekening Amil?</label>
            </div>
          </div>

          <!-- Default Produk + Kode Kas -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label
                class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide"
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
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Kode Kas <span class="text-slate-400 normal-case">(opsional)</span>
              </label>
              <input
                v-model="form.cash_code"
                placeholder="Kode kas unik (opsional)"
                class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          <p class="text-[10px] text-slate-400">Rekening aktif setelah disetujui supervisor melalui sistem otorisasi.</p>

          <div class="flex gap-2 pt-1">
            <button
              class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="submitting"
              @click="router.push({ name: 'finance-bank' })"
            >
              Batal
            </button>
            <button
              class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="submitting"
              @click="submit"
            >
              {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

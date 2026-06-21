<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { reactive, ref, shallowRef } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import DateField from '@/shared/components/DateField.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

interface SelectOption { value: string; label: string }

const router = useRouter()
const toast = useToast()

// ── Lookups ───────────────────────────────────────────────────────────────────
const lookupBranches = ref<SelectOption[]>([])
const lookupCurrencies = ref<SelectOption[]>([])
const lookupGlAccounts = ref<SelectOption[]>([])
const lookupLoaded = shallowRef(false)
const lookupLoading = shallowRef(false)

async function loadLookups() {
  if (lookupLoaded.value) return
  lookupLoading.value = true
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
  } finally {
    lookupLoading.value = false
  }
}

// ── Form state ────────────────────────────────────────────────────────────────
const form = reactive({
  account_name: '',
  branch_code: '',
  currency_code: '',
  account_interface: '',
  cash_code: '',
  opening_date: '',
})

const submitting = shallowRef(false)
const formError = shallowRef<string | null>(null)

function validateForm(): string | null {
  if (!form.account_name.trim()) return 'Nama Rekening wajib diisi'
  if (!form.branch_code) return 'Cabang wajib dipilih'
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
    await api.post<{ account_no: string }>('/api/petty-cash/accounts', {
      account_name: form.account_name.trim(),
      account_interface: form.account_interface,
      currency_code: form.currency_code,
      branch_code: form.branch_code,
      cash_code: form.cash_code.trim() || null,
      opening_date: form.opening_date || null,
    })
    toast.success('Rekening kas kecil berhasil ditambahkan')
    void router.push({ name: 'finance-petty-cash' })
  } catch (e: unknown) {
    const msg = e instanceof ApiError ? e.message : 'Gagal menyimpan data'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}

loadLookups()
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Tombol kembali (judul halaman ada di breadcrumb header) -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-petty-cash' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
    </div>
    <p class="text-xs text-slate-400">Lengkapi data rekening petty cash baru</p>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-xl">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Tambah Rekening Kas Kecil</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <!-- Loading skeleton -->
        <div v-if="lookupLoading" class="space-y-4">
          <div v-for="i in 4" :key="i" class="space-y-1.5">
            <div class="h-3 w-24 rounded bg-slate-200/60 animate-pulse" />
            <div class="h-9 w-full rounded bg-slate-100 animate-pulse" />
          </div>
        </div>

        <template v-else>
          <!-- No. Rekening (auto) -->
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">No. Rekening</label>
            <input
              value="<AUTOGENERATED>"
              disabled
              class="w-full rounded border border-slate-200 bg-slate-50 px-3 py-1.5 text-sm font-mono text-slate-400 cursor-not-allowed"
            />
          </div>

          <!-- Nama Rekening -->
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Nama Rekening <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.account_name"
              placeholder="mis. Petty Cash Operasional"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          <!-- Cabang + Valuta -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Cabang <span class="text-red-500">*</span>
              </label>
              <SearchSelect v-model="form.branch_code" :options="lookupBranches" placeholder="Pilih cabang..." />
            </div>
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                Valuta <span class="text-red-500">*</span>
              </label>
              <SearchSelect v-model="form.currency_code" :options="lookupCurrencies" placeholder="Pilih valuta..." />
            </div>
          </div>

          <!-- GL Interface + Kode Kas -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
                GL Interface <span class="text-red-500">*</span>
              </label>
              <SearchSelect v-model="form.account_interface" :options="lookupGlAccounts" placeholder="Cari akun GL..." />
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

          <!-- Tgl Buka -->
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tgl Buka</label>
            <DateField v-model="form.opening_date" />
          </div>

          <div class="flex gap-2 pt-1">
            <button
              class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="submitting"
              @click="router.push({ name: 'finance-petty-cash' })"
            >
              Batal
            </button>
            <button
              class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="submitting"
              @click="submit"
            >
              {{ submitting ? 'Menyimpan...' : 'Tambah Rekening' }}
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

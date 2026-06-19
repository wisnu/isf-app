<script setup lang="ts">
import { useRouter } from 'vue-router'
import { reactive, ref, shallowRef } from 'vue'

import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

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
    await api.post('/api/otorisasi/save-and-submit/', {
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
  <div class="space-y-4">
    <PageHeader title="Tambah Rekening Bank" subtitle="Permintaan akan diproses melalui otorisasi supervisor" />

    <div class="rounded-xl border border-border bg-surface p-6 space-y-4 max-w-2xl">
      <!-- Loading skeleton -->
      <div v-if="lookupLoading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="space-y-1.5">
          <div class="h-3 w-24 rounded bg-muted/20 animate-pulse" />
          <div class="h-9 w-full rounded-lg bg-muted/10 animate-pulse" />
        </div>
      </div>

      <template v-else>
        <div
          v-if="formError"
          class="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700 dark:bg-red-900/10 dark:border-red-800 dark:text-red-400"
        >
          {{ formError }}
        </div>

        <!-- Nama Rekening + No Rekening Bank -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium">Nama Rekening <span class="text-red-500">*</span></label>
            <input
              v-model="form.account_name"
              placeholder="mis. ZAKAT FITRAH"
              class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">No Rekening Bank <span class="text-red-500">*</span></label>
            <input
              v-model="form.bank_account_no"
              placeholder="min. 8 karakter"
              class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
        </div>

        <!-- Nama Bank + Cabang BPZIS -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium">Nama Bank <span class="text-red-500">*</span></label>
            <SearchSelect v-model="form.bank_code" :options="lookupBanks" placeholder="Pilih bank..." />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">Cabang BPZIS <span class="text-red-500">*</span></label>
            <SearchSelect v-model="form.branch_code" :options="lookupBranches" placeholder="Pilih cabang..." />
          </div>
        </div>

        <!-- Valuta + GL Interface -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium">Valuta <span class="text-red-500">*</span></label>
            <SearchSelect v-model="form.currency_code" :options="lookupCurrencies" placeholder="Pilih valuta..." />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">GL Interface <span class="text-red-500">*</span></label>
            <SearchSelect v-model="form.account_interface" :options="lookupGlAccounts" placeholder="Cari akun GL..." />
          </div>
        </div>

        <!-- Tgl Buka + Rekening Amil -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 items-end">
          <div>
            <label class="mb-1 block text-xs font-medium">Tgl Buka</label>
            <DateField v-model="form.opening_date" />
          </div>
          <div class="flex items-center gap-2 pb-1">
            <input id="is-amil" v-model="form.is_amil_account" type="checkbox" class="rounded" />
            <label for="is-amil" class="text-sm cursor-pointer select-none">Rekening Amil?</label>
          </div>
        </div>

        <!-- Default Produk + Kode Kas -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium" :class="{ 'opacity-40': form.is_amil_account }">
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
            <label class="mb-1 block text-xs font-medium text-muted">Kode Kas <span class="text-muted">(opsional)</span></label>
            <input
              v-model="form.cash_code"
              placeholder="Kode kas unik (opsional)"
              class="h-9 w-full rounded-lg border border-border bg-surface px-2.5 text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
        </div>

        <p class="text-[10px] text-muted">Rekening aktif setelah disetujui supervisor melalui sistem otorisasi.</p>

        <div class="flex justify-end gap-2 pt-2">
          <Button variant="outline" size="sm" :disabled="submitting" @click="router.push({ name: 'finance-bank' })">
            Batal
          </Button>
          <Button size="sm" :disabled="submitting" @click="submit">
            {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
          </Button>
        </div>
      </template>
    </div>
  </div>
</template>

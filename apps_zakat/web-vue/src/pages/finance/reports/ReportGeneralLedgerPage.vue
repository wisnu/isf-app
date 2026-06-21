<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import AppDataTable from '@/components/ui/AppDataTable.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useAuthStore } from '@/stores/auth'
import Column from 'primevue/column'

interface GLRow {
  journal_date: string
  transactionno: string | null
  description: string
  subaccount: string
  debit: number
  credit: number
  lawan: string
}
interface GLAccount {
  account_code: string
  account_name: string | null
  account_type: string
  opening_balance: number
  total_debit: number
  total_credit: number
  net: number
  closing_balance: number
  rows: GLRow[]
}
interface GLPayload { accounts: GLAccount[]; begin: string; end: string; consolidated: boolean; capped: boolean }
interface BranchOption { code: string; name: string }
interface AccountOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef<string>(`${today.getFullYear()}-01-01`)
const end = shallowRef<string>(iso(today))
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const account = shallowRef<string>('')
const branches = ref<BranchOption[]>([])
const accounts = ref<AccountOption[]>([])

const data = ref<GLPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))
const accountOptions = computed(() => accounts.value.map((a) => ({ value: a.code, label: `${a.code} — ${a.name}` })))

const qs = () => {
  let s = `begin=${begin.value}&end=${end.value}`
  if (branch.value) s += `&branch=${encodeURIComponent(branch.value)}`
  if (account.value) s += `&account=${encodeURIComponent(account.value)}`
  return s
}

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/report/general-ledger/branches')
    if (!branch.value && branches.value.length && !canPickBranch.value)
      branch.value = branches.value[0].code
  } catch {
    branches.value = []
  }
}

async function loadAccounts() {
  try {
    const url = branch.value
      ? `/api/report/general-ledger/accounts?branch=${encodeURIComponent(branch.value)}`
      : '/api/report/general-ledger/accounts'
    accounts.value = await api.get<AccountOption[]>(url)
  } catch {
    accounts.value = []
  }
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<GLPayload>(`/api/report/general-ledger?${qs()}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat laporan'
    data.value = null
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  exporting.value = true
  errorMsg.value = null
  try {
    const now = new Date()
    const ts = `${now.getFullYear()}${p(now.getMonth() + 1)}${p(now.getDate())}-${p(now.getHours())}${p(now.getMinutes())}${p(now.getSeconds())}`
    await api.downloadBlob(`/api/report/general-ledger/export.xlsx?${qs()}`, `bukubesar-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

watch([begin, end, account], () => { data.value = null })
watch(branch, () => { data.value = null; account.value = ''; loadAccounts() })

// Standar laporan: data di-load saat klik "Tampilkan", bukan saat buka halaman.
onMounted(async () => {
  await loadBranches()
  await loadAccounts()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Buku Besar</h1>
      <p class="text-sm text-muted">Mutasi per akun: saldo awal, transaksi, saldo akhir. Pilih akun (opsional) untuk fokus.</p>
    </div>

    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[14rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-if="canPickBranch" value="">Konsolidasi (Semua Cabang)</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Akun</label>
        <div class="min-w-[20rem]">
          <SearchSelect v-model="account" :options="accountOptions" all-label="Semua akun" placeholder="Cari no. / nama akun…" />
        </div>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Awal</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Akhir</label>
        <DateField v-model="end" />
      </div>
      <Button size="sm" class="gap-1.5 h-9" :disabled="loading" @click="load">
        <Search class="w-4 h-4" :class="{ 'animate-pulse': loading }" /> Tampilkan
      </Button>
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data || !data.accounts.length" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>
    <Alert v-if="data && data.capped" variant="default" class="text-xs">Hasil dibatasi 50.000 baris — persempit filter (pilih akun/cabang/periode).</Alert>

    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>

    <div v-else class="space-y-5">
      <div v-for="acc in data?.accounts ?? []" :key="acc.account_code" class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="flex flex-wrap items-center gap-x-6 gap-y-1 px-4 py-2 bg-background/40 border-b border-border">
          <span class="font-semibold text-sm">{{ acc.account_code }} — {{ acc.account_name }}</span>
          <span class="text-xs text-muted">Saldo Awal: <span class="tabular-nums text-foreground">{{ fmt(acc.opening_balance) }}</span></span>
          <span class="text-xs text-muted ml-auto">Saldo Akhir: <span class="tabular-nums font-medium text-foreground">{{ fmt(acc.closing_balance) }}</span></span>
        </div>
        <AppDataTable :value="acc.rows" :loading="loading && !data">
          <Column header="Tanggal">
            <template #body="{ data: r }">
              <span class="whitespace-nowrap tabular-nums">{{ dmy(r.journal_date) }}</span>
            </template>
          </Column>
          <Column header="No. Transaksi">
            <template #body="{ data: r }">
              <span class="font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</span>
            </template>
          </Column>
          <Column header="Keterangan" :pt="{ headerCell: { class: 'text-left px-3 py-1 font-semibold min-w-[16rem]' } }">
            <template #body="{ data: r }">
              <span class="whitespace-pre-line">{{ r.description }}</span>
            </template>
          </Column>
          <Column header="Sub / Lawan">
            <template #body="{ data: r }">
              <span class="text-muted">{{ r.subaccount }}<span v-if="r.lawan"> · {{ r.lawan }}</span></span>
            </template>
          </Column>
          <Column header="Debet" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }">
              <span class="block text-right tabular-nums">{{ fmt(r.debit) }}</span>
            </template>
          </Column>
          <Column header="Kredit" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold whitespace-nowrap' } }">
            <template #body="{ data: r }">
              <span class="block text-right tabular-nums">{{ fmt(r.credit) }}</span>
            </template>
          </Column>
          <template #empty>Tidak ada transaksi untuk filter ini.</template>
        </AppDataTable>
        <div class="border-t-2 border-border bg-background/30 font-semibold text-[11px] flex">
          <span class="px-3 py-1 flex-1">Total Mutasi (Bersih: {{ fmt(acc.net) }})</span>
          <span class="px-3 py-1 tabular-nums whitespace-nowrap text-right min-w-[8rem]">{{ fmt(acc.total_debit) }}</span>
          <span class="px-3 py-1 tabular-nums whitespace-nowrap text-right min-w-[8rem]">{{ fmt(acc.total_credit) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

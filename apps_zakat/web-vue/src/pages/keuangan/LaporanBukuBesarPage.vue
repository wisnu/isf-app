<script setup lang="ts">
import { Download, Loader2, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

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
  saldo_awal: number
  total_debit: number
  total_credit: number
  net: number
  saldo_akhir: number
  rows: GLRow[]
}
interface GLPayload { accounts: GLAccount[]; begin: string; end: string; konsolidasi: boolean; capped: boolean }
interface BranchOption { code: string; name: string }
interface AccountOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = ref<string>(`${today.getFullYear()}-01-01`)
const end = ref<string>(iso(today))
const branch = ref<string>(auth.user?.primary_branch ?? '')
const account = ref<string>('')
const branches = ref<BranchOption[]>([])
const accounts = ref<AccountOption[]>([])

const data = ref<GLPayload | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

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
        <select v-model="account" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[16rem] focus:outline-none focus:ring-1 focus:ring-primary">
          <option value="">Semua akun</option>
          <option v-for="a in accounts" :key="a.code" :value="a.code">{{ a.code }} — {{ a.name }}</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Awal</label>
        <input v-model="begin" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Tanggal Akhir</label>
        <input v-model="end" type="date" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
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

    <div v-if="loading && !data" class="flex justify-center p-12"><Loader2 class="w-7 h-7 animate-spin text-primary" /></div>
    <div v-else-if="data && data.accounts.length === 0" class="rounded-xl border border-border bg-surface p-10 text-center text-sm text-muted italic">Tidak ada transaksi untuk filter ini.</div>

    <div v-else-if="data" class="space-y-5">
      <div v-for="acc in data.accounts" :key="acc.account_code" class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="flex flex-wrap items-center gap-x-6 gap-y-1 px-4 py-2 bg-background/40 border-b border-border">
          <span class="font-semibold text-sm">{{ acc.account_code }} — {{ acc.account_name }}</span>
          <span class="text-xs text-muted">Saldo Awal: <span class="tabular-nums text-foreground">{{ fmt(acc.saldo_awal) }}</span></span>
          <span class="text-xs text-muted ml-auto">Saldo Akhir: <span class="tabular-nums font-medium text-foreground">{{ fmt(acc.saldo_akhir) }}</span></span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-xs">
            <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/30">
              <tr>
                <th class="text-left px-3 py-1.5 font-semibold whitespace-nowrap">Tanggal</th>
                <th class="text-left px-3 py-1.5 font-semibold whitespace-nowrap">No. Transaksi</th>
                <th class="text-left px-3 py-1.5 font-semibold min-w-[16rem]">Keterangan</th>
                <th class="text-left px-3 py-1.5 font-semibold">Sub / Lawan</th>
                <th class="text-right px-3 py-1.5 font-semibold whitespace-nowrap">Debet</th>
                <th class="text-right px-3 py-1.5 font-semibold whitespace-nowrap">Kredit</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in acc.rows" :key="i" class="border-b border-border/20 hover:bg-muted/5">
                <td class="px-3 py-1 whitespace-nowrap">{{ r.journal_date }}</td>
                <td class="px-3 py-1 font-mono text-[10px] whitespace-nowrap">{{ r.transactionno }}</td>
                <td class="px-3 py-1 whitespace-pre-line">{{ r.description }}</td>
                <td class="px-3 py-1 text-muted">{{ r.subaccount }}<span v-if="r.lawan"> · {{ r.lawan }}</span></td>
                <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.debit) }}</td>
                <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.credit) }}</td>
              </tr>
              <tr class="border-t-2 border-border bg-background/30 font-semibold">
                <td class="px-3 py-1.5" colspan="4">Total Mutasi (Bersih: {{ fmt(acc.net) }})</td>
                <td class="px-3 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(acc.total_debit) }}</td>
                <td class="px-3 py-1.5 text-right tabular-nums whitespace-nowrap">{{ fmt(acc.total_credit) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

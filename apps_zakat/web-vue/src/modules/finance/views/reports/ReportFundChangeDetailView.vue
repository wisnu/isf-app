<script setup lang="ts">
import { Download, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef, watch } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import { api, ApiError } from '@/shared/api/client'
import { useAuthStore } from '@/app/stores/auth.store'

interface PDDRow { account_code: string; account_name: string | null; value: number }
interface PDDSection { title: string; rows: PDDRow[]; total: number }
interface PDDFund { fund: string; sections: PDDSection[] }
interface PDDPayload { funds: PDDFund[]; begin: string; end: string; consolidated: boolean }
interface BranchOption { code: string; name: string }

const auth = useAuthStore()
const canPickBranch = computed(() => auth.user?.branch_access === 'all')

const today = new Date()
const p = (n: number) => String(n).padStart(2, '0')
const iso = (d: Date) => `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`

const begin = shallowRef<string>(`${today.getFullYear()}-01-01`)
const end = shallowRef<string>(iso(today))
const branch = shallowRef<string>(auth.user?.primary_branch ?? '')
const branches = ref<BranchOption[]>([])

const data = ref<PDDPayload | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
const fmt = (n: number) => idr.format(Math.round(n ?? 0))

const branchQS = () => (branch.value ? `&branch=${encodeURIComponent(branch.value)}` : '')

async function loadBranches() {
  try {
    branches.value = await api.get<BranchOption[]>('/api/finance/report/fund-changes-detail/branches')
    if (!branch.value && branches.value.length && !canPickBranch.value)
      branch.value = branches.value[0].code
  } catch {
    branches.value = []
  }
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<PDDPayload>(`/api/report/fund-changes-detail?begin=${begin.value}&end=${end.value}${branchQS()}`)
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
    await api.downloadBlob(`/api/report/fund-changes-detail/export.xlsx?begin=${begin.value}&end=${end.value}${branchQS()}`, `perubahandanadetail-${ts}.xlsx`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

watch([begin, end, branch], () => { data.value = null })

// Standar laporan: data di-load saat klik "Tampilkan", bukan saat buka halaman.
onMounted(async () => {
  await loadBranches()
})
</script>

<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-2xl font-bold tracking-tight">Perubahan Dana — Rincian per Akun</h1>
      <p class="text-sm text-muted">Rincian penerimaan &amp; penyaluran per akun untuk tiap jenis dana.</p>
    </div>

    <div class="rounded-xl border border-border bg-surface p-4 flex flex-wrap items-end gap-4">
      <div class="flex flex-col gap-1">
        <label class="text-xs font-medium text-muted">Cabang</label>
        <select v-model="branch" :disabled="!canPickBranch" class="h-9 rounded-lg border border-border bg-surface px-2 text-sm min-w-[16rem] disabled:opacity-60 focus:outline-none focus:ring-1 focus:ring-primary">
          <option v-if="canPickBranch" value="">Konsolidasi (Semua Cabang)</option>
          <option v-for="b in branches" :key="b.code" :value="b.code">{{ b.code }} — {{ b.name }}</option>
        </select>
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
      <Button variant="outline" size="sm" class="gap-1.5 h-9" :disabled="exporting || loading || !data" @click="exportXlsx">
        <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
        {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="text-sm">{{ errorMsg }}</Alert>

    <div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
      Atur filter lalu klik "Tampilkan"
    </div>

    <div v-else-if="data" class="space-y-5">
      <div v-for="f in data.funds" :key="f.fund" class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-4 py-2 bg-background/40 border-b border-border font-semibold">{{ f.fund }}</div>
        <div class="p-4 space-y-4">
          <template v-for="(sec, si) in f.sections" :key="si">
            <div v-if="sec.rows.length" class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="text-[10px] uppercase tracking-widest text-muted border-b border-border/50">
                    <td class="px-3 py-1 font-semibold" colspan="3">{{ sec.title }}</td>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(r, ri) in sec.rows" :key="ri" class="border-b border-border/20">
                    <td class="px-3 py-1 font-mono text-[10px] text-muted whitespace-nowrap w-28">{{ r.account_code }}</td>
                    <td class="px-3 py-1">{{ r.account_name }}</td>
                    <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(r.value) }}</td>
                  </tr>
                  <tr class="border-y border-border/40 font-semibold bg-background/20">
                    <td class="px-3 py-1" colspan="2">Total {{ sec.title }}</td>
                    <td class="px-3 py-1 text-right tabular-nums whitespace-nowrap">{{ fmt(sec.total) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

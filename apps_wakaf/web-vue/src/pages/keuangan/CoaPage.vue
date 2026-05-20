<script setup lang="ts">
import {
  Check,
  ChevronDown,
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
  Download,
  FileText,
  Folder,
  HelpCircle,
  Loader2,
  Plus,
  RefreshCw,
  Search,
  X,
} from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Input from '@/components/ui/Input.vue'
import Tooltip from '@/components/ui/Tooltip.vue'
import { api, ApiError } from '@/lib/api/client'

interface CoaRow {
  code: string
  name: string | null
  type_code: string | null
  type_label: string
  level: number | null
  is_detail: boolean
  is_system: boolean
  parent: string | null
  balance: number
}

interface Pagination {
  page: number
  page_size: number
  total: number
  total_pages: number
}

interface CoaList {
  rows: CoaRow[]
  stats: { total: number; by_type: Record<string, number> }
  pagination: Pagination
}

const data = ref<CoaList | null>(null)
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)
const search = ref('')
const page = ref(1)
const pageSize = ref(25)
const tipsOpen = ref(false)
const compactMode = ref(false)

// === Filters ===
type SifatValue = 'all' | 'detail' | 'group'

const TYPE_OPTIONS: { code: string; label: string }[] = [
  { code: 'A', label: 'Aset' },
  { code: 'L', label: 'Liabilitas' },
  { code: 'E', label: 'Saldo Dana' },
  { code: 'I', label: 'Pendapatan' },
  { code: 'X', label: 'Penyaluran' },
]
const SIFAT_OPTIONS: { value: SifatValue; label: string }[] = [
  { value: 'all', label: 'Semua' },
  { value: 'detail', label: 'Detail' },
  { value: 'group', label: 'Grup' },
]
const LEVEL_OPTIONS: { value: number | null; label: string }[] = [
  { value: null, label: 'Semua' },
  { value: 0, label: '≤ 0' },
  { value: 1, label: '≤ 1' },
  { value: 2, label: '≤ 2' },
  { value: 3, label: '≤ 3' },
  { value: 4, label: '≤ 4' },
]

const typeFilters = ref<Set<string>>(new Set())
const sifatFilter = ref<SifatValue>('all')
const levelMax = ref<number | null>(null)

function toggleType(code: string) {
  const next = new Set(typeFilters.value)
  if (next.has(code)) next.delete(code)
  else next.add(code)
  typeFilters.value = next
}

const hasFilters = computed(
  () =>
    typeFilters.value.size > 0 ||
    sifatFilter.value !== 'all' ||
    levelMax.value !== null ||
    search.value.trim() !== '',
)

function resetFilters() {
  typeFilters.value = new Set()
  sifatFilter.value = 'all'
  levelMax.value = null
  search.value = ''
}

let searchTimer: ReturnType<typeof setTimeout> | undefined

function buildQueryParams(includePaging: boolean): URLSearchParams {
  const params = new URLSearchParams()
  if (includePaging) {
    params.set('page', String(page.value))
    params.set('page_size', String(pageSize.value))
  }
  const q = search.value.trim()
  if (q) params.set('search', q)
  if (typeFilters.value.size > 0) {
    params.set('type', [...typeFilters.value].join(','))
  }
  if (sifatFilter.value === 'detail') params.set('is_detail', 'T')
  else if (sifatFilter.value === 'group') params.set('is_detail', 'F')
  if (levelMax.value !== null) params.set('max_level', String(levelMax.value))
  return params
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = buildQueryParams(true)
    data.value = await api.get<CoaList>(`/api/coa/accounts?${params.toString()}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat COA'
    data.value = null
  } finally {
    loading.value = false
  }
}

watch(search, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    load()
  }, 350)
})
watch([page, pageSize], () => load())
watch([typeFilters, sifatFilter, levelMax], () => {
  page.value = 1
  load()
}, { deep: true })

onMounted(load)

const pageInfo = computed(() => {
  if (!data.value) return { from: 0, to: 0, total: 0, totalPages: 0 }
  const { page: p, page_size: ps, total, total_pages } = data.value.pagination
  const from = total === 0 ? 0 : (p - 1) * ps + 1
  const to = Math.min(p * ps, total)
  return { from, to, total, totalPages: total_pages }
})

const stats = computed(() => {
  const rows = data.value?.rows ?? []
  const by = data.value?.stats.by_type ?? {}
  const detail = rows.filter((r) => r.is_detail).length
  const group = rows.length - detail
  return {
    total: data.value?.stats.total ?? 0,
    aset: by['Aset'] ?? 0,
    detail,
    group,
  }
})

// Warna badge Tipe di tabel
const TYPE_BADGE: Record<string, string> = {
  Aset:       'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300',
  Liabilitas: 'bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-300',
  'Saldo Dana':'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
  Pendapatan: 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
  Penyaluran: 'bg-violet-100 text-violet-800 dark:bg-violet-900/30 dark:text-violet-300',
}

function typeBadgeClass(label: string): string {
  return TYPE_BADGE[label] ?? 'bg-background text-muted border border-border'
}

function indentStyle(level: number | null) {
  const px = Math.max(0, (level ?? 0)) * 14
  return { paddingLeft: px + 'px' }
}

function goto(target: number) {
  const tp = pageInfo.value.totalPages || 1
  page.value = Math.min(Math.max(1, target), tp)
}

async function exportXlsx() {
  exporting.value = true
  errorMsg.value = null
  try {
    const params = buildQueryParams(false)
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '')
    const domain = (import.meta.env.VITE_PORTAL_DOMAIN as string | undefined) ?? ''
    const suggested = domain ? `coa-${domain}-${today}.xlsx` : `coa-${today}.xlsx`
    const path = '/api/coa/accounts.xlsx' + (params.toString() ? '?' + params.toString() : '')
    await api.downloadBlob(path, suggested)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}
</script>

<template>
  <div class="space-y-3">

    <!-- Page header: judul + tombol dalam satu baris -->
    <header class="flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-3">
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-xl font-bold tracking-tight">Chart of Accounts</h1>
            <span class="inline-flex items-center gap-1 text-[10px] font-medium text-muted">
              <span class="w-1.5 h-1.5 rounded-full bg-positive"></span>
              <code class="font-mono">transaction.account</code>
            </span>
          </div>
          <p class="text-xs text-muted">Kelola akun perkiraan dari existing DB</p>
        </div>
      </div>
      <div class="flex flex-wrap gap-1.5">
        <Button variant="outline" size="sm" class="gap-1.5 h-8 rounded-lg text-xs" :disabled="loading" @click="load()">
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
          Reload
        </Button>
        <Button
          variant="outline"
          size="sm"
          class="gap-1.5 h-8 rounded-lg text-xs"
          :disabled="exporting || loading || !data || data.pagination.total === 0"
          @click="exportXlsx"
        >
          <Download class="w-3.5 h-3.5" :class="{ 'animate-pulse': exporting }" />
          {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
        </Button>
        <Button size="sm" class="gap-1.5 h-8 rounded-lg text-xs" disabled>
          <Plus class="w-3.5 h-3.5" />
          Tambah Akun
        </Button>
      </div>
    </header>

    <Alert v-if="errorMsg" variant="destructive" class="py-2 text-xs">
      <strong>Error:</strong> {{ errorMsg }}
    </Alert>

    <!-- Two-column: filter sidebar + data panel -->
    <div class="grid grid-cols-1 lg:grid-cols-[256px_1fr] gap-3 items-start">

      <!-- ── Filter Sidebar ── -->
      <Card>
        <CardContent class="p-4">

          <div class="flex items-center justify-between mb-3">
            <span class="font-semibold text-sm">Filter</span>
            <button
              v-if="hasFilters"
              type="button"
              class="text-xs font-medium text-primary hover:underline"
              @click="resetFilters"
            >
              Reset
            </button>
          </div>

          <!-- CARI AKUN -->
          <div class="mb-3">
            <label class="text-[10px] uppercase tracking-widest text-muted font-semibold block mb-1.5">Cari Akun</label>
            <div class="relative">
              <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted pointer-events-none" />
              <Input
                v-model="search"
                placeholder="Kode, nama, atau parent…"
                class="pl-8 rounded-xl text-xs h-8"
              />
            </div>
          </div>

          <!-- TIPE -->
          <div class="mb-3">
            <label class="text-[10px] uppercase tracking-widest text-muted font-semibold block mb-1.5">Tipe</label>
            <div class="flex flex-wrap gap-1">
              <button
                type="button"
                :class="['text-[11px] px-2.5 py-0.5 rounded-full border transition-colors',
                  typeFilters.size === 0
                    ? 'bg-primary text-primary-foreground border-primary font-medium'
                    : 'border-border text-muted hover:bg-background hover:text-foreground']"
                @click="typeFilters = new Set()"
              >Semua</button>
              <button
                v-for="t in TYPE_OPTIONS" :key="t.code"
                type="button"
                :class="['text-[11px] px-2.5 py-0.5 rounded-full border transition-colors',
                  typeFilters.has(t.code)
                    ? 'bg-primary text-primary-foreground border-primary font-medium'
                    : 'border-border text-muted hover:bg-background hover:text-foreground']"
                @click="toggleType(t.code)"
              >{{ t.label }}</button>
            </div>
          </div>

          <!-- SIFAT AKUN -->
          <div class="mb-3">
            <label class="text-[10px] uppercase tracking-widest text-muted font-semibold block mb-1.5">Sifat Akun</label>
            <div class="flex flex-wrap gap-1">
              <button
                v-for="opt in SIFAT_OPTIONS" :key="opt.value"
                type="button"
                :class="['text-[11px] px-2.5 py-0.5 rounded-full border transition-colors',
                  sifatFilter === opt.value
                    ? 'bg-primary text-primary-foreground border-primary font-medium'
                    : 'border-border text-muted hover:bg-background hover:text-foreground']"
                @click="sifatFilter = opt.value"
              >{{ opt.label }}</button>
            </div>
          </div>

          <!-- LEVEL -->
          <div class="mb-3">
            <label class="text-[10px] uppercase tracking-widest text-muted font-semibold block mb-1.5">Level</label>
            <div class="flex flex-wrap gap-1">
              <button
                v-for="lv in LEVEL_OPTIONS" :key="String(lv.value)"
                type="button"
                :class="['text-[11px] px-2.5 py-0.5 rounded-full border transition-colors tabular-nums',
                  levelMax === lv.value
                    ? 'bg-primary text-primary-foreground border-primary font-medium'
                    : 'border-border text-muted hover:bg-background hover:text-foreground']"
                @click="levelMax = lv.value"
              >{{ lv.label }}</button>
            </div>
          </div>

          <!-- Tips penggunaan collapsible -->
          <div class="border-t border-border pt-2.5 mt-3">
            <button
              type="button"
              class="w-full flex items-center justify-between text-xs font-medium text-foreground hover:text-primary transition-colors"
              @click="tipsOpen = !tipsOpen"
            >
              <span>Tips penggunaan</span>
              <ChevronDown class="w-3.5 h-3.5 transition-transform duration-200 text-muted" :class="{ 'rotate-180': tipsOpen }" />
            </button>
            <div v-if="tipsOpen" class="mt-1.5 space-y-1 text-[11px] text-muted">
              <p>• Klik beberapa <strong>Tipe</strong> sekaligus untuk multi-filter</p>
              <p>• <strong>Level ≤ N</strong> tampilkan struktur tanpa detail</p>
              <p>• <strong>Export Excel</strong> ikut filter aktif</p>
            </div>
          </div>

        </CardContent>
      </Card>

      <!-- ── Data Panel ── -->
      <Card>
        <CardContent class="p-0">

          <!-- Panel header -->
          <div class="px-4 py-2.5 border-b border-border flex flex-wrap items-center justify-between gap-2 rounded-t-2xl">
            <div class="flex items-center gap-3">
              <h2 class="font-semibold text-sm">Daftar Akun</h2>
              <p class="text-[11px] text-muted">
                <template v-if="data">{{ data.rows.length }} dari {{ data.pagination.total }} akun</template>
                <template v-else>Memuat…</template>
              </p>
            </div>
            <div class="flex items-center gap-1.5">
              <select
                class="text-[11px] border border-border rounded-lg px-2 py-1 bg-surface text-foreground cursor-pointer focus:outline-none focus:ring-1 focus:ring-primary"
              >
                <option>Urut kode</option>
                <option>Urut nama</option>
              </select>
              <button
                type="button"
                :class="['text-[11px] px-2.5 py-1 rounded-lg border transition-colors',
                  compactMode
                    ? 'bg-primary/10 border-primary text-primary font-medium'
                    : 'border-border text-muted hover:bg-background hover:text-foreground']"
                @click="compactMode = !compactMode"
              >Mode compact</button>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="loading && !data" class="flex justify-center py-10">
            <Loader2 class="w-5 h-5 animate-spin text-primary" />
          </div>

          <!-- Empty -->
          <div v-else-if="data && data.rows.length === 0" class="flex flex-col items-center gap-1.5 py-10 text-muted">
            <Search class="w-6 h-6 opacity-30" />
            <p class="text-xs">Tidak ada akun yang sesuai filter</p>
          </div>

          <!-- Table -->
          <div v-else-if="data" class="overflow-x-auto">
            <table class="w-full">
              <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
                <tr>
                  <th class="text-left px-3 py-1.5 font-semibold w-24">Kode</th>
                  <th class="text-left px-3 py-1.5 font-semibold">Nama Akun</th>
                  <th class="text-left px-3 py-1.5 font-semibold w-24">Tipe</th>
                  <th class="text-left px-3 py-1.5 font-semibold w-20 max-md:hidden">Parent</th>
                  <th class="text-center px-3 py-1.5 font-semibold w-24">
                    <Tooltip side="bottom" content-class="max-w-xs">
                      <template #trigger>
                        <span class="inline-flex items-center gap-1 cursor-help select-none" tabindex="0">
                          Sifat <HelpCircle class="w-2.5 h-2.5 opacity-50" />
                        </span>
                      </template>
                      <div class="space-y-1.5 normal-case tracking-normal text-xs">
                        <div class="flex items-center gap-2">
                          <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-[10px] font-medium bg-positive/10 text-positive border border-positive/20">
                            <Check class="w-2.5 h-2.5" /> DETAIL
                          </span>
                          <span>Akun leaf, bisa transaksi</span>
                        </div>
                        <div class="flex items-center gap-2">
                          <span class="inline-block px-1.5 py-0.5 rounded text-[10px] font-medium bg-muted/20 text-muted border border-border">GRUP</span>
                          <span>Akun header, tidak bisa transaksi</span>
                        </div>
                      </div>
                    </Tooltip>
                  </th>
                  <th class="text-center px-3 py-1.5 font-semibold w-12">Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="row in data.rows"
                  :key="row.code"
                  :class="[
                    'border-b border-border/40 transition-colors hover:bg-muted/5',
                    !row.is_detail ? 'bg-background/50' : '',
                  ]"
                >
                  <td :class="['px-3 font-mono text-[11px] text-muted tabular-nums', compactMode ? 'py-0.5' : 'py-1']">
                    {{ row.code }}
                  </td>
                  <td :class="['px-3', compactMode ? 'py-0.5' : 'py-1']">
                    <div class="flex items-center gap-1" :style="indentStyle(row.level)">
                      <span v-if="!row.is_detail" class="text-[9px] text-muted/50 select-none shrink-0">▸</span>
                      <Folder v-if="!row.is_detail" class="w-3 h-3 text-muted/40 shrink-0" />
                      <FileText v-else class="w-3 h-3 text-muted/25 shrink-0" />
                      <span :class="['text-xs leading-snug', !row.is_detail ? 'font-semibold' : '']">
                        {{ row.name ?? '—' }}
                      </span>
                    </div>
                  </td>
                  <td :class="['px-3', compactMode ? 'py-0.5' : 'py-1']">
                    <span :class="['inline-block text-[10px] font-semibold uppercase tracking-wide px-1.5 py-px rounded', typeBadgeClass(row.type_label)]">
                      {{ row.type_label }}
                    </span>
                  </td>
                  <td :class="['px-3 font-mono text-[11px] text-muted/60 max-md:hidden tabular-nums', compactMode ? 'py-0.5' : 'py-1']">
                    {{ row.parent ?? '—' }}
                  </td>
                  <td :class="['px-3 text-center', compactMode ? 'py-0.5' : 'py-1']">
                    <span v-if="row.is_detail" class="inline-flex items-center gap-0.5 text-[9px] font-medium px-1.5 py-px rounded bg-positive/10 text-positive border border-positive/20">
                      <Check class="w-2 h-2" /> DETAIL
                    </span>
                    <span v-else class="inline-block text-[9px] font-medium px-1.5 py-px rounded bg-muted/10 text-muted border border-border">
                      GRUP
                    </span>
                  </td>
                  <td :class="['px-3 text-center', compactMode ? 'py-0.5' : 'py-1']">
                    <span class="text-[10px] text-muted/30">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination footer -->
          <div
            v-if="data && pageInfo.totalPages > 0"
            class="px-4 py-2 border-t border-border flex items-center justify-between gap-2 flex-wrap rounded-b-2xl"
          >
            <p class="text-[11px] text-muted tabular-nums">
              {{ pageInfo.from }}–{{ pageInfo.to }} / {{ pageInfo.total }}
            </p>
            <div class="flex items-center gap-1">
              <button :disabled="page === 1" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background transition-colors" @click="goto(1)">
                <ChevronsLeft class="w-3 h-3" />
              </button>
              <button :disabled="page === 1" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background transition-colors" @click="goto(page - 1)">
                <ChevronLeft class="w-3 h-3" />
              </button>
              <span class="text-[11px] px-2.5 py-0.5 rounded-md bg-background border border-border tabular-nums">
                {{ page }} / {{ pageInfo.totalPages }}
              </span>
              <button :disabled="page >= pageInfo.totalPages" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background transition-colors" @click="goto(page + 1)">
                <ChevronRight class="w-3 h-3" />
              </button>
              <button :disabled="page >= pageInfo.totalPages" class="p-1 rounded-md border border-border text-muted disabled:opacity-30 hover:bg-background transition-colors" @click="goto(pageInfo.totalPages)">
                <ChevronsRight class="w-3 h-3" />
              </button>
            </div>
            <select
              v-model.number="pageSize"
              class="text-[11px] border border-border rounded-md px-2 py-0.5 bg-surface text-foreground"
            >
              <option :value="15">15/hal</option>
              <option :value="25">25/hal</option>
              <option :value="50">50/hal</option>
            </select>
          </div>

        </CardContent>
      </Card>

    </div>
  </div>
</template>

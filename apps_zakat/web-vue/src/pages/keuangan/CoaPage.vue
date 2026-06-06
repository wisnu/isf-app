<script setup lang="ts">
import { Check, Download, FileText, Folder, Plus, RefreshCw, Search, X } from 'lucide-vue-next'
import Column from 'primevue/column'

const FilterMatchMode = {
  CONTAINS: 'contains',
  STARTS_WITH: 'startsWith',
  IN: 'in',
  EQUALS: 'equals',
} as const
import { computed, onMounted, ref, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import AppDataTable from '@/components/ui/AppDataTable.vue'
import Button from '@/components/ui/Button.vue'
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

interface CoaList {
  rows: CoaRow[]
  stats: { total: number; by_type: Record<string, number> }
  pagination: { page: number; page_size: number; total: number; total_pages: number }
}

const TYPE_OPTIONS = [
  { code: 'A', label: 'Aset' },
  { code: 'L', label: 'Liabilitas' },
  { code: 'E', label: 'Saldo Dana' },
  { code: 'I', label: 'Pendapatan' },
  { code: 'X', label: 'Penyaluran' },
]

const TYPE_BADGE: Record<string, string> = {
  'Aset':       'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300',
  'Liabilitas': 'bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-300',
  'Saldo Dana': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
  'Pendapatan': 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
  'Penyaluran': 'bg-violet-100 text-violet-800 dark:bg-violet-900/30 dark:text-violet-300',
}

function typeBadgeClass(label: string) {
  return TYPE_BADGE[label] ?? 'bg-background text-muted border border-border'
}

const allRows = ref<CoaRow[]>([])
const statsData = shallowRef<{ total: number; by_type: Record<string, number> } | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const compactMode = shallowRef(true)

const filters = ref({
  global:     { value: null as string | null,    matchMode: FilterMatchMode.CONTAINS },
  code:       { value: null as string | null,    matchMode: FilterMatchMode.STARTS_WITH },
  name:       { value: null as string | null,    matchMode: FilterMatchMode.CONTAINS },
  type_label: { value: null as string[] | null,  matchMode: FilterMatchMode.IN },
  parent:     { value: null as string | null,    matchMode: FilterMatchMode.STARTS_WITH },
  is_detail:  { value: null as boolean | null,   matchMode: FilterMatchMode.EQUALS },
})

const hasActiveFilter = computed(() =>
  Object.values(filters.value).some(f => {
    if (f.value === null || f.value === '') return false
    if (Array.isArray(f.value)) return f.value.length > 0
    return true
  }),
)

function clearFilters() {
  filters.value.global.value = null
  filters.value.code.value = null
  filters.value.name.value = null
  filters.value.type_label.value = null
  filters.value.parent.value = null
  filters.value.is_detail.value = null
}

function toggleTypeFilter(label: string, current: string[] | null, cb: () => void) {
  const arr = current ? [...current] : []
  const idx = arr.indexOf(label)
  if (idx >= 0) arr.splice(idx, 1)
  else arr.push(label)
  filters.value.type_label.value = arr.length ? arr : null
  cb()
}

function setIsDetailFilter(val: boolean | null, cb: () => void) {
  filters.value.is_detail.value = val
  cb()
}

const inputClass = 'w-full rounded-lg border border-border bg-surface px-2 py-1.5 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary placeholder:text-muted/60'

async function loadAll() {
  loading.value = true
  errorMsg.value = null
  try {
    const first = await api.get<CoaList>('/api/coa/accounts?page=1&page_size=500')
    let rows = [...first.rows]
    for (let p = 2; p <= first.pagination.total_pages; p++) {
      const more = await api.get<CoaList>(`/api/coa/accounts?page=${p}&page_size=500`)
      rows = [...rows, ...more.rows]
    }
    allRows.value = rows
    statsData.value = first.stats
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat COA'
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  exporting.value = true
  errorMsg.value = null
  try {
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '')
    const domain = (import.meta.env.VITE_PORTAL_DOMAIN as string | undefined) ?? ''
    const suggested = domain ? `coa-${domain}-${today}.xlsx` : `coa-${today}.xlsx`
    await api.downloadBlob('/api/coa/accounts.xlsx', suggested)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}

onMounted(loadAll)
</script>

<template>
  <div class="space-y-4">
    <!-- Header + actions -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Chart of Accounts</h1>
        <p class="text-sm text-muted">Akun perkiraan dari <code class="text-[11px] bg-muted/20 px-1 rounded">transaction.account</code></p>
      </div>
      <div class="flex items-center gap-2">
        <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" :disabled="loading" @click="loadAll">
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
          Reload
        </Button>
        <Button
          variant="outline" size="sm" class="gap-1.5 h-8 text-xs"
          :disabled="exporting || loading || !allRows.length"
          @click="exportXlsx"
        >
          <Download class="w-3.5 h-3.5" :class="{ 'animate-pulse': exporting }" />
          {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
        </Button>
        <Button size="sm" class="gap-1.5 h-8 text-xs" disabled>
          <Plus class="w-3.5 h-3.5" />
          Tambah Akun
        </Button>
      </div>
    </div>

    <!-- Stats ringkas -->
    <div v-if="statsData" class="flex flex-wrap gap-x-5 gap-y-1 text-[11px] text-muted">
      <span>Total: <strong class="text-foreground">{{ statsData.total }}</strong></span>
      <span v-for="(n, label) in statsData.by_type" :key="label">
        {{ label }}: <strong class="text-foreground">{{ n }}</strong>
      </span>
    </div>

    <Alert v-if="errorMsg" variant="destructive" class="py-2 text-xs">
      <strong>Error:</strong> {{ errorMsg }}
    </Alert>

    <!-- Table card -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar: Clear + compact mode + keyword search -->
      <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <Button
            variant="outline" size="sm" class="gap-1 h-7 text-[11px]"
            :disabled="!hasActiveFilter"
            @click="clearFilters"
          >
            <X class="w-3 h-3" />
            Clear
          </Button>
          <button
            type="button"
            :class="[
              'text-[11px] px-2.5 py-0.5 rounded-lg border transition-colors',
              compactMode
                ? 'bg-primary/10 border-primary text-primary font-medium'
                : 'border-border text-muted hover:bg-background hover:text-foreground',
            ]"
            @click="compactMode = !compactMode"
          >
            Compact
          </button>
        </div>

        <!-- Global keyword search -->
        <div class="relative">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted pointer-events-none" />
          <input
            v-model="filters['global'].value"
            placeholder="Keyword Search"
            :class="[inputClass, 'pl-8 h-8 w-52']"
          />
        </div>
      </div>

      <!-- DataTable dengan client-side filter -->
      <AppDataTable
        :value="allRows"
        :loading="loading"
        v-model:filters="filters"
        filter-display="menu"
        :global-filter-fields="['code', 'name', 'type_label', 'parent']"
        :compact="compactMode"
      >
        <!-- Kode -->
        <Column field="code" header="Kode" style="width:110px;min-width:90px" :show-filter-match-modes="false">
          <template #body="{ data: r }">
            <span class="font-mono text-muted tabular-nums">{{ r.code }}</span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <input
              v-model="filterModel.value"
              :class="inputClass"
              placeholder="Cari kode…"
              @input="filterCallback()"
            />
          </template>
        </Column>

        <!-- Nama Akun -->
        <Column field="name" header="Nama Akun" :show-filter-match-modes="false">
          <template #body="{ data: r }">
            <div class="flex items-center gap-1 leading-snug" :style="{ paddingLeft: Math.max(0, r.level ?? 0) * 14 + 'px' }">
              <Folder v-if="!r.is_detail" class="w-3 h-3 text-muted/40 shrink-0" />
              <FileText v-else class="w-3 h-3 text-muted/25 shrink-0" />
              <span :class="['text-[11px]', !r.is_detail && 'font-semibold']">{{ r.name ?? '—' }}</span>
            </div>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <input
              v-model="filterModel.value"
              :class="inputClass"
              placeholder="Cari nama…"
              @input="filterCallback()"
            />
          </template>
        </Column>

        <!-- Tipe -->
        <Column field="type_label" header="Tipe" style="width:110px;min-width:90px" :show-filter-match-modes="false">
          <template #body="{ data: r }">
            <span :class="['inline-block text-[10px] font-semibold uppercase tracking-wide px-1.5 py-px rounded', typeBadgeClass(r.type_label)]">
              {{ r.type_label }}
            </span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <div class="flex flex-col gap-1.5">
              <label
                v-for="t in TYPE_OPTIONS"
                :key="t.code"
                class="flex items-center gap-2 text-[11px] cursor-pointer py-0.5"
              >
                <input
                  type="checkbox"
                  class="rounded"
                  :checked="Array.isArray(filterModel.value) && filterModel.value.includes(t.label)"
                  @change="toggleTypeFilter(t.label, filterModel.value, filterCallback)"
                />
                <span :class="['px-1.5 py-px rounded text-[10px] font-semibold uppercase', typeBadgeClass(t.label)]">
                  {{ t.label }}
                </span>
              </label>
            </div>
          </template>
        </Column>

        <!-- Parent -->
        <Column field="parent" header="Parent" style="width:90px;min-width:80px" :show-filter-match-modes="false">
          <template #body="{ data: r }">
            <span class="font-mono text-muted/60">{{ r.parent ?? '—' }}</span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <input
              v-model="filterModel.value"
              :class="inputClass"
              placeholder="Kode parent…"
              @input="filterCallback()"
            />
          </template>
        </Column>

        <!-- Sifat -->
        <Column field="is_detail" header="Sifat" style="width:90px;min-width:80px" :show-filter-match-modes="false"
          :pt="{ headerCell: { class: 'text-center px-3 py-1 font-semibold whitespace-nowrap' } }"
        >
          <template #body="{ data: r }">
            <div class="flex justify-center">
              <span v-if="r.is_detail" class="inline-flex items-center gap-0.5 text-[9px] font-medium px-1.5 py-px rounded bg-positive/10 text-positive border border-positive/20">
                <Check class="w-2 h-2" /> DETAIL
              </span>
              <span v-else class="inline-block text-[9px] font-medium px-1.5 py-px rounded bg-muted/10 text-muted border border-border">
                GRUP
              </span>
            </div>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <div class="flex flex-col gap-1">
              <button
                v-for="opt in [{ v: null, l: 'Semua' }, { v: true, l: 'Detail' }, { v: false, l: 'Grup' }]"
                :key="String(opt.v)"
                type="button"
                :class="[
                  'text-[11px] px-2.5 py-0.5 rounded-full border text-left transition-colors',
                  filterModel.value === opt.v
                    ? 'bg-primary text-primary-foreground border-primary font-medium'
                    : 'border-border text-muted hover:bg-background hover:text-foreground',
                ]"
                @click="setIsDetailFilter(opt.v, filterCallback)"
              >
                {{ opt.l }}
              </button>
            </div>
          </template>
        </Column>

        <!-- Aksi -->
        <Column header="Aksi" style="width:50px;min-width:50px"
          :pt="{ headerCell: { class: 'text-center px-3 py-1 font-semibold' } }"
        >
          <template #body>
            <span class="flex justify-center text-[10px] text-muted/30">—</span>
          </template>
        </Column>

        <template #empty>Tidak ada akun yang cocok dengan filter.</template>
      </AppDataTable>
    </div>
  </div>
</template>

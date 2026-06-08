<script setup lang="ts">
import { Check, Download, FileText, Folder, Plus, RefreshCw, Search, X } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref, shallowRef, watch } from 'vue'

import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api, ApiError } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

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

interface CoaSubmission {
  id: number
  status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED'
  submitted_by: string | null
  submitted_at: string | null
  payload: {
    code?: string
    name?: string
    type_code?: string
    parent?: string | null
    is_detail?: boolean
  }
}

const toast = useToast()

// ── Submissions (otorisasi) ────────────────────────────────────────────────────
const submissions = ref<CoaSubmission[]>([])
const showAddModal = shallowRef(false)
const submitting = shallowRef(false)
const newCoa = reactive({ code: '', name: '', type_code: 'A', parent: '', is_detail: true })

async function loadSubmissions() {
  try {
    const res = await api.get<{ rows: CoaSubmission[] }>(
      '/api/otorisasi/my-submissions/?entity_type=coa',
    )
    submissions.value = res.rows ?? []
  } catch {
    // silent
  }
}

async function submitNewCoa() {
  if (!newCoa.code || !newCoa.name) {
    toast.error('Kode dan nama akun wajib diisi')
    return
  }
  submitting.value = true
  try {
    await api.post('/api/otorisasi/save-and-submit/', {
      entity_type: 'coa',
      module: 'keuangan',
      payload: {
        action: 'create',
        code: newCoa.code,
        name: newCoa.name,
        type_code: newCoa.type_code,
        parent: newCoa.parent || null,
        is_detail: newCoa.is_detail,
      },
    })
    toast.success('Permintaan tambah COA dikirim untuk otorisasi')
    showAddModal.value = false
    newCoa.code = ''
    newCoa.name = ''
    newCoa.type_code = 'A'
    newCoa.parent = ''
    newCoa.is_detail = true
    await loadSubmissions()
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal mengirim submission')
  } finally {
    submitting.value = false
  }
}

// ── Data ──────────────────────────────────────────────────────────────────────
const allRows = ref<CoaRow[]>([])
const statsData = shallowRef<{ total: number; by_type: Record<string, number> } | null>(null)
const loading = shallowRef(false)
const exporting = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

// ── Filter state ───────────────────────────────────────────────────────────────
const f = reactive({
  global: '',
  typeLabels: [] as string[],
  isDetail: null as boolean | null,
})

const hasActiveFilter = computed(
  () => f.global !== '' || f.typeLabels.length > 0 || f.isDetail !== null,
)

function clearFilters() {
  f.global = ''
  f.typeLabels = []
  f.isDetail = null
}

function toggleType(label: string) {
  const idx = f.typeLabels.indexOf(label)
  if (idx >= 0) f.typeLabels.splice(idx, 1)
  else f.typeLabels.push(label)
}

// ── Client-side filtering ──────────────────────────────────────────────────────
const filteredRows = computed(() => {
  let rows = allRows.value

  const g = f.global.trim().toLowerCase()
  if (g) rows = rows.filter(r =>
    r.code.toLowerCase().includes(g) ||
    (r.name ?? '').toLowerCase().includes(g) ||
    r.type_label.toLowerCase().includes(g) ||
    (r.parent ?? '').toLowerCase().includes(g),
  )

  if (f.typeLabels.length) {
    rows = rows.filter(r => f.typeLabels.includes(r.type_label))
  }

  if (f.isDetail !== null) {
    rows = rows.filter(r => r.is_detail === f.isDetail)
  }

  return rows
})

// ── Pagination client-side ─────────────────────────────────────────────────────
const pageSize = shallowRef(20)
const currentPage = shallowRef(1)

const totalPages = computed(() => Math.max(1, Math.ceil(filteredRows.value.length / pageSize.value)))
const pagedRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredRows.value.slice(start, start + pageSize.value)
})

watch(filteredRows, () => { currentPage.value = 1 })
watch(pageSize, () => { currentPage.value = 1 })

// ── API ────────────────────────────────────────────────────────────────────────
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

onMounted(() => {
  loadAll()
  loadSubmissions()
})
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <PageHeader title="Chart of Accounts" subtitle="Akun perkiraan dari transaction.account">
      <template #actions>
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
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="showAddModal = true">
          <Plus class="w-3.5 h-3.5" />
          Tambah Akun
        </Button>
      </template>
    </PageHeader>

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

    <!-- Pending submissions -->
    <div v-if="submissions.length > 0" class="rounded-lg border border-amber-200 bg-amber-50 dark:bg-amber-900/10 dark:border-amber-800 p-3">
      <p class="mb-2 text-xs font-semibold uppercase tracking-wide text-amber-700 dark:text-amber-400">
        Permintaan Tambah Akun ({{ submissions.length }})
      </p>
      <div class="space-y-1">
        <div
          v-for="sub in submissions"
          :key="sub.id"
          class="flex items-center gap-3 rounded bg-white dark:bg-zinc-900 px-3 py-1.5 text-[11px] border border-border"
        >
          <span class="font-mono text-muted">#{{ sub.id }}</span>
          <span class="font-semibold">{{ sub.payload.code }}</span>
          <span class="text-muted truncate flex-1">{{ sub.payload.name }}</span>
          <StatusBadge :status="sub.status" />
        </div>
      </div>
    </div>

    <!-- Add COA modal -->
    <Teleport to="body">
      <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
        <div class="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-xl">
          <h2 class="mb-4 text-base font-semibold">Permintaan Tambah Akun COA</h2>
          <div class="space-y-3">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="mb-1 block text-xs font-medium">Kode Akun <span class="text-red-500">*</span></label>
                <input
                  v-model="newCoa.code"
                  placeholder="mis. 110101"
                  class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium">Tipe</label>
                <select
                  v-model="newCoa.type_code"
                  class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
                >
                  <option v-for="t in TYPE_OPTIONS" :key="t.code" :value="t.code">{{ t.label }}</option>
                </select>
              </div>
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium">Nama Akun <span class="text-red-500">*</span></label>
              <input
                v-model="newCoa.name"
                placeholder="Nama akun perkiraan"
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="mb-1 block text-xs font-medium">Kode Parent</label>
                <input
                  v-model="newCoa.parent"
                  placeholder="Opsional"
                  class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
                />
              </div>
              <div class="flex items-end gap-2 pb-0.5">
                <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
                  <input type="checkbox" v-model="newCoa.is_detail" class="rounded" />
                  Akun Detail
                </label>
              </div>
            </div>
          </div>
          <p class="mt-3 text-[10px] text-muted">
            Permintaan ini akan disubmit ke sistem otorisasi. Akun baru aktif setelah disetujui supervisor.
          </p>
          <div class="mt-4 flex justify-end gap-2">
            <Button variant="outline" size="sm" :disabled="submitting" @click="showAddModal = false">Batal</Button>
            <Button size="sm" :disabled="submitting" @click="submitNewCoa">
              {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Table card -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">

      <!-- Toolbar: filter + search -->
      <div class="px-4 py-2.5 border-b border-border flex flex-wrap items-center gap-3">
        <!-- Clear filter -->
        <div class="flex items-center gap-2 shrink-0">
          <Button
            variant="outline" size="sm" class="gap-1 h-7 text-[11px]"
            :disabled="!hasActiveFilter"
            @click="clearFilters"
          >
            <X class="w-3 h-3" />
            Clear
          </Button>
        </div>

        <!-- Type filter chips -->
        <div class="flex items-center gap-1 flex-wrap">
          <button
            v-for="t in TYPE_OPTIONS"
            :key="t.code"
            type="button"
            :class="[
              'text-[10px] font-semibold uppercase px-1.5 py-px rounded border transition-colors cursor-pointer',
              f.typeLabels.includes(t.label)
                ? typeBadgeClass(t.label) + ' ring-1 ring-offset-1 ring-current'
                : 'border-border text-muted/60 hover:border-muted',
            ]"
            @click="toggleType(t.label)"
          >{{ t.label }}</button>
        </div>

        <!-- Sifat toggle -->
        <div class="flex items-center rounded-lg border border-border overflow-hidden text-[11px] shrink-0">
          <button
            v-for="opt in [{ v: null, l: 'Semua' }, { v: true, l: 'Detail' }, { v: false, l: 'Grup' }]"
            :key="String(opt.v)"
            type="button"
            :class="[
              'px-2.5 py-1 transition-colors border-r border-border last:border-0',
              f.isDetail === opt.v
                ? 'bg-primary text-primary-foreground font-medium'
                : 'text-muted hover:bg-background',
            ]"
            @click="f.isDetail = opt.v"
          >{{ opt.l }}</button>
        </div>

        <!-- Global search -->
        <div class="relative ml-auto">
          <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted pointer-events-none" />
          <input
            v-model="f.global"
            placeholder="Cari kode, nama, tipe…"
            class="h-8 pl-8 pr-3 w-52 rounded-lg border border-border bg-surface text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
      </div>

      <!-- Pagination -->
      <div class="px-4 py-2 border-b border-border flex items-center justify-between">
        <span class="text-[11px] text-muted tabular-nums">
          <template v-if="allRows.length">
            {{ (currentPage - 1) * pageSize + 1 }}–{{ Math.min(currentPage * pageSize, filteredRows.length) }}
            dari {{ filteredRows.length }} akun
          </template>
        </span>
        <TablePagination
          :page="currentPage"
          :total-pages="totalPages"
          :total="filteredRows.length"
          :page-size="pageSize"
          :loading="loading"
          unit="akun"
          @prev="currentPage--"
          @next="currentPage++"
          @update:page-size="pageSize = $event"
        />
      </div>

      <!-- Native table -->
      <div class="overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 font-medium text-left w-28">Kode</th>
              <th class="px-4 py-2 font-medium text-left">Nama Akun</th>
              <th class="px-4 py-2 font-medium text-left w-28">Tipe</th>
              <th class="px-4 py-2 font-medium text-left w-24">Parent</th>
              <th class="px-4 py-2 font-medium text-center w-20">Sifat</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="5" class="px-4 py-8 text-center text-muted">Memuat...</td>
            </tr>
            <tr v-else-if="pagedRows.length === 0">
              <td colspan="5" class="px-4 py-8 text-center text-muted italic">
                Tidak ada akun yang cocok dengan filter.
              </td>
            </tr>
            <tr
              v-for="r in pagedRows"
              :key="r.code"
              class="border-b border-border last:border-0 hover:bg-background/60"
            >
              <td class="px-4 py-1 font-mono tabular-nums text-muted">
                {{ r.code }}
              </td>
              <td class="px-4 py-1">
                <div
                  class="flex items-center gap-1 leading-snug"
                  :style="{ paddingLeft: Math.max(0, r.level ?? 0) * 14 + 'px' }"
                >
                  <Folder v-if="!r.is_detail" class="w-3 h-3 text-muted/40 shrink-0" />
                  <FileText v-else class="w-3 h-3 text-muted/25 shrink-0" />
                  <span :class="!r.is_detail ? 'font-semibold' : ''">{{ r.name ?? '—' }}</span>
                </div>
              </td>
              <td class="px-4 py-1">
                <span :class="['inline-block text-[10px] font-semibold uppercase tracking-wide px-1.5 py-px rounded', typeBadgeClass(r.type_label)]">
                  {{ r.type_label }}
                </span>
              </td>
              <td class="px-4 py-1 font-mono text-muted/60">
                {{ r.parent ?? '—' }}
              </td>
              <td class="px-4 py-1 text-center">
                <span v-if="r.is_detail" class="inline-flex items-center gap-0.5 text-[9px] font-medium px-1.5 py-px rounded bg-positive/10 text-positive border border-positive/20">
                  <Check class="w-2 h-2" /> DETAIL
                </span>
                <span v-else class="inline-block text-[9px] font-medium px-1.5 py-px rounded bg-muted/10 text-muted border border-border">
                  GRUP
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

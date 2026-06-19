<script setup lang="ts">
import { ClipboardList, RefreshCw } from 'lucide-vue-next'
import { onMounted, shallowRef, ref } from 'vue'

import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import SubmissionDetailDrawer from '@/components/otorisasi/SubmissionDetailDrawer.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import TablePagination from '@/components/ui/TablePagination.vue'
import { api } from '@/lib/api/client'
import { dmy, dmyt } from '@/lib/date'

interface SubmissionRow {
  id: number
  entity_type: string
  entity_label: string
  branch_code: string
  submitted_by: string
  submitted_at: string | null
  status: string
  level_current: number
  level_required: number
  payload: Record<string, any>
  approval_log: any[]
}

interface ListResponse {
  rows: SubmissionRow[]
  pagination: { page: number; limit: number; total: number; total_pages: number }
}

// ── Filter state ──────────────────────────────────────────────────────────────

function defaultDateFrom(): string {
  const d = new Date()
  d.setMonth(d.getMonth() - 1)
  return d.toISOString().slice(0, 10)
}
function todayIso(): string {
  return new Date().toISOString().slice(0, 10)
}

const filterDateFrom = shallowRef(defaultDateFrom())
const filterDateTo = shallowRef(todayIso())
const filterEntityType = shallowRef<string | null>(null)
const filterStatus = shallowRef<string | null>(null)

const entityTypes = [
  { label: 'Semua Jenis', value: null },
  { label: 'Penghimpunan', value: 'penghimpunan' },
  { label: 'Penyaluran', value: 'penyaluran' },
  { label: 'Upload', value: 'upload_penghimpunan' },
  { label: 'COA', value: 'coa' },
  { label: 'Kas', value: 'kas' },
  { label: 'Bank', value: 'bank' },
]

const statusOptions = [
  { label: 'Semua Status', value: null },
  { label: 'Pending', value: 'PENDING' },
  { label: 'Diotorisasi', value: 'AUTHORIZED' },
  { label: 'Ditolak', value: 'REJECTED' },
  { label: 'Draft', value: 'DRAFT' },
]

// ── Data ──────────────────────────────────────────────────────────────────────

const rows = ref<SubmissionRow[]>([])
const total = shallowRef(0)
const totalPages = shallowRef(1)
const page = shallowRef(1)
const pageSize = shallowRef(25)
const loading = shallowRef(false)
const hasLoaded = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      page_size: String(pageSize.value),
    })
    if (filterEntityType.value) params.set('entity_type', filterEntityType.value)
    if (filterStatus.value) params.set('status', filterStatus.value)
    if (filterDateFrom.value) params.set('date_from', filterDateFrom.value)
    if (filterDateTo.value) params.set('date_to', filterDateTo.value)

    const res = await api.get<ListResponse>(`/api/otorisasi/my-submissions/?${params}`)
    rows.value = res.rows ?? []
    total.value = res.pagination?.total ?? 0
    totalPages.value = res.pagination?.total_pages ?? 1
    hasLoaded.value = true
  } catch {
    errorMsg.value = 'Gagal memuat riwayat submission'
    rows.value = []
  } finally {
    loading.value = false
  }
}

function goto(p: number) {
  page.value = Math.min(Math.max(1, p), totalPages.value)
  load()
}

function applyFilter() {
  page.value = 1
  load()
}

// ── Payload helpers ───────────────────────────────────────────────────────────

function parsePayload(payload: unknown): Record<string, any> {
  if (typeof payload === 'string') {
    try { return JSON.parse(payload) } catch { return {} }
  }
  return (payload as Record<string, any>) ?? {}
}

function summaryText(row: SubmissionRow): string {
  const p = parsePayload(row.payload)
  switch (row.entity_type) {
    case 'penghimpunan':
    case 'penyaluran':
      return p.donor_name ?? p.description ?? `${(p.items ?? []).length} item`
    case 'bank':
      return p.account_name ?? p.bank_account_no ?? '—'
    case 'coa':
      return p.account_name ?? p.account_no ?? '—'
    case 'kas':
      return p.account_name ?? p.name ?? p.code ?? '—'
    case 'upload_penghimpunan':
      return p.filename ?? `${p.total_rows ?? 0} baris`
    default:
      return '—'
  }
}

function actionBadge(row: SubmissionRow): { text: string; cls: string } | null {
  const p = parsePayload(row.payload)
  if (!p.action) return null
  const a = String(p.action).toUpperCase()
  const cls = a === 'CREATE' ? 'bg-emerald-100 text-emerald-700'
            : a === 'DELETE' ? 'bg-red-100 text-red-700'
            : a === 'EDIT'   ? 'bg-amber-100 text-amber-700'
            : 'bg-zinc-100 text-zinc-600'
  return { text: a, cls }
}

// ── Detail drawer ─────────────────────────────────────────────────────────────

const drawerOpen = ref(false)
const drawerRow = ref<SubmissionRow | null>(null)

function openDetail(row: SubmissionRow) {
  drawerRow.value = row
  drawerOpen.value = true
}

function onDrawerClose() {
  drawerOpen.value = false
  drawerRow.value = null
}

onMounted(load)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Riwayat Submission" subtitle="Daftar submission yang pernah Anda kirim">
      <template #actions>
        <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" :disabled="loading" @click="load()">
          <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': loading }" />
          Refresh
        </Button>
      </template>
    </PageHeader>

    <!-- Filter bar -->
    <div class="flex flex-wrap items-end gap-3 rounded-t border bg-white px-4 py-3 dark:bg-zinc-900">
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Dari Tanggal</label>
        <DateField v-model="filterDateFrom" />
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Sampai Tanggal</label>
        <DateField v-model="filterDateTo" />
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Jenis Input</label>
        <select
          v-model="filterEntityType"
          class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
        >
          <option v-for="et in entityTypes" :key="String(et.value)" :value="et.value">
            {{ et.label }}
          </option>
        </select>
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium text-zinc-500">Status</label>
        <select
          v-model="filterStatus"
          class="h-9 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
        >
          <option v-for="s in statusOptions" :key="String(s.value)" :value="s.value">
            {{ s.label }}
          </option>
        </select>
      </div>
      <button
        type="button"
        class="h-9 rounded-lg bg-primary px-4 text-sm font-medium text-white hover:bg-primary/90 transition-colors disabled:opacity-50"
        :disabled="loading"
        @click="applyFilter"
      >
        Tampilkan
      </button>
    </div>

    <!-- Count bar -->
    <div class="flex items-center justify-between border-x bg-white px-4 py-2 dark:bg-zinc-900">
      <span class="text-xs text-zinc-500">
        <template v-if="loading">Memuat...</template>
        <template v-else-if="hasLoaded && total > 0">
          {{ (page - 1) * 25 + 1 }}–{{ Math.min(page * 25, total) }} dari {{ total }} submission
        </template>
        <template v-else-if="hasLoaded">Tidak ada submission ditemukan</template>
        <template v-else>Pilih filter lalu klik Tampilkan</template>
      </span>
      <TablePagination
        v-if="hasLoaded"
        :page="page"
        :total-pages="totalPages"
        :total="total"
        :page-size="pageSize"
        :loading="loading"
        unit="submission"
        @prev="goto(page - 1)"
        @next="goto(page + 1)"
        @update:page-size="pageSize = $event; goto(1)"
      />
    </div>

    <!-- Table -->
    <div class="overflow-x-auto rounded-b border">
      <table class="w-full text-sm">
        <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
          <tr>
            <th class="px-4 py-2 font-medium text-left">ID</th>
            <th class="px-4 py-2 font-medium text-left">Jenis</th>
            <th class="px-4 py-2 font-medium text-left">Operasi</th>
            <th class="px-4 py-2 font-medium text-left">Ringkasan</th>
            <th class="px-4 py-2 font-medium text-left">Disubmit</th>
            <th class="px-4 py-2 font-medium text-center">Level</th>
            <th class="px-4 py-2 font-medium text-center">Status</th>
            <th class="px-4 py-2 font-medium text-left">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading && !rows.length">
            <td colspan="8" class="px-4 py-8 text-center text-zinc-400">Memuat...</td>
          </tr>
          <tr v-else-if="hasLoaded && rows.length === 0">
            <td colspan="8" class="px-4 py-8 text-center text-zinc-400">
              Tidak ada submission pada periode ini.
            </td>
          </tr>
          <tr v-else-if="!hasLoaded">
            <td colspan="8" class="px-4 py-8 text-center text-zinc-300 italic">
              Pilih filter lalu klik Tampilkan
            </td>
          </tr>
          <tr
            v-for="row in rows"
            :key="row.id"
            class="cursor-pointer border-b border-border last:border-0 hover:bg-background/60"
            @click="openDetail(row)"
          >
            <td class="px-4 py-2 font-mono text-xs text-zinc-400">#{{ row.id }}</td>
            <td class="px-4 py-2 font-medium text-sm">{{ row.entity_label ?? row.entity_type }}</td>
            <td class="px-4 py-2">
              <span
                v-if="actionBadge(row)"
                :class="['inline-block rounded px-1.5 py-px text-[10px] font-bold uppercase tracking-wide', actionBadge(row)!.cls]"
              >{{ actionBadge(row)!.text }}</span>
              <span v-else class="text-xs text-zinc-300">—</span>
            </td>
            <td class="px-4 py-2 text-xs text-zinc-700 dark:text-zinc-300 max-w-[220px] truncate">
              {{ summaryText(row) }}
            </td>
            <td class="px-4 py-2 text-xs text-zinc-500">
              {{ row.submitted_at ? dmyt(row.submitted_at) : '—' }}
            </td>
            <td class="px-4 py-2 text-center text-xs text-zinc-500">
              {{ row.level_current }}/{{ row.level_required }}
            </td>
            <td class="px-4 py-2 text-center">
              <StatusBadge :status="(row.status as any)" />
            </td>
            <td class="px-4 py-2">
              <button
                class="text-xs font-medium text-primary hover:underline"
                @click.stop="openDetail(row)"
              >
                Lihat Detail
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Detail drawer (reuse komponen otorisasi, tanpa tombol approve/reject) -->
    <SubmissionDetailDrawer
      :submission="drawerRow"
      :open="drawerOpen"
      :readonly="true"
      @close="onDrawerClose"
      @approved="load(); onDrawerClose()"
      @rejected="load(); onDrawerClose()"
    />
  </div>
</template>

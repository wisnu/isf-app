<script setup lang="ts">
import {
  Check,
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
  Download,
  FileText,
  Folder,
  HelpCircle,
  Loader2,
  Lock,
  Plus,
  RefreshCw,
  Search,
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
const pageSize = ref(50)

let searchTimer: ReturnType<typeof setTimeout> | undefined

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const params = new URLSearchParams({
      page: String(page.value),
      page_size: String(pageSize.value),
    })
    const q = search.value.trim()
    if (q) params.set('search', q)
    data.value = await api.get<CoaList>(`/api/coa/accounts?${params.toString()}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat COA'
    data.value = null
  } finally {
    loading.value = false
  }
}

// search → debounce 350ms + reset page
watch(search, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    load()
  }, 350)
})

// page or pageSize → fetch
watch([page, pageSize], () => load())

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

function typeColor(label: string): string {
  switch (label) {
    case 'Aset':
      return 'bg-primary/10 text-primary'
    case 'Liabilitas':
      return 'bg-warning/15 text-warning'
    case 'Saldo Dana':
      return 'bg-accent/15 text-accent'
    case 'Pendapatan':
      return 'bg-positive/15 text-positive'
    case 'Penyaluran':
      return 'bg-destructive/10 text-destructive'
    default:
      return 'bg-background text-muted border border-border'
  }
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
    const params = new URLSearchParams()
    const q = search.value.trim()
    if (q) params.set('search', q)
    const today = new Date().toISOString().slice(0, 10).replace(/-/g, '')
    const domain = (import.meta.env.VITE_PORTAL_DOMAIN as string | undefined) ?? ''
    const suggested = domain ? `coa-${domain}-${today}.xlsx` : `coa-${today}.xlsx`
    const path =
      '/api/coa/accounts.xlsx' +
      (params.toString() ? '?' + params.toString() : '')
    await api.downloadBlob(path, suggested)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? `Export gagal: ${e.message}` : 'Export gagal'
  } finally {
    exporting.value = false
  }
}
</script>

<template>
  <div class="space-y-6">
    <header class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Chart of Accounts</h1>
        <p class="text-sm text-muted">
          Daftar akun perkiraan dari existing DB · tabel
          <code class="text-xs bg-background px-1 rounded">transaction.account</code>
        </p>
      </div>
      <div class="flex flex-wrap gap-2">
        <Button variant="outline" class="gap-1.5" :disabled="loading" @click="load()">
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
          Reload
        </Button>
        <Button
          variant="outline"
          class="gap-1.5"
          :disabled="exporting || loading || !data || data.pagination.total === 0"
          :title="search ? 'Export filter aktif (semua row yang match)' : 'Export semua akun'"
          @click="exportXlsx"
        >
          <Download class="w-4 h-4" :class="{ 'animate-pulse': exporting }" />
          {{ exporting ? 'Mengekspor…' : 'Export Excel' }}
        </Button>
        <Button class="gap-1.5" disabled title="Write akan tersedia di Fase 4 dengan workflow approval">
          <Plus class="w-4 h-4" />
          Tambah Akun
        </Button>
      </div>
    </header>

    <Alert v-if="errorMsg" variant="destructive">
      <span><strong>Error:</strong> {{ errorMsg }} — cek koneksi DB di api-python (env DATABASE_URL).</span>
    </Alert>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Total Akun</p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.total }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Aset</p>
          <p class="text-2xl font-bold tabular-nums text-primary">{{ stats.aset }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted flex items-center gap-1">
            <Check class="w-3.5 h-3.5 text-positive" /> Detail
          </p>
          <p class="text-2xl font-bold tabular-nums text-positive">{{ stats.detail }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted flex items-center gap-1">
            <Folder class="w-3.5 h-3.5" /> Grup / Header
          </p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.group }}</p>
        </CardContent>
      </Card>
    </div>

    <Card>
      <CardContent class="p-0">
        <div class="px-4 py-3 border-b border-border flex items-center gap-2">
          <Search class="w-4 h-4 text-muted shrink-0" />
          <Input
            v-model="search"
            placeholder="Cari kode atau nama akun…"
            class="h-8 border-0 focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent p-0"
          />
        </div>

        <div v-if="loading && !data" class="flex justify-center p-12">
          <Loader2 class="w-6 h-6 animate-spin text-primary" />
        </div>

        <div v-else-if="data" class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-xs text-muted uppercase tracking-wide">
              <tr class="border-b border-border">
                <th class="text-left px-4 py-2 font-medium w-28">Kode</th>
                <th class="text-left px-4 py-2 font-medium">Nama Akun</th>
                <th class="text-left px-4 py-2 font-medium w-32">Tipe</th>
                <th class="text-left px-4 py-2 font-medium w-24 max-md:hidden">Parent</th>
                <th class="text-center px-4 py-2 font-medium w-32">
                  <Tooltip side="bottom" content-class="max-w-md">
                    <template #trigger>
                      <span
                        class="inline-flex items-center gap-1 cursor-help select-none"
                        tabindex="0"
                      >
                        Sifat
                        <HelpCircle class="w-3 h-3 opacity-60" />
                      </span>
                    </template>
                    <div class="space-y-1.5 normal-case tracking-normal">
                      <div class="flex items-start gap-2">
                        <span
                          class="inline-flex items-center gap-1 text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium bg-positive/15 text-positive shrink-0"
                        >
                          <Check class="w-3 h-3" /> Detail
                        </span>
                        <span class="text-foreground">
                          akun leaf (<code class="bg-background px-1 rounded">is_detail = T</code>) — boleh menerima posting jurnal
                        </span>
                      </div>
                      <div class="flex items-start gap-2">
                        <span
                          class="inline-flex items-center gap-1 text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium bg-background text-muted border border-border shrink-0"
                        >
                          <Lock class="w-3 h-3" /> Grup
                        </span>
                        <span class="text-foreground">
                          akun header (<code class="bg-background px-1 rounded">is_detail = F</code>) — hanya agregasi, tidak untuk posting
                        </span>
                      </div>
                    </div>
                  </Tooltip>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="r in data.rows"
                :key="r.code"
                class="border-b border-border last:border-0 hover:bg-background/60"
                :class="{ 'bg-background/40': !r.is_detail }"
              >
                <td
                  class="px-4 py-2 font-mono text-xs tabular-nums whitespace-nowrap"
                  :class="{ 'font-semibold text-foreground': !r.is_detail }"
                >
                  {{ r.code }}
                </td>
                <td class="px-4 py-2">
                  <div :style="indentStyle(r.level)" class="flex items-center gap-2 min-w-0">
                    <Folder
                      v-if="!r.is_detail"
                      class="w-3.5 h-3.5 text-muted shrink-0"
                    />
                    <FileText
                      v-else
                      class="w-3.5 h-3.5 text-muted/60 shrink-0"
                    />
                    <span
                      class="truncate"
                      :class="!r.is_detail ? 'font-semibold' : 'font-normal'"
                    >
                      {{ r.name ?? '—' }}
                    </span>
                  </div>
                </td>
                <td class="px-4 py-2">
                  <span
                    class="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium"
                    :class="typeColor(r.type_label)"
                  >{{ r.type_label }}</span>
                </td>
                <td class="px-4 py-2 text-xs text-muted tabular-nums max-md:hidden">
                  {{ r.parent ?? '—' }}
                </td>
                <td class="px-4 py-2 text-center">
                  <span
                    v-if="r.is_detail"
                    class="inline-flex items-center gap-1 text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium bg-positive/15 text-positive"
                    title="Akun detail — boleh menerima posting transaksi"
                  >
                    <Check class="w-3 h-3" /> Detail
                  </span>
                  <span
                    v-else
                    class="inline-flex items-center gap-1 text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium bg-background text-muted border border-border"
                    title="Akun grup / header — tidak boleh menerima posting transaksi"
                  >
                    <Lock class="w-3 h-3" /> Grup
                  </span>
                </td>
              </tr>
              <tr v-if="data.rows.length === 0">
                <td colspan="5" class="px-4 py-8 text-center text-sm text-muted">
                  Tidak ada akun cocok dengan pencarian.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination footer -->
        <div
          v-if="data && data.pagination.total > 0"
          class="px-4 py-2.5 border-t border-border flex flex-wrap items-center justify-between gap-3 text-sm"
        >
          <span class="text-xs text-muted tabular-nums">
            {{ pageInfo.from }}–{{ pageInfo.to }} dari {{ pageInfo.total }} akun
          </span>

          <div class="flex items-center gap-1">
            <Button
              variant="outline" size="sm" class="h-8 w-8 p-0"
              :disabled="page <= 1" title="Halaman pertama"
              @click="goto(1)"
            >
              <ChevronsLeft class="w-4 h-4" />
            </Button>
            <Button
              variant="outline" size="sm" class="h-8 w-8 p-0"
              :disabled="page <= 1" title="Sebelumnya"
              @click="goto(page - 1)"
            >
              <ChevronLeft class="w-4 h-4" />
            </Button>
            <span class="px-3 py-1 text-xs tabular-nums whitespace-nowrap">
              Hal {{ data.pagination.page }} / {{ pageInfo.totalPages }}
            </span>
            <Button
              variant="outline" size="sm" class="h-8 w-8 p-0"
              :disabled="page >= pageInfo.totalPages" title="Berikutnya"
              @click="goto(page + 1)"
            >
              <ChevronRight class="w-4 h-4" />
            </Button>
            <Button
              variant="outline" size="sm" class="h-8 w-8 p-0"
              :disabled="page >= pageInfo.totalPages" title="Halaman terakhir"
              @click="goto(pageInfo.totalPages)"
            >
              <ChevronsRight class="w-4 h-4" />
            </Button>
          </div>

          <div class="flex items-center gap-2">
            <span class="text-xs text-muted">Per hal:</span>
            <select
              v-model.number="pageSize"
              class="h-8 px-2 rounded border border-border bg-surface text-sm"
              @change="page = 1"
            >
              <option :value="25">25</option>
              <option :value="50">50</option>
              <option :value="100">100</option>
              <option :value="200">200</option>
            </select>
          </div>
        </div>
      </CardContent>
    </Card>

  </div>
</template>

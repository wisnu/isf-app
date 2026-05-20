<script setup lang="ts">
import { Check, FileText, Folder, Loader2, Lock, Plus, RefreshCw, Search } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Input from '@/components/ui/Input.vue'
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
}

const data = ref<CoaList | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const search = ref('')

let timer: ReturnType<typeof setTimeout> | undefined

async function load(query?: string) {
  loading.value = true
  errorMsg.value = null
  try {
    const q = (query ?? '').trim()
    const path = q
      ? `/api/coa/accounts?search=${encodeURIComponent(q)}&limit=2000`
      : `/api/coa/accounts?limit=2000`
    data.value = await api.get<CoaList>(path)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat COA'
    data.value = null
  } finally {
    loading.value = false
  }
}

watch(search, (q) => {
  if (timer) clearTimeout(timer)
  timer = setTimeout(() => load(q), 350)
})

onMounted(() => load())

const stats = computed(() => {
  const rows = data.value?.rows ?? []
  const by = data.value?.stats.by_type ?? {}
  const detail = rows.filter((r) => r.is_detail).length
  const group = rows.length - detail
  return {
    total: data.value?.stats.total ?? rows.length,
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
      <div class="flex gap-2">
        <Button variant="outline" class="gap-1.5" :disabled="loading" @click="load(search)">
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
          Reload
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
          <span class="text-xs text-muted whitespace-nowrap">
            {{ data ? `${data.rows.length} baris` : '—' }}
          </span>
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
                <th class="text-center px-4 py-2 font-medium w-32">Sifat</th>
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
      </CardContent>
    </Card>

    <p class="text-xs text-muted">
      <strong class="text-foreground">Detail</strong> = akun leaf (<code class="bg-background px-1 rounded">is_detail = T</code>) yang dapat menerima posting transaksi jurnal.
      <strong class="text-foreground">Grup</strong> = akun header (<code class="bg-background px-1 rounded">is_detail = F</code>), hanya untuk agregasi laporan, tidak boleh menerima posting.
      Indentasi nama mengikuti kolom <code class="bg-background px-1 rounded">account_level</code>.
    </p>
  </div>
</template>

<script setup lang="ts">
import {
  Coins,
  Gauge,
  HandHeart,
  LayoutGrid,
  Loader2,
} from 'lucide-vue-next'
import type { FunctionalComponent } from 'vue'
import { computed, onMounted, ref, watch } from 'vue'

import AsnafDonut from '@/components/widgets/AsnafDonut.vue'
import FundraisingProgress from '@/components/widgets/FundraisingProgress.vue'
import KpiCard from '@/components/widgets/KpiCard.vue'
import RecentActivity from '@/components/widgets/RecentActivity.vue'
import TrendChart from '@/components/widgets/TrendChart.vue'
import Alert from '@/components/ui/Alert.vue'
import { api, ApiError } from '@/lib/api/client'
import { cn } from '@/lib/utils'
import { useAuthStore } from '@/stores/auth'

interface KpiPair { total: number; delta_pct: number }
interface DashboardSummary {
  tenant_id: string
  tenant_name: string
  period: string
  kpis: {
    penerimaan: KpiPair
    penyaluran: KpiPair
    saldo: KpiPair
    donatur_baru: KpiPair
  }
  trend: { labels: string[]; penerimaan: number[]; penyaluran: number[] }
  asnaf_distribution: { label: string; amount: number }[]
  fundraising_channels: { label: string; actual: number; target: number }[]
  recent_transactions: {
    id: string
    date: string
    type: string
    channel: string
    amount: number
    donor: string
  }[]
}

type View = 'ringkasan' | 'keuangan' | 'penghimpunan' | 'ringkas'

interface Tab {
  id: View
  label: string
  icon: FunctionalComponent
  desc: string
}

const tabs: Tab[] = [
  { id: 'ringkasan', label: 'Ringkasan', icon: LayoutGrid, desc: 'Overview komprehensif semua domain' },
  { id: 'keuangan', label: 'Keuangan', icon: Coins, desc: 'Fokus penerimaan, penyaluran, dan distribusi asnaf' },
  { id: 'penghimpunan', label: 'Penghimpunan', icon: HandHeart, desc: 'Fokus capaian fundraising per channel dan donatur' },
  { id: 'ringkas', label: 'Ringkas', icon: Gauge, desc: 'KPI utama tanpa chart — untuk monitoring cepat' },
]

const VIEW_STORAGE_KEY = 'isf-dashboard-view'
const validViews = tabs.map((t) => t.id)

function loadView(): View {
  const stored = localStorage.getItem(VIEW_STORAGE_KEY)
  if (stored && validViews.includes(stored as View)) return stored as View
  return 'ringkasan'
}

const auth = useAuthStore()
const data = ref<DashboardSummary | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const view = ref<View>(loadView())

watch(view, (v) => {
  localStorage.setItem(VIEW_STORAGE_KEY, v)
})

const activeDesc = computed(() => tabs.find((t) => t.id === view.value)?.desc ?? '')

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<DashboardSummary>('/api/dashboard/summary')
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat dashboard'
    data.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(
  () => auth.activeTenantId,
  () => { if (auth.activeTenantId) load() },
)
</script>

<template>
  <div class="space-y-6">
    <header>
      <h1 class="text-2xl font-bold tracking-tight">Dashboard</h1>
      <p v-if="data" class="text-sm text-muted">
        {{ data.tenant_name }} · Periode {{ data.period }}
      </p>
    </header>

    <!-- Dashboard view tabs -->
    <div>
      <div class="flex flex-wrap gap-1 border-b border-border overflow-x-auto" role="tablist">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          role="tab"
          :aria-selected="view === tab.id"
          :class="
            cn(
              'flex items-center gap-2 px-4 py-2.5 text-sm font-medium border-b-2 -mb-px transition-colors whitespace-nowrap',
              view === tab.id
                ? 'border-primary text-primary'
                : 'border-transparent text-muted hover:text-foreground hover:border-border',
            )
          "
          @click="view = tab.id"
        >
          <component :is="tab.icon" class="w-4 h-4" />
          <span>{{ tab.label }}</span>
        </button>
      </div>
      <p class="text-xs text-muted mt-2">{{ activeDesc }}</p>
    </div>

    <div v-if="loading" class="flex justify-center p-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary" />
    </div>

    <Alert v-else-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <template v-else-if="data">
      <!-- View: Ringkasan (default — all widgets) -->
      <template v-if="view === 'ringkasan'">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard label="Penerimaan" :amount="data.kpis.penerimaan.total" :delta-pct="data.kpis.penerimaan.delta_pct" />
          <KpiCard label="Penyaluran" :amount="data.kpis.penyaluran.total" :delta-pct="data.kpis.penyaluran.delta_pct" />
          <KpiCard label="Saldo Aktif" :amount="data.kpis.saldo.total" :delta-pct="data.kpis.saldo.delta_pct" />
          <KpiCard label="Donatur Baru" :amount="data.kpis.donatur_baru.total" :delta-pct="data.kpis.donatur_baru.delta_pct" format="count" />
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div class="lg:col-span-2">
            <TrendChart :labels="data.trend.labels" :penerimaan="data.trend.penerimaan" :penyaluran="data.trend.penyaluran" />
          </div>
          <div>
            <AsnafDonut :items="data.asnaf_distribution" />
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div>
            <FundraisingProgress :items="data.fundraising_channels" />
          </div>
          <div class="lg:col-span-2">
            <RecentActivity :items="data.recent_transactions" />
          </div>
        </div>
      </template>

      <!-- View: Keuangan (penerimaan/penyaluran/saldo + asnaf focus) -->
      <template v-else-if="view === 'keuangan'">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <KpiCard label="Penerimaan" :amount="data.kpis.penerimaan.total" :delta-pct="data.kpis.penerimaan.delta_pct" />
          <KpiCard label="Penyaluran" :amount="data.kpis.penyaluran.total" :delta-pct="data.kpis.penyaluran.delta_pct" />
          <KpiCard label="Saldo Aktif" :amount="data.kpis.saldo.total" :delta-pct="data.kpis.saldo.delta_pct" />
        </div>
        <div>
          <TrendChart :labels="data.trend.labels" :penerimaan="data.trend.penerimaan" :penyaluran="data.trend.penyaluran" />
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <AsnafDonut :items="data.asnaf_distribution" />
          <FundraisingProgress :items="data.fundraising_channels" />
        </div>
      </template>

      <!-- View: Penghimpunan (channels + donor activity focus) -->
      <template v-else-if="view === 'penghimpunan'">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <KpiCard label="Penerimaan Bulan Ini" :amount="data.kpis.penerimaan.total" :delta-pct="data.kpis.penerimaan.delta_pct" />
          <KpiCard label="Donatur Baru" :amount="data.kpis.donatur_baru.total" :delta-pct="data.kpis.donatur_baru.delta_pct" format="count" />
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div>
            <FundraisingProgress :items="data.fundraising_channels" />
          </div>
          <div class="lg:col-span-2">
            <RecentActivity :items="data.recent_transactions" />
          </div>
        </div>
        <div>
          <TrendChart :labels="data.trend.labels" :penerimaan="data.trend.penerimaan" :penyaluran="data.trend.penyaluran" />
        </div>
      </template>

      <!-- View: Ringkas (compact KPI-only) -->
      <template v-else-if="view === 'ringkas'">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <KpiCard label="Penerimaan" :amount="data.kpis.penerimaan.total" :delta-pct="data.kpis.penerimaan.delta_pct" />
          <KpiCard label="Penyaluran" :amount="data.kpis.penyaluran.total" :delta-pct="data.kpis.penyaluran.delta_pct" />
          <KpiCard label="Saldo Aktif" :amount="data.kpis.saldo.total" :delta-pct="data.kpis.saldo.delta_pct" />
          <KpiCard label="Donatur Baru" :amount="data.kpis.donatur_baru.total" :delta-pct="data.kpis.donatur_baru.delta_pct" format="count" />
        </div>
        <p class="text-xs text-muted text-center pt-4">
          Tampilan ringkas — chart dan tabel disembunyikan. Switch ke tab lain untuk detail.
        </p>
      </template>
    </template>
  </div>
</template>

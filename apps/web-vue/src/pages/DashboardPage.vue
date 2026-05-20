<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'

import AsnafDonut from '@/components/widgets/AsnafDonut.vue'
import FundraisingProgress from '@/components/widgets/FundraisingProgress.vue'
import KpiCard from '@/components/widgets/KpiCard.vue'
import RecentActivity from '@/components/widgets/RecentActivity.vue'
import TrendChart from '@/components/widgets/TrendChart.vue'
import Alert from '@/components/ui/Alert.vue'
import { api, ApiError } from '@/lib/api/client'
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
  trend: {
    labels: string[]
    penerimaan: number[]
    penyaluran: number[]
  }
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

const auth = useAuthStore()
const data = ref<DashboardSummary | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)

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
  () => {
    if (auth.activeTenantId) load()
  },
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

    <div v-if="loading" class="flex justify-center p-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary" />
    </div>

    <Alert v-else-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <template v-else-if="data">
      <!-- Row 1: 4 KPI cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          label="Penerimaan"
          :amount="data.kpis.penerimaan.total"
          :delta-pct="data.kpis.penerimaan.delta_pct"
        />
        <KpiCard
          label="Penyaluran"
          :amount="data.kpis.penyaluran.total"
          :delta-pct="data.kpis.penyaluran.delta_pct"
        />
        <KpiCard
          label="Saldo Aktif"
          :amount="data.kpis.saldo.total"
          :delta-pct="data.kpis.saldo.delta_pct"
        />
        <KpiCard
          label="Donatur Baru"
          :amount="data.kpis.donatur_baru.total"
          :delta-pct="data.kpis.donatur_baru.delta_pct"
          format="count"
        />
      </div>

      <!-- Row 2: trend (2 col) + asnaf donut (1 col) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="lg:col-span-2">
          <TrendChart
            :labels="data.trend.labels"
            :penerimaan="data.trend.penerimaan"
            :penyaluran="data.trend.penyaluran"
          />
        </div>
        <div>
          <AsnafDonut :items="data.asnaf_distribution" />
        </div>
      </div>

      <!-- Row 3: channels (1 col) + recent activity (2 col) -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div>
          <FundraisingProgress :items="data.fundraising_channels" />
        </div>
        <div class="lg:col-span-2">
          <RecentActivity :items="data.recent_transactions" />
        </div>
      </div>
    </template>
  </div>
</template>

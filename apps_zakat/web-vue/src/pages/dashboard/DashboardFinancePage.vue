<script setup lang="ts">
import { onMounted, shallowRef, watch } from 'vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import BudgetProgress from '@/components/widgets/BudgetProgressWidget.vue'
import KpiCard from '@/components/widgets/KpiCardWidget.vue'
import RekeningList from '@/components/widgets/RekeningListWidget.vue'
import TrendChart from '@/components/widgets/TrendChartWidget.vue'
import { api } from '@/shared/api/client'
import { useFetch } from '@/shared/composables/useFetch'

interface KpiCardData {
  total: number
  delta_pct: number | null
  format: string
}

interface KpisBundle {
  period: string
  kpis: {
    collection: KpiCardData
    distribution: KpiCardData
    balance: KpiCardData
    authorization_pending: KpiCardData
  }
}

interface TrendPoint {
  label: string
  collection: number
  distribution: number
}

interface TrendBundle {
  trend: TrendPoint[]
}

interface AnggaranItem {
  owner_id: number
  owner_name: string
  budget: number
  realization: number
  pct: number
}

interface AnggaranBundle {
  budget: AnggaranItem[]
}

interface RekeningItem {
  account_no: string
  account_name: string
  account_type: string
  bank_name: string | null
  balance: number
}

interface RekeningBundle {
  account: RekeningItem[]
}

const bulan = shallowRef(new Date().getMonth() + 1)
const tahun = shallowRef(new Date().getFullYear())

// Per-chart fetchers — masing-masing independen.
const kpisQ = useFetch<KpisBundle>(() =>
  api.get<KpisBundle>(
    `/api/dashboard/finance/kpis?month=${bulan.value}&year=${tahun.value}`,
  ),
)
const trendQ = useFetch<TrendBundle>(() =>
  api.get<TrendBundle>(
    `/api/dashboard/finance/trend?month=${bulan.value}&year=${tahun.value}`,
  ),
)
const budgetQ = useFetch<AnggaranBundle>(() =>
  api.get<AnggaranBundle>(`/api/dashboard/finance/budget?year=${tahun.value}`),
)
const accountQ = useFetch<RekeningBundle>(() =>
  api.get<RekeningBundle>('/api/dashboard/finance/account'),
)

function loadAll() {
  // Parallel — kegagalan di satu chart tidak blok chart lain
  void kpisQ.load()
  void trendQ.load()
  void budgetQ.load()
  void accountQ.load()
}

onMounted(loadAll)
watch([bulan, tahun], loadAll)
</script>

<template>
  <div class="space-y-6">
    <!-- Header row: title + period filter -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard Keuangan</h1>
        <p class="text-sm text-muted">
          {{
            kpisQ.data.value?.period
              ? `Periode ${kpisQ.data.value.period}`
              : `Periode ${tahun}-${String(bulan).padStart(2, '0')}`
          }}
        </p>
      </div>
      <PeriodFilter v-model:bulan="bulan" v-model:tahun="tahun" />
    </div>

    <!-- Row 1: 4 KPI cards. Loading/error per group (1 fetch untuk 4 card) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <KpiCard
        label="Penerimaan"
        :amount="kpisQ.data.value?.kpis.collection.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis.collection.delta_pct ?? 0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Penyaluran"
        :amount="kpisQ.data.value?.kpis.distribution.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis.distribution.delta_pct ?? 0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Saldo Kas/Bank"
        :amount="kpisQ.data.value?.kpis.balance.total ?? 0"
        :delta-pct="0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Pending Otorisasi"
        :amount="kpisQ.data.value?.kpis.authorization_pending.total ?? 0"
        :delta-pct="0"
        format="count"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
    </div>

    <!-- Row 2: Trend chart -->
    <TrendChart
      :labels="trendQ.data.value?.trend.map((t) => t.label) ?? []"
      :collection="trendQ.data.value?.trend.map((t) => t.collection) ?? []"
      :distribution="trendQ.data.value?.trend.map((t) => t.distribution) ?? []"
      :loading="trendQ.loading.value"
      :error="!!trendQ.error.value"
      :error-message="trendQ.error.value ?? undefined"
    />

    <!-- Row 3: Budget + Rekening -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <BudgetProgress
        :items="budgetQ.data.value?.budget ?? []"
        :loading="budgetQ.loading.value"
        :error="!!budgetQ.error.value"
        :error-message="budgetQ.error.value ?? undefined"
      />
      <RekeningList
        :items="accountQ.data.value?.account ?? []"
        :loading="accountQ.loading.value"
        :error="!!accountQ.error.value"
        :error-message="accountQ.error.value ?? undefined"
      />
    </div>
  </div>
</template>

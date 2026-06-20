<script setup lang="ts">
import { onMounted, shallowRef, watch } from 'vue'

import AsnafDonut from '@/components/widgets/AsnafDonutWidget.vue'
import BudgetProgress from '@/components/widgets/BudgetProgressWidget.vue'
import KpiCard from '@/components/widgets/KpiCardWidget.vue'
import TrendChart from '@/components/widgets/TrendChartWidget.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import { api } from '@/lib/api/client'
import { useFetch } from '@/lib/useFetch'

interface KpiCardData {
  total: number
  delta_pct: number | null
  format: string
}

interface TrendPoint {
  label: string
  collection: number
  distribution: number
}

interface AnggaranItem {
  owner_id: number
  owner_name: string
  budget: number
  realization: number
  pct: number
}

interface AsnafItem {
  label: string
  count: number
}

const bulan = shallowRef(new Date().getMonth() + 1)
const tahun = shallowRef(new Date().getFullYear())

// Per-chart fetchers — masing-masing independen. Kegagalan/lambatnya satu
// widget tidak menggagalkan widget lain.
const kpisQ = useFetch<{ period: string; kpis: Record<string, KpiCardData> }>(
  () => api.get(`/api/dashboard/finance/kpis?month=${bulan.value}&year=${tahun.value}`),
)
const trendQ = useFetch<{ trend: TrendPoint[] }>(
  () => api.get(`/api/dashboard/finance/trend?month=${bulan.value}&year=${tahun.value}`),
)
const asnafQ = useFetch<{ asnaf: AsnafItem[] }>(
  () => api.get(`/api/dashboard/finance/asnaf?month=${bulan.value}&year=${tahun.value}`),
)
const budgetQ = useFetch<{ budget: AnggaranItem[] }>(
  () => api.get(`/api/dashboard/finance/budget?year=${tahun.value}`),
)

function loadAll() {
  void kpisQ.load()
  void trendQ.load()
  void asnafQ.load()
  void budgetQ.load()
}

onMounted(loadAll)
watch([bulan, tahun], loadAll)
</script>

<template>
  <div class="space-y-6">
    <!-- Header + Period Filter -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard</h1>
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

    <!-- KPI row: 4 cards (1 fetch untuk 4 card) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <KpiCard
        label="Penerimaan"
        :amount="kpisQ.data.value?.kpis?.collection?.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis?.collection?.delta_pct ?? 0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Penyaluran"
        :amount="kpisQ.data.value?.kpis?.distribution?.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis?.distribution?.delta_pct ?? 0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Saldo Kas/Bank"
        :amount="kpisQ.data.value?.kpis?.balance?.total ?? 0"
        :delta-pct="0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Pending Otorisasi"
        :amount="kpisQ.data.value?.kpis?.authorization_pending?.total ?? 0"
        :delta-pct="0"
        format="count"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
    </div>

    <!-- Trend chart full width -->
    <TrendChart
      :labels="trendQ.data.value?.trend?.map((t) => t.label) ?? []"
      :collection="trendQ.data.value?.trend?.map((t) => t.collection) ?? []"
      :distribution="trendQ.data.value?.trend?.map((t) => t.distribution) ?? []"
      :loading="trendQ.loading.value"
      :error="!!trendQ.error.value"
      :error-message="trendQ.error.value ?? undefined"
    />

    <!-- Bottom row: Asnaf donut + Budget progress -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <AsnafDonut
        :items="(asnafQ.data.value?.asnaf ?? []).map((a) => ({ label: a.label, value: a.count }))"
        value-format="count"
        :loading="asnafQ.loading.value"
        :error="!!asnafQ.error.value"
        :error-message="asnafQ.error.value ?? undefined"
      />
      <BudgetProgress
        :items="budgetQ.data.value?.budget ?? []"
        :loading="budgetQ.loading.value"
        :error="!!budgetQ.error.value"
        :error-message="budgetQ.error.value ?? undefined"
      />
    </div>
  </div>
</template>

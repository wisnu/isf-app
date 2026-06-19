<script setup lang="ts">
import { onMounted, shallowRef, watch } from 'vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import BudgetProgress from '@/components/widgets/BudgetProgressWidget.vue'
import KpiCard from '@/components/widgets/KpiCardWidget.vue'
import RekeningList from '@/components/widgets/RekeningListWidget.vue'
import TrendChart from '@/components/widgets/TrendChartWidget.vue'
import { api } from '@/lib/api/client'
import { useFetch } from '@/lib/useFetch'

interface KpiCardData {
  total: number
  delta_pct: number | null
  format: string
}

interface KpisBundle {
  period: string
  kpis: {
    penerimaan: KpiCardData
    penyaluran: KpiCardData
    saldo: KpiCardData
    otorisasi_pending: KpiCardData
  }
}

interface TrendPoint {
  label: string
  penerimaan: number
  penyaluran: number
}

interface TrendBundle {
  trend: TrendPoint[]
}

interface AnggaranItem {
  owner_id: number
  owner_name: string
  anggaran: number
  realisasi: number
  pct: number
}

interface AnggaranBundle {
  anggaran: AnggaranItem[]
}

interface RekeningItem {
  account_no: string
  account_name: string
  account_type: string
  bank_name: string | null
  balance: number
}

interface RekeningBundle {
  rekening: RekeningItem[]
}

const bulan = shallowRef(new Date().getMonth() + 1)
const tahun = shallowRef(new Date().getFullYear())

// Per-chart fetchers — masing-masing independen.
const kpisQ = useFetch<KpisBundle>(() =>
  api.get<KpisBundle>(
    `/api/dashboard/keuangan/kpis?bulan=${bulan.value}&tahun=${tahun.value}`,
  ),
)
const trendQ = useFetch<TrendBundle>(() =>
  api.get<TrendBundle>(
    `/api/dashboard/keuangan/trend?bulan=${bulan.value}&tahun=${tahun.value}`,
  ),
)
const anggaranQ = useFetch<AnggaranBundle>(() =>
  api.get<AnggaranBundle>(`/api/dashboard/keuangan/anggaran?tahun=${tahun.value}`),
)
const rekeningQ = useFetch<RekeningBundle>(() =>
  api.get<RekeningBundle>('/api/dashboard/keuangan/rekening'),
)

function loadAll() {
  // Parallel — kegagalan di satu chart tidak blok chart lain
  void kpisQ.load()
  void trendQ.load()
  void anggaranQ.load()
  void rekeningQ.load()
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
        :amount="kpisQ.data.value?.kpis.penerimaan.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis.penerimaan.delta_pct ?? 0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Penyaluran"
        :amount="kpisQ.data.value?.kpis.penyaluran.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis.penyaluran.delta_pct ?? 0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Saldo Kas/Bank"
        :amount="kpisQ.data.value?.kpis.saldo.total ?? 0"
        :delta-pct="0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Pending Otorisasi"
        :amount="kpisQ.data.value?.kpis.otorisasi_pending.total ?? 0"
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
      :penerimaan="trendQ.data.value?.trend.map((t) => t.penerimaan) ?? []"
      :penyaluran="trendQ.data.value?.trend.map((t) => t.penyaluran) ?? []"
      :loading="trendQ.loading.value"
      :error="!!trendQ.error.value"
      :error-message="trendQ.error.value ?? undefined"
    />

    <!-- Row 3: Budget + Rekening -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <BudgetProgress
        :items="anggaranQ.data.value?.anggaran ?? []"
        :loading="anggaranQ.loading.value"
        :error="!!anggaranQ.error.value"
        :error-message="anggaranQ.error.value ?? undefined"
      />
      <RekeningList
        :items="rekeningQ.data.value?.rekening ?? []"
        :loading="rekeningQ.loading.value"
        :error="!!rekeningQ.error.value"
        :error-message="rekeningQ.error.value ?? undefined"
      />
    </div>
  </div>
</template>

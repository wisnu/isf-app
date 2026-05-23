<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'

import AsnafDonut from '@/components/widgets/AsnafDonut.vue'
import BudgetProgress from '@/components/widgets/BudgetProgress.vue'
import KpiCard from '@/components/widgets/KpiCard.vue'
import TrendChart from '@/components/widgets/TrendChart.vue'
import Alert from '@/components/ui/Alert.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import { api, ApiError } from '@/lib/api/client'

interface KpiCardData {
  total: number
  delta_pct: number | null
  format: string
}

interface TrendPoint {
  label: string
  penerimaan: number
  penyaluran: number
}

interface AnggaranItem {
  owner_id: number
  owner_name: string
  anggaran: number
  realisasi: number
  pct: number
}

interface AsnafItem2 {
  label: string
  count: number
}

interface DashboardKeuangan {
  period: string
  kpis: {
    penerimaan: KpiCardData
    penyaluran: KpiCardData
    saldo: KpiCardData
    otorisasi_pending: KpiCardData
  }
  trend: TrendPoint[]
  asnaf: AsnafItem2[]
  anggaran: AnggaranItem[]
  rekening: any[]
}

const bulan = ref(new Date().getMonth() + 1)
const tahun = ref(new Date().getFullYear())
const data = ref<DashboardKeuangan | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<DashboardKeuangan>(
      `/api/dashboard/keuangan?bulan=${bulan.value}&tahun=${tahun.value}`
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
    data.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch([bulan, tahun], load)
</script>

<template>
  <div class="space-y-6">
    <!-- Header + Period Filter -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard</h1>
        <p v-if="data" class="text-sm text-muted">Periode {{ data.period }}</p>
      </div>
      <PeriodFilter v-model:bulan="bulan" v-model:tahun="tahun" />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex justify-center p-12">
      <Loader2 class="w-8 h-8 animate-spin text-primary" />
    </div>

    <!-- Error -->
    <Alert v-else-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <!-- Content -->
    <template v-else-if="data">
      <!-- KPI row: 4 cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          label="Penerimaan"
          :amount="data.kpis.penerimaan.total"
          :delta-pct="data.kpis.penerimaan.delta_pct ?? 0"
        />
        <KpiCard
          label="Penyaluran"
          :amount="data.kpis.penyaluran.total"
          :delta-pct="data.kpis.penyaluran.delta_pct ?? 0"
        />
        <KpiCard
          label="Saldo Kas/Bank"
          :amount="data.kpis.saldo.total"
          :delta-pct="0"
        />
        <KpiCard
          label="Pending Otorisasi"
          :amount="data.kpis.otorisasi_pending.total"
          :delta-pct="0"
          format="count"
        />
      </div>

      <!-- Trend chart full width -->
      <TrendChart
        :labels="data.trend.map(t => t.label)"
        :penerimaan="data.trend.map(t => t.penerimaan)"
        :penyaluran="data.trend.map(t => t.penyaluran)"
      />

      <!-- Bottom row: Asnaf donut + Budget progress -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <AsnafDonut
          :items="data.asnaf.map(a => ({ label: a.label, value: a.count }))"
          value-format="count"
        />
        <BudgetProgress :items="data.anggaran" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'
import Alert from '@/components/ui/Alert.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import BudgetProgress from '@/components/widgets/BudgetProgress.vue'
import KpiCard from '@/components/widgets/KpiCard.vue'
import RekeningList from '@/components/widgets/RekeningList.vue'
import TrendChart from '@/components/widgets/TrendChart.vue'
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

interface RekeningItem {
  account_no: string
  account_name: string
  account_type: string
  bank_name: string | null
  balance: number
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
  rekening: RekeningItem[]
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
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data keuangan'
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
    <!-- Header row: title + period filter -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard Keuangan</h1>
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
      <!-- Row 1: 4 KPI cards -->
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

      <!-- Row 2: Trend chart (full width) -->
      <TrendChart
        :labels="data.trend.map(t => t.label)"
        :penerimaan="data.trend.map(t => t.penerimaan)"
        :penyaluran="data.trend.map(t => t.penyaluran)"
      />

      <!-- Row 3: Budget progress + Rekening list side by side -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <BudgetProgress :items="data.anggaran" />
        <RekeningList :items="data.rekening" />
      </div>
    </template>
  </div>
</template>

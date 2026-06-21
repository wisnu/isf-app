<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import AsnafDonut from '@/modules/finance/components/widgets/AsnafDonut.vue'
import BudgetProgress from '@/modules/finance/components/widgets/BudgetProgress.vue'
import KpiCard from '@/modules/finance/components/widgets/KpiCard.vue'
import TrendChart from '@/modules/finance/components/widgets/TrendChart.vue'
import PeriodFilter from '@/shared/components/PeriodFilter.vue'
import { api } from '@/shared/api/client'
import { useFetch } from '@/shared/composables/useFetch'
import { useAuthStore } from '@/app/stores/auth.store'

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

interface AsnafItem {
  label: string
  count: number
}

const auth = useAuthStore()
const route = useRoute()

const bulan = ref(new Date().getMonth() + 1)
const tahun = ref(new Date().getFullYear())

const kpisQ = useFetch<{ period: string; kpis: Record<string, KpiCardData> }>(
  () => api.get(`/api/dashboard/keuangan/kpis?bulan=${bulan.value}&tahun=${tahun.value}`),
)
const trendQ = useFetch<{ trend: TrendPoint[] }>(
  () => api.get(`/api/dashboard/keuangan/trend?bulan=${bulan.value}&tahun=${tahun.value}`),
)
const asnafQ = useFetch<{ asnaf: AsnafItem[] }>(
  () => api.get(`/api/dashboard/keuangan/asnaf?bulan=${bulan.value}&tahun=${tahun.value}`),
)
const anggaranQ = useFetch<{ anggaran: AnggaranItem[] }>(
  () => api.get(`/api/dashboard/keuangan/anggaran?tahun=${tahun.value}`),
)

function loadAll() {
  void kpisQ.load()
  void trendQ.load()
  void asnafQ.load()
  void anggaranQ.load()
}

onMounted(() => {
  const denied = route.query.denied
  if (denied) {
    console.warn(`[auth] Akses ke '${denied}' tidak diizinkan.`)
  }
  loadAll()
})
watch([bulan, tahun], loadAll)
</script>

<template>
  <div v-if="auth.user && auth.menus.length === 0" class="p-6 text-center">
    <h2 class="text-xl font-semibold mb-2">Akses belum dikonfigurasi</h2>
    <p class="text-muted">
      Akun Anda belum punya menu yang aktif. Hubungi administrator untuk request akses.
    </p>
  </div>
  <div v-else>
    <div class="space-y-6">
      <!-- Header + Period Filter -->
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold tracking-tight">Dashboard</h1>
          <p v-if="kpisQ.data.value" class="text-sm text-muted">
            Periode {{ kpisQ.data.value.period }}
          </p>
        </div>
        <PeriodFilter v-model:bulan="bulan" v-model:tahun="tahun" />
      </div>

      <!-- KPI row: 4 cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          label="Penerimaan"
          :amount="kpisQ.data.value?.kpis?.penerimaan?.total ?? 0"
          :delta-pct="kpisQ.data.value?.kpis?.penerimaan?.delta_pct ?? 0"
          :loading="kpisQ.loading.value"
          :error="!!kpisQ.error.value"
          :error-message="kpisQ.error.value ?? undefined"
        />
        <KpiCard
          label="Penyaluran"
          :amount="kpisQ.data.value?.kpis?.penyaluran?.total ?? 0"
          :delta-pct="kpisQ.data.value?.kpis?.penyaluran?.delta_pct ?? 0"
          :loading="kpisQ.loading.value"
          :error="!!kpisQ.error.value"
          :error-message="kpisQ.error.value ?? undefined"
        />
        <KpiCard
          label="Saldo Kas/Bank"
          :amount="kpisQ.data.value?.kpis?.saldo?.total ?? 0"
          :delta-pct="0"
          :loading="kpisQ.loading.value"
          :error="!!kpisQ.error.value"
          :error-message="kpisQ.error.value ?? undefined"
        />
        <KpiCard
          label="Pending Otorisasi"
          :amount="kpisQ.data.value?.kpis?.otorisasi_pending?.total ?? 0"
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
        :penerimaan="trendQ.data.value?.trend?.map((t) => t.penerimaan) ?? []"
        :penyaluran="trendQ.data.value?.trend?.map((t) => t.penyaluran) ?? []"
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
          :items="anggaranQ.data.value?.anggaran ?? []"
          :loading="anggaranQ.loading.value"
          :error="!!anggaranQ.error.value"
          :error-message="anggaranQ.error.value ?? undefined"
        />
      </div>
    </div>
  </div>
</template>

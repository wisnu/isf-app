<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import BudgetProgress from '@/modules/finance/components/widgets/BudgetProgress.vue'
import KpiCard from '@/modules/finance/components/widgets/KpiCard.vue'
import MemoList from '@/modules/finance/components/widgets/MemoList.vue'
import PeriodFilter from '@/shared/components/PeriodFilter.vue'
import { api } from '@/shared/api/client'
import { useFetch } from '@/shared/composables/useFetch'

interface KpiCardData {
  total: number
  delta_pct: number | null
  format: string
}

interface AnggaranItem {
  owner_id: number
  owner_name: string
  anggaran: number
  realisasi: number
  pct: number
}

interface MemoItem {
  memo_id: number
  memo_number: string | null
  subject: string | null
  amount: number | null
  memo_type: string
  memo_date: string | null
}

const bulan = ref(new Date().getMonth() + 1)
const tahun = ref(new Date().getFullYear())

const kpisQ = useFetch<{ period: string; kpis: Record<string, KpiCardData> }>(
  () => api.get(`/api/dashboard/penyaluran/kpis?bulan=${bulan.value}&tahun=${tahun.value}`),
)
const anggaranQ = useFetch<{ anggaran: AnggaranItem[] }>(
  () => api.get(`/api/dashboard/penyaluran/anggaran?tahun=${tahun.value}`),
)
const memoQ = useFetch<{ memo_terbaru: MemoItem[] }>(
  () => api.get('/api/finance/dashboard/penyaluran/memo'),
)

function loadAll() {
  void kpisQ.load()
  void anggaranQ.load()
  void memoQ.load()
}

onMounted(loadAll)
watch([bulan, tahun], loadAll)
</script>

<template>
  <div class="space-y-6">
    <!-- Header row: title + period filter -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard Penyaluran</h1>
        <p v-if="kpisQ.data.value" class="text-sm text-muted">
          Periode {{ kpisQ.data.value.period }}
        </p>
      </div>
      <PeriodFilter v-model:bulan="bulan" v-model:tahun="tahun" />
    </div>

    <!-- Row 1: 3 KPI cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <KpiCard
        label="Total Penyaluran"
        :amount="kpisQ.data.value?.kpis?.penyaluran?.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis?.penyaluran?.delta_pct ?? 0"
        :loading="kpisQ.loading.value"
        :error="!!kpisQ.error.value"
        :error-message="kpisQ.error.value ?? undefined"
      />
      <KpiCard
        label="Mustahiq"
        :amount="kpisQ.data.value?.kpis?.mustahiq?.total ?? 0"
        :delta-pct="0"
        format="count"
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

    <!-- Row 2: Budget progress + Memo list side by side -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <BudgetProgress
        :items="anggaranQ.data.value?.anggaran ?? []"
        :loading="anggaranQ.loading.value"
        :error="!!anggaranQ.error.value"
        :error-message="anggaranQ.error.value ?? undefined"
      />
      <MemoList
        :items="memoQ.data.value?.memo_terbaru ?? []"
        :loading="memoQ.loading.value"
        :error="!!memoQ.error.value"
        :error-message="memoQ.error.value ?? undefined"
      />
    </div>
  </div>
</template>

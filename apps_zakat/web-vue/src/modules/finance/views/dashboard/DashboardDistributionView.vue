<script setup lang="ts">
import { onMounted, shallowRef, watch } from 'vue'

import BudgetProgress from '@/modules/finance/components/widgets/BudgetProgressWidget.vue'
import KpiCard from '@/modules/finance/components/widgets/KpiCardWidget.vue'
import MemoList from '@/modules/finance/components/widgets/MemoListWidget.vue'
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
  budget: number
  realization: number
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

const bulan = shallowRef(new Date().getMonth() + 1)
const tahun = shallowRef(new Date().getFullYear())

const kpisQ = useFetch<{ period: string; kpis: Record<string, KpiCardData> }>(
  () => api.get(`/api/dashboard/fund-distribution/kpis?month=${bulan.value}&year=${tahun.value}`),
)
const budgetQ = useFetch<{ budget: AnggaranItem[] }>(
  () => api.get(`/api/dashboard/fund-distribution/budget?year=${tahun.value}`),
)
const memoQ = useFetch<{ recent_memo: MemoItem[] }>(
  () => api.get('/api/dashboard/fund-distribution/memo'),
)

function loadAll() {
  void kpisQ.load()
  void budgetQ.load()
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
        :amount="kpisQ.data.value?.kpis?.distribution?.total ?? 0"
        :delta-pct="kpisQ.data.value?.kpis?.distribution?.delta_pct ?? 0"
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
        :amount="kpisQ.data.value?.kpis?.authorization_pending?.total ?? 0"
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
        :items="budgetQ.data.value?.budget ?? []"
        :loading="budgetQ.loading.value"
        :error="!!budgetQ.error.value"
        :error-message="budgetQ.error.value ?? undefined"
      />
      <MemoList
        :items="memoQ.data.value?.recent_memo ?? []"
        :loading="memoQ.loading.value"
        :error="!!memoQ.error.value"
        :error-message="memoQ.error.value ?? undefined"
      />
    </div>
  </div>
</template>

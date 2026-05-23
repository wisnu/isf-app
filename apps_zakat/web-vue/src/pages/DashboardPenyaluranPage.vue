<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'
import Alert from '@/components/ui/Alert.vue'
import PeriodFilter from '@/components/ui/PeriodFilter.vue'
import BudgetProgress from '@/components/widgets/BudgetProgress.vue'
import KpiCard from '@/components/widgets/KpiCard.vue'
import MemoList from '@/components/widgets/MemoList.vue'
import { api, ApiError } from '@/lib/api/client'

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

interface DashboardPenyaluran {
  period: string
  kpis: {
    penyaluran: KpiCardData
    mustahiq: KpiCardData
    otorisasi_pending: KpiCardData
  }
  anggaran: AnggaranItem[]
  memo_terbaru: MemoItem[]
}

const bulan = ref(new Date().getMonth() + 1)
const tahun = ref(new Date().getFullYear())
const data = ref<DashboardPenyaluran | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<DashboardPenyaluran>(
      `/api/dashboard/penyaluran?bulan=${bulan.value}&tahun=${tahun.value}`
    )
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data penyaluran'
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
        <h1 class="text-2xl font-bold tracking-tight">Dashboard Penyaluran</h1>
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
      <!-- Row 1: 3 KPI cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <KpiCard
          label="Total Penyaluran"
          :amount="data.kpis.penyaluran.total"
          :delta-pct="data.kpis.penyaluran.delta_pct ?? 0"
        />
        <KpiCard
          label="Mustahiq"
          :amount="data.kpis.mustahiq.total"
          :delta-pct="0"
          format="count"
        />
        <KpiCard
          label="Pending Otorisasi"
          :amount="data.kpis.otorisasi_pending.total"
          :delta-pct="0"
          format="count"
        />
      </div>

      <!-- Row 2: Budget progress + Memo list side by side -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <BudgetProgress :items="data.anggaran" />
        <MemoList :items="data.memo_terbaru" />
      </div>
    </template>
  </div>
</template>

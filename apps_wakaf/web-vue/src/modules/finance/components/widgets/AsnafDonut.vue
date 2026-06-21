<script setup lang="ts">
import { AlertTriangle, Loader2 } from 'lucide-vue-next'
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'

import Card from '@/shared/components/Card.vue'
import CardContent from '@/shared/components/CardContent.vue'
import CardDescription from '@/shared/components/CardDescription.vue'
import CardHeader from '@/shared/components/CardHeader.vue'
import CardTitle from '@/shared/components/CardTitle.vue'

interface AsnafItem {
  label: string
  value: number
}

const props = withDefaults(
  defineProps<{
    items: AsnafItem[]
    valueFormat?: 'currency' | 'count'
    loading?: boolean
    error?: boolean
    errorMessage?: string
  }>(),
  { loading: false, error: false },
)

const PALETTE = [
  '#1976d2',
  '#0f766e',
  '#16a34a',
  '#d97706',
  '#9333ea',
  '#db2777',
  '#0891b2',
  '#ca8a04',
]

function formatValue(n: number): string {
  if (props.valueFormat === 'count') {
    return new Intl.NumberFormat('id-ID').format(n)
  }
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(n)
}

const chartData = computed(() => ({
  labels: props.items.map((i) => i.label),
  datasets: [
    {
      data: props.items.map((i) => i.value),
      backgroundColor: PALETTE,
      borderWidth: 0,
      hoverOffset: 6,
    },
  ],
}))

const options = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '62%',
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        color: 'rgba(120, 120, 120, 0.9)',
        boxWidth: 10,
        boxHeight: 10,
        font: { size: 11 },
        usePointStyle: true,
        padding: 8,
      },
    },
    tooltip: {
      callbacks: {
        label: (ctx: { label?: string; parsed: number }) =>
          `${ctx.label}: ${formatValue(ctx.parsed)}`,
      },
    },
  },
}))
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>Distribusi Asnaf</CardTitle>
      <CardDescription>Penyaluran zakat per kategori</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="h-72 flex items-center justify-center" v-if="loading">
        <div class="flex items-center gap-2 text-muted text-sm">
          <Loader2 class="w-4 h-4 animate-spin" />
          Memuat...
        </div>
      </div>
      <div class="h-72 flex items-center justify-center" v-else-if="error">
        <div class="flex flex-col items-center gap-1 text-destructive text-sm max-w-md text-center px-4">
          <AlertTriangle class="w-5 h-5 mb-1" />
          <span class="font-medium">Gagal memuat data asnaf</span>
          <span v-if="errorMessage" class="text-xs text-muted">{{ errorMessage }}</span>
        </div>
      </div>
      <div
        v-else-if="items.length === 0"
        class="h-72 flex items-center justify-center text-sm text-muted italic"
      >
        Tidak ada data periode ini.
      </div>
      <div v-else class="h-72">
        <Doughnut :data="chartData" :options="options" />
      </div>
    </CardContent>
  </Card>
</template>
